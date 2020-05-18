#!/usr/bin/env python3
# Copyright: see README and LICENSE under the project root directory.
# Author: @Leedehai
#
# File: gn.py
# ---------------------------
# Wrapper script of the GN binary. If binary is not found, it will
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
BIN_PATH = os.path.join(BIN_DIR, "gn")


def execute_with_downloaded_bin(args: list) -> int:
    if not os.path.isfile(BIN_PATH):
        import get_binaries
        if 0 != get_binaries.run():  # Download both GN and Ninja
            return 1
    return subprocess.call([BIN_PATH] + args[1:])


def has_bin_locally(name: str) -> bool:
    # Early return if the Chromium development kit exists. If it exist,
    # the target binary found on PATH was tailored for Chromium projects.
    if shutil.which("gclient") != None:
        return False
    return shutil.which(name) != None


def main(args: list) -> int:
    programe_name = os.path.basename(BIN_PATH)
    if has_bin_locally(programe_name):
        return subprocess.call([programe_name] + args[1:])
    else:
        return execute_with_downloaded_bin(args)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit("\x1b[33mgn.py: Interrupted\x1b[0m")
