# Problems 19-03 · Combinational Logic Families

Chapter: [19-03](../chapters/19-03-logic-families.md) · Worked solutions: [19-03 solutions](../solutions/19-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Square-law transistors with λ = 0. A unit inverter has $W_n$ = 1 and $W_p$ = 2 ($\mu$ = 2) and resistance $R$ for both edges; gates are sized for unit worst-case drive. Delays use $t_p \approx 0.69\,\tau_E$ with the Elmore constant $\tau_E$. Body effect: $V_{TN} = V_{TN0} + \gamma_B(\sqrt{2\phi_B + V_{SB}} - \sqrt{2\phi_B})$. Problems marked *(lab)* can be checked with `labs/19-03-lab/logic.py` or the netlists.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-03.1 [A]

**A complex gate.** Design the static CMOS gate for $F = \overline{A(B + C)}$. (a) Describe the pull-down and pull-up networks and count the transistors. (b) Size them for unit drive. (c) Give each input's capacitance relative to the unit inverter's.

### Problem 19-03.2 [A]

**Counting transistors.** How many transistors does a four-input NOR need in (a) static CMOS, (b) pseudo-NMOS, (c) footed dynamic logic, and (d) domino logic (the dynamic gate plus its output inverter)?

### Problem 19-03.3 [A]

**Elmore on a tree.** A source drives node 1 through $R_1$ = 1 kΩ; node 1 has $C_1$ = 10 fF and branches to node 2 (through $R_2$ = 2 kΩ, $C_2$ = 20 fF) and to node 3 (through $R_3$ = 3 kΩ, $C_3$ = 30 fF). Find the Elmore constants and the estimated delays at nodes 2 and 3.

### Problem 19-03.4 [B]

**Input ordering.** A NAND3 pull-down has three NMOS of width 3 ($R$ = 10 kΩ for the unit NMOS), 1.5 fF at each of its two internal nodes and 20 fF at the output. (a) Find the Elmore constant and delay when all internal nodes start charged. (b) Find them when the latest input drives the transistor next to the output and the other two were already on. (c) By what fraction does the ordering help?

### Problem 19-03.5 [B]

**Designing a pseudo-NMOS NOR4.** $V_{DD}$ = 1.0 V, $V_{TN} = \lvert V_{TP}\rvert$ = 0.3 V, and each pull-down NMOS has $k_n$ = 150 µA/V². (a) What is the largest load $k_p$ that keeps $V_{OL} \le$ 0.15 V with one input high? (b) What static power does the gate then draw when its output is low? (c) What is $V_{OL}$ with two inputs high?

### Problem 19-03.6 [B]

**A degraded 1.** An NMOS pass transistor with its gate at $V_{DD}$ = 1.0 V passes a 1. $V_{TN0}$ = 0.3 V, $\gamma_B$ = 0.5 V$^{1/2}$ and $2\phi_B$ = 0.7 V. (a) What level does its output reach? (b) Does the PMOS of a following inverter ($\lvert V_{TP}\rvert$ = 0.3 V) turn off?

### Problem 19-03.7 [B] *(lab)*

**Buffering a TG chain.** Sixteen transmission gates of 4 kΩ each, with 3 fF per node, form a chain; buffers have $t_{buf}$ = 25 ps. (a) Estimate the unbuffered delay. (b) Find $m_{opt}$. (c) Compare the delays with segments of 2, 4 and 8.

### Problem 19-03.8 [B]

**Charge sharing with two internal nodes.** A dynamic NAND3 has its output, 12 fF, precharged to 1.2 V, and two internal nodes of 2 fF each at 0 V. In evaluation the top two inputs are 1 and the bottom one is 0. $V_{TN}$ = 0.35 V, no body effect. (a) Find the output. (b) Repeat with a 6 fF output.

### Problem 19-03.9 [B]

**Hold time.** A dynamic node of 5 fF leaks 20 nA at the hot corner, and may droop by at most 0.15 V. (a) How long can it hold a high level? (b) If it must hold for half a clock period, what is the minimum clock frequency? (c) What does a keeper change?

### Problem 19-03.10 [C] *(lab)*

**The Elmore estimate for ladders.** (a) Show that the Elmore constant at the end of an $n$-section ladder with total resistance $R_w$ and capacitance $C_w$ is $R_wC_w(n+1)/(2n)$, and find its limit for a continuous line. (b) Using exact step responses, compare the true 50% delay with $0.69\,\tau_E$ for $n$ = 1, 4 and 12. What does the trend imply for long wires (19-05)?

### Problem 19-03.11 [C]

**Charge sharing with the body effect.** Repeat Example 19-03.6(a) and (c) (10 fF output, 1.2 V, $V_{TN0}$ = 0.35 V) with $\gamma_B$ = 0.4 V$^{1/2}$ and $2\phi_B$ = 0.8 V. (a) At what level does the top NMOS cut off? (b) What is the new boundary $C_a/C_L$? (c) What is the output with $C_a$ = 3 fF? Does the body effect help or hurt here?

### Problem 19-03.12 [C]

**A domino gate.** (a) Design a domino gate for $F = AB + C$: give the dynamic gate's pull-down network and explain why the output inverter makes $F$, not $\overline F$. (b) Count its transistors (footed) and compare with a static AOI21 followed by an inverter. (c) Why could you not build $\overline{F}$ as a single domino stage, and what is the usual remedy?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Build and size static CMOS gates | 1, 2 |
| 2. Derive and apply the Elmore delay to stacks | 3, 4, 10 |
| 3. Ratioed (pseudo-NMOS) logic | 2, 5 |
| 4. Pass transistors and transmission gates | 6, 7 |
| 5. Dynamic and domino logic | 8, 9, 11, 12 |
