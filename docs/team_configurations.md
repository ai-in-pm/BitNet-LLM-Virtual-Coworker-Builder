# Advanced Team Configurations

BitNet Virtual Co-worker Builder allows you to create teams of virtual co-workers that can collaborate to solve complex tasks. This guide will show you how to configure teams for different collaboration modes and scenarios.

## Team Basics

A team is a group of virtual co-workers that can work together to solve tasks. Teams can be configured with different collaboration modes, which determine how the virtual co-workers interact with each other.

## Collaboration Modes

BitNet Virtual Co-worker Builder supports four collaboration modes:

1. **Sequential**: Virtual co-workers work one after another, with each one building on the work of the previous one.
2. **Parallel**: Virtual co-workers work independently on the same task, and their results are combined.
3. **Hierarchical**: One virtual co-worker acts as a coordinator, breaking down the task into subtasks for other virtual co-workers.
4. **Consensus**: Virtual co-workers work independently and then reach a consensus on the final result.

### Sequential Mode

In sequential mode, virtual co-workers work one after another, with each one building on the work of the previous one. This is useful for tasks that require a sequence of steps, such as research, analysis, and report writing.

```python
from bitnet_vc_builder import BitNetTeam, CollaborationMode

team = BitNetTeam(
    agents=[researcher, analyst, writer],
    name="ResearchTeam",
    description="A team that researches, analyzes, and reports on topics",
    collaboration_mode=CollaborationMode.SEQUENTIAL
)

result = team.run("Research climate change, analyze the data, and write a report")
```

### Parallel Mode

In parallel mode, virtual co-workers work independently on the same task, and their results are combined. This is useful for tasks that can be divided into independent subtasks, such as searching multiple sources for information.

```python
from bitnet_vc_builder import BitNetTeam, CollaborationMode

team = BitNetTeam(
    agents=[researcher1, researcher2, researcher3],
    name="ResearchTeam",
    description="A team that researches topics from multiple sources",
    collaboration_mode=CollaborationMode.PARALLEL
)

result = team.run("Research climate change from multiple sources")
```

### Hierarchical Mode

In hierarchical mode, one virtual co-worker acts as a coordinator, breaking down the task into subtasks for other virtual co-workers. This is useful for complex tasks that require coordination and integration of multiple subtasks.

```python
from bitnet_vc_builder import BitNetTeam, CollaborationMode

team = BitNetTeam(
    agents=[coordinator, researcher, analyst, writer],
    name="ProjectTeam",
    description="A team that works on complex projects",
    collaboration_mode=CollaborationMode.HIERARCHICAL
)

result = team.run("Create a comprehensive report on climate change", coordinator_agent_name="coordinator")
```

### Consensus Mode

In consensus mode, virtual co-workers work independently and then reach a consensus on the final result. This is useful for tasks that require multiple perspectives and a balanced conclusion.

```python
from bitnet_vc_builder import BitNetTeam, CollaborationMode

team = BitNetTeam(
    agents=[expert1, expert2, expert3, moderator],
    name="ExpertPanel",
    description="A panel of experts that reaches consensus on topics",
    collaboration_mode=CollaborationMode.CONSENSUS
)

result = team.run("What are the most effective strategies for addressing climate change?")
```

## Team Parameters

The `BitNetTeam` class takes the following parameters:

- `agents`: List of virtual co-workers (required)
- `name`: Team name (default: "BitNetTeam")
- `description`: Team description (default: "A team of AI virtual co-workers")
- `collaboration_mode`: Collaboration mode (default: CollaborationMode.SEQUENTIAL)
- `max_parallel_tasks`: Maximum number of parallel tasks (default: 4)
- `enable_conflict_resolution`: Whether to enable conflict resolution (default: True)
- `enable_task_prioritization`: Whether to enable task prioritization (default: True)
- `enable_performance_tracking`: Whether to enable performance tracking (default: True)

## Team Methods

### run

Runs the team on a task.

```python
result = team.run("Research climate change", coordinator_agent_name="coordinator")
```

Parameters:
- `task`: Task description (required)
- `coordinator_agent_name`: Name of the virtual co-worker to coordinate the task (optional, only used in hierarchical mode)

### add_agent

Adds a virtual co-worker to the team.

```python
team.add_agent(new_agent)
```

### remove_agent

Removes a virtual co-worker from the team.

```python
team.remove_agent("AgentName")
```

### get_agent

Gets a virtual co-worker by name.

```python
agent = team.get_agent("AgentName")
```

### get_performance_metrics

Gets performance metrics for all virtual co-workers.

```python
metrics = team.get_performance_metrics()
```

### get_agent_performance

Gets performance metrics for a specific virtual co-worker.

```python
metrics = team.get_agent_performance("AgentName")
```

## Example Team Configurations

### Research Team

