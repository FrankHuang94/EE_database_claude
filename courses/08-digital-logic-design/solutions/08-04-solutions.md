# Solutions 08-04 · Combinational Building Blocks

Problems: [08-04 problems](../problems/08-04-problems.md) · Chapter: [08-04](../chapters/08-04-combinational-building-blocks.md). Every number below is recomputed by [verify_08_04.py](../verify/verify_08_04.py): blocks are simulated bit by bit against their specifications on every input, delays come from static timing analysis of gate netlists, and hazards from a unit-delay simulation of the gates.

---

## Solutions

### Solution 08-04.1

(a) 101₂ = 5: input **$D_5$**.

(b) One product term per data input: **8** terms. Each contains the three select literals and its data input: **4** literals, for example $S_2\overline{S_1}S_0D_5$.

(c) $2^3 - 1$ = **7** two-input multiplexers.

### Solution 08-04.2

$F$ is 1 in rows 000, 011, 101, 110: an even number of 1s. For each select value $AB$, read $F$ against $C$:

- $AB$ = 00 (rows 0, 1): 1, 0, so $D_0 = \overline{C}$;
- $AB$ = 01 (rows 2, 3): 0, 1, so $D_1 = C$;
- $AB$ = 10 (rows 4, 5): 0, 1, so $D_2 = C$;
- $AB$ = 11 (rows 6, 7): 1, 0, so $D_3 = \overline{C}$.

**2** data inputs are $\overline{C}$. (When $A \oplus B = 0$ the output is $\overline{C}$, otherwise $C$: this is $\overline{A \oplus B \oplus C}$.)

### Solution 08-04.3

(a) $Y_0 = E\,\overline{A_1}\,\overline{A_0}$, $Y_1 = E\,\overline{A_1}A_0$, $Y_2 = E\,A_1\overline{A_0}$, $Y_3 = E\,A_1A_0$.

(b) $E = 1$, $A_1A_0 = 10$: **$Y_2$**. With $E = 0$ every output is 0.

(c) Four AND3 gates at $6 + 2 = 8$ transistors each (32), and two inverters (4): **36** transistors.

### Solution 08-04.4

(a) Each of the 16 outputs is the AND of one predecoder output for $A_3A_2$ and one for $A_1A_0$: **16** AND2 gates.

(b) One 2:4 decoder on $A_3A_2$ enables one of four 2:4 decoders on $A_1A_0$: **5** decoders.

(c) With the conventions (any gate 1 unit, inverters 1 unit): predecoded, an address bit passes an inverter, a predecoder AND and the final AND2, **3** units. Tree: an address bit passes an inverter and an AND3 in the first decoder, then the AND3 of a second decoder through its enable, **3** units. They tie on delay. The predecoded version has a regular structure that suits memory layout and needs only two-input gates in the large final array; the tree loads each first-level output with a whole decoder.

### Solution 08-04.5

(a) Output bit $Y_2$ is 1 when the winner is 4 to 7, that is, when any of $D_7 \ldots D_4$ is active. $Y_1$ is 1 when the winner is 7, 6, 3 or 2. $Y_0$ is 1 when it is 7, 5, 3 or 1. Writing "the winner is $k$" as "$D_k$ and no higher input" and simplifying with T7 of 08-02:

$$
\begin{aligned}
Y_2 &= D_7 + D_6 + D_5 + D_4 ,\\
Y_1 &= D_7 + D_6 + \overline{D_5}\,\overline{D_4}\,(D_3 + D_2) ,\\
Y_0 &= D_7 + \overline{D_6}D_5 + \overline{D_6}\,\overline{D_4}D_3 + \overline{D_6}\,\overline{D_4}\,\overline{D_2}D_1 .
\end{aligned}
$$

The verify script checks these three equations against the definition on all 256 inputs.

