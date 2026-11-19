# Course 09 · Final Exam — Solutions

Exam: [README.md](README.md).

All numbers are recomputed by [verify_09_exam.py](../verify/verify_09_exam.py), by routes independent of the hand methods here: carrier densities by solving charge neutrality, depletion widths by integrating Poisson's equation, the diode current by solving the minority-carrier diffusion equation, the MOS threshold by root finding on the surface potential, the inverter by solving current balance, DIBL by the exact barrier minimum, and the solar-cell optimum by maximizing the power directly.

Each solution names the chapter to revisit if you lost points.

**1.** *(09-01)*

(a) $8/(5.431\times10^{-8}\text{ cm})^3$ = **4.99 × 10²²** cm⁻³.

(b) $1/m_c = \tfrac13(1/m_l + 2/m_t) = \tfrac13(1.020 + 10.53)$, so $m_c$ = **0.260** $m_0$.

(c) $\lambda_c = 1.2398/1.12$ = **1.107** µm.

**2.** *(09-02)*

(a) $n_0 = N_D$ = **2 × 10¹⁶** cm⁻³ and $p_0 = n_i^2/n_0$ = **5.0 × 10³** cm⁻³. $E_F - E_i = kT\ln(n_0/n_i)$ = **0.375** eV, and $E_C - E_F = kT\ln(N_C/n_0)$ = **0.191** eV.

(b) The net doping is $N_D - N_A$ = **5 × 10¹⁵** cm⁻³, so $p_0$ = **2.0 × 10⁴** cm⁻³ and $E_F - E_i$ = **0.339** eV. Compensation moves the Fermi level toward midgap but leaves the material n-type.

(c) $\bar N$ = 10¹⁸ × (20 × 20 × 10) × 10⁻²¹ cm³ = **4.0**. $P(0) = e^{-4}$ = **0.0183**: about one device in 55 has no dopant at all in this region. $\sigma/\bar N = 1/\sqrt{4}$ = **0.50**.

**3.** *(09-03)*

(a) $\mu_n$ = **1248** cm²/V·s, $\rho = 1/(qN\mu_n)$ = **0.500** Ω·cm and $R_{sh} = \rho/t$ = **2501** Ω/□.

(b) $R$ = 50 × 2501 = **125** kΩ.

(c) $\mu_p$ = **370** cm²/V·s, $D_p = \mu_pV_T$ = **9.58** cm²/s and $L_p = \sqrt{D_p\tau_p}$ = **30.9** µm.

**4.** *(09-04)*

(a) $\tau_p = 1/(\sigma v_{th}N_t)$ = 1/(10⁻¹⁵ × 1.65 × 10⁷ × 10¹³) = **6.06** µs.

(b) $\Delta p = G\tau_p$ = **6.06 × 10¹⁴** cm⁻³, which is **0.0606** of $n_0$: low-level injection holds.

(c) $E_{Fn} - E_{Fp} = kT\ln[(n_0 + \Delta n)(p_0 + \Delta p)/n_i^2]$ = **0.643** eV.

(d) $L_p = \sqrt{D_p\tau_p}$ = **76.2** µm.

**5.** *(09-05)*

(a) $V_{bi} = V_T\ln(N_AN_D/n_i^2)$ = **0.833** V.

(b) $W = \sqrt{2\varepsilon_s(V_{bi} - V)/q \cdot (1/N_A + 1/N_D)}$: **0.330** µm at 0 V and **1.190** µm at −10 V.

(c) $\mathcal E_{\max}$ = 2 × 10.833/1.190 µm = **1.82 × 10⁵** V/cm, and $C_j = \varepsilon_s/W$ = **8.71** nF/cm².

**6.** *(09-06)*

(a) $D_p$ = 9.58 cm²/s and $L_p$ = 30.9 µm (Question 3), so $I_0 = qAn_i^2D_p/(N_DL_p)$ = **4.96 × 10⁻¹⁶** A.

(b) $V = V_T\ln(I/I_0 + 1)$ = **0.732** V.

(c) $r_d = V_T/I$ = **25.9** Ω and $C_d = (\tau_p/2)(I/V_T)$ = **19.3** nF.

