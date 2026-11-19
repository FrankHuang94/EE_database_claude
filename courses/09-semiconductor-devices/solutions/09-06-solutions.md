# Solutions 09-06 · PN Junction I–V, Capacitance and Breakdown

Problems: [09-06 problems](../problems/09-06-problems.md) · Chapter: [09-06](../chapters/09-06-pn-junction-iv-and-capacitance.md). Every number below is recomputed by [verify_09_06.py](../verify/verify_09_06.py), by these routes:

- diode currents by solving the minority-carrier boundary-value problem numerically;
- voltages by root finding;
- temperature behavior from the full $n_i(T)$ model;
- admittances from the numerically solved small-signal diffusion equation;
- storage times by integrating the time-dependent diffusion equation;
- breakdown from the ionization integral;
- optimum design points by numerical minimization.

---

## Solutions

### Solution 09-06.1

(a) $p_{n0} = n_i^2/N_D = 10^{20}/5\times10^{15}$ = **2.00 × 10⁴** cm⁻³.

(b) $p_n(x_n) = p_{n0}e^{V_A/V_T}$:

- at 0.5 V: $2\times10^4 \times e^{19.34}$ = **5.02 × 10¹²** cm⁻³, a fraction **1.0 × 10⁻³** of $N_D$, so low-level injection holds comfortably;
- at 0.65 V: **1.66 × 10¹⁵** cm⁻³, **33**% of $N_D$, which is no longer low-level injection.

(c) $\Delta p = 0.1N_D$ at $V_A = V_T\ln(0.1N_D/p_{n0} + 1) = 0.025852\ln(2.5\times10^{10} + 1)$ = **0.6190** V.

(d) $e^{-0.2/0.025852}$ = **4.37 × 10⁻⁴**. Reverse bias depletes the edge almost completely, which is why the reverse current saturates.

### Solution 09-06.2

(a) $\mu_n(10^{16})$ = **1248** cm²/V·s, $D_n = V_T\mu_n$ = **32.26** cm²/s and $L_n = \sqrt{32.26 \times 2\times10^{-6}}$ cm = **80.33** µm.

(b) $J_s = qn_i^2D_n/(L_nN_A) = 1.602\times10^{-19} \times 10^{20} \times 32.26/(8.033\times10^{-3} \times 10^{16})$ = **6.435 × 10⁻¹²** A/cm². The area is 2.5 × 10⁻⁵ cm², so $I_s$ = **1.609 × 10⁻¹⁶** A.

(c) $V_A = V_T\ln(10^{-6}/1.609\times10^{-16} + 1)$ = **0.5830** V. At 0.55 V, $I = I_s(e^{0.55/V_T} - 1)$ = **0.279** µA.

### Solution 09-06.3

(a) $\eta = \Delta V/(V_T\ln(I_2/I_1))$.

- First pair: $0.12/(0.025852\ln10.2)$ = **1.999**.
- Second pair: $0.06/(0.025852\ln10)$ = **1.008**.

(b) $I_0 = I\,e^{-V/\eta V_T}$:

- first pair: $10^{-9}e^{-0.2/(1.999\times0.025852)}$ = **2.08 × 10⁻¹¹** A;
- second pair: $2\times10^{-7}e^{-0.5/(1.008\times0.025852)}$ = **9.28 × 10⁻¹⁶** A.

(c) The low range, with $\eta$ ≈ 2 and a large prefactor proportional to $n_i$, is depletion-region recombination. The higher range, with $\eta$ ≈ 1 and a prefactor proportional to $n_i^2$, is ideal diffusion current. At still higher currents, high injection and series resistance would raise $\eta$ again.

### Solution 09-06.4

(a) $\mu_p(10^{15})$ = **433.5** cm²/V·s, $D_p$ = **11.21** cm²/s and $L_p = \sqrt{11.21\times10^{-5}}$ cm = **105.9** µm. The ratio $W_n/L_p$ = **0.1889**, so the diode is short.

(b) $\coth(0.1889)$ = **5.356**, against $L_p/W_n$ = **5.293**. The short-diode estimate is **1.2**% low, because $\coth z \approx 1/z + z/3$.

