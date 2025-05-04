# BitNet Virtual Co-worker Builder API

This document describes the API for BitNet Virtual Co-worker Builder.

## API Server

BitNet Virtual Co-worker Builder includes a RESTful API server that you can use to create and manage virtual co-workers and teams.

### Running the API Server

```bash
# Run the API server
python -m bitnet_vc_builder.api.server
```

The API documentation is available at `http://localhost:8000/docs`.

## API Endpoints

### Root

#### GET /

Returns a welcome message.

**Response:**

```json
{
  "message": "Welcome to BitNet Virtual Co-worker Builder API"
}
```

### Models

#### GET /models

Returns a list of all models.

**Response:**

```json
{
  "models": [
    "BitNet-B1-58-Large",
    "BitNet-B1-32-Medium",
    "BitNet-B1-16-Small"
  ]
}
```

#### POST /models

Creates a new model.

**Request:**

```json
{
  "name": "BitNet-B1-58-Large",
  "model_path": "models/bitnet_b1_58_large",
  "kernel_type": "i2_s",
  "num_threads": 4,
  "context_size": 2048,
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "repetition_penalty": 1.1
}
```

**Response:**

```json
{
  "message": "Model BitNet-B1-58-Large created successfully"
}
```

#### GET /models/{model_name}

Returns information about a model.

**Response:**

```json
{
  "model_info": {
    "model_path": "models/bitnet_b1_58_large",
    "kernel_type": "i2_s",
    "num_threads": 4,
    "context_size": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repetition_penalty": 1.1,
    "is_mock": false
  }
}
```

#### DELETE /models/{model_name}

Deletes a model.

**Response:**

```json
{
  "message": "Model BitNet-B1-58-Large deleted successfully"
}
```

### Virtual Co-workers

#### GET /virtual-coworkers

Returns a list of all virtual co-workers.

**Response:**

```json
{
  "virtual_coworkers": [
    "MathCoworker",
    "ResearchCoworker",
    "WriterCoworker"
  ]
}
```

#### POST /virtual-coworkers

Creates a new virtual co-worker.

**Request:**

```json
{
  "name": "MathCoworker",
  "model_name": "BitNet-B1-58-Large",
  "description": "A virtual co-worker that specializes in mathematics",
  "system_prompt": "You are a mathematics expert. Help users with math problems.",
  "tool_names": ["calculator"]
}
```

**Response:**

```json
{
  "message": "Virtual co-worker MathCoworker created successfully"
}
```

#### GET /virtual-coworkers/{virtual_coworker_name}

Returns information about a virtual co-worker.

**Response:**

```json
{
  "name": "MathCoworker",
  "description": "A virtual co-worker that specializes in mathematics",
  "model": {
    "model_path": "models/bitnet_b1_58_large",
    "kernel_type": "i2_s",
    "num_threads": 4,
    "context_size": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repetition_penalty": 1.1,
    "is_mock": false
  },
  "tools": ["calculator"]
}
```

#### DELETE /virtual-coworkers/{virtual_coworker_name}

Deletes a virtual co-worker.

**Response:**

```json
{
  "message": "Virtual co-worker MathCoworker deleted successfully"
}
```

#### POST /virtual-coworkers/{virtual_coworker_name}/run

Runs a virtual co-worker on a task.

**Request:**

```json
{
  "task": "Calculate 2 + 2 * 3"
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "result": null
}
```

### Teams

#### GET /teams

Returns a list of all teams.

**Response:**

```json
{
  "teams": [
    "ResearchTeam",
    "DevelopmentTeam"
  ]
}
```

#### POST /teams

Creates a new team.

**Request:**

```json
{
  "name": "ResearchTeam",
  "description": "A team that researches, analyzes, and reports on topics",
  "virtual_coworker_names": ["ResearchCoworker", "AnalystCoworker", "WriterCoworker"],
  "collaboration_mode": "SEQUENTIAL",
  "max_parallel_tasks": 4,
  "enable_conflict_resolution": true,
  "enable_task_prioritization": true,
  "enable_performance_tracking": true
}
```

