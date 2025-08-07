"""
Symbolic Processing Module - Princeton ICML Implementation
=========================================================

Implementation of the Princeton ICML three-stage symbolic processing framework
for abstract reasoning through emergent symbolic mechanisms.
"""

from .manager import SymbolicProcessor
from .abstraction import AbstractionEngine
from .induction import InductionEngine
from .retrieval import RetrievalEngine

__all__ = [
    'SymbolicProcessor',
    'AbstractionEngine',
    'InductionEngine',
    'RetrievalEngine'
]