# Selenium Test Automation Framework

A robust and maintainable test automation framework built with Python, Selenium, and pytest. This framework follows the Page Object Model (POM) design pattern and provides a comprehensive set of utilities for web application testing.

## Features

- **Page Object Model**: Organized page classes for better maintainability
- **Cross-Browser Testing**: Support for Chrome, Firefox, and Edge browsers with auto-download capabilities
- **Headless Mode**: Run tests without opening browser windows
- **Parallel Execution**: Run tests in parallel with configurable worker count for faster execution
- **Multiple Report Formats**: HTML reports with screenshots and interactive Allure reports
- **Auto-Driver Management**: Automatic driver download with PATH detection fallback
- **System Checks**: Comprehensive environment verification before test execution
- **Logging**: Comprehensive logging of test execution and system checks
- **Configuration Management**: Flexible configuration for different environments
- **Data-Driven Testing**: Support for external test data
- **Screenshot Capture**: Automatic screenshots on test failures with Allure integration
- **Cleanup Management**: Optional cleanup of temporary files and previous test results

## Project Structure

```text
pytest-selenium-framework/
├── config/                  # Configuration files
│   └── config.json          # Browser and technical settings
├── logs/                    # Log files (auto-generated)
│   ├── system_check.log     # System check logs
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
├── test_data/               # Test data and environment config files
│   ├── default.json         # Environment-specific settings
│   └── test_data.json       # Test data for data-driven tests
├── tests/                   # Test files
│   ├── conftest.py          # Pytest configuration and fixtures
│   ├── test_selenium.py     # Basic Selenium website tests
│   ├── test_features.py     # Advanced feature tests
│   ├── test_parallel.py     # Parallel execution tests
│   └── test_webdriver_support.py # Comprehensive WebDriver capability tests
├── utilities/               # Utility classes
│   ├── __init__.py          # Package initialization
│   ├── logger.py            # Logging configuration
│   ├── screenshot_helper.py # Screenshot capture utility
│   └── system_check.py      # System environment check utility
├── venv/                    # Python virtual environment
├── run_system_check.py      # Script to run system checks
├── run_tests.py             # Main script to run tests with advanced options
├── test_all_features.sh     # Shell script for running all tests
├── requirements.txt         # Project dependencies
├── setup.py                 # Package setup script
├── pytest.ini               # Pytest configuration with Allure support
└── README.md                # Project documentation
```

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
   - Edge driver may require manual installation due to DNS issues

   **Option B: Manual Installation (More Reliable)**
   
   ```bash
   # macOS with Homebrew
   brew install chromedriver geckodriver
   
   # Add EdgeDriver manually to PATH
   # Download from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
   ```
   
   **Option C: PATH Detection**
   - The framework first checks for drivers in your system PATH
   - Falls back to webdriver-manager if PATH drivers not found
   - Provides the most reliable driver resolution

## Usage

### Enhanced Test Orchestrator Script

The framework includes a powerful `test_all_features.sh` script that provides comprehensive testing orchestration with professional-grade features:

#### Key Features

- **Colored Output**: Professional logging with color-coded status messages
- **Flexible Execution**: Command-line options for targeted testing
- **Error Tracking**: Comprehensive failure reporting and statistics
- **Auto-Detection**: Automatic Python executable detection (python3/python)
- **Performance Metrics**: Execution timing and detailed summaries
- **Environment Integration**: Optional system validation with skip capability

#### Usage Examples

```bash
# Run comprehensive testing (all browsers, all configurations)
./test_all_features.sh

# Quick testing (basic configurations only)
./test_all_features.sh --quick

# Browser-specific testing
./test_all_features.sh --chrome-only
./test_all_features.sh --firefox-only
./test_all_features.sh --edge-only

# CI/CD friendly (skip system check)
./test_all_features.sh --firefox-only --no-system-check

# Help and options
./test_all_features.sh --help
```

#### Command-Line Options

| Option | Description | Use Case |
|--------|-------------|----------|
| `--chrome-only` | Run only Chrome browser tests | Chrome-specific validation |
| `--firefox-only` | Run only Firefox browser tests | Firefox-specific validation |
| `--edge-only` | Run only Edge browser tests | Edge-specific validation |
| `--quick` | Run basic configurations only | Fast development testing |
| `--no-system-check` | Skip system environment validation | CI/CD pipelines |
| `--help` | Display usage information | Reference and documentation |

#### Test Configuration Matrix

**Quick Mode (--quick):**

- Browser normal mode
- Browser headless mode

**Full Mode (default):**

- Browser normal mode
- Browser headless mode  
- Parallel execution (2-3 workers)
- Headless + Parallel combinations
- Advanced configurations (4+ workers)
- Allure reporting integration
- Cleanup functionality testing

#### Example Output

