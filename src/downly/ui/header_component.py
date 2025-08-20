# =====
#
#   Downly UI Header Component
#
#   Handles application header with logo and title.
#
# =====

import tkinter as tk
from tkinter import ttk
import os
from ..core.dependency_manager import DependencyManager


class HeaderComponent:
    """
    Header component with logo and title.
    Handles logo loading with graceful fallback.
    """
    
    def __init__(self, parent: tk.Widget, dependency_manager: DependencyManager):
        """
        Initialize header component.
        
        Args:
            parent: Parent widget to contain this component
            dependency_manager: Dependency manager for resource paths
        """
        self.parent = parent
        self.dependency_manager = dependency_manager
        
        # Widget references
        self.header_frame: tk.Frame = None
        self.title_label: ttk.Label = None
        self.logo_left: tk.Label = None
        self.logo_right: tk.Label = None
        self.logo_image: tk.PhotoImage = None
        
        self._create_widgets()
        self._load_logo()
    
    def _create_widgets(self) -> None:
        """Create header widgets."""
        # Header frame
        self.header_frame = tk.Frame(self.parent, bg="#1e1e1e")
        self.header_frame.pack(pady=(0, 20), fill=tk.X)
        
        # Configure grid for centered title with side logos
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Title label
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Downly", 
            style="Title.TLabel"
        )
        self.title_label.grid(row=0, column=1, sticky="")
    
    def _load_logo(self) -> None:
        """Load and display logo images with error handling."""
        try:
            logo_path = self.dependency_manager.get_resource_path("assets/logo.png")
            if os.path.exists(logo_path):
                self.logo_image = tk.PhotoImage(file=logo_path)
                
                # Left logo
                self.logo_left = tk.Label(
                    self.header_frame, 
                    image=self.logo_image, 
                    bg="#1e1e1e"
                )
                self.logo_left.grid(row=0, column=0, padx=(0, 20), sticky="w")
                
                # Right logo
                self.logo_right = tk.Label(
                    self.header_frame, 
                    image=self.logo_image, 
                    bg="#1e1e1e"
                )
                self.logo_right.grid(row=0, column=2, padx=(20, 0), sticky="e")
            else:
                print(f"Logo file not found at path: {logo_path}")
        except Exception as e:
            print(f"Could not load logo: {e}")
    
    def set_title(self, title: str) -> None:
        """
        Set header title text.
        
        Args:
            title: Title text to display
        """
        self.title_label.config(text=title)
