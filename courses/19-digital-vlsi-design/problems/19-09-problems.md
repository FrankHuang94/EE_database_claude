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

**Antenna limits on a minimum gate.** A minimum SKY130 transistor has a 0.150 µm gate length and 0.420 µm width. (a) With an antenna limit of 400 applied to the metal's top area, what metal area may connect to its gate before a diffusion does, and how long may a 0.14 µm-wide metal-1 line be? (b) SKY130's actual metal-1 rule applies the limit of 400 to the line's sidewall area, its perimeter times the metal thickness of 0.35 µm [R-319]. How long may the line be now?

### Problem 19-09.11 [B] *(lab)*

**A NAND2 cell from the rules.** (a) Draw a stick diagram of a two-input NAND: pull-down A and B in series, pull-up A and B in parallel sharing the output drain. (b) Using the chapter's rules, find the length of each diffusion strip in λ: the series pull-down with contacts only at its ends, and the parallel pull-up with contacts at both ends and on the shared middle node. Which strip sets the cell's width? (c) Convert to micrometres with λ = 0.075 µm (half SKY130's 0.150 µm gate length).

### Problem 19-09.12 [B]

**Which check catches it?** For each layout problem, name the signoff check that catches it (DRC, LVS, parasitic extraction with timing, antenna, or none) and say why: (a) two metal-1 lines drawn 0.10 µm apart where the rule is 0.14 µm; (b) a missing via, so a gate's output never reaches the next gate's input; (c) a route 40 % longer than the placer estimated, adding delay to a critical path; (d) a 600 µm metal-1 line connected only to a small gate; (e) a transistor drawn 0.65 µm wide where the schematic says 0.42 µm; (f) a logic mistake that was in the schematic itself.

### Problem 19-09.13 [C]

**Measuring a real cell.** SKY130's `sky130_fd_sc_hd__nand2_1` has a Liberty area of 3.7536 µm² (the 19-10 lab's data file), in rows 2.72 µm tall with 0.46 µm sites. (a) How wide is the cell, in micrometres and in sites? (b) Compare with your λ estimate from Problem 11. (c) Optionally, open the cell's GDS in KLayout or Magic (the library is open source) and measure the transistor widths; compare them with 19-03's 0.65 µm NMOS and 1.0 µm PMOS. Why are real cells smaller than λ-rule estimates?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Layers and reading a layout | 11, 13 |
| 2. Design rules and pitches | 1, 2, 7, 11 |
| 3. Euler paths | 3, 4, 5, 9 |
| 4. Standard cells and area estimation | 6, 8, 13 |
| 5. Physical verification | 10, 12 |
