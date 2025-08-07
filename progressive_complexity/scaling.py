"""
Complexity Scaler - Dynamic Complexity Scaling
==============================================

Handles dynamic scaling between different complexity levels
with resource management and transition optimization.
"""

import asyncio
from typing import Dict, List, Any, Optional

class ComplexityScaler:
    """Handles scaling between different complexity levels"""
    
    def __init__(self, config):
        self.config = config
        self.scaling_history = []
        self.transition_costs = self._initialize_transition_costs()
        
    def _initialize_transition_costs(self) -> Dict[str, Dict[str, float]]:
        """Initialize transition costs between complexity levels"""
        levels = ["atom", "molecule", "cell", "organ", "neural_system", "neural_field"]
        transition_costs = {}
        
        for i, from_level in enumerate(levels):
            transition_costs[from_level] = {}
            for j, to_level in enumerate(levels):
                if i == j:
                    # No cost for staying at same level
                    transition_costs[from_level][to_level] = 0.0
                else:
                    # Cost increases with distance between levels
                    distance = abs(i - j)
                    base_cost = 0.1 * distance
                    
                    # Scaling up is more expensive than scaling down
                    if j > i:  # Scaling up
                        transition_costs[from_level][to_level] = base_cost * 1.5
                    else:  # Scaling down
                        transition_costs[from_level][to_level] = base_cost * 0.8
        
        return transition_costs
    
    async def scale_to_complexity(
        self, 
        current_level: str, 
        target_level: str
    ) -> Dict[str, Any]:
        """Scale from current to target complexity level"""
        
        if current_level == target_level:
            return {
                "success": True,
                "transition_type": "none",
                "cost": 0.0,
                "message": "Already at target complexity level"
            }
        
        # Calculate transition cost
        transition_cost = self.transition_costs.get(current_level, {}).get(target_level, 1.0)
        
        # Determine scaling strategy
        scaling_strategy = self._determine_scaling_strategy(current_level, target_level)
        
        # Perform scaling based on strategy
        scaling_result = await self._execute_scaling(
            current_level, target_level, scaling_strategy, transition_cost
        )
        
        # Record scaling operation
        self.scaling_history.append({
            "from_level": current_level,
            "to_level": target_level,
            "strategy": scaling_strategy,
            "cost": transition_cost,
            "success": scaling_result["success"]
        })
        
        return scaling_result
    
    def _determine_scaling_strategy(self, current_level: str, target_level: str) -> str:
        """Determine optimal scaling strategy"""
        
        level_hierarchy = ["atom", "molecule", "cell", "organ", "neural_system", "neural_field"]
        
        current_index = level_hierarchy.index(current_level) if current_level in level_hierarchy else 3
        target_index = level_hierarchy.index(target_level) if target_level in level_hierarchy else 3
        
        if target_index > current_index:
            # Scaling up
            distance = target_index - current_index
            if distance == 1:
                return "incremental_scale_up"
            elif distance == 2:
                return "moderate_scale_up"
            else:
                return "aggressive_scale_up"
        
        elif target_index < current_index:
            # Scaling down
            distance = current_index - target_index
            if distance == 1:
                return "incremental_scale_down"
            elif distance == 2:
                return "moderate_scale_down"
            else:
                return "aggressive_scale_down"
        
        else:
            return "maintain_level"
    
    async def _execute_scaling(
        self, 
        current_level: str, 
        target_level: str, 
        strategy: str, 
        cost: float
    ) -> Dict[str, Any]:
        """Execute the scaling operation"""
        
        # Check if scaling is permitted based on config
        if not self.config.auto_scaling and cost > 0.5:
            return {
                "success": False,
                "error": "Auto-scaling disabled for high-cost transitions",
                "transition_type": strategy,
                "cost": cost
            }
        
        # Simulate scaling process based on strategy
        if "scale_up" in strategy:
            return await self._scale_up_process(current_level, target_level, strategy, cost)
        elif "scale_down" in strategy:
            return await self._scale_down_process(current_level, target_level, strategy, cost)
        else:
            return {
                "success": True,
                "transition_type": strategy,
                "cost": cost,
                "message": "Level maintained"
            }
    
    async def _scale_up_process(
        self, 
        current_level: str, 
        target_level: str, 
        strategy: str, 
        cost: float
    ) -> Dict[str, Any]:
        """Handle scaling up to higher complexity"""
        
        # Simulate resource allocation for higher complexity
        resource_requirements = self._calculate_scale_up_resources(current_level, target_level)
        
        # Check resource availability (simplified)
        if resource_requirements["cognitive_resources"] > 64:  # Max threshold
            return {
                "success": False,
                "error": "Insufficient cognitive resources for target complexity",
                "transition_type": strategy,
                "cost": cost,
                "resource_requirements": resource_requirements
            }
        
        # Successful scaling up
        return {
            "success": True,
            "transition_type": strategy,
            "cost": cost,
            "message": f"Successfully scaled up from {current_level} to {target_level}",
            "resource_requirements": resource_requirements,
            "optimization_applied": self._get_scale_up_optimizations(strategy)
        }
    
    async def _scale_down_process(
        self, 
        current_level: str, 
        target_level: str, 
        strategy: str, 
        cost: float
    ) -> Dict[str, Any]:
        """Handle scaling down to lower complexity"""
        
        # Calculate resource savings from scaling down
        resource_savings = self._calculate_scale_down_savings(current_level, target_level)
        
        # Successful scaling down
        return {
            "success": True,
            "transition_type": strategy,
            "cost": cost,
            "message": f"Successfully scaled down from {current_level} to {target_level}",
            "resource_savings": resource_savings,
            "optimization_applied": self._get_scale_down_optimizations(strategy)
        }
    
    def _calculate_scale_up_resources(self, current_level: str, target_level: str) -> Dict[str, float]:
        """Calculate resource requirements for scaling up"""
        
        # Simplified resource calculation based on level complexity
        level_multipliers = {
            "atom": 1, "molecule": 2, "cell": 4, 
            "organ": 8, "neural_system": 16, "neural_field": 32
        }
        
        current_resources = level_multipliers.get(current_level, 4)
        target_resources = level_multipliers.get(target_level, 4)
        
        return {
            "cognitive_resources": target_resources,
            "memory_requirements": target_resources * 0.5,
            "processing_power": target_resources * 0.8,
            "resource_increase": target_resources - current_resources
        }
    
    def _calculate_scale_down_savings(self, current_level: str, target_level: str) -> Dict[str, float]:
        """Calculate resource savings from scaling down"""
        
        level_multipliers = {
            "atom": 1, "molecule": 2, "cell": 4,
            "organ": 8, "neural_system": 16, "neural_field": 32
        }
        
        current_resources = level_multipliers.get(current_level, 4)
        target_resources = level_multipliers.get(target_level, 4)
        
        return {
            "cognitive_resources_saved": current_resources - target_resources,
            "memory_freed": (current_resources - target_resources) * 0.5,
            "processing_power_saved": (current_resources - target_resources) * 0.8,
            "efficiency_gain": 0.1 * (current_resources - target_resources)
        }
    
    def _get_scale_up_optimizations(self, strategy: str) -> List[str]:
        """Get optimizations applied during scale up"""
        optimizations = ["resource_preallocation", "gradual_complexity_increase"]
        
        if "aggressive" in strategy:
            optimizations.extend(["parallel_scaling", "resource_caching"])
        elif "moderate" in strategy:
            optimizations.append("intermediate_validation")
        
        return optimizations
    
    def _get_scale_down_optimizations(self, strategy: str) -> List[str]:
        """Get optimizations applied during scale down"""
        optimizations = ["resource_deallocation", "state_preservation"]
        
        if "aggressive" in strategy:
            optimizations.extend(["rapid_simplification", "context_compression"])
        elif "moderate" in strategy:
            optimizations.append("gradual_reduction")
        
        return optimizations
    
    def get_scaling_metrics(self) -> Dict[str, Any]:
        """Get scaling performance metrics"""
        if not self.scaling_history:
            return {"no_scaling_data": True}
        
        successful_scalings = [s for s in self.scaling_history if s["success"]]
        failed_scalings = [s for s in self.scaling_history if not s["success"]]
        
        return {
            "total_scalings": len(self.scaling_history),
            "successful_scalings": len(successful_scalings),
            "failed_scalings": len(failed_scalings),
            "success_rate": len(successful_scalings) / len(self.scaling_history),
            "average_cost": sum(s["cost"] for s in self.scaling_history) / len(self.scaling_history),
            "most_common_strategy": self._get_most_common_strategy(),
            "scaling_patterns": self._analyze_scaling_patterns()
        }
    
    def _get_most_common_strategy(self) -> str:
        """Get the most commonly used scaling strategy"""
        if not self.scaling_history:
            return "none"
        
        strategy_counts = {}
        for scaling in self.scaling_history:
            strategy = scaling["strategy"]
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return max(strategy_counts.items(), key=lambda x: x[1])[0] if strategy_counts else "none"
    
    def _analyze_scaling_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in scaling behavior"""
        if not self.scaling_history:
            return {}
        
        patterns = {
            "scale_up_frequency": len([s for s in self.scaling_history if "up" in s["strategy"]]),
            "scale_down_frequency": len([s for s in self.scaling_history if "down" in s["strategy"]]),
            "most_expensive_transition": max(self.scaling_history, key=lambda x: x["cost"]),
            "least_expensive_transition": min(self.scaling_history, key=lambda x: x["cost"])
        }
        
        return patterns
    
    def reset(self):
        """Reset complexity scaler state"""
        self.scaling_history = []