@echo off
setlocal enabledelayedexpansion
:: Basic Usage Examples for PIC32MZ Project Generator
:: Windows Batch Script Examples
echo For CSharp examples, please run the CSharp script using = csharp.
echo ==============================================
echo For python examples, please run the Python script using = python.
echo ==============================================
set /p LANGUAGE="Choose language (csharp or batch): "
if /i "%LANGUAGE%"=="csharp" (
    echo ==============================================
    echo PIC32MZ Project Generator - CSharp Basic project Examples
    echo ==============================================
    echo.
    goto :csharp_examples
) else if /i "%LANGUAGE%"=="python" (
    echo ==============================================
    echo PIC32MZ Project Generator - Python Basic project Examples
    echo ==============================================
    echo.
    goto :python_examples
) else if /i "%LANGUAGE%"=="batch" (
    echo ==============================================
    echo PIC32MZ Project Generator - batch Basic Usage Examples
    echo ==============================================
    echo.
    goto :batch_examples
) else (
    echo Invalid language choice. Exiting...
    exit /b 1
)   


::=================================================
::CSharp section
::=================================================
:csharp_examples
echo ==============================================
echo PIC32MZ Project Generator - CSharp Basic project Examples
echo ==============================================
echo.

echo Example 1: Create project in current directory
echo Command: generate_cs_project.exe MyBasicProject
echo.
pause

echo Example 2: Create project with specific device
echo Command: generate_project.exe MyProject 32MZ2048EFH064
echo.
pause

echo Example 3: Create project in custom directory
echo Command: generate_project.exe MyProject -d 32MZ1024EFH064 -o C:\Projects
echo.
pause

echo Example 4: Create project with MikroC support
echo Command: generate_project.exe MyProject -d 32MZ1024EFH064 -o C:\Projects mikroc
echo.
pause

echo Example 5: Run csharp example
echo Command: generate_cs_project.exe MyCSharpProject -d 32MZ1024EFH064 -o C:\Temp --mikroc
echo.


color 0A
echo ==============================================
echo Choose an example to run:
echo ==============================================

echo 1. Basic project (current directory).
echo 2. Basic project default device (current directory , 32MZ2048EFH064).
echo 3. Custom directory custom project name (C:\Temp\CustomName).
echo 4. Custom directory custom project name custom device (32MZ1024EFH064).
echo 5. Custom directory custom project name custom device (32MZ1024EFH064) with MikroC support.
echo 6. Exit
echo.

set /p choice="Enter your choice (1-5): "
color 07

