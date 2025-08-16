# Example usage of the project generation scripts (PowerShell version)
# This demonstrates how to create projects in different root directories

Write-Host "========================================"
Write-Host "PIC32MZ Project Generator Examples"
Write-Host "========================================"
Write-Host ""

# Example 1: Create project in current directory
Write-Host "Example 1: Creating project in current directory..." -ForegroundColor Yellow
python generate_project.py TestProject1-PS
Write-Host ""

# Example 2: Create project in a specific root directory (Windows path)
Write-Host "Example 2: Creating project in C:\Temp\EmbeddedProjects..." -ForegroundColor Yellow
python generate_project.py TestProject2-PS --output "C:\Temp\EmbeddedProjects"
Write-Host ""

# Example 3: Create project with specific device and root directory
Write-Host "Example 3: Creating project with custom device and output directory..." -ForegroundColor Yellow
python generate_project.py TestProject3-PS --device 32MZ2048EFH064 --output "C:\Temp\EmbeddedProjects"
Write-Host ""

# Example 4: Create project with MikroC support
Write-Host "Example 4: Creating project with MikroC startup support..." -ForegroundColor Yellow
python generate_project.py TestProject4-PS --mikroc --output "C:\Temp\EmbeddedProjects"
Write-Host ""

# Using the batch script directly
Write-Host "Example 5: Using batch script directly..." -ForegroundColor Yellow
& ".\generate_project.bat" TestProject5-PS 32MZ1024EFH064 "C:\Temp\EmbeddedProjects"
Write-Host ""

Write-Host "========================================"
Write-Host "All examples completed!" -ForegroundColor Green
Write-Host "Check the created projects in their respective directories."
Write-Host "========================================"
Read-Host "Press Enter to continue"
