"""Setup configuration for pytest-selenium-framework."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="selenium-python-framework",
    version="0.1.0",
    description="A robust Selenium test automation framework with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yashwant Das",
    author_email="yashworks@gmail.com",
    url="https://github.com/yashwant-das/pytest-selenium-framework",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies
        "selenium>=4.31.0",
        "pytest>=8.0.2",
        # Pytest plugins
        "pytest-html>=4.1.1",
        "pytest-xdist>=3.5.0",
        "pytest-timeout>=2.2.0",
        "allure-pytest>=2.13.2",
        # WebDriver management
        "webdriver-manager>=4.0.1",
    ],
    keywords=[
        "selenium",
        "pytest",
        "test-automation",
        "web-testing",
        "browser-automation",
        "page-object-model",
        "test-framework",
        "qa",
        "testing",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Quality Engineers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: BDD",
        "Topic :: Software Development :: Quality Assurance",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yashwant-das/pytest-selenium-framework/issues",
        "Source": "https://github.com/yashwant-das/pytest-selenium-framework",
        "Documentation": "https://github.com/yashwant-das/pytest-selenium-framework#readme",
    },
    license="MIT",
) 