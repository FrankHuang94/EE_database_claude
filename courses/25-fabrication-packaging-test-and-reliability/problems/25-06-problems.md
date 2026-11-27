# Problems 25-06 · Packaging I: Wire Bond, Flip-Chip, Substrates, SiP and PoP

Chapter: [25-06](../chapters/25-06-packaging-fundamentals.md) · Worked solutions: [25-06 solutions](../solutions/25-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Perimeter I/O $4D/p_w$; area-array I/O $(D/p_a)^2$.
- Traces between pads $n = \lfloor(p - d - s)/(w + s)\rfloor$; each layer escapes $n + 1$ rows.
- Joint shear strain $\gamma = \Delta\alpha\,\Delta T\,L_{DNP}/h$; fatigue life $N_f \propto \gamma^{-2}$.
- Silicon 2.6 ppm/K; organic substrate 16 ppm/K (assumed).
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-06-lab/package.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-06.1 [A]

**A smaller die.** A 5 mm × 5 mm die could use one row of wire-bond pads at 50 µm pitch or a bump array at 130 µm pitch (assumed). Find (a) each I/O count and (b) the crossover die size at these pitches.

### Problem 25-06.2 [B]

**Smaller pads.** *(lab)* Repeat Example 25-06.2 with 80 µm pads and 12 µm/12 µm lines and spaces. How many traces fit between pads, and how many layers escape 15 rows?

### Problem 25-06.3 [B]

**A finer bump pitch.** A 110 µm pitch array with 70 µm pads must escape 20 rows with 10 µm/10 µm lines and spaces (assumed). How many layers does it need? Compare with Example 25-06.2(b).

### Problem 25-06.4 [B]

**A bigger accelerator.** *(lab)* A die draws 1,500 W at 0.70 V, with 0.2 A per bump allowed (assumed). Find (a) the current, (b) the power bumps, (c) the power and ground bumps and (d) their area at 130 µm pitch.

### Problem 25-06.5 [B]

**Automotive cycling.** Repeat Example 25-06.4(b) for a −40 °C to 125 °C cycle. By what factor does fatigue life fall relative to the 100 K cycle?

### Problem 25-06.6 [B]

**The true corner.** The corner joint of Example 25-06.4's 20 mm die is on the diagonal, 14.14 mm from the centre. Find its strain and its life relative to the edge-midpoint joint.

### Problem 25-06.7 [B]

**Taller joints.** Copper pillars raise the joint height from 70 µm to 100 µm (assumed). Find the new strain for Example 25-06.4 and the life gain.

### Problem 25-06.8 [C]

**The weakest link.** *(lab)* (a) Derive the package survival function for $M$ joints with independent Weibull lives of shape $\beta$ and scales $\eta_i$, and show it is Weibull with $\eta_{pkg} = (\sum_i \eta_i^{-\beta})^{-1/\beta}$. (b) For $M$ = 1,000 identical joints and $\beta$ = 4, by what factor is the package's characteristic life shorter than one joint's?

### Problem 25-06.9 [A]

**An even bigger substrate.** How many 130 mm substrates fit the 510 mm × 515 mm panel of Example 25-06.5, and what is their area relative to 110 mm substrates?

### Problem 25-06.10 [A]

**Concentration.** The 2024 top-five OSATs were ASE ($18.54 B), Amkor ($6.32 B), JCET ($5.00 B), Tongfu ($3.32 B) and Powertech (\$2.28 B), of a top-ten total of \$41.56 B [R-582]. What share of the top ten do the top five hold?

### Problem 25-06.11 [B]

**Ground bounce in the package.** Eight outputs each switch 20 mA in 1.0 ns through a shared ground connection. Find the ground bounce if that connection is (a) a 2 mm bond wire at 1 nH/mm (13-03) or (b) a flip-chip bump of 0.05 nH (assumed).

### Problem 25-06.12 [C]

**Designing the substrate.** A 130 µm pitch array with 80 µm pads must escape 20 rows to each die edge in no more than 5 signal layers. With equal line and space $w = s$, what is the largest line width that works?

### Problem 25-06.13 [A]

**Choosing a package.** Choose among a wire-bonded QFN, a flip-chip BGA on a build-up substrate, fan-out wafer-level packaging and package-on-package, and justify each choice by I/O count, electrical performance, thickness and cost: (a) a 4 mm² temperature-sensor ASIC; (b) a smartwatch application processor that needs LPDDR memory in the same footprint; (c) a 600 mm² network-switch ASIC with 1,500 signal and power connections; (d) a thin phone power-management die with a few dozen I/Os.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Package functions and technologies | 11, 13 |
| 2. Perimeter against area I/O | 1 |
| 3. Escape routing and power bumps | 2, 3, 4, 12 |
| 4. Solder-joint strain, fatigue and the weakest link | 5, 6, 7, 8 |
| 5. Substrate economics and market data | 9, 10 |
