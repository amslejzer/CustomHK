"""Configuration management for CustomHK."""

import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


logger = logging.getLogger(__name__)


class Config:
    """Manages application configuration loaded from YAML file."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_path: Path to config file. If None, searches for config.yaml
                        in current directory, then user home directory.
        """
        self.config_path = config_path or self._find_config()
        self.data: Dict[str, Any] = {}
        self.load()

    def _find_config(self) -> Path:
        """Find configuration file in standard locations.

        Returns:
            Path to configuration file.

        Raises:
            FileNotFoundError: If no config file is found.
        """
        search_paths = [
            Path.cwd() / "config.yaml",
            Path(__file__).parent.parent / "config.yaml",
            Path.home() / ".customhk" / "config.yaml",
        ]

        for path in search_paths:
            if path.exists():
                logger.info(f"Found configuration file: {path}")
                return path

        raise FileNotFoundError(
            f"No configuration file found. Searched: {[str(p) for p in search_paths]}"
        )

    def load(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f) or {}
            logger.info(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def reload(self) -> None:
        """Reload configuration from disk."""
        self.load()

    def save(self) -> None:
        """Save current configuration back to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.data, f, default_flow_style=False, sort_keys=False)
            logger.info(f"Saved configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'app.name' or 'user.signature')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'app.name')
            value: Value to set
        """
        keys = key.split('.')
        data = self.data

        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]

        data[keys[-1]] = value

    def get_global_hotkeys(self) -> List[Dict[str, Any]]:
        """Get list of global hotkey configurations.

        Returns:
            List of hotkey configuration dictionaries
        """
        return self.get('hotkeys.global', [])

    def get_conditional_hotkeys(self) -> List[Dict[str, Any]]:
        """Get list of conditional (app-specific) hotkey configurations.

        Returns:
            List of conditional hotkey configuration dictionaries
        """
        return self.get('hotkeys_conditional', [])

    def get_user_signature(self) -> str:
        """Get user's signature text.

        Returns:
            Signature string
        """
        return self.get('user.signature', 'Thanks')

    def get_action_config(self, action_name: str) -> Dict[str, Any]:
        """Get configuration for a specific action.

        Args:
            action_name: Name of the action

        Returns:
            Action configuration dictionary
        """
        return self.get(f'actions.{action_name}', {})
