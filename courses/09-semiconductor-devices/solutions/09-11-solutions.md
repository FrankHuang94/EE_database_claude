# Solutions 09-11 · CMOS and Scaling: Moore, Dennard and Beyond

Problems: [09-11 problems](../problems/09-11-problems.md) · Chapter: [09-11](../chapters/09-11-cmos-and-scaling.md). Every number below is recomputed by [verify_09_11.py](../verify/verify_09_11.py), by these routes:

- switching thresholds by solving current balance numerically;
- frequencies, energies and optima by root finding and numerical minimization;
- depletion widths by solving for $\phi_B$ from the carrier statistics;
- scaling factors from a device model evaluated before and after scaling.

---

## Solutions

### Solution 09-11.1

With $\sqrt r$ = 2: $V_M = (0.3 \times 2 + 0.7)/3$ = **0.4333** V. For $V_M$ = 0.45 V:

$$
0.3\sqrt r + 0.7 = 0.45(1 + \sqrt r) \;\Rightarrow\; \sqrt r = \frac{0.25}{0.15},\quad r = \mathbf{2.78} .
$$

A stronger NMOS pulls the switching point down, but slowly: quadrupling $r$ moves $V_M$ by only 67 mV from the symmetric point.

### Solution 09-11.2

$\tau_d \propto CV_{DD}/I_{on}$, so the factor is 0.7 × (0.75/0.80)/0.95 = **0.691**: a 31% faster gate, mostly from the smaller capacitance.

### Solution 09-11.3

$T = 2N\tau_d$, so $\tau_d = 1/(2 \times 51 \times 2.5\times10^9)$ = **3.92** ps. With equal on-currents, $\tau_d = CV_{DD}/2I_{on}$, so

$$
I_{on} = \frac{CV_{DD}}{2\tau_d} = \frac{0.8\times10^{-15} \times 0.7}{2 \times 3.92\times10^{-12}} = \mathbf{71.4}\text{ µA} .
$$

### Solution 09-11.4

$f \propto (V_{DD} - V_t)/V_{DD}$, so $f(0.8) = 3 \times (0.5/0.8)/(0.7/1.0)$ = **2.68** GHz. Dynamic power scales as $V_{DD}^2f$: 10 × 0.64 × (2.68/3) = **5.71** W. The energy per cycle scales as $V_{DD}^2$: **0.64**.

Giving up 11% of the frequency saves 43% of the power: the reason every modern processor uses dynamic voltage and frequency scaling.

### Solution 09-11.5

At 1.0 V: $E$ = 10⁻¹⁰ × 1 + 1.0 × 0.1/(2 × 10⁹) = **1.50 × 10⁻¹⁰** J. Lowering $V_{DD}$ shrinks the switching term but slows the clock, so each cycle carries more leakage energy. Minimizing numerically gives $V_{DD}$ = **0.458** V, $E_{\min}$ = **6.74 × 10⁻¹¹** J, at **0.985** GHz: a saving of **2.22**×.

The optimum lies only 0.16 V above threshold. Pushing lower would need a subthreshold current model (09-09 §3.7), in which the frequency falls exponentially and the leakage term rises steeply, so the true optimum stays near this region.

### Solution 09-11.6

$T_2 = 20 \ln 2/\ln 500$ = **2.23** years, an annual growth rate of $2^{1/2.23} - 1$ = **36.4**%. At a two-year doubling, 10 years gives 2⁵ = **32**×.

### Solution 09-11.7

(a) $\phi_B = V_T\ln(10^{16}/10^{10})$ = **0.3572** V and $W_{d\max} = \sqrt{2\varepsilon_s(2\phi_B)/qN_A}$ = **0.304** µm.

(b) At 5 × 10¹⁶ cm⁻³: $\phi_B$ = **0.3988** V and $W_{d\max}$ = **0.1436** µm, a ratio of **0.473**, not 0.2. The band bending at threshold did not scale (it grew), so the width shrank only by about $1/\sqrt5$.

(c) Root finding gives $N_A$ = **3.12 × 10¹⁷** cm⁻³, **31.2** times the original: more than $\kappa^2$ = 25, because $\phi_B$ keeps rising with doping. Heavier doping in turn costs mobility, junction leakage and variability (09-10).

### Solution 09-11.8

The generalized result gives a power-density factor of $\kappa^2/u^2$ per node. With $\kappa$ = 1/0.7 and $u$ = 1/0.9: (0.9/0.7)² = **1.65** per node and **4.52** over three nodes. With constant voltage: $\kappa^6$ = **8.50**.

### Solution 09-11.9

(a) Full-speed dynamic power: 10⁹ × 0.15 × 0.5 × 10⁻¹⁵ × 0.7² × 3 × 10⁹ = **110** W, so only 60/110 = **0.544** of the gates can switch at full speed.

