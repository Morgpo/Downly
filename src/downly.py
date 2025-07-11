import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import threading

import os
import sys
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller) """
    try:
        base_path = sys._MEIPASS  # when running from .exe
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    """Get the path to the bundled ffmpeg executable"""
    # Try to find ffmpeg in the PyInstaller bundle first
    ffmpeg_name = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
    bundled_ffmpeg = resource_path(ffmpeg_name)
    
    if os.path.exists(bundled_ffmpeg):
        return bundled_ffmpeg
        
    # If not found in root bundle, try the common locations
    # For development environment
    dev_ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".venv", "Scripts", ffmpeg_name)
    if os.path.exists(dev_ffmpeg):
        return dev_ffmpeg
        
    # For PyInstaller bundle in possible subdirectories
    for subdir in [".", "bin", "tools", "ffmpeg"]:
        possible_path = resource_path(os.path.join(subdir, ffmpeg_name))
        if os.path.exists(possible_path):
            return possible_path
            
    # Return None if not found, which will let yt-dlp try to use system ffmpeg
    return None



class CustomWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Downly - YouTube Downloader")
        icon_path = resource_path("assets/icon.ico")
        self.iconbitmap(icon_path)
        self.wm_iconbitmap(icon_path)
        self.resizable(False, False)
        self.geometry("900x900")
        self.configure(bg="#1e1e1e")

        # Configure modern styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        # Create main container with scrollable content
        self.main_frame = ttk.Frame(self, padding="20", style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Downly", style="Title.TLabel")
        self.title_label.pack(pady=(0, 20))

        # URL Entry Section
        self.url_frame = ttk.LabelFrame(self.main_frame, text="YouTube URL", padding="15", style="Modern.TLabelframe")
        self.url_frame.pack(fill=tk.X, pady=(0, 15))

        self.url_entry = ttk.Entry(self.url_frame, font=("Segoe UI", 11), style="Modern.TEntry")
        self.url_entry.insert(0, "Paste YouTube link here...")
        self.url_entry.pack(fill=tk.X)

        # Required Settings Section
        self.required_frame = ttk.LabelFrame(self.main_frame, text="Required Settings", 
                                           padding="15", style="Modern.TLabelframe")
        self.required_frame.pack(fill=tk.X, pady=(0, 15))

        # Format selection
        ttk.Label(self.required_frame, text="Format:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.format_var = tk.StringVar(value="mp4")
        self.format_dropdown = ttk.Combobox(self.required_frame, textvariable=self.format_var, 
                                          font=("Segoe UI", 10), style="Modern.TCombobox")
        self.format_dropdown["values"] = ("mp4", "webm", "mp3", "m4a")
        self.format_dropdown.pack(fill=tk.X, pady=(5, 15))

        # Video quality selection
        ttk.Label(self.required_frame, text="Video Quality:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.quality_var = tk.StringVar(value="Highest Video Quality")
        self.quality_dropdown = ttk.Combobox(self.required_frame, textvariable=self.quality_var, 
                                           font=("Segoe UI", 10), style="Modern.TCombobox")
        self.quality_dropdown["values"] = ("Highest Video Quality", "2160p","1440p", "1080p", "720p", "480p", "360p", "240p", "144p")
        self.quality_dropdown.pack(fill=tk.X, pady=(5, 15))

        # Audio quality selection
        ttk.Label(self.required_frame, text="Audio Quality:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.audio_quality_var = tk.StringVar(value="Highest Audio Quality")
        self.audio_quality_dropdown = ttk.Combobox(self.required_frame, textvariable=self.audio_quality_var, 
                                                 font=("Segoe UI", 10), style="Modern.TCombobox")
        self.audio_quality_dropdown["values"] = ("Highest Audio Quality", "256kbps", "192kbps", "128kbps", "64kbps")
        self.audio_quality_dropdown.pack(fill=tk.X, pady=(5, 0))

        # Optional Settings Section
        self.optional_frame = ttk.LabelFrame(self.main_frame, text="Optional Settings", 
                                           padding="15", style="Modern.TLabelframe")
        self.optional_frame.pack(fill=tk.X, pady=(0, 15))

        # Custom filename
        ttk.Label(self.optional_frame, text="Custom Filename:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.filename_var = tk.StringVar()
        self.filename_entry = ttk.Entry(self.optional_frame, textvariable=self.filename_var, 
                                      font=("Segoe UI", 10), style="Modern.TEntry")
        self.filename_entry.pack(fill=tk.X, pady=(5, 15))

        # Time interval section
        ttk.Label(self.optional_frame, text="Time Interval:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Time inputs frame
        self.time_frame = ttk.Frame(self.optional_frame, style="Main.TFrame")
        self.time_frame.pack(fill=tk.X, pady=(5, 15))
        
        # Start time
        ttk.Label(self.time_frame, text="From:", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.start_time_var = tk.StringVar()
        self.start_time_entry = ttk.Entry(self.time_frame, textvariable=self.start_time_var, 
                                        font=("Segoe UI", 10), style="Modern.TEntry", width=12)
        self.start_time_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.start_time_entry.insert(0, "00:00:00")
        
        # End time
        ttk.Label(self.time_frame, text="To:", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.end_time_var = tk.StringVar()
        self.end_time_entry = ttk.Entry(self.time_frame, textvariable=self.end_time_var, 
                                      font=("Segoe UI", 10), style="Modern.TEntry", width=12)
        self.end_time_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.end_time_entry.insert(0, "")
        
        # Time format hint
        ttk.Label(self.optional_frame, text="Format: HH:MM:SS; MM:SS; SS (leave 'To' empty for full video)", 
                 font=("Segoe UI", 8), foreground="#888888").pack(anchor="w", pady=(0, 15))

        # Download location
        ttk.Label(self.optional_frame, text="Download Location:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.location_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.location_entry = ttk.Entry(self.optional_frame, textvariable=self.location_var, 
                                      font=("Segoe UI", 10), style="Modern.TEntry")
        self.location_entry.pack(fill=tk.X, pady=(5, 0))

        # Update video quality dropdown based on format selection
        def on_format_change(event):
            if self.format_var.get() in ["mp3", "m4a"]:
                self.quality_dropdown.set("---")
                self.quality_dropdown.state(["disabled"])
            else:
                self.quality_dropdown["values"] = ("Highest Video Quality", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p")
                self.quality_dropdown.set("Highest Video Quality")
                self.quality_dropdown.state(["!disabled"])

        self.format_dropdown.bind("<<ComboboxSelected>>", on_format_change)

        # Make the dropdowns read only
        self.format_dropdown.state(["readonly"])
        self.quality_dropdown.state(["readonly"])
        self.audio_quality_dropdown.state(["readonly"])

        # Fix selection highlighting issues for read-only comboboxes
        def clear_selection(event):
            """Clear text selection when combobox loses focus"""
            widget = event.widget
            widget.selection_clear()
        
        def on_focus_out(event):
            """Handle focus out events to clear selection"""
            widget = event.widget
            widget.selection_clear()
            
        def on_button_release(event):
            """Clear selection after mouse click"""
            widget = event.widget
            self.after(1, lambda: widget.selection_clear())
        
        # Bind events to all comboboxes to fix selection issues
        for combo in [self.format_dropdown, self.quality_dropdown, self.audio_quality_dropdown]:
            combo.bind('<FocusOut>', on_focus_out)
            combo.bind('<Button-1>', on_button_release)
            combo.bind('<ButtonRelease-1>', on_button_release)

        # Download button
        self.button = ttk.Button(self.main_frame, text="Start Download", 
                               command=self.ytdlp_download, style="Download.TButton", width=15)
        self.button.pack(pady=20, ipady=10)

        # Progress bar (always visible)
        self.progress_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = ttk.Label(self.progress_frame, text="Ready to download", 
                                       font=("Segoe UI", 9), style="TLabel")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate', 
                                          style="Modern.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        self.progress_bar['value'] = 0

        # Animation state for loading text
        self.animation_state = 0
        self.animation_timer = None
        self.is_mp3_finishing = False  # Track MP3 finishing state
        self.progress_increment_timer = None  # Add timer for incremental progress

    def configure_styles(self):
        """Configure modern styling for the application"""
        # Modern color palette with uniform backgrounds
        primary_bg = "#1e1e1e"      # Main background (used everywhere)
        surface_bg = "#2a2a2a"      # Entry/combobox backgrounds
        text_title = "#ff0050"      # Title text
        text_primary = "#ffffff"    # Primary text
        text_secondary = "#cccccc"  # Secondary text
        accent_blue = "#ff0050"     # Primary accent
        accent_green = "#16a085"    # Success/download button
        border_color = "#404040"    # Subtle borders
        border_accent = "#ff0050"   # Accent borders
        
        # Main frame styling
        self.style.configure("Main.TFrame",
                           background=primary_bg)
        
        # Title styling
        self.style.configure("Title.TLabel", 
                           foreground=text_title, 
                           background=primary_bg,
                           font=("Segoe UI", 24, "bold"))
        
        # LabelFrame styling - uniform background with subtle border
        self.style.configure("Modern.TLabelframe", 
                           background=primary_bg, 
                           borderwidth=1,
                           relief="solid",
                           bordercolor=border_color)
        self.style.configure("Modern.TLabelframe.Label", 
                           background=primary_bg, 
                           foreground=accent_blue, 
                           font=("Segoe UI", 11, "bold"))
        
        # Labels inside sections
        self.style.configure("TLabel",
                           background=primary_bg,
                           foreground=text_secondary)
        
        # Entry styling
        self.style.configure("Modern.TEntry", 
                           fieldbackground=surface_bg, 
                           foreground=text_primary, 
                           borderwidth=1,
                           bordercolor=border_color,
                           focuscolor=border_accent,
                           insertcolor=text_primary)
        
        # Combobox styling
        self.style.configure("Modern.TCombobox", 
                           fieldbackground=surface_bg, 
                           foreground=text_primary, 
                           borderwidth=1,
                           bordercolor=border_color,
                           focuscolor=border_accent,
                           arrowcolor=text_secondary,
                           background=primary_bg,
                           selectbackground=surface_bg,
                           selectforeground=text_primary)
        self.style.map("Modern.TCombobox",
                      selectbackground=[("focus", surface_bg), ("!focus", surface_bg)],
                      selectforeground=[("focus", text_primary), ("!focus", text_primary)],
                      fieldbackground=[("readonly", surface_bg), ("focus", surface_bg)],
                      bordercolor=[("focus", border_accent), ("!focus", border_color)],
                      focuscolor=[("focus", "none"), ("!focus", "none")])
        
        # Configure the dropdown listbox styling
        self.option_add('*TCombobox*Listbox.selectBackground', surface_bg)
        self.option_add('*TCombobox*Listbox.selectForeground', text_primary)
        self.option_add('*TCombobox*Listbox.background', surface_bg)
        self.option_add('*TCombobox*Listbox.foreground', text_primary)
        
        # Checkbutton styling
        self.style.configure("Modern.TCheckbutton", 
                           background=primary_bg, 
                           foreground=text_primary, 
                           focuscolor="none",
                           indicatorcolor=surface_bg,
                           indicatorbackground=surface_bg,
                           bordercolor=border_color)
        self.style.map("Modern.TCheckbutton",
                      indicatorcolor=[("selected", accent_blue)],
                      background=[("active", primary_bg)])
        
        # Download button styling
        self.style.configure("Download.TButton", 
                           font=("Segoe UI", 12, "bold"),
                           foreground=text_primary,
                           background=accent_green,
                           borderwidth=0,
                           focuscolor="none")
        self.style.map("Download.TButton",
                      background=[("active", "#138d75"), ("pressed", "#117a65")],
                      foreground=[("active", text_primary), ("pressed", text_primary)])

        # Progress bar styling
        self.style.configure("Modern.Horizontal.TProgressbar",
                           background=accent_blue,
                           troughcolor=surface_bg,
                           borderwidth=1,
                           lightcolor=accent_blue,
                           darkcolor=accent_blue)

    # === Function to handle the download process === #
    def ytdlp_download(self):
        # Get and validate URL
        url = self.url_entry.get().strip()
        
        # Check if URL is empty or still contains placeholder text
        if not url or url == "Paste YouTube link here...":
            messagebox.showerror("Invalid URL", "Please enter a YouTube URL.")
            return
            
        # Check if URL matches YouTube patterns
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
            r'(?:https?://)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/live/[\w-]+',
            r'(?:https?://)?(?:m\.)?youtube\.com/watch\?v=[\w-]+'
        ]
        
        is_valid_youtube = any(re.match(pattern, url, re.IGNORECASE) for pattern in youtube_patterns)
        
        if not is_valid_youtube:
            messagebox.showerror("Invalid URL", "Please enter a valid YouTube URL.\n\nSupported formats:\n• youtube.com/watch?v=...\n• youtu.be/...\n• youtube.com/shorts/...\n• youtube.com/playlist?list=...")
            return
        
        # Start download in separate thread
        self.start_download_thread(url)

    def start_download_thread(self, url):
        """Start the download process in a separate thread"""
        # Show loading animation
        self.show_loading()
        
        # Start download thread
        download_thread = threading.Thread(target=self.download_worker, args=(url,))
        download_thread.daemon = True
        download_thread.start()

    def show_loading(self):
        """Show loading animation and disable download button"""
        self.button.config(state="disabled")
        self.progress_label.config(text="Preparing download...")
        self.progress_bar['value'] = 0
        self.animation_state = 0
        self.animate_button_text()

    def animate_button_text(self):
        """Animate the button text with cycling ellipsis"""
        ellipsis_patterns = [".  ", ".. ", "...", ".. "]
        current_pattern = ellipsis_patterns[self.animation_state % len(ellipsis_patterns)]
        self.button.config(text=f"Downloading{current_pattern}")
        
        self.animation_state += 1
        # Schedule next animation frame
        self.animation_timer = self.after(1000, self.animate_button_text)

    def hide_loading(self):
        """Hide loading animation and re-enable download button"""
        if self.animation_timer:
            self.after_cancel(self.animation_timer)
            self.animation_timer = None
        self.button.config(state="normal", text="Start Download")
        self.progress_label.config(text="Ready to download")
        self.progress_bar['value'] = 0

    def download_worker(self, url):
        """Worker function that runs the actual download"""
        downloads_folder = self.location_var.get() or os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Get the path to the bundled ffmpeg
        ffmpeg_path = get_ffmpeg_path()
        
        # Validate time intervals
        start_time = self.start_time_var.get().strip()
        end_time = self.end_time_var.get().strip()
        
        start_seconds = None
        end_seconds = None
        
        if start_time and start_time != "00:00:00":
            start_seconds = self.validate_time_format(start_time)
            if start_seconds is False:
                self.after(0, lambda: self.download_error("Invalid start time format. Use HH:MM:SS, MM:SS, or SS"))
                return
        
        if end_time:
            end_seconds = self.validate_time_format(end_time)
            if end_seconds is False:
                self.after(0, lambda: self.download_error("Invalid end time format. Use HH:MM:SS, MM:SS, or SS"))
                return
            
            # Validate that end time is after start time
            if start_seconds is not None and end_seconds <= start_seconds:
                self.after(0, lambda: self.download_error("End time must be after start time"))
                return
        
        # Use yt-dlp command directly (assumes bundled executable)
        command = ["yt-dlp", "-P", downloads_folder, "--progress"]
        
        # Add ffmpeg location if available
        if ffmpeg_path:
            print(f"Using bundled ffmpeg: {ffmpeg_path}")
            command.extend(["--ffmpeg-location", ffmpeg_path])
        else:
            print("No bundled ffmpeg found, will use system ffmpeg if available")
        
        # Track if this is an audio-only download
        is_audio_download = self.format_var.get() in ["mp3", "m4a"]
        audio_format = self.format_var.get()
        
        # Add format and quality options
        if is_audio_download:
            command.extend(["-f", "bestaudio/best", "--extract-audio", "--audio-format", audio_format])
            # Add audio quality for audio downloads
            if self.audio_quality_var.get() != "Highest Audio Quality":
                # Map display value to internal yt-dlp audio quality value
                audio_quality_map = {
                    "Highest Audio Quality": "0",
                    "256kbps": "2",
                    "192kbps": "5",
                    "128kbps": "7",
                    "64kbps": "9"
                }
                quality_value = audio_quality_map[self.audio_quality_var.get()]
                command.extend(["--audio-quality", quality_value])
        else:
            # Handle video format with quality selection
            video_format = self.format_var.get()
            quality_selection = self.quality_var.get()
            
            if quality_selection == "Highest Video Quality":
                # Use best available quality
                command.extend(["-f", "bestvideo+bestaudio/best"])
            else:
                # Extract height from quality (e.g., "1080p" -> "1080")
                height = quality_selection.replace('p', '')
                # Fix: Improved format string for more reliable quality selection
                format_str = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
                command.extend(["-f", format_str])
            
            # Add audio quality for video downloads if specified
            if self.audio_quality_var.get() != "Highest Audio Quality":
                # Map display value to internal yt-dlp audio quality value
                audio_quality_map = {
                    "Highest Audio Quality": "0",
                    "256kbps": "2",
                    "192kbps": "5",
                    "128kbps": "7",
                    "64kbps": "9"
                }
                quality_value = audio_quality_map[self.audio_quality_var.get()]
                command.extend(["--audio-quality", quality_value])
            
            # Set the merge output format based on user selection
            if self.format_var.get() == "mp4":
                command.extend(["--merge-output-format", "mp4"])
            elif self.format_var.get() == "webm":
                command.extend(["--merge-output-format", "webm"])
        
        # Add time interval options using yt-dlp's download sections
        if start_seconds is not None or end_seconds is not None:
            if start_seconds is not None and end_seconds is not None:
                # Both start and end times specified
                # Fix: Format time values as HH:MM:SS for better compatibility
                start_formatted = self.format_seconds_to_time(start_seconds)
                end_formatted = self.format_seconds_to_time(end_seconds)
                command.extend(["--download-sections", f"*{start_formatted}-{end_formatted}"])
            elif start_seconds is not None:
                # Only start time specified - download from start time to end
                start_formatted = self.format_seconds_to_time(start_seconds)
                command.extend(["--download-sections", f"*{start_formatted}-inf"])
            elif end_seconds is not None:
                # Only end time specified - download from beginning to end time
                end_formatted = self.format_seconds_to_time(end_seconds)
                command.extend(["--download-sections", f"*0-{end_formatted}"])
            
        # Add optional settings
        if self.filename_var.get():
            # Fix: Ensure filename doesn't contain invalid characters
            safe_filename = self.sanitize_filename(self.filename_var.get())
            command.extend(["-o", f"{safe_filename}.%(ext)s"])
        else:
            # Fix: Add a default output template to prevent filename issues
            command.extend(["-o", "%(title)s.%(ext)s"])
            
        command.append(url)
        
        # Debug: Print the command being executed
        print("yt-dlp command:", " ".join(command))
        
        try:
            # Fix: Check if we're on Windows before using STARTUPINFO
            if os.name == 'nt':  # Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                        text=True, startupinfo=startupinfo, bufsize=1, universal_newlines=True)
            else:  # macOS, Linux, etc.
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                        text=True, bufsize=1, universal_newlines=True)
            
            # Initialize progress tracking
            self.after(0, lambda: self.progress_label.config(text="Starting download..."))
                
            # Read output line by line to track progress
                
            # Add flag to track download state for time-sectioned downloads
            download_started = False
            download_completed = False
            incremental_progress_started = False  # Track if incremental progress has started
            
            for line in process.stdout:
                line = line.strip()
                # Debug the output lines to help diagnose progress issues
                print(f"yt-dlp output: {line}")
                
                # When downloading time sections, use simplified checkpoints
                if start_seconds is not None or end_seconds is not None:
                    # First checkpoint: Downloading - 33%
                    if not download_started and ("[download]" in line or "Downloading" in line):
                        download_started = True
                        self.after(0, lambda: self.progress_label.config(text="Downloading..."))
                        self.after(0, lambda: self.progress_bar.configure(value=33))
                    
                    # Second checkpoint: Preparing File - 50%
                    elif download_started and not download_completed and (
                        "100%" in line or "Merging" in line or "ffmpeg" in line.lower() or 
                        line.startswith("frame=") or "Destination" in line
                    ):
                        download_completed = True
                        self.after(0, lambda: self.progress_label.config(text="Preparing File..."))
                        self.after(0, lambda: self.progress_bar.configure(value=50))
                        
                        # Start incremental progress after reaching "Preparing File" stage
                        if not incremental_progress_started:
                            incremental_progress_started = True
                            self.start_incremental_progress(50)
                    
                    continue  # Skip normal progress parsing for time sections
                
                # Normal progress parsing for non-sectioned downloads
                if '[download]' in line:
                    # Parse progress from yt-dlp output
                    try:
                        # Look for percentage in the line
                        import re
                        # Updated pattern to match both "45.67%" and "100%" formats
                        percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                        if percent_match:
                            percent = float(percent_match.group(1))
                            print(f"Found progress: {percent}%")  # Debug output
                            # Update progress on main thread
                            self.after(0, lambda p=percent, l=line, audio=is_audio_download: self.update_progress(p, l, audio))
                        elif "ETA" in line:
                            # Try to extract download progress from ETA lines
                            eta_match = re.search(r'(\d+\.\d+)% of', line)
                            if eta_match:
                                percent = float(eta_match.group(1))
                                print(f"Found progress from ETA line: {percent}%")  # Debug output
                                self.after(0, lambda p=percent, l=line, audio=is_audio_download: self.update_progress(p, l, audio))
                        elif "Destination" in line:
                            # Show that we're preparing to download
                            self.after(0, lambda: self.progress_label.config(text="Preparing file..."))
                        elif "Resuming" in line:
                            # Show that we're resuming download
                            self.after(0, lambda: self.progress_label.config(text="Resuming download..."))
                    except Exception as e:
                        # Log progress parsing errors
                        print(f"Progress parsing error: {e} on line: {line}")
                
                # Also check for frame progress lines which indicate post-processing
                elif line.startswith("frame="):
                    # This indicates post-processing, update progress to show this
                    self.after(0, lambda: self.progress_label.config(text="Processing video..."))
                    # Keep progress bar at a high value during processing
                    self.after(0, lambda: self.progress_bar.configure(value=85))

            # Cancel any incremental progress timer when the process completes
            self.cancel_incremental_progress()
            
            process.wait()
            if process.returncode == 0:
                self.after(0, self.download_success)
            else:
                self.after(0, lambda: self.download_error(f"Download failed with return code {process.returncode}"))
                
        except subprocess.CalledProcessError as e:
            # Cancel incremental progress on error
            self.cancel_incremental_progress()
            # Schedule UI update on main thread
            self.after(0, lambda: self.download_error(f"Download failed: {e}"))
        except FileNotFoundError:
            # Cancel incremental progress on error
            self.cancel_incremental_progress()
            # Schedule UI update on main thread
            self.after(0, lambda: self.download_error("yt-dlp not found. Please ensure yt-dlp is properly installed."))
        except Exception as e:
            # Cancel incremental progress on error
            self.cancel_incremental_progress()
            # Handle any other exceptions
            self.after(0, lambda: self.download_error(f"Unexpected error: {str(e)}"))

    def start_incremental_progress(self, start_value):
        """Start incremental progress updates that increase by 1% every 1-2 seconds"""
        import random
        
        # Store the current progress value
        self.current_progress = start_value
        
        def update_progress():
            """Update progress bar by 1%"""
            # Increment progress by 1%, but don't exceed 99%
            self.current_progress = min(self.current_progress + 1, 99)
            self.after(0, lambda: self.progress_bar.configure(value=self.current_progress))
            
            # Continue if we haven't reached 99% yet
            if self.current_progress < 99:
                # Schedule next update with random delay between 1-2 seconds
                delay = random.randint(1000, 2000)  # 1-2 seconds in milliseconds
                self.progress_increment_timer = self.after(delay, update_progress)
        
        # Start the first progress update
        update_progress()

    def cancel_incremental_progress(self):
        """Cancel any ongoing incremental progress updates"""
        if self.progress_increment_timer:
            self.after_cancel(self.progress_increment_timer)
            self.progress_increment_timer = None

    def update_progress(self, percent, status_line, is_audio=False):
        """Update progress bar and label (runs on main thread)"""
        # Ensure progress value is between 0 and 100
        percent = max(0, min(percent, 100))
        self.progress_bar['value'] = percent
        
        # Handle audio finishing state
        if is_audio and percent >= 100.0 and not self.is_mp3_finishing:
            self.is_mp3_finishing = True
            self.progress_label.config(text="Extracting Audio...")
            return
        elif is_audio and self.is_mp3_finishing:
            # Don't update progress text if we're in audio finishing state
            return
        
        # Extract useful info from status line for display
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

    def download_success(self):
        """Handle successful download (runs on main thread)"""
        # Cancel any incremental progress
        self.cancel_incremental_progress()
        
        self.progress_bar['value'] = 100
        self.progress_label.config(text="Download completed!")
        self.is_mp3_finishing = False  # Reset finishing state
        self.hide_loading()
        messagebox.showinfo("Success", "Download completed successfully!")

    def download_error(self, error_message):
        """Handle download error (runs on main thread)"""
        # Cancel any incremental progress
        self.cancel_incremental_progress()
        
        self.progress_label.config(text="Download failed")
        self.is_mp3_finishing = False  # Reset finishing state
        self.hide_loading()
        messagebox.showerror("Download Error", error_message)

    def validate_time_format(self, time_str):
        """Validate time format and convert to seconds"""
        if not time_str or time_str.strip() == "":
            return None
            
        time_str = time_str.strip()
        
        # Pattern for H:MM:SS or MM:SS or SS
        patterns = [
            r'^(\d{1,2}):(\d{2}):(\d{2})$',  # H:MM:SS
            r'^(\d{1,2}):(\d{2})$',          # MM:SS
            r'^(\d+)$'                       # SS
        ]
        
        for pattern in patterns:
            match = re.match(pattern, time_str)
            if match:
                groups = match.groups()
                if len(groups) == 3:  # H:MM:SS
                    hours, minutes, seconds = map(int, groups)
                    return hours * 3600 + minutes * 60 + seconds
                elif len(groups) == 2:  # MM:SS
                    minutes, seconds = map(int, groups)
                    return minutes * 60 + seconds
                else:  # SS
                    return int(groups[0])
        
        return False  # Invalid format

    def format_seconds_to_time(self, seconds):
        """Convert seconds to HH:MM:SS format for yt-dlp"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Remove characters that are invalid in filenames
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.strip()

if __name__ == "__main__":
    app = CustomWindow()
    app.mainloop()