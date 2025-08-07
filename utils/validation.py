"""
Validation Utils - Input and Output Validation
==============================================

Provides validation utilities for context engineering inputs, outputs,
and internal data structures.
"""

import re
import json
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import is_dataclass

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class ValidationUtils:
    """Validation utilities for context engineering"""
    
    @staticmethod
    def validate_content_input(content: Any) -> Tuple[bool, List[str]]:
        """Validate content input for processing"""
        errors = []
        
        # Check if content exists
        if content is None:
            errors.append("Content cannot be None")
            return False, errors
        
        # Convert to string if not already
        if not isinstance(content, str):
            content = str(content)
        
        # Check content length
        if len(content) == 0:
            errors.append("Content cannot be empty")
        elif len(content) > 100000:  # 100K character limit
            errors.append("Content exceeds maximum length of 100,000 characters")
        
        # Check for reasonable content
        if len(content.strip()) == 0:
            errors.append("Content cannot be only whitespace")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_context_input(context: Any) -> Tuple[bool, List[str]]:
        """Validate context input for processing"""
        errors = []
        
        # Context can be None (empty context is valid)
        if context is None:
            return True, errors
        
        # Check if context is dictionary
        if not isinstance(context, dict):
            errors.append("Context must be a dictionary")
            return False, errors
        
        # Validate context size
        if len(context) > 100:  # Max 100 context items
            errors.append("Context exceeds maximum of 100 items")
        
        # Validate context keys and values
        for key, value in context.items():
            # Validate key
            if not isinstance(key, str):
                errors.append(f"Context key must be string, got: {type(key)}")
            elif len(key) == 0:
                errors.append("Context key cannot be empty")
            elif len(key) > 100:
                errors.append(f"Context key '{key}' exceeds maximum length of 100 characters")
            
            # Validate value
            if value is None:
                continue  # None values are acceptable
            
            # Check value size (approximate)
            try:
                value_str = json.dumps(value, default=str)
                if len(value_str) > 10000:  # 10K character limit per value
                    errors.append(f"Context value for key '{key}' exceeds maximum size")
            except Exception:
                # If we can't serialize it, it might be too complex
                errors.append(f"Context value for key '{key}' is too complex")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_confidence_score(confidence: Any) -> Tuple[bool, List[str]]:
        """Validate confidence score"""
        errors = []
        
        if confidence is None:
            errors.append("Confidence score cannot be None")
            return False, errors
        
        if not isinstance(confidence, (int, float)):
            errors.append(f"Confidence score must be numeric, got: {type(confidence)}")
            return False, errors
        
        if not 0.0 <= confidence <= 1.0:
            errors.append(f"Confidence score must be between 0.0 and 1.0, got: {confidence}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_processing_result(result: Any) -> Tuple[bool, List[str]]:
        """Validate processing result structure"""
        errors = []
        
        if result is None:
            errors.append("Processing result cannot be None")
            return False, errors
        
        # Check if it's a ProcessingResult dataclass or compatible dict
        if is_dataclass(result):
            # Validate dataclass fields
            if not hasattr(result, 'content'):
                errors.append("ProcessingResult must have 'content' field")
            if not hasattr(result, 'confidence'):
                errors.append("ProcessingResult must have 'confidence' field")
            if not hasattr(result, 'processing_time'):
                errors.append("ProcessingResult must have 'processing_time' field")
            
            # Validate field values
            if hasattr(result, 'content') and result.content is None:
                errors.append("ProcessingResult content cannot be None")
            
            if hasattr(result, 'confidence'):
                conf_valid, conf_errors = ValidationUtils.validate_confidence_score(result.confidence)
                if not conf_valid:
                    errors.extend(conf_errors)
            
            if hasattr(result, 'processing_time'):
                if not isinstance(result.processing_time, (int, float)) or result.processing_time < 0:
                    errors.append("Processing time must be non-negative number")
        
        elif isinstance(result, dict):
            # Validate dictionary structure
            required_keys = ['content', 'confidence', 'processing_time']
            for key in required_keys:
                if key not in result:
                    errors.append(f"Processing result missing required key: {key}")
            
            # Validate values
            if 'content' in result and result['content'] is None:
                errors.append("Processing result content cannot be None")
            
            if 'confidence' in result:
                conf_valid, conf_errors = ValidationUtils.validate_confidence_score(result['confidence'])
                if not conf_valid:
                    errors.extend(conf_errors)
        
        else:
            errors.append(f"Processing result must be ProcessingResult dataclass or dict, got: {type(result)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_complexity_level(complexity: Any) -> Tuple[bool, List[str]]:
        """Validate complexity level"""
        errors = []
        
        valid_levels = ["atom", "molecule", "cell", "organ", "neural_system", "neural_field"]
        
        if complexity is None:
            errors.append("Complexity level cannot be None")
            return False, errors
        
        if not isinstance(complexity, str):
            errors.append(f"Complexity level must be string, got: {type(complexity)}")
            return False, errors
        
        if complexity not in valid_levels:
            errors.append(f"Invalid complexity level: {complexity}. Must be one of: {valid_levels}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_api_key(api_key: Any, provider: str = "openai") -> Tuple[bool, List[str]]:
        """Validate API key format"""
        errors = []
        
        if api_key is None or api_key == "":
            errors.append(f"API key for {provider} cannot be None or empty")
            return False, errors
        
        if not isinstance(api_key, str):
            errors.append(f"API key must be string, got: {type(api_key)}")
            return False, errors
        
        # Provider-specific validation
        if provider == "openai":
            if not api_key.startswith("sk-"):
                errors.append("OpenAI API key must start with 'sk-'")
            if len(api_key) < 20:
                errors.append("OpenAI API key appears to be too short")
        
        elif provider == "anthropic":
            if not api_key.startswith("sk-ant-"):
                errors.append("Anthropic API key must start with 'sk-ant-'")
        
        # General format validation
        if len(api_key) > 200:
            errors.append("API key exceeds maximum length")
        
        # Check for suspicious characters
        if re.search(r'[<>"\'\s]', api_key):
            errors.append("API key contains invalid characters")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_field_state(field_state: Any) -> Tuple[bool, List[str]]:
        """Validate neural field state"""
        errors = []
        
        if field_state is None:
            return True, errors  # Empty field state is valid
        
        if not isinstance(field_state, dict):
            errors.append(f"Field state must be dictionary, got: {type(field_state)}")
            return False, errors
        
        # Validate field state structure
        if "patterns" in field_state:
            if not isinstance(field_state["patterns"], dict):
                errors.append("Field state 'patterns' must be dictionary")
        
        if "attractors" in field_state:
            if not isinstance(field_state["attractors"], dict):
                errors.append("Field state 'attractors' must be dictionary")
        
        if "field_energy" in field_state:
            energy = field_state["field_energy"]
            if not isinstance(energy, (int, float)) or energy < 0:
                errors.append("Field energy must be non-negative number")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_memory_item(memory_item: Any) -> Tuple[bool, List[str]]:
        """Validate memory item structure"""
        errors = []
        
        if memory_item is None:
            errors.append("Memory item cannot be None")
            return False, errors
        
        # Check if it's a dataclass or dict
        if is_dataclass(memory_item):
            required_attrs = ['id', 'content', 'reasoning_value', 'timestamp']
            for attr in required_attrs:
                if not hasattr(memory_item, attr):
                    errors.append(f"Memory item missing required attribute: {attr}")
        
        elif isinstance(memory_item, dict):
            required_keys = ['id', 'content', 'reasoning_value', 'timestamp']
            for key in required_keys:
                if key not in memory_item:
                    errors.append(f"Memory item missing required key: {key}")
            
            # Validate specific values
            if 'reasoning_value' in memory_item:
                rv_valid, rv_errors = ValidationUtils.validate_confidence_score(memory_item['reasoning_value'])
                if not rv_valid:
                    errors.extend(rv_errors)
            
            if 'timestamp' in memory_item:
                if not isinstance(memory_item['timestamp'], (int, float)) or memory_item['timestamp'] < 0:
                    errors.append("Memory item timestamp must be non-negative number")
        
        else:
            errors.append(f"Memory item must be dataclass or dict, got: {type(memory_item)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input(content: str) -> str:
        """Sanitize input content for safe processing"""
        if not isinstance(content, str):
            content = str(content)
        
        # Remove null bytes
        content = content.replace('\0', '')
        
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Remove control characters except newlines and tabs
        content = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', content)
        
        return content
    
    @staticmethod
    def truncate_content(content: str, max_length: int = 10000) -> str:
        """Safely truncate content to maximum length"""
        if len(content) <= max_length:
            return content
        
        # Truncate and add indicator
        truncated = content[:max_length - 3] + "..."
        return truncated
    
    @staticmethod
    def validate_batch_inputs(
        contents: List[Any], 
        contexts: Optional[List[Any]] = None
    ) -> Tuple[bool, List[str]]:
        """Validate batch processing inputs"""
        errors = []
        
        if not isinstance(contents, list):
            errors.append(f"Contents must be list, got: {type(contents)}")
            return False, errors
        
        if len(contents) == 0:
            errors.append("Contents list cannot be empty")
            return False, errors
        
        if len(contents) > 100:  # Reasonable batch size limit
            errors.append("Batch size exceeds maximum of 100 items")
        
        # Validate each content item
        for i, content in enumerate(contents):
            content_valid, content_errors = ValidationUtils.validate_content_input(content)
            if not content_valid:
                errors.extend([f"Content {i}: {error}" for error in content_errors])
        
        # Validate contexts if provided
        if contexts is not None:
            if not isinstance(contexts, list):
                errors.append(f"Contexts must be list, got: {type(contexts)}")
            elif len(contexts) != len(contents):
                errors.append(f"Contexts length ({len(contexts)}) must match contents length ({len(contents)})")
            else:
                for i, context in enumerate(contexts):
                    context_valid, context_errors = ValidationUtils.validate_context_input(context)
                    if not context_valid:
                        errors.extend([f"Context {i}: {error}" for error in context_errors])
        
        return len(errors) == 0, errors