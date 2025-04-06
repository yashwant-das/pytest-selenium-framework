import os
import sys
import platform
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class SystemCheck:
    """Class to check if the system is ready for Selenium testing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.checks_passed = True
    
    def run(self):
        """Run all system checks"""
        self.logger.info("Starting system check...")
        
        # Check Python version
        self.check_python_version()
        
        # Check required packages
        self.check_required_packages()
        
        # Check Chrome browser
        self.check_chrome_browser()
        
        # Check ChromeDriver
        self.check_chromedriver()
        
        # Check directory structure
        self.check_directory_structure()
        
        # Log final result
        if self.checks_passed:
            self.logger.info("All system checks PASSED! The system is ready for automation.")
        else:
            self.logger.error("Some system checks FAILED! Please fix the issues before running tests.")
        
        return self.checks_passed
    
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
        elif system == "Darwin":  # macOS
            chrome_path = "/Applications/Google Chrome.app"
            if os.path.exists(chrome_path):
                self.logger.info("✅ Chrome browser is installed.")
            else:
                self.logger.error("❌ Chrome browser is not installed. Please install Chrome.")
                self.checks_passed = False
        elif system == "Linux":
            try:
                subprocess.run(["google-chrome", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.logger.info("✅ Chrome browser is installed.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.error("❌ Chrome browser is not installed. Please install Chrome.")
                self.checks_passed = False
        else:
            self.logger.warning(f"⚠️ Unsupported operating system: {system}. Chrome check skipped.")
    
    def check_chromedriver(self):
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
        except Exception as e:
            self.logger.error(f"❌ Failed to verify ChromeDriver: {str(e)}")
            self.checks_passed = False
    
    def check_directory_structure(self):
        """Check if required directories exist"""
        self.logger.info("Checking directory structure...")
        
        required_dirs = [
            "logs",
            "reports",
            "reports/html",
            "reports/screenshots",
            "test_data",
            "config"
        ]
        
        for directory in required_dirs:
            if os.path.exists(directory):
                self.logger.info(f"✅ Directory '{directory}' exists.")
            else:
                self.logger.warning(f"⚠️ Directory '{directory}' does not exist. It will be created when needed.")
                # Create the directory
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"✅ Created directory '{directory}'.") 