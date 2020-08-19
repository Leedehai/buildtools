# buildtools

Build tools: [ninja](https://ninja-build.org) and [GN](https://gn.googlesource.com/gn)

[Why Ninja and GN](https://gist.github.com/Leedehai/5a0fba275543891f192b92868ee603c0)

### Prerequisites

- Linux or macOS
- Python 3.7+

### Transparent setup

Unlike Make and CMake, which are almost ubiquitous on every developer's machine,
Ninja and GN are niche. Therefore, the proxy scripts [ninja.py](ninja.py) and
[gn.py](gn.py) will download the binaries over the network on first invocation
if:
- `ninja` and `gn` are missing from `PATH`, or
- `ninja` and `gn` are found on `PATH`, but `gclient` is also found on `PATH`
(presence of `gclient` implies the `ninja` and `gn` commands found are
customized for the Chromium projects).

The zipball URLs for downloading are in the [get_binaries.py](get_binaries.py)
source, or can be shown with command `get_binaries.py --show-urls`.

After downloading, the binaries will be stored in `bin/linux` (or `bin/mac` if
you are on a macOS). They will not be added to your `PATH`. Instead, you should
call the proxy scripts in lieu of calling the binaries.

### Alternative setup

If you wish not to download Ninja and GN binaries over the network or there's an
error, you can tell the proxy scripts to use locally-built/installed binaries.

```sh
# Assume you are at this directory.

# step 1: create bin/XXX and change working directory
mkdir -p bin/linux # on macOS: mkdir -p bin/mac
cd bin/linux       # on macOS: cd bin/mac

# step 2: make symlinks
ln -s /path/to/your/gn gn
ls -s /path/to/your/ninja ninja

# step 3: verify
cd ../..
./gn.py --version
./ninja.py --version
```

###### EOF
