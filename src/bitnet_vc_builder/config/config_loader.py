"""
Configuration loader for BitNet Virtual Co-worker Builder.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    logger.info(f"Loading configuration from {config_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(config_path):
            logger.warning(f"Configuration file {config_path} not found. Using default configuration.")
            return {}
        
        # Load YAML file
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Configuration loaded successfully")
        
        return config or {}
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}

def save_config(config: Dict[str, Any], config_path: str) -> bool:
    """
    Save configuration to a YAML file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to the configuration file
        
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Saving configuration to {config_path}")
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Save YAML file
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        
        logger.info(f"Configuration saved successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False

def get_config_value(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Get a value from the configuration.
    
    Args:
        config: Configuration dictionary
        key: Key to get (can be nested using dots, e.g. "server.host")
        default: Default value if key is not found
        
    Returns:
        Value from the configuration or default
    """
    # Split key by dots
    keys = key.split(".")
    
    # Get value
    value = config
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default
    
    return value

def set_config_value(config: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    """
    Set a value in the configuration.
    
    Args:
        config: Configuration dictionary
        key: Key to set (can be nested using dots, e.g. "server.host")
        value: Value to set
        
    Returns:
        Updated configuration dictionary
    """
    # Split key by dots
    keys = key.split(".")
    
    # Set value
    if len(keys) == 1:
        config[keys[0]] = value
        return config
    
    # Create nested dictionaries if they don't exist
    current = config
    
    for i, k in enumerate(keys[:-1]):
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        
        current = current[k]
    
    # Set value in the last dictionary
    current[keys[-1]] = value
    
    return config