(c) The fraction recombining is $1 - 1/\cosh(W_n/L_p)$ = **1.76**%, against $W_n^2/2L_p^2$ = **1.78**%. (The current entering is $\coth$ times the long-diode value, and the current reaching the contact is $1/\sinh$ times it; their ratio is $1/\cosh$.)

(d) $\tau_t = W_n^2/2D_p = (2\times10^{-3})^2/(2 \times 11.21)$ = **178.5** ns, **56.0** times shorter than the 10 µs lifetime. Carriers cross before they have time to recombine.

### Solution 09-06.5

(a) On the n⁺ side:

- $\tau_p = 1/(C_nN_D^2) = 1/(1.1\times10^{-30} \times 10^{38})$ = **9.09** ns;
- $\mu_p(10^{19})$ = **56.37** cm²/V·s, $D_p$ = **1.457** cm²/s and $L_p$ = **1.151** µm.

On the p side: $\mu_n$ = 1248 cm²/V·s, $D_n$ = 32.26 cm²/s and $L_n = \sqrt{32.26\times10^{-6}}$ cm = **56.80** µm.

(b) The two saturation current densities:

- hole injection into the n⁺ side: $J_{p0} = qn_i^2D_p/(L_pN_D)$ = **2.028 × 10⁻¹⁴** A/cm²;
- electron injection into the p side: $J_{n0} = qn_i^2D_n/(L_nN_A)$ = **9.100 × 10⁻¹²** A/cm².

The electron fraction is $J_{n0}/(J_{n0} + J_{p0})$ = **99.78**%.

(c) $W/L_p = 0.3/1.151$ = **0.2606** and $\coth(0.2606)$ = **3.923**, so $J_{p0}$ = **7.958 × 10⁻¹⁴** A/cm². The short-diode formula $qn_i^2D_p/(WN_D)$ gives **7.782 × 10⁻¹⁴**. The injection efficiency falls to **99.13**%.

(d) In an NPN transistor, only the electrons injected into the base become collector current. Holes injected back into the emitter are wasted base current, so the transistor's current gain is roughly the ratio of the two components. Thinning the emitter multiplies the hole current by **3.92** here. Real emitters also suffer bandgap narrowing, which raises their $n_i^2$, so emitter design is a central topic of 09-07.

### Solution 09-06.6

(a) $I_se^{V/V_T} = I_{r0}e^{V/2V_T}$ at $V_x = 2V_T\ln(I_{r0}/I_s) = 2 \times 0.025852 \times \ln10^5$ = **0.5953** V.

(b) With $I_1 = I_se^{V/V_T}$ and $I_2 = I_{r0}e^{V/2V_T}$, we have $\eta = (I_1 + I_2)/(I_1 + I_2/2)$.

- At 0.3 V: $I$ = **3.32 × 10⁻⁸** A and $\eta$ = **1.993**. Recombination dominates.
- At 0.6 V: $I$ = **2.30 × 10⁻⁵** A and $\eta$ = **1.313**. The two currents are nearly equal.

(c) Let $r = I_2/I_1$. Then $\eta = (1 + r)/(1 + r/2) < 1.1$ requires $r < 2/9$. Since $r = (I_{r0}/I_s)e^{-V/2V_T}$, this means $V > 2V_T\ln(10^5 \times 9/2)$ = **0.6730** V.

### Solution 09-06.7

(a) Diffusion equals generation when $I_s(300)(n_i/n_{i0})^2 = I_{\text{gen}}(300)(n_i/n_{i0})$, that is when $n_i/n_{i0} = 7.00\times10^{-12}/4.973\times10^{-16}$ = **14,076**.

(b) Root finding on the course model gives $T$ = **481.8** K (**208.6** °C).

(c) On an Arrhenius plot ($\ln I$ against $1/kT$), generation current has the slope of $n_i$, an apparent activation energy of **0.64** eV at 300 K in the course model (about half the gap). Diffusion current has the slope of $n_i^2$, **1.28** eV (about the full gap). A measured slope near $E_g/2$ identifies trap generation; a slope near $E_g$ identifies diffusion. A slope that changes between the two marks the crossover. This is a standard diagnostic for junction and image-sensor leakage.