if "%choice%"=="1" (
    echo Running: generate_project.exe ExampleBasic
    cd /d "%~dp0.." && bins\Debug\net6.0\generate_project.exe ExampleBasic
) else if "%choice%"=="2" ('
    echo Running: generate_project.exe ExampleDevice -d 32MZ2048EFH064 -o .
    cd /d "%~dp0.." && bins\Debug\net6.0\generate_project.exe ExampleDevice -d 32MZ2048EFH064 -o .
) else if "%choice%"=="3" (
:: Running: generate_project.exe custom name custom directory
:project_name_prompt
set /p PROJECT_NAME="Enter project name: "
echo ProjectName = !PROJECT_NAME!
if "!PROJECT_NAME!"=="" (
    echo Project name cannot be empty.
    goto :project_name_prompt
)

set /p CUSTOM_DIR="Enter directory (leave blank for C:\Temp\!PROJECT_NAME!): "
if "!CUSTOM_DIR!"=="" (
    echo No directory specified!
    set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
    echo Using default directory: !CUSTOM_DIR!
) else (
    echo Directory specified, using !CUSTOM_DIR!.
)
if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
cd /d "%~dp0..\csharp\bin\Debug\net6.0"
echo Running: generate_project.exe "!PROJECT_NAME!" -d 32MZ1024EFH064 -o "!CUSTOM_DIR!"
generate_project.exe "!PROJECT_NAME!" -d 32MZ1024EFH064 -o "!CUSTOM_DIR!"
) else if "%choice%"=="4" ('
::Custom directory custom project name custom device (32MZ1024EFH064).
  :project_name_prompt
    set /p PROJECT_NAME="Enter project name: "
    if "!PROJECT_NAME!"=="" (
        echo Project name cannot be empty.
        goto :project_name_prompt
    )
    echo ProjectName = !PROJECT_NAME!
    ::Set the directory for the project
    set /p CUSTOM_DIR="Enter directory (leave blank for C:\Temp\!PROJECT_NAME!): "
    if "!CUSTOM_DIR!"=="" (
        echo No directory specified!
        set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
        echo Using default directory: !CUSTOM_DIR!
    ) else (
        echo Directory specified, using !CUSTOM_DIR!.
    )
    if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
    :: Set the device name for the project
    set /p DEVICE_NAME="Enter device name (default is 32MZ1024EFH064): "
    if "!DEVICE_NAME!"=="" (
        set "DEVICE_NAME=32MZ1024EFH064"
        echo Using default device: !DEVICE_NAME!
    )else (
        echo Device specified, using !DEVICE_NAME!.
    )
    :: goto the project path of the script that runs the project generator
    cd /d "%~dp0..\csharp\bin\Debug\net6.0"
    echo Running: generate_project.exe !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR!
    generate_project.exe !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR!
) else if "%choice%"=="5" (
:: Custom directory custom project name custom device (32MZ1024EFH064) with MikroC support.
 :project_name_prompt
    set /p PROJECT_NAME="Enter project name: "
    if "!PROJECT_NAME!"=="" (
        echo Project name cannot be empty.
        goto :project_name_prompt
    )
    echo ProjectName = !PROJECT_NAME!
    ::Set the directory for the project
    set /p CUSTOM_DIR="Enter directory (leave blank for C:\Temp\!PROJECT_NAME!): "
    if "!CUSTOM_DIR!"=="" (
        echo No directory specified!
        set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
        echo Using default directory: !CUSTOM_DIR!
    ) else (
        echo Directory specified, using !CUSTOM_DIR!.
    )
    if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
    :: Set the device name for the project
    :: If the user does not specify a device, use the default 32MZ1024EFH064
    set /p DEVICE_NAME="Enter device name (default is 32MZ1024EFH064): "
    if "!DEVICE_NAME!"=="" (
        set "DEVICE_NAME=32MZ1024EFH064"
        echo Using default device: !DEVICE_NAME!
    )else (
        echo Device specified, using !DEVICE_NAME!.
    )
    :: goto the project path of the script that runs the project generator
    cd /d "%~dp0..\csharp\bin\Debug\net6.0"
    echo Running: generate_project.exe !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR! --mikroc
    generate_project.exe !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR! --mikroc
) else if "%choice%"=="6" (
    goto exiting
) else (
    echo Invalid choice. Please run the script again.
)

echo.
echo Example completed! Check the generated project folder.
goto :exiting




::=================================================
::Pytho section
::=================================================
:python_examples
echo ==============================================
echo PIC32MZ Project Generator - Python Basic project Examples
echo ==============================================
echo.

echo Example 1: Create project in current directory
echo Command: python generate_project.py  MyBasicProject
echo.
pause

echo Example 2: Create project with specific device
echo Command: python generate_project.py MyProject 32MZ2048EFH064
echo.
pause

echo Example 3: Create project in custom directory
echo Command: python generate_project.py MyProject -d 32MZ1024EFH
echo.
pause

echo Example 4: Create project with MikroC support
echo Command: python generate_project.py MyProject -d 32MZ1024EFH064 -o C:\Projects 
echo.
pause

echo Example 5: Run csharp example
echo Command: python generate_cs_project.py MyCSharpProject -d 32MZ1024EFH064 -o C:\Temp --mikroc
echo.

