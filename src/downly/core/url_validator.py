# =====
#
#   Downly URL Validator
#
#   Handles YouTube URL validation using configurable patterns.
#
# =====

import re
from typing import List
from ..config import YOUTUBE_PATTERNS


class URLValidator:
    """
    Validates YouTube URLs against predefined patterns.
    Provides extensible URL validation functionality.
    """
    
    def __init__(self, patterns: List[str] = None):
        """
        Initialize URL validator with patterns.
        
        Args:
            patterns: List of regex patterns to validate against. 
                     If None, uses default YouTube patterns.
        """
        self.patterns = patterns or YOUTUBE_PATTERNS
    
    def is_valid_youtube_url(self, url: str) -> bool:
        """
        Check if a URL matches any of the YouTube URL patterns.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if URL matches a YouTube pattern, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
            
        url = url.strip()
        if not url:
            return False
            
        return any(re.match(pattern, url, re.IGNORECASE) for pattern in self.patterns)
    
    def validate_url_input(self, url: str, placeholder: str = "Paste YouTube link here...") -> tuple[bool, str]:
        """
        Validate URL input including placeholder handling.
        
        Args:
            url: URL string to validate
            placeholder: Placeholder text to check against
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not url or url.strip() == placeholder:
            return False, "Please enter a YouTube URL before downloading."
        
        if not self.is_valid_youtube_url(url):
            error_msg = ("Please enter a valid YouTube URL.\n\n"
                        "Supported formats:\n"
                        "• youtube.com/watch?v=...\n"
                        "• youtu.be/...\n"
                        "• youtube.com/shorts/...\n"
                        "• youtube.com/playlist?list=...")
            return False, error_msg
        
        return True, ""
    
    def add_pattern(self, pattern: str) -> None:
        """
        Add a new URL pattern to the validator.
        
        Args:
            pattern: Regex pattern string to add
        """
        if pattern not in self.patterns:
            self.patterns.append(pattern)
    
    def remove_pattern(self, pattern: str) -> bool:
        """
        Remove a URL pattern from the validator.
        
        Args:
            pattern: Regex pattern string to remove
            
        Returns:
            True if pattern was removed, False if not found
        """
        try:
            self.patterns.remove(pattern)
            return True
        except ValueError:
            return False
