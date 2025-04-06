from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

class LoginPage(BasePage):
    # Locators
    USERNAME_FIELD = (By.ID, "login_field")
    PASSWORD_FIELD = (By.ID, "password")
    SIGN_IN_BUTTON = (By.NAME, "commit")
    ERROR_MESSAGE = (By.CLASS_NAME, "flash-error")
    TWO_FACTOR_FIELD = (By.ID, "otp")
    TWO_FACTOR_BUTTON = (By.CLASS_NAME, "btn-primary")
    AVATAR = (By.CLASS_NAME, "avatar-user")

    def __init__(self, driver, config=None):
        super().__init__(driver)
        self.config = config
        self.logger = logging.getLogger(__name__)

    def navigate_to_login(self):
        """Navigate to the login page"""
        if not self.config or 'github' not in self.config:
            self.logger.error("GitHub configuration not found")
            raise ValueError("GitHub configuration not found")
        
        login_url = self.config['github']['login_url']
        self.logger.info(f"Navigating to login page: {login_url}")
        self.driver.get(login_url)
        try:
            self.wait_for_element_visible(self.USERNAME_FIELD)
            return True
        except TimeoutException:
            self.logger.error("Login page did not load properly")
            return False

    def login(self, username, password):
        """Login with username and password"""
        try:
            self.logger.info(f"Attempting to login with username: {username}")
            
            # Clear fields first
            username_field = self.wait_for_element_visible(self.USERNAME_FIELD)
            password_field = self.wait_for_element_visible(self.PASSWORD_FIELD)
            username_field.clear()
            password_field.clear()
            
            # Enter credentials
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # Click sign in button
            sign_in_button = self.wait_for_element_visible(self.SIGN_IN_BUTTON)
            sign_in_button.click()
            
            # Check for error message
            try:
                error = self.wait_for_element_visible(self.ERROR_MESSAGE)
                self.logger.warning(f"Login failed: {error.text}")
                return False
            except TimeoutException:
                # No error message means login might be successful
                return True
                
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Login failed due to element not found: {str(e)}")
            return False

    def login_with_two_factor(self, username, password, two_factor_code):
        """Login with username, password and two-factor code"""
        try:
            self.logger.info(f"Attempting to login with 2FA for username: {username}")
            
            # First login with username and password
            if not self.login(username, password):
                self.logger.error("Initial login failed, cannot proceed with 2FA")
                return False
            
            # Wait for 2FA field and enter code
            otp_field = self.wait_for_element_visible(self.TWO_FACTOR_FIELD)
            otp_field.clear()
            otp_field.send_keys(two_factor_code)
            
            # Click verify button
            verify_button = self.wait_for_element_visible(self.TWO_FACTOR_BUTTON)
            verify_button.click()
            
            return self.is_logged_in()
            
        except TimeoutException:
            self.logger.error("Two-factor authentication failed - elements not found")
            return False

    def get_error_message(self):
        """Get error message if login fails"""
        try:
            error_element = self.wait_for_element_visible(self.ERROR_MESSAGE)
            return error_element.text
        except TimeoutException:
            return None

    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            # Check for avatar which is only visible when logged in
            self.wait_for_element_visible(self.AVATAR)
            return True
        except TimeoutException:
            return False 