(d) $15 \times 10^{0.6}$ = **59.7** V.

**7.** *(09-07)*

(a) $D_n = \mu_n(10^{17})V_T$ = **20.7** cm²/s. $I_S = qA_En_i^2D_n/(N_BW_B)$ = **3.32 × 10⁻¹⁶** A, so $I_C = I_Se^{0.7/V_T}$ = **0.191** mA.

(b) With $D_p(10^{19})$ in the emitter, $\beta$ = **1422**. Real devices are far lower because band-gap narrowing in the heavily doped emitter raises its $n_i^2$ (09-07).

(c) $\tau_B = W_B^2/2D_n$ = **2.41** ps, $f_T$ = **65.9** GHz from base transit alone, and $g_m = I_C/V_T$ = **7.38** mS.

**8.** *(09-08)*

(a) $C_{ox}$ = **863.3** nF/cm², $\phi_B$ = **0.458** V, and with $E_F - E_V = kT\ln(N_V/N_A)$ = 0.093 eV, $V_{FB}$ = −(1.12 − 0.093) = **−1.027** V.

(b) $Q_{dep} = \sqrt{2qN_A\varepsilon_s(2\phi_B)}$, so $Q_{dep}/C_{ox}$ = **0.452** V and $V_{TH} = V_{FB} + 2\phi_B + Q_{dep}/C_{ox}$ = **0.341** V.

(c) $W_{d\max} = \sqrt{2\varepsilon_s(2\phi_B)/qN_A}$ = **48.7** nm, and $C_{\min} = (1/C_{ox} + W_{d\max}/\varepsilon_s)^{-1}$ = **170.7** nF/cm², **0.198** of $C_{ox}$.

(d) *Rubric.* (i) At threshold the silicon bands bend down toward the surface by $\phi_s = 2\phi_B$ = **0.917** V, so at the surface $E_i$ lies as far below $E_F$ as it lies above it in the bulk ($\phi_B$ = 0.458 V each way); the oxide carries $V_{ox} = Q_{dep}/C_{ox}$ = 0.452 V, drawn as a sloped (linear) band in the oxide; the gate's $E_F$ sits $qV_{TH}$ = 0.341 eV below the body's $E_F$ for a positive gate voltage. (ii) The low-frequency curve starts at $C_{ox}$ in accumulation (left of $V_{FB}$ = −1.027 V), dips through depletion, and returns to $C_{ox}$ in inversion above $V_{TH}$ = 0.341 V; the high-frequency curve follows it down but stays at $C_{\min}$ = 0.198 $C_{ox}$ beyond $V_{TH}$, because the inversion charge cannot follow the signal. *Full marks:* correct band bending direction and labels, the oxide drop, the flat band and threshold positions, and the distinction between the two $C$–$V$ curves.

**9.** *(09-09)*

(a) $V_{Dsat} = V_{ov}/m$ = **0.520** V, $I_{Dsat} = (W/2mL)\mu_{ns}C_{ox}V_{ov}^2$ = **0.438** mA and $g_m = 2I_{Dsat}/V_{ov}$ = **1.35** mS.

(b) $S = mV_T\ln 10$ = **74.4** mV/decade and $I_{off}$ = 1 µA × $10^{-0.35/0.0744}$ = **1.98 × 10⁻¹¹** A.

**10.** *(09-10)*

(a) $\mathcal E_{sat}$ = **8.0 × 10⁴** V/cm and $\mathcal E_{sat}L$ = **0.400** V. $1/V_{Dsat} = 1.2/0.6 + 1/0.4$, so $V_{Dsat}$ = **0.222** V, and $I_{Dsat} = WC_{ox}v_{sat}(V_{ov} - mV_{Dsat})$ = **0.460** mA/µm.

(b) $\Delta V_{TH} = (0.75 + 0.4)e^{-30/8}$ = **27.0** mV, raising the off-current by $10^{27.0/75}$ = **2.29**.

**11.** *(09-11)*

(a) $V_M = (0.25\sqrt{2.5} + 0.65)/(1 + \sqrt{2.5})$ = **0.405** V.

