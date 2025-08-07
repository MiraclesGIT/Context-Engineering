"""
Base Classes for Context Engineering Components
===============================================

Abstract base classes and common interfaces for all context engineering components.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import time

@dataclass
class ProcessingResult:
    """Standard result format for all processing operations"""
    content: str
    confidence: float
    processing_time: float
    metadata: Dict[str, Any]
    reasoning_trace: List[Dict[str, Any]]

class BaseContextProcessor(ABC):
    """Base class for all context processing components"""
    
    def __init__(self, config: Any):
        self.config = config
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.last_processing_time = 0.0
        
    @abstractmethod
    async def process(
        self, 
        content: str, 
        context: Dict[str, Any]
    ) -> ProcessingResult:
        """Process content with given context"""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset processor state"""
        pass
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processing metrics"""
        return {
            "processing_count": self.processing_count,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": (
                self.total_processing_time / self.processing_count 
                if self.processing_count > 0 else 0.0
            ),
            "last_processing_time": self.last_processing_time
        }
    
    def _record_processing(self, processing_time: float):
        """Record processing metrics"""
        self.processing_count += 1
        self.total_processing_time += processing_time
        self.last_processing_time = processing_time

class BaseFieldProcessor(BaseContextProcessor):
    """Base class for field-based processors"""
    
    def __init__(self, config: Any):
        super().__init__(config)
        self.field_state = {}
        self.attractors = {}
    
    @abstractmethod
    def inject_pattern(self, pattern: str, strength: float = 1.0):
        """Inject a pattern into the field"""
        pass
    
    @abstractmethod
    def measure_resonance(self, content: str) -> float:
        """Measure resonance between content and field"""
        pass
    
    def get_field_state(self) -> Dict[str, Any]:
        """Get current field state"""
        return {
            "patterns": self.field_state.copy(),
            "attractors": self.attractors.copy(),
            "field_energy": self._calculate_field_energy(),
            "stability": self._calculate_stability()
        }
    
    def _calculate_field_energy(self) -> float:
        """Calculate total field energy"""
        return sum(self.field_state.values()) if self.field_state else 0.0
    
    def _calculate_stability(self) -> float:
        """Calculate field stability"""
        if not self.attractors:
            return 0.0
        return sum(a.get("strength", 0) for a in self.attractors.values()) / len(self.attractors)

class BaseMemoryProcessor(BaseContextProcessor):
    """Base class for memory-based processors"""
    
    def __init__(self, config: Any):
        super().__init__(config)
        self.memory_store = {}
        self.consolidation_count = 0
    
    @abstractmethod
    def store_memory(self, key: str, content: Any, priority: float = 1.0):
        """Store content in memory"""
        pass
    
    @abstractmethod
    def retrieve_memory(self, query: str, max_results: int = 5) -> List[Any]:
        """Retrieve relevant memories"""
        pass
    
    @abstractmethod
    def consolidate_memory(self) -> Dict[str, Any]:
        """Perform memory consolidation"""
        pass
    
    def get_memory_state(self) -> Dict[str, Any]:
        """Get current memory state"""
        return {
            "memory_count": len(self.memory_store),
            "consolidation_count": self.consolidation_count,
            "memory_efficiency": self._calculate_memory_efficiency(),
            "top_memories": self._get_top_memories()
        }
    
    def _calculate_memory_efficiency(self) -> float:
        """Calculate memory efficiency"""
        if not self.memory_store:
            return 1.0
        # Simplified efficiency calculation
        return min(1.0, 1000 / len(self.memory_store))  # Assume 1000 is optimal
    
    def _get_top_memories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top priority memories"""
        return list(self.memory_store.items())[:limit]

class BaseToolProcessor(BaseContextProcessor):
    """Base class for tool-based processors"""
    
    def __init__(self, config: Any):
        super().__init__(config)
        self.available_tools = {}
        self.tool_usage_count = {}
    
    @abstractmethod
    def execute_tool(
        self, 
        tool_name: str, 
        content: str, 
        parameters: Dict[str, Any]
    ) -> ProcessingResult:
        """Execute a specific tool"""
        pass
    
    def register_tool(self, tool_name: str, tool_function: callable):
        """Register a new tool"""
        self.available_tools[tool_name] = tool_function
        self.tool_usage_count[tool_name] = 0
    
    def get_tool_metrics(self) -> Dict[str, Any]:
        """Get tool usage metrics"""
        return {
            "available_tools": list(self.available_tools.keys()),
            "tool_usage": self.tool_usage_count.copy(),
            "most_used_tool": max(self.tool_usage_count.items(), key=lambda x: x[1])[0] if self.tool_usage_count else None
        }