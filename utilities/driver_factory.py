"""Driver factory for creating WebDriver instances with unified logic."""
import logging
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from typing import Dict, Any, Optional
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utilities.exceptions import DriverInitializationError

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for creating WebDriver instances with smart driver management."""

    @staticmethod
    def _check_driver_in_path(driver_name: str) -> bool:
        """Check if driver is available in system PATH.
        
        Args:
            driver_name: Name of the driver executable (e.g., 'chromedriver')
            
        Returns:
            bool: True if driver is in PATH, False otherwise
        """
        try:
            subprocess.run([driver_name, "--version"],
                           capture_output=True, check=True, timeout=5)
            logger.debug(f"Found {driver_name} in system PATH")
            return True
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            logger.debug(f"{driver_name} not found in system PATH, will use webdriver-manager")
            return False

    @staticmethod
    def _get_driver_path(driver_manager: Any, driver_name: str) -> str:
        """Get driver path from webdriver-manager with proper handling.
        
        Args:
            driver_manager: Instance of webdriver-manager (ChromeDriverManager, GeckoDriverManager, etc.)
            driver_name: Name of the driver executable
            
        Returns:
            str: Path to the driver executable
            
        Raises:
            DriverInitializationError: If driver cannot be installed or found
        """
        try:
            driver_path = driver_manager.install()
            logger.info(f"Downloaded/installed {driver_name} via webdriver-manager: {driver_path}")
        except Exception as e:
            error_msg = f"Failed to install {driver_name} via webdriver-manager: {e}"
            logger.error(error_msg)
            raise DriverInitializationError(error_msg) from e

        # Determine actual driver executable path
        if os.path.isdir(driver_path):
            actual_path = os.path.join(driver_path, driver_name)
        elif os.path.basename(driver_path) == driver_name:
            actual_path = driver_path
        else:
            driver_dir = os.path.dirname(driver_path)
            actual_path = os.path.join(driver_dir, driver_name)

        # Verify driver exists
        if not os.path.exists(actual_path):
            error_msg = f"Driver executable not found at expected path: {actual_path}"
            logger.error(error_msg)
            raise DriverInitializationError(error_msg)

        # Ensure executable permissions
        if not os.access(actual_path, os.X_OK):
            try:
                os.chmod(actual_path, 0o755)
                logger.debug(f"Set executable permissions on {actual_path}")
            except OSError as e:
                logger.warning(f"Could not set executable permissions on {actual_path}: {e}")

        return actual_path

    @staticmethod
    def create_driver(browser: str, headless: bool = False,
                      browser_config: Optional[Dict[str, Any]] = None) -> webdriver.Remote:
        """Create and configure WebDriver instance.
        
        Args:
            browser: Browser name ('chrome', 'firefox'). Edge support planned for next release.
            headless: Run in headless mode
            browser_config: Browser-specific configuration dict
            
        Returns:
            WebDriver instance
            
        Raises:
            ValueError: If browser is not supported
            DriverInitializationError: If driver initialization fails
        """
        browser_config = browser_config or {}

        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless, browser_config)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless, browser_config)
        # TODO: Edge browser support planned for next release (v0.2.0)
        # elif browser == "edge":
        #     return DriverFactory._create_edge_driver(headless, browser_config)
        else:
            raise ValueError(
                f"Unsupported browser: {browser}. Supported browsers: chrome, firefox. Edge support coming in next release.")

    @staticmethod
    def _create_chrome_driver(headless: bool, config: Dict[str, Any]) -> webdriver.Chrome:
        """Create Chrome driver with configuration.
        
        Args:
            headless: Run in headless mode
            config: Browser configuration dict
            
        Returns:
            Chrome WebDriver instance
        """
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless=new")
            logger.info("Chrome running in headless mode with --headless=new")
        else:
            logger.info("Chrome running in normal (non-headless) mode")

        # Add browser arguments
        for arg in config.get("arguments", []):
            options.add_argument(arg)

        # Add preferences
        prefs = config.get("preferences", {})
        if prefs:
            options.add_experimental_option("prefs", prefs)

        logger.info(f"Chrome options: {options.arguments}")

        # Try PATH first, then webdriver-manager
        try:
            if DriverFactory._check_driver_in_path("chromedriver"):
                service = ChromeService()
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver_path = DriverFactory._get_driver_path(
                    ChromeDriverManager(), "chromedriver")
                service = ChromeService(driver_path)
                driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            error_msg = f"Failed to initialize Chrome driver: {e}"
            logger.error(error_msg)
            raise DriverInitializationError(error_msg) from e

        # Configure driver
        DriverFactory._configure_driver(driver, config)
        return driver

    @staticmethod
    def _create_firefox_driver(headless: bool, config: Dict[str, Any]) -> webdriver.Firefox:
        """Create Firefox driver with configuration.
        
        Args:
            headless: Run in headless mode
            config: Browser configuration dict
            
        Returns:
            Firefox WebDriver instance
        """
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")
            logger.info("Firefox running in headless mode")
        else:
            logger.info("Firefox running in normal (non-headless) mode")

        # Add browser arguments
        for arg in config.get("arguments", []):
            options.add_argument(arg)

        # Add preferences
        prefs = config.get("preferences", {})
        if prefs:
            for pref_key, pref_value in prefs.items():
                options.set_preference(pref_key, pref_value)

        logger.info(f"Firefox options: {options.arguments}")

        # Try PATH first, then webdriver-manager
        try:
            if DriverFactory._check_driver_in_path("geckodriver"):
                service = FirefoxService()
                driver = webdriver.Firefox(service=service, options=options)
            else:
                driver_path = DriverFactory._get_driver_path(
                    GeckoDriverManager(), "geckodriver")
                service = FirefoxService(driver_path)
                driver = webdriver.Firefox(service=service, options=options)
        except Exception as e:
            error_msg = f"Failed to initialize Firefox driver: {e}"
            logger.error(error_msg)
            raise DriverInitializationError(error_msg) from e

        # Configure driver
        DriverFactory._configure_driver(driver, config)
        return driver

    @staticmethod
    def _configure_driver(driver: webdriver.Remote, config: Dict[str, Any]) -> None:
        """Configure driver with window size and implicit wait.
        
        Args:
            driver: WebDriver instance to configure
            config: Browser configuration dict
        """
        try:
            # Set window size
            window_size = config.get("window_size", {})
            width = window_size.get("width", 1920)
            height = window_size.get("height", 1080)
            driver.set_window_size(width, height)
            logger.debug(f"Set window size to {width}x{height}")

            # Set implicit wait
            implicit_wait = config.get("implicit_wait", 10)
            driver.implicitly_wait(implicit_wait)
            logger.debug(f"Set implicit wait to {implicit_wait} seconds")
        except Exception as e:
            logger.warning(f"Error configuring driver settings: {e}")
            # Don't raise - driver is still usable with defaults
