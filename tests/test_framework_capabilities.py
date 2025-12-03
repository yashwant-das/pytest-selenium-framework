"""Comprehensive test suite showcasing all framework capabilities.

This test suite demonstrates all features of the pytest-selenium framework:
- Page Object Model pattern
- Cross-browser testing
- Headless mode
- Parallel execution
- Data-driven testing
- Navigation and interaction
- Screenshot capabilities
- Framework features (waits, window management, etc.)
"""
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Dict, Any

from pages.selenium_page import SeleniumPage


class TestPageObjectModel:
    """Test suite demonstrating Page Object Model pattern."""

    def test_page_object_navigation(self, driver: webdriver.Remote):
        """Demonstrate Page Object Model: Navigate using page object methods."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        assert "Selenium" in page.get_page_title(), "Page title should contain 'Selenium'"
        assert page.is_navigation_visible(), "Navigation should be visible"
        assert page.is_logo_visible(), "Logo should be visible"

    def test_page_object_element_interaction(self, driver: webdriver.Remote):
        """Demonstrate Page Object Model: Interact with elements via page object."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        heading = page.get_main_heading()
        assert "Selenium" in heading or "automates" in heading.lower(), \
            f"Main heading should contain 'Selenium' or 'automates', got: {heading}"

        nav_items = page.get_navigation_items()
        assert len(nav_items) > 0, "Navigation items should be present"
        assert any("Downloads" in item or "Documentation" in item for item in nav_items), \
            f"Navigation should contain 'Downloads' or 'Documentation', got: {nav_items}"


class TestCrossBrowser:
    """Test suite demonstrating cross-browser testing capability."""

    @pytest.mark.smoke
    @pytest.mark.browser_chrome
    def test_chrome_browser(self, driver: webdriver.Remote):
        """Test framework works with Chrome browser."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        assert "Selenium" in page.get_page_title(), "Chrome should load Selenium page correctly"

    @pytest.mark.smoke
    @pytest.mark.browser_firefox
    def test_firefox_browser(self, driver: webdriver.Remote):
        """Test framework works with Firefox browser."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        assert "Selenium" in page.get_page_title(), "Firefox should load Selenium page correctly"


class TestHeadlessMode:
    """Test suite demonstrating headless mode capability."""

    @pytest.mark.headless
    def test_headless_execution(self, driver: webdriver.Remote, request: pytest.FixtureRequest):
        """Demonstrate headless mode execution."""
        is_headless = request.config.getoption("--headless", default=False)

        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Verify page loads correctly in headless mode
        assert "Selenium" in page.get_page_title(), "Page should load in headless mode"
        assert page.is_navigation_visible(), "Navigation should be visible in headless mode"

        if is_headless:
            # Additional verification for headless mode
            browser_name = driver.capabilities.get('browserName')
            assert browser_name is not None, "Browser name should be available in capabilities"


