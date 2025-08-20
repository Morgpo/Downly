# =====
#
#   Downly Dependency Manager
#
#   Handles dependency validation and path resolution for external tools.
#
# =====

import os
import sys
import subprocess
from typing import Optional, Tuple


class DependencyManager:
    """
    Manages external dependencies (ffmpeg, yt-dlp) and their path resolution.
    Provides unified interface for locating and validating external tools.
    """
    
    def __init__(self):
        self._ffmpeg_path_cache: Optional[str] = None
        self._ytdlp_path_cache: Optional[str] = None
    
    def get_resource_path(self, relative_path: str) -> str:
        """
        Get absolute path to resource, handling both development and PyInstaller environments.
        
        Args:
            relative_path: Path relative to the application
            
        Returns:
            Absolute path to the resource
        """
        if relative_path.startswith("assets/"):
            # Assets are always relative to the script in development, or in _internal in bundled app
            if getattr(sys, 'frozen', False):
                # Running in PyInstaller bundle - assets are in _internal directory
                base_path = os.path.join(os.path.dirname(sys.executable), "_internal")
            else:
                # Development environment - assets are in src directory
                base_path = os.path.dirname(os.path.abspath(__file__))
                # Go up two levels from downly/core to src
                base_path = os.path.dirname(os.path.dirname(base_path))
        else:
            # Other resources use current directory as base
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def get_ffmpeg_path(self) -> Optional[str]:
        """
        Locate ffmpeg executable in various potential locations.
        
        Returns:
            Path to ffmpeg executable or None if not found
        """
        if self._ffmpeg_path_cache is not None:
            return self._ffmpeg_path_cache
            
        # Check bundled environment
        if getattr(sys, 'frozen', False):
            bundled_ffmpeg = os.path.join(os.path.dirname(sys.executable), "_internal", "ffmpeg.exe")
            if os.path.exists(bundled_ffmpeg):
                self._ffmpeg_path_cache = bundled_ffmpeg
                return bundled_ffmpeg
        else:
            # Development environment - check binaries folder
            current_file_path = os.path.abspath(__file__)
            # Go up from downly/core to src, then to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
            
            dev_ffmpeg_binaries = os.path.join(project_root, "binaries", "ffmpeg.exe")
            if os.path.exists(dev_ffmpeg_binaries):
                self._ffmpeg_path_cache = dev_ffmpeg_binaries
                return dev_ffmpeg_binaries
            
            # Check virtual environment
            dev_ffmpeg = os.path.join(project_root, ".venv", "Scripts", "ffmpeg.exe")
            if os.path.exists(dev_ffmpeg):
                self._ffmpeg_path_cache = dev_ffmpeg
                return dev_ffmpeg

        # Try various subdirectories as fallback
        for subdir in [".", "bin", "tools", "ffmpeg", "binaries"]:
            possible_path = self.get_resource_path(os.path.join(subdir, "ffmpeg.exe"))
            if os.path.exists(possible_path):
                self._ffmpeg_path_cache = possible_path
                return possible_path

        # Try system PATH
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            self._ffmpeg_path_cache = "ffmpeg"
            return "ffmpeg"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return None
    
    def get_ytdlp_path(self) -> Optional[str]:
        """
        Locate yt-dlp executable in various potential locations.
        
        Returns:
            Path to yt-dlp executable or None if not found
        """
        if self._ytdlp_path_cache is not None:
            return self._ytdlp_path_cache
            
        # Check bundled environment
        if getattr(sys, 'frozen', False):
            bundled_ytdlp = os.path.join(os.path.dirname(sys.executable), "_internal", "yt-dlp.exe")
            if os.path.exists(bundled_ytdlp):
                self._ytdlp_path_cache = bundled_ytdlp
                return bundled_ytdlp
        else:
            # Development environment - check binaries folder
            current_file_path = os.path.abspath(__file__)
            # Go up from downly/core to src, then to project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
            
            dev_ytdlp_binaries = os.path.join(project_root, "binaries", "yt-dlp.exe")
            if os.path.exists(dev_ytdlp_binaries):
                self._ytdlp_path_cache = dev_ytdlp_binaries
                return dev_ytdlp_binaries
            
            # Check virtual environment as fallback
            dev_ytdlp = os.path.join(project_root, ".venv", "Scripts", "yt-dlp.exe")
            if os.path.exists(dev_ytdlp):
                self._ytdlp_path_cache = dev_ytdlp
                return dev_ytdlp

        # Try to find yt-dlp in various subdirectories
        for subdir in [".", "bin", "tools", "yt-dlp", "binaries"]:
            possible_path = self.get_resource_path(os.path.join(subdir, "yt-dlp.exe"))
            if os.path.exists(possible_path):
                self._ytdlp_path_cache = possible_path
                return possible_path

        # Try system PATH
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
            self._ytdlp_path_cache = "yt-dlp"
            return "yt-dlp"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return None
    
    def validate_dependencies(self) -> Tuple[bool, str]:
        """
        Validate that all required dependencies are available and working.
        
        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            issues = []
            
            # Check ffmpeg
            ffmpeg_path = self.get_ffmpeg_path()
            if ffmpeg_path is None:
                issues.append("ffmpeg executable not found")
            else:
                try:
                    if ffmpeg_path == "ffmpeg":
                        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True, timeout=10, text=True)
                    else:
                        if not os.path.exists(ffmpeg_path):
                            issues.append("ffmpeg executable not found at expected location")
                        else:
                            result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, check=True, timeout=10, text=True)
                except subprocess.CalledProcessError as e:
                    issues.append(f"ffmpeg failed to run (exit code {e.returncode})")
                    if e.stderr:
                        issues.append(f"ffmpeg error: {e.stderr.strip()}")
                except FileNotFoundError:
                    issues.append("ffmpeg executable cannot be executed (missing dependencies)")
                except subprocess.TimeoutExpired:
                    issues.append("ffmpeg executable timed out")
                except Exception as e:
                    issues.append(f"ffmpeg test failed: {str(e)}")
            
            # Check yt-dlp
            ytdlp_path = self.get_ytdlp_path()
            if ytdlp_path is None:
                issues.append("yt-dlp executable not found")
            else:
                try:
                    if ytdlp_path == "yt-dlp":
                        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True, timeout=10, text=True)
                    else:
                        if not os.path.exists(ytdlp_path):
                            issues.append("yt-dlp executable not found at expected location")
                        else:
                            result = subprocess.run([ytdlp_path, "--version"], capture_output=True, check=True, timeout=10, text=True)
                except subprocess.CalledProcessError as e:
                    issues.append(f"yt-dlp failed to run (exit code {e.returncode})")
                    if e.stderr:
                        issues.append(f"yt-dlp error: {e.stderr.strip()}")
                except FileNotFoundError:
                    issues.append("yt-dlp executable cannot be executed (missing dependencies)")
                except subprocess.TimeoutExpired:
                    issues.append("yt-dlp executable timed out")
                except Exception as e:
                    issues.append(f"yt-dlp test failed: {str(e)}")
            
            if issues:
                error_msg = "\n".join([f"• {issue}" for issue in issues])
                error_msg += "\n\nThis usually indicates missing system dependencies."
                error_msg += "\nTry installing Microsoft Visual C++ Redistributable if not already installed."
                return False, error_msg
            
            return True, ""
            
        except Exception as e:
            return False, f"Dependency validation failed: {str(e)}"
    
    def clear_cache(self) -> None:
        """Clear cached paths (useful for testing or after system changes)."""
        self._ffmpeg_path_cache = None
        self._ytdlp_path_cache = None
