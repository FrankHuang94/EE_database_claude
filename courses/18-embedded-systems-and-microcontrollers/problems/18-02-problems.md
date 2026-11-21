# Problems 18-02 · Bare-Metal C and the Build Toolchain

Chapter: [18-02](../chapters/18-02-bare-metal-c-and-toolchain.md) · Worked solutions: [18-02 solutions](../solutions/18-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Sizes are in bytes unless stated; 1 KiB = 1024 bytes. Addresses are hexadecimal. The linker script is the chapter's (§3.4): sections start and end on 4-byte boundaries, the vector table is first in flash, `.data` and `.bss` start at the bottom of SRAM, the stack occupies the top. The target is a Cortex-M4 (Armv7E-M, little-endian). Problems marked *(lab)* can be checked with `labs/18-02-lab/bmbuild.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-02.1 [A]

**Which section?** For each file-scope declaration (unless stated) say where the object lives at run time and whether it costs flash, SRAM or both: (a) `int limit = 10;` (b) `int counter;` (c) `static char buf[256];` (d) `int zero = 0;` (e) `const uint16_t lut[4] = {1, 2, 4, 8};` (f) `uint8_t *p = buf;` (g) the string literal in `puts("hello");` (h) `int x = 3;` declared inside a function.

### Problem 18-02.2 [A]

**A size report.** A build reports `text` = 41 220, `data` = 2 312 and `bss` = 18 004. The MCU has 128 KiB of flash and 32 KiB of SRAM, and the stack is 2 KiB (no heap). Find the flash and SRAM used, as bytes and percentages, and the SRAM left.

### Problem 18-02.3 [A]

**The vector table.** A Cortex-M part has 82 external interrupts. (a) How many bytes is its vector table? (b) At what offset from the table's start is the entry for interrupt 37 (the first external interrupt is number 0)? (c) A disassembly shows the reset handler at 0x0800 1234, but word 1 of the table holds 0x0800 1235. Explain.

### Problem 18-02.4 [B]

**Fields by hand.** *(lab)* A register holds 0x1234 5678. (a) Set bits [19:16] to 0xA, clear bit 31 and set bit 2, in one expression with masks; give the result. (b) Extract bits [27:20] of the original value. (c) How many distinct (position, width) fields does a 32-bit register have, counting widths from 1 to 32?

### Problem 18-02.5 [B]

**How rare is a race?** A main loop performs a read-modify-write of a GPIO register every 10 µs. The window between its load and its store is 3 cycles at 48 MHz. An interrupt that writes another bit of the same register arrives at random times, 2000 times a second. (a) What fraction of interrupts land inside the window? (b) How many updates are lost per hour? (c) What does this say about testing for races?

### Problem 18-02.6 [B]

**A layout.** *(lab)* With flash at 0x0000 0000, 32 KiB of SRAM at 0x2000 0000, 32 external interrupts, `.text` 0x2F1D, `.rodata` 0x0412, `.data` 0x0099, `.bss` 0x0721 and a 0x800-byte stack, find `_sidata`, `_edata`, `_ebss`, the stack bottom, the free SRAM in bytes and the flash used.

### Problem 18-02.7 [B]

**Two addresses.** (a) In the layout of Problem 18-02.6, what are `.data`'s load and run addresses? (b) A raw binary image (`objcopy -O binary`) covers every loadable byte from the lowest to the highest load address. How large is it? (c) What would go wrong if the linker script said `.data … > RAM` with no `AT > FLASH`?

### Problem 18-02.8 [B]

**Startup time.** A firmware has 3 KiB of `.data` and 24 KiB of `.bss` and resets onto a 16 MHz oscillator. The copy loop costs 6 cycles per word and the zeroing loop 3. (a) How long is startup in µs? (b) The part can retain its SRAM in sleep, so after a wake only `.data` must be reinitialized (and only if the code needs fresh values). How long does that take? (c) Name one risk of skipping the `.bss` zeroing after a warm wake.

### Problem 18-02.9 [B]

**What may the compiler do?** For each fragment, say whether an optimizing compiler may remove, merge or reorder the accesses, and why: (a) `REG = 1; REG = 2;` with `REG` a `volatile` register; (b) the same with a non-volatile variable; (c) `for (int i = 0; i < 1000; i++) { }` used as a delay; (d) `while (!ready) { }` where `ready` is a non-volatile global set by an interrupt handler; (e) `buf[0] = 5; flag = 1;` where `flag` is `volatile` and `buf` is not, and a handler reads `buf` when it sees `flag`.

### Problem 18-02.10 [B]

**A register struct.** A UART's registers are CR at offset 0x00, SR 0x04, DR 0x08, then five reserved words, then BRR at 0x20. (a) Write a CMSIS-style `struct` for it. (b) With base 0x4001 3800, what is the address of BRR, and what is `sizeof` the struct? (c) Which members should be read-only, and why must every member be `volatile`?

### Problem 18-02.11 [B]

**Optimization levels.** *(lab)* The chapter's table gives the lab firmware's `.text` at each optimization level. (a) By what percentage is `-O2` larger than `-Os`, and why can a speed level produce more code? (b) The product's flash budget for the application is 1.3 KiB. Which levels fit? (c) Why should the team test at the level it ships?

### Problem 18-02.12 [C]

**HAL against registers, again.** A product line sells 300 000 units a year for four years. A HAL build is 46 KiB, a register-level build 30 KiB at 3 extra engineer-months of \$20 000. Updates need two slots plus a 4 KiB bootloader, and the team requires at least 20% of the flash free at launch. Parts: 64 KiB at \$0.88, 128 KiB at \$0.99. (a) Which (code base, part) pairs meet the headroom rule? (b) Which is cheapest over the product's life, counting parts and the extra engineering? (c) At what annual volume would the other compliant pair be cheaper?

### Problem 18-02.13 [C]

**Sizing the stack.** The deepest call chain from `main` uses frames of 64, 120, 248 and 56 bytes. Two interrupt priority levels can nest on top of it; their handlers use 96 and 40 bytes of their own stack. (a) What is the worst-case stack with integer-only code (8-word exception frames)? (b) With the FPU in use, so that each exception pushes a 26-word frame? (c) With a 25% margin, rounded up to a multiple of 8 bytes, what stack size should the linker script reserve for case (b)? (d) Why can the hardware frame be 4 bytes larger than stated?

---

## Objective coverage

| Learning objective (chapter 18-02) | Problems |
|---|---|
| 1. From source to flashed image | 3, 7, 11 |
| 2. Sections, flash and SRAM budgets | 1, 2, 6, 7 |
| 3. Linker scripts | 6, 7 |
| 4. Startup code and its cost | 3, 8, 13 |
| 5. Registers from C, races and `volatile` | 4, 5, 9, 10 |
| 6. Registers, CMSIS and HALs | 10, 12 |
