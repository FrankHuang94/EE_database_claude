# Problems 08-04 · Combinational Building Blocks

Chapter: [08-04](../chapters/08-04-combinational-building-blocks.md) · Worked solutions: [08-04 solutions](../solutions/08-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** multiplexer data input $D_i$ is selected when the select lines, most significant first, spell $i$. "Unit delay" means every gate (AND, OR, XOR, NAND, NOR, of any number of inputs) and every inverter takes 1 unit. Numbers are two's complement unless called unsigned. Transistor counts are for static CMOS: $2k$ for a $k$-input NAND or NOR, 2 for an inverter, and AND or OR as the inverting gate plus an inverter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-04.1 [A]

**An 8:1 multiplexer.** (a) Which data input is selected when $S_2S_1S_0 = 101$? (b) Written as a two-level sum of products, how many product terms does an 8:1 multiplexer have, and how many literals in each? (c) How many 2:1 multiplexers does a tree implementation need?

### Problem 08-04.2 [A]

**Even parity from a multiplexer.** Implement $F(A, B, C) = \sum m(0, 3, 5, 6)$ with a 4:1 multiplexer whose selects are $A$ and $B$. What goes on each data input, and how many of them are $\overline{C}$?

### Problem 08-04.3 [A]

**A 2:4 decoder with enable.** (a) Write the four output equations. (b) Which output is 1 for $E = 1$, $A_1A_0 = 10$, and which for $E = 0$? (c) Count transistors if each output is an AND3 (a NAND3 plus an inverter) and two inverters supply $\overline{A_1}$ and $\overline{A_0}$.

### Problem 08-04.4 [B]

**Building a 4:16 decoder.** (a) With two 2:4 predecoders (one for $A_3A_2$, one for $A_1A_0$), how many two-input AND gates complete a 4:16 decoder? (b) Alternatively, use 2:4 decoders with enables in a tree: one decoder on $A_3A_2$ drives the enables of the others. How many 2:4 decoders does that take? (c) Which is faster, under the unit-delay model, if a 2:4 decoder with enable is one level of AND3 gates?

### Problem 08-04.5 [B]

**An 8:3 priority encoder.** Inputs $D_7 \ldots D_0$, with $D_7$ the highest priority. (a) Write $Y_2$, $Y_1$ and $Y_0$. (b) What is the output for $D_7 \ldots D_0$ = 0101 0010? (c) How many of the 256 input patterns give the output 5?

### Problem 08-04.6 [B]

**The full adder from its truth table.** (a) Write the truth table of a full adder. (b) Minimize $C_{out}$ on a map and count literals. (c) Show that $S$ has no adjacent 1s on its map, and count the literals of its minimal SOP. (d) How many two-input gates (XOR, AND, OR) does the generate–propagate form use?

### Problem 08-04.7 [B]

**Ripple delay with real gate delays.** In an 8-bit ripple-carry adder built from generate–propagate full adders, $t_{XOR}$ = 40 ps and $t_{AND} = t_{OR}$ = 25 ps. (a) Find the delay to the most significant sum bit $S_7$. (b) Find the delay to the carry out $C_8$. (c) If the adder sits between registers that add 60 ps of overhead per cycle, what is the highest clock frequency?

### Problem 08-04.8 [B]

**Eight-bit add/subtract.** For each operation give the 8-bit result as a signed number, the carry out $C_8$ and the overflow flag $V$: (a) $100 - 27$; (b) $-100 - 50$; (c) $50 - 100$. (d) For (c), what does $C_8$ say about the unsigned comparison of 50 and 100?

### Problem 08-04.9 [B]

**A 2-bit magnitude comparator.** Inputs $A_1A_0$ and $B_1B_0$ (unsigned). (a) Derive a minimal SOP for $\text{GT} = (A > B)$ and count its literals. (b) Write EQ using XNOR gates. (c) How do you get $\text{LT}$ with no further minimization?

### Problem 08-04.10 [B]

**ALU flags.** A 4-bit ALU adds $A$ = 1001 and $B$ = 0111. Give the result and the flags Z, N, C and V, and interpret the result both as unsigned and as signed numbers.

### Problem 08-04.11 [B]

**Set-less-than.** For 4-bit signed operands, compute $N \oplus V$ after $A - B$ for (a) $A = 3$, $B = -2$; (b) $A = -8$, $B = 7$; (c) $A = 7$, $B = -8$. Which cases overflow, and are all three comparisons still correct?

### Problem 08-04.12 [B]

**A static-1 hazard.** $F = \overline{A}B + AC$, built with an inverter on $A$, two AND gates and an OR gate, all with unit delay. (a) With $B = C = 1$, which change of $A$ produces a glitch, starting when and how wide? (b) Give the hazard-free SOP and its literal count.

### Problem 08-04.13 [C]

**A static-0 hazard.** $F = (A + B)(\overline{A} + C)$, built from an inverter, two OR gates and an AND gate, all with unit delay. (a) With $B = C = 0$ the output should stay 0. Which change of $A$ makes it glitch high, and for how long? (b) Give the hazard-free product of sums and its literal count.

### Problem 08-04.14 [C]

**A carry-select adder.** An 8-bit adder is split into a low 4-bit ripple adder and a high 4-bit half computed twice, once assuming carry in 0 and once assuming 1; 2:1 multiplexers pick the high result when the low carry out arrives. Under the unit-delay model (full adders as in §3.5, a multiplexer as 1 unit): (a) when is the final carry out of the low half ready, and when are both high-half results ready? (b) What is the total delay, against an 8-bit ripple adder? (c) How many full adders and 2:1 multiplexers does it use?

### Problem 08-04.15 [C]

**How much switching is glitches?** In the lab's unit-delay simulation of a 4-bit ripple-carry adder over all $2^{18}$ input transitions: (a) how many output transitions, on average, are *needed* per input change (the outputs whose final value changes)? Derive it without simulating. (b) The simulation counts 5.914 output transitions per input change on average. What share of all output transitions are glitches? (c) Why does this matter for a battery-powered chip, and why does a unit-delay model probably overstate it?

---

## Objective coverage

| Learning objective (chapter 08-04) | Problems |
|---|---|
| 1. Multiplexers, decoders, encoders and priority encoders | 1, 2, 3, 4, 5 |
| 2. Adders, ripple delay, add/subtract and overflow | 6, 7, 8, 14 |
| 3. Equality and magnitude comparators | 9, 11 |
| 4. ALUs and status flags | 10, 11 |
| 5. Hazards and glitches | 12, 13, 15 |
