"""Base page class with common methods for all page objects."""
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.screenshot_helper import ScreenshotHelper
import logging

class BasePage:
    """Base page class providing common functionality for all page objects."""
    
    def __init__(self, driver: webdriver.Remote):
        """Initialize base page.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.screenshot_helper = ScreenshotHelper(driver)
        self.logger = logging.getLogger(__name__)

    def find_element(self, by: By, value: str) -> WebElement:
        """Find an element with explicit wait"""
        try:
            self.logger.debug(f"Finding element: {by}={value}")
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {by}={value}")
            self.screenshot_helper.take_screenshot(f"element_not_found_{value}")
            raise

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """Find multiple elements with explicit wait."""
        try:
            self.logger.debug(f"Finding elements: {by}={value}")
            elements = self.wait.until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {by}={value}")
            self.screenshot_helper.take_screenshot(f"elements_not_found_{value}")
            return []

    def is_element_visible(self, by: By, value: str, timeout: int = 10) -> bool:
        """Check if an element is visible."""
        try:
            self.logger.debug(f"Checking visibility of element: {by}={value}")
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            self.logger.error(f"Element not visible: {by}={value}")
            self.screenshot_helper.take_screenshot(f"element_not_visible_{value}")
            return False

    def wait_for_element_visible(self, by: By, value: str, timeout: int = 10) -> WebElement:
        """Wait for an element to be visible."""
        try:
            self.logger.debug(f"Waiting for element to be visible: {by}={value}")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible after {timeout} seconds: {by}={value}")
            self.screenshot_helper.take_screenshot(f"element_not_visible_{value}")
            raise

    def is_element_clickable(self, by: By, value: str, timeout: int = 10) -> bool:
        """Check if an element is clickable."""
        try:
            self.logger.debug(f"Checking clickability of element: {by}={value}")
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                EC.element_to_be_clickable((by, value))
            )
            return True
        except TimeoutException:
            self.logger.debug(f"Element not clickable: {by}={value}")
            return False

    def click(self, by: By, value: str) -> None:
        """Click on an element."""
        try:
            self.logger.debug(f"Clicking element: {by}={value}")
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element: {by}={value}")
            self.screenshot_helper.take_screenshot(f"click_failed_{value}")
            raise

    def get_text(self, by: By, value: str) -> str:
        """Get text of an element with explicit wait."""
        try:
            self.logger.debug(f"Getting text from element: {by}={value}")
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element.text
        except TimeoutException:
            self.logger.error(f"Could not get text from element: {by}={value}")
            self.screenshot_helper.take_screenshot(f"get_text_failed_{value}")
            raise

    def send_keys(self, by: By, value: str, text: str) -> None:
        """Send keys to an element."""
        try:
            self.logger.debug(f"Sending keys to element: {by}={value}")
            element = self.find_element(by, value)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to send keys to element: {by}={value}")
            self.screenshot_helper.take_screenshot(f"send_keys_failed_{value}")
            raise

    def wait_for_url_contains(self, url_substring: str, timeout: int = 10) -> bool:
        """Wait for URL to contain specific substring."""
        try:
            self.logger.debug(f"Waiting for URL to contain: {url_substring}")
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: url_substring in driver.current_url
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL did not contain: {url_substring}")
            return False

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url

    def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def take_screenshot(self, name: str) -> None:
        """Take a screenshot."""
        try:
            self.driver.save_screenshot(f"reports/screenshots/{name}.png")
            self.logger.info(f"Screenshot saved: {name}.png")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise

    def wait_for_element_to_disappear(self, by: By, value: str, timeout: int = 10) -> bool:
        """Wait for element to disappear with explicit wait and logging."""
        try:
            self.logger.debug(f"Waiting for element to disappear: {by}={value}")
            wait = WebDriverWait(self.driver, timeout)
            wait.until_not(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            self.logger.error(f"Element did not disappear: {by}={value}")
            self.screenshot_helper.take_screenshot(f"element_did_not_disappear_{value}")
            raise 