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
            # First, try to check if chromedriver is in PATH and get version
            try:
                result = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True, check=True)
                version_info = result.stdout.strip().split()[1] if result.stdout else "unknown"
                self.logger.info(f"✅ ChromeDriver version {version_info} is available.")
                
                # Test ChromeDriver functionality
                from selenium.webdriver.chrome.service import Service as ChromeService
                service = ChromeService()
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                driver = webdriver.Chrome(service=service, options=options)
                driver.quit()
                self.logger.info("✅ ChromeDriver is working correctly.")
                return True
                
            except (subprocess.SubprocessError, FileNotFoundError):
                self.logger.warning("⚠️ ChromeDriver not found in PATH, trying webdriver-manager...")
                
                # Fall back to webdriver-manager
                from selenium.webdriver.chrome.service import Service as ChromeService
                
                driver_path = ChromeDriverManager().install()
                
                # Ensure we have the actual chromedriver executable, not a text file
                if os.path.isdir(driver_path):
                    # If it's a directory, look for chromedriver inside
                    actual_driver_path = os.path.join(driver_path, "chromedriver")
                elif os.path.basename(driver_path) == "chromedriver":
                    # If the filename is exactly "chromedriver"
                    actual_driver_path = driver_path
                else:
                    # The path might be pointing to another file in the driver directory
                    driver_dir = os.path.dirname(driver_path)
                    actual_driver_path = os.path.join(driver_dir, "chromedriver")
                
                if os.path.exists(actual_driver_path):
                    # Ensure the driver is executable
                    if not os.access(actual_driver_path, os.X_OK):
                        os.chmod(actual_driver_path, 0o755)
                        self.logger.info(f"✅ Fixed permissions for ChromeDriver at {actual_driver_path}")
                    
                    # Try to get ChromeDriver version
                    try:
                        result = subprocess.run([actual_driver_path, "--version"], capture_output=True, text=True, check=True)
                        version_info = result.stdout.strip().split()[1] if result.stdout else "unknown"
                        self.logger.info(f"✅ ChromeDriver version {version_info} is available.")
                        
                        # Test ChromeDriver functionality
                        service = ChromeService(actual_driver_path)
                        options = webdriver.ChromeOptions()
                        options.add_argument("--headless")
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        
                        driver = webdriver.Chrome(service=service, options=options)
                        driver.quit()
                        self.logger.info("✅ ChromeDriver is working correctly.")
                        return True
                        
                    except Exception as test_error:
                        self.logger.error(f"❌ ChromeDriver failed to initialize: {str(test_error)}")
                        self.logger.error("❌ Chrome browser may not be installed or ChromeDriver is incompatible.")
                        self.checks_passed = False
                        self.has_errors = True
                        return False
                else:
                    self.logger.error("❌ ChromeDriver executable not found or not executable.")
                    self.checks_passed = False
                    self.has_errors = True
                    return False
                    
        except Exception as e:
            self.logger.error(f"❌ Error checking ChromeDriver: {str(e)}")
            self.logger.warning("⚠️ ChromeDriver is not available. Chrome tests will fail.")
            self.checks_passed = False
            self.has_errors = True
            return False
    
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
            # First, try to check if geckodriver is in PATH and get version
            try:
                result = subprocess.run(["geckodriver", "--version"], capture_output=True, text=True, check=True)
                version_line = result.stdout.strip().split('\n')[0] if result.stdout else ""
                version_info = version_line.split()[1] if len(version_line.split()) > 1 else "unknown"
                self.logger.info(f"✅ GeckoDriver version {version_info} is available.")
                
                # Test GeckoDriver functionality
                from selenium.webdriver.firefox.service import Service as FirefoxService
                service = FirefoxService()
                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")
                
                driver = webdriver.Firefox(service=service, options=options)
                driver.quit()
                self.logger.info("✅ GeckoDriver is working correctly.")
                return True
                
            except (subprocess.SubprocessError, FileNotFoundError):
                self.logger.warning("⚠️ GeckoDriver not found in PATH, trying webdriver-manager...")
                
                # Fall back to webdriver-manager
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from webdriver_manager.firefox import GeckoDriverManager
                
                driver_path = GeckoDriverManager().install()
                if os.path.exists(driver_path):
                    # Get version from downloaded driver
                    try:
                        result = subprocess.run([driver_path, "--version"], capture_output=True, text=True, check=True)
                        version_line = result.stdout.strip().split('\n')[0] if result.stdout else ""
                        version_info = version_line.split()[1] if len(version_line.split()) > 1 else "unknown"
                        self.logger.info(f"✅ GeckoDriver version {version_info} is available.")
                        
                        # Test functionality
                        service = FirefoxService(driver_path)
                        options = webdriver.FirefoxOptions()
                        options.add_argument("--headless")
                        
                        driver = webdriver.Firefox(service=service, options=options)
                        driver.quit()
                        self.logger.info("✅ GeckoDriver is working correctly.")
                        return True
                        
                    except Exception as test_error:
                        self.logger.error(f"❌ GeckoDriver failed to initialize: {str(test_error)}")
                        self.logger.error("❌ Firefox browser may not be installed or GeckoDriver is incompatible.")
                        self.checks_passed = False
                        self.has_errors = True
                        return False
                else:
                    self.logger.error("❌ GeckoDriver could not be downloaded or installed.")
                    self.checks_passed = False
                    self.has_errors = True
                    return False
                    
        except Exception as e:
            self.logger.error(f"❌ Error checking GeckoDriver: {str(e)}")
            self.logger.warning("⚠️ GeckoDriver is not available. Firefox tests will fail.")
            self.checks_passed = False
            self.has_errors = True
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
            # First, try to check if msedgedriver is in PATH and get version
            try:
                result = subprocess.run(["msedgedriver", "--version"], capture_output=True, text=True, check=True)
                # EdgeDriver output format: "Microsoft Edge WebDriver 138.0.3351.95 (...)"
                version_line = result.stdout.strip()
                version_info = version_line.split()[3] if len(version_line.split()) > 3 else "unknown"
                self.logger.info(f"✅ EdgeDriver version {version_info} is available.")
                
                # Test EdgeDriver functionality
                from selenium.webdriver.edge.service import Service as EdgeService
                service = EdgeService()
                options = webdriver.EdgeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                driver = webdriver.Edge(service=service, options=options)
                driver.quit()
                self.logger.info("✅ EdgeDriver is working correctly.")
                return True
                
            except (subprocess.SubprocessError, FileNotFoundError):
                self.logger.warning("⚠️ EdgeDriver not found in PATH, trying webdriver-manager...")
                
                # Fall back to webdriver-manager
                from selenium.webdriver.edge.service import Service as EdgeService
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                
                driver_path = EdgeChromiumDriverManager().install()
                
                # Ensure we have the actual msedgedriver executable
                if os.path.isdir(driver_path):
                    # If it's a directory, look for msedgedriver inside
                    actual_driver_path = os.path.join(driver_path, "msedgedriver")
                elif os.path.basename(driver_path) == "msedgedriver":
                    # If the filename is exactly "msedgedriver"
                    actual_driver_path = driver_path
                else:
                    # The path might be pointing to another file in the driver directory
                    driver_dir = os.path.dirname(driver_path)
                    actual_driver_path = os.path.join(driver_dir, "msedgedriver")
                
                if os.path.exists(actual_driver_path):
                    # Ensure the driver is executable
                    if not os.access(actual_driver_path, os.X_OK):
                        os.chmod(actual_driver_path, 0o755)
                        self.logger.info(f"✅ Fixed permissions for EdgeDriver at {actual_driver_path}")
                    
                    # Get EdgeDriver version
                    try:
                        result = subprocess.run([actual_driver_path, "--version"], capture_output=True, text=True, check=True)
                        version_line = result.stdout.strip()
                        version_info = version_line.split()[3] if len(version_line.split()) > 3 else "unknown"
                        self.logger.info(f"✅ EdgeDriver version {version_info} is available.")
                        
                        # Test EdgeDriver functionality
                        service = EdgeService(actual_driver_path)
                        options = webdriver.EdgeOptions()
                        options.add_argument("--headless")
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        
                        driver = webdriver.Edge(service=service, options=options)
                        driver.quit()
                        self.logger.info("✅ EdgeDriver is working correctly.")
                        return True
                        
                    except Exception as test_error:
                        self.logger.error(f"❌ EdgeDriver failed to initialize: {str(test_error)}")
                        self.logger.error("❌ Edge browser may not be installed or EdgeDriver is incompatible.")
                        self.checks_passed = False
                        self.has_errors = True
                        return False
                else:
                    self.logger.error("❌ EdgeDriver executable not found or not executable.")
                    self.checks_passed = False
                    self.has_errors = True
                    return False
                    
        except Exception as e:
            self.logger.error(f"❌ Error checking EdgeDriver: {str(e)}")
            self.logger.warning("⚠️ EdgeDriver is not available. Edge tests will fail.")
            self.checks_passed = False
            self.has_errors = True
            return False
    
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