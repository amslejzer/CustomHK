# CustomHK - Custom Hotkey Automation Tool

A powerful and extensible Windows hotkey automation tool with system tray integration, configurable actions, and a GUI wizard for quick access.

## Features

- **Global Hotkeys**: Define keyboard shortcuts that work across all applications
- **App-Specific Hotkeys**: Create hotkeys that only activate in specific windows/applications
- **GUI Wizard**: Quick access menu to browse and execute actions (Alt+Shift+H)
- **Extensible Actions**: Easy-to-add plugin-style action system
- **YAML Configuration**: Human-readable configuration file
- **System Tray Integration**: Enable/disable hotkeys, reload config without restarting
- **Comprehensive Logging**: Debug issues with configurable logging levels

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows OS

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install in development mode:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Application

Run the application directly:
```bash
python -m customhk.main
```

Or if installed via pip:
```bash
customhk
```

To specify a custom config file:
```bash
customhk path/to/config.yaml
```

### Running at Startup

To run CustomHK automatically when Windows starts:

1. Create a shortcut to the script:
   - Right-click on desktop → New → Shortcut
   - Target: `C:\Path\To\Your\.venv\Scripts\pythonw.exe -m customhk.main`
   - Name it "CustomHK"

2. Move the shortcut to your Startup folder:
   - Press `Win+R` and type: `shell:startup`
   - Move the shortcut into this folder

The application will now start minimized to the system tray on login.

## Configuration

Configuration is stored in `config.yaml`. The file is well-commented and self-documenting.

### Basic Configuration Structure

```yaml
app:
  name: "CustomHK"
  icon: "CHK_icon.png"
  log_level: "INFO"

user:
  signature: "Thanks,\nAndrew"

hotkeys:
  global:
    - key: "<alt>+1"
      action: "type_signature"
      enabled: true
```

### Default Hotkeys

- **Alt+1**: Type your signature
- **Alt+2**: Format clipboard text as bulleted list and paste
- **Alt+3**: Navigation helper for note formatting
- **Alt+Shift+H**: Show the GUI wizard for action selection

### Adding Custom Hotkeys

Edit `config.yaml` and add entries under `hotkeys.global`:

```yaml
hotkeys:
  global:
    - key: "<ctrl>+<shift>+x"
      action: "your_action_name"
      enabled: true
      description: "What this hotkey does"
```

### App-Specific Hotkeys

To create hotkeys that only work in specific applications:

```yaml
hotkeys_conditional:
  - window_title: "Outlook"
    key: "<ctrl>+<shift>+s"
    action: "type_signature"

  - window_title: "Chrome|Firefox|Edge"
    key: "<ctrl>+<shift>+n"
    action: "paste_formatted_notes"
```

The `window_title` field supports regex patterns for flexible matching.

## System Tray Menu

Right-click the tray icon to access:

- **Enabled**: Toggle hotkeys on/off
- **Reload Config**: Reload configuration without restarting
- **Exit**: Quit the application

## Creating Custom Actions

CustomHK uses a plugin-style architecture. To create a new action:

1. Create a new file in `customhk/actions/` (e.g., `my_action.py`)

2. Define your action class:

```python
from typing import Any, Dict
from .base import Action
from .registry import register_action

@register_action("my_custom_action")
class MyCustomAction(Action):
    def __init__(self, config: Dict[str, Any], keyboard_controller: Any):
        super().__init__(config, keyboard_controller)
        # Your initialization here

    def execute(self) -> None:
        # Your action logic here
        self.kb.type("Hello World!")
```

3. Import your module in `customhk/actions/__init__.py`:

```python
from . import my_action
```

4. Add it to your `config.yaml`:

```yaml
hotkeys:
  global:
    - key: "<alt>+4"
      action: "my_custom_action"
      enabled: true
```

5. Reload the config via the tray menu or restart the app

## Architecture

```
CustomHK/
├── customhk/                   # Main package
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration management
│   ├── hotkey_manager.py       # Hotkey registration & lifecycle
│   ├── tray_icon.py            # System tray integration
│   ├── actions/                # Action plugins
│   │   ├── __init__.py
│   │   ├── base.py             # Base Action class
│   │   ├── registry.py         # Action registry system
│   │   ├── signature.py        # Signature typing action
│   │   ├── clipboard.py        # Clipboard actions
│   │   └── wizard.py           # GUI wizard action
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── clipboard.py        # Clipboard utilities
│       ├── keyboard.py         # Keyboard helpers
│       └── window.py           # Window detection
├── config.yaml                 # User configuration
├── requirements.txt            # Dependencies
├── pyproject.toml              # Package metadata
└── CHK_icon.png                # Tray icon
```

## Logging

Logs are written to `customhk.log` by default. Adjust log level in `config.yaml`:

```yaml
app:
  log_level: "DEBUG"  # DEBUG, INFO, WARNING, ERROR
  log_file: "customhk.log"
```

## Troubleshooting

### Hotkeys Not Working

1. Check if the application is running (look for tray icon)
2. Right-click tray icon and ensure "Enabled" is checked
3. Check `customhk.log` for errors
4. Verify your hotkey syntax in `config.yaml`

### Application Won't Start

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check `customhk.log` for error messages
3. Verify `config.yaml` is valid YAML syntax
4. Ensure `CHK_icon.png` exists (or app will use default icon)

### Config Changes Not Taking Effect

- Use "Reload Config" from the tray menu
- Or restart the application

## Future Enhancements

Planned features:

- Macro recording and playback
- Visual macro editor
- More clipboard transformations
- Text expansion/snippets
- Window automation scripts
- Scheduled actions

## Contributing

This is a personal tool, but improvements are welcome. When adding features:

1. Follow the existing code structure
2. Add proper logging
3. Handle errors gracefully
4. Update this README
5. Test thoroughly on Windows

## License

Personal use project. Use and modify as needed.

## Credits

Built with:
- [pynput](https://github.com/moses-palmer/pynput) - Keyboard control
- [pystray](https://github.com/moses-palmer/pystray) - System tray icon
- [PyYAML](https://pyyaml.org/) - Configuration parsing
- [pywin32](https://github.com/mhammond/pywin32) - Windows API access
