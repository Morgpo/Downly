# =====
#
#   Downly UI Progress Panel
#
#   Handles download progress display and controls.
#
# =====

import tkinter as tk
from tkinter import ttk
import re
from typing import Callable, Optional
from ..config import AppConfig


class ProgressPanel:
    """
    Progress panel for download status and controls.
    Manages progress bar, status text, and download/cancel buttons.
    """
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize progress panel.
        
        Args:
            parent: Parent widget to contain this panel
        """
        self.parent = parent
        
        # State variables
        self.is_downloading = False
        self.is_mp3_finishing = False
        self.animation_state = 0
        self.animation_timer: Optional[str] = None
        
        # Widget references
        self.button_frame: Optional[ttk.Frame] = None
        self.download_button: Optional[ttk.Button] = None
        self.cancel_button: Optional[ttk.Button] = None
        self.progress_frame: Optional[ttk.Frame] = None
        self.progress_label: Optional[ttk.Label] = None
        self.progress_bar: Optional[ttk.Progressbar] = None
        
        # Callbacks
        self.on_download: Optional[Callable[[], None]] = None
        self.on_cancel: Optional[Callable[[], None]] = None
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create progress panel widgets."""
        # Button frame
        self.button_frame = ttk.Frame(self.parent, style="Main.TFrame")
        self.button_frame.pack(pady=20)
        
        # Download button
        self.download_button = ttk.Button(
            self.button_frame, 
            text="Download", 
            command=self._on_download_click, 
            style="Download.TButton", 
            width=15
        )
        self.download_button.pack(side=tk.LEFT, padx=(0, 10), ipady=10)
        
        # Cancel button
        self.cancel_button = ttk.Button(
            self.button_frame, 
            text="Cancel", 
            command=self._on_cancel_click, 
            style="Cancel.TButton", 
            width=15
        )
        self.cancel_button.pack(side=tk.LEFT, ipady=10)
        self.cancel_button.config(state="disabled")
        
        # Progress frame
        self.progress_frame = ttk.Frame(self.parent, style="Main.TFrame")
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress label
        self.progress_label = ttk.Label(
            self.progress_frame, 
            text="Ready to download", 
            style="ProgressLabel.TLabel"
        )
        self.progress_label.pack()
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            mode='determinate', 
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        self.progress_bar['value'] = 0
    
    def _on_download_click(self) -> None:
        """Handle download button click."""
        if self.on_download:
            self.on_download()
    
    def _on_cancel_click(self) -> None:
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()
    
    def set_callbacks(self, on_download: Callable = None, on_cancel: Callable = None) -> None:
        """
        Set callback functions for button events.
        
        Args:
            on_download: Called when download button is clicked
            on_cancel: Called when cancel button is clicked
        """
        self.on_download = on_download
        self.on_cancel = on_cancel
    
    def start_download(self) -> None:
        """Start download state - show loading animation and enable cancel."""
        self.is_downloading = True
        self.download_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.progress_label.config(text="Preparing download...")
        self.progress_bar['value'] = 0
        self.animation_state = 0
        self._start_animation()
    
    def finish_download(self) -> None:
        """Finish download state - reset to ready state."""
        self._stop_animation()
        self.download_button.config(state="normal", text="Download")
        self.cancel_button.config(state="disabled")
        self.progress_label.config(text="Ready to download")
        self.progress_bar['value'] = 0
        self.is_downloading = False
        self.is_mp3_finishing = False
    
    def set_progress(self, percent: float, status_line: str = "", is_audio: bool = False) -> None:
        """
        Update progress bar and status.
        
        Args:
            percent: Progress percentage (0-100)
            status_line: Status line from yt-dlp output
            is_audio: Whether this is an audio download
        """
        percent = max(0, min(percent, 100))
        self.progress_bar['value'] = percent
        
        # Handle audio extraction finishing state
        if is_audio and percent >= 100.0 and not self.is_mp3_finishing:
            self.is_mp3_finishing = True
            self.progress_label.config(text="Extracting Audio...")
            return
        elif is_audio and self.is_mp3_finishing:
            return
        
        # Extract and display useful progress information
        if 'ETA' in status_line:
            eta_match = re.search(r'ETA (\d+:\d+)', status_line)
            speed_match = re.search(r'at\s+([^\s]+)', status_line)
            
            progress_text = f"Downloading... {percent:.1f}%"
            
            if eta_match:
                progress_text += f" - ETA {eta_match.group(1)}"
            
            if speed_match:
                progress_text += f" - {speed_match.group(1)}/s"
            
            self.progress_label.config(text=progress_text)
        else:
            self.progress_label.config(text=f"Downloading... {percent:.1f}%")
    
    def set_status(self, status: str) -> None:
        """
        Set status text.
        
        Args:
            status: Status text to display
        """
        self.progress_label.config(text=status)
    
    def set_success(self) -> None:
        """Set success state."""
        if not self.is_downloading:  # Don't show success if cancelled
            return
        self.progress_bar['value'] = 100
        self.progress_label.config(text="Download completed!")
        self.is_mp3_finishing = False
        self.finish_download()
    
    def set_error(self, error_message: str = "Download failed") -> None:
        """
        Set error state.
        
        Args:
            error_message: Error message to display
        """
        if not self.is_downloading:  # Don't show error if cancelled
            return
        self.progress_label.config(text=error_message)
        self.is_mp3_finishing = False
        self.finish_download()
    
    def set_cancelled(self) -> None:
        """Set cancelled state."""
        self.progress_label.config(text="Download cancelled")
        self.finish_download()
    
    def _start_animation(self) -> None:
        """Start download button animation."""
        self._animate_button_text()
    
    def _stop_animation(self) -> None:
        """Stop download button animation."""
        if self.animation_timer:
            self.parent.after_cancel(self.animation_timer)
            self.animation_timer = None
    
    def _animate_button_text(self) -> None:
        """Animate download button with cycling ellipsis pattern."""
        ellipsis_patterns = [".  ", ".. ", "...", ".. "]
        current_pattern = ellipsis_patterns[self.animation_state % len(ellipsis_patterns)]
        self.download_button.config(text=f"Downloading{current_pattern}")
        
        self.animation_state += 1
        self.animation_timer = self.parent.after(AppConfig.ANIMATION_INTERVAL, self._animate_button_text)
