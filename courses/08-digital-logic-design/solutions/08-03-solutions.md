# Solutions 08-03 · Logic Minimization: K-Maps and Beyond

Problems: [08-03 problems](../problems/08-03-problems.md) · Chapter: [08-03](../chapters/08-03-logic-minimization.md). Every number below is recomputed by [verify_08_03.py](../verify/verify_08_03.py), which finds prime implicants by enumerating every product term, finds minimum covers by exhaustive search, and checks each published expression against its function row by row.

---

## Solutions

### Solution 08-03.1

(a) The 1s are in rows 000, 010, 100, 110: every row with $C = 0$. On the three-variable map they fill the columns $BC$ = 00 and 10, which are adjacent through the wrap-around: $F_1 = \overline{C}$, **1** literal.

(b) The 1s are rows 010, 011, 110, 111, every row with $B = 1$ (columns 11 and 10): $F_2 = B$, **1** literal.

### Solution 08-03.2

(a) $m_1, m_3, m_9, m_{11}$: binary 0001, 0011, 1001, 1011. $B = 0$ and $D = 1$ in all four; $A$ and $C$ vary. $\overline{B}D$, **2** literals.

(b) $m_4, m_6, m_{12}, m_{14}$: 0100, 0110, 1100, 1110. $B = 1$, $D = 0$: $B\overline{D}$, **2** literals.

(c) $m_0$–$m_3$ and $m_8$–$m_{11}$: every code with $B = 0$. $\overline{B}$, **1** literal (a group of 8 eliminates 3 variables).

(d) $m_8, m_{10}$: 1000 and 1010 differ only in $C$. $A\overline{B}\,\overline{D}$, **3** literals.

### Solution 08-03.3

The map (rows $A$, columns $BC$):

| $A$ \ $BC$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| **0** | 1 | 1 | 1 | 0 |
| **1** | 1 | 1 | 1 | 0 |

Columns 00 and 01 ($B = 0$) form the quad $\overline{B}$; columns 01 and 11 ($C = 1$) form the quad $C$. $F = \overline{B} + C$, **2** literals. Minterms $m_1$ and $m_5$ (column 01) are covered twice. Overlap costs nothing: an OR gate does not care how many of its inputs are 1, and the larger groups each saved literals.

### Solution 08-03.4

The map:

| $AB$ \ $CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| **00** | 0 | 1 | 1 | 0 |
| **01** | 1 | 1 | 0 | 0 |
| **11** | 1 | 1 | 0 | 0 |
| **10** | 0 | 1 | 1 | 0 |

(a) Three maximal rectangles: $\overline{B}D$ ($m_1, m_3, m_9, m_{11}$: rows 00 and 10 are adjacent by wrap-around, columns 01 and 11), $B\overline{C}$ ($m_4, m_5, m_{12}, m_{13}$) and $\overline{C}D$ ($m_1, m_5, m_9, m_{13}$, column 01): **3** primes.

(b) $m_3$ is covered only by $\overline{B}D$, and $m_4$ only by $B\overline{C}$: **2** essential primes.

(c) The two essentials cover all eight minterms: $F = \overline{B}D + B\overline{C}$, **4** literals.

(d) $\overline{C}D$ is left out. Each of its minterms is already covered: $m_1$ and $m_9$ by $\overline{B}D$, $m_5$ and $m_{13}$ by $B\overline{C}$. It is the consensus of the other two (on $B$), so T8 of 08-02 removes it.

### Solution 08-03.5

The 1s fill row $AB$ = 00 completely, row 10 completely, and $m_4$, $m_6$ in row 01. Rows 00 and 10 together (the $B = 0$ half, adjacent by wrap-around) form the octet $\overline{B}$. The remaining 1s $m_4$ and $m_6$ group with $m_0$ and $m_2$ into the quad $\overline{A}\,\overline{D}$ (rows 00 and 01, columns 00 and 10, which wrap). $F = \overline{B} + \overline{A}\,\overline{D}$: **3** literals.

### Solution 08-03.6

The map of 1s:

| $AB$ \ $CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| **00** | 1 | 1 | 1 | 1 |
| **01** | 1 | 1 | 0 | 1 |
| **11** | 1 | 0 | 0 | 0 |
| **10** | 1 | 0 | 0 | 1 |

(a) Five quads are needed: $\overline{A}\,\overline{B}$ (row 00), $\overline{C}\,\overline{D}$ (column 00), $\overline{A}\,\overline{C}$ (rows 00–01, columns 00–01), $\overline{A}\,\overline{D}$ (rows 00–01, columns 00 and 10), $\overline{B}\,\overline{D}$ (the four corners). All five are essential. SOP: **10** literals.

