"""
Complexity Manager - Progressive Complexity Framework
=====================================================

Manages progressive complexity scaling and adaptive cognitive
architecture optimization based on task complexity and performance.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..core.base import BaseContextProcessor, ProcessingResult
from .scaling import ComplexityScaler
from .assessment import ComplexityAssessment
from .optimization import ComplexityOptimizer

@dataclass
class ComplexityLevel:
    """Represents a complexity level in the progressive framework"""
    name: str
    description: str
    cognitive_resources: int
    processing_depth: int
    abstraction_capacity: float

@dataclass
class ComplexityRecommendation:
    """Recommendation for optimal complexity level"""
    recommended_complexity: str
    confidence: float
    reasoning: str
    resource_requirements: Dict[str, float]

class ComplexityManager(BaseContextProcessor):
    """
    Progressive Complexity Manager implementing adaptive cognitive scaling.
    
    Complexity Levels (inspired by biological organization):
    1. Atom: Basic processing units
    2. Molecule: Combined basic operations
    3. Cell: Self-contained processing modules
    4. Organ: Specialized functional systems
    5. Neural System: Integrated reasoning networks
    6. Neural Field: Emergent field-level cognition
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Initialize complexity components
        self.scaler = ComplexityScaler(config)
        self.assessor = ComplexityAssessment(config)
        self.optimizer = ComplexityOptimizer(config)
        
        # Define complexity levels
        self._initialize_complexity_levels()
        
        # Current complexity state
        self.current_complexity = "neural_system"  # Default
        self.performance_history = []
        
        self.logger = logging.getLogger("ComplexityManager")
        self.logger.info("Progressive complexity framework initialized")
    
    def _initialize_complexity_levels(self):
        """Initialize the progressive complexity levels"""
        self.complexity_levels = {
            "atom": ComplexityLevel(
                name="atom",
                description="Basic processing units - fundamental operations",
                cognitive_resources=1,
                processing_depth=1,
                abstraction_capacity=0.2
            ),
            "molecule": ComplexityLevel(
                name="molecule",
                description="Combined basic operations - simple compositions",
                cognitive_resources=2,
                processing_depth=2,
                abstraction_capacity=0.4
            ),
            "cell": ComplexityLevel(
                name="cell", 
                description="Self-contained processing modules - autonomous units",
                cognitive_resources=4,
                processing_depth=3,
                abstraction_capacity=0.6
            ),
            "organ": ComplexityLevel(
                name="organ",
                description="Specialized functional systems - domain expertise",
                cognitive_resources=8,
                processing_depth=4,
                abstraction_capacity=0.8
            ),
            "neural_system": ComplexityLevel(
                name="neural_system",
                description="Integrated reasoning networks - cognitive integration",
                cognitive_resources=16,
                processing_depth=5,
                abstraction_capacity=1.0
            ),
            "neural_field": ComplexityLevel(
                name="neural_field",
                description="Emergent field-level cognition - collective intelligence",
                cognitive_resources=32,
                processing_depth=6,
                abstraction_capacity=1.2
            )
        }
    
    async def process(self, content: str, context: Dict[str, Any]) -> ProcessingResult:
        """Process content with adaptive complexity management"""
        start_time = asyncio.get_event_loop().time()
        
        # Assess optimal complexity for this task
        complexity_assessment = await self.assess_complexity(content, context)
        
        # Apply complexity scaling if needed
        if complexity_assessment.recommended_complexity != self.current_complexity:
            await self.scale_complexity(complexity_assessment.recommended_complexity)
        
        # Process with current complexity level
        complexity_result = await self._process_at_complexity_level(
            content, context, self.current_complexity
        )
        
        processing_time = asyncio.get_event_loop().time() - start_time
        self._record_processing(processing_time)
        
        # Record performance for optimization
        self._record_performance(complexity_assessment, complexity_result, processing_time)
        
        return ProcessingResult(
            content=complexity_result["output"],
            confidence=complexity_result["confidence"],
            processing_time=processing_time,
            metadata={
                "complexity_level": self.current_complexity,
                "complexity_recommendation": complexity_assessment.recommended_complexity,
                "resource_utilization": complexity_result["resource_utilization"]
            },
            reasoning_trace=[{
                "step": "progressive_complexity_processing",
                "complexity_assessment": complexity_assessment.__dict__,
                "complexity_result": complexity_result
            }]
        )
    
    async def assess_complexity(
        self, 
        content: str, 
        context: Dict[str, Any]
    ) -> ComplexityRecommendation:
        """Assess optimal complexity level for given content and context"""
        self.logger.debug("Assessing complexity requirements")
        
        return await self.assessor.assess_optimal_complexity(content, context)
    
    async def scale_complexity(self, target_complexity: str):
        """Scale to target complexity level"""
        if target_complexity not in self.complexity_levels:
            self.logger.warning(f"Invalid complexity level: {target_complexity}")
            return
        
        self.logger.info(f"Scaling complexity: {self.current_complexity} → {target_complexity}")
        
        # Apply scaling through the scaler
        scaling_result = await self.scaler.scale_to_complexity(
            self.current_complexity, 
            target_complexity
        )
        
        if scaling_result["success"]:
            self.current_complexity = target_complexity
            self.logger.info(f"✓ Complexity scaled to {target_complexity}")
        else:
            self.logger.warning(f"Failed to scale complexity: {scaling_result.get('error', 'Unknown error')}")
    
    async def _process_at_complexity_level(
        self, 
        content: str, 
        context: Dict[str, Any], 
        complexity_level: str
    ) -> Dict[str, Any]:
        """Process content at specified complexity level"""
        
        level_config = self.complexity_levels[complexity_level]
        
        # Simulate processing characteristics based on complexity level
        if complexity_level == "atom":
            return await self._atomic_processing(content, context, level_config)
        elif complexity_level == "molecule":
            return await self._molecular_processing(content, context, level_config)
        elif complexity_level == "cell":
            return await self._cellular_processing(content, context, level_config)
        elif complexity_level == "organ":
            return await self._organ_processing(content, context, level_config)
        elif complexity_level == "neural_system":
            return await self._neural_system_processing(content, context, level_config)
        elif complexity_level == "neural_field":
            return await self._neural_field_processing(content, context, level_config)
        else:
            return await self._default_processing(content, context, level_config)
    
    async def _atomic_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Basic atomic-level processing"""
        return {
            "output": f"ATOMIC PROCESSING: Basic analysis of '{content[:50]}...'",
            "confidence": 0.6,
            "resource_utilization": 0.1,
            "processing_characteristics": {
                "approach": "fundamental_operations",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    async def _molecular_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Molecular-level processing - combined operations"""
        return {
            "output": f"MOLECULAR PROCESSING: Combined analysis of '{content[:50]}...' with basic pattern recognition",
            "confidence": 0.7,
            "resource_utilization": 0.2,
            "processing_characteristics": {
                "approach": "combined_operations",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    async def _cellular_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Cellular-level processing - autonomous modules"""
        return {
            "output": f"CELLULAR PROCESSING: Modular analysis of '{content[:50]}...' with contextual integration",
            "confidence": 0.75,
            "resource_utilization": 0.4,
            "processing_characteristics": {
                "approach": "autonomous_modules",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    async def _organ_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Organ-level processing - specialized systems"""
        return {
            "output": f"ORGAN PROCESSING: Specialized analysis of '{content[:50]}...' with domain expertise and functional specialization",
            "confidence": 0.8,
            "resource_utilization": 0.6,
            "processing_characteristics": {
                "approach": "specialized_systems",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    async def _neural_system_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Neural system-level processing - integrated networks"""
        return {
            "output": f"NEURAL SYSTEM PROCESSING: Integrated cognitive analysis of '{content[:50]}...' with multi-layer reasoning and context synthesis",
            "confidence": 0.85,
            "resource_utilization": 0.8,
            "processing_characteristics": {
                "approach": "integrated_networks",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    async def _neural_field_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Neural field-level processing - emergent cognition"""
        return {
            "output": f"NEURAL FIELD PROCESSING: Emergent field-level cognitive analysis of '{content[:50]}...' with collective intelligence, field dynamics, and meta-cognitive awareness",
            "confidence": 0.9,
            "resource_utilization": 1.0,
            "processing_characteristics": {
                "approach": "emergent_field_cognition",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    async def _default_processing(
        self, 
        content: str, 
        context: Dict[str, Any], 
        level_config: ComplexityLevel
    ) -> Dict[str, Any]:
        """Default processing fallback"""
        return {
            "output": f"DEFAULT PROCESSING: Standard analysis of '{content[:50]}...'",
            "confidence": 0.7,
            "resource_utilization": 0.5,
            "processing_characteristics": {
                "approach": "standard_processing",
                "depth": level_config.processing_depth,
                "abstraction": level_config.abstraction_capacity
            }
        }
    
    def _record_performance(
        self, 
        complexity_assessment: ComplexityRecommendation,
        complexity_result: Dict[str, Any],
        processing_time: float
    ):
        """Record performance metrics for optimization"""
        performance_record = {
            "timestamp": asyncio.get_event_loop().time(),
            "assessed_complexity": complexity_assessment.recommended_complexity,
            "actual_complexity": self.current_complexity,
            "confidence_achieved": complexity_result["confidence"],
            "resource_utilization": complexity_result["resource_utilization"],
            "processing_time": processing_time,
            "efficiency": complexity_result["confidence"] / max(0.1, complexity_result["resource_utilization"])
        }
        
        self.performance_history.append(performance_record)
        
        # Keep only recent performance history
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-100:]
    
    async def optimize_complexity_strategy(self) -> Dict[str, Any]:
        """Optimize complexity scaling strategy based on performance history"""
        if not self.performance_history:
            return {"optimization": "insufficient_data"}
        
        return await self.optimizer.optimize_strategy(self.performance_history)
    
    def get_current_complexity_state(self) -> Dict[str, Any]:
        """Get current complexity state and metrics"""
        current_level = self.complexity_levels[self.current_complexity]
        
        return {
            "current_complexity": self.current_complexity,
            "level_config": current_level.__dict__,
            "performance_history_length": len(self.performance_history),
            "recent_efficiency": self._calculate_recent_efficiency(),
            "complexity_utilization": self._calculate_complexity_utilization()
        }
    
    def _calculate_recent_efficiency(self) -> float:
        """Calculate recent processing efficiency"""
        if not self.performance_history:
            return 0.0
        
        recent_records = self.performance_history[-10:]  # Last 10 records
        efficiencies = [record["efficiency"] for record in recent_records]
        
        return sum(efficiencies) / len(efficiencies)
    
    def _calculate_complexity_utilization(self) -> float:
        """Calculate how well complexity levels are being utilized"""
        if not self.performance_history:
            return 0.0
        
        recent_records = self.performance_history[-20:]  # Last 20 records
        resource_utilizations = [record["resource_utilization"] for record in recent_records]
        
        return sum(resource_utilizations) / len(resource_utilizations)
    
    def reset(self):
        """Reset complexity manager state"""
        self.current_complexity = "neural_system"  # Reset to default
        self.performance_history = []
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.last_processing_time = 0.0
        
        self.scaler.reset()
        self.assessor.reset()
        self.optimizer.reset()
        
        self.logger.info("Complexity manager state reset")