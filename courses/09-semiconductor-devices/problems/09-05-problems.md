# Problems 09-05 · PN Junction Electrostatics

Chapter: [09-05](../chapters/09-05-pn-junction-electrostatics.md) · Worked solutions: [09-05 solutions](../solutions/09-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** silicon at 300 K: $\varepsilon_s = 11.7\varepsilon_0$ = 1.036 × 10⁻¹² F/cm, $n_i$ = 1.0 × 10¹⁰ cm⁻³, $kT/q$ = 25.85 mV. Step junctions and the depletion approximation unless stated; $V_A$ is positive for forward bias. Use the course mobility model of 09-03 where a mobility is needed, and a critical field of 3 × 10⁵ V/cm for silicon where breakdown is estimated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-05.1 [A]

**Built-in potentials.** Find $V_{bi}$ for (a) $N_A$ = 10¹⁸ and $N_D$ = 10¹⁵ cm⁻³; (b) $N_A = N_D$ = 10¹⁶ cm⁻³; (c) a GaAs junction with $N_A = N_D$ = 10¹⁷ cm⁻³ and $n_i$ = 2.1 × 10⁶ cm⁻³. (d) Why is (c) so much larger than a silicon junction with the same doping?

### Problem 09-05.2 [A]

**A symmetric junction.** For $N_A = N_D$ = 10¹⁶ cm⁻³ at zero bias, find $W$, $x_n$ and the peak field.

### Problem 09-05.3 [A]

**Bias and width.** A P⁺N junction has $N_A$ = 10¹⁹ and $N_D$ = 10¹⁵ cm⁻³. Find $W$ at 0, −1, −10 and −100 V, from the full formula and from the one-sided approximation.

### Problem 09-05.4 [A]

**Sketching from numbers.** A junction's depletion region is 0.5 µm wide with 1.2 V across it. (a) What is the peak field? (b) If the n side is ten times more lightly doped than the p side, how wide is the depletion region on each side? (c) Sketch the field and potential.

### Problem 09-05.5 [B]

**Designing a depletion width.** A P⁺N photodiode ($N_A$ = 10¹⁹ cm⁻³) must have a 2 µm depletion region at 5 V reverse bias. Find the n-side doping. (The built-in potential depends on the answer, so solve by root finding.)

### Problem 09-05.6 [B]

**Inside the profile.** For the junction of Example 09-05.2 (10¹⁷/10¹⁶ cm⁻³, zero bias), find (a) the potential at $x = x_n/2$ measured from the n-side neutral region, and (b) the field magnitude at $x = -x_p/2$.

### Problem 09-05.7 [B]

**Charge and capacitance.** For the same junction, find (a) the depleted charge per area on the n side at 0 V and at −5 V; (b) the capacitance per area at −5 V from $\varepsilon_s/W$ and from a numerical derivative of the charge with respect to voltage, and show they agree.

### Problem 09-05.8 [B]

**Debye lengths.** For P⁺N junctions ($N_A$ = 10¹⁹ cm⁻³) with $N_D$ = 10¹⁴, 10¹⁶ and 10¹⁸ cm⁻³, find the Debye length on the n side, the zero-bias depletion width and their ratio. What do you conclude about the depletion approximation?

### Problem 09-05.9 [B]

**A steeply graded junction.** A junction has grading constant $a$ = 10²² cm⁻⁴. Find $W$ and $V_{bi}$ at zero bias self-consistently, the doping at the depletion edges and the peak field.

### Problem 09-05.10 [B]

**Extracting doping from C–V.** A P⁺N test diode of area 10⁻⁴ cm² measures 2.944 pF at −1 V and 1.837 pF at −4 V. (a) Find the slope of $1/C^2$ against $V_A$ and the n-side doping. (b) Find the built-in potential from the intercept.

### Problem 09-05.11 [C]

**A 200 V junction.** A one-sided silicon junction must block 200 V. (a) Estimate the maximum n-side doping, (b) the depletion width at breakdown, and (c) the resistance per area of an n region of exactly that width and doping.

### Problem 09-05.12 [C]

**The PIN diode.** A P⁺–i–N⁺ diode has an undoped (intrinsic) region 2 µm wide between heavily doped regions ($N$ = 10¹⁹ cm⁻³ each). (a) Find $V_{bi}$. (b) Treating the intrinsic region as fully depleted with a uniform field, find the field at 10 V reverse bias and the capacitance per area. (c) Compare the capacitance with a P⁺N junction with $N_D$ = 10¹⁵ cm⁻³ at the same bias. Why are PIN diodes used as fast photodetectors?

### Problem 09-05.13 [C]

**The silicon limit.** (a) Show that a one-sided junction's drift region, sized to break down at $V_{br}$, has resistance per area $4V_{br}^2/(\varepsilon_s\mu\mathcal E_c^3)$. (b) Evaluate the doping, width, mobility and resistance per area for 600 V in silicon. (c) Keeping $\varepsilon_s$ and $\mu$ fixed, what would a tenfold critical field do?

### Problem 09-05.14 [C]

**Correcting the depletion approximation.** For a P⁺N junction with $N_A$ = 10¹⁹ and $N_D$ = 10¹⁵ cm⁻³ at zero bias, find $V_{bi}$, $W$, and the width after the $2kT/q$ correction. Is the correction significant?

### Problem 09-05.15 [B]

**A GaAs junction.** For the GaAs junction of Problem 09-05.1(c), with $\varepsilon_r$ = 12.9 [handbook], find the depletion width and peak field at zero bias, and compare with a silicon junction of the same doping.

---

## Objective coverage

| Learning objective (chapter 09-05) | Problems |
|---|---|
| 1. Band diagram and built-in potential | 1, 15 |
| 2. Depletion approximation and Poisson's equation | 4, 6, 7 |
| 3. Width, split and peak field under bias; one-sided junctions | 2, 3, 5, 11, 12, 13 |
| 4. Graded junctions and accuracy of the approximation | 8, 9, 14 |
| 5. Junction capacitance and C–V profiling | 7, 10, 12 |
