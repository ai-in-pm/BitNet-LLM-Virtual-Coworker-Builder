"""
Tests for BitNetVirtualCoworker class.
"""

import unittest
from unittest.mock import MagicMock, patch

from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.tools.base_tools import Tool
from bitnet_vc_builder.memory.memory import Memory

class TestBitNetVirtualCoworker(unittest.TestCase):
    """
    Test BitNetVirtualCoworker class.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Create mock model
        self.mock_model = MagicMock(spec=BitNetModel)
        self.mock_model.generate.return_value = "This is a test response."
        
        # Create mock tool
        self.mock_tool = MagicMock(spec=Tool)
        self.mock_tool.name = "test_tool"
        self.mock_tool.description = "A test tool"
        self.mock_tool.args_schema = {"arg1": {"type": "string"}}
        self.mock_tool.return_value = "Tool result"
        
        # Create mock memory
        self.mock_memory = MagicMock(spec=Memory)
        self.mock_memory.get_context.return_value = "Memory context"
        
        # Create virtual co-worker
        self.coworker = BitNetVirtualCoworker(
            model=self.mock_model,
            tools=[self.mock_tool],
            memory=self.mock_memory,
            name="TestCoworker",
            description="A test virtual co-worker"
        )
    
    def test_init(self):
        """
        Test initialization.
        """
        self.assertEqual(self.coworker.name, "TestCoworker")
        self.assertEqual(self.coworker.description, "A test virtual co-worker")
        self.assertEqual(self.coworker.model, self.mock_model)
        self.assertEqual(len(self.coworker.tools), 1)
        self.assertEqual(self.coworker.tools[0], self.mock_tool)
        self.assertEqual(self.coworker.memory, self.mock_memory)
    
    def test_default_system_prompt(self):
        """
        Test default system prompt.
        """
        prompt = self.coworker._default_system_prompt()
        self.assertIn("You are TestCoworker", prompt)
        self.assertIn("A test virtual co-worker", prompt)
        self.assertIn("test_tool: A test tool", prompt)
        self.assertIn("Arguments:", prompt)
    
    def test_run_with_final_answer(self):
        """
        Test run method with final answer.
        """
        # Mock the think method to return a final answer
        self.coworker.think = MagicMock(return_value="Final Answer: This is the answer.")
        
        result = self.coworker.run("Test task")
        
        # Check that the think method was called
        self.coworker.think.assert_called_once()
        
        # Check that the result is the final answer
        self.assertEqual(result, "This is the answer.")
        
        # Check that the memory was updated
        self.mock_memory.add.assert_called_once()
    
    def test_run_with_tool_call(self):
        """
        Test run method with tool call.
        """
        # Mock the think method to return a tool call and then a final answer
        self.coworker.think = MagicMock(side_effect=[
            "Action: test_tool\nAction Input: {\"arg1\": \"test\"}\n",
            "Final Answer: Tool result processed."
        ])
        
        # Mock the tool
        self.mock_tool.__call__ = MagicMock(return_value="Tool result")
        
        result = self.coworker.run("Test task")
        
        # Check that the think method was called twice
        self.assertEqual(self.coworker.think.call_count, 2)
        
        # Check that the tool was called
        self.mock_tool.__call__.assert_called_once()
        
        # Check that the result is the final answer
        self.assertEqual(result, "Tool result processed.")
    
    def test_think(self):
        """
        Test think method.
        """
        conversation = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message"},
            {"role": "assistant", "content": "Assistant message"}
        ]
        
        self.coworker.think(conversation)
        
        # Check that the model's generate method was called
        self.mock_model.generate.assert_called_once()
        
        # Check the input to the model
        call_args = self.mock_model.generate.call_args[1]
        self.assertIn("System: System message", call_args["prompt"])
        self.assertIn("User: User message", call_args["prompt"])
        self.assertIn("Assistant: Assistant message", call_args["prompt"])
    
    def test_extract_tool_name(self):
        """
        Test _extract_tool_name method.
        """
        response = "Action: test_tool\nAction Input: {\"arg1\": \"test\"}\n"
        tool_name = self.coworker._extract_tool_name(response)
        self.assertEqual(tool_name, "test_tool")
        
        # Test with no tool name
        response = "This is a response with no tool call."
        tool_name = self.coworker._extract_tool_name(response)
        self.assertEqual(tool_name, "")
    
    def test_extract_tool_input(self):
        """
        Test _extract_tool_input method.
        """
        response = "Action: test_tool\nAction Input: {\"arg1\": \"test\"}\n"
        tool_input = self.coworker._extract_tool_input(response)
        self.assertEqual(tool_input, {"arg1": "test"})
        
        # Test with no tool input
        response = "Action: test_tool\n"
        tool_input = self.coworker._extract_tool_input(response)
        self.assertEqual(tool_input, {})
    
    def test_extract_final_answer(self):
        """
        Test _extract_final_answer method.
        """
        response = "Thinking...\nFinal Answer: This is the answer."
        final_answer = self.coworker._extract_final_answer(response)
        self.assertEqual(final_answer, "This is the answer.")
        
        # Test with no final answer
        response = "This is a response with no final answer."
        final_answer = self.coworker._extract_final_answer(response)
        self.assertEqual(final_answer, response)
    
    def test_find_tool(self):
        """
        Test _find_tool method.
        """
        tool = self.coworker._find_tool("test_tool")
        self.assertEqual(tool, self.mock_tool)
        
        # Test with non-existent tool
        tool = self.coworker._find_tool("non_existent_tool")
        self.assertIsNone(tool)
    
    def test_add_tool(self):
        """
        Test add_tool method.
        """
        new_tool = MagicMock(spec=Tool)
        new_tool.name = "new_tool"
        
        self.coworker.add_tool(new_tool)
        
        self.assertEqual(len(self.coworker.tools), 2)
        self.assertEqual(self.coworker.tools[1], new_tool)
    
    def test_remove_tool(self):
        """
        Test remove_tool method.
        """
        result = self.coworker.remove_tool("test_tool")
        
        self.assertTrue(result)
        self.assertEqual(len(self.coworker.tools), 0)
        
        # Test removing non-existent tool
        result = self.coworker.remove_tool("non_existent_tool")
        self.assertFalse(result)
    
    def test_get_tools(self):
        """
        Test get_tools method.
        """
        tools = self.coworker.get_tools()
        
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0], self.mock_tool)
    
    def test_clear_memory(self):
        """
        Test clear_memory method.
        """
        self.coworker.clear_memory()
        
        self.mock_memory.clear.assert_called_once()
    
    def test_get_memory(self):
        """
        Test get_memory method.
        """
        memory = self.coworker.get_memory()
        
        self.assertEqual(memory, "Memory context")
        self.mock_memory.get_context.assert_called_once()
    
    def test_add_to_memory(self):
        """
        Test add_to_memory method.
        """
        self.coworker.add_to_memory("New memory")
        
        self.mock_memory.add.assert_called_once_with("New memory")
    
    def test_str(self):
        """
        Test __str__ method.
        """
        string = str(self.coworker)
        
        self.assertEqual(string, "TestCoworker: A test virtual co-worker")
    
    def test_repr(self):
        """
        Test __repr__ method.
        """
        representation = repr(self.coworker)
        
        self.assertIn("BitNetVirtualCoworker", representation)
        self.assertIn("name='TestCoworker'", representation)
        self.assertIn("tools=1", representation)

if __name__ == "__main__":
    unittest.main()
