"""Comprehensive test suite showcasing all framework capabilities."""
import pytest
import time
from typing import Dict, Any
from pages.selenium_page import SeleniumPage
from selenium.webdriver.common.by import By


class TestPageObjectModel:
    """Test suite demonstrating Page Object Model pattern."""
    
    def test_page_object_navigation(self, driver, test_data):
        """Demonstrate Page Object Model: Navigate using page object methods."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        assert "Selenium" in page.get_page_title()
        assert page.is_navigation_visible()
        assert page.is_logo_visible()
    
    def test_page_object_element_interaction(self, driver, test_data):
        """Demonstrate Page Object Model: Interact with elements via page object."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        heading = page.get_main_heading()
        assert "Selenium" in heading or "automates" in heading.lower()
        
        nav_items = page.get_navigation_items()
        assert len(nav_items) > 0
        assert any("Downloads" in item or "Documentation" in item for item in nav_items)


class TestCrossBrowser:
    """Test suite demonstrating cross-browser testing capability."""
    
    @pytest.mark.smoke
    def test_chrome_browser(self, driver, request, test_data):
        """Test framework works with Chrome browser."""
        browser = request.config.getoption("--browser", default="chrome")
        if browser != "chrome":
            pytest.skip("This test is for Chrome browser")
        
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        assert "Selenium" in page.get_page_title()
    
    @pytest.mark.smoke
    def test_firefox_browser(self, driver, request, test_data):
        """Test framework works with Firefox browser."""
        browser = request.config.getoption("--browser", default="chrome")
        if browser != "firefox":
            pytest.skip("This test is for Firefox browser")
        
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        assert "Selenium" in page.get_page_title()
    

class TestHeadlessMode:
    """Test suite demonstrating headless mode capability."""
    
    def test_headless_execution(self, driver, request, test_data):
        """Demonstrate headless mode execution."""
        is_headless = request.config.getoption("--headless", default=False)
        
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Verify page loads correctly in headless mode
        assert "Selenium" in page.get_page_title()
        assert page.is_navigation_visible()
        
        if is_headless:
            # Additional verification for headless mode
            assert driver.capabilities.get('browserName') is not None


class TestParallelExecution:
    """Test suite demonstrating parallel execution capability."""
    
    def test_parallel_worker_1(self, driver, test_data):
        """Parallel test worker 1 - demonstrates parallel execution."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        session_id = driver.capabilities.get('sessionId', 'unknown')
        worker_id = driver.capabilities.get('workerId', 'unknown')
        
        # Simulate work
        time.sleep(1)
        
        assert "Selenium" in page.get_page_title()
        print(f"Worker 1 - Session: {session_id}, Worker: {worker_id}")
    
    def test_parallel_worker_2(self, driver, test_data):
        """Parallel test worker 2 - demonstrates parallel execution."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        session_id = driver.capabilities.get('sessionId', 'unknown')
        worker_id = driver.capabilities.get('workerId', 'unknown')
        
        # Simulate work
        time.sleep(1)
        
        assert "Selenium" in page.get_page_title()
        print(f"Worker 2 - Session: {session_id}, Worker: {worker_id}")
    
    def test_parallel_worker_3(self, driver, test_data):
        """Parallel test worker 3 - demonstrates parallel execution."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        session_id = driver.capabilities.get('sessionId', 'unknown')
        worker_id = driver.capabilities.get('workerId', 'unknown')
        
        # Simulate work
        time.sleep(1)
        
        assert "Selenium" in page.get_page_title()
        print(f"Worker 3 - Session: {session_id}, Worker: {worker_id}")
    
    def test_parallel_worker_4(self, driver, test_data):
        """Parallel test worker 4 - demonstrates parallel execution."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        session_id = driver.capabilities.get('sessionId', 'unknown')
        worker_id = driver.capabilities.get('workerId', 'unknown')
        
        # Simulate work
        time.sleep(1)
        
        assert "Selenium" in page.get_page_title()
        print(f"Worker 4 - Session: {session_id}, Worker: {worker_id}")


