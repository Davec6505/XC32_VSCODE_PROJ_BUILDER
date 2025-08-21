@echo off
:: Basic Usage Examples for PIC32MZ Project Generator
:: Windows Batch Script Examples

echo ==============================================
echo PIC32MZ Project Generator - Basic Usage Examples
echo ==============================================
echo.

echo Example 1: Create project in current directory
echo Command: generate_project.cmd MyBasicProject
echo.
pause

echo Example 2: Create project with specific device
echo Command: generate_project.cmd MyProject 32MZ2048EFH064
echo.
pause

echo Example 3: Create project in custom directory
echo Command: generate_project.cmd MyProject 32MZ1024EFH064 C:\Projects
echo.
pause

echo Example 4: Create project with MikroC support
echo Command: generate_project.cmd MyProject 32MZ1024EFH064 C:\Projects mikroc
echo.
pause

echo Example 5: Run csharp example
echo Command: generate_cs_project.cmd MyCSharpProject 32MZ1024EFH064 C:\Temp mikroc csharp
echo.

echo ==============================================
echo Choose an example to run:
echo ==============================================
echo 1. Basic project (current directory)
echo 2. Custom device (32MZ2048EFH064)
echo 3. Custom directory (C:\Temp\TestProjects)
echo 4. MikroC support enabled
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Running: generate_project.cmd ExampleBasic
    cd /d "%~dp0.."
    generate_project.cmd ExampleBasic
) else if "%choice%"=="2" (
    echo Running: generate_project.cmd ExampleDevice 32MZ2048EFH064
    cd /d "%~dp0.."
    generate_project.cmd ExampleDevice 32MZ2048EFH064
) else if "%choice%"=="3" (
    if not exist "C:\Temp\TestProjects" mkdir "C:\Temp\TestProjects"
    echo Running: generate_project.cmd ExampleCustomDir 32MZ1024EFH064 C:\Temp\TestProjects
    cd /d "%~dp0.."
    generate_project.cmd ExampleCustomDir 32MZ1024EFH064 C:\Temp\TestProjects
) else if "%choice%"=="4" (
    echo Running: generate_project.cmd ExampleMikroC 32MZ1024EFH064 . mikroc
    cd /d "%~dp0.."
    generate_project.cmd ExampleMikroC 32MZ1024EFH064 . mikroc
) else if "%choice%"=="5" (
    echo Exiting...
    goto :eof
) else (
    echo Invalid choice. Please run the script again.
)

echo.
echo Example completed! Check the generated project folder.
pause
