#!/usr/bin/env python3

import utils
import os
import subprocess
import sys
import shlex
from colorama import init, Fore, Style
from translations import commands

init(True)

def script_handler(current_dir, argvs:list): # handle scripts passed as arguments
    try:
        script = argvs[1]
        with open(script, 'r') as f:
            scode = f.read().strip() # get script contents without trailing newlines/whitespaces
            for cmd in scode.splitlines(): # for each line
                if not cmd:
                    continue
                if cmd == "خروج" or cmd == "quit" or cmd == "exit":  # exit 
                    break


                # Translate command keywords
                # utils.py
                translated_cmd = utils.replace_all_keywords(cmd, commands)
                base = translated_cmd.split()[0]

                if base == "cd":
                    parts = translated_cmd.split(maxsplit=1)
                    path = parts[1] if len(parts) > 1 else os.path.expanduser("~")

                    try:
                        os.chdir(os.path.expanduser(path))
                        current_dir = os.getcwd()
                    except FileNotFoundError:
                        print(Fore.RED + f"cd: no such file or directory: {path}")
                    except NotADirectoryError:
                        print(Fore.RED + f"cd: not a directory: {path}")
                    except PermissionError:
                        print(Fore.RED + f"cd: permission denied: {path}")
                else:
                    try:
                        # Parse respecting quoted strings, then handle && (AND) and | (pipe)
                        tokens = shlex.split(translated_cmd)

                        # Build a list of pipelines separated by &&. Each pipeline is a list of commands (each command is a list of tokens).
                        and_groups = []
                        pipeline = []
                        current_cmd = []

                        for t in tokens:
                            if t == '|':
                                pipeline.append(current_cmd)
                                current_cmd = []
                            elif t == '&&':
                                pipeline.append(current_cmd)
                                and_groups.append(pipeline)
                                pipeline = []
                                current_cmd = []
                            else:
                                current_cmd.append(t)

                        # append leftovers
                        if current_cmd:
                            pipeline.append(current_cmd)
                        if pipeline:
                            and_groups.append(pipeline)

                        last_rc = 0
                        for pipeline in and_groups:
                            # If previous AND-group failed, stop executing further groups
                            if last_rc != 0:
                                break

                            # If pipeline contains only one command, run it directly with the shell to preserve expansions
                            if len(pipeline) == 1:
                                cmd_str = ' '.join(pipeline[0])
                                ret = subprocess.run(cmd_str, shell=True)
                                last_rc = ret.returncode
                                continue

                            # Execute a pipeline of commands, streaming output to the terminal
                            procs = []
                            prev_proc = None
                            for i, cmd_tokens in enumerate(pipeline):
                                if not cmd_tokens:
                                    continue
                                cmd_str = ' '.join(cmd_tokens)
                                if i == 0:
                                    p = subprocess.Popen(cmd_str, shell=True, stdout=(subprocess.PIPE if len(pipeline) > 1 else None), executable='/bin/bash')
                                elif i < len(pipeline) - 1:
                                    p = subprocess.Popen(cmd_str, shell=True, stdin=prev_proc.stdout, stdout=subprocess.PIPE, executable='/bin/bash')
                                    prev_proc.stdout.close()
                                else:
                                    p = subprocess.Popen(cmd_str, shell=True, stdin=prev_proc.stdout, executable='/bin/bash')
                                    prev_proc.stdout.close()

                                procs.append(p)
                                prev_proc = p

                            # Wait for all procs to finish
                            for p in procs:
                                p.wait()

                            last_rc = procs[-1].returncode if procs else 0

                    except Exception as e:
                        print(Fore.RED + str(e))
        quit()


    except IndexError:
        pass