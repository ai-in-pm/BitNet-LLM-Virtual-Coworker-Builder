"""
Example of using the memory system with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import logging
import argparse
from typing import List, Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.memory.memory import Memory

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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Memory example")
    
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
    
    args = parser.parse_args()
    
    # Create model
    logger.info(f"Creating BitNet model: {args.model_path}")
    model = BitNetModel(
        model_path=args.model_path,
        kernel_type=args.kernel_type,
        use_bitnet_integration=args.use_bitnet
    )
    
    # Create memory
    memory = Memory(
        max_items=10,
        max_context_length=1000,
        recency_bias=0.7
    )
    
    # Create virtual co-worker
    logger.info("Creating virtual co-worker")
    virtual_coworker = BitNetVirtualCoworker(
        model=model,
        memory=memory,
        name="MemoryCoworker",
        description="A virtual co-worker that demonstrates memory capabilities"
    )
    
    # Add some facts to memory
    logger.info("Adding facts to memory")
    memory.add("My name is John.")
    memory.add("I live in New York.")
    memory.add("I work as a software engineer.")
    memory.add("I have a dog named Max.")
    memory.add("My favorite color is blue.")
    
    # Run a series of interactions
    interactions = [
        "What's my name?",
        "Where do I live?",
        "What do I do for a living?",
        "Tell me about my pet.",
        "What's my favorite color?",
        "What's my dog's name?",
        "Summarize what you know about me."
    ]
    
    for i, interaction in enumerate(interactions):
        print(f"\nInteraction {i+1}: {interaction}")
        print("-" * 50)
        
        # Run virtual co-worker
        result = virtual_coworker.run(interaction)
        
        # Print result
        print(result)
        
        # Add user feedback to memory
        if i < len(interactions) - 1:  # Skip feedback for the last interaction
            feedback = f"User asked: {interaction}. You responded correctly about {interaction.lower().replace('?', '')}."
            memory.add(feedback)
    
    # Print memory stats
    print("\nMemory Stats:")
    print("-------------")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Print memory context
    print("\nMemory Context:")
    print("--------------")
    context = memory.get_context()
    print(context)

if __name__ == "__main__":
    main()
