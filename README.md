# Developer Checklist:
## Known Bugs
- Specifying an end time makes the download take exponentially longer than downloading the whole video
   - Same resolution, bitrate, etc
   - Video Duration is correct
   - Console output seems good, but it takes 6:35 to download 10 minutes; 16 minutes (full vid) took only 2 minutes

## Major Features to Add
- N/A

## Minor Features to Add
- Replace Title with an image
   - Maybe a play on the logo

# Notes:
- You can run the program without building the application, just activate the `./venv/` and `python ./src/downly.py`
- There is no percentage for downloading a section of the video - this is an issue with yt-dlp's console logging when passing the flag that specifies downloading a certain portion 
   - It does not show the percentage or the ETA, it show what time in the video is currently being converted which is different than what it usually does
- Run the build script from the main project folder
- Run the setup script from the setup folder

- `ffmpeg` and `yt-dlp` should be grouped into the application when building, but that needs to be double checked
