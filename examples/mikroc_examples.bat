@echo off
:: MikroC Compatibility Examples for PIC32MZ Project Generator
:: Demonstrates bootloader-compatible project creation

echo =====================================================
echo PIC32MZ Project Generator - MikroC Compatibility Examples
echo =====================================================
echo.

echo This script creates projects with MikroC bootloader compatibility:
echo - Includes custom startup files (startup.S)
echo - Compatible with MikroC bootloader systems
echo - Proper memory layout for bootloader applications
echo - Custom C runtime initialization (crt0.c)
echo.
pause

cd /d "%~dp0.."

echo =====================================================
echo Creating MikroC-compatible projects...
echo =====================================================

echo.
echo 1. Creating MikroC Bootloader Application...
generate_project.cmd MikroC_BootloaderApp 32MZ1024EFH064 . mikroc

echo.
echo 2. Creating MikroC Industrial Controller...
generate_project.cmd MikroC_IndustrialCtrl 32MZ2048EFH064 . mikroc

echo.
echo 3. Creating MikroC Communication Gateway...
generate_project.cmd MikroC_CommGateway 32MZ1024EFH064 . mikroc

echo =====================================================
echo Creating organized MikroC project structure...
echo =====================================================

if not exist "C:\Temp\MikroC_Projects" mkdir "C:\Temp\MikroC_Projects"
if not exist "C:\Temp\MikroC_Projects\Bootloader_Apps" mkdir "C:\Temp\MikroC_Projects\Bootloader_Apps"
if not exist "C:\Temp\MikroC_Projects\Legacy_Ports" mkdir "C:\Temp\MikroC_Projects\Legacy_Ports"

echo.
echo Creating bootloader applications...
generate_project.cmd MikroC_SerialBootloader 32MZ1024EFH064 "C:\Temp\MikroC_Projects\Bootloader_Apps" mikroc
generate_project.cmd MikroC_CANBootloader 32MZ2048EFH064 "C:\Temp\MikroC_Projects\Bootloader_Apps" mikroc
generate_project.cmd MikroC_EthernetBootloader 32MZ2048EFH064 "C:\Temp\MikroC_Projects\Bootloader_Apps" mikroc

echo.
echo Creating legacy port projects...
generate_project.cmd MikroC_LegacyPort1 32MZ1024EFH064 "C:\Temp\MikroC_Projects\Legacy_Ports" mikroc
generate_project.cmd MikroC_LegacyPort2 32MZ2048EFH064 "C:\Temp\MikroC_Projects\Legacy_Ports" mikroc

echo =====================================================
echo Verifying MikroC compatibility features...
echo =====================================================

echo.
echo Checking MikroC_BootloaderApp project structure...
if exist "MikroC_BootloaderApp\srcs\startup\startup.S" (
    echo ✓ Custom startup file created: startup.S
) else (
    echo ✗ Missing startup.S file
)

if exist "MikroC_BootloaderApp\srcs\startup" (
    echo ✓ Startup directory created
) else (
    echo ✗ Missing startup directory
)

echo.
echo Displaying startup file contents:
echo ----------------------------------------
if exist "MikroC_BootloaderApp\srcs\startup\startup.S" (
    type "MikroC_BootloaderApp\srcs\startup\startup.S" | findstr /n "vector_0\|startup\|main"
)

echo =====================================================
echo Testing different devices with MikroC support...
echo =====================================================

echo.
echo Creating projects for various PIC32MZ devices with MikroC...
generate_project.cmd MikroC_Test_1024 32MZ1024EFH064 . mikroc
generate_project.cmd MikroC_Test_2048 32MZ2048EFH064 . mikroc

echo =====================================================
echo MikroC Compatibility Examples Complete!
echo =====================================================
echo.
echo Projects created with MikroC support:
echo - Current directory:
echo   * MikroC_BootloaderApp (32MZ1024EFH064)
echo   * MikroC_IndustrialCtrl (32MZ2048EFH064)
echo   * MikroC_CommGateway (32MZ1024EFH064)
echo   * MikroC_Test_1024 (32MZ1024EFH064)
echo   * MikroC_Test_2048 (32MZ2048EFH064)
echo.
echo - C:\Temp\MikroC_Projects\Bootloader_Apps:
echo   * MikroC_SerialBootloader (32MZ1024EFH064)
echo   * MikroC_CANBootloader (32MZ2048EFH064)
echo   * MikroC_EthernetBootloader (32MZ2048EFH064)
echo.
echo - C:\Temp\MikroC_Projects\Legacy_Ports:
echo   * MikroC_LegacyPort1 (32MZ1024EFH064)
echo   * MikroC_LegacyPort2 (32MZ2048EFH064)
echo.
echo All projects include:
echo ✓ Custom startup files (startup.S)
echo ✓ MikroC bootloader compatibility
echo ✓ Proper memory layout
echo ✓ Ready for bootloader deployment
echo.
echo Open any project in VS Code and check the srcs/startup folder!
echo.
pause