class TestParallelExecution:
    """Test suite demonstrating parallel execution capability."""

    @pytest.mark.parallel
    @pytest.mark.parametrize("worker_num", [1, 2, 3, 4])
    def test_parallel_worker(self, driver: webdriver.Remote, worker_num: int):
        """Parallel test worker - demonstrates parallel execution.
        
        Args:
            worker_num: Worker number for identification
        """
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        session_id = driver.capabilities.get('sessionId', 'unknown')
        worker_id = driver.capabilities.get('workerId', 'unknown')

        # Simulate work to demonstrate parallel execution
        time.sleep(0.5)

        assert "Selenium" in page.get_page_title(), \
            f"Worker {worker_num} should load page correctly"
        print(f"Worker {worker_num} - Session: {session_id}, Worker: {worker_id}")


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

    def test_navigate_to_downloads(self, driver: webdriver.Remote):
        """Demonstrate navigation to different pages."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Navigate to downloads page
        page.navigate_to_downloads()
        current_url = page.get_current_url().lower()
        assert "downloads" in current_url, f"Should navigate to downloads page, got: {current_url}"

    def test_navigate_to_documentation(self, driver: webdriver.Remote):
        """Demonstrate navigation to documentation page."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Navigate to documentation page
        page.navigate_to_documentation()
        current_url = page.get_current_url().lower()
        assert "documentation" in current_url, f"Should navigate to documentation page, got: {current_url}"

    def test_element_visibility_checks(self, driver: webdriver.Remote):
        """Demonstrate element visibility checking."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Check various elements are visible
        assert page.is_navigation_visible(), "Navigation should be visible"
        assert page.is_logo_visible(), "Logo should be visible"

    def test_javascript_execution(self, driver: webdriver.Remote):
        """Demonstrate JavaScript execution capability."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Get initial scroll position
        initial_scroll = driver.execute_script("return window.pageYOffset;")
        assert initial_scroll == 0, "Page should start at top"

        # Scroll to bottom
        page.scroll_to_bottom()
        # Wait for scroll animation (using small delay as scroll is instant)
        time.sleep(0.3)
        bottom_scroll = driver.execute_script("return window.pageYOffset;")
        assert bottom_scroll > initial_scroll, \
            f"Should scroll down, initial: {initial_scroll}, bottom: {bottom_scroll}"

        # Scroll back to top
        page.scroll_to_top()
        time.sleep(0.3)
        top_scroll = driver.execute_script("return window.pageYOffset;")
        assert top_scroll < bottom_scroll, \
            f"Should scroll back to top, bottom: {bottom_scroll}, top: {top_scroll}"


class TestScreenshotCapabilities:
    """Test suite demonstrating screenshot capabilities."""

    @pytest.mark.screenshot_on_pass
    def test_screenshot_on_pass(self, driver: webdriver.Remote):
        """Demonstrate screenshot capture on test pass."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()
        assert "Selenium" in page.get_page_title(), "Page should load for screenshot"

    @pytest.mark.xfail(reason="Demonstrates screenshot on failure - this test is expected to fail")
    def test_screenshot_on_failure(self, driver: webdriver.Remote):
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

    def test_implicit_wait(self, driver: webdriver.Remote):
        """Demonstrate implicit wait functionality."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Implicit wait should allow elements to load
        assert page.is_navigation_visible(), "Navigation should be visible with implicit wait"
        assert page.is_logo_visible(), "Logo should be visible with implicit wait"

    def test_explicit_wait(self, driver: webdriver.Remote):
        """Demonstrate explicit wait functionality."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Explicit wait for main heading
        heading = page.wait_for_element_visible(By.TAG_NAME, "h1")
        assert heading is not None, "Heading should be found with explicit wait"
        assert "Selenium" in heading.text, f"Heading should contain 'Selenium', got: {heading.text}"

    def test_window_management(self, driver: webdriver.Remote):
        """Demonstrate window management capabilities."""
        page = SeleniumPage(driver)
        page.navigate_to_homepage()

        # Get window size
        size = driver.get_window_size()
        assert size['width'] > 0, f"Window width should be positive, got: {size['width']}"
        assert size['height'] > 0, f"Window height should be positive, got: {size['height']}"

        # Maximize window
        driver.maximize_window()
        maximized_size = driver.get_window_size()
        assert maximized_size['width'] >= size['width'], \
            f"Maximized width should be >= original, {maximized_size['width']} >= {size['width']}"
        assert maximized_size['height'] >= size['height'], \
            f"Maximized height should be >= original, {maximized_size['height']} >= {size['height']}"

    def test_url_navigation(self, driver: webdriver.Remote):
        """Demonstrate URL navigation and verification."""
        page = SeleniumPage(driver)

        # Navigate to homepage
        page.navigate_to_homepage()
        homepage_url = page.get_current_url().lower()
        assert "selenium.dev" in homepage_url, f"Should be on homepage, got: {homepage_url}"

        # Navigate to downloads
        page.navigate_to_downloads()
        downloads_url = page.get_current_url().lower()
        assert "downloads" in downloads_url, f"Should be on downloads page, got: {downloads_url}"

        # Navigate back
        driver.back()
        back_url = page.get_current_url().lower()
        assert "selenium.dev" in back_url or back_url == "https://www.selenium.dev/", \
            f"Should navigate back to homepage, got: {back_url}"
