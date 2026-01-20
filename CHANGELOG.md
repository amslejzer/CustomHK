# Changelog

All notable changes to CustomHK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-20

### Added

#### Core Features
- **YAML Configuration System**: External `config.yaml` file for easy customization without code changes
- **GUI Hotkey Wizard**: Searchable action selector (Alt+Shift+H) for discovering and executing actions
- **Plugin Architecture**: Extensible action system using decorators and registry pattern
- **Window Detection**: Utilities for app-specific hotkeys based on active window/process
- **Live Config Reload**: Update settings via system tray menu without restarting
- **Comprehensive Logging**: File and console logging with configurable levels (DEBUG, INFO, WARNING, ERROR)

#### Actions
- `type_signature` - Types configured signature text (Alt+1)
- `paste_formatted_notes` - Formats clipboard as bulleted list (Alt+2)
- `pretty_notes` - Navigation helper for note formatting (Alt+3)
- `show_wizard` - Opens GUI action selector (Alt+Shift+H)

#### Infrastructure
- `HotkeyManager` - Central hotkey registration and lifecycle management
- `TrayIconManager` - Enhanced system tray with enable/disable and reload options
- `ActionRegistry` - Plugin system for registering and managing actions
- `Config` - YAML configuration loader with dot notation access
- `ClipboardManager` - Safe clipboard operations with error handling
- `KeyboardHelper` - Keyboard automation utilities
- `WindowManager` - Windows API integration for window/process detection

#### Documentation
- Comprehensive README with installation, usage, and customization guide
- QUICKSTART guide for 5-minute setup
- MIGRATION guide for upgrading from v1.0
- Validation script to check installation (`validate.py`)
- Inline code documentation and type hints

#### Developer Experience
- Modern Python packaging with `pyproject.toml`
- `requirements.txt` for dependency management
- Proper `.gitignore` for Python projects
- Modular package structure for maintainability
- Type hints throughout codebase
- Consistent error handling and logging

### Changed

#### Architecture
- **From**: Single 95-line script with global variables
- **To**: Modular package with ~2,700 lines across 23 files
- Separated concerns into distinct modules (config, actions, managers, utils)
- Object-oriented design replacing procedural code
- Plugin-based actions instead of hardcoded functions

#### Configuration
- **From**: Hardcoded settings in Python script
- **To**: External YAML file with comments and examples
- User signature now configurable in `config.yaml`
- Hotkey bindings customizable without code changes
- Action-specific settings in dedicated sections

#### Hotkey Management
- **From**: Global listener variable with awkward state management
- **To**: `HotkeyManager` class with proper lifecycle
- Enable/disable functionality improved
- Support for conditional (app-specific) hotkeys
- Dynamic hotkey registration from config

#### System Tray
- **From**: Basic menu with enable/disable and exit
- **To**: Enhanced menu with reload config option
- Better state synchronization with hotkey manager
- Improved error handling and icon loading

#### Error Handling
- **From**: Minimal error handling, commented-out print statements
- **To**: Comprehensive try-catch blocks with logging
- Graceful degradation when features unavailable
- Helpful error messages for troubleshooting

### Fixed
- Clipboard operations now handle errors gracefully
- Keyboard operations release modifiers properly
- State management no longer relies on global variables
- System tray menu reflects actual enabled/disabled state
- Icon loading has fallback to default if file not found

### Security
- No hardcoded credentials or sensitive data
- Proper input validation for config values
- Safe clipboard operations with cleanup

## [1.0.0] - 2024-02-07

### Initial Version (Legacy)
- Basic hotkey functionality (Alt+1, Alt+2, Alt+3)
- Type signature action
- Paste formatted notes action
- Pretty notes navigation
- System tray icon with enable/disable
- Windows startup integration

### Limitations of v1.0
- All configuration hardcoded in script
- Single file with global variables
- No error handling or logging
- Difficult to extend or customize
- No documentation
- Commented-out debug code

---

## Migration Guide

Upgrading from v1.0 to v2.0? See [MIGRATION.md](MIGRATION.md) for detailed instructions.

## Future Roadmap

Planned features for future releases:

### [2.1.0] - Planned
- Macro recording and playback
- Text snippet expansion
- More clipboard transformations (case conversion, regex replace, etc.)
- App-specific hotkey configurations

### [3.0.0] - Planned
- Visual configuration editor
- Macro editor GUI
- Scheduled actions
- Window automation scripts
- Cloud sync for configurations

---

## Contributing

This is a personal project, but improvements are welcome! When contributing:

1. Follow the existing code structure and conventions
2. Add proper logging and error handling
3. Include docstrings and type hints
4. Update documentation
5. Test thoroughly on Windows

## License

Personal use project. Use and modify as needed.
