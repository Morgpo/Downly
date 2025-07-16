# =====
#
#   Downly - YouTube Downloader
#
#   A simple YouTube downloader application using yt-dlp, ffmpeg, and tkinter.
#   Designed to be built into a single executable using PyInstaller. A one-stop-shop for downloading YouTube videos into local audio or video; no dependencies or sketchy websites required.
#
#   This is the main application script, which provides the GUI and download functionality.
#
# =====

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import threading
import queue
import time
import sys
import os
import re

# Constants for audio quality mapping
AUDIO_QUALITY_MAP = {
	"Highest Audio Quality": "0",
	"256kbps": "2",
	"192kbps": "5",
	"128kbps": "7",
	"64kbps": "9"
}

# YouTube URL patterns for validation
YOUTUBE_PATTERNS = [
	r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
	r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
	r'(?:https?://)?youtu\.be/[\w-]+',
	r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+',
	r'(?:https?://)?(?:www\.)?youtube\.com/live/[\w-]+',
	r'(?:https?://)?(?:m\.)?youtube\.com/watch\?v=[\w-]+'
]



#
# ===== Helper Functions ===== #
#

def resource_path(relative_path):
	# Get absolute path to resource, handling both development and PyInstaller environments
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
	# Locate ffmpeg executable in various potential locations (bundled, dev environment, system)
	bundled_ffmpeg = resource_path("ffmpeg.exe")

	if os.path.exists(bundled_ffmpeg):
		return bundled_ffmpeg

	dev_ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".venv", "Scripts", "ffmpeg.exe")
	if os.path.exists(dev_ffmpeg):
		return dev_ffmpeg

	for subdir in [".", "bin", "tools", "ffmpeg"]:
		possible_path = resource_path(os.path.join(subdir, "ffmpeg.exe"))
		if os.path.exists(possible_path):
			return possible_path

	return None

def get_ytdlp_path():
	# Locate yt-dlp executable in various potential locations (bundled, dev environment, system)
	bundled_ytdlp = resource_path("yt-dlp.exe")

	if os.path.exists(bundled_ytdlp):
		return bundled_ytdlp

	dev_ytdlp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".venv", "Scripts", "yt-dlp.exe")
	if os.path.exists(dev_ytdlp):
		return dev_ytdlp

	# Try system PATH
	return "yt-dlp"



#
# ===== Main Application Window ===== #
#

class CustomWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Downly - YouTube Downloader")

		# ===== Window Configuration ===== #
		self.resizable(False, False)
		self.geometry("900x900")
		self.minsize(600, 700)
		self.configure(bg="#1e1e1e")

		self.style = ttk.Style()
		self.style.theme_use('clam')

		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.configure_styles()

		# ===== Window Icon Setup ===== #
		try:
			icon_path = resource_path("assets/icon.ico")
			self.iconbitmap(icon_path)
		except Exception as e:
			print(f"Could not load window icon: {e}")

		# ===== Main Container Setup ===== #
		self.main_frame = ttk.Frame(self, padding="20", style="Main.TFrame")
		self.main_frame.pack(fill=tk.BOTH, expand=True)

		# ===== Header Section (Logo and Title) ===== #
		self.header_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
		self.header_frame.pack(pady=(0, 20), fill=tk.X)

		self.header_frame.grid_columnconfigure(1, weight=1)

		self.title_label = ttk.Label(self.header_frame, text="Downly", style="Title.TLabel")
		self.title_label.grid(row=0, column=1, sticky="")

		# Logo loading with error handling
		try:
			logo_path = resource_path("assets/logo.png")
			if os.path.exists(logo_path):
				self.logo_image = tk.PhotoImage(file=logo_path)

				self.logo_left = tk.Label(self.header_frame, image=self.logo_image, bg="#1e1e1e")
				self.logo_left.grid(row=0, column=0, padx=(0, 20), sticky="w")

				self.logo_right = tk.Label(self.header_frame, image=self.logo_image, bg="#1e1e1e")
				self.logo_right.grid(row=0, column=2, padx=(20, 0), sticky="e")
			else:
				print(f"Logo file not found at path: {logo_path}")

		except Exception as e:
			print(f"Could not load logo: {e}")

		# ===== URL Input Section ===== #
		self.url_frame = ttk.LabelFrame(self.main_frame, text="YouTube URL", padding="15", style="Modern.TLabelframe")
		self.url_frame.pack(fill=tk.X, pady=(0, 15))

		self.url_entry = ttk.Entry(self.url_frame, style="Modern.TEntry")
		self.url_entry.insert(0, "Paste YouTube link here...")
		self.url_entry.pack(fill=tk.X)

		# ===== Required Settings Section ===== #
		self.required_frame = ttk.LabelFrame(self.main_frame, text="Required Settings",
										   padding="15", style="Modern.TLabelframe")
		self.required_frame.pack(fill=tk.X, pady=(0, 15))

		# Format selection
		ttk.Label(self.required_frame, text="Format:", style="SectionLabel.TLabel").pack(anchor="w")
		self.format_var = tk.StringVar(value="mp4")
		self.format_dropdown = ttk.Combobox(self.required_frame, textvariable=self.format_var,
										  style="Modern.TCombobox")
		self.format_dropdown["values"] = ("mp4", "webm", "mp3", "m4a")
		self.format_dropdown.pack(fill=tk.X, pady=(5, 15))

		# Video quality selection
		ttk.Label(self.required_frame, text="Video Quality:", style="SectionLabel.TLabel").pack(anchor="w")
		self.quality_var = tk.StringVar(value="Highest Video Quality")
		self.quality_dropdown = ttk.Combobox(self.required_frame, textvariable=self.quality_var,
										   style="Modern.TCombobox")
		self.quality_dropdown["values"] = ("Highest Video Quality", "2160p","1440p", "1080p", "720p", "480p", "360p", "240p", "144p")
		self.quality_dropdown.pack(fill=tk.X, pady=(5, 15))

		# Audio quality selection
		ttk.Label(self.required_frame, text="Audio Quality:", style="SectionLabel.TLabel").pack(anchor="w")
		self.audio_quality_var = tk.StringVar(value="Highest Audio Quality")
		self.audio_quality_dropdown = ttk.Combobox(self.required_frame, textvariable=self.audio_quality_var,
												 style="Modern.TCombobox")
		self.audio_quality_dropdown["values"] = ("Highest Audio Quality", "256kbps", "192kbps", "128kbps", "64kbps")
		self.audio_quality_dropdown.pack(fill=tk.X, pady=(5, 0))

		# ===== Optional Settings Section ===== #
		self.optional_frame = ttk.LabelFrame(self.main_frame, text="Optional Settings",
										   padding="15", style="Modern.TLabelframe")
		self.optional_frame.pack(fill=tk.X, pady=(0, 15))

		# Custom filename
		ttk.Label(self.optional_frame, text="Custom Filename:", style="SectionLabel.TLabel").pack(anchor="w")
		self.filename_var = tk.StringVar()
		self.filename_entry = ttk.Entry(self.optional_frame, textvariable=self.filename_var,
									  style="Modern.TEntry")
		self.filename_entry.pack(fill=tk.X, pady=(5, 15))

		# Time interval section
		ttk.Label(self.optional_frame, text="Time Interval:", style="SectionLabel.TLabel").pack(anchor="w")

		self.time_frame = ttk.Frame(self.optional_frame, style="Main.TFrame")
		self.time_frame.pack(fill=tk.X, pady=(5, 15))

		ttk.Label(self.time_frame, text="From:", style="SmallLabel.TLabel").pack(side=tk.LEFT)
		self.start_time_var = tk.StringVar()
		self.start_time_entry = ttk.Entry(self.time_frame, textvariable=self.start_time_var,
										style="Small.TEntry", width=12)
		self.start_time_entry.pack(side=tk.LEFT, padx=(5, 10))
		self.start_time_entry.insert(0, "00:00:00")

		ttk.Label(self.time_frame, text="To:", style="SmallLabel.TLabel").pack(side=tk.LEFT)
		self.end_time_var = tk.StringVar()
		self.end_time_entry = ttk.Entry(self.time_frame, textvariable=self.end_time_var,
									  style="Small.TEntry", width=12)
		self.end_time_entry.pack(side=tk.LEFT, padx=(5, 0))
		self.end_time_entry.insert(0, "")

		ttk.Label(self.optional_frame, text="Format: HH:MM:SS; MM:SS; SS (leave 'To' empty for full video)",
				 style="HintLabel.TLabel").pack(anchor="w", pady=(0, 15))

		# Download location
		ttk.Label(self.optional_frame, text="Download Location:", style="SectionLabel.TLabel").pack(anchor="w")
		self.location_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
		self.location_entry = ttk.Entry(self.optional_frame, textvariable=self.location_var,
									  style="Modern.TEntry")
		self.location_entry.pack(fill=tk.X, pady=(5, 0))

		# ===== Dropdown Event Handlers ===== #
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

		# Configure dropdown properties and fix selection highlighting issues
		self.format_dropdown.state(["readonly"])
		self.quality_dropdown.state(["readonly"])
		self.audio_quality_dropdown.state(["readonly"])

		def on_focus_out(event):
			# Handle focus out events to clear selection
			widget = event.widget
			widget.selection_clear()

		def on_button_release(event):
			# Clear selection after mouse click
			widget = event.widget
			self.after(1, lambda: widget.selection_clear())

		for combo in [self.format_dropdown, self.quality_dropdown, self.audio_quality_dropdown]:
			combo.bind('<FocusOut>', on_focus_out)
			combo.bind('<Button-1>', on_button_release)
			combo.bind('<ButtonRelease-1>', on_button_release)

		# ===== Download Controls and Progress ===== #
		self.button_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
		self.button_frame.pack(pady=20)
		
		self.button = ttk.Button(self.button_frame, text="Download",
							   command=self.ytdlp_download, style="Download.TButton", width=15)
		self.button.pack(side=tk.LEFT, padx=(0, 10), ipady=10)
		
		self.cancel_button = ttk.Button(self.button_frame, text="Cancel",
									  command=self.cancel_download, style="Cancel.TButton", width=15)
		self.cancel_button.pack(side=tk.LEFT, ipady=10)
		self.cancel_button.config(state="disabled")

		self.progress_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
		self.progress_frame.pack(fill=tk.X, pady=(0, 10))

		self.progress_label = ttk.Label(self.progress_frame, text="Ready to download",
									   style="ProgressLabel.TLabel")
		self.progress_label.pack()

		self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate',
										  style="Modern.Horizontal.TProgressbar")
		self.progress_bar.pack(fill=tk.X, pady=(5, 0))
		self.progress_bar['value'] = 0

		# Initialize animation state variables
		self.animation_state = 0
		self.animation_timer = None
		self.is_mp3_finishing = False
		
		# Initialize download process tracking
		self.download_process = None
		self.download_thread = None
		self.is_downloading = False

	#
	# ===== Style Configuration ===== #
	#

	def configure_styles(self):
		# Configure modern styling for the application with dark theme and consistent color palette
		# Color palette
		primary_bg = "#1e1e1e"
		surface_bg = "#2a2a2a"
		text_title = "#ff0050"
		text_primary = "#ffffff"
		text_secondary = "#cccccc"
		text_hint = "#888888"
		accent_blue = "#ff0050"
		accent_green = "#16a085"
		accent_green_hover = "#138d75"
		accent_green_pressed = "#117a65"
		accent_red = "#e74c3c"
		accent_red_hover = "#c0392b"
		accent_red_pressed = "#a93226"
		border_color = "#404040"
		border_accent = "#ff0050"

		# Font configuration
		title_font = ("Arial", 24, "bold")
		heading_font = ("Arial", 12, "bold")
		normal_font = ("Arial", 10)
		small_font = ("Arial", 9)
		tiny_font = ("Arial", 8)
		button_font = ("Arial", 12, "bold")

		# Configure all widget styles
		self.style.configure("Main.TFrame", background=primary_bg)
		self.style.configure("Title.TLabel", foreground=text_title, background=primary_bg, font=title_font)

		# LabelFrame styling
		self.style.configure("Modern.TLabelframe", background=primary_bg, borderwidth=1, relief="solid", bordercolor=border_color)
		self.style.configure("Modern.TLabelframe.Label", background=primary_bg, foreground=accent_blue, font=heading_font)

		# Label styles
		self.style.configure("SectionLabel.TLabel", background=primary_bg, foreground=text_primary, font=normal_font)
		self.style.configure("SmallLabel.TLabel", background=primary_bg, foreground=text_secondary, font=small_font)
		self.style.configure("HintLabel.TLabel", background=primary_bg, foreground=text_hint, font=tiny_font)
		self.style.configure("ProgressLabel.TLabel", background=primary_bg, foreground=text_secondary, font=small_font)

		# Entry styling
		self.style.configure("Modern.TEntry", fieldbackground=surface_bg, foreground=text_primary, borderwidth=1, bordercolor=border_color, focuscolor=border_accent, insertcolor=text_primary, font=normal_font)
		self.style.configure("Small.TEntry", fieldbackground=surface_bg, foreground=text_primary, borderwidth=1, bordercolor=border_color, focuscolor=border_accent, insertcolor=text_primary, font=small_font)

		# Combobox styling
		self.style.configure("Modern.TCombobox", fieldbackground=surface_bg, foreground=text_primary, borderwidth=1, bordercolor=border_color, focuscolor=border_accent, arrowcolor=text_secondary, background=primary_bg, selectbackground=surface_bg, selectforeground=text_primary, font=normal_font)
		self.style.map("Modern.TCombobox", selectbackground=[("focus", surface_bg), ("!focus", surface_bg)], selectforeground=[("focus", text_primary), ("!focus", text_primary)], fieldbackground=[("readonly", surface_bg), ("focus", surface_bg)], bordercolor=[("focus", border_accent), ("!focus", border_color)], focuscolor=[("focus", "none"), ("!focus", "none")])

		# Configure dropdown listbox styling
		self.option_add('*TCombobox*Listbox.selectBackground', surface_bg)
		self.option_add('*TCombobox*Listbox.selectForeground', text_primary)
		self.option_add('*TCombobox*Listbox.background', surface_bg)
		self.option_add('*TCombobox*Listbox.foreground', text_primary)

		# Button and progress bar styling
		self.style.configure("Download.TButton", font=button_font, foreground=text_primary, background=accent_green, borderwidth=0, focuscolor="none")
		self.style.map("Download.TButton", background=[("active", accent_green_hover), ("pressed", accent_green_pressed)], foreground=[("active", text_primary), ("pressed", text_primary)])
		self.style.configure("Cancel.TButton", font=button_font, foreground=text_primary, background=accent_red, borderwidth=0, focuscolor="none")
		self.style.map("Cancel.TButton", background=[("active", accent_red_hover), ("pressed", accent_red_pressed), ("disabled", "#666666")], foreground=[("active", text_primary), ("pressed", text_primary), ("disabled", "#999999")])
		self.style.configure("Modern.Horizontal.TProgressbar", background=accent_blue, troughcolor=surface_bg, borderwidth=1, lightcolor=accent_blue, darkcolor=accent_blue)

	#
	# ===== Audio Quality and Format String Generation ===== #
	#

	def get_audio_quality_value(self, audio_quality_text):
		# Map audio quality display text to yt-dlp quality values
		return AUDIO_QUALITY_MAP.get(audio_quality_text, "0")

	def add_audio_quality_option(self, command):
		# Add audio quality parameter to yt-dlp command if not using highest quality
		if self.audio_quality_var.get() != "Highest Audio Quality":
			quality_value = self.get_audio_quality_value(self.audio_quality_var.get())
			command.extend(["--audio-quality", quality_value])

	def get_time_section_format_string(self, video_format, quality_selection):
		# Generate optimized format string for time-sectioned downloads with codec compatibility
		if quality_selection == "Highest Video Quality":
			if video_format == "mp4":
				return "best[ext=mp4][acodec^=mp4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
			elif video_format == "webm":
				return "best[ext=webm][acodec^=vorbis]/bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best"
			else:
				return "bestvideo+bestaudio/best"
		else:
			height = quality_selection.replace('p', '')
			if video_format == "mp4":
				return f"best[height<={height}][ext=mp4][acodec^=mp4a]/bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
			elif video_format == "webm":
				return f"best[height<={height}][ext=webm][acodec^=vorbis]/bestvideo[height<={height}][ext=webm]+bestaudio[ext=webm]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
			else:
				return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

	def get_video_format_string(self, video_format, quality_selection):
		# Generate format string for standard video downloads
		if quality_selection == "Highest Video Quality":
			if video_format == "mp4":
				return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
			elif video_format == "webm":
				return "bestvideo[ext=webm]+bestaudio[ext=webm]/bestvideo+bestaudio/best"
			else:
				return "bestvideo+bestaudio/best"
		else:
			height = quality_selection.replace('p', '')
			if video_format == "mp4":
				return f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
			elif video_format == "webm":
				return f"bestvideo[height<={height}][ext=webm]+bestaudio[ext=webm]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
			else:
				return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

	#
	# ===== Download Process Management ===== #
	#

	def ytdlp_download(self):
		# Main download handler - validates URL and initiates download process
		url = self.url_entry.get().strip()
		is_valid_youtube = any(re.match(pattern, url, re.IGNORECASE) for pattern in YOUTUBE_PATTERNS)

		if not is_valid_youtube:
			messagebox.showerror("Invalid URL", "Please enter a valid YouTube URL.\n\nSupported formats:\n• youtube.com/watch?v=...\n• youtu.be/...\n• youtube.com/shorts/...\n• youtube.com/playlist?list=...")
			return

		self.start_download_thread(url)

	def start_download_thread(self, url):
		# Initialize download UI state and start background download thread
		self.is_downloading = True
		self.show_loading()

		self.download_thread = threading.Thread(target=self.download_worker, args=(url,))
		self.download_thread.daemon = True
		self.download_thread.start()

	#
	# ===== UI Animation and State Management ===== #
	#

	def show_loading(self):
		# Display loading animation and disable download controls
		self.button.config(state="disabled")
		self.cancel_button.config(state="normal")
		self.progress_label.config(text="Preparing download...")
		self.progress_bar['value'] = 0
		self.animation_state = 0
		self.animate_button_text()

	def animate_button_text(self):
		# Animate download button with cycling ellipsis pattern
		ellipsis_patterns = [".  ", ".. ", "...", ".. "]
		current_pattern = ellipsis_patterns[self.animation_state % len(ellipsis_patterns)]
		self.button.config(text=f"Downloading{current_pattern}")

		self.animation_state += 1
		self.animation_timer = self.after(1000, self.animate_button_text)

	def hide_loading(self):
		# Reset UI to ready state and re-enable download controls
		if self.animation_timer:
			self.after_cancel(self.animation_timer)
			self.animation_timer = None
		self.button.config(state="normal", text="Download")
		self.cancel_button.config(state="disabled")
		self.progress_label.config(text="Ready to download")
		self.progress_bar['value'] = 0
		self.is_downloading = False
		self.download_process = None
		self.download_thread = None

	def cancel_download(self):
		# Cancel the current download process
		if not self.is_downloading:
			return
			
		try:
			# Set cancellation flag first to stop the download loop
			self.is_downloading = False
			
			# Schedule process termination on a background thread to avoid blocking UI
			def terminate_process():
				try:
					if self.download_process and self.download_process.poll() is None:
						self.download_process.terminate()
						
						# Wait a bit for graceful termination
						for _ in range(10):  # Wait up to 1 second
							if self.download_process.poll() is not None:
								break
							time.sleep(0.1)
						
						# Force kill if it's still running
						if self.download_process.poll() is None:
							self.download_process.kill()
				except Exception as e:
					print(f"Error terminating process: {e}")
			
			# Start termination in background thread
			termination_thread = threading.Thread(target=terminate_process)
			termination_thread.daemon = True
			termination_thread.start()
			
			# Update UI immediately
			self.progress_label.config(text="Cancelling download...")
			self.after(100, lambda: self.progress_label.config(text="Download cancelled"))
			self.after(200, self.hide_loading)
			
		except Exception as e:
			print(f"Error cancelling download: {e}")
			self.hide_loading()

	def process_download_line(self, line, is_audio_download, start_seconds, end_seconds):
		# Process a single line of output from yt-dlp
		if '[download]' in line:
			try:
				percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
				if percent_match:
					percent = float(percent_match.group(1))
					print(f"Found progress: {percent}%")
					self.after(0, lambda p=percent, l=line, audio=is_audio_download: self.update_progress(p, l, audio))
				elif "ETA" in line:
					eta_match = re.search(r'(\d+\.\d+)% of', line)
					if eta_match:
						percent = float(eta_match.group(1))
						print(f"Found progress from ETA line: {percent}%")
						self.after(0, lambda p=percent, l=line, audio=is_audio_download: self.update_progress(p, l, audio))
				elif "Destination" in line:
					self.after(0, lambda: self.progress_label.config(text="Preparing file..."))
				elif "Resuming" in line:
					self.after(0, lambda: self.progress_label.config(text="Resuming download..."))
			except Exception as e:
				print(f"Progress parsing error: {e} on line: {line}")

		elif line.startswith("frame=") or "ffmpeg" in line.lower():
			if start_seconds is not None or end_seconds is not None:
				self.after(0, lambda: self.progress_label.config(text="Trimming video..."))
			else:
				self.after(0, lambda: self.progress_label.config(text="Processing video..."))
			self.after(0, lambda: self.progress_bar.configure(value=90))

		elif "Merging" in line or "merger" in line.lower():
			self.after(0, lambda: self.progress_label.config(text="Merging audio and video..."))
			self.after(0, lambda: self.progress_bar.configure(value=95))

	#
	# ===== Download Worker and Command Building ===== #
	#

	def download_worker(self, url):
		# Main download worker - builds yt-dlp command and executes download process
		downloads_folder = self.location_var.get() or os.path.join(os.path.expanduser("~"), "Downloads")
		ffmpeg_path = get_ffmpeg_path()
		ytdlp_path = get_ytdlp_path()

		# Time interval validation and conversion
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

			if start_seconds is not None and end_seconds <= start_seconds:
				self.after(0, lambda: self.download_error("End time must be after start time"))
				return

		# Build base yt-dlp command
		command = [
			ytdlp_path, 
			"-P", downloads_folder,
			"--progress",
			"--no-part",
			"--no-overwrites",
			
			# Network and reliability flags
			"--retries", "3",
			"--fragment-retries", "3", 
			"--retry-sleep", "2",
			"--socket-timeout", "30",
			
			# User agent and rate limiting
			"--sleep-interval", "1",
			"--max-sleep-interval", "3",
			
			# Error handling and logging
			"--no-warnings",
			"--ignore-errors",
			"--abort-on-unavailable-fragment",
			
			# Format selection safety
			"--prefer-free-formats",
			"--check-formats",
			
			# Security and safety
			"--geo-bypass",
			"--no-check-certificate", 
			
			# Performance optimization
			"--concurrent-fragments", "4",
			"--buffer-size", "16K"
		]

		# Configure format options based on download type
		is_audio_download = self.format_var.get() in ["mp3", "m4a"]
		audio_format = self.format_var.get()

		if is_audio_download:
			command.extend(["-f", "bestaudio/best", "--extract-audio", "--audio-format", audio_format])
			self.add_audio_quality_option(command)

		# Handle time-sectioned downloads with optimized format selection
		if start_seconds is not None or end_seconds is not None:
			if not is_audio_download:
				video_format = self.format_var.get()
				quality_selection = self.quality_var.get()
				format_str = self.get_time_section_format_string(video_format, quality_selection)
				command.extend(["-f", format_str])

				if video_format == "mp4":
					command.extend(["--merge-output-format", "mp4"])
				elif video_format == "webm":
					command.extend(["--merge-output-format", "webm"])

				self.add_audio_quality_option(command)

			# Add download sections based on time constraints
			if start_seconds is not None and end_seconds is not None:
				start_formatted = self.format_seconds_to_time(start_seconds)
				end_formatted = self.format_seconds_to_time(end_seconds)
				command.extend(["--download-sections", f"*{start_formatted}-{end_formatted}"])
			elif start_seconds is not None:
				start_formatted = self.format_seconds_to_time(start_seconds)
				command.extend(["--download-sections", f"*{start_formatted}-inf"])
			elif end_seconds is not None:
				end_formatted = self.format_seconds_to_time(end_seconds)
				command.extend(["--download-sections", f"*0-{end_formatted}"])
		else:
			# Handle full downloads with codec-aware format selection
			if not is_audio_download:
				video_format = self.format_var.get()
				quality_selection = self.quality_var.get()
				format_str = self.get_video_format_string(video_format, quality_selection)
				command.extend(["-f", format_str])

				if self.format_var.get() == "mp4":
					command.extend(["--merge-output-format", "mp4"])
				elif self.format_var.get() == "webm":
					command.extend(["--merge-output-format", "webm"])

				self.add_audio_quality_option(command)

		# Configure output filename
		if self.filename_var.get():
			safe_filename = self.sanitize_filename(self.filename_var.get())
			command.extend(["-o", f"{safe_filename}.%(ext)s"])
		else:
			command.extend(["-o", "%(title)s.%(ext)s"])

		command.append(url)
		print("yt-dlp command:", " ".join(command))

		# Execute download process
		try:
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			startupinfo.wShowWindow = subprocess.SW_HIDE

			self.download_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
									text=True, startupinfo=startupinfo, bufsize=1, universal_newlines=True)

			self.after(0, lambda: self.progress_label.config(text="Starting download..."))

			# Create a queue to read lines from subprocess
			output_queue = queue.Queue()
			
			def read_output():
				try:
					for line in iter(self.download_process.stdout.readline, ''):
						if line:
							output_queue.put(line)
						if self.download_process.poll() is not None:
							break
				except:
					pass
				finally:
					output_queue.put(None)  # Signal end
			
			# Start output reading thread
			output_thread = threading.Thread(target=read_output)
			output_thread.daemon = True
			output_thread.start()
			
			# Process lines with cancellation checks
			while self.download_process.poll() is None:
				# Check if download was cancelled
				if not self.is_downloading:
					break
				
				try:
					# Get line with timeout to allow cancellation checks
					line = output_queue.get(timeout=0.1)
					if line is None:  # End signal
						break
					line = line.strip()
					if line:
						print(f"yt-dlp output: {line}")
						self.process_download_line(line, is_audio_download, start_seconds, end_seconds)
				except queue.Empty:
					# No output available, continue to check for cancellation
					continue

			# Check if download was cancelled before waiting
			if not self.is_downloading:
				return
				
			self.download_process.wait()
			if self.download_process.returncode == 0:
				self.after(0, self.download_success)
			else:
				self.after(0, lambda: self.download_error(f"Download failed with return code {self.download_process.returncode}"))

		except subprocess.CalledProcessError as e:
			self.after(0, lambda: self.download_error(f"Download failed: {e}"))
		except FileNotFoundError:
			self.after(0, lambda: self.download_error("yt-dlp not found. Please ensure yt-dlp is properly installed."))
		except Exception as e:
			self.after(0, lambda: self.download_error(f"Unexpected error: {str(e)}"))

	#
	# ===== Progress Tracking and UI Updates ===== #
	#

	def update_progress(self, percent, status_line, is_audio=False):
		# Update progress bar and status text based on download progress
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

	def download_success(self):
		# Handle successful download completion
		if not self.is_downloading:  # Don't show success if cancelled
			return
		self.progress_bar['value'] = 100
		self.progress_label.config(text="Download completed!")
		self.is_mp3_finishing = False
		self.hide_loading()
		messagebox.showinfo("Success", "Download completed successfully!")

	def download_error(self, error_message):
		# Handle download errors and display error message
		if not self.is_downloading:  # Don't show error if cancelled
			return
		self.progress_label.config(text="Download failed")
		self.is_mp3_finishing = False
		self.hide_loading()
		messagebox.showerror("Download Error", error_message)

	#
	# ===== Time Validation and Utility Functions ===== #
	#

	def validate_time_format(self, time_str):
		# Validate and convert time string to seconds (supports HH:MM:SS, MM:SS, or SS formats)
		if not time_str or time_str.strip() == "":
			return None

		time_str = time_str.strip()

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

		return False

	def format_seconds_to_time(self, seconds):
		# Convert seconds to HH:MM:SS format for yt-dlp
		hours, remainder = divmod(seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

	def sanitize_filename(self, filename):
		# Remove invalid filename characters using efficient string translation
		invalid_chars = '<>:"/\\|?*'
		translation_table = str.maketrans('', '', invalid_chars)
		return filename.translate(translation_table).strip()

	def on_closing(self):
		# Handle application shutdown
		if self.is_downloading:
			self.cancel_download()
		self.destroy()


#
# ===== Application Entry Point ===== #
#

if __name__ == "__main__":
	app = CustomWindow()
	app.mainloop()