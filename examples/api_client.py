"""
Example of using the BitNet Virtual Co-worker Builder API client.
"""

import os
import sys
import time
import json
import logging
import argparse
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class BitNetVCClient:
    """
    Client for the BitNet Virtual Co-worker Builder API.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
    
    def get_models(self):
        """
        Get all models.
        
        Returns:
            List of models
        """
        response = requests.get(f"{self.base_url}/models")
        response.raise_for_status()
        return response.json()["models"]
    
    def create_model(self, name, model_path, kernel_type="i2_s", num_threads=4, context_size=2048,
                    temperature=0.7, top_p=0.9, top_k=40, repetition_penalty=1.1):
        """
        Create a new model.
        
        Args:
            name: Model name
            model_path: Path to the model
            kernel_type: Kernel type
            num_threads: Number of threads
            context_size: Context size
            temperature: Temperature
            top_p: Top-p
            top_k: Top-k
            repetition_penalty: Repetition penalty
            
        Returns:
            Response message
        """
        data = {
            "name": name,
            "model_path": model_path,
            "kernel_type": kernel_type,
            "num_threads": num_threads,
            "context_size": context_size,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repetition_penalty": repetition_penalty
        }
        
        response = requests.post(f"{self.base_url}/models", json=data)
        response.raise_for_status()
        return response.json()["message"]
    
    def get_virtual_coworkers(self):
        """
        Get all virtual co-workers.
        
        Returns:
            List of virtual co-workers
        """
        response = requests.get(f"{self.base_url}/virtual-coworkers")
        response.raise_for_status()
        return response.json()["virtual_coworkers"]
    
    def create_virtual_coworker(self, name, model_name, description="A helpful AI virtual co-worker",
                               system_prompt=None, tool_names=None):
        """
        Create a new virtual co-worker.
        
        Args:
            name: Virtual co-worker name
            model_name: Model name
            description: Virtual co-worker description
            system_prompt: System prompt
            tool_names: List of tool names
            
        Returns:
            Response message
        """
        data = {
            "name": name,
            "model_name": model_name,
            "description": description,
            "system_prompt": system_prompt,
            "tool_names": tool_names or []
        }
        
        response = requests.post(f"{self.base_url}/virtual-coworkers", json=data)
        response.raise_for_status()
        return response.json()["message"]
    
    def run_virtual_coworker(self, name, task):
        """
        Run a virtual co-worker on a task.
        
        Args:
            name: Virtual co-worker name
            task: Task description
            
        Returns:
            Task result
        """
        data = {
            "task": task
        }
        
        response = requests.post(f"{self.base_url}/virtual-coworkers/{name}/run", json=data)
        response.raise_for_status()
        
        task_id = response.json()["task_id"]
        
        # Wait for task to complete
        while True:
            task_response = requests.get(f"{self.base_url}/tasks/{task_id}")
            task_response.raise_for_status()
            
            task_data = task_response.json()
            
            if task_data["status"] == "completed":
                return task_data["result"]
            elif task_data["status"] == "failed":
                raise Exception(f"Task failed: {task_data['result']}")
            
            time.sleep(1)
    
    def get_teams(self):
        """
        Get all teams.
        
        Returns:
            List of teams
        """
        response = requests.get(f"{self.base_url}/teams")
        response.raise_for_status()
        return response.json()["teams"]
    
    def create_team(self, name, virtual_coworker_names, description="A team of AI virtual co-workers",
                   collaboration_mode="SEQUENTIAL", max_parallel_tasks=4, enable_conflict_resolution=True,
                   enable_task_prioritization=True, enable_performance_tracking=True):
        """
        Create a new team.
        
        Args:
            name: Team name
            virtual_coworker_names: List of virtual co-worker names
            description: Team description
            collaboration_mode: Collaboration mode
            max_parallel_tasks: Maximum number of parallel tasks
            enable_conflict_resolution: Whether to enable conflict resolution
            enable_task_prioritization: Whether to enable task prioritization
            enable_performance_tracking: Whether to enable performance tracking
            
        Returns:
            Response message
        """
        data = {
            "name": name,
            "description": description,
            "virtual_coworker_names": virtual_coworker_names,
            "collaboration_mode": collaboration_mode,
            "max_parallel_tasks": max_parallel_tasks,
            "enable_conflict_resolution": enable_conflict_resolution,
            "enable_task_prioritization": enable_task_prioritization,
            "enable_performance_tracking": enable_performance_tracking
        }
        
        response = requests.post(f"{self.base_url}/teams", json=data)
        response.raise_for_status()
        return response.json()["message"]
    
    def run_team(self, name, task, coordinator_agent_name=None):
        """
        Run a team on a task.
        
        Args:
            name: Team name
            task: Task description
            coordinator_agent_name: Name of the coordinator virtual co-worker
            
        Returns:
            Task result
        """
        data = {
            "task": task,
            "coordinator_agent_name": coordinator_agent_name
        }
        
        response = requests.post(f"{self.base_url}/teams/{name}/run", json=data)
        response.raise_for_status()
        
        task_id = response.json()["task_id"]
        
        # Wait for task to complete
        while True:
            task_response = requests.get(f"{self.base_url}/tasks/{task_id}")
            task_response.raise_for_status()
            
            task_data = task_response.json()
            
            if task_data["status"] == "completed":
                return task_data["result"]
            elif task_data["status"] == "failed":
                raise Exception(f"Task failed: {task_data['result']}")
            
            time.sleep(1)
    
    def get_tools(self):
        """
        Get all available tools.
        
        Returns:
            List of tools
        """
        response = requests.get(f"{self.base_url}/tools")
        response.raise_for_status()
        return response.json()["tools"]

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="BitNet Virtual Co-worker Builder API Client")
    
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000",
        help="URL of the API server"
    )
    
    parser.add_argument(
        "--action",
        type=str,
        choices=["list-models", "create-model", "list-virtual-coworkers", "create-virtual-coworker",
                "run-virtual-coworker", "list-teams", "create-team", "run-team", "list-tools"],
        required=True,
        help="Action to perform"
    )
    
    parser.add_argument(
        "--name",
        type=str,
        help="Name of the model, virtual co-worker, or team"
    )
    
    parser.add_argument(
        "--model-path",
        type=str,
        help="Path to the model"
    )
    
    parser.add_argument(
        "--model-name",
        type=str,
        help="Name of the model to use for a virtual co-worker"
    )
    
    parser.add_argument(
        "--description",
        type=str,
        help="Description of the virtual co-worker or team"
    )
    
    parser.add_argument(
        "--system-prompt",
        type=str,
        help="System prompt for the virtual co-worker"
    )
    
    parser.add_argument(
        "--tool-names",
        type=str,
        help="Comma-separated list of tool names"
    )
    
    parser.add_argument(
        "--virtual-coworker-names",
        type=str,
        help="Comma-separated list of virtual co-worker names"
    )
    
    parser.add_argument(
        "--collaboration-mode",
        type=str,
        choices=["SEQUENTIAL", "PARALLEL", "HIERARCHICAL", "CONSENSUS"],
        default="SEQUENTIAL",
        help="Collaboration mode for the team"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        help="Task to run"
    )
    
    parser.add_argument(
        "--coordinator",
        type=str,
        help="Name of the coordinator virtual co-worker"
    )
    
    args = parser.parse_args()
    
    # Create client
    client = BitNetVCClient(args.url)
    
    # Perform action
    if args.action == "list-models":
        models = client.get_models()
        print(f"Models: {models}")
    
    elif args.action == "create-model":
        if not args.name or not args.model_path:
            parser.error("--name and --model-path are required for create-model")
        
        message = client.create_model(args.name, args.model_path)
        print(message)
    
    elif args.action == "list-virtual-coworkers":
        virtual_coworkers = client.get_virtual_coworkers()
        print(f"Virtual Co-workers: {virtual_coworkers}")
    
    elif args.action == "create-virtual-coworker":
        if not args.name or not args.model_name:
            parser.error("--name and --model-name are required for create-virtual-coworker")
        
        tool_names = args.tool_names.split(",") if args.tool_names else []
        
        message = client.create_virtual_coworker(
            args.name,
            args.model_name,
            args.description or f"A virtual co-worker named {args.name}",
            args.system_prompt,
            tool_names
        )
        
        print(message)
    
    elif args.action == "run-virtual-coworker":
        if not args.name or not args.task:
            parser.error("--name and --task are required for run-virtual-coworker")
        
        result = client.run_virtual_coworker(args.name, args.task)
        print(f"Result: {result}")
    
    elif args.action == "list-teams":
        teams = client.get_teams()
        print(f"Teams: {teams}")
    
    elif args.action == "create-team":
        if not args.name or not args.virtual_coworker_names:
            parser.error("--name and --virtual-coworker-names are required for create-team")
        
        virtual_coworker_names = args.virtual_coworker_names.split(",")
        
        message = client.create_team(
            args.name,
            virtual_coworker_names,
            args.description or f"A team named {args.name}",
            args.collaboration_mode
        )
        
        print(message)
    
    elif args.action == "run-team":
        if not args.name or not args.task:
            parser.error("--name and --task are required for run-team")
        
        result = client.run_team(args.name, args.task, args.coordinator)
        print(f"Result: {result}")
    
    elif args.action == "list-tools":
        tools = client.get_tools()
        print(json.dumps(tools, indent=2))

if __name__ == "__main__":
    main()
