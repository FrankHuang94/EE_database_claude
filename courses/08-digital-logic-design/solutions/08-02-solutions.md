# Solutions 08-02 · Boolean Algebra and Logic Gates

Problems: [08-02 problems](../problems/08-02-problems.md) · Chapter: [08-02](../chapters/08-02-boolean-algebra-and-gates.md). Every number below is recomputed by [verify_08_02.py](../verify/verify_08_02.py): functions are evaluated row by row, minimal literal counts come from an exhaustive search over all product terms, minimal gate counts from an exhaustive search over gate circuits, completeness from the closure of the gates under composition, and CMOS gates from a switch-network simulation.

---

## Solutions

### Solution 08-02.1

(a) Evaluate $\overline{A}B$ and $A\overline{C}$ row by row:

| Row | $A$ | $B$ | $C$ | $\overline{A}B$ | $A\overline{C}$ | $Y$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 2 | 0 | 1 | 0 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 | 1 | 0 | 1 |
| 4 | 1 | 0 | 0 | 0 | 1 | 1 |
| 5 | 1 | 0 | 1 | 0 | 0 | 0 |
| 6 | 1 | 1 | 0 | 0 | 1 | 1 |
| 7 | 1 | 1 | 1 | 0 | 0 | 0 |

(b) Bits 2, 3, 4 and 6 are set: $4 + 8 + 16 + 64$ = **92** (5C₁₆).

(c) **4** rows: $Y = \sum m(2, 3, 4, 6) = \overline{A}B\overline{C} + \overline{A}BC + A\overline{B}\,\overline{C} + AB\overline{C}$.

### Solution 08-02.2

(a) Swap $+$ with $\cdot$ (and 0 with 1, of which there are none): the dual of $A + \overline{A}B = A + B$ is $A(\overline{A} + B) = AB$, and the dual of $A(A + B) = A$ is $A + AB = A$.

(b) Two variables give $2^2$ = **4** rows:

| $A$ | $B$ | $\overline{A}B$ | $A + \overline{A}B$ | $A + B$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 |

The last two columns agree in every row.

(c)

$$
\begin{aligned}
A(\overline{A} + B) &= A\overline{A} + AB && \text{distributivity (A3)} \\
&= 0 + AB && \text{complement (A4, dual form)} \\
&= AB + 0 && \text{commutativity (A2)} \\
&= AB && \text{identity (A1).}
\end{aligned}
$$

Each step uses an axiom directly, so the proof does not lean on any theorem whose own proof might use the result. (Proving an axiom, such as the dual distributive law, from theorems that were derived *from* it would be circular; perfect induction is the independent check for axioms.)

### Solution 08-02.3

(a) $\overline{F_1} = \overline{(A + \overline{B})C} = \overline{A + \overline{B}} + \overline{C} = \overline{A}B + \overline{C}$.

(b) $\overline{F_2} = \overline{A} + \overline{B + \overline{C}D} = \overline{A} + \overline{B}\cdot\overline{\overline{C}D} = \overline{A} + \overline{B}(C + \overline{D})$.

(c) $F_2 = 1$ needs $A = 1$ (8 of the 16 rows) and $B + \overline{C}D = 1$. With $B = 1$, all 4 combinations of $C$, $D$ qualify; with $B = 0$, only $C = 0$, $D = 1$. So **5** rows.

(d) $16 - 5$ = **11** rows.

*Check:* from (b), $\overline{A}$ alone gives 8 rows; with $A = 1$ the term $\overline{B}(C + \overline{D})$ adds the rows $B = 0$ and $(C, D) \ne (0, 1)$, three more: $8 + 3 = 11$ ✓.

### Solution 08-02.4

(a) $AB + A\overline{B} + \overline{A}B$. Copy $AB$ (T2), then combine (T6) twice: $(AB + A\overline{B}) + (AB + \overline{A}B) = A + B$. **2** literals.

(b) $(A + B)(A + \overline{B}) = A$ by the dual of T6. **1** literal.

