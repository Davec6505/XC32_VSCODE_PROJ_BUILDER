@echo off
:: Advanced Usage Examples for PIC32MZ Project Generator
:: Demonstrates various project configurations and scenarios

echo ===============================================
echo PIC32MZ Project Generator - Advanced Examples
echo ===============================================
echo.

echo This script demonstrates advanced usage scenarios:
echo 1. Multiple projects with different devices
echo 2. Custom directory structures
echo 3. MikroC bootloader compatibility
echo 4. Batch project creation
echo 5. Different generator backends
echo.
pause

echo ===============================================
echo Creating multiple projects with different devices...
echo ===============================================

cd /d "%~dp0.."

echo.
echo Creating LED_Controller project for 32MZ1024EFH064...
generate_project.cmd LED_Controller 32MZ1024EFH064

echo.
echo Creating DataLogger project for 32MZ2048EFH064...
generate_project.cmd DataLogger 32MZ2048EFH064

echo.
echo Creating MotorControl project with MikroC support...
generate_project.cmd MotorControl 32MZ1024EFH064 . mikroc

echo ===============================================
echo Creating projects in organized directory structure...
echo ===============================================

if not exist "C:\Temp\EmbeddedProjects" mkdir "C:\Temp\EmbeddedProjects"
if not exist "C:\Temp\EmbeddedProjects\Sensors" mkdir "C:\Temp\EmbeddedProjects\Sensors"
if not exist "C:\Temp\EmbeddedProjects\Communication" mkdir "C:\Temp\EmbeddedProjects\Communication"
if not exist "C:\Temp\EmbeddedProjects\Control" mkdir "C:\Temp\EmbeddedProjects\Control"

echo.
echo Creating sensor projects...
generate_project.cmd TempSensor 32MZ1024EFH064 "C:\Temp\EmbeddedProjects\Sensors"
generate_project.cmd PressureSensor 32MZ2048EFH064 "C:\Temp\EmbeddedProjects\Sensors"

echo.
echo Creating communication projects...
generate_project.cmd UART_Gateway 32MZ2048EFH064 "C:\Temp\EmbeddedProjects\Communication"
generate_project.cmd CAN_Bridge 32MZ1024EFH064 "C:\Temp\EmbeddedProjects\Communication" mikroc

echo.
echo Creating control projects...
generate_project.cmd PID_Controller 32MZ2048EFH064 "C:\Temp\EmbeddedProjects\Control"
generate_project.cmd ServoDriver 32MZ1024EFH064 "C:\Temp\EmbeddedProjects\Control" mikroc

echo ===============================================
echo Testing different generator backends...
echo ===============================================

echo.
echo Testing direct C# generator...
dotnet run --project csharp\generate_project.csproj -- CSharpTest 32MZ1024EFH064

echo.
echo Testing Python generator (if available)...
python generate_project.py PythonTest 32MZ2048EFH064 2>nul
if errorlevel 1 echo Python generator not available

echo.
echo Testing Shell script generator (if available)...
bash generate_project.sh ShellTest 32MZ1024EFH064 2>nul
if errorlevel 1 echo Shell script generator not available

echo ===============================================
echo Advanced Example Complete!
echo ===============================================
echo.
echo Projects created:
echo - Current directory: LED_Controller, DataLogger, MotorControl
echo - C:\Temp\EmbeddedProjects\Sensors: TempSensor, PressureSensor
echo - C:\Temp\EmbeddedProjects\Communication: UART_Gateway, CAN_Bridge
echo - C:\Temp\EmbeddedProjects\Control: PID_Controller, ServoDriver
echo - Generator tests: CSharpTest, PythonTest, ShellTest
echo.
echo All projects are ready for development!
echo Open any project folder in VS Code to start coding.
echo.
pause
