"""
Configuration Manager - Context Engineering Configuration
=========================================================

Manages configuration loading, validation, and runtime updates
for all context engineering components.
"""

import os
import json
import yaml
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

class ConfigManager:
    """Manages configuration for context engineering components"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config = {}
        self._config_watchers = []
        
        # Load default configuration
        self._load_default_config()
        
        # Load configuration from file if provided
        if config_path:
            self.load_config_from_file(config_path)
    
    def _load_default_config(self):
        """Load default configuration"""
        self._config = {
            "engine": {
                "model_provider": "openai",
                "model_name": "gpt-4",
                "max_tokens": 4000,
                "temperature": 0.7,
                "enable_streaming": True,
                "timeout": 300,
                "retry_attempts": 3
            },
            "cognitive_tools": {
                "enabled": True,
                "tool_selection": "auto",
                "verification_enabled": True,
                "available_tools": [
                    "understand", "extract", "highlight", "apply", "validate"
                ],
                "max_tool_depth": 5,
                "parallel_processing": True
            },
            "neural_fields": {
                "enabled": True,
                "field_type": "semantic",
                "decay_rate": 0.05,
                "boundary_permeability": 0.8,
                "resonance_bandwidth": 0.6,
                "attractor_formation_threshold": 0.7,
                "max_attractors": 10,
                "field_dimensions": 512
            },
            "memory": {
                "enabled": True,
                "consolidation_frequency": 5,
                "memory_budget": 1000,
                "efficiency_target": 0.8,
                "retention_strategy": "reasoning_value",
                "compression_method": "semantic_similarity",
                "persistence_enabled": True
            },
            "symbolic_processing": {
                "enabled": True,
                "abstraction_depth": 3,
                "induction_method": "pattern_recognition",
                "retrieval_strategy": "best_match",
                "symbolic_validation": True,
                "generalization_enabled": True
            },
            "quantum_semantics": {
                "enabled": True,
                "observer_contexts": ["default"],
                "uncertainty_handling": "bayesian",
                "superposition_threshold": 0.3,
                "measurement_strategy": "context_collapse",
                "degeneracy_management": True
            },
            "progressive_complexity": {
                "enabled": True,
                "auto_scaling": True,
                "performance_threshold": 0.85,
                "complexity_levels": [
                    "atom", "molecule", "cell", "organ", "neural_system", "neural_field"
                ],
                "scaling_strategy": "adaptive",
                "efficiency_monitoring": True
            },
            "logging": {
                "level": "INFO",
                "enable_performance_logging": True,
                "enable_reasoning_traces": True,
                "max_log_history": 1000
            },
            "monitoring": {
                "enable_performance_monitoring": True,
                "snapshot_interval": 60,
                "alert_thresholds": {
                    "cpu_usage": 80,
                    "memory_usage": 85,
                    "response_time": 5.0,
                    "success_rate": 0.95
                }
            }
        }
    
    def load_config_from_file(self, config_path: str):
        """Load configuration from file"""
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_file, 'r') as f:
                if config_file.suffix.lower() == '.json':
                    file_config = json.load(f)
                elif config_file.suffix.lower() in ['.yml', '.yaml']:
                    file_config = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported configuration file format: {config_file.suffix}")
            
            # Merge file config with default config
            self._deep_merge_config(self._config, file_config)
            
        except Exception as e:
            raise ValueError(f"Error loading configuration file: {e}")
    
    def load_config_from_env(self, prefix: str = "CONTEXTUAL_"):
        """Load configuration from environment variables"""
        env_config = {}
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Convert environment variable to config key
                config_key = key[len(prefix):].lower()
                config_path = config_key.split('_')
                
                # Parse value
                parsed_value = self._parse_env_value(value)
                
                # Set nested configuration
                self._set_nested_config(env_config, config_path, parsed_value)
        
        # Merge environment config with current config
        self._deep_merge_config(self._config, env_config)
    
    def _parse_env_value(self, value: str) -> Union[str, int, float, bool, List, Dict]:
        """Parse environment variable value to appropriate type"""
        # Try boolean
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        
        # Try integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Try JSON
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Return as string
        return value
    
    def _set_nested_config(self, config: Dict, path: List[str], value: Any):
        """Set nested configuration value"""
        current = config
        
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[path[-1]] = value
    
    def _deep_merge_config(self, base: Dict, override: Dict):
        """Deep merge configuration dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge_config(base[key], value)
            else:
                base[key] = value
    
    def get_config(self, key_path: Optional[str] = None) -> Any:
        """Get configuration value by key path"""
        if key_path is None:
            return self._config.copy()
        
        keys = key_path.split('.')
        current = self._config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                raise KeyError(f"Configuration key not found: {key_path}")
        
        return current
    
    def set_config(self, key_path: str, value: Any):
        """Set configuration value by key path"""
        keys = key_path.split('.')
        current = self._config
        
        # Navigate to parent of target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the value
        current[keys[-1]] = value
        
        # Notify watchers
        self._notify_config_change(key_path, value)
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Validate current configuration"""
        errors = {}
        
        # Validate engine config
        engine_errors = self._validate_engine_config()
        if engine_errors:
            errors["engine"] = engine_errors
        
        # Validate component configs
        for component in ["cognitive_tools", "neural_fields", "memory", 
                         "symbolic_processing", "quantum_semantics", "progressive_complexity"]:
            component_errors = self._validate_component_config(component)
            if component_errors:
                errors[component] = component_errors
        
        return errors
    
    def _validate_engine_config(self) -> List[str]:
        """Validate engine configuration"""
        errors = []
        engine_config = self._config.get("engine", {})
        
        # Validate model provider
        valid_providers = ["openai", "anthropic", "local"]
        if engine_config.get("model_provider") not in valid_providers:
            errors.append(f"Invalid model_provider. Must be one of: {valid_providers}")
        
        # Validate token limits
        max_tokens = engine_config.get("max_tokens", 0)
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            errors.append("max_tokens must be a positive integer")
        
        # Validate temperature
        temperature = engine_config.get("temperature", 0.7)
        if not isinstance(temperature, (int, float)) or not 0 <= temperature <= 2:
            errors.append("temperature must be a number between 0 and 2")
        
        return errors
    
    def _validate_component_config(self, component: str) -> List[str]:
        """Validate component configuration"""
        errors = []
        component_config = self._config.get(component, {})
        
        # Check if enabled is boolean
        if "enabled" in component_config:
            if not isinstance(component_config["enabled"], bool):
                errors.append(f"{component}.enabled must be boolean")
        
        # Component-specific validations
        if component == "neural_fields":
            decay_rate = component_config.get("decay_rate", 0.05)
            if not isinstance(decay_rate, (int, float)) or not 0 <= decay_rate <= 1:
                errors.append("neural_fields.decay_rate must be between 0 and 1")
        
        elif component == "memory":
            memory_budget = component_config.get("memory_budget", 1000)
            if not isinstance(memory_budget, int) or memory_budget <= 0:
                errors.append("memory.memory_budget must be a positive integer")
        
        elif component == "progressive_complexity":
            performance_threshold = component_config.get("performance_threshold", 0.85)
            if not isinstance(performance_threshold, (int, float)) or not 0 <= performance_threshold <= 1:
                errors.append("progressive_complexity.performance_threshold must be between 0 and 1")
        
        return errors
    
    def add_config_watcher(self, callback):
        """Add configuration change watcher"""
        self._config_watchers.append(callback)
    
    def remove_config_watcher(self, callback):
        """Remove configuration change watcher"""
        if callback in self._config_watchers:
            self._config_watchers.remove(callback)
    
    def _notify_config_change(self, key_path: str, value: Any):
        """Notify watchers of configuration change"""
        for watcher in self._config_watchers:
            try:
                watcher(key_path, value)
            except Exception as e:
                # Log error but don't stop other watchers
                print(f"Error in config watcher: {e}")
    
    def save_config(self, output_path: str):
        """Save current configuration to file"""
        output_file = Path(output_path)
        
        try:
            with open(output_file, 'w') as f:
                if output_file.suffix.lower() == '.json':
                    json.dump(self._config, f, indent=2)
                elif output_file.suffix.lower() in ['.yml', '.yaml']:
                    yaml.dump(self._config, f, default_flow_style=False)
                else:
                    raise ValueError(f"Unsupported output format: {output_file.suffix}")
        
        except Exception as e:
            raise ValueError(f"Error saving configuration: {e}")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self._config.clear()
        self._load_default_config()
        
        # Notify watchers
        for watcher in self._config_watchers:
            try:
                watcher("*", self._config)  # Special key for full reset
            except Exception as e:
                print(f"Error in config watcher: {e}")
    
    def get_component_config(self, component: str) -> Dict[str, Any]:
        """Get configuration for specific component"""
        return self._config.get(component, {}).copy()
    
    def update_component_config(self, component: str, updates: Dict[str, Any]):
        """Update configuration for specific component"""
        if component not in self._config:
            self._config[component] = {}
        
        self._deep_merge_config(self._config[component], updates)
        
        # Notify watchers
        self._notify_config_change(f"{component}.*", updates)