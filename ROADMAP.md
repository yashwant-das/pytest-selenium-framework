# Roadmap

This document outlines the planned features and future development direction for the pytest-selenium-framework.

## Current Version (v0.1.0)

The current version includes:

- ✅ Chrome and Firefox browser support
- ✅ Page Object Model (POM) implementation
- ✅ Multi-environment configuration support
- ✅ Headless mode execution
- ✅ Parallel test execution
- ✅ HTML and Allure reporting
- ✅ Automatic driver management
- ✅ Screenshot capture on failures
- ✅ Comprehensive logging
- ✅ Data-driven testing support

## Upcoming Features

### Next Release (v0.2.0)

#### Edge Browser Support

- **Status**: Planned
- **Priority**: High
- **Description**: Add Microsoft Edge browser support to the framework
- **Implementation Notes**:
    - Add Edge driver factory method in `utilities/driver_factory.py`
    - Add Edge configuration to `config/config.json`
    - Add Edge test case in `tests/test_framework_capabilities.py`
    - Update documentation and examples
    - Add Edge browser marker in `pytest.ini`

---

## Future Considerations

### Potential Features (No Timeline)

- **Safari Browser Support**: Add Safari browser support for macOS testing
- **Mobile Browser Testing**: Support for mobile web browser testing
- **Enhanced Reporting**: Additional report formats and analytics
- **CI/CD Integration**: Examples and templates for popular CI/CD platforms
- **Test Data Management**: Enhanced test data management and external data sources
- **Visual Regression Testing**: Integration with visual testing tools
- **API Testing Support**: Add API testing capabilities alongside UI tests

### Long-term Vision

- Framework extensibility improvements
- Plugin system for custom functionality
- Enhanced documentation and tutorials
- Community contributions and examples
