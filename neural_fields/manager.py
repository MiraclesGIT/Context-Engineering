"""
Neural Field Manager - Field Dynamics Orchestration
===================================================

Manages neural field dynamics, attractors, and resonance patterns
for contextual processing based on Shanghai AI Lab research.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..core.base import BaseFieldProcessor, ProcessingResult
from .field import SemanticField, CognitiveField
from .attractors import AttractorManager
from .resonance import ResonanceProcessor

@dataclass
class FieldInjectionResult:
    """Result from field pattern injection"""
    pattern_id: str
    field_energy: float
    attractors_formed: int
    resonance_score: float

@dataclass
class FieldResonanceResult:
    """Result from field resonance measurement"""
    resonance_score: float
    matching_attractors: List[str]
    field_coherence: float
    stability_measure: float

@dataclass
class FieldUpdateResult:
    """Result from field updates"""
    new_attractors: int
    stability_score: float
    field_evolution: Dict[str, Any]

class NeuralFieldManager(BaseFieldProcessor):
    """
    Neural Field Manager implementing field dynamics for context engineering.
    
    Based on Shanghai AI Lab research on attractor dynamics and field theory,
    this manager provides:
    - Dynamic field evolution and pattern injection
    - Attractor formation and basin dynamics  
    - Resonance measurement and field coherence
    - Symbolic residue tracking and persistence
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Initialize field components
        self.semantic_field = SemanticField(config)
        self.cognitive_field = CognitiveField(config)
        self.attractor_manager = AttractorManager(config)
        self.resonance_processor = ResonanceProcessor(config)
        
        self.logger = logging.getLogger("NeuralFieldManager")
        self.logger.info("Neural field dynamics initialized")
    
    async def process(self, content: str, context: Dict[str, Any]) -> ProcessingResult:
        """Process content through neural field dynamics"""
        start_time = asyncio.get_event_loop().time()
        
        # Inject content into field
        injection_result = await self.inject_pattern(content, strength=1.0)
        
        # Measure field resonance
        resonance_result = await self.measure_field_resonance(content, context)
        
        # Generate field-informed response
        field_response = self._generate_field_response(content, context, resonance_result)
        
        processing_time = asyncio.get_event_loop().time() - start_time
        self._record_processing(processing_time)
        
        return ProcessingResult(
            content=field_response,
            confidence=resonance_result.resonance_score,
            processing_time=processing_time,
            metadata={
                "field_energy": injection_result.field_energy,
                "attractors": injection_result.attractors_formed,
                "resonance": resonance_result.resonance_score
            },
            reasoning_trace=[{
                "step": "field_processing",
                "injection": injection_result.__dict__,
                "resonance": resonance_result.__dict__
            }]
        )
    
    async def inject_pattern(self, pattern: str, strength: float = 1.0) -> FieldInjectionResult:
        """Inject a pattern into the neural field"""
        self.logger.debug(f"Injecting pattern with strength {strength}")
        
        # Apply boundary filtering
        effective_strength = strength * self.config.boundary_permeability
        
        # Inject into semantic field
        semantic_injection = await self.semantic_field.inject(pattern, effective_strength)
        
        # Inject into cognitive field
        cognitive_injection = await self.cognitive_field.inject(pattern, effective_strength)
        
        # Check for attractor formation
        new_attractors = await self.attractor_manager.check_attractor_formation(
            pattern, effective_strength, self.config.attractor_formation_threshold
        )
        
        # Calculate field energy
        field_energy = self.semantic_field.calculate_energy() + self.cognitive_field.calculate_energy()
        
        # Measure resonance
        resonance_score = await self.resonance_processor.measure_pattern_resonance(
            pattern, self.get_field_state()
        )
        
        return FieldInjectionResult(
            pattern_id=f"pattern_{len(self.field_state)}",
            field_energy=field_energy,
            attractors_formed=len(new_attractors),
            resonance_score=resonance_score
        )
    
    async def measure_field_resonance(
        self, 
        content: str, 
        context: Dict[str, Any]
    ) -> FieldResonanceResult:
        """Measure resonance between content and field state"""
        self.logger.debug("Measuring field resonance")
        
        # Calculate resonance with semantic field
        semantic_resonance = await self.semantic_field.measure_resonance(content)
        
        # Calculate resonance with cognitive field
        cognitive_resonance = await self.cognitive_field.measure_resonance(content)
        
        # Find matching attractors
        matching_attractors = await self.attractor_manager.find_resonant_attractors(content)
        
        # Measure field coherence
        field_coherence = await self.resonance_processor.measure_field_coherence(
            self.get_field_state()
        )
        
        # Calculate stability
        stability_measure = self._calculate_stability()
        
        # Combined resonance score
        overall_resonance = (semantic_resonance + cognitive_resonance) / 2.0
        
        return FieldResonanceResult(
            resonance_score=overall_resonance,
            matching_attractors=[a["id"] for a in matching_attractors],
            field_coherence=field_coherence,
            stability_measure=stability_measure
        )
    
    async def update_field_with_result(
        self, 
        result: str, 
        context: Dict[str, Any]
    ) -> FieldUpdateResult:
        """Update field state with processing result"""
        self.logger.debug("Updating field with result")
        
        # Inject result into field with reduced strength
        injection_result = await self.inject_pattern(result, strength=0.8)
        
        # Update attractor basins
        attractor_updates = await self.attractor_manager.update_attractors(result, context)
        
        # Apply field decay
        await self.apply_field_decay()
        
        # Calculate field evolution metrics
        field_evolution = {
            "energy_change": injection_result.field_energy - self._previous_energy,
            "new_patterns": 1,
            "attractor_updates": len(attractor_updates)
        }
        self._previous_energy = injection_result.field_energy
        
        return FieldUpdateResult(
            new_attractors=injection_result.attractors_formed,
            stability_score=self._calculate_stability(),
            field_evolution=field_evolution
        )
    
    async def apply_field_decay(self):
        """Apply natural decay to field patterns"""
        # Apply decay to semantic field
        await self.semantic_field.apply_decay(self.config.decay_rate)
        
        # Apply decay to cognitive field
        await self.cognitive_field.apply_decay(self.config.decay_rate)
        
        # Update attractor strengths
        await self.attractor_manager.apply_attractor_decay(self.config.decay_rate * 0.2)
    
    def inject_pattern(self, pattern: str, strength: float = 1.0):
        """Synchronous version of inject_pattern"""
        return asyncio.run(self.inject_pattern(pattern, strength))
    
    def measure_resonance(self, content: str) -> float:
        """Simple resonance measurement for compatibility"""
        try:
            result = asyncio.run(self.measure_field_resonance(content, {}))
            return result.resonance_score
        except:
            return 0.5  # Default resonance
    
    def get_field_state(self) -> Dict[str, Any]:
        """Get comprehensive field state"""
        semantic_state = self.semantic_field.get_state()
        cognitive_state = self.cognitive_field.get_state()
        attractors = self.attractor_manager.get_attractors()
        
        return {
            "semantic_field": semantic_state,
            "cognitive_field": cognitive_state,
            "attractors": attractors,
            "field_energy": semantic_state.get("energy", 0) + cognitive_state.get("energy", 0),
            "stability": self._calculate_stability(),
            "resonance_bandwidth": self.config.resonance_bandwidth
        }
    
    def reset(self):
        """Reset neural field manager state"""
        self.semantic_field.reset()
        self.cognitive_field.reset()
        self.attractor_manager.reset()
        self.resonance_processor.reset()
        
        self.field_state = {}
        self.attractors = {}
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.last_processing_time = 0.0
        self._previous_energy = 0.0
        
        self.logger.info("Neural field manager state reset")
    
    def _generate_field_response(
        self, 
        content: str, 
        context: Dict[str, Any], 
        resonance_result: FieldResonanceResult
    ) -> str:
        """Generate field-informed response"""
        return f"""
NEURAL FIELD ANALYSIS:

Field Resonance Score: {resonance_result.resonance_score:.2f}
Field Coherence: {resonance_result.field_coherence:.2f}
Stability Measure: {resonance_result.stability_measure:.2f}
Matching Attractors: {len(resonance_result.matching_attractors)}

Field-Informed Response:
Based on the neural field dynamics analysis, this query resonates with existing field patterns at a {resonance_result.resonance_score:.1%} level. The field maintains {resonance_result.field_coherence:.1%} coherence with {resonance_result.stability_measure:.1%} stability.

The neural field processing indicates strong alignment with {len(resonance_result.matching_attractors)} existing attractor basins, suggesting this is within a well-explored cognitive domain with established reasoning patterns.

Field recommendations: Continue with structured approach, leveraging existing cognitive attractors while allowing for pattern evolution and emergence of new insights.
        """
    
    def _calculate_stability(self) -> float:
        """Calculate overall field stability"""
        if not self.attractors:
            return 0.5  # Neutral stability without attractors
            
        attractor_strengths = [a.get("strength", 0) for a in self.attractors.values()]
        if not attractor_strengths:
            return 0.5
            
        return sum(attractor_strengths) / len(attractor_strengths)
    
    def __init__(self, config):
        super().__init__(config)
        
        # Initialize field components
        self.semantic_field = SemanticField(config)
        self.cognitive_field = CognitiveField(config)
        self.attractor_manager = AttractorManager(config)
        self.resonance_processor = ResonanceProcessor(config)
        
        # Initialize state
        self._previous_energy = 0.0
        
        self.logger = logging.getLogger("NeuralFieldManager")
        self.logger.info("Neural field dynamics initialized")