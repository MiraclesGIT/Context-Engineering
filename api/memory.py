"""
Memory API - Memory System Interface
====================================

API interface for memory management operations including storage,
retrieval, consolidation, and memory state management.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .context import APIResponse
from ..memory_systems import MemoryManager
from ..core.config import MemoryConfig
from ..utils.logger import ContextualLogger
from ..utils.validation import ValidationUtils

class MemoryAPI:
    """
    API interface for memory system operations.
    
    Provides access to MEM1 framework capabilities including
    memory storage, retrieval, and consolidation operations.
    """
    
    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.memory_manager = MemoryManager(self.config)
        self.logger = ContextualLogger("MemoryAPI")
        
        self.logger.info("Memory API initialized")
    
    async def store_memory(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        priority: float = 1.0
    ) -> APIResponse:
        """Store content in memory system."""
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(content)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid content: {'; '.join(content_errors)}"
                )
            
            if not 0.0 <= priority <= 1.0:
                return APIResponse(
                    success=False,
                    error="Priority must be between 0.0 and 1.0"
                )
            
            # Store in memory
            memory_id = await self.memory_manager.store_memory(
                f"user_memory_{asyncio.get_event_loop().time()}",
                content,
                priority
            )
            
            return APIResponse(
                success=True,
                data={
                    "memory_id": memory_id,
                    "content_preview": content[:100] + "..." if len(content) > 100 else content,
                    "priority": priority,
                    "context": context
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error storing memory: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Memory storage error: {str(e)}"
            )
    
    async def retrieve_memories(
        self,
        query: str,
        max_results: int = 5,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Retrieve relevant memories based on query."""
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(query)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid query: {'; '.join(content_errors)}"
                )
            
            if max_results <= 0 or max_results > 50:
                return APIResponse(
                    success=False,
                    error="max_results must be between 1 and 50"
                )
            
            # Retrieve memories
            retrieval_result = await self.memory_manager.retrieve_relevant_memories(
                query, context or {}, max_results
            )
            
            # Format memories for API response
            formatted_memories = []
            for memory in retrieval_result.memories:
                formatted_memories.append({
                    "id": memory.id,
                    "content": memory.content,
                    "reasoning_value": memory.reasoning_value,
                    "timestamp": memory.timestamp,
                    "access_count": memory.access_count,
                    "relevance": self._calculate_relevance(memory.content, query)
                })
            
            return APIResponse(
                success=True,
                data={
                    "memories": formatted_memories,
                    "retrieval_stats": {
                        "total_retrieved": len(formatted_memories),
                        "average_relevance": retrieval_result.average_relevance,
                        "retrieval_efficiency": retrieval_result.retrieval_efficiency
                    },
                    "query": query,
                    "max_results": max_results
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error retrieving memories: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Memory retrieval error: {str(e)}"
            )
    
    async def consolidate_memories(self) -> APIResponse:
        """Trigger memory consolidation process."""
        try:
            consolidation_result = await self.memory_manager.consolidate_memory()
            
            return APIResponse(
                success=True,
                data={
                    "consolidation_results": {
                        "insights_extracted": len(consolidation_result.insights),
                        "insights": consolidation_result.insights,
                        "efficiency_score": consolidation_result.efficiency_score,
                        "memories_consolidated": consolidation_result.memories_consolidated,
                        "memories_pruned": consolidation_result.memories_pruned
                    },
                    "memory_state_after": self.memory_manager.get_memory_state()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error consolidating memories: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Memory consolidation error: {str(e)}"
            )
    
    async def get_memory_state(self) -> APIResponse:
        """Get current memory system state."""
        try:
            memory_state = self.memory_manager.get_memory_state()
            
            return APIResponse(
                success=True,
                data={
                    "memory_state": memory_state,
                    "memory_budget": {
                        "current_usage": memory_state["memory_count"],
                        "budget_limit": self.config.memory_budget,
                        "utilization": memory_state["memory_budget_utilization"]
                    },
                    "efficiency_metrics": {
                        "current_efficiency": memory_state["memory_efficiency"],
                        "target_efficiency": self.config.efficiency_target
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting memory state: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Memory state error: {str(e)}"
            )
    
    async def get_memory_analytics(self) -> APIResponse:
        """Get memory system analytics and insights."""
        try:
            memory_state = self.memory_manager.get_memory_state()
            
            # Calculate additional analytics
            analytics = {
                "memory_distribution": self._analyze_memory_distribution(),
                "access_patterns": self._analyze_access_patterns(),
                "consolidation_history": {
                    "consolidations_performed": memory_state["consolidation_count"],
                    "total_interactions": memory_state.get("interaction_count", 0)
                },
                "efficiency_trends": self._analyze_efficiency_trends(),
                "recommendations": self._generate_memory_recommendations(memory_state)
            }
            
            return APIResponse(
                success=True,
                data={
                    "analytics": analytics,
                    "memory_state": memory_state
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting memory analytics: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Memory analytics error: {str(e)}"
            )
    
    async def clear_memories(
        self,
        criteria: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Clear memories based on criteria."""
        try:
            if criteria is None:
                # Clear all memories
                cleared_count = len(self.memory_manager.memory_items)
                self.memory_manager.reset()
                
                return APIResponse(
                    success=True,
                    data={
                        "cleared_memories": cleared_count,
                        "criteria": "all_memories"
                    }
                )
            else:
                # Clear memories based on criteria (implement specific logic)
                return APIResponse(
                    success=False,
                    error="Selective memory clearing not yet implemented"
                )
                
        except Exception as e:
            self.logger.error(f"Error clearing memories: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Memory clearing error: {str(e)}"
            )
    
    def _calculate_relevance(self, memory_content: str, query: str) -> float:
        """Calculate relevance score between memory and query."""
        # Simple token-based relevance
        memory_tokens = set(memory_content.lower().split())
        query_tokens = set(query.lower().split())
        
        if not memory_tokens or not query_tokens:
            return 0.0
        
        intersection = len(memory_tokens.intersection(query_tokens))
        union = len(memory_tokens.union(query_tokens))
        
        return intersection / union if union > 0 else 0.0
    
    def _analyze_memory_distribution(self) -> Dict[str, Any]:
        """Analyze distribution of memories."""
        if not hasattr(self.memory_manager, 'memory_items'):
            return {"no_memories": True}
        
        memories = self.memory_manager.memory_items
        
        if not memories:
            return {"empty_memory": True}
        
        # Analyze reasoning values distribution
        reasoning_values = [memory.reasoning_value for memory in memories.values()]
        
        return {
            "total_memories": len(memories),
            "reasoning_value_stats": {
                "average": sum(reasoning_values) / len(reasoning_values),
                "min": min(reasoning_values),
                "max": max(reasoning_values)
            },
            "high_value_memories": len([rv for rv in reasoning_values if rv > 0.8]),
            "low_value_memories": len([rv for rv in reasoning_values if rv < 0.3])
        }
    
    def _analyze_access_patterns(self) -> Dict[str, Any]:
        """Analyze memory access patterns."""
        if not hasattr(self.memory_manager, 'memory_items'):
            return {"no_data": True}
        
        memories = self.memory_manager.memory_items
        
        if not memories:
            return {"empty_memory": True}
        
        access_counts = [memory.access_count for memory in memories.values()]
        
        return {
            "total_accesses": sum(access_counts),
            "average_accesses": sum(access_counts) / len(access_counts),
            "never_accessed": len([ac for ac in access_counts if ac == 0]),
            "frequently_accessed": len([ac for ac in access_counts if ac > 5])
        }
    
    def _analyze_efficiency_trends(self) -> Dict[str, Any]:
        """Analyze memory efficiency trends."""
        # Simplified efficiency analysis
        current_efficiency = self.memory_manager._calculate_memory_efficiency()
        
        return {
            "current_efficiency": current_efficiency,
            "target_efficiency": self.config.efficiency_target,
            "efficiency_gap": self.config.efficiency_target - current_efficiency,
            "trend": "stable"  # Could be enhanced with historical data
        }
    
    def _generate_memory_recommendations(self, memory_state: Dict[str, Any]) -> List[str]:
        """Generate memory management recommendations."""
        recommendations = []
        
        utilization = memory_state.get("memory_budget_utilization", 0)
        efficiency = memory_state.get("memory_efficiency", 0)
        
        if utilization > 0.9:
            recommendations.append("Memory budget nearly full - consider increasing budget or consolidating memories")
        
        if efficiency < self.config.efficiency_target:
            recommendations.append("Memory efficiency below target - trigger consolidation")
        
        if memory_state.get("consolidation_count", 0) == 0:
            recommendations.append("No consolidations performed - consider triggering first consolidation")
        
        return recommendations
    
    # Synchronous wrapper methods
    def store_memory_sync(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        priority: float = 1.0
    ) -> APIResponse:
        """Synchronous version of store_memory."""
        return asyncio.run(self.store_memory(content, context, priority))
    
    def retrieve_memories_sync(
        self,
        query: str,
        max_results: int = 5,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Synchronous version of retrieve_memories."""
        return asyncio.run(self.retrieve_memories(query, max_results, context))