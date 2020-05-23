# Copyright (c) 2020 Leedehai. All rights reserved.
# Use of this source code is governed under the LICENSE.txt file.

import os, sys
import platform
import shutil
import subprocess
from typing import Dict, List

def _get_sys_arch():
    if platform.machine() not in ["AMD64", "x86_64"]:
        return None
    if sys.platform.startswith("linux"):
        return "linux-amd64"
    if sys.platform == "darwin":
        return "mac-amd64"
    raise NotImplementedError("Platform '%s' not supported" % sys.platform)


def has_bin_on_PATH(name: str) -> bool:
    # Early return if the Chromium development kit exists. If it exist,
    # the target binary found on PATH was tailored for Chromium projects.
    if shutil.which("gclient") != None:
        return False
    return shutil.which(name) != None


sys_arch = _get_sys_arch()
sys, arch = sys_arch.split('-')
binary_dir = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "bin", sys)

def execute(program: str, *, args: List[str], env: Dict[str, str]) -> int:
    return subprocess.Popen([program] + args, env=env).wait()
