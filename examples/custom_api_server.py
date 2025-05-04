"""
Example of running the BitNet Virtual Co-worker Builder API server with a custom configuration.
"""

import os
import sys
import logging
import argparse
import uvicorn
import yaml

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.api.server import app
from bitnet_vc_builder.config.config_loader import load_config, save_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_custom_config():
    """
    Create a custom configuration.
    
    Returns:
        Custom configuration
    """
    return {
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "debug": True,
            "workers": 2
        },
        "model": {
            "path": None,
            "models_dir": "custom_models",
            "kernel_type": "i2_m",
            "num_threads": 8,
            "context_size": 4096,
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 50,
            "repetition_penalty": 1.05
        },
        "memory": {
            "max_items": 200,
            "max_context_length": 4000,
            "recency_bias": 0.8
        },
        "team": {
            "default_collaboration_mode": "HIERARCHICAL",
            "max_parallel_tasks": 8,
            "enable_conflict_resolution": True,
            "enable_task_prioritization": True,
            "enable_performance_tracking": True
        },
        "logging": {
            "level": "DEBUG",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/custom_api_server.log",
            "max_size": 20971520,
            "backup_count": 10
        },
        "ui": {
            "theme": "dark",
            "max_history_items": 100,
            "auto_refresh": True,
            "refresh_interval": 3
        }
    }

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Custom BitNet Virtual Co-worker Builder API Server")
    
    parser.add_argument(
        "--host",
        type=str,
        help="Host to bind to"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        help="Port to bind to"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="custom_config.yaml",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Create a custom configuration file"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    # Create custom configuration if requested
    if args.create_config:
        logger.info(f"Creating custom configuration file: {args.config}")
        custom_config = create_custom_config()
        
        # Save configuration
        if save_config(custom_config, args.config):
            logger.info(f"Custom configuration saved to {args.config}")
            print(f"Custom configuration saved to {args.config}")
        else:
            logger.error(f"Failed to save custom configuration to {args.config}")
            print(f"Failed to save custom configuration to {args.config}")
        
        return
    
    # Load configuration
    logger.info(f"Loading configuration from {args.config}")
    config = load_config(args.config)
    
    if not config:
        logger.warning(f"Configuration file not found or invalid: {args.config}")
        logger.info("Using default configuration")
        
        # Create custom configuration
        config = create_custom_config()
    
    # Update app configuration
    app.config = config
    
    # Get host and port from command line arguments or configuration
    host = args.host or config.get("server", {}).get("host", "0.0.0.0")
    port = args.port or config.get("server", {}).get("port", 8000)
    debug = args.debug or config.get("server", {}).get("debug", False)
    
    # Print configuration
    print("\nServer Configuration:")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    
    print("\nModel Configuration:")
    print(f"Models Directory: {config.get('model', {}).get('models_dir', 'models')}")
    print(f"Kernel Type: {config.get('model', {}).get('kernel_type', 'i2_s')}")
    print(f"Number of Threads: {config.get('model', {}).get('num_threads', 4)}")
    
    print("\nMemory Configuration:")
    print(f"Max Items: {config.get('memory', {}).get('max_items', 100)}")
    print(f"Max Context Length: {config.get('memory', {}).get('max_context_length', 2000)}")
    
    print("\nTeam Configuration:")
    print(f"Default Collaboration Mode: {config.get('team', {}).get('default_collaboration_mode', 'SEQUENTIAL')}")
    print(f"Max Parallel Tasks: {config.get('team', {}).get('max_parallel_tasks', 4)}")
    
    # Run server
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="debug" if debug else "info")

if __name__ == "__main__":
    main()
