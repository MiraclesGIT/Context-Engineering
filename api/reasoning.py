"""
Reasoning API - Specialized Reasoning Interface
===============================================

Specialized API interface for reasoning-focused operations using
cognitive tools and structured reasoning processes.
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .context import APIResponse
from ..cognitive_tools import CognitiveToolsManager
from ..core.config import CognitiveToolsConfig
from ..utils.logger import ContextualLogger

class ReasoningAPI:
    """
    API interface specialized for reasoning operations.
    
    Provides direct access to cognitive tools framework and
    structured reasoning capabilities.
    """
    
    def __init__(self, config: Optional[CognitiveToolsConfig] = None):
        self.config = config or CognitiveToolsConfig()
        self.cognitive_tools = CognitiveToolsManager(self.config)
        self.logger = ContextualLogger("ReasoningAPI")
        
        self.logger.info("Reasoning API initialized")
    
    async def execute_reasoning_sequence(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        complexity: str = "neural_system"
    ) -> APIResponse:
        """Execute full cognitive reasoning sequence."""
        try:
            result = await self.cognitive_tools.execute_reasoning_sequence(
                query, context or {}, complexity
            )
            
            return APIResponse(
                success=True,
                data={
                    "result": result.result,
                    "reasoning_trace": result.reasoning_trace,
                    "tools_used": result.tools_used,
                    "verification_passed": result.verification_passed,
                    "confidence_score": result.confidence_score
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in reasoning sequence: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Reasoning error: {str(e)}"
            )
    
    async def execute_single_tool(
        self,
        tool_name: str,
        content: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Execute a single cognitive tool."""
        try:
            if tool_name not in self.cognitive_tools.available_tools:
                return APIResponse(
                    success=False,
                    error=f"Tool '{tool_name}' not available. Available tools: {list(self.cognitive_tools.available_tools.keys())}"
                )
            
            result = await self.cognitive_tools.execute_tool(
                tool_name, content, parameters or {}
            )
            
            return APIResponse(
                success=True,
                data={
                    "tool": tool_name,
                    "result": result.content,
                    "confidence": result.confidence,
                    "processing_time": result.processing_time,
                    "metadata": result.metadata,
                    "reasoning_trace": result.reasoning_trace
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tool execution error: {str(e)}"
            )
    
    async def get_available_tools(self) -> APIResponse:
        """Get list of available cognitive tools."""
        try:
            tools_info = {}
            
            for tool_name, tool in self.cognitive_tools.available_tools.items():
                tools_info[tool_name] = {
                    "name": tool.name,
                    "description": tool.description,
                    "usage_count": self.cognitive_tools.tool_usage_count.get(tool_name, 0)
                }
            
            return APIResponse(
                success=True,
                data={
                    "available_tools": tools_info,
                    "total_tools": len(tools_info),
                    "tool_metrics": self.cognitive_tools.get_tool_metrics()
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting available tools: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Tools query error: {str(e)}"
            )
    
    async def analyze_reasoning_complexity(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Analyze the reasoning complexity of a query."""
        try:
            # Simple complexity analysis based on query characteristics
            complexity_factors = {
                "query_length": len(query),
                "context_richness": len(context) if context else 0,
                "question_complexity": self._analyze_question_complexity(query),
                "domain_specificity": self._analyze_domain_specificity(query)
            }
            
            # Calculate overall complexity score
            complexity_score = (
                min(1.0, complexity_factors["query_length"] / 500) * 0.2 +
                min(1.0, complexity_factors["context_richness"] / 10) * 0.2 +
                complexity_factors["question_complexity"] * 0.3 +
                complexity_factors["domain_specificity"] * 0.3
            )
            
            # Recommend reasoning approach
            if complexity_score < 0.3:
                recommended_approach = "simple_reasoning"
                recommended_tools = ["understand", "apply"]
            elif complexity_score < 0.6:
                recommended_approach = "structured_reasoning"
                recommended_tools = ["understand", "extract", "apply", "validate"]
            else:
                recommended_approach = "comprehensive_reasoning"
                recommended_tools = ["understand", "extract", "highlight", "apply", "validate"]
            
            return APIResponse(
                success=True,
                data={
                    "complexity_score": complexity_score,
                    "complexity_factors": complexity_factors,
                    "recommended_approach": recommended_approach,
                    "recommended_tools": recommended_tools,
                    "estimated_processing_time": complexity_score * 10  # Rough estimate
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing reasoning complexity: {str(e)}")
            return APIResponse(
                success=False,
                error=f"Complexity analysis error: {str(e)}"
            )
    
    def _analyze_question_complexity(self, query: str) -> float:
        """Analyze the complexity of the question/query."""
        complexity_indicators = [
            "analyze", "compare", "evaluate", "synthesize", "integrate",
            "explain why", "how does", "what if", "predict", "optimize"
        ]
        
        query_lower = query.lower()
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in query_lower)
        
        # Normalize to 0-1 scale
        return min(1.0, complexity_count / len(complexity_indicators))
    
    def _analyze_domain_specificity(self, query: str) -> float:
        """Analyze domain specificity of the query."""
        technical_domains = [
            "algorithm", "machine learning", "neural network", "database",
            "statistical", "mathematical", "scientific", "engineering",
            "programming", "software", "system", "architecture"
        ]
        
        query_lower = query.lower()
        domain_count = sum(1 for domain in technical_domains if domain in query_lower)
        
        # Normalize to 0-1 scale
        return min(1.0, domain_count / 5)  # Max 5 domain indicators
    
    # Synchronous wrapper methods
    def execute_reasoning_sequence_sync(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        complexity: str = "neural_system"
    ) -> APIResponse:
        """Synchronous version of execute_reasoning_sequence."""
        return asyncio.run(self.execute_reasoning_sequence(query, context, complexity))
    
    def execute_single_tool_sync(
        self,
        tool_name: str,
        content: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Synchronous version of execute_single_tool."""
        return asyncio.run(self.execute_single_tool(tool_name, content, parameters))