(b) $\tau_d = (CV/4)(1/I_N + 1/I_P)$ = **7.78** ps, and $f = 1/(2 \times 31 \times \tau_d)$ = **2.07** GHz.

(c) $P = \alpha NCV^2f$ = 0.15 × 10⁸ × 2 × 10⁻¹⁵ × 0.64 × 2 × 10⁹ = **38.4** W.

(d) $\kappa^2 = (1/0.7)^2$ = **2.04**.

**12.** *(09-12)*

(a) $\lambda^2 = (3/2)(6)(1) + 36/8$ = 13.5 nm², so $\lambda$ = **3.67** nm.

(b) $e^{-24/(2 \times 3.674)}$ = **0.0382**. Then $u_{\min}$ = 2√(0.2 × 0.25) × 0.0382 = **17.1** mV at 0.05 V and 2√(0.2 × 0.9) × 0.0382 = **32.4** mV at 0.7 V, so DIBL ≈ **23.6** mV/V.

(c) $W_{\text{eff}}$ = 2 × 46 + 7 = **99** nm; ⌈300/99⌉ = **4** fins, giving **396** nm.

(d) $IR/8$ = 0.25 mA × 500 Ω/8 = **15.6** mV.

**13.** *(09-13)*

(a) $N_D = \varepsilon\mathcal E_c^2/2qV_B$, $W = 2V_B/\mathcal E_c$, $R_{on,sp} = W/q\mu N_D$:

| | $N_D$ (cm⁻³) | $W$ (µm) | $R_{on,sp}$ (mΩ·cm²) |
|---|---|---|---|
| Si | **7.61 × 10¹³** | **170** | **1033** |
| 4H-SiC | **1.01 × 10¹⁶** | **13.6** | **0.839** |

The ratio is **1232**.

(b) $e^{0.15/V_T}$ = **331**.

(c) $R_{sh} = 1/(qn_s\mu)$ = **385** Ω/□.

