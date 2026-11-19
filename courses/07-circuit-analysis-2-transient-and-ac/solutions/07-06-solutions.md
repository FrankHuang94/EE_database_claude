# Solutions 07-06 · AC Power and Power Factor

Problems: [07-06 problems](../problems/07-06-problems.md) · Chapter: [07-06](../chapters/07-06-ac-power-and-power-factor.md). Every number below is recomputed by [verify_07_06.py](../verify/verify_07_06.py), mostly by integrating $v(t)i(t)$ and $i^2(t)$ numerically over a period; values marked † are also confirmed by ngspice in [labs/07-06-lab](../labs/07-06-lab/README.md).

---

## Solutions

### Solution 07-06.1

(a) Over one period the sawtooth is $At/T$, so its mean square is $\frac1T\int_0^T(At/T)^2dt = A^2/3$: RMS **$A/\sqrt3$ = 0.5774 A**.

(b) The half-wave rectified sine is $A\sin\omega t$ for half the period and zero for the other half. Its mean square is half of a full sine's, $A^2/4$: RMS **$A/2$ = 0.5000 A**.

(c) Squaring removes the sign, so a full-wave rectified sine has the same mean square as the sine, $A^2/2$: RMS **$A/\sqrt2$ = 0.7071 A**.

### Solution 07-06.2

$S = \tfrac12\mathbf{V}\mathbf{I}^* = \tfrac12(100\angle20°)(5\angle15°) = 250\angle35°$ VA $= 204.8 + j143.4$ VA. So $\lvert S\rvert$ = **250.0 VA**, $P$ = **204.8 W**, $Q$ = **143.4 var**, and PF $= \cos35° = $ **0.8192**, lagging (voltage leads current, $Q > 0$).

With the current's phase as the time reference, the decomposition of 07-06 §3.4 gives $p(t) = 204.8(1 + \cos2\omega t) - 143.4\sin2\omega t$ W. The two oscillating terms combine into one sinusoid of amplitude $\sqrt{P^2 + Q^2} = \lvert S\rvert$, so $p$ swings between $P + \lvert S\rvert = $ **454.8 W** and $P - \lvert S\rvert = $ **−45.2 W**. For part of each cycle the load returns energy to the source.

### Solution 07-06.3

An ideal inductor absorbs **0 W**. Its reactive power is $Q = I_{rms}^2X = 1^2\times2\pi\times1000\times0.01 = $ **62.83 var**.

### Solution 07-06.4

The loads in parallel: $Z_p = Z_1Z_2/(Z_1 + Z_2) = (36\,750 + j13\,500)/2725 = $ **13.49 + j4.954 Ω**. The line current is $\mathbf{I}_{rms} = 230/(Z_{line} + Z_p) = $ **15.65 A ∠ −21.37°**, and the load voltage $\mathbf{V}_{load,rms} = \mathbf{I}_{rms}Z_p = $ **224.9 V ∠ −1.195°**. All phasors in this solution are RMS, so $S = \mathbf{V}_{rms}\mathbf{I}_{rms}^*$ with no factor ½. Complex powers (source delivering, others absorbing):

| Element | $S$ (VA) |
|---|---|
| Source, delivered: $230\,\mathbf{I}_{rms}^*$ | 3352.2 + j1311.4 |
| Line: $I^2(0.2 + j0.4)$ | 49.0 + j98.0 |
| Load 1: $V_L^2/Z_1^*$ | 1617.9 + j1213.4 |
| Load 2: $V_L^2/30$ | 1685.3 + j0 |
| Sum of absorbed | 3352.2 + j1311.4 |

The absorbed powers sum exactly to the delivered power: **3352 W** and **1311 var**. Real and reactive power each balance separately.

### Solution 07-06.5

$\theta_1 = \arccos0.70 = 45.57°$, $\tan\theta_1 = 1.0202$; $\tan\theta_2 = \tan(\arccos0.95) = 0.3287$. Then $Q_C = 5000(1.0202 - 0.3287) = $ **3458 var** and $C = Q_C/(\omega V^2) = 3458/(314.16\times230^2) = $ **208.1 µF**. The current falls from $5000/(230\times0.70) = $ **31.06 A** to $5000/(230\times0.95) = $ **22.88 A**.

### Solution 07-06.6

Unity: $Q_C = Q_1 = 5101$ var, $C = $ **306.9 µF**. 0.95 leading: the capacitor must cancel the motor's 5101 var and add **1643 var** leading, $Q_C = 6744$ var, $C = $ **405.8 µF**. Going from 0.95 lagging (208.1 µF) to unity takes **47.5%** more capacitance for a current reduction of only **5.0%** (22.88 A to 21.74 A; current scales as 1/PF), and going leading gives back that improvement while adding even more capacitance: a leading power factor of 0.95 draws the same current as a lagging one. Near unity, $\tan\theta$ changes little, so the last increment of power factor is expensive.

### Solution 07-06.7

