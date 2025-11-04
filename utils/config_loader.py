"""
Configuration Loader Utility
Load and merge configurations from multiple sources
"""

import yaml
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from copy import deepcopy


class ConfigLoader:
    """
    Load and manage configuration from multiple sources with precedence
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize ConfigLoader

        Args:
            base_path: Base directory for config files
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.loaded_configs: Dict[str, Dict[str, Any]] = {}

    def load(
        self,
        config_path: str,
        required: bool = True,
        cache: bool = True
    ) -> Dict[str, Any]:
        """
        Load configuration from file

        Args:
            config_path: Path to config file (relative to base_path)
            required: Whether config is required
            cache: Whether to cache loaded config

        Returns:
            Configuration dictionary
        """
        full_path = self.base_path / config_path

        if not full_path.exists():
            if required:
                raise FileNotFoundError(f"Config file not found: {full_path}")
            return {}

        # Check cache
        if cache and str(full_path) in self.loaded_configs:
            return deepcopy(self.loaded_configs[str(full_path)])

        # Load based on extension
        if full_path.suffix in ['.yaml', '.yml']:
            config = self._load_yaml(full_path)
        elif full_path.suffix == '.json':
            config = self._load_json(full_path)
        else:
            raise ValueError(f"Unsupported config format: {full_path.suffix}")

        # Process environment variables
        config = self._process_env_vars(config)

        # Cache if requested
        if cache:
            self.loaded_configs[str(full_path)] = deepcopy(config)

        return config

    def load_multiple(self, paths: List[str], merge: bool = True) -> Dict[str, Any]:
        """
        Load multiple config files

        Args:
            paths: List of config paths
            merge: Whether to merge configs (later overrides earlier)

        Returns:
            Combined configuration
        """
        configs = [self.load(path, required=False) for path in paths]

        if merge:
            return self.merge_configs(configs)
        else:
            return {'configs': configs}

    def merge_configs(self, configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge multiple configurations with deep merge

        Args:
            configs: List of configuration dictionaries

        Returns:
            Merged configuration
        """
        result = {}

        for config in configs:
            result = self._deep_merge(result, config)

        return result

    def get(self, key: str, default: Any = None, config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Get configuration value using dot notation

        Args:
            key: Key in dot notation (e.g., "database.host")
            default: Default value if key not found
            config: Config dict to search (uses last loaded if None)

        Returns:
            Configuration value
        """
        if config is None:
            if not self.loaded_configs:
                return default
            config = list(self.loaded_configs.values())[-1]

        keys = key.split('.')
        value = config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set configuration value using dot notation

        Args:
            key: Key in dot notation
            value: Value to set
            config: Config dict to modify

        Returns:
            Modified config dict
        """
        keys = key.split('.')
        current = config

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        return config

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load YAML config file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}

    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Load JSON config file"""
        with open(path, 'r') as f:
            return json.load(f)

    def _process_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process environment variable substitutions

        Syntax: ${ENV_VAR} or ${ENV_VAR:default}
        """
        if isinstance(config, dict):
            return {k: self._process_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._process_env_vars(item) for item in config]
        elif isinstance(config, str):
            return self._substitute_env_vars(config)
        else:
            return config

    def _substitute_env_vars(self, value: str) -> str:
        """Substitute environment variables in string"""
        import re

        pattern = r'\$\{([A-Z_][A-Z0-9_]*?)(?::([^}]+))?\}'

        def replace(match):
            var_name = match.group(1)
            default = match.group(2)
            return os.environ.get(var_name, default or '')

        return re.sub(pattern, replace, value)

    def _deep_merge(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries

        Args:
            base: Base dictionary
            overlay: Dictionary to overlay (takes precedence)

        Returns:
            Merged dictionary
        """
        result = deepcopy(base)

        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = deepcopy(value)

        return result
