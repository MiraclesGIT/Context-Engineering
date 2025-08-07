"""
Resonance Processor - Field Resonance and Coherence Measurement
===============================================================

Processes field resonance patterns and measures field coherence
for neural field dynamics optimization.
"""

import asyncio
import math
from typing import Dict, List, Any, Optional

class ResonanceProcessor:
    """Processes field resonance patterns and coherence measures"""
    
    def __init__(self, config):
        self.config = config
        self.resonance_history = []  # Historical resonance measurements
        self.coherence_cache = {}  # Cached coherence calculations
    
    async def measure_pattern_resonance(
        self, 
        pattern: str, 
        field_state: Dict[str, Any]
    ) -> float:
        """Measure resonance between pattern and field state"""
        if not field_state:
            return 0.0
        
        semantic_field = field_state.get("semantic_field", {})
        cognitive_field = field_state.get("cognitive_field", {})
        
        # Calculate semantic resonance
        semantic_resonance = await self._calculate_semantic_resonance(
            pattern, semantic_field
        )
        
        # Calculate cognitive resonance  
        cognitive_resonance = await self._calculate_cognitive_resonance(
            pattern, cognitive_field
        )
        
        # Combined resonance with bandwidth modulation
        combined_resonance = (semantic_resonance + cognitive_resonance) / 2.0
        modulated_resonance = combined_resonance * self.config.resonance_bandwidth
        
        # Record measurement
        self.resonance_history.append({
            "pattern": pattern[:50],  # Truncated
            "semantic_resonance": semantic_resonance,
            "cognitive_resonance": cognitive_resonance,
            "combined_resonance": modulated_resonance,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        return modulated_resonance
    
    async def measure_field_coherence(self, field_state: Dict[str, Any]) -> float:
        """Measure overall field coherence"""
        if not field_state:
            return 0.0
        
        # Check cache
        field_hash = hash(str(field_state))
        if field_hash in self.coherence_cache:
            return self.coherence_cache[field_hash]
        
        coherence_components = []
        
        # Semantic field coherence
        semantic_field = field_state.get("semantic_field", {})
        if semantic_field:
            semantic_coherence = await self._measure_semantic_coherence(semantic_field)
            coherence_components.append(semantic_coherence)
        
        # Cognitive field coherence
        cognitive_field = field_state.get("cognitive_field", {})
        if cognitive_field:
            cognitive_coherence = await self._measure_cognitive_coherence(cognitive_field)
            coherence_components.append(cognitive_coherence)
        
        # Attractor coherence
        attractors = field_state.get("attractors", {})
        if attractors:
            attractor_coherence = await self._measure_attractor_coherence(attractors)
            coherence_components.append(attractor_coherence)
        
        # Combined coherence
        overall_coherence = (
            sum(coherence_components) / len(coherence_components) 
            if coherence_components else 0.0
        )
        
        # Cache result
        self.coherence_cache[field_hash] = overall_coherence
        
        return overall_coherence
    
    async def _calculate_semantic_resonance(
        self, 
        pattern: str, 
        semantic_field: Dict[str, Any]
    ) -> float:
        """Calculate resonance with semantic field"""
        patterns = semantic_field.get("patterns", {})
        energy_levels = semantic_field.get("energy_levels", {})
        
        if not patterns:
            return 0.0
        
        total_resonance = 0.0
        total_weight = 0.0
        
        for pattern_id, field_pattern in patterns.items():
            similarity = self._calculate_similarity(pattern, field_pattern)
            pattern_energy = energy_levels.get(pattern_id, 0.0)
            
            total_resonance += similarity * pattern_energy
            total_weight += pattern_energy
        
        return total_resonance / total_weight if total_weight > 0 else 0.0
    
    async def _calculate_cognitive_resonance(
        self, 
        pattern: str, 
        cognitive_field: Dict[str, Any]
    ) -> float:
        """Calculate resonance with cognitive field"""
        patterns = cognitive_field.get("patterns", {})
        energy_levels = cognitive_field.get("energy_levels", {})
        
        if not patterns:
            return 0.0
        
        # Enhanced cognitive resonance calculation
        reasoning_resonance = 0.0
        structural_resonance = 0.0
        
        pattern_tokens = set(pattern.lower().split())
        
        for pattern_id, field_pattern in patterns.items():
            field_tokens = set(field_pattern.lower().split())
            
            # Basic similarity
            similarity = self._calculate_similarity(pattern, field_pattern)
            
            # Reasoning pattern matching
            reasoning_match = self._match_reasoning_patterns(pattern, field_pattern)
            
            pattern_energy = energy_levels.get(pattern_id, 0.0)
            
            reasoning_resonance += (similarity + reasoning_match) * pattern_energy / 2.0
            structural_resonance += similarity * pattern_energy
        
        total_energy = sum(energy_levels.values())
        if total_energy == 0:
            return 0.0
            
        return (reasoning_resonance + structural_resonance) / (2.0 * total_energy)
    
    async def _measure_semantic_coherence(self, semantic_field: Dict[str, Any]) -> float:
        """Measure coherence within semantic field"""
        patterns = semantic_field.get("patterns", {})
        
        if len(patterns) < 2:
            return 1.0  # Perfect coherence for single or no patterns
        
        # Calculate pairwise similarities
        similarities = []
        pattern_list = list(patterns.values())
        
        for i in range(len(pattern_list)):
            for j in range(i + 1, len(pattern_list)):
                similarity = self._calculate_similarity(pattern_list[i], pattern_list[j])
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    async def _measure_cognitive_coherence(self, cognitive_field: Dict[str, Any]) -> float:
        """Measure coherence within cognitive field"""
        patterns = cognitive_field.get("patterns", {})
        
        if len(patterns) < 2:
            return 1.0
        
        # Enhanced coherence measurement for cognitive patterns
        reasoning_coherence = 0.0
        structural_coherence = 0.0
        
        pattern_list = list(patterns.values())
        comparison_count = 0
        
        for i in range(len(pattern_list)):
            for j in range(i + 1, len(pattern_list)):
                # Structural similarity
                structural_sim = self._calculate_similarity(pattern_list[i], pattern_list[j])
                
                # Reasoning pattern coherence
                reasoning_sim = self._match_reasoning_patterns(pattern_list[i], pattern_list[j])
                
                structural_coherence += structural_sim
                reasoning_coherence += reasoning_sim
                comparison_count += 1
        
        if comparison_count == 0:
            return 1.0
            
        avg_structural = structural_coherence / comparison_count
        avg_reasoning = reasoning_coherence / comparison_count
        
        return (avg_structural + avg_reasoning) / 2.0
    
    async def _measure_attractor_coherence(self, attractors: Dict[str, Any]) -> float:
        """Measure coherence between attractors"""
        if len(attractors) < 2:
            return 1.0
        
        # Calculate coherence based on attractor patterns
        attractor_patterns = [a.get("pattern", "") for a in attractors.values()]
        
        similarities = []
        for i in range(len(attractor_patterns)):
            for j in range(i + 1, len(attractor_patterns)):
                similarity = self._calculate_similarity(
                    attractor_patterns[i], 
                    attractor_patterns[j]
                )
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate token-based similarity between texts"""
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        
        if not tokens1 or not tokens2:
            return 0.0
            
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0
    
    def _match_reasoning_patterns(self, pattern1: str, pattern2: str) -> float:
        """Match reasoning patterns between texts"""
        reasoning_indicators = [
            "because", "therefore", "thus", "consequently", "as a result",
            "if", "then", "when", "since", "given that", "analysis", "conclusion",
            "however", "although", "despite", "nevertheless", "moreover"
        ]
        
        indicators1 = set(word for word in pattern1.lower().split() 
                         if word in reasoning_indicators)
        indicators2 = set(word for word in pattern2.lower().split() 
                         if word in reasoning_indicators)
        
        if not indicators1 and not indicators2:
            return 0.5  # Neutral if no reasoning indicators
        if not indicators1 or not indicators2:
            return 0.0  # No match if only one has indicators
            
        intersection = len(indicators1.intersection(indicators2))
        union = len(indicators1.union(indicators2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_resonance_history(self) -> List[Dict[str, Any]]:
        """Get resonance measurement history"""
        return self.resonance_history.copy()
    
    def reset(self):
        """Reset resonance processor state"""
        self.resonance_history = []
        self.coherence_cache = {}