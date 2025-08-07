"""
Contextual Engine Configuration
===============================

Configuration classes for all contextual engine components.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class EngineConfig:
    """Core engine configuration"""
    model_provider: str = "openai"
    model_name: str = "gpt-4"
    api_key: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    enable_streaming: bool = True
    timeout: int = 300
    retry_attempts: int = 3

@dataclass  
class CognitiveToolsConfig:
    """IBM Zurich Cognitive Tools configuration"""
    enabled: bool = True
    tool_selection: str = "auto"  # "auto", "manual", "adaptive"
    verification_enabled: bool = True
    available_tools: List[str] = field(default_factory=lambda: [
        "understand", "extract", "highlight", "apply", "validate"
    ])
    max_tool_depth: int = 5
    parallel_processing: bool = True

@dataclass
class NeuralFieldsConfig:
    """Neural Fields configuration"""
    enabled: bool = True
    field_type: str = "semantic"  # "semantic", "cognitive", "hybrid"
    decay_rate: float = 0.05
    boundary_permeability: float = 0.8
    resonance_bandwidth: float = 0.6
    attractor_formation_threshold: float = 0.7
    max_attractors: int = 10
    field_dimensions: int = 512

@dataclass
class MemoryConfig:
    """Singapore-MIT MEM1 Memory configuration"""
    enabled: bool = True
    consolidation_frequency: int = 5
    memory_budget: int = 1000
    efficiency_target: float = 0.8
    retention_strategy: str = "reasoning_value"  # "reasoning_value", "recency", "frequency"
    compression_method: str = "semantic_similarity"
    persistence_enabled: bool = True

@dataclass
class SymbolicProcessingConfig:
    """Princeton ICML Symbolic Processing configuration"""
    enabled: bool = True
    abstraction_depth: int = 3
    induction_method: str = "pattern_recognition"  # "pattern_recognition", "logical_inference"
    retrieval_strategy: str = "best_match"  # "best_match", "ensemble", "weighted"
    symbolic_validation: bool = True
    generalization_enabled: bool = True

@dataclass
class QuantumSemanticsConfig:
    """Indiana University Quantum Semantics configuration"""
    enabled: bool = True
    observer_contexts: List[str] = field(default_factory=lambda: ["default"])
    uncertainty_handling: str = "bayesian"  # "bayesian", "quantum", "probabilistic"
    superposition_threshold: float = 0.3
    measurement_strategy: str = "context_collapse"
    degeneracy_management: bool = True

@dataclass
class ProgressiveComplexityConfig:
    """Progressive Complexity configuration"""
    enabled: bool = True
    auto_scaling: bool = True
    performance_threshold: float = 0.85
    complexity_levels: List[str] = field(default_factory=lambda: [
        "atom", "molecule", "cell", "organ", "neural_system", "neural_field"
    ])
    scaling_strategy: str = "adaptive"  # "adaptive", "linear", "exponential"
    efficiency_monitoring: bool = True

@dataclass
class ContextualConfig:
    """Main configuration class combining all component configurations"""
    engine: EngineConfig = field(default_factory=EngineConfig)
    cognitive_tools: CognitiveToolsConfig = field(default_factory=CognitiveToolsConfig)
    neural_fields: NeuralFieldsConfig = field(default_factory=NeuralFieldsConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    symbolic_processing: SymbolicProcessingConfig = field(default_factory=SymbolicProcessingConfig)
    quantum_semantics: QuantumSemanticsConfig = field(default_factory=QuantumSemanticsConfig)
    progressive_complexity: ProgressiveComplexityConfig = field(default_factory=ProgressiveComplexityConfig)
    
    # Global settings
    debug_enabled: bool = False
    logging_level: str = "INFO"
    performance_monitoring: bool = True
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ContextualConfig':
        """Create configuration from dictionary"""
        return cls(
            engine=EngineConfig(**config_dict.get("engine", {})),
            cognitive_tools=CognitiveToolsConfig(**config_dict.get("cognitive_tools", {})),
            neural_fields=NeuralFieldsConfig(**config_dict.get("neural_fields", {})),
            memory=MemoryConfig(**config_dict.get("memory", {})),
            symbolic_processing=SymbolicProcessingConfig(**config_dict.get("symbolic_processing", {})),
            quantum_semantics=QuantumSemanticsConfig(**config_dict.get("quantum_semantics", {})),
            progressive_complexity=ProgressiveComplexityConfig(**config_dict.get("progressive_complexity", {})),
            debug_enabled=config_dict.get("debug_enabled", False),
            logging_level=config_dict.get("logging_level", "INFO"),
            performance_monitoring=config_dict.get("performance_monitoring", True)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "engine": self.engine.__dict__,
            "cognitive_tools": self.cognitive_tools.__dict__,
            "neural_fields": self.neural_fields.__dict__,
            "memory": self.memory.__dict__,
            "symbolic_processing": self.symbolic_processing.__dict__,
            "quantum_semantics": self.quantum_semantics.__dict__,
            "progressive_complexity": self.progressive_complexity.__dict__,
            "debug_enabled": self.debug_enabled,
            "logging_level": self.logging_level,
            "performance_monitoring": self.performance_monitoring
        }