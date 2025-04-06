from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class GitHubPage(BasePage):
    """Page object for GitHub website"""
    
    # Locators
    SIGN_IN_BUTTON = (By.LINK_TEXT, "Sign in")
    USERNAME_INPUT = (By.ID, "login_field")
    PASSWORD_INPUT = (By.ID, "password")
    SIGN_IN_SUBMIT = (By.NAME, "commit")
    ERROR_MESSAGE = (By.CLASS_NAME, "js-flash-alert")
    TWO_FACTOR_INPUT = (By.ID, "otp")
    TWO_FACTOR_SUBMIT = (By.CLASS_NAME, "btn-primary")
    PROFILE_MENU = (By.CLASS_NAME, "Header-link")
    SIGN_OUT_BUTTON = (By.CLASS_NAME, "dropdown-signout")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://github.com"
    
    def navigate_to_homepage(self):
        """Navigate to GitHub homepage"""
        self.navigate_to(self.url)
        self.wait_for_element_visible(*self.SIGN_IN_BUTTON)
    
    def click_sign_in(self):
        """Click the sign in button"""
        self.click_element(*self.SIGN_IN_BUTTON)
        self.wait_for_element_visible(*self.USERNAME_INPUT)
    
    def login(self, username, password):
        """Perform login with username and password"""
        self.send_keys(*self.USERNAME_INPUT, username)
        self.send_keys(*self.PASSWORD_INPUT, password)
        self.click_element(*self.SIGN_IN_SUBMIT)
    
    def enter_two_factor_code(self, code):
        """Enter two-factor authentication code"""
        self.wait_for_element_visible(*self.TWO_FACTOR_INPUT)
        self.send_keys(*self.TWO_FACTOR_INPUT, code)
        self.click_element(*self.TWO_FACTOR_SUBMIT)
    
    def get_error_message(self):
        """Get error message if login fails"""
        try:
            error_element = self.find_element(*self.ERROR_MESSAGE)
            return error_element.text
        except:
            return None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            return self.is_element_visible(*self.PROFILE_MENU)
        except:
            return False
    
    def sign_out(self):
        """Sign out of GitHub"""
        if self.is_logged_in():
            self.click_element(*self.PROFILE_MENU)
            self.click_element(*self.SIGN_OUT_BUTTON)
            return True
        return False 