"""
Neural Field Implementations - Semantic and Cognitive Fields
===========================================================

Core field implementations for semantic and cognitive processing
based on field theory and attractor dynamics.
"""

import asyncio
import math
from typing import Dict, List, Any, Optional
from collections import defaultdict

class BaseField:
    """Base class for neural fields"""
    
    def __init__(self, config, field_type: str):
        self.config = config
        self.field_type = field_type
        self.patterns = {}  # Pattern storage
        self.energy_levels = defaultdict(float)  # Energy per pattern
        self.interaction_matrix = {}  # Pattern interactions
        
    async def inject(self, pattern: str, strength: float) -> Dict[str, Any]:
        """Inject a pattern into the field"""
        # Apply boundary permeability
        effective_strength = strength * self.config.boundary_permeability
        
        # Store pattern
        pattern_id = f"{self.field_type}_{len(self.patterns)}"
        self.patterns[pattern_id] = pattern
        self.energy_levels[pattern_id] = effective_strength
        
        # Process interactions with existing patterns
        await self._process_pattern_interactions(pattern_id, pattern)
        
        return {
            "pattern_id": pattern_id,
            "effective_strength": effective_strength,
            "interactions": len(self.interaction_matrix.get(pattern_id, {}))
        }
    
    async def measure_resonance(self, content: str) -> float:
        """Measure resonance between content and field patterns"""
        if not self.patterns:
            return 0.0
            
        total_resonance = 0.0
        total_weight = 0.0
        
        for pattern_id, pattern in self.patterns.items():
            similarity = self._calculate_similarity(content, pattern)
            pattern_energy = self.energy_levels[pattern_id]
            
            total_resonance += similarity * pattern_energy
            total_weight += pattern_energy
        
        return total_resonance / total_weight if total_weight > 0 else 0.0
    
    async def apply_decay(self, decay_rate: float):
        """Apply decay to field patterns"""
        patterns_to_remove = []
        
        for pattern_id in self.patterns:
            # Apply decay
            self.energy_levels[pattern_id] *= (1 - decay_rate)
            
            # Remove patterns below threshold
            if self.energy_levels[pattern_id] < 0.01:
                patterns_to_remove.append(pattern_id)
        
        # Clean up weak patterns
        for pattern_id in patterns_to_remove:
            del self.patterns[pattern_id]
            del self.energy_levels[pattern_id]
            if pattern_id in self.interaction_matrix:
                del self.interaction_matrix[pattern_id]
    
    def calculate_energy(self) -> float:
        """Calculate total field energy"""
        return sum(self.energy_levels.values())
    
    def get_state(self) -> Dict[str, Any]:
        """Get field state"""
        return {
            "type": self.field_type,
            "patterns": dict(self.patterns),
            "energy_levels": dict(self.energy_levels),
            "total_energy": self.calculate_energy(),
            "pattern_count": len(self.patterns)
        }
    
    def reset(self):
        """Reset field state"""
        self.patterns = {}
        self.energy_levels = defaultdict(float)
        self.interaction_matrix = {}
    
    async def _process_pattern_interactions(self, pattern_id: str, pattern: str):
        """Process interactions between patterns"""
        self.interaction_matrix[pattern_id] = {}
        
        for existing_id, existing_pattern in self.patterns.items():
            if existing_id != pattern_id:
                similarity = self._calculate_similarity(pattern, existing_pattern)
                if similarity > 0.2:  # Interaction threshold
                    self.interaction_matrix[pattern_id][existing_id] = similarity
                    
                    # Strengthen both patterns through interaction
                    interaction_strength = similarity * 0.1
                    self.energy_levels[pattern_id] += interaction_strength
                    self.energy_levels[existing_id] += interaction_strength
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        # Simple token-based similarity
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        
        if not tokens1 or not tokens2:
            return 0.0
            
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0

class SemanticField(BaseField):
    """
    Semantic Field for meaning and context processing.
    
    Focuses on semantic relationships, meaning patterns,
    and conceptual resonance in the field.
    """
    
    def __init__(self, config):
        super().__init__(config, "semantic")
        self.semantic_clusters = {}  # Semantic clustering
        self.meaning_attractors = {}  # Meaning-based attractors
    
    async def inject(self, pattern: str, strength: float) -> Dict[str, Any]:
        """Inject pattern with semantic processing"""
        result = await super().inject(pattern, strength)
        
        # Process semantic clustering
        await self._update_semantic_clusters(result["pattern_id"], pattern)
        
        return result
    
    async def _update_semantic_clusters(self, pattern_id: str, pattern: str):
        """Update semantic clusters based on new pattern"""
        # Simple semantic clustering based on key terms
        key_terms = [word for word in pattern.lower().split() if len(word) > 4]
        
        for term in key_terms:
            if term not in self.semantic_clusters:
                self.semantic_clusters[term] = []
            self.semantic_clusters[term].append(pattern_id)

class CognitiveField(BaseField):
    """
    Cognitive Field for reasoning and cognitive processing.
    
    Focuses on cognitive patterns, reasoning structures,
    and thought process dynamics in the field.
    """
    
    def __init__(self, config):
        super().__init__(config, "cognitive")
        self.reasoning_patterns = {}  # Reasoning pattern storage
        self.cognitive_attractors = {}  # Cognitive attractors
    
    async def inject(self, pattern: str, strength: float) -> Dict[str, Any]:
        """Inject pattern with cognitive processing"""
        result = await super().inject(pattern, strength)
        
        # Process cognitive patterns
        await self._extract_reasoning_patterns(result["pattern_id"], pattern)
        
        return result
    
    async def _extract_reasoning_patterns(self, pattern_id: str, pattern: str):
        """Extract reasoning patterns from the content"""
        # Look for reasoning indicators
        reasoning_indicators = [
            "because", "therefore", "thus", "consequently", "as a result",
            "if", "then", "when", "since", "given that", "analysis", "conclusion"
        ]
        
        pattern_lower = pattern.lower()
        found_indicators = [ind for ind in reasoning_indicators if ind in pattern_lower]
        
        if found_indicators:
            self.reasoning_patterns[pattern_id] = {
                "indicators": found_indicators,
                "reasoning_type": self._classify_reasoning_type(found_indicators),
                "complexity": len(found_indicators)
            }
    
    def _classify_reasoning_type(self, indicators: List[str]) -> str:
        """Classify the type of reasoning based on indicators"""
        if any(ind in indicators for ind in ["if", "then", "when"]):
            return "conditional"
        elif any(ind in indicators for ind in ["because", "since", "given that"]):
            return "causal"
        elif any(ind in indicators for ind in ["therefore", "thus", "consequently"]):
            return "deductive"
        elif any(ind in indicators for ind in ["analysis", "conclusion"]):
            return "analytical"
        else:
            return "general"