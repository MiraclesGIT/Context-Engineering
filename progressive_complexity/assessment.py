"""
Complexity Assessment - Task Complexity Analysis
================================================

Analyzes task complexity and recommends optimal complexity levels
for efficient cognitive resource allocation.
"""

import asyncio
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .manager import ComplexityRecommendation

@dataclass
class ComplexityFactors:
    """Factors contributing to task complexity"""
    content_length: float
    vocabulary_complexity: float
    syntactic_complexity: float
    semantic_depth: float
    contextual_richness: float
    abstraction_requirement: float
    integration_demand: float

class ComplexityAssessment:
    """Assesses optimal complexity levels for tasks"""
    
    def __init__(self, config):
        self.config = config
        self.assessment_cache = {}
        
    async def assess_optimal_complexity(
        self, 
        content: str, 
        context: Dict[str, Any]
    ) -> 'ComplexityRecommendation':
        """Assess optimal complexity level for given task"""
        
        # Analyze complexity factors
        complexity_factors = await self._analyze_complexity_factors(content, context)
        
        # Calculate overall complexity score
        complexity_score = self._calculate_complexity_score(complexity_factors)
        
        # Recommend complexity level
        recommended_level = self._recommend_complexity_level(complexity_score, complexity_factors)
        
        # Calculate confidence in recommendation
        confidence = self._calculate_recommendation_confidence(
            complexity_factors, recommended_level
        )
        
        # Generate reasoning
        reasoning = self._generate_complexity_reasoning(
            complexity_factors, complexity_score, recommended_level
        )
        
        # Calculate resource requirements
        resource_requirements = self._calculate_resource_requirements(recommended_level)
        
        # Import here to avoid circular import
        from .manager import ComplexityRecommendation
        
        return ComplexityRecommendation(
            recommended_complexity=recommended_level,
            confidence=confidence,
            reasoning=reasoning,
            resource_requirements=resource_requirements
        )
    
    async def _analyze_complexity_factors(
        self, 
        content: str, 
        context: Dict[str, Any]
    ) -> ComplexityFactors:
        """Analyze various factors contributing to task complexity"""
        
        # Content length factor
        content_length = min(1.0, len(content) / 1000)  # Normalize to 1000 chars
        
        # Vocabulary complexity
        vocabulary_complexity = await self._assess_vocabulary_complexity(content)
        
        # Syntactic complexity
        syntactic_complexity = await self._assess_syntactic_complexity(content)
        
        # Semantic depth
        semantic_depth = await self._assess_semantic_depth(content, context)
        
        # Contextual richness
        contextual_richness = await self._assess_contextual_richness(context)
        
        # Abstraction requirement
        abstraction_requirement = await self._assess_abstraction_requirement(content)
        
        # Integration demand
        integration_demand = await self._assess_integration_demand(content, context)
        
        return ComplexityFactors(
            content_length=content_length,
            vocabulary_complexity=vocabulary_complexity,
            syntactic_complexity=syntactic_complexity,
            semantic_depth=semantic_depth,
            contextual_richness=contextual_richness,
            abstraction_requirement=abstraction_requirement,
            integration_demand=integration_demand
        )
    
    async def _assess_vocabulary_complexity(self, content: str) -> float:
        """Assess vocabulary complexity of content"""
        words = content.lower().split()
        
        if not words:
            return 0.0
        
        # Factors indicating vocabulary complexity
        long_words = sum(1 for word in words if len(word) > 6)
        technical_terms = sum(1 for word in words if self._is_technical_term(word))
        unique_words = len(set(words))
        
        # Calculate complexity score
        long_word_ratio = long_words / len(words)
        technical_ratio = technical_terms / len(words)
        vocabulary_diversity = unique_words / len(words)
        
        complexity = (long_word_ratio * 0.4) + (technical_ratio * 0.4) + (vocabulary_diversity * 0.2)
        
        return min(1.0, complexity)
    
    async def _assess_syntactic_complexity(self, content: str) -> float:
        """Assess syntactic complexity of content"""
        
        # Simple heuristics for syntactic complexity
        sentences = content.split('.')
        
        if not sentences:
            return 0.0
        
        # Average sentence length
        avg_sentence_length = len(content.split()) / len(sentences)
        sentence_length_complexity = min(1.0, avg_sentence_length / 20)  # Normalize to 20 words
        
        # Punctuation complexity (indicates complex structures)
        complex_punctuation = content.count(',') + content.count(';') + content.count(':')
        punctuation_complexity = min(1.0, complex_punctuation / len(sentences) / 3)
        
        # Nested structure indicators
        nesting_indicators = content.count('(') + content.count('[') + content.count('{')
        nesting_complexity = min(1.0, nesting_indicators / len(sentences))
        
        syntactic_complexity = (
            sentence_length_complexity * 0.5 +
            punctuation_complexity * 0.3 +
            nesting_complexity * 0.2
        )
        
        return syntactic_complexity
    
    async def _assess_semantic_depth(self, content: str, context: Dict[str, Any]) -> float:
        """Assess semantic depth and meaning complexity"""
        
        # Abstract concept indicators
        abstract_indicators = [
            'concept', 'theory', 'principle', 'philosophy', 'methodology',
            'framework', 'paradigm', 'perspective', 'interpretation', 'analysis'
        ]
        
        content_lower = content.lower()
        abstract_count = sum(1 for indicator in abstract_indicators if indicator in content_lower)
        
        # Reasoning indicators
        reasoning_indicators = [
            'because', 'therefore', 'thus', 'consequently', 'implies',
            'suggests', 'indicates', 'demonstrates', 'proves', 'shows'
        ]
        
        reasoning_count = sum(1 for indicator in reasoning_indicators if indicator in content_lower)
        
        # Meta-cognitive indicators
        meta_indicators = [
            'thinking', 'understanding', 'reasoning', 'cognition', 'awareness',
            'consciousness', 'reflection', 'introspection', 'analysis'
        ]
        
        meta_count = sum(1 for indicator in meta_indicators if indicator in content_lower)
        
        # Calculate semantic depth
        word_count = len(content.split())
        if word_count == 0:
            return 0.0
        
        abstract_ratio = abstract_count / word_count * 100  # Scale up
        reasoning_ratio = reasoning_count / word_count * 100
        meta_ratio = meta_count / word_count * 100
        
        semantic_depth = min(1.0, (abstract_ratio + reasoning_ratio + meta_ratio) * 0.5)
        
        return semantic_depth
    
    async def _assess_contextual_richness(self, context: Dict[str, Any]) -> float:
        """Assess richness and complexity of context"""
        
        if not context:
            return 0.0
        
        # Context size factor
        context_size = len(context)
        size_factor = min(1.0, context_size / 10)  # Normalize to 10 context items
        
        # Context depth factor (nested structures)
        depth_count = 0
        total_elements = 0
        
        for key, value in context.items():
            total_elements += 1
            if isinstance(value, dict):
                depth_count += 1
                total_elements += len(value)
            elif isinstance(value, list):
                depth_count += 1
                total_elements += len(value)
        
        depth_factor = depth_count / len(context) if context else 0.0
        richness_factor = min(1.0, total_elements / 20)  # Normalize to 20 total elements
        
        contextual_richness = (size_factor * 0.4) + (depth_factor * 0.3) + (richness_factor * 0.3)
        
        return contextual_richness
    
    async def _assess_abstraction_requirement(self, content: str) -> float:
        """Assess requirement for abstract reasoning"""
        
        abstraction_keywords = [
            'abstract', 'general', 'universal', 'pattern', 'model', 'framework',
            'structure', 'relationship', 'system', 'process', 'mechanism',
            'principle', 'rule', 'law', 'theory', 'hypothesis'
        ]
        
        content_lower = content.lower()
        abstraction_count = sum(1 for keyword in abstraction_keywords if keyword in content_lower)
        
        # Question words indicating abstraction needs
        abstract_questions = [
            'why', 'how', 'what if', 'suppose', 'imagine', 'consider',
            'analyze', 'evaluate', 'synthesize', 'generalize'
        ]
        
        question_count = sum(1 for question in abstract_questions if question in content_lower)
        
        word_count = len(content.split())
        if word_count == 0:
            return 0.0
        
        abstraction_ratio = (abstraction_count + question_count) / word_count * 50  # Scale up
        
        return min(1.0, abstraction_ratio)
    
    async def _assess_integration_demand(self, content: str, context: Dict[str, Any]) -> float:
        """Assess demand for integrating multiple sources/perspectives"""
        
        integration_indicators = [
            'combine', 'integrate', 'synthesize', 'merge', 'unify', 'connect',
            'relate', 'compare', 'contrast', 'balance', 'coordinate', 'align'
        ]
        
        content_lower = content.lower()
        integration_count = sum(1 for indicator in integration_indicators if indicator in content_lower)
        
        # Multiple source indicators
        source_indicators = [
            'according to', 'based on', 'from', 'considering', 'given',
            'taking into account', 'in light of', 'perspective', 'viewpoint'
        ]
        
        source_count = sum(1 for indicator in source_indicators if indicator in content_lower)
        
        # Context integration demand
        context_integration = len(context) / 5 if context else 0.0  # Normalize to 5 context items
        
        word_count = len(content.split())
        if word_count == 0:
            return min(1.0, context_integration)
        
        integration_ratio = (integration_count + source_count) / word_count * 50  # Scale up
        total_integration = min(1.0, integration_ratio + context_integration * 0.3)
        
        return total_integration
    
    def _is_technical_term(self, word: str) -> bool:
        """Check if a word is a technical term"""
        # Simplified technical term detection
        technical_suffixes = [
            'tion', 'sion', 'ment', 'ness', 'ity', 'ism', 'ology', 'ics', 'ing'
        ]
        
        return (len(word) > 8 or 
                any(word.endswith(suffix) for suffix in technical_suffixes) or
                word.isupper())
    
    def _calculate_complexity_score(self, factors: ComplexityFactors) -> float:
        """Calculate overall complexity score from factors"""
        
        # Weight different factors based on importance
        weights = {
            'content_length': 0.1,
            'vocabulary_complexity': 0.15,
            'syntactic_complexity': 0.15,
            'semantic_depth': 0.25,
            'contextual_richness': 0.15,
            'abstraction_requirement': 0.2,
            'integration_demand': 0.2
        }
        
        complexity_score = (
            factors.content_length * weights['content_length'] +
            factors.vocabulary_complexity * weights['vocabulary_complexity'] +
            factors.syntactic_complexity * weights['syntactic_complexity'] +
            factors.semantic_depth * weights['semantic_depth'] +
            factors.contextual_richness * weights['contextual_richness'] +
            factors.abstraction_requirement * weights['abstraction_requirement'] +
            factors.integration_demand * weights['integration_demand']
        )
        
        return complexity_score
    
    def _recommend_complexity_level(
        self, 
        complexity_score: float, 
        factors: ComplexityFactors
    ) -> str:
        """Recommend complexity level based on analysis"""
        
        # Define complexity thresholds
        if complexity_score < 0.2:
            return "atom"
        elif complexity_score < 0.35:
            return "molecule"
        elif complexity_score < 0.5:
            return "cell"
        elif complexity_score < 0.65:
            return "organ"
        elif complexity_score < 0.8:
            return "neural_system"
        else:
            return "neural_field"
    
    def _calculate_recommendation_confidence(
        self, 
        factors: ComplexityFactors, 
        recommended_level: str
    ) -> float:
        """Calculate confidence in the complexity recommendation"""
        
        # Base confidence from factor consistency
        factor_values = [
            factors.content_length, factors.vocabulary_complexity,
            factors.syntactic_complexity, factors.semantic_depth,
            factors.contextual_richness, factors.abstraction_requirement,
            factors.integration_demand
        ]
        
        # Calculate variance in factors
        mean_factor = sum(factor_values) / len(factor_values)
        variance = sum((x - mean_factor) ** 2 for x in factor_values) / len(factor_values)
        consistency = 1.0 - min(1.0, variance)
        
        # Adjust confidence based on extreme values
        extreme_penalty = 0.0
        if any(f > 0.9 for f in factor_values) or any(f < 0.1 for f in factor_values):
            extreme_penalty = 0.1
        
        confidence = max(0.3, consistency - extreme_penalty)
        
        return confidence
    
    def _generate_complexity_reasoning(
        self, 
        factors: ComplexityFactors, 
        complexity_score: float, 
        recommended_level: str
    ) -> str:
        """Generate human-readable reasoning for complexity recommendation"""
        
        reasoning_parts = []
        
        # Identify dominant factors
        factor_dict = {
            'content length': factors.content_length,
            'vocabulary complexity': factors.vocabulary_complexity,
            'syntactic complexity': factors.syntactic_complexity,
            'semantic depth': factors.semantic_depth,
            'contextual richness': factors.contextual_richness,
            'abstraction requirement': factors.abstraction_requirement,
            'integration demand': factors.integration_demand
        }
        
        # Sort factors by influence
        sorted_factors = sorted(factor_dict.items(), key=lambda x: x[1], reverse=True)
        top_factors = sorted_factors[:3]
        
        reasoning_parts.append(f"Complexity score: {complexity_score:.2f}")
        reasoning_parts.append(f"Recommended level: {recommended_level}")
        reasoning_parts.append("")
        reasoning_parts.append("Primary complexity drivers:")
        
        for factor_name, factor_value in top_factors:
            if factor_value > 0.3:
                intensity = "high" if factor_value > 0.7 else "moderate"
                reasoning_parts.append(f"- {factor_name}: {intensity} ({factor_value:.2f})")
        
        return "\n".join(reasoning_parts)
    
    def _calculate_resource_requirements(self, complexity_level: str) -> Dict[str, float]:
        """Calculate resource requirements for complexity level"""
        
        level_resources = {
            "atom": {"cognitive": 0.1, "memory": 0.1, "processing": 0.1},
            "molecule": {"cognitive": 0.2, "memory": 0.2, "processing": 0.2},
            "cell": {"cognitive": 0.4, "memory": 0.3, "processing": 0.4},
            "organ": {"cognitive": 0.6, "memory": 0.5, "processing": 0.6},
            "neural_system": {"cognitive": 0.8, "memory": 0.7, "processing": 0.8},
            "neural_field": {"cognitive": 1.0, "memory": 1.0, "processing": 1.0}
        }
        
        return level_resources.get(complexity_level, {"cognitive": 0.5, "memory": 0.5, "processing": 0.5})
    
    def reset(self):
        """Reset complexity assessment state"""
        self.assessment_cache = {}