(c) Every term contains $\overline{C}$: $\overline{C}(\overline{A}\,\overline{B} + \overline{A}B + A\overline{B} + AB)$. The bracket lists all four combinations of $A$ and $B$, so it equals 1 (combine $\overline{A}\,\overline{B} + \overline{A}B = \overline{A}$ and $A\overline{B} + AB = A$, then $\overline{A} + A = 1$). Result $\overline{C}$: **1** literal.

(d) $AB$ is the consensus of $AC$ and $B\overline{C}$ (the variable $C$ appears true in one and complemented in the other, and the rest, $A$ and $B$, form $AB$). By T8, $AB + B\overline{C} + AC = AC + B\overline{C}$: **4** literals.

(e) This is the majority function of Example 08-02.2: $AB + BC + AC$, **6** literals.

The exhaustive search over all sums of products confirms that none of these can be written with fewer literals.

### Solution 08-02.5

(a) The zeros are rows 1, 4, 5 and 6: $F = \prod M(1, 4, 5, 6) = (A + B + \overline{C})(\overline{A} + B + C)(\overline{A} + B + \overline{C})(\overline{A} + \overline{B} + C)$.

(b) $F$: bits 0, 2, 3, 7: $1 + 4 + 8 + 128$ = **141**. $\overline{F}$: the other bits, $255 - 141$ = **114**.

(c) Pairs of minterms differing in one variable: $m_0 + m_2 = \overline{A}\,\overline{C}$; $m_2 + m_3 = \overline{A}B$; $m_3 + m_7 = BC$. Two of these, $\overline{A}\,\overline{C}$ (rows 0, 2) and $BC$ (rows 3, 7), cover all four minterms: $F = \overline{A}\,\overline{C} + BC$, **4** literals. ($\overline{A}B$ is their consensus and is redundant.)

(d) $\overline{F} = \sum m(1, 4, 5, 6)$. Pairs: $m_1 + m_5 = \overline{B}C$, $m_4 + m_5 = A\overline{B}$, $m_4 + m_6 = A\overline{C}$. The cover $\overline{B}C + A\overline{C}$ takes rows 1, 5 and 4, 6, so $\overline{F} = \overline{B}C + A\overline{C}$. Complementing: $F = (B + \overline{C})(\overline{A} + C)$, **4** literals.

*Check:* multiplying out, $(B + \overline{C})(\overline{A} + C) = \overline{A}B + BC + \overline{A}\,\overline{C}$, which is the SOP of (c) plus its consensus term ✓.

### Solution 08-02.6

Write a two-input function as its four outputs $f(0,0)$, $f(0,1)$, $f(1,0)$, $f(1,1)$.

(a) Commutativity constrains only the rows 01 and 10, which must be equal. The other two rows are free: $2 \times 2 \times 2$ = **8** commutative functions (the two constants, AND, OR, NAND, NOR, XOR, XNOR).

(b) **10**, as counted in §3.6: 16 minus 2 constants minus the 4 functions $A$, $\overline{A}$, $B$, $\overline{B}$.

(c) Suppose $f(0, 0) = 0$. Then every circuit built only from copies of $f$ outputs 0 when all its inputs are 0 (each gate sees only 0s, by induction from the inputs), so it can never compute NOT, which must output 1 there. Hence $f(0, 0) = 1$, and by the same argument with all inputs 1, $f(1, 1) = 0$. That leaves $f(0, 1)$ and $f(1, 0)$ free, four candidates:

- 1, 1: NAND;
- 0, 0: NOR;
- 1, 0: $f = \overline{A}$, which ignores $B$;
- 0, 1: $f = \overline{B}$, which ignores $A$.

Circuits of inverters compute only $A$, $\overline{A}$, $B$ or $\overline{B}$, never AND, so the last two fail. NAND and NOR are complete (§3.7). Answer: **2**. The verify script confirms this by building, for each of the 16 functions, everything obtainable by composing it with itself: only NAND and NOR reach all 16 two-input functions.

### Solution 08-02.7

(a) Use De Morgan to turn the SOP into NAND-NAND, $Y = \overline{\overline{\overline{S}D_0}\cdot\overline{SD_1}}$. That needs $\overline{S}$, made by a NAND2 with both inputs on $S$:

