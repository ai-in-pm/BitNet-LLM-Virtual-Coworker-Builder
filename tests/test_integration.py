"""
Integration tests for BitNet Virtual Co-worker Builder.
"""

import unittest
import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.core.team import BitNetTeam, CollaborationMode
from bitnet_vc_builder.tools.base_tools import Tool
from bitnet_vc_builder.memory.memory import Memory

class TestIntegration(unittest.TestCase):
    """
    Integration tests for BitNet Virtual Co-worker Builder.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create a model
        self.model = BitNetModel(
            model_path="models/test_model",
            kernel_type="i2_s",
            use_bitnet_integration=False
        )
        
        # Create tools
        def calculator(expression):
            """
            Simple calculator tool.
            """
            try:
                return eval(expression)
            except Exception as e:
                return f"Error: {str(e)}"
        
        self.calculator_tool = Tool(
            name="calculator",
            description="Calculate a mathematical expression",
            function=calculator,
            args_schema={
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to calculate"
                }
            }
        )
        
        def web_search(query):
            """
            Mock web search tool.
            """
            return f"Search results for: {query}"
        
        self.search_tool = Tool(
            name="search",
            description="Search the web for information",
            function=web_search,
            args_schema={
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            }
        )
        
        # Create memory
        self.memory = Memory()
        
        # Create virtual co-workers
        self.math_coworker = BitNetVirtualCoworker(
            model=self.model,
            tools=[self.calculator_tool],
            memory=self.memory,
            name="MathCoworker",
            description="A virtual co-worker that specializes in mathematics"
        )
        
        self.research_coworker = BitNetVirtualCoworker(
            model=self.model,
            tools=[self.search_tool],
            memory=self.memory,
            name="ResearchCoworker",
            description="A virtual co-worker that specializes in research"
        )
        
        # Create team
        self.team = BitNetTeam(
            agents=[self.math_coworker, self.research_coworker],
            name="TestTeam",
            description="A test team",
            collaboration_mode=CollaborationMode.SEQUENTIAL
        )
    
    def test_virtual_coworker_with_tool(self):
        """
        Test virtual co-worker with tool.
        """
        # Run virtual co-worker
        result = self.math_coworker.run("Calculate 2 + 2 * 3")
        
        # Check that the result contains the correct answer
        self.assertIn("6", result)
    
    def test_virtual_coworker_with_memory(self):
        """
        Test virtual co-worker with memory.
        """
        # Add something to memory
        self.memory.add("The capital of France is Paris.")
        
        # Run virtual co-worker
        result = self.research_coworker.run("What is the capital of France?")
        
        # Check that the result contains the information from memory
        self.assertIn("Paris", result)
    
    def test_team_sequential(self):
        """
        Test team with sequential collaboration mode.
        """
        # Run team
        result = self.team.run("Calculate 2 + 2 and search for information about mathematics")
        
        # Check that the result contains both the calculation and search results
        self.assertIn("4", result)
        self.assertIn("mathematics", result)
    
    def test_team_hierarchical(self):
        """
        Test team with hierarchical collaboration mode.
        """
        # Change collaboration mode
        self.team.collaboration_mode = CollaborationMode.HIERARCHICAL
        
        # Run team
        result = self.team.run("Calculate 2 + 2 and search for information about mathematics")
        
        # Check that the result contains both the calculation and search results
        self.assertIn("4", result)
        self.assertIn("mathematics", result)

if __name__ == "__main__":
    unittest.main()
