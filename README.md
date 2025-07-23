# Downly - YouTube Downloader

A simple, elegant YouTube downloader built with Python, yt-dlp, and tkinter. Download videos and audio with customizable quality settings.

## Features
- Download YouTube videos in multiple formats (MP4, WebM, MP3, M4A)
- Quality selection for both video and audio
- Time interval downloads (clips)
- Custom filename support
- Dark theme UI
- Progress tracking with cancel functionality

## Installation & Usage
- **Standalone**: Run `python ./build_scripts/build.py` to create a distributable directory at `./dist/downly/`
  - The main executable will be at `./dist/downly/downly.exe`
  - All dependencies (ffmpeg, yt-dlp) are bundled in the directory
  - Distribute the entire `downly` folder to end users
- **Development**: Run `python ./src/downly.py` after activating the virtual environment

*Note: ffmpeg and yt-dlp are bundled - no separate installation required.*

---

## Developer Checklist

### Low Priority / Polish
- [ ] **Tooltips** for settings explanations

## Known Issues
- **Time interval downloads**: No progress percentage due to yt-dlp logging limitations
- **Format compatibility**: Some quality/format combinations may not be available for all videos
-**Cross-platform capabilities**: This program was developed for Windows 11. It is not guaranteed to work on other platforms

## Technical Notes
- Uses yt-dlp for downloading and ffmpeg for processing
- PyInstaller for standalone executable creation (directory-based distribution)
- Executable and dependencies are bundled in a single directory for easy distribution
- Path resolution works in both development and bundled environments