```bash
[INFO] Starting comprehensive framework testing...
[INFO] === CHROME BROWSER TESTS ===
[SUCCESS] Test configuration passed: Chrome - Normal mode
[SUCCESS] Test configuration passed: Chrome - Headless mode
========================================
[INFO] TEST EXECUTION SUMMARY
========================================
Total Test Configurations: 8
Passed: 8
Failed: 0
Duration: 2m 45s
========================================
[SUCCESS] All test configurations passed!
```

### Running System Checks

Before running tests, verify that your environment is properly set up:

```bash
python run_system_check.py
```

The system check validates:

- Python version compatibility (3.7+)
- Required packages installation
- Browser installation (Chrome, Firefox, Edge)
- Driver availability (PATH detection + webdriver-manager fallback)
- Directory structure
- Driver functionality testing

**Sample Output:**
```text
✅ Python version 3.13.1 is compatible
✅ Package 'selenium' is installed
✅ Chrome browser is installed
✅ ChromeDriver version 138.0.7204.157 is available
✅ ChromeDriver is working correctly
✅ Firefox browser is installed
✅ GeckoDriver version 0.36.0 is available
✅ GeckoDriver is working correctly
✅ Edge browser is installed
✅ EdgeDriver version 138.0.3351.95 is available
✅ EdgeDriver is working correctly
✅ All system checks PASSED! The system is ready for automation
```

### Running Tests

**Basic Test Execution:**

```bash
# Run all tests
python run_tests.py

# Run specific test file
python run_tests.py --test-path tests/test_selenium.py

# Run specific test method
python run_tests.py --test-path tests/test_features.py::test_browser_support
```

**Browser Selection:**

```bash
# Run tests in Chrome (default)
python run_tests.py --browser chrome

# Run tests in Firefox
python run_tests.py --browser firefox

# Run tests in Edge
python run_tests.py --browser edge
```

**Execution Modes:**

```bash
# Run tests in headless mode (faster, no UI)
python run_tests.py --headless

# Run tests in parallel (much faster for large test suites)
python run_tests.py --parallel 4

# Combine options for optimal performance
python run_tests.py --browser chrome --headless --parallel 4
```

**Cleanup and System Options:**

```bash
# Clean previous results before running (fresh start)
python run_tests.py --clean

# Skip system check (faster startup)
python run_tests.py --skip-system-check

# Environment-specific testing
python run_tests.py --env qa
```

**Advanced Examples:**

```bash
# Full parallel execution with cleanup
python run_tests.py --test-path tests/test_features.py --parallel 4 --headless --clean

# Cross-browser testing
python run_tests.py --browser chrome --test-path tests/test_parallel.py
python run_tests.py --browser firefox --test-path tests/test_parallel.py  
python run_tests.py --browser edge --test-path tests/test_parallel.py
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--test-path` | Path to test file or directory | `--test-path tests/test_features.py` |
| `--browser` | Browser to use (chrome, firefox, edge) | `--browser firefox` |
| `--headless` | Run tests in headless mode | `--headless` |
| `--parallel` | Number of parallel workers | `--parallel 4` |
| `--skip-system-check` | Skip system check before running tests | `--skip-system-check` |
| `--clean` | Clean previous results and temp files | `--clean` |
| `--env` | Environment configuration to use | `--env staging` |

**Performance Comparison:**
- Sequential execution: ~20 seconds for 7 tests
- Parallel execution (4 workers): ~10 seconds for 7 tests (50% faster)
- Headless mode: Additional 20-30% performance improvement

### WebDriver Support Validation

The framework includes a comprehensive WebDriver capability test suite (`test_webdriver_support.py`) that validates all WebDriver functionality to ensure your testing environment is robust and reliable.

#### Test Coverage

The WebDriver support tests cover **35 test cases** across **8 major categories**:

**Core WebDriver Capabilities:**

- Driver initialization and session management
- Browser and platform detection
- Version compatibility validation

**Navigation & Interaction:**

- Page navigation (get, back, forward)
- Element finding strategies (by tag, class, ID, etc.)
- Element interaction (click, text access, form input)
- Link clicking and navigation validation

**Advanced Features:**

- JavaScript execution and interaction
- Window management (size, position, maximize)
- Cookie operations (add, get, delete)
- Screenshot capabilities (page and element-level)

**Waiting Mechanisms:**

- Implicit wait configuration
- Explicit wait with WebDriverWait
- Element state waiting (clickable, visible, present)

**Error Handling:**

- Exception handling validation
- Timeout management
- Invalid selector handling

**Performance & Integration:**

- Page load timing measurement
- Element finding performance
- Framework integration validation

#### WebDriver Test Usage

