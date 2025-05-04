"""
Tests for Tool class.
"""

import unittest
from unittest.mock import MagicMock, patch

import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.tools.base_tools import Tool

class TestTool(unittest.TestCase):
    """
    Test Tool class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create a mock function
        self.mock_function = MagicMock(return_value="Function result")
        
        # Create a tool
        self.tool = Tool(
            name="test_tool",
            description="A test tool",
            function=self.mock_function,
            args_schema={
                "arg1": {
                    "type": "string",
                    "description": "A string argument",
                    "required": True
                },
                "arg2": {
                    "type": "number",
                    "description": "A number argument",
                    "required": False
                }
            }
        )
    
    def test_init(self):
        """
        Test initialization.
        """
        self.assertEqual(self.tool.name, "test_tool")
        self.assertEqual(self.tool.description, "A test tool")
        self.assertEqual(self.tool.function, self.mock_function)
        self.assertEqual(len(self.tool.args_schema), 2)
        self.assertIn("arg1", self.tool.args_schema)
        self.assertIn("arg2", self.tool.args_schema)
    
    def test_call(self):
        """
        Test __call__ method.
        """
        # Call the tool with valid arguments
        result = self.tool({"arg1": "test", "arg2": 42})
        
        # Check that the function was called with the correct arguments
        self.mock_function.assert_called_once_with(arg1="test", arg2=42)
        
        # Check that the result is correct
        self.assertEqual(result, "Function result")
    
    def test_validate_args(self):
        """
        Test _validate_args method.
        """
        # Valid arguments
        self.tool._validate_args({"arg1": "test", "arg2": 42})
        
        # Missing required argument
        with self.assertRaises(ValueError):
            self.tool._validate_args({"arg2": 42})
        
        # Invalid argument type
        with self.assertRaises(ValueError):
            self.tool._validate_args({"arg1": "test", "arg2": "not a number"})
    
    def test_get_schema(self):
        """
        Test get_schema method.
        """
        schema = self.tool.get_schema()
        
        self.assertEqual(schema["name"], "test_tool")
        self.assertEqual(schema["description"], "A test tool")
        self.assertEqual(schema["args_schema"], self.tool.args_schema)
    
    def test_str(self):
        """
        Test __str__ method.
        """
        string = str(self.tool)
        
        self.assertEqual(string, "test_tool: A test tool")

if __name__ == "__main__":
    unittest.main()
