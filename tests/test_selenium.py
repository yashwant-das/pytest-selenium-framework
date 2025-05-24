import pytest
from pages.selenium_page import SeleniumPage

def test_selenium_title(driver, config):
    """Simple test to demonstrate basic page navigation and title verification"""
    page = SeleniumPage(driver)
    page.navigate_to_homepage()
    
    # Get the page title
    title = driver.title
    
    # Check if "Selenium" is in the title
    assert "Selenium" in title, f"Expected 'Selenium' to be in the title, but got: {title}"

def test_navigation_items(driver, config, test_data):
    """Demonstrates data-driven testing using configuration"""
    page = SeleniumPage(driver)
    page.navigate_to_homepage()
    
    # Get actual navigation items
    nav_items = page.get_navigation_items()
    
    # Get expected items from test data
    expected_items = list(test_data["test_data"]["selenium"]["navigation"].values())
    
    # Print for debugging
    print(f"Expected items: {list(expected_items)}")
    print(f"Actual items: {nav_items}")
    
    # Verify each expected item is present
    for item in expected_items:
        assert item in nav_items, f"Navigation item '{item}' should be present"