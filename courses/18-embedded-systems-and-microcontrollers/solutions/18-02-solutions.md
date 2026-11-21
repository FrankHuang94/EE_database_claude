# Solutions 18-02 · Bare-Metal C and the Build Toolchain

Problems: [18-02 problem set](../problems/18-02-problems.md) · Chapter: [18-02](../chapters/18-02-bare-metal-c-and-toolchain.md). Every number below is recomputed by [verify_18_02.py](../verify/verify_18_02.py).

---

## Solutions

### Solution 18-02.1

| Declaration | Section | Costs |
|---|---|---|
| (a) `int limit = 10;` | `.data` | flash (initial value) and SRAM |
| (b) `int counter;` | `.bss` | SRAM only |
| (c) `static char buf[256];` | `.bss` | SRAM only |
| (d) `int zero = 0;` | `.bss` (zero needs no stored value) | SRAM only |
| (e) `const uint16_t lut[4]` | `.rodata` | flash only |
| (f) `uint8_t *p = buf;` | `.data` (its initial value, the address of `buf`, is filled in by the linker) | flash and SRAM |
| (g) `"hello"` | `.rodata` | flash only |
| (h) `int x = 3;` in a function | stack, or only a register after optimization | SRAM (stack) at run time, nothing static |

The rule: anything that changes lives in SRAM; anything with a nonzero initial value also needs that value stored in flash.

### Solution 18-02.2

Flash: $41\,220 + 2\,312$ = **43 532** bytes, $43\,532/131\,072$ = **33.21** %. SRAM: $2\,312 + 18\,004 + 2\,048$ = **22 364** bytes, $22\,364/32\,768$ = **68.25** %, leaving $32\,768 - 22\,364$ = **10 404** bytes. SRAM, not flash, is this design's tighter resource.

### Solution 18-02.3

(a) $16 + 82 = 98$ entries of 4 bytes: **392** bytes.

(b) External interrupt $n$ is exception $16 + n$, so its entry is at offset $(16 + 37) \times 4 = 212$ = **0xD4**.

(c) Bit 0 of a branch target selects the instruction set; on Cortex-M it must be 1 (Thumb), so the toolchain stores the function's address plus 1. Loading a table entry with bit 0 clear would cause a UsageFault (invalid state) on the first instruction.

### Solution 18-02.4

(a) Masks: bits [19:16] are $0xF \ll 16 = 0x000F\,0000$; bit 31 is 0x8000 0000; bit 2 is 0x0000 0004. Then

$$
\text{new} = \big((0x1234\,5678 \mathbin{\&} \lnot 0x800F\,0000) \mathbin{|} (0xA \ll 16)\big) \mathbin{|} 0x4 .
$$

$0x1234\,5678 \mathbin{\&} \lnot 0x800F\,0000 = 0x1230\,5678$ (bit 31 was already 0), OR $0x000A\,0000$ gives 0x123A 5678, and setting bit 2 of the last byte (0x78 = 0111 1000 → 0111 1100) gives **0x123A567C**.

(b) $(0x1234\,5678 \gg 20) \mathbin{\&} 0xFF$: shifting right by 20 bits (five hex digits) leaves 0x123, whose low byte is **0x23**.

(c) A field of width $w$ can start at $33 - w$ positions, so the count is $\sum_{w=1}^{32}(33 - w) = \sum_{k=1}^{32}k = 32 \times 33/2$ = **528**. The lab's host test checks all of them.

### Solution 18-02.5

(a) The window lasts $3/(48 \times 10^6) = 62.5$ ns out of every 10 µs, so a randomly timed interrupt falls in it with probability $62.5\ \text{ns}/10\ \mu\text{s}$ = **0.00625**.

(b) $2000 \times 3600 \times 0.00625$ = **45 000** lost updates an hour.

(c) A race that hits one interrupt in 160 still happens 12 times a second. Races that are "rare" per event are frequent per hour, yet any one bench test may not show them; prevent them by design (single writer, atomic set/clear registers, critical sections) rather than by testing.

### Solution 18-02.6

