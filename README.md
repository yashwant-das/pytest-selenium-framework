# Selenium Test Automation Framework

A robust and maintainable test automation framework built with Python, Selenium, and pytest. This framework follows the Page Object Model (POM) design pattern and provides a comprehensive set of utilities for web application testing.

## Features

- **Page Object Model**: Organized page classes for better maintainability
- **Cross-Browser Testing**: Support for Chrome and Firefox browsers with auto-download capabilities (Edge support planned for next release)
- **Multi-Environment Support**: Built-in support for multiple environments (dev, qa, staging, prod) with easy switching
- **Headless Mode**: Run tests without opening browser windows
- **Parallel Execution**: Run tests in parallel with configurable worker count for faster execution
- **Multiple Report Formats**: HTML reports with screenshots and interactive Allure reports
- **Auto-Driver Management**: Automatic driver download with PATH detection fallback
- **Logging**: Comprehensive logging of test execution
- **Configuration Management**: Flexible configuration for different environments
- **Data-Driven Testing**: Support for external test data
- **Screenshot Capture**: Automatic screenshots on test failures with Allure integration

## Project Structure

```text
pytest-selenium-framework/
├── config/                  # Configuration files
│   ├── config.json          # Framework settings (browser, timeouts, reporting)
│   └── environments.json    # Environment-specific settings (dev, qa, staging, prod)
├── logs/                    # Log files (auto-generated)
│   └── test_run_*.log       # Test execution logs with timestamps
├── pages/                   # Page Object Model classes
│   ├── __init__.py          # Package initialization
│   ├── base_page.py         # Base page with common methods
│   └── selenium_page.py     # Selenium website page
├── reports/                 # Test reports (auto-generated)
│   ├── html/                # HTML reports with screenshots
│   ├── screenshots/         # Failure screenshots with error logs
│   ├── allure-results/      # Allure test results (raw data)
│   └── allure-report/       # Generated Allure HTML reports
├── data/                    # Test data files
│   └── fixtures.json        # Test data for data-driven tests
├── tests/                   # Test files
│   ├── conftest.py          # Pytest configuration and fixtures
│   └── test_framework_capabilities.py # Comprehensive test suite showcasing all framework features
├── utilities/               # Utility classes
│   ├── __init__.py          # Package initialization
│   ├── logger.py            # Logging configuration
│   ├── screenshot_helper.py # Screenshot capture utility
│   ├── driver_factory.py    # WebDriver factory for unified driver creation
│   ├── config_manager.py    # Configuration manager for loading and caching configs
│   └── exceptions.py        # Custom exception classes
├── examples/                # Example files
│   ├── __init__.py          # Package initialization
│   └── environment_usage_example.py # Example demonstrating environment configuration
├── requirements.txt         # Project dependencies
├── setup.py                 # Package setup script
├── pytest.ini               # Pytest configuration with Allure support
├── ROADMAP.md               # Planned features and roadmap
├── LICENSE                  # License file
└── README.md                # Project documentation
```

## Prerequisites

Before installing the framework, ensure you have:

- **Python 3.8+** (check with `python --version`)
- **pip** package manager
- **One or more browsers installed**:
  - Chrome/Chromium
  - Firefox

### Quick Setup Validation

After installation, you can verify your setup:

```bash
# Check Python version
python --version  # Should be 3.8+

# Verify packages installed
pip list | grep selenium
pip list | grep pytest

# Test driver availability (optional - drivers will auto-download if not in PATH)
chromedriver --version  # If installed via Homebrew
geckodriver --version   # If installed via Homebrew
```

If drivers aren't in PATH, the framework will automatically download them on first run using webdriver-manager.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yashwant-das/pytest-selenium-framework.git
   cd pytest-selenium-framework
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Browser Driver Setup:

   The framework supports multiple driver installation methods:

   **Option A: Automatic Download (Recommended)**
   - The framework automatically downloads drivers using webdriver-manager
   - No manual setup required for Chrome and Firefox

   **Option B: Manual Installation (More Reliable)**

   ```bash
   # macOS with Homebrew
   brew install chromedriver geckodriver
   ```

   **Option C: PATH Detection**
   - The framework first checks for drivers in your system PATH
   - Falls back to webdriver-manager if PATH drivers not found
   - Provides the most reliable driver resolution

## Usage

### Running Tests

**Basic Test Execution:**

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_framework_capabilities.py

# Run specific test class
pytest tests/test_framework_capabilities.py::TestPageObjectModel

