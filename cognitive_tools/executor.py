"""
Cognitive Tool Executor - Execution Engine for Cognitive Tools
=============================================================

Handles the execution of cognitive tools with proper error handling,
timeout management, and result processing.
"""

import asyncio
import logging
from typing import Dict, Any
from ..core.base import ProcessingResult

class CognitiveToolExecutor:
    """Executes cognitive tools with proper orchestration and error handling"""
    
    def __init__(self):
        self.logger = logging.getLogger("CognitiveToolExecutor")
    
    async def execute_tool(
        self,
        tool,
        content: str,
        parameters: Dict[str, Any]
    ) -> ProcessingResult:
        """Execute a cognitive tool with error handling and timeout"""
        self.logger.debug(f"Executing cognitive tool: {tool.name}")
        
        try:
            # Execute tool with timeout
            result = await asyncio.wait_for(
                tool.execute(content, parameters),
                timeout=30.0  # 30 second timeout
            )
            
            self.logger.debug(f"✓ Tool {tool.name} executed successfully")
            return result
            
        except asyncio.TimeoutError:
            self.logger.error(f"Tool {tool.name} execution timed out")
            return ProcessingResult(
                content=f"Tool {tool.name} execution timed out",
                confidence=0.0,
                processing_time=30.0,
                metadata={"error": "timeout", "tool": tool.name},
                reasoning_trace=[{"error": "timeout"}]
            )
            
        except Exception as e:
            self.logger.error(f"Error executing tool {tool.name}: {str(e)}")
            return ProcessingResult(
                content=f"Error in tool {tool.name}: {str(e)}",
                confidence=0.0,
                processing_time=0.0,
                metadata={"error": str(e), "tool": tool.name},
                reasoning_trace=[{"error": str(e)}]
            )