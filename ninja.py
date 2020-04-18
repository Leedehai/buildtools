#!/usr/bin/env python3
# Copyright: see README and LICENSE under the project root directory.
# Author: @Leedehai
#
# File: ninja.py
# ---------------------------
# Wrapper script of the ninja binary. If binary is not found, it will
# download it.

import os, sys
import platform
import shutil
import subprocess


def get_platform():
    if platform.machine() not in ["AMD64", "x86_64"]:
        return None
    if sys.platform.startswith("linux"):
        return "linux-amd64"
    if sys.platform == "darwin":
        return "mac-amd64"
    raise NotImplementedError("Platform '%s' not supported" % sys.platform)


BIN_DIR = os.path.join(  # This project only supports Linux or macOS
    os.path.abspath(os.path.dirname(__file__)), "bin",
    ("linux" if get_platform().startswith("linux") else "macos"))
BIN_PATH = os.path.join(BIN_DIR, "ninja")

# The progress status printed before the rule being run:
# %f: finished_tasks_count %t: total_tasks_count
# %e: elapsed_time (seconds in floating number)
ENVIRON = dict(os.environ)
ENVIRON.update({"NINJA_STATUS": "[%f/%t:%es] "})


def execute(program: str, args: list) -> int:
    # Popen.wait() returns the child's return code
    return subprocess.Popen([program] + args, env=ENVIRON).wait()


def execute_with_downloaded_bin(args: list) -> int:
    if not os.path.isfile(BIN_PATH):
        import get_binaries
        if 0 != get_binaries.run():  # Download both GN and Ninja
            return 1
    return execute(BIN_PATH, args[1:])


def has_bin_locally(name: str) -> bool:
    # Early return if the Chromium development kit exists. If it exist,
    # the target binary found on PATH was tailored for Chromium projects.
    if shutil.which("gclient") != None:
        return False
    return shutil.which(name) != None


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
