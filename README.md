# TABSH
 ## The Arabic Bash Shell
 This project is still experimental and NOT reliable for daily use, yet.
 Fork of TABSH by MOHAPY24.
 A better README, improved functionaliy and reliability are coming soon

## Native utilities (optional)

This repo includes optional native utilities under `native/` that can accelerate some tasks.

- `native/csharp/` — a small C# `keyword_replacer` CLI that reads a JSON mapping and a command string and prints the translated command. `tabsh` will try to call this tool (via `dotnet run` or a built DLL) to apply keyword replacements before falling back to the Python implementation.
- `native/` (future) — a Rust executor prototype that can run pipelines and `&&` groups; currently experimental.

Build and run the C# replacer (requires .NET SDK 7):

```bash
cd native/csharp
dotnet build -c Release
# run with mapping and command
dotnet run --project . --configuration Release -- --map /path/to/mapping.json --cmd "echo hello && echo world"
```

If the C# tool is built as a DLL, `tabsh` will prefer calling it directly with `dotnet <dll>`.

Example: run a small script with `tabsh`:

```bash
cat > /tmp/tabsh_test.txt <<'EOF'
echo start && echo ok
echo foo | grep f
EOF

python3 tabsh.py /tmp/tabsh_test.txt
```
