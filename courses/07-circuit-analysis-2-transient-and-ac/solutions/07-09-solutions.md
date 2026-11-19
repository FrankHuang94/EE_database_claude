# Solutions 07-09 · Mutual Inductance and Transformers

Problems: [07-09 problems](../problems/07-09-problems.md) · Chapter: [07-09](../chapters/07-09-mutual-inductance-and-transformers.md). Every number below is recomputed by [verify_07_09.py](../verify/verify_07_09.py), mostly by integrating the coupled-coil differential equations or solving the mesh equations numerically; the circuit results that ngspice also confirms are named in the `* EXPECT` lines of the netlists in [labs/07-09-lab](../labs/07-09-lab/README.md).

---

## Solutions

### Solution 07-09.1

$k = 6/\sqrt{5\times20}$ = **0.6000**.

(a) Both currents enter dots, so the mutual terms are positive: $v_1 = 0.005\times200 + 0.006\times100$ = **1.60 V**; $v_2 = 0.006\times200 + 0.02\times100$ = **3.20 V**.

(b) One enters, one leaves: the mutual terms change sign. $v_1 = 1.0 - 0.6$ = **0.40 V**; $v_2 = -1.2 + 2.0$ = **0.80 V**.

### Solution 07-09.2

Aiding: $L_1 + L_2 + 2M$; opposing: $L_1 + L_2 - 2M$. Their difference is $4M = 70 - 30$ = 40 mH, so $M$ = **10.0 mH** and $k = 10/\sqrt{20\times30}$ = **0.4082**. (The sum, 100 mH, checks: $2(L_1 + L_2)$ = 100 mH ✓.)

### Solution 07-09.3

$V_2 = 120/10$ = **12.0 V**; $I_2 = 12/12$ = **1.00 A**; $I_1 = I_2/10$ = **0.100 A**; the source sees $10^2\times12$ = **1200 Ω** ($= 120/0.1$ ✓).

### Solution 07-09.4

With opposing fluxes, $w = \tfrac12L_1i_1^2 + \tfrac12L_2i_2^2 - Mi_1i_2$. Setting $dw/di_2 = L_2i_2 - Mi_1 = 0$: $i_2 = Mi_1/L_2 = 1.5\times2/4$ = **0.750 A**, flowing in the direction that makes the opposing fluxes cancel as much as possible. Then $w_{min} = \tfrac12i_1^2(L_1 - M^2/L_2) = \tfrac12\times4\times(1 - 2.25/4)$ mJ = **0.875 mJ**. $k = 1.5/\sqrt{4}$ = **0.750**. If $M$ exceeded $\sqrt{L_1L_2}$ = 2 mH, $L_1 - M^2/L_2$ would be negative and the pair could store negative energy, which a passive device cannot do (§3.3).

### Solution 07-09.5

T-equivalent: series arms $L_1 - M$ = **0 mH** and $L_2 - M$ = **30 mH**, shunt leg $M$ = **10 mH**. With the secondary shorted, the 30 mH arm is in parallel with the 10 mH leg: 7.5 mH, in series with the 0 mH arm. So $Z = j\omega\times7.5$ mH = **j47.12 Ω** at 1 kHz. Check with §3.4: $j\omega L_1(1 - k^2) = j6283\times0.01\times0.75$ ✓.

### Solution 07-09.6

$Z_{22} = 50 + j62.83$ Ω and $\omega M$ = 31.42 Ω, so $Z_r = (31.42)^2/(50 + j62.83)$ = **7.653 − j9.618 Ω**, magnitude **12.29 Ω**. The reactance is negative: an inductive secondary reflects as **capacitive**.

### Solution 07-09.7

$N_1/N_2 = \sqrt{600/50}$ = **3.464**. Matched, $P = V^2/(4R_s) = 1/2400$ W = **0.4167 mW**. Directly, $P = (1/650)^2\times50$ = **0.1183 mW**: matching delivers 3.5 times as much.

### Solution 07-09.8

