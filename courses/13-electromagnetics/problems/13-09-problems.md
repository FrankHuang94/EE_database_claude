# Problems 13-09 · The Smith Chart and Impedance Matching

Chapter: [13-09](../chapters/13-09-smith-chart-and-matching.md) · Worked solutions: [13-09 solutions](../solutions/13-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $Z_0$ = 50 Ω unless stated; $c$ = 2.998 × 10⁸ m/s; $\eta_0$ = 376.7 Ω; lines are lossless; distances toward the generator are clockwise on the chart. You may work each problem on a printed Smith chart or with the formulas; the solutions give both readings where useful.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-09.1 [A]

**Read a point.** Find Γ (magnitude and angle) and the VSWR for $z$ = 0.5 − j0.5.

### Problem 13-09.2 [A]

**Draw two circles.** Give the centre and radius in the Γ plane of the $r$ = 0.5 circle and the $x$ = −2 circle.

### Problem 13-09.3 [A]

**Admittance.** Find the normalized admittance of $z$ = 1 + j1 by the 180° rotation, and say which grid circle it lies on.

### Problem 13-09.4 [B]

**Move along a line.** A 30 + j40 Ω load terminates a 50 Ω line. Find the input impedance 0.15λ from the load.

### Problem 13-09.5 [B]

**Make it real.** For a 100 + j100 Ω load on a 50 Ω line, find the shortest distance toward the generator at which the input impedance is purely real, and that impedance. Relate it to the VSWR.

### Problem 13-09.6 [B]

**A high-pass L-network.** Match a 200 Ω load to 50 Ω at 100 MHz with a series capacitor and a shunt inductor. Where does each element go, and what are their values?

### Problem 13-09.7 [B]

**Absorb the reactance.** A transistor's output needs to see the conjugate of 10 + j5 Ω; equivalently, deliver 50 Ω from a 10 + j5 Ω load at 2.4 GHz. Modify Example 13-09.4's low-pass L-network: what series inductance is added, and what shunt capacitance is used?

### Problem 13-09.8 [B]

**An open-stub match.** Match a 100 Ω load to a 50 Ω line with an open-circuited shunt stub. Give both solutions (distance from the load and stub length, in wavelengths).

### Problem 13-09.9 [C]

**Two sections are wider.** Match 10 Ω to 50 Ω at 2.4 GHz with two low-pass L-sections through an intermediate resistance $\sqrt{10 \times 50}$. Find each section's Q and the bandwidth for $\lvert\Gamma\rvert$ < 0.1, and compare with the single section of Example 13-09.4.

### Problem 13-09.10 [C]

**A small antenna's limit.** For a series RL load, the Bode–Fano limit reads $\int\ln(1/\lvert\Gamma\rvert)\,d\omega \le \pi R/L$. A small antenna is modelled as 10 Ω in series with 10 nH. What is the widest band over which any lossless network could keep its return loss at 20 dB?

### Problem 13-09.11 [B]

**The VSWR circle's extremes.** A 12.5 Ω load terminates a 50 Ω line. Find the VSWR and the largest and smallest impedances seen anywhere along the line.

### Problem 13-09.12 [C]

**Coax for minimum loss.** For an air-filled coax with outer radius $b$ fixed, the conductor loss is $\alpha_c = R_s(1/a + 1/b)/(4\pi Z_0)$ with $Z_0 = (\eta_0/2\pi)\ln(b/a)$. Show that $\alpha_c$ is minimized when $x = b/a$ satisfies $\ln x = 1 + 1/x$, and find $x$ and $Z_0$.

### Problem 13-09.13 [C]

**Coax for maximum power.** For the same air coax with $b$ fixed and air breaking down at a field $E_{bd}$, the transmitted power is limited by the field at the inner conductor. Show that the maximum power occurs at $b/a = \sqrt e$, find $Z_0$ there, and find the geometric mean of this impedance and Problem 13-09.12's.

### Problem 13-09.14 [B]

**A stub for a capacitor.** Realize the 2.653 pF shunt capacitor of Example 13-09.4 at 2.4 GHz as an open stub on a 50 Ω air line. Find its length in wavelengths and centimetres.

### Problem 13-09.15 [B]

**A quarter-wave match for a complex load.** Complete a match of the 100 + j100 Ω load of Problem 13-09.5 to 50 Ω with a quarter-wave transformer. (a) Insert the transformer at the first voltage maximum: find its impedance. (b) Instead insert it at the first voltage minimum: find that distance and the transformer's impedance. (c) Which would you build on a printed circuit board, and why? (Use the chart, or the VSWR.)

---

## Objective coverage

| Learning objective (chapter 13-09) | Problems |
|---|---|
| 1. Chart construction | 2 |
| 2. Reading the chart and moving along lines | 1, 3, 4, 5, 11, 15 |
| 3. L-network matching | 6, 7, 9 |
| 4. Single-stub matching | 8, 14 |
| 5. Bandwidth and Bode–Fano | 9, 10 |
| (Practitioner) The 50 Ω standard | 12, 13 |
