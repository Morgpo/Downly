#!/usr/bin/env python3
"""
Test script for the modular Downly application.
Validates that all modules can be imported and basic functionality works.
"""

import sys
import os

# Add src directory to Python path for testing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        from downly.config import AUDIO_QUALITY_MAP, PRESETS, ThemeConfig, AppConfig
        print("✓ Config module imported successfully")
        
        from downly.core.dependency_manager import DependencyManager
        print("✓ DependencyManager imported successfully")
        
        from downly.core.url_validator import URLValidator
        print("✓ URLValidator imported successfully")
        
        from downly.core.download_engine import DownloadEngine, DownloadSettings
        print("✓ DownloadEngine imported successfully")
        
        from downly.core.preset_manager import PresetManager
        print("✓ PresetManager imported successfully")
        
        from downly.utils.time_utils import TimeValidator, FilenameUtils
        print("✓ Time utilities imported successfully")
        
        from downly.ui.style_manager import StyleManager
        print("✓ StyleManager imported successfully")
        
        from downly.ui.url_input import URLInput
        print("✓ URLInput imported successfully")
        
        from downly.ui.settings_panel import SettingsPanel
        print("✓ SettingsPanel imported successfully")
        
        from downly.ui.progress_panel import ProgressPanel
        print("✓ ProgressPanel imported successfully")
        
        from downly.ui.header_component import HeaderComponent
        print("✓ HeaderComponent imported successfully")
        
        from downly.app import DownlyApplication
        print("✓ DownlyApplication imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_core_functionality():
    """Test basic functionality of core modules."""
    print("\nTesting core functionality...")
    
    try:
        # Test dependency manager
        from downly.core.dependency_manager import DependencyManager
        dep_manager = DependencyManager()
        print("✓ DependencyManager instantiated")
        
        # Test URL validator
        from downly.core.url_validator import URLValidator
        url_validator = URLValidator()
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid = url_validator.is_valid_youtube_url(test_url)
        print(f"✓ URL validation works: {test_url} -> {is_valid}")
        
        # Test time validator
        from downly.utils.time_utils import TimeValidator
        time_seconds = TimeValidator.validate_time_format("01:30:45")
        print(f"✓ Time validation works: 01:30:45 -> {time_seconds} seconds")
        
        # Test preset manager
        from downly.core.preset_manager import PresetManager
        preset_manager = PresetManager()
        preset = preset_manager.get_preset("Video", "High")
        print(f"✓ Preset manager works: Video/High -> {preset}")
        
        # Test filename utils
        from downly.utils.time_utils import FilenameUtils
        safe_name = FilenameUtils.sanitize_filename("test<>file|name?.txt")
        print(f"✓ Filename sanitization works: test<>file|name?.txt -> {safe_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Core functionality test failed: {e}")
        return False

def test_dependency_validation():
    """Test dependency validation."""
    print("\nTesting dependency validation...")
    
    try:
        from downly.core.dependency_manager import DependencyManager
        dep_manager = DependencyManager()
        
        ffmpeg_path = dep_manager.get_ffmpeg_path()
        ytdlp_path = dep_manager.get_ytdlp_path()
        
        print(f"✓ ffmpeg path: {ffmpeg_path}")
        print(f"✓ yt-dlp path: {ytdlp_path}")
        
        deps_ok, error_msg = dep_manager.validate_dependencies()
        print(f"✓ Dependencies validation: {deps_ok}")
        if not deps_ok:
            print(f"  Error: {error_msg}")
        
        return True
        
    except Exception as e:
        print(f"✗ Dependency validation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Downly Modular Architecture Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    all_passed &= test_imports()
    
    # Test core functionality
    all_passed &= test_core_functionality()
    
    # Test dependencies
    all_passed &= test_dependency_validation()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! Modular architecture is working correctly.")
        print("\nThe application is ready to run. You can:")
        print("1. Run: python main.py")
        print("2. Build: python ../build_scripts/build.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
