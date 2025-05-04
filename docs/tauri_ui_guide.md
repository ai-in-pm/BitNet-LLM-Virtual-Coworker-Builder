# BitNet_LLM_Virtual_Coworker_Builder Desktop Application Guide

This guide provides detailed information on using the BitNet_LLM_Virtual_Coworker_Builder desktop application built with Tauri.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Models](#models)
  - [Creating Models](#creating-models)
  - [Optimizing Models](#optimizing-models)
  - [Managing Models](#managing-models)
- [Virtual Co-workers](#virtual-co-workers)
  - [Creating Virtual Co-workers](#creating-virtual-co-workers)
  - [Running Virtual Co-workers](#running-virtual-co-workers)
  - [Managing Virtual Co-workers](#managing-virtual-co-workers)
- [Tools](#tools)
  - [Built-in Tools](#built-in-tools)
  - [Creating Custom Tools](#creating-custom-tools)
  - [Testing Tools](#testing-tools)
- [Teams](#teams)
  - [Creating Teams](#creating-teams)
  - [Team Workflows](#team-workflows)
  - [Collaboration Modes](#collaboration-modes)
- [Settings](#settings)
  - [Application Settings](#application-settings)
  - [API Server Settings](#api-server-settings)
- [Troubleshooting](#troubleshooting)
- [Advanced Features](#advanced-features)

## Installation

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **CPU**: 2 GHz dual-core processor or better
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB for the application, plus space for models (1-2 GB per model)
- **Internet Connection**: Required for downloading models and using web-based tools

### Installation Steps

1. Download the installer for your platform from the [releases page](https://github.com/bitnet/bitnet-vc-builder/releases).
2. Run the installer and follow the on-screen instructions.
3. Launch the application after installation.

## Getting Started

When you first launch the application, you'll be greeted with a welcome screen that guides you through the initial setup:

1. **API Server Setup**: The application will automatically start the API server in the background. You can monitor its status in the bottom status bar.
2. **Model Setup**: You'll be prompted to download or select a BitNet model. If you don't have any models yet, you can download one from the Models page.
3. **Create Your First Virtual Co-worker**: Once you have a model, you can create your first virtual co-worker from the Virtual Co-workers page.

## Models

The Models page allows you to manage BitNet models for your virtual co-workers.

### Creating Models

To create a new model:

1. Click the "Create Model" button in the top-right corner of the Models page.
2. Fill in the model details:
   - **Name**: A name for the model (e.g., "BitNet-B1-58-Large")
   - **Model Path**: Path to the model files (use the "Browse" button to select a directory)
   - **Kernel Type**: Select the kernel type (i2_s, i2_m, or i2_l)
   - **Number of Threads**: Number of CPU threads to use
   - **Context Size**: Maximum context size
   - **Temperature**: Generation temperature (0.0-1.0)
   - **Top P**: Top-p sampling parameter
   - **Top K**: Top-k sampling parameter
   - **Repetition Penalty**: Repetition penalty
3. Click "Create" to create the model.

### Optimizing Models

To optimize a model for better performance:

1. Click the "Optimize" button next to the model you want to optimize.
2. Configure optimization settings:
   - **Target Device**: Select the target device (CPU, GPU, or NPU)
   - **Number of Threads**: Number of CPU threads to use
   - **Quantization Level**: Level of quantization to apply
   - **Enable Fast Math**: Whether to enable fast math optimizations
   - **Enable Caching**: Whether to enable caching
   - **Batch Size**: Batch size for inference
3. Click "Optimize Model" to start the optimization process.
4. Once optimization is complete, you can benchmark the optimized model by clicking "Benchmark Optimized Model".

### Managing Models

- **View Model Information**: Click the "Info" button next to a model to view detailed information.
- **Delete Model**: Click the "Delete" button next to a model to delete it.
- **Filter Models**: Use the search box to filter models by name.
- **Sort Models**: Click on column headers to sort models by different attributes.

## Virtual Co-workers

The Virtual Co-workers page allows you to create and manage virtual co-workers.

### Creating Virtual Co-workers

To create a new virtual co-worker:

1. Click the "Create Virtual Co-worker" button in the top-right corner of the Virtual Co-workers page.
2. Fill in the virtual co-worker details:
   - **Name**: A name for the virtual co-worker
   - **Model**: Select a model from the dropdown
   - **Description**: A description of the virtual co-worker's capabilities and purpose
   - **System Prompt**: (Optional) A custom system prompt
   - **Tools**: Select tools that the virtual co-worker can use
3. Click "Create" to create the virtual co-worker.

### Running Virtual Co-workers

To run a virtual co-worker on a task:

1. Click the "Run" button on the virtual co-worker's card.
2. Enter the task in the input field.
3. Click "Run" to execute the task.
4. The result will be displayed in the output area.

### Managing Virtual Co-workers

- **Edit Virtual Co-worker**: Click the "Edit" button on the virtual co-worker's card to modify its settings.
- **Delete Virtual Co-worker**: Click the "Delete" button on the virtual co-worker's card to delete it.
- **View History**: Click the "History" button to view the virtual co-worker's task history.
- **Clear Memory**: Click the "Clear Memory" button to clear the virtual co-worker's memory.

## Tools

The Tools page allows you to manage tools that virtual co-workers can use.

### Built-in Tools

The application comes with several built-in tools:

- **Calculator**: Perform mathematical calculations
- **Web Search**: Search the web for information
- **Wikipedia**: Search Wikipedia
- **Weather**: Get weather information
- **Code Generation**: Generate code
- **Data Analysis**: Analyze data
- **Document Processing**: Process documents

### Creating Custom Tools

To create a custom tool:

1. Click the "Create Tool" button in the top-right corner of the Tools page.
2. Fill in the tool details:
   - **Name**: A name for the tool
   - **Description**: A description of what the tool does
   - **Category**: Select a category for the tool
   - **Arguments Schema**: Define the arguments that the tool accepts (in JSON format)
   - **Function**: Write the function that implements the tool's functionality
3. Click "Create" to create the tool.

### Testing Tools

To test a tool:

1. Click the "Test" button on the tool's card.
2. Enter the arguments for the tool in JSON format.
3. Click "Test" to execute the tool with the provided arguments.
4. The result will be displayed in the output area.

## Teams

The Teams page allows you to create and manage teams of virtual co-workers.

### Creating Teams

To create a new team:

1. Click the "Create Team" button in the top-right corner of the Teams page.
2. Fill in the team details:
   - **Name**: A name for the team
   - **Description**: A description of the team's capabilities and purpose
   - **Virtual Co-workers**: Select virtual co-workers to include in the team
   - **Collaboration Mode**: Select a collaboration mode (Sequential, Hierarchical, or Parallel)
   - **Coordinator**: (For Hierarchical mode) Select a coordinator virtual co-worker
   - **Advanced Settings**: Configure conflict resolution, task prioritization, and performance tracking
3. Click "Create" to create the team.

### Team Workflows

To run a team workflow:

1. Click the "Run" button on the team's card.
2. Enter the task in the input field.
3. (For Hierarchical mode) Select a coordinator virtual co-worker.
4. Click "Start Workflow" to execute the task.
5. The workflow progress will be displayed in the workflow view, showing each step and messages between virtual co-workers.
6. You can pause, resume, or restart the workflow using the buttons in the top-right corner.

### Collaboration Modes

The application supports three collaboration modes:

- **Sequential**: Virtual co-workers work one after another, passing results to the next.
- **Hierarchical**: A coordinator virtual co-worker delegates tasks to specialized virtual co-workers.
- **Parallel**: Virtual co-workers work simultaneously on different aspects of a task.

## Settings

The Settings page allows you to configure the application and API server.

### Application Settings

- **Theme**: Choose between light and dark themes
- **Language**: Select the application language
- **Auto-refresh**: Enable or disable automatic refreshing of data
- **Refresh Interval**: Set the refresh interval in seconds
- **Max History Items**: Set the maximum number of history items to display

### API Server Settings

- **Host**: Set the API server host
- **Port**: Set the API server port
- **Debug Mode**: Enable or disable debug mode
- **Number of Workers**: Set the number of worker processes
- **Log Level**: Set the log level
- **Log File**: Set the log file path

## Troubleshooting

### Common Issues

- **API Server Not Starting**: Check that the port is not in use by another application. Try changing the port in the settings.
- **Model Not Loading**: Verify that the model path is correct and that the model files exist.
- **Virtual Co-worker Not Responding**: Check that the API server is running and that the model is loaded correctly.
- **Tool Execution Error**: Check that the tool's function is implemented correctly and that the arguments are valid.

### Logs

The application logs can be found in the following locations:

- **Windows**: `%APPDATA%\bitnet-vc-builder\logs`
- **macOS**: `~/Library/Application Support/bitnet-vc-builder/logs`
- **Linux**: `~/.config/bitnet-vc-builder/logs`

## Advanced Features

### Keyboard Shortcuts

- **Ctrl+N**: Create new (model, virtual co-worker, tool, or team, depending on the current page)
- **Ctrl+R**: Run (virtual co-worker or team, depending on the current page)
- **Ctrl+E**: Edit (selected item)
- **Ctrl+D**: Delete (selected item)
- **Ctrl+F**: Focus search box
- **Ctrl+Tab**: Switch between pages
- **F5**: Refresh data

### Command Line Interface

The application can be launched with command line arguments:

```bash
bitnet-vc-builder --port 8080 --debug
```

Available options:

- `--port`: Set the API server port
- `--debug`: Enable debug mode
- `--log-level`: Set the log level
- `--log-file`: Set the log file path
- `--model-path`: Set the default model path
- `--no-api-server`: Don't start the API server automatically
