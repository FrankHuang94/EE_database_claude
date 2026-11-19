# Solutions 09-03 · Carrier Transport: Drift and Diffusion

Problems: [09-03 problems](../problems/09-03-problems.md) · Chapter: [09-03](../chapters/09-03-drift-and-diffusion.md). Every number below is recomputed by [verify_09_03.py](../verify/verify_09_03.py): mobilities from the models, inversions by root finding, sheet resistances by integrating slice conductances, velocities from the fits, derivatives numerically, and built-in fields by solving the zero-current condition point by point.

---

## Solutions

### Solution 09-03.1

(a) $\mu_p = 48 + 402/[1 + (10^{16}/6.3\times10^{16})^{0.76}]$ = **370.4** cm²/V·s.

(b) $\tau = \mu m^*/q = 0.03704 \times 0.39 \times 9.109\times10^{-31}/1.602\times10^{-19}$ s = **0.0821** ps.

(c) $v_d = \mu\mathcal E = 370.4 \times 500$ = **1.852 × 10⁵** cm/s.

(d) $v_{th} = \sqrt{3kT/(0.39m_0)}$ = **1.870 × 10⁷** cm/s, so $\lambda = v_{th}\tau$ = **15.4** nm: holes scatter more often and travel shorter distances than electrons (45.5 nm in Example 09-03.1).

### Solution 09-03.2

(a) $1/\mu = 1/1430 + 1/3000$, so $\mu$ = **968.4** cm²/V·s.

(b) $1/\mu_I = 1/1000 - 1/1430$, so $\mu_I$ = **3326** cm²/V·s.

### Solution 09-03.3

$\rho(N) = 1/(qN\mu(N))$ falls monotonically with $N$, so bisection finds the unique root.

(a) n-type: $N_D$ = **4.61 × 10¹⁴** cm⁻³, $\mu_n$ = **1353** cm²/V·s.

(b) p-type: $N_A$ = **1.46 × 10¹⁵** cm⁻³, $\mu_p$ = **428.3** cm²/V·s. The p-type wafer needs about three times the doping for the same resistivity because holes are about three times less mobile.

### Solution 09-03.4

(a) $n = N_D - N_A$ = 10¹⁷ cm⁻³, but the mobility depends on the total $N_D + N_A$ = 3 × 10¹⁷ cm⁻³: $\mu_n$ = **495.8** cm²/V·s and $\rho = 1/(q \times 10^{17} \times 495.8)$ = **0.1259** Ω·cm.

(b) Uncompensated, $\mu_n(10^{17})$ = 801.3 cm²/V·s and $\rho$ = **0.0779** Ω·cm. Compensation raises the resistivity by **1.62** times at the same carrier density.

### Solution 09-03.5

(a) $50\,000/200$ = **250** squares; at 2 µm width the resistor is **500** µm long (folded into a serpentine in practice).

(b) $V = R_sI\ln2/\pi = 200 \times 10^{-3} \times 0.2206$ V = **44.13** mV.

### Solution 09-03.6

(a) Layers conduct in parallel: $1/R_s = q(\mu_1N_1t_1 + \mu_2N_2t_2)$. Top: $1.602\times10^{-19} \times 115.9 \times 10^{19} \times 0.2\times10^{-4}$ = **3.714 × 10⁻³** S; bottom: $1.602\times10^{-19} \times 801.3 \times 10^{17} \times 0.8\times10^{-4}$ = **1.027 × 10⁻³** S. So $R_s = 1/(4.741\times10^{-3})$ = **210.9** Ω/□.

(b) The thin, heavily doped top layer carries **78.3**% of the current despite its low mobility, because it has a hundred times the carriers.

(c) Alone: top **269.2** Ω/□, bottom **973.6** Ω/□.

### Solution 09-03.7

(a) From the hole fit at 300 K ($v_s$ = 8.34 × 10⁶ cm/s, $\mathcal E_c$ = 1.80 × 10⁴ V/cm, $\beta$ = 1.21): **3.34 × 10⁶** cm/s at 10⁴ V/cm, **7.57 × 10⁶** cm/s at 10⁵ V/cm and **7.99 × 10⁶** cm/s at 2 × 10⁵ V/cm.

(b) 1 V over 50 nm is 2 × 10⁵ V/cm: holes cross in $50\times10^{-7}/7.99\times10^6$ = **0.626** ps; electrons, at **1.048 × 10⁷** cm/s, take **0.477** ps. At this field the two carriers differ by only 31% in speed, far less than their threefold difference in low-field mobility: velocity saturation narrows the NMOS–PMOS gap in short channels.

### Solution 09-03.8

(a) $\mu_p(10^{17})$ = **214.1** cm²/V·s, so $D_p = 0.025852 \times 214.1$ = **5.534** cm²/s.

(b) $\sqrt{5.534 \times 10^{-7}}$ cm = **7.44** µm.

