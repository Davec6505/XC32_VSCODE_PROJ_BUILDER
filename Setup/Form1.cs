using csharp;
using Microsoft.VisualBasic.ApplicationServices;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;



namespace Setup
{



    public partial class Form1 : Form
    {
        // Move the initialization of configBitComboBoxes from field initializer to the constructor

        private Dictionary<string, ComboBox> configBitComboBoxes;

        public Form1()
        {
            InitializeComponent();
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
               // { "TSEQ", comboBox_TSEQ },
               // { "CSEQ", comboBox_CSEQ }
            };
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Hide the taskbar icon and set the form as a tool window
            this.ShowInTaskbar = false;
            this.FormBorderStyle = FormBorderStyle.FixedToolWindow;
            // Do not load configWords or call CreateConfigUI on startup
            LoadConfigToForm();
        }



        #region LOAD/GET CONFIG

        private void LoadConfigToForm()
        {
            var config = DeviceConfig.Load("device_config.json");
            if (config == null || config.ConfigBits == null) return;

            foreach (var bit in config.ConfigBits)
            {
                if (bit.Key == "USERID" && numericUpDown_USERID != null)
                {
                    // Parse the value as needed (e.g., hex or decimal)
                    if (int.TryParse(bit.Value.Replace("0x", ""), System.Globalization.NumberStyles.HexNumber, null, out int userIdValue))
                    {
                        userIdValue = Math.Max((int)numericUpDown_USERID.Minimum, Math.Min(userIdValue, (int)numericUpDown_USERID.Maximum));
                        numericUpDown_USERID.Value = userIdValue;
                    }
                    else
                    {
                        numericUpDown_USERID.Value = 0; // Default/fallback
                    }
                }
                else if (bit.Key == "TSEQ" && numericUpDown_TSEQ != null)
                {
                    if (int.TryParse(bit.Value, out int tseqValue))
                    {
                        tseqValue = Math.Max((int)numericUpDown_TSEQ.Minimum, Math.Min(tseqValue, (int)numericUpDown_TSEQ.Maximum));
                        numericUpDown_TSEQ.Value = tseqValue;
                    }
                    else
                    {
                        numericUpDown_TSEQ.Value = 0; // Default/fallback
                    }
                }
                else if (bit.Key == "CSEQ" && numericUpDown_CSEQ != null)
                {
                    if (int.TryParse(bit.Value, out int cseqValue))
                    {
                        cseqValue = Math.Max((int)numericUpDown_CSEQ.Minimum, Math.Min(cseqValue, (int)numericUpDown_CSEQ.Maximum));
                        numericUpDown_CSEQ.Value = cseqValue;
                    }
                    else
                    {
                        numericUpDown_CSEQ.Value = 0; // Default/fallback
                    }
                }
                else if (configBitComboBoxes.TryGetValue(bit.Key, out var comboBox) && comboBox != null)
                {
                    comboBox.SelectedItem = bit.Value;
                }
            }
        }

        private DeviceConfig GetConfigFromForm()
        {
            var config = new DeviceConfig();
            config.Variant = comboBoxVariant.SelectedItem?.ToString() ?? "MZ"; // Example for variant selection

            // Example for config bits
            config.ConfigBits = new Dictionary<string, string>
            {
                { "DEBUG", comboBox_DEBUG.SelectedItem?.ToString() ?? "OFF" },
                { "JTAGEN", comboBox_JTAGEN.SelectedItem?.ToString() ?? "OFF" },
                // ... add all other config bits, mapping to their respective controls
                { "USERID", numericUpDown_USERID.Text }
            };

            // For USERID (NumericUpDown)
            config.ConfigBits["USERID"] = $"0x{((int)numericUpDown_USERID.Value):X}";

            // Example for PRECONbits
            config.PreconBits = new Dictionary<string, string>
            {
                { "PREFEN", textBoxPREFEN.Text },
                { "PFMWS", textBoxPFMWS.Text },
                { "ECCCON", textBoxECCCON.Text }
            };

            return config;
        }
        #endregion LOAD/GET CONFIG
   

        #region BUTTON EVENTS

        private void buttonSaveConfig_Click(object sender, EventArgs e)
        {
            saveConfig_ToJson();
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveConfig_ToJson();
            MessageBox.Show("Configuration saved!");
        }

        #endregion BUTTON EVENTS

        #region MENU EVENTS

        private void buttonSaveConfig_Click_1(object sender, EventArgs e)
        {
            saveConfig_ToJson();
            MessageBox.Show("Configuration saved!");
        }


        #endregion MENU EVENTS


        #region HELPER METHODS

        public void saveConfig_ToJson()
        {
            var config = DeviceConfig.Load("device_config.json"); // Load existing config
            if (config == null) config = new DeviceConfig();      // Fallback if file missing
            UpdateConfigFromFormAndCheckKeys(config);              // Update only changed values
            config.Save("device_config.json");                     // Save back to file
            MessageBox.Show("Configuration saved!");
        }

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

        private void UpdateConfigFromFormAndCheckKeys(DeviceConfig config)
        {
            // For section-based config
            foreach (var kvp in configBitComboBoxes)
            {
                string key = kvp.Key;
                ComboBox combo = kvp.Value;
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
            // Add PreconBits (textboxes)
            if (!config.Sections.ContainsKey("PreconBits"))
                config.Sections["PreconBits"] = new Dictionary<string, string>();
            config.Sections["PreconBits"]["PREFEN"] = textBoxPREFEN.Text;
            config.Sections["PreconBits"]["PFMWS"] = textBoxPFMWS.Text;
            config.Sections["PreconBits"]["ECCCON"] = textBoxECCCON.Text;
        }

        #endregion HELPER METHODS


    }
}

































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































