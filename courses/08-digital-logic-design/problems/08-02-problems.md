# Problems 08-02 · Boolean Algebra and Logic Gates

Chapter: [08-02](../chapters/08-02-boolean-algebra-and-gates.md) · Worked solutions: [08-02 solutions](../solutions/08-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\overline{A}$ is NOT $A$, $AB$ is AND, $A + B$ is OR. Truth-table rows are numbered by reading the inputs as a binary number with $A$ the most significant bit (row $i = 4A + 2B + C$ for three inputs). A function's **lookup-table integer** has row $i$'s output as bit $i$. Transistor counts are for static CMOS: $2k$ for a $k$-input NAND, NOR or compound gate, 2 for an inverter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-02.1 [A]

**Reading an expression.** For $Y = \overline{A}B + A\overline{C}$: (a) write the truth table; (b) give the lookup-table integer; (c) count the rows with $Y = 1$ and write the canonical SOP.

### Problem 08-02.2 [A]

**Duality and proof.** (a) Write the dual of $A + \overline{A}B = A + B$ and of $A(A + B) = A$. (b) Prove $A + \overline{A}B = A + B$ by perfect induction. How many rows does the proof need? (c) Prove $A(\overline{A} + B) = AB$ algebraically from the axioms of §3.2, naming each axiom you use.

### Problem 08-02.3 [A]

**Complements.** Use De Morgan's theorem to complement (a) $F_1 = (A + \overline{B})C$ and (b) $F_2 = A(B + \overline{C}D)$. For the four-input function $F_2$: (c) in how many rows of its truth table is $F_2 = 1$, and (d) in how many is $\overline{F_2} = 1$?

### Problem 08-02.4 [B]

**Algebraic simplification.** Simplify each expression with the theorems of §3.3, and give the number of literals in your result: (a) $AB + A\overline{B} + \overline{A}B$; (b) $(A + B)(A + \overline{B})$; (c) $\overline{A}\,\overline{B}\,\overline{C} + \overline{A}B\overline{C} + A\overline{B}\,\overline{C} + AB\overline{C}$; (d) $AB + B\overline{C} + AC$; (e) $\overline{A}BC + A\overline{B}C + AB\overline{C} + ABC$.

### Problem 08-02.5 [B]

**Canonical forms.** $F(A, B, C) = \sum m(0, 2, 3, 7)$. (a) Write $F$ as a product of maxterms. (b) Give the lookup-table integers of $F$ and of $\overline{F}$. (c) Find a minimal SOP for $F$ and count its literals. (d) Find a minimal POS for $F$ (hint: minimize $\overline{F}$ as an SOP, then complement) and count its literals.

### Problem 08-02.6 [B]

**A census of two-input functions.** Of the 16 Boolean functions $f(A, B)$: (a) how many are commutative, $f(A, B) = f(B, A)$ for all inputs? (b) how many depend on both inputs? (c) A gate is **complete on its own** if every function can be built from copies of it, with no constant inputs. Show that such a gate must have $f(0, 0) = 1$ and $f(1, 1) = 0$, and use this to find how many of the 16 are complete on their own.

### Problem 08-02.7 [B]

**A multiplexer from NANDs.** The 2:1 multiplexer is $Y = \overline{S}D_0 + SD_1$. (a) Implement it with NAND2 gates only (a NAND2 with tied inputs serves as an inverter); how many gates? (b) How many transistors? (c) How many gate levels lie on the longest path, and from which input?

### Problem 08-02.8 [B]

**NOR-only logic.** (a) Implement $Y_1 = (A + B)(C + D)$ with NOR2 gates only; how many gates and (b) transistors? (c) Implement $Y_2 = AB + CD$ with NOR2 gates only, by first inverting the four inputs (a NOR2 with tied inputs is an inverter); how many gates does that construction use, and (d) how many transistors? Explain why the second costs so much more than the first.

### Problem 08-02.9 [B]

**Reading a circuit by bubble pushing.** A circuit computes $G_1 = \overline{AB}$ with a NAND2, $G_2 = \overline{C}$ with an inverter, and $Y = \overline{G_1 G_2}$ with a second NAND2. (a) Redraw the output NAND as an OR with inverted inputs, cancel bubbles and write $Y$. (b) Give its lookup-table integer and (c) the number of rows with $Y = 1$.

### Problem 08-02.10 [B]

**Shannon expansion.** (a) Expand $F = AB + \overline{A}C + BC$ on $A$: find both cofactors and show the result proves the consensus theorem. (b) Expand the three-input XOR $A \oplus B \oplus C$ on $A$, and express each cofactor using $B \oplus C$. (c) Expanding a three-input function on all three variables in turn gives a tree of 2:1 multiplexers whose leaves are the eight truth-table bits. How many multiplexers is that? (d) How many for six inputs?

### Problem 08-02.11 [B]

**A CMOS AOI21 gate.** Design one static CMOS gate for $Y = \overline{AB + C}$. (a) How many transistors? (b) For the input $ABC = 110$, list which transistors conduct and give $Y$. (c) In how many of the 8 rows is $Y = 1$? (d) What is the tallest series stack in each network?

### Problem 08-02.12 [B]

**Three ways to AND three signals.** Compare, by transistor count and inverting stages on the longest path: (a) a NAND3 followed by an inverter; (b) two cascaded AND2 gates, each built as a NAND2 plus an inverter; (c) a NOR3 fed by the complements $\overline{A}$, $\overline{B}$, $\overline{C}$ from three inverters. Which would you choose, and when might (c) win?

### Problem 08-02.13 [C]

**Parity is expensive in two levels.** (a) Prove that XOR is associative by perfect induction. (b) Four-input odd parity $P = A \oplus B \oplus C \oplus D$ is built as a tree of XOR2 gates: how many gates and how many levels? (c) Show that no two minterms of $P$ differ in a single variable, and hence that its minimal SOP is its canonical SOP; how many literals is that? (d) How many transistors does the XOR2 tree use, with 12-transistor XOR2 gates?

### Problem 08-02.14 [C]

**Catching a wrong simplification.** A colleague claims that $\overline{A}B + BC + A\overline{B}\,\overline{C} = \overline{A}B + BC + A\overline{C}$. (a) Find every row in which the two sides differ. (b) Give the lookup-table integers of the left and (c) right sides. (d) An exhaustive check of a block with 50 inputs runs at $10^9$ vectors per second. How many days does it take, and what does that say about checking larger blocks?

### Problem 08-02.15 [C]

**Completeness.** (a) Prove that AND and OR together cannot build NOT, by showing that every circuit of AND and OR gates is monotone. (b) Show that XOR and AND, with the constant 1 available, are complete. (c) How many NAND2 gates does it take to build a NOR2? (d) How many NOR2 gates to build a NAND2?

---

## Objective coverage

| Learning objective (chapter 08-02) | Problems |
|---|---|
| 1. Axioms and theorems, proved algebraically and by perfect induction | 2, 4, 13 |
| 2. Truth tables, canonical SOP and POS, lookup-table integers | 1, 5, 6, 9, 14 |
| 3. De Morgan, bubble pushing, NAND-only and NOR-only logic, completeness | 3, 7, 8, 9, 15 |
| 4. Shannon expansion, multiplexers and equivalence | 10, 14 |
| 5. Static CMOS gates, transistor counts and stages | 11, 12, 13 |
