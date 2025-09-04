using csharp;
using Microsoft.VisualBasic.ApplicationServices;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using System.Text.Json;


namespace Setup
{



    public partial class Form1 : Form
    {
        // Move the initialization of configBitComboBoxes from field initializer to the constructor

        private Dictionary<string, ComboBox> configBitComboBoxes;
        //
        //private string path = String.Empty;//"C:\\Users\\Automation\\GIT\\XC32_VSCODE_PROJ_BUILDER\\Setup\\device_config.json";
        private string path = System.IO.Path.Combine(Application.StartupPath, "device_config.json");

        // Add this mapping in your Form1 class
        private Dictionary<string, string> configBitSections = new Dictionary<string, string>
        {
            // DEVCFG0
            { "DEBUG", "DEVCFG0" }, { "JTAGEN", "DEVCFG0" }, { "ICESEL", "DEVCFG0" }, { "TRCEN", "DEVCFG0" }, { "BOOTISA", "DEVCFG0" }, { "FECCCON", "DEVCFG0" }, { "FSLEEP", "DEVCFG0" }, { "DBGPER", "DEVCFG0" }, { "SMCLR", "DEVCFG0" }, { "SOSCGAIN", "DEVCFG0" }, { "SOSCBOOST", "DEVCFG0" }, { "POSCGAIN", "DEVCFG0" }, { "POSCBOOST", "DEVCFG0" }, { "EJTAGBEN", "DEVCFG0" },
            // DEVCFG1
            { "FNOSC", "DEVCFG1" }, { "DMTINTV", "DEVCFG1" }, { "FSOSCEN", "DEVCFG1" }, { "IESO", "DEVCFG1" }, { "POSCMOD", "DEVCFG1" }, { "OSCIOFNC", "DEVCFG1" }, { "FCKSM", "DEVCFG1" }, { "WDTPS", "DEVCFG1" }, { "WDTSPGM", "DEVCFG1" }, { "FWDTEN", "DEVCFG1" }, { "WINDIS", "DEVCFG1" }, { "FWDTWINSZ", "DEVCFG1" }, { "DMTCNT", "DEVCFG1" }, { "FDMTEN", "DEVCFG1" },
            // DEVCFG2
            { "FPLLIDIV", "DEVCFG2" }, { "FPLLRNG", "DEVCFG2" }, { "FPLLICLK", "DEVCFG2" }, { "FPLLMULT", "DEVCFG2" }, { "FPLLODIV", "DEVCFG2" }, { "UPLLFSEL", "DEVCFG2" },
            // DEVCFG3
            { "FMIIEN", "DEVCFG3" }, { "FETHIO", "DEVCFG3" }, { "PGL1WAY", "DEVCFG3" }, { "PMDL1WAY", "DEVCFG3" }, { "IOL1WAY", "DEVCFG3" }, { "FUSBIDIO", "DEVCFG3" },
            // DEVCP0
            { "CP", "DEVCP0" }
        };


        private Dictionary<string, CheckBox> peripheralCheckBoxes;

        private List<GpioPinConfig> gpioPinConfigs;
        private Dictionary<int, ComboBox> gpioPinFunctionCombos;
        private Dictionary<int, TextBox> gpioPinNameTextBoxes;
        private const int TOTAL_GPIO_PINS = 32; // Adjust based on your device

