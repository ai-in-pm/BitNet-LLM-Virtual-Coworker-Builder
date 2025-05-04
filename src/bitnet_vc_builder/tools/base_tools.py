"""
Base tools for BitNet Virtual Co-worker Builder.
"""

import logging
from typing import Dict, Any, Optional, Callable, List, Union

logger = logging.getLogger(__name__)

class Tool:
    """
    Base class for tools that virtual co-workers can use.
    
    This class provides the foundation for creating tools that can be used by
    BitNet virtual co-workers to interact with external systems and APIs.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        args_schema: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        """
        Initialize tool.
        
        Args:
            name: Tool name
            description: Tool description
            function: Function to call when the tool is used
            args_schema: Schema for tool arguments
        """
        self.name = name
        self.description = description
        self.function = function
        self.args_schema = args_schema or {}
    
    def __call__(self, args: Dict[str, Any]) -> Any:
        """
        Call the tool.
        
        Args:
            args: Tool arguments
            
        Returns:
            Tool result
        """
        logger.info(f"Calling tool {self.name} with args: {args}")
        
        # Validate arguments
        self._validate_args(args)
        
        # Call function
        result = self.function(**args)
        
        logger.info(f"Tool {self.name} returned: {result}")
        
        return result
    
    def _validate_args(self, args: Dict[str, Any]) -> None:
        """
        Validate tool arguments.
        
        Args:
            args: Tool arguments
            
        Raises:
            ValueError: If arguments are invalid
        """
        if not self.args_schema:
            return
        
        # Check required arguments
        for arg_name, arg_schema in self.args_schema.items():
            if arg_schema.get("required", False) and arg_name not in args:
                raise ValueError(f"Missing required argument: {arg_name}")
        
        # Check argument types
        for arg_name, arg_value in args.items():
            if arg_name in self.args_schema:
                arg_schema = self.args_schema[arg_name]
                arg_type = arg_schema.get("type")
                
                if arg_type == "string" and not isinstance(arg_value, str):
                    raise ValueError(f"Argument {arg_name} must be a string")
                elif arg_type == "number" and not isinstance(arg_value, (int, float)):
                    raise ValueError(f"Argument {arg_name} must be a number")
                elif arg_type == "boolean" and not isinstance(arg_value, bool):
                    raise ValueError(f"Argument {arg_name} must be a boolean")
                elif arg_type == "array" and not isinstance(arg_value, list):
                    raise ValueError(f"Argument {arg_name} must be an array")
                elif arg_type == "object" and not isinstance(arg_value, dict):
                    raise ValueError(f"Argument {arg_name} must be an object")
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get tool schema.
        
        Returns:
            Tool schema
        """
        return {
            "name": self.name,
            "description": self.description,
            "args_schema": self.args_schema
        }
    
    def __str__(self) -> str:
        """
        Get string representation of the tool.
        
        Returns:
            String representation
        """
        return f"{self.name}: {self.description}"
