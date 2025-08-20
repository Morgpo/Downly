# =====
#
#   Downly Main Application
#
#   Main application window that orchestrates all components.
#
# =====

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from .config import AppConfig
from .core.dependency_manager import DependencyManager
from .core.url_validator import URLValidator
from .core.download_engine import DownloadEngine, DownloadSettings
from .core.preset_manager import PresetManager
from .ui.style_manager import StyleManager
from .ui.header_component import HeaderComponent
from .ui.url_input import URLInput
from .ui.settings_panel import SettingsPanel
from .ui.progress_panel import ProgressPanel


class DownlyApplication(tk.Tk):
    """
    Main application window for Downly YouTube downloader.
    Orchestrates all components and manages application state.
    """
    
    def __init__(self):
        """Initialize the main application."""
        super().__init__()
        
        # Initialize core managers
        self.dependency_manager = DependencyManager()
        self.url_validator = URLValidator()
        self.download_engine = DownloadEngine(self.dependency_manager)
        self.preset_manager = PresetManager()
        
        # Application state
        self.is_downloading = False
        
        self._setup_window()
        self._setup_style()
        self._create_components()
        self._setup_callbacks()
    
    def _setup_window(self) -> None:
        """Configure main window properties."""
        self.title(AppConfig.WINDOW_TITLE)
        self.resizable(False, False)
        self.geometry(AppConfig.WINDOW_GEOMETRY)
        self.minsize(*AppConfig.WINDOW_MIN_SIZE)
        self.configure(bg="#1e1e1e")
        
        # Set up window closing protocol
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Set window icon
        self._set_window_icon()
        
        # Main container
        self.main_frame = ttk.Frame(self, padding="20", style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def _setup_style(self) -> None:
        """Set up UI styling."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style_manager = StyleManager(self.style)
        self.style_manager.configure_all_styles()
        self.style_manager.configure_dropdown_listbox(self)
    
    def _set_window_icon(self) -> None:
        """Set window icon with error handling."""
        try:
            icon_path = self.dependency_manager.get_resource_path("assets/icon.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load window icon: {e}")
    
    def _create_components(self) -> None:
        """Create and initialize UI components."""
        # Header component
        self.header_component = HeaderComponent(self.main_frame, self.dependency_manager)
        
        # URL input component
        self.url_input = URLInput(self.main_frame)
        
        # Settings panel
        self.settings_panel = SettingsPanel(self.main_frame, self.preset_manager)
        
        # Progress panel
        self.progress_panel = ProgressPanel(self.main_frame)
    
    def _setup_callbacks(self) -> None:
        """Set up callbacks between components."""
        # URL input callbacks
        self.url_input.set_change_callback(self._on_url_change)
        
        # Progress panel callbacks
        self.progress_panel.set_callbacks(
            on_download=self._on_download_click,
            on_cancel=self._on_cancel_click
        )
        
        # Download engine callbacks
        self.download_engine.set_callbacks(
            on_progress=self._on_download_progress,
            on_success=self._on_download_success,
            on_error=self._on_download_error,
            on_status_update=self._on_status_update
        )
    
    def _on_url_change(self, url: str) -> None:
        """Handle URL input changes for validation feedback."""
        if not url:
            self.url_input.set_validation_style(None)
            return
        
        is_valid = self.url_validator.is_valid_youtube_url(url)
        self.url_input.set_validation_style(is_valid)
    
    def _on_download_click(self) -> None:
        """Handle download button click."""
        if self.is_downloading:
            return
        
        # Validate URL
        url = self.url_input.get_url()
        is_valid, error_message = self.url_validator.validate_url_input(url)
        
        if not is_valid:
            messagebox.showerror("Invalid URL", error_message)
            return
        
        # Get settings
        settings_dict = self.settings_panel.get_settings()
        
        # Create download settings object
        settings = DownloadSettings()
        settings.url = url
        settings.format = settings_dict["format"]
        settings.video_quality = settings_dict["video_quality"]
        settings.audio_quality = settings_dict["audio_quality"]
        settings.download_location = settings_dict["download_location"]
        settings.custom_filename = settings_dict["custom_filename"]
        settings.start_time = settings_dict["start_time"]
        settings.end_time = settings_dict["end_time"]
        settings.download_metadata = settings_dict["download_metadata"]
        settings.download_subtitles = settings_dict["download_subtitles"]
        
        # Start download
        if self.download_engine.start_download(settings):
            self.is_downloading = True
            self.progress_panel.start_download()
        else:
            messagebox.showerror("Download Error", "Failed to start download. Please try again.")
    
    def _on_cancel_click(self) -> None:
        """Handle cancel button click."""
        if not self.is_downloading:
            return
        
        self.download_engine.cancel_download()
        self.is_downloading = False
        self.progress_panel.set_status("Cancelling download...")
        
        # Update UI after a short delay
        self.after(100, lambda: self.progress_panel.set_status("Download cancelled"))
        self.after(200, self.progress_panel.finish_download)
    
    def _on_download_progress(self, percent: float, status_line: str, is_audio: bool) -> None:
        """Handle download progress updates."""
        self.progress_panel.set_progress(percent, status_line, is_audio)
    
    def _on_download_success(self) -> None:
        """Handle successful download completion."""
        if not self.is_downloading:  # Don't show success if cancelled
            return
        
        self.is_downloading = False
        self.progress_panel.set_success()
        messagebox.showinfo("Success", "Download completed successfully!")
    
    def _on_download_error(self, error_message: str) -> None:
        """Handle download errors."""
        if not self.is_downloading:  # Don't show error if cancelled
            return
        
        self.is_downloading = False
        self.progress_panel.set_error("Download failed")
        messagebox.showerror("Download Error", error_message)
    
    def _on_status_update(self, status: str) -> None:
        """Handle status updates from download engine."""
        self.progress_panel.set_status(status)
    
    def _on_closing(self) -> None:
        """Handle application shutdown."""
        if self.is_downloading:
            self.download_engine.cancel_download()
        self.destroy()


def main():
    """Main entry point for the application."""
    # Validate dependencies before starting
    dependency_manager = DependencyManager()
    deps_ok, error_msg = dependency_manager.validate_dependencies()
    
    if not deps_ok:
        # Show error message in a simple dialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "Dependency Error", 
            f"Required dependencies are not available:\n\n{error_msg}\n\n"
            "Please ensure the application is properly installed or contact support."
        )
        root.destroy()
        sys.exit(1)
    
    # Start the application
    app = DownlyApplication()
    app.mainloop()


if __name__ == "__main__":
    main()
