import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_selenium_homepage(driver, config, test_data):
    """Test basic navigation on Selenium's homepage"""
    # Navigate to Selenium website
    driver.get(config["environment"]["url"])
    
    # Wait for the main navigation to be visible
    nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "navbar-nav"))
    )
    assert nav.is_displayed(), "Main navigation should be visible"
    
    # Verify Selenium logo is present
    logo = driver.find_element(By.CLASS_NAME, "navbar-brand")
    assert logo.is_displayed(), "Selenium logo should be visible"
    
    # Verify main navigation items
    nav_items = driver.find_elements(By.CSS_SELECTOR, ".navbar-nav .nav-item")
    expected_items = test_data["selenium"]["navigation"].values()
    for item in nav_items:
        assert item.text in expected_items, f"Navigation item {item.text} should be in expected items"

def test_selenium_search(driver, config, test_data):
    """Test search functionality on Selenium's website"""
    # Navigate to Selenium website
    driver.get(config["environment"]["url"])
    
    # Find and click the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='search-button']"))
    )
    search_button.click()
    
    # Wait for search input to be visible and enter search term
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='search-input']"))
    )
    search_term = test_data["search"]["valid_term"]
    search_input.send_keys(search_term)
    search_input.submit()
    
    # Wait for search results
    try:
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
        )
        assert search_results.is_displayed(), "Search results should be visible"
        
        # Verify search results contain the search term
        results_text = search_results.text.lower()
        assert search_term.lower() in results_text, f"Search results should contain '{search_term}'"
    except TimeoutException:
        pytest.fail("Search results did not appear within the expected time")

def test_selenium_downloads(driver, config, test_data):
    """Test navigation to downloads page and verify language options"""
    # Navigate to Selenium website
    driver.get(config["environment"]["url"])
    
    # Click on Downloads link
    downloads_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, test_data["selenium"]["navigation"]["downloads"]))
    )
    downloads_link.click()
    
    # Verify we're on the downloads page
    assert "download" in driver.current_url.lower(), "Should be on the downloads page"
    
    # Verify language options are present
    for language in test_data["selenium"]["downloads"].values():
        language_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{language}')]"))
        )
        assert language_element.is_displayed(), f"Language option {language} should be visible" 