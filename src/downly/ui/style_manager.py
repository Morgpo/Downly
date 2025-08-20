# =====
#
#   Downly UI Style Manager
#
#   Handles UI styling and theme configuration.
#
# =====

from tkinter import ttk
from ..config import ThemeConfig


class StyleManager:
    """
    Manages UI styling and theme configuration.
    Provides centralized styling for consistent UI appearance.
    """
    
    def __init__(self, style: ttk.Style):
        """
        Initialize style manager.
        
        Args:
            style: ttk.Style instance to configure
        """
        self.style = style
        self.config = ThemeConfig()
    
    def configure_all_styles(self) -> None:
        """Configure all UI styles with the current theme."""
        self._configure_frames()
        self._configure_labels()
        self._configure_entries()
        self._configure_comboboxes()
        self._configure_buttons()
        self._configure_progressbar()
        self._configure_checkbuttons()
        self._configure_labelframes()
    
    def _configure_frames(self) -> None:
        """Configure frame styles."""
        self.style.configure("Main.TFrame", background=self.config.PRIMARY_BG)
    
    def _configure_labels(self) -> None:
        """Configure label styles."""
        self.style.configure(
            "Title.TLabel", 
            foreground=self.config.TEXT_TITLE, 
            background=self.config.PRIMARY_BG, 
            font=self.config.TITLE_FONT
        )
        self.style.configure(
            "SubtitleLabel.TLabel", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            font=self.config.HEADING_FONT
        )
        self.style.configure(
            "SectionLabel.TLabel", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            font=self.config.NORMAL_FONT
        )
        self.style.configure(
            "SmallLabel.TLabel", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.TEXT_SECONDARY, 
            font=self.config.SMALL_FONT
        )
        self.style.configure(
            "HintLabel.TLabel", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.TEXT_HINT, 
            font=self.config.TINY_FONT
        )
        self.style.configure(
            "ProgressLabel.TLabel", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.TEXT_SECONDARY, 
            font=self.config.SMALL_FONT
        )
    
    def _configure_entries(self) -> None:
        """Configure entry widget styles."""
        # Modern entry style
        self.style.configure(
            "Modern.TEntry", 
            fieldbackground=self.config.SURFACE_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            borderwidth=1, 
            bordercolor=self.config.BORDER_COLOR, 
            focuscolor=self.config.BORDER_ACCENT, 
            insertcolor=self.config.TEXT_PRIMARY, 
            font=self.config.NORMAL_FONT
        )
        
        # Small entry style
        self.style.configure(
            "Small.TEntry", 
            fieldbackground=self.config.SURFACE_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            borderwidth=1, 
            bordercolor=self.config.BORDER_COLOR, 
            focuscolor=self.config.BORDER_ACCENT, 
            insertcolor=self.config.TEXT_PRIMARY, 
            font=self.config.SMALL_FONT
        )
        
        # Validation styles
        self.style.configure(
            "Valid.TEntry", 
            fieldbackground=self.config.SURFACE_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            borderwidth=1, 
            bordercolor=self.config.ACCENT_GREEN, 
            focuscolor=self.config.ACCENT_GREEN, 
            insertcolor=self.config.TEXT_PRIMARY, 
            font=self.config.NORMAL_FONT
        )
        self.style.configure(
            "Invalid.TEntry", 
            fieldbackground=self.config.SURFACE_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            borderwidth=1, 
            bordercolor=self.config.ACCENT_RED, 
            focuscolor=self.config.ACCENT_RED, 
            insertcolor=self.config.TEXT_PRIMARY, 
            font=self.config.NORMAL_FONT
        )
    
    def _configure_comboboxes(self) -> None:
        """Configure combobox styles."""
        self.style.configure(
            "Modern.TCombobox", 
            fieldbackground=self.config.SURFACE_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            borderwidth=1, 
            bordercolor=self.config.BORDER_COLOR, 
            focuscolor=self.config.BORDER_ACCENT, 
            arrowcolor=self.config.TEXT_SECONDARY, 
            background=self.config.PRIMARY_BG, 
            selectbackground=self.config.SURFACE_BG, 
            selectforeground=self.config.TEXT_PRIMARY, 
            font=self.config.NORMAL_FONT
        )
        
        # Combobox state mappings
        self.style.map(
            "Modern.TCombobox", 
            selectbackground=[("focus", self.config.SURFACE_BG), ("!focus", self.config.SURFACE_BG)], 
            selectforeground=[("focus", self.config.TEXT_PRIMARY), ("!focus", self.config.TEXT_PRIMARY)], 
            fieldbackground=[("readonly", self.config.SURFACE_BG), ("focus", self.config.SURFACE_BG), ("disabled", "#3a3a3a")], 
            bordercolor=[("focus", self.config.BORDER_ACCENT), ("!focus", self.config.BORDER_COLOR), ("disabled", "#555555")], 
            focuscolor=[("focus", "none"), ("!focus", "none")], 
            foreground=[("disabled", self.config.TEXT_HINT)], 
            arrowcolor=[("disabled", "#666666")]
        )
    
    def _configure_buttons(self) -> None:
        """Configure button styles."""
        # Download button
        self.style.configure(
            "Download.TButton", 
            font=self.config.BUTTON_FONT, 
            foreground=self.config.TEXT_PRIMARY, 
            background=self.config.ACCENT_GREEN, 
            borderwidth=0, 
            focuscolor="none"
        )
        self.style.map(
            "Download.TButton", 
            background=[("active", self.config.ACCENT_GREEN_HOVER), ("pressed", self.config.ACCENT_GREEN_PRESSED)], 
            foreground=[("active", self.config.TEXT_PRIMARY), ("pressed", self.config.TEXT_PRIMARY)]
        )
        
        # Cancel button
        self.style.configure(
            "Cancel.TButton", 
            font=self.config.BUTTON_FONT, 
            foreground=self.config.TEXT_PRIMARY, 
            background=self.config.ACCENT_RED, 
            borderwidth=0, 
            focuscolor="none"
        )
        self.style.map(
            "Cancel.TButton", 
            background=[("active", self.config.ACCENT_RED_HOVER), ("pressed", self.config.ACCENT_RED_PRESSED), ("disabled", "#666666")], 
            foreground=[("active", self.config.TEXT_PRIMARY), ("pressed", self.config.TEXT_PRIMARY), ("disabled", "#999999")]
        )
        
        # Browse button
        self.style.configure(
            "Browse.TButton", 
            font=("Arial", 10), 
            foreground=self.config.TEXT_PRIMARY, 
            background=self.config.ACCENT_BLUE, 
            borderwidth=0, 
            focuscolor="none"
        )
        self.style.map(
            "Browse.TButton", 
            background=[("active", "#e73c7e"), ("pressed", "#d63384")], 
            foreground=[("active", self.config.TEXT_PRIMARY), ("pressed", self.config.TEXT_PRIMARY)]
        )
    
    def _configure_progressbar(self) -> None:
        """Configure progress bar style."""
        self.style.configure(
            "Modern.Horizontal.TProgressbar", 
            background=self.config.ACCENT_BLUE, 
            troughcolor=self.config.SURFACE_BG, 
            borderwidth=1, 
            lightcolor=self.config.ACCENT_BLUE, 
            darkcolor=self.config.ACCENT_BLUE
        )
    
    def _configure_checkbuttons(self) -> None:
        """Configure checkbutton styles."""
        self.style.configure(
            "Modern.TCheckbutton", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.TEXT_PRIMARY, 
            focuscolor="none", 
            font=self.config.NORMAL_FONT
        )
        self.style.map(
            "Modern.TCheckbutton", 
            background=[("active", self.config.PRIMARY_BG), ("pressed", self.config.PRIMARY_BG)], 
            foreground=[("active", self.config.TEXT_PRIMARY), ("pressed", self.config.TEXT_PRIMARY)], 
            indicatorcolor=[("selected", self.config.ACCENT_BLUE), ("!selected", self.config.SURFACE_BG)], 
            focuscolor=[("focus", "none"), ("!focus", "none")]
        )
    
    def _configure_labelframes(self) -> None:
        """Configure labelframe styles."""
        self.style.configure(
            "Modern.TLabelframe", 
            background=self.config.PRIMARY_BG, 
            borderwidth=1, 
            relief="solid", 
            bordercolor=self.config.BORDER_COLOR
        )
        self.style.configure(
            "Modern.TLabelframe.Label", 
            background=self.config.PRIMARY_BG, 
            foreground=self.config.ACCENT_BLUE, 
            font=self.config.HEADING_FONT
        )
    
    def configure_dropdown_listbox(self, root) -> None:
        """Configure dropdown listbox styling using option_add."""
        root.option_add('*TCombobox*Listbox.selectBackground', self.config.SURFACE_BG)
        root.option_add('*TCombobox*Listbox.selectForeground', self.config.TEXT_PRIMARY)
        root.option_add('*TCombobox*Listbox.background', self.config.SURFACE_BG)
        root.option_add('*TCombobox*Listbox.foreground', self.config.TEXT_PRIMARY)
