"""
Contextual Logger - Enhanced Logging for Context Engineering
============================================================

Provides structured logging capabilities with context-aware features
and integration with all context engineering components.
"""

import logging
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class ContextualLogger:
    """Enhanced logger with contextual awareness and structured logging"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.logger = logging.getLogger(f"ContextualEngine.{name}")
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Create formatter for structured logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add console handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.context_stack = []
        self.performance_logs = []
    
    def push_context(self, context: Dict[str, Any]):
        """Push a context onto the context stack"""
        self.context_stack.append({
            "context": context,
            "timestamp": time.time()
        })
    
    def pop_context(self):
        """Pop the most recent context from the stack"""
        if self.context_stack:
            return self.context_stack.pop()
        return None
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get the current context"""
        if self.context_stack:
            return self.context_stack[-1]["context"]
        return {}
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Debug level logging with context"""
        self._log_with_context(logging.DEBUG, message, context)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Info level logging with context"""
        self._log_with_context(logging.INFO, message, context)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Warning level logging with context"""
        self._log_with_context(logging.WARNING, message, context)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Error level logging with context"""
        self._log_with_context(logging.ERROR, message, context)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Critical level logging with context"""
        self._log_with_context(logging.CRITICAL, message, context)
    
    def _log_with_context(self, level: int, message: str, context: Optional[Dict[str, Any]]):
        """Internal method to log with context"""
        # Combine provided context with current context
        full_context = self.get_current_context().copy()
        if context:
            full_context.update(context)
        
        # Format message with context
        if full_context:
            context_str = json.dumps(full_context, default=str, separators=(',', ':'))
            formatted_message = f"{message} | Context: {context_str}"
        else:
            formatted_message = message
        
        self.logger.log(level, formatted_message)
    
    def log_performance(
        self, 
        operation: str, 
        duration: float, 
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log performance metrics"""
        performance_record = {
            "operation": operation,
            "duration": duration,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        self.performance_logs.append(performance_record)
        
        # Keep only recent performance logs
        if len(self.performance_logs) > 1000:
            self.performance_logs = self.performance_logs[-1000:]
        
        self.info(
            f"Performance: {operation} completed in {duration:.3f}s",
            {"performance_data": performance_record}
        )
    
    def log_reasoning_step(
        self, 
        step: str, 
        input_data: Any, 
        output_data: Any, 
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log reasoning steps for traceability"""
        reasoning_record = {
            "step": step,
            "input_preview": str(input_data)[:100] + "..." if len(str(input_data)) > 100 else str(input_data),
            "output_preview": str(output_data)[:100] + "..." if len(str(output_data)) > 100 else str(output_data),
            "confidence": confidence,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        self.debug(
            f"Reasoning Step: {step} (confidence: {confidence:.2f})",
            {"reasoning_data": reasoning_record}
        )
    
    def log_component_interaction(
        self, 
        component_from: str, 
        component_to: str, 
        interaction_type: str,
        data_summary: str
    ):
        """Log interactions between components"""
        interaction_record = {
            "from_component": component_from,
            "to_component": component_to,
            "interaction_type": interaction_type,
            "data_summary": data_summary,
            "timestamp": time.time()
        }
        
        self.debug(
            f"Component Interaction: {component_from} -> {component_to} ({interaction_type})",
            {"interaction_data": interaction_record}
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of performance logs"""
        if not self.performance_logs:
            return {"no_performance_data": True}
        
        operations = {}
        for log in self.performance_logs:
            operation = log["operation"]
            if operation not in operations:
                operations[operation] = {"count": 0, "total_duration": 0.0, "durations": []}
            
            operations[operation]["count"] += 1
            operations[operation]["total_duration"] += log["duration"]
            operations[operation]["durations"].append(log["duration"])
        
        # Calculate statistics
        performance_summary = {}
        for operation, stats in operations.items():
            durations = stats["durations"]
            performance_summary[operation] = {
                "count": stats["count"],
                "total_duration": stats["total_duration"],
                "average_duration": stats["total_duration"] / stats["count"],
                "min_duration": min(durations),
                "max_duration": max(durations)
            }
        
        return performance_summary
    
    def export_logs(
        self, 
        start_time: Optional[float] = None, 
        end_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """Export logs within time range"""
        current_time = time.time()
        start_time = start_time or (current_time - 3600)  # Default: last hour
        end_time = end_time or current_time
        
        filtered_performance_logs = [
            log for log in self.performance_logs
            if start_time <= log["timestamp"] <= end_time
        ]
        
        return {
            "logger_name": self.name,
            "export_timestamp": current_time,
            "time_range": {"start": start_time, "end": end_time},
            "performance_logs": filtered_performance_logs,
            "log_count": len(filtered_performance_logs)
        }
    
    def clear_logs(self):
        """Clear performance logs"""
        self.performance_logs = []
        self.context_stack = []
        self.info("Logs cleared")