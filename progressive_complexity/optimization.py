"""
Complexity Optimizer - Performance-Based Optimization
=====================================================

Optimizes complexity scaling strategies based on performance
history and efficiency metrics.
"""

import asyncio
from typing import Dict, List, Any, Optional

class ComplexityOptimizer:
    """Optimizes complexity strategies based on performance data"""
    
    def __init__(self, config):
        self.config = config
        self.optimization_history = []
        
    async def optimize_strategy(self, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize complexity strategy based on performance history"""
        
        if len(performance_history) < 5:
            return {
                "optimization": "insufficient_data",
                "recommendations": [],
                "current_performance": self._analyze_current_performance(performance_history)
            }
        
        # Analyze performance patterns
        performance_analysis = await self._analyze_performance_patterns(performance_history)
        
        # Generate optimization recommendations
        recommendations = await self._generate_optimization_recommendations(
            performance_analysis, performance_history
        )
        
        # Calculate optimization impact
        optimization_impact = await self._calculate_optimization_impact(
            recommendations, performance_history
        )
        
        optimization_result = {
            "optimization": "completed",
            "performance_analysis": performance_analysis,
            "recommendations": recommendations,
            "optimization_impact": optimization_impact,
            "implementation_priority": self._prioritize_recommendations(recommendations)
        }
        
        # Record optimization
        self.optimization_history.append({
            "timestamp": asyncio.get_event_loop().time(),
            "performance_records_analyzed": len(performance_history),
            "recommendations_generated": len(recommendations),
            "optimization_result": optimization_result
        })
        
        return optimization_result
    
    async def _analyze_performance_patterns(
        self, 
        performance_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze patterns in performance history"""
        
        analysis = {
            "efficiency_trends": self._analyze_efficiency_trends(performance_history),
            "complexity_usage_patterns": self._analyze_complexity_usage(performance_history),
            "resource_utilization_patterns": self._analyze_resource_utilization(performance_history),
            "scaling_effectiveness": self._analyze_scaling_effectiveness(performance_history)
        }
        
        return analysis
    
    def _analyze_efficiency_trends(self, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze efficiency trends over time"""
        
        efficiencies = [record["efficiency"] for record in performance_history]
        
        if len(efficiencies) < 3:
            return {"trend": "insufficient_data"}
        
        # Calculate trend
        recent_efficiency = sum(efficiencies[-5:]) / len(efficiencies[-5:])
        older_efficiency = sum(efficiencies[:-5]) / len(efficiencies[:-5])
        
        trend_direction = "improving" if recent_efficiency > older_efficiency else "declining"
        trend_magnitude = abs(recent_efficiency - older_efficiency)
        
        return {
            "trend": trend_direction,
            "magnitude": trend_magnitude,
            "current_efficiency": recent_efficiency,
            "baseline_efficiency": older_efficiency,
            "efficiency_variance": self._calculate_variance(efficiencies)
        }
    
    def _analyze_complexity_usage(self, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how different complexity levels are being used"""
        
        complexity_usage = {}
        complexity_performance = {}
        
        for record in performance_history:
            complexity = record.get("actual_complexity", "unknown")
            efficiency = record.get("efficiency", 0.0)
            
            if complexity not in complexity_usage:
                complexity_usage[complexity] = 0
                complexity_performance[complexity] = []
            
            complexity_usage[complexity] += 1
            complexity_performance[complexity].append(efficiency)
        
        # Calculate average performance per complexity level
        complexity_avg_performance = {}
        for complexity, performances in complexity_performance.items():
            complexity_avg_performance[complexity] = sum(performances) / len(performances)
        
        # Find optimal and suboptimal complexity levels
        if complexity_avg_performance:
            optimal_complexity = max(complexity_avg_performance.items(), key=lambda x: x[1])
            suboptimal_complexities = [
                (k, v) for k, v in complexity_avg_performance.items() 
                if v < optimal_complexity[1] * 0.8
            ]
        else:
            optimal_complexity = ("unknown", 0.0)
            suboptimal_complexities = []
        
        return {
            "usage_distribution": complexity_usage,
            "average_performance": complexity_avg_performance,
            "optimal_complexity": optimal_complexity,
            "suboptimal_complexities": suboptimal_complexities,
            "complexity_diversity": len(complexity_usage)
        }
    
    def _analyze_resource_utilization(self, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze resource utilization patterns"""
        
        resource_utilizations = [record.get("resource_utilization", 0.5) for record in performance_history]
        
        avg_utilization = sum(resource_utilizations) / len(resource_utilizations)
        max_utilization = max(resource_utilizations)
        min_utilization = min(resource_utilizations)
        
        # Categorize utilization efficiency
        if avg_utilization < 0.3:
            utilization_category = "under_utilized"
        elif avg_utilization > 0.9:
            utilization_category = "over_utilized"
        elif 0.6 <= avg_utilization <= 0.8:
            utilization_category = "optimal"
        else:
            utilization_category = "moderate"
        
        return {
            "average_utilization": avg_utilization,
            "utilization_range": (min_utilization, max_utilization),
            "utilization_category": utilization_category,
            "utilization_variance": self._calculate_variance(resource_utilizations),
            "optimization_potential": max(0, 0.75 - avg_utilization)  # Target 75% utilization
        }
    
    def _analyze_scaling_effectiveness(self, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze effectiveness of complexity scaling decisions"""
        
        scaling_decisions = []
        
        for i in range(1, len(performance_history)):
            prev_record = performance_history[i-1]
            curr_record = performance_history[i]
            
            prev_complexity = prev_record.get("actual_complexity")
            curr_complexity = curr_record.get("actual_complexity")
            
            if prev_complexity != curr_complexity:
                # Scaling occurred
                efficiency_change = curr_record["efficiency"] - prev_record["efficiency"]
                scaling_decisions.append({
                    "from_complexity": prev_complexity,
                    "to_complexity": curr_complexity,
                    "efficiency_change": efficiency_change,
                    "was_beneficial": efficiency_change > 0
                })
        
        if not scaling_decisions:
            return {"scaling_frequency": 0, "analysis": "no_scaling_observed"}
        
        beneficial_scalings = [s for s in scaling_decisions if s["was_beneficial"]]
        avg_efficiency_change = sum(s["efficiency_change"] for s in scaling_decisions) / len(scaling_decisions)
        
        return {
            "scaling_frequency": len(scaling_decisions),
            "beneficial_scalings": len(beneficial_scalings),
            "scaling_success_rate": len(beneficial_scalings) / len(scaling_decisions),
            "average_efficiency_change": avg_efficiency_change,
            "scaling_decisions": scaling_decisions[-5:]  # Last 5 scaling decisions
        }
    
    async def _generate_optimization_recommendations(
        self, 
        performance_analysis: Dict[str, Any], 
        performance_history: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate specific optimization recommendations"""
        
        recommendations = []
        
        # Efficiency-based recommendations
        efficiency_trends = performance_analysis["efficiency_trends"]
        if efficiency_trends["trend"] == "declining":
            recommendations.append({
                "type": "efficiency_improvement",
                "priority": "high",
                "recommendation": "Implement efficiency monitoring and adaptive complexity adjustment",
                "rationale": f"Efficiency declining by {efficiency_trends['magnitude']:.2f}",
                "implementation": "Enable more aggressive scaling down when efficiency drops"
            })
        
        # Complexity usage recommendations
        complexity_usage = performance_analysis["complexity_usage_patterns"]
        if complexity_usage["complexity_diversity"] < 3:
            recommendations.append({
                "type": "complexity_diversification", 
                "priority": "medium",
                "recommendation": "Explore broader range of complexity levels",
                "rationale": f"Only using {complexity_usage['complexity_diversity']} complexity levels",
                "implementation": "Reduce scaling thresholds to encourage more adaptive scaling"
            })
        
        # Resource utilization recommendations
        resource_analysis = performance_analysis["resource_utilization_patterns"]
        if resource_analysis["utilization_category"] == "under_utilized":
            recommendations.append({
                "type": "resource_optimization",
                "priority": "medium", 
                "recommendation": "Increase complexity levels to better utilize available resources",
                "rationale": f"Average utilization only {resource_analysis['average_utilization']:.2f}",
                "implementation": "Lower thresholds for scaling up to higher complexity levels"
            })
        elif resource_analysis["utilization_category"] == "over_utilized":
            recommendations.append({
                "type": "resource_optimization",
                "priority": "high",
                "recommendation": "Implement more aggressive scaling down to prevent resource exhaustion",
                "rationale": f"Average utilization {resource_analysis['average_utilization']:.2f} is too high",
                "implementation": "Raise thresholds for scaling up and lower thresholds for scaling down"
            })
        
        # Scaling effectiveness recommendations
        scaling_analysis = performance_analysis["scaling_effectiveness"]
        if isinstance(scaling_analysis, dict) and scaling_analysis.get("scaling_success_rate", 0) < 0.6:
            recommendations.append({
                "type": "scaling_strategy",
                "priority": "high",
                "recommendation": "Improve scaling decision accuracy",
                "rationale": f"Scaling success rate only {scaling_analysis['scaling_success_rate']:.2f}",
                "implementation": "Enhance complexity assessment algorithms and add scaling prediction"
            })
        
        return recommendations
    
    async def _calculate_optimization_impact(
        self, 
        recommendations: List[Dict[str, Any]], 
        performance_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate potential impact of optimization recommendations"""
        
        if not recommendations or not performance_history:
            return {"impact": "minimal", "estimated_improvement": 0.0}
        
        current_efficiency = sum(r["efficiency"] for r in performance_history[-5:]) / 5
        
        # Estimate impact based on recommendation types and priorities
        total_impact = 0.0
        
        for recommendation in recommendations:
            if recommendation["priority"] == "high":
                impact = 0.15  # 15% potential improvement
            elif recommendation["priority"] == "medium":
                impact = 0.08  # 8% potential improvement
            else:
                impact = 0.03  # 3% potential improvement
            
            # Adjust impact based on recommendation type
            if recommendation["type"] == "efficiency_improvement":
                impact *= 1.2  # Efficiency improvements have higher impact
            elif recommendation["type"] == "resource_optimization":
                impact *= 1.1
            
            total_impact += impact
        
        # Cap total impact at reasonable levels
        total_impact = min(0.5, total_impact)  # Max 50% improvement
        
        estimated_new_efficiency = current_efficiency * (1 + total_impact)
        
        return {
            "impact": "significant" if total_impact > 0.2 else "moderate" if total_impact > 0.1 else "minimal",
            "estimated_improvement": total_impact,
            "current_efficiency": current_efficiency,
            "estimated_new_efficiency": estimated_new_efficiency,
            "recommendations_count": len(recommendations)
        }
    
    def _prioritize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize recommendations by impact and urgency"""
        
        # Sort by priority (high > medium > low) and type
        priority_order = {"high": 3, "medium": 2, "low": 1}
        type_priority = {
            "efficiency_improvement": 3,
            "scaling_strategy": 2, 
            "resource_optimization": 2,
            "complexity_diversification": 1
        }
        
        def recommendation_score(rec):
            priority_score = priority_order.get(rec["priority"], 0)
            type_score = type_priority.get(rec["type"], 0)
            return priority_score * 10 + type_score
        
        prioritized = sorted(recommendations, key=recommendation_score, reverse=True)
        
        return prioritized
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        
        return variance
    
    def _analyze_current_performance(self, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze current performance with limited data"""
        
        if not performance_history:
            return {"status": "no_data"}
        
        recent_record = performance_history[-1]
        
        return {
            "status": "limited_data",
            "current_efficiency": recent_record.get("efficiency", 0.0),
            "current_complexity": recent_record.get("actual_complexity", "unknown"),
            "current_utilization": recent_record.get("resource_utilization", 0.0),
            "records_available": len(performance_history)
        }
    
    def get_optimization_metrics(self) -> Dict[str, Any]:
        """Get optimization performance metrics"""
        
        if not self.optimization_history:
            return {"no_optimization_data": True}
        
        return {
            "optimizations_performed": len(self.optimization_history),
            "recent_optimization": self.optimization_history[-1] if self.optimization_history else None,
            "average_recommendations_per_optimization": sum(
                opt["recommendations_generated"] for opt in self.optimization_history
            ) / len(self.optimization_history)
        }
    
    def reset(self):
        """Reset complexity optimizer state"""
        self.optimization_history = []