"""
Abstraction Engine - Stage 1 of Princeton ICML Architecture
===========================================================

Implements symbol abstraction heads that convert input tokens to 
abstract variables based on relationships between tokens.
"""

import asyncio
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass
from collections import defaultdict

if TYPE_CHECKING:
    from .manager import SymbolicVariable

@dataclass
class AbstractionResult:
    """Result from symbol abstraction stage"""
    variables: List['SymbolicVariable']
    relationships: Dict[str, List[str]]
    confidence: float
    max_depth: int

class AbstractionEngine:
    """Engine for converting tokens to abstract symbolic variables"""
    
    def __init__(self, config):
        self.config = config
        self.abstraction_cache = {}  # Cache for repeated abstractions
        
    async def abstract_symbols(
        self, 
        content: str, 
        context: Dict[str, Any],
        focus: str = "relationships"
    ) -> AbstractionResult:
        """Abstract symbols from input content"""
        
        # Tokenize and analyze content
        tokens = self._tokenize_content(content)
        
        # Identify entities and concepts
        entities = await self._identify_entities(tokens, context)
        
        # Extract relationships
        relationships = await self._extract_relationships(tokens, entities, focus)
        
        # Generate abstract variables
        variables = await self._generate_abstract_variables(entities, relationships)
        
        # Calculate abstraction confidence
        confidence = self._calculate_abstraction_confidence(variables, relationships)
        
        # Determine abstraction depth
        max_depth = max((var.abstraction_level for var in variables), default=1)
        
        return AbstractionResult(
            variables=variables,
            relationships=relationships,
            confidence=confidence,
            max_depth=max_depth
        )
    
    def _tokenize_content(self, content: str) -> List[str]:
        """Tokenize content into meaningful units"""
        # Enhanced tokenization that preserves important structures
        import re
        
        # Split on whitespace and punctuation, but preserve important phrases
        tokens = re.findall(r'\b\w+\b|[.,!?;:]', content.lower())
        
        # Filter out stop words and very short tokens
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
        }
        
        meaningful_tokens = [
            token for token in tokens 
            if len(token) > 2 and token not in stop_words
        ]
        
        return meaningful_tokens
    
    async def _identify_entities(self, tokens: List[str], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify entities and concepts in the tokens"""
        entities = []
        entity_types = {
            'concept': [],
            'action': [], 
            'attribute': [],
            'relation': []
        }
        
        # Simple entity classification based on patterns
        action_indicators = ['ing', 'ed', 'ly']
        concept_indicators = ['tion', 'ness', 'ity', 'ism']
        
        for token in tokens:
            entity = {
                'token': token,
                'type': 'concept',  # default
                'importance': self._calculate_token_importance(token, context)
            }
            
            # Classify entity type based on suffixes and context
            if any(token.endswith(suffix) for suffix in action_indicators):
                entity['type'] = 'action'
                entity_types['action'].append(entity)
            elif any(token.endswith(suffix) for suffix in concept_indicators):
                entity['type'] = 'concept'  
                entity_types['concept'].append(entity)
            elif len(token) <= 4 and token in ['is', 'has', 'can', 'will']:
                entity['type'] = 'relation'
                entity_types['relation'].append(entity)
            else:
                entity['type'] = 'attribute'
                entity_types['attribute'].append(entity)
            
            entities.append(entity)
        
        return entities
    
    def _calculate_token_importance(self, token: str, context: Dict[str, Any]) -> float:
        """Calculate importance score for a token"""
        importance = 0.5  # Base importance
        
        # Length factor - longer tokens often more meaningful
        if len(token) > 6:
            importance += 0.2
        
        # Context relevance
        if context:
            context_text = ' '.join(str(v) for v in context.values()).lower()
            if token in context_text:
                importance += 0.3
        
        # Domain-specific importance (could be enhanced with NLP models)
        technical_terms = ['analysis', 'system', 'process', 'method', 'algorithm']
        if token in technical_terms:
            importance += 0.2
            
        return min(1.0, importance)
    
    async def _extract_relationships(
        self, 
        tokens: List[str], 
        entities: List[Dict[str, Any]], 
        focus: str
    ) -> Dict[str, List[str]]:
        """Extract relationships between entities"""
        relationships = defaultdict(list)
        
        if focus == "relationships":
            # Extract explicit relationships
            relationships.update(await self._extract_explicit_relationships(tokens, entities))
        
        elif focus == "sequence":
            # Extract sequence-based relationships
            relationships.update(await self._extract_sequence_relationships(tokens, entities))
        
        elif focus == "semantic":
            # Extract semantic relationships
            relationships.update(await self._extract_semantic_relationships(tokens, entities))
        
        # Add positional relationships
        relationships.update(await self._extract_positional_relationships(entities))
        
        return dict(relationships)
    
    async def _extract_explicit_relationships(
        self, 
        tokens: List[str], 
        entities: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Extract explicit relationships from content"""
        relationships = defaultdict(list)
        
        # Look for relationship indicators
        relation_words = ['is', 'has', 'can', 'will', 'causes', 'leads', 'results', 'means']
        
        for i, token in enumerate(tokens):
            if token in relation_words:
                # Find entities around this relationship word
                before_entities = [e['token'] for e in entities if tokens.index(e['token']) < i]
                after_entities = [e['token'] for e in entities if tokens.index(e['token']) > i]
                
                if before_entities and after_entities:
                    subject = before_entities[-1]  # Last entity before relation
                    object_entity = after_entities[0]  # First entity after relation
                    relationships[f"{subject}_{token}"].append(object_entity)
        
        return relationships
    
    async def _extract_sequence_relationships(
        self, 
        tokens: List[str], 
        entities: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Extract sequence-based relationships"""
        relationships = defaultdict(list)
        
        # Sequential relationships
        entity_tokens = [e['token'] for e in entities]
        
        for i in range(len(entity_tokens) - 1):
            current_entity = entity_tokens[i]
            next_entity = entity_tokens[i + 1]
            relationships[f"sequence_{current_entity}"].append(next_entity)
        
        return relationships
    
    async def _extract_semantic_relationships(
        self, 
        tokens: List[str], 
        entities: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Extract semantic relationships based on meaning"""
        relationships = defaultdict(list)
        
        # Group entities by type
        entities_by_type = defaultdict(list)
        for entity in entities:
            entities_by_type[entity['type']].append(entity['token'])
        
        # Create type-based relationships
        for entity_type, entity_list in entities_by_type.items():
            if len(entity_list) > 1:
                relationships[f"type_{entity_type}"] = entity_list
        
        return relationships
    
    async def _extract_positional_relationships(
        self, 
        entities: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Extract relationships based on position"""
        relationships = defaultdict(list)
        
        # Proximity relationships (entities that appear close together)
        for i, entity in enumerate(entities):
            nearby_entities = []
            
            # Look at entities within window of 3 positions
            window = 3
            start = max(0, i - window)
            end = min(len(entities), i + window + 1)
            
            for j in range(start, end):
                if j != i:
                    nearby_entities.append(entities[j]['token'])
            
            if nearby_entities:
                relationships[f"proximity_{entity['token']}"] = nearby_entities
        
        return relationships
    
    async def _generate_abstract_variables(
        self, 
        entities: List[Dict[str, Any]], 
        relationships: Dict[str, List[str]]
    ) -> List['SymbolicVariable']:
        """Generate abstract symbolic variables from entities and relationships"""
        from .manager import SymbolicVariable  # Import here to avoid circular import
        
        variables = []
        
        # Create variables for high-importance entities
        for i, entity in enumerate(entities):
            if entity['importance'] > 0.6:  # Threshold for abstraction
                
                # Find relationships involving this entity
                entity_relationships = []
                for rel_key, rel_values in relationships.items():
                    if entity['token'] in rel_key or entity['token'] in rel_values:
                        entity_relationships.append(rel_key)
                
                # Determine abstraction level based on complexity
                abstraction_level = min(3, len(entity_relationships) + 1)
                
                # Generate symbolic variable
                variable = SymbolicVariable(
                    id=f"var_{i}",
                    symbol=f"X{i}",  # Abstract symbol
                    relationships=entity_relationships,
                    abstraction_level=abstraction_level,
                    confidence=entity['importance']
                )
                
                variables.append(variable)
        
        # Create variables for important relationship patterns
        for rel_key, rel_values in relationships.items():
            if len(rel_values) > 2:  # Multi-element relationships
                variable = SymbolicVariable(
                    id=f"rel_{len(variables)}",
                    symbol=f"R{len(variables)}",
                    relationships=[rel_key],
                    abstraction_level=2,
                    confidence=0.7
                )
                variables.append(variable)
        
        return variables
    
    def _calculate_abstraction_confidence(
        self, 
        variables: List['SymbolicVariable'], 
        relationships: Dict[str, List[str]]
    ) -> float:
        """Calculate confidence in the abstraction process"""
        if not variables:
            return 0.0
        
        # Base confidence from variable quality
        var_confidences = [var.confidence for var in variables]
        avg_var_confidence = sum(var_confidences) / len(var_confidences)
        
        # Relationship coverage bonus
        total_relationships = len(relationships)
        covered_relationships = sum(len(var.relationships) for var in variables)
        
        coverage_ratio = min(1.0, covered_relationships / max(1, total_relationships))
        
        # Combined confidence
        abstraction_confidence = (avg_var_confidence * 0.7) + (coverage_ratio * 0.3)
        
        return abstraction_confidence
    
    def reset(self):
        """Reset abstraction engine state"""
        self.abstraction_cache = {}