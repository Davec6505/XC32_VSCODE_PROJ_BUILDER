@echo off
:: Example usage of the project generation scripts
:: This demonstrates how to create projects in different root directories
::
:: USAGE: Run this from PowerShell with: .\example_usage.bat
:: Or from Command Prompt with: example_usage.bat

echo ========================================
echo PIC32MZ Project Generator Examples
echo ========================================
echo.
echo NOTE: This script demonstrates various ways to create projects
echo       in different root directories.
echo.

:: Example 1: Create project in current directory
echo Example 1: Creating project in current directory...
python generate_project.py TestProject1
echo.

:: Example 2: Create project in a specific root directory (Windows path)
echo Example 2: Creating project in C:\Temp\EmbeddedProjects...
python generate_project.py TestProject2 --output "C:\Temp\EmbeddedProjects"
echo.

:: Example 3: Create project with specific device and root directory
echo Example 3: Creating project with custom device and output directory...
python generate_project.py TestProject3 --device 32MZ2048EFH064 --output "C:\Temp\EmbeddedProjects"
echo.

:: Example 4: Create project with MikroC support
echo Example 4: Creating project with MikroC startup support...
python generate_project.py TestProject4 --mikroc --output "C:\Temp\EmbeddedProjects"
echo.

:: Using the batch script directly
echo Example 5: Using batch script directly...
call generate_project.bat TestProject5 32MZ1024EFH064 "C:\Temp\EmbeddedProjects"
echo.

echo ========================================
echo All examples completed!
echo Check the created projects in their respective directories.
echo ========================================
pause
