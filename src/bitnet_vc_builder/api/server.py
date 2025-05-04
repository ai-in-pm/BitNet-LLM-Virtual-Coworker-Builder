"""
API server for BitNet Virtual Co-worker Builder.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.tools.base_tools import Tool
from bitnet_vc_builder.core.team import BitNetTeam, CollaborationMode
from bitnet_vc_builder.config.config_loader import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BitNet Virtual Co-worker Builder API",
    description="API for creating and managing BitNet virtual co-workers and teams",
    version="0.2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for models, virtual co-workers, and teams
models: Dict[str, BitNetModel] = {}
virtual_coworkers: Dict[str, BitNetVirtualCoworker] = {}
teams: Dict[str, BitNetTeam] = {}
tasks: Dict[str, Dict[str, Any]] = {}

# Pydantic models for API requests and responses
class ModelConfig(BaseModel):
    name: str
    model_path: str
    kernel_type: str = "i2_s"
    bitnet_path: Optional[str] = None
    num_threads: int = 4
    context_size: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repetition_penalty: float = 1.1
    use_bitnet_integration: bool = True

class VirtualCoworkerConfig(BaseModel):
    name: str
    model_name: str
    description: str = "A helpful AI virtual co-worker powered by BitNet."
    system_prompt: Optional[str] = None
    tools: List[str] = []

class TeamConfig(BaseModel):
    name: str
    description: str = "A team of AI virtual co-workers powered by BitNet."
    virtual_coworker_names: List[str]
    collaboration_mode: str = "SEQUENTIAL"
    max_parallel_tasks: int = 4
    enable_conflict_resolution: bool = True
    enable_task_prioritization: bool = True
    enable_performance_tracking: bool = True

class TaskRequest(BaseModel):
    task: str
    coordinator_name: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str = "pending"
    result: Optional[str] = None

# API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to BitNet Virtual Co-worker Builder API"}

@app.get("/models")
async def get_models():
    return {"models": list(models.keys())}

@app.post("/models")
async def create_model(model_config: ModelConfig):
    if model_config.name in models:
        raise HTTPException(status_code=400, detail=f"Model {model_config.name} already exists")
    
    try:
        model = BitNetModel(
            model_path=model_config.model_path,
            kernel_type=model_config.kernel_type,
            bitnet_path=model_config.bitnet_path,
            num_threads=model_config.num_threads,
            context_size=model_config.context_size,
            temperature=model_config.temperature,
            top_p=model_config.top_p,
            top_k=model_config.top_k,
            repetition_penalty=model_config.repetition_penalty,
            use_bitnet_integration=model_config.use_bitnet_integration
        )
        
        models[model_config.name] = model
        
        return {"message": f"Model {model_config.name} created successfully"}
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating model: {str(e)}")

@app.delete("/models/{model_name}")
async def delete_model(model_name: str):
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    # Check if any virtual co-workers are using this model
    for coworker in virtual_coworkers.values():
        if coworker.model == models[model_name]:
            raise HTTPException(status_code=400, detail=f"Model {model_name} is in use by virtual co-worker {coworker.name}")
    
    del models[model_name]
    
    return {"message": f"Model {model_name} deleted successfully"}

@app.get("/virtual-coworkers")
async def get_virtual_coworkers():
    return {"virtual_coworkers": list(virtual_coworkers.keys())}

@app.post("/virtual-coworkers")
async def create_virtual_coworker(coworker_config: VirtualCoworkerConfig):
    if coworker_config.name in virtual_coworkers:
        raise HTTPException(status_code=400, detail=f"Virtual co-worker {coworker_config.name} already exists")
    
    if coworker_config.model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {coworker_config.model_name} not found")
    
    try:
        # Get tools
        tools = []
        # TODO: Implement tool loading
        
        # Create virtual co-worker
        coworker = BitNetVirtualCoworker(
            model=models[coworker_config.model_name],
            tools=tools,
            name=coworker_config.name,
            description=coworker_config.description,
            system_prompt=coworker_config.system_prompt
        )
        
        virtual_coworkers[coworker_config.name] = coworker
        
        return {"message": f"Virtual co-worker {coworker_config.name} created successfully"}
    except Exception as e:
        logger.error(f"Error creating virtual co-worker: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating virtual co-worker: {str(e)}")

@app.delete("/virtual-coworkers/{coworker_name}")
async def delete_virtual_coworker(coworker_name: str):
    if coworker_name not in virtual_coworkers:
        raise HTTPException(status_code=404, detail=f"Virtual co-worker {coworker_name} not found")
    
    # Check if any teams are using this virtual co-worker
    for team in teams.values():
        if coworker_name in [agent.name for agent in team.agents]:
            raise HTTPException(status_code=400, detail=f"Virtual co-worker {coworker_name} is in use by team {team.name}")
    
    del virtual_coworkers[coworker_name]
    
    return {"message": f"Virtual co-worker {coworker_name} deleted successfully"}

@app.post("/virtual-coworkers/{coworker_name}/run")
async def run_virtual_coworker(coworker_name: str, task_request: TaskRequest, background_tasks: BackgroundTasks):
    if coworker_name not in virtual_coworkers:
        raise HTTPException(status_code=404, detail=f"Virtual co-worker {coworker_name} not found")
    
    coworker = virtual_coworkers[coworker_name]
    
    # Generate task ID
    task_id = f"task_{len(tasks) + 1}"
    
    # Create task
    tasks[task_id] = {
        "task": task_request.task,
        "status": "pending",
        "result": None
    }
    
    # Run virtual co-worker in background
    def run_task():
        try:
            result = coworker.run(task_request.task)
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["result"] = result
        except Exception as e:
            logger.error(f"Error running virtual co-worker: {e}")
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["result"] = f"Error: {str(e)}"
    
    background_tasks.add_task(run_task)
    
    return {"task_id": task_id, "status": "pending"}

@app.get("/teams")
async def get_teams():
    return {"teams": list(teams.keys())}

@app.post("/teams")
async def create_team(team_config: TeamConfig):
    if team_config.name in teams:
        raise HTTPException(status_code=400, detail=f"Team {team_config.name} already exists")
    
    # Check if all virtual co-workers exist
    for coworker_name in team_config.virtual_coworker_names:
        if coworker_name not in virtual_coworkers:
            raise HTTPException(status_code=404, detail=f"Virtual co-worker {coworker_name} not found")
    
    try:
        # Get virtual co-workers
        team_coworkers = [virtual_coworkers[name] for name in team_config.virtual_coworker_names]
        
        # Get collaboration mode
        collaboration_mode = getattr(CollaborationMode, team_config.collaboration_mode, CollaborationMode.SEQUENTIAL)
        
        # Create team
        team = BitNetTeam(
            agents=team_coworkers,
            name=team_config.name,
            description=team_config.description,
            collaboration_mode=collaboration_mode,
            max_parallel_tasks=team_config.max_parallel_tasks,
            enable_conflict_resolution=team_config.enable_conflict_resolution,
            enable_task_prioritization=team_config.enable_task_prioritization,
            enable_performance_tracking=team_config.enable_performance_tracking
        )
        
        teams[team_config.name] = team
        
        return {"message": f"Team {team_config.name} created successfully"}
    except Exception as e:
        logger.error(f"Error creating team: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating team: {str(e)}")

@app.delete("/teams/{team_name}")
async def delete_team(team_name: str):
    if team_name not in teams:
        raise HTTPException(status_code=404, detail=f"Team {team_name} not found")
    
    del teams[team_name]
    
    return {"message": f"Team {team_name} deleted successfully"}

@app.post("/teams/{team_name}/run")
async def run_team(team_name: str, task_request: TaskRequest, background_tasks: BackgroundTasks):
    if team_name not in teams:
        raise HTTPException(status_code=404, detail=f"Team {team_name} not found")
    
    team = teams[team_name]
    
    # Check if coordinator exists
    if task_request.coordinator_name and task_request.coordinator_name not in virtual_coworkers:
        raise HTTPException(status_code=404, detail=f"Coordinator {task_request.coordinator_name} not found")
    
    # Generate task ID
    task_id = f"task_{len(tasks) + 1}"
    
    # Create task
    tasks[task_id] = {
        "task": task_request.task,
        "status": "pending",
        "result": None
    }
    
    # Run team in background
    def run_task():
        try:
            result = team.run(task_request.task, task_request.coordinator_name)
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["result"] = result
        except Exception as e:
            logger.error(f"Error running team: {e}")
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["result"] = f"Error: {str(e)}"
    
    background_tasks.add_task(run_task)
    
    return {"task_id": task_id, "status": "pending"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return tasks[task_id]

@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks}

# Run the server
if __name__ == "__main__":
    import uvicorn
    
    # Load configuration
    config_path = os.environ.get("CONFIG_PATH", "config/config.yaml")
    config = load_config(config_path)
    
    # Get server configuration
    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8000)
    
    uvicorn.run(app, host=host, port=port)
