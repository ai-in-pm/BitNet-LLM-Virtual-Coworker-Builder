"""
Benchmark for BitNet Team.
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
from bitnet_vc_builder.core.team import BitNetTeam, CollaborationMode
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

def create_search_tool():
    """
    Create a search tool.
    
    Returns:
        Search tool
    """
    def search(query):
        """
        Mock search tool.
        """
        return f"Search results for: {query}"
    
    return Tool(
        name="search",
        description="Search the web for information",
        function=search,
        args_schema={
            "query": {
                "type": "string",
                "description": "Search query"
            }
        }
    )

def create_team(model_path: str, kernel_type: str, use_bitnet_integration: bool, collaboration_mode: CollaborationMode):
    """
    Create a team.
    
    Args:
        model_path: Path to the model
        kernel_type: Kernel type
        use_bitnet_integration: Whether to use BitNet integration
        collaboration_mode: Collaboration mode
        
    Returns:
        Team
    """
    # Create model
    model = BitNetModel(
        model_path=model_path,
        kernel_type=kernel_type,
        use_bitnet_integration=use_bitnet_integration
    )
    
    # Create tools
    calculator_tool = create_calculator_tool()
    search_tool = create_search_tool()
    
    # Create memory
    memory = Memory()
    
    # Create virtual co-workers
    math_coworker = BitNetVirtualCoworker(
        model=model,
        tools=[calculator_tool],
        memory=memory,
        name="MathCoworker",
        description="A virtual co-worker that specializes in mathematics"
    )
    
    research_coworker = BitNetVirtualCoworker(
        model=model,
        tools=[search_tool],
        memory=memory,
        name="ResearchCoworker",
        description="A virtual co-worker that specializes in research"
    )
    
    writer_coworker = BitNetVirtualCoworker(
        model=model,
        tools=[],
        memory=memory,
        name="WriterCoworker",
        description="A virtual co-worker that specializes in writing"
    )
    
    # Create team
    team = BitNetTeam(
        agents=[math_coworker, research_coworker, writer_coworker],
        name="BenchmarkTeam",
        description="A team for benchmarking",
        collaboration_mode=collaboration_mode
    )
    
    return team

def run_benchmark(team: BitNetTeam, tasks: List[str], num_runs: int = 3):
    """
    Run benchmark.
    
    Args:
        team: Team to benchmark
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
            team.run(task)
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
    parser = argparse.ArgumentParser(description="Benchmark BitNet Team")
    
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
        "--collaboration-mode",
        type=str,
        choices=["SEQUENTIAL", "PARALLEL", "HIERARCHICAL", "CONSENSUS"],
        default="SEQUENTIAL",
        help="Collaboration mode"
    )
    
    parser.add_argument(
        "--num-runs",
        type=int,
        default=3,
        help="Number of runs per task"
    )
    
    args = parser.parse_args()
    
    # Create team
    team = create_team(
        model_path=args.model_path,
        kernel_type=args.kernel_type,
        use_bitnet_integration=args.use_bitnet,
        collaboration_mode=CollaborationMode[args.collaboration_mode]
    )
    
    # Define tasks
    tasks = [
        "Calculate 2 + 2 * 3 and explain the order of operations",
        "Research the history of mathematics and write a summary",
        "Find information about climate change and analyze the data",
        "Research the benefits of exercise and create a workout plan",
        "Find information about renewable energy and calculate the potential savings"
    ]
    
    # Run benchmark
    logger.info("Running benchmark...")
    results = run_benchmark(team, tasks, args.num_runs)
    
    # Print results
    print("\nBenchmark Results:")
    print("=================")
    print(f"Model: {args.model_path}")
    print(f"Kernel Type: {args.kernel_type}")
    print(f"Use BitNet Integration: {args.use_bitnet}")
    print(f"Collaboration Mode: {args.collaboration_mode}")
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
