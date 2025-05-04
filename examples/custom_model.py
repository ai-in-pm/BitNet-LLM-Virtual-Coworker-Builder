"""
Example of using a custom model with BitNet Virtual Co-worker Builder.
"""

import os
import sys
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

class CustomBitNetModel(BitNetModel):
    """
    Custom BitNet model with specialized capabilities.
    """
    
    def __init__(
        self,
        model_path: str,
        kernel_type: str = "i2_s",
        bitnet_path: Optional[str] = None,
        num_threads: int = 4,
        context_size: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        repetition_penalty: float = 1.1,
        use_bitnet_integration: bool = True,
        specialization: str = "general"
    ):
        """
        Initialize custom BitNet model.
        
        Args:
            model_path: Path to the model
            kernel_type: Kernel type (i2_s, i2_m, i2_l)
            bitnet_path: Path to BitNet installation (optional)
            num_threads: Number of threads to use
            context_size: Context size
            temperature: Temperature for sampling
            top_p: Top-p for sampling
            top_k: Top-k for sampling
            repetition_penalty: Repetition penalty
            use_bitnet_integration: Whether to use BitNet integration
            specialization: Model specialization (general, code, math, writing)
        """
        super().__init__(
            model_path=model_path,
            kernel_type=kernel_type,
            bitnet_path=bitnet_path,
            num_threads=num_threads,
            context_size=context_size,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            use_bitnet_integration=use_bitnet_integration
        )
        
        self.specialization = specialization
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        """
        Generate text from the model.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (overrides instance value)
            top_p: Top-p for sampling (overrides instance value)
            top_k: Top-k for sampling (overrides instance value)
            repetition_penalty: Repetition penalty (overrides instance value)
            stop_sequences: Sequences that stop generation
            
        Returns:
            Generated text
        """
        # Add specialization-specific preprocessing
        if self.specialization == "code":
            # For code specialization, adjust parameters for better code generation
            temperature = temperature or 0.3  # Lower temperature for more deterministic code
            top_p = top_p or 0.95
            repetition_penalty = repetition_penalty or 1.2
            
            # Add code-specific instructions to the prompt
            if "```" not in prompt:
                prompt = f"{prompt}\n\nPlease provide the code in a clear, well-documented format."
        
        elif self.specialization == "math":
            # For math specialization, adjust parameters for better math reasoning
            temperature = temperature or 0.2  # Even lower temperature for math
            top_p = top_p or 0.9
            
            # Add math-specific instructions to the prompt
            if "step-by-step" not in prompt.lower():
                prompt = f"{prompt}\n\nPlease provide a step-by-step solution."
        
        elif self.specialization == "writing":
            # For writing specialization, adjust parameters for more creative text
            temperature = temperature or 0.8  # Higher temperature for creative writing
            top_p = top_p or 0.95
            repetition_penalty = repetition_penalty or 1.05
        
        # Call parent generate method with adjusted parameters
        return super().generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            stop_sequences=stop_sequences
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information.
        
        Returns:
            Dictionary with model information
        """
        info = super().get_model_info()
        info["specialization"] = self.specialization
        return info

def create_calculator_tool():
    """
    Create a calculator tool.
    
    Returns:
        Calculator tool
    """
    def calculator(expression):
        """
        Simple calculator tool.
        """
        try:
            return eval(expression)
        except Exception as e:
            return f"Error: {str(e)}"
    
    return Tool(
        name="calculator",
        description="Calculate a mathematical expression",
        function=calculator,
        args_schema={
            "expression": {
                "type": "string",
                "description": "Mathematical expression to calculate",
                "required": True
            }
        }
    )

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Custom model example")
    
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
        "--specialization",
        type=str,
        choices=["general", "code", "math", "writing"],
        default="general",
        help="Model specialization"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        help="Task to run"
    )
    
    args = parser.parse_args()
    
    # Set default task based on specialization
    if not args.task:
        if args.specialization == "code":
            args.task = "Write a Python function to find the prime numbers up to n using the Sieve of Eratosthenes algorithm."
        elif args.specialization == "math":
            args.task = "Solve the quadratic equation: 2x^2 + 5x - 3 = 0"
        elif args.specialization == "writing":
            args.task = "Write a short story about a robot that develops consciousness."
        else:
            args.task = "Explain the concept of quantum computing in simple terms."
    
    # Create custom model
    logger.info(f"Creating custom BitNet model: {args.model_path} with specialization: {args.specialization}")
    model = CustomBitNetModel(
        model_path=args.model_path,
        kernel_type=args.kernel_type,
        use_bitnet_integration=args.use_bitnet,
        specialization=args.specialization
    )
    
    # Create tools
    calculator_tool = create_calculator_tool()
    
    # Create memory
    memory = Memory()
    
    # Create virtual co-worker
    logger.info("Creating virtual co-worker with custom model")
    virtual_coworker = BitNetVirtualCoworker(
        model=model,
        tools=[calculator_tool] if args.specialization == "math" else [],
        memory=memory,
        name=f"{args.specialization.capitalize()}Coworker",
        description=f"A virtual co-worker that specializes in {args.specialization}"
    )
    
    # Run virtual co-worker
    logger.info(f"Running virtual co-worker on task: {args.task}")
    result = virtual_coworker.run(args.task)
    
    # Print result
    print("\nResult:")
    print("-------")
    print(result)
    
    # Print model info
    print("\nModel Info:")
    print("-----------")
    model_info = model.get_model_info()
    for key, value in model_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