(b) The active inputs are $D_6$, $D_4$ and $D_1$; the highest is $D_6$, so the output is **6** (110). From the equations: $Y_2 = 1$; $Y_1 = D_6 = 1$; $Y_0 = 0 + 0 + 0 + 0 = 0$ because $\overline{D_6} = 0$ kills every term.

(c) Output 5 requires $D_7 = D_6 = 0$ and $D_5 = 1$, with $D_4 \ldots D_0$ free: $2^5$ = **32** patterns.

### Solution 08-04.6

(a)

| $A$ | $B$ | $C_{in}$ | $C_{out}$ | $S$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |

(b) $C_{out}$ is the majority function: $AB + AC_{in} + BC_{in}$, **6** literals (Example 08-02.2).

(c) $S$ is 1 on rows 001, 010, 100, 111. Any two of these differ in two bits (each has an odd number of 1s), so no two are adjacent and the minimal SOP is the canonical one, 4 minterms of 3 literals: **12** literals.

(d) $P = A \oplus B$, $G = AB$, $S = P \oplus C_{in}$, $P\,C_{in}$ and $C_{out} = G + P\,C_{in}$: **5** gates (2 XOR, 2 AND, 1 OR).

### Solution 08-04.7

Column $i$'s carry out is ready at the later of two paths: through its own inputs ($t_{XOR} + t_{AND} + t_{OR}$ = 90 ps) or through its carry in ($t_{C_i} + t_{AND} + t_{OR} = t_{C_i} + 50$ ps). So $t_{C_1}$ = 90 ps, and each later carry adds 50 ps: $t_{C_7} = 90 + 6 \times 50 = 390$ ps.

(a) $t_{S_7} = \max(t_{P_7}, t_{C_7}) + t_{XOR} = 390 + 40$ = **430** ps.

(b) $t_{C_8} = 390 + 50$ = **440** ps.

(c) The cycle must cover the slowest output plus overhead: $440 + 60 = 500$ ps, so $f_{max} = 1/500\ \text{ps}$ = **2.0** GHz.

### Solution 08-04.8

Each subtraction is $A + \overline{B} + 1$ in 8 bits.

(a) $100 - 27 = 73$: result **73**, $C_8$ = **1** (no borrow), $V$ = **0**.

(b) $-100 - 50 = -150$, which is below −128. The adder computes $10011100 + 11001101 + 1 = 01101010$, which reads as **106**, with $C_8$ = **1** and $V$ = **1**: overflow, flagged (a negative minus a positive gave a positive).

(c) $50 - 100 = -50$: result **−50** (11001110), $C_8$ = **0**, $V$ = **0**.

(d) $C_8 = 0$ means a borrow: as unsigned numbers, 50 < 100.

### Solution 08-04.9

(a) GT is 1 for the input pairs with $A > B$. On a map of $A_1A_0B_1B_0$ the 1s form three prime groups: $A_1\overline{B_1}$ ($A$'s high bit wins outright), $A_1A_0\overline{B_0}$ and $A_0\overline{B_1}\,\overline{B_0}$ (high bits tie or $B$ is small, and $A$'s low bit wins):

$$
\text{GT} = A_1\overline{B_1} + A_1A_0\overline{B_0} + A_0\overline{B_1}\,\overline{B_0} ,
$$

**8** literals, confirmed minimal by the exhaustive search.

(b) $\text{EQ} = \overline{A_1 \oplus B_1}\cdot\overline{A_0 \oplus B_0}$.

(c) $\text{LT} = \overline{\text{GT} + \text{EQ}}$: one NOR gate, since exactly one of GT, EQ and LT is true.

### Solution 08-04.10

$1001 + 0111 = 1\,0000$: the 4-bit result is **0000**, with a carry out.

- $Z$ = **1** (the result is zero), $N$ = 0;
- $C$ = **1**: as unsigned numbers, $9 + 7 = 16$ does not fit in 4 bits; the result wrapped to 0;
- $V$ = **0**: as signed numbers, $-7 + 7 = 0$ is exactly right. The carries into and out of the top column are both 1.