(b) The 0s are $m_7$, $m_9$, $m_{11}$, $m_{13}$, $m_{14}$, $m_{15}$. Group them as an SOP for $\overline{F}$: $AD$ ($m_9, m_{11}, m_{13}, m_{15}$), $ABC$ ($m_{14}, m_{15}$) and $BCD$ ($m_7, m_{15}$). So $\overline{F} = AD + ABC + BCD$, and by De Morgan

$$
F = (\overline{A} + \overline{D})(\overline{A} + \overline{B} + \overline{C})(\overline{B} + \overline{C} + \overline{D}) ,
$$

**8** literals. The POS is cheaper (3 sum terms, 8 literals against 5 product terms, 10 literals), so build it as NOR-NOR or, better, as an OAI gate.

### Solution 08-03.7

Segment *a* is 1 for $m_0, m_2, m_3, m_5, m_6, m_7, m_8, m_9$, and the don't cares are $m_{10}$ to $m_{15}$:

| $AB$ \ $CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| **00** | 1 | 0 | 1 | 1 |
| **01** | 0 | 1 | 1 | 1 |
| **11** | X | X | X | X |
| **10** | 1 | 1 | X | X |

(a) With the X cells: $A$ (the bottom two rows), $C$ (columns 11 and 10, all four rows), $BD$ ($m_5, m_7, m_{13}, m_{15}$) and $\overline{B}\,\overline{D}$ (the four corners $m_0, m_2, m_8, m_{10}$). All four are essential: $a = A + C + BD + \overline{B}\,\overline{D}$, **6** literals.

(b) Without the don't cares the bottom-row octet and the large quads are unavailable. The minimum needs 4 terms and **11** literals, and there are **2** minimal solutions, $\overline{A}C + \overline{A}BD + A\overline{B}\,\overline{C} + \overline{A}\,\overline{B}\,\overline{D}$ and the same with $\overline{B}\,\overline{C}\,\overline{D}$ in place of $\overline{A}\,\overline{B}\,\overline{D}$.

(c) Every illegal code has $A = 1$, so the segment is lit on all **6** of them; codes 10 to 15 would display unusual patterns rather than blank digits.

### Solution 08-03.8

(a) Grouping on the map gives six primes: $AB$ ($m_{12}$–$m_{15}$), $AC$ ($m_{10}, m_{11}, m_{14}, m_{15}$), $B\overline{C}$ ($m_4, m_5, m_{12}, m_{13}$), $\overline{A}\,\overline{B}D$ ($m_1, m_3$), $\overline{A}\,\overline{C}D$ ($m_1, m_5$) and $\overline{B}CD$ ($m_3, m_{11}$): **6** primes.

(b) $m_4$ is covered only by $B\overline{C}$, and $m_{10}$ only by $AC$: **2** essentials. Together they cover $m_4, m_5, m_{10}, m_{11}, m_{12}, m_{13}, m_{14}, m_{15}$.

(c) Left: $m_1$ and $m_3$. The single prime $\overline{A}\,\overline{B}D$ covers both. ($AB$ is now redundant.) $F = AC + B\overline{C} + \overline{A}\,\overline{B}D$: **7** literals, and no other cover is as cheap.

### Solution 08-03.9

**Grouping by number of 1s:** 0 (0000); 2 (0010), 8 (1000); 3 (0011), 5 (0101), 10 (1010); 7 (0111), 11 (1011), 13 (1101); 15 (1111).

**First merge:** 0,2 → 00–0; 0,8 → –000; 2,3 → 001–; 2,10 → –010; 8,10 → 10–0; 3,7 → 0–11; 3,11 → –011; 5,7 → 01–1; 5,13 → –101; 10,11 → 101–; 7,15 → –111; 11,15 → 1–11; 13,15 → 11–1.

**Second merge:** 00–0 with 10–0 gives –0–0 (0, 2, 8, 10); –000 with –010 gives the same. 001– with 101– gives –01– (2, 3, 10, 11). 0–11 with 1–11 gives ––11 (3, 7, 11, 15). 01–1 with 11–1 gives –1–1 (5, 7, 13, 15). No third merge is possible.

(a) **4** primes: $\overline{B}\,\overline{D}$ (–0–0), $\overline{B}C$ (–01–), $CD$ (––11), $BD$ (–1–1).

(b) $m_0$ and $m_8$ are covered only by $\overline{B}\,\overline{D}$; $m_5$ and $m_{13}$ only by $BD$. **2** essentials.

(c) The essentials leave $m_3$ and $m_{11}$, each covered by both $\overline{B}C$ and $CD$. Either completes the cover: $F = \overline{B}\,\overline{D} + BD + \overline{B}C$ or $\overline{B}\,\overline{D} + BD + CD$, **6** literals, **2** minimal solutions.