        public Form1()
        {
            InitializeComponent();
            this.AutoScaleMode = AutoScaleMode.Font;
            
            // Initialize variant combo box
            if (comboBoxVariant != null)
            {
                comboBoxVariant.Items.Clear();
                comboBoxVariant.Items.AddRange(new string[] { "MZ", "MX" });
                comboBoxVariant.SelectedItem = "MZ"; // Default
                comboBoxVariant.SelectedIndexChanged += ComboBoxVariant_SelectedIndexChanged;
            }
            
            // Initialize device combo box based on default variant
            UpdateDeviceComboBox("MZ");
            
            // Initialize the dictionary mapping config bits to their respective ComboBoxes
            configBitComboBoxes = new Dictionary<string, ComboBox>
            {
                // DEVCFG0
                { "DEBUG", comboBox_DEBUG },
                { "JTAGEN", comboBox_JTAGEN },
                { "ICESEL", comboBox_ICESEL },
                { "TRCEN", comboBox_TRCEN },
                { "BOOTISA", comboBox_BOOTISA },
                { "FECCCON", comboBox_FECCCON },
                { "FSLEEP", comboBox_FSLEEP },
                { "DBGPER", comboBox_DBGPER },
                { "SMCLR", comboBox_SMCLR },
                { "SOSCGAIN", comboBox_SOSCGAIN },
                { "SOSCBOOST", comboBox_SOSCBOOST },
                { "POSCGAIN", comboBox_POSCGAIN },
                { "POSCBOOST", comboBox_POSCBOOST },
                { "EJTAGBEN", comboBox_EJTAGBEN },

                // DEVCFG1
                { "FNOSC", comboBox_FNOSC },
                { "DMTINTV", comboBox_DMTINTV },
                { "FSOSCEN", comboBox_FSOSCEN },
                { "IESO", comboBox_IESO },
                { "POSCMOD", comboBox_POSCMOD },
                { "OSCIOFNC", comboBox_OSCIOFNC },
                { "FCKSM", comboBox_FCKSM },
                { "WDTPS", comboBox_WDTPS },
                { "WDTSPGM", comboBox_WDTSPGM },
                { "FWDTEN", comboBox_FWDTEN },
                { "WINDIS", comboBox_WINDIS },
                { "FWDTWINSZ", comboBox_FWDTWINSZ },
                { "DMTCNT", comboBox_DMTCNT },
                { "FDMTEN", comboBox_FDMTEN },

                // DEVCFG2
                { "FPLLIDIV", comboBox_FPLLIDIV },
                { "FPLLRNG", comboBox_FPLLRNG },
                { "FPLLICLK", comboBox_FPLLICLK },
                { "FPLLMULT", comboBox_FPLLMULT },
                { "FPLLODIV", comboBox_FPLLODIV },
                { "UPLLFSEL", comboBox_UPLLFSEL },

                // DEVCFG3
               // { "USERID", comboBox_USERID }, // If you use NumericUpDown, handle separately

                { "FMIIEN", comboBox_FMIIEN },
                { "FETHIO", comboBox_FETHIO },
                { "PGL1WAY", comboBox_PGL1WAY },
                { "PMDL1WAY", comboBox_PMDL1WAY },
                { "IOL1WAY", comboBox_IOL1WAY },
                { "FUSBIDIO", comboBox_FUSBIDIO },

                // DEVCP0
                { "CP", comboBox_CP },

                // BF1SEQ0
                //{ "TSEQ", numericUpDown_TSEQ },
                //{ "CSEQ", numericUpDown_CSEQ }
            };

            // Initialize peripheral checkboxes dictionary
            peripheralCheckBoxes = new Dictionary<string, CheckBox>
            {
                { "enable_UART", checkBox_ENUART },
                { "enable_SPI", checkBox_ENSPI },
                { "enable_I2C", checkBox_ENI2C },
                { "enable_Timer", checkBox_ENTIMER },
                { "enable_ADC", checkBox_ENADC },
                { "enable_CAN", checkBox_ENCAN },
                { "enable_PWM", checkBox_ENPWM }
            };

            // Only initialize GPIO controls - don't add extra tab setup
            InitializeGpioControls();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.TopMost = true;
            // Hide the taskbar icon and set the form as a tool window
            this.ShowInTaskbar = false;
            // this.FormBorderStyle = FormBorderStyle.FixedToolWindow;
            // Do not load configWords or call CreateConfigUI on startup
            LoadConfigToForm(path);
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!String.IsNullOrEmpty(path))
            {
                saveConfig_ToJson(path);
            }
            else
            {
                // MessageBox.Show("No file path specified. Use 'Save As' to specify a file.","Closing Application!",MessageBoxButtons.YesNo,MessageBoxIcon.Exclamation);
                if (DialogResult.Cancel == MessageBox.Show("No file path specified. Use 'Save As' to specify a file. click 'OK' to continue or 'Cancel' to abort.", "Closing Application!", MessageBoxButtons.OKCancel, MessageBoxIcon.Exclamation))
                {
                    e.Cancel = true; // Prevent closing if no path
                    return; // Allow closing
                }

                return;
            }
        }



        #region LOAD/GET CONFIG

        private void LoadConfigToForm(string path_)
        {
            var config = DeviceConfig.Load(path_);
            if (config == null) return;

            // Load variant and update UI controls
            if (!string.IsNullOrEmpty(config.Variant))
            {
                // Update variant combo box
                if (comboBoxVariant != null && comboBoxVariant.Items.Contains(config.Variant))
                {
                    comboBoxVariant.SelectedItem = config.Variant;
                }

                // Update device combo box based on variant
                UpdateDeviceComboBox(config.Variant);

                // Set the selected device if it exists in config
                if (!string.IsNullOrEmpty(config.DeviceName) && comboBox_DEVICE != null)
                {
                    // Remove "PIC" prefix if present to match combo box items
                    string deviceToSelect = config.DeviceName.Replace("PIC", "");
                    if (comboBox_DEVICE.Items.Contains(deviceToSelect))
                    {
                        comboBox_DEVICE.SelectedItem = deviceToSelect;
                    }
                    else if (comboBox_DEVICE.Items.Count > 0)
                    {
                        // Default to first item if saved device not found
                        comboBox_DEVICE.SelectedIndex = 0;
                    }
                }
            }
            else
            {
                // Default to MZ if no variant specified in loaded config
                if (comboBoxVariant != null)
                {
                    comboBoxVariant.SelectedItem = "MZ";
                }
                UpdateDeviceComboBox("MZ");
            }

            // Load from Sections if present - MOVED OUTSIDE THE else BLOCK
            if (config.Sections != null)
            {
                foreach (var section in config.Sections)
                {
                    foreach (var bit in section.Value)
                    {
                        if (bit.Key == "USERID" && numericUpDown_USERID != null)
                        {
                            if (int.TryParse(bit.Value.Replace("0x", ""), System.Globalization.NumberStyles.HexNumber, null, out int userIdValue))
                            {
                                userIdValue = Math.Max((int)numericUpDown_USERID.Minimum, Math.Min(userIdValue, (int)numericUpDown_USERID.Maximum));
                                numericUpDown_USERID.Value = userIdValue;
                            }
                            else
                            {
                                numericUpDown_USERID.Value = 0;
                            }
                        }
                        else if (configBitComboBoxes.TryGetValue(bit.Key, out var comboBox) && comboBox != null)
                        {
                            comboBox.SelectedItem = bit.Value;
                        }
                    }
                }

                // Load PreconBits
                if (config.Sections.TryGetValue("PreconBits", out var preconBits))
                {
                    if (numericUpDown_PREFEN != null)
                    {
                        if (int.TryParse(preconBits.TryGetValue("PREFEN", out var prefen) ? prefen : "0", out int prefenValue))
                            numericUpDown_PREFEN.Value = prefenValue;
                    }
                    if (numericUpDown_PFMWS != null)
                    {
                        if (int.TryParse(preconBits.TryGetValue("PFMWS", out var pfmws) ? pfmws : "0", out int pfmwsValue))
                            numericUpDown_PFMWS.Value = pfmwsValue;
                    }
                    if (numericUpDown_ECCCON != null)
                    {
                        if (int.TryParse(preconBits.TryGetValue("ECCCON", out var ecccon) ? ecccon : "0", out int eccconValue))
                            numericUpDown_ECCCON.Value = eccconValue;
                    }
                }

                // Load peripheral settings - NOW RUNS FOR ALL CONFIGS
                if (config.Sections.TryGetValue("PeripheralConfig", out var peripheralSettings))
                {
                    foreach (var kvp in peripheralCheckBoxes)
                    {
                        if (kvp.Value != null && peripheralSettings.TryGetValue(kvp.Key, out var setting))
                        {
                            bool.TryParse(setting, out bool isEnabled);
                            kvp.Value.Checked = isEnabled;
                    
                            // Debug output to verify loading
                            System.Diagnostics.Debug.WriteLine($"Loading peripheral {kvp.Key}: {setting} -> {isEnabled}");
                        }
                    }
                }

                // Load GPIO settings
                if (config.Sections.TryGetValue("GpioConfig", out var gpioSettings))
                {
                    foreach (var pinConfig in gpioPinConfigs)
                    {
                        // Find corresponding config in section
                        if (gpioSettings.TryGetValue($"PIN_{pinConfig.PinNumber}_FUNCTION_TYPE", out var functionType))
                        {
                            // Update function type combo box
                            if (gpioPinFunctionCombos.TryGetValue(pinConfig.PinNumber, out var functionCombo))
                            {
                                functionCombo.SelectedItem = functionType;
                            }
                        }
                        
                        if (gpioSettings.TryGetValue($"PIN_{pinConfig.PinNumber}_FUNCTION_NAME", out var functionName))
                        {
                            // Update function name text box
                            if (gpioPinNameTextBoxes.TryGetValue(pinConfig.PinNumber, out var nameTextBox))
                            {
                                nameTextBox.Text = functionName;
                            }
                        }
                    }
                }
            }
        }

