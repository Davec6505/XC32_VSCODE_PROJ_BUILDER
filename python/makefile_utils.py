import os


def create_root_makefile(project_name, device, project_root):
    content = f'''# Name of the project binary
MODULE     := {project_name}

# Device configuration
# The device is expected to be a PIC32MZ family device.
DEVICE     := {device}

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
    DFP_LOCATION := C:/Users/Automation/.mchp_packs
#    DFP_LOCATION := C:/Program Files/Microchip/MPLABX/v6.25/packs
else
    COMPILER_LOCATION := /opt/microchip/xc32/v4.60/bin
    DFP_LOCATION := /opt/microchip/mplabx/v6.25/packs   
endif
#DFP := $(DFP_LOCATION)/Microchip/PIC32MZ-EF_DFP/1.4.168
DFP := $(DFP_LOCATION)/Microchip/PIC32MZ-EF_DFP/1.5.173

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
    @if exist bins del /q bins\*.* >nul 2>&1
    @if exist objs del /q objs\*.* >nul 2>&1
    @if exist other del /q other\*.* >nul 2>&1
else
    @rm -f bins/* objs/* other/* 2>/dev/null || true
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
    makefile_path = os.path.join(project_root, "Makefile")
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

# This allows the assembly files to be compiled and linked with the C source files.
# The assembly files are expected to be compiled with the same flags as the C source files.
COMPILER  := c99
STD := c99
$(sort $(dir $(wildcard $(1)/*/)) $(dir $(wildcard $(1)/*/*/)) $(dir $(wildcard $(1)/*/*/*/)) $(dir $(wildcard $(1)/*/*/*/*/)))
INC_SUBDIRS := $(call get_inc_dirs,$(INC_DIR))


	@echo "Building project for $(DEVICE)"
	@$(call MKDIR,$(dir $@))
	def create_root_makefile(self):
		from makefile_utils import create_root_makefile
		create_root_makefile(self.project_name, self.device, self.project_root)
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
        else:
            content = '''# DFP (Device Family Pack) configuration
# These variables should be passed from the root Makefile
DFP_DIR
    := $(DFP_DIR)