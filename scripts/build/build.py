import subprocess
import os

def build():
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        
        # Use the virtual environment's PyInstaller
        pyinstaller_path = os.path.join(project_root, '.venv', 'Scripts', 'pyinstaller.exe')
        
        # Check if PyInstaller exists
        if not os.path.exists(pyinstaller_path):
                print(f"Error: PyInstaller not found at: {pyinstaller_path}")
                print("Please ensure the virtual environment is set up and PyInstaller is installed.")
                return False
        
        # Check if main script exists
        main_script = os.path.join(project_root, 'src', 'main.py')
        if not os.path.exists(main_script):
                print(f"Error: Main script not found at: {main_script}")
                return False
        
        # Check if required assets exist
        icon_path = os.path.join(project_root, 'src', 'assets', 'icon.ico')
        logo_path = os.path.join(project_root, 'src', 'assets', 'logo.png')
        ffmpeg_path = os.path.join(project_root, 'binaries', 'ffmpeg.exe')
        ytdlp_path = os.path.join(project_root, 'binaries', 'yt-dlp.exe')
        
        missing_files = []
        if not os.path.exists(icon_path):
                missing_files.append(f"Icon: {icon_path}")
        if not os.path.exists(logo_path):
                missing_files.append(f"Logo: {logo_path}")
        if not os.path.exists(ffmpeg_path):
                missing_files.append(f"ffmpeg: {ffmpeg_path}")
        if not os.path.exists(ytdlp_path):
                missing_files.append(f"yt-dlp: {ytdlp_path}")
        
        if missing_files:
                print("Error: Missing required files:")
                for file in missing_files:
                        print(f"  - {file}")
                if ffmpeg_path in [f.split(": ")[1] for f in missing_files]:
                        print("  Please ensure ffmpeg.exe is in the binaries/ folder")
                if ytdlp_path in [f.split(": ")[1] for f in missing_files]:
                        print("  Please ensure yt-dlp.exe is in the binaries/ folder")
                return False
        
        # Define the command to run PyInstaller
        command = [
                pyinstaller_path,
                # Specify the PyInstaller options
                '--onedir',
                '--windowed',
                '--noconfirm',
                '--icon=src/assets/icon.ico',
                '--name=downly',
                'src/main.py',
                # Add additional data files and binaries
                '--add-data', f'src/assets/icon.ico;assets',
                '--add-data', f'src/assets/logo.png;assets',
                '--add-binary', f'binaries/ffmpeg.exe;.',
                '--add-binary', f'binaries/yt-dlp.exe;.'
        ]

        # Run the command
        print("Building Downly with PyInstaller...")
        try:
                result = subprocess.run(command, check=True)
                print("Build completed successfully.")
                return True
        except subprocess.CalledProcessError as e:
                print(f"Build failed with error: {e}")
                return False
        except FileNotFoundError as e:
                print(f"PyInstaller not found: {e}")
                print("Make sure PyInstaller is installed in the virtual environment.")
                return False

if __name__ == '__main__':
        success = build()
        if not success:
                exit(1)