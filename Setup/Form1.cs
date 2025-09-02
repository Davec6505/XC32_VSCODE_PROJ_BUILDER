using csharp;
using Microsoft.VisualBasic.ApplicationServices;
// Ensure you have installed the Newtonsoft.Json NuGet package.
// In Visual Studio, right-click your project > Manage NuGet Packages > Browse > Search for "Newtonsoft.Json" > Install.

// No code changes are needed in this file if the using directive is present and the package is installed:
// using Newtonsoft.Json;

// If you have already installed the package and still see the error, try rebuilding your solution.
// If you have not installed the package, follow the instructions above.
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Windows.Forms;



namespace Setup
{



    public partial class Form1 : Form
    {


        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Hide the taskbar icon and set the form as a tool window
            this.ShowInTaskbar = false;
            this.FormBorderStyle = FormBorderStyle.FixedToolWindow;
            // Do not load configWords or call CreateConfigUI on startup
            LoadConfigToForm();
        }

        private DeviceConfig GetConfigFromForm()
        {
            var config = new DeviceConfig();
            config.Variant = comboBoxVariant.SelectedItem?.ToString() ?? "MZ"; // Example for variant selection

            // Example for config bits
            config.ConfigBits = new Dictionary<string, string>
            {
                { "DEBUG", comboBox_Debug.SelectedItem?.ToString() ?? "OFF" },
                { "JTAGEN", comboBox_JTAGEN.SelectedItem?.ToString() ?? "OFF" },
                // ... add all other config bits, mapping to their respective controls
                { "USERID", numericUpDown_USERID.Text }
            };

            // Example for PRECONbits
            config.PreconBits = new Dictionary<string, string>
            {
                { "PREFEN", textBoxPREFEN.Text },
                { "PFMWS", textBoxPFMWS.Text },
                { "ECCCON", textBoxECCCON.Text }
            };

            return config;
        }

        private void buttonSaveConfig_Click_1(object sender, EventArgs e)
        {
            var config = GetConfigFromForm();
            config.Save("device_config.json");
            MessageBox.Show("Configuration saved!");
        }

        private void LoadConfigToForm()
        {
            var config = DeviceConfig.Load("device_config.json");
            if (config == null) return;

            comboBoxVariant.SelectedItem = config.Variant;
            comboBox_Debug.SelectedItem = config.ConfigBits.GetValueOrDefault("DEBUG", "OFF");
            comboBox_JTAGEN.SelectedItem = config.ConfigBits.GetValueOrDefault("JTAGEN", "OFF");
            // ... repeat for other config bits and PRECONbits
            numericUpDown_USERID.Text = config.ConfigBits.GetValueOrDefault("USERID", "");
            textBoxPREFEN.Text = config.PreconBits.GetValueOrDefault("PREFEN", "");
            textBoxPFMWS.Text = config.PreconBits.GetValueOrDefault("PFMWS", "");
            textBoxECCCON.Text = config.PreconBits.GetValueOrDefault("ECCCON", "");
        }

        private void buttonSaveConfig_Click(object sender, EventArgs e)
        {
            saveConfig_ToJson();
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveConfig_ToJson();
        }

        public void saveConfig_ToJson()
        {
            var config = GetConfigFromForm();
            config.Save("device_config.json");
            MessageBox.Show("Configuration saved!");
        }
    }
}


