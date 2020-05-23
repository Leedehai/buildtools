#!/usr/bin/env python3
# Copyright (c) 2020 Leedehai. All rights reserved.
# Use of this source code is governed under the LICENSE.txt file.
# -----
# Download latest GN and Ninja binaries.
# You do not need to execute this script directly; gn.py and ninja.py will execute
# it if binaries are needed but not found.

import os, sys
import argparse
import io
import shutil
import stat
import subprocess
import zipfile
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from typing import Optional

import common_utils

BIN_DIR = common_utils.binary_dir
GN_BIN = "gn"
GN_URL = "https://chrome-infra-packages.appspot.com/dl/gn/gn/%s/+/latest" % common_utils.sys_arch
NINJA_BIN = "ninja"
NINJA_URL = "https://github.com/ninja-build/ninja/releases/latest/download/ninja-%s.zip" % common_utils.sys


def _download_and_unpack(what: str, url: str, output_dir: str, bin_name: str,
                         only_dowload_if_must: bool, verbose: bool) -> bool:
    """Download an archive from url and extract gn from it into output_dir."""
    file_path = os.path.join(output_dir, bin_name)
    already_exist = os.path.isfile(file_path)
    if only_dowload_if_must and already_exist:
        if verbose:
            print("[build tools] %s binary for '%s' already downloaded" %
                  (what, common_utils.sys_arch))
        return True
    # Do not remove any existing binary before (re-)downloading, because
    # downloading might encounter an error; a successful download can overwrite.
    if verbose:
        print("[build tools] Downloading %s binary for '%s'..." %
              (what, common_utils.sys_arch))
    try:
        # a bug in macOS's Python3 installation with HTTPS utilities
        # https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
        if sys.platform.lower().startswith("darwin"):
            from ssl import SSLContext
            network_stream = urlopen(url, context=SSLContext())
        else:
            network_stream = urlopen(url)
        zipfile.ZipFile(io.BytesIO(network_stream.read())).extract(
            bin_name, path=output_dir)
    except HTTPError as e:
        print("\tHTTPError %s: %s\n\turl: %s" % (e.code, e.reason, url))
        if 4 <= int(e.code / 100) <= 5:
            print("\t************** ACTION APPRECIATED ************\n"
                  "\t*                                            *\n"
                  "\t* If you are *certain* the URL isn't blocked *\n"
                  "\t* in your region, please alert the author of *\n"
                  "\t* this project (Leedehai on GitHub) this URL *\n"
                  "\t* is likely broken, HTTP error %3s           *\n"
                  "\t*                                            *\n"
                  "\t**********************************************" % e.code)
        return False
    except URLError as e:
        print("\tURLError: %s\n\turl: %s" % (e.reason, url))
        print("\tAre you...\n"
              "\t  1. disconnected from the network? or\n"
              "\t  2. behind an erring proxy?\n"
              "\t(other reasons may apply)")
        return False
    except Exception as e: # pylint: disable=broad-except
        print(e)
        return False
    return True


def _set_executable_bit(filepath: str) -> None:
    file_stats = os.stat(filepath)
    os.chmod(filepath, file_stats.st_mode | stat.S_IXUSR)


def _get_version_string(path: str) -> Optional[str]:
    try:
        out_bytes = subprocess.check_output([path, "--version"])
    except (subprocess.CalledProcessError, OSError):  # OSError: e.g. not found
        sys.stderr.write("[Error] '%s --version' returns an error\n" % path)
        return None
    return out_bytes.decode().strip()


def run(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="Download latest GN and Ninja binaries from:\n  %s\n  %s" %
        (GN_URL, NINJA_URL),
        epilog="If no option is given, download the binaries.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-u",
        "--show-urls",
        action="store_true",
        help="print URLs to download binaries and exit")
    parser.add_argument(
        "-v",
        "--versions",
        action="store_true",
        help="print version numbers of the downloaded binaries")
    parser.add_argument(
        "-i",
        "--skip-if-exists",
        action="store_true",
        help="skip re-downloading a binary if it exists")
    parser.add_argument(
        "-s", "--succinct", action="store_true", help="do not be so verbose")
    parser.add_argument(
        "-r",
        "--remove",
        action="store_true",  # remove bin/mac or bin/linux, depending on the current OS
        help="remove downloaded binaries in %s" % os.path.relpath(BIN_DIR))
    parser.add_argument(
        "-ra",
        "--remove-all",
        action="store_true",  # remove bin/, bin/mac, bin/linux
        help="remove directory %s" % os.path.relpath(os.path.dirname(BIN_DIR)))
    args = parser.parse_args(argv)

    if args.versions:
        gn_ver = _get_version_string(os.path.join(BIN_DIR, GN_BIN))
        ninja_ver = _get_version_string(os.path.join(BIN_DIR, NINJA_BIN))
        if gn_ver and ninja_ver:
            print("ninja: %s\tgn: %s" % (ninja_ver, gn_ver))
            return 0
        return 1

    if args.show_urls:
        print("%s: %s" % (GN_BIN, GN_URL))
        print("%s: %s" % (NINJA_BIN, NINJA_URL))
        return 0

    if args.remove:
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        return 0
    elif args.remove_all:
        shutil.rmtree(os.path.dirname(BIN_DIR), ignore_errors=True)
        return 0

    if not common_utils.sys_arch:
        print("no prebuilt binary offered for '%s'" % sys.platform)
        return 1

    if not os.path.exists(BIN_DIR):
        os.makedirs(
            BIN_DIR
        )  # os.makedirs() recursively make the intermediate directories

    has_error = False

    if True == _download_and_unpack("GN", GN_URL, BIN_DIR, GN_BIN,
                                    args.skip_if_exists, not args.succinct):
        _set_executable_bit(os.path.join(BIN_DIR, GN_BIN))
        gn_ver = _get_version_string(os.path.join(BIN_DIR, GN_BIN))
        if not gn_ver:
            has_error = True
    else:
        has_error = True

    if True == _download_and_unpack("Ninja", NINJA_URL, BIN_DIR, NINJA_BIN,
                                    args.skip_if_exists, not args.succinct):
        _set_executable_bit(os.path.join(BIN_DIR, NINJA_BIN))
        ninja_ver = _get_version_string(os.path.join(BIN_DIR, NINJA_BIN))
        if not ninja_ver:
            has_error = True
    else:
        has_error = True

    if has_error:
        print("Error encountered: cannot download binaries.")
        print("To circumvent: see %s/README.md section 'Alternative setup'." %
              os.path.dirname(__file__))
    else:
        print("  ninja: %s\tgn: %s" % (ninja_ver, gn_ver))

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
