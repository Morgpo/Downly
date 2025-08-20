# =====
#
#   Downly Time Utilities
#
#   Handles time format validation and conversion for download time intervals.
#
# =====

import re
from typing import Optional, Union


class TimeValidator:
    """
    Handles time format validation and conversion.
    Supports multiple time formats: HH:MM:SS, MM:SS, and SS.
    """
    
    # Time format patterns
    PATTERNS = [
        r'^(\d{1,2}):(\d{2}):(\d{2})$',  # H:MM:SS or HH:MM:SS
        r'^(\d{1,2}):(\d{2})$',          # MM:SS
        r'^(\d+)$'                       # SS only
    ]
    
    @staticmethod
    def validate_time_format(time_str: str) -> Union[int, bool]:
        """
        Validate and convert time string to seconds.
        
        Args:
            time_str: Time string in format HH:MM:SS, MM:SS, or SS
            
        Returns:
            Number of seconds if valid, False if invalid, None if empty/placeholder
        """
        if not time_str or time_str.strip() == "" or time_str.strip() == "HH:MM:SS":
            return None

        time_str = time_str.strip()

        for pattern in TimeValidator.PATTERNS:
            match = re.match(pattern, time_str)
            if match:
                groups = match.groups()
                if len(groups) == 3:  # H:MM:SS or HH:MM:SS
                    hours, minutes, seconds = map(int, groups)
                    # Validate ranges
                    if minutes >= 60 or seconds >= 60:
                        return False
                    return hours * 3600 + minutes * 60 + seconds
                elif len(groups) == 2:  # MM:SS
                    minutes, seconds = map(int, groups)
                    # Validate ranges
                    if seconds >= 60:
                        return False
                    return minutes * 60 + seconds
                else:  # SS only
                    return int(groups[0])

        return False
    
    @staticmethod
    def format_seconds_to_time(seconds: int) -> str:
        """
        Convert seconds to HH:MM:SS format for yt-dlp.
        
        Args:
            seconds: Number of seconds to convert
            
        Returns:
            Time string in HH:MM:SS format
        """
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    @staticmethod
    def validate_time_interval(start_time: str, end_time: str, 
                             placeholder: str = "HH:MM:SS") -> tuple[Optional[int], Optional[int], Optional[str]]:
        """
        Validate a time interval (start and end times).
        
        Args:
            start_time: Start time string
            end_time: End time string
            placeholder: Placeholder text to check against
            
        Returns:
            Tuple of (start_seconds, end_seconds, error_message)
            start_seconds and end_seconds are None if not set, int if valid
            error_message is None if valid, string if error
        """
        start_seconds = None
        end_seconds = None
        
        # Validate start time
        if start_time and start_time not in ["", placeholder, "00:00:00"]:
            start_seconds = TimeValidator.validate_time_format(start_time)
            if start_seconds is False:
                return None, None, "Invalid start time format. Use HH:MM:SS (e.g., 01:30:00), MM:SS (e.g., 90:00), or SS (e.g., 54)"
        
        # Validate end time
        if end_time and end_time not in ["", placeholder]:
            end_seconds = TimeValidator.validate_time_format(end_time)
            if end_seconds is False:
                return None, None, "Invalid end time format. Use HH:MM:SS (e.g., 02:45:30), MM:SS (e.g., 15:30), or SS (e.g., 30)"
            
            if start_seconds is not None and end_seconds <= start_seconds:
                return None, None, "End time must be after start time"
        
        return start_seconds, end_seconds, None


class FilenameUtils:
    """Utility functions for filename handling."""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Remove invalid filename characters and handle special cases.
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Sanitized filename safe for file system
        """
        # Remove invalid filename characters
        invalid_chars = '<>:"/\\|?*'
        translation_table = str.maketrans('', '', invalid_chars)
        clean_name = filename.translate(translation_table)
        
        # Replace problematic characters with safe alternatives
        clean_name = clean_name.replace('–', '-')  # em dash to hyphen
        clean_name = clean_name.replace('—', '-')  # en dash to hyphen
        clean_name = clean_name.replace('"', "'")  # double quotes to single
        clean_name = clean_name.replace('…', '...')  # ellipsis
        
        # Remove multiple spaces and trim
        clean_name = ' '.join(clean_name.split())
        clean_name = clean_name.strip()
        
        # Ensure it's not empty and not too long
        if not clean_name:
            clean_name = "video"
        
        # Limit length to avoid filesystem issues
        if len(clean_name) > 200:
            clean_name = clean_name[:200].strip()
            
        return clean_name