# Run specific test method
pytest tests/test_framework_capabilities.py::TestPageObjectModel::test_page_object_navigation
```

**Browser Selection:**

```bash
# Run tests in Chrome (default)
pytest --browser chrome

# Run tests in Firefox
pytest --browser firefox
```

**Execution Modes:**

```bash
# Run tests in headless mode (faster, no UI)
pytest --headless

# Run tests in parallel (much faster for large test suites)
pytest -n 4

# Combine options for optimal performance
pytest --browser chrome --headless -n 4
```

**Test Filtering:**

```bash
# Run only smoke tests
pytest -m smoke

# Run only Chrome browser tests
pytest -m browser_chrome

# Run only parallel execution tests
pytest -m parallel

# Run tests excluding slow tests
pytest -m "not slow"
```

**Advanced Examples:**

```bash
# Full parallel execution with headless mode
pytest -n 4 --headless --browser chrome

# Cross-browser testing
pytest --browser chrome -m smoke
pytest --browser firefox -m smoke

# Run specific test class in parallel
pytest tests/test_framework_capabilities.py::TestParallelExecution -n 4
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--browser` | Browser to use (chrome, firefox) | `--browser firefox` |
| `--headless` | Run tests in headless mode | `--headless` |
| `-n` or `--numprocesses` | Number of parallel workers | `pytest -n 4` |
| `-m` | Run tests matching marker | `pytest -m smoke` |
| `-v` | Verbose output | `pytest -v` |
| `-k` | Run tests matching expression | `pytest -k "navigation"` |

**Performance Comparison:**

- Sequential execution: ~20 seconds for 7 tests
- Parallel execution (4 workers): ~10 seconds for 7 tests (50% faster)
- Headless mode: Additional 20-30% performance improvement

## Page Object Model

The framework follows the Page Object Model design pattern:

- **BasePage**: Contains common methods for all pages
- **Specific Pages**: Each page has its own class with specific locators and methods

Example:

```python
from pages.base_page import BasePage

class SeleniumPage(BasePage):
    # Page-specific locators
    LOCATORS = {
        "title": ("tag name", "h1"),
        "search_input": ("id", "searchbox"),
        "search_button": ("id", "search-button")
    }
    
    def search(self, query):
        """Perform a search on the page"""
        self.find_element(*self.LOCATORS["search_input"]).send_keys(query)
        self.find_element(*self.LOCATORS["search_button"]).click()
```

## Configuration

The framework uses a well-organized configuration structure split across multiple files for better maintainability:

### 1. Environment Configuration (`config/environments.json`)

This file manages environment-specific settings and supports multiple environments. The framework provides built-in support for environment switching without code changes.

**Current Configuration:**

```json
{
    "default": {
        "url": "https://www.selenium.dev",
        "description": "Default environment for demo purposes"
    },
    "environments": {
        "dev": {
            "url": "https://www.selenium.dev",
            "description": "Development environment"
        },
        "qa": {
            "url": "https://www.selenium.dev",
            "description": "QA testing environment"
        },
        "staging": {
            "url": "https://www.selenium.dev",
            "description": "Staging environment for pre-production testing"
        },
        "prod": {
            "url": "https://www.selenium.dev",
            "description": "Production environment"
        }
    }
}
```

**For Your Project:**

Update the URLs and add any environment-specific settings:

```json
{
    "default": {
        "url": "https://www.example.com",
        "api_key": "default_key"
    },
    "environments": {
        "dev": {
            "url": "https://dev.example.com",
            "api_key": "dev_key",
            "timeout": 30
        },
        "qa": {
            "url": "https://qa.example.com",
            "api_key": "qa_key",
            "timeout": 20
        },
        "staging": {
            "url": "https://staging.example.com",
            "api_key": "staging_key"
        },
        "prod": {
            "url": "https://www.example.com",
            "api_key": "prod_key"
        }
    }
}
```

**Accessing Environment Config:**

```python
from utilities.config_manager import ConfigManager

config_manager = ConfigManager()

# Get default environment
default = config_manager.get_env_config()

