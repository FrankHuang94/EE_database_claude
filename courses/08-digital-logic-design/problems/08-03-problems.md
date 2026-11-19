# Problems 08-03 · Logic Minimization: K-Maps and Beyond

Chapter: [08-03](../chapters/08-03-logic-minimization.md) · Worked solutions: [08-03 solutions](../solutions/08-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** minterm $m_i$ of a function of $A, B, C, D$ has $i = 8A + 4B + 2C + D$ ($A$ most significant); $\sum d(\ldots)$ lists don't cares. "Minimal" means fewest product (or sum) terms, then fewest literals. Four-variable maps have rows $AB$ and columns $CD$ in the order 00, 01, 11, 10.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-03.1 [A]

**Two quick maps.** Minimize (a) $F_1(A, B, C) = \sum m(0, 2, 4, 6)$ and (b) $F_2(A, B, C) = \sum m(2, 3, 6, 7)$. Give the literal count of each.

### Problem 08-03.2 [A]

**Reading groups.** On a four-variable map, write the product term for each group and count its literals: (a) $m_1, m_3, m_9, m_{11}$; (b) $m_4, m_6, m_{12}, m_{14}$; (c) $m_0, m_1, m_2, m_3, m_8, m_9, m_{10}, m_{11}$; (d) $m_8, m_{10}$.

### Problem 08-03.3 [A]

**Overlapping groups.** Minimize $F(A, B, C) = \sum m(0, 1, 3, 4, 5, 7)$ and count literals. Which minterms are covered twice, and does that cost anything?

### Problem 08-03.4 [B]

**A four-variable map.** Minimize $F = \sum m(1, 3, 4, 5, 9, 11, 12, 13)$. (a) List all prime implicants. (b) Which are essential? (c) Give the minimal SOP and its literal count. (d) Which prime is left out, and why is it redundant?

### Problem 08-03.5 [B]

**Big groups.** Minimize $F = \sum m(0, 1, 2, 3, 4, 6, 8, 9, 10, 11)$ and count literals.

### Problem 08-03.6 [B]

**SOP against POS.** For $F = \sum m(0, 1, 2, 3, 4, 5, 6, 8, 10, 12)$: (a) find a minimal SOP and its literal count; (b) find a minimal POS (group the 0s) and its literal count. Which would you build?

### Problem 08-03.7 [B]

**A seven-segment display.** Segment *a* (the top bar) of a seven-segment display is lit for the BCD digits 0, 2, 3, 5, 6, 7, 8 and 9, and dark for 1 and 4. Codes 10 to 15 never occur. (a) Minimize segment *a* using the don't cares, and count literals. (b) Minimize it with codes 10 to 15 treated as 0s; how many literals, and how many minimal solutions? (c) On how many of the illegal codes does the circuit from (a) light the segment?

### Problem 08-03.8 [B]

**Primes and essentials.** For $F = \sum m(1, 3, 4, 5, 10, 11, 12, 13, 14, 15)$: (a) find all prime implicants; (b) identify the essential ones; (c) complete a minimal cover and give its literal count.

### Problem 08-03.9 [B]

**Quine–McCluskey by hand.** Use the tabular method on $F = \sum m(0, 2, 3, 5, 7, 8, 10, 11, 13, 15)$: (a) how many prime implicants are there; (b) which are essential; (c) what is the minimal literal count, and how many minimal solutions are there?

### Problem 08-03.10 [B]

**Sharing terms between outputs.** Two outputs of the same inputs are $F_1(A, B, C) = \sum m(2, 6, 7)$ and $F_2(A, B, C) = \sum m(2, 3, 6)$. (a) Minimize each separately. (b) How many distinct AND terms does a two-output implementation need if terms may be shared? (c) How many AND gates does sharing save?

### Problem 08-03.11 [B]

**Don't cares with a choice.** $F = \sum m(1, 3, 7, 11, 15) + \sum d(0, 2, 5)$. (a) Find a minimal SOP using the don't cares, with its literal count. Is it unique? (b) Find the minimal SOP ignoring the don't cares. (c) Do your answers to (a) agree on the don't-care inputs?

### Problem 08-03.12 [C]

**Five variables.** A five-variable map is two four-variable maps, one for $A = 0$ and one for $A = 1$; a cell is also adjacent to the cell in the same position on the other map. Minimize $F(A, B, C, D, E) = \sum m(0, 2, 5, 8, 10, 16, 18, 21, 24, 26)$ (here $i = 16A + 8B + 4C + 2D + E$), and count literals.

### Problem 08-03.13 [C]

**A cyclic four-variable function.** For $F = \sum m(0, 1, 5, 7, 8, 10, 14, 15)$: (a) show that every prime implicant is a pair of minterms, and count them; (b) show that none is essential; (c) write Petrick's product, find the minimal covers, and give their number and literal count.

### Problem 08-03.14 [C]

**Factoring beats two levels.** $F = ACE + ACF + ADE + ADF + BCE + BCF + BDE + BDF$. (a) Count the literals of this minimal SOP and of the factored form $(A + B)(C + D)(E + F)$. (b) Count transistors for NAND-NAND (eight NAND3 gates and a NAND8) and for one OAI222 gate plus an inverter. (c) Give the tallest series stack of each, and comment.

### Problem 08-03.15 [C]

**Where exact minimization breaks.** (a) How many product terms are there in 10 variables, and in 20? (b) How many prime implicants do four-input odd parity and the four-input "exactly two inputs are 1" function have, and what are their minimal literal counts? (c) A covering step must choose among 40 prime implicants. How many subsets would brute force examine, and how long would that take at $10^9$ subsets per second?

---

## Objective coverage

| Learning objective (chapter 08-03) | Problems |
|---|---|
| 1. Karnaugh maps of two to five variables, minimal SOP and POS | 1, 2, 3, 4, 5, 6, 12 |
| 2. Don't-care conditions and their consequences | 7, 11 |
| 3. Prime and essential prime implicants, covers | 4, 8, 13 |
| 4. Quine–McCluskey and Petrick's method; why exact minimization does not scale | 9, 13, 15 |
| 5. Multi-level logic and multiple outputs | 10, 14 |
