"""Logging configuration utility.

This module provides a centralized logging setup function that configures
loggers with both console and file handlers. It prevents duplicate handlers
and ensures consistent logging format across the framework.
"""
import logging
import os
from datetime import datetime
from typing import Optional

__all__ = ['setup_logger']


def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with the specified name and level.
    
    This function configures a logger with both console and file handlers.
    If the logger already has handlers configured, it will not add duplicate
    handlers to prevent log message duplication.
    
    Args:
        name: Name of the logger. If None, the root logger is configured.
        level: Logging level. Default is INFO.
        
    Returns:
        logging.Logger: Configured logger instance
        
    Note:
        The logs directory is created relative to the project root.
        Log files are named with timestamps: test_run_YYYYMMDD_HHMMSS.log
    """
    # Get project root directory (parent of utilities directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(project_root, 'logs')

    # Create logs directory if it doesn't exist
    try:
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir, exist_ok=True)
    except OSError as e:
        # If directory creation fails, log warning but continue
        # (pytest.ini may handle logging configuration)
        print(f"Warning: Could not create logs directory: {e}")

    # Create a logger
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create formatter (shared between handlers)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Create file handler with timestamp
    try:
        log_filename = f'test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        log_filepath = os.path.join(logs_dir, log_filename)
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
    except (OSError, IOError) as e:
        # If file handler creation fails, continue with console handler only
        print(f"Warning: Could not create log file: {e}")
        file_handler = None

    # Add handlers to logger
    logger.addHandler(console_handler)
    if file_handler:
        logger.addHandler(file_handler)

    return logger