class TestDataDrivenTesting:
    """Test suite demonstrating data-driven testing capability."""
    
    def test_navigation_items_from_config(self, driver, test_data):
        """Demonstrate data-driven testing using test data configuration."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Get expected navigation items from test data
        expected_nav = test_data["test_data"]["selenium"]["navigation"]
        expected_items = list(expected_nav.values())
        
        # Get actual navigation items from page
        actual_items = page.get_navigation_items()
        
        # Verify expected items are present
        for expected_item in expected_items:
            assert any(expected_item in item for item in actual_items), \
                f"Navigation item '{expected_item}' not found in {actual_items}"
    
    def test_components_from_config(self, driver, test_data):
        """Demonstrate data-driven testing for component verification."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Get expected components from test data
        expected_components = test_data["test_data"]["selenium"]["components"]
        expected_names = list(expected_components.values())
        
        # Get actual components from page
        actual_components = page.get_component_sections()
        
        # Verify components are present
        for component in expected_names:
            assert component in actual_components, \
                f"Component '{component}' not found on page"


class TestNavigationAndInteraction:
    """Test suite demonstrating navigation and element interaction."""
    
    def test_navigate_to_downloads(self, driver, test_data):
        """Demonstrate navigation to different pages."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Navigate to downloads page
        assert page.navigate_to_downloads()
        assert "downloads" in page.get_current_url().lower()
    
    def test_navigate_to_documentation(self, driver, test_data):
        """Demonstrate navigation to documentation page."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Navigate to documentation page
        assert page.navigate_to_documentation()
        assert "documentation" in page.get_current_url().lower()
    
    def test_element_visibility_checks(self, driver, test_data):
        """Demonstrate element visibility checking."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Check various elements are visible
        assert page.is_navigation_visible()
        assert page.is_logo_visible()
    
    def test_javascript_execution(self, driver, test_data):
        """Demonstrate JavaScript execution capability."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Get initial scroll position
        initial_scroll = driver.execute_script("return window.pageYOffset;")
        
        # Scroll to bottom
        page.scroll_to_bottom()
        time.sleep(0.5)
        bottom_scroll = driver.execute_script("return window.pageYOffset;")
        assert bottom_scroll > initial_scroll
        
        # Scroll back to top
        page.scroll_to_top()
        time.sleep(0.5)
        top_scroll = driver.execute_script("return window.pageYOffset;")
        assert top_scroll < bottom_scroll


class TestScreenshotCapabilities:
    """Test suite demonstrating screenshot capabilities."""
    
    @pytest.mark.screenshot_on_pass
    def test_screenshot_on_pass(self, driver, test_data):
        """Demonstrate screenshot capture on test pass."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        assert "Selenium" in page.get_page_title()
    
    @pytest.mark.xfail(reason="Demonstrates screenshot on failure - this test is expected to fail")
    def test_screenshot_on_failure(self, driver, test_data):
        """Demonstrate screenshot capture on test failure.
        
        Note: This test is marked as xfail to demonstrate failure screenshot capability
        without breaking the test suite.
        """
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        # This assertion will fail to demonstrate failure screenshots
        assert False, "Intentional failure to demonstrate screenshot on failure"


class TestFrameworkFeatures:
    """Test suite demonstrating additional framework features."""
    
    def test_implicit_wait(self, driver, test_data):
        """Demonstrate implicit wait functionality."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Implicit wait should allow elements to load
        assert page.is_navigation_visible()
        assert page.is_logo_visible()
    
    def test_explicit_wait(self, driver, test_data):
        """Demonstrate explicit wait functionality."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Explicit wait for main heading
        heading = page.wait_for_element_visible(By.TAG_NAME, "h1")
        assert heading is not None
        assert "Selenium" in heading.text
    
    def test_window_management(self, driver, test_data):
        """Demonstrate window management capabilities."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        
        # Get window size
        size = driver.get_window_size()
        assert size['width'] > 0
        assert size['height'] > 0
        
        # Maximize window
        driver.maximize_window()
        maximized_size = driver.get_window_size()
        assert maximized_size['width'] >= size['width']
        assert maximized_size['height'] >= size['height']
    
    def test_url_navigation(self, driver, test_data):
        """Demonstrate URL navigation and verification."""
        page = SeleniumPage(driver)
        
        # Navigate to homepage
        page.navigate_to_homepage()
        assert "selenium.dev" in page.get_current_url().lower()
        
        # Navigate to downloads
        page.navigate_to_downloads()
        assert "downloads" in page.get_current_url().lower()
        
        # Navigate back
        driver.back()
        assert "selenium.dev" in page.get_current_url().lower() or \
               page.get_current_url() == "https://www.selenium.dev/"

