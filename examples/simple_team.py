"""
Simple example of using a BitNet team.
"""

import os
import sys
import logging
import argparse

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
                "description": "Mathematical expression to calculate",
                "required": True
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
                "description": "Search query",
                "required": True
            }
        }
    )

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Simple BitNet team example")
    
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
        "--task",
        type=str,
        default="Research climate change and calculate its economic impact",
        help="Task to run"
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
    calculator_tool = create_calculator_tool()
    search_tool = create_search_tool()
    
    # Create memory
    memory = Memory()
    
    # Create virtual co-workers
    logger.info("Creating virtual co-workers")
    
    researcher = BitNetVirtualCoworker(
        model=model,
        tools=[search_tool],
        memory=memory,
        name="Researcher",
        description="A virtual co-worker that specializes in research"
    )
    
    analyst = BitNetVirtualCoworker(
        model=model,
        tools=[calculator_tool],
        memory=memory,
        name="Analyst",
        description="A virtual co-worker that specializes in data analysis"
    )
    
    writer = BitNetVirtualCoworker(
        model=model,
        tools=[],
        memory=memory,
        name="Writer",
        description="A virtual co-worker that specializes in writing"
    )
    
    # Create team
    logger.info(f"Creating team with collaboration mode: {args.collaboration_mode}")
    team = BitNetTeam(
        agents=[researcher, analyst, writer],
        name="SimpleTeam",
        description="A simple team for demonstration",
        collaboration_mode=CollaborationMode[args.collaboration_mode]
    )
    
    # Run team
    logger.info(f"Running team on task: {args.task}")
    result = team.run(args.task)
    
    # Print result
    print("\nResult:")
    print("-------")
    print(result)
    
    # Print performance metrics
    print("\nPerformance Metrics:")
    print("-------------------")
    metrics = team.get_performance_metrics()
    
    for agent_name, agent_metrics in metrics.items():
        print(f"{agent_name}:")
        print(f"  Tasks Completed: {agent_metrics['tasks_completed']}")
        print(f"  Tasks Failed: {agent_metrics['tasks_failed']}")
        print(f"  Success Rate: {agent_metrics['success_rate']:.2f}")
        print(f"  Average Time: {agent_metrics['avg_time']:.2f} seconds")

if __name__ == "__main__":
    main()
