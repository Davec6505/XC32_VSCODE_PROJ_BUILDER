#!/bin/bash
# Basic Usage Examples for PIC32MZ Project Generator
# Shell Script Examples

echo "=============================================="
echo "PIC32MZ Project Generator - Basic Usage Examples"
echo "=============================================="
echo ""

echo "Example 1: Create project in current directory"
echo "Command: ./generate_project.cmd MyBasicProject"
echo ""
read -p "Press Enter to continue..."

echo "Example 2: Create project with specific device"
echo "Command: ./generate_project.cmd MyProject 32MZ2048EFH064"
echo ""
read -p "Press Enter to continue..."

echo "Example 3: Create project in custom directory"
echo "Command: ./generate_project.cmd MyProject 32MZ1024EFH064 /home/projects"
echo ""
read -p "Press Enter to continue..."

echo "Example 4: Create project with MikroC support"
echo "Command: ./generate_project.cmd MyProject 32MZ1024EFH064 /home/projects mikroc"
echo ""
read -p "Press Enter to continue..."

echo "=============================================="
echo "Choose an example to run:"
echo "=============================================="
echo "1. Basic project (current directory)"
echo "2. Custom device (32MZ2048EFH064)"
echo "3. Custom directory (/tmp/TestProjects)"
echo "4. MikroC support enabled"
echo "5. Direct Python generator"
echo "6. Direct shell script generator"
echo "7. Exit"
echo ""

read -p "Enter your choice (1-7): " choice

# Change to parent directory
cd "$(dirname "$0")/.."

case $choice in
    1)
        echo "Running: ./generate_project.cmd ExampleBasic"
        ./generate_project.cmd ExampleBasic
        ;;
    2)
        echo "Running: ./generate_project.cmd ExampleDevice 32MZ2048EFH064"
        ./generate_project.cmd ExampleDevice 32MZ2048EFH064
        ;;
    3)
        mkdir -p "/tmp/TestProjects"
        echo "Running: ./generate_project.cmd ExampleCustomDir 32MZ1024EFH064 /tmp/TestProjects"
        ./generate_project.cmd ExampleCustomDir 32MZ1024EFH064 /tmp/TestProjects
        ;;
    4)
        echo "Running: ./generate_project.cmd ExampleMikroC 32MZ1024EFH064 . mikroc"
        ./generate_project.cmd ExampleMikroC 32MZ1024EFH064 . mikroc
        ;;
    5)
        echo "Running: python3 generate_project.py ExamplePython"
        python3 generate_project.py ExamplePython
        ;;
    6)
        echo "Running: bash generate_project.sh ExampleShell"
        bash generate_project.sh ExampleShell
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "Example completed! Check the generated project folder."
read -p "Press Enter to exit..."
