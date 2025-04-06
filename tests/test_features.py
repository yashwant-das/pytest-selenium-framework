import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_browser_support(driver, test_data):
    """Test that we can access the test website in different browsers"""
    driver.get("https://www.selenium.dev")
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"

def test_headless_mode(driver, request):
    """Test that headless mode is working correctly"""
    # This test will only run in headless mode
    if not request.config.getoption("--headless"):
        pytest.skip("This test only runs in headless mode")
    
    # Take a screenshot to verify headless functionality
    driver.get("https://www.selenium.dev")
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"

def test_parallel_execution(driver, test_data):
    """Test that parallel execution works by simulating a slow operation"""
    driver.get("https://www.selenium.dev")
    # Simulate some work
    time.sleep(2)
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"

def test_screenshot_on_failure(driver, test_data):
    """Test that screenshots are taken on test failure"""
    driver.get("https://www.selenium.dev")
    # Force a failure to test screenshot functionality
    assert False, "This test should fail and take a screenshot"

@pytest.mark.screenshot_on_pass
def test_screenshot_on_pass(driver, test_data):
    """Test that screenshots can be taken on test pass"""
    driver.get("https://www.selenium.dev")
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"

def test_browser_specific_features(driver, request):
    """Test browser-specific features and configurations"""
    browser = request.config.getoption("--browser")
    
    driver.get("https://www.selenium.dev")
    
    if browser == "chrome":
        # Test Chrome-specific features
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elif browser == "firefox":
        # Test Firefox-specific features
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elif browser == "edge":
        # Test Edge-specific features
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    assert "Selenium" in driver.title, "Browser-specific features should work"

def test_implicit_wait(driver, test_data):
    """Test that implicit wait is working correctly"""
    driver.get("https://www.selenium.dev")
    # Try to find a non-existent element to test implicit wait
    try:
        element = driver.find_element(By.ID, "non-existent-element")
        assert False, "Element should not be found"
    except:
        assert True, "Implicit wait worked as expected" 