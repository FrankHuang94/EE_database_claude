# Solutions 25-01 · Process Flow Overview: FEOL, MOL and BEOL

Problems: [25-01 problems](../problems/25-01-problems.md) · Chapter: [25-01](../chapters/25-01-process-flow-overview.md)

Every number is recomputed by [verify_25_01.py](../verify/verify_25_01.py).

---

## Solutions

### Solution 25-01.1

(a) $\pi \times (10\ \text{cm})^2$ = **314** cm² and $\pi \times (15\ \text{cm})^2$ = **707** cm².

(b) Cost per area scales as $1.5/2.25$ = **0.667**: a third cheaper per cm², before counting the smaller edge losses of the larger wafer (25-04). This is the economic engine behind every wafer-size transition.

### Solution 25-01.2

(a) $0.44 \times 15$ = **6.6** nm of silicon.

(b) $15 - 6.6$ = **8.4** nm above the original surface. When the pad oxide is later stripped, the silicon surface sits 6.6 nm lower than it started: a small step, but one that the process must plan for.

### Solution 25-01.3

(a) At 1373.15 K, $kT$ = 0.1183 eV: $B = 772\,e^{-1.23/0.1183}$ = **0.0236** µm²/h and $B/A = (6.23 \times 10^6/1.68)\,e^{-2.0/0.1183}$ = **0.169** µm/h, so $A$ = **0.139** µm.

(b) $\tau = (x_i^2 + Ax_i)/B = (0.025^2 + 0.139 \times 0.025)/0.0236$ = **0.174** h.

(c) $x = (A/2)\left[\sqrt{1 + 4B(t + \tau)/A^2} - 1\right]$ with $t + \tau$ = 1.174 h gives **0.111** µm, that is **111** nm.

The patch matters: without it ($\tau$ = 0) the same hour would give **99** nm, **12** nm less, because the model underestimates the fast initial growth.

### Solution 25-01.4

(a) $B = 386\,e^{-0.78/0.1183}$ = **0.529** µm²/h; $B/A = (1.63 \times 10^8/1.68)\,e^{-2.05/0.1183}$ = **2.90** µm/h.

(b) $t = 0.25/0.529 + 0.5/2.90$ = **0.644** h.

(c) $1.46/0.644$ = **2.27** times faster. The linear term gained more (activation energy 2.05 eV against 0.78 eV for $B$), so at 1100 °C growth of 500 nm is mostly parabolic.

### Solution 25-01.5

(a) At steady state the three fluxes are equal. From $F_3 = k_sC_i$, $C_i = F/k_s$; from $F_2$, $C_0 = C_i + Fx/D$; from $F_1$, $C^* = C_0 + F/h$. Adding,

$$
C^* = F\left(\frac{1}{k_s} + \frac{x}{D} + \frac{1}{h}\right) \quad\Longrightarrow\quad F = \frac{C^*}{1/k_s + 1/h + x/D} .
$$

Growth is $dx/dt = F/N_1$. Separating variables, $(1/k_s + 1/h + x/D)\,dx = (C^*/N_1)\,dt$. Integrating from $x_i$ at $t = 0$:

$$
\left(\frac{1}{k_s} + \frac{1}{h}\right)(x - x_i) + \frac{x^2 - x_i^2}{2D} = \frac{C^*}{N_1}\,t .
$$

Multiplying by $2D$: $x^2 + Ax = B(t + \tau)$ with $A = 2D(1/k_s + 1/h)$, $B = 2DC^*/N_1$ and $\tau = (x_i^2 + Ax_i)/B$, the thickness-equivalent of the starting oxide expressed as time.

(b) With $x_i = 0$, $t = (x^2 + Ax)/B = x^2/B + x\,(A/B) = x^2/B + x/(B/A)$. The terms are equal when $x^2/B = Ax/B$, that is at $x = A$.

(c) From Example 25-01.2, $A$ = **0.424** µm.

(d) At $x = A$ the oxide's diffusion resistance $x/D$ is twice the combined reaction and gas-transport resistance $1/k_s + 1/h$; the factor 2 appears because the time integrates a diffusion resistance that grew from zero, averaging $x/2D$. Below this thickness the interface reaction dominates the growth time; above it diffusion does. For wet oxidation at 1000 °C the crossover is about 0.4 µm, so thin and medium oxides are reaction-limited.

