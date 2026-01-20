"""Validation script to check the CustomHK installation."""

import sys
from pathlib import Path

def validate():
    """Validate the CustomHK installation."""
    print("=" * 60)
    print("CustomHK Installation Validator")
    print("=" * 60)
    print()

    errors = []
    warnings = []

    # Check Python version
    print("✓ Checking Python version...")
    if sys.version_info < (3, 8):
        errors.append(f"Python 3.8+ required, found {sys.version}")
    else:
        print(f"  Python {sys.version_info.major}.{sys.version_info.minor} - OK")

    # Check required files
    print("\n✓ Checking required files...")
    required_files = [
        'config.yaml',
        'requirements.txt',
        'customhk/__init__.py',
        'customhk/main.py',
        'customhk/config.py',
        'customhk/hotkey_manager.py',
        'customhk/tray_icon.py',
    ]

    for file in required_files:
        path = Path(file)
        if not path.exists():
            errors.append(f"Missing required file: {file}")
        else:
            print(f"  {file} - OK")

    # Check optional files
    print("\n✓ Checking optional files...")
    if not Path('CHK_icon.png').exists():
        warnings.append("CHK_icon.png not found - will use default icon")
    else:
        print("  CHK_icon.png - OK")

    # Try importing the package
    print("\n✓ Testing package imports...")
    try:
        import customhk
        print(f"  customhk v{customhk.__version__} - OK")
    except ImportError as e:
        errors.append(f"Cannot import customhk: {e}")

    # Try importing dependencies
    print("\n✓ Checking dependencies...")
    deps = ['pynput', 'pystray', 'PIL', 'win32clipboard', 'yaml']
    for dep in deps:
        try:
            __import__(dep)
            print(f"  {dep} - OK")
        except ImportError:
            errors.append(f"Missing dependency: {dep}")

    # Try loading config
    print("\n✓ Testing configuration...")
    try:
        from customhk.config import Config
        config = Config()
        print(f"  Config loaded from: {config.config_path}")
        print(f"  App name: {config.get('app.name')}")
        print(f"  Global hotkeys: {len(config.get_global_hotkeys())}")
    except Exception as e:
        errors.append(f"Config error: {e}")

    # Try loading actions
    print("\n✓ Testing action registry...")
    try:
        from customhk.actions import get_registry
        registry = get_registry()
        actions = registry.list_actions()
        print(f"  Registered actions: {len(actions)}")
        for action in sorted(actions):
            print(f"    - {action}")
    except Exception as e:
        errors.append(f"Action registry error: {e}")

    # Print summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)

    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")

    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")

    if not errors and not warnings:
        print("\n✅ All checks passed! CustomHK is ready to use.")
        print("\nTo run the application:")
        print("  python -m customhk.main")
    elif not errors:
        print("\n✅ Validation passed with warnings.")
        print("\nTo run the application:")
        print("  python -m customhk.main")
    else:
        print("\n❌ Validation failed. Please fix errors above.")
        return 1

    print()
    return 0


if __name__ == '__main__':
    sys.exit(validate())
