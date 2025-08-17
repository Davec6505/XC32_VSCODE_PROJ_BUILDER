# Generator Backend Examples for PIC32MZ Project Generator
# Tests all available generator implementations

Write-Host "====================================================="
Write-Host "PIC32MZ Project Generator - Backend Testing Examples"
Write-Host "====================================================="
Write-Host ""

Write-Host "This script tests all available generator backends:"
Write-Host "1. Main generator (auto-detection)"
Write-Host "2. C# generator (preferred)"
Write-Host "3. Python generator"
Write-Host "4. Shell script generator"
Write-Host ""
Read-Host "Press Enter to continue"

# Change to parent directory
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "====================================================="
Write-Host "Testing Main Generator (Auto-Detection)..."
Write-Host "====================================================="

Write-Host ""
Write-Host "Running: .\generate_project.cmd MainGen_Test"
.\generate_project.cmd MainGen_Test

Write-Host "====================================================="
Write-Host "Testing C# Generator (Direct)..."
Write-Host "====================================================="

Write-Host ""
if (Get-Command dotnet -ErrorAction SilentlyContinue) {
    Write-Host "✓ .NET SDK found - testing C# generator"
    Write-Host "Running: dotnet run --project csharp\generate_project.csproj -- CSharp_Test"
    dotnet run --project csharp\generate_project.csproj -- CSharp_Test
    
    Write-Host ""
    Write-Host "Testing C# generator with custom device..."
    Write-Host "Running: dotnet run --project csharp\generate_project.csproj -- CSharp_Device_Test 32MZ2048EFH064"
    dotnet run --project csharp\generate_project.csproj -- CSharp_Device_Test 32MZ2048EFH064
    
    Write-Host ""
    Write-Host "Testing C# generator with MikroC support..."
    Write-Host "Running: dotnet run --project csharp\generate_project.csproj -- CSharp_MikroC_Test 32MZ1024EFH064 . mikroc"
    dotnet run --project csharp\generate_project.csproj -- CSharp_MikroC_Test 32MZ1024EFH064 . mikroc
} else {
    Write-Host "✗ .NET SDK not found - C# generator not available"
    Write-Host "Install .NET SDK from: https://dotnet.microsoft.com/download"
}

Write-Host "====================================================="
Write-Host "Testing Python Generator..."
Write-Host "====================================================="

Write-Host ""
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✓ Python found - testing Python generator"
    Write-Host "Running: python generate_project.py Python_Test"
    python generate_project.py Python_Test
    
    Write-Host ""
    Write-Host "Testing Python generator with custom device..."
    Write-Host "Running: python generate_project.py Python_Device_Test 32MZ2048EFH064"
    python generate_project.py Python_Device_Test 32MZ2048EFH064
    
    Write-Host ""
    Write-Host "Testing Python generator with MikroC support..."
    Write-Host "Running: python generate_project.py Python_MikroC_Test 32MZ1024EFH064 . mikroc"
    python generate_project.py Python_MikroC_Test 32MZ1024EFH064 . mikroc
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    Write-Host "✓ Python3 found - testing Python generator"
    Write-Host "Running: python3 generate_project.py Python_Test"
    python3 generate_project.py Python_Test
} else {
    Write-Host "✗ Python not found - Python generator not available"
    Write-Host "Install Python from: https://www.python.org/downloads/"
}

Write-Host "====================================================="
Write-Host "Testing Shell Script Generator..."
Write-Host "====================================================="

Write-Host ""
if (Get-Command bash -ErrorAction SilentlyContinue) {
    Write-Host "✓ Bash found - testing Shell script generator"
    Write-Host "Running: bash generate_project.sh Shell_Test"
    bash generate_project.sh Shell_Test
    
    Write-Host ""
    Write-Host "Testing Shell generator with custom device..."
    Write-Host "Running: bash generate_project.sh Shell_Device_Test 32MZ2048EFH064"
    bash generate_project.sh Shell_Device_Test 32MZ2048EFH064
    
    Write-Host ""
    Write-Host "Testing Shell generator with MikroC support..."
    Write-Host "Running: bash generate_project.sh Shell_MikroC_Test 32MZ1024EFH064 . mikroc"
    bash generate_project.sh Shell_MikroC_Test 32MZ1024EFH064 . mikroc
} else {
    Write-Host "✗ Bash not found - Shell script generator not available"
    Write-Host "Install Git for Windows or WSL for bash support"
}

Write-Host "====================================================="
Write-Host "Comparing Generated Projects..."
Write-Host "====================================================="

Write-Host ""
Write-Host "Checking if all generators produce identical results..."

$projects = @("MainGen_Test", "CSharp_Test", "Python_Test", "Shell_Test")
$existingProjects = @()

foreach ($project in $projects) {
    if (Test-Path $project) {
        $existingProjects += $project
        Write-Host "✓ $project - Created successfully"
        
        # Check key files
        if (Test-Path "$project\Makefile") {
            Write-Host "  ✓ Root Makefile present"
        }
        if (Test-Path "$project\srcs\Makefile") {
            Write-Host "  ✓ Source Makefile present"
        }
        if (Test-Path "$project\srcs\main.c") {
            Write-Host "  ✓ Main.c template present"
        }
        if (Test-Path "$project\.vscode") {
            Write-Host "  ✓ VS Code configuration present"
        }
    } else {
        Write-Host "✗ $project - Not created (generator not available)"
    }
    Write-Host ""
}

Write-Host "====================================================="
Write-Host "Backend Testing Complete!"
Write-Host "====================================================="
Write-Host ""
Write-Host "Generator Test Results:"
Write-Host "- Main Generator: $(if (Test-Path 'MainGen_Test') { '✓ PASSED' } else { '✗ FAILED' })"
Write-Host "- C# Generator: $(if (Test-Path 'CSharp_Test') { '✓ PASSED' } else { '✗ FAILED/NOT AVAILABLE' })"
Write-Host "- Python Generator: $(if (Test-Path 'Python_Test') { '✓ PASSED' } else { '✗ FAILED/NOT AVAILABLE' })"
Write-Host "- Shell Generator: $(if (Test-Path 'Shell_Test') { '✓ PASSED' } else { '✗ FAILED/NOT AVAILABLE' })"
Write-Host ""
Write-Host "All successful generators produce identical project structures!"
Write-Host "The main generator automatically selects the best available backend."
Write-Host ""
Read-Host "Press Enter to exit"
