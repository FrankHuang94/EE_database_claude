# Solutions 20-12 · Why Analog Does Not Scale Like Digital

Problems: [20-12 problem set](../problems/20-12-problems.md) · Chapter: [20-12](../chapters/20-12-why-analog-does-not-scale.md). Every number below is recomputed by [verify_20_12.py](../verify/verify_20_12.py).

---

## Solutions

### Solution 20-12.1

- Digital: delay $1/2$ = **0.5**, energy $1/8$ = **0.125**, area $1/4$ = **0.25**.
- Analog: $C \propto 1/V_{DD}^2$ grows **4**-fold; $P \propto 1/V_{DD}$ grows **2**-fold.

### Solution 20-12.2

$\sqrt{kT/C}$: **91.0** µV on 0.5 pF and **45.5** µV on 2 pF. Quadrupling the capacitance halves the noise voltage.

### Solution 20-12.3

$C = 2kT\cdot\text{SNR}/A^2 = 2 \times 4.142 \times 10^{-21} \times 10^8/0.16$ = **5.18** pF.

### Solution 20-12.4

$P = V_{DD}\cdot 2\pi fC/(\beta\,g_m/I_D) = 1.0 \times 2\pi \times 5 \times 10^7 \times 5.18 \times 10^{-12}/(0.5 \times 15)$ = **217** µW.

### Solution 20-12.5

$C \propto 1/\text{swing}^2$: swings of 0.9 V and 0.4 V give a factor $(0.9/0.4)^2$ = **5.06**. If the swing scaled with the supply the factor would be $(1.2/0.7)^2$ = **2.94**: the fixed $V_{DS,sat}$ nearly doubles the penalty.

### Solution 20-12.6

$A_i = (g_m/I_D)V_A'L$: at 0.1 µm, $10 \times 0.5$ = **5** (**14.0** dB); at 0.4 µm, **20** (**26.0** dB).

### Solution 20-12.7

Telescopic: $0.9 - 5 \times 0.12$ = **0.3** V. Four-device branch: $0.9 - 4 \times 0.12$ = **0.42** V.

### Solution 20-12.8

$C_{ox}A_{VT}^2/kT = 25 \times 10^{-15} \times (1.5 \times 10^{-3})^2/4.142 \times 10^{-21}$ = **13.6**. For 0.2 mV: mismatch $25 \times (1.5/0.2)^2$ fF = **1406** fF; noise $kT/\sigma^2$ = **104** fF.

### Solution 20-12.9

$1 + A_0/2 \ge 2^{14}$ gives $A_0 \ge$ **32766** (**90.3** dB). With calibration, the estimate must be within $2^{-14}/0.02$ = **0.31**% of the 2% error.

### Solution 20-12.10

$\varepsilon = 1/(1 + 12)$ = **7.69**%. Residual $(0.07692 - 0.0625)/(1 - 0.0625)$ = **1.54**%, which is **63** times the 12-bit budget: the calibration must track temperature, which is why background calibration exists.

### Solution 20-12.11

$P \propto V_{DD}C \propto V_{DD}/\text{swing}^2$: $(0.7/1.2) \times 5.06$ = **2.95** times more power at 0.7 V.

### Solution 20-12.12

Analog factor $0.9/0.75$ = **1.2**. Total $0.4 \times 1.2 + 0.6 \times 0.5 \times (0.75/0.9)^2$ = **0.688**: a 31% saving, not a halving. The claim would need the analog part to shrink too, for example through calibration that lets it run nearer the kT/C limit, or a smaller analog share.

### Solution 20-12.13

(a) Settling to ½ LSB at 12 bits means $e^{-T/\tau} \le 2^{-13}$, so $\tau \le 2\ \text{ns}/(13\ln 2)$ = **0.222** ns and the closed-loop bandwidth is $1/(2\pi\tau)$ = **717** MHz. A single stage's closed-loop bandwidth is $\beta g_m/C_L$, so $g_m = C_L/(\beta\tau)$ = **9.01** mS per input device. At 12 V⁻¹ each branch draws 0.751 mA: **1.50** mA in total and **1.20** mW from 0.8 V.

