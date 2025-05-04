"""
Tests for BitNetModel class.
"""

import unittest
from unittest.mock import MagicMock, patch

import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel

class TestBitNetModel(unittest.TestCase):
    """
    Test BitNetModel class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create model with mock implementation
        self.model = BitNetModel(
            model_path="models/test_model",
            kernel_type="i2_s",
            use_bitnet_integration=False
        )
    
    def test_init(self):
        """
        Test initialization.
        """
        self.assertEqual(self.model.model_path, "models/test_model")
        self.assertEqual(self.model.kernel_type, "i2_s")
        self.assertFalse(self.model.use_bitnet_integration)
        self.assertEqual(self.model.num_threads, 4)
        self.assertEqual(self.model.context_size, 2048)
        self.assertEqual(self.model.temperature, 0.7)
        self.assertEqual(self.model.top_p, 0.9)
        self.assertEqual(self.model.top_k, 40)
        self.assertEqual(self.model.repetition_penalty, 1.1)
    
    def test_generate(self):
        """
        Test generate method.
        """
        # Test with default parameters
        result = self.model.generate("Test prompt")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        # Test with custom parameters
        result = self.model.generate(
            prompt="Test prompt",
            max_tokens=100,
            temperature=0.5,
            top_p=0.8,
            top_k=20,
            repetition_penalty=1.2
        )
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_mock_generate(self):
        """
        Test _mock_generate method.
        """
        # Test with search prompt
        result = self.model._mock_generate("Search for climate change", 100)
        self.assertIn("Action: search", result)
        
        # Test with analyze prompt
        result = self.model._mock_generate("Analyze this data", 100)
        self.assertIn("Action: analyze", result)
        
        # Test with summarize prompt
        result = self.model._mock_generate("Summarize this information", 100)
        self.assertIn("Final Answer:", result)
        
        # Test with other prompt
        result = self.model._mock_generate("Some other prompt", 100)
        self.assertIn("Final Answer:", result)
    
    def test_tokenize(self):
        """
        Test tokenize method.
        """
        tokens = self.model.tokenize("This is a test")
        self.assertIsInstance(tokens, list)
        self.assertEqual(len(tokens), 4)  # "This", "is", "a", "test"
    
    def test_detokenize(self):
        """
        Test detokenize method.
        """
        text = self.model.detokenize([1, 2, 3])
        self.assertIsInstance(text, str)
        self.assertIn("<token_1>", text)
        self.assertIn("<token_2>", text)
        self.assertIn("<token_3>", text)
    
    def test_get_model_info(self):
        """
        Test get_model_info method.
        """
        info = self.model.get_model_info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info["model_path"], "models/test_model")
        self.assertEqual(info["kernel_type"], "i2_s")
        self.assertEqual(info["num_threads"], 4)
        self.assertEqual(info["context_size"], 2048)
        self.assertTrue(info["is_mock"])
    
    def test_str(self):
        """
        Test __str__ method.
        """
        string = str(self.model)
        self.assertIn("BitNetModel", string)
        self.assertIn("models/test_model", string)
        self.assertIn("i2_s", string)
        self.assertIn("False", string)

if __name__ == "__main__":
    unittest.main()
