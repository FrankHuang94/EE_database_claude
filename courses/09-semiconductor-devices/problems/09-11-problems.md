# Problems 09-11 · CMOS and Scaling: Moore, Dennard and Beyond

Chapter: [09-11](../chapters/09-11-cmos-and-scaling.md) · Worked solutions: [09-11 solutions](../solutions/09-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 300 K; $n_i$ = 1.0 × 10¹⁰ cm⁻³, $V_T$ = 25.852 mV, $\varepsilon_s$ = 11.7ε₀. Square-law transistors with $m$ = 1 unless a problem says otherwise. "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-11.1 [A]

**Switching threshold.** For the inverter of Example 09-11.1 ($V_{DD}$ = 1.0 V, $V_{TN} = |V_{TP}|$ = 0.3 V), find $V_M$ when $k_n/k_p$ = 4. What ratio $k_n/k_p$ places $V_M$ at 0.45 V?

### Problem 09-11.2 [A]

**Delay across a node.** Moving to a new node cuts the load capacitance to 0.7 of its old value and the supply from 0.80 V to 0.75 V, while the on-current per gate falls to 0.95 of its old value. By what factor does the inverter delay change?

### Problem 09-11.3 [A]

**Reading a ring oscillator.** A 51-stage ring oscillator runs at 2.5 GHz. Find the stage delay $\tau_d$. If each stage drives 0.8 fF at 0.7 V and the NMOS and PMOS on-currents are equal, what on-current does this imply?

### Problem 09-11.4 [B]

**Voltage and frequency scaling.** A core draws 10 W of dynamic power at 1.0 V and 3 GHz. Its maximum frequency is proportional to $I_{on}/(CV_{DD})$ with $I_{on} \propto V_{DD} - V_{TH}$ (velocity-saturated) and $V_{TH}$ = 0.3 V. At 0.8 V, find the maximum frequency, the dynamic power at that frequency, and the ratio of energy per cycle to the 1.0 V value.

### Problem 09-11.5 [C]

**The minimum-energy supply (numerical).** A block switches an effective 100 pF per cycle ($\alpha C$) and leaks a constant 0.1 A. Its clock runs at the maximum frequency, 2 GHz at 1.0 V, scaling with supply as in Problem 09-11.4 ($V_{TH}$ = 0.3 V). The energy per cycle is $E(V) = \alpha CV^2 + VI_{leak}/f(V)$. Find $E$ at 1.0 V, the supply that minimizes $E$, the minimum energy, the clock frequency there, and the energy saving factor. (The current model is reasonable for $V_{DD} \gtrsim V_{TH}$ + 0.1 V.)

### Problem 09-11.6 [A]

**Measuring a doubling time.** The largest chips in a product line grew from 10⁸ to 5 × 10¹⁰ transistors in 20 years. Find the doubling time and the annual growth rate. At a two-year doubling, by what factor does a count grow in 10 years?

### Problem 09-11.7 [B]

**Potentials that do not scale.** A device has uniform body doping $N_A$ = 10¹⁶ cm⁻³. (a) Find $\phi_B$ and the maximum depletion width $W_{d\max}$ at threshold ($2\phi_B$). (b) Scale by $\kappa$ = 5 with the doping raised fivefold, as constant-field scaling prescribes. Find the new $\phi_B$, $W_{d\max}$ and the ratio to the old width. (c) What doping would shrink $W_{d\max}$ by the full factor of 5, and by what factor is that above the original?

### Problem 09-11.8 [B]

**Partial voltage scaling.** Over three nodes, dimensions shrink by 0.7 per node and frequency rises as $1/$delay. Find the power-density growth per node and over three nodes if the supply shrinks by 0.9 per node, and over three nodes if it stays constant. Use the generalized scaling result of §3.5.

### Problem 09-11.9 [B]

**A power-limited chip.** A chip has 10⁹ gates of 0.5 fF each, with activity 0.15, at 0.7 V and 3 GHz. Its dynamic power budget is 60 W. (a) What fraction of the gates can switch at full speed? (b) If the chip instead runs at 0.6 V and 2.4 GHz, what is the full-chip dynamic power and the fraction?

### Problem 09-11.10 [B]

**Projecting a pitch product.** The IRDS 2024 roadmap's "A10 eq" step is G46M20 (IRDS 2024 More Moore table MM01, R-172). (a) Assume its cell height scales from the "2nm" step's 120 nm in proportion to the M0 pitch (fixed track count). Estimate its CPP × cell height and its density gain over "2nm" and over "3nm" (the '"3nm" Enhanced' step). (b) The IRDS table itself lists an 80 nm high-density cell for A10 eq. Repeat the estimate, and compare with the table's NAND2-equivalent densities of 27.33 and 42.77 Mgates/mm² for "2nm" and A10 eq. (c) For the "3nm" to "2nm" step, compare the pitch-product ratio with the table's NAND2 ratio (19.29 to 27.33 Mgates/mm²).

### Problem 09-11.11 [B]

**Leakage across a node.** At constant die area, a new node doubles the transistor count. If the threshold falls by 30 mV (swing 80 mV/decade) and the supply falls to 0.95 of its old value, by what factor does each transistor's off-current change, and by what factor does the die's leakage power change?

### Problem 09-11.12 [C]

**Sizing with velocity saturation (numerical).** Use the short-channel model of 09-10 ($L$ = 50 nm, 2 nm EOT, $m$ = 1.2): NMOS $\mu_{ns}$ = 183 cm²/V·s and $v_{sat}$ = 8 × 10⁶ cm/s, PMOS $\mu_{ps}$ = 61 cm²/V·s and $v_{sat}$ = 6 × 10⁶ cm/s, $V_{TN} = |V_{TP}|$ = 0.25 V, $V_{DD}$ = 0.8 V. (a) Find the on-currents per micrometer and the $W_p/W_n$ that equalizes rise and fall delays. (b) Find the $W_p/W_n$ that places $V_M$ at $V_{DD}/2$ (both transistors saturated there). (c) Compare both with the mobility ratio.

---

## Objective coverage

| Learning objective (chapter 09-11) | Problems |
|---|---|
| 1. Switching threshold and sizing | 1, 12 |
| 2. Delay and ring oscillators | 2, 3, 12 |
| 3. Power and energy per operation | 4, 5, 9, 11 |
| 4. Moore's law as compound growth | 6 |
| 5. Dennard scaling and its end | 7, 8, 11 |
| 6. Node names and physical pitches | 10 |
