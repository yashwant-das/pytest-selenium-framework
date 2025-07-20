"""
WebDriver Support Test Suite

This module contains comprehensive tests for WebDriver functionality,
browser capabilities, and framework integration features.
"""

import pytest
import time
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    ElementClickInterceptedException
)


class TestWebDriverCapabilities:
    """Test WebDriver basic capabilities and functionality"""
    
    def test_driver_initialization(self, driver):
        """Test that WebDriver initializes correctly"""
        assert driver is not None, "Driver should be initialized"
        assert driver.session_id is not None, "Driver should have a valid session ID"
        
    def test_browser_name_detection(self, driver):
        """Test that we can detect the browser name"""
        capabilities = driver.capabilities
        browser_name = capabilities.get('browserName', '').lower()
        assert browser_name in ['chrome', 'firefox', 'microsoftedge'], f"Unsupported browser: {browser_name}"
        
    def test_browser_version_detection(self, driver):
        """Test that we can detect the browser version"""
        capabilities = driver.capabilities
        browser_version = capabilities.get('browserVersion') or capabilities.get('version')
        assert browser_version is not None, "Browser version should be detectable"
        assert len(browser_version) > 0, "Browser version should not be empty"
        
    def test_platform_detection(self, driver):
        """Test that we can detect the platform"""
        capabilities = driver.capabilities
        platform_name = capabilities.get('platformName', '').lower()
        current_platform = platform.system().lower()
        
        # Map platform names
        platform_mapping = {
            'darwin': ['mac', 'macos'],
            'windows': ['windows', 'win32'],
            'linux': ['linux']
        }
        
        expected_platforms = platform_mapping.get(current_platform, [current_platform])
        assert any(exp in platform_name for exp in expected_platforms), \
            f"Platform detection mismatch: detected={platform_name}, expected={expected_platforms}"


class TestNavigationCapabilities:
    """Test WebDriver navigation capabilities"""
    
    def test_page_navigation(self, driver, test_data):
        """Test basic page navigation"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        assert driver.current_url.startswith("https://"), "Should navigate to HTTPS URL"
        
    def test_page_title_access(self, driver, test_data):
        """Test page title access"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        title = driver.title
        assert len(title) > 0, "Page should have a title"
        assert "Selenium" in title, "Title should contain Selenium"
        
    def test_page_source_access(self, driver, test_data):
        """Test page source access"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        source = driver.page_source
        assert len(source) > 0, "Page source should not be empty"
        assert "<html" in source.lower(), "Page source should contain HTML"
        
    def test_back_forward_navigation(self, driver, test_data):
        """Test browser back and forward navigation"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Navigate to documentation link if available
        try:
            doc_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Documentation"))
            )
            doc_link.click()
            time.sleep(2)
            
            # Test back navigation
            driver.back()
            time.sleep(1)
            assert "Selenium" in driver.title, "Should return to main page"
            
            # Test forward navigation
            driver.forward()
            time.sleep(1)
            # Should be on documentation page or similar
            
        except TimeoutException:
            pytest.skip("Documentation link not found for navigation test")


class TestElementInteraction:
    """Test WebDriver element interaction capabilities"""
    
    def test_element_finding_by_tag(self, driver, test_data):
        """Test finding elements by tag name"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Find common HTML elements
        body = driver.find_element(By.TAG_NAME, "body")
        assert body is not None, "Should find body element"
        
        headers = driver.find_elements(By.TAG_NAME, "h1")
        assert len(headers) >= 0, "Should find h1 elements (or empty list)"
        
    def test_element_finding_by_class(self, driver, test_data):
        """Test finding elements by class name"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        try:
            # Try to find elements with common class names
            elements = driver.find_elements(By.CLASS_NAME, "nav")
            # Just verify the method works, elements may or may not exist
            assert isinstance(elements, list), "Should return a list of elements"
        except NoSuchElementException:
            # This is acceptable as the class might not exist
            pass
            
    def test_element_text_access(self, driver, test_data):
        """Test accessing element text content"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Get page title element
        try:
            title_element = driver.find_element(By.TAG_NAME, "h1")
            text = title_element.text
            assert len(text) > 0, "Title element should have text content"
        except NoSuchElementException:
            # Try alternative selectors
            try:
                title_element = driver.find_element(By.TAG_NAME, "title")
                # Title tag text is accessed differently
                text = driver.title
                assert len(text) > 0, "Page should have title text"
            except NoSuchElementException:
                pytest.skip("No suitable title element found for text test")
                
    def test_link_interaction(self, driver, test_data):
        """Test clicking on links"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        try:
            # Find and click a link
            links = driver.find_elements(By.TAG_NAME, "a")
            clickable_links = [link for link in links if link.is_enabled() and link.is_displayed()]
            
            if clickable_links:
                original_url = driver.current_url
                first_link = clickable_links[0]
                href = first_link.get_attribute("href")
                
                if href and not href.startswith("javascript:") and not href.startswith("#"):
                    first_link.click()
                    time.sleep(2)
                    
                    # Verify navigation occurred or page changed
                    new_url = driver.current_url
                    # URL might change or page content might change
                    assert True, "Link click executed successfully"
                else:
                    pytest.skip("No suitable external links found for interaction test")
            else:
                pytest.skip("No clickable links found on the page")
                
        except (ElementClickInterceptedException, TimeoutException):
            pytest.skip("Link interaction not possible due to page layout")


