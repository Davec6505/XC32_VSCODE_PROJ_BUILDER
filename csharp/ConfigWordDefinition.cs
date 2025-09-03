namespace csharp
{
    public class ConfigWordOption
    {
        public string Value { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
    }

    public class ConfigWordDefinition
    {
        public string Name { get; set; }
        public string Mask { get; set; }
        public List<ConfigWordOption> Options { get; set; } = new();
    }

    public static class DaytonaConfigParser
    {
        public static List<ConfigWordDefinition> Parse(string filePath)
        {
            var result = new List<ConfigWordDefinition>();
            var lines = File.ReadAllLines(filePath);
            ConfigWordDefinition current = null;
            foreach (var line in lines)
            {
                if (line.StartsWith("CSETTING:"))
                {
                    var parts = line.Split(':');
                    var mask = parts[1];
                    var name = parts[3];
                    current = new ConfigWordDefinition { Name = name, Mask = mask };
                    result.Add(current);
                }
                else if (line.StartsWith("CVALUE:") && current != null)
                {
                    var parts = line.Split(':');
                    current.Options.Add(new ConfigWordOption
                    {
                        Value = parts[1],
                        Name = parts[2],
                        Description = parts.Length > 3 ? parts[3] : ""
                    });
                }
            }
            return result;
        }
    }
}