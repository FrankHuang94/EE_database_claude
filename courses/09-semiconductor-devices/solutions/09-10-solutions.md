# Solutions 09-10 · Short-Channel Effects and Leakage

Problems: [09-10 problems](../problems/09-10-problems.md) · Chapter: [09-10](../chapters/09-10-short-channel-effects-and-leakage.md). Every number below is recomputed by [verify_09_10.py](../verify/verify_09_10.py), by these routes:

- velocity-saturated currents by integrating the channel equation numerically, with saturation located where the drain-end field reaches $\mathcal E_{sat}$;
- series resistance and design values by root finding;
- the $R_{ds}$ extraction by a least-squares line fit;
- dopant fluctuation by numerical integration of the depth-weighted variance.

---

## Solutions

### Solution 09-10.1

$\mathcal E_{sat} = 2 \times 8\times10^6/200$ = **8.0 × 10⁴** V/cm. The crossover length $L = V_{ov}/\mathcal E_{sat}$ is:

- **12.5** nm at 0.1 V;
- **62.5** nm at 0.5 V;
- **125** nm at 1.0 V.

A logic gate driven hard (0.5–1 V of overdrive) is velocity-saturated at any length below about 100 nm. An analog transistor biased at 0.1 V of overdrive stays nearly long-channel down to a few tens of nanometers, which is Hu's point about low-power analog design (chapter §3.1).

### Solution 09-10.2

$I_{Dsat} = WC_{ox}v_{sat}V_{ov}$ = 10⁻⁴ cm × 1.727 × 10⁻⁶ F/cm² × 8 × 10⁶ cm/s × $V_{ov}$:

- **0.553** mA/µm at 0.4 V;
- **1.105** mA/µm at 0.8 V.

Doubling the overdrive raises the current by a factor of **2.00**, against 4 for the square law.

### Solution 09-10.3

$\mathcal E_{sat}$ = 2 × 8 × 10⁶/183 = 8.74 × 10⁴ V/cm. With $1/V_{Dsat} = m/V_{ov} + 1/\mathcal E_{sat}L$ and $I_{Dsat} = WC_{ox}v_{sat}(V_{ov} - mV_{Dsat})$:

| $L$ | $V_{Dsat}$ (V) | $I_{Dsat}$ (mA/µm) | ratio to long-channel |
|---|---|---|---|
| 1 µm | **0.510** | **0.0524** | **0.942** |
| 200 nm | **0.414** | **0.212** | **0.763** |
| 50 nm | **0.2419** | **0.497** | **0.447** |
| 20 nm | **0.1322** | **0.679** | **0.244** |

From 200 nm to 20 nm the current rises only **3.20**-fold, against the tenfold rise of the $1/L$ law. Even at 1 µm, 6% of the long-channel current is lost.

### Solution 09-10.4

$\mathcal E_{sat} = 2 \times 6\times10^6/61$ = **1.97 × 10⁵** V/cm and $\mathcal E_{sat}L$ = **0.984** V. Then $1/|V_{Dsat}| = 1.2/0.65 + 1/0.984$, so $|V_{Dsat}|$ = **0.349** V, and

$$
|I_{Dsat}| = 10^{-4} \times 1.727\times10^{-6} \times 6\times10^6 \times (0.65 - 1.2 \times 0.349) = \mathbf{0.239}\text{ mA/µm} ,
$$

a ratio of **0.481** to the NMOS. The hole mobility is three times smaller, but in a short channel the current depends mostly on the saturation velocity, which is only 25% lower. The low mobility even helps a little: it raises $\mathcal E_{sat}$, so the PMOS is less deeply velocity-saturated. This is why Hu's measured PMOS deliver about half the NMOS current (chapter §3.1).

### Solution 09-10.5

With $\mathcal E_{sat}L$ = 0.437 V and $I_{\text{long}} = (W/L)\mu_{ns}C_{ox}(V_{ov} - mV_{DS}/2)V_{DS}$:

| $V_{DS}$ | long-channel $I_D$ (mA/µm) | factor $1 + V_{DS}/\mathcal E_{sat}L$ | $I_D$ (mA/µm) | $V_{DS}/I_D$ (Ω·µm) |
|---|---|---|---|---|
| 50 mV | **0.1959** | **1.114** | **0.1758** | **284** |
| 100 mV | **0.3728** | **1.229** | **0.3034** | **330** |

Velocity saturation costs 11% of the current even at 50 mV, because the average field (10⁴ V/cm) is already an eighth of $\mathcal E_{sat}$. The channel resistance is in the same range as the series resistances of Problem 09-10.6: at advanced nodes the parasitics are comparable to the channel itself.

### Solution 09-10.6