(b) At 0.6 V and 2.4 GHz: **64.8** W, and the fraction rises to **0.926**.

Trading 20% of the clock for a 14% lower supply lets nearly the whole chip run.

### Solution 09-11.10

Cell height: 120 nm × 20/22 = 109.1 nm, so CPP × cell height = 46 × 109.1 = **5,018** nm². The density gain is 5,760/5,018 = **1.15** over "2nm" and 7,680/5,018 = **1.53** over "3nm".

### Solution 09-11.11

Each transistor's off-current rises by $10^{0.030/0.080}$ = **2.37**. Die leakage power: 2 (count) × 2.37 × 0.95 (supply) = **4.51**.

Even a modest threshold cut at constant area multiplies leakage power several-fold, which is why thresholds stopped scaling.

### Solution 09-11.12

(a) At $V_{ov}$ = 0.55 V the 09-10 model gives $I_{onN}$ = **0.389** mA/µm and $I_{onP}$ = **0.181** mA/µm. Equal delays need $W_p/W_n = I_{onN}/I_{onP}$ = **2.15**.

(b) At $V_M$ = 0.4 V both have $V_{ov}$ = 0.15 V, and both are saturated ($V_{Dsat}$ ≈ 0.1 V < 0.4 V). The per-width saturation currents are **46.1** and **17.5** µA/µm, so $W_p/W_n$ = **2.63**.

(c) Both are below the mobility ratio of 3. Velocity saturation compresses the NMOS advantage most at high overdrive, so the equal-delay ratio (2.15) is closest to Hu's "about two"; near threshold the devices are closer to long-channel and the ratio approaches 3.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-11.1a | V_M, r = 4 | 0.4333 | V |
| 09-11.1b | r for V_M = 0.45 V | 2.78 | — |
| 09-11.1c | shift of V_M from 0.5 V | 67 | mV |
| 09-11.2a | delay factor | 0.691 | — |
| 09-11.3a | τ_d | 3.92 | ps |
| 09-11.3b | I_on | 71.4 | µA |
| 09-11.4a | f at 0.8 V | 2.68 | GHz |
| 09-11.4b | power at 0.8 V | 5.71 | W |
| 09-11.4c | energy-per-cycle ratio | 0.64 | — |
| 09-11.5a | E at 1.0 V | 1.50e-10 | J |
| 09-11.5b | optimum V_DD | 0.458 | V |
| 09-11.5c | minimum E | 6.74e-11 | J |
| 09-11.5d | f at optimum | 0.985 | GHz |
| 09-11.5e | saving factor | 2.22 | — |
| 09-11.6a | doubling time | 2.23 | years |
| 09-11.6b | annual growth | 36.4 | % |
| 09-11.6c | growth in 10 years | 32 | — |
| 09-11.7a | φ_B at 1e16 | 0.3572 | V |
| 09-11.7b | W_dmax at 1e16 | 0.304 | µm |
| 09-11.7c | φ_B at 5e16 | 0.3988 | V |
| 09-11.7d | W_dmax at 5e16 | 0.1436 | µm |
| 09-11.7e | width ratio | 0.473 | — |
| 09-11.7f | doping for full scaling | 3.12e17 | cm⁻³ |
| 09-11.7g | doping factor | 31.2 | — |
| 09-11.8a | per node, u = 1/0.9 | 1.65 | — |
| 09-11.8b | three nodes, u = 1/0.9 | 4.52 | — |
| 09-11.8c | three nodes, constant V | 8.50 | — |
| 09-11.9a | full-speed power | 110 | W |
| 09-11.9b | active fraction | 0.544 | — |
| 09-11.9c | power at 0.6 V, 2.4 GHz | 64.8 | W |
| 09-11.9d | active fraction there | 0.926 | — |
| 09-11.10a | cell height | 109.1 | nm |
| 09-11.10b | pitch product | 5018 | nm² |
| 09-11.10c | gain over 2nm | 1.15 | — |
| 09-11.10d | gain over 3nm | 1.53 | — |
| 09-11.11a | off-current factor | 2.37 | — |
| 09-11.11b | leakage power factor | 4.51 | — |
| 09-11.12a | I_onN | 0.389 | mA/µm |
| 09-11.12b | I_onP | 0.181 | mA/µm |
| 09-11.12c | W_p/W_n, equal delays | 2.15 | — |
| 09-11.12d | NMOS current at V_M | 46.1 | µA/µm |
| 09-11.12e | PMOS current at V_M | 17.5 | µA/µm |
| 09-11.12f | W_p/W_n for V_M = V_DD/2 | 2.63 | — |
