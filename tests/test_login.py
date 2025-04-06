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
    page.navigate_to_login()
    return page

@pytest.mark.login
class TestLogin:
    @pytest.mark.smoke
    def test_valid_login(self, login_page, test_data):
        """Test login with valid credentials"""
        credentials = test_data['github']['login']['valid_credentials']
        login_page.login(credentials['username'], credentials['password'])
        assert login_page.is_logged_in(), "Login should be successful"

    @pytest.mark.smoke
    def test_invalid_login(self, login_page, test_data):
        """Test login with invalid credentials"""
        credentials = test_data['github']['login']['invalid_credentials']
        login_page.login(credentials['username'], credentials['password'])
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert "Incorrect username or password" in error_message

    def test_empty_credentials(self, login_page):
        """Test login with empty credentials"""
        login_page.login("", "")
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert "Username or password cannot be empty" in error_message

    def test_special_characters(self, login_page, test_data):
        """Test login with special characters in username"""
        login_page.login("test@user#123", "password123")
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"

    def test_two_factor_login(self, login_page, test_data):
        """Test login with two-factor authentication"""
        credentials = test_data['github']['login']['two_factor']
        login_page.login_with_two_factor(
            credentials['username'],
            credentials['password'],
            credentials['code']
        )
        assert login_page.is_logged_in(), "Login with 2FA should be successful" 