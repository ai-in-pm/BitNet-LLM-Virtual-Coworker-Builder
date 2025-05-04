"""
Common tools for BitNet Virtual Co-worker Builder.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional, List, Union

from bitnet_vc_builder.tools.base_tools import Tool

logger = logging.getLogger(__name__)

def web_search(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: Search query
        
    Returns:
        Search results
    """
    logger.info(f"Searching for: {query}")
    
    try:
        # Use a search API (this is a mock implementation)
        # In a real implementation, you would use a search API like Google, Bing, or DuckDuckGo
        
        # Mock response
        if "climate change" in query.lower():
            return """
            Climate change refers to long-term shifts in temperatures and weather patterns.
            These shifts may be natural, but since the 1800s, human activities have been
            the main driver of climate change, primarily due to the burning of fossil fuels
            like coal, oil, and gas, which produces heat-trapping gases.
            
            Key facts:
            - Global temperature has risen by about 1.1°C since the pre-industrial period
            - The last decade (2011-2020) was the warmest on record
            - Sea levels are rising at a rate of about 3.7 mm per year
            - Arctic sea ice is declining at a rate of 13.1% per decade
            
            Addressing climate change requires both mitigation (reducing emissions) and
            adaptation (adjusting to current and future effects).
            """
        elif "renewable energy" in query.lower():
            return """
            Renewable energy is energy derived from natural sources that are replenished
            at a higher rate than they are consumed. Common types include:
            
            - Solar energy: Harnessing energy from the sun
            - Wind energy: Converting wind into electricity
            - Hydroelectric energy: Using flowing water to generate power
            - Geothermal energy: Using heat from the Earth's interior
            - Biomass energy: Using organic material from plants and animals
            
            Renewable energy accounted for about 29% of global electricity generation in 2020,
            with hydropower being the largest source followed by wind and solar.
            """
        else:
            return f"Search results for: {query}\n\nThis is a mock implementation. In a real implementation, this would return actual search results."
    except Exception as e:
        logger.error(f"Error searching: {e}")
        return f"Error searching for '{query}': {str(e)}"

def fetch_weather(location: str) -> Dict[str, Any]:
    """
    Fetch weather information for a location.
    
    Args:
        location: Location to fetch weather for
        
    Returns:
        Weather information
    """
    logger.info(f"Fetching weather for: {location}")
    
    try:
        # Use a weather API (this is a mock implementation)
        # In a real implementation, you would use a weather API like OpenWeatherMap or WeatherAPI
        
        # Mock response
        if "new york" in location.lower():
            return {
                "location": "New York, NY",
                "temperature": 72,
                "condition": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 8,
                "forecast": [
                    {"day": "Today", "high": 75, "low": 65, "condition": "Partly Cloudy"},
                    {"day": "Tomorrow", "high": 78, "low": 67, "condition": "Sunny"},
                    {"day": "Wednesday", "high": 80, "low": 68, "condition": "Sunny"}
                ]
            }
        elif "london" in location.lower():
            return {
                "location": "London, UK",
                "temperature": 18,
                "condition": "Rainy",
                "humidity": 80,
                "wind_speed": 12,
                "forecast": [
                    {"day": "Today", "high": 20, "low": 15, "condition": "Rainy"},
                    {"day": "Tomorrow", "high": 22, "low": 16, "condition": "Cloudy"},
                    {"day": "Wednesday", "high": 23, "low": 17, "condition": "Partly Cloudy"}
                ]
            }
        else:
            return {
                "location": location,
                "temperature": 75,
                "condition": "Sunny",
                "humidity": 60,
                "wind_speed": 5,
                "forecast": [
                    {"day": "Today", "high": 78, "low": 65, "condition": "Sunny"},
                    {"day": "Tomorrow", "high": 80, "low": 67, "condition": "Sunny"},
                    {"day": "Wednesday", "high": 82, "low": 68, "condition": "Partly Cloudy"}
                ]
            }
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return {"error": f"Error fetching weather for '{location}': {str(e)}"}

def calculate(expression: str) -> Union[float, str]:
    """
    Calculate a mathematical expression.
    
    Args:
        expression: Mathematical expression
        
    Returns:
        Result of the calculation
    """
    logger.info(f"Calculating: {expression}")
    
    try:
        # Evaluate the expression (this is unsafe for production use)
        # In a real implementation, you would use a safer method to evaluate expressions
        result = eval(expression)
        return result
    except Exception as e:
        logger.error(f"Error calculating: {e}")
        return f"Error calculating '{expression}': {str(e)}"

def get_available_tools() -> Dict[str, Tool]:
    """
    Get all available tools.
    
    Returns:
        Dictionary of available tools
    """
    tools = {
        "web_search": Tool(
            name="web_search",
            description="Search the web for information",
            function=web_search,
            args_schema={
                "query": {
                    "type": "string",
                    "description": "Search query",
                    "required": True
                }
            }
        ),
        "fetch_weather": Tool(
            name="fetch_weather",
            description="Fetch weather information for a location",
            function=fetch_weather,
            args_schema={
                "location": {
                    "type": "string",
                    "description": "Location to fetch weather for",
                    "required": True
                }
            }
        ),
        "calculate": Tool(
            name="calculate",
            description="Calculate a mathematical expression",
            function=calculate,
            args_schema={
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to calculate",
                    "required": True
                }
            }
        )
    }
    
    return tools
