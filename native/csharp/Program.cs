using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.RegularExpressions;

class Program
{
    static int Main(string[] args)
    {
        string mapPath = null;
        string cmd = null;
        for (int i = 0; i < args.Length; i++)
        {
            if (args[i] == "--map" && i + 1 < args.Length) { mapPath = args[++i]; }
            else if (args[i] == "--cmd" && i + 1 < args.Length) { cmd = args[++i]; }
        }

        if (mapPath == null)
        {
            Console.Error.WriteLine("--map <file> is required");
            return 2;
        }

        if (!File.Exists(mapPath))
        {
            Console.Error.WriteLine($"mapping file not found: {mapPath}");
            return 3;
        }

        if (cmd == null)
        {
            // read command from stdin
            cmd = Console.In.ReadToEnd();
            if (cmd == null) cmd = "";
            cmd = cmd.TrimEnd('\n', '\r');
        }

        Dictionary<string, string> map;
        try
        {
            var json = File.ReadAllText(mapPath);
            map = JsonSerializer.Deserialize<Dictionary<string, string>>(json);
            if (map == null) map = new Dictionary<string, string>();
        }
        catch (Exception e)
        {
            Console.Error.WriteLine("failed to read mapping: " + e.Message);
            return 4;
        }

        // Split string literals out so we only replace outside quoted strings
        var stringRe = new Regex("(\".*?(?<!\\\\)\"|'.*?(?<!\\\\)')", RegexOptions.Singleline);
        var parts = stringRe.Split(cmd);

        for (int i = 0; i < parts.Length; i++)
        {
            if (i % 2 == 0)
            {
                // replace longer keys first
                foreach (var key in map.Keys.OrderByDescending(k => k.Length))
                {
                    if (string.IsNullOrEmpty(key)) continue;
                    parts[i] = parts[i].Replace(key, map[key]);
                }
            }
        }

        Console.Write(string.Join("", parts));
        return 0;
    }
}
