# Solutions 10-03 · BJT DC Operation and Biasing

Problems: [10-03 problems](../problems/10-03-problems.md) · Chapter: [10-03](../chapters/10-03-bjt-dc-operation-and-biasing.md). Every number below is recomputed by [verify_10_03.py](../verify/verify_10_03.py), which solves each circuit with an exponential (Ebers–Moll) transistor and reads the region off the solution.

---

## Solutions

### Solution 10-03.1

(a) Active. (b) Saturated: $V_{CE}$ is below 0.3 V, and the collector junction is forward-biased by 0.62 V. (c) Cutoff: 0.3 V is far below turn-on. (d) Saturated.

### Solution 10-03.2

$\alpha = \beta/(\beta + 1)$: **0.9804**, **0.9901** and **0.9967**. $\beta = \alpha/(1 - \alpha)$ = **199**. Because β depends on $1 - \alpha$, the small fraction of emitter current lost to the base, a 0.3% change in α (0.990 to 0.997) is a threefold change in β.

### Solution 10-03.3

$I_B = (3 - 0.7)/200\text{ kΩ}$ = **11.5** µA, $I_C$ = **1.38** mA and $V_C = 9 - 3 \times 1.38$ = **4.86** V: active.

### Solution 10-03.4

(a) $R_E = 1.5\text{ V}/1\text{ mA}$ = **1.5** kΩ; $R_C \le (9 - 3 - 1.5)/1\text{ mA}$ = **4.5** kΩ.

(b) $V_B = 1.5 + 0.7$ = **2.2** V; the divider is $9\text{ V}/0.1\text{ mA}$ = **90** kΩ in total, so $R_2 = 90 \times 2.2/9$ = **22** kΩ and $R_1$ = **68** kΩ.

(c) $R_{Th}$ = 68 ∥ 22 = **16.62** kΩ and $V_{Th}$ = 2.2 V, so $I_E = 1.5/(1.5 + 16.62/101)\text{ kΩ}$ and $I_C$ = **0.892** mA, **−10.8**% from the target. The ten-times rule makes the divider stiff enough for *stability*, but the base current still drops $I_BR_{Th}$ = 0.15 V across the Thévenin resistance; to hit the target, raise $V_B$ by that amount or stiffen the divider.

### Solution 10-03.5

(a) β = 300: **0.961** mA, **+7.74**% over β = 100.

(b) $V_{BE}$ = 0.6 V: **0.952** mA, **+6.67**%.

### Solution 10-03.6

(a) $R_C$ carries $I_E$, so $V_C = V_{CC} - I_ER_C$; the base loop gives $V_C = I_BR_B + V_{BE} = I_ER_B/(\beta + 1) + V_{BE}$. Equating and solving gives the formula.

(b) $I_E$ = **1.080** mA, $I_C$ = **1.070** mA and $V_C$ = **2.839** V.

(c) β = 300: **1.608** mA, **+50.4**%. The feedback helps (base-current bias would triple), but $R_B/(\beta + 1)$ is comparable to $R_C$, so β still matters; the four-resistor bias moves only 6% (Figure 2).

### Solution 10-03.7

(a) $I_B$ = **5.0** mA, and $R_B \le (5 - 0.95)/5\text{ mA}$ = **810** Ω.

(b) $I_B = 4.05/750$ = **5.40** mA, forced β **9.26**.

(c) $0.4 \times 0.05$ = **20** mW.

### Solution 10-03.8

(a) $0.5/(1 + 2/50)$ = **0.4808** mA, **−3.85**%.

(b) The two base currents, $2I_C/\beta$, now come from the buffer's emitter, whose base takes only $2I_C/[\beta(\beta + 1)]$ from the reference node. So $I_{ref} = I_C[1 + 2/(\beta(\beta + 1))]$ and $I_{out}$ = **0.4996** mA, an error of only **−0.078**%.

### Solution 10-03.9

At −40 °C, $V_{BE}$ = 0.83 V: $I_C$ = **1.167** mA. At 85 °C, 0.58 V: **1.396** mA. Across the range the current rises by **19.6**%: about 0.16% per kelvin, against 7.7% per kelvin at fixed $V_{BE}$.

### Solution 10-03.10

