"""
Basic Usage Examples - Getting Started with Context Engineering
===============================================================

Simple examples demonstrating basic usage of the contextual engine
for common reasoning and processing tasks.
"""

import asyncio
from typing import Dict, Any

from ..core.engine import ContextualEngine
from ..core.config import ContextualConfig
from ..api.context import ContextAPI

class BasicUsageExamples:
    """Basic usage examples for the contextual engine."""
    
    def __init__(self):
        self.engine = ContextualEngine()
        self.api = ContextAPI()
    
    async def simple_reasoning_example(self):
        """Simple reasoning example."""
        print("=== Simple Reasoning Example ===")
        
        query = """
        What are the key factors to consider when designing a machine learning system 
        for a production environment?
        """
        
        result = await self.engine.reason(query)
        
        print(f"Query: {query.strip()}")
        print(f"Result: {result.result}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Components Used: {len(result.reasoning_trace)} reasoning steps")
        print()
        
        return result
    
    async def contextual_reasoning_example(self):
        """Reasoning with context example."""
        print("=== Contextual Reasoning Example ===")
        
        query = "How should we approach this optimization problem?"
        context = {
            "domain": "neural_networks",
            "constraints": ["memory_limited", "real_time_inference"],
            "objectives": ["accuracy", "speed", "efficiency"],
            "current_approach": "standard_backpropagation",
            "performance_metrics": {
                "accuracy": 0.87,
                "inference_time": "150ms",
                "memory_usage": "2.3GB"
            }
        }
        
        result = await self.engine.reason(query, context)
        
        print(f"Query: {query}")
        print(f"Context: {len(context)} context elements provided")
        print(f"Result: {result.result}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Field State: {len(result.field_state)} field elements")
        print()
        
        return result
    
    async def api_usage_example(self):
        """Using the API interface."""
        print("=== API Usage Example ===")
        
        query = "Explain the concept of attention mechanisms in deep learning."
        
        # Using the API interface
        api_result = await self.api.process(query)
        
        if api_result.success:
            print(f"Query: {query}")
            print(f"API Success: {api_result.success}")
            print(f"Result: {api_result.data['result']}")
            print(f"Confidence: {api_result.data['confidence']:.2f}")
            print(f"Request ID: {api_result.metadata['request_id']}")
        else:
            print(f"API Error: {api_result.error}")
        
        print()
        return api_result
    
    async def batch_processing_example(self):
        """Batch processing example."""
        print("=== Batch Processing Example ===")
        
        queries = [
            "What is machine learning?",
            "Explain neural networks.",
            "How do transformers work?",
            "What is reinforcement learning?"
        ]
        
        # Process batch through API
        api_result = await self.api.process_batch(queries)
        
        if api_result.success:
            results = api_result.data["results"]
            stats = api_result.data["batch_statistics"]
            
            print(f"Batch Size: {stats['total_items']}")
            print(f"Success Rate: {stats['success_rate']:.2%}")
            print(f"Average Processing Time: {stats['average_processing_time']:.2f}s")
            print()
            
            for result in results[:2]:  # Show first 2 results
                if result["success"]:
                    print(f"Query {result['index']}: {queries[result['index']]}")
                    print(f"Result: {result['result'][:200]}...")
                    print(f"Confidence: {result['confidence']:.2f}")
                    print()
        else:
            print(f"Batch Processing Error: {api_result.error}")
        
        return api_result
    
    async def streaming_example(self):
        """Streaming processing example."""
        print("=== Streaming Processing Example ===")
        
        query = """
        Provide a comprehensive analysis of the current state of artificial intelligence,
        including recent developments, challenges, and future prospects.
        """
        
        print(f"Query: {query.strip()}")
        print("Streaming Response:")
        
        stream_count = 0
        async for update in self.api.process_stream(query):
            if update.success:
                stream_count += 1
                if "status" in update.data:
                    print(f"  [{stream_count}] Status: {update.data['status']} - Phase: {update.data.get('phase', 'N/A')}")
                elif "result" in update.data:
                    print(f"  [Final] Result: {update.data['result'][:200]}...")
                    print(f"  [Final] Confidence: {update.data['confidence']:.2f}")
                    break
            else:
                print(f"  [Error] {update.error}")
                break
        
        print()
    
    async def engine_status_example(self):
        """Engine status monitoring example."""
        print("=== Engine Status Example ===")
        
        status_result = await self.api.get_engine_status()
        
        if status_result.success:
            status_data = status_result.data
            
            print(f"Engine Status: {status_data['engine_status']}")
            print(f"Active Components: {status_data['active_components']}")
            print(f"Total Requests: {status_data['request_count']}")
            
            # Performance metrics
            perf_metrics = status_data['performance_metrics']
            print(f"Performance Metrics Available: {len(perf_metrics)} categories")
            
            # Field state
            field_state = status_data['field_state']
            if field_state:
                print(f"Field State: {len(field_state)} field elements")
            else:
                print("Field State: No field data available")
                
            # Memory state  
            memory_state = status_data['memory_state']
            if memory_state:
                print(f"Memory State: {memory_state.get('memory_count', 0)} memories stored")
            else:
                print("Memory State: No memory data available")
        else:
            print(f"Status Error: {status_result.error}")
        
        print()
        return status_result
    
    def run_basic_examples(self):
        """Run all basic examples."""
        print("Context Engineering - Basic Usage Examples")
        print("=" * 50)
        
        async def run_examples():
            await self.simple_reasoning_example()
            await self.contextual_reasoning_example()
            await self.api_usage_example()
            await self.batch_processing_example() 
            await self.streaming_example()
            await self.engine_status_example()
            
            print("=== Basic Examples Completed ===")
        
        asyncio.run(run_examples())

# Convenience function to run basic examples
def run_basic_examples():
    """Run basic usage examples."""
    examples = BasicUsageExamples()
    examples.run_basic_examples()

if __name__ == "__main__":
    run_basic_examples()