### Solution 09-06.8

(a) $V = V_T\ln(10^{-6}/2\times10^{-15} + 1)$ = **0.5178** V, and $dV/dT = (0.5178 - 1.2009 - 0.0776)/300$ = **−2.535** mV/K.

(b) $0.5178 - 75 \times 0.002535$ = **0.3277** V.

(c) $I_s(375) = 2\times10^{-15}(n_i(375)/n_i(300))^2$ = **4.39 × 10⁻¹¹** A, so $V = (k \times 375/q)\ln(10^{-6}/4.39\times10^{-11})$ = **0.3242** V. The linear prediction is **3.5** mV high: the curve bends because $dV/dT$ itself depends on $V$ and $T$.

(d) $\Delta V = V_T\ln8$ = **53.76** mV at 300 K and **67.20** mV at 375 K, in exact proportion to $T$.

### Solution 09-06.9

(a) $g_d = 50\ \mu\text{A}/25.852\ \text{mV}$ = **1.934** mS, $r_d$ = **517.0** Ω and $C_d = g_d\tau_p/2$ = **483.5** pF.

(b) $\omega\tau_p = 2\pi \times 10^6 \times 0.5\times10^{-6}$ = **3.142**.

- Exact: $Y = g_d\sqrt{1 + j3.142} + j\omega C_j$ = (**2.835** + j**2.085**) mS, with $|Y|$ = **3.519** mS.
- Low-frequency model: (1.934 + j**3.051**) mS, with $|Y|$ = **3.612** mS, **2.6**% too high.

(c) The exact admittance is an effective conductance of 2.835 mS in parallel with an effective capacitance $\operatorname{Im}Y/\omega$ = **331.9** pF, against 1.934 mS and **485.5** pF at low frequency. As the period approaches the lifetime, the stored charge can no longer follow the voltage. Diffusion capacitance falls, and the conductance rises because injected carriers now return through the terminal within a cycle instead of recombining. The magnitude happens to stay close, but the phase is wrong; above $\omega\tau_p \approx 1$ the low-frequency model should not be used.

### Solution 09-06.10

(a) $Q = I_F\tau_p$ = **1.00** nC.

(b) Charge control gives $\tau_p\ln(1 + 5/2.5)$ = **219.7** ns. The exact result solves $\operatorname{erf}\sqrt{x} = 5/7.5$: $\sqrt x$ = **0.6841**, so $t_s$ = **93.6** ns.

(c) $t_s/\tau_p$ = 0.1 requires $I_F/(I_F + I_R) = \operatorname{erf}\sqrt{0.1}$ = **0.3453**, so $I_R = I_F(1/0.3453 - 1)$ = **9.48** mA. Charge control predicts $\tau_p\ln(1 + 5/9.48)$ = **84.7** ns for that current, a fourfold overestimate.

### Solution 09-06.11

(a) With $W = \varepsilon_s\mathcal E_m/qN_D$, root finding on the ionization integral gives $\mathcal E_m$ = **3.16 × 10⁵** V/cm and $W$ = **10.22** µm. With $V_{bi}$ = **0.851** V, $V_B$ = **160.7** V.

(b) The fixed-critical-field estimate $\varepsilon_s\mathcal E_c^2/2qN_D - V_{bi}$ gives **144.6** V, and Hu's rule $15(10^{17}/N)^{0.6}$ gives **156.8** V. Near 10¹⁵ cm⁻³, where the real breakdown field is close to 3 × 10⁵ V/cm, the simple rules work well.

(c) Root finding on $V_B(N_D)$ = 100 V gives $N_D$ = **4.00 × 10¹⁵** cm⁻³. Hu's rule gives $10^{17}(15/100)^{1/0.6}$ = **4.23 × 10¹⁵** cm⁻³, **6**% higher. Either is a reasonable starting point, but a design with margin should come from measured data on the actual process.

### Solution 09-06.12

