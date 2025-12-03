"""Page object for Selenium website."""
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from .base_page import BasePage

class SeleniumPage(BasePage):
    """Page object for Selenium website."""
    
    # Locators
    NAV_ITEMS: Tuple[By, str] = (By.CSS_SELECTOR, ".navbar-nav > li > a.nav-link")
    MAIN_HEADING: Tuple[By, str] = (By.TAG_NAME, "h1")
    WEBDRIVER_SECTION: Tuple[By, str] = (By.XPATH, "//h4[contains(text(), 'Selenium WebDriver')]")
    IDE_SECTION: Tuple[By, str] = (By.XPATH, "//h4[contains(text(), 'Selenium IDE')]")
    GRID_SECTION: Tuple[By, str] = (By.XPATH, "//h4[contains(text(), 'Selenium Grid')]")
    DOWNLOADS_HEADING: Tuple[By, str] = (By.XPATH, "//h1[contains(text(), 'Downloads')]")
    LANGUAGE_CARDS: Tuple[By, str] = (By.CSS_SELECTOR, "img[alt*='Python'], img[alt*='Java'], img[alt*='JavaScript'], img[alt*='Ruby'], img[alt*='C Sharp']")
    
    def __init__(self, driver: webdriver.Remote):
        """Initialize Selenium page.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.url = "https://www.selenium.dev"
    
    def navigate_to_homepage(self) -> None:
        """Navigate to Selenium homepage."""
        self.navigate_to(self.url)
        self.wait_for_element_visible(By.CLASS_NAME, "navbar")
    
    def is_navigation_visible(self) -> bool:
        """Check if main navigation is visible."""
        return self.is_element_visible(By.CLASS_NAME, "navbar")
    
    def is_logo_visible(self) -> bool:
        """Check if Selenium logo is visible."""
        return self.is_element_visible(By.CLASS_NAME, "navbar-brand")
    
    def get_navigation_items(self) -> List[str]:
        """Get all navigation items.
        
        Returns:
            List of navigation item text strings
        """
        nav_items = self.find_elements(*self.NAV_ITEMS)
        return [item.text.strip() for item in nav_items if item.text.strip()]
    
    def get_main_heading(self) -> str:
        """Get the main heading text.
        
        Returns:
            Main heading text
        """
        heading = self.find_element(*self.MAIN_HEADING)
        return heading.text
    
    def navigate_to_downloads(self) -> bool:
        """Navigate to downloads page.
        
        Returns:
            True if downloads page is loaded
        """
        self.click(By.LINK_TEXT, "Downloads")
        self.wait_for_url_contains("downloads")
        return "downloads" in self.get_current_url().lower()
    
    def navigate_to_documentation(self) -> bool:
        """Navigate to documentation page.
        
        Returns:
            True if documentation page is loaded
        """
        self.click(By.LINK_TEXT, "Documentation")
        self.wait_for_url_contains("documentation")
        return "documentation" in self.get_current_url().lower()
    
    def get_component_sections(self) -> List[str]:
        """Get all component section headings (WebDriver, IDE, Grid).
        
        Returns:
            List of component section text
        """
        sections = []
        if self.is_element_visible(*self.WEBDRIVER_SECTION):
            sections.append("Selenium WebDriver")
        if self.is_element_visible(*self.IDE_SECTION):
            sections.append("Selenium IDE")
        if self.is_element_visible(*self.GRID_SECTION):
            sections.append("Selenium Grid")
        return sections
    
    def scroll_to_bottom(self) -> None:
        """Scroll page to bottom using JavaScript."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scroll_to_top(self) -> None:
        """Scroll page to top using JavaScript."""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def get_page_title(self) -> str:
        """Get page title.
        
        Returns:
            Page title text
        """
        return self.driver.title 