# Get specific environment
qa_config = config_manager.get_env_config("qa")
prod_config = config_manager.get_env_config("prod")
```

### 2. Framework Configuration (`config/config.json`)

This file contains browser-specific settings and configuration:

```json
{
  "browser": {
    "default": "chrome",
    "headless": false,
    "implicit_wait": 10,
    "window_size": {
      "width": 1920,
      "height": 1080
    },
    "chrome": {
      "arguments": ["--no-sandbox", "--disable-dev-shm-usage"],
      "preferences": {}
    },
    "firefox": {
      "arguments": [],
      "preferences": {}
    }
  }
}
```

**Configuration Options:**

- **default**: Default browser to use
- **headless**: Run browsers in headless mode by default
- **implicit_wait**: Default implicit wait time in seconds
- **window_size**: Default browser window size
- **chrome/firefox**: Browser-specific settings
  - **arguments**: List of browser command-line arguments
  - **preferences**: Browser preferences (Chrome) or options (Firefox)

### 3. Test Data (`data/fixtures.json`)

This file contains test-specific data used in data-driven tests. The structure is flexible and can be customized for your application:

```json
{
  "selenium": {
    "navigation": {
      "about": "About",
      "downloads": "Downloads",
      "documentation": "Documentation",
      "projects": "Projects",
      "support": "Support",
      "blog": "Blog"
    },
    "components": {
      "webdriver": "Selenium WebDriver",
      "ide": "Selenium IDE",
      "grid": "Selenium Grid"
    }
  }
}
```

**Usage in Tests:**

```python
from utilities.config_manager import ConfigManager

config_manager = ConfigManager()
test_data = config_manager.get_test_data()

# Access navigation items
nav_items = test_data["selenium"]["navigation"]

# Access components
components = test_data["selenium"]["components"]
```

**Customization:**
You can add any test data structure needed for your application. The framework loads this data and makes it available through the `test_data` fixture in your tests.

### Configuration Management

The framework's configuration is organized into three main categories:

1. **Framework Settings** (`config/config.json`)
   - Browser configuration (default, headless, implicit wait)
   - Window size settings
   - Browser-specific arguments and preferences

2. **Environment Settings** (`config/environments.json`)
   - Environment-specific URLs
   - Environment variables

3. **Test Data** (`data/fixtures.json`)
   - Test-specific data
   - Expected values
   - Test scenarios

This separation provides several benefits:

- Clear organization of different types of configuration
- Easy environment switching
- Simplified maintenance
- Better security for sensitive data
- Improved collaboration among team members

## Reports

The framework generates comprehensive test reports in multiple formats:

### HTML Reports

Standard pytest-html reports are automatically generated:

- **Location**: `reports/html/report.html`
- **Features**:
  - Test results summary
  - Screenshots on failure
  - Test execution time
  - Environment details
  - Browser information

### Allure Reports

Interactive Allure reports provide enhanced visualization:

**Generate and View Allure Reports:**

```bash
# Generate Allure report
allure generate reports/allure-results -o reports/allure-report --clean

# Serve interactive report
allure serve reports/allure-results
```

**Allure Features:**

- Interactive test result dashboard
- Test execution trends and history
- Screenshots and error logs attached to failed tests
- Test categorization and filtering
- Timeline view of test execution
- Environment and configuration details

**Sample Allure Commands:**

```bash
# View existing Allure report
allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report

# Open static report in browser (macOS)
open reports/allure-report/index.html
```

### Screenshots

Screenshots are automatically captured and attached to reports:

- **On Failure**: All failed tests automatically capture screenshots
- **Integration**: Screenshots are embedded in both HTML and Allure reports
- **Storage**: `reports/screenshots/` with timestamps and test names  
- **Error Logs**: Detailed error information saved alongside screenshots

## Test Data

Test data is stored in JSON files in the `data` directory:

```json
{
  "selenium": {
    "title": "Selenium",
    "navigation_items": ["Home", "About", "Documentation", "Support", "Blog"]
  },
  "browser_config": {
    "chrome": {
      "arguments": ["--no-sandbox", "--disable-dev-shm-usage"],
      "preferences": {
        "download.default_directory": "./downloads"
      }
    }
  }
}
```

## Logging

The framework provides comprehensive logging with automatic timestamping:

- **Test Execution Logs**: `logs/test_run_YYYYMMDD_HHMMSS.log`
- **Console Logging**: Real-time test execution information
- **Log Levels**: INFO, WARNING, ERROR with proper formatting

**Log Features:**

- Automatic log rotation with timestamps
- Detailed browser configuration logging
- Driver detection and initialization logs
- Test execution progress tracking

## Advanced Features

### Parallel Test Execution

The framework supports parallel test execution using pytest-xdist:

```bash
# Run tests with 4 parallel workers
pytest -n 4

