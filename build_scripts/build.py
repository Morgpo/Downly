import subprocess

def build():
        # Define the command to run PyInstaller
        command = [
                'pyinstaller',
                # Specify the PyInstaller options
                '--onefile',
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