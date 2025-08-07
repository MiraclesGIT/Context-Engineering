"""
Context Engineering - Comprehensive Contextual AI Engine
======================================================

A production-ready contextual engine integrating cutting-edge research from:
- IBM Zurich: Cognitive Tools Framework  
- Princeton ICML: Emergent Symbolic Mechanisms
- Indiana University: Quantum Semantic Framework
- Singapore-MIT: Memory-Reasoning Synergy (MEM1)
- Shanghai AI Lab: Field Dynamics & Attractors
- Context Engineering: Progressive Complexity Framework

This package provides a unified API for building sophisticated AI systems
that go beyond simple prompt engineering to comprehensive context orchestration.

Quick Start:
-----------
>>> from context_engineering import ContextualEngine
>>> engine = ContextualEngine()
>>> result = engine.reason("Solve this complex problem step by step")

Architecture Overview:
---------------------
- Core Engine: Unified contextual processing engine
- Cognitive Tools: Structured reasoning operations
- Neural Fields: Dynamic context field management
- Memory Systems: Efficient long-horizon memory
- Symbolic Processing: Abstract reasoning capabilities
- Quantum Semantics: Observer-dependent interpretation
- Progressive Complexity: Scalable cognitive architectures

For detailed documentation, examples, and API reference:
https://github.com/context-engineering/context-engineering
"""

__version__ = "1.0.0"
__author__ = "Context Engineering Contributors"
__email__ = "contact@context-engineering.org"
__license__ = "MIT"

# Core Engine Imports
from .core import ContextualEngine, ContextualConfig
from .cognitive_tools import CognitiveToolsManager
from .neural_fields import NeuralFieldManager
from .memory_systems import MemoryManager
from .symbolic_processing import SymbolicProcessor
from .quantum_semantics import QuantumSemanticProcessor
from .progressive_complexity import ComplexityManager

# API Interfaces
from .api import (
    ContextAPI,
    ReasoningAPI,
    MemoryAPI,
    FieldAPI,
    ToolsAPI
)

# Utilities and Helpers
from .utils import (
    ContextualLogger,
    PerformanceMonitor,
    ConfigManager,
    ValidationUtils
)

# Examples and Demos
from . import examples
from . import demos
from . import tutorials

__all__ = [
    # Core Components
    'ContextualEngine',
    'ContextualConfig',
    'CognitiveToolsManager',
    'NeuralFieldManager', 
    'MemoryManager',
    'SymbolicProcessor',
    'QuantumSemanticProcessor',
    'ComplexityManager',
    
    # APIs
    'ContextAPI',
    'ReasoningAPI',
    'MemoryAPI',
    'FieldAPI',
    'ToolsAPI',
    
    # Utilities
    'ContextualLogger',
    'PerformanceMonitor',
    'ConfigManager',
    'ValidationUtils',
    
    # Modules
    'examples',
    'demos',
    'tutorials'
]

# Package Configuration
DEFAULT_CONFIG = {
    "engine": {
        "model_provider": "openai",
        "model_name": "gpt-4",
        "max_tokens": 4000,
        "temperature": 0.7,
        "enable_streaming": True
    },
    "cognitive_tools": {
        "enabled": True,
        "tool_selection": "auto",
        "verification_enabled": True
    },
    "neural_fields": {
        "enabled": True,
        "field_type": "semantic",
        "decay_rate": 0.05,
        "resonance_threshold": 0.6
    },
    "memory": {
        "enabled": True,
        "consolidation_frequency": 5,
        "memory_budget": 1000,
        "efficiency_target": 0.8
    },
    "symbolic_processing": {
        "enabled": True,
        "abstraction_depth": 3,
        "induction_method": "pattern_recognition"
    },
    "quantum_semantics": {
        "enabled": True,
        "observer_contexts": ["default"],
        "uncertainty_handling": "bayesian"
    },
    "progressive_complexity": {
        "enabled": True,
        "auto_scaling": True,
        "performance_threshold": 0.85
    }
}