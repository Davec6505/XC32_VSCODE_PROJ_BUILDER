# PIC32MZ Project Generator - Example Usage Guide

This folder contains comprehensive examples demonstrating all features and use cases of the PIC32MZ Project Generator.

## 📁 Example Files

### Basic Usage Examples
- **`basic_usage.bat`** - Windows Batch script with interactive menu
- **`basic_usage.ps1`** - PowerShell script with interactive examples
- **`basic_usage.sh`** - Shell script for Linux/macOS/WSL

**Features demonstrated:**
- Simple project creation in current directory
- Custom device selection (32MZ1024EFH064, 32MZ2048EFH064)
- Custom output directory specification
- MikroC bootloader support

### Advanced Usage Examples
- **`advanced_usage.bat`** - Windows advanced scenarios
- **`advanced_usage.sh`** - Unix/Linux advanced scenarios

**Features demonstrated:**
- Batch creation of multiple projects
- Organized directory structures
- Mixed device configurations
- Testing all generator backends
- Real-world project scenarios

### Device-Specific Examples
- **`device_specific.ps1`** - PowerShell examples for different devices

**Features demonstrated:**
- Memory-optimized projects for 32MZ1024EFH064 (1MB Flash)
- Feature-rich projects for 32MZ2048EFH064 (2MB Flash)
- Application-specific configurations
- Device-appropriate project templates

### MikroC Compatibility Examples
- **`mikroc_examples.bat`** - Comprehensive MikroC bootloader examples

**Features demonstrated:**
- Bootloader-compatible project creation
- Custom startup file generation (startup.S)
- Legacy system integration
- Bootloader deployment scenarios

### Generator Backend Testing
- **`generator_backends.ps1`** - Tests all available generators

**Features demonstrated:**
- Main generator auto-detection
- Direct C# generator usage
- Python generator testing
- Shell script generator testing
- Result comparison and validation

### Python Script Usage
- **`python_usage.py`** - Interactive Python script examples
- **`python_usage.md`** - Comprehensive Python usage guide

**Features demonstrated:**
- Direct Python script usage
- Cross-platform Python examples
- Virtual environment integration
- Batch project creation with Python
- CI/CD pipeline integration
- Troubleshooting Python issues

## 🚀 Quick Start

### Windows Users
```cmd
# Run basic interactive examples
cd examples
basic_usage.bat

# Run advanced batch scenarios
advanced_usage.bat

# Test MikroC compatibility
mikroc_examples.bat
```

### PowerShell Users
```powershell
# Device-specific examples
cd examples
.\device_specific.ps1

# Test all generator backends
.\generator_backends.ps1

# Interactive Python examples
python python_usage.py
```

### Linux/macOS Users
```bash
# Make scripts executable
chmod +x examples/*.sh

# Run basic examples
cd examples
./basic_usage.sh

# Run advanced scenarios
./advanced_usage.sh
```

## 📋 Example Scenarios Covered

### 1. Basic Project Creation
- Simple embedded application
- LED controller
- Sensor reading project
- Communication hub

### 2. Device-Specific Projects
- **32MZ1024EFH064**: IoT sensors, basic controllers, simple communication
- **32MZ2048EFH064**: Data loggers, gateways, complex motor control

### 3. Application Categories
- **Industrial**: Automation controllers, process monitoring
- **Automotive**: CAN gateways, diagnostics, ECU development
- **Medical**: Device controllers, sensor interfaces
- **IoT/Smart Home**: Wireless nodes, protocol bridges
- **Communication**: UART/SPI/I2C hubs, protocol converters

### 4. MikroC Integration
- Bootloader-compatible applications
- Legacy system ports
- Custom startup configurations
- Memory layout optimization

### 5. Development Workflows
- Multi-project workspaces
- Team development scenarios
- CI/CD pipeline integration
- Cross-platform development

### 6. Direct Python Usage
- Interactive Python script execution
- Virtual environment integration
- Cross-platform Python commands
- Batch automation with Python
- Development workflow integration

## 🛠️ Testing Your Setup

Run the generator backend testing script to verify your development environment:

```powershell
# Test all available generators
.\examples\generator_backends.ps1
```

This will test:
- ✅ Main generator (always available)
- ✅ C# generator (requires .NET SDK 6.0+)
- ✅ Python generator (requires Python 3.6+)
- ✅ Shell generator (requires Bash)

## 📦 Generated Project Structure

All examples create projects with this structure:
```
MyProject/
├── Makefile                 # Root build configuration
├── .gitignore              # Git ignore rules
├── .vscode/                # VS Code integration
│   ├── tasks.json          # Build/flash tasks
│   ├── launch.json         # Debug configuration
│   └── c_cpp_properties.json # IntelliSense
├── srcs/
│   ├── Makefile            # Source build rules
│   ├── main.c              # Application entry point
│   └── startup/            # MikroC support (optional)
│       ├── crt0.c          # C runtime
│       └── startup.S       # Assembly startup
├── incs/                   # Header files
│   └── definitions.h       # System definitions
├── objs/                   # Object files
├── bins/                   # Binary outputs
├── other/                  # Build artifacts
├── docs/                   # Documentation
└── README.md               # Project documentation
```

## 🔧 Customization

Each example can be modified for your specific needs:

1. **Change device types** by editing the device parameter
2. **Modify output directories** to match your workspace
3. **Add/remove MikroC support** using the mikroc flag
4. **Batch create projects** by duplicating generator calls

## 💡 Best Practices

- **Use descriptive project names** that reflect functionality
- **Organize projects in logical directory structures**
- **Enable MikroC support** only when needed for bootloader compatibility
- **Test with different devices** to ensure cross-compatibility
- **Use the main generator** for automatic backend selection

## 🆘 Troubleshooting

If examples fail to run:

1. **Check generator availability**: Run `generator_backends.ps1`
2. **Verify paths**: Ensure you're in the correct directory
3. **Check permissions**: Scripts may need execution permissions
4. **Install dependencies**: .NET SDK, Python, or Bash as needed

## 📚 Learning Path

Recommended order for exploring examples:

1. **Start with `basic_usage`** to understand core concepts
2. **Try `device_specific`** to see device optimization
3. **Explore `python_usage.md`** for direct Python script usage
4. **Try `advanced_usage`** for complex scenarios
5. **Test `generator_backends`** to understand implementation options
6. **Use `mikroc_examples`** if you need bootloader compatibility
7. **Run `python_usage.py`** for interactive Python examples

Each example builds on previous concepts and demonstrates increasingly sophisticated usage patterns.

---

**Ready to generate your first PIC32MZ project? Start with the basic examples and work your way up!** 🚀
