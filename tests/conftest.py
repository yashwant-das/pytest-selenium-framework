import pytest
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
def driver(config, request):
    """Create and configure WebDriver"""
    # Get browser from command line or config
    browser = request.config.getoption("--browser") or config["browser"]["default"]
    
    # Check if --headless flag was passed
    headless = False
    if hasattr(request.config, 'option') and request.config.option.headless:
        headless = True
    
    # Get browser-specific configuration
    browser_config = config["browser"].get(browser, {})
    
    if browser == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        
        # Add browser-specific arguments
        for arg in browser_config.get("arguments", []):
            options.add_argument(arg)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from webdriver_manager.firefox import GeckoDriverManager
        
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        
        # Add browser-specific arguments
        for arg in browser_config.get("arguments", []):
            options.add_argument(arg)
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif browser == "edge":
        from selenium.webdriver.edge.service import Service as EdgeService
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        
        # Add browser-specific arguments
        for arg in browser_config.get("arguments", []):
            options.add_argument(arg)
        
        # Check if running on Apple Silicon
        is_apple_silicon = platform.system() == "Darwin" and platform.machine() == "arm64"
        
        # Use the appropriate driver version for Apple Silicon
        if is_apple_silicon:
            # For Apple Silicon, we need to use a different approach
            # Instead of trying to download the driver, we'll use the Edge browser directly
            # This is a workaround for the CPU architecture issue
            try:
                # Try to use the Edge browser directly
                driver = webdriver.Edge(options=options)
                logger.info("Successfully initialized Edge browser on Apple Silicon")
            except webdriver.WebDriverException as e:
                logger.error(f"WebDriver error when using Edge browser directly: {e}")
                logger.info("Falling back to Chrome browser...")
                # Fall back to Chrome browser
                options = Options()
                if headless:
                    options.add_argument("--headless")
                
                # Add browser-specific arguments
                for arg in browser_config.get("arguments", []):
                    options.add_argument(arg)
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                logger.info("Successfully initialized Chrome browser as fallback")
            except Exception as e:
                logger.error(f"Unexpected error when using Edge browser directly: {e}")
                logger.info("Falling back to Chrome browser...")
                # Fall back to Chrome browser
                options = Options()
                if headless:
                    options.add_argument("--headless")
                
                # Add browser-specific arguments
                for arg in browser_config.get("arguments", []):
                    options.add_argument(arg)
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                logger.info("Successfully initialized Chrome browser as fallback")
        else:
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set implicit wait
    driver.implicitly_wait(browser_config.get("implicit_wait", config["browser"].get("implicit_wait", 10)))
    
    yield driver
    
    # Cleanup
    driver.quit()

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
                    
                    # Add screenshot to the report
                    if hasattr(report, "extras"):
                        report.extras.append(pytest.html.extras.image(screenshot_path))
                    
                    # Log the screenshot
                    logger.info(f"Screenshot saved for failed test: {screenshot_path}")
                    
                    # Add error message to the screenshot filename if available
                    if hasattr(report, "longrepr") and report.longrepr is not None:
                        error_msg = str(report.longrepr)
                        error_filename = f"failure_{test_name}_{timestamp}_error.txt"
                        error_path = os.path.join("reports", "screenshots", error_filename)
                        with open(error_path, "w") as f:
                            f.write(error_msg)
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
                            
                            # Add screenshot to the report
                            if hasattr(report, "extras"):
                                report.extras.append(pytest.html.extras.image(screenshot_path))
                            
                            # Log the screenshot
                            logger.info(f"Screenshot saved for passed test: {screenshot_path}")
                        
                        except Exception as e:
                            logger.error(f"Failed to take screenshot for passed test: {str(e)}")

@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON files.
    
    This fixture loads all JSON files from the test_data directory and returns a dictionary
    with the merged data from all files.
    
    Returns:
        dict: Dictionary containing merged test data from all JSON files
    """
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")
    test_data = {}
    
    try:
        # Create test_data directory if it doesn't exist
        if not os.path.exists(test_data_dir):
            os.makedirs(test_data_dir)
            logger.info(f"Created test_data directory: {test_data_dir}")
        
        # Load all JSON files from the test_data directory
        for filename in os.listdir(test_data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(test_data_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Merge data into test_data
                        test_data.update(data)
                    logger.info(f"Loaded test data from {file_path}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON file {file_path}: {e}")
                except Exception as e:
                    logger.error(f"Failed to load test data from {file_path}: {e}")
        
        # If no test data was loaded, create a default test data file
        if not test_data:
            default_test_data = {
                "default": {
                    "url": "https://www.example.com",
                    "username": "test_user",
                    "password": "test_password"
                }
            }
            
            default_file_path = os.path.join(test_data_dir, "default.json")
            try:
                with open(default_file_path, 'w') as f:
                    json.dump(default_test_data, f, indent=4)
                test_data.update(default_test_data)
                logger.info(f"Created default test data file: {default_file_path}")
            except Exception as e:
                logger.error(f"Failed to create default test data file: {e}")
    except Exception as e:
        logger.error(f"Failed to load test data: {e}")
    
    return test_data 

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "screenshot_on_pass: mark test to take screenshot on pass"
    ) 