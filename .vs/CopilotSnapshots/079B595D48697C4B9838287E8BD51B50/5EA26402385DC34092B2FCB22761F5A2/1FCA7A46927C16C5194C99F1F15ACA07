using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Windows.Forms;

namespace Setup
{
    public class DeviceConfig
    {
        public string Variant { get; set; } // "MX" or "MZ"
        public Dictionary<string, string> ConfigBits { get; set; } = new();
        public Dictionary<string, string> PreconBits { get; set; } = new();

        public static DeviceConfig Load(string path)
        {
            if (!File.Exists(path)) return null;
            var json = File.ReadAllText(path);
            return JsonSerializer.Deserialize<DeviceConfig>(json);
        }

        public void Save(string path)
        {
            var json = JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText(path, json);
        }
    }
}
