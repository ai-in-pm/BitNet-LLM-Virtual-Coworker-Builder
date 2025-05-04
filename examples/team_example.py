"""
Example of using a team of virtual co-workers with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import logging

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

def main():
    """
    Main function.
    """
    # Initialize BitNet model
    # In a real implementation, you would provide the path to a real BitNet model
    model = BitNetModel(
        model_path="models/bitnet_model",  # This is a placeholder path
        kernel_type="i2_s",
        use_bitnet_integration=False  # Set to True when using a real BitNet model
    )
    
    # Create tools
    def web_search(query):
        """
        Mock web search tool.
        """
        logger.info(f"Searching for: {query}")
        
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
            """
        else:
            return f"Search results for: {query}"
    
    def data_analysis(data):
        """
        Mock data analysis tool.
        """
        logger.info(f"Analyzing data: {data[:50]}...")
        
        return {
            "summary": "Analysis of climate change data",
            "trends": [
                "Increasing global temperatures",
                "Rising sea levels",
                "More frequent extreme weather events"
            ]
        }
    
    search_tool = Tool(
        name="search",
        description="Search the web for information",
        function=web_search,
        args_schema={
            "query": {
                "type": "string",
                "description": "Search query"
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
        collaboration_mode=CollaborationMode.SEQUENTIAL
    )
    
    # Run the team on a task
    task = "Research climate change, analyze the data, and write a brief report"
    logger.info(f"Running team on task: {task}")
    
    result = team.run(task)
    
    print("\nTeam Response:")
    print(result)
    
    # Try a different collaboration mode
    team.collaboration_mode = CollaborationMode.HIERARCHICAL
    logger.info(f"Changing collaboration mode to HIERARCHICAL")
    
    result = team.run(task)
    
    print("\nTeam Response (Hierarchical mode):")
    print(result)

if __name__ == "__main__":
    main()
