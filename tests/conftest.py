import pytest
from utilities.driver_factory import DriverFactory
from utilities.screenshot_helper import ScreenshotHelper
from utilities.email_reporter import EmailReporter
import json
import os
from datetime import datetime

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests: chrome or firefox")
    parser.addoption("--email-config", action="store", default=None,
                     help="Path to email configuration file")

@pytest.fixture(scope="session")
def config():
    with open(os.path.join(os.path.dirname(__file__), "../config/config.json")) as config_file:
        config = json.load(config_file)
    return config

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    driver = DriverFactory.get_driver(browser)
    driver.maximize_window()
    yield driver
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
def test_data():
    with open(os.path.join(os.path.dirname(__file__), "../test_data/test_data.json")) as data_file:
        test_data = json.load(data_file)
    return test_data

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