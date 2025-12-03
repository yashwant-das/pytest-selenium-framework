"""Logging configuration utility."""
import logging
import os
from typing import Optional
from datetime import datetime

def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with the specified name and level.
    
    Args:
        name: Name of the logger. If None, the root logger is configured.
        level: Logging level. Default is INFO.
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f'logs/test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    # Set levels
    console_handler.setLevel(level)
    file_handler.setLevel(level)
    
    # Create formatters
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                         datefmt='%Y-%m-%d %H:%M:%S')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    
    # Add formatters to handlers
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 