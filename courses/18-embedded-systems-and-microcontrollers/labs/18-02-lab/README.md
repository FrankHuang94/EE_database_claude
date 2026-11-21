# Lab 18-02 · A Bare-Metal Cortex-M4 Project, Built and Run

Chapter: [18-02 · Bare-Metal C and the Build Toolchain](../../chapters/18-02-bare-metal-c-and-toolchain.md)

## Objective

Build a complete bare-metal firmware image from C, with no vendor code at all, and run it on an emulated Cortex-M4:

- cross-compile with clang and link with ld.lld under your own linker script;
- read the image: sections, symbols, the vector table and the layout the linker chose;
- run the firmware on QEMU and watch its self-checks pass, then break the startup code and watch them fail;
- see what the optimizer does to code with and without `volatile`, and to code size.

## Background

The linker script places the vector table, code and constants in flash, gives `.data` a run address in SRAM and a load address in flash, and reserves `.bss` and the stack in SRAM (§3.4). The startup code copies `.data`, zeroes `.bss` and calls `main` (§3.5). Registers are reached through `volatile` pointers, and fields are changed with masks (§3.6). QEMU's `mps2-an386` machine models Arm's MPS2 FPGA board with a Cortex-M4; its code memory at 0x0000 0000 plays the role of flash. The firmware reports through Arm **semihosting**: `BKPT 0xAB` with a request in R0, which QEMU services to print text and to exit with status 0 (pass) or 1 (fail).

## Tools

clang, ld.lld and the LLVM binary tools (`llvm-size`, `llvm-nm`, `llvm-objdump`), and `qemu-system-arm`. On Ubuntu or WSL: `sudo apt-get install clang lld llvm qemu-system-arm`. The published numbers were produced with clang 18.1 and QEMU 8.2; other versions may place code differently, and the verify script will flag it.

## Files

- `fw/link.ld`: the linker script (256 KiB "flash" at 0x0000 0000, 64 KiB SRAM at 0x2000 0000, a 4 KiB stack).
- `fw/startup.c`: the vector table and `Reset_Handler`; compile with `-DLAB_SKIP_DATA_COPY` or `-DLAB_SKIP_BSS_ZERO` to break it.
- `fw/main.c`: the self-checking application (startup checks, register fields, the CPUID and SysTick core registers).
- `fw/regbits.h`: field mask, insert and extract helpers; `fw/semihost.h`: semihosting calls.
- `fw/poll.c`: the `volatile` example of Example 18-02.5 (compiled and disassembled, not run).
- `host/regbits_test.c`: a host-side test of `regbits.h` over every field position and width, run by `tools/run_c.py` with sanitizers.
- `bmbuild.py`: `build`, `compile_object`, `sections`, `berkeley`, `symbols`, `vector_table`, `disassemble`, `run_qemu`, and the chapter's `layout` and `startup_cycles` models.
- `18-02-bare-metal-lab.ipynb`: the guided notebook.

To build and run by hand from this directory:

```bash
clang --target=thumbv7em-none-eabi -mcpu=cortex-m4 -mthumb -mfloat-abi=soft -O2 -ffreestanding -nostdlib -fno-unwind-tables -fno-asynchronous-unwind-tables -fuse-ld=lld -Wl,-T,fw/link.ld -o fw.elf fw/startup.c fw/main.c
```

```bash
qemu-system-arm -M mps2-an386 -nographic -monitor none -semihosting-config enable=on,target=native -kernel fw.elf
```

## Procedure

