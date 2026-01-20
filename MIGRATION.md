# Migration Guide: CustomHK v1 to v2

This guide will help you migrate from the old `CustomHK.pyw` script to the new modular version.

## What's Changed

### Architecture
- **Old**: Single 95-line script with global variables
- **New**: Modular package with separate concerns (config, actions, managers)

### Configuration
- **Old**: Hardcoded in Python script
- **New**: External YAML file (`config.yaml`)

### Actions
- **Old**: Functions defined in main script
- **New**: Plugin-style classes in `customhk/actions/`

### Extensibility
- **Old**: Edit Python code to add features
- **New**: Add action classes, update config file

## Migration Steps

### 1. Backup Your Old Setup

Your original script has been backed up to `CustomHK.pyw.backup`

### 2. Install Dependencies

```bash
# Activate your existing virtual environment
.venv\Scripts\activate

# Install new dependencies
pip install -r requirements.txt
```

### 3. Customize Your Configuration

Edit `config.yaml` to match your preferences:

```yaml
user:
  signature: "Thanks,\nAndrew"  # Change to your signature
```

### 4. Update Your Startup Shortcut

**Old shortcut target:**
```
C:\Path\To\.venv\Scripts\pythonw.exe CustomHK.pyw
```

**New shortcut target:**
```
C:\Path\To\.venv\Scripts\pythonw.exe -m customhk.main
```

Or install the package and use:
```bash
pip install -e .
```

Then the shortcut target becomes:
```
C:\Path\To\.venv\Scripts\customhk.exe
```

### 5. Test the New Version

Before updating your startup shortcut:

1. Run the new version manually:
   ```bash
   python -m customhk.main
   ```

2. Test your hotkeys:
   - Alt+1: Type signature
   - Alt+2: Paste formatted notes
   - Alt+3: Pretty notes navigation
   - Alt+Shift+H: Show GUI wizard (NEW!)

3. Try the system tray menu:
   - Right-click the tray icon
   - Toggle enabled/disabled
   - Try "Reload Config"

### 6. Update Startup

Once you've verified everything works:

1. Remove the old shortcut from your Startup folder
2. Create a new shortcut with the updated target
3. Test by logging out and back in

## Feature Comparison

| Feature | Old Version | New Version |
|---------|-------------|-------------|
| Type Signature | ✅ Alt+1 | ✅ Alt+1 (configurable) |
| Paste Formatted Notes | ✅ Alt+2 | ✅ Alt+2 (configurable) |
| Pretty Notes | ✅ Alt+3 | ✅ Alt+3 (configurable) |
| System Tray | ✅ Basic | ✅ Enhanced with reload |
| Enable/Disable | ✅ | ✅ Improved state management |
| Configuration | ❌ Hardcoded | ✅ YAML file |
| Logging | ❌ Commented prints | ✅ Proper logging system |
| Error Handling | ❌ Minimal | ✅ Comprehensive |
| GUI Wizard | ❌ | ✅ Alt+Shift+H |
| App-Specific Hotkeys | ❌ | ✅ Configurable |
| Custom Actions | ⚠️ Edit Python | ✅ Plugin system |
| Reload Config | ❌ | ✅ Via tray menu |

## New Features to Explore

### 1. GUI Wizard
Press Alt+Shift+H to bring up a searchable list of all actions. Great for discovering or triggering actions you don't remember the hotkey for.

### 2. Configuration Reloading
Change your hotkeys or settings in `config.yaml`, then right-click the tray icon and select "Reload Config". No need to restart!

### 3. Logging
Check `customhk.log` to see what's happening under the hood. Useful for debugging or understanding behavior.

### 4. App-Specific Hotkeys (Coming Soon)
Once configured, you can have different hotkeys or actions based on which application is active.

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Hotkeys don't work
1. Check the tray icon exists
2. Right-click → verify "Enabled" is checked
3. Check `customhk.log` for errors

### Want to revert to the old version?
```bash
# Restore the backup
cp CustomHK.pyw.backup CustomHK.pyw

# Update your shortcut back to:
# C:\Path\To\.venv\Scripts\pythonw.exe CustomHK.pyw
```

## Getting Help

- Check `customhk.log` for error messages
- Review `config.yaml` for syntax errors
- See `README.md` for full documentation

## Next Steps

Now that you're migrated, you can:

1. **Customize your hotkeys** - Edit `config.yaml` to change key combinations
2. **Add new actions** - See README.md for the action creation guide
3. **Adjust logging** - Set `log_level: "DEBUG"` for verbose output
4. **Experiment with the wizard** - Press Alt+Shift+H and explore

Enjoy your upgraded CustomHK!
