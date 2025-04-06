# Selenium Python Test Framework

A robust and scalable test automation framework built with Python, Selenium, and pytest.

## Features

- Page Object Model design pattern
- Multi-browser support (Chrome, Firefox, Edge)
- Configurable test environments (DEV, QA, STAGING, UAT, PROD)
- HTML and Allure reporting
- Screenshot capture on test failure
- Email reporting
- Logging and error handling
- System check utility
- Cross-platform support

## Prerequisites

- Python 3.7 or higher
- Chrome, Firefox, or Edge browser
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd selenium-python-framework
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

4. Run system check:
```bash
python utilities/check_system.py
```

## System Check Utility

The framework includes a system check utility that verifies all prerequisites and dependencies before running tests. To use it:

```bash
python utilities/check_system.py
```

The utility checks:
- Python version
- Required packages
- Browser installations and drivers
- Directory structure
- Configuration files
- System requirements

Results are logged to both console and `system_check.log` file.

## Project Structure

```
selenium-python-framework/
├── config/                 # Configuration files
├── pages/                  # Page objects
│   ├── base_page.py       # Base page class
│   └── specific_pages/    # Page-specific classes
├── tests/                 # Test files
├── test_data/            # Test data files
├── utilities/            # Utility functions
├── reports/              # Test reports
│   ├── html/            # HTML reports
│   ├── screenshots/     # Failure screenshots
│   └── allure-results/  # Allure results
├── requirements.txt      # Python dependencies
└── pytest.ini           # pytest configuration
```

## Configuration

### Environment Configuration

The framework supports multiple environments:

```json
{
    "environment": {
        "default": "qa",
        "urls": {
            "dev": "https://github.com",
            "qa": "https://github.com",
            "staging": "https://github.com",
            "uat": "https://github.com",
            "prod": "https://github.com"
        }
    }
}
```

### Browser Configuration

```json
{
    "browser": {
        "default": "chrome",
        "headless": false,
        "implicit_wait": 10,
        "page_load_timeout": 30,
        "script_timeout": 30
    }
}
```

## Running Tests

1. Run all tests:
```bash
pytest
```

2. Run tests for a specific environment:
```bash
pytest --env=qa
```

3. Run tests with specific browser:
```bash
pytest --browser=chrome
```

4. Run tests with HTML report:
```bash
pytest --html=reports/html/report.html
```

## Page Objects

### Base Page

The `BasePage` class provides common functionality for all page objects:

```python
class BasePage:
    def find_element(self, by, value):
        """Find an element with explicit wait"""
        pass

    def click_element(self, by, value):
        """Click an element with explicit wait"""
        pass

    def send_keys(self, by, value, text):
        """Send keys to an element with explicit wait"""
        pass
```

### Example Page Object

```python
class GitHubPage(BasePage):
    # Locators
    SIGN_IN_BUTTON = (By.LINK_TEXT, "Sign in")
    USERNAME_INPUT = (By.ID, "login_field")
    
    def login(self, username, password):
        """Perform login"""
        pass
```

## Test Data

Test data is stored in JSON format:

```json
{
    "github": {
        "login": {
            "valid_credentials": {
                "username": "testuser",
                "password": "Test@123"
            }
        }
    }
}
```

## Reporting

### HTML Reports

HTML reports are generated in the `reports/html` directory and include:
- Test results
- Screenshots of failures
- Test execution details

### Allure Reports

Allure reports provide detailed test execution information:
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Best Practices

1. **Page Objects**
   - Keep locators at class level
   - Use meaningful method names
   - Implement reusable functions

2. **Test Data**
   - Store data in JSON files
   - Use environment-specific data
   - Keep sensitive data secure

3. **Configuration**
   - Use environment variables
   - Keep configurations separate
   - Document all settings

4. **Reporting**
   - Capture screenshots on failure
   - Use descriptive test names
   - Add test documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
