<div align="center">
  <a href="https://docs.wasmer.io/ecosystem/wasix" target="_blank" rel="noopener noreferrer">
    <img width="240" src="https://raw.githubusercontent.com/wasmer/wasix/master/logo.png" alt="Wasmer logo">
  </a>
  
  <p>
    <a href="https://github.com/wasmer/wasix/actions?workflow=CI">
      <img src="https://github.com/wasmer/wasix/workflows/CI/badge.svg?style=flat-square" alt="Tests">
    </a>
    <a href="https://slack.wasmer.io">
      <img src="https://img.shields.io/static/v1?label=Slack&message=join%20chat&color=brighgreen&style=flat-square" alt="Slack channel">
    </a> 
    <a href="https://github.com/wasmerio/wasmer/blob/master/LICENSE">
      <img src="https://img.shields.io/github/license/wasix/wasix.svg?style=flat-square" alt="License">
    </a>
  </p>

  <h3>
    <a href="https://docs.wasmer.io/ecosystem/wasix">wasix Docs</a>
    <span> • </span>
    <a href="https://slack.wasmer.io/">Slack</a>
    <span> • </span>
    <a href="https://twitter.com/wasmerio">Twitter</a>
  </h3>

</div>

<br />

wasix is a tool that aims to bring all programming languages to [WebAssembly WASI](https://github.com/WebAssembly/WASI). With `wasix` you can compile:

* C/C++ projects to Wasm + WASI ([see usage example](https://docs.wasmer.io/ecosystem/wasix/compile-c-c++-to-wasm-wasix))
* Swift to Wasm + WASI ([see usage example](https://docs.wasmer.io/ecosystem/wasix/compile-swift-to-wasm-wasix))

So you can run them anywhere (with any [Standalone WASI WebAssembly runtime](https://wasmer.io), or [in the Browser](https://webassembly.sh)).

> Note: If you aim to use the WebAssembly files in the web directly (using graphics, audio or other tools that are not supported in WASI) then [Emscripten](https://emscripten.org/) is probably a much better choice.

## Install

You can install `wasix` with:

```sh
curl https://raw.githubusercontent.com/wasmer/wasix/master/install.sh | sh
```

> Note: we also ship `wasix` in a Docker image. You can check [how to use the wasix Docker image here](https://github.com/wasmer/wasix/blob/master/docker/).


### Develop

If you want to develop wasix locally, you can simply do:

```bash
# Clone the repo
git clone https://github.com/wasmerio/wasix.git
cd wasix

# Setup the package locally
make install-dev
```

And then, activate the virtual environment `wasix-cc`, `wasix-ld` and the rest of the commands are available:

```
source ./venv/bin/activate
```

## Using wasix for C projects

If you want to compile a C file to a WebAssembly WASI:

```sh
# To compile to a WebAssembly WASI file
# This command will generate:
#  • An executable: ./example
#  • A WebAssembly file: ./example.wasm
wasix-cc examples/example.c -o example

# If you are using configure
wasix-configure ./configure

# If you are using cmake (or make)
wasix-make cmake .
```

If you want to compile a C file to plain WebAssembly:

```sh
# To compile to a WebAssembly file
# This command will generate:
#  • An executable: ./example
#  • A WebAssembly file: ./example.wasm
wasm-cc examples/example.c -o example
```

## Commands

### `wasix-cc`

It's a wrapper on top of `clang`, with additions for the stubs, sysroot and target.
It also detects autoexecutables in the output and wraps to execute them with a WebAssembly WASI runtime via `wasix-run`.

### `wasixc++`

It's a wrapper on top of `clang++`, with additions for the stubs, sysroot and target.
It also detects autoexecutables in the output and wraps to execute them with a WebAssembly WASI runtime via `wasix-run`.

### `wasm-cc`

It's a wrapper on top of `clang`, with additions for preconfiguring the wasm linker, target, etc...

### `wasm-c++`

It's a wrapper on top of `clang++`, with additions for preconfiguring the wasm linker, target, etc...

### `wasix-configure`

It's a helper that adds the wasix environment vars (`CC`, `CXX`, `RUNLIB`, ...) to the following command (`./configure`).

Example:

```sh
wasix-configure ./configure
```

### `wasix-make`

It's a helper that adds the wasix environment vars (`CC`, `CXX`, `RUNLIB`, ...) for the make (`make` or `cmake`).

Example:

```sh
# With CMake
wasix-make cmake .

# With Make
wasix-make make
```

### `wasix-run`

It executes a given WebAssembly file with a standalone WebAssembly runtime.

```sh
wasix-run myfile.wasm
```

## Contributing

After cloning this repo, ensure dependencies are installed by running:

```sh
make install-dev
```

After that, all the commands will be available on your shell and you should be able to start seeing the changes directly without re-installing wasix.

## Testing

After running `make install-dev` you can run directly:

```sh
make test
```

## How wasix compares to …?

### Emscripten

[Emscripten](https://emscripten.org/) is a great toolchain that let's you compile your C/C++ projects to WebAssembly so you can use them in the web easily.

However, Emscripten has a **non-stable ABI** (because constant and fast iteration is very useful for their usecase).
This makes it a bit challening for standalone-runtimes to continually adapt.
Because of that, adopting the WASI ABI is a much easier path for standalone server-side WebAssembly runtimes.

Right now Emscripten is [moving towards WASI adoption](https://github.com/emscripten-core/emscripten/issues/9479). 
However, Emscripten can only emit WASI WebAssembly files for some programs as Emscripten's filesystem layer supports POSIX features not yet present in WASI.

Emscripten has also some tools that are not needed (nor supported) in the case of server-side Standalone WebAssembly runtimes, such as [`EM_JS` and `EM_ASM`](https://emscripten.org/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.html#calling-javascript-from-c-c).

wasix learns a lot from Emscripten, since they figured out the perfect ergonomics for having C/C++ projects to adopt WebAssembly. Alon, the creator of Emscripten, is without any doubt one of the brilliant minds behind WebAssembly and he inspired us with his work to keep improving the ergonomics of WASI.

### WASI-libc

WASI-libc is the "frontend ABI" for WASI. By itself, it only provides header files and implementations that make C compilers adopt WASI very easily via the `--sysroot` flag.

### WASI-SDK

We can see WASI-SDK as the union between `WASI-libc` and the compiler binaries `clang`, `wasm-ld`, ...

wasix is using WASI-SDK under the hood to compile to WebAssembly, however it differs from it in two major ways:
1. `wasix` is designed to work with **multiple SDKs** versions
2. `wasix` is completely focused on the **ergonomics**, exposing very simple to use CLI tools so that projects can adopt it easily.

We can think of `wasix` as applying the ergonomic ideas from Emscripten to the WASI-SDK
