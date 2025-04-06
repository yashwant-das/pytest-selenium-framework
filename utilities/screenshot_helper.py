import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ScreenshotHelper:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self, name=None):
        """
        Take a screenshot and save it with timestamp
        :param name: Optional name for the screenshot
        :return: Path to the screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        self.driver.save_screenshot(filepath)
        return filepath

    def wait_and_take_screenshot(self, by, value, timeout=10, name=None):
        """
        Wait for an element to be visible and take a screenshot
        :param by: Locator strategy
        :param value: Locator value
        :param timeout: Maximum time to wait
        :param name: Optional name for the screenshot
        :return: Path to the screenshot file
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return self.take_screenshot(name)
        except TimeoutException:
            return self.take_screenshot(f"{name}_timeout" if name else "timeout") 