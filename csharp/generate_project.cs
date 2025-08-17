using System;
using System.IO;
using System.Text;

namespace PIC32MZProjectGenerator
{
    class Program
    {
        // Default values
        private static string device = "32MZ1024EFH064";
        private static string outputDir = ".";
        private static string projectName = "";
        private static bool includeStartup = false;

        static void Main(string[] args)
        {
            // Check arguments
            if (args.Length == 0)
            {
                ShowUsage();
                return;
            }

            // Parse arguments
            projectName = args[0];
            if (args.Length > 1) device = args[1];
            if (args.Length > 2) outputDir = args[2];
            if (args.Length > 3 && args[3].ToLower() == "mikroc") includeStartup = true;

            // Ensure output directory exists
            if (!Directory.Exists(outputDir))
            {
                Console.WriteLine($"Creating root directory: {outputDir}");
                try
                {
                    Directory.CreateDirectory(outputDir);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error: Could not create root directory '{outputDir}': {ex.Message}");
                    return;
                }
            }

            string projectRoot = Path.Combine(outputDir, projectName);

            // Show project info
            Console.WriteLine("PIC32MZ Project Generator");
            Console.WriteLine("==========================");
            Console.WriteLine($"Project Name: {projectName}");
            Console.WriteLine($"Device: {device}");
            Console.WriteLine($"Root Directory: {outputDir}");
            Console.WriteLine($"Project Location: {projectRoot}");
            if (includeStartup) Console.WriteLine("MikroC support: ENABLED");
            Console.WriteLine();

            try
            {
                CreateProjectStructure(projectRoot);
                CreateRootMakefile(projectRoot);
                CreateSrcsMakefile(projectRoot);
                CreateTemplateFiles(projectRoot);
                CreateVSCodeConfiguration(projectRoot);
                if (includeStartup) CreateStartupFiles(projectRoot);

                Console.WriteLine();
                Console.WriteLine($"✅ Project '{projectName}' generated successfully!");
                Console.WriteLine($"📁 Location: {projectRoot}");
                Console.WriteLine();
                Console.WriteLine("Next steps:");
                Console.WriteLine($"  cd {projectName}");
                Console.WriteLine("  make build_dir");
                Console.WriteLine("  make");
                Console.WriteLine();
                if (includeStartup)
                {
                    Console.WriteLine("MikroC startup files included for bootloader compatibility! 🚀");
                }
                else
                {
                    Console.WriteLine("The project is ready for development! 🚀");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error generating project: {ex.Message}");
                Environment.Exit(1);
            }
        }

        static void ShowUsage()
        {
            Console.WriteLine($"Usage: {System.AppDomain.CurrentDomain.FriendlyName} <project_name> [device] [root_directory] [mikroc]");
            Console.WriteLine();
            Console.WriteLine("Arguments:");
            Console.WriteLine("  project_name     Name of the project to generate (required)");
            Console.WriteLine("  device          PIC32MZ device (default: 32MZ1024EFH064)");
            Console.WriteLine("  root_directory  Root directory where project folder will be created (default: current directory)");
            Console.WriteLine("  mikroc          Include startup files for MikroC compatibility (optional)");
            Console.WriteLine();
            Console.WriteLine("Examples:");
            Console.WriteLine($"  {System.AppDomain.CurrentDomain.FriendlyName} MyProject");
            Console.WriteLine($"  {System.AppDomain.CurrentDomain.FriendlyName} MyProject 32MZ2048EFH064");
            Console.WriteLine($"  {System.AppDomain.CurrentDomain.FriendlyName} MyProject 32MZ1024EFH064 C:\\Projects");
            Console.WriteLine($"  {System.AppDomain.CurrentDomain.FriendlyName} MyProject 32MZ1024EFH064 C:\\Projects mikroc");
            Console.WriteLine();
            Console.WriteLine("The script will create: <root_directory>\\<project_name>\\");
        }

        static void CreateProjectStructure(string projectRoot)
        {
            Console.WriteLine("Creating directory structure...");

            Directory.CreateDirectory(projectRoot);
            Directory.CreateDirectory(Path.Combine(projectRoot, "srcs"));
            Directory.CreateDirectory(Path.Combine(projectRoot, "incs"));
            Directory.CreateDirectory(Path.Combine(projectRoot, "objs"));
            Directory.CreateDirectory(Path.Combine(projectRoot, "bins"));
            Directory.CreateDirectory(Path.Combine(projectRoot, "other"));
            Directory.CreateDirectory(Path.Combine(projectRoot, "docs"));

            if (includeStartup)
            {
                Directory.CreateDirectory(Path.Combine(projectRoot, "srcs", "startup"));
                Console.WriteLine("  + Added startup directory for MikroC support");
            }

            Console.WriteLine("✓ Directory structure created");
        }

        static void CreateRootMakefile(string projectRoot)
        {
            Console.WriteLine("Creating root Makefile...");

            var makefile = new StringBuilder();
            makefile.AppendLine("# Name of the project binary");
            makefile.AppendLine($"MODULE    \t:= {projectName}");
            makefile.AppendLine();
            makefile.AppendLine("# Device configuration");
            makefile.AppendLine($"DEVICE \t\t:= {device}");
            makefile.AppendLine();
            makefile.AppendLine("# Cross-platform compiler and DFP paths");
            makefile.AppendLine("ifeq ($(OS),Windows_NT)");
            makefile.AppendLine("    COMPILER_LOCATION := C:/Program Files/Microchip/xc32/v4.60/bin");
            makefile.AppendLine("    DFP_LOCATION := C:/Program Files/Microchip/MPLABX/v6.25/packs");
            makefile.AppendLine("else");
            makefile.AppendLine("    COMPILER_LOCATION := /opt/microchip/xc32/v4.60/bin");
            makefile.AppendLine("    DFP_LOCATION := /opt/microchip/mplabx/v6.25/packs");
            makefile.AppendLine("endif");
            makefile.AppendLine("DFP := $(DFP_LOCATION)/Microchip/PIC32MZ-EF_DFP/1.4.168");
            makefile.AppendLine();
            makefile.AppendLine("# Build system");
            makefile.AppendLine("BUILD=make");
            makefile.AppendLine("CLEAN=make clean");
            makefile.AppendLine("BUILD_DIR=make build_dir");
            makefile.AppendLine();
            makefile.AppendLine("all:");
            makefile.AppendLine("\t@echo \"######  BUILDING   ########\"");
            makefile.AppendLine("\tcd srcs && $(BUILD) COMPILER_LOCATION=\"$(COMPILER_LOCATION)\" DFP_LOCATION=\"$(DFP_LOCATION)\" DFP=\"$(DFP)\" DEVICE=$(DEVICE) MODULE=$(MODULE)");
            makefile.AppendLine("\t@echo \"###### BIN TO HEX ########\"");
            makefile.AppendLine("\tcd bins && \"$(COMPILER_LOCATION)/xc32-bin2hex\" $(MODULE)");
            makefile.AppendLine("\t@echo \"######  BUILD COMPLETE   ########\"");
            makefile.AppendLine();
            makefile.AppendLine("build_dir:");
            makefile.AppendLine("\t@echo \"#######BUILDING DIRECTORIES FOR OUTPUT BINARIES#######\"");
            makefile.AppendLine("\tcd srcs && $(BUILD_DIR)");
            makefile.AppendLine();
            makefile.AppendLine("debug:");
            makefile.AppendLine("\t@echo \"#######DEBUGGING OUTPUTS#######\"");
            makefile.AppendLine("\tcd srcs && $(BUILD) debug COMPILER_LOCATION=\"$(COMPILER_LOCATION)\" DFP_LOCATION=\"$(DFP_LOCATION)\" DFP=\"$(DFP)\" DEVICE=$(DEVICE) MODULE=$(MODULE)");
            makefile.AppendLine();
            makefile.AppendLine("platform:");
            makefile.AppendLine("\t@echo \"#######PLATFORM INFO#######\"");
            makefile.AppendLine("\tcd srcs && $(BUILD) platform COMPILER_LOCATION=\"$(COMPILER_LOCATION)\" DFP_LOCATION=\"$(DFP_LOCATION)\" DFP=\"$(DFP)\" DEVICE=$(DEVICE) MODULE=$(MODULE)");
            makefile.AppendLine();
            makefile.AppendLine("clean:");
            makefile.AppendLine("\t@echo \"####### CLEANING OUTPUTS #######\"");
            makefile.AppendLine("\tcd srcs && $(CLEAN)");
            makefile.AppendLine("\t@echo \"####### REMOVING BUILD ARTIFACTS #######\"");
            makefile.AppendLine("ifeq ($(OS),Windows_NT)");
            makefile.AppendLine("\t@if exist \"bins\\\\*\" del /q \"bins\\\\*\" >nul 2>&1");
            makefile.AppendLine("\t@if exist \"objs\\\\*\" rmdir /s /q \"objs\" >nul 2>&1 && mkdir \"objs\" >nul 2>&1");
            makefile.AppendLine("\t@if exist \"other\\\\*\" del /q \"other\\\\*\" >nul 2>&1");
            makefile.AppendLine("else");
            makefile.AppendLine("\t@rm -rf bins/* objs/* other/* 2>/dev/null || true");
            makefile.AppendLine("endif");
            makefile.AppendLine();
            makefile.AppendLine(".PHONY: all build_dir clean debug platform");

            File.WriteAllText(Path.Combine(projectRoot, "Makefile"), makefile.ToString());
            Console.WriteLine("✓ Root Makefile created");
        }

        static void CreateSrcsMakefile(string projectRoot)
        {
            Console.WriteLine("Creating srcs Makefile...");

            var makefile = new StringBuilder();
            makefile.AppendLine("# Simple Makefile for PIC32MZ project");
            makefile.AppendLine("# DFP configuration");
            makefile.AppendLine("DFP_DIR := $(DFP)");
            makefile.AppendLine("DFP_INCLUDE := $(DFP)/include");
            makefile.AppendLine();
            makefile.AppendLine("# Cross-platform support");
            makefile.AppendLine("ifeq ($(OS),Windows_NT)");
            makefile.AppendLine("    detected_OS := Windows");
            makefile.AppendLine("    MKDIR = if not exist \"$(subst /,\\\\,$(1))\" mkdir \"$(subst /,\\\\,$(1))\"");
            makefile.AppendLine("else");
            makefile.AppendLine("    detected_OS := Unix");
            makefile.AppendLine("    MKDIR = mkdir -p $(1)");
            makefile.AppendLine("endif");
            makefile.AppendLine();
            makefile.AppendLine("# Project directories");
            makefile.AppendLine("ROOT     := ..");
            makefile.AppendLine("OBJ_DIR  := $(ROOT)/objs");
            makefile.AppendLine("INC_DIR  := $(ROOT)/incs");
            makefile.AppendLine("BIN_DIR  := $(ROOT)/bins");
            makefile.AppendLine("OUT_DIR  := $(ROOT)/other");
            makefile.AppendLine();
            makefile.AppendLine("# Source files");
            makefile.AppendLine("SRCS := $(wildcard *.c)");
            makefile.AppendLine("OBJS := $(SRCS:%.c=$(OBJ_DIR)/%.o)");
            makefile.AppendLine();
            makefile.AppendLine("# Compiler and flags");
            makefile.AppendLine("CC := \"$(COMPILER_LOCATION)/xc32-gcc\"");
            makefile.AppendLine("MCU := -mprocessor=$(DEVICE)");
            makefile.AppendLine("FLAGS := -Werror -Wall -MP -MMD -g -O1 -ffunction-sections -fdata-sections -fno-common");
            makefile.AppendLine("INCS := -I\"$(INC_DIR)\" -I\"$(DFP_INCLUDE)\"");
            makefile.AppendLine();
            makefile.AppendLine("# Build target");
            makefile.AppendLine("$(BIN_DIR)/$(MODULE): $(OBJS)");
            makefile.AppendLine("\t@echo \"Linking $(MODULE) for $(DEVICE)\"");
            makefile.AppendLine("\t$(CC) $(MCU) -nostartfiles -mdfp=\"$(DFP)\" -Wl,--script=\"$(DFP)/xc32/$(DEVICE)/p32MZ1024EFH064.ld\" -Wl,-Map=\"$(OUT_DIR)/production.map\" -o $@ $^");
            makefile.AppendLine("\t@echo \"Build complete: $@\"");
            makefile.AppendLine();
            makefile.AppendLine("# Compile rule");
            makefile.AppendLine("$(OBJ_DIR)/%.o: %.c");
            makefile.AppendLine("\t@echo \"Compiling $< to $@\"");
            makefile.AppendLine("\t@$(call MKDIR,$(dir $@))");
            makefile.AppendLine("\t$(CC) -x c -c $(MCU) $(FLAGS) $(INCS) -mdfp=\"$(DFP)\" -MF $(@:%.o=%.d) $< -o $@");
            makefile.AppendLine();
            makefile.AppendLine("# Targets");
            makefile.AppendLine(".PHONY: all build_dir clean debug platform");
            makefile.AppendLine();
            makefile.AppendLine("all: $(BIN_DIR)/$(MODULE)");
            makefile.AppendLine();
            makefile.AppendLine("build_dir:");
            makefile.AppendLine("\t@echo \"Creating build directories ($(detected_OS))\"");
            makefile.AppendLine("\t@$(call MKDIR,$(OBJ_DIR))");
            makefile.AppendLine("\t@$(call MKDIR,$(BIN_DIR))");
            makefile.AppendLine("\t@$(call MKDIR,$(OUT_DIR))");
            makefile.AppendLine("\t@echo \"Build directories created\"");
            makefile.AppendLine();
            makefile.AppendLine("clean:");
            makefile.AppendLine("\t@echo \"Cleaning build artifacts\"");
            makefile.AppendLine("ifeq ($(OS),Windows_NT)");
            makefile.AppendLine("\t@if exist \"$(OBJ_DIR)\\\\*\" rmdir /s /q \"$(OBJ_DIR)\" >nul 2>&1 && mkdir \"$(OBJ_DIR)\" >nul 2>&1");
            makefile.AppendLine("\t@if exist \"$(BIN_DIR)\\\\*\" del /q \"$(BIN_DIR)\\\\*\" >nul 2>&1");
            makefile.AppendLine("\t@if exist \"$(OUT_DIR)\\\\*\" del /q \"$(OUT_DIR)\\\\*\" >nul 2>&1");
            makefile.AppendLine("else");
            makefile.AppendLine("\t@rm -rf $(OBJ_DIR)/* $(BIN_DIR)/* $(OUT_DIR)/* 2>/dev/null || true");
            makefile.AppendLine("\t@mkdir -p $(OBJ_DIR)");
            makefile.AppendLine("endif");
            makefile.AppendLine("\t@echo \"Clean complete\"");
            makefile.AppendLine();
            makefile.AppendLine("debug:");
            makefile.AppendLine("\t@echo \"Build system debug info:\"");
            makefile.AppendLine("\t@echo \"Source files: $(SRCS)\"");
            makefile.AppendLine("\t@echo \"Object files: $(OBJS)\"");
            makefile.AppendLine();
            makefile.AppendLine("platform:");
            makefile.AppendLine("\t@echo \"Platform: $(detected_OS)\"");
            makefile.AppendLine("\t@echo \"Compiler: $(CC)\"");
            makefile.AppendLine("\t@echo \"Device: $(DEVICE)\"");

            File.WriteAllText(Path.Combine(projectRoot, "srcs", "Makefile"), makefile.ToString());
            Console.WriteLine("✓ Srcs Makefile created");
        }

        static void CreateTemplateFiles(string projectRoot)
        {
            Console.WriteLine("Creating template files...");

            // main.c in srcs
            var mainC = new StringBuilder();
            mainC.AppendLine("/*******************************************************************************");
            mainC.AppendLine("  Main Source File");
            mainC.AppendLine("");
            mainC.AppendLine("  Company:");
            mainC.AppendLine("    Your Company Name");
            mainC.AppendLine("");
            mainC.AppendLine("  File Name:");
            mainC.AppendLine("    main.c");
            mainC.AppendLine("");
            mainC.AppendLine("  Summary:");
            mainC.AppendLine($"    This file contains the \"main\" function for {projectName}.");
            mainC.AppendLine("");
            mainC.AppendLine("  Description:");
            mainC.AppendLine("    This file contains the \"main\" function for the project.");
            mainC.AppendLine("    Simple bare-metal main function without system initialization dependencies.");
            mainC.AppendLine(" *******************************************************************************/");
            mainC.AppendLine("");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// Section: Included Files");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("");
            mainC.AppendLine("#include <stddef.h>                     // Defines NULL");
            mainC.AppendLine("#include <stdbool.h>                    // Defines true");
            mainC.AppendLine("#include <stdlib.h>                     // Defines EXIT_FAILURE");
            mainC.AppendLine("#include <stdint.h>                     // Defines uint32_t, uintptr_t");
            mainC.AppendLine("");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// Variables ");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// Section: Main Entry Point");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("// *****************************************************************************");
            mainC.AppendLine("");
            mainC.AppendLine("int main ( void )");
            mainC.AppendLine("{");
            mainC.AppendLine("    // Initialize your hardware/peripherals here");
            mainC.AppendLine("    // Example: GPIO configuration, clock setup, etc.");
            mainC.AppendLine("    ");
            mainC.AppendLine("    while ( true )");
            mainC.AppendLine("    {");
            mainC.AppendLine("        // Your main application code here");
            mainC.AppendLine("        // Example: toggle LED, read sensors, communicate, etc.");
            mainC.AppendLine("    }");
            mainC.AppendLine("");
            mainC.AppendLine("    /* Execution should not come here during normal operation */");
            mainC.AppendLine("    return ( EXIT_FAILURE );");
            mainC.AppendLine("}");
            mainC.AppendLine("");
            mainC.AppendLine("/*******************************************************************************");
            mainC.AppendLine(" End of File");
            mainC.AppendLine("*/");

            File.WriteAllText(Path.Combine(projectRoot, "srcs", "main.c"), mainC.ToString());

            // definitions.h in incs
            var definitionsH = new StringBuilder();
            definitionsH.AppendLine("/*******************************************************************************");
            definitionsH.AppendLine("  System Definitions");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("  File Name:");
            definitionsH.AppendLine("    definitions.h");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("  Summary:");
            definitionsH.AppendLine($"    {projectName} system definitions.");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("  Description:");
            definitionsH.AppendLine($"    This file contains the system-wide prototypes and definitions for {projectName}.");
            definitionsH.AppendLine("");
            definitionsH.AppendLine(" *******************************************************************************/");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("#ifndef DEFINITIONS_H");
            definitionsH.AppendLine("#define DEFINITIONS_H");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// Section: Included Files");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("#include <stddef.h>");
            definitionsH.AppendLine("#include <stdbool.h>");
            definitionsH.AppendLine("#include <stdint.h>");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// Section: Project Definitions");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("// Add your project-specific definitions here");
            definitionsH.AppendLine("// Examples:");
            definitionsH.AppendLine("// #define LED_PIN     1");
            definitionsH.AppendLine("// #define BUTTON_PIN  2");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// Section: Function Prototypes");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("// *****************************************************************************");
            definitionsH.AppendLine("#ifdef __cplusplus  // Provide C++ Compatibility");
            definitionsH.AppendLine("extern \"C\" {");
            definitionsH.AppendLine("#endif");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("// Add your function prototypes here");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("#ifdef __cplusplus");
            definitionsH.AppendLine("}");
            definitionsH.AppendLine("#endif");
            definitionsH.AppendLine("");
            definitionsH.AppendLine("#endif /* DEFINITIONS_H */");

            File.WriteAllText(Path.Combine(projectRoot, "incs", "definitions.h"), definitionsH.ToString());

            // README.md
            var readme = new StringBuilder();
            readme.AppendLine($"# {projectName}");
            readme.AppendLine("");
            readme.AppendLine("PIC32MZ Embedded Project using XC32 Compiler");
            readme.AppendLine("");
            readme.AppendLine("## Device");
            readme.AppendLine($"- **Microcontroller**: {device}");
            readme.AppendLine("- **Compiler**: XC32 v4.60+");
            readme.AppendLine("");
            readme.AppendLine("## Building");
            readme.AppendLine("");
            readme.AppendLine("```bash");
            readme.AppendLine("make");
            readme.AppendLine("```");
            readme.AppendLine("");
            readme.AppendLine("## Useful Commands");
            readme.AppendLine("");
            readme.AppendLine("- `make` - Build the project");
            readme.AppendLine("- `make clean` - Clean build artifacts");
            readme.AppendLine("- `make debug` - Show build configuration");
            readme.AppendLine("- `make platform` - Show cross-platform settings");
            readme.AppendLine("");
            readme.AppendLine("Generated by PIC32MZ Project Generator");

            File.WriteAllText(Path.Combine(projectRoot, "README.md"), readme.ToString());

            // .gitignore
            var gitignore = new StringBuilder();
            gitignore.AppendLine("# Build outputs");
            gitignore.AppendLine("objs/");
            gitignore.AppendLine("bins/");
            gitignore.AppendLine("other/");
            gitignore.AppendLine("*.o");
            gitignore.AppendLine("*.d");
            gitignore.AppendLine("*.hex");
            gitignore.AppendLine("*.elf");
            gitignore.AppendLine("*.map");
            gitignore.AppendLine("*.xml");
            gitignore.AppendLine("");
            gitignore.AppendLine("# IDE files");
            gitignore.AppendLine("*.X/");
            gitignore.AppendLine(".generated_files/");
            gitignore.AppendLine("");
            gitignore.AppendLine("# System files");
            gitignore.AppendLine(".DS_Store");
            gitignore.AppendLine("Thumbs.db");

            File.WriteAllText(Path.Combine(projectRoot, ".gitignore"), gitignore.ToString());

            Console.WriteLine("✓ Template files created");
        }

        static void CreateStartupFiles(string projectRoot)
        {
            Console.WriteLine("Creating startup files for MikroC support...");

            string startupPath = Path.Combine(projectRoot, "srcs", "startup", "startup.S");

            if (!File.Exists(startupPath))
            {
                var startup = new StringBuilder();
                startup.AppendLine("/*******************************************************************************");
                startup.AppendLine("  System Startup File");
                startup.AppendLine(" *******************************************************************************/");
                startup.AppendLine("");
                startup.AppendLine("#include <xc.h>");
                startup.AppendLine("");
                startup.AppendLine("    .section .vector_0,code, keep");
                startup.AppendLine("    .equ __vector_spacing_0, 0x00000001");
                startup.AppendLine("    .align 4");
                startup.AppendLine("    .set nomips16");
                startup.AppendLine("    .set noreorder");
                startup.AppendLine("    .ent __vector_0");
                startup.AppendLine("__vector_0:");
                startup.AppendLine("    j  _startup");
                startup.AppendLine("    nop");
                startup.AppendLine("    .end __vector_0");
                startup.AppendLine("    .size __vector_0, .-__vector_0");
                startup.AppendLine("");
                startup.AppendLine("    .section .startup,code, keep");
                startup.AppendLine("    .align 4");
                startup.AppendLine("    .set nomips16");
                startup.AppendLine("    .set noreorder");
                startup.AppendLine("    .ent _startup");
                startup.AppendLine("_startup:");
                startup.AppendLine("    # Add your startup code here");
                startup.AppendLine("    # Jump to main");
                startup.AppendLine("    la   $t0, main");
                startup.AppendLine("    jr   $t0");
                startup.AppendLine("    nop");
                startup.AppendLine("    .end _startup");
                startup.AppendLine("    .size _startup, .-_startup");

                File.WriteAllText(startupPath, startup.ToString());
                Console.WriteLine($"✓ Created startup file: {startupPath}");
            }
            else
            {
                Console.WriteLine($"✓ Startup file already exists: {startupPath}");
            }

            Console.WriteLine("✓ Startup files processed");
        }

        static void CreateVSCodeConfiguration(string projectRoot)
        {
            Console.WriteLine("Creating VS Code configuration...");

            var vscodeDir = Path.Combine(projectRoot, ".vscode");
            Directory.CreateDirectory(vscodeDir);

            // tasks.json
            var tasksJson = @"{
    ""version"": ""2.0.0"",
    ""tasks"": [
        {
            ""label"": ""makemake"",
            ""type"": ""shell"",
            ""command"": ""make"",
            ""group"": {
                ""kind"": ""build"",
                ""isDefault"": true
            },
            ""presentation"": {
                ""echo"": true,
                ""reveal"": ""always"",
                ""focus"": false,
                ""panel"": ""shared""
            },
            ""problemMatcher"": [
                ""$gcc""
            ]
        },
        {
            ""label"": ""makeclean"",
            ""type"": ""shell"",
            ""command"": ""make"",
            ""args"": [""clean""],
            ""group"": ""build"",
            ""presentation"": {
                ""echo"": true,
                ""reveal"": ""always"",
                ""focus"": false,
                ""panel"": ""shared""
            }
        },
        {
            ""label"": ""Flash"",
            ""type"": ""shell"",
            ""command"": ""make"",
            ""args"": [""flash""],
            ""group"": ""build"",
            ""presentation"": {
                ""echo"": true,
                ""reveal"": ""always"",
                ""focus"": false,
                ""panel"": ""shared""
            },
            ""dependsOn"": ""makemake""
        },
        {
            ""label"": ""Test"",
            ""type"": ""shell"",
            ""command"": ""make"",
            ""args"": [""test""],
            ""group"": {
                ""kind"": ""test"",
                ""isDefault"": true
            },
            ""presentation"": {
                ""echo"": true,
                ""reveal"": ""always"",
                ""focus"": false,
                ""panel"": ""shared""
            }
        }
    ]
}";
            File.WriteAllText(Path.Combine(vscodeDir, "tasks.json"), tasksJson);

            // launch.json
            var launchJson = $@"{{
    ""version"": ""0.2.0"",
    ""configurations"": [
        {{
            ""name"": ""Debug {projectName}"",
            ""type"": ""cppdbg"",
            ""request"": ""launch"",
            ""program"": ""${{workspaceFolder}}/bins/{projectName}.elf"",
            ""args"": [],
            ""stopAtEntry"": true,
            ""cwd"": ""${{workspaceFolder}}"",
            ""environment"": [],
            ""externalConsole"": false,
            ""MIMode"": ""gdb"",
            ""miDebuggerPath"": ""C:/Program Files/Microchip/xc32/v4.60/bin/xc32-gdb.exe"",
            ""setupCommands"": [
                {{
                    ""description"": ""Enable pretty-printing for gdb"",
                    ""text"": ""-enable-pretty-printing"",
                    ""ignoreFailures"": true
                }}
            ],
            ""preLaunchTask"": ""makemake"",
            ""miDebuggerServerAddress"": ""localhost:3333"",
            ""debugServerPath"": ""openocd"",
            ""debugServerArgs"": ""-f interface/pickit4.cfg -f target/pic32mz.cfg"",
            ""serverStarted"": ""Info : Listening on port 3333 for gdb connections"",
            ""filterStderr"": true,
            ""customLaunchSetupCommands"": [
                {{
                    ""text"": ""target remote localhost:3333""
                }},
                {{
                    ""text"": ""monitor reset halt""
                }},
                {{
                    ""text"": ""load""
                }}
            ]
        }}
    ]
}}";
            File.WriteAllText(Path.Combine(vscodeDir, "launch.json"), launchJson);

            // c_cpp_properties.json
            var cppPropertiesJson = $@"{{
    ""version"": 4,
    ""configurations"": [
        {{
            ""name"": ""XC32"",
            ""includePath"": [
                ""${{workspaceFolder}}/incs"",
                ""${{workspaceFolder}}/srcs"",
                ""C:/Program Files/Microchip/xc32/v4.60/pic32mx/include"",
                ""C:/Program Files/Microchip/xc32/v4.60/include"",
                ""C:/Program Files/Microchip/MPLABX/v6.20/packs/Microchip/PIC32MZ-EF_DFP/1.3.58/xc32""
            ],
            ""defines"": [
                ""__PIC32MZ__"",
                ""__32{device}__"",
                ""__XC32__""
            ],
            ""compilerPath"": ""C:/Program Files/Microchip/xc32/v4.60/bin/xc32-gcc.exe"",
            ""cStandard"": ""c99"",
            ""cppStandard"": ""c++14"",
            ""intelliSenseMode"": ""gcc-x86""
        }}
    ]
}}";
            File.WriteAllText(Path.Combine(vscodeDir, "c_cpp_properties.json"), cppPropertiesJson);

            Console.WriteLine("✓ VS Code configuration created");
        }
    }
}