(a) Billed demand $= 100\times0.90/0.70 = $ **128.6 kW** (Minnesota Power's example, published as 129 kW).

(b) $Q_C = 100(\tan\theta_{0.70} - \tan\theta_{0.90}) = 100(1.0202 - 0.4843) = $ **53.59 kvar**.

### Solution 07-06.8

Conjugate match $Z_L = 4 - j3$ Ω gives $P_{max} = V_{Th,rms}^2/(4R_{Th}) = 400/16 = $ **25.00 W**. The best resistor is $R_L = \lvert Z_{Th}\rvert = $ **5.000 Ω**, with $I_{rms} = 20/\lvert9 + j3\rvert = 2.108$ A and $P = 2.108^2\times5 = $ **22.22 W**.

### Solution 07-06.9

$I_{rms} = \sqrt{5^2 + 2^2 + 1^2} = \sqrt{30} = $ **5.477 A**. THD $= \sqrt{2^2 + 1^2}/5 = $ **44.72%**. Only the fundamental carries power: $P = 230\times5 = $ **1150 W**, and PF $= P/(V_{rms}I_{rms}) = 5/5.477 = $ **0.9129**, entirely from distortion.

### Solution 07-06.10

PF $= \cos30°/\sqrt{1 + 0.5^2} = 0.8660/1.1180 = $ **0.7746**. A meter that assumes sinusoidal current and measures the phase of the fundamental would report the displacement factor, **0.8660**, overstating the power factor by **11.8%**.

### Solution 07-06.11

$P_{in} = 1500/0.96 = $ **1563 W** (1562.5 W), so the losses are **62.5 W**. $\lvert S\rvert = 1562.5/0.95 = $ **1645 VA**, and $I = 1644.7/230 = $ **7.151 A**.

### Solution 07-06.12

$I = P/(V\,\text{PF})$ and $P_{loss} = I^2R = P^2R/(V^2\text{PF}^2)$:

- (a) 230 V, PF 1: $I$ = 217.4 A, loss **2363 W** = **4.726%**.
- (b) 230 V, PF 0.8: $I$ = 271.7 A, loss **3692 W** = **7.384%**.
- (c) 400 V, PF 0.8: $I$ = 156.3 A, loss **1221 W** = **2.441%**.

The loss scales as $1/(V^2\,\text{PF}^2)$: raising the voltage from 230 V to 400 V cuts it by $(400/230)^2 = $ **3.025**, more than enough to offset the poor power factor. This is why distribution moves to higher voltages (data centers to 400/230 V or above, 07-11) as well as correcting power factor.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-06.1a | sawtooth RMS / A | 0.5774 | — |
| 07-06.1b | half-wave RMS / A | 0.5000 | — |
| 07-06.1c | full-wave RMS / A | 0.7071 | — |
| 07-06.2a | $\lvert S\rvert$ | 250.0 | VA |
| 07-06.2b | P | 204.8 | W |
| 07-06.2c | Q | 143.4 | var |
| 07-06.2d | PF | 0.8192 | — |
| 07-06.2e | maximum instantaneous power | 454.8 | W |
| 07-06.2f | minimum instantaneous power | −45.2 | W |
| 07-06.3a | real power | 0 | W |
| 07-06.3b | reactive power | 62.83 | var |
| 07-06.4a | line current | 15.65 | A |
| 07-06.4b | its angle | −21.37 | ° |
| 07-06.4c | load voltage | 224.9 | V |
| 07-06.4d | its angle | −1.195 | ° |
| 07-06.4e | total real power | 3352 | W |
| 07-06.4f | total reactive power | 1311 | var |
| 07-06.4g | line real power | 49.0 | W |
| 07-06.4h | load 1 real power | 1617.9 | W |
| 07-06.4i | load 1 reactive power | 1213.4 | var |
| 07-06.4j | load 2 real power | 1685.3 | W |
| 07-06.4k | $Z_p$ real part | 13.49 | Ω |
| 07-06.4l | $Z_p$ imaginary part | 4.954 | Ω |
| 07-06.4m | line reactive power | 98.0 | var |
| 07-06.5a | capacitor kvar | 3458 | var |
| 07-06.5b | capacitance | 208.1 | µF |
| 07-06.5c | current before | 31.06 | A |
| 07-06.5d | current after | 22.88 | A |
| 07-06.6a | capacitance for unity | 306.9 | µF |
| 07-06.6b | capacitance for 0.95 leading | 405.8 | µF |
| 07-06.6c | current at unity | 21.74 | A |
| 07-06.6d | leading var added | 1643 | var |
| 07-06.6e | extra capacitance for unity versus 0.95 | 47.5 | % |
| 07-06.6f | current reduction from 0.95 to unity | 5.0 | % |
| 07-06.7a | billed demand | 128.6 | kW |
| 07-06.7b | capacitor kvar to reach 0.90 | 53.59 | kvar |
| 07-06.8a | $P_{max}$ | 25.00 | W |
| 07-06.8b | best resistor | 5.000 | Ω |
| 07-06.8c | power to it | 22.22 | W |
| 07-06.9a | RMS current | 5.477 | A |
| 07-06.9b | THD | 44.72 | % |
| 07-06.9c | power factor | 0.9129 | — |
| 07-06.9d | real power | 1150 | W |
| 07-06.10a | true power factor | 0.7746 | — |
| 07-06.10b | displacement factor | 0.8660 | — |
| 07-06.10c | overstatement | 11.8 | % |
| 07-06.11a | input power | 1563 | W |
| 07-06.11b | losses | 62.5 | W |
| 07-06.11c | apparent power | 1645 | VA |
| 07-06.11d | input current | 7.151 | A |
| 07-06.12a | loss at 230 V, PF 1 | 2363 | W |
| 07-06.12b | as a percentage | 4.726 | % |
| 07-06.12c | loss at 230 V, PF 0.8 | 3692 | W |
| 07-06.12d | as a percentage | 7.384 | % |
| 07-06.12e | loss at 400 V, PF 0.8 | 1221 | W |
| 07-06.12f | as a percentage | 2.441 | % |
| 07-06.12g | loss reduction factor from 230 V to 400 V | 3.025 | — |
