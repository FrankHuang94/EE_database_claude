# Lab 14-02 · Instruction Set Architecture: RISC-V, Arm and x86

Chapter: [14-02 Instruction Set Architecture: RISC-V, Arm and x86](../../chapters/14-02-isa-risc-v-arm-x86.md)

## Objective

Write an RV32I encoder and decoder from the format table and check them, instruction by instruction, against a production assembler. Build 32-bit constants with LUI and ADDI and test the rule on every possible low half. Measure the code size of one function in four instruction sets, and run the RISC-V version on a small instruction-set simulator to connect static size with the dynamic instruction count of the iron law.

## Background

The six RV32I formats and their immediates (§3.3), constants and reach (§3.4), compressed instructions (§3.5), and the A64 and x86-64 contrast (§3.6).

## Tools

The lab uses `llvm-mc`, the LLVM machine-code assembler, which assembles RISC-V, Arm and x86 from one installation:

- Ubuntu/Debian: `sudo apt-get install llvm`.
- macOS: `brew install llvm`, then use the `llvm-mc` in Homebrew's `llvm/bin` directory.
- Windows: the LLVM release installer, or WSL with the Ubuntu package.

Try it by hand first:

```bash
echo "add x5, x6, x7" | llvm-mc -triple=riscv32 -mattr=-c -show-encoding
```

## Files

- [14-02-isa-lab.ipynb](14-02-isa-lab.ipynb): the notebook (Parts 1–4).
- [sum_rv32.s](sum_rv32.s), [sum_a64.s](sum_a64.s) and [sum_x86.s](sum_x86.s): the array-sum function of Example 14-02.5, tested at the top of the loop.
- [sum_rv32_rot.s](sum_rv32_rot.s), [sum_a64_rot.s](sum_a64_rot.s) and [sum_x86_rot.s](sum_x86_rot.s): the rotated versions of Problem 14-02.9.

## Procedure

1. **Encoder and decoder (Part 1).** Implement the R, I, S, B, U and J formats and a decoder that slices fields and reassembles immediates. Encode a list of instructions, compare each with `llvm-mc`, and round-trip each through the decoder.
2. **Constants (Part 2).** Implement hi = ⌊(C + 0x800)/4096⌋ mod 2²⁰ and lo = C − 4096·hi. Test the pair on random constants by executing LUI and ADDI in the simulator. Then count how many of the 4096 possible low halves need the rounded-up upper part.
3. **Code size (Part 3).** Assemble the three `sum_*.s` files, with RISC-V both with and without compression, and print each instruction's bytes. *Predict first:* which version is smallest, and which largest?
4. **Simulator (Part 4).** Assemble `sum_rv32.s` and `sum_rv32_rot.s` to machine code, load them into a 30-line RV32I simulator, and run each on the array 1, 2, …, 100. Count the instructions executed.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Encoder against assembler | Every word matches; for example `sw x5, 12(x2)` is 0x00512623 |
| 2 | Constants | Every random constant is rebuilt exactly; half of all low halves need the rounding |
| 3 | Code size | x86-64 19 bytes, RV32IC 20, A64 32, RV32I 36 |
| 4 | Simulator | Both versions return 5050; the top-tested loop executes 604 instructions and the rotated one 504 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-02.a | encoding of sw x5, 12(x2) | 0x00512623 | — |
| Lab 14-02.b | low halves needing the rounded-up upper part | 50 | % |
| Lab 14-02.c | sum returned for 1, 2, …, 100 | 5050 | — |
| Lab 14-02.d | instructions executed, top-tested loop, n = 100 | 604 | — |
| Lab 14-02.e | instructions executed, rotated loop, n = 100 | 504 | — |

*These are recomputed by [verify_14_02.py](../../verify/verify_14_02.py), which assembles the same files with `llvm-mc` and runs them on its own simulator.*

## Discussion questions

1. Why does exactly half of all 32-bit constants need the upper part rounded up?
2. The RV32IC version shrinks from 36 to 20 bytes, but executes exactly as many instructions. Which term of the iron law does compression improve, and how could it still speed the program up?
3. Your simulator decodes one instruction at a time. What would a hardware decoder for RV32IC need to do differently to decode four instructions per cycle?

### Answers

1. The rounding is needed exactly when bit 11 of the constant is 1, because that is when the low 12 bits read as a negative signed number. Bit 11 is 1 for half of all values.
2. None directly: IC, CPI and clock period are unchanged in an ideal machine. Compression reduces the bytes fetched, so more of the program fits in the instruction cache and less fetch bandwidth is needed. Fewer instruction-cache misses lower the *effective* CPI (14-09).
3. It must find where each instruction starts. Each 16-bit parcel's bottom two bits say whether it begins a 32-bit instruction, so the decoder examines every parcel of the fetch block in parallel. It then picks the first four starts and expands each 16-bit instruction to its 32-bit equivalent. That is more logic than RV32I's fixed 4-byte slots, but far less than x86's byte-by-byte length decoding.

## Optional hardware extension

Any RISC-V development board (many low-cost microcontroller boards use RISC-V cores) can run the same function. Compile a C version with `-O2` for the board, disassemble it with `llvm-objdump -d`, and compare the compiler's loop with the hand-written ones. Compilers rotate loops and often unroll them.
