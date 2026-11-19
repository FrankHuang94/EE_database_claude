# Solutions 09-09 · The Long-Channel MOSFET

Problems: [09-09 problems](../problems/09-09-problems.md) · Chapter: [09-09](../chapters/09-09-long-channel-mosfet.md). Every number below is recomputed by [verify_09_09.py](../verify/verify_09_09.py), by these routes:

- drain currents by integrating the channel charge numerically;
- saturation by maximizing the current;
- small-signal quantities by numerical differentiation;
- design values by root finding.

---

## Solutions

### Solution 09-09.1

With $K = \mu_nC_{ox}W/L$ = 1.0 mA/V²:

(a) $V_{GS} < V_{TH}$: cutoff, $I_D$ ≈ 0 (only subthreshold leakage).

(b) $V_{DS}$ = 0.2 V < $V_{ov}$ = 1.0 V: linear region, $I_D = K(V_{ov}V_{DS} - V_{DS}^2/2)$ = **0.180** mA.

(c) $V_{DS} > V_{ov}$: saturation, $I_D = KV_{ov}^2/2$ = **0.500** mA.

### Solution 09-09.2

$C_{ox}$ = **1.727** µF/cm², and $W/L = 1/(R\mu C_{ox}V_{ov})$ = **27.6**.

### Solution 09-09.3

The saturation current is proportional to $\mu W$, so the PMOS must be $315.1/100$ = **3.15** times wider. In practice the ratio is smaller, because strain and orientation raise hole mobility (09-12).

### Solution 09-09.4

$\phi_B$ = **0.4762** V, $W_{d\max}$ = **35.1** nm and $m = 1 + 3 \times 2/35.1$ = **1.171**. Then $V_{Dsat} = 0.6/1.171$ = **0.512** V, and the square law overestimates $I_{Dsat}$ by the factor **1.171**. The thin oxide keeps $m$ small even at heavy doping.

### Solution 09-09.5

$C_{ox}$ = **690.6** nF/cm², $\gamma = \sqrt{2qN_A\varepsilon_s}/C_{ox}$ = **0.264** V^1/2, and the linear coefficient is $\gamma/(2\sqrt{2\phi_B})$ = **0.1445**. The threshold shifts are:

- **0.0638** V at $V_{SB}$ = 0.5 V;
- **0.1164** V at 1 V;
- **0.2032** V at 2 V.

The shift grows sublinearly, as the square root predicts.

### Solution 09-09.6

(a) $\mathcal E_{\text{eff}} = (V_{GS} + 0.35 + 0.2)/(6 \times 2\text{ nm})$:

| $V_{GS}$ (V) | $\mathcal E_{\text{eff}}$ (MV/cm) | $\mu_{ns}$ (cm²/V·s) |
|---|---|---|
| 0.8 | **1.125** | **215.0** |
| 1.2 | **1.458** | **156.9** |
| 1.8 | **1.958** | **103.6** |

(b) With the varying mobility, $I_{Dsat}$ rises **5.00**-fold; with a constant mobility it would rise **10.38**-fold. Mobility degradation roughly halves the benefit of the extra gate voltage, which is one reason real transfer curves look closer to linear than square-law at high overdrive.

### Solution 09-09.7

$W = 2mLI_D/(\mu C_{ox}V_{ov}^2)$ = **7.16** µm. The average field at saturation is $(0.8/1.246)/0.5\text{ µm}$ = **1.28 × 10⁴** V/cm, a factor of **3.96** below $\mathcal E_{sat}$ = 5.08 × 10⁴ V/cm. That is marginal: velocity saturation already trims the current noticeably (09-10 quantifies this). At 0.5 µm and this overdrive, the device is entering the short-channel regime.

### Solution 09-09.8

$\Delta L = \sqrt{2\varepsilon_s \times 0.5/(qN_A)}$ = **36.0** nm. As a fraction of $L$:

- **7.19**% at 0.5 µm;
- **3.60**% at 1 µm;
- **1.80**% at 2 µm.

Output resistance therefore grows faster than linearly with $L$ (both $\Delta L/L$ and the current fall).

