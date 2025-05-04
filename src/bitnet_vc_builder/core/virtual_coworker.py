"""
Base virtual co-worker class for BitNet Virtual Co-worker Builder.
"""

import json
import logging
from typing import List, Dict, Any, Optional, Union, Callable

from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.memory.memory import Memory
from bitnet_vc_builder.tools.base_tools import Tool

logger = logging.getLogger(__name__)

class BitNetVirtualCoworker:
    """
    Base virtual co-worker class powered by BitNet.
    
    This class provides the foundation for creating AI virtual co-workers powered by BitNet's
    1-bit quantized language models. It handles the integration with the model,
    tools, and memory systems.
    """
    
    def __init__(
        self, 
        model: BitNetModel, 
        tools: Optional[List[Tool]] = None,
        memory: Optional[Memory] = None,
        name: str = "BitNetVirtualCoworker",
        description: str = "A general-purpose AI assistant powered by BitNet.",
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize BitNet virtual co-worker.
        
        Args:
            model: BitNet model instance
            tools: List of tools available to the virtual co-worker
            memory: Memory instance for the virtual co-worker
            name: Name of the virtual co-worker
            description: Description of the virtual co-worker
            system_prompt: System prompt for the virtual co-worker
        """
        self.model = model
        self.tools = tools or []
        self.memory = memory or Memory()
        self.name = name
        self.description = description
        self.system_prompt = system_prompt or self._default_system_prompt()
        
        # Validate model
        if not isinstance(model, BitNetModel):
            raise TypeError("Model must be an instance of BitNetModel")
    
    def _default_system_prompt(self) -> str:
        """
        Get default system prompt.
        
        Returns:
            Default system prompt
        """
        tools_description = ""
        if self.tools:
            tools_description = "You have access to the following tools:\n\n"
            for tool in self.tools:
                tools_description += f"- {tool.name}: {tool.description}\n"
                if tool.args_schema:
                    tools_description += f"  Arguments: {json.dumps(tool.args_schema, indent=2)}\n"
        
        return f"""You are {self.name}, {self.description}

{tools_description}

To use a tool, use the following format:
Action: tool_name
Action Input: {{
    "arg1": "value1",
    "arg2": "value2"
}}

When you have a final answer, use the following format:
Final Answer: your final answer here

Begin!
"""
    
    def run(self, task: str) -> str:
        """
        Run virtual co-worker on a task.
        
        Args:
            task: Task description
            
        Returns:
            Virtual co-worker's response
        """
        logger.info(f"Running virtual co-worker {self.name} on task: {task}")
        
        # Initialize conversation
        conversation = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task}
        ]
        
        # Add memory context if available
        memory_context = self.memory.get_context()
        if memory_context:
            conversation.insert(1, {"role": "system", "content": f"Context from memory:\n\n{memory_context}"})
        
        # Maximum number of iterations to prevent infinite loops
        max_iterations = 10
        
        for _ in range(max_iterations):
            # Generate response
            response = self.think(conversation)
            
            # Check if the response contains a tool call
            tool_name = self._extract_tool_name(response)
            
            if tool_name:
                # Extract tool input
                tool_input = self._extract_tool_input(response)
                
                # Find the tool
                tool = self._find_tool(tool_name)
                
                if tool:
                    try:
                        # Call the tool
                        tool_result = tool(tool_input)
                        
                        # Add tool call and result to conversation
                        conversation.append({"role": "assistant", "content": response})
                        conversation.append({"role": "system", "content": f"Tool result: {tool_result}"})
                    except Exception as e:
                        # Add error to conversation
                        conversation.append({"role": "assistant", "content": response})
                        conversation.append({"role": "system", "content": f"Error: {str(e)}"})
                else:
                    # Tool not found
                    conversation.append({"role": "assistant", "content": response})
                    conversation.append({"role": "system", "content": f"Error: Tool '{tool_name}' not found. Available tools: {', '.join(tool.name for tool in self.tools)}"})
            
            # Check if the response contains a final answer
            elif "Final Answer:" in response:
                # Extract final answer
                final_answer = self._extract_final_answer(response)
                
                # Add final answer to memory
                self.memory.add(f"Task: {task}\nAnswer: {final_answer}")
                
                return final_answer
            
            # If no tool call or final answer, treat as intermediate thinking
            else:
                conversation.append({"role": "assistant", "content": response})
                conversation.append({"role": "system", "content": "Please use the specified format for tool usage or provide a final answer."})
        
        # If we reach here, we've hit the maximum number of iterations
        return "I apologize, but I was unable to complete the task within the allowed number of iterations."
    
    def think(self, conversation: List[Dict[str, str]]) -> str:
        """
        Virtual co-worker thinking process.
        
        Args:
            conversation: Conversation history
            
        Returns:
            Virtual co-worker's response
        """
        # Convert conversation to model input format
        model_input = ""
        for message in conversation:
            if message["role"] == "system":
                model_input += f"System: {message['content']}\n\n"
            elif message["role"] == "user":
                model_input += f"User: {message['content']}\n\n"
            elif message["role"] == "assistant":
                model_input += f"Assistant: {message['content']}\n\n"
        
        model_input += "Assistant: "
        
        # Generate response
        response = self.model.generate(
            prompt=model_input,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            repetition_penalty=1.1
        )
        
        return response
    
    def _extract_tool_name(self, response: str) -> str:
        """
        Extract tool name from response.
        
        Args:
            response: Virtual co-worker's response
            
        Returns:
            Tool name
        """
        lines = response.split('\n')
        for line in lines:
            if line.startswith("Action:"):
                return line.replace("Action:", "").strip()
        return ""
    
    def _extract_tool_input(self, response: str) -> Dict[str, Any]:
        """
        Extract tool input from response.
        
        Args:
            response: Virtual co-worker's response
            
        Returns:
            Tool input
        """
        # Find the action input section
        action_input_start = response.find("Action Input:")
        if action_input_start == -1:
            return {}
        
        action_input_text = response[action_input_start:].replace("Action Input:", "").strip()
        
        # Extract JSON
        try:
            # Find the start and end of the JSON object
            json_start = action_input_text.find("{")
            json_end = action_input_text.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                return {}
            
            json_text = action_input_text[json_start:json_end]
            return json.loads(json_text)
        except json.JSONDecodeError:
            return {}
    
    def _extract_final_answer(self, response: str) -> str:
        """
        Extract final answer from response.
        
        Args:
            response: Virtual co-worker's response
            
        Returns:
            Final answer
        """
        if "Final Answer:" not in response:
            return response
            
        final_answer_parts = response.split("Final Answer:")
        if len(final_answer_parts) > 1:
            return final_answer_parts[1].strip()
        return ""
    
    def _find_tool(self, tool_name: str) -> Optional[Tool]:
        """
        Find tool by name.
        
        Args:
            tool_name: Tool name
            
        Returns:
            Tool instance or None if not found
        """
        for tool in self.tools:
            if tool.name.lower() == tool_name.lower():
                return tool
        return None
    
    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the virtual co-worker.
        
        Args:
            tool: Tool instance
        """
        self.tools.append(tool)
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the virtual co-worker.
        
        Args:
            tool_name: Tool name
            
        Returns:
            True if the tool was removed, False otherwise
        """
        for i, tool in enumerate(self.tools):
            if tool.name.lower() == tool_name.lower():
                self.tools.pop(i)
                return True
        return False
    
    def get_tools(self) -> List[Tool]:
        """
        Get all tools available to the virtual co-worker.
        
        Returns:
            List of tools
        """
        return self.tools
    
    def clear_memory(self) -> None:
        """
        Clear virtual co-worker's memory.
        """
        self.memory.clear()
    
    def get_memory(self) -> str:
        """
        Get virtual co-worker's memory.
        
        Returns:
            Memory context
        """
        return self.memory.get_context()
    
    def add_to_memory(self, content: str) -> None:
        """
        Add content to virtual co-worker's memory.
        
        Args:
            content: Content to add
        """
        self.memory.add(content)
    
    def __str__(self) -> str:
        """
        Get string representation of the virtual co-worker.
        
        Returns:
            String representation
        """
        return f"{self.name}: {self.description}"
    
    def __repr__(self) -> str:
        """
        Get representation of the virtual co-worker.
        
        Returns:
            Representation
        """
        return f"BitNetVirtualCoworker(name='{self.name}', tools={len(self.tools)}, memory={self.memory})"
