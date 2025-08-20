# =====
#
#   Downly Download Engine
#
#   Core download functionality with command building and process management.
#
# =====

import os
import subprocess
import threading
import queue
import time
import re
from typing import Optional, List, Callable, Dict, Any
from ..config import AUDIO_QUALITY_MAP, AppConfig
from ..core.dependency_manager import DependencyManager
from ..utils.time_utils import TimeValidator, FilenameUtils


class DownloadSettings:
    """Data class to hold download configuration settings."""
    
    def __init__(self):
        self.url: str = ""
        self.format: str = "mp4"
        self.video_quality: str = "Highest Video Quality"
        self.audio_quality: str = "Highest Audio Quality"
        self.download_location: str = ""
        self.custom_filename: str = ""
        self.start_time: str = ""
        self.end_time: str = ""
        self.download_metadata: bool = False
        self.download_subtitles: bool = False


class DownloadEngine:
    """
    Core download engine that handles yt-dlp command construction and execution.
    Manages download processes and provides callbacks for progress updates.
    """
    
    def __init__(self, dependency_manager: DependencyManager):
        """
        Initialize download engine.
        
        Args:
            dependency_manager: Dependency manager instance for tool paths
        """
        self.dependency_manager = dependency_manager
        self.download_process: Optional[subprocess.Popen] = None
        self.download_thread: Optional[threading.Thread] = None
        self.is_downloading: bool = False
        
        # Callbacks for UI updates
        self.on_progress: Optional[Callable[[float, str, bool], None]] = None
        self.on_success: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
        self.on_status_update: Optional[Callable[[str], None]] = None
    
    def set_callbacks(self, on_progress: Callable = None, on_success: Callable = None,
                     on_error: Callable = None, on_status_update: Callable = None) -> None:
        """
        Set callback functions for download events.
        
        Args:
            on_progress: Called with (percent, status_line, is_audio)
            on_success: Called when download completes successfully
            on_error: Called with error message string
            on_status_update: Called with status string updates
        """
        self.on_progress = on_progress
        self.on_success = on_success
        self.on_error = on_error
        self.on_status_update = on_status_update
    
    def start_download(self, settings: DownloadSettings) -> bool:
        """
        Start download with given settings.
        
        Args:
            settings: Download configuration
            
        Returns:
            True if download started successfully, False otherwise
        """
        if self.is_downloading:
            return False
        
        # Validate dependencies
        ffmpeg_path = self.dependency_manager.get_ffmpeg_path()
        ytdlp_path = self.dependency_manager.get_ytdlp_path()
        
        if ytdlp_path is None or ffmpeg_path is None:
            if self.on_error:
                self.on_error("Required dependencies not found. Please restart the application.")
            return False
        
        # Validate time interval
        start_seconds, end_seconds, time_error = TimeValidator.validate_time_interval(
            settings.start_time, settings.end_time
        )
        
        if time_error:
            if self.on_error:
                self.on_error(time_error)
            return False
        
        # Start download thread
        self.is_downloading = True
        self.download_thread = threading.Thread(
            target=self._download_worker_with_fallback, 
            args=(settings, ffmpeg_path, ytdlp_path, start_seconds, end_seconds)
        )
        self.download_thread.daemon = True
        self.download_thread.start()
        
        return True
    
    def cancel_download(self) -> None:
        """Cancel the current download process."""
        if not self.is_downloading:
            return
        
        try:
            # Set cancellation flag first
            self.is_downloading = False
            
            # Schedule process termination on background thread
            def terminate_process():
                try:
                    if self.download_process and self.download_process.poll() is None:
                        self.download_process.terminate()
                        
                        # Wait for graceful termination
                        for _ in range(10):  # Wait up to 1 second
                            if self.download_process.poll() is not None:
                                break
                            time.sleep(0.1)
                        
                        # Force kill if still running
                        if self.download_process.poll() is None:
                            self.download_process.kill()
                except Exception as e:
                    print(f"Error terminating process: {e}")
            
            # Start termination in background thread
            termination_thread = threading.Thread(target=terminate_process)
            termination_thread.daemon = True
            termination_thread.start()
            
        except Exception as e:
            print(f"Error cancelling download: {e}")
    
    def _download_worker(self, settings: DownloadSettings, ffmpeg_path: str, 
                        ytdlp_path: str, start_seconds: Optional[int], 
                        end_seconds: Optional[int]) -> None:
        """
        Background worker thread for download execution.
        
        Args:
            settings: Download configuration
            ffmpeg_path: Path to ffmpeg executable
            ytdlp_path: Path to yt-dlp executable
            start_seconds: Start time in seconds (None if not set)
            end_seconds: End time in seconds (None if not set)
        """
        try:
            # Build command
            command = self._build_command(settings, ffmpeg_path, ytdlp_path, start_seconds, end_seconds)
            print("yt-dlp command:", " ".join(command))
            
            # Execute download
            self._execute_download(command, settings.format in ["mp3", "m4a"], start_seconds, end_seconds)
            
        except Exception as e:
            if self.on_error:
                self.on_error(f"Unexpected error: {str(e)}")
        finally:
            # Ensure process cleanup
            if hasattr(self, 'download_process') and self.download_process:
                try:
                    if self.download_process.poll() is None:
                        self.download_process.terminate()
                        self.download_process.wait(timeout=AppConfig.CANCELLATION_TIMEOUT)
                except Exception:
                    pass
    
    def _download_worker_with_fallback(self, settings: DownloadSettings, ffmpeg_path: str, 
                                     ytdlp_path: str, start_seconds: Optional[int], 
                                     end_seconds: Optional[int]) -> None:
        """
        Background worker thread with format fallback mechanism.
        
        Args:
            settings: Download configuration
            ffmpeg_path: Path to ffmpeg executable
            ytdlp_path: Path to yt-dlp executable
            start_seconds: Start time in seconds (None if not set)
            end_seconds: End time in seconds (None if not set)
        """
        try:
            # Try with original format first
            command = self._build_command(settings, ffmpeg_path, ytdlp_path, start_seconds, end_seconds)
            print("yt-dlp command:", " ".join(command))
            
            # Execute download
            success = self._execute_download_safe(command, settings.format in ["mp3", "m4a"], start_seconds, end_seconds)
            
            # If failed and format was webm, try with mp4 fallback
            if not success and settings.format == "webm" and not (settings.format in ["mp3", "m4a"]):
                if self.on_status_update:
                    self.on_status_update("Retrying with MP4 format...")
                
                # Create fallback settings with MP4
                fallback_settings = DownloadSettings()
                fallback_settings.__dict__.update(settings.__dict__)
                fallback_settings.format = "mp4"
                
                fallback_command = self._build_command(fallback_settings, ffmpeg_path, ytdlp_path, start_seconds, end_seconds)
                print("yt-dlp fallback command:", " ".join(fallback_command))
                
                self._execute_download_safe(fallback_command, False, start_seconds, end_seconds)
            
        except Exception as e:
            if self.on_error:
                self.on_error(f"Unexpected error: {str(e)}")
        finally:
            # Ensure process cleanup
            if hasattr(self, 'download_process') and self.download_process:
                try:
                    if self.download_process.poll() is None:
                        self.download_process.terminate()
                        self.download_process.wait(timeout=AppConfig.CANCELLATION_TIMEOUT)
                except Exception:
                    pass
    
    def _build_command(self, settings: DownloadSettings, ffmpeg_path: str, 
                      ytdlp_path: str, start_seconds: Optional[int], 
                      end_seconds: Optional[int]) -> List[str]:
        """
        Build yt-dlp command from settings.
        
        Args:
            settings: Download configuration
            ffmpeg_path: Path to ffmpeg executable
            ytdlp_path: Path to yt-dlp executable
            start_seconds: Start time in seconds
            end_seconds: End time in seconds
            
        Returns:
            Complete command list for subprocess
        """
        downloads_folder = settings.download_location or os.path.join(os.path.expanduser("~"), AppConfig.DEFAULT_DOWNLOAD_LOCATION)
        
        # Build base command
        command = [
            ytdlp_path,
            "-P", downloads_folder,
            "--ffmpeg-location", ffmpeg_path,
            "--progress",
            "--no-part",
            "--no-overwrites",
            
            # Network and reliability flags
            "--retries", str(AppConfig.DOWNLOAD_RETRIES),
            "--fragment-retries", str(AppConfig.FRAGMENT_RETRIES),
            "--retry-sleep", str(AppConfig.RETRY_SLEEP),
            "--socket-timeout", str(AppConfig.SOCKET_TIMEOUT),
            
            # User agent and rate limiting
            "--sleep-interval", str(AppConfig.SLEEP_INTERVAL),
            "--max-sleep-interval", str(AppConfig.MAX_SLEEP_INTERVAL),
            
            # Error handling and logging
            "--no-warnings",
            "--ignore-errors",
            "--abort-on-unavailable-fragment",
            
        # Add format selection safety
        "--check-formats",
        
        # Add format merging safety flags
        "--no-post-overwrites",
        "--prefer-ffmpeg",
        
        # Security and safety
        "--geo-bypass",
        "--no-check-certificate",            # Performance optimization
            "--concurrent-fragments", str(AppConfig.CONCURRENT_FRAGMENTS),
            "--buffer-size", AppConfig.BUFFER_SIZE
        ]
        
        # Add metadata options
        if settings.download_metadata:
            command.extend([
                "--write-info-json",
                "--write-description",
                "--write-thumbnail",
                "--embed-metadata"
            ])
        else:
            command.extend([
                "--no-write-info-json",
                "--no-write-description",
                "--no-write-thumbnail"
            ])
        
        # Add subtitle options
        if settings.download_subtitles:
            command.extend([
                "--write-subs",
                "--write-auto-subs",
                "--embed-subs"
            ])
        
        # Configure format options
        is_audio_download = settings.format in ["mp3", "m4a"]
        self._add_format_options(command, settings, is_audio_download, start_seconds, end_seconds)
        
        # Configure output filename
        if settings.custom_filename:
            safe_filename = FilenameUtils.sanitize_filename(settings.custom_filename)
            command.extend(["-o", f"{safe_filename}.%(ext)s"])
        else:
            # Use a safer default filename template
            command.extend(["-o", "%(title)s.%(ext)s", "--restrict-filenames"])
        
        command.append(settings.url)
        return command
    
    def _execute_download_safe(self, command: List[str], is_audio_download: bool, 
                              start_seconds: Optional[int], end_seconds: Optional[int]) -> bool:
        """
        Execute download with error handling and return success status.
        
        Args:
            command: Command to execute
            is_audio_download: Whether this is an audio download
            start_seconds: Start time in seconds
            end_seconds: End time in seconds
            
        Returns:
            True if download succeeded, False otherwise
        """
        try:
            self._execute_download(command, is_audio_download, start_seconds, end_seconds)
            return True
        except Exception as e:
            print(f"Download attempt failed: {str(e)}")
            return False
    
    def _add_format_options(self, command: List[str], settings: DownloadSettings, 
                           is_audio_download: bool, start_seconds: Optional[int], 
                           end_seconds: Optional[int]) -> None:
        """
        Add format-specific options to command.
        
        Args:
            command: Command list to modify
            settings: Download configuration
            is_audio_download: Whether this is an audio-only download
            start_seconds: Start time in seconds
            end_seconds: End time in seconds
        """
        # Handle time-sectioned downloads
        if start_seconds is not None or end_seconds is not None:
            if is_audio_download:
                # For audio with time trimming, prefer M4A/AAC source
                command.extend(["-f", "bestaudio[ext=m4a]/bestaudio[acodec^=mp4a]/bestaudio[container^=mp4]/bestaudio/best"])
                command.extend(["--extract-audio", "--audio-format", settings.format])
                self._add_audio_quality_option(command, settings.audio_quality)
            else:
                # Force MP4 format for time-sectioned downloads
                format_str = self._get_time_section_format_string("mp4", settings.video_quality)
                command.extend(["-f", format_str])
                command.extend(["--merge-output-format", "mp4"])
                command.extend(["--remux-video", "mp4"])
                # Ensure AAC audio for MP4 compatibility
                command.extend(["--postprocessor-args", "ffmpeg:-c:a aac -b:a 192k"])
                self._add_audio_quality_option(command, settings.audio_quality)
            
            # Add download sections
            self._add_time_sections(command, start_seconds, end_seconds)
        else:
            # Handle full downloads
            if is_audio_download:
                command.extend(["-f", "bestaudio/best", "--extract-audio", "--audio-format", settings.format])
                self._add_audio_quality_option(command, settings.audio_quality)
            else:
                # Use simplified format selection for video downloads
                if settings.video_quality == "Highest Video Quality":
                    # Use format selection that ensures codec compatibility
                    if settings.format == "mp4":
                        # For MP4, prefer AAC audio for better compatibility
                        command.extend(["-f", "bestvideo*[ext=mp4]+bestaudio[ext=m4a]/bestvideo*+bestaudio[ext=m4a]/bestvideo*+bestaudio/best"])
                        command.extend(["--merge-output-format", "mp4"])
                        command.extend(["--remux-video", "mp4"])
                        # Ensure AAC audio for MP4 compatibility
                        command.extend(["--postprocessor-args", "ffmpeg:-c:a aac -b:a 192k"])
                    elif settings.format == "webm":
                        # For WebM, Opus audio is fine
                        command.extend(["-f", "bestvideo*+bestaudio/best"])
                        command.extend(["--merge-output-format", "webm"])
                    else:
                        # For other formats, let yt-dlp choose the best completely
                        # Don't specify -f at all to use yt-dlp's default behavior
                        pass
                else:
                    # Use specific quality selection for non-highest quality
                    format_str = self._get_video_format_string(settings.format, settings.video_quality)
                    command.extend(["-f", format_str])
                    
                    # Add format-specific merging options
                    if settings.format == "mp4":
                        command.extend(["--merge-output-format", "mp4"])
                        command.extend(["--remux-video", "mp4"])
                        # Ensure AAC audio for MP4 compatibility
                        command.extend(["--postprocessor-args", "ffmpeg:-c:a aac -b:a 192k"])
                    elif settings.format == "webm":
                        command.extend(["--merge-output-format", "webm"])
                        # Add webm-specific flags for better compatibility
                        command.extend(["--postprocessor-args", "ffmpeg:-c:v libvpx-vp9 -c:a libopus"])
                
                self._add_audio_quality_option(command, settings.audio_quality)
    
    def _add_audio_quality_option(self, command: List[str], audio_quality: str) -> None:
        """Add audio quality parameter to command if not using highest quality."""
        if audio_quality != "Highest Audio Quality":
            quality_value = AUDIO_QUALITY_MAP.get(audio_quality, "0")
            command.extend(["--audio-quality", quality_value])
    
    def _add_time_sections(self, command: List[str], start_seconds: Optional[int], 
                          end_seconds: Optional[int]) -> None:
        """Add time section parameters to command."""
        if start_seconds is not None and end_seconds is not None:
            start_formatted = TimeValidator.format_seconds_to_time(start_seconds)
            end_formatted = TimeValidator.format_seconds_to_time(end_seconds)
            command.extend(["--download-sections", f"*{start_formatted}-{end_formatted}"])
        elif start_seconds is not None:
            start_formatted = TimeValidator.format_seconds_to_time(start_seconds)
            command.extend(["--download-sections", f"*{start_formatted}-inf"])
        elif end_seconds is not None:
            end_formatted = TimeValidator.format_seconds_to_time(end_seconds)
            command.extend(["--download-sections", f"*0-{end_formatted}"])
    
    def _get_time_section_format_string(self, video_format: str, quality_selection: str) -> str:
        """Generate optimized format string for time-sectioned downloads."""
        if quality_selection == "Highest Video Quality":
            # Use codec-compatible format selection for time sections
            if video_format == "mp4":
                return "bestvideo*[ext=mp4]+bestaudio[ext=m4a]/bestvideo*+bestaudio[ext=m4a]/bestvideo*+bestaudio/best"
            else:
                return "bestvideo*+bestaudio/best"
        else:
            height = quality_selection.replace('p', '')
            if video_format == "mp4":
                return f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
            else:
                return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
    
    def _get_video_format_string(self, video_format: str, quality_selection: str) -> str:
        """Generate format string for standard video downloads."""
        if quality_selection == "Highest Video Quality":
            # Use codec-aware format selection for better compatibility
            if video_format == "mp4":
                return "bestvideo*[ext=mp4]+bestaudio[ext=m4a]/bestvideo*+bestaudio[ext=m4a]/bestvideo*+bestaudio/best"
            elif video_format == "webm":
                return "bestvideo*+bestaudio/best"
            else:
                return "bestvideo*+bestaudio/best"
        else:
            height = quality_selection.replace('p', '')
            if video_format == "mp4":
                return f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]"
            elif video_format == "webm":
                return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
            else:
                return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
    
    def _execute_download(self, command: List[str], is_audio_download: bool, 
                         start_seconds: Optional[int], end_seconds: Optional[int]) -> None:
        """
        Execute the download command and handle output.
        
        Args:
            command: Command to execute
            is_audio_download: Whether this is an audio download
            start_seconds: Start time in seconds
            end_seconds: End time in seconds
        """
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            self.download_process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True, 
                startupinfo=startupinfo, 
                bufsize=1, 
                universal_newlines=True
            )

            if self.on_status_update:
                self.on_status_update("Starting download...")

            # Create queue for output processing
            output_queue = queue.Queue()
            
            def read_output():
                try:
                    for line in iter(self.download_process.stdout.readline, ''):
                        if line:
                            output_queue.put(line)
                        if self.download_process.poll() is not None:
                            break
                except:
                    pass
                finally:
                    output_queue.put(None)  # Signal end
            
            # Start output reading thread
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()
            
            # Process lines with cancellation checks
            while self.download_process.poll() is None:
                if not self.is_downloading:
                    break
                
                try:
                    line = output_queue.get(timeout=0.1)
                    if line is None:  # End signal
                        break
                    line = line.strip()
                    if line:
                        print(f"yt-dlp output: {line}")
                        self._process_download_line(line, is_audio_download, start_seconds, end_seconds)
                except queue.Empty:
                    continue

            # Check if download was cancelled
            if not self.is_downloading:
                return
                
            self.download_process.wait()
            if self.download_process.returncode == 0:
                if self.on_success:
                    self.on_success()
            else:
                error_msg = f"Download failed with return code {self.download_process.returncode}"
                if self.on_error:
                    self.on_error(error_msg)

        except subprocess.CalledProcessError as e:
            error_msg = f"Download failed (exit code {e.returncode})"
            if hasattr(e, 'stderr') and e.stderr:
                error_msg += f": {e.stderr.strip()}"
            if self.on_error:
                self.on_error(error_msg)
        except FileNotFoundError as e:
            if self.on_error:
                self.on_error(f"yt-dlp executable not found: {str(e)}")
        except Exception as e:
            if self.on_error:
                self.on_error(f"Unexpected error: {str(e)}")
    
    def _process_download_line(self, line: str, is_audio_download: bool, 
                             start_seconds: Optional[int], end_seconds: Optional[int]) -> None:
        """Process a single line of output from yt-dlp."""
        if '[download]' in line:
            try:
                percent_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                if percent_match:
                    percent = float(percent_match.group(1))
                    if self.on_progress:
                        self.on_progress(percent, line, is_audio_download)
                elif "ETA" in line:
                    eta_match = re.search(r'(\d+\.\d+)% of', line)
                    if eta_match:
                        percent = float(eta_match.group(1))
                        if self.on_progress:
                            self.on_progress(percent, line, is_audio_download)
                elif "Destination" in line:
                    if self.on_status_update:
                        self.on_status_update("Preparing file...")
                elif "Resuming" in line:
                    if self.on_status_update:
                        self.on_status_update("Resuming download...")
            except Exception as e:
                print(f"Progress parsing error: {e} on line: {line}")

        elif line.startswith("frame=") or "ffmpeg" in line.lower():
            if start_seconds is not None or end_seconds is not None:
                if self.on_status_update:
                    self.on_status_update("Trimming video...")
            else:
                if self.on_status_update:
                    self.on_status_update("Processing video...")
            if self.on_progress:
                self.on_progress(90, line, is_audio_download)

        elif "Merging" in line or "merger" in line.lower():
            if self.on_status_update:
                self.on_status_update("Merging audio and video...")
            if self.on_progress:
                self.on_progress(95, line, is_audio_download)

        elif "ERROR:" in line.upper():
            if "conversion failed" in line.lower() or "merger" in line.lower():
                if self.on_status_update:
                    self.on_status_update("Format conversion error detected...")
            # Let the main error handling deal with the actual error