(a) $V_{bi} = V_T\ln(10^{36}/10^{20})$ = **0.9524** V. For a symmetric junction the effective doping is $N_AN_D/(N_A + N_D)$ = 5 × 10¹⁷ cm⁻³, so $W = \sqrt{2\varepsilon_sV_{bi}/(qN_{\text{eff}})}$ = **49.6** nm.

(b) The peak field is $\sqrt{2qN_{\text{eff}}(V_{bi} + V_R)/\varepsilon_s}$. Setting it to 10⁶ V/cm gives $V_{bi} + V_R = \varepsilon_s\mathcal E^2/(2qN_{\text{eff}})$ = **6.466** V, so $V_R$ = **5.51** V. The depletion width is $2(V_{bi} + V_R)/\mathcal E$ = **129** nm. Electrons tunnel only where the bands are closest, across the horizontal distance $E_g/q\mathcal E$ = **11.2** nm at the peak field.

(c) At 10⁶ V/cm the coefficients are $\alpha_n$ = **1.03 × 10⁵** and $\alpha_p$ = **1.50 × 10⁵** cm⁻¹. These come from extrapolating the handbook fits far beyond the fields at which they were measured, and they ignore the distance a carrier needs to gain the ionization energy, so treat them as rough. The integral over the 129 nm region is **0.539**, so $M_n = 1/(1 - 0.539)$ = **2.17**. Avalanche roughly doubles the current but is not self-sustaining: breakdown near 5.5 V is mixed, mostly tunneling assisted by avalanche.

(d) For mostly tunneling, a negative coefficient: the bandgap shrinks with temperature, so tunneling increases. The avalanche contribution has a positive coefficient, so the net coefficient is small. This is why diodes near this voltage make the most temperature-stable Zener references.

### Solution 09-06.13

(a) $I_0 = AKT^2e^{-\phi_B/V_T}$ with $A$ = 0.01 cm²:

- Ti: **3.59 × 10⁻⁴** A;
- Pt: **6.84 × 10⁻¹¹** A.

(b) At 100 mA:

- Ti: $V = V_T\ln(0.1/3.59\times10^{-4} + 1)$ = **0.1457** V;
- Pt: **0.5456** V.

(c) At 400 K:

- Ti: $I_0$ = **80.2** mA, **224** times higher;
- Pt: **0.732** µA, **10,708** times higher.

The higher barrier has the steeper temperature dependence (its activation energy is larger), but from a far lower base.

(d) Titanium's 0.15 V drop is attractive, but its leakage is 0.36 mA at room temperature and 80 mA at 400 K, which would cost real power and could run away thermally as leakage heats the junction. Platinum's leakage is negligible, but its drop is close to a PN diode's. A practical rectifier uses an intermediate barrier chosen for the maximum junction temperature, as Problem 09-06.14 shows; Hu warns that too small a barrier "can lead to thermal runaway" [Hu §4.19].

### Solution 09-06.14

(a) At 373.15 K, $V_T$ = **32.156** mV.

- Schottky: $I_0 = 0.05 \times 100 \times 373.15^2e^{-0.6/0.032157}$ = **5.48** mA.
- PN: $J_s$ rises by $(n_i(373)/n_i(300))^2$ = **17,979**, to $1.80\times10^{-8}$ A/cm², so $I_0$ = **8.99 × 10⁻¹⁰** A.

Forward drops at 5 A, from $V_T\ln(5/I_0 + 1)$: Schottky **0.2192** V, PN **0.7215** V.

(b) Losses, with conduction loss $0.5 \times V_F \times 5$ A and leakage loss $0.5 \times 20 \times I_0$:

| | Conduction loss | Leakage loss | Total |
|---|---|---|---|
| Schottky | **0.548** W | **0.0548** W | **0.603** W |
| PN | **1.804** W | negligible (9 nW) | **1.804** W |

The Schottky diode loses **0.334** times as much, even at 100 °C.

(c) Since $I_F \gg I_0$, write $P = d\,I_FV_T\ln(I_F/I_0) + (1 - d)V_RI_0$ (dropping the negligible +1 in the logarithm), with $d$ = 0.5, and use $dI_0/d\phi_B = -I_0/V_T$:

