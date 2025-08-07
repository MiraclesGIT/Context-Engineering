"""
Memory Consolidation - MEM1 Reasoning-Driven Consolidation
==========================================================

Implements reasoning-driven memory consolidation based on MEM1 principles
from Singapore-MIT research.
"""

import asyncio
from typing import Dict, List, Any
from collections import defaultdict

class MemoryConsolidator:
    """Consolidates memories using reasoning-driven MEM1 approach"""
    
    def __init__(self, config):
        self.config = config
    
    async def consolidate_memories(
        self, 
        memory_items: Dict[str, Any], 
        efficiency_target: float
    ) -> Dict[str, Any]:
        """Consolidate memories to improve efficiency while preserving reasoning value"""
        
        if not memory_items:
            return {
                "updated_memories": {},
                "insights": {},
                "efficiency_score": 1.0,
                "memories_consolidated": 0,
                "memories_pruned": 0
            }
        
        # Step 1: Analyze memory patterns and interactions
        memory_patterns = await self._analyze_memory_patterns(memory_items)
        
        # Step 2: Identify consolidation opportunities
        consolidation_groups = await self._identify_consolidation_groups(
            memory_items, memory_patterns
        )
        
        # Step 3: Perform selective consolidation
        consolidated_memories = await self._perform_consolidation(
            memory_items, consolidation_groups
        )
        
        # Step 4: Extract high-value insights
        insights = await self._extract_insights(consolidated_memories, memory_patterns)
        
        # Step 5: Prune low-value memories
        final_memories, pruned_count = await self._prune_low_value_memories(
            consolidated_memories, efficiency_target
        )
        
        # Calculate efficiency improvement
        efficiency_score = await self._calculate_efficiency_improvement(
            len(memory_items), len(final_memories)
        )
        
        return {
            "updated_memories": final_memories,
            "insights": insights,
            "efficiency_score": efficiency_score,
            "memories_consolidated": len(consolidation_groups),
            "memories_pruned": pruned_count
        }
    
    async def _analyze_memory_patterns(self, memory_items: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in memory interactions and content"""
        patterns = {
            "topic_clusters": defaultdict(list),
            "reasoning_chains": [],
            "temporal_patterns": [],
            "interaction_frequencies": defaultdict(int)
        }
        
        # Group memories by topic similarity
        for memory_id, memory in memory_items.items():
            key_terms = self._extract_key_terms(memory.content)
            for term in key_terms:
                patterns["topic_clusters"][term].append(memory_id)
        
        # Identify reasoning chains
        patterns["reasoning_chains"] = await self._identify_reasoning_chains(memory_items)
        
        # Analyze temporal access patterns
        patterns["temporal_patterns"] = await self._analyze_temporal_patterns(memory_items)
        
        # Track interaction frequencies
        for memory_id, memory in memory_items.items():
            patterns["interaction_frequencies"][memory_id] = memory.access_count
        
        return patterns
    
    async def _identify_consolidation_groups(
        self, 
        memory_items: Dict[str, Any], 
        patterns: Dict[str, Any]
    ) -> List[List[str]]:
        """Identify groups of memories that can be consolidated"""
        consolidation_groups = []
        processed_memories = set()
        
        # Group by topic clusters
        for topic, memory_ids in patterns["topic_clusters"].items():
            if len(memory_ids) >= 3:  # Need multiple memories to consolidate
                # Filter out already processed memories
                available_memories = [mid for mid in memory_ids if mid not in processed_memories]
                
                if len(available_memories) >= 2:
                    consolidation_groups.append(available_memories)
                    processed_memories.update(available_memories)
        
        # Group by reasoning chains
        for chain in patterns["reasoning_chains"]:
            if len(chain) >= 2:
                # Check if memories are not already grouped
                available_chain = [mid for mid in chain if mid not in processed_memories]
                if len(available_chain) >= 2:
                    consolidation_groups.append(available_chain)
                    processed_memories.update(available_chain)
        
        return consolidation_groups
    
    async def _perform_consolidation(
        self, 
        memory_items: Dict[str, Any], 
        consolidation_groups: List[List[str]]
    ) -> Dict[str, Any]:
        """Perform memory consolidation for identified groups"""
        consolidated_memories = memory_items.copy()
        
        for group in consolidation_groups:
            if len(group) < 2:
                continue
            
            # Consolidate group into a single high-value memory
            consolidated_memory = await self._consolidate_group(
                [memory_items[mid] for mid in group]
            )
            
            # Remove original memories
            for memory_id in group:
                if memory_id in consolidated_memories:
                    del consolidated_memories[memory_id]
            
            # Add consolidated memory
            consolidated_id = f"consolidated_{len(consolidated_memories)}"
            consolidated_memories[consolidated_id] = consolidated_memory
        
        return consolidated_memories
    
    async def _consolidate_group(self, memories: List[Any]) -> Any:
        """Consolidate a group of memories into a single memory"""
        # Combine content from all memories
        combined_content = []
        combined_reasoning_value = 0.0
        max_timestamp = 0.0
        total_access_count = 0
        
        for memory in memories:
            combined_content.append(memory.content)
            combined_reasoning_value += memory.reasoning_value
            max_timestamp = max(max_timestamp, memory.timestamp)
            total_access_count += memory.access_count
        
        # Create consolidated memory
        from .manager import MemoryItem  # Import here to avoid circular import
        
        consolidated_memory = MemoryItem(
            id=f"consolidated_{max_timestamp}",
            content=self._synthesize_content(combined_content),
            context={},
            reasoning_value=min(1.0, combined_reasoning_value / len(memories) * 1.2),  # Slight boost
            timestamp=max_timestamp,
            access_count=total_access_count
        )
        
        return consolidated_memory
    
    def _synthesize_content(self, content_list: List[str]) -> str:
        """Synthesize multiple content pieces into consolidated insight"""
        # Extract key points from each content
        key_points = []
        for content in content_list:
            # Simple extraction of sentences containing reasoning indicators
            sentences = content.split('.')
            for sentence in sentences:
                if any(indicator in sentence.lower() for indicator in 
                      ['analysis', 'conclusion', 'insight', 'therefore', 'because']):
                    key_points.append(sentence.strip())
        
        if not key_points:
            # Fallback: combine first sentences
            key_points = [content.split('.')[0] for content in content_list if content.strip()]
        
        # Create synthesized content
        synthesis = "CONSOLIDATED INSIGHT:\n\n"
        synthesis += "Key findings:\n"
        for i, point in enumerate(key_points[:5], 1):  # Limit to top 5 points
            synthesis += f"{i}. {point}\n"
        
        synthesis += f"\nBased on {len(content_list)} related memory items."
        
        return synthesis
    
    async def _extract_insights(
        self, 
        consolidated_memories: Dict[str, Any], 
        patterns: Dict[str, Any]
    ) -> Dict[str, str]:
        """Extract high-value insights from consolidated memories"""
        insights = {}
        
        # Extract insights from topic clusters
        for topic, memory_ids in patterns["topic_clusters"].items():
            if len(memory_ids) >= 2:
                insight = f"Pattern identified in {topic}: {len(memory_ids)} related memories suggest recurring themes in this domain."
                insights[f"topic_insight_{topic}"] = insight
        
        # Extract insights from reasoning chains
        for i, chain in enumerate(patterns["reasoning_chains"]):
            if len(chain) >= 2:
                insight = f"Reasoning chain {i+1}: {len(chain)} memories show connected logical progression."
                insights[f"chain_insight_{i}"] = insight
        
        # Extract insights from high-value consolidated memories
        for memory_id, memory in consolidated_memories.items():
            if memory.reasoning_value > 0.8:
                insight = f"High-value insight from {memory_id}: {memory.content[:100]}..."
                insights[f"memory_insight_{memory_id}"] = insight
        
        return insights
    
    async def _prune_low_value_memories(
        self, 
        memories: Dict[str, Any], 
        efficiency_target: float
    ) -> tuple:
        """Prune low-value memories to reach efficiency target"""
        current_efficiency = self._calculate_current_efficiency(memories)
        
        if current_efficiency >= efficiency_target:
            return memories, 0
        
        # Sort memories by reasoning value (ascending)
        sorted_memories = sorted(
            memories.items(),
            key=lambda x: x[1].reasoning_value
        )
        
        target_count = int(len(memories) * efficiency_target)
        pruned_count = len(memories) - target_count
        
        # Keep highest-value memories
        kept_memories = dict(sorted_memories[-target_count:]) if target_count > 0 else {}
        
        return kept_memories, pruned_count
    
    def _calculate_current_efficiency(self, memories: Dict[str, Any]) -> float:
        """Calculate current memory efficiency"""
        if not memories:
            return 1.0
        
        # Efficiency based on average reasoning value
        total_value = sum(memory.reasoning_value for memory in memories.values())
        return total_value / len(memories)
    
    async def _calculate_efficiency_improvement(self, original_count: int, final_count: int) -> float:
        """Calculate efficiency improvement from consolidation"""
        if original_count == 0:
            return 1.0
        
        reduction_ratio = (original_count - final_count) / original_count
        return min(1.0, 0.5 + reduction_ratio)  # Base efficiency + improvement
    
    def _extract_key_terms(self, content: str) -> List[str]:
        """Extract key terms from content"""
        # Simple keyword extraction
        words = content.lower().split()
        # Filter out common words and keep meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        key_terms = [word for word in words if len(word) > 3 and word not in stop_words]
        return key_terms[:10]  # Return top 10 terms
    
    async def _identify_reasoning_chains(self, memory_items: Dict[str, Any]) -> List[List[str]]:
        """Identify chains of related reasoning memories"""
        chains = []
        
        # Simple approach: group memories with similar reasoning indicators
        reasoning_groups = defaultdict(list)
        
        for memory_id, memory in memory_items.items():
            reasoning_type = self._classify_reasoning_type(memory.content)
            reasoning_groups[reasoning_type].append(memory_id)
        
        # Convert groups to chains if they have multiple items
        for reasoning_type, memory_ids in reasoning_groups.items():
            if len(memory_ids) >= 2:
                chains.append(memory_ids)
        
        return chains
    
    def _classify_reasoning_type(self, content: str) -> str:
        """Classify the type of reasoning in content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['analysis', 'analyze']):
            return 'analytical'
        elif any(word in content_lower for word in ['conclusion', 'therefore', 'thus']):
            return 'deductive'  
        elif any(word in content_lower for word in ['because', 'since', 'cause']):
            return 'causal'
        elif any(word in content_lower for word in ['pattern', 'trend', 'relationship']):
            return 'pattern_recognition'
        else:
            return 'general'
    
    async def _analyze_temporal_patterns(self, memory_items: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze temporal access patterns"""
        patterns = []
        
        # Group memories by time periods
        time_groups = defaultdict(list)
        
        for memory_id, memory in memory_items.items():
            time_period = int(memory.timestamp // 3600)  # Group by hour
            time_groups[time_period].append(memory_id)
        
        # Identify patterns in temporal groupings
        for time_period, memory_ids in time_groups.items():
            if len(memory_ids) >= 2:
                patterns.append({
                    "time_period": time_period,
                    "memory_count": len(memory_ids),
                    "memory_ids": memory_ids
                })
        
        return patterns