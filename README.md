# Downly - YouTube Downloader

A simple, elegant YouTube downloader built with Python, yt-dlp, and tkinter. Download videos and audio with customizable quality settings.

## Features
- Download YouTube videos in multiple formats (MP4, WebM, MP3, M4A)
- Quality selection for both video and audio
- Time interval downloads (clips)
- Custom filename support
- Dark theme UI
- Progress tracking with cancel functionality
- Able to download subtitles and metadata

## Installation & Usage

### Quick Start
- **Installer**: Download and run the downly_installer from the latest release.
- **Portable**: Extract the portable version from the latest release .zip file and run `downly.exe`.
- **Development**: Clone the repository and run `python ./setup/setup_venv.py`. Then activate the virtual environment and run `python ./src/main.py`.

*Note: Release builds are stand-alone apps that have yt-dlp and ffmpeg bundled - ffmpeg and yt-dlp.exe standalone will need to be downloaded seperately for development*

---

## Developer Checklist

# High Priority
- [ ] **.wav support** for audio downloads

### Low Priority / Polish
- [ ] **Tooltips** for settings explanations
- [ ] **Time interval downloads** try to find a workaround for FFMPEG needing to stream the old file to trim it

## Limitations & Known Behavior

### Time Interval Downloads (Video Clips)
- **Processing Time**: Downloading specific sections takes significantly longer than expected
- **Performance Impact**: Processing adds approximately 50% of the clip duration to download time
  - *Example: A 1-hour clip requires an additional 30 minutes for processing*
- **Recommendation**: For best performance, either download the entire video or limit clips to short sections
- **Progress Tracking**: Limited progress information available during processing due to yt-dlp constraints

### General Limitations
- **Format Availability**: Not all quality/format combinations are available for every video
- **Platform Dependency**: Some features may vary based on the source platform's capabilities

## Technical Notes
- Uses yt-dlp for downloading and ffmpeg for processing
- PyInstaller for standalone executable creation
- Inno Setup for installer creation
- FFMPEG and yt-dlp are bundled with the application
- Find  yt-dlp standalone releases [here](https://github.com/yt-dlp/yt-dlp/releases).
