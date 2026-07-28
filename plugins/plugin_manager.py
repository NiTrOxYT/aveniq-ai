"""
Plugin Manager & Plugin Interface for AVENIQ AI Runtime v1.
Extensible plugin system allowing GitHub, Reddit, Product Hunt, Slack, Discord plugins without modifying runtime kernel core.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("aveniq.plugins.plugin_manager")


class BasePlugin:
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.enabled = True

    def initialize(self, kernel: Any):
        """Called when plugin is initialized by Runtime Kernel."""
        pass

    def shutdown(self):
        """Called during runtime shutdown."""
        pass

    def register_events(self, event_bus: Any):
        """Register event handlers with EventBus."""
        pass

    def register_search(self, search_service: Any):
        """Register custom search providers."""
        pass


class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}

    def register_plugin(self, plugin: BasePlugin):
        """Register an installable plugin."""
        self._plugins[plugin.name] = plugin
        logger.info(f"[PluginManager] Registered plugin '{plugin.name}' v{plugin.version}")

    def initialize_all(self, kernel: Any):
        """Initialize all enabled plugins."""
        for p in self._plugins.values():
            if p.enabled:
                try:
                    p.initialize(kernel)
                    logger.info(f"[PluginManager] Initialized plugin '{p.name}'")
                except Exception as e:
                    logger.error(f"[PluginManager] Error initializing plugin '{p.name}': {e}")

    def list_plugins(self) -> List[Dict[str, Any]]:
        return [{"name": p.name, "version": p.version, "enabled": p.enabled} for p in self._plugins.values()]


global_plugin_manager = PluginManager()
