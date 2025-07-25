import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import json
import platform
from utilities.screenshot_helper import ScreenshotHelper
from utilities.logger import setup_logger
from datetime import datetime
import subprocess
import uuid

# Configure logging
logger = setup_logger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run tests in headless mode")

@pytest.fixture(scope="session")
def config():
    """Load test configuration"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default configuration if file doesn't exist
        return {
            "browser": {
                "default": "chrome",
                "chrome": {
                    "headless": False,
                    "implicit_wait": 10
                }
            }
        }

@pytest.fixture(scope="function")
def driver(request, test_data):
    """Fixture to create and manage WebDriver instances"""
    browser = request.config.getoption("--browser", default="chrome")
    headless = request.config.getoption("--headless", default=False)
    
    # Debug logging to check what flags are being passed
    logger.info(f"Browser: {browser}, Headless: {headless}")
    
    # Get browser-specific configuration
    browser_config = test_data["browser_config"].get(browser, {})
    
    # Create options based on browser type
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")  # Use new headless mode for Chrome >= 109
            logger.info("Chrome running in headless mode with --headless=new")
        else:
            logger.info("Chrome running in normal (non-headless) mode")
        # Collect all preferences into a single dict
        prefs = {}
        for pref in browser_config.get("preferences", {}).items():
            prefs[pref[0]] = pref[1]
        if prefs:
            options.add_experimental_option("prefs", prefs)
        for arg in browser_config.get("arguments", []):
            options.add_argument(arg)
        
        # Log all Chrome options for debugging
        logger.info(f"Chrome options: {options.arguments}")
        
        # Try to use local chromedriver first
        try:
            # Check if chromedriver is in PATH
            subprocess.run(["chromedriver", "--version"], capture_output=True, check=True)
            from selenium.webdriver.chrome.service import Service as ChromeService
            service = ChromeService()
            driver = webdriver.Chrome(service=service, options=options)
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fall back to webdriver-manager if local chromedriver is not available
            try:
                from selenium.webdriver.chrome.service import Service as ChromeService
                
                # Get ChromeDriver path and ensure we have the actual executable
                driver_path = ChromeDriverManager().install()
                if os.path.isdir(driver_path):
                    # If it's a directory, look for chromedriver inside
                    actual_driver_path = os.path.join(driver_path, "chromedriver")
                elif os.path.basename(driver_path) == "chromedriver":
                    # If the filename is exactly "chromedriver"
                    actual_driver_path = driver_path
                else:
                    # The path might be pointing to another file in the driver directory
                    driver_dir = os.path.dirname(driver_path)
                    actual_driver_path = os.path.join(driver_dir, "chromedriver")
                
                # Ensure the driver is executable
                if os.path.exists(actual_driver_path) and not os.access(actual_driver_path, os.X_OK):
                    os.chmod(actual_driver_path, 0o755)
                
                service = ChromeService(actual_driver_path)
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.error(f"Failed to initialize Chrome driver: {str(e)}")
                raise
    
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        for arg in browser_config.get("arguments", []):
            options.add_argument(arg)
        for pref in browser_config.get("preferences", {}).items():
            options.set_preference(pref[0], pref[1])
        
        # Try to use local geckodriver first
        try:
            # Check if geckodriver is in PATH
            subprocess.run(["geckodriver", "--version"], capture_output=True, check=True)
            from selenium.webdriver.firefox.service import Service as FirefoxService
            service = FirefoxService()
            driver = webdriver.Firefox(service=service, options=options)
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fall back to webdriver-manager if local geckodriver is not available
            try:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                logger.error(f"Failed to initialize Firefox driver: {str(e)}")
                raise
    
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        # Collect all preferences into a single dict
        prefs = {}
        for pref in browser_config.get("preferences", {}).items():
            prefs[pref[0]] = pref[1]
        if prefs:
            options.add_experimental_option("prefs", prefs)
        for arg in browser_config.get("arguments", []):
            options.add_argument(arg)
        
        # Try to use local msedgedriver first
        try:
            # Check if msedgedriver is in PATH
            subprocess.run(["msedgedriver", "--version"], capture_output=True, check=True)
            from selenium.webdriver.edge.service import Service as EdgeService
            service = EdgeService()
            driver = webdriver.Edge(service=service, options=options)
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fall back to webdriver-manager if local msedgedriver is not available
            try:
                from selenium.webdriver.edge.service import Service as EdgeService
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                
                # Get EdgeDriver path and ensure we have the actual executable
                driver_path = EdgeChromiumDriverManager().install()
                if os.path.isdir(driver_path):
                    # If it's a directory, look for msedgedriver inside
                    actual_driver_path = os.path.join(driver_path, "msedgedriver")
                elif os.path.basename(driver_path) == "msedgedriver":
                    # If the filename is exactly "msedgedriver"
                    actual_driver_path = driver_path
                else:
                    # The path might be pointing to another file in the driver directory
                    driver_dir = os.path.dirname(driver_path)
                    actual_driver_path = os.path.join(driver_dir, "msedgedriver")
                
                # Ensure the driver is executable
                if os.path.exists(actual_driver_path) and not os.access(actual_driver_path, os.X_OK):
                    os.chmod(actual_driver_path, 0o755)
                
                service = EdgeService(actual_driver_path)
                driver = webdriver.Edge(service=service, options=options)
            except Exception as edge_error:
                logger.error(f"Failed to initialize Edge driver: {edge_error}")
                raise
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set window size
    driver.set_window_size(
        browser_config.get("window_size", {}).get("width", 1920),
        browser_config.get("window_size", {}).get("height", 1080)
    )
    
    # Set implicit wait
    driver.implicitly_wait(browser_config.get("implicit_wait", 10))
    
    # Generate a unique session ID for parallel execution
    session_id = str(uuid.uuid4())
    driver.capabilities['sessionId'] = session_id
    
    # Add worker ID for parallel execution
    if hasattr(request.config, 'slaveinput'):
        worker_id = request.config.slaveinput.get('slaveid', 'unknown')
        driver.capabilities['workerId'] = worker_id
    
    yield driver
    
    # Cleanup
    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Error quitting driver: {str(e)}")

@pytest.fixture(scope="function")
def screenshot_helper(driver):
    return ScreenshotHelper(driver)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the PyTest Plugin to take screenshots when a test fails.
    Also takes screenshots for tests marked with @pytest.mark.screenshot_on_pass.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only take screenshots for call phase (not setup/teardown)
    if report.when == "call":
        # Get the test name and timestamp
        test_name = item.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get the driver from the test
        driver = item.funcargs.get("driver")
        if driver is not None:
            # Take screenshot on failure
            if report.failed:
                try:
                    # Create a more descriptive filename
                    filename = f"failure_{test_name}_{timestamp}.png"
                    screenshot_path = os.path.join("reports", "screenshots", filename)
                    
                    # Take the screenshot
                    driver.save_screenshot(screenshot_path)
                    
                    # Add screenshot to HTML report
                    if hasattr(report, "extras"):
                        report.extras.append(pytest.html.extras.image(screenshot_path))
                    
                    # Add screenshot to Allure report
                    with open(screenshot_path, "rb") as screenshot_file:
                        allure.attach(
                            screenshot_file.read(),
                            name=f"Screenshot - {test_name}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    
                    # Log the screenshot
                    logger.info(f"Screenshot saved for failed test: {screenshot_path}")
                    
                    # Add error message to the screenshot filename if available
                    if hasattr(report, "longrepr") and report.longrepr is not None:
                        error_msg = str(report.longrepr)
                        error_filename = f"failure_{test_name}_{timestamp}_error.txt"
                        error_path = os.path.join("reports", "screenshots", error_filename)
                        with open(error_path, "w") as f:
                            f.write(error_msg)
                        
                        # Attach error log to Allure
                        allure.attach(
                            error_msg,
                            name=f"Error Log - {test_name}",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        
                        logger.info(f"Error details saved: {error_path}")
                
                except Exception as e:
                    logger.error(f"Failed to take screenshot: {str(e)}")
            
            # Take screenshot on pass if marked
            elif report.passed and hasattr(item, "markers"):
                for marker in item.markers:
                    if marker.name == "screenshot_on_pass":
                        try:
                            # Create a more descriptive filename
                            filename = f"pass_{test_name}_{timestamp}.png"
                            screenshot_path = os.path.join("reports", "screenshots", filename)
                            
                            # Take the screenshot
                            driver.save_screenshot(screenshot_path)
                            
                            # Add screenshot to HTML report
                            if hasattr(report, "extras"):
                                report.extras.append(pytest.html.extras.image(screenshot_path))
                            
                            # Add screenshot to Allure report
                            with open(screenshot_path, "rb") as screenshot_file:
                                allure.attach(
                                    screenshot_file.read(),
                                    name=f"Screenshot - {test_name} (Passed)",
                                    attachment_type=allure.attachment_type.PNG
                                )
                            
                            # Log the screenshot
                            logger.info(f"Screenshot saved for passed test: {screenshot_path}")
                        
                        except Exception as e:
                            logger.error(f"Failed to take screenshot for passed test: {str(e)}")

@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON files.
    
    This fixture loads test data from test_data.json and environment configuration
    from default.json separately.
    
    Returns:
        dict: Dictionary containing test data and environment configuration
    """
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")
    result = {
        "test_data": {},
        "env_config": {},
        "browser_config": {}
    }
    
    try:
        # Create test_data directory if it doesn't exist
        if not os.path.exists(test_data_dir):
            os.makedirs(test_data_dir)
            logger.info(f"Created test_data directory: {test_data_dir}")
        
        # Load test data
        test_data_path = os.path.join(test_data_dir, "test_data.json")
        if os.path.exists(test_data_path):
            with open(test_data_path, 'r') as f:
                result["test_data"] = json.load(f)
                logger.info("Loaded test data from test_data.json")
        
        # Load environment configuration
        env_config_path = os.path.join(test_data_dir, "default.json")
        if os.path.exists(env_config_path):
            with open(env_config_path, 'r') as f:
                result["env_config"] = json.load(f)
                logger.info("Loaded environment configuration from default.json")
        
        # Load browser configuration
        browser_config_path = os.path.join(test_data_dir, "browser_config.json")
        if os.path.exists(browser_config_path):
            with open(browser_config_path, 'r') as f:
                result["browser_config"] = json.load(f)
                logger.info("Loaded browser configuration from browser_config.json")
        
        return result
    
    except Exception as e:
        logger.error(f"Error loading test data: {str(e)}")
        return result

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "screenshot_on_pass: mark test to take screenshot on pass"
    )