from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SeleniumPage(BasePage):
    """Page object for Selenium website"""
    
    # Locators
    NAVBAR = (By.CLASS_NAME, "navbar-nav")
    LOGO = (By.CLASS_NAME, "navbar-brand")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-test='search-button']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test='search-input']")
    SEARCH_RESULTS = (By.CLASS_NAME, "search-results")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.selenium.dev"
    
    def navigate_to_homepage(self):
        """Navigate to Selenium homepage"""
        self.navigate_to(self.url)
        self.wait_for_element_visible(*self.NAVBAR)
    
    def is_navigation_visible(self):
        """Check if main navigation is visible"""
        return self.is_element_visible(*self.NAVBAR)
    
    def is_logo_visible(self):
        """Check if Selenium logo is visible"""
        return self.is_element_visible(*self.LOGO)
    
    def get_navigation_items(self):
        """Get all navigation items"""
        nav_items = self.find_elements(By.CSS_SELECTOR, ".navbar-nav .nav-item")
        return [item.text for item in nav_items]
    
    def search(self, search_term):
        """Perform a search"""
        # Click search button
        self.click_element(*self.SEARCH_BUTTON)
        
        # Enter search term
        self.send_keys(*self.SEARCH_INPUT, search_term)
        
        # Submit search
        search_input = self.find_element(*this.SEARCH_INPUT)
        search_input.submit()
        
        # Wait for results
        return self.is_element_visible(*this.SEARCH_RESULTS)
    
    def get_search_results_text(self):
        """Get text from search results"""
        return self.get_text(*this.SEARCH_RESULTS)
    
    def navigate_to_downloads(self):
        """Navigate to downloads page"""
        downloads_link = self.find_element(By.LINK_TEXT, "Downloads")
        self.click_element(By.LINK_TEXT, "Downloads")
        return "download" in self.get_current_url()
    
    def get_download_options(self):
        """Get all download language options"""
        language_elements = this.find_elements(By.CSS_SELECTOR, ".language-option")
        return [elem.text for elem in language_elements] 