color 0A
echo ==============================================
echo Choose an example to run:
echo ==============================================
echo 1. Basic project (current directory).
echo 2. Basic project default device (current directory , 32MZ2048EFH064).
echo 3. Custom directory custom project name (C:\Temp\CustomName).
echo 4. Custom directory custom project name custom device (32MZ1024EFH064).
echo 5. Custom directory custom project name custom device (32MZ1024EFH064) with MikroC support.
echo 6. Exit
echo.
set /p choice="Enter your choice (1-5): "

color 07
if "%choice%"=="1" (
    :: Running: python generate_project.py ExampleBasic
    echo Running: python generate_project.py ExampleBasic
    cd /d "%~dp0..\python" && python generate_project.py ExampleBasic
) else if "%choice%"=="2" (
    :: Running: python generate_project.py ExampleDevice -d 32MZ2048EFH064 -o .
    echo Running: python generate_project.py ExampleDevice -d 32MZ2048EFH064 -o .
    cd /d "%~dp0..\python" && python generate_project.py ExampleDevice -d 32MZ2048EFH064 -o .
) else if "%choice%"=="3" (
    :: Running: python generate_project.py custom name custom directory
    :project_name_prompt
    set /p PROJECT_NAME="Enter project name: "
    if "!PROJECT_NAME!"=="" (
        echo Project name cannot be empty.
        goto :project_name_prompt
    )
    echo ProjectName = !PROJECT_NAME!
    set /p CUSTOM_DIR="Enter directory (leave blank for C:\Temp\!PROJECT_NAME!): "
    if "!CUSTOM_DIR!"=="" (
        echo No directory specified!
        set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
        echo Using default directory: !CUSTOM_DIR!
    ) else (
        echo Directory specified, using !CUSTOM_DIR!.
    )
    if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
    echo Running: python generate_project.py !PROJECT_NAME! -o !CUSTOM_DIR!
    cd /d "%~dp0..\python" && python generate_project.py !PROJECT_NAME! -o !CUSTOM_DIR!
) else if "%choice%"=="4" (
    :: Custom directory custom project name custom device (32MZ1024EFH064).
    :project_name_prompt
    set /p PROJECT_NAME="Enter project name: "
    if "!PROJECT_NAME!"=="" (
        echo Project name cannot be empty.
        goto :project_name_prompt
    )
    echo ProjectName = !PROJECT_NAME!
    set /p CUSTOM_DIR="Enter directory (leave blank for C:\Temp\!PROJECT_NAME!): "
    if "!CUSTOM_DIR!"=="" (
        echo No directory specified!
        set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
        echo Using default directory: !CUSTOM_DIR!
    ) else (
        echo Directory specified, using !CUSTOM_DIR!.
    )
    if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
    set /p DEVICE_NAME="Enter device name (default is 32MZ1024EFH064): "
    if "!DEVICE_NAME!"=="" (
        set "DEVICE_NAME=32MZ1024EFH064"
        echo Using default device: !DEVICE_NAME!
    ) else (
        echo Device specified, using !DEVICE_NAME!.
    )
    echo Running: python generate_project.py !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR!
    cd /d "%~dp0..\python" && python generate_project.py !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR!
) else if "%choice%"=="5" (
    :: Custom directory custom project name custom device (32MZ1024EFH064) with MikroC support.
    :project_name_prompt
    set /p PROJECT_NAME="Enter project name: "
    if "!PROJECT_NAME!"=="" (
        echo Project name cannot be empty.
        goto :project_name_prompt
    )
    echo ProjectName = !PROJECT_NAME!
    set /p CUSTOM_DIR="Enter directory (leave blank for C:\Temp\!PROJECT_NAME!): "
    if "!CUSTOM_DIR!"=="" (
        echo No directory specified!
        set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
        echo Using default directory: !CUSTOM_DIR!
    ) else (
        echo Directory specified, using !CUSTOM_DIR!.
    )
    if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
    set /p DEVICE_NAME="Enter device name (default is 32MZ1024EFH064): "
    if "!DEVICE_NAME!"=="" (
        set "DEVICE_NAME=32MZ1024EFH064"
        echo Using default device: !DEVICE_NAME!
    ) else (
        echo Device specified, using !DEVICE_NAME!.
    )
    :: goto the project path of the script that runs the project generator
    echo Running: python generate_project.py !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR! --mikroc
    cd /d "%~dp0..\python" && python generate_project.py !PROJECT_NAME! -d !DEVICE_NAME! -o !CUSTOM_DIR! --mikroc
) else if "%choice%"=="6" (
    goto exiting
) else (
    echo Invalid choice. Please run the script again.
)   
echo.
echo Example completed! Check the generated project folder.

