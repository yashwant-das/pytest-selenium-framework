"""Pytest configuration and fixtures."""
import os
import json
import platform
import sys
import pytest
import uuid
from selenium import webdriver
from typing import Dict, Any, Generator

from utilities.config_manager import ConfigManager
from utilities.driver_factory import DriverFactory
from utilities.logger import setup_logger
from utilities.screenshot_helper import ScreenshotHelper

# Configure logging
logger = setup_logger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom pytest command line options."""
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run tests in headless mode")


@pytest.fixture(scope="session")
def config() -> Dict[str, Any]:
    """Load main framework configuration using ConfigManager.

    Returns:
        dict: Main configuration from config.json
    """
    return ConfigManager().get_config()


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest, test_data: Dict[str, Any]) -> Generator[webdriver.Remote, None, None]:
    """Fixture to create and manage WebDriver instances.

    Args:
        request: Pytest request object
        test_data: Test data fixture

    Yields:
        WebDriver instance
    """
    browser = request.config.getoption("--browser", default="chrome")
    headless = request.config.getoption("--headless", default=False)

    logger.info(f"Browser: {browser}, Headless: {headless}")

    # Get browser-specific configuration
    browser_config = test_data["browser_config"].get(browser, {})

    # Create driver using factory
    driver = DriverFactory.create_driver(browser, headless, browser_config)

    # Generate a unique session ID for parallel execution
    session_id = str(uuid.uuid4())

    # Add session and worker IDs to capabilities for parallel execution tracking
    # Use workerinput (pytest-xdist) or gw0 for main process
    if hasattr(request.config, 'workerinput'):
        # pytest-xdist worker process
        worker_id = request.config.workerinput.get('workerid', 'unknown')
    else:
        # Main process (not parallel)
        worker_id = 'main'

    # Safely add metadata to capabilities if it's a dict
    if isinstance(driver.capabilities, dict):
        driver.capabilities['sessionId'] = session_id
        driver.capabilities['workerId'] = worker_id
        logger.debug(
            f"Driver session ID: {session_id}, Worker ID: {worker_id}")

    yield driver

    # Cleanup: Quit driver and handle any errors gracefully
    try:
        if driver:
            driver.quit()
            logger.debug("Driver quit successfully")
    except Exception as e:
        logger.warning(f"Error quitting driver (may already be closed): {e}")


@pytest.fixture(scope="function")
def screenshot_helper(driver: webdriver.Remote) -> ScreenshotHelper:
    """Provide ScreenshotHelper instance for taking and managing screenshots.

    Args:
        driver: WebDriver instance

    Returns:
        ScreenshotHelper instance configured for the current driver
    """
    return ScreenshotHelper(driver)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Extends PyTest to take screenshots when tests fail or pass (if marked)."""
    outcome = yield
    report = outcome.get_result()

    # Only take screenshots for call phase (not setup/teardown)
    if report.when == "call":
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshot_helper = ScreenshotHelper(driver)
            test_name = item.name

            try:
                # Take screenshot on failure
                if report.failed:
                    error_msg = str(report.longrepr) if hasattr(
                        report, "longrepr") and report.longrepr else None
                    screenshot_path = screenshot_helper.take_failure_screenshot(
                        test_name, error_msg)

                    # Attach to HTML report
                    if hasattr(report, "extras"):
                        html_extra = screenshot_helper.attach_to_html_report(
                            screenshot_path)
                        if html_extra:
                            report.extras.append(html_extra)

                # Take screenshot on pass if marked
                elif report.passed and hasattr(item, "markers"):
                    for marker in item.markers:
                        if marker.name == "screenshot_on_pass":
                            screenshot_path = screenshot_helper.take_pass_screenshot(
                                test_name)

                            # Attach to HTML report
                            if hasattr(report, "extras"):
                                html_extra = screenshot_helper.attach_to_html_report(
                                    screenshot_path)
                                if html_extra:
                                    report.extras.append(html_extra)
                            break
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")


