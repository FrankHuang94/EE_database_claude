# Problems 25-01 · Process Flow Overview: FEOL, MOL and BEOL

Chapter: [25-01](../chapters/25-01-process-flow-overview.md) · Worked solutions: [25-01 solutions](../solutions/25-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- $k$ = 8.61733 × 10⁻⁵ eV/K; temperatures in kelvin are °C + 273.15.
- Deal–Grove coefficients are the chapter's table (§3.2); for (100) silicon divide $C_2$ by 1.68. Silicon consumed is 0.44 of the oxide grown.
- Distributed RC delay is $0.3787\,RC$ (19-05); a month is 30.4375 days and a year 365.25 days.
- Drive loss from a source resistance is $1 - 1/(1 + g_mR_S)$ (first order).
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-01-lab/process.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-01.1 [A]

**Wafer sizes.** (a) Find the areas of 200 mm and 300 mm wafers in cm². (b) If processing a 300 mm wafer costs 1.5 times as much as a 200 mm wafer (assumed), what is the ratio of cost per unit area, 300 mm to 200 mm?

### Problem 25-01.2 [A]

**A pad oxide.** A 15 nm pad oxide is grown on bare silicon. (a) How much silicon does it consume? (b) How far above the original silicon surface is its top?

### Problem 25-01.3 [B]

**Dry oxidation with the thin-oxide patch.** *(lab)* (100) silicon is oxidized in dry O₂ at 1100 °C, with an effective initial thickness $x_i$ = 25 nm. Find (a) $B$ and $B/A$, (b) $\tau$ and (c) the thickness after 1.0 h.

### Problem 25-01.4 [B]

**Hotter is faster.** *(lab)* Repeat Example 25-01.2 (500 nm, wet, bare (100) silicon) at 1100 °C. Find (a) $B$ and $B/A$, (b) the time and (c) the speed-up against 1000 °C.

### Problem 25-01.5 [C]

**Deriving the linear-parabolic law.** (a) Starting from the three fluxes of §3.2, derive $x^2 + Ax = B(t + \tau)$ and identify $A$, $B$ and $\tau$. (b) Show that the time to grow $x$ from bare silicon is $x^2/B + x/(B/A)$, and find the thickness at which the two terms are equal. (c) Evaluate that thickness for wet oxidation of (100) silicon at 1000 °C. (d) What does it mean physically?

### Problem 25-01.6 [B]

**Room for the work-function metal.** A gate trench is 14 nm wide and lined with 1.6 nm of HfO₂ (assumed). (a) What is the thickest work-function stack that still leaves 3.0 nm of fill? (b) If a second threshold flavour needs 1.0 nm more work-function metal than the first, how wide must the trench be to keep 3.0 nm of fill with the second flavour, whose stack is (a)'s maximum plus 1.0 nm?

### Problem 25-01.7 [A]

**Cycle time from masks.** A process has 80 mask layers (assumed). (a) What is the cycle time at 1.2 days per mask layer, in days and weeks? (b) What days per mask layer would a 12-week cycle require?

### Problem 25-01.8 [B]

**A contact budget.** A trench contact lands on 15 nm × 30 nm (assumed). (a) What specific contact resistivity keeps $R_c$ at or below 50 Ω? (b) With $g_m$ = 1 mS (assumed), what fraction of drive does a 50 Ω source contact cost? (c) What fraction of Example 25-01.5's 10⁻⁹ Ω·cm² is the required resistivity?

### Problem 25-01.9 [C]

**Copper or ruthenium?** A local wire is 12 nm wide and 24 nm thick. Copper needs a 2 nm barrier on its sides and bottom; ruthenium needs none and has an effective resistivity of 7.0 µΩ·cm at this size (assumed). (a) Find each metal's conducting area. (b) Find ruthenium's resistance per µm. (c) Above what effective copper resistivity does ruthenium win? (d) If narrow copper here is 6.0 µΩ·cm (assumed), which wins, and by how much?

### Problem 25-01.10 [B]

**Two millimetres on the intermediate tier.** Using Example 25-01.6's intermediate tier (9.97 Ω/µm, 0.2 fF/µm), find (a) the delay of a 2 mm route, (b) the same route on the local tier (74.0 Ω/µm), and (c) the intermediate-tier delay if the route is split into four equal segments by ideal, zero-delay repeaters.

### Problem 25-01.11 [A]

**Step yield.** (a) What per-step yield gives 95% survival over 1,200 steps? (b) What survival do 1,200 steps at 99.995% each give?

### Problem 25-01.12 [B]

**Releasing inventory.** A fab starts 50,000 wafers a month. Its cycle time falls from 14 to 12 weeks. (a) Find the work in process before and after. (b) At an average $6,000 per wafer in process (assumed), how much inventory is released?

### Problem 25-01.13 [B]

**What backside power buys.** Model gate speed with the alpha-power law of 19-02, $f \propto (V - V_{TH})^\alpha/V$, with $V_{TH}$ = 0.30 V and $\alpha$ = 1.3 (assumed). The supply is 0.75 V. Moving power to the backside cuts the worst-case IR drop from 50 mV to 20 mV (assumed). (a) Find the frequency gain. (b) Compare it with Intel's PowerVia test-chip result [R-555].

### Problem 25-01.14 [A]

**Mixed density.** (a) A node improves logic density 1.6× and leaves SRAM and analog unchanged. What mixed density gain does TSMC's 50/30/20 blend report? (b) What would it report if SRAM also improved 1.2×?

### Problem 25-01.15 [C]

**A wet-oxidation recipe.** *(lab)* At what temperature does wet oxidation grow 300 nm on bare (100) silicon in exactly 1.0 h? Give $B$ and $B/A$ there.

### Problem 25-01.16 [B]

**Putting the flow in order.** Arrange these nanosheet-logic steps in process order and justify each placement by thermal budget or by what must already exist: (a) copper dual damascene M1; (b) source/drain epitaxy and activation anneal; (c) Si/SiGe superlattice epitaxy; (d) high-k and work-function metal deposition; (e) STI fill, CMP and fin reveal; (f) dummy polysilicon gate and spacers; (g) fin patterning; (h) contact silicide; (i) SiGe release (channel release); (j) well implants and anneal.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. The FEOL, MOL and BEOL flow and its order | 2, 6, 16 |
| 2. The Deal–Grove model and silicon consumption | 2, 3, 4, 5, 15 |
| 3. Gate-trench budget and contact resistance | 6, 8 |
| 4. Wire tiers, delay and alternative metals | 9, 10, 13 |
| 5. Step yield, cycle time and Little's law | 1, 7, 11, 12 |
| 6. Reading node and density claims | 13, 14 |
