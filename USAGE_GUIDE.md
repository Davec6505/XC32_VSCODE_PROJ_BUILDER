# Quick Usage Guide

## How to Run the Example Scripts

### Option 1: PowerShell (Recommended)
```powershell
# Run the PowerShell version
.\example_usage.ps1

# Or run individual commands
python generate_project.py MyProject --output "C:\MyProjects"
```

### Option 2: Command Prompt
```cmd
# Run the batch version
example_usage.bat

# Or run individual commands
python generate_project.py MyProject --output "C:\MyProjects"
```

### Option 3: PowerShell with Batch File
```powershell
# Run the batch file from PowerShell
.\example_usage.bat
```

## Common Issues and Solutions

### Issue: "Command not found"
**Problem**: Running `example_usage.bat` in PowerShell without `.\`
**Solution**: Use `.\example_usage.bat` instead

### Issue: Character encoding problems
**Problem**: Special characters not displaying correctly in batch files
**Solution**: Use the PowerShell version (`example_usage.ps1`) instead

### Issue: Python not found
**Problem**: Python is not in your PATH
**Solution**: 
- Install Python and ensure it's in your PATH, or
- Use full path: `C:\Python\python.exe generate_project.py ...`

## Direct Usage Examples

### Python Script (Most Flexible)
```bash
# Basic usage
python generate_project.py MyProject

# With custom root directory
python generate_project.py MyProject --output "C:\MyProjects"

# With custom device
python generate_project.py MyProject --device 32MZ2048EFH064 --output "C:\MyProjects"

# With MikroC support
python generate_project.py MyProject --mikroc --output "C:\MyProjects"
```

### Batch Script
```cmd
generate_project.bat MyProject
generate_project.bat MyProject 32MZ2048EFH064 "C:\MyProjects"
generate_project.bat MyProject 32MZ2048EFH064 "C:\MyProjects" mikroc
```

### Shell Scripts (Linux/macOS/WSL)
```bash
./generate_project.sh MyProject
./generate_project.sh MyProject 32MZ2048EFH064 "/home/user/projects"
./generate_project_simple.sh MyProject 32MZ2048EFH064 "/home/user/projects" mikroc
```
