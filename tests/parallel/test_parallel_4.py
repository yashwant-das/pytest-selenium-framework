import pytest
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_parallel_4(driver, test_data):
    """Test parallel execution 4"""
    url = test_data["env_config"]["default"]["url"]
    driver.get(url)
    
    # Simulate a slow operation with random duration
    start_time = time.time()
    sleep_time = random.uniform(2, 4)  # Random sleep between 2-4 seconds
    time.sleep(sleep_time)
    end_time = time.time()
    
    # Log the execution time and session ID
    execution_time = end_time - start_time
    session_id = driver.capabilities.get('sessionId', 'unknown')
    worker_id = driver.capabilities.get('workerId', 'unknown')
    print(f"\nTest parallel_4 execution time: {execution_time:.2f} seconds")
    print(f"Browser session ID: {session_id}")
    print(f"Worker ID: {worker_id}")
    
    # Verify the page loaded correctly
    assert "Selenium" in driver.title, "Page title should contain 'Selenium'"
    assert "WebDriver" in driver.page_source, "Page should contain WebDriver text" 