# BitNet_LLM_Virtual_Coworker_Builder Python API

This document provides a comprehensive reference for the BitNet_LLM_Virtual_Coworker_Builder Python API.

## Table of Contents

- [Core API](#core-api)
  - [BitNetVirtualCoworker](#bitnetvirtualcoworker)
  - [BitNetTeam](#bitnetteam)
  - [CollaborationMode](#collaborationmode)
- [Models API](#models-api)
  - [BitNetModel](#bitnetmodel)
  - [ModelOptimizer](#modeloptimizer)
- [Tools API](#tools-api)
  - [Tool](#tool)
  - [Built-in Tools](#built-in-tools)
- [Memory API](#memory-api)
  - [Memory](#memory)
  - [ConversationMemory](#conversationmemory)
- [Utilities](#utilities)
  - [Configuration](#configuration)
  - [Logging](#logging)

## Core API

### BitNetVirtualCoworker

The `BitNetVirtualCoworker` class is the foundation of the framework, providing the interface for creating and running virtual co-workers.

#### Constructor

```python
BitNetVirtualCoworker(
    model: BitNetModel,
    tools: List[Tool] = None,
    name: str = None,
    description: str = None,
    memory: Memory = None,
    system_prompt: str = None
)
```

**Parameters:**

- `model`: A `BitNetModel` instance that will be used for generating responses.
- `tools` (optional): A list of `Tool` instances that the virtual co-worker can use.
- `name` (optional): A name for the virtual co-worker. If not provided, a default name will be generated.
- `description` (optional): A description of the virtual co-worker's capabilities and purpose.
- `memory` (optional): A `Memory` instance for storing and retrieving information. If not provided, a default `ConversationMemory` will be created.
- `system_prompt` (optional): A custom system prompt to use instead of the default one.

#### Methods

##### run

```python
run(task: str) -> str
```

Runs the virtual co-worker on a task and returns the result.

**Parameters:**
- `task`: The task to run the virtual co-worker on.

**Returns:**
- The result of the task.

##### run_batch

```python
run_batch(tasks: List[str]) -> List[str]
```

Runs the virtual co-worker on multiple tasks and returns the results.

**Parameters:**
- `tasks`: A list of tasks to run the virtual co-worker on.

**Returns:**
- A list of results, one for each task.

##### add_tool

```python
add_tool(tool: Tool) -> None
```

Adds a tool to the virtual co-worker.

**Parameters:**
- `tool`: The tool to add.

##### remove_tool

```python
remove_tool(tool_name: str) -> bool
```

Removes a tool from the virtual co-worker.

**Parameters:**
- `tool_name`: The name of the tool to remove.

**Returns:**
- `True` if the tool was removed, `False` if the tool was not found.

##### get_tool

```python
get_tool(tool_name: str) -> Optional[Tool]
```

Gets a tool by name.

**Parameters:**
- `tool_name`: The name of the tool to get.

**Returns:**
- The tool if found, `None` otherwise.

##### get_tools

```python
get_tools() -> List[Tool]
```

Gets all tools available to the virtual co-worker.

**Returns:**
- A list of all tools.

##### clear_memory

```python
clear_memory() -> None
```

Clears the virtual co-worker's memory.

##### get_memory

```python
get_memory() -> str
```

Gets the virtual co-worker's memory as a string.

**Returns:**
- The memory as a string.

##### add_to_memory

```python
add_to_memory(content: str) -> None
```

Adds content to the virtual co-worker's memory.

**Parameters:**
- `content`: The content to add to memory.

#### Example

```python
from bitnet_vc_builder import BitNetVirtualCoworker, BitNetModel, Tool

# Initialize BitNet model
model = BitNetModel(model_path="models/bitnet-b1.58-2b")

# Create a virtual co-worker
coworker = BitNetVirtualCoworker(
    model=model,
    name="AssistantCoworker",
    description="A helpful virtual co-worker"
)

# Run the virtual co-worker on a task
result = coworker.run("What is the capital of France?")
print(result)
```

### BitNetTeam

The `BitNetTeam` class enables collaboration between multiple virtual co-workers.

#### Constructor

```python
BitNetTeam(
    agents: List[BitNetVirtualCoworker],
    name: str = None,
    description: str = None,
    collaboration_mode: CollaborationMode = CollaborationMode.SEQUENTIAL,
    coordinator_agent: str = None,
    memory: Memory = None,
    enable_conflict_resolution: bool = False,
    conflict_resolution_strategy: str = "voting",
    enable_task_prioritization: bool = False,
    enable_performance_tracking: bool = False,
    max_parallel_tasks: int = None
)
```

**Parameters:**

- `agents`: A list of `BitNetVirtualCoworker` instances that will be part of the team.
- `name` (optional): A name for the team. If not provided, a default name will be generated.
- `description` (optional): A description of the team's capabilities and purpose.
- `collaboration_mode` (optional): The mode of collaboration between virtual co-workers. Default is `CollaborationMode.SEQUENTIAL`.
- `coordinator_agent` (optional): The name of the virtual co-worker that will coordinate the team in hierarchical mode.
- `memory` (optional): A `Memory` instance for storing and retrieving information. If not provided, a default `ConversationMemory` will be created.
- `enable_conflict_resolution` (optional): Whether to enable conflict resolution between virtual co-workers. Default is `False`.
- `conflict_resolution_strategy` (optional): The strategy to use for resolving conflicts. Options are "voting", "consensus", and "authority". Default is "voting".
- `enable_task_prioritization` (optional): Whether to enable task prioritization. Default is `False`.
- `enable_performance_tracking` (optional): Whether to enable performance tracking for virtual co-workers. Default is `False`.
- `max_parallel_tasks` (optional): The maximum number of tasks that can be executed in parallel in parallel mode.

#### Methods

##### run

```python
run(task: str) -> str
```

Runs the team on a task and returns the result.

**Parameters:**
- `task`: The task to run the team on.

**Returns:**
- The result of the task.

##### add_agent

```python
add_agent(agent: BitNetVirtualCoworker) -> None
```

Adds a virtual co-worker to the team.

**Parameters:**
- `agent`: The virtual co-worker to add.

##### remove_agent

```python
remove_agent(agent_name: str) -> bool
```

Removes a virtual co-worker from the team.

**Parameters:**
- `agent_name`: The name of the virtual co-worker to remove.

**Returns:**
- `True` if the virtual co-worker was removed, `False` if the virtual co-worker was not found.

##### get_agent

```python
get_agent(agent_name: str) -> Optional[BitNetVirtualCoworker]
```

Gets a virtual co-worker by name.

**Parameters:**
- `agent_name`: The name of the virtual co-worker to get.

**Returns:**
- The virtual co-worker if found, `None` otherwise.

##### get_agents

```python
get_agents() -> List[BitNetVirtualCoworker]
```

Gets all virtual co-workers in the team.

**Returns:**
- A list of all virtual co-workers.

##### set_collaboration_mode

```python
set_collaboration_mode(mode: CollaborationMode) -> None
```

Sets the collaboration mode for the team.

**Parameters:**
- `mode`: The collaboration mode to set.

##### set_coordinator_agent

```python
set_coordinator_agent(agent_name: str) -> None
```

Sets the coordinator virtual co-worker for hierarchical mode.

**Parameters:**
- `agent_name`: The name of the virtual co-worker to set as coordinator.

**Raises:**
- `ValueError`: If the virtual co-worker is not found in the team.

##### clear_memory

```python
clear_memory() -> None
```

Clears the team's memory.

##### get_memory

```python
get_memory() -> str
```

Gets the team's memory as a string.

**Returns:**
- The memory as a string.

##### add_to_memory

```python
add_to_memory(content: str) -> None
```

Adds content to the team's memory.

**Parameters:**
- `content`: The content to add to memory.

#### Example

```python
from bitnet_vc_builder import BitNetVirtualCoworker, BitNetModel, BitNetTeam, CollaborationMode

# Initialize BitNet model
model = BitNetModel(model_path="models/bitnet-b1.58-2b")

# Create virtual co-workers
researcher = BitNetVirtualCoworker(
    model=model,
    name="Researcher",
    description="A virtual co-worker that specializes in research"
)

analyst = BitNetVirtualCoworker(
    model=model,
    name="Analyst",
    description="A virtual co-worker that specializes in data analysis"
)

writer = BitNetVirtualCoworker(
    model=model,
    name="Writer",
    description="A virtual co-worker that specializes in writing"
)

# Create a team
team = BitNetTeam(
    agents=[researcher, analyst, writer],
    name="ResearchTeam",
    description="A team that researches topics, analyzes data, and writes reports",
    collaboration_mode=CollaborationMode.HIERARCHICAL,
    coordinator_agent="Researcher"
)

# Run the team on a task
result = team.run("Research climate change and write a report")
print(result)
```

### CollaborationMode

The `CollaborationMode` enum defines the different modes of collaboration between virtual co-workers in a team.

```python
class CollaborationMode(Enum):
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    PARALLEL = "parallel"
```

- `SEQUENTIAL`: Virtual co-workers work one after another, passing results to the next.
- `HIERARCHICAL`: A coordinator virtual co-worker delegates tasks to specialized virtual co-workers.
- `PARALLEL`: Virtual co-workers work simultaneously on different aspects of a task.

## Models API

### BitNetModel

The `BitNetModel` class provides a unified interface to BitNet's 1-bit quantized language models.

#### Constructor

```python
BitNetModel(
    model_path: str,
    kernel_type: str = "i2_s",
    num_threads: int = 4,
    context_size: int = 2048,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 40,
    repetition_penalty: float = 1.1,
    bitnet_path: str = None
)
```

**Parameters:**

- `model_path`: Path to the BitNet model.
- `kernel_type` (optional): Type of kernel to use. Options are "i2_s" (small), "i2_m" (medium), and "i2_l" (large). Default is "i2_s".
- `num_threads` (optional): Number of CPU threads to use. Default is 4.
- `context_size` (optional): Maximum context size. Default is 2048.
- `temperature` (optional): Generation temperature (0.0-1.0). Default is 0.7.
- `top_p` (optional): Top-p sampling parameter. Default is 0.9.
- `top_k` (optional): Top-k sampling parameter. Default is 40.
- `repetition_penalty` (optional): Repetition penalty. Default is 1.1.
- `bitnet_path` (optional): Path to BitNet installation. If not provided, the default installation will be used.

#### Methods

##### generate

```python
generate(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = None,
    top_p: float = None,
    top_k: int = None,
    repetition_penalty: float = None,
    stop_sequences: List[str] = None
) -> str
```

Generates text based on the prompt.

**Parameters:**
- `prompt`: The prompt to generate text from.
- `max_tokens` (optional): Maximum number of tokens to generate. Default is 512.
- `temperature` (optional): Generation temperature (0.0-1.0). If not provided, the model's default temperature will be used.
- `top_p` (optional): Top-p sampling parameter. If not provided, the model's default top_p will be used.
- `top_k` (optional): Top-k sampling parameter. If not provided, the model's default top_k will be used.
- `repetition_penalty` (optional): Repetition penalty. If not provided, the model's default repetition_penalty will be used.
- `stop_sequences` (optional): List of sequences that will stop generation when encountered.

**Returns:**
- The generated text.

##### tokenize

```python
tokenize(text: str) -> List[int]
```

Tokenizes text into token IDs.

**Parameters:**
- `text`: The text to tokenize.

**Returns:**
- A list of token IDs.

##### detokenize

```python
detokenize(tokens: List[int]) -> str
```

Converts token IDs back to text.

**Parameters:**
- `tokens`: The token IDs to convert.

**Returns:**
- The detokenized text.

##### get_token_count

```python
get_token_count(text: str) -> int
```

Gets the number of tokens in the text.

**Parameters:**
- `text`: The text to count tokens in.

**Returns:**
- The number of tokens.

##### set_parameters

```python
set_parameters(
    temperature: float = None,
    top_p: float = None,
    top_k: int = None,
    repetition_penalty: float = None
) -> None
```

Sets generation parameters.

**Parameters:**
- `temperature` (optional): Generation temperature (0.0-1.0).
- `top_p` (optional): Top-p sampling parameter.
- `top_k` (optional): Top-k sampling parameter.
- `repetition_penalty` (optional): Repetition penalty.

#### Example

```python
from bitnet_vc_builder import BitNetModel

# Initialize BitNet model
model = BitNetModel(
    model_path="models/bitnet-b1.58-2b",
    kernel_type="i2_s",
    num_threads=4,
    context_size=2048,
    temperature=0.7
)

# Generate text
response = model.generate(
    prompt="What is the capital of France?",
    max_tokens=100,
    temperature=0.8
)
print(response)
```

### ModelOptimizer

The `ModelOptimizer` class provides utilities for optimizing BitNet models for better performance.

#### Constructor

```python
ModelOptimizer(
    model_path: str,
    output_path: str = None,
    target_device: str = "cpu",
    num_threads: int = 4,
    quantization_level: int = 0,
    enable_fast_math: bool = True,
    enable_caching: bool = True,
    batch_size: int = 1
)
```

**Parameters:**

- `model_path`: Path to the BitNet model to optimize.
- `output_path` (optional): Path to save the optimized model. If not provided, a default path will be generated.
- `target_device` (optional): Target device for optimization. Options are "cpu", "gpu", and "npu". Default is "cpu".
- `num_threads` (optional): Number of CPU threads to use. Default is 4.
- `quantization_level` (optional): Level of quantization to apply. 0 = none, 1 = light, 2 = medium, 3 = heavy, 4 = extreme. Default is 0.
- `enable_fast_math` (optional): Whether to enable fast math optimizations. Default is `True`.
- `enable_caching` (optional): Whether to enable caching. Default is `True`.
- `batch_size` (optional): Batch size for inference. Default is 1.

#### Methods

##### optimize

```python
optimize() -> Dict[str, Any]
```

Optimizes the model and returns optimization results.

**Returns:**
- A dictionary containing optimization results, including:
  - `original_size`: Original model size in MB.
  - `optimized_size`: Optimized model size in MB.
  - `speedup`: Speedup factor compared to the original model.
  - `memory_reduction`: Memory reduction percentage.
  - `optimized_model_path`: Path to the optimized model.
  - `optimization_time`: Time taken for optimization in seconds.
  - `settings`: Optimization settings used.

##### benchmark

```python
benchmark(
    prompt: str = "Hello, world!",
    max_tokens: int = 100,
    num_runs: int = 10
) -> Dict[str, Any]
```

Benchmarks the optimized model and returns performance metrics.

**Parameters:**
- `prompt` (optional): Prompt to use for benchmarking. Default is "Hello, world!".
- `max_tokens` (optional): Maximum number of tokens to generate. Default is 100.
- `num_runs` (optional): Number of runs to average over. Default is 10.

**Returns:**
- A dictionary containing benchmark results, including:
  - `tokens_per_second`: Tokens generated per second.
  - `latency`: Average latency in milliseconds.
  - `memory_usage`: Memory usage in MB.
  - `comparison_to_original`: Comparison to the original model.

#### Example

```python
from bitnet_vc_builder.models.optimizers import ModelOptimizer

# Create a model optimizer
optimizer = ModelOptimizer(
    model_path="models/bitnet-b1.58-2b",
    target_device="cpu",
    num_threads=4,
    quantization_level=2,
    enable_fast_math=True,
    enable_caching=True
)

# Optimize the model
result = optimizer.optimize()
print(f"Optimized model saved to: {result['optimized_model_path']}")
print(f"Size reduction: {result['memory_reduction']}%")
print(f"Speed improvement: {result['speedup']}x")

# Benchmark the optimized model
benchmark = optimizer.benchmark()
print(f"Tokens per second: {benchmark['tokens_per_second']}")
print(f"Latency: {benchmark['latency']} ms")
print(f"Memory usage: {benchmark['memory_usage']} MB")
```

## Tools API

### Tool

The `Tool` class is the base class for all tools that can be used by virtual co-workers.

#### Constructor

```python
Tool(
    name: str,
    description: str,
    function: Callable,
    args_schema: Dict[str, Dict[str, Any]] = None,
    return_direct: bool = False,
    category: str = None
)
```

**Parameters:**

- `name`: The name of the tool.
- `description`: A description of what the tool does.
- `function`: The function that implements the tool's functionality.
- `args_schema` (optional): A schema describing the arguments that the tool accepts.
- `return_direct` (optional): Whether to return the tool's output directly without further processing. Default is `False`.
- `category` (optional): The category of the tool. Default is `None`.

#### Methods

##### execute

```python
execute(**kwargs) -> Any
```

Executes the tool with the given arguments.

**Parameters:**
- `**kwargs`: Arguments to pass to the tool's function.

**Returns:**
- The result of the tool's function.

##### validate_args

```python
validate_args(args: Dict[str, Any]) -> Dict[str, Any]
```

Validates the arguments against the schema.

**Parameters:**
- `args`: The arguments to validate.

**Returns:**
- The validated arguments.

**Raises:**
- `ValueError`: If the arguments are invalid.

##### to_dict

```python
to_dict() -> Dict[str, Any]
```

Converts the tool to a dictionary representation.

**Returns:**
- A dictionary representation of the tool.

#### Example

```python
from bitnet_vc_builder import Tool

def calculator(expression):
    """Simple calculator tool"""
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {str(e)}"

calculator_tool = Tool(
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

# Execute the tool
result = calculator_tool.execute(expression="2 + 2")
print(result)  # Output: 4
```

### Built-in Tools

The framework includes several built-in tools that can be used by virtual co-workers:

#### WebSearchTool

A tool for searching the web.

```python
from bitnet_vc_builder.tools.common_tools import WebSearchTool

web_search = WebSearchTool()
```

#### CalculatorTool

A tool for performing mathematical calculations.

```python
from bitnet_vc_builder.tools.common_tools import CalculatorTool

calculator = CalculatorTool()
```

#### WikipediaTool

A tool for searching Wikipedia.

```python
from bitnet_vc_builder.tools.common_tools import WikipediaTool

wikipedia = WikipediaTool()
```

#### WeatherTool

A tool for getting weather information.

```python
from bitnet_vc_builder.tools.common_tools import WeatherTool

weather = WeatherTool(api_key="your_api_key")
```

#### CodeGenerationTool

A tool for generating code.

```python
from bitnet_vc_builder.tools.code_tools import CodeGenerationTool

code_generator = CodeGenerationTool()
```

#### DataAnalysisTool

A tool for analyzing data.

```python
from bitnet_vc_builder.tools.data_tools import DataAnalysisTool

data_analyzer = DataAnalysisTool()
```

#### DocumentProcessingTool

A tool for processing documents.

```python
from bitnet_vc_builder.tools.document_tools import DocumentProcessingTool

document_processor = DocumentProcessingTool()
```

## Memory API

### Memory

The `Memory` class is the base class for all memory systems.

#### Constructor

```python
Memory(max_items: int = 100)
```

**Parameters:**

- `max_items` (optional): Maximum number of items to store in memory. Default is 100.

#### Methods

##### add

```python
add(content: str) -> None
```

Adds content to memory.

**Parameters:**
- `content`: The content to add to memory.

##### get

```python
get() -> List[str]
```

Gets all items in memory.

**Returns:**
- A list of all items in memory.

##### get_context

```python
get_context() -> str
```

Gets the memory context as a string.

**Returns:**
- The memory context as a string.

##### clear

```python
clear() -> None
```

Clears all items from memory.

#### Example

```python
from bitnet_vc_builder.memory.memory import Memory

# Create a memory system
memory = Memory(max_items=50)

# Add items to memory
memory.add("This is an important fact.")
memory.add("Remember this for later.")

# Get all items
items = memory.get()
print(items)

# Get memory context
context = memory.get_context()
print(context)

# Clear memory
memory.clear()
```

### ConversationMemory

The `ConversationMemory` class is a memory system that stores conversation history.

#### Constructor

```python
ConversationMemory(max_items: int = 100)
```

**Parameters:**

- `max_items` (optional): Maximum number of conversation turns to store. Default is 100.

#### Methods

##### add_user_message

```python
add_user_message(message: str) -> None
```

Adds a user message to the conversation history.

**Parameters:**
- `message`: The user message to add.

##### add_assistant_message

```python
add_assistant_message(message: str) -> None
```

Adds an assistant message to the conversation history.

**Parameters:**
- `message`: The assistant message to add.

##### get_conversation

```python
get_conversation() -> List[Dict[str, str]]
```

Gets the conversation history.

**Returns:**
- A list of dictionaries, each containing a "role" and "content" key.

##### get_context

```python
get_context() -> str
```

Gets the conversation history as a string.

**Returns:**
- The conversation history as a string.

##### clear

```python
clear() -> None
```

Clears the conversation history.

#### Example

```python
from bitnet_vc_builder.memory.memory import ConversationMemory

# Create a conversation memory
memory = ConversationMemory(max_items=50)

# Add messages to the conversation
memory.add_user_message("Hello, how are you?")
memory.add_assistant_message("I'm doing well, thank you! How can I help you today?")
memory.add_user_message("I need information about climate change.")

# Get the conversation history
conversation = memory.get_conversation()
print(conversation)

# Get the conversation context
context = memory.get_context()
print(context)

# Clear the conversation
memory.clear()
```

## Utilities

### Configuration

The framework includes utilities for loading and saving configuration.

#### load_config

```python
load_config(config_path: str) -> Dict[str, Any]
```

Loads configuration from a YAML file.

**Parameters:**
- `config_path`: Path to the configuration file.

**Returns:**
- The configuration as a dictionary.

#### save_config

```python
save_config(config: Dict[str, Any], config_path: str) -> None
```

Saves configuration to a YAML file.

**Parameters:**
- `config`: The configuration to save.
- `config_path`: Path to save the configuration to.

#### Example

```python
from bitnet_vc_builder.utils.config import load_config, save_config

# Load configuration
config = load_config("config/config.yaml")

# Modify configuration
config["models"]["default_model"] = "bitnet-b1.58-2b"

# Save configuration
save_config(config, "config/config.yaml")
```

### Logging

The framework includes utilities for logging.

#### setup_logging

```python
setup_logging(
    log_level: str = "INFO",
    log_file: str = None,
    log_format: str = None
) -> None
```

Sets up logging.

**Parameters:**
- `log_level` (optional): The log level. Default is "INFO".
- `log_file` (optional): Path to the log file. If not provided, logs will be written to stdout.
- `log_format` (optional): The log format. If not provided, a default format will be used.

#### Example

```python
from bitnet_vc_builder.utils.logging import setup_logging, get_logger

# Set up logging
setup_logging(log_level="DEBUG", log_file="logs/app.log")

# Get a logger
logger = get_logger(__name__)

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```
