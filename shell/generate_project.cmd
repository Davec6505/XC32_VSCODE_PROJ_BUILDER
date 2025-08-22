#!/bin/bash
# PIC32MZ Project Generator - Shell Script Version
# Cross-platform project generator for PIC32MZ embedded projects

set -e

echo "PIC32MZ Project Generator - Shell Script Version"
echo "==============================================="

# Default values
PROJECT_NAME=""
DEVICE="32MZ1024EFH064"
OUTPUT_DIR="."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage: $0 <project_name> [device] [root_directory]"
    echo ""
    echo "Arguments:"
    echo "  project_name     Name of the project to generate (required)"
    echo "  device          PIC32MZ device (default: 32MZ1024EFH064)"
    echo "  root_directory  Root directory where project folder will be created (default: current directory)"
    echo ""
    echo "Examples:"
    echo "  $0 MyProject"
    echo "  $0 MyProject 32MZ2048EFH064"
    echo "  $0 MyProject 32MZ1024EFH064 /home/projects"
    echo "  $0 MyProject 32MZ1024EFH064 ~/workspace/embedded"
    echo ""
    echo "The script will create: <root_directory>/<project_name>/"
}

create_directories() {
    local project_root="$1"
    
    echo -e "${BLUE}Creating directory structure...${NC}"
    
    # Create simple directory structure - first level only
    mkdir -p "$project_root"/{srcs,incs,objs,bins,other,docs}
    
    echo -e "${GREEN}✓ Directory structure created${NC}"
}

