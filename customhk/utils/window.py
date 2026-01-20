"""Window detection and management utilities for Windows."""

import logging
import re
from typing import Optional
import ctypes
from ctypes import wintypes


logger = logging.getLogger(__name__)


class WindowManager:
    """Manages window detection and querying for app-specific hotkeys."""

    @staticmethod
    def get_active_window_title() -> Optional[str]:
        """Get the title of the currently active window.

        Returns:
            Window title string or None if unable to get title
        """
        try:
            # Get handle to foreground window
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return None

            # Get window title length
            length = user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return None

            # Get window title
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)

            return buffer.value
        except Exception as e:
            logger.error(f"Failed to get active window title: {e}")
            return None

    @staticmethod
    def get_active_window_class() -> Optional[str]:
        """Get the class name of the currently active window.

        Returns:
            Window class name or None if unable to get class
        """
        try:
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return None

            buffer = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, buffer, 256)

            return buffer.value
        except Exception as e:
            logger.error(f"Failed to get active window class: {e}")
            return None

    @staticmethod
    def get_active_process_name() -> Optional[str]:
        """Get the process name of the currently active window.

        Returns:
            Process name or None if unable to get process name
        """
        try:
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return None

            # Get process ID
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            # Open process
            PROCESS_QUERY_INFORMATION = 0x0400
            PROCESS_VM_READ = 0x0010
            process = kernel32.OpenProcess(
                PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                False,
                pid
            )

            if not process:
                return None

            # Get process name
            buffer = ctypes.create_unicode_buffer(260)
            size = wintypes.DWORD(260)

            if kernel32.QueryFullProcessImageNameW(process, 0, buffer, ctypes.byref(size)):
                kernel32.CloseHandle(process)
                # Extract just the process name from full path
                return buffer.value.split('\\')[-1]

            kernel32.CloseHandle(process)
            return None
        except Exception as e:
            logger.error(f"Failed to get active process name: {e}")
            return None

    @staticmethod
    def matches_window_pattern(pattern: str, case_sensitive: bool = False) -> bool:
        """Check if current window title matches a pattern.

        Args:
            pattern: String or regex pattern to match against window title
            case_sensitive: Whether to match case-sensitively

        Returns:
            True if current window matches pattern, False otherwise
        """
        title = WindowManager.get_active_window_title()
        if not title:
            return False

        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            return bool(re.search(pattern, title, flags))
        except re.error as e:
            logger.error(f"Invalid regex pattern '{pattern}': {e}")
            return False

    @staticmethod
    def is_window_active(window_identifier: str) -> bool:
        """Check if a window matching identifier is active.

        Args:
            window_identifier: Can be window title substring, regex pattern, or process name

        Returns:
            True if matching window is active
        """
        title = WindowManager.get_active_window_title()
        process = WindowManager.get_active_process_name()

        if not title:
            return False

        # Try substring match on title
        if window_identifier.lower() in title.lower():
            return True

        # Try regex match on title
        if WindowManager.matches_window_pattern(window_identifier):
            return True

        # Try process name match
        if process and window_identifier.lower() in process.lower():
            return True

        return False
