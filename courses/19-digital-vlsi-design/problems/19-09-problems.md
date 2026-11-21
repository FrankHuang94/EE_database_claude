# Problems 19-09 · Layout, Design Rules and Standard Cells

Chapter: [19-09](../chapters/19-09-layout-and-standard-cells.md) · Worked solutions: [19-09 solutions](../solutions/19-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** This chapter's illustrative λ rules: poly width 2λ, poly spacing 3λ, active width 3λ, contacts 2λ × 2λ, contact-to-gate spacing 2λ, active enclosure of contacts 1λ, poly extension 2λ, metal-1 width and spacing 3λ. Networks are written as series (s) and parallel (p) compositions; an ordering is valid if it is an Euler path in both the pull-down network and its dual pull-up network. Problems marked *(lab)* can be checked with `labs/19-09-lab/layout.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-09.1 [A]

**A contacted strip.** What is the minimum width of an active region that holds a contact, and why is it larger than the minimum active width?

### Problem 19-09.2 [A]

**Changing a rule.** If the contact-to-gate spacing grows to 3λ, what are the contacted and uncontacted pitches?

### Problem 19-09.3 [A] *(lab)*

**NAND3.** With the pull-down stack drawn in the order A (top), B, C (bottom), which input orderings are valid? Could a designer get more freedom, and how?

### Problem 19-09.4 [B] *(lab)*

**AOI211.** For $F = \overline{AB + C + D}$, how many of the 24 orderings are valid? Give one.

### Problem 19-09.5 [B] *(lab)*

**OAI22.** For $F = \overline{(A + B)(C + D)}$, how many orderings are valid, and why is the count the same as for the AOI22?

### Problem 19-09.6 [B]

**Block area.** A block has 500 kGates of logic and 30 000 `dfxtp_1` flip-flops (20.02 µm² each). (a) Estimate the logic area from the 120 kGates/mm² routed density. (b) What is the flip-flops' cell area, and their core area at 65% and at 80% utilization?

### Problem 19-09.7 [B]

**Contacts cost length.** Using the illustrative rules, find the length of the diffusion strip for three series transistors (a) with contacts only at the two ends, and (b) with every node contacted. By what percentage does (a) save?

### Problem 19-09.8 [B]

**Utilization.** A block's cells occupy 3.0 mm² in a 4.0 mm² core. (a) What is the utilization? (b) What core area would 85% utilization need, and how much smaller is it?

### Problem 19-09.9 [C]

**Why Euler paths exist.** (a) State the condition for a connected graph to have an Euler path. (b) Count the odd-degree nodes in the AOI22's pull-down and pull-up graphs (Example 19-09.3) and explain why every valid ordering there is in fact a closed walk. (c) Show that a series-parallel network with all transistors in series always has exactly one valid direction pair (two orderings).

### Problem 19-09.10 [C]

**Antenna limits on a minimum gate.** A minimum SKY130 transistor has a 0.150 µm gate length and 0.420 µm width. With an illustrative antenna limit of 400, what metal area may connect to its gate before a diffusion does, and how long may a 0.14 µm-wide metal-1 line be?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Layers and reading a layout | 1, 7 |
| 2. Design rules and pitches | 1, 2, 7 |
| 3. Euler paths | 3, 4, 5, 9 |
| 4. Standard cells and area estimation | 6, 8 |
| 5. Physical verification | 10 |
