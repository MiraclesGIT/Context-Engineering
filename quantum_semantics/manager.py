"""
Quantum Semantic Processor - Indiana University Implementation
=============================================================

Implements quantum semantic framework where meaning exists in superposition
until observed/measured, based on Indiana University research on quantum semantics.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..core.base import BaseContextProcessor, ProcessingResult
from .observer import ObserverManager
from .superposition import SuperpositionProcessor
from .measurement import MeasurementEngine

@dataclass
class SemanticInterpretation:
    """Represents a potential semantic interpretation"""
    id: str
    interpretation: str
    probability: float
    observer_context: str
    coherence: float

@dataclass
class QuantumSemanticResult:
    """Result from quantum semantic processing"""
    interpretations: List[SemanticInterpretation]
    collapsed_meaning: str
    uncertainty_score: float
    observer_influence: float

class QuantumSemanticProcessor(BaseContextProcessor):
    """
    Quantum Semantic Processor implementing Indiana University framework.
    
    Key Principles:
    - Semantic Superposition: Meaning exists in multiple states simultaneously
    - Observer Effect: Meaning collapses upon observation/measurement  
    - Contextual Entanglement: Meanings are correlated across contexts
    - Uncertainty Principle: Precision and scope are complementary
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Initialize quantum semantic components
        self.observer_manager = ObserverManager(config)
        self.superposition_processor = SuperpositionProcessor(config)
        self.measurement_engine = MeasurementEngine(config)
        
        self.logger = logging.getLogger("QuantumSemanticProcessor")
        self.logger.info("Indiana University quantum semantic framework initialized")
    
    async def process(self, content: str, context: Dict[str, Any]) -> ProcessingResult:
        """Process content through quantum semantic framework"""
        start_time = asyncio.get_event_loop().time()
        
        # Interpret with quantum semantic context
        quantum_result = await self.interpret_with_context(content, context)
        
        processing_time = asyncio.get_event_loop().time() - start_time
        self._record_processing(processing_time)
        
        return ProcessingResult(
            content=quantum_result.collapsed_meaning,
            confidence=1.0 - quantum_result.uncertainty_score,
            processing_time=processing_time,
            metadata={
                "interpretations_count": len(quantum_result.interpretations),
                "uncertainty_score": quantum_result.uncertainty_score,
                "observer_influence": quantum_result.observer_influence
            },
            reasoning_trace=[{
                "step": "quantum_semantic_processing",
                "interpretations": [i.__dict__ for i in quantum_result.interpretations],
                "measurement_outcome": quantum_result.collapsed_meaning
            }]
        )
    
    async def interpret_with_context(
        self, 
        content: str, 
        context: Dict[str, Any]
    ) -> QuantumSemanticResult:
        """Interpret content using quantum semantic principles"""
        self.logger.debug("Starting quantum semantic interpretation")
        
        # Phase 1: Create semantic superposition
        superposition = await self.superposition_processor.create_superposition(content, context)
        
        # Phase 2: Apply observer contexts
        observed_superposition = await self.observer_manager.apply_observer_effects(
            superposition, self.config.observer_contexts
        )
        
        # Phase 3: Measure/collapse semantic meaning
        measurement_result = await self.measurement_engine.measure_semantic_state(
            observed_superposition, context
        )
        
        # Calculate overall uncertainty and observer influence
        uncertainty_score = self._calculate_uncertainty(measurement_result.interpretations)
        observer_influence = self._calculate_observer_influence(
            superposition, observed_superposition
        )
        
        self.logger.info("✓ Quantum semantic interpretation completed")
        
        return QuantumSemanticResult(
            interpretations=measurement_result.interpretations,
            collapsed_meaning=measurement_result.collapsed_meaning,
            uncertainty_score=uncertainty_score,
            observer_influence=observer_influence
        )
    
    def _calculate_uncertainty(self, interpretations: List[SemanticInterpretation]) -> float:
        """Calculate quantum uncertainty in semantic interpretations"""
        if not interpretations:
            return 1.0
        
        # Shannon entropy-based uncertainty
        import math
        
        probabilities = [interp.probability for interp in interpretations if interp.probability > 0]
        if not probabilities:
            return 1.0
        
        # Normalize probabilities
        total_prob = sum(probabilities)
        normalized_probs = [p / total_prob for p in probabilities]
        
        # Calculate entropy
        entropy = -sum(p * math.log2(p) for p in normalized_probs if p > 0)
        max_entropy = math.log2(len(normalized_probs))
        
        # Normalize to 0-1 scale
        uncertainty = entropy / max_entropy if max_entropy > 0 else 0.0
        
        return uncertainty
    
    def _calculate_observer_influence(
        self, 
        original_superposition: Dict[str, Any], 
        observed_superposition: Dict[str, Any]
    ) -> float:
        """Calculate the influence of observer on semantic meaning"""
        # Compare original and observed superposition states
        original_interpretations = len(original_superposition.get("interpretations", []))
        observed_interpretations = len(observed_superposition.get("interpretations", []))
        
        if original_interpretations == 0:
            return 0.0
        
        # Observer influence = reduction in superposition states
        state_reduction = (original_interpretations - observed_interpretations) / original_interpretations
        
        return max(0.0, state_reduction)
    
    def reset(self):
        """Reset quantum semantic processor state"""
        self.observer_manager.reset()
        self.superposition_processor.reset()
        self.measurement_engine.reset()
        
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.last_processing_time = 0.0
        
        self.logger.info("Quantum semantic processor state reset")