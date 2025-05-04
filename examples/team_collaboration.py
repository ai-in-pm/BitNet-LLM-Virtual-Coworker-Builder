"""
Example of using a team of virtual co-workers with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import logging
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder import BitNetVirtualCoworker, BitNetModel, Tool, BitNetTeam
from bitnet_vc_builder.core.team import CollaborationMode

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
    elif "data analysis" in query.lower():
        return """
        Data analysis is the process of inspecting, cleaning, transforming, and modeling data
        to discover useful information, draw conclusions, and support decision-making.
        
        Key steps in data analysis:
        1. Data collection
        2. Data cleaning and preprocessing
        3. Exploratory data analysis
        4. Statistical analysis
        5. Data visualization
        6. Interpretation and reporting
        
        Common tools for data analysis include Python (with libraries like Pandas, NumPy, and Matplotlib),
        R, SQL, Excel, and specialized software like Tableau and Power BI.
        """
    else:
        return f"No specific information found for: {query}"

def data_analysis(data: str) -> Dict[str, Any]:
    """
    Mock data analysis function.
    
    Args:
        data: Data to analyze
        
    Returns:
        Analysis results
    """
    logger.info(f"Analyzing data: {data[:50]}...")
    
    # In a real implementation, this would perform actual data analysis
    return {
        "summary": "Analysis of climate change data",
        "trends": [
            "Increasing global temperatures",
            "Rising sea levels",
            "More frequent extreme weather events"
        ],
        "confidence": 0.95
    }

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
    
    analysis_tool = Tool(
        name="analyze",
        description="Analyze data",
        function=data_analysis,
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
        description="A virtual co-worker that searches for information"
    )
    
    analyst = BitNetVirtualCoworker(
        model=model,
        tools=[analysis_tool],
        name="Analyst",
        description="A virtual co-worker that analyzes information"
    )
    
    writer = BitNetVirtualCoworker(
        model=model,
        tools=[],
        name="Writer",
        description="A virtual co-worker that writes reports"
    )
    
    # Create a team
    team = BitNetTeam(
        agents=[researcher, analyst, writer],
        name="ResearchTeam",
        description="A team that researches, analyzes, and reports on topics",
        collaboration_mode=CollaborationMode.HIERARCHICAL
    )
    
    # Run the team on a task
    task = "Research climate change, analyze the data, and write a brief report with recommendations"
    logger.info(f"Running team on task: {task}")
    
    result = team.run(task)
    
    print("\nTeam Response:")
    print(result)

if __name__ == "__main__":
    main()
