import subprocess
import os

def build():
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        
        # Use the virtual environment's PyInstaller
        pyinstaller_path = os.path.join(project_root, '.venv', 'Scripts', 'pyinstaller.exe')
        
        # Define the command to run PyInstaller
        command = [
                pyinstaller_path,
                # Specify the PyInstaller options
                '--onedir',
                '--windowed',
                '--icon=src/assets/icon.ico',
                'src/downly.py',
                # Add additional data files and binaries
                '--add-data', f'src/assets/icon.ico;assets',
                '--add-data', f'src/assets/logo.png;assets',
                '--add-binary', f'.venv/Scripts/ffmpeg.exe;.',
                '--add-binary', f'.venv/Scripts/yt-dlp.exe;.'
        ]

        # Run the command
        print("Building Downly with PyInstaller...")
        subprocess.run(command)
        print("Build completed.")

if __name__ == '__main__':
        build()