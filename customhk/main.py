"""Main application entry point for CustomHK."""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import Config
from .hotkey_manager import HotkeyManager
from .tray_icon import TrayIconManager
import customhk.actions  # Import to register all actions
from .utils import __init__ as utils_init  # Create utils __init__.py


logger = logging.getLogger(__name__)


class CustomHKApp:
    """Main application class for CustomHK."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the application.

        Args:
            config_path: Optional path to configuration file
        """
        self.config: Optional[Config] = None
        self.hotkey_manager: Optional[HotkeyManager] = None
        self.tray_manager: Optional[TrayIconManager] = None
        self.config_path = config_path

    def setup_logging(self) -> None:
        """Configure logging based on config settings."""
        log_level = self.config.get('app.log_level', 'INFO')
        log_file = self.config.get('app.log_file', 'customhk.log')

        # Convert string log level to logging constant
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )

        # File handler (detailed)
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)

        # Console handler (simple)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(simple_formatter)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Remove existing handlers
        root_logger.handlers.clear()

        # Add handlers
        if log_file:
            root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        logger.info("Logging configured")
        logger.info(f"Log level: {log_level}")
        if log_file:
            logger.info(f"Log file: {log_file}")

    def initialize(self) -> None:
        """Initialize all application components."""
        try:
            # Load configuration
            logger.info("Loading configuration...")
            self.config = Config(self.config_path)

            # Setup logging
            self.setup_logging()

            # Initialize hotkey manager
            logger.info("Initializing hotkey manager...")
            self.hotkey_manager = HotkeyManager(self.config)

            # Initialize tray icon manager
            logger.info("Initializing tray icon...")
            self.tray_manager = TrayIconManager(
                self.config,
                self.hotkey_manager,
                on_exit=self.shutdown
            )

            logger.info("Application initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize application: {e}", exc_info=True)
            sys.exit(1)

    def run(self) -> None:
        """Run the application."""
        try:
            # Start hotkey listener
            logger.info("Starting hotkey listener...")
            self.hotkey_manager.start()

            # Start tray icon (blocking)
            logger.info("Starting system tray icon...")
            logger.info("CustomHK is now running. Right-click the tray icon for options.")
            self.tray_manager.run()

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self.shutdown()
        except Exception as e:
            logger.error(f"Application error: {e}", exc_info=True)
            self.shutdown()
            sys.exit(1)

    def shutdown(self) -> None:
        """Gracefully shutdown the application."""
        logger.info("Shutting down CustomHK...")

        if self.hotkey_manager:
            self.hotkey_manager.stop()

        if self.tray_manager:
            self.tray_manager.stop()

        logger.info("CustomHK shutdown complete")


def main() -> None:
    """Main entry point for the application."""
    # Initial basic logging setup
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )

    logger.info("Starting CustomHK...")

    # Parse command line arguments
    config_path = None
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            sys.exit(1)

    # Create and run application
    app = CustomHKApp(config_path)
    app.initialize()
    app.run()


if __name__ == '__main__':
    main()
