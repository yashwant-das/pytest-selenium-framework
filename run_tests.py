#!/usr/bin/env python3
import os
import sys
import logging
import subprocess
import argparse

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/test_execution.log')
        ]
    )

def run_system_check():
    """Run system check before tests"""
    logger = logging.getLogger(__name__)
    logger.info("Running system check...")
    
    try:
        result = subprocess.run(['python', 'run_system_check.py'], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error("System check failed. Please fix the issues before running tests.")
            logger.error(result.stdout)
            logger.error(result.stderr)
            return False
        
        logger.info("System check passed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error running system check: {str(e)}")
        return False

def run_tests(test_path=None, browser=None, headless=False):
    """Run tests with specified parameters"""
    logger = logging.getLogger(__name__)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    # Add test path if specified
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append('tests')
    
    # Add browser option if specified
    if browser:
        cmd.extend(['--browser', browser])
    
    # Add headless option if specified
    if headless:
        cmd.extend(['--headless'])
    
    # Add verbose flag
    cmd.append('-v')
    
    # Add HTML report
    cmd.extend(['--html=reports/html/report.html', '--self-contained-html'])
    
    # Log the command
    logger.info(f"Running tests with command: {' '.join(cmd)}")
    
    # Run the tests
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Log the output
        logger.info(result.stdout)
        
        if result.stderr:
            logger.error(result.stderr)
        
        # Check the return code
        if result.returncode != 0:
            logger.error(f"Tests failed with return code: {result.returncode}")
            return False
        
        logger.info("Tests completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        return False

def main():
    """Main function to run tests"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Selenium tests')
    parser.add_argument('--test-path', help='Path to test file or directory')
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'edge'], 
                        help='Browser to run tests')
    parser.add_argument('--headless', action='store_true', 
                        help='Run tests in headless mode')
    parser.add_argument('--skip-system-check', action='store_true', 
                        help='Skip system check before running tests')
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Run system check if not skipped
    if not args.skip_system_check:
        if not run_system_check():
            logger.error("Exiting due to system check failure.")
            sys.exit(1)
    
    # Run tests
    if not run_tests(args.test_path, args.browser, args.headless):
        logger.error("Tests failed.")
        sys.exit(1)
    
    logger.info("All tests completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main() 