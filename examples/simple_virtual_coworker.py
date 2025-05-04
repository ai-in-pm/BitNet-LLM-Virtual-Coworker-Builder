"""
Simple example of using BitNet Virtual Co-worker Builder.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder import BitNetVirtualCoworker, BitNetModel, Tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function.
    """
    # Initialize BitNet model
    # In a real implementation, you would provide the path to a real BitNet model
    model = BitNetModel(
        model_path="models/bitnet_model",  # This is a placeholder path
        kernel_type="i2_s",
        use_bitnet_integration=False  # Set to True when using a real BitNet model
    )
    
    # Create a simple tool
    def calculator(expression):
        """
        Simple calculator tool.
        """
        try:
            return eval(expression)
        except Exception as e:
            return f"Error: {str(e)}"
    
    calculator_tool = Tool(
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
    
    # Create virtual co-worker
    coworker = BitNetVirtualCoworker(
        model=model,
        tools=[calculator_tool],
        name="MathCoworker",
        description="A virtual co-worker that can perform mathematical calculations"
    )
    
    # Run virtual co-worker on a task
    task = "Calculate 2 + 2 * 3"
    logger.info(f"Running virtual co-worker on task: {task}")
    
    result = coworker.run(task)
    
    print("\nVirtual Co-worker Response:")
    print(result)
    
    # Run another task
    task = "What is the square root of 16?"
    logger.info(f"Running virtual co-worker on task: {task}")
    
    result = coworker.run(task)
    
    print("\nVirtual Co-worker Response:")
    print(result)

if __name__ == "__main__":
    main()
