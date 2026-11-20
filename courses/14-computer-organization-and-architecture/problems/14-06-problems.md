# Problems 14-06 · Pipelining and Hazards

Chapter: [14-06](../chapters/14-06-pipelining-and-hazards.md) · Worked solutions: [14-06 solutions](../solutions/14-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** the five-stage pipeline of §3.2 with forwarding from EX/MEM and MEM/WB, register-file write-before-read, a one-cycle load-use stall, and branches and jumps resolved in EX with predict-not-taken (two-cycle penalty) unless a problem says otherwise. Cycle counts start from an empty pipeline and include the cycle in which the last instruction (an EBREAK where shown) is in WB: $N + 4$ + stalls + flush cycles.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-06.1 [A]

**Fill time.** How many cycles do 1000 hazard-free instructions take on a 5-stage pipeline, and on a 10-stage one?

### Problem 14-06.2 [A]

**Spot the hazards.** For this sequence, find every data dependence, say how each is resolved (which forwarding path, or a stall), and count the cycles:

```asm
_start:
    li   x10, 0x2000
    lw   x5, 0(x10)
    add  x6, x5, x5
    sub  x7, x6, x5
    sw   x7, 4(x10)
    ebreak
```

### Problem 14-06.3 [A]

**Unbalanced stages.** A datapath's logic is split into five stages of 200, 150, 250, 300 and 100 ps, and each pipeline register adds 30 ps. Find the clock period and the speedup limit over a single-cycle design of the same logic (one register's overhead).

### Problem 14-06.4 [B]

**Rebalancing.** In Problem 14-06.3, the 300 ps stage is split into two stages of 150 ps. Find the new clock period and speedup limit. What new cost might the extra stage bring?

### Problem 14-06.5 [B]

**Forwarding priority.** Trace

```asm
_start:
    li   x5, 3
    li   x5, 10
    add  x6, x5, x5
    ebreak
```

through the pipeline. What value does x6 receive? What would it receive if the forwarding unit preferred MEM/WB over EX/MEM?

### Problem 14-06.6 [B]

**Scheduling two loads.** Count the load-use stalls in (a), then reorder the instructions without changing the results to remove them all, as in (b):

```asm
_start:                      # (a)
    li   x10, 0x2000
    lw   x5, 0(x10)
    add  x6, x5, x5
    lw   x7, 4(x10)
    add  x8, x7, x6
    ebreak
```

```asm
_start:                      # (b)
    li   x10, 0x2000
    lw   x5, 0(x10)
    lw   x7, 4(x10)
    add  x6, x5, x5
    add  x8, x7, x6
    ebreak
```

### Problem 14-06.7 [B]

**The cost of branches.** A workload has 20% conditional branches, 60% of them taken, and 5% unconditional jumps (JAL and JALR), and no other stalls. Find the CPI with branches and jumps resolved in EX (penalty 2) and in ID (penalty 1).

### Problem 14-06.8 [B]

**One memory port.** A pipeline uses a single-ported unified memory for instructions and data. Each load or store, in MEM, blocks the instruction fetch in IF for one cycle. With 35% loads and stores and no other stalls, what is the CPI?

### Problem 14-06.9 [B]

**A slow divider.** An integer divider occupies EX for 20 cycles and is not pipelined, so the instructions behind a division wait. How many stall cycles does each division cause, and what is the CPI if 1% of instructions are divisions (and there are no other stalls)?

### Problem 14-06.10 [C]

**A bigger run.** The lab program with `fib(15)` instead of `fib(10)` executes 20782 instructions including the EBREAK. Using the model of §3.5 and the counts from the simulator (load-use stalls $S$ and taken branches and jumps $T$, which the verify script obtains from the trace), find the cycles and CPI on the pipelined core. Explain why the CPI is close to that of the `fib(10)` run.

### Problem 14-06.11 [C]

**How deep?** Model the time per instruction as $t(k) = (t_{\text{logic}}/k + t_{\text{reg}})(1 + ck)$ with $t_{\text{logic}}$ = 1000 ps, $t_{\text{reg}}$ = 50 ps and $c$ = 0.1. (a) Derive $k^*$ and evaluate it. (b) Find the best integer depth and its time per instruction. (c) What do the terms $t_{\text{reg}}$ and $c$ represent physically?

### Problem 14-06.12 [C]

**Resolving branches in ID.** Moving the branch comparison into ID cuts the taken penalty to one cycle, but a branch that depends on the instruction just before it must now stall one cycle (that result is ready only at the end of EX). Compare cycles per element of the array-sum loop with EX and ID resolution, (a) for the rotated loop, where `bne` immediately follows `addi a1, a1, -1`, and (b) for the scheduled loop of Example 14-06.5(c). Assume the one load-use stall in (a) is unchanged.

---

## Objective coverage

| Learning objective (chapter 14-06) | Problems |
|---|---|
| 1. Pipelined cycles, clock, speedup | 1, 3, 4, 11 |
| 2. The five-stage pipeline | 2, 5, 8 |
| 3. Data hazards, forwarding, load-use | 2, 5, 6 |
| 4. Control hazards and penalties | 7, 12 |
| 5. Cycle-count model and the Verilog core | 2, 6, 9, 10 |
