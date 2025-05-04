"""
Main entry point for BitNet Virtual Co-worker Builder.
"""

import os
import sys
import argparse
import logging
from typing import Dict, Any, Optional

from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.core.team import BitNetTeam, CollaborationMode
from bitnet_vc_builder.tools.common_tools import get_available_tools
from bitnet_vc_builder.config.config_loader import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="BitNet Virtual Co-worker Builder")
    
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        help="Path to BitNet model"
    )
    
    parser.add_argument(
        "--kernel-type",
        type=str,
        choices=["i2_s", "i2_m", "i2_l"],
        help="BitNet kernel type"
    )
    
    parser.add_argument(
        "--bitnet-path",
        type=str,
        help="Path to BitNet installation"
    )
    
    parser.add_argument(
        "--virtual-coworker",
        type=str,
        help="Name of the virtual co-worker to run"
    )
    
    parser.add_argument(
        "--team",
        type=str,
        help="Name of the team to run"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        help="Task to run"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available virtual co-workers and teams"
    )
    
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run API server"
    )
    
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Run web UI"
    )
    
    return parser.parse_args()

def load_model(config: Dict[str, Any], args) -> BitNetModel:
    """
    Load BitNet model.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
        
    Returns:
        BitNetModel instance
    """
    # Get model path
    model_path = args.model or config.get("model", {}).get("path")
    
    if not model_path:
        logger.error("Model path not specified")
        sys.exit(1)
    
    # Get kernel type
    kernel_type = args.kernel_type or config.get("model", {}).get("kernel_type", "i2_s")
    
    # Get BitNet path
    bitnet_path = args.bitnet_path or config.get("bitnet", {}).get("path")
    
    # Get other model parameters
    num_threads = config.get("model", {}).get("num_threads", 4)
    context_size = config.get("model", {}).get("context_size", 2048)
    temperature = config.get("model", {}).get("temperature", 0.7)
    top_p = config.get("model", {}).get("top_p", 0.9)
    top_k = config.get("model", {}).get("top_k", 40)
    repetition_penalty = config.get("model", {}).get("repetition_penalty", 1.1)
    
    # Create model
    logger.info(f"Loading BitNet model from {model_path} with kernel type {kernel_type}")
    
    model = BitNetModel(
        model_path=model_path,
        kernel_type=kernel_type,
        bitnet_path=bitnet_path,
        num_threads=num_threads,
        context_size=context_size,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repetition_penalty=repetition_penalty
    )
    
    return model

def create_agent(config: Dict[str, Any], model: BitNetModel) -> BitNetVirtualCoworker:
    """
    Create a BitNet virtual co-worker from configuration.
    
    Args:
        config: Virtual co-worker configuration
        model: BitNetModel instance
        
    Returns:
        BitNetVirtualCoworker instance
    """
    logger.info(f"Creating BitNet virtual co-worker with config: {config}")
    
    # Get tools
    available_tools = get_available_tools()
    tools = []
    
    for tool_name in config.get("tools", []):
        if tool_name in available_tools:
            tools.append(available_tools[tool_name])
    
    # Create virtual co-worker
    agent = BitNetVirtualCoworker(
        model=model,
        tools=tools,
        name=config.get("name", "BitNetVirtualCoworker"),
        description=config.get("description", "A helpful AI virtual co-worker"),
        system_prompt=config.get("system_prompt")
    )
    
    return agent

def create_team(config: Dict[str, Any], agents: Dict[str, BitNetVirtualCoworker]) -> BitNetTeam:
    """
    Create a BitNet team from configuration.
    
    Args:
        config: Team configuration
        agents: Dictionary of available virtual co-workers
        
    Returns:
        BitNetTeam instance
    """
    logger.info(f"Creating BitNet team with config: {config}")
    
    # Get virtual co-workers
    team_agents = []
    
    for agent_name in config.get("agents", []):
        if agent_name in agents:
            team_agents.append(agents[agent_name])
    
    # Get collaboration mode
    collaboration_mode_str = config.get("collaboration_mode", "SEQUENTIAL")
    collaboration_mode = getattr(CollaborationMode, collaboration_mode_str, CollaborationMode.SEQUENTIAL)
    
    # Create team
    team = BitNetTeam(
        agents=team_agents,
        name=config.get("name", "BitNetTeam"),
        description=config.get("description", "A team of AI virtual co-workers"),
        collaboration_mode=collaboration_mode,
        max_parallel_tasks=config.get("max_parallel_tasks", 4),
        enable_conflict_resolution=config.get("enable_conflict_resolution", True),
        enable_task_prioritization=config.get("enable_task_prioritization", True),
        enable_performance_tracking=config.get("enable_performance_tracking", True)
    )
    
    return team

