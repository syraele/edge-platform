"""Plugin system primitives for Platform Evolution milestones."""

from .base import EdgePlugin
from .loader import PluginDiscoveryError, PluginLoader
from .manager import (
	PluginActivationError,
	PluginManager,
	PluginNotFoundError,
	PluginValidationError,
)

__all__ = [
	"EdgePlugin",
	"PluginLoader",
	"PluginDiscoveryError",
	"PluginManager",
	"PluginValidationError",
	"PluginNotFoundError",
	"PluginActivationError",
]