class TestWaitingMechanisms:
    """Test WebDriver waiting mechanisms and timeouts"""
    
    def test_implicit_wait_setting(self, driver):
        """Test setting implicit wait timeout"""
        driver.implicitly_wait(5)
        # Verify timeout is set (no direct way to check, but should not raise exception)
        assert True, "Implicit wait should be settable"
        
    def test_explicit_wait_functionality(self, driver, test_data):
        """Test explicit wait with WebDriverWait"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        # Wait for body element to be present
        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert body is not None, "Explicit wait should find body element"
        
    def test_element_to_be_clickable_wait(self, driver, test_data):
        """Test waiting for element to be clickable"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        try:
            # Wait for any link to be clickable
            clickable_element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
            assert clickable_element is not None, "Should find clickable element"
        except TimeoutException:
            pytest.skip("No clickable elements found within timeout")


class TestJavaScriptExecution:
    """Test WebDriver JavaScript execution capabilities"""
    
    def test_execute_simple_javascript(self, driver, test_data):
        """Test executing simple JavaScript"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Execute simple JavaScript
        result = driver.execute_script("return document.title;")
        assert result == driver.title, "JavaScript should return page title"
        
    def test_execute_javascript_with_arguments(self, driver, test_data):
        """Test executing JavaScript with arguments"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Execute JavaScript with arguments
        result = driver.execute_script("return arguments[0] + arguments[1];", 10, 20)
        assert result == 30, "JavaScript should calculate sum correctly"
        
    def test_javascript_element_interaction(self, driver, test_data):
        """Test JavaScript element interaction"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Scroll to bottom using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Get scroll position
        scroll_y = driver.execute_script("return window.pageYOffset;")
        assert scroll_y >= 0, "Should be able to scroll and get position"


class TestWindowManagement:
    """Test WebDriver window and tab management"""
    
    def test_window_size_management(self, driver):
        """Test window size operations"""
        # Get current window size
        size = driver.get_window_size()
        assert 'width' in size and 'height' in size, "Should return window size"
        assert size['width'] > 0 and size['height'] > 0, "Window should have positive dimensions"
        
        # Set window size
        driver.set_window_size(1024, 768)
        new_size = driver.get_window_size()
        # Allow some tolerance for browser chrome
        assert abs(new_size['width'] - 1024) <= 50, "Window width should be approximately correct"
        assert abs(new_size['height'] - 768) <= 100, "Window height should be approximately correct"
        
    def test_window_position_management(self, driver):
        """Test window position operations"""
        # Get current position
        position = driver.get_window_position()
        assert 'x' in position and 'y' in position, "Should return window position"
        
        # Set window position
        driver.set_window_position(100, 100)
        new_position = driver.get_window_position()
        # Allow some tolerance for OS differences
        assert abs(new_position['x'] - 100) <= 50, "Window X position should be approximately correct"
        assert abs(new_position['y'] - 100) <= 50, "Window Y position should be approximately correct"
        
    def test_window_maximize(self, driver):
        """Test window maximize functionality"""
        original_size = driver.get_window_size()
        driver.maximize_window()
        maximized_size = driver.get_window_size()
        
        # Window should be larger after maximizing (unless already maximized)
        assert maximized_size['width'] >= original_size['width'], "Maximized width should be >= original"
        assert maximized_size['height'] >= original_size['height'], "Maximized height should be >= original"


class TestCookieManagement:
    """Test WebDriver cookie management capabilities"""
    
    def test_cookie_operations(self, driver, test_data):
        """Test cookie add, get, and delete operations"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Add a cookie
        cookie_name = "test_cookie"
        cookie_value = "test_value"
        driver.add_cookie({"name": cookie_name, "value": cookie_value})
        
        # Get the cookie
        cookie = driver.get_cookie(cookie_name)
        assert cookie is not None, "Should retrieve added cookie"
        assert cookie["value"] == cookie_value, "Cookie value should match"
        
        # Get all cookies
        all_cookies = driver.get_cookies()
        assert isinstance(all_cookies, list), "Should return list of cookies"
        
        # Delete the cookie
        driver.delete_cookie(cookie_name)
        deleted_cookie = driver.get_cookie(cookie_name)
        assert deleted_cookie is None, "Cookie should be deleted"


