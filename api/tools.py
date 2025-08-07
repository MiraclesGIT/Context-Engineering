"""
Tools API - Cognitive Tools Interface
=====================================

API interface for cognitive tools operations providing direct access
to individual tools and tool management capabilities.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .context import APIResponse
from ..cognitive_tools import CognitiveToolsManager
from ..core.config import CognitiveToolsConfig
from ..utils.logger import ContextualLogger
from ..utils.validation import ValidationUtils

class ToolsAPI:
    """
    API interface for cognitive tools operations.
    
    Provides direct access to individual cognitive tools and
    tool management capabilities.
    """
    
    def __init__(self, config: Optional[CognitiveToolsConfig] = None):
        self.config = config or CognitiveToolsConfig()
        self.cognitive_tools = CognitiveToolsManager(self.config)
        self.logger = ContextualLogger("ToolsAPI")
        
        self.logger.info("Tools API initialized")
    
    async def execute_tool(
        self,
        tool_name: str,
        content: str,
        parameters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Execute a specific cognitive tool."""
        try:
            # Validate inputs
            content_valid, content_errors = ValidationUtils.validate_content_input(content)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid content: {'; '.join(content_errors)}"
                )
            
            if tool_name not in self.cognitive_tools.available_tools:
                return APIResponse(
                    success=False,
                    error=f"Tool '{tool_name}' not available. Available tools: {list(self.cognitive_tools.available_tools.keys())}"
                )
            
            # Prepare parameters
            tool_parameters = parameters or {}
            if context:
                tool_parameters["context"] = context
            
            # Execute tool
            result = await self.cognitive_tools.execute_tool(
                tool_name, content, tool_parameters
            )
            
            return APIResponse(
                success=True,
                data={
                    "tool_execution": {
                        "tool_name": tool_name,
                        "result": result.content,
                        "confidence": result.confidence,
                        "processing_time": result.processing_time,
                        "metadata": result.metadata,
                        "reasoning_trace": result.reasoning_trace
                    },
                    "content_preview": content[:100] + "..." if len(content) > 100 else content,
                    "parameters_used": tool_parameters,
                    "tool_usage_count": self.cognitive_tools.tool_usage_count.get(tool_name, 0)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tool execution error: {str(e)}"
            )
    
    async def execute_tool_sequence(
        self,
        tools_sequence: List[Dict[str, Any]],
        initial_content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Execute a sequence of cognitive tools."""
        try:
            # Validate initial content
            content_valid, content_errors = ValidationUtils.validate_content_input(initial_content)
            if not content_valid:
                return APIResponse(
                    success=False,
                    error=f"Invalid initial content: {'; '.join(content_errors)}"
                )
            
            # Validate tool sequence
            if not tools_sequence or not isinstance(tools_sequence, list):
                return APIResponse(
                    success=False,
                    error="Tool sequence must be a non-empty list"
                )
            
            # Execute tools in sequence
            current_content = initial_content
            execution_results = []
            cumulative_context = context.copy() if context else {}
            
            for i, tool_config in enumerate(tools_sequence):
                tool_name = tool_config.get("tool")
                tool_params = tool_config.get("parameters", {})
                
                if not tool_name:
                    return APIResponse(
                        success=False,
                        error=f"Tool name missing in sequence step {i}"
                    )
                
                if tool_name not in self.cognitive_tools.available_tools:
                    return APIResponse(
                        success=False,
                        error=f"Tool '{tool_name}' not available in sequence step {i}"
                    )
                
                # Add cumulative context to parameters
                full_params = tool_params.copy()
                full_params["context"] = cumulative_context
                
                # Execute tool
                result = await self.cognitive_tools.execute_tool(
                    tool_name, current_content, full_params
                )
                
                # Record execution result
                execution_results.append({
                    "step": i,
                    "tool": tool_name,
                    "input": current_content[:100] + "..." if len(current_content) > 100 else current_content,
                    "output": result.content,
                    "confidence": result.confidence,
                    "processing_time": result.processing_time,
                    "metadata": result.metadata
                })
                
                # Update content and context for next tool
                current_content = result.content
                cumulative_context[f"step_{i}_{tool_name}"] = result.content
            
            # Calculate sequence statistics
            total_processing_time = sum(step["processing_time"] for step in execution_results)
            average_confidence = sum(step["confidence"] for step in execution_results) / len(execution_results)
            
            return APIResponse(
                success=True,
                data={
                    "sequence_execution": {
                        "initial_content": initial_content[:100] + "..." if len(initial_content) > 100 else initial_content,
                        "final_result": current_content,
                        "steps_executed": len(execution_results),
                        "execution_results": execution_results,
                        "sequence_statistics": {
                            "total_processing_time": total_processing_time,
                            "average_confidence": average_confidence,
                            "tools_used": [step["tool"] for step in execution_results]
                        }
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error executing tool sequence: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tool sequence execution error: {str(e)}"
            )
    
    async def get_tool_info(self, tool_name: str) -> APIResponse:
        """Get detailed information about a specific tool."""
        try:
            if tool_name not in self.cognitive_tools.available_tools:
                return APIResponse(
                    success=False,
                    error=f"Tool '{tool_name}' not available"
                )
            
            tool = self.cognitive_tools.available_tools[tool_name]
            tool_usage_count = self.cognitive_tools.tool_usage_count.get(tool_name, 0)
            
            return APIResponse(
                success=True,
                data={
                    "tool_info": {
                        "name": tool.name,
                        "description": tool.description,
                        "usage_count": tool_usage_count,
                        "process_steps": tool._get_process_steps() if hasattr(tool, '_get_process_steps') else "Not available"
                    },
                    "usage_statistics": {
                        "times_used": tool_usage_count,
                        "usage_rank": self._get_tool_usage_rank(tool_name)
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting tool info for {tool_name}: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tool info error: {str(e)}"
            )
    
    async def get_all_tools(self) -> APIResponse:
        """Get information about all available tools."""
        try:
            tools_info = {}
            
            for tool_name, tool in self.cognitive_tools.available_tools.items():
                usage_count = self.cognitive_tools.tool_usage_count.get(tool_name, 0)
                
                tools_info[tool_name] = {
                    "name": tool.name,
                    "description": tool.description,
                    "usage_count": usage_count
                }
            
            # Get tool metrics
            tool_metrics = self.cognitive_tools.get_tool_metrics()
            
            return APIResponse(
                success=True,
                data={
                    "available_tools": tools_info,
                    "tool_statistics": {
                        "total_tools": len(tools_info),
                        "total_usage": sum(info["usage_count"] for info in tools_info.values()),
                        "most_used_tool": tool_metrics.get("most_used_tool"),
                        "tool_metrics": tool_metrics
                    }
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting all tools: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tools query error: {str(e)}"
            )
    
    async def analyze_tool_performance(self) -> APIResponse:
        """Analyze performance of cognitive tools."""
        try:
            tool_metrics = self.cognitive_tools.get_tool_metrics()
            
            # Calculate additional performance metrics
            performance_analysis = {
                "usage_distribution": self.cognitive_tools.tool_usage_count.copy(),
                "total_executions": sum(self.cognitive_tools.tool_usage_count.values()),
                "tool_efficiency": self._calculate_tool_efficiency(),
                "usage_patterns": self._analyze_usage_patterns(),
                "recommendations": self._generate_tool_recommendations()
            }
            
            return APIResponse(
                success=True,
                data={
                    "performance_analysis": performance_analysis,
                    "tool_metrics": tool_metrics
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing tool performance: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tool performance analysis error: {str(e)}"
            )
    
    async def reset_tool_statistics(self) -> APIResponse:
        """Reset tool usage statistics."""
        try:
            # Store current stats for reporting
            current_stats = self.cognitive_tools.tool_usage_count.copy()
            total_usage = sum(current_stats.values())
            
            # Reset statistics
            self.cognitive_tools.tool_usage_count = {
                tool: 0 for tool in self.cognitive_tools.available_tools.keys()
            }
            
            return APIResponse(
                success=True,
                data={
                    "reset_completed": True,
                    "previous_statistics": {
                        "total_usage": total_usage,
                        "usage_by_tool": current_stats
                    },
                    "current_statistics": self.cognitive_tools.tool_usage_count.copy()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error resetting tool statistics: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tool statistics reset error: {str(e)}"
            )
    
    def _get_tool_usage_rank(self, tool_name: str) -> int:
        """Get usage rank of a tool."""
        usage_counts = list(self.cognitive_tools.tool_usage_count.values())
        usage_counts.sort(reverse=True)
        
        tool_usage = self.cognitive_tools.tool_usage_count.get(tool_name, 0)
        
        try:
            return usage_counts.index(tool_usage) + 1
        except ValueError:
            return len(usage_counts) + 1
    
    def _calculate_tool_efficiency(self) -> Dict[str, Any]:
        """Calculate tool efficiency metrics."""
        # Simplified efficiency calculation
        # In a real implementation, this would consider processing time, success rate, etc.
        
        total_usage = sum(self.cognitive_tools.tool_usage_count.values())
        if total_usage == 0:
            return {"no_usage_data": True}
        
        tool_count = len(self.cognitive_tools.available_tools)
        expected_usage_per_tool = total_usage / tool_count
        
        efficiency_scores = {}
        for tool_name, usage_count in self.cognitive_tools.tool_usage_count.items():
            # Higher usage relative to expected usage indicates higher efficiency
            efficiency_score = min(1.0, usage_count / max(1, expected_usage_per_tool))
            efficiency_scores[tool_name] = efficiency_score
        
        return {
            "tool_efficiency_scores": efficiency_scores,
            "average_efficiency": sum(efficiency_scores.values()) / len(efficiency_scores),
            "most_efficient_tool": max(efficiency_scores.items(), key=lambda x: x[1])[0] if efficiency_scores else None,
            "least_efficient_tool": min(efficiency_scores.items(), key=lambda x: x[1])[0] if efficiency_scores else None
        }
    
    def _analyze_usage_patterns(self) -> Dict[str, Any]:
        """Analyze tool usage patterns."""
        usage_counts = self.cognitive_tools.tool_usage_count
        total_usage = sum(usage_counts.values())
        
        if total_usage == 0:
            return {"no_usage_data": True}
        
        # Identify usage categories
        never_used = [tool for tool, count in usage_counts.items() if count == 0]
        rarely_used = [tool for tool, count in usage_counts.items() if 0 < count <= 2]
        frequently_used = [tool for tool, count in usage_counts.items() if count > 10]
        
        return {
            "usage_categories": {
                "never_used": never_used,
                "rarely_used": rarely_used,
                "frequently_used": frequently_used
            },
            "usage_distribution": {
                "never_used_count": len(never_used),
                "rarely_used_count": len(rarely_used),
                "frequently_used_count": len(frequently_used)
            },
            "usage_concentration": len(frequently_used) / len(usage_counts) if usage_counts else 0
        }
    
    def _generate_tool_recommendations(self) -> List[str]:
        """Generate tool usage recommendations."""
        recommendations = []
        
        usage_patterns = self._analyze_usage_patterns()
        
        if usage_patterns.get("no_usage_data"):
            recommendations.append("No tool usage data available - start using cognitive tools")
            return recommendations
        
        never_used = usage_patterns.get("usage_categories", {}).get("never_used", [])
        if never_used:
            recommendations.append(f"Consider trying unused tools: {', '.join(never_used[:3])}")
        
        rarely_used = usage_patterns.get("usage_categories", {}).get("rarely_used", [])
        if rarely_used:
            recommendations.append(f"Explore underutilized tools: {', '.join(rarely_used[:3])}")
        
        usage_concentration = usage_patterns.get("usage_concentration", 0)
        if usage_concentration < 0.3:
            recommendations.append("Tool usage is well distributed across available tools")
        elif usage_concentration > 0.7:
            recommendations.append("Tool usage is concentrated - consider diversifying tool selection")
        
        return recommendations
    
    # Synchronous wrapper methods
    def execute_tool_sync(
        self,
        tool_name: str,
        content: str,
        parameters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Synchronous version of execute_tool."""
        return asyncio.run(self.execute_tool(tool_name, content, parameters, context))
    
    def get_all_tools_sync(self) -> APIResponse:
        """Synchronous version of get_all_tools."""
        return asyncio.run(self.get_all_tools())