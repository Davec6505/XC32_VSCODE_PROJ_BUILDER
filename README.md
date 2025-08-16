 # XC32_VSCODE_PROJ_BUILDER
A GNU make build process and VS Code project generator independent of any MPLAB products, purely using copilot.

## Project Generation Scripts

This repository contains several scripts to automatically generate PIC32MZ embedded project structures with cross-platform Makefiles:

### Available Scripts

1. **`generate_project.py`** - Python version (most feature-complete)
2. **`generate_project.sh`** - Bash shell script (Linux/macOS/WSL)
3. **`generate_project_simple.sh`** - Simplified bash version with MikroC support
4. **`generate_project.bat`** - Windows batch script

### Usage Examples

#### Python Script
```bash
# Create project in current directory
python generate_project.py MyProject

# Create project with specific device
python generate_project.py MyProject --device 32MZ2048EFH064

# Create project in specific root directory
python generate_project.py MyProject --output /home/projects
python generate_project.py MyProject --output ~/workspace/embedded

# Create project with MikroC startup support
python generate_project.py MyProject --mikroc --output /home/projects

# Full example
python generate_project.py MyEmbeddedApp --device 32MZ1024EFH064 --output ~/projects/embedded --mikroc
```

#### Shell Scripts
```bash
# Create project in current directory
./generate_project.sh MyProject

# Create project with specific device and root directory
./generate_project.sh MyProject 32MZ2048EFH064 ~/projects/embedded

# With MikroC support (simple version)
./generate_project_simple.sh MyProject 32MZ1024EFH064 ~/projects/embedded mikroc
```

#### Windows Batch Script
```cmd
REM Create project in current directory
generate_project.bat MyProject

REM Create project with specific device and root directory
generate_project.bat MyProject 32MZ2048EFH064 C:\Projects\Embedded

REM With MikroC support
generate_project.bat MyProject 32MZ1024EFH064 C:\Projects\Embedded mikroc
```

### What Gets Created

All scripts will create the following structure at `<root_directory>/<project_name>/`:

```
MyProject/
├── Makefile                 # Root build file
├── .gitignore              # Git ignore file
├── srcs/
│   ├── Makefile            # Source build configuration
│   ├── main.c              # Template main file
│   └── startup/            # (MikroC option only)
│       ├── crt0.c          # C runtime startup
│       └── startup.S       # Assembly startup
├── incs/                   # Header files
├── objs/                   # Object files (build artifacts)
├── bins/                   # Binary outputs
├── other/                  # Other build artifacts
└── docs/                   # Documentation
```

### Building Projects

After generation, navigate to your project and build:

```bash
cd path/to/your/project
make build_dir          # Create build directories
make                    # Build the project
make clean              # Clean build artifacts
make flash              # Flash to device (if configured)
```

### Features

- **Cross-platform**: Works on Windows, Linux, and macOS
- **Automatic path handling**: Creates root directories if they don't exist  
- **Device flexibility**: Support for various PIC32MZ devices
- **MikroC compatibility**: Optional startup files for bootloader compatibility
- **Template files**: Includes working main.c template and build configuration
- **Git ready**: Includes appropriate .gitignore file

### Requirements

- **XC32 Compiler**: Must be installed in standard locations
  - Windows: `C:/Program Files/Microchip/xc32/v4.60/`
  - Linux/macOS: `/opt/microchip/xc32/v4.60/`
- **DFP (Device Family Pack)**: PIC32MZ-EF family pack
- **Make**: GNU Make build system
