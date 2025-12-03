"""Custom exception classes for the framework."""


class DriverInitializationError(Exception):
    """Raised when driver initialization fails."""
    pass


class ConfigLoadError(Exception):
    """Raised when configuration file cannot be loaded."""
    pass