```bash
# Run WebDriver capability validation
python run_tests.py --test-path tests/test_webdriver_support.py

# Cross-browser WebDriver validation
python run_tests.py --test-path tests/test_webdriver_support.py --browser chrome
python run_tests.py --test-path tests/test_webdriver_support.py --browser firefox
python run_tests.py --test-path tests/test_webdriver_support.py --browser edge

# Quick WebDriver health check (headless mode)
python run_tests.py --test-path tests/test_webdriver_support.py --headless

# Performance-focused WebDriver validation
python run_tests.py --test-path tests/test_webdriver_support.py::TestPerformanceCapabilities
```

#### When to Run WebDriver Support Tests

**Recommended scenarios:**

- **Environment Setup**: When setting up new testing environments
- **Browser Updates**: After browser or driver updates
- **Troubleshooting**: When debugging WebDriver-related issues
- **CI/CD Validation**: As part of environment health checks
- **Framework Validation**: Before important test campaigns

**Sample Output:**

```bash
===== 35 passed in 66.40s =====
TestWebDriverCapabilities: ✓ All 4 tests passed
TestNavigationCapabilities: ✓ All 4 tests passed  
TestElementInteraction: ✓ All 4 tests passed
TestJavaScriptExecution: ✓ All 3 tests passed
TestWindowManagement: ✓ All 3 tests passed
TestErrorHandling: ✓ All 3 tests passed
```

This comprehensive validation ensures your WebDriver setup is production-ready and can handle all required automation scenarios.

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

### 1. Environment Configuration (`test_data/default.json`)

This file manages environment-specific settings and credentials. It supports multiple environments with their own configurations:

```json
{
    "default": {
        "url": "https://www.example.com",
        "username": "test_user",
        "password": "test_password"
    },
    "environments": {
        "dev": {
            "url": "https://dev.example.com",
            "username": "dev_user",
            "password": "dev_password"
        },
        "qa": {
            "url": "https://qa.example.com",
            "username": "qa_user",
            "password": "qa_password"
        },
        "staging": {
            "url": "https://staging.example.com",
            "username": "staging_user",
            "password": "staging_password"
        },
        "prod": {
            "url": "https://www.example.com",
            "username": "prod_user",
            "password": "prod_password"
        }
    }
}
```

### 2. Browser Configuration (`config/config.json`)

This file contains browser-specific settings and timeouts that remain constant across environments:

```json
{
  "browser": {
    "name": "chrome",
    "headless": false,
    "implicit_wait": 10
  },
  "timeouts": {
    "page_load": 30,
    "element_wait": 10
  }
}
```

### 3. Test Data (`test_data/test_data.json`)

This file contains test-specific data used in data-driven tests:

```json
{
  "selenium": {
    "title": "Selenium",
    "navigation_items": ["Home", "About", "Documentation", "Support", "Blog"]
  }
}
```

### Configuration Management

The framework's configuration is organized into three main categories:

1. **Environment Settings** (`test_data/default.json`)
   - Environment-specific URLs
   - User credentials
   - Other environment variables

2. **Technical Settings** (`config/config.json`)
   - Browser configuration
   - Timeout values
   - Other technical parameters

3. **Test Data** (`test_data/test_data.json`)
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

Test data is stored in JSON files in the `test_data` directory:

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

- **System Check Logs**: `logs/system_check.log`
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
python run_tests.py --parallel 4

# Optimal parallel execution with headless mode
python run_tests.py --parallel 4 --headless --browser chrome
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

Flexible environment configuration:

```bash
# Test against different environments
python run_tests.py --env dev
python run_tests.py --env staging  
python run_tests.py --env prod
```

### Cleanup Management

Optional cleanup for different use cases:

```bash
# Development: Preserve history for debugging
python run_tests.py

# CI/CD: Fresh start for consistent results  
python run_tests.py --clean
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Setup.py

The `setup.py` file is used to define metadata about the package and specify dependencies required for the package to run. It is essential for packaging Python projects, managing dependencies, and facilitating the installation and distribution of Python packages.

### Purpose for End Users

- **Easy Installation**: End users can easily install the package using pip. They simply need to run a command like `pip install selenium-python-framework` if the package is available on PyPI, or `pip install .` if they have downloaded the source code.
- **Dependency Management**: The `setup.py` file automatically handles the installation of all required dependencies. End users don't need to manually install each dependency; pip will take care of this for them.
- **Version Control**: The `setup.py` file specifies the version of the package, allowing users to know which version they are installing. This is useful for compatibility and troubleshooting.
- **Metadata**: It provides metadata about the package, such as the author, description, and supported Python versions. This information helps users understand what the package does and who maintains it.
- **Distribution**: If the package is distributed, `setup.py` is used to create distribution files that can be uploaded to PyPI. This makes it easy for users to find and install the package.
- **Customization**: Advanced users can customize the installation process by modifying the `setup.py` file, although this is less common for typical end users.
