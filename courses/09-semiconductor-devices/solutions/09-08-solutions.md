# Solutions 09-08 · The MOS Capacitor

Problems: [09-08 problems](../problems/09-08-problems.md) · Chapter: [09-08](../chapters/09-08-mos-capacitor.md). Every number below is recomputed by [verify_09_08.py](../verify/verify_09_08.py), by these routes:

- band positions from Boltzmann densities;
- depletion widths by root finding on the voltage balance;
- exact charges by integrating Poisson's equation numerically;
- capacitances by numerical differentiation of the computed charge;
- design values by root finding.

---

## Solutions

### Solution 09-08.1

$V_{fb} = \psi_g - \psi_s$.

(a) $E_C - E_F = 1.12 - V_T\ln(1.8\times10^{19}/10^{16})$ = 0.9262 eV, so $V_{fb} = 4.05 - (4.05 + 0.9262)$ = **−0.9262** V.

(b) For the n-body, $E_C - E_F = V_T\ln(3.2\times10^{19}/10^{17})$ = 0.1491 eV, so $\psi_s$ = 4.199 V and $V_{fb} = 5.17 - 4.199$ = **0.9709** V.

(c) $V_{fb} = 4.6 - 4.976$ = **−0.3762** V. A mid-gap metal gives a flat band between those of n⁺ and p⁺ poly.

### Solution 09-08.2

(a) $C_{ox} = 3.453\times10^{-13}/3\times10^{-7}$ = **1151** nF/cm².

(b) EOT = 0.6 + 4 × 3.9/21.2 = **1.336** nm, so $C$ = **2585** nF/cm².

(c) The stack is 4.6 nm thick against 3 nm, **1.53** times thicker, yet it has **2.25** times the capacitance.

### Solution 09-08.3

$C_{ox}$ = **690.6** nF/cm². $Q_{acc} = -C_{ox}(V_g - V_{fb})$ = +**1.036 × 10⁻⁶** C/cm², which is **6.47 × 10¹²** holes per cm².

### Solution 09-08.4

Solve $V_g = V_{fb} + qN_AW^2/2\varepsilon_s + qN_AW/C_{ox}$:

- at −0.5 V, $W$ = **54.7** nm and $\phi_s$ = **0.232** V;
- at +0.2 V, $W$ = **97.4** nm and $\phi_s$ = **0.734** V.

Both are below the threshold surface potential of 0.833 V.

### Solution 09-08.5

With $C_{ox}$ = 1151 nF/cm²:

| $N_A$ (cm⁻³) | $V_{fb}$ (V) | $V_t$ (V) |
|---|---|---|
| 10¹⁶ | **−0.9262** | **−0.1696** |
| 10¹⁷ | **−0.9858** | **−0.0079** |
| 10¹⁸ | **−1.0453** | **0.3956** |

At thin oxides the depletion-charge term shrinks ($C_{ox}$ is large), so an n⁺ gate needs very heavy body doping to reach a positive threshold, at the cost of mobility, junction capacitance and dopant fluctuation. That is why advanced processes tune thresholds with gate work function (metal gates, dipole layers) rather than doping.

### Solution 09-08.6

Root finding on $V_t(N_A)$ = 0.4 V gives $N_A$ = **1.015 × 10¹⁸** cm⁻³.

### Solution 09-08.7

$\phi_B = V_T\ln(10^{17}/10^{10})$ = **0.4167** V. $V_{fb}$ = **0.9709** V (Solution 09-08.1(b)). Then

$$
V_t = 0.9709 - 0.8334 - \frac{\sqrt{2qN_D\varepsilon_s(0.8334)}}{1151\text{ nF/cm}^2} = \mathbf{-0.0070}\text{ V} ,
$$

the mirror image of the n-channel case.

### Solution 09-08.8

(a) $C_{ox}$ = **1.727** µF/cm², $Q_{inv} = C_{ox} \times 0.8$ V = **1.381 × 10⁻⁶** C/cm², and $n_s$ = **8.62 × 10¹²** cm⁻².