# Optimal parallel execution with headless mode
pytest -n 4 --headless --browser chrome
```

**Benefits:**

- 50% faster execution with 4 workers
- Dynamic load balancing with work-stealing scheduling
- Independent browser sessions for each worker
- Automatic test distribution across workers

### Driver Management

Smart driver detection and management:

1. **PATH Detection**: Checks system PATH for installed drivers first
2. **Auto-Download**: Falls back to webdriver-manager for automatic download
3. **Version Compatibility**: Ensures driver-browser compatibility
4. **Cross-Platform**: Works on macOS, Windows, and Linux

### Environment Management

The framework supports multiple environment configurations through `config/environments.json`. This allows you to easily switch between different environments (dev, qa, staging, prod) without changing your test code.

**Example Usage:**

```python
from utilities.config_manager import ConfigManager

# Get default environment config
config_manager = ConfigManager()
default_env = config_manager.get_env_config()
print(default_env["url"])  # https://www.selenium.dev

# Get specific environment config
qa_env = config_manager.get_env_config("qa")
print(qa_env["url"])  # https://www.selenium.dev

# Use in your page objects
class MyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        env_config = ConfigManager().get_env_config("prod")
        self.url = env_config["url"]
```

**Configuration Structure:**

The `config/environments.json` file supports:

- **default**: Default environment configuration
- **environments**: Named environment configurations (dev, qa, staging, prod)
- Each environment can have its own URL, credentials, and other settings

**Benefits:**

- Easy environment switching without code changes
- Centralized environment configuration
- Support for environment-specific credentials and settings
- Clear separation between test code and environment configuration

### Directory Management

Required directories (logs, reports, screenshots) are automatically created when tests run. No manual setup needed.

## Troubleshooting

### Common Issues

**Driver Not Found Errors:**

- The framework will automatically download drivers if not found in PATH
- If auto-download fails, manually install drivers:

  ```bash
  # macOS
  brew install chromedriver geckodriver
  
  # Or download from browser vendor websites
  ```

**Browser Not Installed:**

- Ensure the browser is installed before running tests
- Tests will fail with clear error messages if browser is missing

**Import Errors:**

- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**Permission Issues:**

- On macOS/Linux, ensure drivers have execute permissions
- Framework automatically fixes permissions for auto-downloaded drivers

**Configuration Errors:**

- Verify `config/config.json` exists and is valid JSON
- Check `config/environments.json` and `data/fixtures.json` are valid

### Getting Help

If tests fail, check:

1. Log files in `logs/` directory for detailed error messages
2. Screenshots in `reports/screenshots/` for visual debugging
3. HTML/Allure reports for test execution details

The framework provides clear error messages to help diagnose issues quickly.

## Why Selenium in 2025?

While modern tools like Playwright have gained popularity, Selenium remains valuable:

- **Ecosystem Maturity**: Extensive community, documentation, and integrations
- **Enterprise Adoption**: Many organizations standardize on Selenium
- **Python Integration**: Excellent pytest integration and Python ecosystem support
- **Cross-Browser Support**: Proven support for Chrome and Firefox
- **Learning Value**: Demonstrates solid framework design patterns
- **Existing Infrastructure**: Works with existing Selenium Grid setups

This framework provides a production-ready, maintainable foundation for Selenium-based test automation.

## Framework Architecture

### Core Components

**DriverFactory** (`utilities/driver_factory.py`):

- Unified driver creation for all browsers
- Smart PATH detection with webdriver-manager fallback
- Consistent configuration handling

**ConfigManager** (`utilities/config_manager.py`):

- Singleton pattern for configuration loading
- Caches all configs to avoid repeated file reads
- Provides typed access to browser, environment, and test data configs

**ScreenshotHelper** (`utilities/screenshot_helper.py`):

- Centralized screenshot capture logic
- Automatic Allure and HTML report integration
- Support for failure and pass screenshots

**BasePage** (`pages/base_page.py`):

- Common page object methods with type hints
- Explicit waits and error handling
- Screenshot integration for debugging

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and upcoming releases.

**Next Release (v0.2.0):**

- Microsoft Edge browser support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Examples

The framework includes example files to help you get started:

### Environment Configuration Example

See `examples/environment_usage_example.py` for a complete example demonstrating:

- How to use `ConfigManager` to access environment configurations
- Creating environment-aware page objects
- Testing across multiple environments
- Pytest test patterns with environment support

Run the example:

```bash
python examples/environment_usage_example.py
```

This example shows practical usage patterns that you can adapt for your own test automation needs.