create_root_makefile() {
    local project_root="$1"
    local project_name="$2"
    local device="$3"
    
    cat > "$project_root/Makefile" << EOF
# Name of the project binary
MODULE    	:= $project_name

# Device configuration
# The device is expected to be a PIC32MZ family device.
DEVICE 		:= $device

# Compiler location and DFP (Device Family Pack) location
# Cross-platform compiler and DFP paths
ifeq (\$(OS),Windows_NT)
    COMPILER_LOCATION := C:/Program Files/Microchip/xc32/v4.60/bin
    DFP_LOCATION := C:/Program Files/Microchip/MPLABX/v6.25/packs
else
    COMPILER_LOCATION := /opt/microchip/xc32/v4.60/bin
    DFP_LOCATION := /opt/microchip/mplabx/v6.25/packs
endif
DFP := \$(DFP_LOCATION)/Microchip/PIC32MZ-EF_DFP/1.4.168

# Simple Unix-style build system
BUILD=make
CLEAN=make clean
BUILD_DIR=make build_dir

all:
	@echo "######  BUILDING   ########"
	cd srcs && \$(BUILD) COMPILER_LOCATION="\$(COMPILER_LOCATION)" DFP_LOCATION="\$(DFP_LOCATION)" DFP="\$(DFP)" DEVICE=\$(DEVICE) MODULE=\$(MODULE)
	@echo "###### BIN TO HEX ########"
	cd bins && "\$(COMPILER_LOCATION)/xc32-bin2hex" \$(MODULE)
	@echo "######  BUILD COMPLETE   ########"

build_dir:
	@echo "#######BUILDING DIRECTORIES FOR OUTPUT BINARIES#######"
	cd srcs && \$(BUILD_DIR)

debug:
	@echo "#######DEBUGGING OUTPUTS#######"
	cd srcs && \$(BUILD) debug COMPILER_LOCATION="\$(COMPILER_LOCATION)" DFP_LOCATION="\$(DFP_LOCATION)" DFP="\$(DFP)" DEVICE=\$(DEVICE) MODULE=\$(MODULE)

platform:
	@echo "#######PLATFORM INFO#######"
	cd srcs && \$(BUILD) platform COMPILER_LOCATION="\$(COMPILER_LOCATION)" DFP_LOCATION="\$(DFP_LOCATION)" DFP="\$(DFP)" DEVICE=\$(DEVICE) MODULE=\$(MODULE)

clean:
	@echo "####### CLEANING OUTPUTS #######"
	cd srcs && \$(CLEAN)
	@echo "####### REMOVING BUILD ARTIFACTS #######"
ifeq (\$(OS),Windows_NT)
	@if exist "bins\\\\*" del /q "bins\\\\*" >nul 2>&1
	@if exist "objs\\\\*" rmdir /s /q "objs" >nul 2>&1 && mkdir "objs" >nul 2>&1
	@if exist "other\\\\*" del /q "other\\\\*" >nul 2>&1
else
	@rm -rf bins/* objs/* other/* 2>/dev/null || true
endif

find-source:
	@echo "####### FINDING SOURCE FILES #######"
ifeq (\$(OS),Windows_NT)
	@powershell -Command "Get-ChildItem -Recurse srcs -Include *.c,*.h | Select-Object -ExpandProperty FullName"
else
	@find srcs -name "*.c" -o -name "*.h"
endif

help:
	@echo "####### HELP #######"
	cd srcs && \$(BUILD) help

.PHONY: all build_dir clean find-source debug platform help
EOF

    echo -e "${GREEN}✓ Root Makefile created${NC}"
}

create_srcs_makefile() {
    local project_root="$1"
    
    # This is a long file, so I'll create it in parts
    cat > "$project_root/srcs/Makefile" << 'EOF'
# DFP (Device Family Pack) configuration
DFP_DIR := $(DFP)
DFP_INCLUDE := $(DFP)/include

# Helper variables for cross-platform compatibility
space := $(empty) $(empty)
comma := ,

# Detect operating system for cross-platform compatibility
ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    MKDIR = if not exist "$(subst /,\,$(1))" mkdir "$(subst /,\,$(1))"
    RMDIR = if exist "$(subst /,\,$(1))" rmdir /s /q "$(subst /,\,$(1))"
    RM = if exist "$(subst /,\,$(1))" del /q "$(subst /,\,$(1))"
    MOVE = if exist "$(subst /,\,$(1))" move "$(subst /,\,$(1))" "$(subst /,\,$(2))"
    PATH_SEP = \\
    NULL_DEVICE = nul
else
    detected_OS := $(shell uname -s)
    MKDIR = mkdir -p $(1)
    RMDIR = rm -rf $(1)
    RM = rm -f $(1)
    MOVE = if [ -f "$(1)" ]; then mv "$(1)" "$(2)"; fi
    PATH_SEP = /
    NULL_DEVICE = /dev/null
endif

# Project directories
ROOT     := ..
OBJ_DIR  := $(ROOT)/objs
INC_DIR  := $(ROOT)/incs
BIN_DIR  := $(ROOT)/bins
SRC_DIR  := $(ROOT)/srcs
OUT_DIR  := $(ROOT)/other

# Source files - dynamically find all .c files
define get_c_files
$(wildcard $(1)/*.c) $(wildcard $(1)/*/*.c) $(wildcard $(1)/*/*/*.c) $(wildcard $(1)/*/*/*/*.c)
endef
SRCS := $(call get_c_files,$(SRC_DIR))
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Assembly files - dynamically find all .S files
define get_s_files
$(wildcard $(1)/*.S) $(wildcard $(1)/*/*.S) $(wildcard $(1)/*/*/*.S) $(wildcard $(1)/*/*/*/*.S)
endef
ASM := $(call get_s_files,$(SRC_DIR))
ASMS := $(ASM:$(SRC_DIR)/%.S=$(OBJ_DIR)/%.o)
OBJS += $(ASMS)

# Compiler and flags
COMPILER  := c99
ifeq ($(COMPILER),c99)
CC := "$(COMPILER_LOCATION)/xc32-gcc"
MCU := -mprocessor=$(DEVICE)
STD := c99
FLAGS := -Werror -Wall -MP -MMD
else
CC := "$(COMPILER_LOCATION)/xc32"
MCU := -mprocessor=$(DEVICE)
STD := c90
endif

# Dynamic include directories
define get_inc_dirs
$(sort $(dir $(wildcard $(1)/*/)) $(dir $(wildcard $(1)/*/*/)) $(dir $(wildcard $(1)/*/*/*/)) $(dir $(wildcard $(1)/*/*/*/*/)))
endef

INC_SUBDIRS := $(call get_inc_dirs,$(INC_DIR))
INC_FLAGS := $(foreach d,$(patsubst %/,%,$(INC_SUBDIRS)),-I"$(d)")
INCS := -I"$(INC_DIR)" $(INC_FLAGS) -I"$(DFP_INCLUDE)"

# Compiler directives
DIRECT_OBJ := $(CC) -g -x c -c $(MCU) -ffunction-sections -fdata-sections -O1 -fno-common \
			$(INCS) $(FLAGS) -MF $(@:.o=.d) -DXPRJ_default=default -mdfp="$(DFP)"

LINKER_SCRIPT := $(DFP)/xc32/$(DEVICE)/p32MZ1024EFH064.ld
DIRECT_LINK := $(CC) $(MCU) -nostartfiles -DXPRJ_default=default -mdfp="$(DFP)" \
			-Wl,--defsym=__MPLAB_BUILD=1,--script="$(LINKER_SCRIPT)",--defsym=_min_heap_size=512,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="$(OUT_DIR)/production.map",--memorysummary,$(OUT_DIR)/memoryfile.xml

DIRECT_ASM := -c -DXPRJ_default=default -Wa,--defsym=__MPLAB_BUILD=1,-MD=$(OBJ_DIR)/startup/startup.o.asm.d,--gdwarf-2 -mdfp="$(DFP)" -MMD -MF $(OBJ_DIR)/startup/startup.o.d

# Build targets
$(BIN_DIR)/$(MODULE): $(OBJS)
	@echo "Building project for $(DEVICE)"
	@echo "Linking object files to create the final executable"
	$(DIRECT_LINK) -o $@ $^ 
	@echo "Build complete. Output is in $(BIN_DIR)"

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@echo "Compiling $< to $@"
	@$(call MKDIR,$(dir $@))
	$(DIRECT_OBJ) $< -o $@
	@echo "Object file created: $@"

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.S
	@echo "Compiling assembly file $< to object file $@"
	@$(call MKDIR,$(dir $@))
	$(CC) $(MCU) $(DIRECT_ASM) -o $@ $<
	@echo "Object file created: $@"

.PHONY: clean build_dir debug help platform

# Get source subdirectories
SRC_DIRS := $(sort $(dir $(wildcard $(SRC_DIR)/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/*/*/)))
SRC_SUBDIRS := $(sort $(filter-out startup/,$(SRC_DIRS:$(SRC_DIR)/%=%)))

