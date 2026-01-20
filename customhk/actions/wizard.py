"""GUI wizard for interactive hotkey selection."""

import logging
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, Optional, Callable
import threading

from .base import Action
from .registry import register_action, get_registry


logger = logging.getLogger(__name__)


class HotkeyWizard:
    """GUI wizard for selecting and executing actions."""

    def __init__(self, action_registry, config, on_action_selected: Optional[Callable] = None):
        """Initialize the wizard.

        Args:
            action_registry: ActionRegistry instance
            config: Configuration object
            on_action_selected: Callback when action is selected
        """
        self.registry = action_registry
        self.config = config
        self.on_action_selected = on_action_selected
        self.window: Optional[tk.Tk] = None
        self.selected_action: Optional[str] = None

    def show(self) -> None:
        """Show the wizard window."""
        if self.window is not None:
            # Window already exists, bring to front
            try:
                self.window.lift()
                self.window.focus_force()
                return
            except:
                self.window = None

        # Create new window
        self.window = tk.Tk()
        self.window.title("CustomHK - Hotkey Wizard")
        self.window.geometry("600x400")

        # Make window stay on top
        self.window.attributes('-topmost', True)

        # Configure grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            self.window,
            text="Select an Action",
            font=('Segoe UI', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=20, padx=20, sticky='w')

        # Search box
        search_frame = ttk.Frame(self.window)
        search_frame.grid(row=1, column=0, pady=10, padx=20, sticky='ew')

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side='left', padx=(0, 10))

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        search_entry.focus()

        # Action list frame
        list_frame = ttk.Frame(self.window)
        list_frame.grid(row=2, column=0, pady=10, padx=20, sticky='nsew')
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Listbox for actions
        self.action_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 11),
            activestyle='none',
            selectmode='single',
            height=12
        )
        self.action_listbox.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.action_listbox.yview)

        # Populate actions
        self._populate_actions()

        # Bind events
        self.action_listbox.bind('<Double-Button-1>', self._on_action_selected)
        self.action_listbox.bind('<Return>', self._on_action_selected)
        search_var.trace('w', lambda *args: self._filter_actions(search_var.get()))

        # Button frame
        button_frame = ttk.Frame(self.window)
        button_frame.grid(row=3, column=0, pady=20, padx=20, sticky='ew')

        execute_btn = ttk.Button(
            button_frame,
            text="Execute",
            command=self._on_execute_clicked
        )
        execute_btn.pack(side='right', padx=5)

        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel_clicked
        )
        cancel_btn.pack(side='right', padx=5)

        # Bind escape key to close
        self.window.bind('<Escape>', lambda e: self._on_cancel_clicked())

        # Start main loop
        self.window.mainloop()

    def _populate_actions(self, filter_text: str = "") -> None:
        """Populate the action list.

        Args:
            filter_text: Optional filter string
        """
        self.action_listbox.delete(0, tk.END)

        actions = self.registry.list_actions()
        actions.sort()

        for action_name in actions:
            if not filter_text or filter_text.lower() in action_name.lower():
                # Format action name for display
                display_name = action_name.replace('_', ' ').title()
                self.action_listbox.insert(tk.END, f"{display_name}  ({action_name})")

    def _filter_actions(self, filter_text: str) -> None:
        """Filter actions based on search text.

        Args:
            filter_text: Search filter
        """
        self._populate_actions(filter_text)

    def _on_action_selected(self, event=None) -> None:
        """Handle action selection from list."""
        selection = self.action_listbox.curselection()
        if not selection:
            return

        selected_text = self.action_listbox.get(selection[0])
        # Extract action name from parentheses
        if '(' in selected_text and ')' in selected_text:
            action_name = selected_text.split('(')[1].split(')')[0]
            self.selected_action = action_name
            self._execute_and_close()

    def _on_execute_clicked(self) -> None:
        """Handle execute button click."""
        self._on_action_selected()

    def _on_cancel_clicked(self) -> None:
        """Handle cancel button click."""
        if self.window:
            self.window.destroy()
            self.window = None

    def _execute_and_close(self) -> None:
        """Execute selected action and close wizard."""
        if self.selected_action and self.on_action_selected:
            self.on_action_selected(self.selected_action)

        self._on_cancel_clicked()


@register_action("show_wizard")
class ShowWizardAction(Action):
    """Shows the GUI wizard for selecting actions."""

    def __init__(self, config: Dict[str, Any], keyboard_controller: Any):
        """Initialize show wizard action.

        Args:
            config: Configuration dict with app config
            keyboard_controller: pynput keyboard controller
        """
        super().__init__(config, keyboard_controller)
        self.app_config = config
        logger.debug("Initialized ShowWizardAction")

    def execute(self) -> None:
        """Show the wizard in a separate thread."""
        logger.info("Showing hotkey wizard")

        # Run wizard in separate thread to avoid blocking
        def run_wizard():
            try:
                registry = get_registry()
                wizard = HotkeyWizard(
                    registry,
                    self.app_config,
                    on_action_selected=self._on_action_selected
                )
                wizard.show()
            except Exception as e:
                logger.error(f"Error showing wizard: {e}", exc_info=True)

        wizard_thread = threading.Thread(target=run_wizard, daemon=True)
        wizard_thread.start()

    def _on_action_selected(self, action_name: str) -> None:
        """Handle action selection from wizard.

        Args:
            action_name: Name of selected action
        """
        logger.info(f"Action selected from wizard: {action_name}")

        # Get action instance and execute it
        registry = get_registry()
        action = registry.get_instance(action_name)

        if action:
            try:
                action()
            except Exception as e:
                logger.error(f"Error executing action {action_name}: {e}", exc_info=True)
        else:
            logger.error(f"Action {action_name} not found in registry")
