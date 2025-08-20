# =====
#
#   Downly Configuration Module
#
#   Contains all application constants, settings, and configuration data.
#
# =====

import os

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

# Preset configurations for simplified user experience
PRESETS = {
    "Video": {
        "High": {"format": "mp4", "video_quality": "Highest Video Quality", "audio_quality": "Highest Audio Quality"},
        "Standard": {"format": "mp4", "video_quality": "720p", "audio_quality": "192kbps"},
        "Low": {"format": "mp4", "video_quality": "240p", "audio_quality": "64kbps"}
    },
    "Audio": {
        "High": {"format": "mp3", "video_quality": "---", "audio_quality": "Highest Audio Quality"},
        "Standard": {"format": "mp3", "video_quality": "---", "audio_quality": "192kbps"},
        "Low": {"format": "mp3", "video_quality": "---", "audio_quality": "64kbps"}
    }
}

# UI Theme Configuration
class ThemeConfig:
    """UI theme configuration with dark theme color palette."""
    
    # Color palette
    PRIMARY_BG = "#1e1e1e"
    SURFACE_BG = "#2a2a2a"
    TEXT_TITLE = "#ff0050"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#cccccc"
    TEXT_HINT = "#888888"
    ACCENT_BLUE = "#ff0050"
    ACCENT_GREEN = "#16a085"
    ACCENT_GREEN_HOVER = "#138d75"
    ACCENT_GREEN_PRESSED = "#117a65"
    ACCENT_RED = "#e74c3c"
    ACCENT_RED_HOVER = "#c0392b"
    ACCENT_RED_PRESSED = "#a93226"
    BORDER_COLOR = "#404040"
    BORDER_ACCENT = "#ff0050"

    # Font configuration
    TITLE_FONT = ("Arial", 24, "bold")
    HEADING_FONT = ("Arial", 12, "bold")
    NORMAL_FONT = ("Arial", 10)
    SMALL_FONT = ("Arial", 9)
    TINY_FONT = ("Arial", 8)
    BUTTON_FONT = ("Arial", 12, "bold")

# Application Configuration
class AppConfig:
    """Application configuration settings."""
    
    WINDOW_TITLE = "Downly - YouTube Downloader"
    WINDOW_GEOMETRY = "600x860"
    WINDOW_MIN_SIZE = (600, 700)
    
    # Download settings
    DEFAULT_DOWNLOAD_LOCATION = "Downloads"
    
    # Process settings
    DOWNLOAD_RETRIES = 3
    FRAGMENT_RETRIES = 3
    RETRY_SLEEP = 2
    SOCKET_TIMEOUT = 30
    SLEEP_INTERVAL = 1
    MAX_SLEEP_INTERVAL = 3
    CONCURRENT_FRAGMENTS = 4
    BUFFER_SIZE = "16K"
    
    # Animation settings
    ANIMATION_INTERVAL = 1000  # milliseconds
    CANCELLATION_TIMEOUT = 5   # seconds