**Response:**

```json
{
  "message": "Team ResearchTeam created successfully"
}
```

#### GET /teams/{team_name}

Returns information about a team.

**Response:**

```json
{
  "name": "ResearchTeam",
  "description": "A team that researches, analyzes, and reports on topics",
  "virtual_coworkers": ["ResearchCoworker", "AnalystCoworker", "WriterCoworker"],
  "collaboration_mode": "SEQUENTIAL",
  "max_parallel_tasks": 4,
  "enable_conflict_resolution": true,
  "enable_task_prioritization": true,
  "enable_performance_tracking": true
}
```

#### DELETE /teams/{team_name}

Deletes a team.

**Response:**

```json
{
  "message": "Team ResearchTeam deleted successfully"
}
```

#### POST /teams/{team_name}/run

Runs a team on a task.

**Request:**

```json
{
  "task": "Research climate change, analyze the data, and write a report",
  "coordinator_agent_name": "ResearchCoworker"
}
```

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "result": null
}
```

### Tasks

#### GET /tasks

Returns a list of all tasks.

**Response:**

```json
{
  "tasks": {
    "123e4567-e89b-12d3-a456-426614174000": {
      "task": "Calculate 2 + 2 * 3",
      "status": "completed",
      "result": "The result is 8.",
      "created_at": 1626100000.0
    },
    "456e7890-e12d-34a5-b678-426614174000": {
      "task": "Research climate change, analyze the data, and write a report",
      "status": "in_progress",
      "result": null,
      "created_at": 1626100100.0
    }
  }
}
```

#### GET /tasks/{task_id}

Returns information about a task.

**Response:**

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "result": "The result is 8."
}
```

### Tools

#### GET /tools

Returns a list of all available tools.

**Response:**

```json
{
  "tools": [
    {
      "name": "calculator",
      "description": "Calculate a mathematical expression",
      "args_schema": {
        "expression": {
          "type": "string",
          "description": "Mathematical expression to calculate"
        }
      }
    },
    {
      "name": "search",
      "description": "Search the web for information",
      "args_schema": {
        "query": {
          "type": "string",
          "description": "Search query"
        }
      }
    }
  ]
}
```

#### GET /tools/{tool_name}

Returns information about a tool.

**Response:**

```json
{
  "name": "calculator",
  "description": "Calculate a mathematical expression",
  "args_schema": {
    "expression": {
      "type": "string",
      "description": "Mathematical expression to calculate"
    }
  }
}
```

### Config

#### GET /config

Returns the current configuration.

**Response:**

```json
{
  "config": {
    "server": {
      "host": "0.0.0.0",
      "port": 8000,
      "debug": false,
      "workers": 4
    },
    "model": {
      "path": null,
      "models_dir": "models",
      "kernel_type": "i2_s",
      "num_threads": 4,
      "context_size": 2048,
      "temperature": 0.7,
      "top_p": 0.9,
      "top_k": 40,
      "repetition_penalty": 1.1
    },
    "memory": {
      "max_items": 100,
      "max_context_length": 2000,
      "recency_bias": 0.7
    },
    "team": {
      "default_collaboration_mode": "SEQUENTIAL",
      "max_parallel_tasks": 4,
      "enable_conflict_resolution": true,
      "enable_task_prioritization": true,
      "enable_performance_tracking": true
    },
    "logging": {
      "level": "INFO",
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
      "file": "logs/bitnet_vc_builder.log",
      "max_size": 10485760,
      "backup_count": 5
    },
    "ui": {
      "theme": "light",
      "max_history_items": 50,
      "auto_refresh": true,
      "refresh_interval": 5
    }
  }
}
```

#### POST /config

Updates the configuration.

**Request:**

```json
{
  "server": {
    "port": 8080
  },
  "model": {
    "kernel_type": "i2_m"
  }
}
```

**Response:**

```json
{
  "message": "Configuration updated successfully"
}
```

### Health Check

#### GET /health

Returns the health status of the API server.

**Response:**

```json
{
  "status": "ok"
}
```
