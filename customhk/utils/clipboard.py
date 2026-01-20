"""Clipboard utilities for Windows."""

import logging
from typing import Optional
import win32clipboard


logger = logging.getLogger(__name__)


class ClipboardManager:
    """Manages clipboard operations with proper error handling."""

    @staticmethod
    def get_text() -> Optional[str]:
        """Get text from clipboard.

        Returns:
            Clipboard text or None if clipboard doesn't contain text or error occurs
        """
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                return text
            else:
                logger.debug("Clipboard does not contain text")
                return None
        except Exception as e:
            logger.error(f"Failed to get clipboard text: {e}")
            return None
        finally:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass

    @staticmethod
    def set_text(text: str) -> bool:
        """Set clipboard text.

        Args:
            text: Text to set in clipboard

        Returns:
            True if successful, False otherwise
        """
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            return True
        except Exception as e:
            logger.error(f"Failed to set clipboard text: {e}")
            return False
        finally:
            try:
                win32clipboard.CloseClipboard()
            except:
                pass

    @staticmethod
    def format_as_list(text: str, prefix: str = "-") -> str:
        """Format text lines with prefix (e.g., convert to bullet list).

        Args:
            text: Input text
            prefix: Prefix to add to each line

        Returns:
            Formatted text with prefix on each line
        """
        if not text:
            return ""

        lines = text.splitlines()
        formatted_lines = [f"{prefix}{line}" for line in lines]
        return "\n".join(formatted_lines)
