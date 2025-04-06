import pytest
import json
from pages.specific_pages.login_page import LoginPage

def load_test_data():
    with open('test_data/test_data.json', 'r') as f:
        return json.load(f)

@pytest.fixture
def test_data():
    return load_test_data()

@pytest.fixture
def login_page(driver, config):
    page = LoginPage(driver, config)
    return page

@pytest.mark.login
class TestLogin:
    def test_valid_login(self, login_page, test_data):
        """Test successful login with valid credentials"""
        # Navigate to login page
        assert login_page.navigate_to_login(test_data["login"]["url"]), "Should navigate to login page"
        
        # Login with valid credentials
        credentials = test_data["login"]["valid_credentials"]
        assert login_page.login(credentials["username"], credentials["password"]), "Login should be successful"
        assert login_page.is_logged_in(), "User should be logged in"

    def test_invalid_login(self, login_page, test_data):
        """Test login with invalid credentials"""
        # Navigate to login page
        assert login_page.navigate_to_login(test_data["login"]["url"]), "Should navigate to login page"
        
        # Login with invalid credentials
        credentials = test_data["login"]["invalid_credentials"]
        assert not login_page.login(credentials["username"], credentials["password"]), "Login should fail"
        error_message = login_page.get_error_message()
        assert error_message is not None, "Should show error message"
        assert test_data["login"]["error_messages"]["invalid_credentials"] in error_message, "Should show invalid credentials error"

    def test_empty_credentials(self, login_page, test_data):
        """Test login with empty credentials"""
        # Navigate to login page
        assert login_page.navigate_to_login(test_data["login"]["url"]), "Should navigate to login page"
        
        # Login with empty credentials
        assert not login_page.login("", ""), "Login should fail with empty credentials"
        error_message = login_page.get_error_message()
        assert error_message is not None, "Should show error message"

    def test_special_characters(self, login_page, test_data):
        """Test login with special characters in credentials"""
        # Navigate to login page
        assert login_page.navigate_to_login(test_data["login"]["url"]), "Should navigate to login page"
        
        # Login with special characters
        special_chars = test_data["login"]["special_chars"]
        assert not login_page.login(special_chars, special_chars), "Login should fail with special characters"
        error_message = login_page.get_error_message()
        assert error_message is not None, "Should show error message"

    def test_two_factor_login(self, login_page, test_data):
        """Test login with two-factor authentication"""
        # Navigate to login page
        assert login_page.navigate_to_login(test_data["login"]["url"]), "Should navigate to login page"
        
        # Login with 2FA
        credentials = test_data["login"]["two_factor"]
        assert login_page.login_with_two_factor(
            credentials["username"],
            credentials["password"],
            credentials["code"]
        ), "2FA login should be successful"
        assert login_page.is_logged_in(), "User should be logged in after 2FA" 