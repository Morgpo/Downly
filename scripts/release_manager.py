#!/usr/bin/env python3
"""
Release management script for Downly
Helps create standardized releases and manage build outputs
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def main():
    """Main release management function."""
    parser = argparse.ArgumentParser(description="Manage Downly releases")
    parser.add_argument("--list", action="store_true", help="List all available builds")
    parser.add_argument("--clean", action="store_true", help="Clean all build outputs")
    parser.add_argument("--copy-to-releases", action="store_true", help="Copy current builds to a releases folder")
    parser.add_argument("--version", type=str, help="Version tag for release copy")
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    build_output_dir = project_root / "build_output"
    portable_dir = build_output_dir / "portable"
    installer_dir = build_output_dir / "installer"
    releases_dir = project_root / "releases"
    
    print("Downly Release Management")
    print("=" * 40)
    
    if args.list:
        print("\nAvailable builds:")
        
        # Check portable builds
        if portable_dir.exists():
            portable_exe = portable_dir / "downly" / "downly.exe"
            if portable_exe.exists():
                stat = portable_exe.stat()
                size_mb = stat.st_size / (1024 * 1024)
                modified = datetime.fromtimestamp(stat.st_mtime)
                print(f"✓ Portable: {portable_exe} ({size_mb:.1f} MB, {modified.strftime('%Y-%m-%d %H:%M')})")
            else:
                print("✗ Portable: Not found")
        else:
            print("✗ Portable: Build directory not found")
        
        # Check installer builds
        if installer_dir.exists():
            installer_files = list(installer_dir.glob("*.exe"))
            if installer_files:
                for installer in installer_files:
                    stat = installer.stat()
                    size_mb = stat.st_size / (1024 * 1024)
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    print(f"✓ Installer: {installer.name} ({size_mb:.1f} MB, {modified.strftime('%Y-%m-%d %H:%M')})")
            else:
                print("✗ Installer: No installer files found")
        else:
            print("✗ Installer: Build directory not found")
        
        return True
    
    if args.clean:
        print("\nCleaning all build outputs...")
        
        if build_output_dir.exists():
            try:
                shutil.rmtree(build_output_dir)
                print(f"✓ Cleaned {build_output_dir}")
            except Exception as e:
                print(f"✗ Failed to clean {build_output_dir}: {e}")
                return False
        else:
            print("ℹ Build output directory doesn't exist")
        
        print("✓ All build outputs cleaned")
        return True
    
    if args.copy_to_releases:
        if not args.version:
            print("✗ Error: --version is required when using --copy-to-releases")
            print("Example: --copy-to-releases --version v0.3.1")
            return False
        
        version = args.version
        if not version.startswith('v'):
            version = f'v{version}'
        
        print(f"\nCreating release copy for {version}...")
        
        # Create releases directory structure
        version_dir = releases_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        
        # Copy portable build
        if portable_dir.exists():
            portable_exe = portable_dir / "downly" / "downly.exe"
            if portable_exe.exists():
                portable_release_name = f"Downly-{version}-Portable.exe"
                portable_dest = version_dir / portable_release_name
                try:
                    shutil.copy2(portable_exe, portable_dest)
                    print(f"✓ Copied portable: {portable_release_name}")
                    copied_files.append(portable_release_name)
                except Exception as e:
                    print(f"✗ Failed to copy portable: {e}")
            else:
                print("⚠ Portable build not found, skipping")
        
        # Copy installer build
        if installer_dir.exists():
            installer_files = list(installer_dir.glob("*.exe"))
            if installer_files:
                latest_installer = max(installer_files, key=lambda x: x.stat().st_mtime)
                installer_release_name = f"Downly-{version}-Setup.exe"
                installer_dest = version_dir / installer_release_name
                try:
                    shutil.copy2(latest_installer, installer_dest)
                    print(f"✓ Copied installer: {installer_release_name}")
                    copied_files.append(installer_release_name)
                except Exception as e:
                    print(f"✗ Failed to copy installer: {e}")
            else:
                print("⚠ Installer build not found, skipping")
        
        if copied_files:
            print(f"\n✓ Release {version} created successfully!")
            print(f"Location: {version_dir}")
            print("Files:")
            for file in copied_files:
                file_path = version_dir / file
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  - {file} ({size_mb:.1f} MB)")
            
            # Create a simple release info file
            info_file = version_dir / "release-info.txt"
            with open(info_file, 'w') as f:
                f.write(f"Downly Release {version}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Files: {len(copied_files)}\n\n")
                for file in copied_files:
                    file_path = version_dir / file
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    f.write(f"{file} ({size_mb:.1f} MB)\n")
            
            print(f"✓ Release info saved to: {info_file.name}")
            
        else:
            print("✗ No files were copied. Make sure builds exist first.")
            return False
        
        return True
    
    # Default action: show current status
    print("\nCurrent build status:")
    print(f"Build output directory: {build_output_dir}")
    print(f"Portable builds: {portable_dir}")
    print(f"Installer builds: {installer_dir}")
    
    if build_output_dir.exists():
        print("\nUse --list to see available builds")
        print("Use --copy-to-releases --version X.X.X to create a release")
        print("Use --clean to clean all build outputs")
    else:
        print("\nNo builds found. Run the build script first:")
        print("  python scripts/build/build_all.py --installer")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
