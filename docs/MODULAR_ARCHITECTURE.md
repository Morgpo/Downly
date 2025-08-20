# Downly - Modular Architecture

This document describes the modular architecture of the Downly YouTube downloader application.

## Architecture Overview

The application has been refactored from a monolithic structure into a clean, modular architecture that separates concerns and makes the codebase easier to maintain, extend, and debug.

## Directory Structure

```
src/
├── downly/                     # Main application package
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration and constants
│   ├── app.py                 # Main application class
│   ├── core/                  # Core business logic
│   │   ├── __init__.py
│   │   ├── dependency_manager.py    # External tool management
│   │   ├── url_validator.py         # URL validation logic
│   │   ├── download_engine.py       # Download processing
│   │   └── preset_manager.py        # Preset configurations
│   ├── ui/                    # User interface components
│   │   ├── __init__.py
│   │   ├── style_manager.py         # UI styling and themes
│   │   ├── header_component.py      # Application header
│   │   ├── url_input.py             # URL input widget
│   │   ├── settings_panel.py        # Settings configuration
│   │   └── progress_panel.py        # Progress and controls
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── time_utils.py            # Time and filename utilities
├── main.py                    # Application entry point
├── test_modular.py           # Architecture validation tests
└── assets/                   # Static resources
    ├── icon.ico
    └── logo.png
```

## Module Descriptions

### Core Modules (`downly/core/`)

#### `dependency_manager.py`
- **Purpose**: Manages external dependencies (ffmpeg, yt-dlp)
- **Key Features**:
  - Path resolution for bundled and development environments
  - Dependency validation and health checks
  - Caching for performance
  - Resource path management

#### `url_validator.py`
- **Purpose**: Validates YouTube URLs
- **Key Features**:
  - Configurable regex patterns
  - Support for multiple YouTube URL formats
  - Input validation with user-friendly error messages
  - Extensible pattern system

#### `download_engine.py`
- **Purpose**: Core download functionality
- **Key Features**:
  - yt-dlp command construction
  - Process management and monitoring
  - Progress tracking and callbacks
  - Format string generation
  - Error handling and cancellation

#### `preset_manager.py`
- **Purpose**: Manages download presets
- **Key Features**:
  - Preset configuration storage
  - Dynamic preset application
  - Extensible preset system
  - Default preset management

### UI Components (`downly/ui/`)

#### `style_manager.py`
- **Purpose**: Centralized UI styling
- **Key Features**:
  - Dark theme configuration
  - Consistent widget styling
  - Color palette management
  - Font configuration

#### `header_component.py`
- **Purpose**: Application header with logo and title
- **Key Features**:
  - Logo loading with fallback
  - Responsive layout
  - Error handling for missing assets

#### `url_input.py`
- **Purpose**: URL input with placeholder management
- **Key Features**:
  - Intelligent placeholder handling
  - Real-time validation feedback
  - Clean API for URL access

#### `settings_panel.py`
- **Purpose**: Download configuration interface
- **Key Features**:
  - Preset and custom mode switching
  - Form validation
  - File browser integration
  - Event handling for UI state

#### `progress_panel.py`
- **Purpose**: Download progress and controls
- **Key Features**:
  - Progress visualization
  - Download/cancel controls
  - Status message management
  - Animation handling

### Utilities (`downly/utils/`)

#### `time_utils.py`
- **Purpose**: Time and filename utilities
- **Key Features**:
  - Multiple time format support (HH:MM:SS, MM:SS, SS)
  - Time validation and conversion
  - Filename sanitization
  - Safe string processing

### Configuration (`downly/config.py`)

- **Purpose**: Centralized configuration
- **Key Features**:
  - Application constants
  - UI theme configuration
  - Preset definitions
  - YouTube URL patterns

### Main Application (`downly/app.py`)

- **Purpose**: Application orchestration
- **Key Features**:
  - Component initialization and coordination
  - Event handling and routing
  - Application lifecycle management
  - Dependency injection

## Key Benefits of Modular Architecture

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Business logic separated from UI components
- Configuration isolated from implementation

### 2. **Improved Maintainability**
- Smaller, focused modules are easier to understand
- Changes to one module don't affect unrelated functionality
- Clear interfaces between components

### 3. **Enhanced Testability**
- Individual modules can be tested in isolation
- Mock dependencies for unit testing
- Validation scripts for architecture testing

### 4. **Better Extensibility**
- New features can be added without modifying existing code
- Plugin-like architecture for UI components
- Configurable and extensible validation/processing

### 5. **Easier Debugging**
- Clear error isolation to specific modules
- Structured logging and error handling
- Component-level debugging capabilities

### 6. **Object-Oriented Design**
- Proper encapsulation of state and behavior
- Inheritance and composition where appropriate
- Clean interfaces and contracts

## Object-Oriented Principles Applied

### 1. **Encapsulation**
- Private methods and state in classes
- Clear public interfaces
- Information hiding for internal details

### 2. **Single Responsibility Principle**
- Each class has one reason to change
- Focused, cohesive functionality
- Clear separation of concerns

### 3. **Dependency Injection**
- Components receive dependencies rather than creating them
- Loose coupling between modules
- Easier testing and mocking

### 4. **Composition over Inheritance**
- UI components compose smaller pieces
- Managers coordinate multiple objects
- Flexible, runtime behavior configuration

## Usage Examples

### Running the Application
```bash
# From the src directory
python main.py
```

### Testing the Architecture
```bash
# Validate all modules work correctly
python test_modular.py
```

### Building the Application
```bash
# The build script automatically uses the new structure
python ../build_scripts/build.py
```

## Migration from Monolithic Structure

The original `downly.py` (1253 lines) has been broken down into:
- **13 focused modules** averaging ~200 lines each
- **Clear interfaces** between components
- **Testable units** with isolated functionality
- **Maintainable codebase** with logical organization

## Future Extensions

The modular architecture makes it easy to add:
- **New download sources** (by extending URL validation and download engine)
- **Additional UI themes** (by extending style manager)
- **Plugin system** (by leveraging the component architecture)
- **Configuration persistence** (by extending preset manager)
- **Advanced progress tracking** (by extending progress panel)

This architecture provides a solid foundation for future development while maintaining the existing functionality and user experience.