def run_agent(agent: BitNetVirtualCoworker, task: str) -> str:
    """
    Run a virtual co-worker on a task.
    
    Args:
        agent: BitNetVirtualCoworker instance
        task: Task description
        
    Returns:
        Virtual co-worker's response
    """
    logger.info(f"Running virtual co-worker {agent.name} on task: {task}")
    
    result = agent.run(task)
    
    return result

def run_team(team: BitNetTeam, task: str, coordinator_agent_name: Optional[str] = None) -> str:
    """
    Run a team on a task.
    
    Args:
        team: BitNetTeam instance
        task: Task description
        coordinator_agent_name: Name of the virtual co-worker to coordinate the task
        
    Returns:
        Team's response
    """
    logger.info(f"Running team {team.name} on task: {task}")
    
    result = team.run(task, coordinator_agent_name)
    
    return result

def run_server(config: Dict[str, Any]):
    """
    Run API server.
    
    Args:
        config: Configuration dictionary
    """
    logger.info("Starting API server")
    
    # Import server module
    from bitnet_vc_builder.api.server import app
    import uvicorn
    
    # Get server configuration
    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8000)
    
    # Run server
    uvicorn.run(app, host=host, port=port)

def run_ui(config: Dict[str, Any]):
    """
    Run web UI.
    
    Args:
        config: Configuration dictionary
    """
    logger.info("Starting web UI")
    
    # Import UI module
    # TODO: Implement web UI
    
    logger.error("Web UI not implemented yet")
    sys.exit(1)

def main():
    """
    Main entry point.
    """
    # Parse command line arguments
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Check if we should run the server
    if args.server:
        run_server(config)
        return
    
    # Check if we should run the UI
    if args.ui:
        run_ui(config)
        return
    
    # Load model
    model = load_model(config, args)
    
    # Load virtual co-workers
    agents = {}
    
    for agent_config in config.get("agents", []):
        agent = create_agent(agent_config, model)
        agents[agent.name] = agent
    
    # Load teams
    teams = {}
    
    for team_config in config.get("teams", []):
        team = create_team(team_config, agents)
        teams[team.name] = team
    
    # Check if we should list virtual co-workers and teams
    if args.list:
        # Print available virtual co-workers and teams
        print("Available virtual co-workers:")
        for agent_name in agents:
            print(f"  - {agent_name}")
        
        print("\nAvailable teams:")
        for team_name in teams:
            print(f"  - {team_name}")
        
        return
    
    # Check if we should run a virtual co-worker
    if args.virtual_coworker:
        if args.virtual_coworker not in agents:
            logger.error(f"Virtual co-worker {args.virtual_coworker} not found")
            sys.exit(1)
        
        if not args.task:
            logger.error("Task not specified")
            sys.exit(1)
        
        # Run virtual co-worker
        agent = agents[args.virtual_coworker]
        result = run_agent(agent, args.task)
        
        print(f"\nVirtual Co-worker Response:")
        print(result)
        
        return
    
    # Check if we should run a team
    if args.team:
        if args.team not in teams:
            logger.error(f"Team {args.team} not found")
            sys.exit(1)
        
        if not args.task:
            logger.error("Task not specified")
            sys.exit(1)
        
        # Run team
        team = teams[args.team]
        result = run_team(team, args.task)
        
        print(f"\nTeam Response:")
        print(result)
        
        return
    
    # If we get here, no action was specified
    logger.error("No action specified. Use --help for usage information.")
    sys.exit(1)

if __name__ == "__main__":
    main()
