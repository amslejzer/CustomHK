"""Base classes for hotkey actions."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


logger = logging.getLogger(__name__)


class Action(ABC):
    """Base class for all hotkey actions."""

    def __init__(self, config: Dict[str, Any], keyboard_controller: Any):
        """Initialize action.

        Args:
            config: Configuration dictionary for this action
            keyboard_controller: pynput keyboard controller instance
        """
        self.config = config
        self.kb = keyboard_controller
        self.name = self.__class__.__name__
        self.enabled = True

    @abstractmethod
    def execute(self) -> None:
        """Execute the action. Must be implemented by subclasses."""
        pass

    def pre_execute(self) -> bool:
        """Called before execute(). Return False to cancel execution.

        Returns:
            True to continue with execution, False to cancel
        """
        if not self.enabled:
            logger.debug(f"Action {self.name} is disabled, skipping")
            return False
        return True

    def post_execute(self, success: bool, error: Optional[Exception] = None) -> None:
        """Called after execute() completes.

        Args:
            success: Whether execution completed successfully
            error: Exception if one occurred, None otherwise
        """
        if success:
            logger.debug(f"Action {self.name} completed successfully")
        else:
            logger.error(f"Action {self.name} failed: {error}")

    def __call__(self) -> None:
        """Make action callable. Handles pre/post execution hooks and error handling."""
        if not self.pre_execute():
            return

        try:
            self.execute()
            self.post_execute(success=True)
        except Exception as e:
            self.post_execute(success=False, error=e)
            logger.exception(f"Error executing action {self.name}: {e}")

    def enable(self) -> None:
        """Enable this action."""
        self.enabled = True
        logger.info(f"Action {self.name} enabled")

    def disable(self) -> None:
        """Disable this action."""
        self.enabled = False
        logger.info(f"Action {self.name} disabled")
