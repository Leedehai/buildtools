#!/usr/bin/env python3
# Copyright: see README and LICENSE under the project root directory.
# Author: @Leedehai
#
# File: ninja.py
# ---------------------------
# Wrapper script of the ninja binary. If binary is not found, it will
# download it.

import os, sys
from typing import Callable

import common_utils

BIN_PATH = os.path.join(common_utils.binary_dir, "ninja")

# The progress status printed before the rule being run:
# %f: finished_tasks_count %t: total_tasks_count
# %e: elapsed_time (seconds in floating number)
ENVIRON = dict(os.environ)
ENVIRON.update({"NINJA_STATUS": "[%f/%t:%es] "})


# export
def find_binary(callback: Callable[[str], int]) -> int:
    bin_basename = os.path.basename(BIN_PATH)
    if common_utils.has_bin_on_PATH(bin_basename):
        return callback(bin_basename)
    if not os.path.isfile(BIN_PATH):
        import get_binaries # pylint: disable=import-outside-toplevel
        if 0 != get_binaries.run(argv=[]):  # Download both GN and Ninja
            return 1
    return callback(BIN_PATH)


if __name__ == "__main__":
    try:
        sys.exit(find_binary(
            lambda binary: common_utils.execute(
                binary, args=sys.argv[1:], env=ENVIRON)))
    except KeyboardInterrupt:
        sys.exit("\x1b[33mgn.py: Interrupted\x1b[0m")
