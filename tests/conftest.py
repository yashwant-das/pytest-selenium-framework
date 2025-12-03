"""Pytest configuration and fixtures."""
import os
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
        logger.debug(f"Driver session ID: {session_id}, Worker ID: {worker_id}")

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
                    error_msg = str(report.longrepr) if hasattr(report, "longrepr") and report.longrepr else None
                    screenshot_path = screenshot_helper.take_failure_screenshot(test_name, error_msg)

                    # Attach to HTML report
                    if hasattr(report, "extras"):
                        html_extra = screenshot_helper.attach_to_html_report(screenshot_path)
                        if html_extra:
                            report.extras.append(html_extra)

                # Take screenshot on pass if marked
                elif report.passed and hasattr(item, "markers"):
                    for marker in item.markers:
                        if marker.name == "screenshot_on_pass":
                            screenshot_path = screenshot_helper.take_pass_screenshot(test_name)

                            # Attach to HTML report
                            if hasattr(report, "extras"):
                                html_extra = screenshot_helper.attach_to_html_report(screenshot_path)
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
