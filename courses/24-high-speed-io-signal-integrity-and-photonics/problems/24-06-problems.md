# Problems 24-06 · Die-to-Die Links, Memory PHYs and Scale-Up Fabrics

Chapter: [24-06](../chapters/24-06-d2d-memory-phys-scale-up.md) · Worked solutions: [24-06 solutions](../solutions/24-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Unterminated energy per bit is $CV^2/4$; terminated energy is $V^2/(4Rf_b)$.
- Bumps lie on a square grid; areal density is $\phi r/(8p^2)$.
- Elmore delay is $R_{on}C_{tot} + R_w(C_w/2 + C_L)$, and the 10–90% rise time is about $2.2\times$ the Elmore delay (single-pole approximation).
- Bandwidths "both directions" add the two directions.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-06-lab/d2d.py` or `wire.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-06.1 [A]

**A wider bus.** *(lab)* Each of 1,024 unterminated wires presents 500 fF and swings 0.6 V at 16 Gb/s (assumed). Find (a) the energy per rising edge, (b) the energy per bit, (c) the power per wire and (d) the power of the whole bus.

### Problem 24-06.2 [B]

**Terminated or not?** A link swings 0.3 V. (a) Terminated with 50 Ω at each end at 16 Gb/s, what is its energy per bit? (b) Unterminated with 300 fF, what is it? (c) At what rate would the two be equal, and why does that rate say the lumped model has broken down?

### Problem 24-06.3 [B]

**Pitch and density.** *(lab)* With half the bumps carrying data at 32 Gb/s, find the areal bandwidth density at (a) 25 µm and (b) 55 µm pitch.

### Problem 24-06.4 [B]

**Enough edge?** A die has 25 mm of edge available for a die-to-die link that must carry 10 TB/s in both directions (assumed). (a) What shoreline density is needed? (b) Is that inside UCIe-A's 165–1,317 GB/s/mm range? (c) How much edge would UCIe-S need at its best 224 GB/s/mm?

### Problem 24-06.5 [A]

**UCIe 3.0 rates.** How many UCIe-A modules at 64 GT/s carry 10 TB/s in both directions, and what power do they need at 0.25 pJ/b?

### Problem 24-06.6 [B]

**How fast can this wire go?** A 1 mm wire has $R_w$ = 25 Ω and $C_w$ = 100 fF, a 50 fF load and a driver of $R_{on}$ = 100 Ω with 50 fF of its own pad (assumed). Find (a) $C_{tot}$, (b) the Elmore delay, (c) the approximate 10–90% rise time and (d) the rate at which the UI equals that rise time.

### Problem 24-06.7 [A]

**BoW edge density.** Four BoW-512 slices fit along each millimetre of die edge (assumed). What bandwidth per millimetre is that, in Gb/s and GB/s?

### Problem 24-06.8 [B]

**NVLink 4.** A Hopper GPU has 18 NVLink 4 links of 2 lanes at 100 Gb/s each way [R-521]. Find (a) a link's bandwidth each way and in both directions, (b) the GPU's total and (c) the total for an 8-GPU node.

### Problem 24-06.9 [B]

**UALink ports.** A UALink x4 port runs 4 lanes of 200 Gb/s each way. (a) What does it carry each way in GB/s? (b) How many x4 ports would match NVLink 5's 1.8 TB/s per GPU (both directions)? (c) What is the line-rate overhead of signalling at 212.5 GT/s?

### Problem 24-06.10 [B]

**An accelerator's I/O power.** An accelerator moves 2 TB/s die to die at 0.25 pJ/b, 1.8 TB/s over its scale-up fabric at 1.3 pJ/b and 0.2 TB/s of scale-out traffic on SerDes at 3 pJ/b (all assumed). Find each power and the total.

### Problem 24-06.11 [C]

**What does a quoted HBM bandwidth imply?** A GPU has 8 HBM4 stacks (assumed), each with a 2048-bit interface. (a) What bandwidth does the JEDEC baseline of 8 Gb/s per wire give? NVIDIA's preliminary pages quote 22 TB/s and 19.2 TB/s per GPU [R-522]. (b) What per-wire rate does each figure imply with 8 stacks?

### Problem 24-06.12 [C]

**The limit of hybrid bonding.** At 1 µm pitch, with half the bonds carrying data at 1 GT/s (assumed), find (a) the areal density in TB/s per mm² and (b) the power of a 10 TB/s link at 0.01 pJ/b.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Wire energy and speed | 1, 2, 6 |
| 2. Bandwidth density from pitch | 3, 4, 7, 12 |
| 3. UCIe and BoW sizing | 4, 5, 7 |
| 4. Memory PHYs against SerDes | 11 |
| 5. Scale-up fabric bandwidth | 8, 9 |
| 6. The energy ladder | 10, 12 |
