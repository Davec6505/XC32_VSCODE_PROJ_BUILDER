using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace Setup
{
    public class PinConfigurationUtility
    {
        /// <summary>
        /// Converts the old pin configuration format to the new comprehensive format
        /// </summary>
        public static void ConvertOldFormatToNew(string oldConfigPath, string newConfigPath, string pinMappingPath)
        {
            try
            {
                // Load old config
                var oldConfig = DeviceConfig.Load(oldConfigPath);
                if (oldConfig == null) return;

                // Load pin mappings
                var pinMappingManager = new PinMappingManager();
                if (!pinMappingManager.LoadPinMappings(pinMappingPath)) return;

                // Create new config with enhanced pin information
                var newConfig = oldConfig; // Start with the old config

                // Enhance pin configurations if they exist
                if (oldConfig.Sections?.TryGetValue("PinConfigurations", out var pinConfigs) == true)
                {
                    var enhancedPinConfigs = new Dictionary<string, object>();

                    foreach (var pinConfig in pinConfigs)
                    {
                        if (int.TryParse(pinConfig.Key, out _)) // It's a pin number
                        {
                            try
                            {
                                var oldPinData = JsonConvert.DeserializeObject<dynamic>(pinConfig.Value);
                                
                                // Get enhanced pin information from mapping
                                var pinMapping = pinMappingManager.GetPinMapping(pinConfig.Key);
                                
                                if (pinMapping != null)
                                {
                                    var enhancedPinData = new
                                    {
                                        PinName = oldPinData.PinName?.ToString() ?? pinMapping.PinName,
                                        SelectedFunction = oldPinData.SelectedFunction?.ToString() ?? pinMapping.DefaultFunction,
                                        AvailableFunctions = pinMapping.AvailableFunctions,
                                        Package = oldPinData.Package?.ToString() ?? "64-pin",
                                        PinType = pinMapping.PinType,
                                        Port = pinMapping.Port,
                                        PortPin = pinMapping.PortPin,
                                        AnalogChannel = pinMapping.AnalogChannel,
                                        PeripheralMappings = pinMapping.PeripheralMappings,
                                        IsReadOnly = pinMapping.IsReadOnly
                                    };
                                    
                                    enhancedPinConfigs[pinConfig.Key] = enhancedPinData;
                                }
                                else
                                {
                                    // Keep old data if no mapping found
                                    enhancedPinConfigs[pinConfig.Key] = oldPinData;
                                }
                            }
                            catch
                            {
                                // Skip invalid entries
                            }
                        }
                    }

                    // Update the config with enhanced data
                    newConfig.Sections["PinConfigurations"]["Enhanced"] = JsonConvert.SerializeObject(enhancedPinConfigs, Formatting.Indented);
                }

                // Save enhanced config
                newConfig.Save(newConfigPath);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error converting pin configuration: {ex.Message}");
            }
        }

        /// <summary>
        /// Validates pin configuration against available functions
        /// </summary>
        public static List<string> ValidatePinConfiguration(DeviceConfig config, string pinMappingPath)
        {
            var validationErrors = new List<string>();

            try
            {
                var pinMappingManager = new PinMappingManager();
                if (!pinMappingManager.LoadPinMappings(pinMappingPath))
                {
                    validationErrors.Add("Could not load pin mappings for validation");
                    return validationErrors;
                }

                // Extract device name for package determination
                if (!string.IsNullOrEmpty(config.DeviceName))
                {
                    string deviceName = config.DeviceName.Replace("PIC", "");
                    if (!pinMappingManager.SetDevice(deviceName))
                    {
                        validationErrors.Add($"Device '{deviceName}' not found in pin mappings");
                        return validationErrors;
                    }
                }

                // Validate pin configurations
                if (config.Sections?.TryGetValue("PinConfigurations", out var pinConfigs) == true)
                {
                    foreach (var pinConfig in pinConfigs)
                    {
                        if (int.TryParse(pinConfig.Key, out _)) // It's a pin number
                        {
                            try
                            {
                                var pinData = JsonConvert.DeserializeObject<dynamic>(pinConfig.Value);
                                string selectedFunction = pinData.SelectedFunction?.ToString();
                                
                                var pinMapping = pinMappingManager.GetPinMapping(pinConfig.Key);
                                if (pinMapping != null)
                                {
                                    if (!string.IsNullOrEmpty(selectedFunction) && 
                                        !pinMapping.AvailableFunctions.Contains(selectedFunction))
                                    {
                                        validationErrors.Add($"Pin {pinConfig.Key}: Function '{selectedFunction}' not available. Available functions: {string.Join(", ", pinMapping.AvailableFunctions)}");
                                    }

                                    // Check for read-only pins
                                    if (pinMapping.IsReadOnly && selectedFunction != pinMapping.DefaultFunction)
                                    {
                                        validationErrors.Add($"Pin {pinConfig.Key}: Cannot change function on read-only pin. Must be '{pinMapping.DefaultFunction}'");
                                    }
                                }
                            }
                            catch (Exception ex)
                            {
                                validationErrors.Add($"Pin {pinConfig.Key}: Error parsing configuration - {ex.Message}");
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                validationErrors.Add($"Validation error: {ex.Message}");
            }

            return validationErrors;
        }

        /// <summary>
        /// Generates a report of pin usage and conflicts
        /// </summary>
        public static string GeneratePinUsageReport(DeviceConfig config, string pinMappingPath)
        {
            var report = new System.Text.StringBuilder();
            report.AppendLine("Pin Usage Report");
            report.AppendLine("================");
            report.AppendLine();

            try
            {
                var pinMappingManager = new PinMappingManager();
                if (!pinMappingManager.LoadPinMappings(pinMappingPath))
                {
                    report.AppendLine("Error: Could not load pin mappings");
                    return report.ToString();
                }

                // Set device
                if (!string.IsNullOrEmpty(config.DeviceName))
                {
                    string deviceName = config.DeviceName.Replace("PIC", "");
                    if (pinMappingManager.SetDevice(deviceName))
                    {
                        report.AppendLine($"Device: {config.DeviceName}");
                        report.AppendLine($"Package: {pinMappingManager.GetCurrentPackage()}");
                        report.AppendLine();
                    }
                }

                // Analyze pin configurations
                var usedPeripherals = new Dictionary<string, List<string>>();
                var powerPins = new List<string>();
                var gpioPins = new List<string>();
                var analogPins = new List<string>();

                if (config.Sections?.TryGetValue("PinConfigurations", out var pinConfigs) == true)
                {
                    foreach (var pinConfig in pinConfigs)
                    {
                        if (int.TryParse(pinConfig.Key, out _)) // It's a pin number
                        {
                            try
                            {
                                var pinData = JsonConvert.DeserializeObject<dynamic>(pinConfig.Value);
                                string selectedFunction = pinData.SelectedFunction?.ToString() ?? "GPIO";
                                string pinName = pinData.PinName?.ToString() ?? "";

                                var pinMapping = pinMappingManager.GetPinMapping(pinConfig.Key);
                                if (pinMapping != null)
                                {
                                    // Categorize pins
                                    switch (pinMapping.PinType)
                                    {
                                        case "Power":
                                            powerPins.Add($"Pin {pinConfig.Key}: {pinName}");
                                            break;
                                        case "Analog":
                                            if (selectedFunction.StartsWith("ADC"))
                                                analogPins.Add($"Pin {pinConfig.Key}: {pinName} -> {selectedFunction}");
                                            else
                                                gpioPins.Add($"Pin {pinConfig.Key}: {pinName} -> {selectedFunction}");
                                            break;
                                        default:
                                            if (selectedFunction == "GPIO")
                                                gpioPins.Add($"Pin {pinConfig.Key}: {pinName}");
                                            else
                                                gpioPins.Add($"Pin {pinConfig.Key}: {pinName} -> {selectedFunction}");
                                            break;
                                    }

                                    // Track peripheral usage
                                    if (pinMapping.PeripheralMappings != null)
                                    {
                                        foreach (var peripheral in pinMapping.PeripheralMappings)
                                        {
                                            if (selectedFunction.Contains(peripheral.Key))
                                            {
                                                if (!usedPeripherals.ContainsKey(peripheral.Key))
                                                    usedPeripherals[peripheral.Key] = new List<string>();
                                                usedPeripherals[peripheral.Key].Add($"Pin {pinConfig.Key} ({peripheral.Value})");
                                            }
                                        }
                                    }
                                }
                            }
                            catch
                            {
                                // Skip invalid entries
                            }
                        }
                    }
                }

                // Generate report sections
                report.AppendLine("Power Pins:");
                foreach (var pin in powerPins)
                    report.AppendLine($"  {pin}");
                report.AppendLine();

                report.AppendLine("Peripheral Usage:");
                foreach (var peripheral in usedPeripherals)
                {
                    report.AppendLine($"  {peripheral.Key}:");
                    foreach (var pin in peripheral.Value)
                        report.AppendLine($"    {pin}");
                }
                report.AppendLine();

                report.AppendLine("Analog Pins:");
                foreach (var pin in analogPins)
                    report.AppendLine($"  {pin}");
                report.AppendLine();

                report.AppendLine("GPIO/Digital Pins:");
                foreach (var pin in gpioPins)
                    report.AppendLine($"  {pin}");
            }
            catch (Exception ex)
            {
                report.AppendLine($"Error generating report: {ex.Message}");
            }

            return report.ToString();
        }
    }
}