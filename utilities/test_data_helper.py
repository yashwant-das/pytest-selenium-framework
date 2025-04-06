import json
import os
from typing import Any, Dict, Optional
import logging

class TestDataHelper:
    def __init__(self, test_data_path: str = "test_data/test_data.json"):
        """
        Initialize TestDataHelper with path to test data file
        Args:
            test_data_path (str): Path to test data JSON file
        """
        self.logger = logging.getLogger(__name__)
        self.test_data_path = test_data_path
        self.test_data = self._load_test_data()

    def _load_test_data(self) -> Dict[str, Any]:
        """Load test data from JSON file"""
        try:
            with open(self.test_data_path) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load test data: {e}")
            raise

    def get_test_data(self, section: str, key: Optional[str] = None) -> Any:
        """
        Get test data for a specific section and key
        Args:
            section (str): Section name in test data
            key (str, optional): Key within the section
        Returns:
            Any: Test data value
        """
        try:
            if key:
                return self.test_data[section][key]
            return self.test_data[section]
        except KeyError as e:
            self.logger.error(f"Test data not found: {e}")
            raise

    def get_random_test_data(self, section: str, key: Optional[str] = None) -> Any:
        """
        Get random test data from a section
        Args:
            section (str): Section name in test data
            key (str, optional): Key within the section
        Returns:
            Any: Random test data value
        """
        import random
        try:
            data = self.get_test_data(section, key)
            if isinstance(data, list):
                return random.choice(data)
            return data
        except Exception as e:
            self.logger.error(f"Failed to get random test data: {e}")
            raise

    def update_test_data(self, section: str, key: str, value: Any) -> None:
        """
        Update test data with new value
        Args:
            section (str): Section name in test data
            key (str): Key within the section
            value (Any): New value to set
        """
        try:
            self.test_data[section][key] = value
            with open(self.test_data_path, 'w') as f:
                json.dump(self.test_data, f, indent=4)
        except Exception as e:
            self.logger.error(f"Failed to update test data: {e}")
            raise

    def get_test_data_by_index(self, section: str, index: int) -> Any:
        """
        Get test data by index from a section
        Args:
            section (str): Section name in test data
            index (int): Index of the data
        Returns:
            Any: Test data value at the specified index
        """
        try:
            data = self.get_test_data(section)
            if isinstance(data, list):
                return data[index]
            raise ValueError(f"Section {section} is not a list")
        except Exception as e:
            self.logger.error(f"Failed to get test data by index: {e}")
            raise 