### Solution 08-03.10

(a) $F_1$: $m_2$ (010), $m_6$ (110), $m_7$ (111). $B\overline{C}$ covers $m_2, m_6$ and $AB$ covers $m_6, m_7$: $F_1 = B\overline{C} + AB$. $F_2$: $m_2, m_3, m_6$. $\overline{A}B$ covers $m_2, m_3$ and $B\overline{C}$ covers $m_2, m_6$: $F_2 = \overline{A}B + B\overline{C}$.

(b) The term $B\overline{C}$ appears in both, so one AND gate can feed both OR gates: **3** distinct terms ($AB$, $B\overline{C}$, $\overline{A}B$).

(c) Separately they need 4 AND gates; shared, 3: sharing saves **1**. In a PLA, where the AND plane is the expensive part, this is the main objective.

### Solution 08-03.11

(a) With the don't cares $m_0, m_2, m_5$ available: $CD$ ($m_3, m_7, m_{11}, m_{15}$) is the only prime covering $m_{11}$ and $m_{15}$, so it is essential. That leaves $m_1$, which two primes can cover: $\overline{A}\,\overline{B}$ (using don't cares $m_0, m_2$) or $\overline{A}D$ (using $m_5$). Either gives **4** literals: $F = CD + \overline{A}\,\overline{B}$ or $F = CD + \overline{A}D$. Not unique: **2** minimal solutions.

(b) Without the don't cares: $F = CD + \overline{A}\,\overline{B}D$, **5** literals.

(c) No. On $m_0$ (0000), $CD + \overline{A}\,\overline{B} = 1$ but $CD + \overline{A}D = 0$; on $m_5$ (0101) the reverse. Both are correct implementations of the specification, and they differ exactly where the specification says it does not care.

### Solution 08-03.12

Draw two four-variable maps (rows $BC$, columns $DE$), one for $A = 0$ (minterms 0 to 15) and one for $A = 1$ (16 to 31).

- On the $A = 0$ map, $m_0, m_2, m_8, m_{10}$ are its four corners ($C = 0$, $E = 0$). On the $A = 1$ map, $m_{16}, m_{18}, m_{24}, m_{26}$ are its corners. The two groups sit in the same positions, so they merge across the maps into one group of 8, losing $A$: $\overline{C}\,\overline{E}$.
- $m_5$ (00101) and $m_{21}$ (10101) are in the same position on the two maps: $\overline{B}C\overline{D}E$.

$F = \overline{C}\,\overline{E} + \overline{B}C\overline{D}E$: **6** literals.

### Solution 08-03.13

(a) The minterms, in binary: 0000, 0001, 0101, 0111, 1000, 1010, 1110, 1111. Each has exactly two neighbors in the on-set at Hamming distance 1: 0 with 1 and 8; 1 with 0 and 5; 5 with 1 and 7; 7 with 5 and 15; 15 with 7 and 14; 14 with 15 and 10; 10 with 14 and 8; 8 with 10 and 0. They form a ring of 8, and no four of them form a quad (a quad needs a 4-cycle of neighbors). So every prime is a pair: **8** primes, $P_1 = \overline{A}\,\overline{B}\,\overline{C}$ (0, 1), $P_2 = \overline{A}\,\overline{C}D$ (1, 5), $P_3 = \overline{A}BD$ (5, 7), $P_4 = BCD$ (7, 15), $P_5 = ABC$ (14, 15), $P_6 = AC\overline{D}$ (10, 14), $P_7 = A\overline{B}\,\overline{D}$ (8, 10), $P_8 = \overline{B}\,\overline{C}\,\overline{D}$ (0, 8).

(b) Each minterm lies in exactly two primes (its two ring edges), so no prime is essential.

(c) Petrick's product, one factor per minterm:

$$
(P_8 + P_1)(P_1 + P_2)(P_2 + P_3)(P_3 + P_4)(P_4 + P_5)(P_5 + P_6)(P_6 + P_7)(P_7 + P_8) .
$$

Eight minterms and two per prime need at least 4 primes, and 4 suffice only if no two chosen primes share a minterm: alternate primes around the ring. The two cheapest products are $P_1P_3P_5P_7$ and $P_2P_4P_6P_8$: **2** minimal solutions, each with 4 three-literal terms, **12** literals:

$$
F = \overline{A}\,\overline{B}\,\overline{C} + \overline{A}BD + ABC + A\overline{B}\,\overline{D} = \overline{A}\,\overline{C}D + BCD + AC\overline{D} + \overline{B}\,\overline{C}\,\overline{D} .
$$

### Solution 08-03.14

(a) SOP: 8 terms of 3 literals, **24** literals. Factored: **6** literals.