class TestScreenshotCapabilities:
    """Test WebDriver screenshot capabilities"""
    
    def test_page_screenshot(self, driver, test_data):
        """Test taking full page screenshot"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        # Take screenshot
        screenshot = driver.get_screenshot_as_png()
        assert screenshot is not None, "Should capture screenshot"
        assert len(screenshot) > 0, "Screenshot should have content"
        
    def test_element_screenshot(self, driver, test_data):
        """Test taking element-specific screenshot"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        try:
            # Find body element and take screenshot
            body = driver.find_element(By.TAG_NAME, "body")
            element_screenshot = body.screenshot_as_png
            assert element_screenshot is not None, "Should capture element screenshot"
            assert len(element_screenshot) > 0, "Element screenshot should have content"
        except Exception:
            # Some drivers might not support element screenshots
            pytest.skip("Element screenshot not supported by current driver")


class TestBrowserSpecificFeatures:
    """Test browser-specific WebDriver features"""
    
    def test_browser_capabilities(self, driver):
        """Test accessing browser-specific capabilities"""
        capabilities = driver.capabilities
        
        # Common capabilities that should be present
        assert 'browserName' in capabilities, "Should have browser name"
        assert 'platformName' in capabilities or 'platform' in capabilities, "Should have platform info"
        
        browser_name = capabilities.get('browserName', '').lower()
        
        if browser_name == 'chrome':
            assert 'chrome' in capabilities, "Chrome should have chrome-specific capabilities"
        elif browser_name == 'firefox':
            assert 'moz:firefoxOptions' in capabilities or 'firefox_profile' in capabilities, \
                "Firefox should have Firefox-specific capabilities"
        elif browser_name == 'microsoftedge':
            assert 'ms:edgeOptions' in capabilities or 'edgeOptions' in capabilities, \
                "Edge should have Edge-specific capabilities"
                
    def test_user_agent_access(self, driver, test_data):
        """Test accessing browser user agent"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        user_agent = driver.execute_script("return navigator.userAgent;")
        assert user_agent is not None, "Should get user agent string"
        assert len(user_agent) > 0, "User agent should not be empty"
        
        # Verify user agent contains browser information
        browser_name = driver.capabilities.get('browserName', '').lower()
        if browser_name == 'chrome':
            assert 'chrome' in user_agent.lower(), "Chrome user agent should contain 'chrome'"
        elif browser_name == 'firefox':
            assert 'firefox' in user_agent.lower(), "Firefox user agent should contain 'firefox'"
        elif browser_name == 'microsoftedge':
            assert 'edg' in user_agent.lower(), "Edge user agent should contain 'edg'"


class TestErrorHandling:
    """Test WebDriver error handling capabilities"""
    
    def test_no_such_element_exception(self, driver, test_data):
        """Test NoSuchElementException handling"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        with pytest.raises(NoSuchElementException):
            driver.find_element(By.ID, "non_existent_element_id_12345")
            
    def test_timeout_exception_handling(self, driver, test_data):
        """Test TimeoutException handling with WebDriverWait"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        wait = WebDriverWait(driver, 1)  # Very short timeout
        with pytest.raises(TimeoutException):
            wait.until(EC.presence_of_element_located((By.ID, "non_existent_element_id_12345")))
            
    def test_invalid_selector_handling(self, driver, test_data):
        """Test handling of invalid CSS selectors"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        with pytest.raises(Exception):  # Could be various exception types
            driver.find_element(By.CSS_SELECTOR, "invalid[[[selector")


@pytest.mark.performance
class TestPerformanceCapabilities:
    """Test WebDriver performance-related capabilities"""
    
    def test_page_load_timing(self, driver, test_data):
        """Test measuring page load performance"""
        url = test_data["env_config"]["default"]["url"]
        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        
        assert load_time > 0, "Page load should take some time"
        assert load_time < 30, "Page load should complete within 30 seconds"
        
    def test_element_finding_performance(self, driver, test_data):
        """Test element finding performance"""
        url = test_data["env_config"]["default"]["url"]
        driver.get(url)
        
        start_time = time.time()
        body = driver.find_element(By.TAG_NAME, "body")
        find_time = time.time() - start_time
        
        assert body is not None, "Should find body element"
        assert find_time < 5, "Element finding should be fast"


class TestFrameworkIntegration:
    """Test framework-specific WebDriver integration"""
    
    def test_pytest_fixture_integration(self, driver):
        """Test that WebDriver integrates properly with pytest fixtures"""
        assert driver is not None, "Driver fixture should be available"
        assert hasattr(driver, 'get'), "Driver should have get method"
        assert hasattr(driver, 'quit'), "Driver should have quit method"
        
    def test_test_data_integration(self, test_data):
        """Test that test data is properly loaded and accessible"""
        assert test_data is not None, "Test data should be available"
        assert 'env_config' in test_data, "Test data should contain env_config"
        assert 'default' in test_data['env_config'], "Test data should contain default environment"
        
    def test_configuration_integration(self, config):
        """Test that configuration is properly loaded"""
        assert config is not None, "Configuration should be available"
        assert 'browser' in config, "Configuration should contain browser settings"
        
    def test_logging_integration(self, driver, test_data):
        """Test that logging works during WebDriver operations"""
        url = test_data["env_config"]["default"]["url"]
        # This test implicitly checks that logging doesn't interfere with WebDriver
        driver.get(url)
        title = driver.title
        assert len(title) > 0, "Should successfully get page title with logging active"
