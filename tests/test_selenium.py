import pytest
from pages.selenium_page import SeleniumPage

def test_selenium_homepage(driver, config, test_data):
    """Test basic navigation on Selenium's homepage"""
    page = SeleniumPage(driver)
    page.navigate_to_homepage()
    
    # Verify navigation and logo
    assert page.is_navigation_visible(), "Main navigation should be visible"
    assert page.is_logo_visible(), "Selenium logo should be visible"
    
    # Verify navigation items
    nav_items = page.get_navigation_items()
    expected_items = test_data["selenium"]["navigation"].values()
    for item in nav_items:
        assert item in expected_items, f"Navigation item {item} should be in expected items"

def test_selenium_search(driver, config, test_data):
    """Test search functionality on Selenium's website"""
    page = SeleniumPage(driver)
    page.navigate_to_homepage()
    
    # Perform search
    search_term = test_data["search"]["valid_term"]
    assert page.search(search_term), "Search should return results"
    
    # Verify search results
    results_text = page.get_search_results_text().lower()
    assert search_term.lower() in results_text, f"Search results should contain '{search_term}'"

def test_selenium_downloads(driver, config, test_data):
    """Test navigation to downloads page and verify language options"""
    page = SeleniumPage(driver)
    page.navigate_to_homepage()
    
    # Navigate to downloads
    assert page.navigate_to_downloads(), "Should be on the downloads page"
    
    # Verify language options
    download_options = page.get_download_options()
    expected_languages = test_data["selenium"]["downloads"].values()
    for language in expected_languages:
        assert language in download_options, f"Language option {language} should be available" 