# Problems 14-03 · Assembly and the Compilation Stack

Chapter: [14-03](../chapters/14-03-assembly-and-the-compilation-stack.md) · Worked solutions: [14-03 solutions](../solutions/14-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** RV32I with the standard calling convention and the ILP32 ABI (§3.1, §3.5). Instruction counts include every instruction from a function's first instruction through its final `ret`, and treat each `call` as a single JAL (the linker has relaxed it), unless a problem says otherwise. Frame sizes are rounded up to the 16-byte stack alignment.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution. You can check any listing by running it in the lab's simulator.

---

## Problems

### Problem 14-03.1 [A]

**Who saves what?** A function keeps three values that it needs after calls in s0, s1 and s2, uses t0–t2 for short-lived temporaries, calls other functions, and has no local variables in memory. (a) Which registers must its prologue save? (b) What is its frame size?

### Problem 14-03.2 [A]

**Array access.** Translate `x = a[3] + a[i];` with `a` in a0, `i` in a1 and `x` returned in a0. What offset does the access to `a[3]` use, and how many instructions does your translation take, not counting `ret`?

### Problem 14-03.3 [A]

**Pseudo-instructions.** Give the base instructions for each: `li a0, 100`; `li a0, 0x12345678`; `not a0, a1`; `neg a0, a1`; `seqz a0, a1`; `bgt a0, a1, L`; `ret`; and `call f` as the assembler emits it. How many base instructions does each of `li a0, 100`, `li a0, 0x12345678` and `call f` occupy?

### Problem 14-03.4 [A]

**Sizing a frame.** A non-leaf function saves ra, s0 and s1 and needs a local array `int buf[6]` on the stack. Find its minimum frame size and the bytes of padding the alignment rule adds.

### Problem 14-03.5 [B]

**Absolute value without a branch.** Show that

```asm
abs:
    srai t0, a0, 31
    xor  a0, a0, t0
    sub  a0, a0, t0
    ret
```

computes $\lvert a \rvert$. How many instructions does it execute (including `ret`)? What does it return for −7, and for −2,147,483,648? Explain the second result.

### Problem 14-03.6 [B]

**A string loop.** This function returns the length of a zero-terminated string:

```asm
strlen:
    mv   t0, a0
1:  lbu  t1, 0(t0)
    addi t0, t0, 1
    bnez t1, 1b
    sub  a0, t0, a0
    addi a0, a0, -1
    ret
```

(a) Explain why the final `addi` is needed. (b) Find the number of instructions it executes for a string of length $L$, and for `"hello"`.

### Problem 14-03.7 [B]

**Find the bug.** `g` computes $2x + 1$ using temporaries. `sum2` is meant to return `g(x) + g(y)`:

```asm
g:
    slli t0, a0, 1
    addi t1, t0, 1
    mv   a0, t1
    ret

sum2:
    addi sp, sp, -16
    sw   ra, 12(sp)
    mv   t0, a1           # keep y
    call g                # a0 = g(x)
    mv   t1, a0           # keep g(x)
    mv   a0, t0
    call g                # a0 = g(y)
    add  a0, t1, a0
    lw   ra, 12(sp)
    addi sp, sp, 16
    ret
```

(a) What does `sum2(3, 4)` return, and what should it return? (b) Explain the bug and write a correct version. (c) How many instructions does your correct version execute for `sum2(3, 4)`, including those in `g`?

### Problem 14-03.8 [B]

**Recursion against iteration.** A recursive sum:

```asm
sumto:                    # int sumto(int n) { return n == 0 ? 0 : n + sumto(n - 1); }
    beqz a0, 1f
    addi sp, sp, -16
    sw   ra, 12(sp)
    sw   s0, 8(sp)
    mv   s0, a0
    addi a0, a0, -1
    call sumto
    add  a0, a0, s0
    lw   ra, 12(sp)
    lw   s0, 8(sp)
    addi sp, sp, 16
1:  ret
```

(a) Find the instruction count $I(n)$ and the maximum stack depth for `sumto(n)`, and evaluate both for $n$ = 100. (b) A loop version is

```asm
sumto_loop:
    li   t0, 0
    beqz a0, 2f
1:  add  t0, t0, a0
    addi a0, a0, -1
    bnez a0, 1b
2:  mv   a0, t0
    ret
```

Find its count for $n$ = 100 and the ratio of the two. (c) The function runs in a thread with an 8 KiB stack. What is the largest $n$ the recursive version can handle?

### Problem 14-03.9 [B]

**Fibonacci, two ways.** For the recursive `fib` of Example 14-03.4, find the number of calls, the instructions and the stack depth for `fib(20)`. An iterative version is

```asm
fibi:
    li   t0, 0
    li   t1, 1
    beqz a0, 2f
1:  add  t2, t0, t1
    mv   t0, t1
    mv   t1, t2
    addi a0, a0, -1
    bnez a0, 1b
2:  mv   a0, t0
    ret
```

Find its count for $n$ = 20 and the ratio of the recursive count to it.

### Problem 14-03.10 [B]

**Structure layouts.** Under ILP32 find the size of (a) `struct { char a; double b; char c; int d; }` and of the same members reordered to minimize size; (b) `struct { short s; char c[3]; }`; (c) `struct { char *p; char c; }` under ILP32 and under LP64.

### Problem 14-03.11 [B]

**Linking by hand.** File `a.o` has a 40-byte `.text` section containing `call g`, whose AUIPC is at offset 0x10. File `b.o` has a `.text` section in which `g` starts at offset 8. The linker places `a.o`'s `.text` at 0x10000, immediately followed by `b.o`'s. (a) Without relaxation, find the address of `g`, the AUIPC and JALR immediates, and both encodings. (b) With relaxation (this is the only call), find the new address of `g`, the JAL offset and its encoding. (c) Why did the offset change?

### Problem 14-03.12 [C]

**Why two kinds of register?** A function runs a loop that calls a leaf function `h` 100 times; one value must survive every call. (a) If the value lives in a temporary, the caller must save and restore it around each call. How many extra instructions is that? (b) If it lives in s0, how many extra instructions does the function execute? (c) Now suppose `h` itself needs three scratch registers. Compare the costs to `h` of using temporaries and of using saved registers. (d) What does this say about why ABIs provide both kinds?

### Problem 14-03.13 [C]

**What `-O0` costs.** Unoptimized compilers keep every variable in a stack slot so that a debugger can always find it. A translation of the increment loop in that style is:

```asm
inc_o0:
    addi sp, sp, -32
    sw   a0, 28(sp)       # a
    sw   a1, 24(sp)       # n
    sw   a2, 20(sp)       # k
    sw   zero, 16(sp)     # i = 0
1:  lw   t0, 16(sp)       # i
    lw   t1, 24(sp)       # n
    bge  t0, t1, 2f
    lw   t0, 28(sp)       # a
    lw   t1, 16(sp)       # i
    slli t1, t1, 2
    add  t0, t0, t1       # &a[i]
    lw   t1, 0(t0)
    lw   t2, 20(sp)       # k
    add  t1, t1, t2
    sw   t1, 0(t0)        # a[i] += k
    lw   t0, 16(sp)
    addi t0, t0, 1
    sw   t0, 16(sp)       # i++
    j    1b
2:  addi sp, sp, 32
    ret
```

(a) Find its instruction count for $n$ elements and for $n$ = 100. (b) Compare with the pointer version of Example 14-03.2. (c) How many memory accesses does each iteration make in each version? (d) Why might the gap in *time* be larger or smaller than the gap in instruction count?

### Problem 14-03.14 [C]

**An ABI break.** Version 1 of a shared library exports `struct account { int id; int flags; double balance; };` and functions that take pointers to it. Version 2 inserts `short region;` after `id`. (a) Give the offsets and size of the structure in both versions under ILP32. (b) A program compiled against version 1 runs with version 2 of the library. What does it read when it reads `flags` and `balance` from a structure the library filled in? (c) Name three ways library designers avoid this problem.

---

## Objective coverage

| Learning objective (chapter 14-03) | Problems |
|---|---|
| 1. Translate C into RV32I and back | 2, 3, 5, 6 |
| 2. Calling convention, frames, recursion | 1, 4, 7, 8, 9, 12 |
| 3. Compiler, assembler, linker, loader; relocations | 3, 11 |
| 4. ABIs and structure layout | 10, 14 |
| 5. Instruction counts and the iron law | 6, 8, 9, 13 |
