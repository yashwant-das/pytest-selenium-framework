"""
Example: Using Environment Configuration

This example demonstrates how to use the framework's multi-environment support
to switch between different environments without changing your test code.

Run this example:
    python examples/environment_usage_example.py
"""

from selenium import webdriver
from typing import Optional, Dict, Any

from pages.base_page import BasePage
from utilities.config_manager import ConfigManager


def example_environment_usage() -> None:
    """Example showing how to use environment configuration.
    
    This function demonstrates:
    - Getting default environment configuration
    - Getting specific environment configurations
    - Accessing environment-specific settings
    """
    # Initialize ConfigManager (singleton pattern)
    config_manager = ConfigManager()

    # Get default environment (returns config from "default" key)
    default_env = config_manager.get_env_config()
    print(f"Default Environment:")
    print(f"  URL: {default_env.get('url', 'Not configured')}")
    print(f"  Description: {default_env.get('description', 'N/A')}")
    print()

    # Get specific environment configurations
    environments = ["dev", "qa", "staging", "prod"]

    print("Environment Configurations:")
    for env_name in environments:
        env_config = config_manager.get_env_config(env_name)
        url = env_config.get('url', 'Not configured')
        description = env_config.get('description', 'N/A')
        print(f"  {env_name.upper()}:")
        print(f"    URL: {url}")
        print(f"    Description: {description}")
        print()


class EnvironmentAwarePage(BasePage):
    """Example page object that uses environment configuration.
    
    This class demonstrates how to create a page object that automatically
    uses the correct environment URL based on configuration.
    
    Example:
        >>> # Use default environment
        >>> page = EnvironmentAwarePage(driver)
        >>> page.navigate_to_environment()
        
        >>> # Use specific environment
        >>> page = EnvironmentAwarePage(driver, environment="qa")
        >>> page.navigate_to_environment()
    """

    def __init__(self, driver: webdriver.Remote, environment: Optional[str] = None):
        """Initialize page with environment-specific configuration.
        
        Args:
            driver: WebDriver instance
            environment: Environment name ('dev', 'qa', 'staging', 'prod').
                        If None, uses default environment from config.
        """
        super().__init__(driver)

        # Get environment-specific config
        config_manager = ConfigManager()
        env_config = config_manager.get_env_config(environment)

        # Use environment URL
        self.url = env_config.get("url", "https://www.selenium.dev")
        self.environment = environment or "default"
        self.env_description = env_config.get("description", "")

        # You can add other environment-specific settings
        self.timeout = env_config.get("timeout", 10)

    def navigate_to_environment(self) -> None:
        """Navigate to the environment-specific URL."""
        self.navigate_to(self.url)
        print(f"Navigated to {self.environment} environment: {self.url}")

    def get_environment_info(self) -> Dict[str, Any]:
        """Get current environment information.
        
        Returns:
            dict: Environment information including URL and description
        """
        return {
            "environment": self.environment,
            "url": self.url,
            "description": self.env_description,
            "timeout": self.timeout
        }


# Example usage in tests
def example_test_with_environment() -> None:
    """Example test showing environment switching.
    
    This demonstrates how you could use environment configuration in your tests.
    Note: This is a standalone example - actual tests would use pytest fixtures.
    """
    print("Example: Testing across multiple environments")
    print("=" * 50)

    # You can switch environments easily
    environments = ["dev", "qa", "staging", "prod"]
    config_manager = ConfigManager()

    for env in environments:
        print(f"\nTesting {env.upper()} environment...")
        config = config_manager.get_env_config(env)
        url = config.get('url', 'Not configured')
        description = config.get('description', 'N/A')

        print(f"  URL: {url}")
        print(f"  Description: {description}")

        # In actual tests, you would:
        # 1. Create driver (from pytest fixture)
        # 2. Create page object with environment
        # 3. Run your test logic
        # 
        # Example:
        # page = EnvironmentAwarePage(driver, environment=env)
        # page.navigate_to_environment()
        # assert page.is_navigation_visible()
        # ... your test assertions ...

    print("\n" + "=" * 50)
    print("Note: In actual pytest tests, use the driver fixture from conftest.py")
    print("Example pytest test:")
    print("""
    def test_login_across_environments(driver):
        \"\"\"Test login functionality across different environments.\"\"\"
        for env in ["dev", "qa", "staging"]:
            page = EnvironmentAwarePage(driver, environment=env)
            page.navigate_to_environment()
            # Your test logic here
    """)


def example_pytest_test_pattern() -> None:
    """Example showing pytest test pattern with environment configuration.
    
    This demonstrates the recommended pattern for using environments in pytest tests.
    """
    print("\n" + "=" * 50)
    print("Recommended Pytest Test Pattern:")
    print("=" * 50)
    print("""
import pytest
from examples.environment_usage_example import EnvironmentAwarePage

@pytest.mark.parametrize("environment", ["dev", "qa", "staging"])
def test_feature_across_environments(driver, environment):
    \"\"\"Test a feature across multiple environments.\"\"\"
    page = EnvironmentAwarePage(driver, environment=environment)
    page.navigate_to_environment()
    
    # Verify page loads
    assert page.is_navigation_visible()
    
    # Your test logic here
    # ...

# Or use environment from command line:
def test_with_environment_from_config(driver):
    \"\"\"Test using environment from configuration.\"\"\"
    from utilities.config_manager import ConfigManager
    
    config_manager = ConfigManager()
    # Get environment from config or use default
    env_config = config_manager.get_env_config()
    
    page = EnvironmentAwarePage(driver)
    page.navigate_to_environment()
    
    # Your test logic here
    # ...
    """)


if __name__ == "__main__":
    """Run examples when executed directly."""
    print("=" * 50)
    print("Environment Configuration Examples")
    print("=" * 50)
    print()

    # Example 1: Basic environment usage
    example_environment_usage()

    # Example 2: Testing across environments
    example_test_with_environment()

    # Example 3: Pytest test patterns
    example_pytest_test_pattern()

    print("\n" + "=" * 50)
    print("For more information, see README.md")
    print("=" * 50)