### Solution 25-01.6

(a) $t_{wf} = (14 - 3.0)/2 - 1.6$ = **3.9** nm.

(b) The second flavour needs 4.9 nm: $3.0 + 2(1.6 + 4.9)$ = **16.0** nm. Each extra nanometre of work-function metal costs two nanometres of trench, which is why multi-threshold menus get harder as gates shrink.

### Solution 25-01.7

(a) $80 \times 1.2$ = **96** days, **13.7** weeks.

(b) $84/80$ = **1.05** days per mask layer, near the best fabs' practice [R-020].

### Solution 25-01.8

(a) The area is $15 \times 10^{-7} \times 30 \times 10^{-7}$ cm² = 4.5 × 10⁻¹² cm², so $\rho_c \le 50 \times 4.5 \times 10^{-12}$ = **2.25e-10** Ω·cm².

(b) $1 - 1/(1 + 10^{-3} \times 50)$ = **4.8**%.

The required $\rho_c$ is a quarter of Example 25-01.5's 10⁻⁹ Ω·cm²; contact interfaces must keep improving just to hold the resistance budget as contacts shrink.

### Solution 25-01.9

(a) Copper: $(12 - 4)(24 - 2)$ = **176** nm². Ruthenium: $12 \times 24$ = **288** nm².

(b) $7.0 \times 10^{-8}\ \Omega\text{m}/288 \times 10^{-18}\ \text{m}^2$ = **243** Ω/µm.

(c) Equal resistance when $\rho_{Cu}/176 = 7.0/288$: $\rho_{Cu}$ = **4.28** µΩ·cm.

(d) Copper: $6.0 \times 10^{-8}/176 \times 10^{-18}$ = **341** Ω/µm, so ruthenium wins with **29**% lower resistance. The barrier takes 39% of copper's trench here, and that tax, not bulk resistivity (copper's 1.68 against ruthenium's 5.7–7.4 µΩ·cm, 04-05), decides the narrowest layers.

### Solution 25-01.10

(a) $R = 9.97 \times 2000$ Ω and $C$ = 400 fF: $0.379 \times 19.94\ \text{kΩ} \times 400\ \text{fF}$ = **3.02** ns, four times the 1 mm value.

(b) Local tier: $0.379 \times 148\ \text{kΩ} \times 400\ \text{fF}$ = **22.4** ns.

(c) Four 0.5 mm segments each take a sixteenth of the 2 mm delay: $4 \times 3.02/16$ = **0.755** ns. Real repeaters add their own delay, so the optimum number is finite (19-05).

### Solution 25-01.11

(a) $0.95^{1/1200}$ = **0.999957**: each step may lose only **4.27e-5** of wafers.

(b) $0.99995^{1200}$ = **0.942**.

### Solution 25-01.12

(a) 14 weeks is 3.22 months and 12 weeks 2.76 months: WIP falls from $50{,}000 \times 3.22$ = **1.61e5** to **1.38e5** wafers.

(b) **2.30e4** wafers released, worth **138** $M.

### Solution 25-01.13

(a) Worst-case supply rises from 0.70 V to 0.73 V. $f_2/f_1 = (0.43/0.40)^{1.3} \times (0.70/0.73)$ = **1.053**: **5.3**% faster.

(b) Intel reported "more than 5% frequency benefit in silicon due to reduced IR drop" on its PowerVia test chip [R-555]. The model is consistent with that size of gain, but the result depends entirely on how much IR drop the front-side design had: a design with little droop gains little.

### Solution 25-01.14

(a) $1/(0.5/1.6 + 0.3 + 0.2)$ = **1.23**.

(b) $1/(0.5/1.6 + 0.3/1.2 + 0.2)$ = **1.31**.

A 60% logic gain reports as 23% at chip level when SRAM and analog stand still; mixed figures compress logic progress.

### Solution 25-01.15