(b) $R_\square = 1/(qn_s\mu_n)$ = **2896** Ω/□. A channel 10 squares long (L/W = 10) would have **29.0** kΩ.

### Solution 09-08.9

Root finding on $V_g = V_{fb} + \phi_s - Q_s/C_{ox}$ with the exact $Q_s$:

| $V_g - V_t$ | $\phi_s$ (V) | exact $Q_{inv}$ (C/cm²) | sheet $C_{ox}(V_g - V_t)$ | ratio |
|---|---|---|---|---|
| 0.5 V | **0.9432** | **1.265 × 10⁻⁷** | **1.727 × 10⁻⁷** | **0.733** |
| 1.5 V | **0.9899** | **4.514 × 10⁻⁷** | **5.180 × 10⁻⁷** | **0.871** |

The sheet model overestimates the inversion charge most near threshold. The deficit is roughly a fixed offset in gate voltage (the extra depletion charge and band bending), so the ratio approaches 1 far above threshold.

### Solution 09-08.10

(a) $C_{ox}$ = **690.6** nF/cm² and $V_{fb}$ = **−0.9678** V.

(b) $L_D$ = **18.28** nm, so $C_{FB} = (1/C_{ox} + L_D/\varepsilon_s)^{-1}$ = **311.2** nF/cm².

(c) $W_{d\max}$ = **143.6** nm and $C_{\min}$ = **65.31** nF/cm².

(d) At $V_g$ = 0 the depletion width is **143.9** nm, slightly beyond $W_{d\max}$, so the device is just past threshold. The depletion formula gives $C$ = **65.19** nF/cm²; in reality the high-frequency curve sits at $C_{\min}$ there.

(e) $d(1/C^2)/dV_g = 2/(q\varepsilon_sN_A)$ = **2.41 × 10¹⁴** cm⁴/(F²·V).

### Solution 09-08.11

(a) $C_{ox}$ = 69.06 pF/10⁻⁴ cm² = 690.6 nF/cm², so $T_{ox}$ = **5.00** nm.

(b) Root finding on $C_{\min}/C_{ox}$ = 0.0760 gives $N_A$ = **3.00 × 10¹⁶** cm⁻³.

(c) The ideal $V_{fb} = 4.05 - \psi_s$ = **−0.9546** V.

(d) $\Delta V_{fb}$ = −1.05 + 0.9546 = **−0.0954** V, so $Q_{ox} = -C_{ox}\Delta V_{fb}$ = **6.59 × 10⁻⁸** C/cm², which is **4.11 × 10¹¹** positive charges per cm².

### Solution 09-08.12

$C_{ox}$ = **172.7** nF/cm², and $Q_m = C_{ox} \times 0.15$ V = **2.59 × 10⁻⁸** C/cm², or **1.62 × 10¹¹** ions per cm². Even this small density, about one ion per **4.2 × 10³** surface atoms, shifts the threshold by 0.15 V, which is why sodium contamination was the scourge of early MOS manufacturing.

### Solution 09-08.13

$W_{dpoly} = \varepsilon_{ox}\mathcal E_{ox}/qN_{poly}$, $\phi_{poly} = qN_{poly}W_{dpoly}^2/2\varepsilon_s$ and $T_{oxe} = 1.5 + W_{dpoly}/3 + 0.5$ nm:

| $N_{poly}$ (cm⁻³) | $W_{dpoly}$ (nm) | $\phi_{poly}$ (V) | $T_{oxe}$ (nm) |
|---|---|---|---|
| 5 × 10¹⁹ | **2.16** | **0.180** | **2.72** |
| 10²⁰ | **1.08** | **0.0898** | **2.36** |
| 3 × 10²⁰ | **0.359** | **0.0299** | **2.12** |

Even very heavy doping leaves $T_{oxe}$ 0.6 nm above the physical oxide, because the inversion term remains; doping much beyond 10²⁰ cm⁻³ also risks dopant penetration through the oxide [Hu §5.8].

### Solution 09-08.14

