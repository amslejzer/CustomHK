# Quick Start Guide

Get CustomHK up and running in 5 minutes!

## First Time Setup

### 1. Install Dependencies (Windows)

```bash
# Make sure you're in the project directory
cd C:\Path\To\CustomHK

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Validate Installation

```bash
python validate.py
```

This will check that everything is set up correctly.

### 3. Test Run

```bash
python -m customhk.main
```

You should see:
- A small icon appear in your system tray
- A message: "CustomHK is now running..."

### 4. Test Your Hotkeys

Try these default hotkeys:

- **Alt+1** - Types your signature
- **Alt+2** - Formats clipboard as bullet list
- **Alt+3** - Navigation helper for notes
- **Alt+Shift+H** - Opens the GUI wizard (NEW!)

### 5. Check the System Tray

Right-click the CustomHK icon in your system tray to see:
- Enable/Disable toggle
- Reload Config option
- Exit

## Customization

### Change Your Signature

Edit `config.yaml`:

```yaml
user:
  signature: "Best regards,\nYour Name"
```

Then right-click tray icon → Reload Config

### Add a New Hotkey

Edit `config.yaml`:

```yaml
hotkeys:
  global:
    - key: "<ctrl>+<shift>+h"
      action: "type_signature"
      enabled: true
```

Right-click tray icon → Reload Config

### Adjust Logging

For more detailed logs, edit `config.yaml`:

```yaml
app:
  log_level: "DEBUG"  # Change from INFO to DEBUG
```

Check `customhk.log` to see what's happening.

## Auto-Start at Login

### Create Startup Shortcut

1. Press `Win+R` and type: `shell:startup`
2. Create a new shortcut in that folder:
   - **Target**: `C:\Path\To\CustomHK\.venv\Scripts\pythonw.exe -m customhk.main`
   - **Start in**: `C:\Path\To\CustomHK`
   - **Name**: CustomHK

Now CustomHK will start automatically when you log in!

## Next Steps

- Read [README.md](README.md) for full documentation
- See [MIGRATION.md](MIGRATION.md) if upgrading from the old version
- Explore creating custom actions

## Troubleshooting

### Nothing happens when I press hotkeys

1. Check if CustomHK is running (look for tray icon)
2. Right-click tray icon → make sure "Enabled" is checked
3. Check `customhk.log` for errors

### Import errors

```bash
pip install -r requirements.txt
```

### Config not reloading

- Try exiting and restarting the application
- Check `customhk.log` for error messages
- Validate your YAML syntax (spaces, not tabs!)

## Common Issues

**Q: The GUI wizard doesn't show**
A: Try running `pip install tkinter` or make sure Python was installed with tk support

**Q: Hotkeys conflict with other software**
A: Change the key combinations in `config.yaml`

**Q: Want to disable a hotkey temporarily**
A: Set `enabled: false` in config.yaml and reload

## Getting Help

1. Check `customhk.log` for detailed error messages
2. Run `python validate.py` to diagnose issues
3. Review the full [README.md](README.md)

---

**You're all set!** Press Alt+Shift+H to see all available actions.