At fixed $V_{BE}$, $L = (I_C/V_T)(2\text{ mV/K})(V_{CE}R_{\theta JA})$, which reaches 1 at $I_C = V_T/(0.002 \times 1000)$ = **12.93** mA. With $R_E$ = 10 Ω, $L = 0.002 \times 1000/(10 + V_T/I_C)$, which approaches its largest value, **0.2**, at high current: the loop can never run away.

### Solution 10-03.11

(a) $I_B$ = **2.0** mA and $R_B = (1.8 - 0.85)/2\text{ mA}$ = **475** Ω.

(b) $I_B = (1.8 - 0.98)/475$ = **1.73** mA, forced β **11.6**, still far below the minimum β of 100 at 10 mA [1]: saturated, with margin. The lesson is that from 1.8 V logic, $V_{BE}$'s temperature drift takes a large bite (14%) out of the base drive.

(c) $(5 - 2 - 0.2)/20\text{ mA}$ = **140** Ω.

### Solution 10-03.12

(a) $I_E = (9 - 0.7)/(1 + 330/(\beta + 1))\text{ kΩ}$: **1.926** mA at β = 100 and **3.946** mA at β = 300, **+105**%.

(b) The emitter resistor only helps when it dominates the base resistance as seen from the emitter: here $R_B/(\beta + 1)$ = 3.3 kΩ dwarfs $R_E$ = 1 kΩ, so the current is still set mostly by β. In the four-resistor bias, $R_{Th}/(\beta + 1)$ = 82 Ω is small against $R_E$.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-03.2a | α at β = 50 | 0.9804 | — |
| 10-03.2b | α at β = 100 | 0.9901 | — |
| 10-03.2c | α at β = 300 | 0.9967 | — |
| 10-03.2d | β at α = 0.995 | 199 | — |
| 10-03.3a | I_B | 11.5 | µA |
| 10-03.3b | I_C | 1.38 | mA |
| 10-03.3c | V_C | 4.86 | V |
| 10-03.4a | R_E | 1.5 | kΩ |
| 10-03.4b | largest R_C | 4.5 | kΩ |
| 10-03.4c | V_B | 2.2 | V |
| 10-03.4d | divider total | 90 | kΩ |
| 10-03.4e | R_2 | 22 | kΩ |
| 10-03.4f | R_1 | 68 | kΩ |
| 10-03.4g | R_Th | 16.62 | kΩ |
| 10-03.4h | actual I_C | 0.892 | mA |
| 10-03.4i | error | -10.8 | % |
| 10-03.5a | I_C at β = 300 | 0.961 | mA |
| 10-03.5b | change | 7.74 | % |
| 10-03.5c | I_C at V_BE = 0.6 V | 0.952 | mA |
| 10-03.5d | change | 6.67 | % |
| 10-03.6a | I_E | 1.080 | mA |
| 10-03.6b | I_C | 1.070 | mA |
| 10-03.6c | V_C | 2.839 | V |
| 10-03.6d | I_C at β = 300 | 1.608 | mA |
| 10-03.6e | change | 50.4 | % |
| 10-03.7a | base current | 5.0 | mA |
| 10-03.7b | largest R_B | 810 | Ω |
| 10-03.7c | I_B with 750 Ω | 5.40 | mA |
| 10-03.7d | forced β | 9.26 | — |
| 10-03.7e | collector dissipation | 20 | mW |
| 10-03.8a | I_out | 0.4808 | mA |
| 10-03.8b | error | -3.85 | % |
| 10-03.8c | buffered I_out | 0.4996 | mA |
| 10-03.8d | buffered error | -0.078 | % |
| 10-03.9a | I_C at −40 °C | 1.167 | mA |
| 10-03.9b | I_C at 85 °C | 1.396 | mA |
| 10-03.9c | change across the range | 19.6 | % |
| 10-03.10a | current for unit loop gain | 12.93 | mA |
| 10-03.10b | largest loop gain with 10 Ω | 0.2 | — |
| 10-03.11a | base current | 2.0 | mA |
| 10-03.11b | R_B | 475 | Ω |
| 10-03.11c | I_B at −40 °C | 1.73 | mA |
| 10-03.11d | forced β at −40 °C | 11.6 | — |
| 10-03.11e | LED resistor | 140 | Ω |
| 10-03.12a | I_C at β = 100 | 1.926 | mA |
| 10-03.12b | I_C at β = 300 | 3.946 | mA |
| 10-03.12c | change | 105 | % |
