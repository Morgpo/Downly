# =====
#
#   Downly UI URL Input Component
#
#   Handles URL input with placeholder management and validation.
#
# =====

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class URLInput:
    """
    URL input component with placeholder management.
    Provides clean interface for URL entry and validation feedback.
    """
    
    def __init__(self, parent: tk.Widget, placeholder: str = "Paste YouTube link here..."):
        """
        Initialize URL input component.
        
        Args:
            parent: Parent widget to contain this component
            placeholder: Placeholder text to display when empty
        """
        self.parent = parent
        self.placeholder = placeholder
        
        # Variables
        self.url_var = tk.StringVar()
        
        # Widget references
        self.url_frame: Optional[ttk.LabelFrame] = None
        self.url_entry: Optional[ttk.Entry] = None
        
        # Callbacks
        self.on_url_change: Optional[Callable[[str], None]] = None
        
        self._create_widgets()
        self._bind_events()
        self._set_initial_state()
    
    def _create_widgets(self) -> None:
        """Create the URL input widgets."""
        self.url_frame = ttk.LabelFrame(
            self.parent, 
            text="YouTube URL", 
            padding="15", 
            style="Modern.TLabelframe"
        )
        self.url_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_entry = ttk.Entry(
            self.url_frame, 
            textvariable=self.url_var,
            style="Modern.TEntry"
        )
        self.url_entry.pack(fill=tk.X)
    
    def _bind_events(self) -> None:
        """Bind events for placeholder management."""
        self.url_entry.bind('<FocusIn>', self._on_focus_in)
        self.url_entry.bind('<FocusOut>', self._on_focus_out)
        self.url_var.trace('w', self._on_url_change_internal)
    
    def _set_initial_state(self) -> None:
        """Set initial placeholder state."""
        self.url_entry.insert(0, self.placeholder)
    
    def _on_focus_in(self, event) -> None:
        """Handle focus in event - clear placeholder if present."""
        if self.url_entry.get() == self.placeholder:
            self.url_entry.delete(0, tk.END)
    
    def _on_focus_out(self, event) -> None:
        """Handle focus out event - restore placeholder if empty."""
        if not self.url_entry.get().strip():
            self.url_entry.insert(0, self.placeholder)
    
    def _on_url_change_internal(self, *args) -> None:
        """Internal handler for URL changes."""
        if self.on_url_change:
            current_url = self.get_url()
            self.on_url_change(current_url)
    
    def get_url(self) -> str:
        """
        Get current URL, excluding placeholder text.
        
        Returns:
            Current URL string, empty if placeholder is shown
        """
        current_text = self.url_var.get().strip()
        return "" if current_text == self.placeholder else current_text
    
    def set_url(self, url: str) -> None:
        """
        Set URL value.
        
        Args:
            url: URL string to set
        """
        self.url_entry.delete(0, tk.END)
        if url:
            self.url_entry.insert(0, url)
        else:
            self.url_entry.insert(0, self.placeholder)
    
    def clear(self) -> None:
        """Clear URL input and restore placeholder."""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, self.placeholder)
    
    def set_validation_style(self, is_valid: Optional[bool]) -> None:
        """
        Set visual validation style.
        
        Args:
            is_valid: True for valid style, False for invalid, None for default
        """
        if is_valid is True:
            self.url_entry.configure(style="Valid.TEntry")
        elif is_valid is False:
            self.url_entry.configure(style="Invalid.TEntry")
        else:
            self.url_entry.configure(style="Modern.TEntry")
    
    def focus(self) -> None:
        """Set focus to the URL entry."""
        self.url_entry.focus_set()
    
    def set_change_callback(self, callback: Callable[[str], None]) -> None:
        """
        Set callback for URL changes.
        
        Args:
            callback: Function to call when URL changes
        """
        self.on_url_change = callback
