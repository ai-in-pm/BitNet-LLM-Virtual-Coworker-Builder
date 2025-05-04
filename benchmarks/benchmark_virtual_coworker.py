"""
Benchmark for BitNet Virtual Co-worker Builder.
"""

import os
import sys
import time
import argparse
import logging
from typing import List, Dict, Any

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
                "description": "Mathematical expression to calculate"
            }
        }
    )

def create_virtual_coworker(model_path: str, kernel_type: str, use_bitnet_integration: bool):
    """
    Create a virtual co-worker.
    
    Args:
        model_path: Path to the model
        kernel_type: Kernel type
        use_bitnet_integration: Whether to use BitNet integration
        
    Returns:
        Virtual co-worker
    """
    # Create model
    model = BitNetModel(
        model_path=model_path,
        kernel_type=kernel_type,
        use_bitnet_integration=use_bitnet_integration
    )
    
    # Create tools
    calculator_tool = create_calculator_tool()
    
    # Create memory
    memory = Memory()
    
    # Create virtual co-worker
    virtual_coworker = BitNetVirtualCoworker(
        model=model,
        tools=[calculator_tool],
        memory=memory,
        name="BenchmarkCoworker",
        description="A virtual co-worker for benchmarking"
    )
    
    return virtual_coworker

def run_benchmark(virtual_coworker: BitNetVirtualCoworker, tasks: List[str], num_runs: int = 3):
    """
    Run benchmark.
    
    Args:
        virtual_coworker: Virtual co-worker to benchmark
        tasks: List of tasks to run
        num_runs: Number of runs per task
        
    Returns:
        Benchmark results
    """
    results = []
    
    for task in tasks:
        task_times = []
        
        for _ in range(num_runs):
            # Run task and measure time
            start_time = time.time()
            virtual_coworker.run(task)
            end_time = time.time()
            
            # Calculate time
            task_time = end_time - start_time
            task_times.append(task_time)
        
        # Calculate average time
        avg_time = sum(task_times) / len(task_times)
        
        # Add result
        results.append({
            "task": task,
            "avg_time": avg_time,
            "min_time": min(task_times),
            "max_time": max(task_times),
            "times": task_times
        })
    
    return results

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Benchmark BitNet Virtual Co-worker Builder")
    
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
        "--num-runs",
        type=int,
        default=3,
        help="Number of runs per task"
    )
    
    args = parser.parse_args()
    
    # Create virtual co-worker
    virtual_coworker = create_virtual_coworker(
        model_path=args.model_path,
        kernel_type=args.kernel_type,
        use_bitnet_integration=args.use_bitnet
    )
    
    # Define tasks
    tasks = [
        "Calculate 2 + 2 * 3",
        "What is the square root of 16?",
        "Calculate the factorial of 5",
        "What is the capital of France?",
        "Explain the concept of artificial intelligence in simple terms",
        "Write a short poem about nature",
        "Summarize the plot of Romeo and Juliet",
        "What are the benefits of exercise?",
        "How does photosynthesis work?",
        "What is the difference between a virus and a bacterium?"
    ]
    
    # Run benchmark
    logger.info("Running benchmark...")
    results = run_benchmark(virtual_coworker, tasks, args.num_runs)
    
    # Print results
    print("\nBenchmark Results:")
    print("=================")
    print(f"Model: {args.model_path}")
    print(f"Kernel Type: {args.kernel_type}")
    print(f"Use BitNet Integration: {args.use_bitnet}")
    print(f"Number of Runs: {args.num_runs}")
    print()
    
    for result in results:
        print(f"Task: {result['task']}")
        print(f"  Average Time: {result['avg_time']:.4f} seconds")
        print(f"  Min Time: {result['min_time']:.4f} seconds")
        print(f"  Max Time: {result['max_time']:.4f} seconds")
        print()
    
    # Print summary
    total_avg_time = sum(result["avg_time"] for result in results) / len(results)
    print(f"Overall Average Time: {total_avg_time:.4f} seconds")

if __name__ == "__main__":
    main()