goto :exiting


::==================================================
::Shell section
::==================================================
:batch_examples
setlocal enabledelayedexpansion
echo.
echo ==============================================
echo PIC32MZ Project Generator - Batch Basic project Examples
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
echo Example 5: Run csharp example
echo Command: generate_cs_project.cmd MyCSharpProject 32MZ1024EFH
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
    bash "%~dp0..\shell\generate_project.sh" . ExampleBasic
) else if "%choice%"=="2" (
    echo Running: generate_project.cmd ExampleDevice 32MZ2048EFH064
    bash "%~dp0..\shell\generate_project.sh" ExampleDevice . 32MZ2048EFH064
) else if "%choice%"=="3" (
    :project_name_prompt_batch
    set /p PROJECT_NAME="Enter project name: "
    if "!PROJECT_NAME!"=="" (
        echo Project name cannot be empty.
        goto :project_name_prompt_batch
    )
    set /p CUSTOM_DIR="Enter directory (default is C:\Temp\!PROJECT_NAME!): "
    if "!CUSTOM_DIR!"=="" set "CUSTOM_DIR=C:\Temp\!PROJECT_NAME!"
    if not exist "!CUSTOM_DIR!" mkdir "!CUSTOM_DIR!"
    :: Convert Windows path to WSL path for bash (force lowercase drive letter)
    set "WSL_CUSTOM_DIR=!CUSTOM_DIR:\=/%!"
    set "WSL_CUSTOM_DIR=/mnt/!WSL_CUSTOM_DIR:~0,1!!WSL_CUSTOM_DIR:~1!"
    set "WSL_CUSTOM_DIR=!WSL_CUSTOM_DIR:/mnt/C=/mnt/c!"
    set "SCRIPT_PATH=%~dp0..\shell\generate_project.sh"
    set "WSL_SCRIPT_PATH=!SCRIPT_PATH:\=/%!"
    set "WSL_SCRIPT_PATH=/mnt/!WSL_SCRIPT_PATH:~0,1!!WSL_SCRIPT_PATH:~1!"
    set "WSL_SCRIPT_PATH=!WSL_SCRIPT_PATH:/mnt/C=/mnt/c!"
    if exist "!SCRIPT_PATH!" (
        echo Running: generate_project.sh !PROJECT_NAME! 32MZ1024EFH064 !CUSTOM_DIR!
        bash "!WSL_SCRIPT_PATH!" !PROJECT_NAME! 32MZ1024EFH064 "!WSL_CUSTOM_DIR!"
    ) else (
        echo ERROR: Script not found: !SCRIPT_PATH!
    )
    endlocal
    pause
) else if "%choice%"=="4" (
    echo Running: generate_project.sh ExampleMikroC 32MZ1024EFH064 C:\Temp mikroc
    bash "%~dp0..\shell\generate_project.sh" ExampleMikroC 32MZ1024EFH064 C:\Temp mikroc
) else if "%choice%"=="5" (
   goto :exiting
) else (
    echo Invalid choice. Please run the script again.
)
echo.
echo Example completed! Check the generated project folder.
echo.
echo ==============================================

:exiting
    echo Exiting...
    exit /b