#!/usr/bin/env python3
"""
PIC32MZ XC32 Project Generator
Automatically creates a complete embedded project structure with cross-platform Makefiles
"""

import os
import sys
import argparse
from pathlib import Path
# from makefile_utils import create_root_makefile


class PIC32ProjectGenerator:
    def __init__(self):
        self.project_name = ""
        self.device = "32MZ1024EFH064"
        self.project_root = ""

    def create_directory_structure(self, include_startup=False):
        """Create the simple directory structure - first level only"""
        dirs = [
            "srcs",
            "incs",
            "objs",
            "bins",
            "other",
            "docs"
        ]

        # Add startup directory if mikroc option is enabled
        if include_startup:
            dirs.extend([
                "srcs/startup"
            ])

        for dir_path in dirs:
            full_path = os.path.join(self.project_root, dir_path)
            Path(full_path).mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {full_path}")
        return dirs

# Copy the root makefile to the project
    def copy_root_makefile(self):
        """Copy root files to the project structure. Specifically, copy Makefile_Root from the dependancies folder one level up from this script's directory to the project root folder as Makefile. Also copy README.md and LICENSE if present in this script's directory."""
        import shutil
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
        dependancies_dir = os.path.join(parent_dir, 'dependancies')

        # Copy Makefile_Root from dependancies as Makefile in project root
        makefile_src = os.path.join(dependancies_dir, 'Makefile_Root')
        makefile_dst = os.path.join(self.project_root, 'Makefile')
        if os.path.exists(makefile_src):
            if not os.path.exists(makefile_dst):
                shutil.copyfile(makefile_src, makefile_dst)
                print(f"Copied {makefile_src} to {makefile_dst}")
            else:
                print(f"File {makefile_dst} already exists, skipping.")
        else:
            print(f"Source Makefile_Root not found at {makefile_src}")

    # Copy the source makefile from dependancies folder to root/srcs folder
    def copy_srcs_makefile(self):
        """Copy srcs maefile to the project srcs folder from dependancies folder."""
        import shutil
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
        dependancies_dir = os.path.join(parent_dir, 'dependancies')

        # copy the Makefile_Srcs from dependancies to srcs/ folder
        makefile_src = os.path.join(dependancies_dir, 'Makefile_Srcs')
        makefile_dst = os.path.join(self.project_root, 'srcs', 'Makefile')
        if os.path.exists(makefile_src):
            if not os.path.exists(makefile_dst):
                shutil.copyfile(makefile_src, makefile_dst)
                print(f"Copied {makefile_src} to {makefile_dst}")
            else:
                print(f"File {makefile_dst} already exists, skipping.")
        else:
            print(f"Source Makefile_Srcs not found at {makefile_src}")

    # If the --mikroc flag has been set then copy then create the startup folder and copy the startup.S file to srcs folder
    def copy_startup_file(self):
        """create a startup folder under srcs and copy the startup.S file from dependancies to the new startup folder."""
        import shutil
        startup_src = os.path.dirname(os.path.abspath(__file__))
        startup_dst = os.path.join(self.project_root, 'srcs', 'startup')
        if not os.path.exists(startup_dst):
            os.makedirs(startup_dst)
            print(f"Created directory: {startup_dst}")

        startup_file_src = os.path.join(startup_src, 'startup.S')
        startup_file_dst = os.path.join(startup_dst, 'startup.S')
        if os.path.exists(startup_file_src):
            if not os.path.exists(startup_file_dst):
                shutil.copyfile(startup_file_src, startup_file_dst)
                print(f"Copied {startup_file_src} to {startup_file_dst}")
            else:
                print(f"File {startup_file_dst} already exists, skipping.")
        else:
            print(f"Source startup.S not found at {startup_file_src}")

    def create_main_c(self):
        """Create a main.c file in srcs/ with a template similar to the C# version."""
        srcs_dir = os.path.join(self.project_root, "srcs")
        os.makedirs(srcs_dir, exist_ok=True)
        main_c_path = os.path.join(srcs_dir, "main.c")
        if os.path.exists(main_c_path):
            print(f"File {main_c_path} already exists, skipping.")
            return
        content = f"""/*****************************************************************************
  Main Source File

  Company:
    Your Company Name

  File Name:
    main.c

  Summary:
    This file contains the \"main\" function for {self.project_name}.

  Description:
    This file contains the \"main\" function for the project.
    Simple bare-metal main function without system initialization dependencies.
 ******************************************************************************/

// *****************************************************************************
// Section: Included Files
// *****************************************************************************

#include <stddef.h>                     // Defines NULL
#include <stdbool.h>                    // Defines true
#include <stdlib.h>                     // Defines EXIT_FAILURE
#include <stdint.h>                     // Defines uint32_t, uintptr_t

// *****************************************************************************
// Variables
// *****************************************************************************

// *****************************************************************************
// Section: Main Entry Point
// *****************************************************************************

int main ( void )
{{
    // Initialize your hardware/peripherals here
    // Example: GPIO configuration, clock setup, etc.
    
    while ( true )
    {{
        // Your main application code here
        // Example: toggle LED, read sensors, communicate, etc.
    }}

    /* Execution should not come here during normal operation */
    return ( EXIT_FAILURE );
}}

/*****************************************************************************
 End of File
*/
"""
        with open(main_c_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {main_c_path}")


def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(
        description="PIC32MZ XC32 Project Generator")
    parser.add_argument("projname", help="Name of the project to generate")
    parser.add_argument("-d", "--device", default="32MZ1024EFH064",
                        help="PIC32MZ device (default: 32MZ1024EFH064)")
    parser.add_argument("-o", "--output", default=".",
                        help="Root directory where project folder will be created (default: current directory)")
    parser.add_argument("--mikroc", action="store_false",
                        help="Include startup files for MikroC compatibility (optional)")

    args = parser.parse_args()

    # Set up project generator
    generator = PIC32ProjectGenerator()
    generator.project_name = args.projname
    generator.device = args.device
    generator.project_root = os.path.abspath(
        os.path.join(args.output, args.projname))

    print("PIC32MZ Project Generator")
    print("==========================")
    print(f"Project Name: {generator.project_name}")
    print(f"Device: {generator.device}")
    print(f"Root Directory: {args.output}")
    print(f"Project Location: {generator.project_root}")
    if args.mikroc:
        print("MikroC support: ENABLED")
    print()

    try:
        generator.create_directory_structure(include_startup=args.mikroc)
        generator.copy_root_makefile()
        generator.copy_srcs_makefile()
        if args.mikroc:
            generator.copy_startup_file()
        generator.create_main_c()
        # Add more method calls as needed, e.g. generator.create_root_makefile(), etc.
        print(
            f"\n✅ Project '{generator.project_name}' generated successfully!")
        print(f"📁 Location: {generator.project_root}")
    except Exception as ex:
        print(f"Error generating project: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()
