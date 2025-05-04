"""
Example of creating a specialized virtual co-worker with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import re
import json
import logging
import argparse
from typing import List, Dict, Any, Optional, Union

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.tools.base_tools import Tool
from bitnet_vc_builder.memory.memory import Memory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class CodeVirtualCoworker(BitNetVirtualCoworker):
    """
    Specialized virtual co-worker for coding tasks.
    """
    
    def __init__(
        self,
        model: BitNetModel,
        tools: Optional[List[Tool]] = None,
        memory: Optional[Memory] = None,
        name: str = "CodeVirtualCoworker",
        description: str = "A virtual co-worker that specializes in coding",
        system_prompt: Optional[str] = None,
        max_iterations: int = 10,
        max_tokens_per_iteration: int = 512,
        supported_languages: Optional[List[str]] = None
    ):
        """
        Initialize code virtual co-worker.
        
        Args:
            model: BitNetModel instance
            tools: List of tools
            memory: Memory instance
            name: Virtual co-worker name
            description: Virtual co-worker description
            system_prompt: System prompt (if None, a default prompt will be used)
            max_iterations: Maximum number of iterations for a task
            max_tokens_per_iteration: Maximum number of tokens to generate per iteration
            supported_languages: List of supported programming languages
        """
        super().__init__(
            model=model,
            tools=tools,
            memory=memory,
            name=name,
            description=description,
            system_prompt=system_prompt,
            max_iterations=max_iterations,
            max_tokens_per_iteration=max_tokens_per_iteration
        )
        
        self.supported_languages = supported_languages or ["python", "javascript", "java", "c++", "rust"]
    
    def _default_system_prompt(self) -> str:
        """
        Generate default system prompt.
        
        Returns:
            Default system prompt
        """
        prompt = super()._default_system_prompt()
        
        # Add code-specific instructions
        prompt += "\n\nYou are a coding expert with the following capabilities:\n"
        prompt += "1. Writing clean, efficient, and well-documented code\n"
        prompt += "2. Debugging and fixing issues in existing code\n"
        prompt += "3. Explaining code and concepts clearly\n"
        prompt += "4. Following best practices and coding standards\n"
        
        prompt += f"\nYou are proficient in the following programming languages: {', '.join(self.supported_languages)}.\n"
        
        prompt += "\nWhen writing code, always:\n"
        prompt += "- Include comments to explain complex logic\n"
        prompt += "- Use meaningful variable and function names\n"
        prompt += "- Handle errors appropriately\n"
        prompt += "- Follow language-specific conventions\n"
        
        return prompt
    
    def generate_code(self, language: str, requirements: str) -> str:
        """
        Generate code based on requirements.
        
        Args:
            language: Programming language
            requirements: Code requirements
            
        Returns:
            Generated code
        """
        if language.lower() not in [lang.lower() for lang in self.supported_languages]:
            return f"Error: Unsupported language '{language}'. Supported languages: {', '.join(self.supported_languages)}"
        
        task = f"Generate {language} code that meets the following requirements:\n\n{requirements}\n\nProvide only the code with appropriate comments."
        
        return self.run(task)
    
    def explain_code(self, code: str, detail_level: str = "medium") -> str:
        """
        Explain code.
        
        Args:
            code: Code to explain
            detail_level: Level of detail (low, medium, high)
            
        Returns:
            Code explanation
        """
        task = f"Explain the following code with a {detail_level} level of detail:\n\n```\n{code}\n```"
        
        return self.run(task)
    
    def debug_code(self, code: str, error_message: Optional[str] = None) -> str:
        """
        Debug code.
        
        Args:
            code: Code to debug
            error_message: Error message (optional)
            
        Returns:
            Debugging results
        """
        task = f"Debug the following code"
        
        if error_message:
            task += f" that produces this error: {error_message}"
        
        task += f":\n\n```\n{code}\n```\n\nIdentify issues and provide a fixed version."
        
        return self.run(task)
    
    def optimize_code(self, code: str, optimization_goal: str = "performance") -> str:
        """
        Optimize code.
        
        Args:
            code: Code to optimize
            optimization_goal: Optimization goal (performance, readability, memory)
            
        Returns:
            Optimized code
        """
        task = f"Optimize the following code for {optimization_goal}:\n\n```\n{code}\n```\n\nProvide the optimized code with an explanation of the improvements."
        
        return self.run(task)

def create_code_generator_tool():
    """
    Create a code generator tool.
    
    Returns:
        Code generator tool
    """
    def generate_code(language: str, requirements: str) -> str:
        """
        Generate code based on requirements.
        
        Args:
            language: Programming language
            requirements: Code requirements
            
        Returns:
            Generated code
        """
        # In a real implementation, you would use a code generation model
        # For this example, we'll use a mock implementation
        
        logger.info(f"Generating {language} code for: {requirements}")
        
        if language.lower() == "python":
            return """
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
"""
        elif language.lower() == "javascript":
            return """
