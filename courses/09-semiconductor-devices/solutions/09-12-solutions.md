# Solutions 09-12 · Advanced Transistors: FinFET, GAA, CFET and Backside Power

Problems: [09-12 problems](../problems/09-12-problems.md) · Chapter: [09-12](../chapters/09-12-finfet-gaa-cfet-backside-power.md). Every number below is recomputed by [verify_09_12.py](../verify/verify_09_12.py), by these routes:

- scale lengths by solving the parabolic-potential boundary-value problems numerically;
- threshold shifts and DIBL by solving the center-potential equation by finite differences;
- IR drops by solving resistor ladders;
- confinement energies from the constants in SciPy.

---

## Solutions

### Solution 09-12.1

$W_{\text{eff}}$ = 2 × 45 + 7 = **97** nm. For 400 nm the transistor needs ⌈400/97⌉ = **5** fins, giving **485** nm: 21% more than asked, because widths come in whole fins.

### Solution 09-12.2

$\lambda^2 = (3/2)(6)(0.8) + 36/8$ = 7.2 + 4.5 = 11.7 nm², so $\lambda$ = **3.42** nm.

### Solution 09-12.3

(a) Let the gate potential be $V_G'$ and $C_{ox} = \varepsilon_{ox}/t_{ox}$. In the oxide (above $y$ = 0) the potential rises linearly from $c_0$ at the surface to $V_G'$, so continuity of $\varepsilon\mathcal E$ at $y$ = 0 gives

$$
\varepsilon_s\frac{\partial\phi}{\partial y}\Big|_0 = \varepsilon_sc_1 = C_{ox}(c_0 - V_G') .
$$

Zero normal field at the back, $\partial\phi/\partial y = c_1 + 2c_2t_{si} = 0$, gives $c_2 = -c_1/2t_{si}$. The back-surface potential is $\phi_b = c_0 + c_1t_{si} + c_2t_{si}^2 = c_0 + c_1t_{si}/2$. Substituting $c_1$:

$$
\phi_b - V_G' = (c_0 - V_G')\Big(1 + \frac{C_{ox}t_{si}}{2\varepsilon_s}\Big) .
$$

Laplace's equation at the back surface, $\partial^2\phi_b/\partial x^2 + 2c_2 = 0$, gives

