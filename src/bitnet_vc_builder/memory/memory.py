"""
Memory system for BitNet Virtual Co-worker Builder.
"""

import time
import logging
from typing import List, Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

class Memory:
    """
    Memory system for BitNet virtual co-workers.
    
    This class provides functionality for storing and retrieving information
    that virtual co-workers can use across interactions.
    """
    
    def __init__(
        self,
        max_items: int = 100,
        max_context_length: int = 2000,
        recency_bias: float = 0.7
    ):
        """
        Initialize memory.
        
        Args:
            max_items: Maximum number of items to store
            max_context_length: Maximum length of context to return
            recency_bias: Bias towards recent items (0-1, higher means more bias)
        """
        self.max_items = max_items
        self.max_context_length = max_context_length
        self.recency_bias = recency_bias
        self.items = []
    
    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an item to memory.
        
        Args:
            content: Content to add
            metadata: Additional metadata
        """
        # Create memory item
        item = {
            "content": content,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        # Add to items
        self.items.append(item)
        
        # Trim if necessary
        if len(self.items) > self.max_items:
            self.items = self.items[-self.max_items:]
    
    def get_context(self, query: Optional[str] = None, max_items: Optional[int] = None) -> str:
        """
        Get context from memory.
        
        Args:
            query: Query to filter items (optional)
            max_items: Maximum number of items to return (optional)
            
        Returns:
            Context string
        """
        if not self.items:
            return ""
        
        # Use instance max_items if not provided
        max_items = max_items or self.max_items
        
        # Get items
        items = self._get_relevant_items(query, max_items)
        
        # Format context
        context = ""
        total_length = 0
        
        for item in items:
            item_text = f"[{self._format_timestamp(item['timestamp'])}] {item['content']}\n\n"
            item_length = len(item_text)
            
            # Check if adding this item would exceed max context length
            if total_length + item_length > self.max_context_length:
                # If this is the first item, add a truncated version
                if total_length == 0:
                    truncated_text = item_text[:self.max_context_length - 3] + "..."
                    context += truncated_text
                break
            
            context += item_text
            total_length += item_length
        
        return context.strip()
    
    def _get_relevant_items(self, query: Optional[str], max_items: int) -> List[Dict[str, Any]]:
        """
        Get relevant items from memory.
        
        Args:
            query: Query to filter items
            max_items: Maximum number of items to return
            
        Returns:
            List of relevant items
        """
        # If no query, return most recent items
        if not query:
            return sorted(self.items, key=lambda x: x["timestamp"], reverse=True)[:max_items]
        
        # Score items based on relevance to query and recency
        scored_items = []
        
        for item in self.items:
            # Calculate relevance score (simple substring matching for now)
            relevance_score = 1.0 if query.lower() in item["content"].lower() else 0.0
            
            # Calculate recency score (normalized between 0 and 1)
            newest_timestamp = self.items[-1]["timestamp"]
            oldest_timestamp = self.items[0]["timestamp"]
            timestamp_range = newest_timestamp - oldest_timestamp
            
            if timestamp_range == 0:
                recency_score = 1.0
            else:
                recency_score = (item["timestamp"] - oldest_timestamp) / timestamp_range
            
            # Combine scores
            combined_score = (relevance_score * (1 - self.recency_bias)) + (recency_score * self.recency_bias)
            
            scored_items.append((item, combined_score))
        
        # Sort by score and return top items
        return [item for item, score in sorted(scored_items, key=lambda x: x[1], reverse=True)[:max_items]]
    
    def _format_timestamp(self, timestamp: float) -> str:
        """
        Format timestamp.
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            Formatted timestamp
        """
        from datetime import datetime
        
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def clear(self) -> None:
        """
        Clear memory.
        """
        self.items = []
    
    def search(self, query: str, max_items: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search memory.
        
        Args:
            query: Search query
            max_items: Maximum number of items to return
            
        Returns:
            List of matching items
        """
        # Use instance max_items if not provided
        max_items = max_items or self.max_items
        
        # Get relevant items
        return self._get_relevant_items(query, max_items)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory statistics
        """
        return {
            "total_items": len(self.items),
            "max_items": self.max_items,
            "max_context_length": self.max_context_length,
            "recency_bias": self.recency_bias,
            "oldest_timestamp": self._format_timestamp(self.items[0]["timestamp"]) if self.items else None,
            "newest_timestamp": self._format_timestamp(self.items[-1]["timestamp"]) if self.items else None
        }
    
    def __len__(self) -> int:
        """
        Get number of items in memory.
        
        Returns:
            Number of items
        """
        return len(self.items)
    
    def __str__(self) -> str:
        """
        Get string representation of memory.
        
        Returns:
            String representation
        """
        return f"Memory(items={len(self.items)}, max={self.max_items})"