@pytest.fixture(scope="session")
def test_data() -> Dict[str, Any]:
    """Load all test data and configurations using ConfigManager.

    Returns:
        dict: Dictionary containing:
            - test_data: Test data from fixtures.json
            - env_config: Environment configurations
            - browser_config: Browser-specific configurations
    """
    return ConfigManager().get_all_configs()


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers and setup required directories."""
    # Register custom markers
    config.addinivalue_line(
        "markers",
        "screenshot_on_pass: mark test to take screenshot on pass"
    )

    # Ensure required directories exist
    directories = [
        'logs',
        'reports',
        'reports/html',
        'reports/screenshots',
        'reports/allure-results'
    ]

    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
        except OSError as e:
            logger.warning(f"Could not create directory {directory}: {e}")

    # Create Allure environment.properties and executor.json
    _create_allure_environment_files()


def _create_allure_environment_files() -> None:
    """Create Allure environment.properties and executor.json files.

    This populates the Environment and Executors sections in Allure reports.
    """
    allure_results_dir = 'reports/allure-results'

    try:
        # Get configuration
        config_manager = ConfigManager()
        env_config = config_manager.get_env_config()
        browser_config = config_manager.get_config().get('browser', {})
        default_browser = browser_config.get('default', 'chrome').title()

        # Get system information
        python_version = sys.version.split()[0]
        os_name = platform.system()
        os_version = platform.release()
        os_arch = platform.machine()

        # Get browser version if available
        browser_version = "N/A"
        try:
            import subprocess
            if default_browser.lower() == 'chrome':
                # Try different Chrome executable paths based on OS
                chrome_paths = []
                if os_name == 'Darwin':  # macOS
                    chrome_paths = [
                        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                        'google-chrome'
                    ]
                elif os_name == 'Linux':
                    chrome_paths = ['google-chrome',
                                    'chromium-browser', 'chromium']
                elif os_name == 'Windows':
                    chrome_paths = [
                        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
                    ]

                for chrome_path in chrome_paths:
                    try:
                        result = subprocess.run([chrome_path, '--version'],
                                                capture_output=True, text=True, timeout=2)
                        if result.returncode == 0:
                            browser_version = result.stdout.strip().split()[-1]
                            break
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        continue
        except Exception:
            pass

        # Write environment.properties
        env_file = os.path.join(allure_results_dir, 'environment.properties')
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(f"Browser={default_browser}\n")
            if browser_version != "N/A":
                f.write(f"Browser.Version={browser_version}\n")
            f.write(f"Python.Version={python_version}\n")
            f.write(f"OS={os_name}\n")
            f.write(f"OS.Version={os_version}\n")
            f.write(f"OS.Architecture={os_arch}\n")
            f.write(f"Framework=pytest-selenium-framework\n")
            f.write(f"Framework.Version=0.1.0\n")
            f.write(f"Environment=Default\n")
            f.write(f"Test.URL={env_config.get('url', 'N/A')}\n")
            f.write(f"Headless.Mode={browser_config.get('headless', False)}\n")

        logger.debug(f"Created Allure environment.properties: {env_file}")

        # Write executor.json
        executor_file = os.path.join(allure_results_dir, 'executor.json')
        executor_data = {
            "name": "Local Machine",
            "type": "local",
            "buildName": "pytest-selenium-framework",
            "buildOrder": 1,
            "reportName": "Test Execution Report",
            "reportUrl": ""
        }
        with open(executor_file, 'w', encoding='utf-8') as f:
            json.dump(executor_data, f, indent=2)

        logger.debug(f"Created Allure executor.json: {executor_file}")

        # Copy history from previous report if it exists (for Trend section)
        previous_report_dir = 'reports/allure-report'
        history_source = os.path.join(previous_report_dir, 'history')
        history_dest = os.path.join(allure_results_dir, 'history')

        if os.path.exists(history_source):
            try:
                import shutil
                if os.path.exists(history_dest):
                    shutil.rmtree(history_dest)
                shutil.copytree(history_source, history_dest)
                logger.debug(
                    f"Copied history from previous report for Trend section")
            except Exception as e:
                logger.warning(f"Could not copy history directory: {e}")

    except Exception as e:
        logger.warning(f"Could not create Allure environment files: {e}")