$$
\frac{d^2\phi_b}{dx^2} = -2c_2 = \frac{c_1}{t_{si}} = \frac{C_{ox}(c_0 - V_G')}{\varepsilon_st_{si}} = \frac{\phi_b - V_G'}{\lambda^2},\qquad
\lambda^2 = \frac{\varepsilon_st_{si}}{C_{ox}}\Big(1 + \frac{C_{ox}t_{si}}{2\varepsilon_s}\Big) = \frac{\varepsilon_s}{\varepsilon_{ox}}t_{si}t_{ox} + \frac{t_{si}^2}{2} .
$$

(b) With a 1 nm oxide: $\lambda$ = **6.745** nm at 7 nm and **4.472** nm at 4 nm. The double-gate value at 4 nm is **2.828** nm, so the single gate's scale length is **1.581** times longer.

### Solution 09-12.4

With $\lambda$ = 3.42 nm, solving $\text{DIBL}(L)$ = 30 mV/V with the exact barrier minimum gives $L$ = **20.6** nm, $L/\lambda$ = **6.03**: the "about six scale lengths" of Example 09-12.5.

### Solution 09-12.5

$T_{si}$ = 10 nm: $\lambda^2 = (3/2)(10)(1) + 100/8$ = 27.5, so $\lambda$ = **5.24** nm, $L/\lambda$ = **3.81** and DIBL = **83.7** mV/V. Root finding gives DIBL = 50 mV/V at $T_{si}$ = **6.86** nm, where $\lambda$ = **4.02** nm. Hu's rule gets the thin body into the useful range; the DIBL target needs a body about a third thinner.

### Solution 09-12.6

(a) $4 \times 2 \times (25 + 5)$ = **240** nm and $3 \times 2 \times (35 + 5)$ = **240** nm: two stacks with different footprints and heights give the same width.

(b) One fin gives 106 nm, so 240 nm needs **2.26** fins. The whole-fin choices give **212** nm (2 fins, 12% short) or **318** nm (3 fins, 32.5% over).

### Solution 09-12.7

$S = mV_T\ln 10$ = **62.5** mV/decade at 300 K and **74.6** mV/decade at 358.15 K. At a fixed threshold the off-current rises by $10^{0.25/0.0625 - 0.25/0.0746}$ = **4.46**.

### Solution 09-12.8

(a) Fed from one end, the current still flowing at distance $x$ is $I(1 - x/\ell)$, and the rail resistance per length is $R/\ell$:

$$
\Delta V_{\max} = \int_0^\ell I\Big(1 - \frac{x}{\ell}\Big)\frac{R}{\ell}\,dx = \frac{IR}{2} .
$$

Fed from both ends, by symmetry each half carries current $I/2$ over resistance $R/2$ and is fed from one end, so $\Delta V_{\max} = (I/2)(R/2)/2 = IR/8$.

(b) $IR/2$ = **60.0** mV and $IR/8$ = **15.0** mV.

### Solution 09-12.9

6 × 24 = **144** nm and 5 × 24 = **120** nm, a density gain of **1.20** at the same gate pitch.

### Solution 09-12.10

| Per-node area gain | Area after six nodes | Density gain |
|---|---|---|
| 20% | **0.262** | **3.81** |
| 25% | **0.178** | **5.62** |
| Classical halving | **0.0156** | **64** |

At the roadmap's pace, six nodes give 4–6× the density that classical scaling would have delivered in about two nodes.

### Solution 09-12.11

$E_1 = h^2/8m_lt_{si}^2$ with $m_l$ = 0.98 $m_0$:

- **15.3** meV at 5 nm;
- **24.0** meV at 4 nm;
- **42.6** meV at 3 nm.

From 5 to 4 nm the subband rises by **8.63** meV. Since $E_1 \propto t_{si}^{-2}$, $|dE_1/dt_{si}| = 2E_1/t_{si}$: **6.14** meV/nm at 5 nm and **28.4** meV/nm at 3 nm.

The threshold rises with the subband energy, so in a 3 nm body a ±0.3 nm thickness variation moves $V_t$ by roughly ±9 mV. Thin bodies trade random dopant fluctuation (09-10) for thickness fluctuation.

### Solution 09-12.12

Side-by-side: 18 + 30 + 40 + 30 + 18 = **136** nm. CFET devices: 18 + 30 + 18 = **66** nm, but 4 tracks need 4 × 18 = **72** nm, so the cell is 72 nm. The density gain is 136/72 = **1.89**, not the 2.06 the devices alone would suggest: wiring, not transistors, now limits the cell.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-12.1a | W_eff per fin | 97 | nm |
| 09-12.1b | fins needed | 5 | — |
| 09-12.1c | resulting width | 485 | nm |
| 09-12.1d | excess width | 21 | % |
| 09-12.2a | λ | 3.42 | nm |
| 09-12.3a | λ, single gate 7 nm | 6.745 | nm |
| 09-12.3b | λ, single gate 4 nm | 4.472 | nm |
| 09-12.3c | λ, double gate 4 nm | 2.828 | nm |
| 09-12.3d | ratio | 1.581 | — |
| 09-12.4a | L for 30 mV/V | 20.6 | nm |
| 09-12.4b | L/λ | 6.03 | — |
| 09-12.5a | λ at 10 nm body | 5.24 | nm |
| 09-12.5b | L/λ | 3.81 | — |
| 09-12.5c | DIBL | 83.7 | mV/V |
| 09-12.5d | body for 50 mV/V | 6.86 | nm |
| 09-12.5e | λ there | 4.02 | nm |
| 09-12.6a | four-sheet width | 240 | nm |
| 09-12.6b | three-sheet width | 240 | nm |
| 09-12.6c | fins to match | 2.26 | — |
| 09-12.6d | two-fin width | 212 | nm |
| 09-12.6e | three-fin width | 318 | nm |
| 09-12.6f | two-fin shortfall | 12 | % |
| 09-12.6g | three-fin excess | 32.5 | % |
| 09-12.7a | S at 300 K | 62.5 | mV/decade |
| 09-12.7b | S at 85 °C | 74.6 | mV/decade |
| 09-12.7c | off-current factor | 4.46 | — |
| 09-12.8a | drop, one end | 60.0 | mV |
| 09-12.8b | drop, both ends | 15.0 | mV |
| 09-12.9a | old cell height | 144 | nm |
| 09-12.9b | new cell height | 120 | nm |
| 09-12.9c | density gain | 1.20 | — |
| 09-12.10a | area, 20% per node | 0.262 | — |
| 09-12.10b | density, 20% per node | 3.81 | — |
| 09-12.10c | area, 25% per node | 0.178 | — |
| 09-12.10d | density, 25% per node | 5.62 | — |
| 09-12.10e | area, halving | 0.0156 | — |
| 09-12.10f | density, halving | 64 | — |
| 09-12.11a | E_1 at 5 nm | 15.3 | meV |
| 09-12.11b | E_1 at 4 nm | 24.0 | meV |
| 09-12.11c | E_1 at 3 nm | 42.6 | meV |
| 09-12.11d | shift 5 to 4 nm | 8.63 | meV |
| 09-12.11e | slope at 5 nm | 6.14 | meV/nm |
| 09-12.11f | slope at 3 nm | 28.4 | meV/nm |
| 09-12.11g | V_t change for 0.3 nm at 3 nm | 9 | mV |
| 09-12.12a | side-by-side height | 136 | nm |
| 09-12.12b | CFET device height | 66 | nm |
| 09-12.12c | track-limited height | 72 | nm |
| 09-12.12d | density gain | 1.89 | — |
| 09-12.12e | device-only gain | 2.06 | — |