        private DeviceConfig GetConfigFromForm()
        {
            var config = new DeviceConfig();
            
            // Get variant from variant combo box
            if (comboBoxVariant != null && comboBoxVariant.SelectedItem != null)
            {
                config.Variant = comboBoxVariant.SelectedItem.ToString();
            }
            else
            {
                config.Variant = "MZ"; // Default value
            }
            
            config.Sections = new Dictionary<string, Dictionary<string, string>>();

            // Set device properties based on variant and selected device
            if (config.Variant == "MZ")
            {
                config.DeviceArch = "MIPS";
                config.DeviceFamily = "PIC32MZEF";
                config.DeviceSeries = "PIC32MZ";
                config.CpuClockFrequency = 200000000U;
                
                // Get device name from combo box
                if (comboBox_DEVICE != null && comboBox_DEVICE.SelectedItem != null)
                {
                    config.DeviceName = "PIC" + comboBox_DEVICE.SelectedItem.ToString();
                }
                else
                {
                    config.DeviceName = "PIC32MZ2048EFH064"; // Default
                }
            }
            else
            {
                config.DeviceArch = "MIPS";
                config.DeviceFamily = "PIC32MX";
                config.DeviceSeries = "PIC32MX";
                config.CpuClockFrequency = 80000000U;
                
                // Get device name from combo box
                if (comboBox_DEVICE != null && comboBox_DEVICE.SelectedItem != null)
                {
                    config.DeviceName = "PIC" + comboBox_DEVICE.SelectedItem.ToString();
                }
                else
                {
                    config.DeviceName = "PIC32MX795F512L"; // Default
                }
            }

            // Populate config bits from form controls using the section mapping
            foreach (var kvp in configBitComboBoxes)
            {
                string key = kvp.Key;
                ComboBox combo = kvp.Value;
                if (combo == null) continue; // Skip null controls
                
                string section = configBitSections.ContainsKey(key) ? configBitSections[key] : "DEVCFG0";
                string value = combo.SelectedItem?.ToString() ?? "";

                if (!config.Sections.ContainsKey(section))
                    config.Sections[section] = new Dictionary<string, string>();
                
                config.Sections[section][key] = value;
            }

            // Add USERID (NumericUpDown)
            if (numericUpDown_USERID != null)
            {
                if (!config.Sections.ContainsKey("DEVCFG3"))
                    config.Sections["DEVCFG3"] = new Dictionary<string, string>();
                config.Sections["DEVCFG3"]["USERID"] = $"0x{((int)numericUpDown_USERID.Value):X}";
            }

            // Add PreconBits (numeric up/down controls)
            if (!config.Sections.ContainsKey("PreconBits"))
                config.Sections["PreconBits"] = new Dictionary<string, string>();
            
            if (numericUpDown_PREFEN != null)
                config.Sections["PreconBits"]["PREFEN"] = numericUpDown_PREFEN.Value.ToString();
            if (numericUpDown_PFMWS != null)
                config.Sections["PreconBits"]["PFMWS"] = numericUpDown_PFMWS.Value.ToString();
            if (numericUpDown_ECCCON != null)
                config.Sections["PreconBits"]["ECCCON"] = numericUpDown_ECCCON.Value.ToString();

            // Add peripheral enable settings
            if (!config.Sections.ContainsKey("PeripheralConfig"))
                config.Sections["PeripheralConfig"] = new Dictionary<string, string>();
            
            foreach (var kvp in peripheralCheckBoxes)
            {
                if (kvp.Value != null)
                {
                    config.Sections["PeripheralConfig"][kvp.Key] = kvp.Value.Checked.ToString().ToLower();
                }
            }
            
            // Add GPIO configuration
            if (!config.Sections.ContainsKey("GpioConfig"))
                config.Sections["GpioConfig"] = new Dictionary<string, string>();
            
            var gpioSection = config.Sections["GpioConfig"];
            
            // Clear existing GPIO config
            var keysToRemove = gpioSection.Keys.Where(k => k.StartsWith("PIN_") || k.StartsWith("GPIO_PIN_")).ToList();
            foreach (var key in keysToRemove)
            {
                gpioSection.Remove(key);
            }
            
            // Count pins that are not "None"
            int activePinCount = 0;
            
            // Add current configuration (only for pins that are not "None")
            foreach (var pin in gpioPinConfigs.Where(p => p.FunctionType != "None"))
            {
                string pinPrefix = $"PIN_{pin.PinNumber}_";
                gpioSection[$"{pinPrefix}FUNCTION_TYPE"] = pin.FunctionType;
                gpioSection[$"{pinPrefix}FUNCTION_NAME"] = pin.FunctionName;
                gpioSection[$"{pinPrefix}GPIO_CTRL_REG_NUM"] = pin.CtrlRegNum.ToString();
                gpioSection[$"{pinPrefix}GPIO_CTRL_REG_INDEX"] = pin.CtrlRegIndex.ToString();
                gpioSection[$"GPIO_PIN_NAME_{pin.PinNumber}"] = pin.PinName;
                activePinCount++;
            }
            
            // Only set max index if there are active pins
            if (activePinCount > 0)
            {
                gpioSection["GPIO_PIN_MAX_INDEX"] = TOTAL_GPIO_PINS.ToString();
                
                // Add some default enums for the template
                gpioSection["GPIO_MUX_FUNC_ENUM_LIST"] = "GPIO_FUNCTION_GPIO = 0, GPIO_FUNCTION_ALT1 = 1, GPIO_FUNCTION_ALT2 = 2";
                gpioSection["GPIO_PU_PD_ENUM_LIST"] = "GPIO_PULL_NONE = 0, GPIO_PULL_UP = 1, GPIO_PULL_DOWN = 2";
            }
            else
            {
                // If no active pins, remove the section entirely
                config.Sections.Remove("GpioConfig");
            }
            
            return config;
        }


