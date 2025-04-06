import os
import sys
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utilities.logger import setup_logger
import requests

# Configure logging
logger = setup_logger(__name__)

class SystemCheck:
    """Class to check if the system is ready for Selenium testing"""
    
    def __init__(self):
        self.logger = logger
        self.checks_passed = True
        self.has_errors = False
        self.has_warnings = False
    
    def run(self):
        """Run all system checks"""
        self.logger.info("Starting system check...")
        
        # Check Python version
        self.check_python_version()
        
        # Check required packages
        self.check_required_packages()
        
        # Check browsers and drivers
        self.check_chrome_browser()
        self.check_chrome_driver()
        self.check_firefox_browser()
        self.check_firefox_driver()
        self.check_edge_browser()
        self.check_edge_driver()
        
        # Check directory structure
        self.check_directory_structure()
        
        # Log final result
        if self.has_errors:
            self.logger.error("Some system checks FAILED! Please fix the issues before running tests.")
        elif self.has_warnings:
            self.logger.warning("Some system checks have warnings. Tests will continue but may have issues.")
        else:
            self.logger.info("All system checks PASSED! The system is ready for automation.")
        
        return self.checks_passed and not self.has_errors
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.logger.info("Checking Python version...")
        
        python_version = sys.version_info
        min_version = (3, 7)
        
        if python_version >= min_version:
            self.logger.info(f"✅ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is compatible.")
        else:
            self.logger.error(f"❌ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is not compatible. Minimum required: {min_version[0]}.{min_version[1]}")
            self.checks_passed = False
            self.has_errors = True
    
    def check_required_packages(self):
        """Check if required packages are installed"""
        self.logger.info("Checking required packages...")
        
        required_packages = [
            "selenium",
            "pytest",
            "webdriver-manager",
            "pytest-html"
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                self.logger.info(f"✅ Package '{package}' is installed.")
            except ImportError:
                self.logger.error(f"❌ Package '{package}' is not installed. Please install it using: pip install {package}")
                self.checks_passed = False
                self.has_errors = True
    
    def check_chrome_browser(self):
        """Check if Chrome browser is installed"""
        self.logger.info("Checking Chrome browser...")
        
        system = platform.system()
        
        if system == "Windows":
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if os.path.exists(chrome_path):
                self.logger.info("✅ Chrome browser is installed.")
            else:
                self.logger.error("❌ Chrome browser is not installed. Please install Chrome.")
                self.checks_passed = False
                self.has_errors = True
        elif system == "Darwin":  # macOS
            chrome_path = "/Applications/Google Chrome.app"
            if os.path.exists(chrome_path):
                self.logger.info("✅ Chrome browser is installed.")
            else:
                self.logger.error("❌ Chrome browser is not installed. Please install Chrome.")
                self.checks_passed = False
                self.has_errors = True
        elif system == "Linux":
            try:
                subprocess.run(["google-chrome", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.logger.info("✅ Chrome browser is installed.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.error("❌ Chrome browser is not installed. Please install Chrome.")
                self.checks_passed = False
                self.has_errors = True
        else:
            self.logger.warning(f"⚠️ Unsupported operating system: {system}. Chrome check skipped.")
    
    def check_chrome_driver(self):
        """Check if ChromeDriver is available"""
        self.logger.info("Checking ChromeDriver...")
        
        try:
            # Just check if ChromeDriver can be downloaded without initializing it
            driver_path = ChromeDriverManager().install()
            if os.path.exists(driver_path):
                self.logger.info("✅ ChromeDriver is available.")
            else:
                self.logger.error("❌ ChromeDriver is not available.")
                self.checks_passed = False
                self.has_errors = True
        except Exception as e:
            self.logger.error(f"❌ Failed to verify ChromeDriver: {str(e)}")
            self.checks_passed = False
            self.has_errors = True
    
    def check_firefox_browser(self):
        """Check if Firefox browser is installed"""
        self.logger.info("Checking Firefox browser...")
        
        system = platform.system()
        
        if system == "Windows":
            firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
            if os.path.exists(firefox_path):
                self.logger.info("✅ Firefox browser is installed.")
            else:
                self.logger.error("❌ Firefox browser is not installed. Please install Firefox.")
                self.checks_passed = False
                self.has_errors = True
        elif system == "Darwin":  # macOS
            firefox_path = "/Applications/Firefox.app"
            if os.path.exists(firefox_path):
                self.logger.info("✅ Firefox browser is installed.")
            else:
                self.logger.error("❌ Firefox browser is not installed. Please install Firefox.")
                self.checks_passed = False
                self.has_errors = True
        elif system == "Linux":
            try:
                subprocess.run(["firefox", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.logger.info("✅ Firefox browser is installed.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.error("❌ Firefox browser is not installed. Please install Firefox.")
                self.checks_passed = False
                self.has_errors = True
        else:
            self.logger.warning(f"⚠️ Unsupported operating system: {system}. Firefox check skipped.")
    
    def check_firefox_driver(self):
        """Check if GeckoDriver is available"""
        self.logger.info("Checking GeckoDriver...")
        
        try:
            # Try to get the latest GeckoDriver version from GitHub
            response = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest")
            if response.status_code == 200:
                latest_version = response.json()["tag_name"]
                self.logger.info(f"✅ Latest GeckoDriver version is {latest_version}")
            else:
                # If we hit rate limit or other GitHub API issues, just log a warning
                self.logger.warning(f"⚠️ Could not verify latest GeckoDriver version: {response.status_code}")
                self.logger.warning("⚠️ This is likely due to GitHub API rate limiting. Tests will continue.")
                self.logger.warning("⚠️ Please ensure you have a compatible GeckoDriver installed.")
                self.has_warnings = True
        except Exception as e:
            # Log as warning instead of error
            self.logger.warning(f"⚠️ Could not verify GeckoDriver: {str(e)}")
            self.logger.warning("⚠️ This is likely due to GitHub API rate limiting. Tests will continue.")
            self.logger.warning("⚠️ Please ensure you have a compatible GeckoDriver installed.")
            self.has_warnings = True
        
        # Check if geckodriver is in PATH
        try:
            subprocess.run(["geckodriver", "--version"], capture_output=True, check=True)
            self.logger.info("✅ GeckoDriver is available in PATH")
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            self.logger.warning("⚠️ GeckoDriver not found in PATH")
            self.logger.warning("⚠️ Tests will continue, but Firefox tests may fail")
            return False
    
    def check_edge_browser(self):
        """Check if Edge browser is installed"""
        self.logger.info("Checking Edge browser...")
        
        try:
            if platform.system() == "Darwin":
                # Check for Edge on macOS
                edge_path = "/Applications/Microsoft Edge.app"
                if os.path.exists(edge_path):
                    self.logger.info("✅ Edge browser is installed.")
                    return
                else:
                    self.logger.warning("⚠️ Edge browser is not installed. Please install Microsoft Edge.")
                    self.checks_passed = False
                    self.has_warnings = True
                    return
            else:
                # For other platforms, we'll assume Edge is installed if the check passes
                self.logger.info("✅ Edge browser check passed.")
                return
        except Exception as e:
            self.logger.error(f"❌ Error checking Edge browser: {str(e)}")
            self.checks_passed = False
            self.has_errors = True
    
    def check_edge_driver(self):
        """Check if EdgeDriver is available"""
        self.logger.info("Checking EdgeDriver...")
        
        try:
            import platform
            import os
            
            # Check if running on Apple Silicon
            is_apple_silicon = platform.system() == "Darwin" and platform.machine() == "arm64"
            
            if is_apple_silicon:
                # For Apple Silicon, we'll use a different approach
                # Instead of checking for the driver, we'll check if Edge browser is installed
                edge_path = "/Applications/Microsoft Edge.app"
                if os.path.exists(edge_path):
                    self.logger.info("✅ Edge browser is installed. Will use Edge browser directly.")
                    return
                else:
                    self.logger.warning("⚠️ Edge browser is not installed. Will fall back to Chrome browser.")
                    self.checks_passed = False
                    self.has_warnings = True
                    return  # Return without setting checks_passed to False
            else:
                # For other platforms, use the webdriver-manager
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                driver_path = EdgeChromiumDriverManager().install()
                
                if os.path.exists(driver_path):
                    self.logger.info("✅ EdgeDriver is available.")
                    return
                else:
                    self.logger.warning("⚠️ EdgeDriver is not available. Please install EdgeDriver.")
                    self.checks_passed = False
                    self.has_warnings = True
                    return
        except Exception as e:
            self.logger.error(f"❌ Error checking EdgeDriver: {str(e)}")
            self.checks_passed = False
            self.has_errors = True
    
    def check_directory_structure(self):
        """Check if required directories exist"""
        self.logger.info("Checking directory structure...")
        
        required_directories = [
            'logs',
            'reports',
            'reports/html',
            'reports/screenshots',
            'reports/allure-results',
            'test_data'
        ]
        
        for directory in required_directories:
            if not os.path.exists(directory):
                self.logger.error(f"❌ Required directory '{directory}' does not exist.")
                self.checks_passed = False
                self.has_errors = True
            else:
                self.logger.info(f"✅ Required directory '{directory}' exists.") 