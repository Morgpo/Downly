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
- **Standalone**: Run `python ./build_scripts/build.py` to create a distributable directory at `./dist/downly/`
  - The main executable will be at `./dist/downly/downly.exe`
  - All dependencies (ffmpeg, yt-dlp) are bundled in the directory
  - Use Inno Setup to create the installer by running `ISCC downly_installer.iss` in the `./installer/` directory
- **Development**: Run `python ./src/downly.py` after activating the virtual environment

*Note: ffmpeg and yt-dlp are bundled - no separate installation required.*

---

## Developer Checklist

### Low Priority / Polish
- [ ] **Tooltips** for settings explanations
- [ ] **Time interval downloads** try to find a workaround for FFMPEG needing to stream the old file to trim it

## Known Issues
- **Time interval latency**: Downloading a specific section of a video will take much longer than excpected
  - *Recommend either downloading the entire video, or only specifying a short section of the video*
  - *Processing adds ~50% of the clip duration to download time (e.g., a 1-hour clip takes an extra 30 minutes)*
- **Time interval progress**: No progress percentage due to yt-dlp logging limitations
- **Format compatibility**: Some quality/format combinations may not be available for all videos
- **Cross-platform capabilities**: This program was developed for Windows 11. It is not guaranteed to work on other platforms

## Technical Notes
- Uses yt-dlp for downloading and ffmpeg for processing
- PyInstaller for standalone executable creation
- Inno Setup for installer creation
- All dependencies are bundled (ffmpeg and yt-dlp) in the installer. Dependencies DO NOT need to be installed seperately on your machine
