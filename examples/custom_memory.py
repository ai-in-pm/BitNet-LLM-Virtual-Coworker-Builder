"""
Example of using a custom memory implementation with BitNet Virtual Co-worker Builder.
"""

import os
import sys
import time
import json
import logging
import argparse
from typing import List, Dict, Any, Optional, Union

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

class PersistentMemory(Memory):
    """
    Custom memory implementation with persistence.
    """
    
    def __init__(
        self,
        max_items: int = 100,
        max_context_length: int = 2000,
        recency_bias: float = 0.7,
        file_path: Optional[str] = None,
        auto_save: bool = True
    ):
        """
        Initialize persistent memory.
        
        Args:
            max_items: Maximum number of items to store
            max_context_length: Maximum length of context to return
            recency_bias: Bias towards more recent items (0-1, higher means more bias)
            file_path: Path to the memory file
            auto_save: Whether to automatically save memory after adding items
        """
        super().__init__(
            max_items=max_items,
            max_context_length=max_context_length,
            recency_bias=recency_bias
        )
        
        self.file_path = file_path or "memory.json"
        self.auto_save = auto_save
        
        # Load memory from file if it exists
        self._load()
    
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an item to memory.
        
        Args:
            content: Content to add
            metadata: Additional metadata
        """
        # Add item to memory
        super().add(content, metadata)
        
        # Save memory if auto_save is enabled
        if self.auto_save:
            self.save()
    
    def save(self) -> bool:
        """
        Save memory to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
            
            # Save memory to file
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.items, f, indent=2)
            
            logger.info(f"Memory saved to {self.file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            return False
    
    def _load(self) -> bool:
        """
        Load memory from file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(self.file_path):
                logger.info(f"Memory file not found: {self.file_path}")
                return False
            
            # Load memory from file
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.items = json.load(f)
            
            logger.info(f"Memory loaded from {self.file_path} ({len(self.items)} items)")
            return True
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return False
    
    def clear(self) -> None:
        """
        Clear memory.
        """
        super().clear()
        
        # Save empty memory if auto_save is enabled
        if self.auto_save:
            self.save()

class CategorizedMemory(Memory):
    """
    Custom memory implementation with categorization.
    """
    
    def __init__(
        self,
        max_items: int = 100,
        max_context_length: int = 2000,
        recency_bias: float = 0.7,
        categories: Optional[List[str]] = None
    ):
        """
        Initialize categorized memory.
        
        Args:
            max_items: Maximum number of items to store
            max_context_length: Maximum length of context to return
            recency_bias: Bias towards more recent items (0-1, higher means more bias)
            categories: List of categories
        """
        super().__init__(
            max_items=max_items,
            max_context_length=max_context_length,
            recency_bias=recency_bias
        )
        
        self.categories = categories or ["general", "personal", "work", "technical"]
        self.categorized_items = {category: [] for category in self.categories}
    
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None, category: str = "general") -> None:
        """
        Add an item to memory.
        
        Args:
            content: Content to add
            metadata: Additional metadata
            category: Category to add the item to
        """
        # Create memory item
        item = {
            "content": content,
            "timestamp": time.time(),
            "metadata": metadata or {},
            "category": category
        }
        
        # Add item to general items
        self.items.append(item)
        
        # Trim if necessary
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]
        
        # Add item to categorized items
        if category in self.categories:
            self.categorized_items[category].append(item)
            
            # Trim if necessary
            if len(self.categorized_items[category]) > self.max_items:
                self.categorized_items[category] = self.categorized_items[category][-self.max_items:]
        else:
            # Add to general category if category doesn't exist
            self.categorized_items["general"].append(item)
            
            # Trim if necessary
            if len(self.categorized_items["general"]) > self.max_items:
                self.categorized_items["general"] = self.categorized_items["general"][-self.max_items:]
    
    def get_context(
        self,
        query: Optional[str] = None,
        max_items: Optional[int] = None,
        max_length: Optional[int] = None,
        category: Optional[str] = None
    ) -> str:
        """
        Get context from memory.
        
        Args:
            query: Query to filter items (optional)
            max_items: Maximum number of items to include (optional)
            max_length: Maximum length of context (optional)
            category: Category to get context from (optional)
            
        Returns:
            Context string
        """
        # Use default values if not provided
        max_items = max_items or self.max_items
        max_length = max_length or self.max_context_length
        
        # Get items from specific category if provided
        if category and category in self.categories:
            items = self.categorized_items[category]
        else:
            items = self.items
        
        # Get relevant items
        if query:
            # Search for relevant items
            scored_items = []
            
            for item in items:
                # Calculate relevance score
                relevance = self._calculate_relevance(item, query)
                
                # Add to scored items
                scored_items.append((item, relevance))
            
            # Sort by relevance score (highest first)
            scored_items.sort(key=lambda x: x[1], reverse=True)
            
            # Get top items
            items = [item for item, _ in scored_items[:max_items]]
        else:
            # Sort by timestamp (newest first)
            items = sorted(items, key=lambda x: x["timestamp"], reverse=True)
            
            # Limit number of items
            items = items[:max_items]
        
        # Build context
        context = ""
        
        for item in items:
            # Add category if available
            item_text = f"[{item.get('category', 'general')}] {item['content']}\n\n"
            
            # Check if adding this item would exceed max length
            if len(context) + len(item_text) > max_length:
                # Truncate item text to fit within max length
                available_length = max_length - len(context)
                if available_length > 0:
                    item_text = item_text[:available_length]
                    context += item_text
                break
            
            # Add item text
            context += item_text
        
        return context.strip()
    
    def get_categories(self) -> List[str]:
        """
        Get list of categories.
        
        Returns:
            List of categories
        """
        return self.categories
    
    def get_category_stats(self) -> Dict[str, int]:
        """
        Get statistics for each category.
        
        Returns:
            Dictionary of category names to item counts
        """
        return {category: len(items) for category, items in self.categorized_items.items()}
    
    def clear(self) -> None:
        """
        Clear memory.
        """
        super().clear()
        self.categorized_items = {category: [] for category in self.categories}

def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Custom memory example")
    
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
        "--memory-type",
        type=str,
        choices=["persistent", "categorized"],
        default="persistent",
        help="Type of memory to use"
    )
    
    parser.add_argument(
        "--memory-file",
        type=str,
        default="memory.json",
        help="Path to memory file (for persistent memory)"
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
    if args.memory_type == "persistent":
        logger.info(f"Creating persistent memory with file: {args.memory_file}")
        memory = PersistentMemory(
            max_items=100,
            max_context_length=2000,
            recency_bias=0.7,
            file_path=args.memory_file,
            auto_save=True
        )
    else:
        logger.info("Creating categorized memory")
        memory = CategorizedMemory(
            max_items=100,
            max_context_length=2000,
            recency_bias=0.7,
            categories=["general", "personal", "work", "technical"]
        )
    
    # Create virtual co-worker
    logger.info("Creating virtual co-worker")
    virtual_coworker = BitNetVirtualCoworker(
        model=model,
        memory=memory,
        name="MemoryCoworker",
        description="A virtual co-worker that demonstrates custom memory capabilities"
    )
    
    # Add some facts to memory
    if args.memory_type == "persistent":
        logger.info("Adding facts to persistent memory")
        memory.add("My name is John.")
        memory.add("I live in New York.")
        memory.add("I work as a software engineer.")
        memory.add("I have a dog named Max.")
        memory.add("My favorite color is blue.")
    else:
        logger.info("Adding facts to categorized memory")
        memory.add("My name is John.", category="personal")
        memory.add("I live in New York.", category="personal")
        memory.add("I work as a software engineer.", category="work")
        memory.add("I'm currently working on a machine learning project.", category="work")
        memory.add("I have a dog named Max.", category="personal")
        memory.add("My favorite color is blue.", category="personal")
        memory.add("Python is a high-level programming language.", category="technical")
        memory.add("TensorFlow is a machine learning framework.", category="technical")
    
    # Run a series of interactions
    interactions = [
        "What's my name?",
        "Where do I live?",
        "What do I do for a living?",
        "Tell me about my pet.",
        "What's my favorite color?",
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
            
            if args.memory_type == "categorized":
                memory.add(feedback, category="general")
            else:
                memory.add(feedback)
    
    # Print memory stats
    print("\nMemory Stats:")
    print("-------------")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Print category stats for categorized memory
    if args.memory_type == "categorized":
        print("\nCategory Stats:")
        print("--------------")
        category_stats = memory.get_category_stats()
        for category, count in category_stats.items():
            print(f"{category}: {count} items")
    
    # Print memory context
    print("\nMemory Context:")
    print("--------------")
    context = memory.get_context()
    print(context)
    
    # Save persistent memory
    if args.memory_type == "persistent":
        memory.save()
        print(f"\nMemory saved to {args.memory_file}")

if __name__ == "__main__":
    main()
