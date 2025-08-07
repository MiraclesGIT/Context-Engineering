"""
Context API - Main Contextual Engine API Interface
==================================================

Primary API interface for the contextual engine providing comprehensive
access to all context engineering capabilities.
"""

import asyncio
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass, asdict

from ..core.engine import ContextualEngine, ContextualRequest, ContextualResponse
from ..core.config import ContextualConfig
from ..utils.validation import ValidationUtils, ValidationError
from ..utils.logger import ContextualLogger

@dataclass
class APIResponse:
    """Standard API response format"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

class ContextAPI:
    """
    Main API interface for the Contextual Engine.
    
    Provides a clean, RESTful-style interface for all context engineering
    capabilities with proper error handling, validation, and documentation.
    """
    
    def __init__(self, config: Optional[ContextualConfig] = None):
        self.engine = ContextualEngine(config)
        self.logger = ContextualLogger("ContextAPI")
        self.request_count = 0
        
        self.logger.info("Context API initialized")
    
    async def process(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        **options
    ) -> APIResponse:
        """
        Process content through the contextual engine.
        
        Args:
            content: The content to process
            context: Optional context dictionary
            **options: Additional processing options
            
        Returns:
            APIResponse with processing results
        """
        self.request_count += 1
        
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(content)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid content: {'; '.join(content_errors)}"
                )
            
            context_valid, context_errors = ValidationUtils.validate_context_input(context)
            if not context_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid context: {'; '.join(context_errors)}"
                )
            
            # Process through engine
            result = await self.engine.reason(content, context, **options)
            
            # Validate result
            result_valid, result_errors = ValidationUtils.validate_processing_result(result)
            if not result_valid:
                self.logger.error(f"Invalid processing result: {result_errors}")
                # Continue anyway, but log the validation issues
            
            return APIResponse(
                success=True,
                data={
                    "result": result.result,
                    "confidence": result.confidence_score,
                    "processing_time": result.processing_time,
                    "reasoning_trace": result.reasoning_trace,
                    "performance_metrics": result.performance_metrics,
                    "field_state": result.field_state,
                    "memory_updates": result.memory_updates
                },
                metadata={
                    "request_id": self.request_count,
                    "engine_version": "1.0.0",
                    "components_used": self._get_active_components()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in process request: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Processing error: {str(e)}",
                metadata={"request_id": self.request_count}
            )
    
    async def process_stream(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None,
        **options
    ) -> AsyncGenerator[APIResponse, None]:
        """
        Process content with streaming responses.
        
        Args:
            content: The content to process
            context: Optional context dictionary
            **options: Additional processing options
            
        Yields:
            APIResponse objects with streaming updates
        """
        self.request_count += 1
        
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(content)
            if not content_valid:
                yield APIResponse(
                    success=False,
                    error=f"Invalid content: {'; '.join(content_errors)}"
                )
                return
            
            context_valid, context_errors = ValidationUtils.validate_context_input(context)
            if not context_valid:
                yield APIResponse(
                    success=False,
                    error=f"Invalid context: {'; '.join(context_errors)}"
                )
                return
            
            # Stream processing updates
            async for update in self.engine.reason_stream(content, context, **options):
                yield APIResponse(
                    success=True,
                    data=update,
                    metadata={"request_id": self.request_count, "stream": True}
                )
                
        except Exception as e:
            self.logger.error(f"Error in streaming request: {str(e)}")
            yield APIResponse(
                success=False,
                error=f"Streaming error: {str(e)}",
                metadata={"request_id": self.request_count}
            )
    
    async def process_batch(
        self,
        contents: List[str],
        contexts: Optional[List[Dict[str, Any]]] = None,
        **options
    ) -> APIResponse:
        """
        Process multiple contents in batch.
        
        Args:
            contents: List of contents to process
            contexts: Optional list of context dictionaries
            **options: Additional processing options
            
        Returns:
            APIResponse with batch processing results
        """
        self.request_count += 1
        
        try:
            # Validate batch inputs
            batch_valid, batch_errors = ValidationUtils.validate_batch_inputs(contents, contexts)
            if not batch_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid batch inputs: {'; '.join(batch_errors)}"
                )
            
            # Process each item
            results = []
            for i, content in enumerate(contents):
                context = contexts[i] if contexts and i < len(contexts) else None
                
                try:
                    result = await self.engine.reason(content, context, **options)
                    results.append({
                        "index": i,
                        "success": True,
                        "result": result.result,
                        "confidence": result.confidence_score,
                        "processing_time": result.processing_time
                    })
                except Exception as e:
                    results.append({
                        "index": i,
                        "success": False,
                        "error": str(e)
                    })
            
            # Calculate batch statistics
            successful_results = [r for r in results if r["success"]]
            success_rate = len(successful_results) / len(results)
            avg_processing_time = (
                sum(r["processing_time"] for r in successful_results) / len(successful_results)
                if successful_results else 0.0
            )
            
            return APIResponse(
                success=True,
                data={
                    "results": results,
                    "batch_statistics": {
                        "total_items": len(results),
                        "successful_items": len(successful_results),
                        "success_rate": success_rate,
                        "average_processing_time": avg_processing_time
                    }
                },
                metadata={
                    "request_id": self.request_count,
                    "batch_size": len(contents)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in batch processing: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Batch processing error: {str(e)}",
                metadata={"request_id": self.request_count}
            )
    
    async def get_engine_status(self) -> APIResponse:
        """Get current engine status and metrics."""
        try:
            performance_metrics = self.engine.get_performance_metrics()
            field_state = self.engine.get_field_state()
            memory_state = self.engine.get_memory_state()
            
            return APIResponse(
                success=True,
                data={
                    "engine_status": "operational",
                    "performance_metrics": performance_metrics,
                    "field_state": field_state,
                    "memory_state": memory_state,
                    "active_components": self._get_active_components(),
                    "request_count": self.request_count
                },
                metadata={"timestamp": asyncio.get_event_loop().time()}
            )
            
        except Exception as e:
            self.logger.error(f"Error getting engine status: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Status error: {str(e)}"
            )
    
    async def configure_engine(self, config_updates: Dict[str, Any]) -> APIResponse:
        """Update engine configuration."""
        try:
            # Create new config with updates
            current_config = self.engine.config
            new_config = ContextualConfig.from_dict({
                **current_config.to_dict(),
                **config_updates
            })
            
            # Validate new configuration
            # (Add validation logic here if needed)
            
            # Apply new configuration
            self.engine.configure(new_config)
            
            return APIResponse(
                success=True,
                data={"message": "Configuration updated successfully"},
                metadata={"config_updates": config_updates}
            )
            
        except Exception as e:
            self.logger.error(f"Error updating configuration: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Configuration error: {str(e)}"
            )
    
    async def reset_engine(self) -> APIResponse:
        """Reset engine state."""
        try:
            self.engine.reset()
            self.request_count = 0
            
            return APIResponse(
                success=True,
                data={"message": "Engine reset successfully"}
            )
            
        except Exception as e:
            self.logger.error(f"Error resetting engine: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Reset error: {str(e)}"
            )
    
    def _get_active_components(self) -> List[str]:
        """Get list of active engine components."""
        active_components = []
        
        if hasattr(self.engine, 'cognitive_tools') and self.engine.cognitive_tools:
            active_components.append("cognitive_tools")
        if hasattr(self.engine, 'neural_fields') and self.engine.neural_fields:
            active_components.append("neural_fields")
        if hasattr(self.engine, 'memory_manager') and self.engine.memory_manager:
            active_components.append("memory_manager")
        if hasattr(self.engine, 'symbolic_processor') and self.engine.symbolic_processor:
            active_components.append("symbolic_processor")
        if hasattr(self.engine, 'quantum_semantic') and self.engine.quantum_semantic:
            active_components.append("quantum_semantic")
        if hasattr(self.engine, 'complexity_manager') and self.engine.complexity_manager:
            active_components.append("complexity_manager")
        
        return active_components
    
    # Synchronous wrapper methods for convenience
    def process_sync(self, content: str, context: Optional[Dict[str, Any]] = None, **options) -> APIResponse:
        """Synchronous version of process method."""
        return asyncio.run(self.process(content, context, **options))
    
    def get_engine_status_sync(self) -> APIResponse:
        """Synchronous version of get_engine_status method."""
        return asyncio.run(self.get_engine_status())
    
    def configure_engine_sync(self, config_updates: Dict[str, Any]) -> APIResponse:
        """Synchronous version of configure_engine method."""
        return asyncio.run(self.configure_engine(config_updates))
    
    def reset_engine_sync(self) -> APIResponse:
        """Synchronous version of reset_engine method."""
        return asyncio.run(self.reset_engine())