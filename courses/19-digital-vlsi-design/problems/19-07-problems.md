# Problems 19-07 · Sequential Circuits, Timing and Clocking

Chapter: [19-07](../chapters/19-07-sequential-timing-and-clocking.md) · Worked solutions: [19-07 solutions](../solutions/19-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Skew δ is the capture clock's arrival minus the launch clock's. Setup: $T_c \ge t_{pcq} + t_{pd} + t_{setup} + t_{jitter} - \delta$. Hold: $t_{ccq} + t_{cd} \ge t_{hold} + \delta$. MTBF $= e^{t_r/\tau}/(T_0f_{clk}f_{data})$. A year is 365.25 days. Problems marked *(lab)* can be checked with `labs/19-07-lab/timing.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-07.1 [A]

**Maximum frequency.** Flip-flops have $t_{pcq}$ = 40 ps and $t_{setup}$ = 25 ps, and the slowest path has 500 ps of logic. Find the minimum period and maximum frequency with an ideal clock.

### Problem 19-07.2 [A]

**Back-to-back flip-flops.** Two flip-flops are connected directly ($t_{cd}$ = 0) with $t_{ccq}$ = 30 ps and $t_{hold}$ = 10 ps. (a) What is the hold slack with no skew? (b) How much positive skew would cause a violation?

### Problem 19-07.3 [A]

**Overhead in FO4.** A design's sequencing overhead and clock uncertainty total 60 ps in a process whose FO4 delay is 15 ps. (a) How many FO4 is the overhead? (b) What fraction of a 20-FO4 cycle is it?

### Problem 19-07.4 [B]

**A skew window.** A path has $t_{pcq}$ = 35 ps, $t_{pd}$ = 600 ps, $t_{setup}$ = 30 ps, $t_{ccq}$ = 25 ps, $t_{cd}$ = 40 ps and $t_{hold}$ = 20 ps, with $T_c$ = 700 ps. Find the range of skew that meets both constraints.

### Problem 19-07.5 [B]

**A cycle budget.** A 400 ps cycle carries 70 ps of flip-flop overhead, 15 ps of jitter and up to 20 ps of adverse skew. How much logic fits?

### Problem 19-07.6 [B]

**Pipelining to a target.** A function has 1200 ps of logic and each stage adds 50 ps of overhead. What is the fewest stages that reach 4 GHz, and what is the latency?

### Problem 19-07.7 [B]

**Overhead share.** For Problem 6's pipeline, what fraction of each cycle is overhead, and what throughput would 12 stages give?

### Problem 19-07.8 [B]

**Borrowing.** A two-phase latch design has $T_c$ = 400 ps (50% duty), latch $t_{setup}$ = 15 ps and $t_{pdq}$ = 20 ps. (a) What is the maximum a half-cycle may borrow? (b) The half-cycles carry 260 ps and 90 ps of logic. Does the loop meet timing, and how much does the first half borrow?

### Problem 19-07.9 [B]

**A latch's time constant.** A latch's storage nodes have 5 fF each and the cross-coupled inverters have $g_m$ = 200 µS at their switching point. (a) Find τ. (b) How much longer does it take to resolve from a 10 µV imbalance than from 10 mV?

### Problem 19-07.10 [B] *(lab)*

**A synchronizer target.** A synchronizer flip-flop has τ = 15 ps and $T_0$ = 10 ps; the clock is 2 GHz and data change at 50 MHz. (a) With a two-flip-flop synchronizer giving 450 ps to resolve, what is the MTBF? (b) What resolution time would give 10 years? (c) What MTBF does a third flip-flop (950 ps) give?

### Problem 19-07.11 [C]

**Optimal pipeline depth with hazards.** Suppose each instruction's average time is $T_c(1 + bN)$, where the term $bN$ models stalls whose cost grows with depth. (a) With $T_c = t_L/N + t_o$, show that the optimal depth is $N_{opt} = \sqrt{t_L/(bt_o)}$. (b) For $t_L$ = 2000 ps, $t_o$ = 60 ps and $b$ = 0.1, find $N_{opt}$, the best integer depth and the time per instruction, and compare with no pipelining.

### Problem 19-07.12 [C]

**Resolving faster.** (a) Derive τ = C/g_m for a cross-coupled pair of identical inverters near their switching point, and show that for square-law devices with λ = 0, $g_m = 2kV_{ov}$. (b) What is τ for the lab's pair if both inverters are made twice as wide while each node keeps 10 fF? (c) What happens to τ if, instead, the node capacitance is entirely the inverters' own gate and drain capacitance, which doubles with width?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Timing parameters of latches and flip-flops | 2, 9 |
| 2. Setup and hold with skew and jitter | 1, 2, 4, 5 |
| 3. Sequencing overhead and pipelining | 3, 6, 7, 11 |
| 4. Time borrowing | 8 |
| 5. Metastability and synchronizers | 9, 10, 12 |
