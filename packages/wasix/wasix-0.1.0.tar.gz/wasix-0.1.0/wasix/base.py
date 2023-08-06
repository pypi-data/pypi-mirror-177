from .constants import WASIX_CMAKE
from .utils import (
    find_output_arg,
    try_to_wrap_executable,
    get_environ,
    run_process,
)

import sys, subprocess, os
import os


class CommandException(Exception):
    pass


def ar(cmd_args, *args, **kwargs):
    return run_process(
        [sys.executable, "-m", "ziglang", "ar", *cmd_args], *args, **kwargs
    )


def cc(cmd_args, *args, **kwargs):
    # Add a wasi target, if it doesn't have one
    has_target = any([arg.startswith("--target") for arg in cmd_args])
    if not has_target:
        cmd_args.append("--target=wasm32-wasi")

    output_target, outcmd_args = find_output_arg(cmd_args)

    # cmd_args.append('-D_WASI_EMULATED_MMAN')
    # cmd_args.append('-D_WASI_EMULATED_SIGNAL')
    # cmd_args.append('-D_WASI_EMULATED_TERMIOS')
    # cmd_args.append('-D_WASI_EMULATED_PTHREAD')

    # cmd_args.append('-Wl,-lwasi-emulated-mman')
    # cmd_args.append('-Wl,-lwasi-emulated-signal')
    # cmd_args.append('-Wl,-lwasi-emulated-termios')
    # cmd_args.append('-Wl,-lwasi-emulated-pthread')

    # if '-Wno-unused-command-line-argument' not in cmd_args:
    #     # We silence the not used libraries
    #     cmd_args.append('-Wno-unused-command-line-argument')

    process = run_process(
        [sys.executable, "-m", "ziglang", "cc", *cmd_args], *args, **kwargs
    )

    if output_target:
        try_to_wrap_executable(output_target)

    return process


def cpp(cmd_args, *args, **kwargs):
    # Add a wasi target, if it doesn't have one
    has_target = any([arg.startswith("--target") for arg in cmd_args])
    if not has_target:
        cmd_args.append("--target=wasm32-wasi")

    output_target, outcmd_args = find_output_arg(cmd_args)

    process = run_process(
        [sys.executable, "-m", "ziglang", "c++", *cmd_args], *args, **kwargs
    )

    if output_target:
        try_to_wrap_executable(output_target)

    return process


def base_cc(cmd_args, *args, **kwargs):
    # has_target = any([arg.startswith("--target") for arg in cmd_args])

    # # Flags decided by following: https://github.com/wasmer/wasix/pull/8
    # cmd_args.append("--no-standard-libraries")
    # cmd_args.append("-Wl,--export-all")
    # cmd_args.append("-Wl,--no-entry")

    # if not has_target:
    #     cmd_args.append("--target=wasm32-unknown-wasi")

    raise CommandException("wasm-cc not currently supported")


def configure(cmd_args, *args, **kwargs):
    kwargs["env"] = get_environ(kwargs.get("env"))

    if len(cmd_args) == 0:
        raise CommandException(
            "You need to run wasiconfigure with another command (eg. `wasiconfigure ./configure`)"
        )

    return run_process([*cmd_args], *args, **kwargs)


def ld(cmd_args, *args, **kwargs):
    # cmd_args.append('-lwasi-emulated-mman')
    # cmd_args.append('-lwasi-emulated-signal')
    # cmd_args.append('-lwasi-emulated-termios')
    # cmd_args.append('-lwasi-emulated-pthread')

    output_target, outcmd_args = find_output_arg(cmd_args)

    process = run_process(
        [sys.executable, "-m", "ziglang", "ld", *cmd_args], *args, **kwargs
    )

    if output_target:
        try_to_wrap_executable(output_target)

    return process


def make(cmd_args, *args, **kwargs):
    # If using cmake, we point to the toolchain file directly
    kwargs["env"] = get_environ(kwargs.get("env"))

    if len(cmd_args) == 0:
        raise CommandException(
            "You need to run wasimake with make or cmake (eg. `wasimake cmake .`)"
        )

    if cmd_args[0] == "cmake":
        path = cmd_args[1]
        if len(cmd_args) == 0:
            raise CommandException("cmake needs to have a path")
        return run_process(
            [
                "cmake",
                path,
                "-DCMAKE_TOOLCHAIN_FILE={}".format(WASIX_CMAKE),
                *cmd_args[2:],
            ],
            *args,
            **kwargs
        )

    elif cmd_args[0] == "make":
        return run_process(["make", *cmd_args[1:]], *args, **kwargs)

    else:
        raise CommandException(
            "wasix-make can only be called with cmake or make (eg. `wasimake make`), received {}".format(
                cmd_args[0:]
            )
        )


def ranlib(cmd_args, *args, **kwargs):
    return run_process(
        [sys.executable, "-m", "ziglang", "ranlib", *cmd_args], *args, **kwargs
    )


def run(cmd_args, *args, **kwargs):
    if len(cmd_args) < 1:
        # It should be wasix-run x.wasm
        raise CommandException("You need to provide a WebAssembly file")
    filename = cmd_args[0]
    process = run_process(
        ["wasmer", "run", "--dir=.", "--enable-all", filename, "--", *cmd_args[1:]],
        *args,
        **kwargs
    )
    return process