$I_{HV} = 10\,000/2400$ = **4.167 A**. Open circuit: $R_c = 240^2/60$ = **960.0 Ω**; $Q = \sqrt{(240\times0.8)^2 - 60^2}$ = 182.4 var; $X_m = 240^2/182.4$ = **315.8 Ω**. Short circuit: $R_{eq} = 180/4.167^2$ = **10.37 Ω**; $Z_{eq} = 48/4.167$ = 11.52 Ω; $X_{eq} = \sqrt{11.52^2 - 10.37^2}$ = **5.021 Ω**. This small transformer's series impedance is mostly resistive.

### Solution 07-09.9

$x^* = \sqrt{60/180}$ = **0.5774**, where η = **97.96%** (copper loss = core loss = 60 W on 5.774 kW).

| Load | η at PF 1 | η at PF 0.8 |
|---|---|---|
| 25% | **97.23%** | **96.56%** |
| 50% | **97.94%** | **97.44%** |
| 100% | **97.66%** | **97.09%** |

The same losses on less real power make every lagging-PF efficiency lower.

### Solution 07-09.10

Losses $= P(1/\eta - 1)$ with $P$ = half the rating:

- 167 kVA ($P$ = 83.5 kW): **563.2 W** at 99.33% and **453.3 W** at 99.46%, a cut of **19.5%**.
- 25 kVA ($P$ = 12.5 kW): **132.6 W** at 98.95% and **126.3 W** at 99.00%, a cut of **4.81%**.

Small changes in the efficiency figure are large changes in the loss figure, because the loss is $1 - \eta$.

### Solution 07-09.11

Lagging (load current lags, $\sin\theta$ = 0.6): $\Delta V \approx 4.167(10.37\times0.8 + 5.021\times0.6)$ = 47.11 V, **1.963%**; exactly **1.964%**. Leading ($\sin\theta$ = −0.6): $\Delta V \approx 4.167(8.294 - 3.013)$ = 22.01 V, **0.917%**; exactly **0.933%**. The leakage reactance's drop $jX\mathbf{I}$ points partly *against* the load voltage for a leading current (07-05 §3.5), offsetting the resistive drop.

### Solution 07-09.12

(a) $C = 1/(\omega^2L) = 1/\big((2\pi\times360\ \text{kHz})^2\times24\ \text{µH}\big)$ = **8.144 nF**.

(b) With the secondary tuned, $Z_{22} = R_2 + R_L$ = 5.2 Ω, purely resistive, so the reflected impedance is a resistance $(\omega M)^2/5.2$. The efficiency is the product of the primary's share, $R_{ref}/(R_1 + R_{ref})$, and the secondary's share, $R_L/(R_2 + R_L)$:

| $k$ | $R_{ref}$ | Efficiency |
|---|---|---|
| 0.25 | **35.42 Ω** | **95.6%** |
| 0.1 | **5.667 Ω** | **92.9%** |
| 0.03 | **0.5101 Ω** | **69.1%** |

As the coils move apart ($k$ falls), the reflected resistance falls as $k^2$ until the primary coil's own resistance takes a large share.

(c) Untuned, $Z_{22} = 5.2 + j54.29$ Ω, and the reflected impedance is **0.3220 − j3.362 Ω**: a small resistance, so the efficiency falls to **59.3%**, and the primary must also supply a large reactive current. Tuning cancels the secondary's reactance so that it reflects a large, purely resistive load; the primary is tuned too in practice, so the source sees a resistive input.

### Solution 07-09.13

(a) $N = V/(4.443\,fAB_m)$ with $A = 2\times10^{-4}$ m²: at 60 Hz, **9003** turns; at 100 kHz, **5.402** turns (6 in practice).

(b) $A = 120/(4.443\times10^5\times10\times0.25)$ = **1.080 cm²**.