1. **Sections and symbols.** Predict the section and address of `magic`, `offsets`, `zeros`, `squares` and `fake_reg` in `main.c`. Build, then list the sections and symbols.
2. **The vector table.** Predict words 0 and 1. Read them from the ELF, and find the function whose address is word 1 minus 1.
3. **Run it, then break it.** Run the firmware. Then build with `LAB_SKIP_DATA_COPY` and with `LAB_SKIP_BSS_ZERO`, predict each outcome, and run.
4. **`volatile`.** Predict the code of `wait_plain` and `wait_volatile` in `poll.c` at `-O0`, `-O2` and `-Os`; compile and disassemble.
5. **Optimization and size.** Predict the order of `.text` sizes at `-O0`, `-O1`, `-O2`, `-Os` and `-Oz`; build all five and check that each still passes on QEMU.
6. **The layout formulas.** From the section sizes, predict `_sidata`, `_edata` and `_ebss` with §3.4's formulas and compare with the symbol table.

## Expected results

- Part 1: `magic`, `offsets` and `fake_reg` in `.data` at the bottom of SRAM (0x2000 0000 onward), `zeros` in `.bss` after them, `squares` in flash with the code.
- Part 2: word 0 = 0x2001 0000, the top of the 64 KiB SRAM; word 1 = 0x0000 005D, which is `Reset_Handler` (at 0x5C) plus the Thumb bit.
- Part 3: `TEST PASSED` and exit status 0. Without the `.data` copy, the `.data` checks fail (and the field checks, whose register starts with an initial value) and QEMU exits with status 1. Without the `.bss` zeroing the firmware still passes, because QEMU's SRAM starts at zero; on real hardware it would not.
- Part 4: at `-O2` `wait_plain` is a single `bx lr`; `wait_volatile` loads the flag on every test; at `-O0` both load it every iteration.
- Part 5: `-O0` 1504, `-O1` 1244, `-O2` 1452, `-Os` 1232, `-Oz` 860 bytes of `.text` (clang 18), all passing.
- Part 6: `_sidata` = 0x0000 0604 (the code ends at 0x5EC, followed by a 24-byte unwind index), `_edata` = 0x2000 0010, `_ebss` = 0x2000 0114.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-02.a | vector-table word 0 (initial SP) | 0x20010000 | — |
| Lab 18-02.b | vector-table word 1 (reset handler) | 0x0000005D | — |
| Lab 18-02.c | `.data` size | 16 | bytes |
| Lab 18-02.d | `.bss` size | 260 | bytes |
| Lab 18-02.e | _sidata | 0x00000604 | — |
| Lab 18-02.f | _ebss | 0x20000114 | — |
| Lab 18-02.g | QEMU exit status without the .data copy | 1 | — |
| Lab 18-02.h | field cases checked by the host test | 2640 | — |

## Discussion

1. Why does the vector table need `KEEP` in the linker script, and what would happen at reset without it?
2. Why did removing the `.bss` loop not fail under QEMU, and how would you make the test catch it?
3. In Part 4, why does `wait_volatile` at `-O2` contain four loads instead of one?

## Answers

1. Nothing in the program refers to `vector_table` by name; it is read only by the hardware at reset. With `--gc-sections`, the linker would discard it as unused, and the core would read its stack pointer and reset address from whatever landed at address 0, typically crashing at once. `KEEP` (and the `used` attribute in C) marks it as a root.
2. QEMU, like many simulators, starts with RAM full of zeros, so variables in `.bss` happen to read 0 even if nobody cleared them. To catch the missing loop, fill SRAM with a pattern before the startup code runs (QEMU can load a RAM image, or a debugger script can write one), or have the test write nonzero values to `.bss`, trigger a soft reset that preserves RAM, and check again.
3. The compiler unrolled the loop four times to reduce branch overhead. Each copy must still load the flag, because every read of a `volatile` object is a required access; the unrolling changes how often the loop branches, not how often the flag is read.

## Optional hardware

On any Cortex-M4 board (an STM32 Nucleo-F4, an NXP FRDM-K64F or similar), change `link.ld`'s memory origins and lengths to the part's flash (often 0x0800 0000) and SRAM, add the part's interrupt vectors, and replace semihosting output with a GPIO toggle or ITM. Flash the image through the board's debug probe with OpenOCD or pyOCD, then read the reset-cause register and time the startup with the cycle counter (`DWT->CYCCNT`) to compare with §3.5's estimate.
