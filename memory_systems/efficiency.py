"""
Efficiency Optimizer - MEM1 Efficiency Optimization
===================================================

Optimizes memory system efficiency based on MEM1 principles
for resource utilization and performance optimization.
"""

import asyncio
import time
import math
from typing import Dict, List, Any, Optional

class EfficiencyOptimizer:
    """Optimizes memory system efficiency using MEM1 principles"""
    
    def __init__(self, config):
        self.config = config
        self.efficiency_history = []  # Track efficiency over time
        self.optimization_metrics = {}
    
    async def calculate_retrieval_efficiency(
        self, 
        retrieved_count: int, 
        total_memories: int
    ) -> float:
        """Calculate efficiency of memory retrieval"""
        if total_memories == 0:
            return 1.0
        
        # Base efficiency: lower retrieval ratio is more efficient
        retrieval_ratio = retrieved_count / total_memories
        base_efficiency = 1.0 - min(0.9, retrieval_ratio)
        
        # Bonus for targeted retrieval (not too many, not too few)
        optimal_range = (0.05, 0.2)  # 5-20% of memories retrieved is optimal
        
        if optimal_range[0] <= retrieval_ratio <= optimal_range[1]:
            targeting_bonus = 0.2
        else:
            # Penalty for being outside optimal range
            if retrieval_ratio < optimal_range[0]:
                targeting_bonus = -0.1 * (optimal_range[0] - retrieval_ratio) / optimal_range[0]
            else:
                targeting_bonus = -0.1 * (retrieval_ratio - optimal_range[1]) / (1.0 - optimal_range[1])
        
        efficiency = min(1.0, base_efficiency + targeting_bonus)
        
        # Record efficiency metric
        self.efficiency_history.append({
            "timestamp": time.time(),
            "retrieval_efficiency": efficiency,
            "retrieved_count": retrieved_count,
            "total_memories": total_memories
        })
        
        return efficiency
    
    async def optimize_memory_allocation(
        self, 
        memory_items: Dict[str, Any], 
        target_efficiency: float
    ) -> Dict[str, Any]:
        """Optimize memory allocation for target efficiency"""
        current_metrics = await self._calculate_current_metrics(memory_items)
        
        optimization_recommendations = {
            "current_efficiency": current_metrics["efficiency"],
            "target_efficiency": target_efficiency,
            "recommendations": []
        }
        
        # Memory count optimization
        if current_metrics["efficiency"] < target_efficiency:
            memory_count_rec = await self._optimize_memory_count(
                memory_items, target_efficiency
            )
            optimization_recommendations["recommendations"].append(memory_count_rec)
        
        # Memory quality optimization
        quality_rec = await self._optimize_memory_quality(memory_items)
        optimization_recommendations["recommendations"].append(quality_rec)
        
        # Access pattern optimization
        access_rec = await self._optimize_access_patterns(memory_items)
        optimization_recommendations["recommendations"].append(access_rec)
        
        return optimization_recommendations
    
    async def _calculate_current_metrics(self, memory_items: Dict[str, Any]) -> Dict[str, float]:
        """Calculate current memory system metrics"""
        if not memory_items:
            return {"efficiency": 1.0, "quality": 1.0, "utilization": 0.0}
        
        # Calculate memory quality (average reasoning value)
        total_reasoning_value = sum(memory.reasoning_value for memory in memory_items.values())
        average_quality = total_reasoning_value / len(memory_items)
        
        # Calculate utilization (against budget)
        utilization = len(memory_items) / self.config.memory_budget
        
        # Calculate overall efficiency
        efficiency = self._calculate_overall_efficiency(average_quality, utilization)
        
        return {
            "efficiency": efficiency,
            "quality": average_quality,
            "utilization": utilization
        }
    
    def _calculate_overall_efficiency(self, quality: float, utilization: float) -> float:
        """Calculate overall memory system efficiency"""
        # Efficiency combines quality and utilization
        # High quality with optimal utilization = high efficiency
        
        # Optimal utilization is around 70-80% of budget
        optimal_utilization = 0.75
        utilization_efficiency = 1.0 - abs(utilization - optimal_utilization)
        
        # Combined efficiency
        overall_efficiency = (quality * 0.6) + (utilization_efficiency * 0.4)
        
        return min(1.0, max(0.0, overall_efficiency))
    
    async def _optimize_memory_count(
        self, 
        memory_items: Dict[str, Any], 
        target_efficiency: float
    ) -> Dict[str, Any]:
        """Optimize memory count for target efficiency"""
        current_count = len(memory_items)
        
        # Calculate optimal count based on quality distribution
        memory_values = [memory.reasoning_value for memory in memory_items.values()]
        memory_values.sort(reverse=True)
        
        # Find optimal count that maintains target efficiency
        optimal_count = current_count
        
        for count in range(int(current_count * 0.5), current_count):
            if count == 0:
                continue
                
            # Calculate efficiency with top 'count' memories
            top_memories_value = sum(memory_values[:count]) / count
            utilization = count / self.config.memory_budget
            
            efficiency = self._calculate_overall_efficiency(top_memories_value, utilization)
            
            if efficiency >= target_efficiency:
                optimal_count = count
                break
        
        return {
            "type": "memory_count_optimization",
            "current_count": current_count,
            "optimal_count": optimal_count,
            "reduction_needed": max(0, current_count - optimal_count),
            "efficiency_gain": self._estimate_efficiency_gain(current_count, optimal_count)
        }
    
    async def _optimize_memory_quality(self, memory_items: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize memory quality through consolidation and enhancement"""
        if not memory_items:
            return {"type": "memory_quality_optimization", "recommendations": []}
        
        # Identify low-quality memories
        low_quality_memories = [
            memory_id for memory_id, memory in memory_items.items()
            if memory.reasoning_value < 0.3
        ]
        
        # Identify high-quality memories
        high_quality_memories = [
            memory_id for memory_id, memory in memory_items.items()
            if memory.reasoning_value > 0.8
        ]
        
        recommendations = []
        
        if low_quality_memories:
            recommendations.append(
                f"Consider consolidating or removing {len(low_quality_memories)} low-quality memories"
            )
        
        if high_quality_memories:
            recommendations.append(
                f"Preserve and potentially expand {len(high_quality_memories)} high-quality memories"
            )
        
        # Quality improvement strategies
        quality_strategies = await self._generate_quality_strategies(memory_items)
        recommendations.extend(quality_strategies)
        
        return {
            "type": "memory_quality_optimization",
            "low_quality_count": len(low_quality_memories),
            "high_quality_count": len(high_quality_memories),
            "recommendations": recommendations
        }
    
    async def _optimize_access_patterns(self, memory_items: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize memory access patterns for efficiency"""
        if not memory_items:
            return {"type": "access_pattern_optimization", "insights": []}
        
        # Analyze access patterns
        access_stats = {
            "frequently_accessed": [],
            "rarely_accessed": [],
            "never_accessed": []
        }
        
        for memory_id, memory in memory_items.items():
            if memory.access_count == 0:
                access_stats["never_accessed"].append(memory_id)
            elif memory.access_count < 2:
                access_stats["rarely_accessed"].append(memory_id)
            else:
                access_stats["frequently_accessed"].append(memory_id)
        
        insights = []
        
        if access_stats["never_accessed"]:
            insights.append(
                f"{len(access_stats['never_accessed'])} memories never accessed - candidates for removal"
            )
        
        if access_stats["frequently_accessed"]:
            insights.append(
                f"{len(access_stats['frequently_accessed'])} memories frequently accessed - ensure retention"
            )
        
        # Access pattern recommendations
        pattern_recommendations = await self._generate_access_recommendations(access_stats)
        insights.extend(pattern_recommendations)
        
        return {
            "type": "access_pattern_optimization",
            "access_distribution": {k: len(v) for k, v in access_stats.items()},
            "insights": insights
        }
    
    async def _generate_quality_strategies(self, memory_items: Dict[str, Any]) -> List[str]:
        """Generate strategies for improving memory quality"""
        strategies = []
        
        # Analyze reasoning value distribution
        reasoning_values = [memory.reasoning_value for memory in memory_items.values()]
        avg_quality = sum(reasoning_values) / len(reasoning_values)
        
        if avg_quality < 0.5:
            strategies.append("Overall memory quality is low - increase consolidation frequency")
        
        if max(reasoning_values) - min(reasoning_values) > 0.7:
            strategies.append("High quality variance - consider selective retention strategies")
        
        # Content-based strategies
        content_lengths = [len(memory.content) for memory in memory_items.values()]
        avg_length = sum(content_lengths) / len(content_lengths)
        
        if avg_length < 50:
            strategies.append("Memories are very short - consider content enrichment")
        elif avg_length > 500:
            strategies.append("Memories are very long - consider content summarization")
        
        return strategies
    
    async def _generate_access_recommendations(self, access_stats: Dict[str, List]) -> List[str]:
        """Generate recommendations based on access patterns"""
        recommendations = []
        
        total_memories = sum(len(memories) for memories in access_stats.values())
        
        if len(access_stats["never_accessed"]) > total_memories * 0.3:
            recommendations.append(
                "High proportion of unused memories - review retention criteria"
            )
        
        if len(access_stats["frequently_accessed"]) < total_memories * 0.1:
            recommendations.append(
                "Few frequently accessed memories - improve retrieval targeting"
            )
        
        return recommendations
    
    def _estimate_efficiency_gain(self, current_count: int, optimal_count: int) -> float:
        """Estimate efficiency gain from count optimization"""
        if current_count == 0:
            return 0.0
        
        reduction_ratio = (current_count - optimal_count) / current_count
        return min(0.3, reduction_ratio * 0.5)  # Cap at 30% gain
    
    def get_efficiency_metrics(self) -> Dict[str, Any]:
        """Get comprehensive efficiency metrics"""
        if not self.efficiency_history:
            return {"no_data": True}
        
        recent_efficiency = self.efficiency_history[-10:]  # Last 10 measurements
        
        return {
            "recent_average_efficiency": sum(e["retrieval_efficiency"] for e in recent_efficiency) / len(recent_efficiency),
            "total_measurements": len(self.efficiency_history),
            "trend": self._calculate_efficiency_trend(),
            "optimization_opportunities": self._identify_optimization_opportunities()
        }
    
    def _calculate_efficiency_trend(self) -> str:
        """Calculate efficiency trend over time"""
        if len(self.efficiency_history) < 2:
            return "insufficient_data"
        
        recent = self.efficiency_history[-5:]
        older = self.efficiency_history[-10:-5] if len(self.efficiency_history) >= 10 else self.efficiency_history[:-5]
        
        if not older:
            return "insufficient_data"
        
        recent_avg = sum(e["retrieval_efficiency"] for e in recent) / len(recent)
        older_avg = sum(e["retrieval_efficiency"] for e in older) / len(older)
        
        if recent_avg > older_avg + 0.05:
            return "improving"
        elif recent_avg < older_avg - 0.05:
            return "declining"
        else:
            return "stable"
    
    def _identify_optimization_opportunities(self) -> List[str]:
        """Identify optimization opportunities"""
        opportunities = []
        
        if not self.efficiency_history:
            return opportunities
        
        recent_efficiency = [e["retrieval_efficiency"] for e in self.efficiency_history[-10:]]
        avg_efficiency = sum(recent_efficiency) / len(recent_efficiency)
        
        if avg_efficiency < 0.7:
            opportunities.append("retrieval_efficiency_low")
        
        if len(set(recent_efficiency)) == 1:
            opportunities.append("efficiency_stagnant")
        
        return opportunities