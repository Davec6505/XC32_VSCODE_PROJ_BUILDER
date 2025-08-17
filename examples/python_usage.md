# Python Script Usage Examples

This guide demonstrates how to use the `generate_project.py` script directly.

## Prerequisites

- Python 3.6 or later
- Access to the `generate_project.py` file

## Basic Usage

```bash
python generate_project.py <project_name> [device] [output_dir] [mikroc]
```

### Arguments
- `project_name` - Name of the project (required)
- `device` - PIC32MZ device (optional, default: 32MZ1024EFH064)
- `output_dir` - Output directory (optional, default: current directory)
- `mikroc` - Add MikroC support (optional, use "mikroc" to enable)

## Examples

### 1. Basic Project Creation
```bash
# Create a simple project in current directory
python generate_project.py MyBasicProject

# Same as above but more explicit
python generate_project.py MyBasicProject 32MZ1024EFH064 .
```

### 2. Custom Device Selection
```bash
# Create project for 32MZ2048EFH064 (2MB Flash)
python generate_project.py MyLargeProject 32MZ2048EFH064

# Create project for 32MZ1024EFH064 (1MB Flash) 
python generate_project.py MySmallProject 32MZ1024EFH064
```

### 3. Custom Output Directory
```bash
# Windows-style paths
python generate_project.py MyProject 32MZ1024EFH064 C:\Projects
python generate_project.py MyProject 32MZ1024EFH064 C:\Dev\Embedded

# Unix-style paths (Linux/macOS)
python3 generate_project.py MyProject 32MZ1024EFH064 /home/user/projects
python3 generate_project.py MyProject 32MZ1024EFH064 ~/embedded_projects

# Relative paths (cross-platform)
python generate_project.py MyProject 32MZ1024EFH064 ./projects
python generate_project.py MyProject 32MZ1024EFH064 ../workspace/embedded
```

### 4. MikroC Bootloader Support
```bash
# Enable MikroC compatibility (includes startup files)
python generate_project.py MyBootloaderApp 32MZ1024EFH064 . mikroc
python generate_project.py MyBootloaderApp 32MZ2048EFH064 ./projects mikroc

# MikroC project in custom directory
python generate_project.py IndustrialController 32MZ2048EFH064 C:\MikroC_Projects mikroc
```

## Application-Specific Examples

### IoT and Sensor Projects (Memory Optimized)
```bash
# IoT sensor node (32MZ1024EFH064 for lower power/cost)
python generate_project.py IoT_TempSensor 32MZ1024EFH064 ./iot_projects

# Simple communication hub
python generate_project.py UART_CommHub 32MZ1024EFH064 ./iot_projects

# Basic LED controller with MikroC
python generate_project.py LED_Controller 32MZ1024EFH064 ./iot_projects mikroc
```

### Industrial and Complex Projects (High Performance)
```bash
# Data logger (32MZ2048EFH064 for large data storage)
python generate_project.py DataLogger_Industrial 32MZ2048EFH064 ./industrial

# Multi-protocol gateway
python generate_project.py Protocol_Gateway 32MZ2048EFH064 ./industrial

# Motor control system with MikroC
python generate_project.py Motor_Controller 32MZ2048EFH064 ./industrial mikroc
```

### Automotive Projects
```bash
# CAN bus gateway
python generate_project.py CAN_Gateway 32MZ2048EFH064 ./automotive

# OBD-II diagnostic tool
python generate_project.py OBD2_Diagnostic 32MZ1024EFH064 ./automotive mikroc

# ECU development platform
python generate_project.py ECU_Platform 32MZ2048EFH064 ./automotive
```

## Cross-Platform Usage

### Windows
```cmd
# Command Prompt
python generate_project.py MyWindowsProject 32MZ1024EFH064 C:\Projects

# PowerShell
python generate_project.py MyPSProject 32MZ2048EFH064 C:\Dev\Embedded mikroc
```

### Linux/macOS
```bash
# Use python3 explicitly
python3 generate_project.py MyUnixProject 32MZ1024EFH064 /tmp/projects

# With home directory
python3 generate_project.py MyHomeProject 32MZ2048EFH064 ~/embedded_dev mikroc
```

### WSL (Windows Subsystem for Linux)
```bash
# Linux commands in Windows
python3 generate_project.py MyWSLProject 32MZ1024EFH064 /mnt/c/Projects

# Access Windows directories from WSL
python3 generate_project.py MyWSLWinProject 32MZ2048EFH064 /mnt/c/Users/YourName/Desktop/Projects
```

