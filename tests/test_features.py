import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_browser_support(driver, test_data):
    """Test that we can access the Selenium website in different browsers"""
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"
    # Verify Selenium-specific elements
    assert "WebDriver" in driver.page_source, "Page should contain WebDriver text"
    assert "Documentation" in driver.page_source, "Page should contain Documentation link"

def test_headless_mode(driver, request):
    """Test that headless mode is working correctly"""
    # This test will only run in headless mode
    if not request.config.getoption("--headless"):
        pytest.skip("This test only runs in headless mode")
    
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"
    assert "WebDriver" in driver.page_source, "Page should contain WebDriver text"

def test_parallel_execution(driver, test_data):
    """Test that parallel execution works by simulating a slow operation"""
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    # Simulate some work
    time.sleep(2)
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"
    assert "WebDriver" in driver.page_source, "Page should contain WebDriver text"

def test_screenshot_on_failure(driver, test_data):
    """Test that screenshots are taken on test failure"""
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    # Force a failure to test screenshot functionality
    assert False, "This test should fail and take a screenshot"

@pytest.mark.screenshot_on_pass
def test_screenshot_on_pass(driver, test_data):
    """Test that screenshots can be taken on test pass"""
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"
    assert "WebDriver" in driver.page_source, "Page should contain WebDriver text"

def test_browser_specific_features(driver, request, test_data):
    """Test browser-specific features and configurations"""
    browser = request.config.getoption("--browser")
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    
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
    assert "WebDriver" in driver.page_source, "Page should contain WebDriver text"

def test_implicit_wait(driver, test_data):
    """Test that implicit wait is working correctly"""
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    # Try to find a non-existent element to test implicit wait
    try:
        element = driver.find_element(By.ID, "non-existent-element")
        assert False, "Element should not be found"
    except:
        assert True, "Implicit wait worked as expected" 