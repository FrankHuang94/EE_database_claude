# Problems 06-03 · Kirchhoff's Laws, Series/Parallel and Dividers

Chapter: [06-03](../chapters/06-03-kirchhoffs-laws.md) · Worked solutions: [06-03 solutions](../solutions/06-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention; resistances in ohms unless marked. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-03.1 [A]

**Counting equations.** A circuit has 4 nodes and 6 branches. (a) How many independent KCL and KVL equations does it have, and how many unknowns? (b) Why is the KCL equation of the fourth node redundant? (c) If the circuit is planar, how many meshes does it have?

### Problem 06-03.2 [A]

**Equivalent resistances.** Find: (a) 1 kΩ, 2.2 kΩ and 4.7 kΩ in series; (b) three 1 kΩ resistors in parallel; (c) 2 kΩ in parallel with 3 kΩ, the pair in series with 1.8 kΩ; (d) 10 Ω, 15 Ω and 30 Ω in parallel.

### Problem 06-03.3 [A]

**Dividers.** (a) A 5 V source drives 6.8 kΩ (top) in series with 3.3 kΩ (bottom). Find the voltage across the 3.3 kΩ resistor. (b) A 10 mA current splits between 470 Ω and 1 kΩ in parallel. Find the current in the 470 Ω resistor.

### Problem 06-03.4 [B]

**Setting a regulator's output.** A regulator holds its feedback pin at 0.800 V and its output is $V_{out} = 0.8\,(1 + R_1/R_2)$ (the feedback divider: $R_1$ from output to the pin, $R_2$ from the pin to ground, drawing negligible pin current). (a) With $R_2$ = 10.0 kΩ, what $R_1$ gives exactly 3.30 V? (b) The nearest E96 values are 30.9 kΩ and 31.6 kΩ. What output does each give? (c) With 31.6 kΩ and both resistors ±1%, find the worst-case output range. Why is the ratio's error twice each resistor's tolerance?

### Problem 06-03.5 [B]

**A meter loads a divider.** A 10 V source drives two 100 kΩ resistors in series. The voltage across the bottom one is measured with a meter whose input resistance is (a) 10 MΩ, (b) 1 MΩ. Find the reading and its error in each case.

### Problem 06-03.6 [B]

**Reduce, then expand.** A 12 V source drives $R_1$ = 2 Ω, then a parallel pair $R_2$ = 6 Ω and $R_3$ = 3 Ω, then $R_4$ = 1 Ω back to the source, all in one loop apart from the parallel pair. Find the equivalent resistance, the source current, the current in $R_2$ and $R_3$, and every resistor's power. Check the power balance.

### Problem 06-03.7 [B]

**Measuring with a bridge.** A Wheatstone bridge has $R_1$ = $R_3$ = 1.000 kΩ, an unknown $R_2$ and a decade resistance box $R_4$, with the notation of Figure 2. (a) The bridge balances with $R_4$ = 1372.5 Ω. What is $R_2$? (b) With 5 V excitation, what output would the detector see if $R_4$ were set 1 Ω above the balance value? (c) Why does the excitation's accuracy not matter at balance?

### Problem 06-03.8 [B]

**A bridge slightly out of balance.** A bridge with all arms 1.000 kΩ except $R_2$ = 1.010 kΩ is excited at 10 V. Find the exact output and the linear approximation $(V/4)(\Delta R/R)$.

### Problem 06-03.9 [B]

**Delta and wye.** (a) Convert a delta with $R_{ab}$ = 10 Ω, $R_{bc}$ = 20 Ω and $R_{ca}$ = 30 Ω to a wye. (b) Convert a wye with $R_a$ = 10 Ω, $R_b$ = 20 Ω and $R_c$ = 30 Ω to a delta. (c) Check (a) by computing the resistance between a and b in both networks with c open.

### Problem 06-03.10 [B]

**Bonding wires in parallel.** Three bonding wires of 20 mΩ, 25 mΩ and 30 mΩ connect a die pad to a package lead and together carry 6.0 A. Find each wire's current and power. Which wire is at greatest risk, and why might the current not divide this way in practice?

### Problem 06-03.11 [C]

**A dummy gauge for temperature compensation.** A strain gauge (350 Ω, gauge factor 2.0) on a structure at 500 µε also changes resistance with temperature by an apparent $\Delta R/R = 5\times10^{-4}$ for a 10 K warm-up. (a) In a quarter bridge excited at 2.5 V, find the output and the strain the system would report (assuming it divides by $V\,\text{GF}/4$). (b) An identical unstrained "dummy" gauge, at the same temperature, is placed in the adjacent arm of the same divider (top, with the active gauge at the bottom). Find the output now and compare with the output at the reference temperature. (c) Explain why the dummy works.

### Problem 06-03.12 [C]

**An R–2R ladder.** A four-bit R–2R ladder with $R$ = 10 kΩ is driven from $V_{ref}$ = 5 V: series resistors $R$ join nodes N1 to N4; each node has a 2R leg to (virtual) ground, and N4 also has a 2R termination to ground. (a) Show that the resistance looking into N1 is $R$, and find the input current. (b) Find the current in each node's 2R leg. (c) The legs of bits 3, 1 and 0 (N1, N3 and N4; code 1011) are steered into a summing node and the others to ground. What current reaches the summing node? Why does the ladder need only two resistor values?

### Problem 06-03.13 [C]

**Another unbalanced bridge.** A source connects between nodes a and b of a bridge network with $R_{ac}$ = 6 Ω, $R_{ad}$ = 12 Ω, $R_{cd}$ = 6 Ω, $R_{cb}$ = 12 Ω and $R_{db}$ = 6 Ω. (a) Find the equivalent resistance between a and b by a delta–wye conversion. (b) If the source delivers 1.0 A, find the current in $R_{cd}$ and its direction.

### Problem 06-03.14 [B]

**Combining sources.** (a) How many 1.5 V cells in series give at least 7 V, and what voltage do they give? (b) Current sources of 2 mA, −0.5 mA and 1 mA (all referenced into the same node) are in parallel. What single source replaces them? (c) Two 6 V sources, each with 1 Ω internal resistance, are connected in parallel. What single practical source replaces them?

---

## Objective coverage

| Learning objective (chapter 06-03) | Problems |
|---|---|
| 1. KCL and KVL, independent equations | 1, 6 |
| 2. Series and parallel combination | 2, 6, 10, 12, 14 |
| 3. Dividers and loading | 3, 4, 5 |
| 4. The Wheatstone bridge | 7, 8, 11 |
| 5. Delta–wye transformation | 9, 13 |
