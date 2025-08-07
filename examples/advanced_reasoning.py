"""
Advanced Reasoning Examples - Complex Cognitive Processing
==========================================================

Advanced examples demonstrating sophisticated reasoning capabilities
using cognitive tools, symbolic processing, and integrated frameworks.
"""

import asyncio
from typing import Dict, Any

from ..core.engine import ContextualEngine
from ..cognitive_tools import CognitiveToolsManager
from ..symbolic_processing import SymbolicProcessor
from ..api.reasoning import ReasoningAPI
from ..core.config import ContextualConfig

class AdvancedReasoningExamples:
    """Advanced reasoning examples for complex cognitive tasks."""
    
    def __init__(self):
        # Initialize with enhanced configuration
        config = ContextualConfig()
        config.cognitive_tools.verification_enabled = True
        config.symbolic_processing.abstraction_depth = 4
        config.progressive_complexity.auto_scaling = True
        
        self.engine = ContextualEngine(config)
        self.reasoning_api = ReasoningAPI()
    
    async def multi_step_reasoning_example(self):
        """Multi-step reasoning with cognitive tools."""
        print("=== Multi-Step Reasoning Example ===")
        
        complex_problem = """
        A technology company is experiencing a 40% increase in customer complaints about
        their mobile app's performance. The app has 2 million active users, processes 
        500,000 transactions daily, and uses a microservices architecture with 12 services.
        Recent changes include: new recommendation engine (deployed 2 weeks ago), 
        database migration to cloud (completed 1 month ago), and new UI redesign 
        (launched 3 weeks ago). How should they systematically diagnose and resolve this issue?
        """
        
        context = {
            "domain": "software_engineering",
            "urgency": "high",
            "resources": {
                "engineering_team": 15,
                "budget": "$50000",
                "timeline": "2_weeks"
            },
            "constraints": [
                "minimal_downtime",
                "preserve_user_data", 
                "maintain_transaction_integrity"
            ]
        }
        
        result = await self.reasoning_api.execute_reasoning_sequence(
            complex_problem,
            context,
            complexity="neural_field"
        )
        
        if result.success:
            reasoning_data = result.data
            
            print(f"Problem: {complex_problem.strip()[:200]}...")
            print(f"Tools Used: {reasoning_data['tools_used']}")
            print(f"Verification Passed: {reasoning_data['verification_passed']}")
            print(f"Overall Confidence: {reasoning_data['confidence_score']:.2f}")
            print()
            
            print("Reasoning Steps:")
            for i, step in enumerate(reasoning_data['reasoning_trace'], 1):
                print(f"  {i}. {step['tool']}: {step.get('output', step.get('result', 'N/A'))[:150]}...")
                print(f"     Confidence: {step.get('confidence', 0):.2f}")
            
            print(f"\nFinal Solution:\n{reasoning_data['result']}")
        else:
            print(f"Reasoning Error: {result.error}")
        
        print()
        return result
    
    async def symbolic_processing_example(self):
        """Symbolic processing and abstraction example."""
        print("=== Symbolic Processing Example ===")
        
        abstract_problem = """
        Consider a system where entities can form dynamic relationships that evolve over time.
        Each relationship has strength, direction, and temporal characteristics. Entities can
        join groups, influence each other, and create emergent behaviors. How would you model
        the fundamental principles governing such a system?
        """
        
        context = {
            "abstraction_focus": "relationships",
            "modeling_approach": "mathematical",
            "emergence_patterns": ["network_effects", "feedback_loops", "phase_transitions"],
            "temporal_dynamics": True
        }
        
        # Use symbolic processor directly for detailed control
        symbolic_result = await self.engine.symbolic_processor.three_stage_process(
            abstract_problem,
            context
        )
        
        print(f"Problem: {abstract_problem.strip()[:200]}...")
        print(f"Symbolic Variables Generated: {len(symbolic_result.variables)}")
        print(f"Patterns Identified: {len(symbolic_result.patterns)}")
        print(f"Abstraction Depth: {symbolic_result.abstraction_depth}")
        print(f"Overall Confidence: {symbolic_result.confidence:.2f}")
        print()
        
        print("Symbolic Variables:")
        for var in symbolic_result.variables[:3]:  # Show first 3 variables
            print(f"  {var.symbol}: {var.relationships[:50]}...")
            print(f"    Abstraction Level: {var.abstraction_level}, Confidence: {var.confidence:.2f}")
        
        print()
        print("Identified Patterns:")
        for pattern in symbolic_result.patterns[:2]:  # Show first 2 patterns
            print(f"  Pattern: {pattern.pattern}")
            print(f"    Rule: {pattern.rule}")
            print(f"    Generalization: {pattern.generalization[:100]}...")
            print(f"    Confidence: {pattern.confidence:.2f}")
        
        print(f"\nConcrete Solution:\n{symbolic_result.concrete_result}")
        print()
        
        return symbolic_result
    
    async def complexity_scaling_example(self):
        """Progressive complexity scaling example."""
        print("=== Complexity Scaling Example ===")
        
        # Start with simple problem
        simple_query = "What is 2 + 2?"
        
        # Medium complexity problem
        medium_query = """
        Explain how to optimize a binary search algorithm for better cache performance
        in modern CPU architectures.
        """
        
        # Complex problem
        complex_query = """
        Design a distributed consensus algorithm that can handle Byzantine failures
        in a network of 100+ nodes while maintaining high throughput and low latency.
        Consider network partitions, message delays, and malicious actors.
        """
        
        queries = [
            ("Simple", simple_query),
            ("Medium", medium_query), 
            ("Complex", complex_query)
        ]
        
        for complexity_label, query in queries:
            print(f"\n--- {complexity_label} Query ---")
            
            # Let the engine auto-scale complexity
            result = await self.engine.reason(query, {})
            
            print(f"Query: {query[:100]}...")
            print(f"Processing Time: {result.processing_time:.2f}s")
            print(f"Confidence: {result.confidence_score:.2f}")
            print(f"Reasoning Steps: {len(result.reasoning_trace)}")
            
            # Show complexity metrics if available
            if result.performance_metrics:
                print(f"Performance Metrics: {len(result.performance_metrics)} categories")
        
        print()
    
    async def meta_reasoning_example(self):
        """Meta-reasoning about reasoning processes."""
        print("=== Meta-Reasoning Example ===")
        
        meta_query = """
        Analyze the reasoning process itself: When facing a complex problem, how should
        an AI system decide which reasoning strategies to employ? Consider factors like
        problem type, available context, time constraints, and confidence requirements.
        """
        
        context = {
            "reasoning_context": {
                "available_strategies": [
                    "deductive_reasoning",
                    "inductive_reasoning", 
                    "abductive_reasoning",
                    "analogical_reasoning",
                    "causal_reasoning"
                ],
                "constraints": {
                    "time_limit": "flexible",
                    "accuracy_requirement": "high",
                    "explainability": "required"
                }
            },
            "meta_level": True,
            "self_reflection": True
        }
        
        result = await self.engine.reason(meta_query, context)
        
        print(f"Meta-Query: {meta_query.strip()[:200]}...")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Confidence: {result.confidence_score:.2f}")
        print()
        
        print("Meta-Reasoning Analysis:")
        print(result.result)
        
        # Analyze the reasoning trace itself
        print(f"\nReasoning Trace Analysis:")
        print(f"Total reasoning steps: {len(result.reasoning_trace)}")
        
        for i, step in enumerate(result.reasoning_trace[:3], 1):
            print(f"  Step {i}: {step.get('phase', 'Unknown phase')}")
            if 'confidence' in step:
                print(f"    Confidence: {step['confidence']:.2f}")
        
        print()
        return result
    
    async def analogical_reasoning_example(self):
        """Analogical reasoning example."""
        print("=== Analogical Reasoning Example ===")
        
        analogical_query = """
        The human brain processes information through billions of interconnected neurons.
        How is this similar to modern distributed computing systems, and what can we learn
        from this analogy to improve distributed system design?
        """
        
        context = {
            "analogy_focus": "structural_and_functional",
            "domains": {
                "source": "neuroscience",
                "target": "distributed_computing"
            },
            "mapping_dimensions": [
                "information_processing",
                "network_topology",
                "fault_tolerance", 
                "adaptive_behavior",
                "emergence"
            ]
        }
        
        result = await self.engine.reason(analogical_query, context)
        
        print(f"Analogical Query: {analogical_query.strip()[:200]}...")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Confidence: {result.confidence_score:.2f}")
        print()
        
        print("Analogical Analysis:")
        print(result.result)
        
        # Check if field resonance detected similar patterns
        if result.field_state:
            field_energy = result.field_state.get('field_energy', 0)
            print(f"\nField Analysis:")
            print(f"Field Energy: {field_energy:.2f}")
            print(f"Resonance detected: {'Yes' if field_energy > 1.0 else 'No'}")
        
        print()
        return result
    
    async def complexity_analysis_example(self):
        """Reasoning complexity analysis example."""
        print("=== Complexity Analysis Example ===")
        
        test_queries = [
            "What is the weather like today?",
            "Explain quantum entanglement and its applications in quantum computing.",
            "Design a comprehensive strategy for transitioning a large organization to sustainable practices while maintaining profitability and stakeholder satisfaction."
        ]
        
        print("Analyzing reasoning complexity for different query types:")
        print()
        
        for i, query in enumerate(test_queries, 1):
            complexity_result = await self.reasoning_api.analyze_reasoning_complexity(query)
            
            if complexity_result.success:
                analysis = complexity_result.data
                
                print(f"Query {i}: {query[:80]}...")
                print(f"Complexity Score: {analysis['complexity_score']:.2f}")
                print(f"Recommended Approach: {analysis['recommended_approach']}")
                print(f"Recommended Tools: {analysis['recommended_tools']}")
                print(f"Estimated Processing Time: {analysis['estimated_processing_time']:.1f}s")
                
                factors = analysis['complexity_factors']
                print("Contributing Factors:")
                for factor, value in factors.items():
                    if value > 0:
                        print(f"  {factor}: {value:.2f}")
                print()
            else:
                print(f"Error analyzing query {i}: {complexity_result.error}")
        
        return complexity_result
    
    def run_advanced_examples(self):
        """Run all advanced reasoning examples."""
        print("Context Engineering - Advanced Reasoning Examples")
        print("=" * 55)
        
        async def run_examples():
            await self.multi_step_reasoning_example()
            await self.symbolic_processing_example()
            await self.complexity_scaling_example()
            await self.meta_reasoning_example()
            await self.analogical_reasoning_example()
            await self.complexity_analysis_example()
            
            print("=== Advanced Reasoning Examples Completed ===")
        
        asyncio.run(run_examples())

# Convenience function to run advanced examples
def run_advanced_examples():
    """Run advanced reasoning examples."""
    examples = AdvancedReasoningExamples()
    examples.run_advanced_examples()

if __name__ == "__main__":
    run_advanced_examples()