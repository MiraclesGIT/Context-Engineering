"""
Fields API - Neural Field Interface
===================================

API interface for neural field operations including field injection,
resonance measurement, and attractor management.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .context import APIResponse
from ..neural_fields import NeuralFieldManager
from ..core.config import NeuralFieldsConfig
from ..utils.logger import ContextualLogger
from ..utils.validation import ValidationUtils

class FieldAPI:
    """
    API interface for neural field operations.
    
    Provides access to neural field dynamics, pattern injection,
    resonance measurement, and attractor management.
    """
    
    def __init__(self, config: Optional[NeuralFieldsConfig] = None):
        self.config = config or NeuralFieldsConfig()
        self.neural_fields = NeuralFieldManager(self.config)
        self.logger = ContextualLogger("FieldAPI")
        
        self.logger.info("Field API initialized")
    
    async def inject_pattern(
        self,
        pattern: str,
        strength: float = 1.0,
        field_type: str = "both"
    ) -> APIResponse:
        """Inject a pattern into neural fields."""
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(pattern)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid pattern: {'; '.join(content_errors)}"
                )
            
            if not 0.0 <= strength <= 2.0:
                return APIResponse(
                    success=False,
                    error="Strength must be between 0.0 and 2.0"
                )
            
            # Inject pattern
            injection_result = await self.neural_fields.inject_pattern(pattern, strength)
            
            return APIResponse(
                success=True,
                data={
                    "injection_result": {
                        "pattern_id": injection_result.pattern_id,
                        "field_energy": injection_result.field_energy,
                        "attractors_formed": injection_result.attractors_formed,
                        "resonance_score": injection_result.resonance_score
                    },
                    "field_state_after": self.neural_fields.get_field_state(),
                    "pattern_preview": pattern[:100] + "..." if len(pattern) > 100 else pattern,
                    "injection_strength": strength
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error injecting pattern: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Pattern injection error: {str(e)}"
            )
    
    async def measure_resonance(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Measure field resonance with content."""
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(content)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid content: {'; '.join(content_errors)}"
                )
            
            # Measure resonance
            resonance_result = await self.neural_fields.measure_field_resonance(
                content, context or {}
            )
            
            return APIResponse(
                success=True,
                data={
                    "resonance_measurement": {
                        "resonance_score": resonance_result.resonance_score,
                        "matching_attractors": resonance_result.matching_attractors,
                        "field_coherence": resonance_result.field_coherence,
                        "stability_measure": resonance_result.stability_measure
                    },
                    "content_preview": content[:100] + "..." if len(content) > 100 else content,
                    "context_provided": bool(context),
                    "field_state": self.neural_fields.get_field_state()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error measuring resonance: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Resonance measurement error: {str(e)}"
            )
    
    async def get_field_state(self) -> APIResponse:
        """Get current neural field state."""
        try:
            field_state = self.neural_fields.get_field_state()
            
            # Validate field state
            state_valid, state_errors = ValidationUtils.validate_field_state(field_state)
            if not state_valid:
                self.logger.warning(f"Invalid field state detected: {state_errors}")
            
            return APIResponse(
                success=True,
                data={
                    "field_state": field_state,
                    "field_summary": {
                        "total_patterns": len(field_state.get("semantic_field", {}).get("patterns", {})) + 
                                        len(field_state.get("cognitive_field", {}).get("patterns", {})),
                        "total_attractors": len(field_state.get("attractors", {})),
                        "field_energy": field_state.get("field_energy", 0),
                        "stability": field_state.get("stability", 0),
                        "resonance_bandwidth": field_state.get("resonance_bandwidth", 0)
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting field state: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Field state error: {str(e)}"
            )
    
    async def get_attractors(self) -> APIResponse:
        """Get current field attractors."""
        try:
            attractors = self.neural_fields.attractor_manager.get_attractors()
            interaction_graph = self.neural_fields.attractor_manager.get_interaction_graph()
            
            # Format attractors for API response
            formatted_attractors = []
            for attractor_id, attractor_data in attractors.items():
                formatted_attractors.append({
                    "id": attractor_id,
                    "pattern_preview": attractor_data["pattern"][:100] + "..." if len(attractor_data["pattern"]) > 100 else attractor_data["pattern"],
                    "strength": attractor_data["strength"],
                    "basin_width": attractor_data["basin_width"],
                    "formation_time": attractor_data["formation_time"],
                    "interaction_count": attractor_data["interaction_count"],
                    "age": attractor_data["age"]
                })
            
            return APIResponse(
                success=True,
                data={
                    "attractors": formatted_attractors,
                    "attractor_summary": {
                        "total_attractors": len(formatted_attractors),
                        "average_strength": sum(a["strength"] for a in formatted_attractors) / len(formatted_attractors) if formatted_attractors else 0,
                        "strongest_attractor": max(formatted_attractors, key=lambda x: x["strength"]) if formatted_attractors else None,
                        "interaction_connections": len(interaction_graph)
                    },
                    "interaction_graph": interaction_graph
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting attractors: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Attractors error: {str(e)}"
            )
    
    async def apply_field_decay(self, decay_rate: Optional[float] = None) -> APIResponse:
        """Apply decay to field patterns."""
        try:
            if decay_rate is None:
                decay_rate = self.config.decay_rate
            
            if not 0.0 <= decay_rate <= 1.0:
                return APIResponse(
                    success=False,
                    error="Decay rate must be between 0.0 and 1.0"
                )
            
            # Get state before decay
            state_before = self.neural_fields.get_field_state()
            patterns_before = len(state_before.get("semantic_field", {}).get("patterns", {})) + \
                            len(state_before.get("cognitive_field", {}).get("patterns", {}))
            energy_before = state_before.get("field_energy", 0)
            
            # Apply decay
            await self.neural_fields.apply_field_decay()
            
            # Get state after decay
            state_after = self.neural_fields.get_field_state()
            patterns_after = len(state_after.get("semantic_field", {}).get("patterns", {})) + \
                           len(state_after.get("cognitive_field", {}).get("patterns", {}))
            energy_after = state_after.get("field_energy", 0)
            
            return APIResponse(
                success=True,
                data={
                    "decay_applied": {
                        "decay_rate": decay_rate,
                        "patterns_before": patterns_before,
                        "patterns_after": patterns_after,
                        "patterns_removed": patterns_before - patterns_after,
                        "energy_before": energy_before,
                        "energy_after": energy_after,
                        "energy_lost": energy_before - energy_after
                    },
                    "field_state_after": state_after
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error applying field decay: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Field decay error: {str(e)}"
            )
    
    async def reset_fields(self) -> APIResponse:
        """Reset neural fields to initial state."""
        try:
            # Get state before reset for reporting
            state_before = self.neural_fields.get_field_state()
            
            # Reset fields
            self.neural_fields.reset()
            
            return APIResponse(
                success=True,
                data={
                    "reset_completed": True,
                    "state_before_reset": {
                        "total_patterns": len(state_before.get("semantic_field", {}).get("patterns", {})) + 
                                        len(state_before.get("cognitive_field", {}).get("patterns", {})),
                        "total_attractors": len(state_before.get("attractors", {})),
                        "field_energy": state_before.get("field_energy", 0)
                    },
                    "state_after_reset": self.neural_fields.get_field_state()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error resetting fields: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Field reset error: {str(e)}"
            )
    
    async def get_field_analytics(self) -> APIResponse:
        """Get field analytics and insights."""
        try:
            field_state = self.neural_fields.get_field_state()
            
            # Calculate analytics
            analytics = {
                "field_health": self._analyze_field_health(field_state),
                "pattern_distribution": self._analyze_pattern_distribution(field_state),
                "attractor_analysis": self._analyze_attractors(field_state),
                "resonance_patterns": self._analyze_resonance_patterns(),
                "field_evolution": self._analyze_field_evolution()
            }
            
            return APIResponse(
                success=True,
                data={
                    "analytics": analytics,
                    "field_state": field_state,
                    "recommendations": self._generate_field_recommendations(analytics)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting field analytics: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Field analytics error: {str(e)}"
            )
    
    def _analyze_field_health(self, field_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall field health."""
        energy = field_state.get("field_energy", 0)
        stability = field_state.get("stability", 0)
        attractor_count = len(field_state.get("attractors", {}))
        
        # Health score based on energy, stability, and attractor presence
        health_score = (
            min(1.0, energy / 10.0) * 0.4 +  # Energy contribution
            stability * 0.4 +  # Stability contribution
            min(1.0, attractor_count / 5.0) * 0.2  # Attractor contribution
        )
        
        if health_score > 0.8:
            health_status = "excellent"
        elif health_score > 0.6:
            health_status = "good"
        elif health_score > 0.4:
            health_status = "fair"
        else:
            health_status = "poor"
        
        return {
            "health_score": health_score,
            "health_status": health_status,
            "energy_level": energy,
            "stability_level": stability,
            "attractor_count": attractor_count
        }
    
    def _analyze_pattern_distribution(self, field_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze pattern distribution across fields."""
        semantic_patterns = len(field_state.get("semantic_field", {}).get("patterns", {}))
        cognitive_patterns = len(field_state.get("cognitive_field", {}).get("patterns", {}))
        total_patterns = semantic_patterns + cognitive_patterns
        
        return {
            "total_patterns": total_patterns,
            "semantic_patterns": semantic_patterns,
            "cognitive_patterns": cognitive_patterns,
            "semantic_ratio": semantic_patterns / total_patterns if total_patterns > 0 else 0,
            "cognitive_ratio": cognitive_patterns / total_patterns if total_patterns > 0 else 0,
            "distribution_balance": abs(0.5 - (semantic_patterns / total_patterns)) < 0.2 if total_patterns > 0 else True
        }
    
    def _analyze_attractors(self, field_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze attractor characteristics."""
        attractors = field_state.get("attractors", {})
        
        if not attractors:
            return {"no_attractors": True}
        
        strengths = []
        ages = []
        
        for attractor_data in attractors.values():
            if isinstance(attractor_data, dict):
                strengths.append(attractor_data.get("strength", 0))
                ages.append(attractor_data.get("age", 0))
        
        return {
            "total_attractors": len(attractors),
            "strength_stats": {
                "average": sum(strengths) / len(strengths) if strengths else 0,
                "max": max(strengths) if strengths else 0,
                "min": min(strengths) if strengths else 0
            },
            "age_stats": {
                "average": sum(ages) / len(ages) if ages else 0,
                "oldest": max(ages) if ages else 0,
                "newest": min(ages) if ages else 0
            }
        }
    
    def _analyze_resonance_patterns(self) -> Dict[str, Any]:
        """Analyze resonance patterns (simplified)."""
        # This would require historical resonance data
        return {
            "analysis": "resonance_history_not_available",
            "recommendation": "implement_resonance_tracking"
        }
    
    def _analyze_field_evolution(self) -> Dict[str, Any]:
        """Analyze field evolution over time (simplified)."""
        # This would require historical field state data
        return {
            "analysis": "evolution_history_not_available",
            "recommendation": "implement_field_history_tracking"
        }
    
    def _generate_field_recommendations(self, analytics: Dict[str, Any]) -> List[str]:
        """Generate field management recommendations."""
        recommendations = []
        
        health = analytics.get("field_health", {})
        if health.get("health_score", 0) < 0.5:
            recommendations.append("Field health is low - consider pattern injection or reducing decay rate")
        
        pattern_dist = analytics.get("pattern_distribution", {})
        if not pattern_dist.get("distribution_balance", True):
            recommendations.append("Pattern distribution is imbalanced - inject patterns into underrepresented field")
        
        attractor_analysis = analytics.get("attractor_analysis", {})
        if attractor_analysis.get("no_attractors"):
            recommendations.append("No attractors present - inject strong patterns to form attractors")
        elif attractor_analysis.get("total_attractors", 0) > self.config.max_attractors:
            recommendations.append("Too many attractors - consider applying decay or consolidation")
        
        return recommendations
    
    # Synchronous wrapper methods
    def inject_pattern_sync(
        self,
        pattern: str,
        strength: float = 1.0,
        field_type: str = "both"
    ) -> APIResponse:
        """Synchronous version of inject_pattern."""
        return asyncio.run(self.inject_pattern(pattern, strength, field_type))
    
    def measure_resonance_sync(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Synchronous version of measure_resonance."""
        return asyncio.run(self.measure_resonance(content, context))