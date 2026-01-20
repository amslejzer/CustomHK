"""Action registry for managing available actions."""

from typing import Dict, Type, Any, Optional
import logging

from .base import Action


logger = logging.getLogger(__name__)


class ActionRegistry:
    """Registry for all available actions."""

    def __init__(self):
        """Initialize the action registry."""
        self._actions: Dict[str, Type[Action]] = {}
        self._instances: Dict[str, Action] = {}

    def register(self, name: str, action_class: Type[Action]) -> None:
        """Register an action class.

        Args:
            name: Name to register the action under
            action_class: Action class to register
        """
        if name in self._actions:
            logger.warning(f"Action '{name}' already registered, overwriting")

        self._actions[name] = action_class
        logger.info(f"Registered action: {name}")

    def create_instance(
        self,
        name: str,
        config: Dict[str, Any],
        keyboard_controller: Any
    ) -> Optional[Action]:
        """Create an instance of a registered action.

        Args:
            name: Name of the action to instantiate
            config: Configuration for the action
            keyboard_controller: Keyboard controller instance

        Returns:
            Action instance or None if action not found
        """
        if name not in self._actions:
            logger.error(f"Action '{name}' not found in registry")
            return None

        try:
            instance = self._actions[name](config, keyboard_controller)
            self._instances[name] = instance
            logger.debug(f"Created instance of action: {name}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create instance of action '{name}': {e}")
            return None

    def get_instance(self, name: str) -> Optional[Action]:
        """Get existing action instance.

        Args:
            name: Name of the action

        Returns:
            Action instance or None if not found
        """
        return self._instances.get(name)

    def list_actions(self) -> list[str]:
        """Get list of all registered action names.

        Returns:
            List of action names
        """
        return list(self._actions.keys())

    def unregister(self, name: str) -> None:
        """Unregister an action.

        Args:
            name: Name of the action to unregister
        """
        if name in self._actions:
            del self._actions[name]
            logger.info(f"Unregistered action: {name}")

        if name in self._instances:
            del self._instances[name]


# Global registry instance
_registry = ActionRegistry()


def register_action(name: str):
    """Decorator to register an action class.

    Args:
        name: Name to register the action under

    Example:
        @register_action("my_action")
        class MyAction(Action):
            def execute(self):
                pass
    """
    def decorator(action_class: Type[Action]):
        _registry.register(name, action_class)
        return action_class
    return decorator


def get_registry() -> ActionRegistry:
    """Get the global action registry.

    Returns:
        Global ActionRegistry instance
    """
    return _registry
