# Creating Custom Tools

BitNet Virtual Co-worker Builder allows you to create custom tools that virtual co-workers can use to interact with external systems and APIs. This guide will show you how to create custom tools.

## Tool Basics

A tool is a function that a virtual co-worker can call to perform a specific task. Tools can be used to:

- Search the web
- Retrieve information from databases
- Perform calculations
- Generate images
- Call external APIs
- And much more

## Creating a Tool

To create a tool, you need to:

1. Define a function that performs the task
2. Create a `Tool` instance with the function and metadata

Here's a simple example of a calculator tool:

```python
from bitnet_vc_builder import Tool

def calculator(expression):
    """
    Simple calculator tool.
    """
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
            "description": "Mathematical expression to calculate",
            "required": True
        }
    }
)
```

## Tool Parameters

The `Tool` class takes the following parameters:

- `name`: The name of the tool (required)
- `description`: A description of what the tool does (required)
- `function`: The function to call when the tool is used (required)
- `args_schema`: A schema for the tool's arguments (optional)

## Arguments Schema

The `args_schema` parameter is a dictionary that defines the arguments that the tool accepts. Each argument has the following properties:

- `type`: The type of the argument (string, number, boolean, array, object)
- `description`: A description of the argument
- `required`: Whether the argument is required (default: False)

Here's an example of a more complex arguments schema:

```python
args_schema = {
    "query": {
        "type": "string",
        "description": "Search query",
        "required": True
    },
    "num_results": {
        "type": "number",
        "description": "Number of results to return",
        "required": False
    },
    "include_images": {
        "type": "boolean",
        "description": "Whether to include images in the results",
        "required": False
    }
}
```

## Using Tools with Virtual Co-workers

Once you've created a tool, you can add it to a virtual co-worker:

```python
from bitnet_vc_builder import BitNetModel, BitNetVirtualCoworker

# Initialize BitNet model
model = BitNetModel(
    model_path="path/to/bitnet_model",
    kernel_type="i2_s"
)

# Create virtual co-worker with tools
coworker = BitNetVirtualCoworker(
    model=model,
    tools=[calculator_tool],
    name="MathCoworker",
    description="A virtual co-worker that specializes in mathematics"
)

# Run virtual co-worker
result = coworker.run("Calculate 2 + 2 * 3")
print(result)
```

## Example Tools

### Web Search Tool

```python
import requests

def web_search(query, num_results=5):
    """
    Search the web for information.
    """
    # In a real implementation, you would use a search API
    # For this example, we'll use a mock implementation
    
    return f"Search results for '{query}':\n\n" + "\n".join([
        f"Result {i+1}: This is a mock search result for '{query}'"
        for i in range(num_results)
    ])

search_tool = Tool(
    name="web_search",
    description="Search the web for information",
    function=web_search,
    args_schema={
        "query": {
            "type": "string",
            "description": "Search query",
            "required": True
        },
        "num_results": {
            "type": "number",
            "description": "Number of results to return",
            "required": False
        }
    }
)
```

### Weather Tool

```python
import requests

def get_weather(location):
    """
    Get weather information for a location.
    """
    # In a real implementation, you would use a weather API
    # For this example, we'll use a mock implementation
    
    return {
        "location": location,
        "temperature": 72,
        "condition": "Sunny",
        "humidity": 65,
        "wind_speed": 5,
        "forecast": [
            {"day": "Today", "high": 75, "low": 65, "condition": "Sunny"},
            {"day": "Tomorrow", "high": 78, "low": 67, "condition": "Partly Cloudy"},
            {"day": "Wednesday", "high": 80, "low": 68, "condition": "Cloudy"}
        ]
    }

weather_tool = Tool(
    name="get_weather",
    description="Get weather information for a location",
    function=get_weather,
    args_schema={
        "location": {
            "type": "string",
            "description": "Location to get weather for",
            "required": True
        }
    }
)
```

### Database Tool

```python
import sqlite3

def query_database(query, database_path):
    """
    Query a SQLite database.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        return results
    except Exception as e:
        return f"Error querying database: {str(e)}"

database_tool = Tool(
    name="query_database",
    description="Query a SQLite database",
    function=query_database,
    args_schema={
        "query": {
            "type": "string",
            "description": "SQL query to execute",
            "required": True
        },
        "database_path": {
            "type": "string",
            "description": "Path to the SQLite database",
            "required": True
        }
    }
)
```

## Best Practices

When creating custom tools, follow these best practices:

1. **Keep tools focused**: Each tool should do one thing well.
2. **Provide clear descriptions**: Make sure the tool's description and argument descriptions are clear and concise.
3. **Handle errors gracefully**: Tools should handle errors and return meaningful error messages.
4. **Validate inputs**: Validate inputs before using them to prevent security issues.
5. **Limit side effects**: Be careful with tools that have side effects (e.g., writing to a database).
6. **Document tools**: Document your tools so that others can understand how to use them.
7. **Test tools**: Test your tools to make sure they work as expected.

## Advanced Tool Features

### Tool Validation

You can add custom validation to your tools by overriding the `_validate_args` method:

```python
from bitnet_vc_builder.tools.base_tools import Tool

class CustomTool(Tool):
    def _validate_args(self, args):
        super()._validate_args(args)
        
        # Add custom validation
        if "query" in args and len(args["query"]) < 3:
            raise ValueError("Query must be at least 3 characters long")
```

### Tool Caching

You can add caching to your tools to improve performance:

```python
import functools

@functools.lru_cache(maxsize=100)
def cached_web_search(query):
    # Perform web search
    return f"Search results for '{query}'"

search_tool = Tool(
    name="web_search",
    description="Search the web for information",
    function=cached_web_search,
    args_schema={
        "query": {
            "type": "string",
            "description": "Search query",
            "required": True
        }
    }
)
```

### Tool Composition

You can compose tools to create more complex tools:

```python
def research_and_summarize(query):
    # Use web_search tool
    search_results = web_search(query)
    
    # Use summarize tool
    summary = summarize(search_results)
    
    return summary

research_tool = Tool(
    name="research_and_summarize",
    description="Research a topic and summarize the results",
    function=research_and_summarize,
    args_schema={
        "query": {
            "type": "string",
            "description": "Research query",
            "required": True
        }
    }
)
```
