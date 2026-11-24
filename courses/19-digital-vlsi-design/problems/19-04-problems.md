# Problems 19-04 · Transistor Sizing and Logical Effort

Chapter: [19-04](../chapters/19-04-sizing-and-logical-effort.md) · Worked solutions: [19-04 solutions](../solutions/19-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $\mu$ = 2 and $p_{inv}$ = 1, so NAND-$n$ has $g = (n+2)/3$, NOR-$n$ has $g = (2n+1)/3$, and both have $p = n$. Delays are in units of τ unless stated. Capacitances are in units of the unit inverter's input capacitance. Problems marked *(lab)* can be checked with `labs/19-04-lab/effort.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-04.1 [A]

**Fan-out-of-3 delays.** Find the delay of a NAND3, a NOR3 and a NAND4, each driving three copies of itself.

### Problem 19-04.2 [A]

**A short path.** An inverter drives a NAND2, which drives an inverter; the load is 12 times the first inverter's input capacitance and there is no branching. Find $G$, $F$, the best stage effort and the minimum delay.

### Problem 19-04.3 [A]

**Branching.** A gate's output drives the next gate on the path and two identical copies of it elsewhere. (a) What is its branching effort? (b) What is it if, in addition, a wire with the capacitance of one such input hangs on the output?

### Problem 19-04.4 [B]

**Sizing a path.** A NAND3 with input capacitance 6 drives a NOR2, which drives an inverter loaded by 120. Find $G$, $F$, $\hat f$, the minimum delay and each gate's input capacitance.

### Problem 19-04.5 [B] *(lab)*

**A clock buffer.** A unit inverter with 3 fF of input capacitance must drive a 2 pF clock net. With τ = 15 ps, find the best number of stages, the delays with four, five and six stages, and the minimum delay in picoseconds.

### Problem 19-04.6 [B]

**Adding inverters.** A NAND2 with input capacitance 1 drives a load of 50. Find the delay (a) as is, (b) with one inverter added (if the polarity can be absorbed elsewhere), and (c) with two inverters added. What stage effort does (c) use?

### Problem 19-04.7 [B]

**Equal sizes are not optimal.** Three unit inverters in a chain drive a load of 64. What is the delay, and how does it compare with Example 19-04.2's optimally sized chain?

### Problem 19-04.8 [B]

**Calibrating τ.** In a new process, a simulated inverter in a chain of FO4 inverters has a delay of 22 ps. Taking $p_{inv}$ = 1, find τ, and predict the FO4 delay of a NAND2 and the minimum delay of Example 19-04.3's path. Then find τ with $p_{inv}$ = 0.5 and the percentage difference between the two calibrations.

### Problem 19-04.9 [B]

**Two ways to make OR2.** A 2-input OR must drive a load 10 times its input capacitance. Compare (a) a NOR2 followed by an inverter with (b) an inverter on each input followed by a NAND2 (De Morgan), each optimally sized.

### Problem 19-04.10 [C]

**The best stage effort.** (a) Derive $\rho(\ln\rho - 1) = p_{inv}$ by minimizing the delay of an $N$-stage inverter chain over $N$. (b) Show that at the optimum the delay per unit of $\ln F$ equals ρ. (c) Find ρ for $p_{inv}$ = 0.5. *(lab)*

### Problem 19-04.11 [C]

**Area against delay.** For the chain of Example 19-04.2 ($H$ = 64), compare two, three and four stages by delay and by total inverter input capacitance (a proxy for area and switching energy). What does a designer give up by choosing two stages?

### Problem 19-04.12 [C] *(lab)*

**When does the tree win?** Repeat Example 19-04.6 for $H$ = 1 and $H$ = 100. Which topology is best in each case, and why does the answer change with the load?

### Problem 19-04.13 [B]

**Efforts of complex gates.** Size each gate for unit drive (the same pull-down and pull-up resistance as a unit inverter with an NMOS of width 1). (a) With μ = 2, derive the logical effort of each input and the parasitic delay of an AOI22, $F = \overline{AB + CD}$, with the pull-up's parallel pair C, D next to the output. (b) Repeat §3.2's AOI21 and part (a) with μ = 2.5. (c) Which efforts changed, and why did the AOI21's A and B inputs not?

### Problem 19-04.14 [B]

**Skewed gates.** (a) A LO-skew inverter keeps the unit NMOS (width 1) and halves the PMOS to width 1 (μ = 2). Find its rising, falling and average logical efforts. (b) A HI-skew NAND2 keeps the unit PMOS (width 2 each) and halves each series NMOS to width 1. Find the same three efforts. (c) After a domino gate (19-03), a HI-skew inverter is used rather than a LO-skew one. Explain why, from which output edge the evaluation needs.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Derive $d = gh + p$; efforts of common gates | 1, 8, 13, 14 |
| 2. Path efforts and the minimum delay | 2, 3, 4, 7 |
| 3. Size the gates on a path | 4, 7 |
| 4. Best stage effort and number of stages | 5, 6, 10, 11 |
| 5. Compare topologies; limits and calibration | 8, 9, 12 |
