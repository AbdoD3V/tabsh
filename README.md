# TABSH
## The Arabic Bash Shell
This project is experimental. It provides a small shell-like wrapper around system commands and supports Arabic aliases/keywords.

Basic build & run
- Requirements: `python3` (3.8+), `pip`, and the packages in `requirements.txt`.
- Install dependencies:

```bash
pip3 install --user -r requirements.txt
```

- Run directly (recommended for development):

```bash
./tabsh.sh        # runs the packaged shell script
# or
python3 tabsh.py  # run the Python entrypoint
```

- Install for system-wide use (put in `PATH`):

```bash
sudo cp tabsh.sh /usr/local/bin/tabsh
sudo chmod +x /usr/local/bin/tabsh
# after this you can run `tabsh` from anywhere
```

There is also an installer script `tabshinstaller.sh` that tries to set up the environment and copy files into `/usr/local/bin` — review it before running.

Notes on native utilities
- Optional native helpers live under `native/` and are not required. The Python `utils.replace_all_keywords` will attempt to call the C# `keyword_replacer` (via `dotnet run` or a built DLL) if present, otherwise it falls back to the pure-Python implementation.

To build the C# replacer (optional, requires .NET SDK 7):

```bash
cd native/csharp
dotnet build -c Release
dotnet run --project . --configuration Release -- --map /path/to/mapping.json --cmd "echo hello && echo world"
```

Example script

```bash
cat > /tmp/tabsh_test.txt <<'EOF'
echo start && echo ok
echo foo | grep f
EOF

./tabsh.sh /tmp/tabsh_test.txt
```

If you'd like, I can also add a packaged `make` or `setup` target to build the optional native utilities.