The same bits give "overflowed" (unsigned) and "correct" (signed); which flag matters depends on how the program interprets the numbers.

### Solution 08-04.11

(a) $3 - (-2)$: $0011 + 0001 + 1 = 0101$ (+5), $N = 0$, $V = 0$, so $N \oplus V$ = **0**: $3$ is not less than $-2$ ✓.

(b) $-8 - 7$: $1000 + 1000 + 1 = 0001$. The true difference, −15, does not fit: $V = 1$, $N = 0$, so $N \oplus V$ = **1**: $-8 < 7$ ✓.

(c) $7 - (-8)$: $0111 + 0111 + 1 = 1111$. The true difference, +15, does not fit: $V = 1$, $N = 1$, so $N \oplus V$ = **0** ✓.

**2** of the three subtractions overflow, and the comparisons are all correct anyway: that is exactly what the $\oplus V$ correction is for.

### Solution 08-04.12

(a) The two product terms hand over when $A$ changes. If $A$ **falls**, $AC$ falls at $t = 1$, while $\overline{A}$ rises at $t = 1$ and $\overline{A}B$ rises only at $t = 2$. For $1 \le t < 2$ neither OR input is 1, so the output drops at $t$ = **2** for **1** unit. When $A$ rises, $\overline{A}B$ falls at $t = 2$ but $AC$ is already 1 from $t = 1$, so there is no glitch.

(b) Add the consensus term: $F = \overline{A}B + AC + BC$, **6** literals. With $B = C = 1$, $BC$ holds the output at 1 throughout.

### Solution 08-04.13

(a) The two sum terms hand over when $A$ changes. If $A$ **rises**, $A + B$ rises at $t = 1$, while $\overline{A}$ falls at $t = 1$ and $\overline{A} + C$ falls only at $t = 2$. For $1 \le t < 2$ both AND inputs are 1, so the output rises at $t$ = **2** for **1** unit: a static-0 hazard. When $A$ falls, $A + B$ falls at $t = 1$, before $\overline{A} + C$ rises at $t = 2$, so the output stays 0.

(b) Add the consensus sum term $B + C$ (the dual of T8): $F = (A + B)(\overline{A} + C)(B + C)$, **6** literals. With $B = C = 0$ it holds the output at 0 throughout.

### Solution 08-04.14

(a) The low 4-bit ripple adder's carry out is ready at $2n + 1$ = **9** units (§3.5). The two high halves start at $t = 0$, since their carry ins are constants; their sum bits settle by $2 \times 4 = 8$ units and their carry outs by **9**.

(b) At $t = 9$ the low carry out selects between the two high results through one level of multiplexers: everything is ready at **10** units. An 8-bit ripple adder's carry out takes $2 \times 8 + 1$ = **17** units, so the carry-select adder is **1.7** times faster.

(c) Three 4-bit adders: **12** full adders (against 8). Multiplexers for the four high sum bits and the carry out: **5**. Speed costs area, a trade that [08-09](../chapters/08-09-arithmetic-circuits.md) develops into adders whose delay grows with $\log_2 n$.

### Solution 08-04.15

(a) An output needs a transition only if its old and new final values differ. For independent, uniformly random old and new inputs, each sum bit is equally likely to be 0 or 1. So is the carry out: the map $(A, B, C_0) \mapsto (15 - A, 15 - B, 1 - C_0)$ turns every sum $s$ into $31 - s$, pairing each input with a carry out of 1 (sum ≥ 16) with one whose carry out is 0. So each of the 5 outputs changes with probability 1/2: **2.5** needed transitions per input change.

(b) Glitch share = $1 - 2.5/5.914$ = **57.7**%: more than half of all output transitions, under this model, are glitches.

