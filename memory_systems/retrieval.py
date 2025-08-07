"""
Memory Retrieval - Efficient Memory Retrieval System
====================================================

Implements efficient memory retrieval based on MEM1 principles
with relevance ranking and context-aware selection.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

class MemoryRetriever:
    """Retrieves memories efficiently based on relevance and context"""
    
    def __init__(self, config):
        self.config = config
    
    async def retrieve_memories(
        self, 
        query: str, 
        context: Dict[str, Any], 
        memory_items: Dict[str, Any], 
        max_results: int = 5
    ) -> List[Any]:
        """Retrieve most relevant memories for a query"""
        
        if not memory_items:
            return []
        
        # Calculate relevance scores for all memories
        scored_memories = []
        
        for memory_id, memory in memory_items.items():
            relevance_score = await self._calculate_comprehensive_relevance(
                query, context, memory
            )
            
            scored_memories.append((memory, relevance_score))
        
        # Sort by relevance score (descending)
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        # Apply filtering and selection
        filtered_memories = await self._apply_retrieval_filters(
            scored_memories, query, context
        )
        
        # Return top results
        return [memory for memory, _ in filtered_memories[:max_results]]
    
    async def _calculate_comprehensive_relevance(
        self, 
        query: str, 
        context: Dict[str, Any], 
        memory
    ) -> float:
        """Calculate comprehensive relevance score"""
        
        # Base semantic similarity
        semantic_relevance = self._calculate_semantic_similarity(query, memory.content)
        
        # Context relevance
        context_relevance = await self._calculate_context_relevance(context, memory)
        
        # Reasoning value boost
        reasoning_boost = memory.reasoning_value * 0.2
        
        # Recency factor
        recency_factor = self._calculate_recency_factor(memory)
        
        # Access frequency factor
        frequency_factor = self._calculate_frequency_factor(memory)
        
        # Combined relevance score
        comprehensive_relevance = (
            semantic_relevance * 0.4 +      # Primary: semantic match
            context_relevance * 0.25 +      # Secondary: context alignment
            reasoning_boost +               # Boost: high reasoning value
            recency_factor * 0.15 +         # Recency: recent memories
            frequency_factor * 0.1          # Frequency: often accessed
        )
        
        return min(1.0, comprehensive_relevance)  # Cap at 1.0
    
    def _calculate_semantic_similarity(self, query: str, content: str) -> float:
        """Calculate semantic similarity between query and content"""
        # Token-based similarity
        query_tokens = set(query.lower().split())
        content_tokens = set(content.lower().split())
        
        if not query_tokens or not content_tokens:
            return 0.0
        
        # Jaccard similarity
        intersection = len(query_tokens.intersection(content_tokens))
        union = len(query_tokens.union(content_tokens))
        
        jaccard = intersection / union if union > 0 else 0.0
        
        # Enhanced similarity for important terms
        important_terms = [token for token in query_tokens if len(token) > 4]
        important_matches = sum(1 for term in important_terms if term in content_tokens)
        
        if important_terms:
            importance_boost = important_matches / len(important_terms) * 0.3
        else:
            importance_boost = 0.0
        
        return min(1.0, jaccard + importance_boost)
    
    async def _calculate_context_relevance(
        self, 
        context: Dict[str, Any], 
        memory
    ) -> float:
        """Calculate relevance based on context alignment"""
        if not context:
            return 0.0
        
        relevance_score = 0.0
        context_factors = 0
        
        # Check for context overlap
        memory_context = getattr(memory, 'context', {})
        
        for key, value in context.items():
            context_factors += 1
            
            if key in memory_context:
                if memory_context[key] == value:
                    relevance_score += 1.0  # Exact match
                elif str(value).lower() in str(memory_context[key]).lower():
                    relevance_score += 0.5  # Partial match
        
        return relevance_score / context_factors if context_factors > 0 else 0.0
    
    def _calculate_recency_factor(self, memory) -> float:
        """Calculate recency factor for memory"""
        current_time = time.time()
        memory_age = current_time - memory.timestamp
        
        # Decay factor: more recent memories get higher scores
        # Memories older than 24 hours start to decay
        decay_threshold = 24 * 3600  # 24 hours in seconds
        
        if memory_age < decay_threshold:
            return 1.0
        else:
            # Exponential decay after threshold
            decay_rate = 0.1
            decay_factor = math.exp(-decay_rate * (memory_age - decay_threshold) / 3600)
            return max(0.1, decay_factor)  # Minimum 0.1
    
    def _calculate_frequency_factor(self, memory) -> float:
        """Calculate frequency factor based on access count"""
        # Normalize access count to 0-1 range
        max_expected_accesses = 10  # Assume 10 is high frequency
        normalized_frequency = min(1.0, memory.access_count / max_expected_accesses)
        
        # Apply logarithmic scaling to prevent over-emphasis
        import math
        if memory.access_count > 0:
            return math.log(1 + normalized_frequency * math.e) / math.log(1 + math.e)
        else:
            return 0.0
    
    async def _apply_retrieval_filters(
        self, 
        scored_memories: List[tuple], 
        query: str, 
        context: Dict[str, Any]
    ) -> List[tuple]:
        """Apply filters to retrieved memories"""
        filtered_memories = []
        
        # Filter 1: Minimum relevance threshold
        min_relevance = 0.1
        for memory, score in scored_memories:
            if score >= min_relevance:
                filtered_memories.append((memory, score))
        
        # Filter 2: Diversity filter - avoid too similar memories
        diverse_memories = await self._apply_diversity_filter(filtered_memories)
        
        # Filter 3: Context-specific filters
        context_filtered = await self._apply_context_filters(
            diverse_memories, query, context
        )
        
        return context_filtered
    
    async def _apply_diversity_filter(
        self, 
        memories: List[tuple], 
        similarity_threshold: float = 0.8
    ) -> List[tuple]:
        """Filter out very similar memories to ensure diversity"""
        if len(memories) <= 1:
            return memories
        
        diverse_memories = []
        
        for memory, score in memories:
            is_diverse = True
            
            # Check similarity with already selected memories
            for selected_memory, _ in diverse_memories:
                similarity = self._calculate_semantic_similarity(
                    memory.content, selected_memory.content
                )
                
                if similarity > similarity_threshold:
                    is_diverse = False
                    break
            
            if is_diverse:
                diverse_memories.append((memory, score))
        
        return diverse_memories
    
    async def _apply_context_filters(
        self, 
        memories: List[tuple], 
        query: str, 
        context: Dict[str, Any]
    ) -> List[tuple]:
        """Apply context-specific filtering"""
        # For now, return all memories
        # Could add domain-specific filters, temporal filters, etc.
        return memories

import math  # Add this import at the top