from .base_page import BasePage
from selenium.webdriver.common.by import By

class SeleniumPage(BasePage):
    """Page object for Selenium website"""
    
    # Locators
    NAV_ITEMS = (By.CSS_SELECTOR, ".navbar-nav > li > a.nav-link")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.selenium.dev"
    
    def navigate_to_homepage(self):
        """Navigate to Selenium homepage"""
        self.navigate_to(self.url)
        # Wait for the page to load
        self.wait_for_element_visible(By.CLASS_NAME, "navbar")
    
    def is_navigation_visible(self):
        """Check if main navigation is visible"""
        return self.is_element_visible(By.CLASS_NAME, "navbar")
    
    def is_logo_visible(self):
        """Check if Selenium logo is visible"""
        return self.is_element_visible(By.CLASS_NAME, "navbar-brand")
    
    def get_navigation_items(self):
        """Get all navigation items"""
        nav_items = self.find_elements(*self.NAV_ITEMS)
        return [item.text.strip() for item in nav_items if item.text.strip()]
    
    def navigate_to_downloads(self):
        """Navigate to downloads page"""
        self.click(By.LINK_TEXT, "Downloads")
        return "downloads" in self.get_current_url().lower()
    
    def get_download_options(self):
        """Get all download language options"""
        language_elements = self.find_elements(By.CSS_SELECTOR, ".card-title")
        return [elem.text.strip() for elem in language_elements if elem.text.strip()] 