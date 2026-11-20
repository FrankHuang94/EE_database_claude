# Solutions 14-03 · Assembly and the Compilation Stack

Problems: [14-03 problems](../problems/14-03-problems.md) · Chapter: [14-03](../chapters/14-03-assembly-and-the-compilation-stack.md). Every listing below and in the problems is assembled by LLVM, linked by LLD and executed on an RV32I simulator by [verify_14_03.py](../verify/verify_14_03.py). The script also compiles the structures with clang for three ABIs and links the two-file example to read its addresses and encodings.

---

## Solutions

### Solution 14-03.1

(a) The function makes calls, so it must save **ra**. It uses the callee-saved registers s0, s1 and s2, so it must save each before use and restore it before returning. That is **4** registers. The temporaries need no saving by the function itself: if it needs one across a call, that is its own problem as the caller. (b) Four 4-byte registers fill 16 bytes, already a multiple of 16: a **16**-byte frame.

### Solution 14-03.2

`a[3]` is at a constant offset of $3 \times 4$ = **12** bytes, which the load absorbs. `a[i]` needs an address computation:

```asm
pick:
    lw   t0, 12(a0)       # a[3]
    slli t1, a1, 2
    add  t1, a0, t1       # &a[i]
    lw   t1, 0(t1)        # a[i]
    add  a0, t0, t1
    ret
```

That is **5** instructions before the `ret`.

### Solution 14-03.3

| Pseudo-instruction | Base instructions |
|---|---|
| `li a0, 100` | `addi a0, zero, 100` (1) |
| `li a0, 0x12345678` | `lui a0, 0x12345` then `addi a0, a0, 0x678` (2; 14-02 §3.4) |
| `not a0, a1` | `xori a0, a1, -1` |
| `neg a0, a1` | `sub a0, zero, a1` |
| `seqz a0, a1` | `sltiu a0, a1, 1` (only 0 is below 1 unsigned) |
| `bgt a0, a1, L` | `blt a1, a0, L` (operands swapped) |
| `ret` | `jalr zero, 0(ra)` |
| `call f` | `auipc ra, 0` then `jalr ra, 0(ra)`, with relocations for the linker (2) |

So `li a0, 100` is **1** instruction, `li a0, 0x12345678` is **2**, and `call f` is **2** as the assembler emits it (often relaxed to 1 by the linker).

### Solution 14-03.4

Three saved registers (12 bytes) plus `buf` (6 × 4 = 24 bytes) need 36 bytes. The next multiple of 16 is **48** bytes, so the alignment rule adds **12** bytes of padding. One possible layout puts ra at 44(sp), s0 at 40(sp), s1 at 36(sp) and `buf` at 0(sp) to 23(sp), leaving 24–35 unused.

### Solution 14-03.5

`srai t0, a0, 31` copies the sign bit into all 32 bits: t0 = 0 if $a \ge 0$ and t0 = −1 (all ones) if $a < 0$.

