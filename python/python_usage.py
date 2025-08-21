#!/usr/bin/env python3
"""
Python Script Usage Examples for PIC32MZ Project Generator
Demonstrates direct usage of the generate_project.py script
"""

import os
import sys
import subprocess
import platform


def print_header():
    print("=" * 55)
    print("PIC32MZ Project Generator - Python Script Examples")
    print("=" * 55)
    print()


def print_section(title):
    print("-" * 50)
    print(f"{title}")
    print("-" * 50)
    print()


def run_command(cmd, description):
    print(f"Example: {description}")
    print(f"Command: {cmd}")
    print()

    # Ask user if they want to run it
    response = input("Run this example? (y/n/q to quit): ").lower()
    if response == 'q':
        print("Exiting...")
        sys.exit(0)
    elif response == 'y':
        try:
            # Change to parent directory
            parent_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            os.chdir(parent_dir)

            # Run the command
            result = subprocess.run(
                cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Success!")
                print(result.stdout)
            else:
                print("✗ Error:")
                print(result.stderr)
        except Exception as e:
            print(f"✗ Failed to run command: {e}")
    else:
        print("Skipped.")
    print()


def check_python():
    print_section("Python Environment Check")

    # Check Python version
    python_version = sys.version_info
    print(
        f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

    if python_version >= (3, 6):
        print("✓ Python version is compatible (3.6+)")
    else:
        print("✗ Python version too old. Please upgrade to Python 3.6 or later")
        return False

    # Check if script exists
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(parent_dir, "generate_project.py")

    if os.path.exists(script_path):
        print(f"✓ Found generate_project.py at: {script_path}")
    else:
        print(f"✗ Cannot find generate_project.py at: {script_path}")
        return False

    print(f"Operating System: {platform.system()}")
    print()
    return True


def show_basic_examples():
    print_section("Basic Python Script Usage")

    print("The generate_project.py script accepts the following arguments:")
    print(
        "python generate_project.py <project_name> [device] [output_dir] [mikroc]")
    print()

    # Basic examples
    examples = [
        ("python generate_project.py MyBasicProject",
         "Create project in current directory"),

        ("python generate_project.py MyDevice32MZ2048 32MZ2048EFH064",
         "Create project with specific device"),

        ("python generate_project.py MyCustomProject 32MZ1024EFH064 ./projects",
         "Create project in custom directory"),

        ("python generate_project.py MyMikroCProject 32MZ1024EFH064 . mikroc",
         "Create project with MikroC bootloader support"),
    ]

    for cmd, desc in examples:
        run_command(cmd, desc)


def show_advanced_examples():
    print_section("Advanced Python Script Usage")

    print("Advanced scenarios using Python script directly:")
    print()

    # Create projects directory
    projects_dir = "./PythonProjects"
    if not os.path.exists(projects_dir):
        try:
            os.makedirs(projects_dir)
            print(f"Created projects directory: {projects_dir}")
        except:
            projects_dir = "./temp_projects"
            print(f"Using fallback directory: {projects_dir}")

    advanced_examples = [
        ("python generate_project.py IoT_Sensor 32MZ1024EFH064 ./PythonProjects",
         "IoT sensor project (memory optimized)"),

        ("python generate_project.py DataLogger_Advanced 32MZ2048EFH064 ./PythonProjects",
         "Data logger project (high memory)"),

        ("python generate_project.py MotorControl_MikroC 32MZ2048EFH064 ./PythonProjects mikroc",
         "Motor control with MikroC support"),

        ("python generate_project.py CommHub_Gateway 32MZ1024EFH064 ./PythonProjects",
         "Communication hub project"),
    ]

    for cmd, desc in advanced_examples:
        run_command(cmd, desc)


def show_cross_platform_examples():
    print_section("Cross-Platform Python Examples")

    system = platform.system()
    print(f"Detected OS: {system}")
    print()

    if system == "Windows":
        examples = [
            ("python generate_project.py WindowsProject 32MZ1024EFH064 C:\\Temp\\Projects",
             "Windows-style path"),

            ("python generate_project.py MikroCWindows 32MZ2048EFH064 C:\\Dev\\Embedded mikroc",
             "Windows MikroC project"),
        ]
    else:
        examples = [
            ("python3 generate_project.py UnixProject 32MZ1024EFH064 /tmp/projects",
             "Unix-style path"),

            ("python3 generate_project.py MikroCUnix 32MZ2048EFH064 ~/embedded mikroc",
             "Unix MikroC project"),
        ]

    for cmd, desc in examples:
        run_command(cmd, desc)


def show_batch_creation_example():
    print_section("Batch Project Creation with Python")

    print("Creating multiple projects using Python script:")
    print()

    # Define multiple projects
    projects = [
        ("LED_Controller_Python", "32MZ1024EFH064", "./PythonBatch"),
        ("UART_Gateway_Python", "32MZ2048EFH064", "./PythonBatch"),
        ("SensorHub_Python", "32MZ1024EFH064", "./PythonBatch"),
        ("MikroC_Bootloader_Python", "32MZ2048EFH064", "./PythonBatch", "mikroc"),
    ]

    response = input("Create all batch projects? (y/n): ").lower()
    if response == 'y':
        parent_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        os.chdir(parent_dir)

        for project in projects:
            name, device, output = project[0], project[1], project[2]
            mikroc = project[3] if len(project) > 3 else ""

            cmd = f"python generate_project.py {name} {device} {output}"
            if mikroc:
                cmd += f" {mikroc}"

            print(f"Creating: {name}...")
            print(f"Command: {cmd}")

            try:
                result = subprocess.run(
                    cmd.split(), capture_output=True, text=True)
                if result.returncode == 0:
                    print("✓ Success!")
                else:
                    print("✗ Error:", result.stderr)
            except Exception as e:
                print(f"✗ Failed: {e}")
            print()
    else:
        print("Skipped batch creation.")
    print()


def show_python_integration_examples():
    print_section("Python Integration Examples")

    print("Using Python script in different environments:")
    print()

    environments = [
        ("Virtual Environment",
         "python -m venv myenv && myenv\\Scripts\\activate && python generate_project.py VenvProject",
         "Windows virtual environment"),

        ("Conda Environment",
         "conda create -n pic32 python=3.8 && conda activate pic32 && python generate_project.py CondaProject",
         "Anaconda/Miniconda environment"),

        ("Docker Container",
         "docker run -v .:/workspace -w /workspace python:3.9 python generate_project.py DockerProject",
         "Docker containerized execution"),

        ("CI/CD Pipeline",
         "python generate_project.py CI_Project 32MZ2048EFH064 ./build/projects",
         "Continuous integration usage"),
    ]

    for title, cmd, desc in environments:
        print(f"{title}:")
        print(f"  Description: {desc}")
        print(f"  Command: {cmd}")
        print()


def show_troubleshooting():
    print_section("Python Script Troubleshooting")

    print("Common issues and solutions:")
    print()

    issues = [
        ("Python not found",
         "Install Python 3.6+ from https://python.org/downloads/"),

        ("'python' not recognized",
         "Use 'python3' or 'py' command, or add Python to PATH"),

        ("Permission denied",
         "Run with appropriate permissions or use different output directory"),

        ("Module import errors",
         "Ensure Python installation is complete and not corrupted"),

        ("Path not found errors",
         "Use absolute paths or ensure working directory is correct"),
    ]

    for issue, solution in issues:
        print(f"Issue: {issue}")
        print(f"Solution: {solution}")
        print()


def main():
    print_header()

    # Check Python environment
    if not check_python():
        print("Please fix Python environment issues before proceeding.")
        return

    print("This script demonstrates various ways to use generate_project.py")
    print("Choose what you'd like to explore:")
    print()

    while True:
        print("Options:")
        print("1. Basic Python script examples")
        print("2. Advanced usage scenarios")
        print("3. Cross-platform examples")
        print("4. Batch project creation")
        print("5. Python environment integration")
        print("6. Troubleshooting guide")
        print("7. Exit")
        print()

        choice = input("Enter your choice (1-7): ").strip()
        print()

        if choice == '1':
            show_basic_examples()
        elif choice == '2':
            show_advanced_examples()
        elif choice == '3':
            show_cross_platform_examples()
        elif choice == '4':
            show_batch_creation_example()
        elif choice == '5':
            show_python_integration_examples()
        elif choice == '6':
            show_troubleshooting()
        elif choice == '7':
            print("Thanks for exploring Python script examples!")
            break
        else:
            print("Invalid choice. Please select 1-7.")

        input("Press Enter to continue...")
        print()


if __name__ == "__main__":
    main()
