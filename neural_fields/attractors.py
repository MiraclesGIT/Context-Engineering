"""
Attractor Manager - Dynamic Attractor Formation and Management
=============================================================

Manages attractor basins, formation dynamics, and stability
based on Shanghai AI Lab research on attractor dynamics.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class Attractor:
    """Represents an attractor in the neural field"""
    id: str
    pattern: str
    strength: float
    basin_width: float
    formation_time: float
    interaction_count: int = 0

class AttractorManager:
    """Manages attractor formation, evolution, and dynamics"""
    
    def __init__(self, config):
        self.config = config
        self.attractors = {}  # Attractor storage
        self.formation_history = []  # Formation timeline
        self.interaction_graph = {}  # Attractor interactions
        
    async def check_attractor_formation(
        self, 
        pattern: str, 
        strength: float, 
        threshold: float
    ) -> List[Attractor]:
        """Check if pattern should form new attractor"""
        new_attractors = []
        
        if strength > threshold:
            # Form new attractor
            attractor = Attractor(
                id=f"attractor_{len(self.attractors)}",
                pattern=pattern,
                strength=strength,
                basin_width=self.config.resonance_bandwidth,
                formation_time=time.time()
            )
            
            self.attractors[attractor.id] = attractor
            self.formation_history.append({
                "attractor_id": attractor.id,
                "formation_time": attractor.formation_time,
                "initial_strength": strength
            })
            
            new_attractors.append(attractor)
            
            # Update interaction graph
            await self._update_interaction_graph(attractor.id, pattern)
        
        return new_attractors
    
    async def find_resonant_attractors(self, content: str) -> List[Dict[str, Any]]:
        """Find attractors that resonate with given content"""
        resonant_attractors = []
        
        for attractor_id, attractor in self.attractors.items():
            resonance = self._calculate_pattern_resonance(content, attractor.pattern)
            
            if resonance > 0.3:  # Resonance threshold
                resonant_attractors.append({
                    "id": attractor_id,
                    "resonance": resonance,
                    "strength": attractor.strength,
                    "pattern": attractor.pattern[:100]  # Truncated for display
                })
        
        # Sort by resonance strength
        resonant_attractors.sort(key=lambda x: x["resonance"], reverse=True)
        
        return resonant_attractors
    
    async def update_attractors(self, result: str, context: Dict[str, Any]) -> List[str]:
        """Update attractor strengths based on new result"""
        updated_attractors = []
        
        for attractor_id, attractor in self.attractors.items():
            # Calculate resonance with result
            resonance = self._calculate_pattern_resonance(result, attractor.pattern)
            
            if resonance > 0.2:
                # Strengthen attractor
                strength_increase = resonance * 0.1
                attractor.strength += strength_increase
                attractor.interaction_count += 1
                
                updated_attractors.append(attractor_id)
        
        return updated_attractors
    
    async def apply_attractor_decay(self, decay_rate: float):
        """Apply decay to attractor strengths"""
        attractors_to_remove = []
        
        for attractor_id, attractor in self.attractors.items():
            # Apply decay
            attractor.strength *= (1 - decay_rate)
            
            # Mark weak attractors for removal
            if attractor.strength < 0.1:
                attractors_to_remove.append(attractor_id)
        
        # Remove weak attractors
        for attractor_id in attractors_to_remove:
            del self.attractors[attractor_id]
            if attractor_id in self.interaction_graph:
                del self.interaction_graph[attractor_id]
    
    async def _update_interaction_graph(self, attractor_id: str, pattern: str):
        """Update interactions between attractors"""
        self.interaction_graph[attractor_id] = {}
        
        for existing_id, existing_attractor in self.attractors.items():
            if existing_id != attractor_id:
                resonance = self._calculate_pattern_resonance(pattern, existing_attractor.pattern)
                if resonance > 0.2:
                    self.interaction_graph[attractor_id][existing_id] = resonance
    
    def _calculate_pattern_resonance(self, pattern1: str, pattern2: str) -> float:
        """Calculate resonance between two patterns"""
        # Token-based similarity
        tokens1 = set(pattern1.lower().split())
        tokens2 = set(pattern2.lower().split())
        
        if not tokens1 or not tokens2:
            return 0.0
            
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_attractors(self) -> Dict[str, Any]:
        """Get all attractors with metadata"""
        return {
            attractor_id: {
                "pattern": attractor.pattern,
                "strength": attractor.strength,
                "basin_width": attractor.basin_width,
                "formation_time": attractor.formation_time,
                "interaction_count": attractor.interaction_count,
                "age": time.time() - attractor.formation_time
            }
            for attractor_id, attractor in self.attractors.items()
        }
    
    def get_interaction_graph(self) -> Dict[str, Dict[str, float]]:
        """Get attractor interaction graph"""
        return self.interaction_graph.copy()
    
    def reset(self):
        """Reset attractor manager state"""
        self.attractors = {}
        self.formation_history = []
        self.interaction_graph = {}