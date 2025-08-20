#!/usr/bin/env python3
"""
Complete build automation script for Downly
Builds the application and optionally creates the installer
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors gracefully."""
    print(f"\n{description}...")
    print(f"Command: {' '.join(command) if isinstance(command, list) else command}")
    
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check)
        else:
            result = subprocess.run(command, check=check)
        
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed with return code {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False
    except FileNotFoundError as e:
        print(f"✗ Command not found: {e}")
        return False

def main():
    """Main build automation function."""
    parser = argparse.ArgumentParser(description="Build Downly application")
    parser.add_argument("--installer", action="store_true", help="Also build the installer")
    parser.add_argument("--clean", action="store_true", help="Clean build directories first")
    parser.add_argument("--check-only", action="store_true", help="Only check dependencies")
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent.parent
    
    print("Downly Build Automation")
    print("=" * 40)
    
    # Check dependencies first
    print("\nStep 1: Checking dependencies...")
    dep_check = run_command([sys.executable, str(project_root / "scripts" / "dependencies" / "check_dependencies.py")], "Dependency check")
    if not dep_check:
        print("Please fix missing dependencies before building.")
        return False
    
    if args.check_only:
        print("\n✓ Dependency check complete. Ready to build!")
        return True
    
    # Clean build directories if requested
    if args.clean:
        print("\nStep 2: Cleaning build directories...")
        # Clean old directories
        old_dist_dir = project_root / "dist"
        old_build_dir = project_root / "build"
        # Clean new standardized directories
        build_output_dir = project_root / "build_output"
        
        for dir_path in [old_dist_dir, old_build_dir, build_output_dir]:
            if dir_path.exists():
                try:
                    import shutil
                    shutil.rmtree(dir_path)
                    print(f"✓ Cleaned {dir_path}")
                except Exception as e:
                    print(f"✗ Failed to clean {dir_path}: {e}")
    
    # Build the application
    print(f"\nStep {'3' if args.clean else '2'}: Building application...")
    build_success = run_command([sys.executable, str(project_root / "scripts" / "build" / "build.py")], "Application build")
    
    if not build_success:
        print("\n✗ Application build failed. Cannot proceed to installer.")
        return False
    
    # Check if build_output directory was created
    portable_exe = project_root / "build_output" / "portable" / "downly" / "downly.exe"
    if not portable_exe.exists():
        print(f"✗ Expected executable not found at {portable_exe}")
        return False
    
    print(f"✓ Application built successfully at {portable_exe}")
    
    # Build installer if requested
    if args.installer:
        step_num = '4' if args.clean else '3'
        print(f"\nStep {step_num}: Building installer...")
        installer_success = run_command([sys.executable, str(project_root / "scripts" / "installer" / "build_installer.py")], "Installer build")
        
        if installer_success:
            installer_output = project_root / "build_output" / "installer"
            if installer_output.exists():
                installer_files = list(installer_output.glob("*.exe"))
                if installer_files:
                    print(f"✓ Installer created: {installer_files[0]}")
                else:
                    print("⚠ Installer build reported success but no .exe found")
        else:
            print("✗ Installer build failed")
            return False
    
    # Summary
    print("\n" + "=" * 40)
    print("✓ Build process completed successfully!")
    print(f"Application: {portable_exe}")
    
    if args.installer:
        installer_output = project_root / "build_output" / "installer"
        installer_files = list(installer_output.glob("*.exe"))
        if installer_files:
            print(f"Installer: {installer_files[0]}")
    
    print("\nNext steps:")
    print("1. Test the application by running the executable")
    if args.installer:
        print("2. Test the installer on a clean system")
    else:
        print("2. Run with --installer flag to create installer")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