(c) $kT/q$ = **34.47** mV at 400 K: the Einstein ratio $D/\mu$ grows in proportion to $T$, by a third, though $\mu$ itself falls with temperature.

### Solution 09-03.9

(a) $dn/dx = -n/L$, so $J_n = qD_n\,dn/dx = -qD_nn/L$. With $D_n$ = 34.77 cm²/s (Example 09-03.6): at $x = 0$, $J_n = -1.602\times10^{-19} \times 34.77 \times 10^{15}/10^{-3}$ = **−5.571** A/cm²; at $x = 2L$ it is $e^{-2}$ times that, **−0.754** A/cm².

(b) Electrons diffuse toward $+x$ (lower density), so the current flows toward $-x$.

### Solution 09-03.10

(a) Zero electron current with $n = N_D(x)$ requires $\mathcal E = -(kT/q)(1/N_D)(dN_D/dx)$. Here $dN_D/dx = (10^{16} - 10^{17})/10^{-4} = -9\times10^{20}$ cm⁻⁴, so $\mathcal E = +0.025852 \times 9\times10^{20}/N_D$: **232.7** V/cm at $x = 0$, **423.0** V/cm at the midpoint ($N_D$ = 5.5 × 10¹⁶ cm⁻³) and **2327** V/cm at 1 µm. It points toward $+x$, the lightly doped side, and grows as the doping falls.

(b) $\Delta V = \int\mathcal E\,dx = (kT/q)\ln(N_D(0)/N_D(1\ \mu\text{m})) = 0.025852\ln10$ = **59.5** mV, independent of the shape of the profile: the potential difference depends only on the end-point doping ratio.

### Solution 09-03.11

(a) $R \propto 1/\mu \propto T^{2.2}$, so $d\ln R/dT = 2.2/T$ = **7333** ppm/K at 300 K.

(b) With $\mu_I(300\ \text{K})$ = 1823 cm²/V·s (Example 09-03.4) and $\mu_L(300\ \text{K})$ = 1430 cm²/V·s, differentiating $1/\mu = 1/\mu_L + 1/\mu_I$ numerically gives $d\ln R/dT$ = **1911** ppm/K: a quarter of the lightly doped value.

### Solution 09-03.12

(a) $\frac{d}{dT}\left(\frac1\mu\right) = \frac{2.2}{T\mu_L} - \frac{1.5}{T\mu_I} = 0$ requires $\mu_I/\mu_L = 1.5/2.2$ = **0.682**, so $\mu_I$ = **975.0** cm²/V·s at 300 K.

(b) $\mu = 1/(1/1430 + 1/975)$ = **579.7** cm²/V·s.

(c) Solving $\mu_n(N) = 579.7$ in the course model: $N$ ≈ **2.18 × 10¹⁷** cm⁻³.

(d) The result depends on assumed exponents (−2.2 and +1.5), on the mobility fit (which differs between sources by several percent for electrons, §3.3), and on the temperature: the cancellation holds only near 300 K. Real low-tempco resistors are tuned on silicon and measured over temperature.

### Solution 09-03.13

(a) $v_{th}$ = 2.29 × 10⁷ cm/s and $\lambda$ = 45.5 nm, so $D = v_{th}\lambda/3$ = **34.77** cm²/s: the same as the Einstein value, 34.77 cm²/s.

(b) $D = v_{th}\lambda/3 = v_{th}^2\tau/3 = (3kT/m^*)\tau/3 = kT\tau/m^* = (kT/q)(q\tau/m^*) = (kT/q)\mu$.

(c) Both rest on the same model: the thermal speed from equipartition and the same scattering time define both the random walk and the drift, so they must agree. The Einstein relation is more general, because it follows from equilibrium statistics alone, whatever the scattering details.

### Solution 09-03.14

(a) $n = IB/(qt|V_H|) = 10^{-3} \times 0.5/(1.602\times10^{-19} \times 5\times10^{-4} \times 6.24\times10^{-3})$ m⁻³ = **1.00 × 10¹⁵** cm⁻³, and $|R_H| = |V_H|t/(IB)$ = **6240** cm³/C (equivalently $1/(qn)$).

(b) $\mu_H = |R_H|/\rho = 6240/4.7$ = **1328** cm²/V·s.

(c) The course model gives **1345** cm²/V·s at 10¹⁵ cm⁻³, so the implied Hall factor is $1328/1345$ = **0.987**, within the range expected; quoting the Hall mobility as the drift mobility here would be off by about 1%.

### Solution 09-03.15

(a) Inverting the fits numerically for $v_d$ = 5 × 10⁶ cm/s: electrons need **5.41 × 10³** V/cm, or **2.71** V across 5 µm; holes need **2.03 × 10⁴** V/cm, or **10.2** V.

(b) At saturation, electrons take $5\times10^{-4}/1.071\times10^7$ = **46.7** ps and holes $5\times10^{-4}/8.34\times10^6$ = **59.9** ps.

