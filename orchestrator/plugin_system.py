"""
Plugin System for ByteClaude
Enables extensibility through custom plugins and extensions
"""

from typing import Dict, List, Any, Callable, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
import importlib
import sys
from pathlib import Path


@dataclass
class PluginMetadata:
    """Metadata for a plugin"""
    name: str
    version: str
    author: str
    description: str
    entry_point: str
    dependencies: List[str] = None
    hooks: Dict[str, List[str]] = None


class Hook(ABC):
    """Base class for plugin hooks"""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute hook"""
        pass


class Plugin(ABC):
    """Base class for all plugins"""
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata"""
        pass
    
    @abstractmethod
    def initialize(self, context: Dict[str, Any]):
        """Initialize plugin with context"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute plugin"""
        pass


class PluginManager:
    """
    Manages plugin loading, registration, and execution
    """
    
    def __init__(self, plugin_dirs: List[str] = None):
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Hook]] = {}
        self.plugin_dirs = plugin_dirs or []
        self.context: Dict[str, Any] = {}

    def register_hook(self, hook_name: str, hook: Hook):
        """Register a hook"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(hook)

    def execute_hooks(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute all hooks for a hook point"""
        results = []
        for hook in self.hooks.get(hook_name, []):
            try:
                result = hook.execute(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Error executing hook {hook_name}: {e}")
        return results

    def load_plugin(self, plugin_path: str) -> Plugin:
        """Load a plugin from path"""
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(
                "plugin_module",
                plugin_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules["plugin_module"] = module
            spec.loader.exec_module(module)

            # Find plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                    plugin_class = attr
                    break

            if not plugin_class:
                raise ValueError(f"No Plugin class found in {plugin_path}")

            # Create and register plugin
            plugin = plugin_class()
            plugin.initialize(self.context)
            self.plugins[plugin.metadata.name] = plugin

            return plugin

        except Exception as e:
            print(f"Error loading plugin {plugin_path}: {e}")
            return None

    def load_plugins_from_directory(self, directory: str) -> List[Plugin]:
        """Load all plugins from a directory"""
        plugins = []
        plugin_dir = Path(directory)

        if not plugin_dir.exists():
            return plugins

        for plugin_file in plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            plugin = self.load_plugin(str(plugin_file))
            if plugin:
                plugins.append(plugin)

        return plugins

    def execute_plugin(self, plugin_name: str, *args, **kwargs) -> Any:
        """Execute a specific plugin"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' not found")

        plugin = self.plugins[plugin_name]
        return plugin.execute(*args, **kwargs)

    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """Get a plugin by name"""
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> List[PluginMetadata]:
        """List all loaded plugins"""
        return [plugin.metadata for plugin in self.plugins.values()]

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return True
        return False


class PluginRegistry:
    """
    Global registry for all available plugins
    """
    
    _instance = None
    _plugins: Dict[str, PluginMetadata] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, metadata: PluginMetadata):
        """Register a plugin in the registry"""
        self._plugins[metadata.name] = metadata

    def unregister(self, plugin_name: str):
        """Unregister a plugin"""
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]

    def get(self, plugin_name: str) -> Optional[PluginMetadata]:
        """Get plugin metadata"""
        return self._plugins.get(plugin_name)

    def list_all(self) -> List[PluginMetadata]:
        """List all registered plugins"""
        return list(self._plugins.values())

    def search(self, query: str) -> List[PluginMetadata]:
        """Search plugins by name or description"""
        query_lower = query.lower()
        results = []
        
        for metadata in self._plugins.values():
            if (query_lower in metadata.name.lower() or
                query_lower in metadata.description.lower()):
                results.append(metadata)
        
        return results


# Example plugin implementation
class ExamplePlugin(Plugin):
    """Example plugin demonstrating the plugin system"""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="example-plugin",
            version="1.0.0",
            author="ByteClaude",
            description="Example plugin for ByteClaude",
            entry_point="ExamplePlugin",
            hooks={
                "pre_execution": ["before_task"],
                "post_execution": ["after_task"]
            }
        )
    
    def initialize(self, context: Dict[str, Any]):
        """Initialize plugin"""
        self.context = context
        print(f"Initialized {self.metadata.name}")
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute plugin"""
        return {"status": "success", "message": "Example plugin executed"}


# Helper functions
def create_plugin_manager(plugin_dirs: List[str] = None) -> PluginManager:
    """Create a new plugin manager"""
    return PluginManager(plugin_dirs)


def get_registry() -> PluginRegistry:
    """Get the global plugin registry"""
    return PluginRegistry()
