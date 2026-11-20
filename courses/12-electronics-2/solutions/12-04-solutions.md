# Solutions 12-04 · High-Frequency Analysis Methods

Problems: [12-04 problems](../problems/12-04-problems.md) · Chapter: [12-04](../chapters/12-04-high-frequency-analysis-methods.md). Every number below is recomputed by [verify_12_04.py](../verify/verify_12_04.py), which finds each resistance with a test source and each coefficient from $\det(\mathbf{G} + s\mathbf{C})$.

---

## Solutions

### Solution 12-04.1

With node B's capacitor open, node A's capacitor sees the source's 1 kΩ (the second resistor leads nowhere): $R_{A0}$ = **1** kΩ. With node A's open, node B's sees both resistors in series: $R_{B0}$ = **2** kΩ. Sum $1 + 2$ µs = **3** µs, estimate **53.05** kHz. The denominator is $1 + 3RCs + R^2C^2s^2$, with roots at **60.79** kHz and **416.7** kHz; the exact −3 dB frequency is **59.56** kHz. The poles are under a decade apart, so the estimate is 11% low.

### Solution 12-04.2

$R_{gd0} = R_S + R_L + g_mR_SR_L = 2 + 10 + 5 \times 2 \times 10$ kΩ = **112** kΩ.

### Solution 12-04.3

