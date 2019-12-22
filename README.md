# buildtools

Build tools: [ninja](https://ninja-build.org) and [GN](https://gn.googlesource.com/gn)

### Prerequisites

- Linux or macOS
- Python 3.5+

### Transparent setup

Ninja and GN are niche, unlike Make and CMake, which are almost ubiquitous on every
developer's machine. Therefore, the proxy scripts [ninja.py](ninja.py) and [gn.py](gn.py)
will download the binaries over the network on first invocation if:
- `ninja` and `gn` are missing from `PATH`, or
- `ninja` and `gn` are found on `PATH`, but `gclient` is also found on `PATH` (presence
of `gclient` implies the `ninja` and `gn` commands found are customized for the Chromium projects).

### Alternative setup

If you wish not to download Ninja and GN binaries over the network or there's an error,
you can tell the proxy scripts to use locally-built/installed binaries.

```sh
# Assume you are at this directory.

# step 1: create bin/XXX and change working directory
mkdir -p bin/linux # on macOS: mkdir -p bin/darwin
cd bin/linux       # on macOS: cd bin/darwin

# step 2: make symlinks
ln -s /path/to/your/gn gn
ls -s /path/to/your/ninja ninja

# step 3: verify
cd ../..
./gn.py --version
./ninja.py --version
```

###### EOF
