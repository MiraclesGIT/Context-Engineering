"""
Neural Fields Module - Shanghai AI Lab & Context Engineering Implementation
===========================================================================

Implementation of neural field dynamics for context management and emergent
cognitive behaviors based on field theory and attractor dynamics.
"""

from .manager import NeuralFieldManager
from .field import SemanticField, CognitiveField
from .attractors import AttractorManager
from .resonance import ResonanceProcessor

__all__ = [
    'NeuralFieldManager',
    'SemanticField',
    'CognitiveField', 
    'AttractorManager',
    'ResonanceProcessor'
]