$\tau_{gs} = 5\ \text{k}\Omega \times 50\ \text{fF}$ = **0.25** ns; $R_{gd0} = 5 + 10 + 2 \times 5 \times 10$ = 115 kΩ, so $\tau_{gd}$ = **1.15** ns; $\tau_L = 10\ \text{k}\Omega \times 50\ \text{fF}$ = **0.5** ns. Sum **1.9** ns (12-03 Problem 5's $b_1$), estimate **83.77** MHz. $C_{gd}$ contributes **60.5**%: here the Miller term dominates.

### Solution 12-04.4

With $C_{gs}$ shorted, the gate is grounded and both $C_{gd}$ and $C_L$ see $R_L$: $R_{gd}^{gs} = R_L^{gs}$ = **10** kΩ. With $C_{gd}$ shorted, the transistor is a diode: $R_L^{gd} = R_L \parallel R_S \parallel 1/g_m$ = **434.8** Ω. Then $b_2 = 0.25\ \text{ns}(10\ \text{k}\Omega \times 10\ \text{fF} + 10\ \text{k}\Omega \times 50\ \text{fF}) + 1.15\ \text{ns} \times 434.8\ \Omega \times 50\ \text{fF}$ = **1.75** × 10⁻¹⁹ s², matching 12-03 Problem 5.

### Solution 12-04.5

Input coupling: $1/[(0.6 + 10)\ \text{k}\Omega \times 1\ \mu\text{F}]$ = **94.34** rad/s. Output coupling: $1/[(2 + 8)\ \text{k}\Omega \times 10\ \mu\text{F}]$ = **10** rad/s. Sum **104.3** rad/s, so $f_L$ ≈ **16.61** Hz. The input capacitor dominates.

### Solution 12-04.6

The capacitor sees $1\ \text{k}\Omega \parallel 1/g_m = 1\ \text{k}\Omega \parallel 100\ \Omega$ = **90.91** Ω, so $C = 1/(2\pi \times 20\ \text{Hz} \times 90.91\ \Omega)$ = **87.54** µF: the small resistance forces a large capacitor.

### Solution 12-04.7

$b_1 = 100\ \text{k}\Omega(0.1\ \text{pF} + 2\ \text{pF} \times 101) + 50\ \text{k}\Omega \times 4\ \text{pF}$ = **20.41** µs. $b_2 = 100\ \text{k}\Omega \times 50\ \text{k}\Omega \times (0.2 + 4.2)\ \text{pF}^2$ = **2.2** × 10⁻¹⁴ s². The exact poles are at **7.798** kHz and **147.6** MHz; the simple estimates give **7.958** kHz and **144.7** MHz. The right-half-plane zero, $g_{m2}/(2\pi C_c)$ = **159.2** MHz, sits just above the second pole: it will add phase lag near the loop's crossover, which 12-06's nulling resistor fixes.

### Solution 12-04.8

$\Sigma = 100 \times 10 + 10 \times 2000 + 100 \times 2000$ fF² = **221 000** fF². $Q = \sqrt{2\ \text{mA/V} \times 20\ \text{k}\Omega \times \Sigma}/(100\ \text{fF} + 2\ \text{pF} + 400\ \text{fF})$ = **1.189**, $f_0$ = **107.1** MHz. $Q > 1/\sqrt2$: it will peak.

### Solution 12-04.9

With $C_L$ shorted, the drain is grounded, so $C_{gd}$ sees only $R_S$: $R_{gd}^L = R_S$, and $R_{L0}R_{gd}^L = R_LR_S$. With $C_{gd}$ shorted, $R_L^{gd} = 1/(1/R_L + 1/R_S + g_m) = R_SR_L/(R_S + R_L + g_mR_SR_L)$, so $R_{gd0}R_L^{gd} = (R_S + R_L + g_mR_SR_L) \cdot R_SR_L/(R_S + R_L + g_mR_SR_L) = R_SR_L$. Both equal $R_SR_L$ = **2** × 10⁸ Ω² for $R_S$ = 10 kΩ and $R_L$ = 20 kΩ.

### Solution 12-04.10

The input capacitor sees $R_S \parallel 1/g_m$ = 909.1 Ω: $\tau_{in}$ = **0.06606** ns. The output: $20\ \text{k}\Omega \times 106\ \text{fF}$ = **2.12** ns. Sum **2.186** ns, estimate **72.80** MHz, 3% below the exact 75.00 MHz: with one dominant node, OCTC is accurate.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-04.1a | R_A0 | 1 | kΩ |
| 12-04.1b | R_B0 | 2 | kΩ |
| 12-04.1c | sum of time constants | 3 | µs |
| 12-04.1d | OCTC estimate | 53.05 | kHz |
| 12-04.1e | first pole | 60.79 | kHz |
| 12-04.1f | second pole | 416.7 | kHz |
| 12-04.1g | exact −3 dB | 59.56 | kHz |
| 12-04.1h | estimate's shortfall | 11 | % |
| 12-04.2a | R_gd0 | 112 | kΩ |
| 12-04.3a | τ_gs | 0.25 | ns |
| 12-04.3b | τ_gd | 1.15 | ns |
| 12-04.3c | τ_L | 0.5 | ns |
| 12-04.3d | sum | 1.9 | ns |
| 12-04.3e | estimate | 83.77 | MHz |
| 12-04.3f | C_gd's share | 60.5 | % |
| 12-04.4a | R_gd with C_gs shorted | 10 | kΩ |
| 12-04.4b | R_L with C_gd shorted | 434.8 | Ω |
| 12-04.4c | b_2 | 1.75 × 10⁻¹⁹ | s² |
| 12-04.5a | input coupling 1/(RC) | 94.34 | rad/s |
| 12-04.5b | output coupling 1/(RC) | 10 | rad/s |
| 12-04.5c | sum | 104.3 | rad/s |
| 12-04.5d | low corner | 16.61 | Hz |
| 12-04.6a | resistance seen | 90.91 | Ω |
| 12-04.6b | bypass capacitance | 87.54 | µF |
| 12-04.7a | b_1 | 20.41 | µs |
| 12-04.7b | b_2 | 2.2 × 10⁻¹⁴ | s² |
| 12-04.7c | first pole, exact | 7.798 | kHz |
| 12-04.7d | second pole, exact | 147.6 | MHz |
| 12-04.7e | first pole, simple | 7.958 | kHz |
| 12-04.7f | second pole, simple | 144.7 | MHz |
| 12-04.7g | right-half-plane zero | 159.2 | MHz |
| 12-04.8a | Σ | 221000 | fF² |
| 12-04.8b | Q | 1.189 | — |
| 12-04.8c | f_0 | 107.1 | MHz |
| 12-04.9a | R_S R_L | 2 × 10⁸ | Ω² |
| 12-04.10a | τ_in | 0.06606 | ns |
| 12-04.10b | τ_out | 2.12 | ns |
| 12-04.10c | sum | 2.186 | ns |
| 12-04.10d | estimate | 72.80 | MHz |
| 12-04.10e | estimate's shortfall | 3 | % |
