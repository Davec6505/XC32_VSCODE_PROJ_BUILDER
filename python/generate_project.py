#!/usr/bin/env python3
"""
PIC32MZ XC32 Project Generator
Automatically creates a complete embedded project structure with cross-platform Makefiles
"""

import os
import sys
import argparse
from pathlib import Path


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

    def create_root_makefile(self):
        """Create the root Makefile with cross-platform support"""
        content = f'''# Name of the project binary
MODULE    	:= {self.project_name}

# Device configuration
# The device is expected to be a PIC32MZ family device.
DEVICE 		:= {self.device}

# Compiler location and DFP (Device Family Pack) location
# The compiler location is expected to be the path to the xc32-gcc compiler.
# The DFP location is expected to be the path to the Microchip Device Family Pack.
# The DFP is used to provide the necessary header files and libraries for the specific device.
# The DFP is expected to be installed in the MPLAB X IDE installation directory.
# The DFP is expected to be in the packs directory of the MPLAB X IDE installation directory.
# The DFP is expected to be in the format of Microchip/PIC32MZ-EF_DFP/1.4.168.
# Cross-platform compiler and DFP paths
ifeq ($(OS),Windows_NT)
    COMPILER_LOCATION := C:/Program Files/Microchip/xc32/v4.60/bin
    DFP_LOCATION := C:/Program Files/Microchip/MPLABX/v6.25/packs
else
    COMPILER_LOCATION := /opt/microchip/xc32/v4.60/bin
    DFP_LOCATION := /opt/microchip/mplabx/v6.25/packs
endif
DFP := $(DFP_LOCATION)/Microchip/PIC32MZ-EF_DFP/1.4.168

# Simple Unix-style build system
BUILD=make
CLEAN=make clean
BUILD_DIR=make build_dir

all:
	@echo "######  BUILDING   ########"
	cd srcs && $(BUILD) COMPILER_LOCATION="$(COMPILER_LOCATION)" DFP_LOCATION="$(DFP_LOCATION)" DFP="$(DFP)" DEVICE=$(DEVICE) MODULE=$(MODULE)
	@echo "###### BIN TO HEX ########"
	cd bins && "$(COMPILER_LOCATION)/xc32-bin2hex" $(MODULE)
	@echo "######  BUILD COMPLETE   ########"

build_dir:
	@echo "#######BUILDING DIRECTORIES FOR OUTPUT BINARIES#######"
	cd srcs && $(BUILD_DIR)

debug:
	@echo "#######DEBUGGING OUTPUTS#######"
	cd srcs && $(BUILD) debug COMPILER_LOCATION="$(COMPILER_LOCATION)" DFP_LOCATION="$(DFP_LOCATION)" DFP="$(DFP)" DEVICE=$(DEVICE) MODULE=$(MODULE)

platform:
	@echo "#######PLATFORM INFO#######"
	cd srcs && $(BUILD) platform COMPILER_LOCATION="$(COMPILER_LOCATION)" DFP_LOCATION="$(DFP_LOCATION)" DFP="$(DFP)" DEVICE=$(DEVICE) MODULE=$(MODULE)

clean:
	@echo "####### CLEANING OUTPUTS #######"
	cd srcs && $(CLEAN)
	@echo "####### REMOVING BUILD ARTIFACTS #######"
ifeq ($(OS),Windows_NT)
	@if exist "bins\\*" del /q "bins\\*" >nul 2>&1
	@if exist "objs\\*" rmdir /s /q "objs" >nul 2>&1 && mkdir "objs" >nul 2>&1
	@if exist "other\\*" del /q "other\\*" >nul 2>&1
else
	@rm -rf bins/* objs/* other/* 2>/dev/null || true
endif

install:
	cd srcs && $(BUILD) install

flash:
	@echo "#######LOADING OUTPUTS#######"
	cd bins && sudo ../../MikroC_bootloader_lnx/bins/mikro_hb $(MODULE).hex
	@echo "#######LOAD COMPLETE#######"

dfp_dir:
	@echo "####### DFP DIRECTORY #######"
	@echo $(DFP)

help:
	@echo "####### HELP #######"
	cd srcs && $(BUILD) help
	@echo "#####################"

# Unix-style utility targets (cross-platform)
find-source:
	@echo "####### FINDING SOURCE FILES #######"
ifeq ($(OS),Windows_NT)
	@powershell -Command "Get-ChildItem -Recurse srcs -Include *.c,*.h | Select-Object -ExpandProperty FullName"
else
	@find srcs -name "*.c" -o -name "*.h"
endif

grep-pattern:
	@echo "####### SEARCHING FOR PATTERN (usage: make grep-pattern PATTERN=your_pattern) #######"
ifeq ($(OS),Windows_NT)
	@powershell -Command "Select-String -Pattern '$(PATTERN)' -Path 'srcs\\*' -Recurse || Write-Host 'No matches found'"
else
	@grep -r "$(PATTERN)" srcs/ || echo "No matches found"
endif

list-files:
	@echo "####### LISTING PROJECT FILES #######"
ifeq ($(OS),Windows_NT)
	@dir /b
else
	@ls -la
endif

.PHONY: all build_dir clean install find-source grep-pattern list-files debug platform
'''
        makefile_path = os.path.join(self.project_root, "Makefile")
        with open(makefile_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"Created root Makefile: {makefile_path}")

    def create_srcs_makefile(self, include_startup=False):
        """Create the srcs/Makefile with simple structure"""
        if include_startup:
            content = '''# DFP (Device Family Pack) configuration
# These variables should be passed from the root Makefile
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

# Project directories expected in the project.
# These directories are created if they do not exist when "make build_dir" is run.
# The directories are used to store object files, binaries, source files, include files, and other files.
# The directories are created relative to the project root directory.
# The project root directory is expected to be one level above the srcs directory.
# The project root directory is expected to contain the srcs, objs, incs, bins, and other directories.
# The objs directory is used to store object files.
# The incs directory is used to store header files.
# The bins directory is used to store binaries.
# The other directory is used to store other files such as maps and XML files.
ROOT     := ..
OBJ_DIR  := $(ROOT)/objs
INC_DIR  := $(ROOT)/incs
BIN_DIR  := $(ROOT)/bins
SRC_DIR  := $(ROOT)/srcs
OUT_DIR  := $(ROOT)/other


# Source files and object files
# The source files are expected to be in the srcs directory & sub-directories.
# The source files are expected to have the .c extension.
# The object file list is created from the SRCS variable with the .o extension inplaceof the .c extension.
# Dynamically find all .c files using Make functions (up to 4 levels deep)
define get_c_files
$(wildcard $(1)/*.c) $(wildcard $(1)/*/*.c) $(wildcard $(1)/*/*/*.c) $(wildcard $(1)/*/*/*/*.c)
endef
SRCS := $(call get_c_files,$(SRC_DIR))
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)


# The assembly files are expected to be in the srcs directory & sub-directories.
# Dynamically find all .S files using Make functions (up to 4 levels deep)
define get_s_files
$(wildcard $(1)/*.S) $(wildcard $(1)/*/*.S) $(wildcard $(1)/*/*/*.S) $(wildcard $(1)/*/*/*/*.S)
endef
ASM := $(call get_s_files,$(SRC_DIR))
ASMS := $(ASM:$(SRC_DIR)/%.S=$(OBJ_DIR)/%.o)

# The assembly object files are created from the ASM variable with the .o extension inplace of the .S extension.
# The assembly object files are added to the OBJS variable.
# This allows the assembly files to be compiled and linked with the C source files.
# The assembly files are expected to be in the srcs directory & sub-directories.
# The assembly files are expected to have the .S extension.
# The assembly files are expected to be compiled with the same compiler as the C source files.
# The assembly files are expected to be compiled with the same flags as the C source files.
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


# Assign all Include directories dynamically, first run "make build_dir" from terminal.
# Get all directories under INC_DIR recursively (up to 4 levels deep)
define get_inc_dirs
$(sort $(dir $(wildcard $(1)/*/)) $(dir $(wildcard $(1)/*/*/)) $(dir $(wildcard $(1)/*/*/*/)) $(dir $(wildcard $(1)/*/*/*/*/)))
endef

INC_SUBDIRS := $(call get_inc_dirs,$(INC_DIR))
# Remove trailing slashes and add -I prefix for each directory
INC_FLAGS := $(foreach d,$(patsubst %/,%,$(INC_SUBDIRS)),-I"$(d)")
INCS := -I"$(INC_DIR)" $(INC_FLAGS) -I"$(DFP_INCLUDE)"


#Direct the compiler outputs for .o files from .c or .cpp code
DIRECT_OBJ := $(CC)    -g -x c -c $(MCU)  -ffunction-sections -fdata-sections -O1 -fno-common \
			$(INCS)  $(FLAGS) -MF $(@:.o=.d) -DXPRJ_default=default -mdfp="$(DFP)"
			

# Direct compiler output for linker 
LINKER_SCRIPT := $(DFP)/xc32/$(DEVICE)/p32MZ1024EFH064.ld
DIRECT_LINK := $(CC)  $(MCU) -nostartfiles -DXPRJ_default=default -mdfp="$(DFP)" 	\
			-Wl,--defsym=__MPLAB_BUILD=1,--script="$(LINKER_SCRIPT)",--defsym=_min_heap_size=512,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="$(OUT_DIR)/production.map",--memorysummary,$(OUT_DIR)/memoryfile.xml \




DIRECT_ASM :=   -c  -DXPRJ_default=default    -Wa,--defsym=__MPLAB_BUILD=1,-MD=$(OBJ_DIR)/startup/startup.o.asm.d,--gdwarf-2 -mdfp="$(DFP)" -MMD -MF $(OBJ_DIR)/startup/startup.o.d

# Define the default target (which is built when make is invoked without any arguments)
$(BIN_DIR)/$(MODULE): $(OBJS)
	@echo "Building project for $(DEVICE)"
	@echo "Linking object files to create the final executable"
	$(DIRECT_LINK) -o $@ $^ 
	@echo "Build complete. Output is in $(BIN_DIR)"

# Compile all source files to object files
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

# Show platform-specific configuration
platform:
	@echo "Cross-platform build configuration:"
	@echo "  Detected OS: $(detected_OS)"
	@echo "  Path separator: $(PATH_SEP)"
	@echo "  Null device: $(NULL_DEVICE)"
	@echo "  MKDIR command: $(value MKDIR)"
	@echo "  RMDIR command: $(value RMDIR)"
	@echo "  RM command: $(value RM)"
	@echo "  MOVE command: $(value MOVE)"

# Create the build directories if they do not exist
# This target is used to create the necessary directories for the build process.
# It creates the OBJ_DIR, BIN_DIR, SRC_DIR, INC_DIR, and OUT_DIR
# It also creates subdirectories in OBJ_DIR and INC_DIR for each subdirectory in SRC_DIR
# This is useful for organizing the build output and include files.
# To run this target, use: make build_dir
# Get all directories under SRC_DIR dynamically (similar to how we get source files)
SRC_DIRS := $(sort $(dir $(wildcard $(SRC_DIR)/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/*/*/)))
# Filter out startup directory from automatic creation and convert to relative paths
SRC_SUBDIRS := $(sort $(filter-out startup/,$(SRC_DIRS:$(SRC_DIR)/%=%)))

build_dir: 
	@echo "Creating build base directories if they do not exist ($(detected_OS))"
	@$(call MKDIR,$(OBJ_DIR))
	@$(call MKDIR,$(BIN_DIR))
	@$(call MKDIR,$(SRC_DIR))
	@$(call MKDIR,$(INC_DIR))
	@$(call MKDIR,$(OUT_DIR))
	@echo "Creating subdirectories in OBJ_DIR and INC_DIR based on SRC_DIR structure"
	@$(foreach subdir,$(SRC_SUBDIRS),$(call MKDIR,$(OBJ_DIR)/$(subdir)) && $(call MKDIR,$(INC_DIR)/$(subdir)) &&) echo "Created peripheral directories"
	@echo "Moving header files from src subdirectories to corresponding inc subdirectories"
	@$(foreach subdir,$(SRC_SUBDIRS),$(foreach header,$(wildcard $(SRC_DIR)/$(subdir)*.h),$(call MOVE,$(header),$(INC_DIR)/$(subdir)) &&)) echo "Headers moved"
	@echo "Build directories created successfully"

# Display the source files, object files, and include directories
debug:
	@echo "Build system debug info ($(detected_OS)):"
	@echo "Source files:"
	@$(foreach src,$(SRCS),echo "  $(src)" &&) echo ""
	@echo "Object files:"
	@$(foreach obj,$(OBJS),echo "  $(obj)" &&) echo ""
	@echo "Include directories:"
	@$(foreach inc,$(subst -I",,$(subst ",,$(INCS))),echo "  -I\"$(inc)\"" &&) echo ""
	@echo "Include subdirectories found:"
	@$(foreach dir,$(INC_SUBDIRS),echo "  $(dir)" &&) echo ""
	@echo "Include flags generated:"
	@$(foreach flag,$(INC_FLAGS),echo "  $(flag)" &&) echo ""
	@echo "Source subdirectories found:"
	@$(foreach dir,$(SRC_SUBDIRS),echo "  $(dir)" &&) echo ""
	@echo "DFP Include path:"
	@echo "  $(DFP_INCLUDE)"
	@echo "Linker script:"
	@echo "  $(LINKER_SCRIPT)"


# For xc32 Compiler help with less use: make help less
# For xc32 Compiler help without less use: make help
help:
	@echo "Displaying help information for xc32-gcc"
ifeq ($(filter less,$(MAKECMDGOALS)),less)
	xc32-gcc --help | less
else
	xc32-gcc --help
endif





clean:
	@echo "Cleaning up object files and binaries ($(detected_OS))"
	@$(call RM,$(BIN_DIR)/*) 2>$(NULL_DEVICE) || true
	@$(call RMDIR,$(OBJ_DIR)) 2>$(NULL_DEVICE) || true
	@$(call MKDIR,$(OBJ_DIR))
	@$(call RM,$(OUT_DIR)/*) 2>$(NULL_DEVICE) || true
	@echo "Clean complete."


define clear_build_dir
	-@rm -rf $(BIN_DIR)/* $(OBJ_DIR)/* $(OUT_DIR)/* 2>/dev/null || true
endef



##################################################################################################
##                       Table 5-6. Kind-of-Output Control Options								##
##################################################################################################
# Option      |  Definition
# -----------------------------------------------------------------------------------------------
# -c          |  Stop compilation before the link step, producing an intermediate file.
# -E          |  Stop compilation after preprocessing, producing a preprocessed file.
# --help      |  Print a description of the command line options.
# -o file     |Place the output in a file with the specified name.
# -S          |  Stop compilation before the assembly step, producing an assembly file output.
# -specs=file |  Overrides the standard specs file.
# -v          |  Print the commands executed during each stage of compilation.
# --version   |  Show version information then quit.
# -x          |  Specify the language of a source file regardless of its file extension.
#################################################################################################
'''
        else:
            content = '''# DFP (Device Family Pack) configuration
# These variables should be passed from the root Makefile
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

# Project directories expected in the project.
# These directories are created if they do not exist when "make build_dir" is run.
# The directories are used to store object files, binaries, source files, include files, and other files.
# The directories are created relative to the project root directory.
# The project root directory is expected to be one level above the srcs directory.
# The project root directory is expected to contain the srcs, objs, incs, bins, and other directories.
# The objs directory is used to store object files.
# The incs directory is used to store header files.
# The bins directory is used to store binaries.
# The other directory is used to store other files such as maps and XML files.
ROOT     := ..
OBJ_DIR  := $(ROOT)/objs
INC_DIR  := $(ROOT)/incs
BIN_DIR  := $(ROOT)/bins
SRC_DIR  := $(ROOT)/srcs
OUT_DIR  := $(ROOT)/other


# Source files and object files
# The source files are expected to be in the srcs directory & sub-directories.
# The source files are expected to have the .c extension.
# The object file list is created from the SRCS variable with the .o extension inplaceof the .c extension.
# Dynamically find all .c files using Make functions (up to 4 levels deep)
define get_c_files
$(wildcard $(1)/*.c) $(wildcard $(1)/*/*.c) $(wildcard $(1)/*/*/*.c) $(wildcard $(1)/*/*/*/*.c)
endef
SRCS := $(call get_c_files,$(SRC_DIR))
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)


# The assembly files are expected to be in the srcs directory & sub-directories.
# Dynamically find all .S files using Make functions (up to 4 levels deep)
define get_s_files
$(wildcard $(1)/*.S) $(wildcard $(1)/*/*.S) $(wildcard $(1)/*/*/*.S) $(wildcard $(1)/*/*/*/*.S)
endef
ASM := $(call get_s_files,$(SRC_DIR))
ASMS := $(ASM:$(SRC_DIR)/%.S=$(OBJ_DIR)/%.o)

# The assembly object files are created from the ASM variable with the .o extension inplace of the .S extension.
# The assembly object files are added to the OBJS variable.
# This allows the assembly files to be compiled and linked with the C source files.
# The assembly files are expected to be in the srcs directory & sub-directories.
# The assembly files are expected to have the .S extension.
# The assembly files are expected to be compiled with the same compiler as the C source files.
# The assembly files are expected to be compiled with the same flags as the C source files.
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


# Assign all Include directories dynamically, first run "make build_dir" from terminal.
# Get all directories under INC_DIR recursively (up to 4 levels deep)
define get_inc_dirs
$(sort $(dir $(wildcard $(1)/*/)) $(dir $(wildcard $(1)/*/*/)) $(dir $(wildcard $(1)/*/*/*/)) $(dir $(wildcard $(1)/*/*/*/*/)))
endef

INC_SUBDIRS := $(call get_inc_dirs,$(INC_DIR))
# Remove trailing slashes and add -I prefix for each directory
INC_FLAGS := $(foreach d,$(patsubst %/,%,$(INC_SUBDIRS)),-I"$(d)")
INCS := -I"$(INC_DIR)" $(INC_FLAGS) -I"$(DFP_INCLUDE)"


#Direct the compiler outputs for .o files from .c or .cpp code
DIRECT_OBJ := $(CC)    -g -x c -c $(MCU)  -ffunction-sections -fdata-sections -O1 -fno-common \
			$(INCS)  $(FLAGS) -MF $(@:.o=.d) -DXPRJ_default=default -mdfp="$(DFP)"
			

# Direct compiler output for linker 
LINKER_SCRIPT := $(DFP)/xc32/$(DEVICE)/p32MZ1024EFH064.ld
DIRECT_LINK := $(CC)  $(MCU) -nostartfiles -DXPRJ_default=default -mdfp="$(DFP)" 	\
			-Wl,--defsym=__MPLAB_BUILD=1,--script="$(LINKER_SCRIPT)",--defsym=_min_heap_size=512,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="$(OUT_DIR)/production.map",--memorysummary,$(OUT_DIR)/memoryfile.xml \




DIRECT_ASM :=   -c  -DXPRJ_default=default    -Wa,--defsym=__MPLAB_BUILD=1,-MD=$(OBJ_DIR)/startup/startup.o.asm.d,--gdwarf-2 -mdfp="$(DFP)" -MMD -MF $(OBJ_DIR)/startup/startup.o.d

# Define the default target (which is built when make is invoked without any arguments)
$(BIN_DIR)/$(MODULE): $(OBJS)
	@echo "Building project for $(DEVICE)"
	@echo "Linking object files to create the final executable"
	$(DIRECT_LINK) -o $@ $^ 
	@echo "Build complete. Output is in $(BIN_DIR)"

# Compile all source files to object files
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

# Show platform-specific configuration
platform:
	@echo "Cross-platform build configuration:"
	@echo "  Detected OS: $(detected_OS)"
	@echo "  Path separator: $(PATH_SEP)"
	@echo "  Null device: $(NULL_DEVICE)"
	@echo "  MKDIR command: $(value MKDIR)"
	@echo "  RMDIR command: $(value RMDIR)"
	@echo "  RM command: $(value RM)"
	@echo "  MOVE command: $(value MOVE)"

# Create the build directories if they do not exist
# This target is used to create the necessary directories for the build process.
# It creates the OBJ_DIR, BIN_DIR, SRC_DIR, INC_DIR, and OUT_DIR
# It also creates subdirectories in OBJ_DIR and INC_DIR for each subdirectory in SRC_DIR
# This is useful for organizing the build output and include files.
# To run this target, use: make build_dir
# Get all directories under SRC_DIR dynamically (similar to how we get source files)
SRC_DIRS := $(sort $(dir $(wildcard $(SRC_DIR)/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/*/)) $(dir $(wildcard $(SRC_DIR)/*/*/*/*/)))
# Filter out startup directory from automatic creation and convert to relative paths
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

# Display the source files, object files, and include directories
debug:
	@echo "Build system debug info ($(detected_OS)):"
	@echo "Source files:"
	@$(foreach src,$(SRCS),echo "  $(src)" &&) echo ""
	@echo "Object files:"
	@$(foreach obj,$(OBJS),echo "  $(obj)" &&) echo ""
	@echo "Include directories:"
	@$(foreach inc,$(subst -I",,$(subst ",,$(INCS))),echo "  -I\"$(inc)\"" &&) echo ""
	@echo "Include subdirectories found:"
	@$(foreach dir,$(INC_SUBDIRS),echo "  $(dir)" &&) echo ""
	@echo "Include flags generated:"
	@$(foreach flag,$(INC_FLAGS),echo "  $(flag)" &&) echo ""
	@echo "Source subdirectories found:"
	@$(foreach dir,$(SRC_SUBDIRS),echo "  $(dir)" &&) echo ""
	@echo "DFP Include path:"
	@echo "  $(DFP_INCLUDE)"
	@echo "Linker script:"
	@echo "  $(LINKER_SCRIPT)"


# For xc32 Compiler help with less use: make help less
# For xc32 Compiler help without less use: make help
help:
	@echo "Displaying help information for xc32-gcc"
ifeq ($(filter less,$(MAKECMDGOALS)),less)
	xc32-gcc --help | less
else
	xc32-gcc --help
endif





clean:
	@echo "Cleaning up object files and binaries ($(detected_OS))"
	@$(call RM,$(BIN_DIR)/*) 2>$(NULL_DEVICE) || true
	@$(call RMDIR,$(OBJ_DIR)) 2>$(NULL_DEVICE) || true
	@$(call MKDIR,$(OBJ_DIR))
	@$(call RM,$(OUT_DIR)/*) 2>$(NULL_DEVICE) || true
	@echo "Clean complete."


define clear_build_dir
	-@rm -rf $(BIN_DIR)/* $(OBJ_DIR)/* $(OUT_DIR)/* 2>/dev/null || true
endef



##################################################################################################
##                       Table 5-6. Kind-of-Output Control Options								##
##################################################################################################
# Option      |  Definition
# -----------------------------------------------------------------------------------------------
# -c          |  Stop compilation before the link step, producing an intermediate file.
# -E          |  Stop compilation after preprocessing, producing a preprocessed file.
# --help      |  Print a description of the command line options.
# -o file     |Place the output in a file with the specified name.
# -S          |  Stop compilation before the assembly step, producing an assembly file output.
# -specs=file |  Overrides the standard specs file.
# -v          |  Print the commands executed during each stage of compilation.
# --version   |  Show version information then quit.
# -x          |  Specify the language of a source file regardless of its file extension.
#################################################################################################
'''
        makefile_path = os.path.join(self.project_root, "srcs", "Makefile")
        with open(makefile_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"Created srcs Makefile: {makefile_path}")

    def create_template_files(self):
        """Create template source files"""

        # Create definitions.h
        definitions_content = f'''/*******************************************************************************
  System Definitions

  File Name:
    definitions.h

  Summary:
    {self.project_name} system definitions.

  Description:
    This file contains the system-wide prototypes and definitions for {self.project_name}.

 *******************************************************************************/

#ifndef DEFINITIONS_H
#define DEFINITIONS_H

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************
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


// *****************************************************************************
// *****************************************************************************
// Section: Function Prototypes
// *****************************************************************************
// *****************************************************************************
#ifdef __cplusplus  // Provide C++ Compatibility
extern "C" {{
#endif

// Add your function prototypes here

#ifdef __cplusplus
}}
#endif

#endif /* DEFINITIONS_H */
'''

        # Create template source files in srcs directory

        # Create main.c in srcs
        main_content = f'''/*******************************************************************************
  Main Source File

  Company:
    Your Company Name

  File Name:
    main.c

  Summary:
    This file contains the "main" function for {self.project_name}.

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

/*******************************************************************************
 End of File
*/
'''

        # Create README.md
        readme_content = f'''# {self.project_name}

PIC32MZ Embedded Project using XC32 Compiler

## Device
- **Microcontroller**: {self.device}
- **Compiler**: XC32 v4.60+
- **IDE**: VS Code with Makefile support

## Project Structure

```
{self.project_name}/
├── Makefile              # Root build file
├── README.md            # This file
├── srcs/                # Source files
│   ├── Makefile         # Source build configuration
│   └── main.c           # Main application
├── incs/                # Header files
│   └── definitions.h    # Project definitions
├── objs/                # Object files (generated)
├── bins/                # Binary outputs (generated)
├── other/               # Maps, XML files (generated)
└── docs/                # Documentation
```

## Building

### Windows
```bash
make
```

### Linux/macOS
```bash
make
```

The build system automatically detects your platform and uses appropriate commands.

## Useful Commands

- `make` - Build the project
- `make clean` - Clean build artifacts
- `make debug` - Show build configuration
- `make platform` - Show cross-platform settings
- `make build_dir` - Create directory structure
- `make find-source` - List all source files
- `make help` - Show compiler help

## Cross-Platform Support

This project automatically detects Windows, Linux, and macOS and adjusts build commands accordingly. No modifications needed when switching platforms.

## Generated by PIC32MZ Project Generator
Generated on: {sys.platform}
'''

        # Write files (excluding MCC Harmony generated files)
        files_to_create = [
            ("srcs/main.c", main_content),
            ("incs/definitions.h", definitions_content),
            ("README.md", readme_content)
        ]

        for file_path, content in files_to_create:
            full_path = os.path.join(self.project_root, file_path)
            with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            print(f"Created template file: {full_path}")

    def create_gitignore(self):
        """Create .gitignore for the project"""
        gitignore_content = '''# Build outputs
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

# Python cache (for generator script)
__pycache__/
*.pyc
*.pyo
'''
        gitignore_path = os.path.join(self.project_root, ".gitignore")
        with open(gitignore_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(gitignore_content)
        print(f"Created .gitignore: {gitignore_path}")

    def create_startup_files(self):
        """Create startup files for mikroc compatibility - only if they don't exist"""
        startup_s_path = os.path.join(
            self.project_root, "srcs", "startup", "startup.S")

        # Only create startup.S if it doesn't exist
        if not os.path.exists(startup_s_path):
            # Create startup.S file
            startup_s_content = '''/*******************************************************************************
 *
 *                  C Runtime Startup
 *
 *********************************************************************
 * Filename:        crt0.S
 *
 * Processor:       PIC32
 *
 * Compiler:        MPLAB XC32
 *                  MPLAB X IDE
 * Company:         Microchip Technology Inc.
 *
 * Software License Agreement
 *
 * Copyright (c) 2014, Microchip Technology Inc. and its subsidiaries ("Microchip")
 * All rights reserved.
 *
 * This software is developed by Microchip Technology Inc. and its
 * subsidiaries ("Microchip").
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1.      Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * 2.      Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * 3.      Microchip's name may not be used to endorse or promote products
 * derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY MICROCHIP "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
 * MICROCHIP BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING BUT NOT LIMITED TO
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWSOEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 ********************************************************************/

/* Edited: J. Bajic 2021, v2.15r01 */ 
 
/* !!! THIS IS MODIFIED crt0.s (XC32 v2.15) STARTUP CODE FOR USE WITH MIKROE BOOTLOADER !!! */
    
#include "xc.h"
#include <cp0defs.h>	    
    
#define USE_MIKROE_BOOTLOADER    /* !!! Added this line, define USE_MIKROE_BOOTLOADER */
    
#ifdef __LIBBUILD__
   # Replace the standard debugging information with a simple filename. This
   # prevents the library build directory from showing up in MPLAB IDE. It
   # also effectively disables source-line debugging.
   .file 1 "libpic32/startup/crt0.S"
   .loc 1 0
#endif

#if (__XC32_VERSION > 1000) && !defined(CPP_INIT)
#define CPP_INIT
#endif

#if !defined(PIC32_SRS_SET_COUNT)
#  if defined(__PIC32_SRS_SET_COUNT)
#    define PIC32_SRS_SET_COUNT __PIC32_SRS_SET_COUNT
#  else
#    warning PIC32_SRS_SET_COUNT not defined on build line
#    define PIC32_SRS_SET_COUNT 2
#  endif
#endif
   
/* !!! Commented this section */ 
/* !!! Processor header conatains info if PIC32 has init data ->   __PIC32_HAS_INIT_DATA */
/*#if defined(__PIC32MX) || defined(__PIC32MM) || defined(__PIC32MZ)*/
/*#define INIT_DATA 1*/
/*#endif*/
/* !!! end of commented section */

/* This file contains 32-bit assembly code */
       .set nomips16

        ##################################################################
        # Entry point of the entire application
        ##################################################################
        .section .reset,code,keep
        .align 2
        .set noreorder
        .ent _reset

############################
# Begin ISA switching code #
############################

#if defined (__mips_micromips)
        .set micromips	
#endif
	
#if(!defined(USE_MIKROE_BOOTLOADER))/* !!! Added this line, USE_MIKROE_BOOTLOADER defined in CPUconfig.h */
    #if (defined(__PIC32_HAS_MICROMIPS)) && (defined(__PIC32_HAS_MIPS32R2))
    _reset:
	    .word 0x10000003     /* MIPS32:    branch forward 0x10 bytes from here  */
				 /* MicroMIPS: ADDI32 $0, $0, 0x0007 (nop)          */
				 /* DO NOT change the relative branch               */

	    .word 0x00000000     /* NOP */
    __reset_micromips_isa:
	    .set    micromips
	    jal     _startup
	    nop

	    .align 2
	    /* Device not in proper ISA mode */
	    .set nomicromips
    __reset_switch_isa:
	    jal _startup
	    nop

    #else

    _reset:
	    jal _startup
	    nop

    #endif  /* __PIC32_HAS_MICROMIPS */
 /* !!! Added reset section, skip isa switching and jump to startup */    
#else
#    warning Startup set for MIKROE bootloader
_reset:
    
        la      k0, _startup
        jr      k0                      # Jump to startup code
        nop
	
#endif
 /* !!! end of added reset section */
 /* !!! NO CHANGES IN CODE BELOW !!! */
        .align 2
        .end _reset
        .globl _reset
        .size _reset, .-_reset

        .section .reset.startup,code,keep
        .align 2
        .set noreorder

#if defined (__mips_micromips)
        .set micromips	
#else
        .set nomicromips
#endif

############################
# End ISA switching code   #
############################

        ##################################################################
        # Startup code
        ##################################################################
        .align 2
        .globl _startup
        .set noreorder
        .ent _startup
_startup:
        ##################################################################
        # If entered because of an NMI, jump to the NMI handler.
        ##################################################################
        mfc0    k0,_CP0_STATUS
        ext     k0,k0,19,1              # Extract NMI bit
        beqz    k0,_no_nmi
        nop
        la      k0,_nmi_handler
        jr      k0
        nop
_no_nmi:

        ##################################################################
        # Initialize Stack Pointer
        #   _stack is initialized by the linker script to point to the
        #    starting location of the stack in DRM
        ##################################################################
        la      sp,_stack

        ##################################################################
        # Initialize Global Pointer
        #   _gp is initialized by the linker script to point to "middle"
        #   of the small variables region
        ##################################################################
        la      gp,_gp

#if (PIC32_SRS_SET_COUNT == 2)
        ##################################################################
        # Initialize Global Pointer in Shadow Set
        #   The SRSCtl's PSS field must be set to the shadow set in which
        #   to initialize the global pointer.  Since we have only a
        #   single shadow set (besides the normal), we will initialize
        #   SRSCtl<PSS> to SRSCtl<HSS>.  We then write the global pointer
        #   to the previous shadow set to ensure that on interrupt, the
        #   global pointer has been initialized.
        ##################################################################
        mfc0    t1,_CP0_SRSCTL          # Read SRSCtl register
        add     t3,t1,zero              # Save off current SRSCtl
        ext     t2,t1,26,4              # to obtain HSS field
        ins     t1,t2,6,4               # Put HSS field
        mtc0    t1,_CP0_SRSCTL          # into SRSCtl<PSS>
        ehb                             # Clear hazard before using new SRSCTL
        wrpgpr  gp,gp                   # Set global pointer in PSS
        mtc0    t3,_CP0_SRSCTL          # Restore SRSCtl
        ehb

#elif (PIC32_SRS_SET_COUNT > 2)
        ##################################################################
        # Initialize Global Pointer in Shadow Set(s)
        #   The SRSCtl PSS field must be set to the shadow set in which
        #   to initialize the global pointer.  We will initialize
        #   SRSCtl<PSS> to the number of reg sets and work down to set zero.
        #   We write the global pointer to the previous shadow set to
        #   ensure that on interrupt, the global pointer has been
        #   initialized.
        ##################################################################
        mfc0    t1,_CP0_SRSCTL          # Read SRSCtl register
        add     t3,t1,zero              # Save off current SRSCtl

        li      t2,(PIC32_SRS_SET_COUNT-1)

1:      ins     t1,t2,6,4               # Put next shadow set field
        mtc0    t1,_CP0_SRSCTL          # into SRSCtl<PSS>
        ehb                             # Clear hazard before using new SRSCTL
        wrpgpr  gp,gp                   # Set global pointer in PSS

        addiu   t2,t2,-1                # Next lower shadow set
                                        # Loop for all sets
        bne     t2,$0,1b                # Down to zero (normal GPR set)
        nop

        mtc0    t3,_CP0_SRSCTL          # Restore SRSCtl
        ehb

#endif /* (PIC32_SRS_SET_COUNT > 2) */

        ##################################################################
        # Call the "on reset" procedure
        ##################################################################
        la      t0,_on_reset
        jalr    t0
        nop

#if defined(INIT_MMU_MZ_FIXED) || defined(__PIC32_HAS_MMU_MZ_FIXED)
        ##################################################################
        # Initialize TLB for fixed mapping to EBI and SQI
        ##################################################################
        .extern __pic32_tlb_init_ebi_sqi
        la      t0,__pic32_tlb_init_ebi_sqi
        jalr    t0
        nop
#endif

        ##################################################################
        # Clear uninitialized data sections
        ##################################################################
_start_bss_init:
        la      t0,_bss_begin
        la      t1,_bss_end
        b       _bss_check
        nop

_bss_init:
        sw      zero,0x0(t0)
        sw      zero,0x4(t0)
        sw      zero,0x8(t0)
        sw      zero,0xc(t0)
        addu    t0,16
_bss_check:
        bltu    t0,t1,_bss_init
        nop

#if defined(INIT_L1_CACHE) || defined(__PIC32_HAS_L1CACHE)
        ##################################################################
        # Initialize L1 cache. This must be done after bss clearing
        # since the _bss_end symbol may not be cache-line aligned.
        ##################################################################
        .extern   __pic32_init_cache
        la      t0,__pic32_init_cache
        jalr    t0
        nop
#endif

#if defined(INIT_DATA) || defined(__PIC32_HAS_INIT_DATA)
        ##################################################################
        # Initialize data using the linker-generated .dinit table
        ##################################################################
        .extern   __pic32_data_init
        la      t0, __pic32_data_init
        jalr    t0
        nop
#endif /* INIT_DATA */

        ##################################################################
        # If there are no RAM functions, skip the next section --
        # initializing bus matrix registers.
        ##################################################################
        la      t1,_ramfunc_begin
        beqz    t1,_ramfunc_done
        nop

#if defined(INIT_SSX) || defined(__PIC32_HAS_SSX)
  /* No initialization required */
#else /* Use BMX */
        ##################################################################
        # Initialize bus matrix registers if RAM functions exist in the
        # application
        ##################################################################
        la      t1,_bmxdkpba_address
        la      t2,BMXDKPBA
        sw      t1,0(t2)
        la      t1,_bmxdudba_address
        la      t2,BMXDUDBA
        sw      t1,0(t2)
        la      t1,_bmxdupba_address
        la      t2,BMXDUPBA
        sw      t1,0(t2)
#endif /* INIT_SSX */

_ramfunc_done:

        ##################################################################
        # Initialize CP0 registers
        ##################################################################
        # Initialize Count register
        ##################################################################
        mtc0    zero,_CP0_COUNT

        ##################################################################
        # Initialize Compare register
        ##################################################################
        li      t2,-1
        mtc0    t2,_CP0_COMPARE

        ##################################################################
        # Ensure BEV set and Initialize EBase register
        ##################################################################
        li      t0, (1<<22)
        mfc0    t2,_CP0_STATUS
        or      t2,t0,t2               # Set BEV bit 22
        mtc0    t2,_CP0_STATUS

        la      t1,_ebase_address
        ehb
        mtc0    t1,_CP0_EBASE
        
        ##################################################################
        # Initialize PRISS register to a safer default for devices that 
        # have it. The application should re-initialize it to an
        # application-specific value.
        #
        # We do NOT do this by default.
        ##################################################################
#if defined(USE_DEFAULT_PRISS_VALUE) 
#if defined(_PRISS_PRI7SS_POSITION)
#if (PIC32_SRS_SET_COUNT >= 7)
        li	    t2, 0x76540000
        addiu	t2, t2, 0x3210
        lui	    t1, %hi(PRISS)
        sw	    t2, %lo(PRISS)(t1)
#elif (PIC32_SRS_SET_COUNT <= 2)
        li	    t2, 0x10000000
        lui	    t1, %hi(PRISS)
        sw	    t2, %lo(PRISS)(t1)
#endif /* PIC32_SRS_SET_COUNT */
#endif /* _PRISS_PRI7SS_POSITION */
#endif /* USE_DEFAULT_PRISS_VALUE */
        
        ##################################################################
        # Initialize IntCtl/INTCON.VS register with _vector_spacing
        ##################################################################
        la      t1,_vector_spacing
#if defined(INIT_INTCONVS) || defined(__PIC32_HAS_INTCONVS)
        la      t0, INTCON
        lw      t2, 0(t0)
        li      t2, 0
        ins     t2, t1, 16, 7
#if defined(__PIC32MM) && defined(_INTCON_MVEC_MASK)
        ori     t2, t2, _INTCON_MVEC_MASK
#endif
        sw      t2, 0(t0)
#endif
        li      t2,0                    # Clear t2 and
        ins     t2,t1,5,5               # shift value to VS field
        mtc0    t2,_CP0_INTCTL

        ##################################################################
        # Initialize CAUSE registers
        # - Enable counting of Count register <DC = 0>
        # - Use special exception vector <IV = 1>
        # - Clear pending software interrupts <IP1:IP0 = 0>
        ##################################################################
        li      t1,0x00800000
        mtc0    t1,_CP0_CAUSE

        ##################################################################
        # Initialize STATUS register
        # - Access to Coprocessor 0 not allowed in user mode <CU0 = 0>
        # - User mode uses configured endianness <RE = 0>
        # - Preserve Bootstrap Exception vectors <BEV>
        # - Preserve soft reset <SR> and non-maskable interrupt <NMI>
        # - CorExtend enabled based on whether CorExtend User Defined
        #   Instructions have been implemented <CEE = Config<UDI>>
        # - Disable any pending interrupts <IM7..IM2 = 0, IM1..IM0 = 0>
        # - Disable hardware interrupts <IPL7:IPL2 = 0>
        # - Base mode is Kernel mode <UM = 0>
        # - Error level is normal <ERL = 0>
        # - Exception level is normal <EXL = 0>
        # - Interrupts are disabled <IE = 0>
        # - DSPr2 ASE is enabled for devices that support it <MX = 1>
        # - FPU64 is enabled for devices that support it <CU1=1> & <FR=1>
        ##################################################################
        mfc0    t0,_CP0_CONFIG
        ext     t1,t0,22,1              # Extract UDI from Config register
        sll     t1,t1,17                # Move UDI to Status.CEE location
        mfc0    t0,_CP0_STATUS
        and     t0,t0,0x00580000        # Preserve SR, NMI, and BEV
#if defined(INIT_DSPR2) || defined(__PIC32_HAS_DSPR2)
        li      t2, 0x01000000          # Set the Status.MX bit to enable DSP
        or      t0,t2,t0
#endif
#if defined(INIT_FPU64) || defined(__PIC32_HAS_FPU64)
        li      t2, 0x24000000          # Set the Status.CU1 and Status.FR bits to
        or      t0,t2,t0                # enable the FPU in FR64 mode
#endif

        or      t0,t1,t0                # Include Status.CEE (from UDI)
        mtc0    t0,_CP0_STATUS
        
#if defined(PIC32WK) && defined(_CP0_CONFIG3) && defined (__mips_micromips)
        # Ensure that the ISAONEXEC bit is set for the microMIPS ISA for the PIC32WK family
        # _bsc0 (_CP0_CONFIG3, _CP0_CONFIG3_SELECT, ISAONEXEC_MASK)
        li      t1,0x10000              # ISAONEXEC bit
        mfc0    t0,_CP0_CONFIG3
        or      t1,t0,t1
        mtc0    t1,_CP0_CONFIG3

#endif /* PIC32WK && __mips_micromips */

#if defined(INIT_FPU64) || defined(__PIC32_HAS_FPU64)
                                        # FPU Control and Status
        li      t2,0x1000000            # FCSR: RM=0, FS=1, FO=0, FN=0
                                        # Enables: 0b00000 E=1, V=0, Z=0, O=0, U=0, I=0
        ctc1    t2, $31                 # High perf on denormal operands & tiny results
#endif
        ehb

        ##################################################################
        # Call the "on bootstrap" procedure
        ##################################################################
        la      t0,_on_bootstrap
        jalr    t0
        nop

        ##################################################################
        # Initialize Status<BEV> for normal exception vectors
        ##################################################################
        mfc0    t0,_CP0_STATUS
        and     t0,t0,0xffbfffff        # Clear BEV
        mtc0    t0,_CP0_STATUS

        ##################################################################
        # Call main. We do this via a thunk in the text section so that
        # a normal jump and link can be used, enabling the startup code
        # to work properly whether main is written in MIPS16 or MIPS32
        # code. I.e., the linker will correctly adjust the JAL to JALX if
        # necessary
        ##################################################################
        and     a0,a0,0
        and     a1,a1,0
        la      t0,_main_entry
        jr      t0
        nop

        .end _startup

        ##################################################################
        # Boot Exception Vector Handler
        # Jumps to _bootstrap_exception_handler
        ##################################################################
        .section .bev_handler,code,keep
        .align 2
        .set noreorder
        .ent _bev_exception
_bev_exception:
        la        k0,_bootstrap_exception_handler
        jr        k0
        nop

        .end _bev_exception

        ##################################################################
        # General Exception Vector Handler
        # Jumps to _general_exception_context
        ##################################################################
        .section .gen_handler,code
        .align 2
        .set noreorder
        .ent _gen_exception
_gen_exception:
0:      la      k0,_general_exception_context
        jr      k0
        nop

        .end _gen_exception

#if defined(INIT_MMU_MZ_FIXED) || defined(__PIC32_HAS_MMU_MZ_FIXED)
        ##################################################################
        # Simple TLB-Refill Exception Vector
        # Jumps to _simple_tlb_refill_exception_context
        ##################################################################
        .section .simple_tlb_refill_vector,code,keep
        .align 2
        .set noreorder
        .ent simple_tlb_refill_vector
simple_tlb_refill_vector:
        la      k0,_simple_tlb_refill_exception_context
        jr      k0
        nop

        .end simple_tlb_refill_vector
#endif

#if defined(INIT_L1_CACHE) || defined(__PIC32_HAS_L1CACHE)
        ##################################################################
        # Cache-Error Exception Vector Handler
        # Jumps to _cache_err_exception_context
        ##################################################################
        .section .cache_err_vector,code,keep
        .align 2
        .set noreorder
        .ent _cache_err_vector
_cache_err_vector:
        la      k0,_cache_err_exception_context
        jr      k0
        nop

        .end _cache_err_vector
#endif

        .section .text.main_entry,code,keep
        .align 2
        .ent _main_entry
_main_entry:

#if defined(CPP_INIT)
        .weak _init
        # call .init section to run constructors etc
        lui	a0,%hi(_init)
        addiu	sp,sp,-24
        addiu	a0,a0,%lo(_init)
        beq	a0,$0,2f
        sw	$31,20(sp)	 #,
        jalr	a0
        nop
2:
#endif
        and     a0,a0,0
        and     a1,a1,0

        ##################################################################

        # Call main
        ##################################################################
        la    	t0,main
        jalr 	t0
        nop

#if defined(CALL_EXIT)
        ##################################################################
        # Call exit()
        ##################################################################
        jal exit
        nop
#endif

        ##################################################################
        # Just in case, go into infinite loop
        # Call a software breakpoint only with -mdebugger compiler option
        ##################################################################
        .weak __exception_handler_break
__crt0_exit:
1:
        la      v0,__exception_handler_break
        beq     v0,0,0f
        nop
        jalr    v0
        nop

0:      b       1b
        nop

        .globl __crt0_exit
        .end _main_entry

'''

            with open(startup_s_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(startup_s_content)
            print(f"Created startup file: {startup_s_path}")
        else:
            print(f"Startup file already exists: {startup_s_path}")

    def generate_project(self, project_name, device="32MZ1024EFH064", output_dir=".", mikroc=False):
        """Generate complete project structure"""
        self.project_name = project_name
        self.device = device
        self.project_root = os.path.join(output_dir, project_name)

        print(f"Generating PIC32MZ project: {project_name}")
        print(f"Target device: {device}")
        print(f"Output directory: {os.path.abspath(self.project_root)}")
        if mikroc:
            print("MikroC support: ENABLED")
        print("-" * 50)

        # Create root directory
        Path(self.project_root).mkdir(parents=True, exist_ok=True)

        # Generate project structure
        self.create_directory_structure(include_startup=mikroc)
        self.create_root_makefile()
        self.create_srcs_makefile(include_startup=mikroc)
        self.create_template_files()
        self.create_gitignore()

        # Create startup files if mikroc option is enabled
        if mikroc:
            self.create_startup_files()

        print("-" * 50)
        print(f"✅ Project '{project_name}' generated successfully!")
        print(f"📁 Location: {os.path.abspath(self.project_root)}")
        print("")
        print("Next steps:")
        print(f"  cd {project_name}")
        print("  make build_dir")
        print("  make")
        print("")
        if mikroc:
            print("MikroC startup files included for bootloader compatibility! 🚀")
        else:
            print("The project is ready for development! 🚀")


def main():
    parser = argparse.ArgumentParser(
        description='PIC32MZ XC32 Project Generator')
    parser.add_argument('project_name', help='Name of the project to generate')
    parser.add_argument('--device', '-d', default='32MZ1024EFH064',
                        help='PIC32MZ device (default: 32MZ1024EFH064)')
    parser.add_argument('--output', '-o', default='.',
                        help='Root directory where project folder will be created (default: current directory)')
    parser.add_argument('--mikroc', action='store_true',
                        help='Include startup directory and files for MikroC compatibility')

    args = parser.parse_args()

    # Expand and normalize the output path
    output_path = os.path.abspath(os.path.expanduser(args.output))

    # Ensure output directory exists
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path, exist_ok=True)
            print(f"Created output directory: {output_path}")
        except OSError as e:
            print(
                f"Error: Could not create output directory '{output_path}': {e}")
            sys.exit(1)

    generator = PIC32ProjectGenerator()
    generator.generate_project(
        args.project_name, args.device, output_path, args.mikroc)


if __name__ == "__main__":
    main()