Vectors: $(16 + 32) \times 4 = 192$ = 0xC0 bytes. Code and constants: $0x2F1D + 0x0412 = 0x332F$, ending at $0xC0 + 0x332F = 0x33EF$, aligned up: `_sidata` = **0x000033F0**. `.data` rounds to 0x9C: `_edata` = **0x2000009C**. `.bss`: $0x2000\,009C + 0x721 = 0x2000\,07BD$, aligned: `_ebss` = **0x200007C0**. Stack top $0x2000\,8000$, bottom $0x2000\,8000 - 0x800$ = **0x20007800**. Free SRAM: $0x7800 - 0x07C0 = 0x7040$ = **28 736** bytes. Flash used: $0x33F0 + 0x9C = 0x348C$ = **13 452** bytes.

### Solution 18-02.7

(a) Load address 0x0000 33F0 (in flash), run address 0x2000 0000 (in SRAM).

(b) The loadable bytes run from 0x0000 0000 to the end of `.data`'s load image, $0x33F0 + 0x9C = 0x348C$: the binary is **13 452** bytes. (Had `.data` no load address in flash, `objcopy` would have to span from 0x0000 0000 to 0x2000 009C: a 512 MiB file of mostly padding, a classic symptom of a broken script.)

(c) Without `AT > FLASH`, `.data`'s load address would equal its run address in SRAM. The initial values would not be in flash at all, so a programmer could not store them, and after power-up the variables would hold whatever SRAM contained.

### Solution 18-02.8

(a) $3072/4 = 768$ words to copy and $24\,576/4 = 6144$ to zero: $768 \times 6 + 6144 \times 3 = 4608 + 18\,432 = 23\,040$ cycles, $23\,040/(16 \times 10^6)$ = **1440** µs.

(b) Only the copy: $4608/(16 \times 10^6)$ = **288** µs.

(c) Variables in `.bss` keep their values from before the sleep. Code written for a cold start (assuming zero) may misbehave, for example a counter that should restart, or a stale pointer. Retention needs an explicit design: which variables persist, and which must be reset.

### Solution 18-02.9

(a) **Neither removed nor merged:** both stores to a `volatile` object are observable side effects and must occur, in order. (Some peripherals need exactly this, for example an unlock sequence.)

(b) The first store is dead (overwritten before any read), so the compiler may **remove** it and keep only `= 2`.

(c) The loop has no observable effect, so the compiler may **delete** it entirely; the "delay" becomes zero. Use a hardware timer, or a loop over a `volatile` counter (whose timing still depends on the compiler and the clock).

(d) The compiler may read `ready` **once** and spin forever, or, because a side-effect-free loop may be assumed to terminate, **delete** the loop (Example 18-02.5). Declare `ready` `volatile` or atomic.

(e) The compiler may **reorder** the non-volatile store to `buf` after the volatile store to `flag`, since only volatile accesses are ordered among themselves. The handler can then see `flag` = 1 and read a stale `buf[0]`. Make `buf` volatile, put a compiler barrier (`__asm__ volatile("" ::: "memory")`) between the stores, or use C11 atomics with release/acquire ordering.

### Solution 18-02.10

(a)

```c
typedef struct {
    volatile uint32_t CR;            /* 0x00 */
    volatile const uint32_t SR;      /* 0x04, read-only */
    volatile uint32_t DR;            /* 0x08 */
    uint32_t RESERVED[5];            /* 0x0C to 0x1F */
    volatile uint32_t BRR;           /* 0x20 */
} uart_t;
#define UART1 ((uart_t *)0x40013800u)
```

(b) BRR is at $0x4001\,3800 + 0x20$ = **0x40013820**. The struct is nine 32-bit words: **36** bytes.

(c) Status registers whose bits only hardware sets (SR here) should be `const` (CMSIS writes `__I`), so that the compiler rejects accidental writes; but if SR has write-1-to-clear bits, it must stay writable. Every member must be `volatile` because hardware changes registers on its own and because reads and writes have side effects (reading DR pops a received byte); without it the compiler could cache, merge or drop accesses.

### Solution 18-02.11

(a) $1452/1232 - 1$ = **17.9** %. Speed levels unroll loops and inline functions to save cycles, trading code size for speed; the lab's startup loops are unrolled four times at `-O2`.

