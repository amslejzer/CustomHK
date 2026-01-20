"""Action modules for CustomHK."""

# Import all action modules to ensure they register themselves
from . import signature
from . import clipboard
from . import wizard

# Export the registry for external use
from .registry import get_registry, register_action

__all__ = ['get_registry', 'register_action']