(a) Hu's closed form gives $I_{Dsat}/I_{Dsat0} = 1/(1 + R_SI_{Dsat0}/V_{ov})$ = 0.8 when $R_SI_{Dsat0}/V_{ov}$ = 0.25:

$$
R_S = \frac{0.25 \times 0.65\text{ V}}{0.4968\text{ mA}} = \mathbf{327}\ \Omega\cdot\text{µm} .
$$

(b) Self-consistently, find the internal overdrive at which the full model gives 0.8 × 0.4968 mA: **0.558** V. The drop 0.65 − 0.558 = 0.092 V must equal $R_S \times 0.3975$ mA, so $R_S$ = **231** Ω·µm.

The closed form assumes a fully velocity-saturated device, whose current is proportional to $V_{ov}$. This device's current falls faster than linearly as the overdrive drops (it is partly long-channel), so each millivolt of IR drop costs more.

### Solution 09-10.7

The slopes are (410.6 − 265.8)/0.5 = **289.6** Ω/µm at 1 V and (280.3 − 207.9)/0.5 = **144.8** Ω/µm at 2 V. The intercepts at $L_{drawn}$ = 0 are **121.0** Ω and **135.5** Ω, and the lines cross where

$$
121.0 + 289.6\,L = 135.5 + 144.8\,L \;\Rightarrow\; L_{drawn} = \Delta L = \mathbf{0.100}\text{ µm}, \qquad R_{ds} = \mathbf{150.0}\ \Omega .
$$

From the 1 V slope, $\mu_{ns}C_{ox} = 1/(W \times \text{slope} \times V_{ov})$ = 1/(10 µm × 289.6 Ω/µm × 1 V) = **345.3** µA/V² (for $C_{ox}$ = 1.727 µF/cm², a mobility of 200 cm²/V·s).

### Solution 09-10.8

The prefactor cancels in the ratio: $0.090/0.020 = e^{15\text{ nm}/l_d}$, so

$$
l_d = \frac{15\text{ nm}}{\ln 4.5} = \mathbf{9.97}\text{ nm}, \qquad A = 0.020\,e^{40/9.97} = \mathbf{1.10} .
$$

A prefactor near one says Hu's simple form describes this technology well. At 25 nm the coupling is the measured 0.090, so the roll-off is 0.45 × 0.090 = **40.5** mV at 50 mV and 1.4 × 0.090 = **126** mV at 1.0 V. DIBL falls to 50 mV/V where $e^{-(L - 25\text{ nm})/l_d} = 50/90$, at $L = 25 + l_d\ln 1.8$ = **30.9** nm.

### Solution 09-10.9

(a) The cube root of 0.7³ is **0.7**: uniform vertical scaling keeps $L/l_d$, and so DIBL, constant.

(b) $0.7^{1/3}$ = **0.888**: the oxide alone buys little.

(c) $0.7^3 = 0.9 \times (W_{dep}X_j \text{ factor})$, so the product must shrink by **0.381**, or each by **0.617**. Every millivolt of oxide scaling lost to gate leakage has to be made up by shallower junctions and thinner depletion regions, which is ultimately why the body itself became thin (09-12).

### Solution 09-10.10

Off-currents scale as $10^{-(V_{TH} - 0.20)/S}$ and on-currents as $(0.7 - V_{TH})/0.5$:

| Flavor | $V_{TH}$ (V) | relative $I_{off}$ | relative $I_{on}$ |
|---|---|---|---|
| Low | 0.20 | 1 | 1 |
| Standard | 0.27 | **0.117** | **0.86** |
| High | 0.34 | **0.0136** | **0.72** |

Block leakage: 0.05 × 1 + 0.95 × 0.0136 = **0.0629** of the all-low-$V_{TH}$ design, a sixteenfold saving, while the 5% of critical-path devices keep full speed.

### Solution 09-10.11

(a) $V_{TH,sat}$ = 0.30 − 0.060 × (0.75 − 0.05) = **0.258** V. DIBL raises the off-current by $10^{0.042/0.075}$ = **3.63**.

(b) $S$ = 75 × 358.15/300 = **89.5** mV/decade, and $V_{TH,sat}$ = 0.258 − 0.8 × 10⁻³ × 58.15 = **0.2115** V.

(c) Relative to 300 K at $V_{DD}$: $10^{0.258/0.075 - 0.2115/0.0895}$ = **12.0**. Relative to the naive room-temperature linear-threshold estimate: $10^{0.30/0.075 - 0.2115/0.0895}$ = **43.5**.

Quoting a linear threshold at room temperature understates hot leakage at the supply by more than an order of magnitude here.

### Solution 09-10.12

From §3.6, $V_{DG,\max} = E_g/q + 3T_{ox}\mathcal E_s$:

- 1.5 nm: 1.12 + 3 × 1.5 × 10⁻⁷ × 5 × 10⁵ = **1.345** V;
- 3 nm: **1.57** V.

At $V_{DG}$ = 1.8 V, $\mathcal E_s = 0.68/(3T_{ox})$ = **1.51** MV/cm for 1.5 nm, well into the tunneling range, and **0.756** MV/cm for 3 nm. I/O transistors need the thicker oxide: besides GIDL, the oxide field and gate tunneling at 1.8 V would be unacceptable in the thin one. This is why processes offer a separate thick-oxide device for I/O.

### Solution 09-10.13

(a) The gate area is 100 nm × 20 nm = 2 × 10⁻¹¹ cm², so each transistor leaks 10 × 2 × 10⁻¹¹ A = **0.200** nA through its gate. Chip-wide, the subthreshold leakage is **1.00** A and the gate leakage **0.200** A, a total leakage power of 1.2 A × 0.75 V = **0.900** W.

(b) Hot: 10 A + 0.24 A at 0.75 V = **7.68** W, with a subthreshold share of **97.7**%.

Attack subthreshold leakage first, with threshold flavors and power gating, and remember the budget is set at the hot corner. (The numbers here are illustrative, but the pattern of a temperature-driven subthreshold term and a weakly temperature-dependent tunneling term is general.)

### Solution 09-10.14

(a) $\phi_B = V_T\ln(N_A/n_i)$ = **0.4762** V. Then $W_{dep} = \sqrt{2\varepsilon_s(2\phi_B)/qN_A}$ = **35.1** nm and $\bar N = N_AWLW_{dep}$ = **56.2** dopants. With $C_{ox}$ = 2.302 µF/cm²,

$$
\sigma_{V_{TH}} = \frac{q}{C_{ox}}\sqrt{\frac{N_AW_{dep}}{3WL}} = \mathbf{18.8}\text{ mV} .
$$

(b) $A_{V_{TH}}$ = 18.8 mV × 0.04 µm = **0.753** mV·µm.

(c) $\sigma_{V_{TH}}$ grows with doping (as roughly $N_A^{1/4}$, since $W_{dep}$ shrinks as $N_A^{-1/2}$). Root finding gives $N_A$ = **5.89 × 10¹⁸** cm⁻³, where $W_{dep}$ has shrunk to **15.1** nm and $\bar N$ = **143**.

The doping needed to suppress short-channel effects in a planar device of this size would bring 30 mV of random threshold spread with it.

### Solution 09-10.15

(a) The roll-off at $V_{DD}$ is $(0.7 + 0.4)e^{-L/l_d}$, and it may not exceed one swing (75 mV):

$$
L_{\min} = l_d\ln\frac{1.1}{0.075} = \mathbf{21.5}\text{ nm} = \mathbf{2.69}\,l_d .
$$