## Batch Project Creation

### Create Multiple Projects
```bash
# Create several related projects
python generate_project.py SensorNode1 32MZ1024EFH064 ./sensor_network
python generate_project.py SensorNode2 32MZ1024EFH064 ./sensor_network
python generate_project.py SensorGateway 32MZ2048EFH064 ./sensor_network

# Create projects for different applications
python generate_project.py HomeAutomation 32MZ2048EFH064 ./smart_home
python generate_project.py SecuritySystem 32MZ1024EFH064 ./smart_home mikroc
python generate_project.py EnergyMonitor 32MZ1024EFH064 ./smart_home
```

### Organized Project Structure
```bash
# Create organized directory structure
python generate_project.py TempSensor 32MZ1024EFH064 ./projects/sensors
python generate_project.py PressureSensor 32MZ2048EFH064 ./projects/sensors
python generate_project.py UART_Bridge 32MZ1024EFH064 ./projects/communication
python generate_project.py CAN_Interface 32MZ2048EFH064 ./projects/communication mikroc
python generate_project.py ServoDriver 32MZ1024EFH064 ./projects/actuators
python generate_project.py StepperController 32MZ2048EFH064 ./projects/actuators mikroc
```

## Virtual Environment Usage

### Python Virtual Environment
```bash
# Create and activate virtual environment
python -m venv pic32_env

# Windows activation
pic32_env\Scripts\activate

# Linux/macOS activation  
source pic32_env/bin/activate

# Use generator in virtual environment
python generate_project.py VenvProject 32MZ1024EFH064
```

### Conda Environment
```bash
# Create conda environment
conda create -n pic32_dev python=3.9

# Activate environment
conda activate pic32_dev

# Use generator
python generate_project.py CondaProject 32MZ2048EFH064 ./conda_projects
```

## Development Workflow Integration

### IDE Integration
```bash
# VS Code integrated terminal
python generate_project.py VSCodeProject 32MZ1024EFH064 ./vscode_workspace

# PyCharm terminal
python generate_project.py PyCharmProject 32MZ2048EFH064 ./pycharm_projects
```

### CI/CD Pipeline
```bash
# Jenkins/GitHub Actions
python generate_project.py CI_Project 32MZ1024EFH064 ./build/artifacts

# Docker container
docker run -v $(pwd):/workspace -w /workspace python:3.9 python generate_project.py DockerProject
```

## Troubleshooting

### Common Issues and Solutions

**Issue**: `python: command not found`
```bash
# Solution: Use python3 or install Python
python3 generate_project.py MyProject

# Or install Python from https://python.org/downloads/
```

**Issue**: `Permission denied`
```bash
# Solution: Use different directory or run with permissions
python generate_project.py MyProject 32MZ1024EFH064 ./my_projects

# Or on Unix systems:
sudo python generate_project.py MyProject 32MZ1024EFH064 /opt/projects
```

**Issue**: `No such file or directory: 'generate_project.py'`
```bash
# Solution: Ensure you're in the correct directory
cd path/to/XC32_VSCODE_PROJ_BUILDER
python generate_project.py MyProject

# Or use full path
python /full/path/to/generate_project.py MyProject
```

**Issue**: Python version too old
```bash
# Check Python version
python --version

# Upgrade if less than 3.6
# Install newer Python from https://python.org/downloads/
```

## Generated Project Structure

All Python-generated projects include:
```
MyProject/
├── Makefile                 # Root build configuration
├── .gitignore              # Git ignore rules
├── .vscode/                # VS Code integration (if C# backend used)
├── srcs/
│   ├── Makefile            # Source build rules
│   ├── main.c              # Application entry point
│   └── startup/            # MikroC support (if enabled)
├── incs/                   # Header files
├── objs/                   # Object files
├── bins/                   # Binary outputs  
├── other/                  # Build artifacts
├── docs/                   # Documentation
└── README.md               # Project documentation
```

## Next Steps

After generating a project:

1. **Navigate to project directory**:
   ```bash
   cd MyProject
   ```

2. **Build the project**:
   ```bash
   make build_dir
   make
   ```

3. **Open in VS Code** (if VS Code integration available):
   ```bash
   code .
   ```

4. **Start developing** - edit `srcs/main.c` and add your application code!

---

**Pro Tip**: Use the main `generate_project.cmd` for automatic backend detection, or use `python generate_project.py` directly when you specifically want the Python implementation!
