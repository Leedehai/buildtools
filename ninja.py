#!/usr/bin/env python3
# Copyright: see README and LICENSE under the project root directory.
# Author: @Leedehai
#
# File: ninja.py
# ---------------------------
# Wrapper script of the ninja binary. If binary is not found, it will
# download it.
#
# Migrated from Python2.7; new features not all applied yet.

import os, sys
import platform
import subprocess

def get_platform():
    if platform.machine() not in ["AMD64", "x86_64"]:
        return None
    if sys.platform.startswith("linux"):
        return "linux-amd64"
    if sys.platform == "darwin":
        return "mac-amd64"
    raise NotImplementedError("Platform '%s' not supported" % sys.platform)

BIN_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "bin", (
        "linux" if get_platform().startswith("linux") else "darwin"))
BIN_PATH = os.path.join(BIN_DIR, "ninja")

# the progress status printed before the rule being run:
# %f: finished_tasks_count %t: total_tasks_count
# %e: elapsed_time (seconds in floating number)
ENVIRON = dict(os.environ)
ENVIRON.update({ "NINJA_STATUS": "[%f/%t:%es] " })
def execute(program: str, args: list) -> int:
    # Popen.wait() returns the child's return code
    return subprocess.Popen([ program ] + args, env=ENVIRON).wait()

def execute_with_downloaded_bin(args: list) -> int:
    if not os.path.isfile(BIN_PATH):
        import get_binaries
        if 0 != get_binaries.run(): # Download both GN and Ninja
            return 1
    return execute(BIN_PATH, args[1:])

def has_bin_locally(name: str) -> bool:
    # I could use shutil.which() but it's only available in Python3.3+
    with open(os.devnull, 'w') as devnull:
        has_chromium_dev_depot_tools = 0 == subprocess.call(
            [ "which", "gclient" ], stdout=devnull, stderr=devnull
        )
        if has_chromium_dev_depot_tools:
            return False
        ret = subprocess.call(
            [ "which" ] + [ name ], stdout=devnull, stderr=devnull
        )
    return ret == 0

def main(args: list) -> int:
    programe_name = os.path.basename(BIN_PATH)
    if has_bin_locally(programe_name):
        return execute(programe_name, args[1:])
    else:
        return execute_with_downloaded_bin(args)

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.stderr.write("\x1b[33m ninja.py: Interrupted\x1b[0m")
        sys.exit(1)