$$
\frac{dP}{d\phi_B} = dI_F - (1 - d)V_R\frac{I_0}{V_T} = 0
\quad\Longrightarrow\quad
I_0 = \frac{V_T\,dI_F}{(1 - d)V_R} = \frac{0.032156 \times 2.5}{10} = \mathbf{8.04}\text{ mA}.
$$

The barrier giving that $I_0$ is $\phi_B = V_T\ln(AKT^2/I_0)$ = **0.5877** V, and the minimum loss is **0.598** W. The 0.60 V barrier costs only **0.87**% more; ±20 mV around the optimum costs **3.2**% (lower barrier) and **2.1**% (higher barrier). The optimum is flat, so the barrier can be chosen for leakage margin at the worst-case temperature rather than for minimum nominal loss.

### Solution 09-06.15

(a) At 10²⁰ cm⁻³ (10²⁶ m⁻³) the exponent is $(4\pi \times 0.6/6.626\times10^{-34})\sqrt{1.036\times10^{-10} \times 2.368\times10^{-31}/10^{26}}$ = **5.64**. Since the exponent scales as $1/\sqrt N$, it reaches 3 at $N = 10^{20}(5.64/3)^2$ = **3.53 × 10²⁰** cm⁻³.

(b) At 3 × 10²⁰ the exponent is **3.25**. The tunneling probability rises by $e^{5.64 - 3.25}$ = **10.8**, so $\rho_c$ ≈ $10^{-7}/10.8$ = **9.2 × 10⁻⁹** Ω·cm².

(c) At $\phi_B$ = 0.4 V the exponent is **3.76**, so $\rho_c$ falls by $e^{5.64 - 3.76}$ = **6.55**.

(d) $R = \rho_c/A = 10^{-9}/(20\times10^{-7} \times 30\times10^{-7})$ = **167** Ω.