(b) $\varepsilon = 1/(1 + A_0\beta) = 1/(1 + 7.5)$ = **11.8**%. The residual must stay below 1/4096, so the estimate must be within $(1/4096)/0.1176$ = **0.208**% of ε: harder than Example 20-12.5's 0.39%, because the error is larger, but a background calibration can track it.

(c) No. The telescopic cascode reaches 53.1 dB but leaves 0.05 V of swing, and two simple stages give 47.0 dB: both fall more than 25 dB short of 78.3 dB, so an uncalibrated design at 0.8 V needs gain boosting or a third stage. Even the two-stage Miller amplifier, sized only for speed, costs more. Its loop crosses over at $\beta\omega_u = 1/\tau$, so $\omega_u = 2/\tau$ = 9.01 × 10⁹ rad/s. The non-dominant pole $g_{m6}/C_L \ge 2.2/\tau$ needs $g_{m6}$ = **9.91** mS, 0.826 mA per branch; the first stage needs $g_{m1} = \omega_uC_c$ = **2.25** mS, 0.188 mA per side. In total **2.03** mA and **1.62** mW, and it still provides only about 47 dB.

(d) The calibrated single stage uses **0.74** times the power of a two-stage design that does not even meet the gain target; a design that does (with gain boosting or a third stage) costs more still, and more compensation risk. The calibrated design pays instead with digital logic (small in a modern node), a calibration that must converge before the specification holds and keep tracking temperature and supply, and test time to prove it does. That is the trade §3.6 describes: analog precision replaced by digital correction, which scales.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-12.1a | delay factor | 0.5 | — |
| 20-12.1b | energy factor | 0.125 | — |
| 20-12.1c | area factor | 0.25 | — |
| 20-12.1d | analog capacitance factor | 4 | — |
| 20-12.1e | analog power factor | 2 | — |
| 20-12.2a | noise on 0.5 pF | 91.0 | µV |
| 20-12.2b | noise on 2 pF | 45.5 | µV |
| 20-12.3a | capacitance | 5.18 | pF |
| 20-12.4a | power | 217 | µW |
| 20-12.5a | capacitance factor | 5.06 | — |
| 20-12.5b | factor with proportional swing | 2.94 | — |
| 20-12.6a | gain at 0.1 µm | 5 | — |
| 20-12.6b | gain at 0.1 µm | 14.0 | dB |
| 20-12.6c | gain at 0.4 µm | 20 | — |
| 20-12.6d | gain at 0.4 µm | 26.0 | dB |
| 20-12.7a | telescopic swing | 0.3 | V |
| 20-12.7b | four-device swing | 0.42 | V |
| 20-12.8a | ratio | 13.6 | — |
| 20-12.8b | mismatch capacitance | 1406 | fF |
| 20-12.8c | noise capacitance | 104 | fF |
| 20-12.9a | open-loop gain | 32766 | — |
| 20-12.9b | open-loop gain | 90.3 | dB |
| 20-12.9c | calibration accuracy | 0.31 | % |
| 20-12.10a | hot gain error | 7.69 | % |
| 20-12.10b | residual error | 1.54 | % |
| 20-12.10c | times the budget | 63 | — |
| 20-12.11a | power factor | 2.95 | — |
| 20-12.12a | analog factor | 1.2 | — |
| 20-12.12b | total factor | 0.688 | — |
| 20-12.13a | time constant | 0.222 | ns |
| 20-12.13b | closed-loop bandwidth | 717 | MHz |
| 20-12.13c | single-stage gm | 9.01 | mS |
| 20-12.13d | single-stage current | 1.50 | mA |
| 20-12.13e | single-stage power | 1.20 | mW |
| 20-12.13f | gain error | 11.8 | % |
| 20-12.13g | required estimate accuracy | 0.208 | % |
| 20-12.13h | second-stage gm | 9.91 | mS |
| 20-12.13i | first-stage gm | 2.25 | mS |
| 20-12.13j | two-stage current | 2.03 | mA |
| 20-12.13k | two-stage power | 1.62 | mW |
| 20-12.13l | power ratio, calibrated to two-stage | 0.74 | — |
