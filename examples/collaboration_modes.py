"""
Example of using different collaboration modes with BitNet teams.
"""

import os
import sys
import logging
import argparse
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
    parser = argparse.ArgumentParser(description="Collaboration modes example")
    
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
        "--task",
        type=str,
        default="Research climate change, analyze its economic impact, and write a summary report.",
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
        description="A virtual co-worker that specializes in research",
        system_prompt="You are a research specialist. Your role is to gather information and provide factual data."
    )
    
    analyst = BitNetVirtualCoworker(
        model=model,
        tools=[calculator_tool],
        memory=memory,
        name="Analyst",
        description="A virtual co-worker that specializes in data analysis",
        system_prompt="You are a data analyst. Your role is to analyze information, identify patterns, and draw insights."
    )
    
    writer = BitNetVirtualCoworker(
        model=model,
        tools=[],
        memory=memory,
        name="Writer",
        description="A virtual co-worker that specializes in writing",
        system_prompt="You are a professional writer. Your role is to create clear, concise, and engaging content."
    )
    
    coordinator = BitNetVirtualCoworker(
        model=model,
        tools=[],
        memory=memory,
        name="Coordinator",
        description="A virtual co-worker that specializes in coordination",
        system_prompt="You are a project coordinator. Your role is to break down tasks, assign them to team members, and integrate their work."
    )
    
    # Create teams with different collaboration modes
    teams = {
        "Sequential": BitNetTeam(
            agents=[researcher, analyst, writer],
            name="SequentialTeam",
            description="A team that works sequentially",
            collaboration_mode=CollaborationMode.SEQUENTIAL
        ),
        "Parallel": BitNetTeam(
            agents=[researcher, analyst, writer],
            name="ParallelTeam",
            description="A team that works in parallel",
            collaboration_mode=CollaborationMode.PARALLEL
        ),
        "Hierarchical": BitNetTeam(
            agents=[coordinator, researcher, analyst, writer],
            name="HierarchicalTeam",
            description="A team that works hierarchically",
            collaboration_mode=CollaborationMode.HIERARCHICAL
        ),
        "Consensus": BitNetTeam(
            agents=[researcher, analyst, writer],
            name="ConsensusTeam",
            description="A team that works by consensus",
            collaboration_mode=CollaborationMode.CONSENSUS
        )
    }
    
    # Run each team on the task
    for mode, team in teams.items():
        print(f"\n{mode} Collaboration Mode")
        print("=" * 50)
        
        logger.info(f"Running {mode} team on task: {args.task}")
        
        # For hierarchical mode, specify the coordinator
        if mode == "Hierarchical":
            result = team.run(args.task, coordinator_agent_name="Coordinator")
        else:
            result = team.run(args.task)
        
        # Print result
        print(result)
        
        # Print performance metrics
        print("\nPerformance Metrics:")
        print("-" * 20)
        metrics = team.get_performance_metrics()
        
        for agent_name, agent_metrics in metrics.items():
            print(f"{agent_name}:")
            print(f"  Tasks Completed: {agent_metrics['tasks_completed']}")
            print(f"  Tasks Failed: {agent_metrics['tasks_failed']}")
            print(f"  Success Rate: {agent_metrics['success_rate']:.2f}")
            print(f"  Average Time: {agent_metrics['avg_time']:.2f} seconds")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
