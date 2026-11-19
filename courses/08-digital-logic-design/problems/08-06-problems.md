# Problems 08-06 · Latches, Flip-Flops and Sequential Timing

Chapter: [08-06](../chapters/08-06-latches-and-flip-flops.md) · Worked solutions: [08-06 solutions](../solutions/08-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $t_{pcq}$ and $t_{ccq}$ are the clock-to-Q propagation and contamination delays, $t_{pd}$ and $t_{cd}$ the logic's propagation and contamination delays. Unless stated otherwise all registers share one ideal clock (no skew). In sampled waveforms, a rising edge occurs at a sample where CLK goes from 0 to 1, and a flip-flop captures $D$'s value at that sample.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-06.1 [A]

**A NAND latch.** An $\overline{S}\,\overline{R}$ latch built from two NAND gates starts with $Q$ = 0. Its active-low inputs $(\overline{S}, \overline{R})$ take the values (0, 1), (1, 1), (1, 0), (1, 1), (0, 0). (a) Give $Q$ after each step. (b) In how many steps is $Q$ = 1? (c) In how many are both outputs 1?

### Problem 08-06.2 [A]

**Three storage elements, one waveform.** CLK = 0, 1, 1, 0, 0, 1, 1, 0 and $D$ = 1, 1, 0, 0, 1, 0, 1, 0 at $t$ = 0 to 7. A positive-level latch (transparent when CLK = 1), a negative-level latch (transparent when CLK = 0) and a rising-edge flip-flop all start with $Q$ = 0. For each, count the output transitions and give the final output.

### Problem 08-06.3 [A]

**Reading a timing violation.** A flip-flop has $t_{\text{setup}}$ = 30 ps and $t_{\text{hold}}$ = 15 ps. (a) Its $D$ input last changes 25 ps before a rising edge. What is the setup slack? (b) After the edge, $D$ next changes 20 ps after it. What is the hold slack? (c) Which constraint is violated, and what may the flip-flop do?

### Problem 08-06.4 [B]

**The critical path.** Flip-flops with $t_{pcq}$ = 80 ps and $t_{\text{setup}}$ = 50 ps bound three register-to-register paths whose logic delays are 400, 650 and 520 ps. (a) Find the minimum clock period and maximum frequency. (b) What is the setup slack of each path at that period?

### Problem 08-06.5 [B]

**Hold across several paths.** Flip-flops with $t_{ccq}$ = 40 ps and $t_{\text{hold}}$ = 70 ps bound three paths whose logic contamination delays are 10, 35 and 50 ps. (a) Find each path's hold slack. How many paths violate? (b) Buffers add 12 ps of contamination delay each. How many are needed on the worst path?

### Problem 08-06.6 [B]

**Pipelining with overhead.** A block of logic has 1200 ps of delay, and each register adds 100 ps of overhead ($t_{pcq} + t_{\text{setup}}$). (a) What clock frequency does one stage allow? (b) With the logic split into 4 equal stages? (c) What is the throughput speedup, and (d) what speedup is approached as the number of stages grows without limit?

### Problem 08-06.7 [B]

**The cost of enables.** (a) Write the next-state equation of a D flip-flop with enable. (b) Built with a NAND-only 2:1 multiplexer (16 transistors, Problem 08-02.7) and a 24-transistor flip-flop, how many transistors per bit? (c) For a 32-bit register, how many multiplexer transistors would one clock-gating cell replace?

### Problem 08-06.8 [B]

**Reset timing.** The clock period is 8 ns, with rising edges at 0, 8, 16, 24, 32 ns. A reset is asserted at 13 ns and released at 29.5 ns. (a) When does the output reset with a synchronous reset, and with an asynchronous one? (b) For the asynchronous case, the recovery time is 1 ns. How much margin is there before the next edge?

### Problem 08-06.9 [B]

**A board-level path.** Two SN74LVC74A flip-flops at 3.3 V ($t_{pcq}$ = 5.2 ns maximum, $t_{\text{setup}}$ = 3 ns) are connected through a gate with a maximum delay of 3.5 ns. (a) What is the minimum clock period and maximum frequency? (b) Which number would you need from the gate's datasheet to check hold, and why?

### Problem 08-06.10 [B]

**Switching thresholds.** Use the square-law expression for $V_M$ with $V_{DD}$ = 1.8 V and $V_{Tn} = |V_{Tp}|$ = 0.45 V. (a) Find $V_M$ for $\beta_n = \beta_p$. (b) Find $V_M$ for $\beta_n = 4\beta_p$. (c) Which way does a stronger nMOS move the threshold, and why?

### Problem 08-06.11 [B]

**How fast does a latch resolve?** Near $V_M$, the difference between the two nodes of a cross-coupled pair grows as $\Delta V(t) = \Delta V_0\,e^{t/\tau}$ with $\tau$ = 20 ps. Starting from $\Delta V_0$ = 1 mV, how long until $\Delta V$ = 0.9 V? How does that time change if $\Delta V_0$ = 1 µV?

### Problem 08-06.12 [C]

**Inside a flip-flop.** A master–slave flip-flop's master latch has a setup of 20 ps and a hold of 15 ps relative to its own clock; the slave's clock-to-output delay is 45 ps; and both latches see the clock 25 ps after the clock pin. (a) Find the flip-flop's setup, hold and clock-to-Q at its pins. (b) What is the width of its capture window? (c) Explain the sign of the setup time.

### Problem 08-06.13 [C]

**A first look at clock skew.** In a path with $t_{pcq}$ = 50 ps, $t_{pd}$ = 300 ps, $t_{\text{setup}}$ = 40 ps, $t_{ccq}$ = 30 ps, $t_{cd}$ = 40 ps and $t_{\text{hold}}$ = 60 ps, the receiving register's clock arrives $t_{\text{skew}}$ = 30 ps after the launching register's. (a) Derive the setup and hold constraints with skew. (b) Find the minimum period and maximum frequency. (c) Find the hold slack. What does skew do to each constraint?

### Problem 08-06.14 [C]

**Counting transistors in a flip-flop.** A transmission-gate latch uses two transmission gates and two inverters; a master–slave flip-flop uses two such latches and shares one clock inverter. (a) How many transistors is that? (b) The SKY130 `dfxtp_1` uses 24. Suggest what the extra transistors are for.

### Problem 08-06.15 [C]

**Loops without registers.** (a) Three inverters, each with a delay of 20 ps, are connected in a ring. Show that the ring oscillates, and find its period and frequency. (b) What happens with a ring of two inverters? (c) Which rule of synchronous design forbids both, and why does a register in the loop fix it?

---

## Objective coverage

| Learning objective (chapter 08-06) | Problems |
|---|---|
| 1. Feedback, bistability, SR latches | 1, 10, 11, 15 |
| 2. D latches and master–slave flip-flops | 2, 12, 14 |
| 3. Enables and resets | 7, 8 |
| 4. Setup, hold, clock-to-Q; register-to-register constraints | 3, 4, 5, 6, 9, 13 |
| 5. Synchronous design discipline | 6, 15 |