### Solution 09-09.9

$g_m/I_D = 2/V_{ov}$: **20.0**, **10.0** and **4.0** V⁻¹ at 0.1, 0.2 and 0.5 V. The weak-inversion limit is $1/(1.3V_T)$ = **29.76** V⁻¹. The strong-inversion formula would reach it at $V_{ov} = 2mV_T$ = **67.2** mV. Below roughly that overdrive the square law fails, and the device enters moderate inversion, where $g_m/I_D$ saturates at the weak-inversion value.

### Solution 09-09.10

$f_T = 3\mu V_{ov}/(4\pi mL^2)$:

- **0.746** GHz at 2 µm;
- **2.98** GHz at 1 µm;
- **11.94** GHz at 0.5 µm.

The $1/L^2$ scaling is the long-channel promise. Velocity saturation (09-10) weakens it to roughly $1/L$ in short devices.

### Solution 09-09.11

(a) $S = mV_T\ln10$: **65.5** mV/decade for $m$ = 1.1 and **77.4** mV/decade for $m$ = 1.3.

(b) $I_{off} = 100\text{ nA} \times 10 \times 10^{-0.3/0.0774}$ = **1.33 × 10⁻¹⁰** A.

(c) $10^{0.15/0.0774}$ = **86.8** times less leakage.

### Solution 09-09.12

At 358.15 K:

- $S = 1.3 \times (k \times 358.15/q) \times \ln10$ = **92.4** mV/decade;
- $V_{TH} = 0.3 - 0.058$ = **0.2419** V;
- $I_{off} = 1\text{ µA} \times 10^{-0.2419/0.0924}$ = **2.41 × 10⁻⁹** A, against **1.33 × 10⁻¹⁰** A at 300 K.

The ratio is **18.1**. Junction leakage (09-06), which this estimate omits, rises even faster with temperature. Leakage at the hot corner, not at room temperature, sets battery and thermal budgets.

### Solution 09-09.13

$C_{gs} = \tfrac23WLC_{ox} + C_{ov}$ = 57.55 + 2 = **59.55** fF. The Miller effect multiplies the 2 fF gate–drain overlap by $1 - A_v$ = 11, adding **22.0** fF, so $C_{in}$ = **81.55** fF. (Why $1 - A_v$: when the gate moves by $v_g$, the drain moves by $A_vv_g$, so the voltage across $C_{gd}$ changes by $(1 - A_v)v_g$ and the gate must supply charge $C_{gd}(1 - A_v)v_g$, as if a capacitor $(1 - A_v)C_{gd}$ hung from the gate to ground.) Even a small $C_{gd}$ dominates the input once the gain is large (Course 12).

### Solution 09-09.14

$m$ = **1.475** and $\gamma$ = **0.944** V^1/2.

- $m$-model: $V_{Dsat} = 0.8/1.475$ = **0.542** V.
- Exact: the charge vanishes at **0.563** V.

The $m$-model underestimates $I_{Dsat}$ by **2.53**%, more than at 5 × 10¹⁷ cm⁻³: the linearization error grows with doping, because the bulk-charge slope varies more along the channel.

### Solution 09-09.15

$W/L = 2mI_D/(\mu C_{ox}V_{ov}^2)$ = **22.98**, so $W$ = **22.98** µm. Then:

- $g_m = 2I_D/V_{ov}$ = **1.00** mS;
- $r_o = 1/(\lambda I_D)$ = **250** kΩ;
- intrinsic gain $g_mr_o$ = **250**;
- $C_{gs} = \tfrac23WLC_{ox}$ = **132.2** fF;
- $f_T = g_m/(2\pi C_{gs})$ = **1.20** GHz.

