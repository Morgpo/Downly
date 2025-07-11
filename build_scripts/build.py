import os
import sys
import subprocess

def build():
    # Handle path separator for different platforms
    separator = ';' if os.name == 'nt' else ':'
    
    # Define the command to run PyInstaller
    command = [
        'pyinstaller',
        '--onefile',  # Create a single executable
        '--windowed',  # No console window
        '--icon=src/assets/icon.ico',  # Application icon
        'src/downly.py',  # Main application script
        '--add-data', f'src/utils/resource_path.py{separator}utils',  # Include resource_path
        '--add-data', f'src/assets/icon.ico{separator}assets',  # Include icon
        # Add ffmpeg binary to the distribution
        '--add-binary', f'.venv/Scripts/ffmpeg.exe{separator}.',  # Include ffmpeg.exe in root directory
    ]

    # Run the command
    print("Building Downly with PyInstaller...")
    subprocess.run(command)
    print("Build completed.")

if __name__ == '__main__':
    build()