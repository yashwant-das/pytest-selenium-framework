"""Custom exception classes for the framework.

This module defines custom exceptions used throughout the framework to provide
more specific error handling and clearer error messages.
"""

__all__ = ['DriverInitializationError', 'ConfigLoadError']


class DriverInitializationError(Exception):
    """Raised when WebDriver initialization fails.
    
    This exception is raised when there are issues creating or configuring
    a WebDriver instance, such as:
    - Driver executable not found
    - Driver download/installation failures
    - Browser startup errors
    - Configuration errors
    
    Examples:
        >>> try:
        ...     driver = DriverFactory.create_driver("chrome")
        ... except DriverInitializationError as e:
        ...     print(f"Failed to initialize driver: {e}")
    """
    pass


class ConfigLoadError(Exception):
    """Raised when configuration file cannot be loaded or parsed.
    
    This exception is raised when there are issues loading configuration files,
    such as:
    - Configuration file not found
    - Invalid JSON syntax
    - File permission errors
    - Encoding issues
    
    Examples:
        >>> try:
        ...     config = ConfigManager()
        ... except ConfigLoadError as e:
        ...     print(f"Failed to load configuration: {e}")
    """
    pass

