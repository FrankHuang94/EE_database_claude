# Lab 14-03 · Assembly and the Compilation Stack

Chapter: [14-03 Assembly and the Compilation Stack](../../chapters/14-03-assembly-and-the-compilation-stack.md)

## Objective

Drive a real toolchain (the clang compiler, LLVM's assembler and the LLD linker) from C to a running RV32I program. Read compiler output at two optimization levels, inspect object files for symbols and relocations, link with and without relaxation, and execute the results on an instruction-set simulator that counts instructions, calls and stack depth. Finally, measure how the ABI lays out structures on 32- and 64-bit targets.

## Background

Translating C (§3.2), procedures and the stack (§3.3), object files, linking and loading (§3.4), the ABI (§3.5) and the compiler's effect on instruction count (§3.6).

## Tools

You need `clang`, `ld.lld` and the LLVM tools (`llvm-mc`, `llvm-objdump`, `llvm-size`):

- Ubuntu/Debian: `sudo apt-get install llvm clang lld`.
- macOS: `brew install llvm lld`. Homebrew installs them outside your `PATH`; the notebook looks in Homebrew's directory.
- Windows: WSL with the Ubuntu packages.

The simulator is the course's own RV32I simulator, [verify/_rv32.py](../../verify/_rv32.py), which the notebook imports. It is about 150 lines of Python written from the instruction descriptions in the RISC-V specification; read it.

## Files

- [14-03-toolchain-lab.ipynb](14-03-toolchain-lab.ipynb): the notebook (Parts 1–4).
- [fib.s](fib.s) and [main.s](main.s): the hand-written recursive Fibonacci of Example 14-03.4 and a two-line program that calls it.
- [fib.c](fib.c) and [inc.c](inc.c): the same Fibonacci and the increment loop of Example 14-03.2, in C.
- [layouts.c](layouts.c): the structures of Example 14-03.6.

## Procedure

1. **Compiler output (Part 1).** Compile `inc.c` and `fib.c` to RV32I assembly with `-O0` and `-O2`. Compare the `-O2` loop with Example 14-03.2's pointer version, and count the stack accesses in the `-O0` code.
2. **Object files (Part 2).** Assemble `main.s` and `fib.s`, list their symbols (`llvm-objdump -t`) and relocations (`llvm-objdump -r`), then link with and without `--no-relax` and disassemble both executables.
3. **Running it (Part 3).** Run `fib(15)` from `fib.s` and from `fib.c` at `-O0` and `-O2`. *Predict first:* from $21F(n+1) - 18$, how many instructions does the hand-written version execute, and how deep does its stack go?
4. **Layouts (Part 4).** Compile `layouts.c` for 32-bit RISC-V, 64-bit RISC-V and x86-64, and print the sizes and offsets.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Compiler output | clang 18 at `-O2` produces the pointer loop of Example 14-03.2 (504 instructions for 100 elements); `-O0` reloads `i`, `n`, `k` and `a` from the stack every iteration and executes more than three times as many |
| 2 | Linking | Each `call` carries `R_RISCV_CALL_PLT` and `R_RISCV_RELAX`; relaxation turns each AUIPC + JALR into a JAL and shrinks the program from 96 to 84 bytes |
| 3 | Running | Hand-written `fib(15)` returns 610 after 20709 instructions and 1973 calls, 224 bytes deep. With clang 18, `-O0` code executes about twice as many instructions; `-O2` code makes half as many calls (987) but executes about 8% more instructions, because it builds a frame even for the base case |
| 4 | Layouts | `struct A` is 24 bytes and its reordering 16 on every target; `struct P` is 8 bytes on RV32 and 16 on RV64 and x86-64 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-03.a | fib(15), hand-written | 610 | — |
| Lab 14-03.b | instructions | 20709 | — |
| Lab 14-03.c | calls | 1973 | — |
| Lab 14-03.d | maximum stack depth | 224 | bytes |

*These are recomputed by [verify_14_03.py](../../verify/verify_14_03.py), which links and runs the same `fib.s` and checks the count against $21F(n+1) - 18$ for every $n$ from 0 to 15.*

## Discussion questions

1. Why does the `-O0` code store every argument to the stack on entry, even though it never needed to?
2. The linker, not the assembler, decides whether a call becomes one instruction or two. Why can't the assembler decide?
3. Clang's `-O2` Fibonacci makes about half the calls of the hand-written version, yet both are recursive. What did the compiler change?

### Answers

1. At `-O0` the compiler keeps every variable in a fixed stack slot for the whole function, so that a debugger can always show and change it. Arguments arrive in registers, so they are stored to their slots first. Optimization levels above `-O0` give up that convenience for speed.
2. The assembler sees one file at a time, so it does not know where a function in another file, or even later in the same section, will end up after linking; only the linker knows final addresses. RISC-V's answer is to emit the long form with a "relaxable" mark and let the linker shrink it.
3. It turned the second recursive call, `fib(n - 2)`, into a loop: the function calls itself for `fib(n - 1)` and then iterates instead of calling for the other branch. Each activation then makes only one call, roughly halving the number of activations. The algorithm is still exponential; the constant factor improved.

## Optional hardware extension

Build the same C functions for a RISC-V microcontroller board with its vendor's GCC or LLVM toolchain at `-O0` and `-O2`, read the cycle counter (`rdcycle`, or the board's timer) before and after a call, and compare measured cycles with the instruction counts from Part 3. The ratio is the board's effective CPI for that code.
