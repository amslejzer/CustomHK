"""Clipboard-related actions."""

import logging
from typing import Any, Dict
from pynput.keyboard import Key

from .base import Action
from .registry import register_action
from ..utils.clipboard import ClipboardManager
from ..utils.keyboard import KeyboardHelper


logger = logging.getLogger(__name__)


@register_action("paste_formatted_notes")
class PasteFormattedNotesAction(Action):
    """Formats clipboard text as a bulleted list and pastes it."""

    def __init__(self, config: Dict[str, Any], keyboard_controller: Any):
        """Initialize paste formatted notes action.

        Args:
            config: Configuration dict with 'prefix' and 'separator'
            keyboard_controller: pynput keyboard controller
        """
        super().__init__(config, keyboard_controller)
        self.prefix = config.get('prefix', '-')
        self.separator = config.get('separator', '\n\n---------------\n\n')
        self.helper = KeyboardHelper(keyboard_controller)
        self.clipboard = ClipboardManager()
        logger.debug(f"Initialized PasteFormattedNotesAction (prefix: '{self.prefix}')")

    def execute(self) -> None:
        """Get clipboard text, format it, and type it."""
        logger.info("Executing paste formatted notes")

        # Get clipboard text
        text = self.clipboard.get_text()
        if not text:
            logger.warning("No text in clipboard, aborting")
            return

        # Format as list
        formatted = self.clipboard.format_as_list(text, self.prefix)

        # Type separator and formatted text
        self.helper.type_text(self.separator + formatted, release_alt=True)


@register_action("pretty_notes")
class PrettyNotesAction(Action):
    """Performs keyboard navigation to format notes (legacy behavior)."""

    def __init__(self, config: Dict[str, Any], keyboard_controller: Any):
        """Initialize pretty notes action.

        Args:
            config: Configuration dict
            keyboard_controller: pynput keyboard controller
        """
        super().__init__(config, keyboard_controller)
        self.helper = KeyboardHelper(keyboard_controller)
        logger.debug("Initialized PrettyNotesAction")

    def execute(self) -> None:
        """Execute the legacy pretty notes key sequence."""
        logger.info("Executing pretty notes navigation")

        # Release alt first
        self.helper.release_modifiers(Key.alt)

        # Press dash
        self.helper.press_key_sequence('-')

        # Navigate up and home
        self.helper.press_key_sequence(Key.up, Key.home)

        # Re-press alt to maintain modifier state
        self.kb.press(Key.alt)
