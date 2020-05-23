#!/usr/bin/env python3
# Copyright (c) 2020 Leedehai. All rights reserved.
# Use of this source code is governed under the LICENSE.txt file.
# -----
# Wrapper script of the GN binary. If binary is not found, it will
# download it.

import os, sys
from typing import Callable

import common_utils

BIN_PATH = os.path.join(common_utils.binary_dir, "gn")


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
                binary, args=sys.argv[1:], env=dict(os.environ))))
    except KeyboardInterrupt:
        sys.exit("\x1b[33mgn.py: Interrupted\x1b[0m")