(a) With no inversion charge, the whole voltage drops across oxide and depletion: solving the quadratic gives $W$ = **0.199** µm (almost twice $W_{d\max}$ = 0.104 µm) and $\phi_s$ = **3.06** V, with $C/C_{ox}$ = **0.131**.

(b) In equilibrium, $Q_{inv} = C_{ox}(3 - 0.3293)$ = **9.22 × 10⁻⁷** C/cm².

(c) The generation current is $J = qn_iW/2\tau_0$.

- Using the deep-depletion width: $J$ = **1.59 × 10⁻⁸** A/cm², and the time is $Q_{inv}/J$ = **57.8** s.
- Using $W_{d\max}$: **111** s.

The first is an underestimate of the time, because the depletion region shrinks back toward $W_{d\max}$ as electrons arrive; the second is an overestimate. Inversion takes about a minute (Hu says it "can take minutes" [Hu §5.5]). In real devices, generation at the surface and at the capacitor's edges usually makes it faster. This slow recovery is what lets a CCD integrate light for tens of milliseconds.

### Solution 09-08.15

(a) CET = 0.4 + $t \times 3.9/21.2$ + 0.3, so:

- for 1.0 nm, $t$ = **1.63** nm;
- for 0.9 nm, $t$ = **1.09** nm.