(b) 1.3 KiB = 1331 bytes: `-O1` (1244), `-Os` (1232) and `-Oz` (860) fit; `-O0` (1504) and `-O2` (1452) do not.

(c) Optimization changes code layout, timing and, where the source has latent bugs (a missing `volatile`, undefined behaviour), the program's behaviour. A test campaign at `-O0` does not test the shipped binary.

### Solution 18-02.12

(a) Requirements: HAL $2 \times 46 + 4$ = **96** KiB; register-level $2 \times 30 + 4$ = **64** KiB. With 20% free required, a 64 KiB part allows at most 51.2 KiB, so neither build qualifies on it; a 128 KiB part allows 102.4 KiB, so both qualify: HAL leaves **25** % free and register-level **50** %.

(b) Both compliant pairs use the same \$0.99 part, so the parts cost is $0.99 \times 300\,000 \times 4$ = **\$1 188 000** either way, and the register-level build adds \$60 000 of engineering: the HAL on the 128 KiB part is cheaper by **\$60 000**.

(c) **Never.** Volume multiplies the part price, which is the same for both; the register-level build's saving in flash buys nothing unless it moves the product to a cheaper part, and here the headroom rule prevents that. Its remaining value is technical (speed, control, 50% headroom for growth), which the team may still judge worth \$60 000.

### Solution 18-02.13

(a) Calls: $64 + 120 + 248 + 56 = 488$ bytes. Each nested interrupt pushes an 8-word (32-byte) frame plus its handler's own use: $(32 + 96) + (32 + 40) = 200$. Total **688** bytes.

(b) With 26-word (104-byte) frames: $488 + (104 + 96) + (104 + 40)$ = **832** bytes.

(c) $832 \times 1.25 = 1040$, already a multiple of 8: reserve **1040** bytes (in practice a round 1.5 or 2 KiB, since measurement, library calls and future code all add depth).

(d) On exception entry the Cortex-M aligns the frame to 8 bytes (the default `CCR.STKALIGN` setting), inserting one padding word when the stack pointer is only 4-byte aligned; each frame can therefore be 4 bytes larger.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-02.2a | flash used | 43532 | bytes |
| 18-02.2b | flash used | 33.21 | % |
| 18-02.2c | SRAM used | 22364 | bytes |
| 18-02.2d | SRAM used | 68.25 | % |
| 18-02.2e | SRAM left | 10404 | bytes |
| 18-02.3a | vector table size | 392 | bytes |
| 18-02.3b | offset of interrupt 37 | 0xD4 | — |
| 18-02.4a | register after the three changes | 0x123A567C | — |
| 18-02.4b | bits [27:20] | 0x23 | — |
| 18-02.4c | fields in a 32-bit register | 528 | — |
| 18-02.5a | fraction of interrupts in the window | 0.00625 | — |
| 18-02.5b | lost updates per hour | 45000 | — |
| 18-02.6a | _sidata | 0x000033F0 | — |
| 18-02.6b | _edata | 0x2000009C | — |
| 18-02.6c | _ebss | 0x200007C0 | — |
| 18-02.6d | stack bottom | 0x20007800 | — |
| 18-02.6e | free SRAM | 28736 | bytes |
| 18-02.6f | flash used | 13452 | bytes |
| 18-02.7a | binary image size | 13452 | bytes |
| 18-02.8a | startup time | 1440 | µs |
| 18-02.8b | .data reinitialization time | 288 | µs |
| 18-02.10a | BRR address | 0x40013820 | — |
| 18-02.10b | struct size | 36 | bytes |
| 18-02.11a | -O2 over -Os | 17.9 | % |
| 18-02.12a | HAL flash requirement | 96 | KiB |
| 18-02.12b | register-level flash requirement | 64 | KiB |
| 18-02.12c | HAL free on 128 KiB | 25 | % |
| 18-02.12d | register-level free on 128 KiB | 50 | % |
| 18-02.12e | lifetime parts cost | 1188000 | \$ |
| 18-02.12f | HAL advantage | 60000 | \$ |
| 18-02.13a | worst-case stack, integer only | 688 | bytes |
| 18-02.13b | worst-case stack with FPU frames | 832 | bytes |
| 18-02.13c | reserved stack | 1040 | bytes |