(e) Barrier heights to electrons and holes add to about the bandgap, $\phi_{Bn} + \phi_{Bp} \approx E_g$ (§3.10). A silicide with a low barrier on n⁺ silicon has a high barrier on p⁺ silicon, and the exponent depends directly on the barrier. Using one silicide for both forces a compromise near mid-gap, so advanced processes consider separate contact materials or interface treatments for each polarity [Hu §4.21].

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-06.1a | p_n0 at 5e15 | 2.00e4 | cm⁻³ |
| 09-06.1b | edge density at 0.5 V | 5.02e12 | cm⁻³ |
| 09-06.1c | edge density/N_D at 0.5 V | 1.0e-3 | — |
| 09-06.1d | edge density at 0.65 V | 1.66e15 | cm⁻³ |
| 09-06.1e | edge density/N_D at 0.65 V | 33 | % |
| 09-06.1f | V for Δp = 0.1 N_D | 0.6190 | V |
| 09-06.1g | edge fraction at −0.2 V | 4.37e-4 | — |
| 09-06.2a | μ_n at 1e16 | 1248 | cm²/V·s |
| 09-06.2b | D_n | 32.26 | cm²/s |
| 09-06.2c | L_n | 80.33 | µm |
| 09-06.2d | J_s | 6.435e-12 | A/cm² |
| 09-06.2e | I_s | 1.609e-16 | A |
| 09-06.2f | V at 1 µA | 0.5830 | V |
| 09-06.2g | I at 0.55 V | 0.279 | µA |
| 09-06.3a | η, low pair | 1.999 | — |
| 09-06.3b | η, high pair | 1.008 | — |
| 09-06.3c | I_0, low pair | 2.08e-11 | A |
| 09-06.3d | I_0, high pair | 9.28e-16 | A |
| 09-06.4a | μ_p at 1e15 | 433.5 | cm²/V·s |
| 09-06.4b | D_p | 11.21 | cm²/s |
| 09-06.4c | L_p | 105.9 | µm |
| 09-06.4d | W_n/L_p | 0.1889 | — |
| 09-06.4e | coth(W_n/L_p) | 5.356 | — |
| 09-06.4f | L_p/W_n | 5.293 | — |
| 09-06.4g | fraction recombining | 1.76 | % |
| 09-06.4h | W²/2L² estimate | 1.78 | % |
| 09-06.4i | transit time | 178.5 | ns |
| 09-06.4j | lifetime/transit time | 56.0 | — |
| 09-06.4k | short estimate shortfall | 1.2 | % |
| 09-06.5a | Auger hole lifetime at 1e19 | 9.09 | ns |
| 09-06.5b | μ_p at 1e19 | 56.37 | cm²/V·s |
| 09-06.5c | D_p at 1e19 | 1.457 | cm²/s |
| 09-06.5d | L_p at 1e19 | 1.151 | µm |
| 09-06.5e | L_n at 1e16, τ = 1 µs | 56.80 | µm |
| 09-06.5f | J_p0, long n⁺ | 2.028e-14 | A/cm² |
| 09-06.5g | J_n0 | 9.100e-12 | A/cm² |
| 09-06.5h | injection efficiency, long n⁺ | 99.78 | % |
| 09-06.5i | W/L_p, thin n⁺ | 0.2606 | — |
| 09-06.5j | coth, thin n⁺ | 3.923 | — |
| 09-06.5k | J_p0, thin n⁺ | 7.958e-14 | A/cm² |
| 09-06.5l | J_p0, short-diode formula | 7.782e-14 | A/cm² |
| 09-06.5m | injection efficiency, thin n⁺ | 99.13 | % |
| 09-06.5n | hole-current increase, thin n⁺ | 3.92 | — |
| 09-06.6a | crossover voltage | 0.5953 | V |
| 09-06.6b | total current at 0.3 V | 3.32e-8 | A |
| 09-06.6c | η at 0.3 V | 1.993 | — |
| 09-06.6d | total current at 0.6 V | 2.30e-5 | A |
| 09-06.6e | η at 0.6 V | 1.313 | — |
| 09-06.6f | voltage above which η < 1.1 | 0.6730 | V |
| 09-06.7a | n_i ratio at crossover | 14076 | — |
| 09-06.7b | crossover temperature | 481.8 | K |
| 09-06.7c | crossover temperature | 208.6 | °C |
| 09-06.7d | apparent activation energy of n_i at 300 K | 0.64 | eV |
| 09-06.7e | apparent activation energy of n_i² at 300 K | 1.28 | eV |
| 09-06.8a | V at 1 µA, 300 K | 0.5178 | V |
| 09-06.8b | dV/dT | -2.535 | mV/K |
| 09-06.8c | linear prediction at 375 K | 0.3277 | V |
| 09-06.8d | I_s at 375 K | 4.39e-11 | A |
| 09-06.8e | V at 375 K, full model | 0.3242 | V |
| 09-06.8f | error of linear prediction | 3.5 | mV |
| 09-06.8g | ΔV at 300 K, ratio 8 | 53.76 | mV |
| 09-06.8h | ΔV at 375 K, ratio 8 | 67.20 | mV |
| 09-06.9a | g_d | 1.934 | mS |
| 09-06.9b | r_d | 517.0 | Ω |
| 09-06.9c | C_d low frequency | 483.5 | pF |
| 09-06.9d | ωτ at 1 MHz | 3.142 | — |
| 09-06.9e | exact conductance at 1 MHz | 2.835 | mS |
| 09-06.9f | exact susceptance at 1 MHz | 2.085 | mS |
| 09-06.9g | exact admittance magnitude | 3.519 | mS |
| 09-06.9h | model susceptance | 3.051 | mS |
| 09-06.9i | model admittance magnitude | 3.612 | mS |
| 09-06.9j | model magnitude error | 2.6 | % |
| 09-06.9k | effective capacitance at 1 MHz | 331.9 | pF |
| 09-06.9l | low-frequency C_d + C_j | 485.5 | pF |
| 09-06.10a | stored charge | 1.00 | nC |
| 09-06.10b | t_s charge control | 219.7 | ns |
| 09-06.10c | erf⁻¹(2/3) | 0.6841 | — |
| 09-06.10d | t_s exact | 93.6 | ns |
| 09-06.10e | erf(√0.1) | 0.3453 | — |
| 09-06.10f | I_R for 20 ns | 9.48 | mA |
| 09-06.10g | charge control at that I_R | 84.7 | ns |
| 09-06.11a | peak field at breakdown, 2e15 | 3.16e5 | V/cm |
| 09-06.11b | W at breakdown | 10.22 | µm |
| 09-06.11c | V_bi | 0.851 | V |
| 09-06.11d | V_B | 160.7 | V |
| 09-06.11e | fixed-field estimate | 144.6 | V |
| 09-06.11f | Hu's rule | 156.8 | V |
| 09-06.11g | doping for 100 V | 4.00e15 | cm⁻³ |
| 09-06.11h | Hu's rule doping for 100 V | 4.23e15 | cm⁻³ |
| 09-06.11i | Hu's doping above the computed | 6 | % |
| 09-06.12a | V_bi, 1e18 symmetric | 0.9524 | V |
| 09-06.12b | W at zero bias | 49.6 | nm |
| 09-06.12c | V_bi + V_R at 1e6 V/cm | 6.466 | V |
| 09-06.12d | V_R at 1e6 V/cm | 5.51 | V |
| 09-06.12e | W at 1e6 V/cm | 129 | nm |
| 09-06.12j | tunneling distance | 11.2 | nm |
| 09-06.12f | α_n at 1e6 V/cm | 1.03e5 | cm⁻¹ |
| 09-06.12g | α_p at 1e6 V/cm | 1.50e5 | cm⁻¹ |
| 09-06.12h | ionization integral | 0.539 | — |
| 09-06.12i | M_n | 2.17 | — |
| 09-06.13a | I_0, Ti | 3.59e-4 | A |
| 09-06.13b | I_0, Pt | 6.84e-11 | A |
| 09-06.13c | V at 100 mA, Ti | 0.1457 | V |
| 09-06.13d | V at 100 mA, Pt | 0.5456 | V |
| 09-06.13e | I_0 at 400 K, Ti | 80.2 | mA |
| 09-06.13f | increase factor, Ti | 224 | — |
| 09-06.13g | I_0 at 400 K, Pt | 0.732 | µA |
| 09-06.13h | increase factor, Pt | 10708 | — |
| 09-06.14a | V_T at 373.15 K | 32.156 | mV |
| 09-06.14b | Schottky I_0 | 5.48 | mA |
| 09-06.14c | n_i² ratio 373 K/300 K | 17979 | — |
| 09-06.14d | PN I_0 | 8.99e-10 | A |
| 09-06.14e | Schottky V_F | 0.2192 | V |
| 09-06.14f | PN V_F | 0.7215 | V |
| 09-06.14g | Schottky conduction loss | 0.548 | W |
| 09-06.14h | Schottky leakage loss | 0.0548 | W |
| 09-06.14i | Schottky total loss | 0.603 | W |
| 09-06.14j | PN conduction loss | 1.804 | W |
| 09-06.14k | PN total loss | 1.804 | W |
| 09-06.14l | optimum I_0 | 8.04 | mA |
| 09-06.14m | optimum barrier | 0.5877 | V |
| 09-06.14n | minimum loss | 0.598 | W |
| 09-06.14o | excess loss at 0.60 V | 0.87 | % |
| 09-06.14p | excess loss 20 mV below optimum | 3.2 | % |
| 09-06.14q | excess loss 20 mV above optimum | 2.1 | % |
| 09-06.14r | Schottky/PN total loss | 0.334 | — |
| 09-06.15a | exponent at 1e20 | 5.64 | — |
| 09-06.15b | doping for exponent 3 | 3.53e20 | cm⁻³ |
| 09-06.15c | exponent at 3e20 | 3.25 | — |
| 09-06.15d | tunneling gain 1e20 to 3e20 | 10.8 | — |
| 09-06.15e | ρ_c at 3e20 | 9.2e-9 | Ω·cm² |
| 09-06.15f | exponent at 0.4 V | 3.76 | — |
| 09-06.15g | reduction for 0.4 V barrier | 6.55 | — |
| 09-06.15h | contact resistance | 167 | Ω |