(d) With uniform doping $N_D$ the field falls linearly, $d\mathcal E/dx = -qN_D/\varepsilon$ (Poisson's equation), from $\mathcal E_c$ at the junction to zero at the far edge, a distance $W = \varepsilon\mathcal E_c/qN_D$ away. The blocked voltage is the triangle's area, $V_B = \tfrac12\mathcal E_cW$, so $W = 2V_B/\mathcal E_c$ and $N_D = \varepsilon\mathcal E_c/qW = \varepsilon\mathcal E_c^2/2qV_B$. The layer's resistance per area is $R_{on,sp} = W/(q\mu N_D) = (2V_B/\mathcal E_c)\cdot 2V_B/(\mu\varepsilon\mathcal E_c^2) = 4V_B^2/(\varepsilon\mu\mathcal E_c^3)$: thickness falls as $1/\mathcal E_c$ and doping rises as $\mathcal E_c^2$, giving the cube. *Full marks:* the field slope from Poisson, the triangle area, and the algebra to the cube law.

**14.** *(09-14)*

(a) $\mathcal R = 0.6 \times 0.905/1.2398$ = **0.438** A/W.

(b) $t = 2d/c$ = **1.001** µs.

(c) DR = 20 log₁₀(10000/3) = **70.5** dB.

(d) $V_{oc} = V_T\ln(J_{sc}/J_0 + 1)$ = **0.6714** V. The iteration gives 0.5893 V and then $V_{mp}$ = **0.5894** V. Then $J_{mp}$ = **36.40** mA/cm², $FF$ = **0.841** and the efficiency is **21.5**%.

(e) Open circuit means $J = 0$: $J_0(e^{V_{oc}/V_T} - 1) = J_{sc}$, so $V_{oc} = V_T\ln(J_{sc}/J_0 + 1)$. The output power per area is $P = VJ = V[J_{sc} - J_0(e^{V/V_T} - 1)]$. Setting $dP/dV = J_{sc} + J_0 - J_0e^{V/V_T}(1 + V/V_T) = 0$ gives $e^{V/V_T}(1 + V/V_T) = (J_{sc} + J_0)/J_0 = e^{V_{oc}/V_T}$. Taking logarithms, $V/V_T + \ln(1 + V/V_T) = V_{oc}/V_T$, which is $V = V_{oc} - V_T\ln(1 + V/V_T)$. *Full marks:* both steps, with the logarithm taken correctly.

**15.** *(09-09 to 09-13; rubric)*

(a) (3 points) $R_{on,sp} \propto 1/\mathcal E_c^3$ at equal $\varepsilon\mu$, so a tenfold reduction needs $10^{1/3}$ = **2.15** times the critical field. With SiC's 2.84 MV/cm (09-13), the claim needs about **6.12** MV/cm. That is far beyond SiC, and GaN's field is reported to be at best comparable to SiC's (09-13), so the claim more likely mixes total and drift resistance, different voltage classes, temperatures or chip areas. A strong answer also notes the premise: ultra-wide-gap materials (gallium oxide, diamond, aluminum nitride) are reported to have higher critical fields, but with lower mobility or immature processing, so \"equal $\varepsilon\mu$\" is itself the weak assumption (not sourced in this course). *Full marks:* the cube law, the ratio, the implied field, and a plausible alternative explanation or the $\mathcal E_c$–$\mu$ trade-off.

(b) (3 points) Node names describe logic transistors: gate pitch, metal pitch and cell height (09-11). A 1200 V device is set by its drift layer, tens of micrometers thick (09-13), so lithographic pitch is irrelevant to its blocking voltage and on-resistance. At best the phrase refers to an integrated controller. *Full marks:* separating logic density from power-device physics.

(c) (3 points) Any three of: $R_{DS(on)}$ × active area at the rated voltage and at 125–175 °C (temperature raises resistance); the breakdown voltage distribution and avalanche rating; the split of resistance into drift, channel, substrate and package; dynamic on-resistance after high-voltage switching; threshold stability; a third-party test against a named SiC part under the same conditions. *Full marks:* three specific, physically motivated requests.

(d) (3 points) The wavelength, the excess bias, whether the figure includes the fill factor (photon detection efficiency per pixel area against per active area), the dark-count rate and timing jitter at that bias, and the temperature (09-14). *Full marks:* at least wavelength, excess bias and fill factor.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X09.1a | atom density | 4.99e22 | cm⁻³ |
| X09.1b | conductivity mass | 0.260 | m₀ |
| X09.1c | cutoff wavelength | 1.107 | µm |
| X09.2a | n₀ | 2e16 | cm⁻³ |
| X09.2b | p₀ | 5.0e3 | cm⁻³ |
| X09.2c | E_F − E_i | 0.375 | eV |
| X09.2d | E_C − E_F | 0.191 | eV |
| X09.2e | compensated n₀ | 5e15 | cm⁻³ |
| X09.2f | compensated p₀ | 2.0e4 | cm⁻³ |
| X09.2g | compensated E_F − E_i | 0.339 | eV |
| X09.2h | mean dopant count | 4.0 | — |
| X09.2i | probability of none | 0.0183 | — |
| X09.2j | relative spread | 0.50 | — |
| X09.3a | electron mobility | 1248 | cm²/V·s |
| X09.3b | resistivity | 0.500 | Ω·cm |
| X09.3c | sheet resistance | 2501 | Ω/□ |
| X09.3d | resistor | 125 | kΩ |
| X09.3e | hole mobility | 370 | cm²/V·s |
| X09.3f | D_p | 9.58 | cm²/s |
| X09.3g | L_p, 1 µs | 30.9 | µm |
| X09.4a | SRH lifetime | 6.06 | µs |
| X09.4b | excess holes | 6.06e14 | cm⁻³ |
| X09.4c | ratio to n₀ | 0.0606 | — |
| X09.4d | quasi-Fermi split | 0.643 | eV |
| X09.4e | diffusion length | 76.2 | µm |
| X09.5a | V_bi | 0.833 | V |
| X09.5b | W at 0 V | 0.330 | µm |
| X09.5c | W at −10 V | 1.190 | µm |
| X09.5d | peak field at −10 V | 1.82e5 | V/cm |
| X09.5e | C_j at −10 V | 8.71 | nF/cm² |
| X09.6a | I₀ | 4.96e-16 | A |
| X09.6b | V at 1 mA | 0.732 | V |
| X09.6c | r_d | 25.9 | Ω |
| X09.6d | C_d | 19.3 | nF |
| X09.6e | Hu's V_B | 59.7 | V |
| X09.7a | D_n in the base | 20.7 | cm²/s |
| X09.7b | I_S | 3.32e-16 | A |
| X09.7c | I_C at 0.7 V | 0.191 | mA |
| X09.7d | β | 1422 | — |
| X09.7e | base transit time | 2.41 | ps |
| X09.7f | f_T, base transit | 65.9 | GHz |
| X09.7g | g_m | 7.38 | mS |
| X09.8a | C_ox | 863.3 | nF/cm² |
| X09.8b | φ_B | 0.458 | V |
| X09.8c | E_F − E_V | 0.093 | eV |
| X09.8d | V_FB | -1.027 | V |
| X09.8e | Q_dep/C_ox | 0.452 | V |
| X09.8f | V_TH | 0.341 | V |
| X09.8g | W_dmax | 48.7 | nm |
| X09.8h | C_min | 170.7 | nF/cm² |
| X09.8i | C_min/C_ox | 0.198 | — |
| X09.8j | surface band bending at threshold | 0.917 | V |
| X09.9a | V_Dsat | 0.520 | V |
| X09.9b | I_Dsat | 0.438 | mA |
| X09.9c | g_m | 1.35 | mS |
| X09.9d | swing | 74.4 | mV/decade |
| X09.9e | I_off | 1.98e-11 | A |
| X09.10a | E_sat | 8.0e4 | V/cm |
| X09.10b | E_sat L | 0.400 | V |
| X09.10c | V_Dsat | 0.222 | V |
| X09.10d | I_Dsat | 0.460 | mA/µm |
| X09.10e | threshold reduction | 27.0 | mV |
| X09.10f | off-current factor | 2.29 | — |
| X09.11a | V_M | 0.405 | V |
| X09.11b | τ_d | 7.78 | ps |
| X09.11c | ring frequency | 2.07 | GHz |
| X09.11d | dynamic power | 38.4 | W |
| X09.11e | power-density factor | 2.04 | — |
| X09.12a | λ | 3.67 | nm |
| X09.12b | e^(−L/2λ) | 0.0382 | — |
| X09.12c | ΔV_TH at 0.05 V | 17.1 | mV |
| X09.12d | ΔV_TH at 0.7 V | 32.4 | mV |
| X09.12e | DIBL | 23.6 | mV/V |
| X09.12f | fin width | 99 | nm |
| X09.12g | fins | 4 | — |
| X09.12h | total width | 396 | nm |
| X09.12i | IR drop | 15.6 | mV |
| X09.13a | Si doping | 7.61e13 | cm⁻³ |
| X09.13b | Si thickness | 170 | µm |
| X09.13c | Si R_on,sp | 1033 | mΩ·cm² |
| X09.13d | SiC doping | 1.01e16 | cm⁻³ |
| X09.13e | SiC thickness | 13.6 | µm |
| X09.13f | SiC R_on,sp | 0.839 | mΩ·cm² |
| X09.13g | ratio | 1232 | — |
| X09.13h | HBT gain factor | 331 | — |
| X09.13i | 2DEG sheet resistance | 385 | Ω/□ |
| X09.14a | responsivity | 0.438 | A/W |
| X09.14b | round trip | 1.001 | µs |
| X09.14c | dynamic range | 70.5 | dB |
| X09.14d | V_oc | 0.6714 | V |
| X09.14e | first iterate | 0.5893 | V |
| X09.14f | V_mp | 0.5894 | V |
| X09.14g | J_mp | 36.40 | mA/cm² |
| X09.14h | fill factor | 0.841 | — |
| X09.14i | efficiency | 21.5 | % |
| X09.15a | critical-field ratio | 2.15 | — |
| X09.15b | implied critical field | 6.12 | MV/cm |