        public void saveConfig_ToJson(string path_)
        {
            // Always create a fresh config from the current form state
            var config = GetConfigFromForm();
            config.Save(path_); // Save to file
            MessageBox.Show("Configuration saved!");
        }

        private void UpdateConfigFromFormAndCheckKeys(DeviceConfig config)
        {
            // Initialize Sections if null
            if (config.Sections == null)
                config.Sections = new Dictionary<string, Dictionary<string, string>> ();

            // Get current variant from variant combo box
            if (comboBoxVariant != null && comboBoxVariant.SelectedItem != null)
            {
                config.Variant = comboBoxVariant.SelectedItem.ToString();
            }
            else
            {
                config.Variant = "MZ"; // Default
            }

            // Update device properties based on current variant and selected device
            if (config.Variant == "MZ")
            {
                config.DeviceArch = "MIPS";
                config.DeviceFamily = "PIC32MZEF";
                config.DeviceSeries = "PIC32MZ";
                config.CpuClockFrequency = 200000000U;
                
                // Get device name from combo box
                if (comboBox_DEVICE != null && comboBox_DEVICE.SelectedItem != null)
                {
                    config.DeviceName = "PIC" + comboBox_DEVICE.SelectedItem.ToString();
                }
                else
                {
                    config.DeviceName = "PIC32MZ2048EFH064"; // Default
                }
            }
            else if (config.Variant == "MX")
            {
                config.DeviceArch = "MIPS";
                config.DeviceFamily = "PIC32MX";
                config.DeviceSeries = "PIC32MX";
                config.CpuClockFrequency = 80000000U;
                
                // Get device name from combo box
                if (comboBox_DEVICE != null && comboBox_DEVICE.SelectedItem != null)
                {
                    config.DeviceName = "PIC" + comboBox_DEVICE.SelectedItem.ToString();
                }
                else
                {
                    config.DeviceName = "PIC32MX795F512L"; // Default
                }
            }

            // For section-based config
            foreach (var kvp in configBitComboBoxes)
            {
                string key = kvp.Key;
                ComboBox combo = kvp.Value;
                if (combo == null) continue; // Skip null controls
                
                string section = configBitSections.ContainsKey(key) ? configBitSections[key] : "DEVCFG0"; // fallback
                string newValue = combo.SelectedItem?.ToString() ?? "";
                
                if (!config.Sections.ContainsKey(section))
                    config.Sections[section] = new Dictionary<string, string>();
                config.Sections[section][key] = newValue;
            }

            // NumericUpDown USERID
            if (numericUpDown_USERID != null)
            {
                if (!config.Sections.ContainsKey("DEVCFG3"))
                    config.Sections["DEVCFG3"] = new Dictionary<string, string>();
                config.Sections["DEVCFG3"]["USERID"] = $"0x{((int)numericUpDown_USERID.Value):X}";
            }

            // Add PreconBits (numeric up/down controls)
            if (!config.Sections.ContainsKey("PreconBits"))
                config.Sections["PreconBits"] = new Dictionary<string, string>();
            
            if (numericUpDown_PREFEN != null)
                config.Sections["PreconBits"]["PREFEN"] = numericUpDown_PREFEN.Value.ToString();
            if (numericUpDown_PFMWS != null)
                config.Sections["PreconBits"]["PFMWS"] = numericUpDown_PFMWS.Value.ToString();
            if (numericUpDown_ECCCON != null)
                config.Sections["PreconBits"]["ECCCON"] = numericUpDown_ECCCON.Value.ToString();
        }


        #endregion LOAD/GET CONFIG


        #region BUTTON / FORM EVENTS


