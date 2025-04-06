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
        "selenium>=4.31.0",
        "pytest>=8.0.2",
        "pytest-html>=4.1.1",
        "pytest-xdist>=3.5.0",
        "allure-pytest>=2.13.2",
        "webdriver-manager>=4.0.1",
        "python-dotenv>=1.0.1",
        "pytest-rerunfailures>=12.0",
        "pytest-timeout>=2.2.0",
        "pytest-ordering>=0.6",
        "requests>=2.31.0",
        "colorama>=0.4.6",
        "setuptools>=65.5.1"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: BDD",
    ],
) 