Solve $(0.3^2 + 0.3A)/B = 1.0$ h, with $A = B/(B/A)$, for $T$ numerically (bisection or Brent's method): $T$ = **968** °C, where $B$ = **0.262** µm²/h and $B/A$ = **0.457** µm/h. Check: $0.09/0.262 + 0.3/0.457$ = **1.00** h. ✓

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-01.1a | 200 mm wafer area | 314 | cm² |
| 25-01.1a1 | 300 mm wafer area | 707 | cm² |
| 25-01.1b | cost per area ratio | 0.667 | |
| 25-01.2a | silicon consumed | 6.6 | nm |
| 25-01.2b | oxide above original surface | 8.4 | nm |
| 25-01.3a0 | kT at 1100 C | 0.1183 | eV |
| 25-01.3a | B, dry 1100 C | 0.0236 | µm²/h |
| 25-01.3a1 | B/A, dry 1100 C (100) | 0.169 | µm/h |
| 25-01.3a2 | A, dry 1100 C | 0.139 | µm |
| 25-01.3b | tau | 0.174 | h |
| 25-01.3b1 | t + tau | 1.174 | h |
| 25-01.3c | thickness after 1 h | 0.111 | µm |
| 25-01.3c1 | thickness after 1 h | 111 | nm |
| 25-01.3d0 | thickness without the patch | 99 | nm |
| 25-01.3d | thickness lost without the patch | 12 | nm |
| 25-01.4a | B, wet 1100 C | 0.529 | µm²/h |
| 25-01.4a1 | B/A, wet 1100 C (100) | 2.90 | µm/h |
| 25-01.4b | time for 500 nm | 0.644 | h |
| 25-01.4c | speed-up over 1000 C | 2.27 | |
| 25-01.5c | crossover thickness A | 0.424 | µm |
| 25-01.6a | thickest work-function stack | 3.9 | nm |
| 25-01.6b | trench width for second flavour | 16.0 | nm |
| 25-01.7a | cycle time | 96 | days |
| 25-01.7a1 | cycle time in weeks | 13.7 | weeks |
| 25-01.7b | days per mask layer for 12 weeks | 1.05 | days |
| 25-01.8a0 | contact area | 4.5e-12 | cm² |
| 25-01.8a | specific contact resistivity | 2.25e-10 | Ω·cm² |
| 25-01.8b | drive loss | 4.8 | % |
| 25-01.8c | ratio to 1e-9 | 0.225 | |
| 25-01.9a | copper conducting area | 176 | nm² |
| 25-01.9a1 | ruthenium conducting area | 288 | nm² |
| 25-01.9b | ruthenium resistance | 243 | Ω/µm |
| 25-01.9c | crossover copper resistivity | 4.28 | µΩ·cm |
| 25-01.9d | copper resistance | 341 | Ω/µm |
| 25-01.9d1 | ruthenium advantage | 29 | % |
| 25-01.9d2 | barrier share of trench | 39 | % |
| 25-01.10a0 | 2 mm intermediate resistance | 19.94 | kΩ |
| 25-01.10a | 2 mm intermediate delay | 3.02 | ns |
| 25-01.10b0 | 2 mm local resistance | 148 | kΩ |
| 25-01.10b | 2 mm local delay | 22.4 | ns |
| 25-01.10c | with four repeated segments | 0.755 | ns |
| 25-01.11a | per-step yield | 0.999957 | |
| 25-01.11a1 | allowed loss per step | 4.27e-5 | |
| 25-01.11b | survival at 99.995% | 0.942 | |
| 25-01.12a0 | 14 weeks in months | 3.22 | months |
| 25-01.12a1 | 12 weeks in months | 2.76 | months |
| 25-01.12a | WIP before | 1.61e5 | wafers |
| 25-01.12a2 | WIP after | 1.38e5 | wafers |
| 25-01.12b | wafers released | 2.30e4 | wafers |
| 25-01.12b1 | inventory released | 138 | $M |
| 25-01.13a | frequency ratio | 1.053 | |
| 25-01.13a1 | frequency gain | 5.3 | % |
| 25-01.14a | mixed gain, SRAM flat | 1.23 | |
| 25-01.14b | mixed gain, SRAM 1.2x | 1.31 | |
| 25-01.15a | temperature | 968 | °C |
| 25-01.15b | B there | 0.262 | µm²/h |
| 25-01.15b1 | B/A there | 0.457 | µm/h |
| 25-01.15c | check time | 1.00 | h |
