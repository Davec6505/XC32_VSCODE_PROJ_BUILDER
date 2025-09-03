using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Windows.Forms;

namespace Setup
{
    public class DeviceConfig
    {
        public string Variant { get; set; } = string.Empty; // "MX" or "MZ"
        public Dictionary<string, string> ConfigBits { get; set; } = new();
        public Dictionary<string, string> PreconBits { get; set; } = new();
        public Dictionary<string, Dictionary<string, string>> Sections { get; set; } = new();

        public static DeviceConfig? Load(string path)
        {
            if (!File.Exists(path))
            {
                MessageBox.Show($"File not found: {path}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return null;
            }
            var json = File.ReadAllText(path);

            DeviceConfig? config = null;
            try
            {
                config = JsonSerializer.Deserialize<DeviceConfig>(json, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
                if (config == null)
                {
                    MessageBox.Show("Deserialization returned null. Check JSON format.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    // Debug: Show loaded values
                    MessageBox.Show($"Loaded Variant: {config.Variant}\nConfigBits: {config.ConfigBits.Count}\nPreconBits: {config.PreconBits.Count}\nSections: {config.Sections.Count}", "Debug", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    foreach (var section in config.Sections)
                    {
                        foreach (var bit in section.Value)
                        {
                            if (!config.ConfigBits.ContainsKey(bit.Key))
                                config.ConfigBits[bit.Key] = bit.Value;
                        }
                    }
                    if (config.Sections.TryGetValue("PreconBits", out var precon))
                    {
                        foreach (var kvp in precon)
                        {
                            if (!config.PreconBits.ContainsKey(kvp.Key))
                                config.PreconBits[kvp.Key] = kvp.Value;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error loading JSON: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            config ??= new DeviceConfig();
            config.ConfigBits ??= new();
            config.PreconBits ??= new();
            config.Sections ??= new();

            return config;
        }

        public void Save(string path)
        {
            var json = JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText(path, json);
        }
    }
}