(b) At 0.9 × 21.5 nm, the roll-off is $1.1e^{-0.9 \times 2.686}$ = **98.1** mV. That is an extra factor of $10^{(98.1 - 75)/75}$ = **2.03** over a device at the minimum, and **20.3** over a long-channel device. The exponential makes the shortest devices in the distribution dominate chip leakage, which is why a real minimum length carries margin for variation ("several times $l_d$").

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-10.1a | E_sat | 8.0e4 | V/cm |
| 09-10.1b | crossover L at 0.1 V | 12.5 | nm |
| 09-10.1c | crossover L at 0.5 V | 62.5 | nm |
| 09-10.1d | crossover L at 1.0 V | 125 | nm |
| 09-10.2a | I_Dsat at 0.4 V | 0.553 | mA/µm |
| 09-10.2b | I_Dsat at 0.8 V | 1.105 | mA/µm |
| 09-10.2c | ratio | 2.00 | — |
| 09-10.3a | V_Dsat, 1 µm | 0.510 | V |
| 09-10.3b | I_Dsat, 1 µm | 0.0524 | mA/µm |
| 09-10.3c | ratio, 1 µm | 0.942 | — |
| 09-10.3d | V_Dsat, 200 nm | 0.414 | V |
| 09-10.3e | I_Dsat, 200 nm | 0.212 | mA/µm |
| 09-10.3f | ratio, 200 nm | 0.763 | — |
| 09-10.3g | V_Dsat, 50 nm | 0.2419 | V |
| 09-10.3h | I_Dsat, 50 nm | 0.497 | mA/µm |
| 09-10.3i | ratio, 50 nm | 0.447 | — |
| 09-10.3j | V_Dsat, 20 nm | 0.1322 | V |
| 09-10.3k | I_Dsat, 20 nm | 0.679 | mA/µm |
| 09-10.3l | ratio, 20 nm | 0.244 | — |
| 09-10.3m | rise 200 nm to 20 nm | 3.20 | — |
| 09-10.4a | PMOS E_sat | 1.97e5 | V/cm |
| 09-10.4b | E_sat L | 0.984 | V |
| 09-10.4c | V_Dsat | 0.349 | V |
| 09-10.4d | I_Dsat | 0.239 | mA/µm |
| 09-10.4e | PMOS/NMOS ratio | 0.481 | — |
| 09-10.5a | long-channel I_D at 50 mV | 0.1959 | mA/µm |
| 09-10.5b | factor at 50 mV | 1.114 | — |
| 09-10.5c | I_D at 50 mV | 0.1758 | mA/µm |
| 09-10.5d | resistance at 50 mV | 284 | Ω·µm |
| 09-10.5e | long-channel I_D at 100 mV | 0.3728 | mA/µm |
| 09-10.5f | factor at 100 mV | 1.229 | — |
| 09-10.5g | I_D at 100 mV | 0.3034 | mA/µm |
| 09-10.5h | resistance at 100 mV | 330 | Ω·µm |
| 09-10.6a | R_S, closed form | 327 | Ω·µm |
| 09-10.6b | R_S, self-consistent | 231 | Ω·µm |
| 09-10.6c | internal overdrive at 80% | 0.558 | V |
| 09-10.7a | slope at 1 V | 289.6 | Ω/µm |
| 09-10.7b | slope at 2 V | 144.8 | Ω/µm |
| 09-10.7f | intercept at 1 V | 121.0 | Ω |
| 09-10.7g | intercept at 2 V | 135.5 | Ω |
| 09-10.7c | ΔL | 0.100 | µm |
| 09-10.7d | R_ds | 150.0 | Ω |
| 09-10.7e | μ C_ox | 345.3 | µA/V² |
| 09-10.8a | l_d | 9.97 | nm |
| 09-10.8b | roll-off at 50 mV | 40.5 | mV |
| 09-10.8c | roll-off at 1.0 V | 126 | mV |
| 09-10.8d | L for 50 mV/V | 30.9 | nm |
| 09-10.8e | prefactor A | 1.10 | — |
| 09-10.9a | l_d factor, uniform | 0.7 | — |
| 09-10.9b | l_d factor, oxide only | 0.888 | — |
| 09-10.9c | W_dep X_j factor | 0.381 | — |
| 09-10.9d | each factor | 0.617 | — |
| 09-10.10a | relative I_off, standard | 0.117 | — |
| 09-10.10b | relative I_off, high | 0.0136 | — |
| 09-10.10c | relative I_on, standard | 0.86 | — |
| 09-10.10d | relative I_on, high | 0.72 | — |
| 09-10.10e | block leakage | 0.0629 | — |
| 09-10.11a | saturation threshold | 0.258 | V |
| 09-10.11b | DIBL leakage factor | 3.63 | — |
| 09-10.11c | S at 85 °C | 89.5 | mV/decade |
| 09-10.11d | V_TH,sat at 85 °C | 0.2115 | V |
| 09-10.11e | hot vs room at V_DD | 12.0 | — |
| 09-10.11f | hot vs naive estimate | 43.5 | — |
| 09-10.12a | max V_DG, 1.5 nm | 1.345 | V |
| 09-10.12b | max V_DG, 3 nm | 1.57 | V |
| 09-10.12c | E_s at 1.8 V, 1.5 nm | 1.51 | MV/cm |
| 09-10.12d | E_s at 1.8 V, 3 nm | 0.756 | MV/cm |
| 09-10.13a | gate leakage per device | 0.200 | nA |
| 09-10.13b | chip subthreshold leakage | 1.00 | A |
| 09-10.13c | chip gate leakage | 0.200 | A |
| 09-10.13d | leakage power | 0.900 | W |
| 09-10.13e | hot leakage power | 7.68 | W |
| 09-10.13f | subthreshold share | 97.7 | % |
| 09-10.14a | φ_B | 0.4762 | V |
| 09-10.14b | W_dep | 35.1 | nm |
| 09-10.14c | mean dopant count | 56.2 | — |
| 09-10.14d | σ(V_TH) | 18.8 | mV |
| 09-10.14e | A_Vt | 0.753 | mV·µm |
| 09-10.14f | doping for 30 mV | 5.89e18 | cm⁻³ |
| 09-10.14g | dopant count there | 143 | — |
| 09-10.14h | W_dep there | 15.1 | nm |
| 09-10.15a | L_min | 21.5 | nm |
| 09-10.15b | L_min / l_d | 2.69 | — |
| 09-10.15c | roll-off at 0.9 L_min | 98.1 | mV |
| 09-10.15d | extra factor | 2.03 | — |
| 09-10.15e | total factor | 20.3 | — |
