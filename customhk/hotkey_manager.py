"""Hotkey management and listener lifecycle."""

import logging
from typing import Dict, Any, Optional, Callable
from pynput import keyboard
from pynput.keyboard import Controller

from .actions.registry import get_registry
from .utils.window import WindowManager


logger = logging.getLogger(__name__)


class HotkeyManager:
    """Manages hotkey registration, listeners, and action execution."""

    def __init__(self, config):
        """Initialize hotkey manager.

        Args:
            config: Configuration object
        """
        self.config = config
        self.kb_controller = Controller()
        self.listener: Optional[keyboard.GlobalHotKeys] = None
        self.enabled = True
        self.registry = get_registry()
        self.action_instances: Dict[str, Any] = {}
        self.hotkey_map: Dict[str, Callable] = {}

        # Initialize all actions from config
        self._initialize_actions()

    def _initialize_actions(self) -> None:
        """Initialize action instances from configuration."""
        logger.info("Initializing actions from configuration")

        # Get global hotkeys
        global_hotkeys = self.config.get_global_hotkeys()

        for hotkey_config in global_hotkeys:
            action_name = hotkey_config.get('action')
            if not action_name:
                logger.warning(f"Hotkey config missing action name: {hotkey_config}")
                continue

            # Skip if already created
            if action_name in self.action_instances:
                continue

            # Get action-specific config
            action_config = self.config.get_action_config(action_name)

            # Add user signature to config if needed
            if action_name == 'type_signature':
                action_config['signature'] = self.config.get_user_signature()

            # Add entire config for wizard action
            if action_name == 'show_wizard':
                action_config = self.config.data

            # Create action instance
            instance = self.registry.create_instance(
                action_name,
                action_config,
                self.kb_controller
            )

            if instance:
                self.action_instances[action_name] = instance
                logger.info(f"Created action instance: {action_name}")
            else:
                logger.error(f"Failed to create action instance: {action_name}")

    def _build_hotkey_map(self) -> Dict[str, Callable]:
        """Build hotkey mapping from configuration.

        Returns:
            Dictionary mapping hotkey strings to callable actions
        """
        hotkey_map = {}

        # Add global hotkeys
        global_hotkeys = self.config.get_global_hotkeys()
        for hotkey_config in global_hotkeys:
            if not hotkey_config.get('enabled', True):
                continue

            key = hotkey_config.get('key')
            action_name = hotkey_config.get('action')

            if not key or not action_name:
                logger.warning(f"Invalid hotkey config: {hotkey_config}")
                continue

            action = self.action_instances.get(action_name)
            if not action:
                logger.warning(f"Action {action_name} not found for hotkey {key}")
                continue

            hotkey_map[key] = action
            logger.debug(f"Mapped hotkey {key} -> {action_name}")

        # TODO: Add conditional (app-specific) hotkeys
        # This will require checking active window in the action wrapper

        return hotkey_map

    def start(self) -> None:
        """Start listening for hotkeys."""
        if self.listener is not None:
            logger.warning("Listener already running")
            return

        self.hotkey_map = self._build_hotkey_map()

        if not self.hotkey_map:
            logger.warning("No hotkeys configured, listener not started")
            return

        try:
            self.listener = keyboard.GlobalHotKeys(self.hotkey_map)
            self.listener.start()
            self.enabled = True
            logger.info(f"Started hotkey listener with {len(self.hotkey_map)} hotkeys")
        except Exception as e:
            logger.error(f"Failed to start hotkey listener: {e}")
            self.listener = None

    def stop(self) -> None:
        """Stop listening for hotkeys."""
        if self.listener is None:
            logger.warning("Listener not running")
            return

        try:
            self.listener.stop()
            self.listener = None
            self.enabled = False
            logger.info("Stopped hotkey listener")
        except Exception as e:
            logger.error(f"Failed to stop hotkey listener: {e}")

    def restart(self) -> None:
        """Restart the hotkey listener (useful after config changes)."""
        logger.info("Restarting hotkey listener")
        self.stop()
        self._initialize_actions()  # Reinitialize actions with new config
        self.start()

    def is_running(self) -> bool:
        """Check if listener is running.

        Returns:
            True if listener is active
        """
        return self.listener is not None and self.enabled

    def enable(self) -> None:
        """Enable hotkey listening."""
        if not self.enabled:
            self.start()

    def disable(self) -> None:
        """Disable hotkey listening."""
        if self.enabled:
            self.stop()

    def toggle(self) -> bool:
        """Toggle hotkey listening on/off.

        Returns:
            New enabled state
        """
        if self.enabled:
            self.disable()
        else:
            self.enable()

        return self.enabled
