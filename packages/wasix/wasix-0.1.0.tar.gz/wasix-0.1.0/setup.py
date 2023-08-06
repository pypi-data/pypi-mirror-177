# -*- coding: utf-8 -*-

from setuptools import setup
import os
import codecs


CURRENT_DIR = os.path.dirname(__file__)


def get_long_description():
    readme_md = os.path.join(CURRENT_DIR, "README.md")
    with open(readme_md) as ld_file:
        return ld_file.read()


setup(
    name='wasix',
    description="WASIX is a POSIX-Compliant WebAssembly compiler based on WASI",
    # long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="webassembly wasi wasienv wasix wasmer",
    author="Syrus Akbary",
    author_email="syrus@wasmer.io",
    url="https://github.com/wasmer/wasix",
    version='0.1.0',
    packages=['wasix'],
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    install_requires=[
        "ziglang",
    ],
    entry_points={'console_scripts': [
        'wasix-ar = wasix.commands:wasix_ar',
        'wasix-cc = wasix.commands:wasix_cc',
        'wasix-c++ = wasix.commands:wasix_cpp',
        'wasix-clang = wasix.commands:wasix_cc',
        'wasix-clang++ = wasix.commands:wasix_cpp',
        'wasix-configure = wasix.commands:wasix_configure',
        'wasix-ld = wasix.commands:wasix_ld',
        'wasix-make = wasix.commands:wasix_make',
        'wasix-run = wasix.commands:wasix_run',
        'wasix-nm = wasix.commands:wasix_nm',
        'wasix-ranlib = wasix.commands:wasix_ranlib',
        'wasm-cc = wasix.commands:wasm_cc',
        'wasm-c++ = wasix.commands:wasm_cc',
    ]},
)
