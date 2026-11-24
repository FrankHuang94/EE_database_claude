# Problems 20-03 · Bandgap and Voltage References

Chapter: [20-03](../chapters/20-03-bandgap-references.md) · Worked solutions: [20-03 solutions](../solutions/20-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unless stated, use the chapter's T130 substrate PNP ($I_{S0}$ = 2 × 10⁻¹⁷ A per unit device at 300 K, $V_{g0}$ = 1.2009 V, η = 3), $T_0$ = 300 K, $V_T$ = 25.85 mV at 300 K, resistors with no temperature coefficient and base currents neglected. "The design" means Example 20-03.2's reference: $N$ = 8, 5 µA per branch at 300 K, zero TC centered for −40 to 125 °C ($T_c$ = 312.0 K), $R_1$ = 10.75 kΩ, $R_2$ = 115.2 kΩ, $V_{REF}$(300 K) = 1.25463 V. Box-method TCs use the 300 K output as $V_{nom}$. Problems marked *(lab)* can be checked with `labs/20-03-lab/bandgap.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-03.1 [A]

**Current density and slope.** A unit PNP is biased with a PTAT current. Find $V_{BE}$ at 300 K and its temperature coefficient there for 1 µA and for 20 µA. Which current gives the flatter junction voltage, and why?

### Problem 20-03.2 [A]

**Choosing N.** Find the slope of $\Delta V_{BE}$ for $N$ = 8 and $N$ = 24, and the gain $K$ each needs to cancel the −1.914 mV/K slope of a unit PNP at 5 µA (PTAT bias, zero TC at 300 K). Give one advantage of the larger $N$.

### Problem 20-03.3 [B]

**The magic voltage for a constant current.** (a) Repeat §3.3's derivation for a junction biased with a constant current ($m$ = 0) plus a PTAT voltage, and show that the zero-TC output at $T_c$ is $V_{g0} + \eta V_T(T_c)$. (b) Evaluate it at 300 K and compare with the PTAT-biased case.

### Problem 20-03.4 [B] *(lab)*

**Wider and narrower ranges.** For a first-order bandgap (η − 1 = 2) with the zero-TC temperature centered in each range, find the centered temperature, the total variation and the box TC over (a) −55 to 125 °C and (b) −40 to 85 °C. Compare with the chapter's −40 to 125 °C result.

### Problem 20-03.5 [B] *(lab)*

**A low-power design.** Redesign the reference with 2 µA per branch and $N$ = 24, zero TC still centered at 312.0 K. Find $V_{BE0}$, $R_1$, $K$, $R_2$ and the output at 300 K. Explain why the output equals the original design's to all the digits computed.

### Problem 20-03.6 [B]

**A process corner.** In the design, every PNP's $I_S$ is 20% *low*. Find the output error at 300 K and its slope, and the percentage change of $R_2$ that trims it out. Check the trim against $\Delta K/K = \ln(1 + \varepsilon)/(K\ln N)$ (with ε = −0.2).

### Problem 20-03.7 [B] *(lab)*

**A chopped op-amp's residual offset.** Chopping reduces the op-amp's offset to 0.2 mV. Find the output error at 300 K, and the box TC and the error at 125 °C if $R_2$ is then trimmed to restore 1.25463 V at 300 K. Compare with the chapter's 1 mV case.

### Problem 20-03.8 [A]

**Resistor errors.** (a) $R_2$ is 0.5% high (ratio error). Find the output error at 300 K and show it is PTAT. (b) Both resistors have a temperature coefficient of +2000 ppm/K. What happens to the output and to the supply current between 300 K and 400 K?

### Problem 20-03.9 [B]

**A 0.5 V reference.** Use the current-mode circuit with the design's $R_1$, $R_2$ and $N$. (a) Find $R_3$ for 0.5 V at 300 K. (b) Find $V_{BE1}$ at −40 °C and the minimum supply if each current source needs 0.15 V.

### Problem 20-03.10 [C]

**Curvature compensation.** (a) Show from §3.1 that two junctions with the same $V_{BE0}$, one biased with a PTAT current and one with a constant current, differ by exactly $V_T\ln(T/T_0)$. (b) Devices have η = 3.5. Find the box TC over −40 to 125 °C uncompensated and with a correction designed for α = 2 (that is, assuming η = 3), and the improvement factor.

### Problem 20-03.11 [B]

**β-multiplier design.** Find $R$ for a 1 µA reference current with $K$ = 8 (a) with both bulks at ground and (b) with M2 in its own well tied to its source ($n$ = 1.3), assuming weak inversion in both cases. (c) Why must both designs include a startup circuit?

### Problem 20-03.12 [C] *(lab)*

**Two operating points.** For Example 20-03.6's β-multiplier ($W/L$ = 10, $M$ = 4, $R$ = 100 kΩ), plot (on paper or in the lab) M1's current against its gate voltage and the current that M2 + $R$ conducts at the same gate voltage. (a) Where do the curves intersect? (b) Why is the lower intersection a valid but useless state? (c) A startup device leaks δ = 1 nA into the M1 branch in normal operation, so M1 carries $I_P + δ$ while M2 carries the mirror current $I_P$. Derive the weak-inversion relation $I_PR = V_T\ln[K(I_P + δ)/I_P]$ and estimate the change in $I_P$.

### Problem 20-03.13 [B]

**Noise.** The design's op-amp has a white input noise of 30 nV/√Hz. (a) What is the output noise density, and the rms noise in a 10 kHz bandwidth, in µV and in ppm of the output? (b) How much does $N$ = 24 (same current and zero-TC temperature) reduce it?

### Problem 20-03.14 [A]

**Reading a data sheet.** A 2.5 V reference specifies an initial accuracy of ±0.05% and a box-method TC of 3 ppm/K (max) over −40 to 125 °C. (a) What is the worst-case total error band over temperature, in ppm and in mV? (b) Compare with the LSB of a 12-bit and a 16-bit converter using it as full scale.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Junction temperature dependence, PTAT voltage, why the sum is flat | 1, 2, 3 |
| 2. Design an op-amp bandgap and predict its curvature | 4, 5 |
| 3. Errors and trimming | 6, 7, 8 |
| 4. Sub-1 V references and curvature compensation | 9, 10 |
| 5. Startup and self-biased current references | 11, 12 |
| 6. Reading data sheets, noise | 13, 14 |
