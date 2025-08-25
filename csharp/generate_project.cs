using generate_project;
using System;
using System.IO;
using System.Reflection;
using System.Text;

namespace PIC32MZProjectGenerator
{

    class Program
    {
        static MAKE_Strings makeStrings;
        static startup startup;

        // Default values
        private static string device = "32MZ1024EFH064";
        private static string outputDir = ".";
        private static string projectName = "";
        private static bool includeStartup = false;
        private static bool includeDefinitions = false;
        static void Main(string[] args)
        {
            // Check arguments
            if (args.Length == 0)
            {
                ShowUsage();
                return;
            }

            // Parse arguments for options
            projectName = args[0];

            for (int i = 1; i < args.Length; i++)
            {
                if (args[i] == "-d" || args[i] == "--device")
                {
                    if (i + 1 < args.Length)
                    {
                        device = args[i + 1];
                        i++; // skip value
                    }
                }
                else if (args[i] == "-o" || args[i] == "--output")
                {
                    if (i + 1 < args.Length)
                    {
                        outputDir = args[i + 1];
                        i++; // skip value
                    }
                }
                else if (args[i].ToLower() == "--mikroc")
                {
                    includeStartup = true;
                    if(i + 1 < args.Length)
                    { 
                        i++; // skip value
                    }
                }
                else if (args[i].ToLower() == "--definitions" || args[i] == "-h")
                {           
                    includeDefinitions = true;
                }


            }

            // Check for required project name
            if (string.IsNullOrEmpty(projectName))
            {
                ShowUsage();
                return;
            }

            // Parse arguments        

            /*
             if (args.Length > 1) device = args[1];
             if (args.Length > 2) outputDir = args[2];
             if (args.Length > 3 && args[3].ToLower() == "mikroc") includeStartup = true;
           */

            // Ensure output directory exists
            //  makeStrings = new MAKE_Strings(projectName, device);
            //  startup = new startup();

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
                //CreateRootMakefile(projectRoot);
                CopyRootMakefile(projectRoot);
                //CreateSrcsMakefile(projectRoot);
                CopySrcMakefile(projectRoot);
                CreateTemplateFiles(projectRoot);
                CreateVSCodeConfiguration(projectRoot);
                //if (includeStartup) CreateStartupFiles(projectRoot);
                if (includeStartup) CopyStartupFiles(projectRoot);
                if (includeDefinitions) CopyDefinitionsfile(projectRoot);

                Console.WriteLine();
                Console.WriteLine($"✅ Project '{projectName}' generated successfully!");
                Console.WriteLine($"?  Ensure that xc32 Compiler is installed on your pc and its PATH is set");
                Console.WriteLine($"📁 Location: {projectRoot}");
                Console.WriteLine();
                Console.WriteLine("Next steps:");
                Console.WriteLine($"  cd {projectRoot}\\{projectName}");
                Console.WriteLine("   make cmdlet               #- A detailed view of all make commands.");
                Console.WriteLine("   make build_dir  DRY_RUN=1 #- Test folder and file manipulation.");
                Console.WriteLine("   make build_dir  DRY_RUN=0 #- Run folder and file manipulation.");
                Console.WriteLine("   make                      #- Build the project");
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


        #region Copy files from dependancies folder
        // Copy the Makefile_Root to root directory
        static void CopyRootMakefile(string projectRoot)
        {
            string currentDir = Directory.GetCurrentDirectory();
            string project_root = Directory.GetParent(currentDir).Parent.FullName;
            string sourcePath = Path.Combine(project_root, "..\\..\\dependancies\\Makefile_Root");
            string destPath = Path.Combine(projectRoot, "Makefile");
            if (File.Exists(sourcePath))
            {
                File.Copy(sourcePath, destPath);
                Console.WriteLine("✓ Copied root Makefile to root directory");
            }
            else
            {
                Console.WriteLine("✗ Root Makefile not found to copy @ " + sourcePath);
            }
        }


        // Copy the Makefile_SRC to srcs directory
        static void CopySrcMakefile(string projectRoot)
        {
            string currentDir = Directory.GetCurrentDirectory();
            string project_root = Directory.GetParent(currentDir).Parent.FullName;
            string sourcePath = Path.Combine(project_root, "..\\..\\dependancies\\Makefile_Srcs");
            string destPath = Path.Combine(projectRoot, "srcs", "Makefile");
            if (File.Exists(sourcePath))
            {
                File.Copy(sourcePath, destPath);
                Console.WriteLine("✓ Copied srcs Makefile to srcs directory");
            }
            else
            {
                Console.WriteLine("✗ Srcs Makefile not found to copy @ " + sourcePath);
            }
        }

        // Copy the startup.S file to srcs/startup directory
        static void CopyStartupFiles(string projectRoot)
        {
            string currentDir = Directory.GetCurrentDirectory();
            string project_root = Directory.GetParent(currentDir).Parent.FullName;
            string sourcePath = Path.Combine(project_root, "..\\..\\dependancies\\startup.S");
            string destDir = Path.Combine(projectRoot, "srcs", "startup");
            string destPath = Path.Combine(destDir, "startup.S");
            if (!Directory.Exists(destDir))
            {
                Directory.CreateDirectory(destDir);
            }
            if (File.Exists(sourcePath))
            {
                File.Copy(sourcePath, destPath, true);
                Console.WriteLine("✓ Copied startup file to startup directory");
            }
            else
            {
                Console.WriteLine("✗ Startup file not found to copy @ " + sourcePath);
            }
        }


        // Copy the PIC32MZ_EF_Dev_Board_Definitions.h file to incs directory
        static void CopyDefinitionsfile(string projectRoot)
        {
            string currentDir = Directory.GetCurrentDirectory();
            string project_root = Directory.GetParent(currentDir).Parent.FullName;
            string sourcePath = Path.Combine(project_root, "..\\..\\dependancies\\PIC32MZ_EF_Dev_Board_Definitions.h");
            string destPath = Path.Combine(projectRoot, "incs", "PIC32MZ_EF_Dev_Board_Definitions.h");
            if (File.Exists(sourcePath))
            {
                File.Copy(sourcePath, destPath);
                Console.WriteLine("✓ Copied PIC32MZ_EF_Dev_Board_Definitions.h to incs directory");
            }
            else
            {
                Console.WriteLine("✗ PIC32MZ_EF_Dev_Board_Definitions.h not found to copy @ " + sourcePath);
            }
        }
        #endregion Copy files from dependancies folder

    

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
            ""options"": {
                ""cwd"": ""${workspaceFolder}""
            },
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


            #region un-used functions
        static void CreateRootMakefile(string projectRoot)
        {
            Console.WriteLine("Creating root Makefile...");

            File.WriteAllText(Path.Combine(projectRoot, "Makefile"), makeStrings.Get_RootMakefileContent()); //makefile.ToString());
            Console.WriteLine("✓ Root Makefile created");
        }

        static void CreateSrcsMakefile(string projectRoot)
        {
            Console.WriteLine("Creating srcs Makefile...");

            File.WriteAllText(Path.Combine(projectRoot, "srcs", "Makefile"), makeStrings.Get_SRCMakefileContent());//.Get_SrcsMakefileContent());//makefile.ToString());
            Console.WriteLine("✓ Srcs Makefile created");
        }


        static void CreateStartupFiles(string projectRoot)
        {
            Console.WriteLine("Creating startup files for MikroC support...");

            string startupPath = Path.Combine(projectRoot, "srcs", "startup", "startup.S");

            if (!File.Exists(startupPath))
            {


                File.WriteAllText(startupPath, startup.GetStartupCode());
                Console.WriteLine($"✓ Created startup file: {startupPath}");
            }
            else
            {
                Console.WriteLine($"✓ Startup file already exists: {startupPath}");
            }

            Console.WriteLine("✓ Startup files processed");
        }
        #endregion un-used functions
    }
}
