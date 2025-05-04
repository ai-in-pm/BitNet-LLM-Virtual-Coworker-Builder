"""
Example of creating and using a custom tool with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import logging
import argparse
import requests
from typing import Dict, Any, List, Optional

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.tools.base_tools import Tool
from bitnet_vc_builder.memory.memory import Memory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_weather_tool():
    """
    Create a weather tool.
    
    Returns:
        Weather tool
    """
    def get_weather(location: str) -> Dict[str, Any]:
        """
        Get weather information for a location.
        
        Args:
            location: Location to get weather for
            
        Returns:
            Weather information
        """
        # In a real implementation, you would use a weather API
        # For this example, we'll use a mock implementation
        
        logger.info(f"Getting weather for {location}")
        
        # Generate mock weather data
        weather_data = {
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
        
        return weather_data
    
    return Tool(
        name="weather",
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

def create_news_tool():
    """
    Create a news tool.
    
    Returns:
        News tool
    """
    def get_news(topic: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Get news articles about a topic.
        
        Args:
            topic: Topic to get news about
            max_results: Maximum number of results to return
            
        Returns:
            List of news articles
        """
        # In a real implementation, you would use a news API
        # For this example, we'll use a mock implementation
        
        logger.info(f"Getting news about {topic}")
        
        # Generate mock news data
        news_data = []
        
        for i in range(max_results):
            news_data.append({
                "title": f"News article {i+1} about {topic}",
                "source": f"News Source {i+1}",
                "url": f"https://example.com/news/{topic.lower().replace(' ', '-')}/{i+1}",
                "summary": f"This is a summary of news article {i+1} about {topic}."
            })
        
        return news_data
    
    return Tool(
        name="news",
        description="Get news articles about a topic",
        function=get_news,
        args_schema={
            "topic": {
                "type": "string",
                "description": "Topic to get news about",
                "required": True
            },
            "max_results": {
                "type": "number",
                "description": "Maximum number of results to return",
                "required": False
            }
        }
    )

def create_translator_tool():
    """
    Create a translator tool.
    
    Returns:
        Translator tool
    """
    def translate(text: str, target_language: str) -> str:
        """
        Translate text to a target language.
        
        Args:
            text: Text to translate
            target_language: Target language
            
        Returns:
            Translated text
        """
        # In a real implementation, you would use a translation API
        # For this example, we'll use a mock implementation
        
        logger.info(f"Translating text to {target_language}")
        
        # Simple mock translation
        if target_language.lower() == "spanish":
            return f"[Spanish translation of: {text}]"
        elif target_language.lower() == "french":
            return f"[French translation of: {text}]"
        elif target_language.lower() == "german":
            return f"[German translation of: {text}]"
        else:
            return f"[{target_language} translation of: {text}]"
    
    return Tool(
        name="translate",
        description="Translate text to a target language",
        function=translate,
        args_schema={
            "text": {
                "type": "string",
                "description": "Text to translate",
                "required": True
            },
            "target_language": {
                "type": "string",
                "description": "Target language",
                "required": True
            }
        }
    )

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Custom tool example")
    
    parser.add_argument(
        "--model-path",
        type=str,
        default="models/bitnet_model",
        help="Path to BitNet model"
    )
    
    parser.add_argument(
        "--kernel-type",
        type=str,
        choices=["i2_s", "i2_m", "i2_l"],
        default="i2_s",
        help="BitNet kernel type"
    )
    
    parser.add_argument(
        "--use-bitnet",
        action="store_true",
        help="Use BitNet integration"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        default="What's the weather in New York? Also, get me the latest news about technology and translate 'Hello, how are you?' to Spanish.",
        help="Task to run"
    )
    
    args = parser.parse_args()
    
    # Create model
    logger.info(f"Creating BitNet model: {args.model_path}")
    model = BitNetModel(
        model_path=args.model_path,
        kernel_type=args.kernel_type,
        use_bitnet_integration=args.use_bitnet
    )
    
    # Create tools
    weather_tool = create_weather_tool()
    news_tool = create_news_tool()
    translator_tool = create_translator_tool()
    
    # Create memory
    memory = Memory()
    
    # Create virtual co-worker
    logger.info("Creating virtual co-worker")
    virtual_coworker = BitNetVirtualCoworker(
        model=model,
        tools=[weather_tool, news_tool, translator_tool],
        memory=memory,
        name="AssistantCoworker",
        description="A virtual co-worker that can help with various tasks"
    )
    
    # Run virtual co-worker
    logger.info(f"Running virtual co-worker on task: {args.task}")
    result = virtual_coworker.run(args.task)
    
    # Print result
    print("\nResult:")
    print("-------")
    print(result)

if __name__ == "__main__":
    main()
