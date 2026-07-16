"""Plugin system primitives for Platform Evolution milestones."""

from .base import EdgePlugin
from .manager import (
	PluginActivationError,
	PluginManager,
	PluginNotFoundError,
	PluginValidationError,
)

__all__ = [
	"EdgePlugin",
	"PluginManager",
	"PluginValidationError",
	"PluginNotFoundError",
	"PluginActivationError",
]
