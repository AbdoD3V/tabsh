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

Example script

```bash
cat > /tmp/tabsh_test.txt <<'EOF'
echo start && echo ok
echo foo | grep f
EOF

./tabsh.sh /tmp/tabsh_test.txt
```

If you'd like, I can also add a packaged `make` or `setup` target to build the optional native utilities.
