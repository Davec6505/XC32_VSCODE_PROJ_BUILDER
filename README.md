# PIC32MZ VS Code Project Generator

This repository contains cross-platform scripts to generate PIC32MZ embedded projects compatible with the XC32 compiler toolchain and VS Code development environment.

## Features

- **Smart Generator Selection**: Automatically chooses the best available generator
- **Cross-Platform Support**: C#, Python, Shell script, and Windows Batch implementations
- **XC32 Integration**: Configured for Microchip's PIC32MZ toolchain v4.60+
- **VS Code Ready**: Includes `.vscode` configuration for debugging and building
- **GNU Make Build System**: Cross-platform Makefiles with proper dependency handling
- **Device Support**: Configurable for different PIC32MZ variants
- **Debug Configuration**: Pre-configured for PICkit 4, Snap, and ICD4 debuggers

## Quick Start

Simply run the main generator with your project name:

```cmd
generate_project.cmd MyProject
```

The script will automatically detect and use the best available generator on your system.

## Requirements

### XC32 Compiler Toolchain
- XC32 Compiler v4.60 or later
- GNU Make utility
- Microchip debugger (PICkit 4, Snap, or ICD4)

### Generator Runtime (Auto-detected)
- **Preferred**: .NET SDK 6.0+ (for C# generator)
- **Fallback**: Python 3.6+ (for Python generator)
- **Alternative**: Bash environment (for shell script)

## Usage

### Main Generator (Recommended)
```cmd
# Basic usage - creates project in current directory
generate_project.cmd MyProject

# With custom device
generate_project.cmd MyProject 32MZ2048EFH064

# With custom root directory
generate_project.cmd MyProject 32MZ1024EFH064 C:\Projects

# With MikroC compatibility
generate_project.cmd MyProject 32MZ1024EFH064 C:\Projects mikroc
```

### Direct Generator Usage
You can also run the generators directly if needed:

#### C# Generator (Preferred)
```cmd
# Requires .NET SDK 6.0+
dotnet run --project csharp\generate_project.csproj -- MyProject [device] [root_dir] [mikroc]
```

#### Python Generator
```bash
# Requires Python 3.6+
python generate_project.py MyProject [device] [root_dir] [mikroc]
```

#### Shell Script Generator
```bash
# Linux/macOS/WSL
./generate_project.sh MyProject [device] [root_dir] [mikroc]
```

#### Windows Batch Generator
```cmd
# Windows Command Prompt
generate_project.bat MyProject [device] [root_dir] [mikroc]
```

## Generated Project Structure

All generators create the same professional project structure:

```
MyProject/
├── Makefile                 # Root build configuration
├── .gitignore              # Git ignore rules
├── .vscode/
│   ├── tasks.json          # VS Code build tasks
│   ├── launch.json         # Debug configuration
│   └── c_cpp_properties.json # IntelliSense settings
├── srcs/
│   ├── Makefile            # Source build rules
│   ├── main.c              # Application entry point
│   └── startup/            # (MikroC option only)
│       ├── crt0.c          # C runtime startup
│       └── startup.S       # Assembly startup
├── incs/                   # Header files directory
├── objs/                   # Object files (build artifacts)
├── bins/                   # Binary outputs
├── other/                  # Other build artifacts
└── docs/                   # Documentation
```

## Building Projects

After project generation:

### VS Code Integration
1. Open the project folder in VS Code
2. Use **Ctrl+Shift+P** → "Tasks: Run Task"
3. Select from available tasks:
   - **makemake**: Build the project
   - **makeclean**: Clean build artifacts
   - **Flash**: Program device
   - **Test**: Run tests

### Command Line
```bash
cd path/to/MyProject
make                    # Build the project
make clean              # Clean build artifacts
make flash              # Flash to device
make test               # Run tests
```

## Device Support

Supported PIC32MZ devices (default: 32MZ1024EFH064):
- 32MZ1024EFH064
- 32MZ2048EFH064  
- 32MZ1024EFG064
- 32MZ2048EFG064
- And other PIC32MZ-EF family devices

## VS Code Features

Generated projects include:
- **IntelliSense**: Full code completion and syntax highlighting
- **Debugging**: Hardware debugger integration (PICkit 4, Snap, ICD4)
- **Build Integration**: One-click building via tasks
- **Error Navigation**: Click to jump to compiler errors
- **Git Integration**: Pre-configured .gitignore

## Installation

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd XC32_VSCODE_PROJ_BUILDER
   ```

2. **Install Prerequisites**:
   - Install XC32 Compiler v4.60+
   - Install .NET SDK 6.0+ (recommended) or Python 3.6+
   - Ensure `make` is available in PATH

3. **Generate your first project**:
   ```cmd
   generate_project.cmd MyFirstProject
   ```

## Troubleshooting

### Generator Not Found
If `generate_project.cmd` reports no suitable generator:
- Install .NET SDK from https://dotnet.microsoft.com/download
- Or install Python from https://www.python.org/downloads/

### Build Errors
- Verify XC32 compiler installation path
- Check that device family pack (DFP) is installed
- Ensure Make utility is in PATH

### VS Code Issues
- Install C/C++ extension pack
- Verify XC32 paths in `c_cpp_properties.json`
- Check debugger configuration in `launch.json`

## Contributing

All generators produce identical project structures. When adding features:
1. Update all generator implementations (C#, Python, Shell, Batch)
2. Test cross-platform compatibility
3. Update documentation

## License

This project is designed for use with Microchip's XC32 toolchain and PIC32MZ microcontrollers.
