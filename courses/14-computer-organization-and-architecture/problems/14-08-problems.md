# Problems 14-08 · Out-of-Order and Superscalar Execution

Chapter: [14-08](../chapters/14-08-out-of-order-and-superscalar.md) · Worked solutions: [14-08 solutions](../solutions/14-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- **Latencies:** 1 cycle for ALU operations, branches and stores; 3 for loads (cache hits) and multiplies; 20 for divides.
- **Counting dependences:**
  - a RAW pair links each source to the most recent earlier writer of that register;
  - a WAR pair links each source to the next later writer of that register;
  - a WAW pair links consecutive writers of the same register.
- **"The model"** is the lab's trace-driven scheduler (chapter §3.5), run on the course simulator's instruction traces:
  - "4-wide out-of-order" means width 4 with a 64-entry window;
  - "8-wide" means width 8 with a 256-entry window;
  - perfect branch prediction unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-08.1 [A]

**Naming the dependence.** For each pair (first instruction, then second), name the dependence, if any, and say whether renaming removes it. Assume a0 is not changed in between.

(a) `add t0, t1, t2` then `sub t3, t0, t4`
(b) `add t0, t1, t2` then `addi t1, t5, 1`
(c) `lw t0, 0(a0)` then `li t0, 7`
(d) `sw t1, 0(a0)` then `lw t2, 0(a0)`
(e) `sw t1, 0(a0)` then `lw t2, 8(a0)`

### Problem 14-08.2 [A]

**Chains and trees.** Four words are loaded into t0–t3 and summed, either as a chain, `((t0 + t1) + t2) + t3`, or as a tree, `(t0 + t1) + (t2 + t3)`. Each version has 7 instructions. Find each version's critical path and the highest IPC it allows. Then give both critical paths for 64 words, summed as a chain and as a balanced tree.

### Problem 14-08.3 [A]

**Little's law.** (a) How many window entries does a 6-wide core need to keep issuing through a 40-cycle level-3 cache hit? (b) What latency can a 512-entry reorder buffer cover at 8 instructions per cycle? (c) A core with a 128-entry window meets a 100-cycle miss that everything behind it depends on. Roughly what IPC can it sustain while the miss is outstanding?

### Problem 14-08.4 [A]

**Precise exceptions.** The reorder buffer holds I10 to I20, with I10 the oldest. I11 has not finished yet; I12 and I17 have finished. I14, a load, raises a page fault. (a) Which instructions retire? (b) How many are squashed, and does I17's result ever become visible? (c) What must happen to the register map table?

### Problem 14-08.5 [B]

**Renaming by hand.** The map table holds x5 → p5, x6 → p6, x7 → p7 and x8 → p8, and the free list is p32, p33, p34, …. Consider:

```text
I1: add  x5, x6, x7
I2: lw   x6, 0(x5)
I3: add  x5, x6, x8
I4: sw   x5, 4(x6)
I5: addi x6, x6, 4
```

(a) Count the RAW, WAR and WAW dependences. (b) Rename the five instructions. How many new physical registers are used, and what are the final mappings of x5 and x6? (c) When can each overwritten physical register return to the free list?

### Problem 14-08.6 [B]

**Issue timelines.** Consider:

```text
I1: lw   t1, 0(a0)
I2: add  t2, t1, t1
I3: lw   t3, 4(a0)
I4: add  t4, t3, t3
I5: mul  t5, a1, a2
I6: add  t6, t5, t4
```

An instruction issues once its sources are ready, and its result is ready its latency later. I1 issues in cycle 0. Find the cycle in which the last result is ready:

- (a) on an in-order machine that issues at most one instruction per cycle, in program order;
- (b) on an out-of-order machine of unlimited width;
- (c) on the in-order machine, after a compiler reorders the code as I1, I3, I5, I2, I4, I6.

### Problem 14-08.7 [B]

**Breaking a reduction chain.** A loop multiplies together 128 words (`lw`, `mul t0, t0, t1`, and three loop-control instructions per element). (a) Explain why its critical path is 388 cycles. (b) What does the model give at 4-wide and at 8-wide? (c) The loop is rewritten with four partial products in t0, t2, t4 and t6 (four loads, four multiplies and three loop-control instructions per iteration of four elements), combined at the end as a tree, $(t_0 t_2)(t_4 t_6)$, with three multiplies. Find its critical path, its cycles at 4-wide and 8-wide, and the speedup at 4-wide. (d) Why may a compiler do this for integers but, by default, not for floating point?

### Problem 14-08.8 [B]

**Array against linked list.** Example 14-08.5 sums 100 values in a linked list. The same values stored in an array are summed by a loop of `lw`, `add`, `addi a0`, `addi a1` and `bnez`: 503 instructions. Find its critical path, its cycles and IPC on the 4-wide out-of-order core, and its speedup over the linked list on the same core, although it executes more instructions.

### Problem 14-08.9 [B]

**One register for everything.** Example 14-08.4's loop loads four elements into t1–t4. A careless compiler instead uses t1 for all four (`lw t1; add t1; sw t1`, four times per iteration), with the same 901 instructions. On the 4-wide core, what does the model give with and without renaming? Compare with the four-register version (262 and 388 cycles) and explain.

### Problem 14-08.10 [B]

**What a misprediction costs.** On the lab program (1923 instructions), the gshare predictor with a return stack mispredicts 42 control transfers. The model gives these cycle counts:

| Core | Perfect prediction | 42 mispredictions, 10-cycle refill |
|---|---|---|
| 4-wide out-of-order | 491 | 1027 |
| 8-wide out-of-order | 255 | 819 |

(a) What does each misprediction cost on each core? (b) What fraction of the 8-wide core's time is lost to mispredictions? (c) Why is each misprediction's cost more than the 10-cycle refill?

### Problem 14-08.11 [B]

**How many physical registers?** (a) A RISC-V core has a 256-entry reorder buffer. How many integer physical registers does it need so that renaming never stalls, whatever the mix in a full window? How many cover a full window if exactly 70% of its instructions write an integer register? (b) Zen 5 has 240 integer physical registers and a 448-entry ROB, and x86-64 has 16 general-purpose registers. With one thread, how many integer results can be in flight, and what fraction of the ROB is that?

### Problem 14-08.12 [C]

**A recurrence through memory.** The loop

```text
1:  lw   t1, 0(a0)
    addi t1, t1, 1
    sw   t1, 4(a0)
    addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
```

sets `a[i+1] = a[i] + 1` for 256 elements: 1538 instructions in all.

- (a) Each load reads the word the previous iteration stored. What does the chain cost per element?
- (b) Find the critical path and the model's cycles at 4-wide and 8-wide.
- (c) A compiler keeps the running value in t1 instead: one load before the loop, then `addi t1; sw t1; addi a0; addi a1; bnez`, 1283 instructions. Find its 4-wide cycles and the speedup.

### Problem 14-08.13 [C]

**Sizing the window for a divide.** A loop executes `lw`, `div t2, t1, a2`, `add t0, t0, t2` and three loop-control instructions per element, for 200 elements (1204 instructions). Each divide's result is ready about 23 cycles after its load issues. Counting one cycle from entering the window to issuing, and the dependent add, an instruction spends about $L$ = 25 cycles in the window.

- (a) Use Little's law to estimate the IPC of a 4-wide core with windows of 16, 32 and 64 entries, and the window needed for 4 instructions per cycle.
- (b) Compare the model's IPC for 16, 32, 64 and 128 entries.
- (c) The model gives an average residence time of 22.2 cycles with the 16-entry window. Show that Little's law then holds exactly, and explain why the estimate was low.

### Problem 14-08.14 [C]

**The cost of width.** Each cycle, every issue-queue entry compares each of its 2 source tags with each of the $w$ result tags broadcast that cycle. Every ALU's result must be forwardable to both inputs of every ALU. (a) How many tag comparators does a 4-wide core with a 48-entry issue queue need? An 8-wide core with 96 entries? (b) How many bypass paths connect $w$ ALUs, for $w$ = 4 and 8? (c) What does this say about doubling the width?

### Problem 14-08.15 [B]

**A Tomasulo table.** A Tomasulo-style core runs:

```asm
    lw   x1, 0(x10)     # 1
    mul  x2, x1, x3     # 2
    add  x4, x2, x5     # 3
    lw   x6, 4(x10)     # 4
    sub  x1, x6, x9     # 5
    add  x7, x1, x4     # 6
```

Rules:

- One instruction issues per cycle, in order, starting in cycle 1; reservation stations never run out.
- At issue, an instruction takes ready operands from the register file and otherwise records which instruction will produce each one (renaming).
- It starts executing in the cycle after the last of its operands appears on the common data bus (CDB), and no earlier than the cycle after it issues.
- Execution takes 2 cycles for a load, 4 for a multiply and 1 for an add or subtract. Units are pipelined and never busy.
- An instruction broadcasts its result on the CDB in the cycle after it finishes. There is one CDB: if two results are ready in the same cycle, the older instruction goes first and the other waits.

(a) Give each instruction's issue cycle, execution cycles and CDB cycle, and the total cycles. (b) Which name dependences did renaming remove? (c) With two CDBs, which broadcast moves, and does the total change?

### Problem 14-08.16 [C]

**Packing a VLIW.** A two-slot VLIW issues one bundle per cycle with one ALU/branch slot and one load/store slot. An ALU result can be used in the next bundle. A loaded value can be used two bundles later (one bundle in between). All operations in a bundle read their registers at the start of the bundle. There are no branch delay slots, so the branch must sit in the loop's last bundle. The loop is:

```asm
loop:
    lw   t0, 0(a0)
    add  a1, a1, t0
    addi a0, a0, 4
    bne  a0, a2, loop
```

(a) Schedule one iteration in as few bundles as possible. How many bundles per element? (b) Unroll by 2 (two loads, two adds, `addi a0, a0, 8`) and schedule. Adjust load offsets where a load comes after the `addi`. (c) Repeat for an unroll by 4, and find the speedup over (a). (d) What limits the speedup as unrolling grows, and what bundles-per-element does it approach?

---

## Objective coverage

| Learning objective (chapter 14-08) | Problems |
|---|---|
| 1. True and name dependences; what renaming removes | 1, 5, 9, 15 |
| 2. The dataflow limit | 2, 6, 7, 8, 12, 16 |
| 3. Renaming, the window and the reorder buffer | 4, 5, 11, 14, 15 |
| 4. Trace-driven measurement of ILP limits | 7, 8, 9, 10, 12, 13 |
| 5. Window sizing with Little's law | 3, 11, 13 |
