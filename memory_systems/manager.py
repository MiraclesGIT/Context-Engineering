"""
Memory Manager - MEM1 Framework Implementation
==============================================

Manages memory consolidation, retrieval, and efficiency optimization
based on Singapore-MIT MEM1 research for long-horizon reasoning.
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..core.base import BaseMemoryProcessor, ProcessingResult
from .consolidation import MemoryConsolidator
from .retrieval import MemoryRetriever
from .efficiency import EfficiencyOptimizer

@dataclass
class MemoryItem:
    """Individual memory item"""
    id: str
    content: str
    context: Dict[str, Any]
    reasoning_value: float
    timestamp: float
    access_count: int = 0
    last_accessed: float = 0.0

@dataclass
class RetrievalResult:
    """Result from memory retrieval"""
    memories: List[MemoryItem]
    average_relevance: float
    retrieval_efficiency: float

@dataclass
class ConsolidationResult:
    """Result from memory consolidation"""
    insights: List[str]
    efficiency_score: float
    memories_consolidated: int
    memories_pruned: int

class MemoryManager(BaseMemoryProcessor):
    """
    Memory Manager implementing Singapore-MIT MEM1 framework.
    
    Provides:
    - Reasoning-driven memory consolidation
    - Selective retention and compression  
    - Efficient retrieval and organization
    - Performance optimization for long-horizon tasks
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Initialize components
        self.consolidator = MemoryConsolidator(config)
        self.retriever = MemoryRetriever(config)
        self.efficiency_optimizer = EfficiencyOptimizer(config)
        
        # Memory storage
        self.memory_items = {}  # Full memory storage
        self.consolidated_insights = {}  # Consolidated high-value insights
        self.interaction_count = 0
        
        self.logger = logging.getLogger("MemoryManager")
        self.logger.info("MEM1 memory framework initialized")
    
    async def process(self, content: str, context: Dict[str, Any]) -> ProcessingResult:
        """Process content through memory systems"""
        start_time = asyncio.get_event_loop().time()
        
        # Store new memory
        memory_id = await self.store_memory(
            f"memory_{len(self.memory_items)}", 
            content, 
            priority=1.0
        )
        
        # Retrieve relevant memories
        retrieval_result = await self.retrieve_relevant_memories(content, context)
        
        # Check if consolidation is needed
        if self.interaction_count % self.config.consolidation_frequency == 0:
            consolidation_result = await self.consolidate_memory()
        else:
            consolidation_result = None
        
        processing_time = asyncio.get_event_loop().time() - start_time
        self._record_processing(processing_time)
        
        return ProcessingResult(
            content=f"Memory processing completed. Retrieved {len(retrieval_result.memories)} relevant memories.",
            confidence=retrieval_result.average_relevance,
            processing_time=processing_time,
            metadata={
                "memory_id": memory_id,
                "memories_retrieved": len(retrieval_result.memories),
                "consolidation_performed": consolidation_result is not None
            },
            reasoning_trace=[{
                "step": "memory_processing",
                "retrieval": retrieval_result.__dict__,
                "consolidation": consolidation_result.__dict__ if consolidation_result else None
            }]
        )
    
    async def retrieve_relevant_memories(
        self, 
        query: str, 
        context: Dict[str, Any], 
        max_results: int = 5
    ) -> RetrievalResult:
        """Retrieve memories relevant to the query using MEM1 principles"""
        self.logger.debug(f"Retrieving memories for query: {query[:50]}...")
        
        relevant_memories = await self.retriever.retrieve_memories(
            query, context, self.memory_items, max_results
        )
        
        # Update access statistics
        for memory in relevant_memories:
            memory.access_count += 1
            memory.last_accessed = time.time()
        
        # Calculate retrieval metrics
        if relevant_memories:
            relevance_scores = [
                self._calculate_relevance(memory.content, query) 
                for memory in relevant_memories
            ]
            average_relevance = sum(relevance_scores) / len(relevance_scores)
        else:
            average_relevance = 0.0
        
        efficiency_score = await self.efficiency_optimizer.calculate_retrieval_efficiency(
            len(relevant_memories), len(self.memory_items)
        )
        
        return RetrievalResult(
            memories=relevant_memories,
            average_relevance=average_relevance,
            retrieval_efficiency=efficiency_score
        )
    
    async def consolidate_experience(
        self, 
        query: str, 
        result: str, 
        context: Dict[str, Any]
    ) -> ConsolidationResult:
        """Consolidate experience using MEM1 reasoning-driven approach"""
        self.logger.debug("Consolidating experience with reasoning-driven approach")
        
        # Store the experience
        experience_memory = MemoryItem(
            id=f"experience_{len(self.memory_items)}",
            content=f"Query: {query}\nResult: {result}",
            context=context,
            reasoning_value=0.8,  # High value for complete experiences
            timestamp=time.time()
        )
        
        self.memory_items[experience_memory.id] = experience_memory
        
        # Perform consolidation
        return await self.consolidate_memory()
    
    async def consolidate_memory(self) -> ConsolidationResult:
        """Perform MEM1-style memory consolidation"""
        self.logger.info("Performing MEM1 memory consolidation...")
        
        consolidation_result = await self.consolidator.consolidate_memories(
            self.memory_items, self.config.efficiency_target
        )
        
        # Update memory storage based on consolidation
        self.memory_items = consolidation_result["updated_memories"]
        self.consolidated_insights.update(consolidation_result["insights"])
        
        self.consolidation_count += 1
        
        return ConsolidationResult(
            insights=list(consolidation_result["insights"].values()),
            efficiency_score=consolidation_result["efficiency_score"],
            memories_consolidated=consolidation_result["memories_consolidated"],
            memories_pruned=consolidation_result["memories_pruned"]
        )
    
    async def store_memory(self, key: str, content: Any, priority: float = 1.0):
        """Store content in memory with reasoning value assessment"""
        reasoning_value = await self._assess_reasoning_value(content, priority)
        
        memory_item = MemoryItem(
            id=key,
            content=str(content),
            context={},
            reasoning_value=reasoning_value,
            timestamp=time.time()
        )
        
        self.memory_items[key] = memory_item
        self.interaction_count += 1
        
        # Check memory budget
        if len(self.memory_items) > self.config.memory_budget:
            await self._enforce_memory_budget()
        
        return key
    
    def retrieve_memory(self, query: str, max_results: int = 5) -> List[Any]:
        """Synchronous memory retrieval"""
        try:
            result = asyncio.run(
                self.retrieve_relevant_memories(query, {}, max_results)
            )
            return [memory.content for memory in result.memories]
        except:
            return []
    
    async def _assess_reasoning_value(self, content: str, base_priority: float) -> float:
        """Assess the reasoning value of content using MEM1 principles"""
        content_str = str(content)
        
        # Factors that increase reasoning value
        reasoning_indicators = [
            "analysis", "conclusion", "insight", "pattern", "relationship",
            "because", "therefore", "thus", "consequently", "implies"
        ]
        
        # Count reasoning indicators
        indicator_count = sum(1 for indicator in reasoning_indicators 
                            if indicator.lower() in content_str.lower())
        
        # Length factor (more substantial content has higher value)
        length_factor = min(1.0, len(content_str) / 500)  # Normalize to 500 chars
        
        # Recency factor (newer memories start with higher value)
        recency_factor = 1.0  # Full value for new memories
        
        # Calculate combined reasoning value
        reasoning_value = base_priority * (
            0.4 * (indicator_count / len(reasoning_indicators)) +  # Reasoning density
            0.3 * length_factor +  # Content substantiality
            0.3 * recency_factor   # Temporal relevance
        )
        
        return min(1.0, reasoning_value)  # Cap at 1.0
    
    async def _enforce_memory_budget(self):
        """Enforce memory budget by removing low-value memories"""
        if len(self.memory_items) <= self.config.memory_budget:
            return
        
        # Sort memories by reasoning value (ascending)
        sorted_memories = sorted(
            self.memory_items.items(),
            key=lambda x: x[1].reasoning_value
        )
        
        # Remove lowest-value memories to fit budget
        memories_to_remove = len(self.memory_items) - self.config.memory_budget
        
        for i in range(memories_to_remove):
            memory_id, _ = sorted_memories[i]
            del self.memory_items[memory_id]
        
        self.logger.info(f"Removed {memories_to_remove} low-value memories to fit budget")
    
    def _calculate_relevance(self, memory_content: str, query: str) -> float:
        """Calculate relevance score between memory and query"""
        # Simple token-based relevance
        memory_tokens = set(memory_content.lower().split())
        query_tokens = set(query.lower().split())
        
        if not memory_tokens or not query_tokens:
            return 0.0
        
        intersection = len(memory_tokens.intersection(query_tokens))
        union = len(memory_tokens.union(query_tokens))
        
        return intersection / union if union > 0 else 0.0
    
    def get_memory_state(self) -> Dict[str, Any]:
        """Get comprehensive memory state"""
        return {
            "memory_count": len(self.memory_items),
            "consolidated_insights": len(self.consolidated_insights),
            "consolidation_count": self.consolidation_count,
            "interaction_count": self.interaction_count,
            "memory_efficiency": self._calculate_memory_efficiency(),
            "top_memories": self._get_top_memories(),
            "memory_budget_utilization": len(self.memory_items) / self.config.memory_budget
        }
    
    def reset(self):
        """Reset memory manager state"""
        self.memory_items = {}
        self.consolidated_insights = {}
        self.consolidation_count = 0
        self.interaction_count = 0
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.last_processing_time = 0.0
        
        self.logger.info("Memory manager state reset")