# Migration Guide: Monolithic to Modular Architecture

This guide helps developers understand the transition from the original monolithic `downly.py` to the new modular architecture.

## Overview of Changes

The original 1253-line `downly.py` file has been restructured into 13 focused modules, each with a specific responsibility. The functionality remains identical, but the code is now much more maintainable and extensible.

## File Mapping

### Original Structure
```
src/
├── downly.py          # 1253 lines - everything
└── assets/
    ├── icon.ico
    └── logo.png
```

### New Structure
```
src/
├── main.py                           # Entry point (5 lines)
├── downly/                          # Main package
│   ├── config.py                    # Constants and configuration
│   ├── app.py                       # Main application orchestration
│   ├── core/                        # Business logic modules
│   │   ├── dependency_manager.py    # External tool management
│   │   ├── url_validator.py         # URL validation
│   │   ├── download_engine.py       # Download processing
│   │   └── preset_manager.py        # Preset management
│   ├── ui/                          # UI component modules
│   │   ├── style_manager.py         # Styling and themes
│   │   ├── header_component.py      # Header widget
│   │   ├── url_input.py             # URL input widget
│   │   ├── settings_panel.py        # Settings widgets
│   │   └── progress_panel.py        # Progress and controls
│   └── utils/                       # Utility modules
│       └── time_utils.py            # Time and filename utilities
└── test_modular.py                  # Architecture validation
```

## Code Migration Examples

### 1. Constants and Configuration

**Before (downly.py lines 23-55):**
```python
# Constants for audio quality mapping
AUDIO_QUALITY_MAP = {
    "Highest Audio Quality": "0",
    # ... rest of mapping
}

# YouTube URL patterns for validation
YOUTUBE_PATTERNS = [
    r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
    # ... rest of patterns
]

# Preset configurations
PRESETS = {
    "Video": {
        "High": {"format": "webm", ...},
        # ... rest of presets
    }
}
```

**After (downly/config.py):**
```python
# Now organized in a dedicated configuration module
# with classes for better organization

class ThemeConfig:
    PRIMARY_BG = "#1e1e1e"
    # ... theme configuration

class AppConfig:
    WINDOW_TITLE = "Downly - YouTube Downloader"
    # ... app configuration
```

### 2. Helper Functions → Dedicated Classes

**Before (downly.py lines 60-150):**
```python
def resource_path(relative_path):
    # Resource path resolution logic
    pass

def get_ffmpeg_path():
    # ffmpeg path resolution logic
    pass

def get_ytdlp_path():
    # yt-dlp path resolution logic
    pass

def validate_dependencies():
    # Dependency validation logic
    pass
```

**After (downly/core/dependency_manager.py):**
```python
class DependencyManager:
    def __init__(self):
        self._ffmpeg_path_cache = None
        self._ytdlp_path_cache = None
    
    def get_resource_path(self, relative_path: str) -> str:
        # Improved resource path resolution
        pass
    
    def get_ffmpeg_path(self) -> Optional[str]:
        # Cached ffmpeg path resolution
        pass
    
    def get_ytdlp_path(self) -> Optional[str]:
        # Cached yt-dlp path resolution
        pass
    
    def validate_dependencies(self) -> Tuple[bool, str]:
        # Enhanced dependency validation
        pass
```

### 3. Monolithic UI Class → Composed Components

**Before (downly.py lines 210-1200):**
```python
class CustomWindow(tk.Tk):
    def __init__(self):
        # Massive constructor with all UI setup
        # Header setup (50 lines)
        # URL input setup (20 lines)
        # Settings setup (200 lines)
        # Progress setup (30 lines)
        # Event binding (100 lines)
        # Style configuration (150 lines)
        pass
    
    def configure_styles(self):
        # 200 lines of style configuration
        pass
    
    def ytdlp_download(self):
        # 400 lines of download logic
        pass
    
    # ... 50+ more methods in one class
```

**After (downly/app.py + UI components):**
```python
class DownlyApplication(tk.Tk):
    def __init__(self):
        # Clean initialization with dependency injection
        self.dependency_manager = DependencyManager()
        self.url_validator = URLValidator()
        self.download_engine = DownloadEngine(self.dependency_manager)
        self.preset_manager = PresetManager()
        
        self._setup_window()
        self._setup_style()
        self._create_components()
        self._setup_callbacks()
    
    def _create_components(self):
        # Compose from focused components
        self.header_component = HeaderComponent(self.main_frame, self.dependency_manager)
        self.url_input = URLInput(self.main_frame)
        self.settings_panel = SettingsPanel(self.main_frame, self.preset_manager)
        self.progress_panel = ProgressPanel(self.main_frame)
```

### 4. Embedded Logic → Specialized Classes

**Before - Download logic embedded in UI class:**
```python
class CustomWindow(tk.Tk):
    def download_worker(self, url):
        # 300 lines of download logic mixed with UI updates
        # Command building
        # Process execution
        # Progress parsing
        # Error handling
        pass
```

**After - Separated into specialized classes:**
```python
# downly/core/download_engine.py
class DownloadEngine:
    def start_download(self, settings: DownloadSettings) -> bool:
        # Clean download orchestration
        pass
    
    def _download_worker(self, settings, ffmpeg_path, ytdlp_path, start_seconds, end_seconds):
        # Focused download execution
        pass

# downly/ui/progress_panel.py
class ProgressPanel:
    def set_progress(self, percent: float, status_line: str, is_audio: bool):
        # Focused progress display
        pass
```

## API Changes

### Entry Point Change

**Before:**
```bash
python src/downly.py
```

**After:**
```bash
python src/main.py
```

### Import Changes for Extensions

**Before - Everything in one module:**
```python
from downly import CustomWindow, validate_dependencies
```

**After - Focused imports:**
```python
from downly.app import DownlyApplication
from downly.core.dependency_manager import DependencyManager
from downly.core.download_engine import DownloadEngine
from downly.ui.settings_panel import SettingsPanel
```

### Build Script Changes

**Before:**
```python
'src/downly.py',  # Main script
```

**After:**
```python
'--name=downly',  # Explicit name
'src/main.py',    # New entry point
```

## Benefits Realized

### 1. **Maintainability**
- **Before**: 1253-line file was difficult to navigate and modify
- **After**: 13 focused modules, each under 300 lines

### 2. **Testability**
- **Before**: Testing required instantiating the entire UI
- **After**: Individual components can be tested in isolation

### 3. **Extensibility**
- **Before**: Adding features required modifying the monolithic class
- **After**: New features can be added as new modules or components

### 4. **Debugging**
- **Before**: Errors could originate from anywhere in 1253 lines
- **After**: Clear error isolation to specific modules

### 5. **Code Reuse**
- **Before**: Utility functions were embedded in the main class
- **After**: Utilities are standalone and reusable

## Testing the Migration

Run the validation script to ensure everything works:

```bash
cd src
python test_modular.py
```

This will:
- ✅ Test all module imports
- ✅ Validate core functionality
- ✅ Check dependency resolution
- ✅ Confirm API compatibility

## Backward Compatibility

The original `downly.py` is preserved for reference, but the new entry point is `main.py`. The application functionality remains identical - only the internal organization has changed.

## Future Development

With the modular architecture, future enhancements become much easier:

1. **New download sources**: Extend `URLValidator` and `DownloadEngine`
2. **UI themes**: Extend `StyleManager`
3. **Additional formats**: Extend `PresetManager`
4. **Advanced features**: Add new modules without touching existing code

The modular architecture provides a solid foundation for continued development while maintaining clean separation of concerns.
