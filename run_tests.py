#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import logging
from datetime import datetime
from utilities.system_check import SystemCheck
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'logs',
        'reports',
        'reports/html',
        'reports/screenshots',
        'reports/allure-results'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

def run_system_check():
    """Run system check to verify environment"""
    logger.info("Running system check...")
    system_check = SystemCheck()
    if system_check.run():
        logger.info("System check passed successfully.")
        return True
    else:
        logger.error("System check failed. Please fix the issues before running tests.")
        return False

def run_tests(args):
    """Run the tests with the specified options"""
    # Set headless mode in config if specified
    if args.headless:
        config = load_config()
        config["browser"]["headless"] = True
        save_config(config)

    # Build pytest command
    pytest_cmd = ["python", "-m", "pytest", "-v", "--html=reports/html/report.html", "--self-contained-html"]
    if args.test_path:
        pytest_cmd.append(args.test_path)

    # Run pytest
    try:
        result = subprocess.run(pytest_cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logging.error(f"Tests failed with return code: {e.returncode}")
        return False

def load_config():
    """Load configuration from config.json"""
    with open('config/config.json', 'r') as f:
        return json.load(f)

def save_config(config):
    """Save configuration to config.json"""
    with open('config/config.json', 'w') as f:
        json.dump(config, f, indent=4)

def main():
    """Main function to run the tests"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Selenium tests with pytest")
    parser.add_argument("--test-path", help="Path to test file or directory")
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    parser.add_argument("--skip-system-check", action="store_true", help="Skip system check")
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    # Run system check unless skipped
    if not args.skip_system_check:
        if not run_system_check():
            return 1
    
    # Run tests
    success = run_tests(args)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 