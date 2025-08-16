# Simple Makefile for PIC32MZ project
# DFP (Device Family Pack) configuration
DFP_DIR := $(DFP)
DFP_INCLUDE := $(DFP)/include

# Detect operating system for cross-platform compatibility
ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    MKDIR = if not exist "$(subst /,\,$(1))" mkdir "$(subst /,\,$(1))"
    RMDIR = if exist "$(subst /,\,$(1))" rmdir /s /q "$(subst /,\,$(1))"
    RM = if exist "$(subst /,\,$(1))" del /q "$(subst /,\,$(1))"
    NULL_DEVICE = nul
else
    detected_OS := $(shell uname -s)
    MKDIR = mkdir -p $(1)
    RMDIR = rm -rf $(1)
    RM = rm -f $(1)
    NULL_DEVICE = /dev/null
endif

# Project directories
ROOT     := ..
OBJ_DIR  := $(ROOT)/objs
INC_DIR  := $(ROOT)/incs
BIN_DIR  := $(ROOT)/bins
SRC_DIR  := $(ROOT)/srcs
OUT_DIR  := $(ROOT)/other

# Source files (only current directory)
SRCS := $(wildcard *.c)
OBJS := $(SRCS:%.c=$(OBJ_DIR)/%.o)

# Compiler and flags
CC := "$(COMPILER_LOCATION)/xc32-gcc"
MCU := -mprocessor=$(DEVICE)
FLAGS := -Werror -Wall -MP -MMD -g -O1 -ffunction-sections -fdata-sections -fno-common

# Include directories (simple structure)
INCS := -I"$(INC_DIR)" -I"$(DFP_INCLUDE)"

# Compiler command for object files
COMPILE_OBJ := $(CC) -x c -c $(MCU) $(FLAGS) $(INCS) -DXPRJ_default=default -mdfp="$(DFP)"

# Linker script and command
LINKER_SCRIPT := $(DFP)/xc32/$(DEVICE)/p32MZ1024EFH064.ld
LINK_CMD := $(CC) $(MCU) -nostartfiles -DXPRJ_default=default -mdfp="$(DFP)" \
            -Wl,--defsym=__MPLAB_BUILD=1,--script="$(LINKER_SCRIPT)",--defsym=_min_heap_size=512,--gc-sections,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="$(OUT_DIR)/production.map",--memorysummary,$(OUT_DIR)/memoryfile.xml

# Default target
$(BIN_DIR)/$(MODULE): $(OBJS)
	@echo "Linking $(MODULE) for $(DEVICE)"
	$(LINK_CMD) -o $@ $^ 
	@echo "Build complete: $@"

# Compile C source files
$(OBJ_DIR)/%.o: %.c
	@echo "Compiling $< to $@"
	@$(call MKDIR,$(dir $@))
	$(COMPILE_OBJ) -MF $(@:.o=.d) $< -o $@

.PHONY: clean build_dir debug help platform

# Create build directories
build_dir: 
	@echo "Creating build directories ($(detected_OS))"
	@$(call MKDIR,$(OBJ_DIR))
	@$(call MKDIR,$(BIN_DIR))
	@$(call MKDIR,$(OUT_DIR))
	@echo "Build directories created"

# Debug information
debug:
	@echo "Build system debug info ($(detected_OS)):"
	@echo "Source files: $(SRCS)"
	@echo "Object files: $(OBJS)"
	@echo "Include dirs: $(INCS)"
	@echo "DFP Include: $(DFP_INCLUDE)"
	@echo "Linker script: $(LINKER_SCRIPT)"

# Platform info
platform:
	@echo "Cross-platform build configuration:"
	@echo "  Detected OS: $(detected_OS)"
	@echo "  Compiler: $(CC)"
	@echo "  Device: $(DEVICE)"

# Help
help:
	@echo "Available targets:"
	@echo "  all (default) - Build the project"
	@echo "  build_dir     - Create build directories"
	@echo "  clean         - Clean build artifacts"
	@echo "  debug         - Show debug information"
	@echo "  platform      - Show platform information"
	@echo "  help          - Show this help"

# Clean
clean:
	@echo "Cleaning build artifacts ($(detected_OS))"
	@$(call RM,$(BIN_DIR)/*) 2>$(NULL_DEVICE) || true
	@$(call RMDIR,$(OBJ_DIR)) 2>$(NULL_DEVICE) || true
	@$(call MKDIR,$(OBJ_DIR))
	@$(call RM,$(OUT_DIR)/*) 2>$(NULL_DEVICE) || true
	@echo "Clean complete"