(c) Every transition charges or discharges the capacitance of the wire and the gate inputs it drives, so glitch transitions cost energy like real ones, which matters most in always-on and battery-powered chips. A unit-delay model overstates the effect: real gates have unequal delays, and a pulse much shorter than a gate's own delay is filtered out (inertial delay) rather than passed on. Real circuits glitch less than this simulation, but long unbalanced paths such as ripple carries still glitch noticeably.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-04.1a | data input selected by 101 | 5 | — |
| 08-04.1b | product terms, 8:1 multiplexer | 8 | — |
| 08-04.1c | literals per term | 4 | — |
| 08-04.1d | 2:1 multiplexers in a tree | 7 | — |
| 08-04.2a | data inputs equal to $\overline{C}$ | 2 | — |
| 08-04.3a | output selected by $E = 1$, 10 | 2 | — |
| 08-04.3b | transistors, 2:4 decoder | 36 | — |
| 08-04.4a | AND2 gates after predecoding | 16 | — |
| 08-04.4b | 2:4 decoders in a tree | 5 | — |
| 08-04.4c | delay, predecoded | 3 | units |
| 08-04.4d | delay, tree | 3 | units |
| 08-04.5a | output for 0101 0010 | 6 | — |
| 08-04.5b | patterns giving output 5 | 32 | — |
| 08-04.6a | literals, minimal carry | 6 | — |
| 08-04.6b | literals, minimal sum | 12 | — |
| 08-04.6c | gates, generate–propagate full adder | 5 | — |
| 08-04.7a | delay to $S_7$ | 430 | ps |
| 08-04.7b | delay to $C_8$ | 440 | ps |
| 08-04.7c | maximum clock frequency | 2.0 | GHz |
| 08-04.8a | $100 - 27$, result | 73 | — |
| 08-04.8b | $100 - 27$, carry out | 1 | — |
| 08-04.8c | $100 - 27$, overflow | 0 | — |
| 08-04.8d | $-100 - 50$, result | 106 | — |
| 08-04.8e | $-100 - 50$, carry out | 1 | — |
| 08-04.8f | $-100 - 50$, overflow | 1 | — |
| 08-04.8g | $50 - 100$, result | -50 | — |
| 08-04.8h | $50 - 100$, carry out | 0 | — |
| 08-04.8i | $50 - 100$, overflow | 0 | — |
| 08-04.9a | literals, minimal GT | 8 | — |
| 08-04.10a | result of 1001 + 0111 | 0 | — |
| 08-04.10b | Z flag | 1 | — |
| 08-04.10c | C flag | 1 | — |
| 08-04.10d | V flag | 0 | — |
| 08-04.11a | $N \oplus V$ for $3 - (-2)$ | 0 | — |
| 08-04.11b | $N \oplus V$ for $-8 - 7$ | 1 | — |
| 08-04.11c | $N \oplus V$ for $7 - (-8)$ | 0 | — |
| 08-04.11d | subtractions that overflow | 2 | — |
| 08-04.12a | glitch start | 2 | units |
| 08-04.12b | glitch width | 1 | units |
| 08-04.12c | literals, hazard-free SOP | 6 | — |
| 08-04.13a | glitch width, static-0 | 1 | units |
| 08-04.13b | literals, hazard-free POS | 6 | — |
| 08-04.13c | glitch start, static-0 | 2 | units |
| 08-04.14a | low-half carry out ready | 9 | units |
| 08-04.14b | high halves ready | 9 | units |
| 08-04.14c | carry-select total delay | 10 | units |
| 08-04.14d | 8-bit ripple total delay | 17 | units |
| 08-04.14e | full adders, carry-select | 12 | — |
| 08-04.14f | multiplexers, carry-select | 5 | — |
| 08-04.14g | speed-up over the ripple adder | 1.7 | — |
| 08-04.15a | needed output transitions per input change | 2.5 | — |
| 08-04.15b | share of output transitions that are glitches | 57.7 | % |
