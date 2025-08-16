#!/bin/bash
# Example usage of the project generation scripts
# This demonstrates how to create projects in different root directories

echo "========================================"
echo "PIC32MZ Project Generator Examples"
echo "========================================"
echo

# Example 1: Create project in current directory
echo "Example 1: Creating project in current directory..."
python3 generate_project.py TestProject1
echo

# Example 2: Create project in a specific root directory (Unix path)
echo "Example 2: Creating project in ~/temp/embedded-projects..."
python3 generate_project.py TestProject2 --output "$HOME/temp/embedded-projects"
echo

# Example 3: Create project with specific device and root directory
echo "Example 3: Creating project with custom device and output directory..."
python3 generate_project.py TestProject3 --device 32MZ2048EFH064 --output "$HOME/temp/embedded-projects"
echo

# Example 4: Create project with MikroC support
echo "Example 4: Creating project with MikroC startup support..."
python3 generate_project.py TestProject4 --mikroc --output "$HOME/temp/embedded-projects"
echo

# Using the shell script directly
echo "Example 5: Using shell script directly..."
./generate_project.sh TestProject5 32MZ1024EFH064 "$HOME/temp/embedded-projects"
echo

# Using the simple shell script with MikroC
echo "Example 6: Using simple shell script with MikroC..."
./generate_project_simple.sh TestProject6 32MZ1024EFH064 "$HOME/temp/embedded-projects" mikroc
echo

echo "========================================"
echo "All examples completed!"
echo "Check the created projects in their respective directories."
echo "========================================"
