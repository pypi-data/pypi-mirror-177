#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import shutil
import stat
import logging
import subprocess

# Part of this implementation is taken/inspired from Emscripten tools/shared.py
# https://github.com/emscripten-core/emscripten/blob/2431347a32dcce89ab3e26e86de445cada58745c/tools/shared.py#L140-L191
# LICENSE below:

# Copyright (c) 2010-2014 Emscripten authors, see AUTHORS file.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Configure logging before importing any other local modules so even
# log message during import are shown as expected.
DEBUG = int(os.environ.get("WASIX_DEBUG", "0"))

logging.basicConfig(
    format="%(name)s:%(levelname)s: %(message)s",
    level=logging.DEBUG if DEBUG else logging.INFO,
)

logger = logging.getLogger("wasix")


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def is_wasm(fpath):
    with open(fpath, "rb") as f:
        first_bytes = f.read(4)
        # is_wasm = first_bytes == [0x00, 0x61, 0x73, 0x6d]
        is_wasm = bytearray(first_bytes) == b"\x00asm"
        f.seek(0)
        return is_wasm
    return False


def print_debug(what):
    if not DEBUG:
        return
    print(what)


def try_to_wrap_executable(exe_name):
    print_debug("Trying to wrap executable {}".format(exe_name))
    target_path = os.path.join(os.getcwd(), exe_name)
    if (
        not is_exe(target_path)
        or exe_name.endswith(".wasm")
        or exe_name.endswith(".dylib")
        or exe_name.endswith(".dll")
        or exe_name.endswith(".so")
    ):
        print_debug("Executable is not really executable. Skipping")
        return

    # It's a cmake file, we skip
    # CMake does some checks like the size of a struct generating
    # a file with certain contents on it and then doing a check using
    # regex. That means that we can't wrap it in a executable
    if os.path.basename(exe_name).startswith("cmTC_"):
        return

    st = os.stat(target_path)
    if not is_wasm(target_path):
        print_debug("Executable is not a Wasm file")
        return

    new_target_path = "{}.wasm".format(target_path)
    # shutil.copy(target_path, new_target_path)
    # Needed for old Python
    # run_process(["wasm-opt", target_path, "--fpcast-emu", "-o", new_target_path])
    # run_process(["wasm-opt", target_path, "-O3", "-o", new_target_path])

    shutil.copy(target_path, new_target_path)

    with open(target_path, "w") as f:
        f.write('#!/bin/bash\nwasix-run {} "$@"\n'.format(new_target_path))

    os.chmod(new_target_path, st.st_mode)

    # # Copy files to the temp folder
    # # Wasm file
    # temp_target_path = os.path.join('/tmp', os.path.split(new_target_path)[1])
    # shutil.copy(new_target_path, temp_target_path)
    # # Executable file
    # temp_target_path = os.path.join('/tmp', os.path.split(target_path)[1])
    # shutil.copy(target_path, temp_target_path)


def find_output_arg(args):
    """Find and remove any -o arguments.  The final one takes precedence.
    Return the final -o target along with the remaining (non-o) arguments.
    """
    outargs = []
    specified_target = None
    use_next = False
    for arg in args:
        if use_next:
            specified_target = arg
            use_next = False
            continue
        if arg == "-o":
            use_next = True
        elif arg.startswith("-o"):
            specified_target = arg[2:]
        else:
            outargs.append(arg)
    return specified_target, outargs


def get_environ(base_env=None):
    from .constants import (
        WASIX_CC,
        WASIX_CXX,
        WASIX_LD,
        WASIX_AR,
        WASIX_RANLIB,
        WASIX_NM,
    )

    if base_env is None:
        base_env = os.environ

    return {
        **base_env,
        "CC": WASIX_CC,
        "CXX": WASIX_CXX,
        "LD": WASIX_LD,
        "AR": WASIX_AR,
        "RANLIB": WASIX_RANLIB,
        "NM": WASIX_NM,
        "WASIX_CC": WASIX_CC,
        "WASIX_CXX": WASIX_CXX,
        "WASIX_LD": WASIX_LD,
        "WASIX_AR": WASIX_AR,
        "WASIX_RANLIB": WASIX_RANLIB,
        "WASIX_NM": WASIX_NM,
    }


# TODO: Investigate switching to shlex.quote
def shlex_quote(arg):
    arg = os.fspath(arg)
    if (
        " " in arg
        and (not (arg.startswith('"') and arg.endswith('"')))
        and (not (arg.startswith("'") and arg.endswith("'")))
    ):
        return '"' + arg.replace('"', '\\"') + '"'

    return arg


# Switch to shlex.join once we can depend on python 3.8:
# https://docs.python.org/3/library/shlex.html#shlex.join
def shlex_join(cmd):
    return " ".join(shlex_quote(x) for x in cmd)


def run_process(cmd, check=False, input=None, *args, **kw):
    """Runs a subprocess returning the exit code.
    By default this function will raise an exception on failure.  Therefor this should only be
    used if you want to handle such failures.  For most subprocesses, failures are not recoverable
    and should be fatal.  In those cases the `check_call` wrapper should be preferred.
    """

    # Flush standard streams otherwise the output of the subprocess may appear in the
    # output before messages that we have already written.
    sys.stdout.flush()
    sys.stderr.flush()
    kw.setdefault("universal_newlines", True)
    kw.setdefault("encoding", "utf-8")
    ret = subprocess.run(cmd, check=check, input=input, *args, **kw)
    debug_text = "%sexecuted %s" % ("successfully " if check else "", shlex_join(cmd))
    logger.debug(debug_text)
    return ret
