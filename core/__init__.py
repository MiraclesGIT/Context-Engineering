"""
Context Engineering Core Module
==============================

The core module provides the main ContextualEngine class that orchestrates
all context engineering capabilities into a unified interface.
"""

from .engine import ContextualEngine
from .config import ContextualConfig
from .base import BaseContextProcessor
from .orchestrator import ContextOrchestrator

__all__ = [
    'ContextualEngine',
    'ContextualConfig', 
    'BaseContextProcessor',
    'ContextOrchestrator'
]