(c) Core loss per unit volume rises steeply with frequency, so $B_m$ must be lowered as frequency rises; winding AC resistance (skin and proximity effects) rises; and the switches driving the transformer lose energy on every transition. The optimum is a balance of these, which wide-bandgap switches push to higher frequencies (§9).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-09.1a | k | 0.6000 | — |
| 07-09.1b | $v_1$, both enter | 1.60 | V |
| 07-09.1c | $v_2$, both enter | 3.20 | V |
| 07-09.1d | $v_1$, one leaves | 0.40 | V |
| 07-09.1e | $v_2$, one leaves | 0.80 | V |
| 07-09.2a | M | 10.0 | mH |
| 07-09.2b | k | 0.4082 | — |
| 07-09.3a | secondary voltage | 12.0 | V |
| 07-09.3b | secondary current | 1.00 | A |
| 07-09.3c | primary current | 0.100 | A |
| 07-09.3d | resistance seen | 1200 | Ω |
| 07-09.4a | $i_2$ at minimum energy | 0.750 | A |
| 07-09.4b | minimum energy | 0.875 | mJ |
| 07-09.4c | k | 0.750 | — |
| 07-09.5a | arm $L_1 - M$ | 0 | mH |
| 07-09.5b | arm $L_2 - M$ | 30 | mH |
| 07-09.5c | leg M | 10 | mH |
| 07-09.5d | reactance with shorted secondary | 47.12 | Ω |
| 07-09.6a | reflected resistance | 7.653 | Ω |
| 07-09.6b | reflected reactance | −9.618 | Ω |
| 07-09.6c | magnitude | 12.29 | Ω |
| 07-09.7a | turns ratio | 3.464 | — |
| 07-09.7b | matched power | 0.4167 | mW |
| 07-09.7c | direct power | 0.1183 | mW |
| 07-09.8a | rated high-voltage current | 4.167 | A |
| 07-09.8b | $R_c$ | 960.0 | Ω |
| 07-09.8c | $X_m$ | 315.8 | Ω |
| 07-09.8d | $R_{eq}$ | 10.37 | Ω |
| 07-09.8e | $X_{eq}$ | 5.021 | Ω |
| 07-09.9a | load fraction at maximum efficiency | 0.5774 | — |
| 07-09.9b | maximum efficiency | 97.96 | % |
| 07-09.9c | 25%, PF 1 | 97.23 | % |
| 07-09.9d | 25%, PF 0.8 | 96.56 | % |
| 07-09.9e | 50%, PF 1 | 97.94 | % |
| 07-09.9f | 50%, PF 0.8 | 97.44 | % |
| 07-09.9g | 100%, PF 1 | 97.66 | % |
| 07-09.9h | 100%, PF 0.8 | 97.09 | % |
| 07-09.10a | 167 kVA losses, 2016 level | 563.2 | W |
| 07-09.10b | 167 kVA losses, 2029 level | 453.3 | W |
| 07-09.10c | cut | 19.5 | % |
| 07-09.10d | 25 kVA losses, 2016 level | 132.6 | W |
| 07-09.10e | 25 kVA losses, 2029 level | 126.3 | W |
| 07-09.10f | cut | 4.81 | % |
| 07-09.11a | regulation, lagging (approximate) | 1.963 | % |
| 07-09.11b | regulation, lagging (exact) | 1.964 | % |
| 07-09.11c | regulation, leading (approximate) | 0.917 | % |
| 07-09.11d | regulation, leading (exact) | 0.933 | % |
| 07-09.12a | tuning capacitance | 8.144 | nF |
| 07-09.12b | reflected resistance, k = 0.25 | 35.42 | Ω |
| 07-09.12c | efficiency, k = 0.25 | 95.6 | % |
| 07-09.12d | reflected resistance, k = 0.1 | 5.667 | Ω |
| 07-09.12e | efficiency, k = 0.1 | 92.9 | % |
| 07-09.12f | reflected resistance, k = 0.03 | 0.5101 | Ω |
| 07-09.12g | efficiency, k = 0.03 | 69.1 | % |
| 07-09.12h | untuned reflected resistance | 0.3220 | Ω |
| 07-09.12i | untuned reflected reactance | −3.362 | Ω |
| 07-09.12j | untuned efficiency | 59.3 | % |
| 07-09.13a | turns at 60 Hz | 9003 | — |
| 07-09.13b | turns at 100 kHz | 5.402 | — |
| 07-09.13c | area at 100 kHz, 10 turns | 1.080 | cm² |
