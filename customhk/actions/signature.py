"""Signature typing action."""

import logging
from typing import Any, Dict

from .base import Action
from .registry import register_action
from ..utils.keyboard import KeyboardHelper


logger = logging.getLogger(__name__)


@register_action("type_signature")
class TypeSignatureAction(Action):
    """Types a configured signature text."""

    def __init__(self, config: Dict[str, Any], keyboard_controller: Any):
        """Initialize signature action.

        Args:
            config: Configuration dict, should contain 'signature' key
            keyboard_controller: pynput keyboard controller
        """
        super().__init__(config, keyboard_controller)
        self.signature = config.get('signature', 'Thanks')
        self.helper = KeyboardHelper(keyboard_controller)
        logger.debug(f"Initialized TypeSignatureAction with signature: {self.signature[:20]}...")

    def execute(self) -> None:
        """Type the configured signature."""
        logger.info("Typing signature")
        self.helper.type_text(self.signature, release_alt=True)
