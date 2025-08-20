# =====
#
#   Downly Preset Manager
#
#   Handles preset configurations and application logic.
#
# =====

from typing import Dict, Any, Optional
from ..config import PRESETS


class PresetManager:
    """
    Manages preset configurations for download settings.
    Provides interface for applying and managing presets.
    """
    
    def __init__(self):
        """Initialize preset manager with default presets."""
        self.presets = PRESETS.copy()
    
    def get_preset(self, format_type: str, quality: str) -> Optional[Dict[str, Any]]:
        """
        Get preset configuration for given format and quality.
        
        Args:
            format_type: Format type ("Video", "Audio", etc.)
            quality: Quality level ("High", "Standard", "Low")
            
        Returns:
            Preset configuration dictionary or None if not found
        """
        return self.presets.get(format_type, {}).get(quality)
    
    def get_available_formats(self) -> list[str]:
        """
        Get list of available preset formats.
        
        Returns:
            List of format type strings
        """
        return list(self.presets.keys())
    
    def get_available_qualities(self, format_type: str) -> list[str]:
        """
        Get list of available qualities for a format type.
        
        Args:
            format_type: Format type to get qualities for
            
        Returns:
            List of quality strings
        """
        return list(self.presets.get(format_type, {}).keys())
    
    def add_preset(self, format_type: str, quality: str, config: Dict[str, Any]) -> None:
        """
        Add a new preset configuration.
        
        Args:
            format_type: Format type for the preset
            quality: Quality level for the preset
            config: Configuration dictionary
        """
        if format_type not in self.presets:
            self.presets[format_type] = {}
        self.presets[format_type][quality] = config.copy()
    
    def remove_preset(self, format_type: str, quality: str) -> bool:
        """
        Remove a preset configuration.
        
        Args:
            format_type: Format type of the preset
            quality: Quality level of the preset
            
        Returns:
            True if preset was removed, False if not found
        """
        if format_type in self.presets and quality in self.presets[format_type]:
            del self.presets[format_type][quality]
            # Remove format type if no qualities left
            if not self.presets[format_type]:
                del self.presets[format_type]
            return True
        return False
    
    def reset_to_defaults(self) -> None:
        """Reset presets to default configuration."""
        self.presets = PRESETS.copy()
