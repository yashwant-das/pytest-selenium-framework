#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict, Any, Optional
from utilities.system_check import SystemCheck
from utilities.logger import setup_logger

# Configure logging
logger = setup_logger(__name__)

def setup_directories() -> None:
    """Create necessary directories if they don't exist.
    
    This function creates the following directories if they don't exist:
    - logs: For storing log files
    - reports: For storing test reports
    - reports/html: For storing HTML test reports
    - reports/screenshots: For storing test failure screenshots
    - reports/allure-results: For storing Allure test results
    """
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

def run_system_check() -> bool:
    """Run system check to verify environment.
    
    This function runs a system check to verify that the environment is ready for testing.
    It checks for the following:
    - Python version
    - Required packages
    - Browsers and drivers
    - Directory structure
    
    Returns:
        bool: True if all checks pass, False otherwise
    """
    logger.info("Running system check...")
    system_check = SystemCheck()
    if system_check.run():
        logger.info("System check passed successfully.")
        return True
    else:
        logger.error("System check failed. Please fix the issues before running tests.")
        return False

def run_tests(args: argparse.Namespace) -> bool:
    """Run the tests with the specified options.
    
    Args:
        args: Command line arguments parsed by argparse
        
    Returns:
        bool: True if tests pass, False otherwise
    """
    # Build pytest command
    pytest_cmd: List[str] = ["python", "-m", "pytest", "-v", "--html=reports/html/report.html", "--self-contained-html"]
    
    # Add headless flag if specified
    if args.headless:
        pytest_cmd.append("--headless")
        logger.info("Running tests in headless mode")
    
    # Add browser flag if specified
    if args.browser:
        pytest_cmd.append(f"--browser={args.browser}")
        logger.info(f"Running tests with browser: {args.browser}")
    
    # Add parallel execution flag if specified
    if args.parallel:
        pytest_cmd.append(f"-n={args.parallel}")
        logger.info(f"Running tests in parallel with {args.parallel} workers")
    
    if args.test_path:
        pytest_cmd.append(args.test_path)

    # Run pytest
    try:
        result = subprocess.run(pytest_cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Tests failed with return code: {e.returncode}")
        return False

def main() -> int:
    """Main function to run the tests.
    
    This function parses command line arguments, sets up directories, runs system check,
    and runs the tests with the specified options.
    
    Returns:
        int: 0 if tests pass, 1 if tests fail
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run Selenium tests with pytest")
    parser.add_argument("--test-path", help="Path to test file or directory")
    parser.add_argument("test_path", nargs="?", default="tests", help="Path to test file or directory (positional argument)")
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge"], help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", help="Run tests in headless mode")
    parser.add_argument("--skip-system-check", action="store_true", help="Skip system check")
    parser.add_argument("--parallel", type=int, help="Number of parallel workers for test execution")
    args = parser.parse_args()
    
    # Use --test-path if provided, otherwise use positional argument
    if args.test_path:
        test_path = args.test_path
    else:
        test_path = "tests"  # default value
    
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