(c) Holes: they need nearly four times the field. Fast photodiodes are often designed so that the slower carrier has the shorter path, or are biased well into saturation for both.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-03.1a | hole mobility at 1e16 | 370.4 | cm²/V·s |
| 09-03.1b | hole mean free time | 0.0821 | ps |
| 09-03.1c | hole drift velocity at 500 V/cm | 1.852e5 | cm/s |
| 09-03.1d | hole thermal velocity | 1.870e7 | cm/s |
| 09-03.1e | hole mean free path | 15.4 | nm |
| 09-03.2a | combined mobility | 968.4 | cm²/V·s |
| 09-03.2b | impurity mobility for 1000 | 3326 | cm²/V·s |
| 09-03.3a | n-type doping for 10 Ω·cm | 4.61e14 | cm⁻³ |
| 09-03.3b | μ_n at that doping | 1353 | cm²/V·s |
| 09-03.3c | p-type doping for 10 Ω·cm | 1.46e15 | cm⁻³ |
| 09-03.3d | μ_p at that doping | 428.3 | cm²/V·s |
| 09-03.4a | μ_n at 3e17 | 495.8 | cm²/V·s |
| 09-03.4b | ρ, compensated | 0.1259 | Ω·cm |
| 09-03.4c | ρ, uncompensated | 0.0779 | Ω·cm |
| 09-03.4d | resistivity ratio | 1.62 | — |
| 09-03.5a | squares for 50 kΩ | 250 | — |
| 09-03.5b | resistor length | 500 | µm |
| 09-03.5c | four-point-probe voltage | 44.13 | mV |
| 09-03.6a | top-layer sheet conductance | 3.714e-3 | S |
| 09-03.6b | bottom-layer sheet conductance | 1.027e-3 | S |
| 09-03.6c | stack sheet resistance | 210.9 | Ω/□ |
| 09-03.6d | top-layer current fraction | 78.3 | % |
| 09-03.6e | top layer alone | 269.2 | Ω/□ |
| 09-03.6f | bottom layer alone | 973.6 | Ω/□ |
| 09-03.7a | hole v at 1e4 V/cm | 3.34e6 | cm/s |
| 09-03.7b | hole v at 1e5 V/cm | 7.57e6 | cm/s |
| 09-03.7c | hole v at 2e5 V/cm | 7.99e6 | cm/s |
| 09-03.7d | hole transit time, 50 nm | 0.626 | ps |
| 09-03.7e | electron v at 2e5 V/cm | 1.048e7 | cm/s |
| 09-03.7f | electron transit time, 50 nm | 0.477 | ps |
| 09-03.7g | electron speed advantage | 31 | % |
| 09-03.8a | μ_p at 1e17 | 214.1 | cm²/V·s |
| 09-03.8b | D_p | 5.534 | cm²/s |
| 09-03.8c | hole diffusion distance in 100 ns | 7.44 | µm |
| 09-03.8d | kT/q at 400 K | 34.47 | mV |
| 09-03.9a | J_n at x = 0 | -5.571 | A/cm² |
| 09-03.9b | J_n at x = 2L | -0.754 | A/cm² |
| 09-03.10a | dN_D/dx | -9e20 | cm⁻⁴ |
| 09-03.10b | field at x = 0 | 232.7 | V/cm |
| 09-03.10c | field at the midpoint | 423.0 | V/cm |
| 09-03.10d | field at 1 µm | 2327 | V/cm |
| 09-03.10e | potential difference | 59.5 | mV |
| 09-03.11a | TCR, lattice-limited | 7333 | ppm/K |
| 09-03.11b | TCR at 1e17 | 1911 | ppm/K |
| 09-03.12a | required μ_I/μ_L | 0.682 | — |
| 09-03.12b | μ_I at zero TCR | 975.0 | cm²/V·s |
| 09-03.12c | mobility at zero TCR | 579.7 | cm²/V·s |
| 09-03.12d | doping for zero TCR | 2.18e17 | cm⁻³ |
| 09-03.13a | D from kinetic theory | 34.77 | cm²/s |
| 09-03.14a | electron density from Hall | 1.00e15 | cm⁻³ |
| 09-03.14b | Hall coefficient magnitude | 6240 | cm³/C |
| 09-03.14c | Hall mobility | 1328 | cm²/V·s |
| 09-03.14d | drift mobility from the model | 1345 | cm²/V·s |
| 09-03.14e | Hall factor | 0.987 | — |
| 09-03.15a | field for electrons | 5.41e3 | V/cm |
| 09-03.15b | voltage for electrons | 2.71 | V |
| 09-03.15c | field for holes | 2.03e4 | V/cm |
| 09-03.15d | voltage for holes | 10.2 | V |
| 09-03.15e | shortest electron crossing | 46.7 | ps |
| 09-03.15f | shortest hole crossing | 59.9 | ps |
