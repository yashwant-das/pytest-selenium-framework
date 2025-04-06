import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import json
import logging
from utilities.screenshot_helper import ScreenshotHelper
from utilities.email_reporter import EmailReporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests: chrome or firefox")
    parser.addoption("--email-config", action="store", default=None,
                     help="Path to email configuration file")

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
            },
            "test_data": {
                "selenium": {
                    "navigation": {
                        "home": "Home",
                        "downloads": "Downloads",
                        "documentation": "Documentation",
                        "projects": "Projects",
                        "blog": "Blog"
                    },
                    "downloads": {
                        "java": "Java",
                        "python": "Python",
                        "javascript": "JavaScript",
                        "ruby": "Ruby",
                        "csharp": "C#",
                        "php": "PHP"
                    }
                },
                "search": {
                    "valid_term": "Selenium WebDriver",
                    "invalid_term": "xyz123nonexistent",
                    "special_chars": "!@#$%^&*()"
                }
            }
        }

@pytest.fixture(scope="function")
def driver(config):
    """Create and configure WebDriver"""
    browser = config["browser"]["default"]
    browser_config = config["browser"][browser]
    
    if browser == "chrome":
        options = Options()
        if browser_config.get("headless", False):
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set implicit wait
    driver.implicitly_wait(browser_config.get("implicit_wait", 10))
    
    yield driver
    
    # Cleanup
    driver.quit()

@pytest.fixture(scope="function")
def screenshot_helper(driver):
    return ScreenshotHelper(driver)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Add screenshot to report if test fails
    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs["driver"]
            screenshot_helper = ScreenshotHelper(driver)
            screenshot_path = screenshot_helper.take_screenshot(f"failure_{item.name}")
            if hasattr(report, "extras"):
                report.extras.append(pytest.html.extras.image(screenshot_path))
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

@pytest.fixture(scope="session")
def test_data(config):
    """Load test data"""
    test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data", "test_data.json")
    try:
        with open(test_data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to config test data if file doesn't exist
        return config.get("test_data", {})

def pytest_sessionfinish(session, exitstatus):
    """
    Called after all tests have been executed
    """
    # Collect test results
    test_results = {
        "passed": session.testscollected - session.testsfailed,
        "failed": session.testsfailed,
        "total": session.testscollected
    }
    
    # Send email report
    try:
        email_config_path = session.config.getoption("--email-config")
        email_reporter = EmailReporter(email_config_path)
        email_reporter.send_report(test_results)
    except Exception as e:
        print(f"Failed to send email report: {e}") 