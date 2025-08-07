"""
Memory Operations Examples - Memory System Demonstrations
=========================================================

Examples demonstrating memory storage, retrieval, consolidation,
and management using the MEM1 framework.
"""

import asyncio
import time
from typing import Dict, Any

from ..api.memory import MemoryAPI
from ..core.config import MemoryConfig

class MemoryOperationsExamples:
    """Examples for memory operations and management."""
    
    def __init__(self):
        # Configure memory system
        config = MemoryConfig()
        config.consolidation_frequency = 3  # More frequent consolidation for demo
        config.memory_budget = 50  # Smaller budget to see management in action
        config.efficiency_target = 0.8
        
        self.memory_api = MemoryAPI(config)
    
    async def basic_memory_operations_example(self):
        """Basic memory storage and retrieval."""
        print("=== Basic Memory Operations Example ===")
        
        # Store some memories
        knowledge_items = [
            {
                "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn and improve from data without being explicitly programmed.",
                "priority": 0.9
            },
            {
                "content": "Deep learning uses artificial neural networks with multiple layers to model and understand complex patterns in data.",
                "priority": 0.8
            },
            {
                "content": "Natural language processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language.",
                "priority": 0.7
            },
            {
                "content": "Computer vision enables machines to interpret and make decisions based on visual data from the world.",
                "priority": 0.7
            },
            {
                "content": "Reinforcement learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize rewards.",
                "priority": 0.6
            }
        ]
        
        print("Storing knowledge in memory...")
        stored_memories = []
        
        for item in knowledge_items:
            result = await self.memory_api.store_memory(
                item["content"],
                context={"domain": "ai_ml", "type": "definition"},
                priority=item["priority"]
            )
            
            if result.success:
                stored_memories.append(result.data["memory_id"])
                print(f"✓ Stored: {item['content'][:60]}... (Priority: {item['priority']})")
            else:
                print(f"✗ Failed to store: {result.error}")
        
        print(f"\nStored {len(stored_memories)} memories successfully.")
        
        # Retrieve memories based on queries
        queries = [
            "What is machine learning?",
            "Explain neural networks and deep learning", 
            "How does reinforcement learning work?"
        ]
        
        print("\nRetrieving memories based on queries:")
        for query in queries:
            retrieval_result = await self.memory_api.retrieve_memories(query, max_results=3)
            
            if retrieval_result.success:
                memories = retrieval_result.data["memories"]
                stats = retrieval_result.data["retrieval_stats"]
                
                print(f"\nQuery: {query}")
                print(f"Retrieved {len(memories)} memories (Avg Relevance: {stats['average_relevance']:.2f})")
                
                for memory in memories[:2]:  # Show top 2
                    print(f"  • {memory['content'][:80]}... (Relevance: {memory['relevance']:.2f})")
            else:
                print(f"Retrieval failed: {retrieval_result.error}")
        
        print()
    
    async def memory_consolidation_example(self):
        """Memory consolidation and efficiency optimization."""
        print("=== Memory Consolidation Example ===")
        
        # Add more memories to trigger consolidation
        learning_experiences = [
            "Implemented a convolutional neural network for image classification with 94% accuracy on CIFAR-10 dataset.",
            "Used transfer learning with ResNet to achieve state-of-the-art results on custom dataset with only 1000 training samples.",
            "Applied data augmentation techniques including rotation, scaling, and color jittering to improve model generalization.",
            "Experimented with different optimizers: Adam achieved faster convergence than SGD for our specific use case.",
            "Discovered that batch normalization significantly improved training stability and reduced overfitting.",
            "Learning rate scheduling with cosine annealing provided better final accuracy than constant learning rate.",
            "Dropout with rate 0.3 proved optimal for preventing overfitting in our fully connected layers.",
            "Ensemble methods combining CNN and Vision Transformer improved accuracy by 2.3%."
        ]
        
        print("Adding learning experiences to memory...")
        for i, experience in enumerate(learning_experiences):
            await self.memory_api.store_memory(
                experience,
                context={"type": "experience", "domain": "deep_learning", "project": f"experiment_{i}"},
                priority=0.6 + (i % 3) * 0.1  # Varying priorities
            )
        
        # Check memory state before consolidation
        state_before = await self.memory_api.get_memory_state()
        if state_before.success:
            before_data = state_before.data
            print(f"Before consolidation: {before_data['memory_state']['memory_count']} memories")
            print(f"Memory efficiency: {before_data['memory_state']['memory_efficiency']:.2f}")
            print(f"Budget utilization: {before_data['memory_budget']['utilization']:.2%}")
        
        # Trigger consolidation
        print("\nTriggering memory consolidation...")
        consolidation_result = await self.memory_api.consolidate_memories()
        
        if consolidation_result.success:
            consolidation_data = consolidation_result.data["consolidation_results"]
            
            print(f"Consolidation completed:")
            print(f"  • Insights extracted: {consolidation_data['insights_extracted']}")
            print(f"  • Memories consolidated: {consolidation_data['memories_consolidated']}")  
            print(f"  • Memories pruned: {consolidation_data['memories_pruned']}")
            print(f"  • Efficiency score: {consolidation_data['efficiency_score']:.2f}")
            
            print("\nKey insights extracted:")
            for insight in consolidation_data["insights"][:3]:  # Show top 3 insights
                print(f"  • {insight}")
            
            # Check state after consolidation
            after_state = consolidation_result.data["memory_state_after"]
            print(f"\nAfter consolidation: {after_state['memory_count']} memories")
            print(f"New efficiency: {after_state['memory_efficiency']:.2f}")
        else:
            print(f"Consolidation failed: {consolidation_result.error}")
        
        print()
    
    async def memory_analytics_example(self):
        """Memory system analytics and insights."""
        print("=== Memory Analytics Example ===")
        
        analytics_result = await self.memory_api.get_memory_analytics()
        
        if analytics_result.success:
            analytics = analytics_result.data["analytics"]
            
            print("Memory System Analytics:")
            
            # Memory distribution analysis
            if "memory_distribution" in analytics:
                dist = analytics["memory_distribution"]
                if "total_memories" in dist:
                    print(f"  Total memories: {dist['total_memories']}")
                    print(f"  High-value memories: {dist.get('high_value_memories', 0)}")
                    print(f"  Low-value memories: {dist.get('low_value_memories', 0)}")
                    
                    if "reasoning_value_stats" in dist:
                        stats = dist["reasoning_value_stats"]
                        print(f"  Average reasoning value: {stats['average']:.2f}")
                        print(f"  Value range: {stats['min']:.2f} - {stats['max']:.2f}")
            
            # Access patterns
            if "access_patterns" in analytics:
                access = analytics["access_patterns"]
                if "total_accesses" in access:
                    print(f"\n  Memory Access Patterns:")
                    print(f"    Total accesses: {access['total_accesses']}")
                    print(f"    Average accesses per memory: {access['average_accesses']:.1f}")
                    print(f"    Never accessed: {access['never_accessed']}")
                    print(f"    Frequently accessed: {access['frequently_accessed']}")
            
            # Efficiency trends
            if "efficiency_trends" in analytics:
                efficiency = analytics["efficiency_trends"]
                print(f"\n  Efficiency Analysis:")
                print(f"    Current efficiency: {efficiency['current_efficiency']:.2f}")
                print(f"    Target efficiency: {efficiency['target_efficiency']:.2f}")
                print(f"    Efficiency gap: {efficiency['efficiency_gap']:.2f}")
            
            # Recommendations
            if "recommendations" in analytics:
                recommendations = analytics["recommendations"]
                if recommendations:
                    print(f"\n  Recommendations:")
                    for rec in recommendations:
                        print(f"    • {rec}")
                else:
                    print(f"\n  No specific recommendations - system performing well!")
        
        else:
            print(f"Analytics failed: {analytics_result.error}")
        
        print()
    
    async def intelligent_retrieval_example(self):
        """Intelligent memory retrieval with context."""
        print("=== Intelligent Memory Retrieval Example ===")
        
        # Store domain-specific knowledge
        domains = {
            "computer_vision": [
                "Image classification involves training models to categorize images into predefined classes.",
                "Object detection not only classifies objects but also localizes them with bounding boxes.",
                "Semantic segmentation assigns a class label to every pixel in an image."
            ],
            "nlp": [
                "Tokenization is the process of breaking text into individual words or subwords.",
                "Word embeddings represent words as dense vectors in a high-dimensional space.",
                "Attention mechanisms allow models to focus on relevant parts of input sequences."
            ],
            "reinforcement_learning": [
                "Q-learning is a model-free reinforcement learning algorithm.",
                "Policy gradient methods optimize the policy directly rather than learning value functions.",
                "Actor-critic methods combine value function approximation with policy optimization."
            ]
        }
        
        # Store memories with domain context
        print("Storing domain-specific knowledge...")
        for domain, knowledge_list in domains.items():
            for knowledge in knowledge_list:
                await self.memory_api.store_memory(
                    knowledge,
                    context={"domain": domain, "type": "knowledge"},
                    priority=0.8
                )
        
        # Test context-aware retrieval
        test_scenarios = [
            {
                "query": "How do you identify objects in images?",
                "context": {"domain": "computer_vision", "task": "object_detection"}
            },
            {
                "query": "What are the key components of modern language models?", 
                "context": {"domain": "nlp", "application": "text_generation"}
            },
            {
                "query": "How does learning work in interactive environments?",
                "context": {"domain": "reinforcement_learning", "environment": "games"}
            }
        ]
        
        print("\nTesting context-aware retrieval:")
        for scenario in test_scenarios:
            print(f"\nQuery: {scenario['query']}")
            print(f"Context: {scenario['context']}")
            
            retrieval_result = await self.memory_api.retrieve_memories(
                scenario["query"],
                max_results=2,
                context=scenario["context"]
            )
            
            if retrieval_result.success:
                memories = retrieval_result.data["memories"]
                print(f"Retrieved {len(memories)} relevant memories:")
                
                for memory in memories:
                    print(f"  • {memory['content']} (Relevance: {memory['relevance']:.2f})")
            else:
                print(f"  Retrieval failed: {retrieval_result.error}")
        
        print()
    
    async def memory_lifecycle_example(self):
        """Complete memory lifecycle demonstration."""
        print("=== Memory Lifecycle Example ===")
        
        # Start with empty memory
        print("Starting with fresh memory system...")
        await self.memory_api.clear_memories()
        
        # Phase 1: Learning phase - store various types of information
        print("\nPhase 1: Learning Phase")
        learning_content = [
            ("fact", "Python is a high-level programming language known for its simplicity.", 0.7),
            ("experience", "Debugging a memory leak took 3 hours but taught me about profiling tools.", 0.9),
            ("insight", "Code readability is more important than premature optimization.", 0.8),
            ("procedure", "To deploy: 1) Run tests, 2) Build image, 3) Push to registry, 4) Update deployment.", 0.6),
            ("concept", "Microservices architecture promotes loose coupling and independent scaling.", 0.7)
        ]
        
        for content_type, content, priority in learning_content:
            result = await self.memory_api.store_memory(
                content,
                context={"type": content_type, "phase": "learning"},
                priority=priority
            )
            if result.success:
                print(f"  Learned ({content_type}): {content[:50]}...")
        
        # Phase 2: Application phase - retrieve and use knowledge
        print("\nPhase 2: Application Phase")
        application_queries = [
            "What programming language should I use?",
            "How do I debug performance issues?", 
            "What's the best architecture for scalable systems?"
        ]
        
        for query in application_queries:
            retrieval_result = await self.memory_api.retrieve_memories(query, max_results=2)
            if retrieval_result.success:
                memories = retrieval_result.data["memories"]
                print(f"  Query: {query}")
                print(f"  Retrieved: {len(memories)} relevant memories")
        
        # Phase 3: Consolidation phase - optimize memory system
        print("\nPhase 3: Consolidation Phase")
        consolidation_result = await self.memory_api.consolidate_memories()
        if consolidation_result.success:
            insights = consolidation_result.data["consolidation_results"]["insights"]
            print(f"  Extracted {len(insights)} insights from experiences")
            
        # Phase 4: Analysis phase - understand memory patterns
        print("\nPhase 4: Analysis Phase")
        analytics_result = await self.memory_api.get_memory_analytics()
        if analytics_result.success:
            memory_state = analytics_result.data["memory_state"]
            print(f"  Final memory count: {memory_state['memory_count']}")
            print(f"  System efficiency: {memory_state['memory_efficiency']:.2f}")
        
        print("\nMemory lifecycle demonstration completed!")
        print()
    
    def run_memory_examples(self):
        """Run all memory operation examples."""
        print("Context Engineering - Memory Operations Examples")
        print("=" * 52)
        
        async def run_examples():
            await self.basic_memory_operations_example()
            await self.memory_consolidation_example()
            await self.memory_analytics_example()
            await self.intelligent_retrieval_example()
            await self.memory_lifecycle_example()
            
            print("=== Memory Operations Examples Completed ===")
        
        asyncio.run(run_examples())

# Convenience function to run memory examples
def run_memory_examples():
    """Run memory operations examples."""
    examples = MemoryOperationsExamples()
    examples.run_memory_examples()

if __name__ == "__main__":
    run_memory_examples()