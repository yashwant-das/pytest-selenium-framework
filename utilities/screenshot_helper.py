"""Screenshot helper for capturing and attaching screenshots to reports."""
import os
import logging
from datetime import datetime
from typing import Optional
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import pytest

logger = logging.getLogger(__name__)


class ScreenshotHelper:
    """Helper class for taking screenshots and attaching them to test reports."""
    
    def __init__(self, driver):
        """Initialize screenshot helper.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.screenshot_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self, name: Optional[str] = None) -> str:
        """Take a screenshot and save it with timestamp.
        
        Args:
            name: Optional name for the screenshot
            
        Returns:
            str: Path to the screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        self.driver.save_screenshot(filepath)
        return filepath

    def wait_and_take_screenshot(self, by, value, timeout: int = 10, 
                                 name: Optional[str] = None) -> str:
        """Wait for an element to be visible and take a screenshot.
        
        Args:
            by: Locator strategy
            value: Locator value
            timeout: Maximum time to wait
            name: Optional name for the screenshot
            
        Returns:
            str: Path to the screenshot file
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return self.take_screenshot(name)
        except TimeoutException:
            return self.take_screenshot(f"{name}_timeout" if name else "timeout")
    
    def take_failure_screenshot(self, test_name: str, 
                               error_msg: Optional[str] = None) -> str:
        """Take a screenshot for a failed test and attach to reports.
        
        Args:
            test_name: Name of the test that failed
            error_msg: Optional error message to save
            
        Returns:
            str: Path to the screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"failure_{test_name}_{timestamp}.png"
        screenshot_path = os.path.join(self.screenshot_dir, filename)
        
        # Take screenshot
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved for failed test: {screenshot_path}")
        
        # Attach to Allure report
        self.attach_to_allure(screenshot_path, f"Screenshot - {test_name}", 
                            allure.attachment_type.PNG)
        
        # Save error message if provided
        if error_msg:
            error_filename = f"failure_{test_name}_{timestamp}_error.txt"
            error_path = os.path.join(self.screenshot_dir, error_filename)
            with open(error_path, "w") as f:
                f.write(error_msg)
            
            self.attach_to_allure(error_msg, f"Error Log - {test_name}",
                                allure.attachment_type.TEXT)
            logger.info(f"Error details saved: {error_path}")
        
        return screenshot_path
    
    def take_pass_screenshot(self, test_name: str) -> str:
        """Take a screenshot for a passed test and attach to reports.
        
        Args:
            test_name: Name of the test that passed
            
        Returns:
            str: Path to the screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pass_{test_name}_{timestamp}.png"
        screenshot_path = os.path.join(self.screenshot_dir, filename)
        
        # Take screenshot
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved for passed test: {screenshot_path}")
        
        # Attach to Allure report
        self.attach_to_allure(screenshot_path, f"Screenshot - {test_name} (Passed)",
                            allure.attachment_type.PNG)
        
        return screenshot_path
    
    def attach_to_allure(self, file_path: str, name: str, 
                        attachment_type: allure.attachment_type) -> None:
        """Attach file to Allure report.
        
        Args:
            file_path: Path to the file to attach
            name: Name for the attachment in Allure
            attachment_type: Type of attachment (PNG, TEXT, etc.)
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    allure.attach(f.read(), name=name, attachment_type=attachment_type)
        except Exception as e:
            logger.error(f"Failed to attach to Allure: {e}")
    
    def attach_to_html_report(self, screenshot_path: str) -> None:
        """Attach screenshot to HTML report.
        
        Args:
            screenshot_path: Path to the screenshot file
        """
        try:
            if hasattr(pytest, 'html') and os.path.exists(screenshot_path):
                import pytest_html
                # This will be called from pytest hook which has access to report.extras
                return pytest_html.extras.image(screenshot_path)
        except Exception as e:
            logger.error(f"Failed to attach to HTML report: {e}")
        return None 