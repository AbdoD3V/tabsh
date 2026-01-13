#!/usr/bin/env python3

# ____IMPORTS______
from translations import commands
import subprocess
import utils
import os
try:
    from prompt_toolkit import PromptSession
    import prompt_toolkit
    from prompt_toolkit.history import FileHistory
    HAVE_PROMPT_TOOLKIT = True
except Exception:
    PromptSession = None
    prompt_toolkit = None
    FileHistory = None
    HAVE_PROMPT_TOOLKIT = False
import sys
from handle_scripts import script_handler
from rc_handler import handle_rc
from colorama import init, Fore, Style

# handle history and rc files
if not os.path.exists(os.path.expanduser("~/.config/.tabshhistory")):
    with open(os.path.expanduser("~/.config/.tabshhistory"), 'w') as f:
        f.close()

if not os.path.exists(".tabshrc"):
    with open(".tabshrc", 'w') as f:
        f.write("clear")
        f.close()


init(True)

# For directory tracking
global curr_dir
curr_dir = ""

# handle_scripts.py
script_handler(curr_dir, sys.argv)

safe_history_file = os.path.expanduser("~/.config/.tabshhistory")


if HAVE_PROMPT_TOOLKIT:
    try:
        history = FileHistory(safe_history_file)
    except PermissionError:
        from prompt_toolkit.history import InMemoryHistory
        history = InMemoryHistory()
    session = PromptSession(history=history, editing_mode=prompt_toolkit.enums.EditingMode.VI)
else:
    history = []
    session = None

# to be written to .tabshhistory
command_history = []



r = open(os.path.expanduser("~/.config/.tabshhistory"), 'a')

# rc_handler.py
curr_dir, alias = handle_rc(curr_dir)

while True:
    try:
        cmd = session.prompt(f"{curr_dir.replace(os.path.expanduser('~'), '~', 1)} $$ ").strip() # Clean prompt  
        command_history.append(cmd) # add to command history
    except (KeyboardInterrupt, EOFError): # Safe end
        continue # now to exit only use 'exit'

    
    if not cmd: # prevent empty commands
        continue
    if cmd == "خروج" or cmd == "quit" or cmd == "exit":  # exit
        r.write(utils.format_list(command_history))
        r.close()
        break

    # utils.py
    translated_cmd = utils.replace_all_keywords(cmd, commands) 
    base = translated_cmd.split()[0]

    # apply aliases (aliases are stored using translated command names)
    if base in aliases:
        alias_expansion = aliases[base]
        rest = '' if len(parts) == 1 else ' ' + ' '.join(parts[1:])
        translated_cmd = alias_expansion + rest
        parts = translated_cmd.split()
        base = parts[0]

    if base == "cd": # Handle directory changes safely
        parts = translated_cmd.split(maxsplit=1)
        path = parts[1] if len(parts) > 1 else os.path.expanduser("~")

        try:
            os.chdir(os.path.expanduser(path))
            curr_dir = os.getcwd()
        except FileNotFoundError:
            print(Fore.RED + f"cd: no such file or directory: {path}")
        except NotADirectoryError:
            print(Fore.RED + f"cd: not a directory: {path}")
        except PermissionError:
            print(Fore.RED + f"cd: permission denied: {path}")
    else:
        try:
            shell_exe = os.environ.get('SHELL', '/bin/sh')
            subprocess.run(translated_cmd, shell=True, executable=shell_exe)
        except Exception as e:
            print(Fore.RED + e) # error handling

r.close()