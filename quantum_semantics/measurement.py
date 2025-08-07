"""
Measurement Engine - Quantum Semantic Measurement
=================================================

Handles measurement/collapse of semantic superposition states
into concrete meanings based on context and observation.
"""

import asyncio
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class MeasurementResult:
    """Result from quantum semantic measurement"""
    collapsed_meaning: str
    interpretations: List[Any]
    measurement_basis: str
    collapse_probability: float

class MeasurementEngine:
    """Handles quantum measurement of semantic states"""
    
    def __init__(self, config):
        self.config = config
        self.measurement_history = []
        
    async def measure_semantic_state(
        self, 
        superposition: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> MeasurementResult:
        """Measure/collapse semantic superposition into concrete meaning"""
        
        # Determine measurement basis
        measurement_basis = await self._determine_measurement_basis(superposition, context)
        
        # Perform quantum measurement
        measurement_result = await self._perform_measurement(
            superposition, measurement_basis, context
        )
        
        # Record measurement in history
        self.measurement_history.append({
            "superposition_id": id(superposition),
            "measurement_basis": measurement_basis,
            "collapse_result": measurement_result.collapsed_meaning[:100],  # Truncated
            "interpretations_count": len(measurement_result.interpretations)
        })
        
        return measurement_result
    
    async def _determine_measurement_basis(
        self, 
        superposition: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> str:
        """Determine the basis for quantum measurement"""
        
        # Strategy selection based on context and configuration
        if self.config.measurement_strategy == "context_collapse":
            return await self._context_based_measurement_basis(superposition, context)
        
        elif self.config.measurement_strategy == "max_probability":
            return "max_probability_basis"
        
        elif self.config.measurement_strategy == "coherence_preservation":
            return "coherence_basis"
        
        else:
            # Default to context-based measurement
            return await self._context_based_measurement_basis(superposition, context)
    
    async def _context_based_measurement_basis(
        self, 
        superposition: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> str:
        """Determine measurement basis based on context"""
        
        if not context:
            return "uniform_measurement"
        
        # Analyze context to determine most relevant measurement approach
        context_characteristics = self._analyze_context_characteristics(context)
        
        if context_characteristics["complexity"] > 0.7:
            return "complex_context_measurement"
        elif context_characteristics["specificity"] > 0.8:
            return "specific_context_measurement"
        else:
            return "general_context_measurement"
    
    def _analyze_context_characteristics(self, context: Dict[str, Any]) -> Dict[str, float]:
        """Analyze characteristics of the context"""
        
        characteristics = {
            "complexity": 0.0,
            "specificity": 0.0,
            "richness": 0.0
        }
        
        if not context:
            return characteristics
        
        # Complexity: based on nesting and variety of context elements
        total_elements = 0
        nested_elements = 0
        
        for key, value in context.items():
            total_elements += 1
            if isinstance(value, (dict, list)):
                nested_elements += 1
                if isinstance(value, dict):
                    total_elements += len(value)
                elif isinstance(value, list):
                    total_elements += len(value)
        
        characteristics["complexity"] = min(1.0, nested_elements / max(1, len(context)))
        characteristics["richness"] = min(1.0, total_elements / 10.0)  # Normalize to 10 elements
        
        # Specificity: based on detailed/specific information
        specific_indicators = ["id", "name", "type", "specific", "detail", "exact"]
        specific_count = sum(1 for key in context.keys() 
                           if any(indicator in key.lower() for indicator in specific_indicators))
        
        characteristics["specificity"] = min(1.0, specific_count / max(1, len(context)))
        
        return characteristics
    
    async def _perform_measurement(
        self, 
        superposition: Dict[str, Any], 
        measurement_basis: str, 
        context: Dict[str, Any]
    ) -> MeasurementResult:
        """Perform the actual quantum measurement"""
        
        interpretations = superposition.get("interpretations", [])
        
        if not interpretations:
            return MeasurementResult(
                collapsed_meaning="No semantic interpretations available for measurement",
                interpretations=[],
                measurement_basis=measurement_basis,
                collapse_probability=0.0
            )
        
        # Apply measurement basis to collapse superposition
        if measurement_basis == "max_probability_basis":
            return await self._max_probability_collapse(interpretations, measurement_basis)
        
        elif measurement_basis == "coherence_basis":
            return await self._coherence_preserving_collapse(interpretations, superposition, measurement_basis)
        
        elif measurement_basis in ["complex_context_measurement", "specific_context_measurement"]:
            return await self._context_weighted_collapse(interpretations, context, measurement_basis)
        
        else:
            # Default: weighted random collapse based on probabilities
            return await self._probability_weighted_collapse(interpretations, measurement_basis)
    
    async def _max_probability_collapse(
        self, 
        interpretations: List[Dict[str, Any]], 
        measurement_basis: str
    ) -> MeasurementResult:
        """Collapse to interpretation with maximum probability"""
        
        # Find interpretation with highest probability
        max_interp = max(interpretations, key=lambda x: x.get("probability", 0))
        
        # Create structured interpretations list
        structured_interpretations = []
        for interp in interpretations:
            from .manager import SemanticInterpretation
            structured_interp = SemanticInterpretation(
                id=interp.get("id", "unknown"),
                interpretation=interp.get("text", ""),
                probability=interp.get("probability", 0.0),
                observer_context=interp.get("observer_influence", "none"),
                coherence=interp.get("confidence", 0.5)
            )
            structured_interpretations.append(structured_interp)
        
        collapsed_meaning = self._format_collapsed_meaning(max_interp, "maximum_probability")
        
        return MeasurementResult(
            collapsed_meaning=collapsed_meaning,
            interpretations=structured_interpretations,
            measurement_basis=measurement_basis,
            collapse_probability=max_interp.get("probability", 0.0)
        )
    
    async def _coherence_preserving_collapse(
        self, 
        interpretations: List[Dict[str, Any]], 
        superposition: Dict[str, Any], 
        measurement_basis: str
    ) -> MeasurementResult:
        """Collapse while preserving quantum coherence"""
        
        superposition_coherence = superposition.get("coherence", 0.5)
        
        # Weight interpretations by coherence preservation
        coherence_weighted_interpretations = []
        for interp in interpretations:
            coherence_weight = interp.get("probability", 0.0) * superposition_coherence
            weighted_interp = interp.copy()
            weighted_interp["coherence_weight"] = coherence_weight
            coherence_weighted_interpretations.append(weighted_interp)
        
        # Select interpretation that best preserves coherence
        selected_interp = max(coherence_weighted_interpretations, 
                            key=lambda x: x.get("coherence_weight", 0))
        
        # Create structured interpretations
        structured_interpretations = []
        for interp in interpretations:
            from .manager import SemanticInterpretation
            structured_interp = SemanticInterpretation(
                id=interp.get("id", "unknown"),
                interpretation=interp.get("text", ""),
                probability=interp.get("probability", 0.0),
                observer_context=interp.get("observer_influence", "none"),
                coherence=superposition_coherence
            )
            structured_interpretations.append(structured_interp)
        
        collapsed_meaning = self._format_collapsed_meaning(selected_interp, "coherence_preservation")
        
        return MeasurementResult(
            collapsed_meaning=collapsed_meaning,
            interpretations=structured_interpretations,
            measurement_basis=measurement_basis,
            collapse_probability=selected_interp.get("coherence_weight", 0.0)
        )
    
    async def _context_weighted_collapse(
        self, 
        interpretations: List[Dict[str, Any]], 
        context: Dict[str, Any], 
        measurement_basis: str
    ) -> MeasurementResult:
        """Collapse with context-weighted probabilities"""
        
        # Calculate context alignment for each interpretation
        context_weighted_interpretations = []
        
        for interp in interpretations:
            context_alignment = self._calculate_context_alignment(interp, context)
            context_weight = interp.get("probability", 0.0) * (1.0 + context_alignment)
            
            weighted_interp = interp.copy()
            weighted_interp["context_weight"] = context_weight
            context_weighted_interpretations.append(weighted_interp)
        
        # Normalize context weights
        total_weight = sum(interp.get("context_weight", 0) for interp in context_weighted_interpretations)
        if total_weight > 0:
            for interp in context_weighted_interpretations:
                interp["context_weight"] /= total_weight
        
        # Select based on context weighting
        selected_interp = max(context_weighted_interpretations, 
                            key=lambda x: x.get("context_weight", 0))
        
        # Create structured interpretations
        structured_interpretations = []
        for interp in interpretations:
            from .manager import SemanticInterpretation
            structured_interp = SemanticInterpretation(
                id=interp.get("id", "unknown"),
                interpretation=interp.get("text", ""),
                probability=interp.get("probability", 0.0),
                observer_context=interp.get("observer_influence", "none"),
                coherence=interp.get("confidence", 0.5)
            )
            structured_interpretations.append(structured_interp)
        
        collapsed_meaning = self._format_collapsed_meaning(selected_interp, "context_weighted")
        
        return MeasurementResult(
            collapsed_meaning=collapsed_meaning,
            interpretations=structured_interpretations,
            measurement_basis=measurement_basis,
            collapse_probability=selected_interp.get("context_weight", 0.0)
        )
    
    async def _probability_weighted_collapse(
        self, 
        interpretations: List[Dict[str, Any]], 
        measurement_basis: str
    ) -> MeasurementResult:
        """Collapse using probability-weighted random selection"""
        
        # Prepare probability distribution
        probabilities = [interp.get("probability", 0.0) for interp in interpretations]
        total_prob = sum(probabilities)
        
        if total_prob == 0:
            # Equal probability if no probabilities specified
            selected_interp = random.choice(interpretations)
            collapse_probability = 1.0 / len(interpretations)
        else:
            # Weighted random selection
            normalized_probs = [p / total_prob for p in probabilities]
            selected_interp = random.choices(interpretations, weights=normalized_probs)[0]
            collapse_probability = selected_interp.get("probability", 0.0)
        
        # Create structured interpretations
        structured_interpretations = []
        for interp in interpretations:
            from .manager import SemanticInterpretation
            structured_interp = SemanticInterpretation(
                id=interp.get("id", "unknown"),
                interpretation=interp.get("text", ""),
                probability=interp.get("probability", 0.0),
                observer_context=interp.get("observer_influence", "none"),
                coherence=interp.get("confidence", 0.5)
            )
            structured_interpretations.append(structured_interp)
        
        collapsed_meaning = self._format_collapsed_meaning(selected_interp, "probability_weighted")
        
        return MeasurementResult(
            collapsed_meaning=collapsed_meaning,
            interpretations=structured_interpretations,
            measurement_basis=measurement_basis,
            collapse_probability=collapse_probability
        )
    
    def _calculate_context_alignment(
        self, 
        interpretation: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> float:
        """Calculate alignment between interpretation and context"""
        
        if not context:
            return 0.0
        
        # Simple token-based alignment
        interp_text = interpretation.get("text", "").lower().split()
        context_text = " ".join(str(v) for v in context.values()).lower().split()
        
        if not interp_text or not context_text:
            return 0.0
        
        # Calculate overlap
        interp_set = set(interp_text)
        context_set = set(context_text)
        
        intersection = len(interp_set.intersection(context_set))
        union = len(interp_set.union(context_set))
        
        alignment = intersection / union if union > 0 else 0.0
        
        return alignment
    
    def _format_collapsed_meaning(
        self, 
        selected_interpretation: Dict[str, Any], 
        collapse_method: str
    ) -> str:
        """Format the collapsed meaning with metadata"""
        
        interpretation_text = selected_interpretation.get("text", "Unknown interpretation")
        probability = selected_interpretation.get("probability", 0.0)
        confidence = selected_interpretation.get("confidence", 0.0)
        
        formatted_meaning = f"""
QUANTUM SEMANTIC MEASUREMENT RESULT:

Collapsed Interpretation: {interpretation_text}

Measurement Details:
- Collapse Method: {collapse_method}
- Selection Probability: {probability:.3f}
- Interpretation Confidence: {confidence:.3f}
- Interpretation Type: {selected_interpretation.get("type", "general")}

Quantum Semantic Analysis:
The semantic superposition has collapsed into a definite interpretation through 
{collapse_method} measurement. This represents the actualized meaning from the 
quantum semantic field based on observer context and measurement conditions.
        """
        
        return formatted_meaning.strip()
    
    def get_measurement_history(self) -> List[Dict[str, Any]]:
        """Get history of quantum measurements"""
        return self.measurement_history.copy()
    
    def reset(self):
        """Reset measurement engine state"""
        self.measurement_history = []