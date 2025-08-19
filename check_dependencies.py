#!/usr/bin/env python3
"""
Dependency checker for Downly build process
Verifies all required files and tools are available before building.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(path, name):
    """Check if a file exists and report the result."""
    if os.path.exists(path):
        print(f"✓ {name}: Found at {path}")
        return True
    else:
        print(f"✗ {name}: Missing at {path}")
        return False

def check_executable(command, name):
    """Check if an executable is available in PATH."""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        print(f"✓ {name}: Available in PATH")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {name}: Not available in PATH")
        return False

def main():
    """Main dependency checking function."""
    print("Downly Build Dependencies Check")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    all_good = True
    
    # Check Python environment
    print(f"\nPython version: {sys.version}")
    venv_path = project_root / ".venv"
    if venv_path.exists():
        print(f"✓ Virtual environment: Found at {venv_path}")
    else:
        print(f"✗ Virtual environment: Missing at {venv_path}")
        all_good = False
    
    # Check required executables
    print("\nExecutables:")
    pyinstaller_path = project_root / ".venv" / "Scripts" / "pyinstaller.exe"
    all_good &= check_file_exists(pyinstaller_path, "PyInstaller")
    
    ytdlp_path = project_root / "binaries" / "yt-dlp.exe"
    all_good &= check_file_exists(ytdlp_path, "yt-dlp")
    
    ffmpeg_path = project_root / "binaries" / "ffmpeg.exe"
    all_good &= check_file_exists(ffmpeg_path, "ffmpeg")
    
    # Check source files
    print("\nSource files:")
    main_script = project_root / "src" / "downly.py"
    all_good &= check_file_exists(main_script, "Main script")
    
    icon_path = project_root / "src" / "assets" / "icon.ico"
    all_good &= check_file_exists(icon_path, "Icon")
    
    logo_path = project_root / "src" / "assets" / "logo.png"
    all_good &= check_file_exists(logo_path, "Logo")
    
    # Check build scripts
    print("\nBuild scripts:")
    build_script = project_root / "build_scripts" / "build.py"
    all_good &= check_file_exists(build_script, "Build script")
    
    installer_script = project_root / "installer" / "build_installer.py"
    all_good &= check_file_exists(installer_script, "Installer build script")
    
    iss_file = project_root / "installer" / "downly_installer.iss"
    all_good &= check_file_exists(iss_file, "Inno Setup script")
    
    # Check Inno Setup (if needed for installer)
    print("\nOptional tools:")
    issc_path = os.path.expanduser(r"~\Desktop\Coding\InnoSetup\ISCC.exe")
    check_file_exists(issc_path, "Inno Setup Compiler")
    
    # Summary
    print("\n" + "=" * 40)
    if all_good:
        print("✓ All required dependencies are available!")
        print("You can proceed with building the application.")
    else:
        print("✗ Some dependencies are missing.")
        print("Please install missing dependencies before building.")
        print("\nQuick setup commands:")
        print("1. Set up virtual environment: python setup/setup_venv.py")
        print("2. Ensure ffmpeg.exe is in binaries/ folder")
        print("3. Ensure yt-dlp.exe is in binaries/ folder")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
