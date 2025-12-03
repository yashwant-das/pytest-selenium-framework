from setuptools import setup, find_packages

setup(
    name="selenium-python-framework",
    version="0.1.0",
    description="A robust Selenium test automation framework with Python",
    author="Yashwant Das",
    author_email="yashworks@gmail.com",
    packages=find_packages(),
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: BDD",
    ],
) 