$$
N_1 = \overline{SS} = \overline{S},\quad N_2 = \overline{N_1 D_0},\quad N_3 = \overline{S D_1},\quad Y = \overline{N_2 N_3} .
$$

**4** gates. (An exhaustive search confirms that no circuit of 3 NAND2 gates computes the multiplexer.)

(b) $4 \times 4$ = **16** transistors.

(c) **3** levels, from $S$ through $N_1$, $N_2$ and the output gate. The data inputs pass through **2**.

### Solution 08-02.8

(a) $(A + B)(C + D)$ is a POS, so NOR-NOR implements it directly: $P = \overline{A + B}$, $Q = \overline{C + D}$, $Y_1 = \overline{P + Q} = \overline{\overline{A + B} + \overline{C + D}} = (A + B)(C + D)$. **3** gates; (b) **12** transistors.

(c) $Y_2 = AB + CD$ is an SOP, the wrong shape for NOR. Invert the inputs (4 gates), form $AB = \overline{\overline{A} + \overline{B}}$ and $CD = \overline{\overline{C} + \overline{D}}$ (2 gates), NOR them to get $\overline{AB + CD}$ (1 gate) and invert (1 gate): **8** gates, (d) **32** transistors, and **4** levels.

The asymmetry is De Morgan's: NOR-NOR naturally makes products of sums, NAND-NAND sums of products. Forcing the other shape costs inverters on the inputs and output. In practice one would use NAND-NAND for $Y_2$ (12 transistors) or AOI22 plus an inverter (10).

### Solution 08-02.9

(a) A NAND is an OR with inverted inputs. The output gate's input bubbles meet the output bubble of $G_1$ (cancelling) and the inverter's bubble on $G_2$ (cancelling), leaving $Y = AB + C$:

$$
Y = \overline{G_1 G_2} = \overline{G_1} + \overline{G_2} = AB + C .
$$

(b) $C = 1$ in rows 1, 3, 5, 7, and $AB = 1$ in rows 6, 7: rows {1, 3, 5, 6, 7}, integer $2 + 8 + 32 + 64 + 128$ = **234**.

(c) **5** rows.

### Solution 08-02.10

(a) $F(A{=}1) = B + BC = B$ and $F(A{=}0) = C + BC = C$, by absorption. So $F = \overline{A}C + AB$: the expansion has thrown away the term $BC$, proving the consensus theorem $AB + \overline{A}C + BC = AB + \overline{A}C$.

(b) With $A = 0$ the XOR is $B \oplus C$; with $A = 1$ it is $1 \oplus B \oplus C = \overline{B \oplus C}$. So $A \oplus B \oplus C = \overline{A}(B \oplus C) + A\,\overline{(B \oplus C)}$.

(c) Splitting on $A$ needs 1 multiplexer whose two inputs are functions of $B$ and $C$; each of those needs 1 multiplexer splitting on $B$, whose inputs are functions of $C$; each of those 4 needs a multiplexer selecting between two stored bits. Total $1 + 2 + 4$ = **7** $= 2^3 - 1$.

(d) $2^6 - 1$ = **63** multiplexers, selecting among 64 stored bits: the structure of a six-input lookup table ([08-11](../chapters/08-11-memories-and-programmable-logic.md)).

### Solution 08-02.11

(a) The pull-down network conducts when $AB + C = 1$: nMOS $A$ and $B$ in series, in parallel with nMOS $C$. The pull-up network is its dual: pMOS $A$ and $B$ in parallel, in series with pMOS $C$. The expression has three literals, $A$, $B$ and $C$, so the gate has **6** transistors.

(b) $ABC = 110$: nMOS $A$ and $B$ are ON (gates at 1), nMOS $C$ is OFF; pMOS $A$ and $B$ are OFF, pMOS $C$ is ON. The series pair $A$–$B$ connects the output to ground. In the pull-up, pMOS $C$ is ON but the parallel pair above it is OFF, so the path to the supply is open. $Y = 0$ ✓ (since $AB + C = 1$).

