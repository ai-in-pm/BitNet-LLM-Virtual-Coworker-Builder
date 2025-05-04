"""
Tests for config_loader module.
"""

import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import tempfile
import yaml

import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.config.config_loader import load_config, save_config, get_config_value, set_config_value

class TestConfigLoader(unittest.TestCase):
    """
    Test config_loader module.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create a temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a test config
        self.test_config = {
            "server": {
                "host": "localhost",
                "port": 8000
            },
            "model": {
                "path": "models/test_model",
                "kernel_type": "i2_s"
            },
            "logging": {
                "level": "INFO"
            }
        }
    
    def tearDown(self):
        """
        Clean up test fixtures.
        """
        # Remove the temporary directory
        self.temp_dir.cleanup()
    
    def test_load_config(self):
        """
        Test load_config function.
        """
        # Create a test config file
        config_path = os.path.join(self.temp_dir.name, "config.yaml")
        with open(config_path, "w") as f:
            yaml.dump(self.test_config, f)
        
        # Load the config
        config = load_config(config_path)
        
        # Check that the config was loaded correctly
        self.assertEqual(config["server"]["host"], "localhost")
        self.assertEqual(config["server"]["port"], 8000)
        self.assertEqual(config["model"]["path"], "models/test_model")
        self.assertEqual(config["model"]["kernel_type"], "i2_s")
        self.assertEqual(config["logging"]["level"], "INFO")
        
        # Test loading a non-existent config file
        config = load_config("non_existent_config.yaml")
        self.assertEqual(config, {})
    
    def test_save_config(self):
        """
        Test save_config function.
        """
        # Save the config
        config_path = os.path.join(self.temp_dir.name, "config.yaml")
        result = save_config(self.test_config, config_path)
        
        # Check that the config was saved correctly
        self.assertTrue(result)
        self.assertTrue(os.path.exists(config_path))
        
        # Load the saved config
        with open(config_path, "r") as f:
            loaded_config = yaml.safe_load(f)
        
        # Check that the loaded config matches the original
        self.assertEqual(loaded_config, self.test_config)
        
        # Test saving to a non-existent directory
        result = save_config(self.test_config, "/non_existent_dir/config.yaml")
        self.assertFalse(result)
    
    def test_get_config_value(self):
        """
        Test get_config_value function.
        """
        # Test getting a value
        value = get_config_value(self.test_config, "server.host")
        self.assertEqual(value, "localhost")
        
        # Test getting a nested value
        value = get_config_value(self.test_config, "server.port")
        self.assertEqual(value, 8000)
        
        # Test getting a non-existent value
        value = get_config_value(self.test_config, "server.non_existent")
        self.assertIsNone(value)
        
        # Test getting a non-existent value with a default
        value = get_config_value(self.test_config, "server.non_existent", "default")
        self.assertEqual(value, "default")
        
        # Test getting a top-level value
        value = get_config_value(self.test_config, "server")
        self.assertEqual(value, {"host": "localhost", "port": 8000})
    
    def test_set_config_value(self):
        """
        Test set_config_value function.
        """
        # Test setting a value
        config = set_config_value(self.test_config.copy(), "server.host", "0.0.0.0")
        self.assertEqual(config["server"]["host"], "0.0.0.0")
        
        # Test setting a nested value
        config = set_config_value(self.test_config.copy(), "server.port", 9000)
        self.assertEqual(config["server"]["port"], 9000)
        
        # Test setting a non-existent value
        config = set_config_value(self.test_config.copy(), "server.non_existent", "value")
        self.assertEqual(config["server"]["non_existent"], "value")
        
        # Test setting a deeply nested value
        config = set_config_value(self.test_config.copy(), "server.nested.value", "nested_value")
        self.assertEqual(config["server"]["nested"]["value"], "nested_value")
        
        # Test setting a top-level value
        config = set_config_value(self.test_config.copy(), "new_key", "new_value")
        self.assertEqual(config["new_key"], "new_value")

if __name__ == "__main__":
    unittest.main()
