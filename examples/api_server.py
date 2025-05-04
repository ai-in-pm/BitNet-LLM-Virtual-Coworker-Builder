"""
Example of running the BitNet Virtual Co-worker Builder API server.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.api.server import app
from bitnet_vc_builder.config.config_loader import load_config
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """
    Main function.
    """
    # Load configuration
    config_path = os.environ.get("CONFIG_PATH", "../config/config.yaml")
    config = load_config(config_path)
    
    # Get server configuration
    host = config.get("server", {}).get("host", "0.0.0.0")
    port = config.get("server", {}).get("port", 8000)
    
    # Print server information
    logger.info(f"Starting BitNet Virtual Co-worker Builder API server on {host}:{port}")
    logger.info(f"API documentation available at http://{host}:{port}/docs")
    
    # Run server
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
