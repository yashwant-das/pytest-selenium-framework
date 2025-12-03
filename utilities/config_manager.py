"""Configuration manager for loading and caching all framework configurations."""
import os
import json
import logging
from typing import Dict, Any, Optional
from utilities.exceptions import ConfigLoadError

logger = logging.getLogger(__name__)


class ConfigManager:
    """Singleton configuration manager that loads and caches all configuration files."""
    
    _instance: Optional['ConfigManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Create singleton instance."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager and load all configs.
        
        This is a singleton class, so initialization only happens once.
        All configuration files are loaded and cached during first initialization.
        """
        if not self._initialized:
            self._base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._config: Dict[str, Any] = {}
            self._env_config: Dict[str, Any] = {}
            self._test_data: Dict[str, Any] = {}
            self._browser_config: Dict[str, Any] = {}
            self._load_all_configs()
            ConfigManager._initialized = True
            logger.debug("ConfigManager initialized and all configurations loaded")
    
    def _load_config_file(self, file_path: str, description: str) -> Dict[str, Any]:
        """Load a JSON configuration file.
        
        Args:
            file_path: Path to the JSON file
            description: Description of the config file for logging
            
        Returns:
            dict: Loaded configuration data
            
        Raises:
            ConfigLoadError: If file cannot be loaded
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {description} from {file_path}")
                    return data
            else:
                logger.warning(f"{description} file not found: {file_path}")
                return {}
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in {file_path}: {e}"
            logger.error(error_msg)
            raise ConfigLoadError(error_msg) from e
        except Exception as e:
            error_msg = f"Error loading {file_path}: {e}"
            logger.error(error_msg)
            raise ConfigLoadError(error_msg) from e
    
    def _load_all_configs(self) -> None:
        """Load all configuration files."""
        # Load main config.json
        config_path = os.path.join(self._base_dir, "config", "config.json")
        self._config = self._load_config_file(config_path, "main configuration")
        
        # Extract browser config from main config
        self._browser_config = self._config.get("browser", {})
        
        # Load environment configuration
        env_config_path = os.path.join(self._base_dir, "config", "environments.json")
        self._env_config = self._load_config_file(env_config_path, "environment configuration")
        
        # Load test data
        test_data_path = os.path.join(self._base_dir, "data", "fixtures.json")
        self._test_data = self._load_config_file(test_data_path, "test data")
    
    def get_config(self) -> Dict[str, Any]:
        """Get main configuration.
        
        Returns:
            dict: Main configuration from config.json
        """
        return self._config
    
    def get_browser_config(self, browser: Optional[str] = None) -> Dict[str, Any]:
        """Get browser-specific configuration.
        
        Args:
            browser: Browser name ('chrome', 'firefox'). If None, returns all browser configs.
            
        Returns:
            dict: Browser configuration. If browser is specified, returns that browser's config
                 merged with defaults. If None, returns all browser configurations.
                 
        Note:
            If a specific browser is requested but not found, a warning is logged and
            default values are used.
        """
        if browser:
            # Get browser-specific config, merge with defaults
            browser_specific = self._browser_config.get(browser, {})
            if not browser_specific and browser not in ['chrome', 'firefox']:
                logger.warning(f"Browser '{browser}' not found in configuration. Available browsers: {list(self._browser_config.keys())}")
            
            # Merge with default browser settings
            default_config = {
                "implicit_wait": self._browser_config.get("implicit_wait", 10),
                "arguments": [],
                "preferences": {},
                "window_size": self._browser_config.get("window_size", {"width": 1920, "height": 1080})
            }
            default_config.update(browser_specific)
            return default_config
        return self._browser_config
    
    def get_env_config(self, env: Optional[str] = None) -> Dict[str, Any]:
        """Get environment configuration.
        
        Args:
            env: Environment name ('dev', 'qa', 'staging', 'prod'). 
                 If None, returns default environment config.
                 
        Returns:
            dict: Environment configuration. Returns empty dict if environment not found.
            
        Note:
            If a specific environment is requested but not found, a warning is logged
            and an empty dict is returned.
        """
        if env:
            # Get specific environment config
            envs = self._env_config.get("environments", {})
            env_config = envs.get(env, {})
            if not env_config:
                logger.warning(f"Environment '{env}' not found in configuration. Available environments: {list(envs.keys())}")
            return env_config
        # Return default environment
        default_config = self._env_config.get("default", {})
        if not default_config:
            logger.warning("Default environment configuration not found")
        return default_config
    
    def get_test_data(self) -> Dict[str, Any]:
        """Get test data.
        
        Returns:
            dict: Test data from fixtures.json
        """
        return self._test_data
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Get all configurations in a single dict.
        
        This method is primarily used for backward compatibility with existing test fixtures.
        For new code, prefer using specific getter methods (get_config, get_env_config, etc.).
        
        Returns:
            dict: Dictionary with keys:
                - test_data: Test data from fixtures.json
                - env_config: Environment configurations
                - browser_config: Browser-specific configurations
        """
        return {
            "test_data": self._test_data,
            "env_config": self._env_config,
            "browser_config": self._browser_config
        }

