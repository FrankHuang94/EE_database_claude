# Problems 25-05 · Foundries, PDKs and Specialty Processes

Chapter: [25-05](../chapters/25-05-foundries-pdks-specialty-processes.md) · Worked solutions: [25-05 solutions](../solutions/25-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Delay follows $t_d \propto V/(V - V_{TH})^{\alpha}$; corners as in Example 25-05.4 unless stated.
- Relative permittivities: SiO₂ 3.9, Si 11.7.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-05-lab/foundry.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-05.1 [A]

**Shares.** Using TrendForce's 2Q26 figures (SMIC 5.4%, Samsung 5.9%, top-10 revenue $53.49 B, TSMC $40.2 B at 72.5%) [R-578], find (a) the gap between Samsung and SMIC in percentage points and (b) SMIC's approximate revenue on the implied market base.

### Problem 25-05.2 [A]

**A node mix check.** Confirm that TSMC's 2Q26 node shares (2 nm 3%, 3 nm 30%, 5 nm 33%, 7 nm 11%) sum to its reported 77% for 7 nm and below [R-579]. What share came from nodes older than 7 nm?

### Problem 25-05.3 [A]

**An open-source shuttle slot.** Europractice prices GF180MCU at €913/mm² with a 6 mm² minimum [R-581]. What does a 2 mm² design cost, and what does it pay per square millimetre it actually uses?

### Problem 25-05.4 [B]

**A pricier mask set.** For the 22 nm FD-SOI shuttle of Example 25-05.3, find the break-even area against a dedicated run costing €2.5 M (assumed).

### Problem 25-05.5 [B]

**A long-channel exponent.** *(lab)* Repeat Example 25-05.4(a) and (b) with $\alpha$ = 2.0. Is the corner spread larger or smaller, and why?

### Problem 25-05.6 [B]

**Guaranteed frequency.** With Example 25-05.4's corners ($\alpha$ = 1.3), a design must guarantee 2.0 GHz at the slow corner. What typical-corner frequency must its critical path achieve?

### Problem 25-05.7 [B]

**Sizing back bias.** With Example 25-05.5's 20 nm BOX coupling, (a) what back-gate swing shifts the threshold by 80 mV? (b) By what factor does that cut leakage at 70 mV/decade?

### Problem 25-05.8 [C]

**Deriving the coupling.** *(lab)* (a) Draw the FD-SOI stack as series capacitors and derive $\Delta V_{TH}/\Delta V_{BG}$ in §3.5, stating the assumption about the front surface at threshold. (b) Evaluate it for a 1.0 nm EOT gate, a 6 nm body and a 25 nm BOX. (c) Which single dimension would you change to double the coupling, and by how much?

### Problem 25-05.9 [B]

**A more digital MCU.** Repeat Example 25-05.6 for a 10 mm² die with 6 mm² digital, 1 mm² NVM and 3 mm² analog and I/O. Find the new area and die-cost ratio.

### Problem 25-05.10 [B]

**A discounted slot.** At Europractice's discounted €16,200/mm² for GF 22 nm FD-SOI [R-581], what does the 4 mm² minimum slot cost, and what is that per sample if the run returns 40 dies (assumed)?

### Problem 25-05.11 [A]

**High-voltage area.** Using the unipolar-limit scaling $R_{on,sp} \propto V_B^2$ of 09-13, by what factor does the specific on-resistance of an 80 V LDMOS exceed a 20 V one? What does that imply for the die area of a BCD power stage at fixed on-resistance?

### Problem 25-05.12 [B]

**Corners and yield.** If the slow corner is set at +3σ of a normal global distribution of delay, what fraction of dies is slower than it? How many dies per million?

### Problem 25-05.13 [B]

**Starting on an early PDK.** Starting a design on a 0.5 PDK adds a 30% chance of a $20 M respin (assumed) and launches six months earlier. What gross profit per month of earlier launch makes the early start worth it on expected value?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Foundry models and market data | 1, 2 |
| 2. PDK contents and maturity | 13 |
| 3. Corners and signoff margin | 5, 6, 12 |
| 4. Shuttles against dedicated runs | 3, 4, 10 |
| 5. FD-SOI back-gate coupling | 7, 8 |
| 6. Specialty processes and node choice | 9, 11 |
