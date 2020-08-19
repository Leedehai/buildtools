# Copyright (c) 2020 Leedehai. All rights reserved.
# Use of this source code is governed under the LICENSE.txt file.

import os, sys
import platform
import shutil
import subprocess
from typing import Dict, List, Optional, cast

def _get_sys() -> Optional[str]:
    sys_platform = sys.platform
    if sys_platform.startswith("linux"):
        return "linux"
    if sys_platform in ["darwin", "mac"]:
        return "mac"
    return None

def _get_arch() -> Optional[str]:
    machine = platform.machine()
    if machine in ["AMD64", "amd64", "x86_64", "x64"]:
        return "x64"
    if machine in ["arm64", "aarch64"]:
        return "arm64"
    if machine in "riscv64":
        return "riscv64"
    return None

def has_bin_on_PATH(name: str) -> bool:
    # Early return if the Chromium development kit exists. If it exist,
    # the target binary found on PATH was tailored for Chromium projects.
    if shutil.which("gclient") != None:
        return False
    return shutil.which(name) != None


sys_name, arch_name = _get_sys(), _get_arch()
binary_dir = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "bin", cast(str, sys_name))

def execute(program: str, *, args: List[str], env: Dict[str, str]) -> int:
    return subprocess.Popen([program] + args, env=env).wait()
