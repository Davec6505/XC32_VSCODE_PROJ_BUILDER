# Basic Usage Examples for PIC32MZ Project Generator
# PowerShell Script Examples

Write-Host "=============================================="
Write-Host "PIC32MZ Project Generator - Basic Usage Examples"
Write-Host "=============================================="
Write-Host ""

Write-Host "Example 1: Create project in current directory"
Write-Host "Command: .\generate_project.cmd MyBasicProject"
Write-Host ""
Read-Host "Press Enter to continue"

Write-Host "Example 2: Create project with specific device"
Write-Host "Command: .\generate_project.cmd MyProject 32MZ2048EFH064"
Write-Host ""
Read-Host "Press Enter to continue"

Write-Host "Example 3: Create project in custom directory"
Write-Host "Command: .\generate_project.cmd MyProject 32MZ1024EFH064 C:\Projects"
Write-Host ""
Read-Host "Press Enter to continue"

Write-Host "Example 4: Create project with MikroC support"
Write-Host "Command: .\generate_project.cmd MyProject 32MZ1024EFH064 C:\Projects mikroc"
Write-Host ""
Read-Host "Press Enter to continue"

Write-Host "=============================================="
Write-Host "Choose an example to run:"
Write-Host "=============================================="
Write-Host "1. Basic project (current directory)"
Write-Host "2. Custom device (32MZ2048EFH064)"
Write-Host "3. Custom directory (C:\Temp\TestProjects)"
Write-Host "4. MikroC support enabled"
Write-Host "5. Exit"
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

# Change to parent directory
Set-Location (Split-Path $PSScriptRoot -Parent)

switch ($choice) {
    "1" {
        Write-Host "Running: .\generate_project.cmd ExampleBasic"
        .\generate_project.cmd ExampleBasic
    }
    "2" {
        Write-Host "Running: .\generate_project.cmd ExampleDevice 32MZ2048EFH064"
        .\generate_project.cmd ExampleDevice 32MZ2048EFH064
    }
    "3" {
        if (!(Test-Path "C:\Temp\TestProjects")) {
            New-Item -ItemType Directory -Path "C:\Temp\TestProjects" -Force
        }
        Write-Host "Running: .\generate_project.cmd ExampleCustomDir 32MZ1024EFH064 C:\Temp\TestProjects"
        .\generate_project.cmd ExampleCustomDir 32MZ1024EFH064 C:\Temp\TestProjects
    }
    "4" {
        Write-Host "Running: .\generate_project.cmd ExampleMikroC 32MZ1024EFH064 . mikroc"
        .\generate_project.cmd ExampleMikroC 32MZ1024EFH064 . mikroc
    }
    "5" {
        Write-Host "Exiting..."
        exit
    }
    default {
        Write-Host "Invalid choice. Please run the script again."
        exit 1
    }
}

Write-Host ""
Write-Host "Example completed! Check the generated project folder."
Read-Host "Press Enter to exit"
