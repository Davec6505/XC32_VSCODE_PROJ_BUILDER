# Simple Makefile for PIC32MZ project
# DFP configuration
DFP_DIR := $(DFP)
DFP_INCLUDE := $(DFP)/include

# Cross-platform support
ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    MKDIR = if not exist "$(subst /,\\,$(1))" mkdir "$(subst /,\\,$(1))"
else
    detected_OS := Unix
    MKDIR = mkdir -p $(1)
endif

# Project directories
ROOT     := ..
OBJ_DIR  := $(ROOT)/objs
INC_DIR  := $(ROOT)/incs
BIN_DIR  := $(ROOT)/bins
OUT_DIR  := $(ROOT)/other

# Source files
SRCS := $(wildcard *.c)
OBJS := $(SRCS:%.c=$(OBJ_DIR)/%.o)

# Compiler and flags
CC := "$(COMPILER_LOCATION)/xc32-gcc"
MCU := -mprocessor=$(DEVICE)
FLAGS := -Werror -Wall -MP -MMD -g -O1 -ffunction-sections -fdata-sections -fno-common
INCS := -I"$(INC_DIR)" -I"$(DFP_INCLUDE)"

# Build target
$(BIN_DIR)/$(MODULE): $(OBJS)
	@echo "Linking $(MODULE) for $(DEVICE)"
	$(CC) $(MCU) -nostartfiles -mdfp="$(DFP)" -Wl,--script="$(DFP)/xc32/$(DEVICE)/p32MZ1024EFH064.ld" -Wl,-Map="$(OUT_DIR)/production.map" -o $@ $^
	@echo "Build complete: $@"

# Compile rule
$(OBJ_DIR)/%.o: %.c
	@echo "Compiling $< to $@"
	@$(call MKDIR,$(dir $@))
	$(CC) -x c -c $(MCU) $(FLAGS) $(INCS) -mdfp="$(DFP)" -MF $(@:%.o=%.d) $< -o $@

# Targets
.PHONY: all build_dir clean debug platform

all: $(BIN_DIR)/$(MODULE)

build_dir:
	@echo "Creating build directories ($(detected_OS))"
	@$(call MKDIR,$(OBJ_DIR))
	@$(call MKDIR,$(BIN_DIR))
	@$(call MKDIR,$(OUT_DIR))
	@echo "Build directories created"

clean:
	@echo "Cleaning build artifacts"
ifeq ($(OS),Windows_NT)
	@if exist "$(OBJ_DIR)\\*" rmdir /s /q "$(OBJ_DIR)" >nul 2>&1 && mkdir "$(OBJ_DIR)" >nul 2>&1
	@if exist "$(BIN_DIR)\\*" del /q "$(BIN_DIR)\\*" >nul 2>&1
	@if exist "$(OUT_DIR)\\*" del /q "$(OUT_DIR)\\*" >nul 2>&1
else
	@rm -rf $(OBJ_DIR)/* $(BIN_DIR)/* $(OUT_DIR)/* 2>/dev/null || true
	@mkdir -p $(OBJ_DIR)
endif
	@echo "Clean complete"

debug:
	@echo "Build system debug info:"
	@echo "Source files: $(SRCS)"
	@echo "Object files: $(OBJS)"

platform:
	@echo "Platform: $(detected_OS)"
	@echo "Compiler: $(CC)"
	@echo "Device: $(DEVICE)"
