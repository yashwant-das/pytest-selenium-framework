"""Page object for Selenium website."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List, Tuple, Optional

from utilities.config_manager import ConfigManager
from .base_page import BasePage


class SeleniumPage(BasePage):
    """Page object for Selenium website."""

    # Locators
    NAV_ITEMS: Tuple[By, str] = (By.CSS_SELECTOR, ".navbar-nav > li > a.nav-link")
    MAIN_HEADING: Tuple[By, str] = (By.TAG_NAME, "h1")
    WEBDRIVER_SECTION: Tuple[By, str] = (By.XPATH, "//h4[contains(text(), 'Selenium WebDriver')]")
    IDE_SECTION: Tuple[By, str] = (By.XPATH, "//h4[contains(text(), 'Selenium IDE')]")
    GRID_SECTION: Tuple[By, str] = (By.XPATH, "//h4[contains(text(), 'Selenium Grid')]")

    def __init__(self, driver: webdriver.Remote, environment: Optional[str] = None):
        """Initialize Selenium page.
        
        Args:
            driver: WebDriver instance
            environment: Optional environment name ('dev', 'qa', 'staging', 'prod').
                         If None, uses default environment from config.
        """
        super().__init__(driver)
        config_manager = ConfigManager()
        env_config = config_manager.get_env_config(environment)
        self.url = env_config.get("url", "https://www.selenium.dev")

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
        """Get all navigation items from the page.
        
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

    def navigate_to_downloads(self) -> None:
        """Navigate to downloads page.
        
        Raises:
            TimeoutException: If downloads page does not load within timeout
        """
        self.click(By.LINK_TEXT, "Downloads")
        self.wait_for_url_contains("downloads")

    def navigate_to_documentation(self) -> None:
        """Navigate to documentation page.
        
        Raises:
            TimeoutException: If documentation page does not load within timeout
        """
        self.click(By.LINK_TEXT, "Documentation")
        self.wait_for_url_contains("documentation")

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
        self.logger.debug("Scrolled to bottom of page")

    def scroll_to_top(self) -> None:
        """Scroll page to top using JavaScript."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.logger.debug("Scrolled to top of page")

    def get_page_title(self) -> str:
        """Get the current page title.
        
        Returns:
            str: Page title text
        """
        return self.driver.title
