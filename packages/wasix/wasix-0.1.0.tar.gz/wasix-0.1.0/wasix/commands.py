import sys
from .base import CommandException, cc, cpp, ar, configure, ld, make, ranlib, run
from subprocess import PIPE, CompletedProcess


def wrap_command(func):
    def f(*args, **kwargs):
        try:
            process = func(*args, **kwargs)
            assert isinstance(process, CompletedProcess)
            return process.returncode
        except CommandException as e:
            print(e)
            exit(1)

    return f


@wrap_command
def wasix_ar():
    args = sys.argv[1:]
    return ar(args)


@wrap_command
def wasix_cc():
    args = sys.argv[1:]
    return cc(args)


@wrap_command
def wasix_cpp():
    args = sys.argv[1:]
    return cpp(args)


@wrap_command
def wasm_cc():
    raise Exception("wasm-cc not currently supported")


@wrap_command
def wasix_configure():
    args = sys.argv[1:]
    return configure(args)


@wrap_command
def wasix_ld():
    args = sys.argv[1:]
    return ld(args)


@wrap_command
def wasix_make():
    args = sys.argv[1:]
    return make(args)


@wrap_command
def wasix_nm():
    raise Exception("nm not currently supported")


@wrap_command
def wasix_ranlib():
    args = sys.argv[1:]
    return ranlib(args)


@wrap_command
def wasix_run():
    args = sys.argv[1:]
    return run(args)
