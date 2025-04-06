from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import platform
import os

class DriverFactory:
    @staticmethod
    def get_driver(browser_name="chrome"):
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            
            # Handle Mac ARM64 architecture
            if platform.system() == "Darwin" and platform.machine() == "arm64":
                options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            
            # Let Selenium Manager handle driver compatibility
            return webdriver.Chrome(options=options)
        
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            return webdriver.Firefox(options=options)
        
        else:
            raise ValueError(f"Browser {browser_name} is not supported") 