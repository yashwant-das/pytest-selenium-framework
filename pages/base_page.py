from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.screenshot_helper import ScreenshotHelper
import logging
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.screenshot_helper = ScreenshotHelper(driver)
        self.logger = logging.getLogger(__name__)

    def find_element(self, by, value):
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

    def find_elements(self, by, value):
        """Find multiple elements with explicit wait"""
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

    def is_element_visible(self, by, value, timeout=10):
        """Check if an element is visible"""
        try:
            self.logger.debug(f"Checking visibility of element: {by}={value}")
            self.wait.until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            self.logger.error(f"Element not visible: {by}={value}")
            self.screenshot_helper.take_screenshot(f"element_not_visible_{value}")
            return False

    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for an element to be visible"""
        try:
            self.logger.debug(f"Waiting for element to be visible: {locator}")
            self.wait = WebDriverWait(self.driver, timeout)
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible after {timeout} seconds: {locator}")
            self.screenshot_helper.take_screenshot(f"element_not_visible_{locator[1]}")
            raise

    def is_element_clickable(self, by, value, timeout=10):
        """Check if an element is clickable"""
        try:
            self.logger.debug(f"Checking clickability of element: {by}={value}")
            self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            return True
        except TimeoutException:
            self.logger.debug(f"Element not clickable: {by}={value}")
            return False

    def click(self, locator):
        """Click on an element"""
        try:
            self.logger.debug(f"Clicking element: {locator}")
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator}")
            self.screenshot_helper.take_screenshot(f"click_failed_{locator[1]}")
            raise

    def get_text(self, by, value):
        """Get text of an element with explicit wait"""
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

    def send_keys(self, locator, text):
        """Send keys to an element"""
        try:
            self.logger.debug(f"Sending keys to element: {locator}")
            element = self.find_element(*locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to send keys to element: {locator}")
            self.screenshot_helper.take_screenshot(f"send_keys_failed_{locator[1]}")
            raise

    def wait_for_url_contains(self, url_substring, timeout=10):
        """Wait for URL to contain specific substring"""
        try:
            self.logger.debug(f"Waiting for URL to contain: {url_substring}")
            self.wait.until(
                lambda driver: url_substring in driver.current_url
            )
            return True
        except TimeoutException:
            self.logger.error(f"URL did not contain: {url_substring}")
            return False

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def navigate_to(self, url):
        """Navigate to a URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def take_screenshot(self, name):
        """Take a screenshot"""
        try:
            self.driver.save_screenshot(f"reports/screenshots/{name}.png")
            self.logger.info(f"Screenshot saved: {name}.png")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise

    def wait_for_element_to_disappear(self, locator, timeout=10):
        """Wait for element to disappear with explicit wait and logging"""
        try:
            self.logger.debug(f"Waiting for element to disappear: {locator}")
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.error(f"Element did not disappear: {locator}")
            self.screenshot_helper.take_screenshot(f"element_did_not_disappear_{locator[1]}")
            raise 