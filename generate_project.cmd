@echo off
:: PIC32MZ Project Generator
:: Cross-platform project generator for PIC32MZ embedded projects
::
:: This is the main entry point that automatically selects the best available generator:
:: 1. C# version (recommended - requires .NET SDK)
:: 2. Python version (fallback - requires Python)  
:: 3. Shell script version (Linux/Mac/WSL)

:: Show usage if no arguments
if "%~1"=="" (
    echo Usage: %~nx0 ^<project_name^> [device] [root_directory] [mikroc]
    echo.
    echo Arguments:
    echo   project_name     Name of the project to generate ^(required^)
    echo   device          PIC32MZ device ^(default: 32MZ1024EFH064^)
    echo   root_directory  Root directory where project folder will be created ^(default: current directory^)
    echo   mikroc          Include startup files for MikroC compatibility ^(optional^)
    echo.
    echo Examples:
    echo   %~nx0 MyProject
    echo   %~nx0 MyProject 32MZ2048EFH064
    echo   %~nx0 MyProject 32MZ1024EFH064 C:\Projects
    echo   %~nx0 MyProject 32MZ1024EFH064 C:\Projects mikroc
    echo.
    echo Available generators:
    echo   - C# version ^(preferred^): Requires .NET SDK 6.0+
    echo   - Python version: python generate_project.py [args]
    echo   - Shell script: bash generate_project.sh [args]
    goto :eof
)

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Try C# version first (preferred)
where dotnet >nul 2>nul
if not errorlevel 1 (
    echo Using C# generator...
    dotnet run --project "%SCRIPT_DIR%csharp\generate_project.csproj" -- %*
    goto :eof
)

:: Fallback to Python version
where python >nul 2>nul
if not errorlevel 1 (
    echo .NET not found, using Python generator...
    python "%SCRIPT_DIR%generate_project.py" %*
    goto :eof
)

:: No suitable generator found
echo Error: No suitable project generator found!
echo.
echo Please install one of the following:
echo   - .NET SDK 6.0+ for C# version ^(recommended^)
echo   - Python 3.6+ for Python version
echo.
echo Downloads:
echo   - .NET SDK: https://dotnet.microsoft.com/download
echo   - Python: https://www.python.org/downloads/
echo.
echo Alternatively, you can run the generators directly:
echo   python generate_project.py [args]
echo   bash generate_project.sh [args]
