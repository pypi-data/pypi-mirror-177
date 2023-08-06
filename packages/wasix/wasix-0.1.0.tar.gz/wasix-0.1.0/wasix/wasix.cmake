# Cmake toolchain description file for the Makefile for WASI
cmake_minimum_required(VERSION 3.4.0)

set(WASI TRUE)

set(CMAKE_SYSTEM_NAME Generic) # Generic for now, to not trigger a Warning
set(CMAKE_SYSTEM_VERSION 1)
set(CMAKE_SYSTEM_PROCESSOR wasm32)
set(CMAKE_C_COMPILER_ID wasix)
set(triple wasm32-wasi)

set(CMAKE_C_COMPILER $ENV{WASIX_CC})
set(CMAKE_CXX_COMPILER $ENV{WASIX_CXX})
set(CMAKE_LINKER $ENV{WASIX_LD} CACHE STRING "Linker for wasm32-wasix")
set(CMAKE_AR $ENV{WASIX_AR} CACHE STRING "Archiver for wasm32-wasix")
set(CMAKE_RANLIB $ENV{WASIX_RANLIB} CACHE STRING "Ranlib for wasm32-wasix")
set(CMAKE_C_COMPILER_TARGET ${triple} CACHE STRING "")
set(CMAKE_ASM_COMPILER_TARGET ${triple} CACHE STRING "")

# Don't look in the sysroot for executables to run during the build
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# Only look in the sysroot (not in the host paths) for the rest
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

set(CMAKE_C_COMPILER_WORKS ON)
set(CMAKE_CXX_COMPILER_WORKS ON)
set(CMAKE_CROSSCOMPILING, OFF)
set(CMAKE_BUILD_TESTS, OFF)
