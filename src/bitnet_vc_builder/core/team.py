"""
Multi-virtual co-worker collaboration system for BitNet Virtual Co-worker Builder.
"""

import os
import json
import time
import logging
import threading
from typing import List, Dict, Any, Optional, Union, Callable, Set
from enum import Enum
from collections import deque

from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker

logger = logging.getLogger(__name__)

class CollaborationMode(Enum):
    """
    Collaboration modes for BitNet teams.
    """
    SEQUENTIAL = "sequential"  # Agents work one after another
    PARALLEL = "parallel"      # Agents work in parallel
    HIERARCHICAL = "hierarchical"  # Agents work in a hierarchical structure
    CONSENSUS = "consensus"    # Agents work together to reach a consensus

class TaskStatus(Enum):
    """
    Status of a task.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task:
    """
    Task for BitNet team.
    """
    
    def __init__(
        self,
        task_id: str,
        description: str,
        assigned_agent: Optional[str] = None,
        priority: int = 1,
        dependencies: Optional[List[str]] = None
    ):
        """
        Initialize task.
        
        Args:
            task_id: Task ID
            description: Task description
            assigned_agent: Name of the agent assigned to the task
            priority: Task priority (1-5, 5 being highest)
            dependencies: List of task IDs that this task depends on
        """
        self.task_id = task_id
        self.description = description
        self.assigned_agent = assigned_agent
        self.priority = priority
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING
        self.result = None
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
        self.error = None

class BitNetTeam:
    """
    Manage multiple BitNet virtual co-workers working together.

    This class provides functionality for creating and managing teams of
    specialized virtual co-workers that can collaborate on complex tasks.
    """

    def __init__(
        self,
        agents: Optional[List[BitNetVirtualCoworker]] = None,
        name: str = "BitNetTeam",
        description: str = "A team of AI virtual co-workers powered by BitNet.",
        collaboration_mode: CollaborationMode = CollaborationMode.SEQUENTIAL,
        max_parallel_tasks: int = 4,
        enable_conflict_resolution: bool = True,
        enable_task_prioritization: bool = True,
        enable_performance_tracking: bool = True
    ):
        """
        Initialize BitNet team.

        Args:
            agents: List of BitNet virtual co-workers
            name: Name of the team
            description: Description of the team
            collaboration_mode: Mode of collaboration between virtual co-workers
            max_parallel_tasks: Maximum number of tasks to execute in parallel
            enable_conflict_resolution: Whether to enable conflict resolution
            enable_task_prioritization: Whether to enable task prioritization
            enable_performance_tracking: Whether to enable performance tracking
        """
        self.agents = agents or []
        self.name = name
        self.description = description
        self.collaboration_mode = collaboration_mode
        self.max_parallel_tasks = max_parallel_tasks
        self.enable_conflict_resolution = enable_conflict_resolution
        self.enable_task_prioritization = enable_task_prioritization
        self.enable_performance_tracking = enable_performance_tracking
        
        # Create agent map for quick lookup
        self._agent_map = {agent.name: agent for agent in self.agents}
        
        # Task management
        self.tasks = {}
        self.task_queue = deque()
        self.active_tasks = set()
        self.completed_tasks = set()
        self.failed_tasks = set()
        self.next_task_id = 1
        
        # Performance tracking
        self.agent_performance = {
            agent.name: {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "avg_time": 0.0
            }
            for agent in self.agents
        }
        
        # Locks for thread safety
        self._task_lock = threading.Lock()
        self._performance_lock = threading.Lock()
    
    def add_agent(self, agent: BitNetVirtualCoworker) -> None:
        """
        Add a virtual co-worker to the team.
        
        Args:
            agent: BitNet virtual co-worker to add
        """
        if agent.name in self._agent_map:
            logger.warning(f"Virtual co-worker {agent.name} already exists in the team. Replacing.")
        
        self.agents.append(agent)
        self._agent_map[agent.name] = agent
        
        # Initialize performance tracking for the new virtual co-worker
        if self.enable_performance_tracking:
            with self._performance_lock:
                self.agent_performance[agent.name] = {
                    "tasks_completed": 0,
                    "tasks_failed": 0,
                    "avg_time": 0.0
                }
    
    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove a virtual co-worker from the team.
        
        Args:
            agent_name: Name of the virtual co-worker to remove
            
        Returns:
            True if the virtual co-worker was removed, False otherwise
        """
        if agent_name not in self._agent_map:
            logger.warning(f"Virtual co-worker {agent_name} does not exist in the team.")
            return False
        
        agent = self._agent_map[agent_name]
        self.agents.remove(agent)
        del self._agent_map[agent_name]
        
        # Remove performance tracking for the virtual co-worker
        if self.enable_performance_tracking:
            with self._performance_lock:
                if agent_name in self.agent_performance:
                    del self.agent_performance[agent_name]
        
        return True
    
    def get_agent(self, agent_name: str) -> Optional[BitNetVirtualCoworker]:
        """
        Get a virtual co-worker by name.
        
        Args:
            agent_name: Name of the virtual co-worker
            
        Returns:
            BitNet virtual co-worker or None if not found
        """
        return self._agent_map.get(agent_name)
    
    def create_task(
        self,
        description: str,
        assigned_agent: Optional[str] = None,
        priority: int = 1,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """
        Create a new task.
        
        Args:
            description: Task description
            assigned_agent: Name of the virtual co-worker assigned to the task
            priority: Task priority (1-5, 5 being highest)
            dependencies: List of task IDs that this task depends on
            
        Returns:
            Task ID
        """
        with self._task_lock:
            task_id = f"task_{self.next_task_id}"
            self.next_task_id += 1
            
            task = Task(
                task_id=task_id,
                description=description,
                assigned_agent=assigned_agent,
                priority=priority,
                dependencies=dependencies
            )
            
            self.tasks[task_id] = task
            
            # Add to queue if no dependencies or all dependencies are completed
            if not task.dependencies or all(dep_id in self.completed_tasks for dep_id in task.dependencies):
                if self.enable_task_prioritization:
                    # Insert task in priority order
                    for i, queued_task_id in enumerate(self.task_queue):
                        queued_task = self.tasks[queued_task_id]
                        if task.priority > queued_task.priority:
                            self.task_queue.insert(i, task_id)
                            break
                    else:
                        self.task_queue.append(task_id)
                else:
                    self.task_queue.append(task_id)
            
            return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task or None if not found
        """
        return self.tasks.get(task_id)
    
    def run(self, task: str, coordinator_agent_name: Optional[str] = None) -> str:
        """
        Run team on a task.

        Args:
            task: Task description
            coordinator_agent_name: Name of the virtual co-worker to coordinate the task

        Returns:
            Team's response
        """
        logger.info(f"Running team {self.name} on task: {task}")

        if not self.agents:
            return "No virtual co-workers available in the team."

        # If coordinator is specified, use that virtual co-worker
        if coordinator_agent_name and coordinator_agent_name in self._agent_map:
            coordinator = self._agent_map[coordinator_agent_name]
        else:
            # Otherwise, use the first virtual co-worker as coordinator
            coordinator = self.agents[0]

        # Different collaboration modes
        if self.collaboration_mode == CollaborationMode.SEQUENTIAL:
            return self._run_sequential(task, coordinator)
        elif self.collaboration_mode == CollaborationMode.PARALLEL:
            return self._run_parallel(task, coordinator)
        elif self.collaboration_mode == CollaborationMode.HIERARCHICAL:
            return self._run_hierarchical(task, coordinator)
        elif self.collaboration_mode == CollaborationMode.CONSENSUS:
            return self._run_consensus(task, coordinator)
        else:
            return self._run_sequential(task, coordinator)
    
    def run_async(self, task: str, coordinator_agent_name: Optional[str] = None, callback: Optional[Callable[[str], None]] = None) -> str:
        """
        Run team on a task asynchronously.

        Args:
            task: Task description
            coordinator_agent_name: Name of the virtual co-worker to coordinate the task
            callback: Callback function to call with the result

        Returns:
            Task ID
        """
        logger.info(f"Running team {self.name} on task asynchronously: {task}")

        # Create a task
        task_id = self.create_task(
            description=task,
            assigned_agent=coordinator_agent_name,
            priority=2  # Higher priority for user-initiated tasks
        )

        # Start a thread to run the task
        def run_task_thread():
            result = self.run(task, coordinator_agent_name)
            
            # Update task
            with self._task_lock:
                task_obj = self.tasks[task_id]
                task_obj.status = TaskStatus.COMPLETED
                task_obj.result = result
                task_obj.completed_at = time.time()
                self.completed_tasks.add(task_id)
            
            # Call callback if provided
            if callback:
                callback(result)
        
        thread = threading.Thread(target=run_task_thread)
        thread.daemon = True
        thread.start()
        
        return task_id
    
    def _run_sequential(self, task: str, coordinator: BitNetVirtualCoworker) -> str:
        """
        Run virtual co-workers sequentially on a task.
        
        Args:
            task: Task description
            coordinator: Coordinator virtual co-worker
            
        Returns:
            Team's response
        """
        logger.info(f"Running team {self.name} in sequential mode")
        
        # Start with the coordinator's response
        current_result = coordinator.run(task)
        
        # Track performance if enabled
        if self.enable_performance_tracking:
            with self._performance_lock:
                perf = self.agent_performance[coordinator.name]
                perf["tasks_completed"] += 1
        
        # Pass the result to each virtual co-worker in sequence
        for agent in self.agents:
            # Skip the coordinator
            if agent == coordinator:
                continue
            
            # Create a new task for the virtual co-worker
            agent_task = f"Task: {task}\n\nPrevious work: {current_result}\n\nContinue the work."
            
            # Run the virtual co-worker
            start_time = time.time()
            try:
                agent_result = agent.run(agent_task)
                current_result = agent_result
                
                # Track performance if enabled
                if self.enable_performance_tracking:
                    with self._performance_lock:
                        perf = self.agent_performance[agent.name]
                        perf["tasks_completed"] += 1
                        execution_time = time.time() - start_time
                        perf["avg_time"] = ((perf["avg_time"] * (perf["tasks_completed"] - 1)) + execution_time) / perf["tasks_completed"]
            except Exception as e:
                logger.error(f"Error running virtual co-worker {agent.name}: {e}")
                
                # Track performance if enabled
                if self.enable_performance_tracking:
                    with self._performance_lock:
                        perf = self.agent_performance[agent.name]
                        perf["tasks_failed"] += 1
        
        return current_result
    
    def _run_parallel(self, task: str, coordinator: BitNetVirtualCoworker) -> str:
        """
        Run virtual co-workers in parallel on a task.
        
        Args:
            task: Task description
            coordinator: Coordinator virtual co-worker
            
        Returns:
            Team's response
        """
        logger.info(f"Running team {self.name} in parallel mode")
        
        # Coordinator creates a plan
        plan_prompt = f"""
        Task: {task}
        
        You need to create a plan to solve this task by breaking it down into subtasks.
        Each subtask will be assigned to a different virtual co-worker.
        
        Available virtual co-workers:
        {', '.join(agent.name for agent in self.agents)}
        
        Create a plan with the following format:
        [
            {{
                "subtask": "Description of subtask 1",
                "agent_name": "Name of virtual co-worker for subtask 1",
                "depends_on": []
            }},
            {{
                "subtask": "Description of subtask 2",
                "agent_name": "Name of virtual co-worker for subtask 2",
                "depends_on": [0]
            }},
            ...
        ]
        
        The "depends_on" field should contain the indices of the subtasks that this subtask depends on.
        If a subtask doesn't depend on any other subtasks, use an empty list.
        """
        
        plan_result = coordinator.run(plan_prompt)
        
        # Extract the plan from the result
        try:
            # Find the JSON array in the result
            start_idx = plan_result.find("[")
            end_idx = plan_result.rfind("]") + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("Could not find a valid plan in the coordinator's response")
                return f"Error: Could not create a plan for the task. Coordinator's response: {plan_result}"
            
            plan_json = plan_result[start_idx:end_idx]
            plan = json.loads(plan_json)
        except Exception as e:
            logger.error(f"Error parsing plan: {e}")
            return f"Error: Could not parse the plan. Coordinator's response: {plan_result}"
        
        # Execute the plan
        results = {}
        threads = {}
        results_lock = threading.Lock()
        
        def execute_step(step_idx, step):
            agent_name = step["agent_name"]
            subtask = step["subtask"]
            
            # Get the virtual co-worker
            if agent_name not in self._agent_map:
                with results_lock:
                    results[step_idx] = f"Error: Virtual co-worker {agent_name} not found"
                return
            
            agent = self._agent_map[agent_name]
            
            # Get the results of dependencies
            dependencies_results = ""
            for dep_idx in step["depends_on"]:
                if dep_idx in results:
                    dependencies_results += f"Result from step {dep_idx}: {results[dep_idx]}\n\n"
            
            # Create the virtual co-worker task
            agent_task = f"""
            Task: {task}
            
            Your specific subtask: {subtask}
            
            {dependencies_results}
            
            Please complete your subtask.
            """
            
            # Run the virtual co-worker
            start_time = time.time()
            try:
                agent_result = agent.run(agent_task)
                
                with results_lock:
                    results[step_idx] = agent_result
                
                # Update performance metrics if enabled
                if self.enable_performance_tracking:
                    end_time = time.time()
                    execution_time = end_time - start_time

                    # Update virtual co-worker performance
                    with results_lock:
                        perf = self.agent_performance[agent_name]
                        perf["tasks_completed"] += 1
                        perf["avg_time"] = ((perf["avg_time"] * (perf["tasks_completed"] - 1)) + execution_time) / perf["tasks_completed"]

            except Exception as e:
                logger.error(f"Error running virtual co-worker {agent_name}: {e}")
                with results_lock:
                    results[step_idx] = f"Error: {str(e)}"
                
                # Update performance metrics if enabled
                if self.enable_performance_tracking:
                    with results_lock:
                        perf = self.agent_performance[agent_name]
                        perf["tasks_failed"] += 1
        
        # Create threads for steps with no dependencies
        for i, step in enumerate(plan):
            if not step["depends_on"]:
                threads[i] = threading.Thread(target=execute_step, args=(i, step))
                threads[i].start()
        
        # Wait for all threads to complete
        while len(results) < len(plan):
            # Check if we can start any new threads
            for i, step in enumerate(plan):
                if i not in threads and all(dep_idx in results for dep_idx in step["depends_on"]):
                    threads[i] = threading.Thread(target=execute_step, args=(i, step))
                    threads[i].start()
            
            time.sleep(0.1)
        
        # Compile the final result
        final_result = "Task Execution Results:\n\n"
        for i, step in enumerate(plan):
            final_result += f"Step {i} ({step['agent_name']} - {step['subtask']}):\n{results[i]}\n\n"
        
        return final_result
    
    def _run_hierarchical(self, task: str, coordinator: BitNetVirtualCoworker) -> str:
        """
        Run virtual co-workers in a hierarchical structure on a task.
        
        Args:
            task: Task description
            coordinator: Coordinator virtual co-worker
            
        Returns:
            Team's response
        """
        logger.info(f"Running team {self.name} in hierarchical mode")
        
        # Coordinator creates a hierarchical plan
        plan_prompt = f"""
        Task: {task}
        
        You need to create a hierarchical plan to solve this task.
        You will be the coordinator, and you'll delegate subtasks to other virtual co-workers.
        
        Available virtual co-workers:
        {', '.join(agent.name for agent in self.agents if agent != coordinator)}
        
        Create a hierarchical plan with the following format:
        [
            {{
                "subtask": "Description of subtask 1",
                "agent_name": "Name of virtual co-worker for subtask 1"
            }},
            {{
                "subtask": "Description of subtask 2",
                "agent_name": "Name of virtual co-worker for subtask 2"
            }},
            ...
        ]
        """
        
        plan_result = coordinator.run(plan_prompt)
        
        # Extract the plan from the result
        try:
            # Find the JSON array in the result
            start_idx = plan_result.find("[")
            end_idx = plan_result.rfind("]") + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("Could not find a valid plan in the coordinator's response")
                return f"Error: Could not create a plan for the task. Coordinator's response: {plan_result}"
            
            plan_json = plan_result[start_idx:end_idx]
            plan = json.loads(plan_json)
        except Exception as e:
            logger.error(f"Error parsing plan: {e}")
            return f"Error: Could not parse the plan. Coordinator's response: {plan_result}"
        
        # Execute the plan
        subtask_results = []
        
        for step in plan:
            agent_name = step["agent_name"]
            subtask = step["subtask"]
            
            # Get the virtual co-worker
            if agent_name not in self._agent_map:
                subtask_results.append(f"Error: Virtual co-worker {agent_name} not found")
                continue
            
            agent = self._agent_map[agent_name]
            
            # Run the virtual co-worker
            start_time = time.time()
            try:
                agent_result = agent.run(subtask)
                subtask_results.append(agent_result)
                
                # Update performance metrics if enabled
                if self.enable_performance_tracking:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    with self._performance_lock:
                        perf = self.agent_performance[agent_name]
                        perf["tasks_completed"] += 1
                        perf["avg_time"] = ((perf["avg_time"] * (perf["tasks_completed"] - 1)) + execution_time) / perf["tasks_completed"]
            except Exception as e:
                logger.error(f"Error running virtual co-worker {agent_name}: {e}")
                subtask_results.append(f"Error: {str(e)}")
                
                # Update performance metrics if enabled
                if self.enable_performance_tracking:
                    with self._performance_lock:
                        perf = self.agent_performance[agent_name]
                        perf["tasks_failed"] += 1
        
        # Coordinator synthesizes the final result
        synthesis_prompt = f"""
        Task: {task}
        
        You delegated the following subtasks to other virtual co-workers:
        
        {', '.join(step['subtask'] for step in plan)}
        
        Here are the results from each virtual co-worker:
        
        {', '.join(f"Result {i+1}: {result}" for i, result in enumerate(subtask_results))}
        
        Please synthesize these results into a final response that addresses the original task.
        """
        
        final_result = coordinator.run(synthesis_prompt)
        
        # Update performance metrics for coordinator if enabled
        if self.enable_performance_tracking:
            with self._performance_lock:
                perf = self.agent_performance[coordinator.name]
                perf["tasks_completed"] += 1
        
        return final_result
    
    def _run_consensus(self, task: str, coordinator: BitNetVirtualCoworker) -> str:
        """
        Run virtual co-workers to reach a consensus on a task.
        
        Args:
            task: Task description
            coordinator: Coordinator virtual co-worker
            
        Returns:
            Team's response
        """
        logger.info(f"Running team {self.name} in consensus mode")
        
        # Each virtual co-worker works on the task independently
        agent_results = {}
        
        for agent in self.agents:
            # Run the virtual co-worker
            start_time = time.time()
            try:
                agent_result = agent.run(task)
                agent_results[agent.name] = agent_result
                
                # Update performance metrics if enabled
                if self.enable_performance_tracking:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    with self._performance_lock:
                        perf = self.agent_performance[agent.name]
                        perf["tasks_completed"] += 1
                        perf["avg_time"] = ((perf["avg_time"] * (perf["tasks_completed"] - 1)) + execution_time) / perf["tasks_completed"]
            except Exception as e:
                logger.error(f"Error running virtual co-worker {agent.name}: {e}")
                agent_results[agent.name] = f"Error: {str(e)}"
                
                # Update performance metrics if enabled
                if self.enable_performance_tracking:
                    with self._performance_lock:
                        perf = self.agent_performance[agent.name]
                        perf["tasks_failed"] += 1
        
        # Coordinator synthesizes the consensus
        consensus_prompt = f"""
        Task: {task}
        
        The following virtual co-workers have provided their responses:
        
        {', '.join(f"{agent_name}: {result}" for agent_name, result in agent_results.items())}
        
        Please synthesize these responses into a consensus that represents the best answer to the task.
        Highlight areas of agreement and address any disagreements.
        """
        
        consensus_result = coordinator.run(consensus_prompt)
        
        return consensus_result
    
    def get_performance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get performance metrics for all virtual co-workers.
        
        Returns:
            Dictionary of virtual co-worker performance metrics
        """
        if not self.enable_performance_tracking:
            return {}
        
        with self._performance_lock:
            return self.agent_performance.copy()
    
    def get_agent_performance(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Get performance metrics for a specific virtual co-worker.
        
        Args:
            agent_name: Name of the virtual co-worker
            
        Returns:
            Dictionary of virtual co-worker performance metrics or None if not found
        """
        if not self.enable_performance_tracking:
            return None
        
        with self._performance_lock:
            return self.agent_performance.get(agent_name)
