"""
Example of using a single virtual co-worker with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import logging
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder import BitNetVirtualCoworker, BitNetModel, Tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def web_search(query: str) -> str:
    """
    Mock web search function.
    
    Args:
        query: Search query
        
    Returns:
        Search results
    """
    logger.info(f"Searching for: {query}")
    
    # In a real implementation, this would call a search API
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
    else:
        return f"No specific information found for: {query}"

def main():
    """
    Main function.
    """
    # Initialize BitNet model
    # In a real implementation, you would provide the path to a real BitNet model
    model = BitNetModel(
        model_path="models/bitnet_b1_58-large",  # This is a placeholder path
        kernel_type="i2_s",
        bitnet_path=None,  # Optional: Path to BitNet installation
        use_bitnet_integration=False  # Set to True when using a real BitNet model
    )
    
    # Create tools
    search_tool = Tool(
        name="search",
        description="Search the web for information",
        function=web_search,
        args_schema={
            "query": {
                "type": "string",
                "description": "The search query"
            }
        }
    )
    
    # Create virtual co-worker
    coworker = BitNetVirtualCoworker(
        model=model,
        tools=[search_tool],
        name="ResearchCoworker",
        description="A virtual co-worker that can search for and summarize information"
    )
    
    # Run virtual co-worker on a task
    task = "Find information about climate change and summarize it in 3 bullet points"
    logger.info(f"Running virtual co-worker on task: {task}")
    
    result = coworker.run(task)
    
    print("\nVirtual Co-worker Response:")
    print(result)

if __name__ == "__main__":
    main()
