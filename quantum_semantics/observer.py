"""
Observer Manager - Quantum Observer Effects
============================================

Manages observer contexts and their effects on semantic interpretations
based on quantum semantic principles.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class Observer:
    """Represents an observer context"""
    id: str
    perspective: str
    influence_strength: float
    focus_areas: List[str]

class ObserverManager:
    """Manages observer effects on semantic interpretations"""
    
    def __init__(self, config):
        self.config = config
        self.active_observers = []
        self._initialize_default_observers()
        
    def _initialize_default_observers(self):
        """Initialize default observer contexts"""
        default_observers = [
            Observer(
                id="analytical",
                perspective="analytical_reasoning",
                influence_strength=0.8,
                focus_areas=["logic", "structure", "analysis"]
            ),
            Observer(
                id="contextual", 
                perspective="contextual_interpretation",
                influence_strength=0.7,
                focus_areas=["context", "relationships", "environment"]
            ),
            Observer(
                id="creative",
                perspective="creative_synthesis", 
                influence_strength=0.6,
                focus_areas=["innovation", "synthesis", "emergence"]
            ),
            Observer(
                id="practical",
                perspective="practical_application",
                influence_strength=0.9,
                focus_areas=["application", "utility", "implementation"]
            )
        ]
        
        # Add observers based on configuration
        for observer_id in self.config.observer_contexts:
            matching_observer = next((o for o in default_observers if o.id == observer_id), None)
            if matching_observer:
                self.active_observers.append(matching_observer)
        
        # Ensure at least one observer is active
        if not self.active_observers:
            self.active_observers.append(default_observers[0])  # Default to analytical
    
    async def apply_observer_effects(
        self, 
        superposition: Dict[str, Any], 
        observer_contexts: List[str]
    ) -> Dict[str, Any]:
        """Apply observer effects to semantic superposition"""
        
        observed_superposition = superposition.copy()
        
        # Apply each active observer's influence
        for observer in self.active_observers:
            if observer.id in observer_contexts or "all" in observer_contexts:
                observed_superposition = await self._apply_single_observer_effect(
                    observed_superposition, observer
                )
        
        return observed_superposition
    
    async def _apply_single_observer_effect(
        self, 
        superposition: Dict[str, Any], 
        observer: Observer
    ) -> Dict[str, Any]:
        """Apply a single observer's effect on the superposition"""
        
        # Modify interpretations based on observer's perspective
        modified_interpretations = []
        
        for interpretation in superposition.get("interpretations", []):
            # Calculate observer resonance with interpretation
            resonance = self._calculate_observer_resonance(interpretation, observer)
            
            # Modify interpretation probability based on observer influence
            modified_probability = interpretation["probability"] * (
                1.0 + (resonance * observer.influence_strength - 0.5)
            )
            modified_probability = max(0.0, min(1.0, modified_probability))  # Clamp to [0,1]
            
            # Create observer-influenced interpretation
            modified_interpretation = interpretation.copy()
            modified_interpretation["probability"] = modified_probability
            modified_interpretation["observer_influence"] = observer.id
            modified_interpretation["resonance"] = resonance
            
            modified_interpretations.append(modified_interpretation)
        
        # Renormalize probabilities
        total_probability = sum(interp["probability"] for interp in modified_interpretations)
        if total_probability > 0:
            for interp in modified_interpretations:
                interp["probability"] /= total_probability
        
        # Update superposition with observer effects
        observed_superposition = superposition.copy()
        observed_superposition["interpretations"] = modified_interpretations
        observed_superposition["observer_applied"] = observer.id
        
        return observed_superposition
    
    def _calculate_observer_resonance(
        self, 
        interpretation: Dict[str, Any], 
        observer: Observer
    ) -> float:
        """Calculate resonance between interpretation and observer"""
        
        interpretation_text = interpretation.get("text", "").lower()
        
        # Calculate focus area matches
        focus_matches = 0
        for focus_area in observer.focus_areas:
            if focus_area.lower() in interpretation_text:
                focus_matches += 1
        
        # Base resonance from focus area alignment
        focus_resonance = focus_matches / len(observer.focus_areas) if observer.focus_areas else 0.0
        
        # Perspective alignment (simplified keyword matching)
        perspective_keywords = observer.perspective.split("_")
        perspective_matches = sum(1 for keyword in perspective_keywords if keyword in interpretation_text)
        perspective_resonance = perspective_matches / len(perspective_keywords)
        
        # Combined resonance
        overall_resonance = (focus_resonance * 0.6) + (perspective_resonance * 0.4)
        
        return overall_resonance
    
    def add_observer(self, observer: Observer):
        """Add a custom observer"""
        self.active_observers.append(observer)
    
    def remove_observer(self, observer_id: str):
        """Remove an observer by ID"""
        self.active_observers = [obs for obs in self.active_observers if obs.id != observer_id]
    
    def get_active_observers(self) -> List[Observer]:
        """Get list of active observers"""
        return self.active_observers.copy()
    
    def reset(self):
        """Reset observer manager state"""
        self.active_observers = []
        self._initialize_default_observers()