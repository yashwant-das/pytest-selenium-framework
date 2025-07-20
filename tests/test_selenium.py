import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.selenium_page import SeleniumPage

def test_selenium_title(driver, config):
    """Simple test to demonstrate basic page navigation and title verification"""
    print("\n🚀 Starting test_selenium_title...")
    
    page = SeleniumPage(driver)
    print("📄 Navigating to homepage...")
    page.navigate_to_homepage()
    
    # Wait for page to load and add visual delay
    print("⏳ Waiting for page to load...")
    time.sleep(2)  # 2 second delay to observe navigation
    
    # Get the page title
    title = driver.title
    print(f"📋 Page title retrieved: '{title}'")
    
    # Add delay before assertion
    time.sleep(1)
    
    # Check if "Selenium" is in the title
    print("✅ Verifying 'Selenium' is in the title...")
    assert "Selenium" in title, f"Expected 'Selenium' to be in the title, but got: {title}"
    
    print("✨ test_selenium_title completed successfully!\n")

def test_navigation_items(driver, config, test_data):
    """Demonstrates data-driven testing using configuration"""
    print("\n🚀 Starting test_navigation_items...")
    
    page = SeleniumPage(driver)
    print("📄 Navigating to homepage...")
    page.navigate_to_homepage()
    
    # Wait for page to load completely
    print("⏳ Waiting for page to load completely...")
    time.sleep(3)  # 3 second delay to observe page load
    
    # Get actual navigation items
    print("🔍 Extracting navigation items from page...")
    nav_items = page.get_navigation_items()
    time.sleep(1)  # Brief pause after extraction
    
    # Get expected items from test data
    expected_items = list(test_data["test_data"]["selenium"]["navigation"].values())
    
    # Print for debugging with enhanced formatting
    print(f"\n📊 Test Data Comparison:")
    print(f"   Expected items: {list(expected_items)}")
    print(f"   Actual items: {nav_items}")
    print(f"   Total expected: {len(expected_items)}")
    print(f"   Total found: {len(nav_items)}")
    
    # Add delay before verification
    time.sleep(2)
    
    # Verify each expected item is present with individual feedback
    print("\n🔍 Verifying each navigation item...")
    for i, item in enumerate(expected_items, 1):
        print(f"   [{i}/{len(expected_items)}] Checking for: '{item}'")
        assert item in nav_items, f"Navigation item '{item}' should be present"
        print(f"   ✅ Found: '{item}'")
        time.sleep(0.5)  # Small delay between each check
    
    print("\n✨ test_navigation_items completed successfully!\n")