build_dir: 
	@echo "Creating build base directories if they do not exist ($(detected_OS))"
	@$(call MKDIR,$(OBJ_DIR))
	@$(call MKDIR,$(BIN_DIR))
	@$(call MKDIR,$(SRC_DIR))
	@$(call MKDIR,$(INC_DIR))
	@$(call MKDIR,$(OUT_DIR))
	@echo "Creating subdirectories in OBJ_DIR and INC_DIR based on SRC_DIR structure"
	@$(call MKDIR,$(OBJ_DIR)/startup)
	@$(foreach subdir,$(SRC_SUBDIRS),$(call MKDIR,$(OBJ_DIR)/$(subdir)) && $(call MKDIR,$(INC_DIR)/$(subdir)) &&) echo "Created peripheral directories"
	@echo "Moving header files from src subdirectories to corresponding inc subdirectories"
	@$(foreach subdir,$(SRC_SUBDIRS),$(foreach header,$(wildcard $(SRC_DIR)/$(subdir)*.h),$(call MOVE,$(header),$(INC_DIR)/$(subdir)) &&)) echo "Headers moved"
	@echo "Build directories created successfully"

debug:
	@echo "Build system debug info ($(detected_OS)):"
	@echo "Source files:"
	@$(foreach src,$(SRCS),echo "  $(src)" &&) echo ""
	@echo "Object files:"
	@$(foreach obj,$(OBJS),echo "  $(obj)" &&) echo ""
	@echo "Include directories:"
	@$(foreach inc,$(subst -I",,$(subst ",,$(INCS))),echo "  -I\"$(inc)\"" &&) echo ""
	@echo "DFP Include path:"
	@echo "  $(DFP_INCLUDE)"

