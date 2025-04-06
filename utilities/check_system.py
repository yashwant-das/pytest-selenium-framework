#!/usr/bin/env python3
import logging
import sys
from system_check import SystemCheck

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('system_check.log')
        ]
    )

def main():
    """Main function to run system checks"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting system check...")
    checker = SystemCheck()
    
    try:
        if checker.run_all_checks():
            logger.info("\nAll system checks PASSED! The system is ready for automation.")
            sys.exit(0)
        else:
            logger.error("\nSome system checks FAILED! Please fix the issues before running tests.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error during system check: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 