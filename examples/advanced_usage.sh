#!/bin/bash
# Advanced Usage Examples for PIC32MZ Project Generator
# Demonstrates various project configurations and scenarios

echo "==============================================="
echo "PIC32MZ Project Generator - Advanced Examples"
echo "==============================================="
echo ""

echo "This script demonstrates advanced usage scenarios:"
echo "1. Multiple projects with different devices"
echo "2. Custom directory structures"
echo "3. MikroC bootloader compatibility"
echo "4. Batch project creation"
echo "5. Different generator backends"
echo ""
read -p "Press Enter to continue..."

echo "==============================================="
echo "Creating multiple projects with different devices..."
echo "==============================================="

# Change to parent directory
cd "$(dirname "$0")/.."

echo ""
echo "Creating LED_Controller project for 32MZ1024EFH064..."
./generate_project.cmd LED_Controller 32MZ1024EFH064

echo ""
echo "Creating DataLogger project for 32MZ2048EFH064..."
./generate_project.cmd DataLogger 32MZ2048EFH064

echo ""
echo "Creating MotorControl project with MikroC support..."
./generate_project.cmd MotorControl 32MZ1024EFH064 . mikroc

echo "==============================================="
echo "Creating projects in organized directory structure..."
echo "==============================================="

# Create organized directory structure
mkdir -p "/tmp/EmbeddedProjects/Sensors"
mkdir -p "/tmp/EmbeddedProjects/Communication"
mkdir -p "/tmp/EmbeddedProjects/Control"

echo ""
echo "Creating sensor projects..."
./generate_project.cmd TempSensor 32MZ1024EFH064 "/tmp/EmbeddedProjects/Sensors"
./generate_project.cmd PressureSensor 32MZ2048EFH064 "/tmp/EmbeddedProjects/Sensors"

echo ""
echo "Creating communication projects..."
./generate_project.cmd UART_Gateway 32MZ2048EFH064 "/tmp/EmbeddedProjects/Communication"
./generate_project.cmd CAN_Bridge 32MZ1024EFH064 "/tmp/EmbeddedProjects/Communication" mikroc

echo ""
echo "Creating control projects..."
./generate_project.cmd PID_Controller 32MZ2048EFH064 "/tmp/EmbeddedProjects/Control"
./generate_project.cmd ServoDriver 32MZ1024EFH064 "/tmp/EmbeddedProjects/Control" mikroc

echo "==============================================="
echo "Testing different generator backends..."
echo "==============================================="

echo ""
echo "Testing direct C# generator..."
if command -v dotnet >/dev/null 2>&1; then
    dotnet run --project csharp/generate_project.csproj -- CSharpTest 32MZ1024EFH064
else
    echo "C# generator not available (.NET SDK not found)"
fi

echo ""
echo "Testing Python generator..."
if command -v python3 >/dev/null 2>&1; then
    python3 generate_project.py PythonTest 32MZ2048EFH064
elif command -v python >/dev/null 2>&1; then
    python generate_project.py PythonTest 32MZ2048EFH064
else
    echo "Python generator not available"
fi

echo ""
echo "Testing Shell script generator..."
if [ -f "generate_project.sh" ]; then
    bash generate_project.sh ShellTest 32MZ1024EFH064
else
    echo "Shell script generator not found"
fi

echo "==============================================="
echo "Advanced Example Complete!"
echo "==============================================="
echo ""
echo "Projects created:"
echo "- Current directory: LED_Controller, DataLogger, MotorControl"
echo "- /tmp/EmbeddedProjects/Sensors: TempSensor, PressureSensor"
echo "- /tmp/EmbeddedProjects/Communication: UART_Gateway, CAN_Bridge"
echo "- /tmp/EmbeddedProjects/Control: PID_Controller, ServoDriver"
echo "- Generator tests: CSharpTest, PythonTest, ShellTest"
echo ""
echo "All projects are ready for development!"
echo "Open any project folder in VS Code to start coding."
echo ""
read -p "Press Enter to exit..."