platform:
	@echo "Cross-platform build configuration:"
	@echo "  Detected OS: $(detected_OS)"
	@echo "  Path separator: $(PATH_SEP)"
	@echo "  Null device: $(NULL_DEVICE)"

help:
	@echo "Displaying help information for xc32-gcc"
	xc32-gcc --help

clean:
	@echo "Cleaning up object files and binaries ($(detected_OS))"
	@$(call RM,$(BIN_DIR)/*) 2>$(NULL_DEVICE) || true
	@$(call RMDIR,$(OBJ_DIR)) 2>$(NULL_DEVICE) || true
	@$(call MKDIR,$(OBJ_DIR))
	@$(call RM,$(OUT_DIR)/*) 2>$(NULL_DEVICE) || true
	@echo "Clean complete."
EOF

    echo -e "${GREEN}✓ Srcs Makefile created${NC}"
}

create_template_files() {
    local project_root="$1"
    local project_name="$2"
    local device="$3"
    
    # Create definitions.h
    cat > "$project_root/incs/definitions.h" << EOF
/*******************************************************************************
  System Definitions

  File Name:
    definitions.h

  Summary:
    $project_name system definitions.

  Description:
    This file contains the system-wide prototypes and definitions for $project_name.

 *******************************************************************************/

#ifndef DEFINITIONS_H
#define DEFINITIONS_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

// *****************************************************************************
// *****************************************************************************
// Section: Project Definitions
// *****************************************************************************
// *****************************************************************************

// Add your project-specific definitions here
// Examples:
// #define LED_PIN     1
// #define BUTTON_PIN  2

// *****************************************************************************
// *****************************************************************************
// Section: Function Prototypes
// *****************************************************************************
// *****************************************************************************
#ifdef __cplusplus
extern "C" {
#endif

// Add your function prototypes here

#ifdef __cplusplus
}
#endif

#endif /* DEFINITIONS_H */
EOF

    # Create device.h
    cat > "$project_root/incs/device.h" << EOF
/*******************************************************************************
  Device Configuration Header

  File Name:
    device.h

  Summary:
    Device specific definitions for $project_name

  Description:
    This file contains device specific definitions and includes.
*******************************************************************************/

#ifndef DEVICE_H
#define DEVICE_H

#include <xc.h>
#include <sys/attribs.h>

// Device specific configurations can be added here

#endif /* DEVICE_H */
EOF

    # Create main.c
    cat > "$project_root/srcs/main.c" << EOF
/*******************************************************************************
  Main Source File

  Company:
    Your Company Name

  File Name:
    main.c

  Summary:
    This file contains the "main" function for $project_name.

  Description:
    This file contains the "main" function for the project.
    Simple bare-metal main function without system initialization dependencies.
 *******************************************************************************/

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <stddef.h>                     // Defines NULL
#include <stdbool.h>                    // Defines true
#include <stdlib.h>                     // Defines EXIT_FAILURE
#include <stdint.h>                     // Defines uint32_t, uintptr_t

// *****************************************************************************
// *****************************************************************************
// Variables 
// *****************************************************************************
// *****************************************************************************

// *****************************************************************************
// *****************************************************************************
// Section: Main Entry Point
// *****************************************************************************
// *****************************************************************************

int main ( void )
{
    // Initialize your hardware/peripherals here
    // Example: GPIO configuration, clock setup, etc.
    
    while ( true )
    {
        // Your main application code here
        // Example: toggle LED, read sensors, communicate, etc.
    }

    /* Execution should not come here during normal operation */
    return ( EXIT_FAILURE );
}

/*******************************************************************************
 End of File
*/
EOF

    */
EOF

    # Create README.md
    cat > "$project_root/README.md" << EOF
# $project_name

PIC32MZ Embedded Project using XC32 Compiler

## Device
- **Microcontroller**: $device
- **Compiler**: XC32 v4.60+
- **IDE**: VS Code with Makefile support

## Building

### Windows
\`\`\`bash
make
\`\`\`

### Linux/macOS
\`\`\`bash
make
\`\`\`

## Useful Commands

- \`make\` - Build the project
- \`make clean\` - Clean build artifacts
- \`make debug\` - Show build configuration
- \`make platform\` - Show cross-platform settings
- \`make build_dir\` - Create directory structure
- \`make find-source\` - List all source files
- \`make help\` - Show compiler help

## Cross-Platform Support

This project automatically detects Windows, Linux, and macOS and adjusts build commands accordingly.

Generated by PIC32MZ Project Generator
EOF

    # Create .gitignore
    cat > "$project_root/.gitignore" << EOF
# Build outputs
objs/
bins/
other/
*.o
*.d
*.hex
*.elf
*.map
*.xml

# IDE files
*.mcp
*.mcw
*.mcs
*.mcpar
*.X/
.generated_files/

# System files
.DS_Store
Thumbs.db
*.tmp
*.temp
*.swp
*.swo
*~
EOF

    echo -e "${GREEN}✓ Template files created${NC}"
}

# Main execution
main() {
    if [ $# -eq 0 ]; then
        print_usage
        exit 1
    fi
    
    PROJECT_NAME="$1"
    DEVICE="${2:-$DEVICE}"
    OUTPUT_DIR="${3:-$OUTPUT_DIR}"
    
    # Expand and normalize the output directory path
    OUTPUT_DIR=$(realpath "$OUTPUT_DIR" 2>/dev/null || echo "$OUTPUT_DIR")
    PROJECT_ROOT="$OUTPUT_DIR/$PROJECT_NAME"
    
    # Ensure output directory exists
    if [ ! -d "$OUTPUT_DIR" ]; then
        echo -e "${YELLOW}Creating output directory: $OUTPUT_DIR${NC}"
        mkdir -p "$OUTPUT_DIR" || {
            echo -e "${RED}Error: Could not create output directory '$OUTPUT_DIR'${NC}"
            exit 1
        }
    fi
    
    echo -e "${BLUE}PIC32MZ Project Generator${NC}"
    echo "=========================="
    echo -e "${YELLOW}Project Name:${NC} $PROJECT_NAME"
    echo -e "${YELLOW}Device:${NC} $DEVICE"
    echo -e "${YELLOW}Root Directory:${NC} $OUTPUT_DIR"
    echo -e "${YELLOW}Project Location:${NC} $PROJECT_ROOT"
    echo ""
    
    # Generate project
    create_directories "$PROJECT_ROOT"
    create_root_makefile "$PROJECT_ROOT" "$PROJECT_NAME" "$DEVICE"
    create_srcs_makefile "$PROJECT_ROOT"
    create_template_files "$PROJECT_ROOT" "$PROJECT_NAME" "$DEVICE"
    
    echo ""
    echo -e "${GREEN}✅ Project '$PROJECT_NAME' generated successfully!${NC}"
    echo -e "${BLUE}📁 Location:${NC} $(cd "$PROJECT_ROOT" && pwd)"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  cd \"$PROJECT_ROOT\""
    echo "  make build_dir"
    echo "  make"
    echo ""
    echo -e "${GREEN}The project is ready for development! 🚀${NC}"
}

main "$@"