```python
from bitnet_vc_builder import BitNetModel, BitNetVirtualCoworker, BitNetTeam, CollaborationMode, Tool

# Initialize BitNet model
model = BitNetModel(
    model_path="path/to/bitnet_model",
    kernel_type="i2_s"
)

# Create tools
search_tool = Tool(
    name="search",
    description="Search the web for information",
    function=web_search,
    args_schema={
        "query": {
            "type": "string",
            "description": "Search query"
        }
    }
)

analyze_tool = Tool(
    name="analyze",
    description="Analyze data",
    function=analyze_data,
    args_schema={
        "data": {
            "type": "string",
            "description": "Data to analyze"
        }
    }
)

# Create virtual co-workers
researcher = BitNetVirtualCoworker(
    model=model,
    tools=[search_tool],
    name="Researcher",
    description="A virtual co-worker that specializes in research"
)

analyst = BitNetVirtualCoworker(
    model=model,
    tools=[analyze_tool],
    name="Analyst",
    description="A virtual co-worker that specializes in data analysis"
)

writer = BitNetVirtualCoworker(
    model=model,
    tools=[],
    name="Writer",
    description="A virtual co-worker that specializes in writing"
)

# Create team
team = BitNetTeam(
    agents=[researcher, analyst, writer],
    name="ResearchTeam",
    description="A team that researches, analyzes, and reports on topics",
    collaboration_mode=CollaborationMode.SEQUENTIAL
)

# Run team
result = team.run("Research climate change, analyze the data, and write a report")
```

### Development Team

```python
from bitnet_vc_builder import BitNetModel, BitNetVirtualCoworker, BitNetTeam, CollaborationMode, Tool

# Initialize BitNet model
model = BitNetModel(
    model_path="path/to/bitnet_model",
    kernel_type="i2_s"
)

# Create tools
code_tool = Tool(
    name="code",
    description="Generate code",
    function=generate_code,
    args_schema={
        "language": {
            "type": "string",
            "description": "Programming language"
        },
        "requirements": {
            "type": "string",
            "description": "Code requirements"
        }
    }
)

test_tool = Tool(
    name="test",
    description="Test code",
    function=test_code,
    args_schema={
        "code": {
            "type": "string",
            "description": "Code to test"
        },
        "language": {
            "type": "string",
            "description": "Programming language"
        }
    }
)

# Create virtual co-workers
architect = BitNetVirtualCoworker(
    model=model,
    tools=[],
    name="Architect",
    description="A virtual co-worker that specializes in software architecture"
)

developer = BitNetVirtualCoworker(
    model=model,
    tools=[code_tool],
    name="Developer",
    description="A virtual co-worker that specializes in coding"
)

tester = BitNetVirtualCoworker(
    model=model,
    tools=[test_tool],
    name="Tester",
    description="A virtual co-worker that specializes in testing"
)

# Create team
team = BitNetTeam(
    agents=[architect, developer, tester],
    name="DevelopmentTeam",
    description="A team that develops software",
    collaboration_mode=CollaborationMode.HIERARCHICAL
)

# Run team
result = team.run("Create a simple calculator application", coordinator_agent_name="Architect")
```

### Expert Panel

```python
from bitnet_vc_builder import BitNetModel, BitNetVirtualCoworker, BitNetTeam, CollaborationMode

# Initialize BitNet model
model = BitNetModel(
    model_path="path/to/bitnet_model",
    kernel_type="i2_s"
)

# Create virtual co-workers
expert1 = BitNetVirtualCoworker(
    model=model,
    tools=[],
    name="Expert1",
    description="An expert in climate science",
    system_prompt="You are an expert in climate science. Provide insights based on your expertise."
)

expert2 = BitNetVirtualCoworker(
    model=model,
    tools=[],
    name="Expert2",
    description="An expert in economics",
    system_prompt="You are an expert in economics. Provide insights based on your expertise."
)

expert3 = BitNetVirtualCoworker(
    model=model,
    tools=[],
    name="Expert3",
    description="An expert in policy",
    system_prompt="You are an expert in policy. Provide insights based on your expertise."
)

moderator = BitNetVirtualCoworker(
    model=model,
    tools=[],
    name="Moderator",
    description="A moderator that synthesizes expert opinions",
    system_prompt="You are a moderator. Synthesize the opinions of experts into a balanced conclusion."
)

# Create team
team = BitNetTeam(
    agents=[expert1, expert2, expert3, moderator],
    name="ExpertPanel",
    description="A panel of experts that reaches consensus on topics",
    collaboration_mode=CollaborationMode.CONSENSUS
)

# Run team
result = team.run("What are the most effective strategies for addressing climate change?")
```

## Best Practices

When configuring teams, follow these best practices:

1. **Choose the right collaboration mode**: Select the collaboration mode that best fits the task.
2. **Balance team composition**: Include virtual co-workers with complementary skills.
3. **Provide clear instructions**: Make sure the task description is clear and specific.
4. **Monitor performance**: Use performance metrics to identify areas for improvement.
5. **Iterate and refine**: Experiment with different team configurations and refine based on results.
6. **Use the right tools**: Equip virtual co-workers with the tools they need for their specific roles.
7. **Consider task complexity**: For complex tasks, use hierarchical mode with a coordinator.
8. **Enable conflict resolution**: For tasks with multiple perspectives, enable conflict resolution.
9. **Track performance**: Enable performance tracking to identify high-performing virtual co-workers.
10. **Limit team size**: Keep teams small and focused for better coordination.
