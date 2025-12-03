"""Screenshot helper for capturing and attaching screenshots to reports.

This module provides a centralized class for taking screenshots and attaching
them to test reports (Allure and HTML). It handles screenshot naming, directory
creation, and report integration.
"""
import os
import logging
from datetime import datetime
from typing import Optional, Union, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure
import pytest

logger = logging.getLogger(__name__)

__all__ = ['ScreenshotHelper']


class ScreenshotHelper:
    """Helper class for taking screenshots and attaching them to test reports."""
    
    def __init__(self, driver: webdriver.Remote):
        """Initialize screenshot helper.
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        # Get project root directory (parent of utilities directory)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.screenshot_dir = os.path.join(project_root, "reports", "screenshots")
        
        # Create screenshot directory if it doesn't exist
        try:
            os.makedirs(self.screenshot_dir, exist_ok=True)
        except OSError as e:
            logger.warning(f"Could not create screenshot directory: {e}")

    def take_screenshot(self, name: Optional[str] = None) -> str:
        """Take a screenshot and save it with timestamp.
        
        Args:
            name: Optional name for the screenshot
            
        Returns:
            str: Path to the screenshot file
            
        Raises:
            Exception: If screenshot cannot be saved
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            logger.debug(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            raise

    def wait_and_take_screenshot(self, by: By, value: str, timeout: int = 10, 
                                 name: Optional[str] = None) -> str:
        """Wait for an element to be visible and take a screenshot.
        
        Args:
            by: Locator strategy (from selenium.webdriver.common.by.By)
            value: Locator value
            timeout: Maximum time to wait in seconds
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
            logger.debug(f"Element not visible after {timeout}s, taking timeout screenshot")
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
            try:
                error_filename = f"failure_{test_name}_{timestamp}_error.txt"
                error_path = os.path.join(self.screenshot_dir, error_filename)
                with open(error_path, "w", encoding='utf-8') as f:
                    f.write(error_msg)
                
                self.attach_to_allure(error_msg, f"Error Log - {test_name}",
                                    allure.attachment_type.TEXT)
                logger.info(f"Error details saved: {error_path}")
            except Exception as e:
                logger.warning(f"Failed to save error message: {e}")
        
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
    
    def attach_to_allure(self, content: Union[str, bytes], name: str, 
                        attachment_type: allure.attachment_type) -> None:
        """Attach content to Allure report.
        
        This method can attach either file content (from a file path) or
        string content directly to Allure reports.
        
        Args:
            content: Either a file path (str) or content bytes/string to attach
            name: Name for the attachment in Allure
            attachment_type: Type of attachment (PNG, TEXT, etc.)
        """
        try:
            # If content is a file path, read the file
            if isinstance(content, str) and os.path.exists(content):
                with open(content, "rb") as f:
                    file_content = f.read()
                allure.attach(file_content, name=name, attachment_type=attachment_type)
                logger.debug(f"Attached file to Allure: {content}")
            # If content is bytes or string, attach directly
            elif isinstance(content, (bytes, str)):
                if isinstance(content, str):
                    content = content.encode('utf-8')
                allure.attach(content, name=name, attachment_type=attachment_type)
                logger.debug(f"Attached content to Allure: {name}")
            else:
                logger.warning(f"Invalid content type for Allure attachment: {type(content)}")
        except Exception as e:
            logger.error(f"Failed to attach to Allure: {e}")
    
    def attach_to_html_report(self, screenshot_path: str) -> Optional[Any]:
        """Attach screenshot to HTML report.
        
        Args:
            screenshot_path: Path to the screenshot file
            
        Returns:
            pytest_html.extras.image object if successful, None otherwise
        """
        try:
            if not os.path.exists(screenshot_path):
                logger.warning(f"Screenshot file not found: {screenshot_path}")
                return None
                
            # Check if pytest-html is available
            try:
                import pytest_html
            except ImportError:
                logger.debug("pytest-html not available, skipping HTML report attachment")
                return None
            
            # Return the extra object for pytest-html
            html_extra = pytest_html.extras.image(screenshot_path)
            logger.debug(f"Attached screenshot to HTML report: {screenshot_path}")
            return html_extra
        except Exception as e:
            logger.error(f"Failed to attach to HTML report: {e}")
            return None 