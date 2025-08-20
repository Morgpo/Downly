# =====
#
#   Downly UI Settings Panel
#
#   Contains download settings and configuration widgets.
#
# =====

import tkinter as tk
from tkinter import ttk, filedialog
import os
from typing import Callable, Optional
from ..core.preset_manager import PresetManager


class SettingsPanel:
    """
    UI panel for download settings configuration.
    Handles presets, custom settings, and optional parameters.
    """
    
    def __init__(self, parent: tk.Widget, preset_manager: PresetManager):
        """
        Initialize settings panel.
        
        Args:
            parent: Parent widget to contain this panel
            preset_manager: Preset manager instance
        """
        self.parent = parent
        self.preset_manager = preset_manager
        
        # Variables for settings
        self.preset_format_var = tk.StringVar(value="Video")
        self.preset_quality_var = tk.StringVar(value="High")
        self.format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="Highest Video Quality")
        self.audio_quality_var = tk.StringVar(value="Highest Audio Quality")
        self.filename_var = tk.StringVar()
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        self.location_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.metadata_var = tk.BooleanVar(value=False)
        self.subtitles_var = tk.BooleanVar(value=False)
        
        # Widget references
        self.preset_format_dropdown: Optional[ttk.Combobox] = None
        self.preset_quality_dropdown: Optional[ttk.Combobox] = None
        self.format_dropdown: Optional[ttk.Combobox] = None
        self.quality_dropdown: Optional[ttk.Combobox] = None
        self.audio_quality_dropdown: Optional[ttk.Combobox] = None
        self.start_time_entry: Optional[ttk.Entry] = None
        self.end_time_entry: Optional[ttk.Entry] = None
        
        self._create_widgets()
        self._bind_events()
        self._setup_initial_state()
    
    def _create_widgets(self) -> None:
        """Create all widgets for the settings panel."""
        # Main settings frame
        self.required_frame = ttk.LabelFrame(
            self.parent, 
            text="Download Settings", 
            padding="15", 
            style="Modern.TLabelframe"
        )
        self.required_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create two-column layout
        self.settings_container = ttk.Frame(self.required_frame, style="Main.TFrame")
        self.settings_container.pack(fill=tk.X)
        self.settings_container.grid_columnconfigure(0, weight=1)
        self.settings_container.grid_columnconfigure(1, weight=1)
        
        self._create_preset_section()
        self._create_custom_section()
        self._create_optional_section()
    
    def _create_preset_section(self) -> None:
        """Create preset settings section."""
        # Preset frame (left side)
        self.preset_frame = ttk.Frame(self.settings_container, style="Main.TFrame")
        self.preset_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        ttk.Label(self.preset_frame, text="Presets", style="SubtitleLabel.TLabel").pack(anchor="w", pady=(0, 10))
        
        # Format dropdown
        ttk.Label(self.preset_frame, text="Format:", style="SmallLabel.TLabel").pack(anchor="w", pady=(0, 5))
        self.preset_format_dropdown = ttk.Combobox(
            self.preset_frame, 
            textvariable=self.preset_format_var, 
            style="Modern.TCombobox"
        )
        self.preset_format_dropdown["values"] = ("Video", "Audio", "Custom")
        self.preset_format_dropdown.pack(fill=tk.X, pady=(0, 15), ipady=3)
        
        # Quality dropdown
        ttk.Label(self.preset_frame, text="Quality:", style="SmallLabel.TLabel").pack(anchor="w", pady=(0, 5))
        self.preset_quality_dropdown = ttk.Combobox(
            self.preset_frame, 
            textvariable=self.preset_quality_var, 
            style="Modern.TCombobox"
        )
        self.preset_quality_dropdown["values"] = ("High", "Standard", "Low")
        self.preset_quality_dropdown.pack(fill=tk.X, pady=(0, 0), ipady=3)
    
    def _create_custom_section(self) -> None:
        """Create custom settings section."""
        # Custom frame (right side)
        self.custom_frame = ttk.Frame(self.settings_container, style="Main.TFrame")
        self.custom_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        ttk.Label(self.custom_frame, text="Custom Settings", style="SubtitleLabel.TLabel").pack(anchor="w", pady=(0, 10))
        
        # File type dropdown
        ttk.Label(self.custom_frame, text="File Type:", style="SmallLabel.TLabel").pack(anchor="w", pady=(0, 5))
        self.format_dropdown = ttk.Combobox(
            self.custom_frame, 
            textvariable=self.format_var, 
            style="Modern.TCombobox"
        )
        self.format_dropdown["values"] = ("mp4", "webm", "mp3", "m4a")
        self.format_dropdown.pack(fill=tk.X, pady=(0, 15), ipady=3)
        
        # Video quality dropdown
        ttk.Label(self.custom_frame, text="Video Quality:", style="SmallLabel.TLabel").pack(anchor="w", pady=(0, 5))
        self.quality_dropdown = ttk.Combobox(
            self.custom_frame, 
            textvariable=self.quality_var, 
            style="Modern.TCombobox"
        )
        self.quality_dropdown["values"] = ("Highest Video Quality", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p")
        self.quality_dropdown.pack(fill=tk.X, pady=(0, 15), ipady=3)
        
        # Audio quality dropdown
        ttk.Label(self.custom_frame, text="Audio Quality:", style="SmallLabel.TLabel").pack(anchor="w", pady=(0, 5))
        self.audio_quality_dropdown = ttk.Combobox(
            self.custom_frame, 
            textvariable=self.audio_quality_var, 
            style="Modern.TCombobox"
        )
        self.audio_quality_dropdown["values"] = ("Highest Audio Quality", "256kbps", "192kbps", "128kbps", "64kbps")
        self.audio_quality_dropdown.pack(fill=tk.X, pady=(0, 0), ipady=3)
    
    def _create_optional_section(self) -> None:
        """Create optional settings section."""
        # Optional settings frame
        self.optional_frame = ttk.LabelFrame(
            self.parent, 
            text="Optional Settings", 
            padding="15", 
            style="Modern.TLabelframe"
        )
        self.optional_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Optional container
        self.optional_container = ttk.Frame(self.optional_frame, style="Main.TFrame")
        self.optional_container.pack(fill=tk.X)
        self.optional_container.grid_columnconfigure(0, weight=1)
        self.optional_container.grid_columnconfigure(1, weight=1)
        
        self._create_filename_section()
        self._create_time_section()
        self._create_location_section()
        self._create_checkbox_section()
    
    def _create_filename_section(self) -> None:
        """Create custom filename section."""
        # Left side - Custom filename
        self.left_optional_frame = ttk.Frame(self.optional_container, style="Main.TFrame")
        self.left_optional_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ttk.Label(self.left_optional_frame, text="Custom Filename:", style="SectionLabel.TLabel").pack(anchor="w")
        self.filename_entry = ttk.Entry(
            self.left_optional_frame, 
            textvariable=self.filename_var, 
            style="Modern.TEntry"
        )
        self.filename_entry.pack(fill=tk.X, pady=(5, 15))
    
    def _create_time_section(self) -> None:
        """Create time interval section."""
        # Right side - Time interval
        self.right_optional_frame = ttk.Frame(self.optional_container, style="Main.TFrame")
        self.right_optional_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ttk.Label(self.right_optional_frame, text="Time Interval:", style="SectionLabel.TLabel").pack(anchor="w")
        
        self.time_frame = ttk.Frame(self.right_optional_frame, style="Main.TFrame")
        self.time_frame.pack(fill=tk.X, pady=(5, 15))
        
        # Start time
        ttk.Label(self.time_frame, text="From:", style="SmallLabel.TLabel").pack(side=tk.LEFT)
        self.start_time_entry = ttk.Entry(
            self.time_frame, 
            textvariable=self.start_time_var, 
            style="Small.TEntry", 
            width=15
        )
        self.start_time_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.start_time_entry.insert(0, "HH:MM:SS")
        
        # End time
        ttk.Label(self.time_frame, text="To:", style="SmallLabel.TLabel").pack(side=tk.LEFT)
        self.end_time_entry = ttk.Entry(
            self.time_frame, 
            textvariable=self.end_time_var, 
            style="Small.TEntry", 
            width=15
        )
        self.end_time_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.end_time_entry.insert(0, "HH:MM:SS")
    
    def _create_location_section(self) -> None:
        """Create download location section."""
        # Download location (full width)
        self.location_full_frame = ttk.Frame(self.optional_container, style="Main.TFrame")
        self.location_full_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(15, 0))
        
        ttk.Label(self.location_full_frame, text="Download Location:", style="SectionLabel.TLabel").pack(anchor="w")
        
        self.location_frame = ttk.Frame(self.location_full_frame, style="Main.TFrame")
        self.location_frame.pack(fill=tk.X, pady=(5, 15))
        
        self.location_entry = ttk.Entry(
            self.location_frame, 
            textvariable=self.location_var, 
            style="Modern.TEntry"
        )
        self.location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.browse_button = ttk.Button(
            self.location_frame, 
            text="Browse...", 
            command=self._browse_download_location, 
            style="Browse.TButton", 
            width=10
        )
        self.browse_button.pack(side=tk.RIGHT)
    
    def _create_checkbox_section(self) -> None:
        """Create checkbox section for metadata and subtitles."""
        # Checkboxes (side by side)
        self.checkboxes_frame = ttk.Frame(self.location_full_frame, style="Main.TFrame")
        self.checkboxes_frame.pack(fill=tk.X)
        
        self.metadata_checkbox = ttk.Checkbutton(
            self.checkboxes_frame, 
            text="Download metadata", 
            variable=self.metadata_var, 
            style="Modern.TCheckbutton"
        )
        self.metadata_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        
        self.subtitles_checkbox = ttk.Checkbutton(
            self.checkboxes_frame, 
            text="Download subtitles", 
            variable=self.subtitles_var, 
            style="Modern.TCheckbutton"
        )
        self.subtitles_checkbox.pack(side=tk.LEFT)
    
    def _bind_events(self) -> None:
        """Bind events for interactive behavior."""
        # Preset change handlers
        self.preset_format_dropdown.bind("<<ComboboxSelected>>", self._on_preset_format_change)
        self.preset_quality_dropdown.bind("<<ComboboxSelected>>", self._on_preset_quality_change)
        
        # Custom change handlers
        self.format_dropdown.bind("<<ComboboxSelected>>", self._on_format_change)
        self.quality_dropdown.bind("<<ComboboxSelected>>", self._on_custom_change)
        self.audio_quality_dropdown.bind("<<ComboboxSelected>>", self._on_custom_change)
        
        # Time entry placeholder handling
        self.start_time_entry.bind('<FocusIn>', self._on_time_focus_in)
        self.start_time_entry.bind('<FocusOut>', self._on_time_focus_out)
        self.end_time_entry.bind('<FocusIn>', self._on_time_focus_in)
        self.end_time_entry.bind('<FocusOut>', self._on_time_focus_out)
        
        # Configure dropdown selection behavior
        self._configure_dropdown_behavior()
    
    def _configure_dropdown_behavior(self) -> None:
        """Configure dropdown properties and fix selection highlighting."""
        dropdowns = [
            self.preset_format_dropdown,
            self.preset_quality_dropdown,
            self.format_dropdown,
            self.quality_dropdown,
            self.audio_quality_dropdown
        ]
        
        for dropdown in dropdowns:
            dropdown.state(["readonly"])
            dropdown.bind('<FocusOut>', self._on_focus_out)
            dropdown.bind('<Button-1>', self._on_button_release)
            dropdown.bind('<ButtonRelease-1>', self._on_button_release)
    
    def _setup_initial_state(self) -> None:
        """Set up initial widget states."""
        # Apply initial preset
        self._apply_preset()
        
        # Set initial state: preset mode with custom controls disabled
        self.format_dropdown.state(["disabled"])
        self.quality_dropdown.state(["disabled"])
        self.audio_quality_dropdown.state(["disabled"])
    
    def _on_preset_format_change(self, event) -> None:
        """Handle preset format change."""
        preset_format = self.preset_format_var.get()
        if preset_format == "Custom":
            # Custom mode: disable presets, enable custom controls
            self.preset_quality_var.set("---")
            self.preset_quality_dropdown.state(["disabled"])
            
            # Enable all custom controls
            self.format_dropdown.state(["!disabled"])
            self.quality_dropdown.state(["!disabled"])
            self.audio_quality_dropdown.state(["!disabled"])
            
            # Reset custom controls to default values
            self.format_var.set("mp4")
            self.quality_var.set("Highest Video Quality")
            self.audio_quality_var.set("Highest Audio Quality")
        else:
            # Preset mode: enable quality selector, disable custom controls
            self.preset_quality_dropdown.state(["!disabled"])
            if self.preset_quality_var.get() == "---":
                self.preset_quality_var.set("High")
            
            # Disable custom controls
            self.format_dropdown.state(["disabled"])
            self.quality_dropdown.state(["disabled"])
            self.audio_quality_dropdown.state(["disabled"])
            
            # Apply preset settings
            self._apply_preset()
    
    def _on_preset_quality_change(self, event) -> None:
        """Handle preset quality change."""
        if self.preset_format_var.get() != "Custom":
            self._apply_preset()
    
    def _on_format_change(self, event) -> None:
        """Handle format change for video quality adjustment."""
        if self.format_var.get() in ["mp3", "m4a"]:
            self.quality_dropdown.set("---")
            self.quality_dropdown.state(["disabled"])
        else:
            if self.quality_dropdown.get() == "---":
                self.quality_dropdown.set("Highest Video Quality")
            # Only enable if in custom mode
            if self.preset_format_var.get() == "Custom":
                self.quality_dropdown.state(["!disabled"])
        self._on_custom_change(event)
    
    def _on_custom_change(self, event) -> None:
        """Handle custom setting changes."""
        # Prevent custom changes when in preset mode
        if self.preset_format_var.get() != "Custom":
            # Revert the change and reapply preset
            self._apply_preset()
    
    def _on_time_focus_in(self, event) -> None:
        """Handle time entry focus in."""
        widget = event.widget
        if widget.get() == "HH:MM:SS":
            widget.delete(0, tk.END)
    
    def _on_time_focus_out(self, event) -> None:
        """Handle time entry focus out."""
        widget = event.widget
        if not widget.get().strip():
            widget.insert(0, "HH:MM:SS")
    
    def _on_focus_out(self, event) -> None:
        """Handle dropdown focus out."""
        widget = event.widget
        widget.selection_clear()
    
    def _on_button_release(self, event) -> None:
        """Handle dropdown button release."""
        widget = event.widget
        widget.after(1, lambda: widget.selection_clear())
    
    def _apply_preset(self) -> None:
        """Apply preset configuration to custom controls."""
        preset_format = self.preset_format_var.get()
        preset_quality = self.preset_quality_var.get()
        
        if preset_format == "Custom":
            return
        
        preset_config = self.preset_manager.get_preset(preset_format, preset_quality)
        
        if preset_config:
            # Update custom controls to show what the preset will use
            self.format_var.set(preset_config["format"])
            self.quality_var.set(preset_config["video_quality"])
            self.audio_quality_var.set(preset_config["audio_quality"])
            
            # Update dropdown states based on format
            if preset_config["format"] in ["mp3", "m4a"]:
                self.quality_var.set("---")
    
    def _browse_download_location(self) -> None:
        """Open file dialog to browse for download location."""
        initial_dir = self.location_var.get()
        if not os.path.exists(initial_dir):
            initial_dir = os.path.expanduser("~")
        
        folder_selected = filedialog.askdirectory(
            title="Select Download Location",
            initialdir=initial_dir
        )
        
        if folder_selected:
            self.location_var.set(folder_selected)
    
    def get_settings(self) -> dict:
        """
        Get current settings as a dictionary.
        
        Returns:
            Dictionary containing all current settings
        """
        return {
            "preset_format": self.preset_format_var.get(),
            "preset_quality": self.preset_quality_var.get(),
            "format": self.format_var.get(),
            "video_quality": self.quality_var.get(),
            "audio_quality": self.audio_quality_var.get(),
            "custom_filename": self.filename_var.get(),
            "start_time": self.start_time_var.get(),
            "end_time": self.end_time_var.get(),
            "download_location": self.location_var.get(),
            "download_metadata": self.metadata_var.get(),
            "download_subtitles": self.subtitles_var.get()
        }
