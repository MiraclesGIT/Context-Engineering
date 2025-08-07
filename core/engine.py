"""
Contextual Engine - Main Processing Engine
==========================================

The ContextualEngine is the primary interface for all context engineering
operations. It integrates all research components into a unified system.
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Union, AsyncGenerator
from dataclasses import dataclass, field

from .config import ContextualConfig
from .orchestrator import ContextOrchestrator
from ..cognitive_tools import CognitiveToolsManager
from ..neural_fields import NeuralFieldManager
from ..memory_systems import MemoryManager
from ..symbolic_processing import SymbolicProcessor
from ..quantum_semantics import QuantumSemanticProcessor
from ..progressive_complexity import ComplexityManager
from ..utils import ContextualLogger, PerformanceMonitor

@dataclass
class ContextualRequest:
    """Represents a request to the contextual engine"""
    query: str
    context: Dict[str, Any] = field(default_factory=dict)
    task_type: str = "general_reasoning"
    complexity_preference: str = "auto"
    enable_streaming: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass  
class ContextualResponse:
    """Represents a response from the contextual engine"""
    result: str
    reasoning_trace: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    field_state: Dict[str, Any]
    memory_updates: Dict[str, Any]
    confidence_score: float
    processing_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)

class ContextualEngine:
    """
    Main Contextual Engine integrating all research components.
    
    This engine provides a unified interface for:
    - Cognitive tools-based reasoning (IBM Zurich)
    - Symbolic processing (Princeton ICML)  
    - Quantum semantic interpretation (Indiana University)
    - Memory-reasoning synergy (Singapore-MIT MEM1)
    - Neural field dynamics (Shanghai AI Lab)
    - Progressive complexity management (Context Engineering)
    """
    
    def __init__(self, config: Optional[ContextualConfig] = None):
        """Initialize the contextual engine with configuration"""
        self.config = config or ContextualConfig()
        self.logger = ContextualLogger("ContextualEngine")
        self.performance_monitor = PerformanceMonitor()
        
        # Initialize core components
        self._initialize_components()
        
        # Initialize orchestrator
        self.orchestrator = ContextOrchestrator(
            cognitive_tools=self.cognitive_tools,
            neural_fields=self.neural_fields,
            memory_manager=self.memory_manager,
            symbolic_processor=self.symbolic_processor,
            quantum_semantic=self.quantum_semantic,
            complexity_manager=self.complexity_manager
        )
        
        self.logger.info("ContextualEngine initialized successfully")
    
    def _initialize_components(self):
        """Initialize all component managers"""
        self.logger.info("Initializing contextual engine components...")
        
        # Cognitive Tools Manager (IBM Zurich Framework)
        if self.config.cognitive_tools.enabled:
            self.cognitive_tools = CognitiveToolsManager(self.config.cognitive_tools)
            self.logger.info("✓ Cognitive Tools Manager initialized")
        else:
            self.cognitive_tools = None
            
        # Neural Field Manager (Shanghai AI Lab + Context Engineering)
        if self.config.neural_fields.enabled:
            self.neural_fields = NeuralFieldManager(self.config.neural_fields) 
            self.logger.info("✓ Neural Field Manager initialized")
        else:
            self.neural_fields = None
            
        # Memory Manager (Singapore-MIT MEM1)
        if self.config.memory.enabled:
            self.memory_manager = MemoryManager(self.config.memory)
            self.logger.info("✓ Memory Manager initialized")
        else:
            self.memory_manager = None
            
        # Symbolic Processor (Princeton ICML)
        if self.config.symbolic_processing.enabled:
            self.symbolic_processor = SymbolicProcessor(self.config.symbolic_processing)
            self.logger.info("✓ Symbolic Processor initialized")
        else:
            self.symbolic_processor = None
            
        # Quantum Semantic Processor (Indiana University)
        if self.config.quantum_semantics.enabled:
            self.quantum_semantic = QuantumSemanticProcessor(self.config.quantum_semantics)
            self.logger.info("✓ Quantum Semantic Processor initialized")
        else:
            self.quantum_semantic = None
            
        # Complexity Manager (Context Engineering Progressive Framework)
        if self.config.progressive_complexity.enabled:
            self.complexity_manager = ComplexityManager(self.config.progressive_complexity)
            self.logger.info("✓ Complexity Manager initialized")
        else:
            self.complexity_manager = None
    
    async def reason(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ContextualResponse:
        """
        Main reasoning interface using integrated contextual processing.
        
        Args:
            query: The query or problem to reason about
            context: Optional context dictionary
            **kwargs: Additional processing options
            
        Returns:
            ContextualResponse with result and processing metadata
        """
        start_time = time.time()
        
        # Create request
        request = ContextualRequest(
            query=query,
            context=context or {},
            **kwargs
        )
        
        self.logger.info(f"Processing contextual reasoning request: {query[:100]}...")
        
        try:
            # Use orchestrator for integrated processing
            result = await self.orchestrator.process_request(request)
            
            processing_time = time.time() - start_time
            self.performance_monitor.record_request(processing_time, len(query), len(result.result))
            
            # Create response
            response = ContextualResponse(
                result=result.result,
                reasoning_trace=result.reasoning_trace,
                performance_metrics=result.performance_metrics,
                field_state=result.field_state,
                memory_updates=result.memory_updates,
                confidence_score=result.confidence_score,
                processing_time=processing_time,
                metadata=result.metadata
            )
            
            self.logger.info(f"✓ Contextual reasoning completed in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            self.logger.error(f"Error in contextual reasoning: {str(e)}")
            processing_time = time.time() - start_time
            
            # Return error response
            return ContextualResponse(
                result=f"Error in contextual processing: {str(e)}",
                reasoning_trace=[{"error": str(e)}],
                performance_metrics={"processing_time": processing_time, "success": False},
                field_state={},
                memory_updates={},
                confidence_score=0.0,
                processing_time=processing_time,
                metadata={"error": True}
            )
    
    def reason_sync(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ContextualResponse:
        """
        Synchronous version of reasoning interface.
        
        Args:
            query: The query or problem to reason about  
            context: Optional context dictionary
            **kwargs: Additional processing options
            
        Returns:
            ContextualResponse with result and processing metadata
        """
        return asyncio.run(self.reason(query, context, **kwargs))
    
    async def reason_stream(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming reasoning interface for real-time processing updates.
        
        Args:
            query: The query or problem to reason about
            context: Optional context dictionary  
            **kwargs: Additional processing options
            
        Yields:
            Processing updates and partial results
        """
        request = ContextualRequest(
            query=query,
            context=context or {},
            enable_streaming=True,
            **kwargs
        )
        
        async for update in self.orchestrator.process_request_stream(request):
            yield update
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get engine performance metrics"""
        return {
            "engine_metrics": self.performance_monitor.get_metrics(),
            "component_metrics": {
                "cognitive_tools": self.cognitive_tools.get_metrics() if self.cognitive_tools else None,
                "neural_fields": self.neural_fields.get_metrics() if self.neural_fields else None,
                "memory_manager": self.memory_manager.get_metrics() if self.memory_manager else None,
                "symbolic_processor": self.symbolic_processor.get_metrics() if self.symbolic_processor else None,
                "quantum_semantic": self.quantum_semantic.get_metrics() if self.quantum_semantic else None,
                "complexity_manager": self.complexity_manager.get_metrics() if self.complexity_manager else None
            }
        }
    
    def get_field_state(self) -> Dict[str, Any]:
        """Get current neural field state"""
        if self.neural_fields:
            return self.neural_fields.get_field_state()
        return {}
    
    def get_memory_state(self) -> Dict[str, Any]:
        """Get current memory system state"""
        if self.memory_manager:
            return self.memory_manager.get_memory_state()
        return {}
    
    def reset(self):
        """Reset engine state"""
        self.logger.info("Resetting contextual engine state...")
        
        if self.neural_fields:
            self.neural_fields.reset()
        if self.memory_manager:
            self.memory_manager.reset()
        if self.cognitive_tools:
            self.cognitive_tools.reset()
        if self.symbolic_processor:
            self.symbolic_processor.reset()
        if self.quantum_semantic:
            self.quantum_semantic.reset()
        if self.complexity_manager:
            self.complexity_manager.reset()
            
        self.performance_monitor.reset()
        self.logger.info("✓ Engine state reset completed")
    
    def configure(self, new_config: ContextualConfig):
        """Update engine configuration"""
        self.logger.info("Updating contextual engine configuration...")
        self.config = new_config
        
        # Reinitialize components with new config
        self._initialize_components()
        
        # Update orchestrator
        self.orchestrator.update_components(
            cognitive_tools=self.cognitive_tools,
            neural_fields=self.neural_fields,
            memory_manager=self.memory_manager,
            symbolic_processor=self.symbolic_processor,
            quantum_semantic=self.quantum_semantic,
            complexity_manager=self.complexity_manager
        )
        
        self.logger.info("✓ Configuration update completed")
    
    def __repr__(self) -> str:
        """String representation of the engine"""
        enabled_components = []
        if self.cognitive_tools: enabled_components.append("CognitiveTools")
        if self.neural_fields: enabled_components.append("NeuralFields")
        if self.memory_manager: enabled_components.append("Memory")
        if self.symbolic_processor: enabled_components.append("SymbolicProcessing")
        if self.quantum_semantic: enabled_components.append("QuantumSemantics")
        if self.complexity_manager: enabled_components.append("ProgressiveComplexity")
        
        return f"ContextualEngine(components={enabled_components})"