(c) $Y = 1$ when $AB + C = 0$: $C = 0$ and not both $A$ and $B$, rows 000, 010 and 100: **3** rows.

(d) **2** in each: the $A$–$B$ series pair in the PDN, and the parallel pair in series with $C$ in the PUN.

### Solution 08-02.12

(a) NAND3 (6 transistors) and an inverter (2): **8** transistors, **2** stages.

(b) $AB$ = NAND2 + inverter (6), then $(AB)C$ = NAND2 + inverter (6): **12** transistors, **4** stages.

(c) By De Morgan, $\overline{\overline{A} + \overline{B} + \overline{C}} = ABC$. Three inverters (6) and a NOR3 (6): **12** transistors, **2** stages.

Choose (a): fewest transistors and two stages. Option (c) has a three-high pMOS stack, normally the slowest choice, but it can win when the complements $\overline{A}$, $\overline{B}$, $\overline{C}$ already exist in the circuit (for instance from flip-flops with complementary outputs), so its inverters cost nothing.

### Solution 08-02.13

(a) Tabulate $(A \oplus B) \oplus C$ and $A \oplus (B \oplus C)$ over the 8 rows: both equal 1 exactly in rows 1, 2, 4 and 7, where an odd number of inputs are 1. They agree everywhere, so XOR is associative.

(b) Pair the inputs, $(A \oplus B) \oplus (C \oplus D)$: **3** gates in **2** levels. (In general, $n - 1$ gates in $\lceil \log_2 n \rceil$ levels.)

(c) Two minterms that differ in one variable have numbers of 1s differing by exactly one, so one has odd and one even parity. They cannot both be minterms of $P$. So no two minterms of $P$ combine (T6), every prime implicant is a single minterm, and the minimal SOP is the canonical one: 8 minterms of 4 literals, **32** literals. The exhaustive search agrees.

(d) $3 \times 12$ = **36** transistors, against a two-level SOP needing eight 4-input ANDs and an 8-input OR. Parity is the classic function for which two-level logic is hopeless, which is why parity and CRC hardware is built from XOR trees (08-01).

### Solution 08-02.14

(a) Tabulate both sides. Left: $\overline{A}B$ (rows 2, 3), $BC$ (3, 7), $A\overline{B}\,\overline{C}$ (4), so rows {2, 3, 4, 7}. Right: $\overline{A}B$ (2, 3), $BC$ (3, 7), $A\overline{C}$ (4, 6), so rows {2, 3, 4, 6, 7}. They differ only in row **6**, $ABC = 110$: the colleague dropped the literal $\overline{B}$, which is only legal when the extra rows it admits are already covered.

(b) Left: $4 + 8 + 16 + 128$ = **156**. (c) Right: $156 + 64$ = **220**.

(d) $2^{50} / 10^9$ s = **1.126 × 10⁶** s, or **13.0** days. Each extra input doubles it: 60 inputs take $2^{60}/10^9$ s, about **36.5** years. Blocks of realistic size must be checked symbolically (§3.5), and exhaustive simulation is reserved for small blocks or for random sampling, which can miss a single wrong row like this one.

### Solution 08-02.15

(a) **Monotone** means: raising any input from 0 to 1 never lowers the output. AND and OR are monotone (check their truth tables), and a composition of monotone functions is monotone, by induction through the circuit: if raising an input can only raise each gate's inputs, it can only raise each gate's output. NOT is not monotone (raising $A$ lowers $\overline{A}$), so no AND-OR circuit computes it. The verify script confirms that composing AND and OR from $A$ and $B$ yields only 4 of the 16 functions: $A$, $B$, $AB$ and $A + B$.

(b) $\overline{A} = A \oplus 1$, so XOR with the constant 1 gives NOT. With NOT and AND, OR follows by De Morgan, $A + B = \overline{\overline{A}\,\overline{B}}$, and {AND, OR, NOT} is complete. (This is the basis of the Reed–Muller, or algebraic-normal, form used in cryptography and coding theory.)

(c) $A + B = \overline{\overline{A}\cdot\overline{B}}$ needs two inverters (NAND2 with tied inputs) and a NAND2; then a fourth NAND2 as an inverter gives $\overline{A + B}$: **4** gates.