function calculateFibonacci(n) {
  // Calculate the nth Fibonacci number
  if (n <= 0) {
    return 0;
  } else if (n === 1) {
    return 1;
  } else {
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
      [a, b] = [b, a + b];
    }
    return b;
  }
}
"""
        else:
            return f"// Mock {language} code for: {requirements}"
    
    return Tool(
        name="generate_code",
        description="Generate code based on requirements",
        function=generate_code,
        args_schema={
            "language": {
                "type": "string",
                "description": "Programming language",
                "required": True
            },
            "requirements": {
                "type": "string",
                "description": "Code requirements",
                "required": True
            }
        }
    )

def create_code_explainer_tool():
    """
    Create a code explainer tool.
    
    Returns:
        Code explainer tool
    """
    def explain_code(code: str, detail_level: str = "medium") -> str:
        """
        Explain code.
        
        Args:
            code: Code to explain
            detail_level: Level of detail (low, medium, high)
            
        Returns:
            Code explanation
        """
        # In a real implementation, you would use a code explanation model
        # For this example, we'll use a mock implementation
        
        logger.info(f"Explaining code with {detail_level} detail level")
        
        return f"This code appears to be calculating Fibonacci numbers using an iterative approach."
    
    return Tool(
        name="explain_code",
        description="Explain code",
        function=explain_code,
        args_schema={
            "code": {
                "type": "string",
                "description": "Code to explain",
                "required": True
            },
            "detail_level": {
                "type": "string",
                "description": "Level of detail (low, medium, high)",
                "required": False
            }
        }
    )

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Specialized virtual co-worker example")
    
    parser.add_argument(
        "--model-path",
        type=str,
        default="models/bitnet_model",
        help="Path to BitNet model"
    )
    
    parser.add_argument(
        "--kernel-type",
        type=str,
        choices=["i2_s", "i2_m", "i2_l"],
        default="i2_s",
        help="BitNet kernel type"
    )
    
    parser.add_argument(
        "--use-bitnet",
        action="store_true",
        help="Use BitNet integration"
    )
    
    parser.add_argument(
        "--action",
        type=str,
        choices=["generate", "explain", "debug", "optimize"],
        default="generate",
        help="Action to perform"
    )
    
    parser.add_argument(
        "--language",
        type=str,
        default="python",
        help="Programming language"
    )
    
    parser.add_argument(
        "--requirements",
        type=str,
        default="Write a function to calculate the nth Fibonacci number",
        help="Code requirements (for generate action)"
    )
    
    parser.add_argument(
        "--code",
        type=str,
        help="Code to explain, debug, or optimize (for explain, debug, and optimize actions)"
    )
    
    parser.add_argument(
        "--error-message",
        type=str,
        help="Error message (for debug action)"
    )
    
    parser.add_argument(
        "--optimization-goal",
        type=str,
        choices=["performance", "readability", "memory"],
        default="performance",
        help="Optimization goal (for optimize action)"
    )
    
    args = parser.parse_args()
    
    # Create model
    logger.info(f"Creating BitNet model: {args.model_path}")
    model = BitNetModel(
        model_path=args.model_path,
        kernel_type=args.kernel_type,
        use_bitnet_integration=args.use_bitnet
    )
    
    # Create tools
    code_generator_tool = create_code_generator_tool()
    code_explainer_tool = create_code_explainer_tool()
    
    # Create memory
    memory = Memory()
    
    # Create specialized virtual co-worker
    logger.info("Creating specialized virtual co-worker")
    code_coworker = CodeVirtualCoworker(
        model=model,
        tools=[code_generator_tool, code_explainer_tool],
        memory=memory,
        name="CodeCoworker",
        description="A virtual co-worker that specializes in coding",
        supported_languages=["python", "javascript", "java", "c++", "rust"]
    )
    
    # Perform action
    if args.action == "generate":
        logger.info(f"Generating {args.language} code for: {args.requirements}")
        result = code_coworker.generate_code(args.language, args.requirements)
    elif args.action == "explain":
        if not args.code:
            parser.error("--code is required for explain action")
        
        logger.info("Explaining code")
        result = code_coworker.explain_code(args.code)
    elif args.action == "debug":
        if not args.code:
            parser.error("--code is required for debug action")
        
        logger.info("Debugging code")
        result = code_coworker.debug_code(args.code, args.error_message)
    elif args.action == "optimize":
        if not args.code:
            parser.error("--code is required for optimize action")
        
        logger.info(f"Optimizing code for {args.optimization_goal}")
        result = code_coworker.optimize_code(args.code, args.optimization_goal)
    
    # Print result
    print("\nResult:")
    print("-------")
    print(result)

if __name__ == "__main__":
    main()
