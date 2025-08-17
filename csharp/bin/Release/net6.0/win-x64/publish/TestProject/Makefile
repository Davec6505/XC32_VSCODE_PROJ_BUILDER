# Name of the project binary
MODULE    	:= TestProject

# Device configuration
DEVICE 		:= 32MZ2048EFH064

# Cross-platform compiler and DFP paths
ifeq ($(OS),Windows_NT)
    COMPILER_LOCATION := C:/Program Files/Microchip/xc32/v4.60/bin
    DFP_LOCATION := C:/Program Files/Microchip/MPLABX/v6.25/packs
else
    COMPILER_LOCATION := /opt/microchip/xc32/v4.60/bin
    DFP_LOCATION := /opt/microchip/mplabx/v6.25/packs
endif
DFP := $(DFP_LOCATION)/Microchip/PIC32MZ-EF_DFP/1.4.168

# Build system
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

.PHONY: all build_dir clean debug platform
