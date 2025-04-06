import os
import sys
import subprocess
import platform
import json
import logging
import importlib.util
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

class SystemCheck:
    """System check utility for automation framework"""
    
    # Status Emojis
    STATUS_EMOJIS = {
        "pass": "✅",
        "fail": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "python": "🐍",
        "package": "📦",
        "browser": "🌐",
        "folder": "📁",
        "file": "📄",
        "os": "💻",
        "arch": "⚙️",
        "version": "🔢"
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system_info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": sys.version,
            "architecture": platform.machine()
        }
    
    def check_python_version(self):
        """Check if Python version meets requirements"""
        required_version = (3, 7)
        current_version = sys.version_info[:2]
        
        if current_version < required_version:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Python version {current_version} is not supported. Required version: {required_version}")
            return False
        
        self.logger.info(f"{self.STATUS_EMOJIS['pass']} Python version check passed: {sys.version}")
        return True
    
    def check_required_packages(self):
        """Check if all required packages are installed"""
        required_packages = [
            "selenium",
            "pytest",
            "webdriver_manager",
            "requests",
            "pytest_html",
            "allure_pytest"
        ]
        
        missing_packages = []
        for package in required_packages:
            spec = importlib.util.find_spec(package)
            if spec is None:
                missing_packages.append(package)
                self.logger.error(f"{self.STATUS_EMOJIS['fail']} Package {package} is not installed")
            else:
                self.logger.info(f"{self.STATUS_EMOJIS['pass']} Package {package} is installed")
        
        if missing_packages:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Missing packages: " + ", ".join(missing_packages))
            return False
        
        return True
    
    def check_browser_installation(self):
        """Check if required browsers are installed"""
        browsers = {
            "chrome": self._check_chrome,
            "firefox": self._check_firefox,
            "edge": self._check_edge
        }
        
        results = {}
        for browser, check_func in browsers.items():
            try:
                results[browser] = check_func()
            except Exception as e:
                self.logger.error(f"{self.STATUS_EMOJIS['fail']} Error checking {browser}: {str(e)}")
                results[browser] = False
        
        return results
    
    def _check_chrome(self):
        """Check Chrome installation and ChromeDriver"""
        try:
            # Try to get Chrome version
            if platform.system() == "Darwin":  # macOS
                process = subprocess.run(
                    ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                    capture_output=True,
                    text=True
                )
            elif platform.system() == "Windows":
                process = subprocess.run(
                    ["reg", "query", "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon", "/v", "version"],
                    capture_output=True,
                    text=True
                )
            else:  # Linux
                process = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
            
            chrome_version = process.stdout.strip()
            self.logger.info(f"{self.STATUS_EMOJIS['browser']} Chrome version: {chrome_version}")
            
            # Try to install/update ChromeDriver
            ChromeDriverManager().install()
            self.logger.info(f"{self.STATUS_EMOJIS['pass']} ChromeDriver is ready")
            
            return True
        except Exception as e:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Chrome check failed: {str(e)}")
            return False
    
    def _check_firefox(self):
        """Check Firefox installation and GeckoDriver"""
        try:
            # Try to get Firefox version
            if platform.system() == "Darwin":  # macOS
                process = subprocess.run(
                    ["/Applications/Firefox.app/Contents/MacOS/firefox", "--version"],
                    capture_output=True,
                    text=True
                )
            elif platform.system() == "Windows":
                process = subprocess.run(
                    ["reg", "query", "HKEY_CURRENT_USER\\Software\\Mozilla\\Firefox", "/v", "CurrentVersion"],
                    capture_output=True,
                    text=True
                )
            else:  # Linux
                process = subprocess.run(["firefox", "--version"], capture_output=True, text=True)
            
            firefox_version = process.stdout.strip()
            self.logger.info(f"{self.STATUS_EMOJIS['browser']} Firefox version: {firefox_version}")
            
            # Try to install/update GeckoDriver
            GeckoDriverManager().install()
            self.logger.info(f"{self.STATUS_EMOJIS['pass']} GeckoDriver is ready")
            
            return True
        except Exception as e:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Firefox check failed: {str(e)}")
            return False
    
    def _check_edge(self):
        """Check Edge installation and EdgeDriver"""
        try:
            # Try to get Edge version
            if platform.system() == "Windows":
                process = subprocess.run(
                    ["reg", "query", "HKEY_CURRENT_USER\\Software\\Microsoft\\Edge\\BLBeacon", "/v", "version"],
                    capture_output=True,
                    text=True
                )
                edge_version = process.stdout.strip()
                self.logger.info(f"{self.STATUS_EMOJIS['browser']} Edge version: {edge_version}")
                
                # Try to install/update EdgeDriver
                EdgeChromiumDriverManager().install()
                self.logger.info(f"{self.STATUS_EMOJIS['pass']} EdgeDriver is ready")
                
                return True
            else:
                self.logger.warning(f"{self.STATUS_EMOJIS['warning']} Edge browser check skipped - not supported on this OS")
                return False
        except Exception as e:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Edge check failed: {str(e)}")
            return False
    
    def check_directory_structure(self):
        """Check if required directories exist"""
        required_dirs = [
            "config",
            "pages",
            "tests",
            "test_data",
            "reports",
            "reports/screenshots",
            "reports/html",
            "reports/allure-results",
            "utilities"
        ]
        
        missing_dirs = []
        for directory in required_dirs:
            if not os.path.exists(directory):
                missing_dirs.append(directory)
                self.logger.error(f"{self.STATUS_EMOJIS['fail']} Directory {directory} does not exist")
            else:
                self.logger.info(f"{self.STATUS_EMOJIS['folder']} Directory {directory} exists")
        
        if missing_dirs:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Missing directories: " + ", ".join(missing_dirs))
            return False
        
        return True
    
    def check_configuration_files(self):
        """Check if configuration files exist and are valid"""
        required_files = [
            "config/config.json",
            "test_data/test_data.json",
            "pytest.ini"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
                self.logger.error(f"{self.STATUS_EMOJIS['fail']} File {file} does not exist")
            else:
                try:
                    with open(file, 'r') as f:
                        if file.endswith('.json'):
                            json.load(f)
                    self.logger.info(f"{self.STATUS_EMOJIS['file']} File {file} exists and is valid")
                except json.JSONDecodeError:
                    self.logger.error(f"{self.STATUS_EMOJIS['fail']} File {file} contains invalid JSON")
                    missing_files.append(file)
        
        if missing_files:
            self.logger.error(f"{self.STATUS_EMOJIS['fail']} Missing or invalid files: " + ", ".join(missing_files))
            return False
        
        return True
    
    def run_all_checks(self):
        """Run all system checks"""
        self.logger.info("\n" + "="*50)
        self.logger.info("🚀 Starting System Check")
        self.logger.info("="*50 + "\n")
        
        checks = {
            "Python Version": self.check_python_version(),
            "Required Packages": self.check_required_packages(),
            "Directory Structure": self.check_directory_structure(),
            "Configuration Files": self.check_configuration_files()
        }
        
        browser_checks = self.check_browser_installation()
        checks.update({f"Browser - {browser.capitalize()}": status 
                      for browser, status in browser_checks.items()})
        
        # Log system information
        self.logger.info("\n" + "="*50)
        self.logger.info("💻 System Information")
        self.logger.info("="*50)
        
        info_emojis = {
            "os": self.STATUS_EMOJIS["os"],
            "os_version": self.STATUS_EMOJIS["version"],
            "python_version": self.STATUS_EMOJIS["python"],
            "architecture": self.STATUS_EMOJIS["arch"]
        }
        
        for key, value in self.system_info.items():
            self.logger.info(f"{info_emojis.get(key, self.STATUS_EMOJIS['info'])} {key}: {value}")
        
        # Log check results
        self.logger.info("\n" + "="*50)
        self.logger.info("🎯 Check Results")
        self.logger.info("="*50)
        
        all_passed = True
        for check, passed in checks.items():
            status = "PASSED" if passed else "FAILED"
            emoji = self.STATUS_EMOJIS["pass"] if passed else self.STATUS_EMOJIS["fail"]
            self.logger.info(f"{emoji} {check}: {status}")
            if not passed:
                all_passed = False
        
        self.logger.info("\n" + "="*50)
        if all_passed:
            self.logger.info("🎉 All checks passed! System is ready for automation!")
        else:
            self.logger.error("⚠️  Some checks failed. Please fix the issues before running tests.")
        self.logger.info("="*50 + "\n")
        
        return all_passed 

if __name__ == "__main__":
    system_check = SystemCheck()
    success = system_check.run_all_checks()
    sys.exit(0 if success else 1) 