        private void ComboBoxVariant_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBoxVariant != null && comboBoxVariant.SelectedItem != null)
            {
                string selectedVariant = comboBoxVariant.SelectedItem.ToString();
                UpdateDeviceComboBox(selectedVariant);
            }
        }


        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (String.IsNullOrEmpty(path))
            {
                MessageBox.Show("No file path specified. Use 'Save As' to specify a file.");
                return;
            }
            saveConfig_ToJson(path);
        }

        #endregion BUTTON EVENTS

        #region MENU EVENTS

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog
            {
                Filter = "JSON Files (*.json)|*.json|All Files (*.*)|*.*",
                Title = "Open Device Configuration"
            };
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                path = ofd.FileName;
                var config = DeviceConfig.Load(path);
                if (config != null)
                {
                    LoadConfigToForm(path);
                }
            }
        }



        private void saveAsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog
            {
                Filter = "JSON Files (*.json)|*.json|All Files (*.*)|*.*",
                Title = "Save Device Configuration As"
            };
            if (sfd.ShowDialog() == DialogResult.OK)
            {
                path = sfd.FileName; // Update the path to the new location
                saveConfig_ToJson(path);
            }
        }


        private void generateToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                System.Diagnostics.Debug.WriteLine("Starting generation process...");
                
                // Always save current form state to ensure we have the latest config
                var config = GetConfigFromForm();
                System.Diagnostics.Debug.WriteLine($"Got config from form: Variant={config.Variant}, Device={config.DeviceName}");
                
                config.Save(path);
                System.Diagnostics.Debug.WriteLine($"Saved config to: {path}");
                
                // Generate the C file using T4 template
                GenerateConfigBitsFile();
                System.Diagnostics.Debug.WriteLine("Generation process completed");
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Exception in generation: {ex}");
                MessageBox.Show($"Error generating config bits file: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        #endregion MENU EVENTS

        #region HELPER METHODS
        private void GenerateConfigBitsFile()
        {
            try
            {
                // First try to find templates relative to the application startup path
                string templatesDir = Path.Combine(Application.StartupPath, "Templates");
                string templatePathC = Path.Combine(templatesDir, "config_bits.c.tt");
                string templatePathH = Path.Combine(templatesDir, "config_bits.h.tt");
                
                // If not found in startup path, try to find project directory
                if (!File.Exists(templatePathC) || !File.Exists(templatePathH))
                {
                    // Navigate up from startup path to find the workspace root
                    string projectDir = Application.StartupPath;
                    
                    // Navigate up to find the project directory (where Setup.csproj is located)
                    while (projectDir != null && !File.Exists(Path.Combine(projectDir, "Setup.csproj")))
                    {
                        var parentDir = Directory.GetParent(projectDir);
                        if (parentDir == null) break;
                        projectDir = parentDir.FullName;
                    }

                    if (projectDir != null && File.Exists(Path.Combine(projectDir, "Setup.csproj")))
                    {
                        templatesDir = Path.Combine(projectDir, "Templates");
                        templatePathC = Path.Combine(templatesDir, "config_bits.c.tt");
                        templatePathH = Path.Combine(templatesDir, "config_bits.h.tt");
                    }
                }

                // Final fallback: try current directory
                if (!File.Exists(templatePathC) || !File.Exists(templatePathH))
                {
                    templatesDir = Path.Combine(Directory.GetCurrentDirectory(), "Setup", "Templates");
                    templatePathC = Path.Combine(templatesDir, "config_bits.c.tt");
                    templatePathH = Path.Combine(templatesDir, "config_bits.h.tt");
                }

                string configPath = path; // Use the same path as the form

                // Check if templates exist
                if (!File.Exists(templatePathC))
                {
                    MessageBox.Show($"C Template file not found at:\n{templatePathC}\n\nSearched in:\n- {Path.Combine(Application.StartupPath, "Templates")}\n- {templatesDir}\n\nPlease ensure the template file exists.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                if (!File.Exists(templatePathH))
                {
                    MessageBox.Show($"Header Template file not found at:\n{templatePathH}\n\nSearched in:\n- {Path.Combine(Application.StartupPath, "Templates")}\n- {templatesDir}\n\nPlease ensure the template file exists.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Check if config exists
                if (!File.Exists(configPath))
                {
                    MessageBox.Show($"Configuration file not found: {configPath}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Use the directory where the JSON file was saved (from the path variable)
                string targetProjectDir = Path.GetDirectoryName(configPath);
                
                if (string.IsNullOrEmpty(targetProjectDir) || !Directory.Exists(targetProjectDir))
                {
                    MessageBox.Show($"Invalid project directory from saved JSON path: {targetProjectDir}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Create srcs/default directory structure in the same directory as the JSON file
                string srcsDir = Path.Combine(targetProjectDir, "srcs");
                string defaultDir = Path.Combine(srcsDir, "default");
                
                try
                {
                    if (!Directory.Exists(srcsDir))
                        Directory.CreateDirectory(srcsDir);
                    if (!Directory.Exists(defaultDir))
                        Directory.CreateDirectory(defaultDir);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error creating directory structure: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Final output paths: place both .c and .h files in srcs/default folder
                string finalOutputPathC = Path.Combine(defaultDir, "config_bits.c");
                string finalOutputPathH = Path.Combine(defaultDir, "definitions.h");

                bool successC = false, successH = false;
                string errorMessages = "";

                // Generate C file using T4 template
                try
                {
                    successC = GenerateTemplateFile(templatePathC, configPath, finalOutputPathC, "C source");
                }
                catch (Exception ex)
                {
                    errorMessages += $"C file generation error: {ex.Message}\n";
                }

                // Generate H file using T4 template
                try
                {
                    successH = GenerateTemplateFile(templatePathH, configPath, finalOutputPathH, "header");
                }
                catch (Exception ex)
                {
                    errorMessages += $"Header file generation error: {ex.Message}\n";
                }

                // Show results
                if (successC && successH)
                {
                    MessageBox.Show($"Configuration files generated successfully!\n\nC File: {finalOutputPathC}\nHeader File: {finalOutputPathH}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    
                    // Optionally open the generated files
                    if (MessageBox.Show("Would you like to open the generated files?", "Open Files", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes)
                    {
                        try
                        {
                            Process.Start(new ProcessStartInfo(finalOutputPathC) { UseShellExecute = true });
                            Process.Start(new ProcessStartInfo(finalOutputPathH) { UseShellExecute = true });
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Error opening files: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        }
                    }
                }
                else
                {
                    string message = "Some files failed to generate:\n";
                    if (!successC) message += "- C source file failed\n";
                    if (!successH) message += "- Header file failed\n";
                    if (!string.IsNullOrEmpty(errorMessages)) message += $"\nErrors:\n{errorMessages}";
                    
                    MessageBox.Show(message, "Generation Issues", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error running T4 templates: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private bool GenerateTemplateFile(string templatePath, string configPath, string outputPath, string fileType)
        {
            try
            {
                // Prepare the T4 command with properly quoted paths
                string t4Command = "t4";
                string arguments = $"-p ConfigPath=\"{configPath.Replace("\\", "\\\\")}\" \"{templatePath}\" -o \"{outputPath}\"";

                // Debug output
                System.Diagnostics.Debug.WriteLine($"Executing: {t4Command} {arguments}");
                System.Diagnostics.Debug.WriteLine($"ConfigPath being passed: {configPath}");
                System.Diagnostics.Debug.WriteLine($"File exists: {File.Exists(configPath)}");

                // Verify the config file exists before calling T4
                if (!File.Exists(configPath))
                {
                    MessageBox.Show($"Configuration file not found: {configPath}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }

                var processInfo = new ProcessStartInfo
                {
                    FileName = t4Command,
                    Arguments = arguments,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true,
                    WorkingDirectory = Path.GetDirectoryName(templatePath)
                };

                // Start the process with timeout
                using (var process = Process.Start(processInfo))
                {
                    if (process == null)
                    {
                        MessageBox.Show($"Failed to start T4 process for {fileType}. Make sure 't4' tool is installed and in your PATH.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }

                    // Set a timeout of 30 seconds
                    bool finished = process.WaitForExit(30000);
                    
                    if (!finished)
                    {
                        // Process is taking too long, kill it
                        try
                        {
                            process.Kill();
                            MessageBox.Show($"T4 process for {fileType} timed out after 30 seconds and was terminated.", "Timeout Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Failed to kill T4 process: {ex.Message}", "Process Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                        return false;
                    }

                    // Read output and errors
                    string output = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();

                    System.Diagnostics.Debug.WriteLine($"T4 Exit Code: {process.ExitCode}");
                    System.Diagnostics.Debug.WriteLine($"T4 Output: {output}");
                    System.Diagnostics.Debug.WriteLine($"T4 Error: {error}");

                    if (process.ExitCode == 0)
                    {
                        return true;
                    }
                    else
                    {
                        string errorMessage = $"T4 process failed for {fileType} with exit code {process.ExitCode}";
                        if (!string.IsNullOrEmpty(error))
                            errorMessage += $"\n\nError: {error}";
                        if (!string.IsNullOrEmpty(output))
                            errorMessage += $"\n\nOutput: {output}";
                            
                        MessageBox.Show(errorMessage, "T4 Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Exception in T4 generation for {fileType}: {ex.Message}", "Exception Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }
        }

        private void UpdateDeviceComboBox(string variant)
        {
            if (comboBox_DEVICE == null)
                return;

            comboBox_DEVICE.Items.Clear();

            if (variant == "MZ")
            {
                // Add MZ devices
                comboBox_DEVICE.Items.AddRange(new string[]
                {
                    "32MZ1024EFH064",
                    "32MZ1024EFH100",
                    "32MZ1024EFH124",
                    "32MZ1024EFH144",
                    "32MZ2048EFH064",
                    "32MZ2048EFH100",
                    "32MZ2048EFH124",
                    "32MZ2048EFH144"
                });
                
                // Set default selection for MZ
                if (comboBox_DEVICE.Items.Count > 0)
                {
                    comboBox_DEVICE.SelectedIndex = 4; // Default to 32MZ2048EFH064
                }
            }
            else if (variant == "MX")
            {
                // Add MX devices
                comboBox_DEVICE.Items.AddRange(new string[]
                {
                    "32MX795F512L",
                    "32MX795F512H",
                    "32MX675F512L",
                    "32MX675F512H",
                    "32MX575F512L",
                    "32MX575F512H"
                });
                
                // Set default selection for MX
                if (comboBox_DEVICE.Items.Count > 0)
                {
                    comboBox_DEVICE.SelectedIndex = 0; // Default to 32MX795F512L
                }
            }
        }

        private void InitializeGpioControls()
        {
            gpioPinConfigs = new List<GpioPinConfig>();
            gpioPinFunctionCombos = new Dictionary<int, ComboBox>();
            gpioPinNameTextBoxes = new Dictionary<int, TextBox>();
            
            CreateGpioPinControls();
        }

        private void CreateGpioPinControls()
        {
            int pinsPerSide = TOTAL_GPIO_PINS / 4; // 8 pins per side for 32 total pins
            
            for (int i = 1; i <= TOTAL_GPIO_PINS; i++)
            {
                // Create pin configuration
                var pinConfig = new GpioPinConfig
                {
                    PinNumber = i,
                    PinName = $"PIN_{i:D2}",
                    CtrlRegNum = (i - 1) / 32,
                    CtrlRegIndex = (i - 1) % 32
                };
                gpioPinConfigs.Add(pinConfig);
                
                // Calculate position around the square
                Point position = CalculatePinControlPosition(i, pinsPerSide);
                
                // Create function type combo box
                var functionCombo = new ComboBox
                {
                    Name = $"cmbPin{i}Function",
                    Location = position,
                    Size = new Size(100, 23),
                    DropDownStyle = ComboBoxStyle.DropDownList,
                    Tag = i // Store pin number
                };
                functionCombo.Items.AddRange(GpioPinConfig.FunctionTypes);
                functionCombo.SelectedItem = "None"; // Default to None
                functionCombo.SelectedIndexChanged += GpioFunctionCombo_SelectedIndexChanged;
                
                // Create function name text box
                var nameTextBox = new TextBox
                {
                    Name = $"txtPin{i}Name",
                    Location = new Point(position.X, position.Y + 25),
                    Size = new Size(100, 23),
                    Text = $"PIN_{i:D2}",
                    Tag = i // Store pin number
                };
                nameTextBox.TextChanged += GpioNameTextBox_TextChanged;
                
                // Create pin number label
                var pinLabel = new Label
                {
                    Name = $"lblPin{i}",
                    Location = new Point(position.X + 25, position.Y - 20),
                    Size = new Size(50, 15),
                    Text = $"Pin {i}",
                    Font = new Font("Segoe UI", 8F, FontStyle.Bold),
                    TextAlign = ContentAlignment.MiddleCenter
                };
                
                // Store references
                gpioPinFunctionCombos[i] = functionCombo;
                gpioPinNameTextBoxes[i] = nameTextBox;
                
                // Add controls to the container
                panelGpioContainer.Controls.Add(functionCombo);
                panelGpioContainer.Controls.Add(nameTextBox);
                panelGpioContainer.Controls.Add(pinLabel);
            }
        }

        private Point CalculatePinControlPosition(int pinNumber, int pinsPerSide)
        {
            // Get center square position and size
            int centerX = panelCenterSquare.Location.X + panelCenterSquare.Width / 2;
            int centerY = panelCenterSquare.Location.Y + panelCenterSquare.Height / 2;
            int squareHalfWidth = panelCenterSquare.Width / 2;
            int squareHalfHeight = panelCenterSquare.Height / 2;
            
            // Determine which side of the square (0=top, 1=right, 2=bottom, 3=left)
            int side = (pinNumber - 1) / pinsPerSide;
            int positionOnSide = (pinNumber - 1) % pinsPerSide;
            
            // Calculate spacing between pins
            int spacing = 120; // Space between pin controls
            int offset = (pinsPerSide - 1) * spacing / 2; // Center the pins on each side
            
            switch (side)
            {
                case 0: // Top side
                    return new Point(
                        centerX - offset + (positionOnSide * spacing) - 50,
                        centerY - squareHalfHeight - 80
                    );
                    
                case 1: // Right side
                    return new Point(
                        centerX + squareHalfWidth + 30,
                        centerY - offset + (positionOnSide * spacing) - 25
                    );
                    
                case 2: // Bottom side
                    return new Point(
                        centerX + offset - (positionOnSide * spacing) - 50,
                        centerY + squareHalfHeight + 30
                    );
                    
                case 3: // Left side
                    return new Point(
                        centerX - squareHalfWidth - 130,
                        centerY + offset - (positionOnSide * spacing) - 25
                    );
                    
                default:
                    return new Point(0, 0);
            }
        }

        // Event handlers for GPIO controls
        private void GpioFunctionCombo_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (sender is ComboBox combo && combo.Tag is int pinNumber)
            {
                var pinConfig = gpioPinConfigs.Find(p => p.PinNumber == pinNumber);
                if (pinConfig != null)
                {
                    pinConfig.FunctionType = combo.SelectedItem?.ToString() ?? "None";
                    
                    // Auto-generate function name based on type (only if not "None")
                    if (pinConfig.FunctionType != "None" && 
                        (string.IsNullOrEmpty(pinConfig.FunctionName) || pinConfig.FunctionName.StartsWith("PIN_")))
                    {
                        pinConfig.FunctionName = GenerateFunctionName(pinConfig.FunctionType, pinNumber);
                        if (gpioPinNameTextBoxes.TryGetValue(pinNumber, out var textBox))
                        {
                            textBox.Text = pinConfig.FunctionName;
                        }
                    }
                    
                    UpdateGpioConfigInDeviceConfig();
                }
            }
        }

        private void GpioNameTextBox_TextChanged(object sender, EventArgs e)
        {
            if (sender is TextBox textBox && textBox.Tag is int pinNumber)
            {
                var pinConfig = gpioPinConfigs.Find(p => p.PinNumber == pinNumber);
                if (pinConfig != null)
                {
                    pinConfig.FunctionName = textBox.Text;
                    UpdateGpioConfigInDeviceConfig();
                }
            }
        }

        private string GenerateFunctionName(string functionType, int pinNumber)
        {
            switch (functionType)
            {
                case "UART_TX": return $"UART_TX_{pinNumber}";
                case "UART_RX": return $"UART_RX_{pinNumber}";
                case "SPI_CLK": return $"SPI_CLK_{pinNumber}";
                case "SPI_MOSI": return $"SPI_MOSI_{pinNumber}";
                case "SPI_MISO": return $"SPI_MISO_{pinNumber}";
                case "SPI_CS": return $"SPI_CS_{pinNumber}";
                case "I2C_SCL": return $"I2C_SCL_{pinNumber}";
                case "I2C_SDA": return $"I2C_SDA_{pinNumber}";
                case "PWM": return $"PWM_{pinNumber}";
                case "ADC": return $"ADC_CH_{pinNumber}";
                case "TIMER": return $"TIMER_{pinNumber}";
                case "LED": return $"LED_{pinNumber}";
                case "SWITCH": return $"SW_{pinNumber}";
                case "GPIO": return $"GPIO_{pinNumber}";
                default: return $"PIN_{pinNumber:D2}";
            }
        }

        private void CheckBox_GenerateGpio_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox_GenerateGpio.Checked)
            {
                try
                {
                    // Update configuration first
                    UpdateGpioConfigInDeviceConfig();
                    
                    // Save current config
                    var config = GetConfigFromForm();
                    config.Save(path);
                    
                    // Generate GPIO files
                    GenerateGpioFiles();
                    
                    MessageBox.Show("GPIO files generated successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error generating GPIO files: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                finally
                {
                    // Uncheck the checkbox
                    checkBox_GenerateGpio.Checked = false;
                }
            }
        }

        private void GenerateGpioFiles()
        {
            // Find templates directory
            string templatesDir = Path.Combine(Application.StartupPath, "Templates", "gpio");
            string templatePathC = Path.Combine(templatesDir, "plib_gpio.c.tt");
            string templatePathH = Path.Combine(templatesDir, "plib_gpio.h.tt");
            
            // If not found in startup path, try project directory
            if (!File.Exists(templatePathC) || !File.Exists(templatePathH))
            {
                string projectDir = Application.StartupPath;
                while (projectDir != null && !File.Exists(Path.Combine(projectDir, "Setup.csproj")))
                {
                    var parentDir = Directory.GetParent(projectDir);
                    if (parentDir == null) break;
                    projectDir = parentDir.FullName;
                }

                if (projectDir != null)
                {
                    templatesDir = Path.Combine(projectDir, "Templates", "gpio");
                    templatePathC = Path.Combine(templatesDir, "plib_gpio.c.tt");
                    templatePathH = Path.Combine(templatesDir, "plib_gpio.h.tt");
                }
            }

            string configPath = path;

            // Check if templates exist
            if (!File.Exists(templatePathC))
            {
                throw new FileNotFoundException($"GPIO C template not found: {templatePathC}");
            }
            if (!File.Exists(templatePathH))
            {
                throw new FileNotFoundException($"GPIO header template not found: {templatePathH}");
            }
            if (!File.Exists(configPath))
            {
                throw new FileNotFoundException($"Configuration file not found: {configPath}");
            }

            // Create target directory: same as config file but add /srcs/default/gpio
            string targetProjectDir = Path.GetDirectoryName(configPath);
            string srcsDir = Path.Combine(targetProjectDir, "srcs");
            string defaultDir = Path.Combine(srcsDir, "default");
            string gpioDir = Path.Combine(defaultDir, "gpio");
            
            // Create directory structure
            if (!Directory.Exists(srcsDir))
                Directory.CreateDirectory(srcsDir);
            if (!Directory.Exists(defaultDir))
                Directory.CreateDirectory(defaultDir);
            if (!Directory.Exists(gpioDir))
                Directory.CreateDirectory(gpioDir);

            // Generate files
            string finalOutputPathC = Path.Combine(gpioDir, "plib_gpio.c");
            string finalOutputPathH = Path.Combine(gpioDir, "plib_gpio.h");

            bool successC = GenerateTemplateFile(templatePathC, configPath, finalOutputPathC, "GPIO C source");
            bool successH = GenerateTemplateFile(templatePathH, configPath, finalOutputPathH, "GPIO header");

            if (!successC || !successH)
            {
                throw new Exception("Failed to generate one or more GPIO files");
            }
        }

        private void UpdateGpioConfigInDeviceConfig()
        {
            var config = GetConfigFromForm();
            
            // Add GPIO configuration section
            if (!config.Sections.ContainsKey("GpioConfig"))
                config.Sections["GpioConfig"] = new Dictionary<string, string>();
            
            var gpioSection = config.Sections["GpioConfig"];
            
            // Clear existing GPIO config
            var keysToRemove = gpioSection.Keys.Where(k => k.StartsWith("PIN_") || k.StartsWith("GPIO_PIN_")).ToList();
            foreach (var key in keysToRemove)
            {
                gpioSection.Remove(key);
            }
            
            // Count pins that are not "None"
            int activePinCount = 0;
            
            // Add current configuration (only for pins that are not "None")
            foreach (var pin in gpioPinConfigs.Where(p => p.FunctionType != "None"))
            {
                string pinPrefix = $"PIN_{pin.PinNumber}_";
                gpioSection[$"{pinPrefix}FUNCTION_TYPE"] = pin.FunctionType;
                gpioSection[$"{pinPrefix}FUNCTION_NAME"] = pin.FunctionName;
                gpioSection[$"{pinPrefix}GPIO_CTRL_REG_NUM"] = pin.CtrlRegNum.ToString();
                gpioSection[$"{pinPrefix}GPIO_CTRL_REG_INDEX"] = pin.CtrlRegIndex.ToString();
                gpioSection[$"GPIO_PIN_NAME_{pin.PinNumber}"] = pin.PinName;
                activePinCount++;
            }
            
            // Only set max index if there are active pins
            if (activePinCount > 0)
            {
                gpioSection["GPIO_PIN_MAX_INDEX"] = TOTAL_GPIO_PINS.ToString();
                
                // Add some default enums for the template
                gpioSection["GPIO_MUX_FUNC_ENUM_LIST"] = "GPIO_FUNCTION_GPIO = 0, GPIO_FUNCTION_ALT1 = 1, GPIO_FUNCTION_ALT2 = 2";
                gpioSection["GPIO_PU_PD_ENUM_LIST"] = "GPIO_PULL_NONE = 0, GPIO_PULL_UP = 1, GPIO_PULL_DOWN = 2";
            }
            else
            {
                // If no active pins, remove the section entirely
                config.Sections.Remove("GpioConfig");
            }
        }
        #endregion  
    }
}