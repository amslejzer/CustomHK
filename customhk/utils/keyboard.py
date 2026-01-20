"""Keyboard utilities and helpers."""

import logging
from typing import Any
from pynput.keyboard import Key


logger = logging.getLogger(__name__)


class KeyboardHelper:
    """Helper methods for keyboard operations."""

    def __init__(self, controller: Any):
        """Initialize with a keyboard controller.

        Args:
            controller: pynput keyboard Controller instance
        """
        self.kb = controller

    def release_modifiers(self, *keys: Key) -> None:
        """Release modifier keys.

        Args:
            keys: Keys to release (e.g., Key.alt, Key.ctrl)
        """
        for key in keys:
            try:
                self.kb.release(key)
            except Exception as e:
                logger.warning(f"Failed to release key {key}: {e}")

    def type_text(self, text: str, release_alt: bool = True) -> None:
        """Type text, optionally releasing alt first.

        Args:
            text: Text to type
            release_alt: If True, release alt key before typing
        """
        if release_alt:
            self.release_modifiers(Key.alt)

        try:
            self.kb.type(text)
        except Exception as e:
            logger.error(f"Failed to type text: {e}")

    def press_key_sequence(self, *keys: Any) -> None:
        """Press and release a sequence of keys.

        Args:
            keys: Keys to press in sequence
        """
        for key in keys:
            try:
                self.kb.press(key)
                self.kb.release(key)
            except Exception as e:
                logger.error(f"Failed to press key {key}: {e}")

    def hold_keys(self, *keys: Any) -> None:
        """Press multiple keys simultaneously (hold them down).

        Args:
            keys: Keys to press
        """
        for key in keys:
            try:
                self.kb.press(key)
            except Exception as e:
                logger.error(f"Failed to press key {key}: {e}")

    def release_keys(self, *keys: Any) -> None:
        """Release multiple keys.

        Args:
            keys: Keys to release
        """
        for key in keys:
            try:
                self.kb.release(key)
            except Exception as e:
                logger.error(f"Failed to release key {key}: {e}")