- **If $a \ge 0$:** `xor` with 0 and `sub` of 0 leave $a$ unchanged.
- **If $a < 0$:** `xor` with all ones gives $\sim a = -a - 1$ (the two's-complement identity, 08-01), and subtracting −1 adds 1, giving $-a$.

The function executes **4** instructions with `ret`, and there is no branch to mispredict.

`abs(-7)` = **7**. `abs(-2147483648)` returns **−2147483648**. Its negation, $2^{31}$, does not fit in a 32-bit signed integer, so it wraps back to $-2^{31}$. (In C this input is undefined behaviour for `abs`; the hardware simply wraps.)

### Solution 14-03.6

(a) t0 is incremented *after* each byte is loaded, including the terminating zero. When the loop exits, t0 points one past the terminator, so $t0 - a0 = L + 1$, and the `addi` removes the 1.

(b) Count in three parts:

- `mv` before the loop: 1.
- The loop body (`lbu`, `addi`, `bnez`) runs once per character plus once for the terminator: $3(L + 1)$.
- `sub`, `addi` and `ret` at the end: 3.

The total is $I = 3L + 7$. For `"hello"` ($L$ = 5) that is **22**.

### Solution 14-03.7

(a) The intended result is $g(3) + g(4) = 7 + 9$ = **16**. Trace the buggy version:

1. t0 = 4.
2. `g(3)` overwrites t0 with 6 and t1 with 7, and returns 7.
3. t1 = 7, then a0 = t0 = 6, not 4.
4. `g(6)` returns 13, and also sets t1 = 13.
5. The final `add` gives 13 + 13 = **26**.

(b) The bug is keeping y and g(x) in temporaries across calls. Temporaries are caller-saved, and `g` is entitled to overwrite them, which it does. Keep both in callee-saved registers, saved in the prologue:

```asm
sum2_fixed:
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s0, 8(sp)
    sw   s1, 4(sp)
    mv   s0, a1           # keep y in a saved register
    call g
    mv   s1, a0           # keep g(x) in a saved register
    mv   a0, s0
    call g
    add  a0, s1, a0
    lw   ra, 12(sp)
    lw   s0, 8(sp)
    lw   s1, 4(sp)
    addi sp, sp, 16
    ret
```

(c) `sum2_fixed` executes 15 instructions and each `g` 4, so the total is **23**. The frame holds three registers (12 bytes), rounded to 16.

### Solution 14-03.8

(a) `sumto(0)` executes `beqz` and `ret`, 2 instructions. Any other call executes all 12 instructions plus the inner call, so $I(n) = 12 + I(n-1)$, giving $I(n) = 12n + 2$. For $n$ = 100 that is **1202**. Each of the $n$ non-base activations holds a 16-byte frame at the deepest point, so the depth is $16n$ = **1600** bytes.

(b) The loop executes `li` and `beqz` (2), then three instructions per step (3n), then `mv` and `ret` (2): $3n + 4$ = **304** for $n$ = 100. The ratio is 1202/304 = **3.954**. The recursive version also touches 1.6 KB of stack, which the loop does not.

(c) $16n \le 8192$ gives $n \le$ **512**. Any larger $n$ overflows the stack and overwrites whatever lies below it, often silently on a microcontroller without memory protection. This is one reason embedded coding standards discourage recursion.

### Solution 14-03.9

From Example 14-03.4 with $F(21)$ = 10,946:

- calls $= 2F(21) - 1$ = **21891**;
- instructions $= 21F(21) - 18$ = **229848**;
- stack depth $= 16(n - 1)$ = **304** bytes.

The iterative version executes 3 instructions before the loop, 5 per step, then `mv` and `ret`: $5n + 5$ = **105** for $n$ = 20. The ratio is 229848/105 = **2189**. The recursive algorithm recomputes the same values exponentially many times. No compiler optimization recovers that; the algorithm has to change.

### Solution 14-03.10

(a) `{ char a; double b; char c; int d; }`: `a` at 0, `b` at 8 (8-aligned), `c` at 16, and `d` at 20 (4-aligned), ending at 24. The size is **24** bytes. Reordered as `{ double b; int d; char a; char c; }`: offsets 0, 8, 12 and 13, ending at 14, rounded up to a multiple of 8: **16** bytes.

(b) `{ short s; char c[3]; }`: `s` at 0, then the array (alignment 1) at 2, ending at 5. The largest alignment is 2, so the size is **6** bytes.

(c) `{ char *p; char c; }`: under ILP32 the pointer is 4 bytes, so `c` sits at 4, ending at 5, rounded to **8**. Under LP64 the pointer is 8 bytes, so `c` sits at 8, ending at 9, rounded to **16**. The same source has different layouts on 32- and 64-bit systems. That is harmless inside one program, but fatal if the bytes are written to a file or a network and read back by the other kind of system.

### Solution 14-03.11

(a) `b.o`'s `.text` begins at 0x10000 + 40 = 0x10028, so `g` is at 0x10028 + 8 = **0x00010030**. The AUIPC is at 0x10010, so the offset is 0x20 = 32. That splits into an AUIPC immediate of **0** and a JALR immediate of **32**.

- **AUIPC:** `auipc ra, 0` has a zero U-immediate, rd = 1 and opcode 0010111: **0x00000097**.
- **JALR:** `jalr ra, 32(ra)` has imm = 32, rs1 = 1, funct3 = 000, rd = 1 and opcode 1100111: **0x020080E7**.

(b) Relaxation replaces the 8-byte pair with a 4-byte JAL. Everything after the call moves 4 bytes earlier, so `b.o` starts at 0x10024 and `g` is at **0x0001002C**. The JAL is still at 0x10010, so its offset is 0x1C = **28**. With imm[11:1] encoding 28, rd = 1 and opcode 1101111, it is **0x01C000EF**.

(c) The relaxation itself removed 4 bytes between the call and its target. A linker must therefore iterate: shrinking one call can bring other targets within range, and every offset that spans a shrunken sequence must be recomputed. The linker run by the verify script produces exactly these addresses and encodings.

### Solution 14-03.12

(a) Saving a temporary means one `sw` before and one `lw` after each call: 2 × 100 = **200** extra instructions.

(b) In s0, the value survives the calls by the callee's guarantee. The function itself saves s0 once in its prologue and restores it once in its epilogue: **2** extra instructions, however many calls it makes.

(c) As a leaf, `h` can use three temporaries for free. If it used three saved registers instead, it would need a frame: an `addi` to allocate it, three `sw`, three `lw` and an `addi` to release it, which is **8** extra instructions per call, or 800 over the loop.

(d) Values that must survive calls are cheapest in callee-saved registers (one save for many calls), and short-lived scratch values are cheapest in caller-saved ones (no saves at all in leaf functions). Real code has both kinds, so the ABI provides both. The 12 + 15 split (excluding x0, sp, gp, tp and ra) is a compromise tuned on typical programs.

### Solution 14-03.13

(a) Count in four parts:

- The prologue (`addi`, four stores): 5.
- Each iteration: the test (`lw`, `lw`, `bge`) plus 12 body instructions (`lw` a, `lw` i, `slli`, `add`, `lw`, `lw` k, `add`, `sw`, `lw`, `addi`, `sw`, `j`): 15.
- The final test: 3.
- The epilogue: 2.

The total is $15n + 10$, which is **1510** for $n$ = 100.

(b) The pointer version takes 504, so the ratio is 1510/504 = **2.996**: about three times the instructions for the same work.

(c) The `-O0`-style loop makes **9** memory accesses per iteration (seven loads and two stores). The optimized loop makes **2** (one load, one store), both to the array itself.

(d) The extra accesses all hit the same few stack slots, which stay in the L1 cache (14-09), so each costs a few cycles rather than a trip to DRAM. They do, however, create store-to-load dependences through memory (`i` is stored and reloaded every iteration) that a pipelined core must forward or stall on (14-06). The time ratio can therefore be smaller than 3 on a core that overlaps the independent loads, or larger on a simple core where every load costs extra cycles. Never ship performance-critical code at `-O0`.

### Solution 14-03.14

(a) **Version 1:** `id` at 0, `flags` at 4, `balance` at 8; size 16. **Version 2:** `id` at 0, `region` at 4 (2 bytes, then 2 bytes of padding), `flags` at **8**, `balance` at **16** (8-aligned, after 4 bytes of padding); size **24**.

(b) The old program still uses the old offsets.

- **Reading `flags` at offset 4:** it gets the 2 bytes of `region` plus 2 bytes of padding.
- **Reading `balance` at offset 8:** it gets the new `flags` and 4 padding bytes, reinterpreted as a `double`, which is garbage.
- **Allocating the structure:** if the program allocates it itself, it reserves 16 bytes where the library writes 24, so the library overwrites adjacent memory.

Nothing reports an error; the program simply computes with wrong data.

(c) Any three of the following:

- add fields only at the end, and only to structures the library allocates;
- make structures opaque, so that callers hold only pointers and use accessor functions;
- reserve padding fields for future use;
- version the ABI explicitly: a new shared-library version number (soname) when the ABI changes, so that old programs keep loading the old library;
- version the structures themselves with a size or version field that the library checks.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-03.1a | registers to save | 4 | — |
| 14-03.1b | frame size | 16 | bytes |
| 14-03.2a | offset of a[3] | 12 | bytes |
| 14-03.2b | instructions before ret | 5 | — |
| 14-03.3a | base instructions in li a0, 100 | 1 | — |
| 14-03.3b | base instructions in li a0, 0x12345678 | 2 | — |
| 14-03.3c | base instructions in call (before linking) | 2 | — |
| 14-03.4a | frame size | 48 | bytes |
| 14-03.4b | padding | 12 | bytes |
| 14-03.5a | instructions executed | 4 | — |
| 14-03.5b | abs(−7) | 7 | — |
| 14-03.5c | abs(−2147483648) | −2147483648 | — |
| 14-03.6a | instructions for "hello" | 22 | — |
| 14-03.7a | buggy sum2(3, 4) | 26 | — |
| 14-03.7b | correct sum2(3, 4) | 16 | — |
| 14-03.7c | instructions, fixed version | 23 | — |
| 14-03.8a | recursive count, n = 100 | 1202 | instructions |
| 14-03.8b | recursive stack depth, n = 100 | 1600 | bytes |
| 14-03.8c | loop count, n = 100 | 304 | instructions |
| 14-03.8d | ratio | 3.954 | — |
| 14-03.8e | largest n with an 8 KiB stack | 512 | — |
| 14-03.9a | calls for fib(20) | 21891 | — |
| 14-03.9b | instructions for fib(20) | 229848 | — |
| 14-03.9c | stack depth for fib(20) | 304 | bytes |
| 14-03.9d | iterative count, n = 20 | 105 | instructions |
| 14-03.9e | ratio | 2189 | — |
| 14-03.10a | size of the first structure | 24 | bytes |
| 14-03.10b | size reordered | 16 | bytes |
| 14-03.10c | size of { short; char[3] } | 6 | bytes |
| 14-03.10d | { char *; char } under ILP32 | 8 | bytes |
| 14-03.10e | { char *; char } under LP64 | 16 | bytes |
| 14-03.11a | address of g, no relaxation | 0x00010030 | — |
| 14-03.11b | AUIPC immediate | 0 | — |
| 14-03.11c | JALR immediate | 32 | bytes |
| 14-03.11d | AUIPC encoding | 0x00000097 | — |
| 14-03.11e | JALR encoding | 0x020080E7 | — |
| 14-03.11f | address of g, relaxed | 0x0001002C | — |
| 14-03.11g | JAL offset | 28 | bytes |
| 14-03.11h | JAL encoding | 0x01C000EF | — |
| 14-03.12a | extra instructions, temporary | 200 | — |
| 14-03.12b | extra instructions, saved register | 2 | — |
| 14-03.12c | extra instructions per call of h with saved registers | 8 | — |
| 14-03.13a | -O0-style count, n = 100 | 1510 | instructions |
| 14-03.13b | ratio to the pointer version | 2.996 | — |
| 14-03.13c | memory accesses per iteration, -O0 style | 9 | — |
| 14-03.13d | memory accesses per iteration, optimized | 2 | — |
| 14-03.14a | version 2 offset of flags | 8 | bytes |
| 14-03.14b | version 2 offset of balance | 16 | bytes |
| 14-03.14c | version 2 size | 24 | bytes |
