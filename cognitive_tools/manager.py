"""
Cognitive Tools Manager - IBM Zurich Implementation
===================================================

Manages and orchestrates cognitive tools for structured reasoning operations.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ..core.base import BaseToolProcessor, ProcessingResult
from .tools import UnderstandTool, ExtractTool, HighlightTool, ApplyTool, ValidateTool
from .executor import CognitiveToolExecutor

@dataclass
class CognitiveReasoningResult:
    """Result from cognitive reasoning sequence"""
    result: str
    reasoning_trace: List[Dict[str, Any]]
    tools_used: List[str]
    verification_passed: bool
    confidence_score: float

class CognitiveToolsManager(BaseToolProcessor):
    """
    Manager for IBM Zurich Cognitive Tools framework.
    
    Implements structured reasoning through modular cognitive operations:
    - Understand: Comprehend the problem and requirements
    - Extract: Identify and extract relevant information
    - Highlight: Emphasize key relationships and patterns
    - Apply: Execute appropriate reasoning techniques  
    - Validate: Verify reasoning steps and conclusions
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.executor = CognitiveToolExecutor()
        
        # Initialize cognitive tools
        self._initialize_tools()
        
        self.logger = logging.getLogger("CognitiveToolsManager")
        self.logger.info("IBM Zurich Cognitive Tools framework initialized")
    
    def _initialize_tools(self):
        """Initialize all cognitive tools"""
        # Register core cognitive tools
        self.register_tool("understand", UnderstandTool())
        self.register_tool("extract", ExtractTool())
        self.register_tool("highlight", HighlightTool())
        self.register_tool("apply", ApplyTool())
        self.register_tool("validate", ValidateTool())
        
        self.logger.info(f"Registered {len(self.available_tools)} cognitive tools")
    
    async def process(self, content: str, context: Dict[str, Any]) -> ProcessingResult:
        """Process content using cognitive tools"""
        start_time = asyncio.get_event_loop().time()
        
        # Execute standard cognitive reasoning sequence
        result = await self.execute_reasoning_sequence(
            content, context, complexity="neural_system"
        )
        
        processing_time = asyncio.get_event_loop().time() - start_time
        self._record_processing(processing_time)
        
        return ProcessingResult(
            content=result.result,
            confidence=result.confidence_score,
            processing_time=processing_time,
            metadata={"tools_used": result.tools_used},
            reasoning_trace=result.reasoning_trace
        )
    
    async def execute_reasoning_sequence(
        self,
        query: str,
        context: Dict[str, Any],
        complexity: str = "neural_system"
    ) -> CognitiveReasoningResult:
        """
        Execute structured reasoning sequence using cognitive tools.
        
        Args:
            query: The query or problem to reason about
            context: Contextual information
            complexity: Target complexity level
            
        Returns:
            CognitiveReasoningResult with reasoning trace
        """
        self.logger.info("Executing cognitive reasoning sequence...")
        
        reasoning_trace = []
        tools_used = []
        cumulative_context = context.copy()
        cumulative_context["original_query"] = query
        
        # Phase 1: Understand
        understand_result = await self.execute_tool(
            "understand", query, {"context": cumulative_context}
        )
        reasoning_trace.append({
            "tool": "understand",
            "input": query,
            "output": understand_result.content,
            "confidence": understand_result.confidence
        })
        tools_used.append("understand")
        cumulative_context["understanding"] = understand_result.content
        
        # Phase 2: Extract
        extract_result = await self.execute_tool(
            "extract", query, {"context": cumulative_context}
        )
        reasoning_trace.append({
            "tool": "extract", 
            "input": query,
            "output": extract_result.content,
            "confidence": extract_result.confidence
        })
        tools_used.append("extract")
        cumulative_context["extracted_info"] = extract_result.content
        
        # Phase 3: Highlight
        highlight_result = await self.execute_tool(
            "highlight", query, {"context": cumulative_context}
        )
        reasoning_trace.append({
            "tool": "highlight",
            "input": query, 
            "output": highlight_result.content,
            "confidence": highlight_result.confidence
        })
        tools_used.append("highlight")
        cumulative_context["key_insights"] = highlight_result.content
        
        # Phase 4: Apply
        apply_result = await self.execute_tool(
            "apply", query, {"context": cumulative_context}
        )
        reasoning_trace.append({
            "tool": "apply",
            "input": query,
            "output": apply_result.content, 
            "confidence": apply_result.confidence
        })
        tools_used.append("apply")
        cumulative_context["reasoning_result"] = apply_result.content
        
        # Phase 5: Validate (if enabled)
        verification_passed = True
        if self.config.verification_enabled:
            validate_result = await self.execute_tool(
                "validate", apply_result.content, {"context": cumulative_context}
            )
            reasoning_trace.append({
                "tool": "validate",
                "input": apply_result.content,
                "output": validate_result.content,
                "confidence": validate_result.confidence
            })
            tools_used.append("validate")
            verification_passed = validate_result.confidence > 0.7
        
        # Calculate overall confidence
        confidence_scores = [step["confidence"] for step in reasoning_trace]
        overall_confidence = sum(confidence_scores) / len(confidence_scores)
        
        self.logger.info(f"✓ Cognitive reasoning completed. Tools used: {', '.join(tools_used)}")
        
        return CognitiveReasoningResult(
            result=apply_result.content,
            reasoning_trace=reasoning_trace,
            tools_used=tools_used,
            verification_passed=verification_passed,
            confidence_score=overall_confidence
        )
    
    async def execute_tool(
        self,
        tool_name: str,
        content: str,
        parameters: Dict[str, Any]
    ) -> ProcessingResult:
        """Execute a specific cognitive tool"""
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not available")
        
        tool = self.available_tools[tool_name]
        self.tool_usage_count[tool_name] += 1
        
        # Execute tool through executor
        result = await self.executor.execute_tool(tool, content, parameters)
        
        return result
    
    def reset(self):
        """Reset cognitive tools manager state"""
        self.tool_usage_count = {tool: 0 for tool in self.available_tools.keys()}
        self.processing_count = 0
        self.total_processing_time = 0.0
        self.last_processing_time = 0.0
        
        self.logger.info("Cognitive tools manager state reset")