"""System tray icon management."""

import logging
from pathlib import Path
from typing import Optional, Callable
import pystray
from PIL import Image


logger = logging.getLogger(__name__)


class TrayIconManager:
    """Manages the system tray icon and menu."""

    def __init__(
        self,
        config,
        hotkey_manager,
        on_exit: Optional[Callable] = None
    ):
        """Initialize tray icon manager.

        Args:
            config: Configuration object
            hotkey_manager: HotkeyManager instance
            on_exit: Callback when exit is requested
        """
        self.config = config
        self.hotkey_manager = hotkey_manager
        self.on_exit_callback = on_exit
        self.icon: Optional[pystray.Icon] = None

        # Load icon image
        icon_path = self._find_icon()
        if icon_path and icon_path.exists():
            self.icon_image = Image.open(icon_path)
        else:
            # Create a simple default icon if file not found
            logger.warning(f"Icon not found at {icon_path}, using default")
            self.icon_image = self._create_default_icon()

    def _find_icon(self) -> Optional[Path]:
        """Find the icon file.

        Returns:
            Path to icon file or None
        """
        icon_name = self.config.get('app.icon', 'CHK_icon.png')

        # Search in various locations
        search_paths = [
            Path.cwd() / icon_name,
            Path(__file__).parent.parent / icon_name,
            Path.home() / '.customhk' / icon_name,
        ]

        for path in search_paths:
            if path.exists():
                logger.info(f"Found icon at: {path}")
                return path

        return None

    def _create_default_icon(self) -> Image.Image:
        """Create a simple default icon.

        Returns:
            PIL Image
        """
        # Create a simple 64x64 icon with a colored square
        img = Image.new('RGB', (64, 64), color=(73, 109, 137))
        return img

    def _create_menu(self) -> pystray.Menu:
        """Create the tray icon menu.

        Returns:
            pystray.Menu instance
        """
        app_name = self.config.get('app.name', 'CustomHK')

        return pystray.Menu(
            pystray.MenuItem(app_name, None),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                'Enabled',
                self._on_toggle,
                checked=lambda item: self.hotkey_manager.is_running()
            ),
            pystray.MenuItem('Reload Config', self._on_reload_config),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', self._on_exit)
        )

    def _on_toggle(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Handle enable/disable toggle.

        Args:
            icon: Tray icon instance
            item: Menu item
        """
        new_state = self.hotkey_manager.toggle()
        status = "enabled" if new_state else "disabled"
        logger.info(f"Hotkeys {status}")

        # Update icon menu
        icon.update_menu()

    def _on_reload_config(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Handle config reload request.

        Args:
            icon: Tray icon instance
            item: Menu item
        """
        logger.info("Reloading configuration")
        try:
            self.config.reload()
            self.hotkey_manager.restart()
            logger.info("Configuration reloaded successfully")
        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")

    def _on_exit(self, icon: pystray.Icon, item: pystray.MenuItem) -> None:
        """Handle exit request.

        Args:
            icon: Tray icon instance
            item: Menu item
        """
        logger.info("Exit requested from tray icon")

        # Stop hotkey listener
        self.hotkey_manager.stop()

        # Stop tray icon
        icon.stop()

        # Call exit callback if provided
        if self.on_exit_callback:
            self.on_exit_callback()

    def run(self) -> None:
        """Start the tray icon (blocking call)."""
        app_name = self.config.get('app.name', 'CustomHK')

        self.icon = pystray.Icon(
            "customhk_icon",
            self.icon_image,
            app_name,
            self._create_menu()
        )

        logger.info("Starting system tray icon")
        self.icon.run()

    def run_detached(self) -> None:
        """Start the tray icon in detached mode (non-blocking)."""
        app_name = self.config.get('app.name', 'CustomHK')

        self.icon = pystray.Icon(
            "customhk_icon",
            self.icon_image,
            app_name,
            self._create_menu()
        )

        logger.info("Starting system tray icon (detached)")
        self.icon.run_detached()

    def stop(self) -> None:
        """Stop the tray icon."""
        if self.icon:
            self.icon.stop()
            logger.info("Stopped system tray icon")