(b) With $t$ = 1.5 nm (0.276 nm equivalent), the interfacial layer must be 0.9 − 0.3 − 0.276 = **0.324** nm, about one monolayer of SiO₂. Reaching the roadmap's 0.9 nm leaves almost nothing to trade.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-08.1a | V_fb, n⁺ on p 1e16 | -0.9262 | V |
| 09-08.1b | V_fb, p⁺ on n 1e17 | 0.9709 | V |
| 09-08.1c | V_fb, 4.6 V metal on p 1e16 | -0.3762 | V |
| 09-08.1d | E_C − E_F, p 1e16 | 0.9262 | eV |
| 09-08.1e | E_C − E_F, n 1e17 | 0.1491 | eV |
| 09-08.1f | ψ_s, n 1e17 | 4.199 | V |
| 09-08.2a | C_ox, 3 nm | 1151 | nF/cm² |
| 09-08.2b | stack EOT | 1.336 | nm |
| 09-08.2c | stack capacitance | 2585 | nF/cm² |
| 09-08.2d | physical thickness ratio | 1.53 | — |
| 09-08.2e | capacitance ratio | 2.25 | — |
| 09-08.3a | C_ox, 5 nm | 690.6 | nF/cm² |
| 09-08.3b | Q_acc | 1.036e-6 | C/cm² |
| 09-08.3c | hole sheet density | 6.47e12 | cm⁻² |
| 09-08.4a | W at −0.5 V | 54.7 | nm |
| 09-08.4b | φ_s at −0.5 V | 0.232 | V |
| 09-08.4c | W at +0.2 V | 97.4 | nm |
| 09-08.4d | φ_s at +0.2 V | 0.734 | V |
| 09-08.5a | V_fb, 1e16 | -0.9262 | V |
| 09-08.5b | V_t, 1e16 | -0.1696 | V |
| 09-08.5c | V_fb, 1e17 | -0.9858 | V |
| 09-08.5d | V_t, 1e17 | -0.0079 | V |
| 09-08.5e | V_fb, 1e18 | -1.0453 | V |
| 09-08.5f | V_t, 1e18 | 0.3956 | V |
| 09-08.6a | doping for V_t = 0.4 V | 1.015e18 | cm⁻³ |
| 09-08.7a | φ_B, n 1e17 | 0.4167 | V |
| 09-08.7b | V_fb | 0.9709 | V |
| 09-08.7c | V_t | -0.0070 | V |
| 09-08.8a | C_ox, 2 nm | 1.727 | µF/cm² |
| 09-08.8b | Q_inv | 1.381e-6 | C/cm² |
| 09-08.8c | n_s | 8.62e12 | cm⁻² |
| 09-08.8d | sheet resistance | 2896 | Ω/□ |
| 09-08.8e | 10-square channel resistance | 29.0 | kΩ |
| 09-08.9a | φ_s at V_t + 0.5 V | 0.9432 | V |
| 09-08.9b | exact Q_inv at V_t + 0.5 V | 1.265e-7 | C/cm² |
| 09-08.9c | sheet Q_inv at V_t + 0.5 V | 1.727e-7 | C/cm² |
| 09-08.9d | ratio at V_t + 0.5 V | 0.733 | — |
| 09-08.9e | φ_s at V_t + 1.5 V | 0.9899 | V |
| 09-08.9f | exact Q_inv at V_t + 1.5 V | 4.514e-7 | C/cm² |
| 09-08.9g | sheet Q_inv at V_t + 1.5 V | 5.180e-7 | C/cm² |
| 09-08.9h | ratio at V_t + 1.5 V | 0.871 | — |
| 09-08.10a | C_ox, 5 nm | 690.6 | nF/cm² |
| 09-08.10b | V_fb, 5e16 | -0.9678 | V |
| 09-08.10c | L_D | 18.28 | nm |
| 09-08.10d | C_FB | 311.2 | nF/cm² |
| 09-08.10e | W_dmax | 143.6 | nm |
| 09-08.10f | C_min | 65.31 | nF/cm² |
| 09-08.10g | W at V_g = 0 | 143.9 | nm |
| 09-08.10h | C at V_g = 0 (formula) | 65.19 | nF/cm² |
| 09-08.10i | slope of 1/C² | 2.41e14 | cm⁴/(F²·V) |
| 09-08.11a | T_ox | 5.00 | nm |
| 09-08.11b | C_min/C_ox | 0.0760 | — |
| 09-08.11c | N_A | 3.00e16 | cm⁻³ |
| 09-08.11d | ideal V_fb | -0.9546 | V |
| 09-08.11e | ΔV_fb | -0.0954 | V |
| 09-08.11f | Q_ox | 6.59e-8 | C/cm² |
| 09-08.11g | oxide charges per cm² | 4.11e11 | cm⁻² |
| 09-08.12a | C_ox, 20 nm | 172.7 | nF/cm² |
| 09-08.12b | mobile charge | 2.59e-8 | C/cm² |
| 09-08.12c | ions per cm² | 1.62e11 | cm⁻² |
| 09-08.12d | surface atoms per ion | 4.2e3 | — |
| 09-08.13a | W_dpoly, 5e19 | 2.16 | nm |
| 09-08.13b | φ_poly, 5e19 | 0.180 | V |
| 09-08.13c | T_oxe, 5e19 | 2.72 | nm |
| 09-08.13d | W_dpoly, 1e20 | 1.08 | nm |
| 09-08.13e | φ_poly, 1e20 | 0.0898 | V |
| 09-08.13f | T_oxe, 1e20 | 2.36 | nm |
| 09-08.13g | W_dpoly, 3e20 | 0.359 | nm |
| 09-08.13h | φ_poly, 3e20 | 0.0299 | V |
| 09-08.13i | T_oxe, 3e20 | 2.12 | nm |
| 09-08.14a | deep-depletion width | 0.199 | µm |
| 09-08.14b | deep-depletion φ_s | 3.06 | V |
| 09-08.14c | C/C_ox in deep depletion | 0.131 | — |
| 09-08.14d | final Q_inv | 9.22e-7 | C/cm² |
| 09-08.14e | generation current density | 1.59e-8 | A/cm² |
| 09-08.14f | time with deep-depletion width | 57.8 | s |
| 09-08.14g | time with W_dmax | 111 | s |
| 09-08.15a | HfO₂ for CET 1.0 nm | 1.63 | nm |
| 09-08.15b | HfO₂ for CET 0.9 nm | 1.09 | nm |
| 09-08.15c | interfacial layer for 0.9 nm | 0.324 | nm |
| 09-08.15d | equivalent of 1.5 nm HfO₂ | 0.276 | nm |