(b) NAND-NAND: eight NAND3 ($8 \times 6 = 48$) and a NAND8 ($2 \times 8 = 16$): **64** transistors. OAI222 computes $\overline{(A + B)(C + D)(E + F)}$ with 6 literals, 12 transistors; with the inverter, **14**.

(c) The NAND8 has an **8**-high nMOS stack, unusable in practice: it would be split into a tree of smaller gates, adding levels. The OAI222's pull-down is three parallel pairs in series, **3** high, and its pull-up three series pairs in parallel, 2 high. The factored form is better on every count here.

### Solution 08-03.15

(a) Each variable appears true, complemented or not at all: $3^{10}$ = **59 049** terms in 10 variables, $3^{20}$ ≈ **3.487 × 10⁹** in 20.

(b) Odd parity: no two minterms are adjacent (Problem 08-02.13), so its **8** minterms are its primes, and the minimum is all of them, **32** literals. "Exactly two of four": its 6 minterms have two 1s each, and any neighbor of one has one or three 1s, so again no merges: **6** primes, **24** literals. Both are worst cases for two-level logic, and both are cheap as multi-level circuits (XOR trees, adders).

(c) $2^{40}$ ≈ **1.100 × 10¹²** subsets, which at $10^9$ per second takes about **1100** s, or 18 minutes, for one covering problem. Every extra prime doubles it; at 60 primes it is about 37 years. Branch-and-bound pruning and heuristics such as Espresso exist because of this growth.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-03.1a | literals, $F_1$ | 1 | — |
| 08-03.1b | literals, $F_2$ | 1 | — |
| 08-03.2a | literals, group (a) | 2 | — |
| 08-03.2b | literals, group (b) | 2 | — |
| 08-03.2c | literals, group (c) | 1 | — |
| 08-03.2d | literals, group (d) | 3 | — |
| 08-03.3a | literals, minimal SOP | 2 | — |
| 08-03.4a | prime implicants | 3 | — |
| 08-03.4b | essential prime implicants | 2 | — |
| 08-03.4c | literals, minimal SOP | 4 | — |
| 08-03.5a | literals, minimal SOP | 3 | — |
| 08-03.6a | literals, minimal SOP | 10 | — |
| 08-03.6b | literals, minimal POS | 8 | — |
| 08-03.7a | literals with don't cares | 6 | — |
| 08-03.7b | literals without don't cares | 11 | — |
| 08-03.7c | minimal solutions without don't cares | 2 | — |
| 08-03.7d | illegal codes lighting the segment | 6 | — |
| 08-03.8a | prime implicants | 6 | — |
| 08-03.8b | essential prime implicants | 2 | — |
| 08-03.8c | literals, minimal SOP | 7 | — |
| 08-03.9a | prime implicants | 4 | — |
| 08-03.9b | essential prime implicants | 2 | — |
| 08-03.9c | literals, minimal SOP | 6 | — |
| 08-03.9d | minimal solutions | 2 | — |
| 08-03.10a | distinct AND terms with sharing | 3 | — |
| 08-03.10b | AND gates saved | 1 | — |
| 08-03.11a | literals with don't cares | 4 | — |
| 08-03.11b | minimal solutions with don't cares | 2 | — |
| 08-03.11c | literals without don't cares | 5 | — |
| 08-03.12a | literals, five-variable minimum | 6 | — |
| 08-03.13a | prime implicants | 8 | — |
| 08-03.13b | essential prime implicants | 0 | — |
| 08-03.13c | minimal solutions | 2 | — |
| 08-03.13d | literals, minimal SOP | 12 | — |
| 08-03.14a | literals, SOP | 24 | — |
| 08-03.14b | literals, factored | 6 | — |
| 08-03.14c | transistors, NAND-NAND | 64 | — |
| 08-03.14d | transistors, OAI222 + inverter | 14 | — |
| 08-03.14e | tallest stack, NAND-NAND | 8 | — |
| 08-03.14f | tallest stack, OAI222 | 3 | — |
| 08-03.15a | product terms in 10 variables | 59049 | — |
| 08-03.15b | product terms in 20 variables | 3.487e9 | — |
| 08-03.15c | prime implicants of 4-input parity | 8 | — |
| 08-03.15d | literals, minimal SOP of 4-input parity | 32 | — |
| 08-03.15e | prime implicants of "exactly two of four" | 6 | — |
| 08-03.15f | literals, minimal SOP of "exactly two of four" | 24 | — |
| 08-03.15g | subsets of 40 primes | 1.100e12 | — |
| 08-03.15h | time to try them all at 10⁹ per second | 1100 | s |
| 08-03.15i | the same for 60 primes | 37 | yr |
