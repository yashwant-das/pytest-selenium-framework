# Selenium Test Automation Framework

A robust and maintainable test automation framework built with Python, Selenium, and pytest. This framework follows the Page Object Model (POM) design pattern and provides a comprehensive set of utilities for web application testing.

## Features

- **Page Object Model**: Organized page classes for better maintainability
- **Cross-Browser Testing**: Support for Chrome, Firefox, and Edge browsers
- **Headless Mode**: Run tests without opening browser windows
- **HTML Reports**: Detailed test execution reports with screenshots
- **System Checks**: Environment verification before test execution
- **Logging**: Comprehensive logging of test execution and system checks
- **Configuration Management**: Flexible configuration for different environments
- **Data-Driven Testing**: Support for external test data

## Project Structure

```
pytest-selenium-framework/
├── config/                  # Configuration files
│   └── config.json          # Browser and technical settings
├── drivers/                 # Browser driver files
├── logs/                    # Log files
│   ├── system_check.log     # System check logs
│   └── test_execution.log   # Test execution logs
├── pages/                   # Page Object Model classes
│   ├── base_page.py         # Base page with common methods
│   └── selenium_page.py     # Selenium website page
├── reports/                 # Test reports
│   ├── html/                # HTML reports
│   └── screenshots/         # Failure screenshots
├── test_data/               # Test data and environment config files
│   ├── default.json         # Environment-specific settings
│   └── test_data.json       # Test data for data-driven tests
├── tests/                   # Test files
│   ├── conftest.py          # Pytest configuration and fixtures
│   └── test_selenium.py     # Selenium website tests
├── utilities/               # Utility classes
│   ├── screenshot_helper.py # Screenshot capture utility
│   └── system_check.py      # System environment check utility
├── .venv/                   # Python virtual environment
├── run_system_check.py      # Script to run system checks
├── run_tests.py             # Main script to run tests
├── test_all_features.sh     # Shell script for running all tests
├── requirements.txt         # Project dependencies
├── setup.py                 # Package setup script
├── pytest.ini              # Pytest configuration
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

4. Install browser drivers:
   - Chrome: The framework will automatically download the appropriate ChromeDriver
   - Firefox: Install GeckoDriver and add it to your PATH
   - Edge: Install EdgeDriver and add it to your PATH

## Usage

### Running System Checks

Before running tests, you can verify that your environment is properly set up:

```bash
python run_system_check.py
```

This will check:
- Python version
- Required packages
- Browser installation
- ChromeDriver availability
- Directory structure

### Running Tests

Run all tests:
```bash
python run_tests.py
```

Run specific test file:
```bash
python run_tests.py --test-path tests/test_selenium.py
```

Run tests in a specific browser:
```bash
python run_tests.py --browser chrome
```

Run tests in headless mode:
```bash
python run_tests.py --headless
```

Run tests in Edge browser:
```bash
python run_tests.py --browser edge
```

Skip system check:
```bash
python run_tests.py --skip-system-check
```

### Command Line Options

- `--test-path`: Path to test file or directory
- `--browser`: Browser to use (chrome, firefox, edge)
- `--headless`: Run tests in headless mode
- `--skip-system-check`: Skip system check before running tests

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

## Test Data

Test data is stored in JSON files in the `test_data` directory:

```json
{
  "selenium": {
    "title": "Selenium",
    "navigation_items": ["Home", "About", "Documentation", "Support", "Blog"]
  }
}
```

## Logging

The framework provides comprehensive logging:

- System check logs: `logs/system_check.log`
- Test execution logs: `logs/test_execution.log`

## Reports

After test execution, HTML reports are generated in the `reports/html` directory:

- Test results
- Screenshots on failure
- Test execution time
- Environment details

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
