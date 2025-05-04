"""
Tests for Memory class.
"""

import unittest
from unittest.mock import MagicMock, patch
import time

import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.memory.memory import Memory

class TestMemory(unittest.TestCase):
    """
    Test Memory class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        self.memory = Memory(
            max_items=5,
            max_context_length=100,
            recency_bias=0.7
        )
    
    def test_init(self):
        """
        Test initialization.
        """
        self.assertEqual(self.memory.max_items, 5)
        self.assertEqual(self.memory.max_context_length, 100)
        self.assertEqual(self.memory.recency_bias, 0.7)
        self.assertEqual(len(self.memory.items), 0)
    
    def test_add(self):
        """
        Test add method.
        """
        # Add an item
        self.memory.add("Test item 1")
        self.assertEqual(len(self.memory.items), 1)
        self.assertEqual(self.memory.items[0]["content"], "Test item 1")
        self.assertIsInstance(self.memory.items[0]["timestamp"], float)
        self.assertEqual(self.memory.items[0]["metadata"], {})
        
        # Add an item with metadata
        self.memory.add("Test item 2", {"key": "value"})
        self.assertEqual(len(self.memory.items), 2)
        self.assertEqual(self.memory.items[1]["content"], "Test item 2")
        self.assertEqual(self.memory.items[1]["metadata"], {"key": "value"})
        
        # Add more items than max_items
        for i in range(3, 8):
            self.memory.add(f"Test item {i}")
        
        # Check that only the last max_items are kept
        self.assertEqual(len(self.memory.items), 5)
        self.assertEqual(self.memory.items[0]["content"], "Test item 3")
        self.assertEqual(self.memory.items[4]["content"], "Test item 7")
    
    def test_get_context(self):
        """
        Test get_context method.
        """
        # Add some items
        for i in range(1, 6):
            self.memory.add(f"Test item {i}")
            time.sleep(0.01)  # Ensure different timestamps
        
        # Get context
        context = self.memory.get_context()
        
        # Check that all items are included
        for i in range(1, 6):
            self.assertIn(f"Test item {i}", context)
        
        # Check that items are in reverse chronological order
        self.assertGreater(context.find("Test item 5"), context.find("Test item 4"))
        self.assertGreater(context.find("Test item 4"), context.find("Test item 3"))
        self.assertGreater(context.find("Test item 3"), context.find("Test item 2"))
        self.assertGreater(context.find("Test item 2"), context.find("Test item 1"))
        
        # Get context with query
        context = self.memory.get_context("item 3")
        
        # Check that the query is used to filter items
        self.assertIn("Test item 3", context)
        
        # Get context with max_items
        context = self.memory.get_context(max_items=2)
        
        # Check that only the specified number of items are included
        self.assertIn("Test item 5", context)
        self.assertIn("Test item 4", context)
        self.assertNotIn("Test item 3", context)
        self.assertNotIn("Test item 2", context)
        self.assertNotIn("Test item 1", context)
    
    def test_clear(self):
        """
        Test clear method.
        """
        # Add some items
        for i in range(1, 4):
            self.memory.add(f"Test item {i}")
        
        # Clear memory
        self.memory.clear()
        
        # Check that memory is empty
        self.assertEqual(len(self.memory.items), 0)
    
    def test_search(self):
        """
        Test search method.
        """
        # Add some items
        for i in range(1, 6):
            self.memory.add(f"Test item {i}")
            time.sleep(0.01)  # Ensure different timestamps
        
        # Search for items
        results = self.memory.search("item 3")
        
        # Check that the search returns the correct items
        self.assertEqual(len(results), 5)  # All items are returned, but in relevance order
        self.assertEqual(results[0]["content"], "Test item 3")  # Most relevant item first
    
    def test_get_stats(self):
        """
        Test get_stats method.
        """
        # Add some items
        for i in range(1, 4):
            self.memory.add(f"Test item {i}")
        
        # Get stats
        stats = self.memory.get_stats()
        
        # Check stats
        self.assertEqual(stats["total_items"], 3)
        self.assertEqual(stats["max_items"], 5)
        self.assertEqual(stats["max_context_length"], 100)
        self.assertEqual(stats["recency_bias"], 0.7)
        self.assertIsNotNone(stats["oldest_timestamp"])
        self.assertIsNotNone(stats["newest_timestamp"])
    
    def test_len(self):
        """
        Test __len__ method.
        """
        # Add some items
        for i in range(1, 4):
            self.memory.add(f"Test item {i}")
        
        # Check length
        self.assertEqual(len(self.memory), 3)
    
    def test_str(self):
        """
        Test __str__ method.
        """
        # Add some items
        for i in range(1, 4):
            self.memory.add(f"Test item {i}")
        
        # Check string representation
        string = str(self.memory)
        self.assertIn("Memory", string)
        self.assertIn("items=3", string)
        self.assertIn("max=5", string)

if __name__ == "__main__":
    unittest.main()
