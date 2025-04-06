import pytest
from pages.github_page import GitHubPage

def test_github_login_success(driver, config, test_data):
    """Test successful login to GitHub"""
    page = GitHubPage(driver)
    page.navigate_to_homepage()
    
    # Click sign in button
    page.click_sign_in()
    
    # Login with valid credentials
    credentials = test_data["github"]["login"]["valid_credentials"]
    page.login(credentials["username"], credentials["password"])
    
    # Check if login was successful
    assert page.is_logged_in(), "User should be logged in"
    
    # Sign out
    assert page.sign_out(), "User should be able to sign out"

def test_github_login_invalid_credentials(driver, config, test_data):
    """Test login with invalid credentials"""
    page = GitHubPage(driver)
    page.navigate_to_homepage()
    
    # Click sign in button
    page.click_sign_in()
    
    # Login with invalid credentials
    credentials = test_data["github"]["login"]["invalid_credentials"]
    page.login(credentials["username"], credentials["password"])
    
    # Check error message
    error_message = page.get_error_message()
    assert error_message is not None, "Error message should be displayed"
    assert test_data["github"]["error_messages"]["invalid_credentials"] in error_message, "Should show invalid credentials error"

def test_github_login_two_factor(driver, config, test_data):
    """Test login with two-factor authentication"""
    page = GitHubPage(driver)
    page.navigate_to_homepage()
    
    # Click sign in button
    page.click_sign_in()
    
    # Login with credentials that require 2FA
    credentials = test_data["github"]["login"]["valid_credentials"]
    page.login(credentials["username"], credentials["password"])
    
    # Enter 2FA code
    two_factor_code = test_data["github"]["login"]["two_factor_code"]
    page.enter_two_factor_code(two_factor_code)
    
    # Check if login was successful
    assert page.is_logged_in(), "User should be logged in after 2FA"
    
    # Sign out
    assert page.sign_out(), "User should be able to sign out" 