(d) By duality, **4** NOR2 gates: two inverters, a NOR2 making $\overline{\overline{A} + \overline{B}} = AB$, and an inverter. In both cases the exhaustive search finds no circuit with 3 gates.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-02.1a | lookup-table integer of $\overline{A}B + A\overline{C}$ | 92 | — |
| 08-02.1b | rows with $Y = 1$ | 4 | — |
| 08-02.2a | rows in the perfect-induction proof | 4 | — |
| 08-02.3a | rows with $F_2 = 1$ | 5 | — |
| 08-02.3b | rows with $\overline{F_2} = 1$ | 11 | — |
| 08-02.4a | literals in (a) simplified | 2 | — |
| 08-02.4b | literals in (b) simplified | 1 | — |
| 08-02.4c | literals in (c) simplified | 1 | — |
| 08-02.4d | literals in (d) simplified | 4 | — |
| 08-02.4e | literals in (e) simplified | 6 | — |
| 08-02.5a | lookup-table integer of $F$ | 141 | — |
| 08-02.5b | lookup-table integer of $\overline{F}$ | 114 | — |
| 08-02.5c | literals, minimal SOP | 4 | — |
| 08-02.5d | literals, minimal POS | 4 | — |
| 08-02.6a | commutative two-input functions | 8 | — |
| 08-02.6b | two-input functions depending on both inputs | 10 | — |
| 08-02.6c | two-input functions complete on their own | 2 | — |
| 08-02.7a | NAND2 gates in the multiplexer | 4 | — |
| 08-02.7b | transistors | 16 | — |
| 08-02.7c | levels on the longest path | 3 | — |
| 08-02.7d | levels from a data input | 2 | — |
| 08-02.8a | NOR2 gates for $(A + B)(C + D)$ | 3 | — |
| 08-02.8b | transistors | 12 | — |
| 08-02.8c | NOR2 gates for $AB + CD$ by input inversion | 8 | — |
| 08-02.8d | transistors | 32 | — |
| 08-02.8e | levels, NOR-only $AB + CD$ | 4 | — |
| 08-02.9a | lookup-table integer of $AB + C$ | 234 | — |
| 08-02.9b | rows with $Y = 1$ | 5 | — |
| 08-02.10a | 2:1 multiplexers for any 3-input function | 7 | — |
| 08-02.10b | 2:1 multiplexers for any 6-input function | 63 | — |
| 08-02.11a | transistors, AOI21 | 6 | — |
| 08-02.11b | rows with $Y = 1$ | 3 | — |
| 08-02.11c | tallest series stack | 2 | — |
| 08-02.12a | transistors, NAND3 + inverter | 8 | — |
| 08-02.12b | transistors, two AND2 | 12 | — |
| 08-02.12c | transistors, inverters + NOR3 | 12 | — |
| 08-02.12d | stages, NAND3 + inverter | 2 | — |
| 08-02.12e | stages, two AND2 | 4 | — |
| 08-02.12f | stages, inverters + NOR3 | 2 | — |
| 08-02.13a | XOR2 gates for 4-input parity | 3 | — |
| 08-02.13b | levels | 2 | — |
| 08-02.13c | literals, minimal SOP of 4-input parity | 32 | — |
| 08-02.13d | transistors, XOR2 tree | 36 | — |
| 08-02.14a | row where the two sides differ | 6 | — |
| 08-02.14b | lookup-table integer, left side | 156 | — |
| 08-02.14c | lookup-table integer, right side | 220 | — |
| 08-02.14d | exhaustive check of 50 inputs at 10⁹ per second | 13.0 | days |
| 08-02.14e | the same, in seconds | 1.126e6 | s |
| 08-02.14f | exhaustive check of 60 inputs | 36.5 | yr |
| 08-02.15a | functions of two inputs reachable with AND and OR | 4 | — |
| 08-02.15c | NAND2 gates to build NOR2 | 4 | — |
| 08-02.15d | NOR2 gates to build NAND2 | 4 | — |
