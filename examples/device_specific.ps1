# Device-Specific Examples for PIC32MZ Project Generator
# PowerShell Script Examples

Write-Host "=================================================="
Write-Host "PIC32MZ Project Generator - Device-Specific Examples"
Write-Host "=================================================="
Write-Host ""

Write-Host "This script creates projects optimized for different PIC32MZ devices:"
Write-Host "- 32MZ1024EFH064 (1MB Flash, 512KB RAM)"
Write-Host "- 32MZ2048EFH064 (2MB Flash, 512KB RAM)"
Write-Host "- Various application scenarios"
Write-Host ""
Read-Host "Press Enter to continue"

# Change to parent directory
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "=================================================="
Write-Host "Creating projects for 32MZ1024EFH064 (1MB Flash)..."
Write-Host "=================================================="

Write-Host ""
Write-Host "1. Simple IoT Sensor Node (low memory footprint)..."
.\generate_project.cmd IoT_SensorNode 32MZ1024EFH064

Write-Host ""
Write-Host "2. UART Communication Hub..."
.\generate_project.cmd UART_CommHub 32MZ1024EFH064

Write-Host ""
Write-Host "3. Basic LED Controller with MikroC support..."
.\generate_project.cmd LED_BasicController 32MZ1024EFH064 . mikroc

Write-Host "=================================================="
Write-Host "Creating projects for 32MZ2048EFH064 (2MB Flash)..."
Write-Host "=================================================="

Write-Host ""
Write-Host "1. Advanced Data Logger (large storage needs)..."
.\generate_project.cmd Advanced_DataLogger 32MZ2048EFH064

Write-Host ""
Write-Host "2. Multi-Protocol Gateway..."
.\generate_project.cmd MultiProtocol_Gateway 32MZ2048EFH064

Write-Host ""
Write-Host "3. Complex Motor Control System with MikroC..."
.\generate_project.cmd Complex_MotorControl 32MZ2048EFH064 . mikroc

Write-Host "=================================================="
Write-Host "Creating Application-Specific Projects..."
Write-Host "=================================================="

# Create application-specific directory
if (!(Test-Path "C:\Temp\PIC32MZ_Applications")) {
    New-Item -ItemType Directory -Path "C:\Temp\PIC32MZ_Applications" -Force
}

Write-Host ""
Write-Host "1. Industrial Automation Controller..."
.\generate_project.cmd Industrial_Automation 32MZ2048EFH064 "C:\Temp\PIC32MZ_Applications"

Write-Host ""
Write-Host "2. Smart Home Hub..."
.\generate_project.cmd SmartHome_Hub 32MZ2048EFH064 "C:\Temp\PIC32MZ_Applications" mikroc

Write-Host ""
Write-Host "3. Medical Device Controller..."
.\generate_project.cmd Medical_Device 32MZ1024EFH064 "C:\Temp\PIC32MZ_Applications"

Write-Host ""
Write-Host "4. Automotive CAN Gateway..."
.\generate_project.cmd Automotive_CAN_Gateway 32MZ2048EFH064 "C:\Temp\PIC32MZ_Applications" mikroc

Write-Host ""
Write-Host "5. Wireless Communication Node..."
.\generate_project.cmd Wireless_CommNode 32MZ1024EFH064 "C:\Temp\PIC32MZ_Applications"

Write-Host "=================================================="
Write-Host "Device-Specific Examples Complete!"
Write-Host "=================================================="
Write-Host ""
Write-Host "Projects created for 32MZ1024EFH064 (1MB Flash):"
Write-Host "- IoT_SensorNode (optimized for low memory)"
Write-Host "- UART_CommHub (basic communication)"
Write-Host "- LED_BasicController (with MikroC support)"
Write-Host ""
Write-Host "Projects created for 32MZ2048EFH064 (2MB Flash):"
Write-Host "- Advanced_DataLogger (large data handling)"
Write-Host "- MultiProtocol_Gateway (complex protocols)"
Write-Host "- Complex_MotorControl (with MikroC support)"
Write-Host ""
Write-Host "Application-specific projects in C:\Temp\PIC32MZ_Applications:"
Write-Host "- Industrial_Automation"
Write-Host "- SmartHome_Hub (with MikroC)"
Write-Host "- Medical_Device"
Write-Host "- Automotive_CAN_Gateway (with MikroC)"
Write-Host "- Wireless_CommNode"
Write-Host ""
Write-Host "Each project is configured with appropriate device settings!"
Write-Host "Check the generated Makefiles for device-specific configurations."
Write-Host ""
Read-Host "Press Enter to exit"