Low overdrive buys gain and efficiency ($g_m/I_D$ = **10.0** V⁻¹) at the cost of width and speed.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-09.1a | linear current | 0.180 | mA |
| 09-09.1b | saturation current | 0.500 | mA |
| 09-09.2a | C_ox, 2 nm | 1.727 | µF/cm² |
| 09-09.2b | W/L | 27.6 | — |
| 09-09.3a | PMOS width ratio | 3.15 | — |
| 09-09.4a | φ_B at 1e18 | 0.4762 | V |
| 09-09.4b | W_dmax | 35.1 | nm |
| 09-09.4c | m | 1.171 | — |
| 09-09.4d | V_Dsat | 0.512 | V |
| 09-09.5a | C_ox, 5 nm | 690.6 | nF/cm² |
| 09-09.5b | γ | 0.264 | V^1/2 |
| 09-09.5c | linear coefficient | 0.1445 | — |
| 09-09.5d | shift at 0.5 V | 0.0638 | V |
| 09-09.5e | shift at 1 V | 0.1164 | V |
| 09-09.5f | shift at 2 V | 0.2032 | V |
| 09-09.6a | E_eff at 0.8 V | 1.125 | MV/cm |
| 09-09.6b | μ at 0.8 V | 215.0 | cm²/V·s |
| 09-09.6c | E_eff at 1.2 V | 1.458 | MV/cm |
| 09-09.6d | μ at 1.2 V | 156.9 | cm²/V·s |
| 09-09.6e | E_eff at 1.8 V | 1.958 | MV/cm |
| 09-09.6f | μ at 1.8 V | 103.6 | cm²/V·s |
| 09-09.6g | current ratio with degradation | 5.00 | — |
| 09-09.6h | current ratio, constant mobility | 10.38 | — |
| 09-09.7a | width for 1 mA | 7.16 | µm |
| 09-09.7b | average field | 1.28e4 | V/cm |
| 09-09.7c | margin to E_sat | 3.96 | — |
| 09-09.8a | ΔL | 36.0 | nm |
| 09-09.8b | fraction at 0.5 µm | 7.19 | % |
| 09-09.8c | fraction at 1 µm | 3.60 | % |
| 09-09.8d | fraction at 2 µm | 1.80 | % |
| 09-09.9a | g_m/I_D at 0.1 V | 20.0 | V⁻¹ |
| 09-09.9b | g_m/I_D at 0.2 V | 10.0 | V⁻¹ |
| 09-09.9c | g_m/I_D at 0.5 V | 4.0 | V⁻¹ |
| 09-09.9d | weak-inversion limit | 29.76 | V⁻¹ |
| 09-09.9e | overdrive where they meet | 67.2 | mV |
| 09-09.10a | f_T at 2 µm | 0.746 | GHz |
| 09-09.10b | f_T at 1 µm | 2.98 | GHz |
| 09-09.10c | f_T at 0.5 µm | 11.94 | GHz |
| 09-09.11a | S, m = 1.1 | 65.5 | mV/decade |
| 09-09.11b | S, m = 1.3 | 77.4 | mV/decade |
| 09-09.11c | I_off at V_TH 0.3 V | 1.33e-10 | A |
| 09-09.11d | leakage reduction for 0.45 V | 86.8 | — |
| 09-09.12a | S at 85 °C | 92.4 | mV/decade |
| 09-09.12b | V_TH at 85 °C | 0.2419 | V |
| 09-09.12c | I_off at 85 °C | 2.41e-9 | A |
| 09-09.12d | leakage ratio | 18.1 | — |
| 09-09.13a | C_gs | 59.55 | fF |
| 09-09.13b | Miller addition | 22.0 | fF |
| 09-09.13c | C_in | 81.55 | fF |
| 09-09.14a | m at 2e18 | 1.475 | — |
| 09-09.14b | γ | 0.944 | V^1/2 |
| 09-09.14c | V_Dsat, m-model | 0.542 | V |
| 09-09.14d | V_Dsat, exact | 0.563 | V |
| 09-09.14e | m-model shortfall | 2.53 | % |
| 09-09.15a | W/L | 22.98 | — |
| 09-09.15b | g_m | 1.00 | mS |
| 09-09.15c | r_o | 250 | kΩ |
| 09-09.15d | intrinsic gain | 250 | — |
| 09-09.15e | C_gs | 132.2 | fF |
| 09-09.15f | f_T | 1.20 | GHz |
| 09-09.15g | g_m/I_D | 10.0 | V⁻¹ |
