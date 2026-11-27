# Solutions 10-05 · Amplifier Fundamentals

Problems: [10-05 problems](../problems/10-05-problems.md) · Chapter: [10-05](../chapters/10-05-amplifier-fundamentals.md). Every number below is recomputed by [verify_10_05.py](../verify/verify_10_05.py), which solves each circuit's nodal equations with the stages as controlled sources.

---

## Solutions

### Solution 10-05.1

(a) $10\log 2$ = **3.01** dB. (b) $20\log 2$ = **6.02** dB. (c) **30** dB. (d) $20\log(1/\sqrt2)$ = **−3.01** dB. (e) $10^{26/20}$ = **19.95** V/V. (f) $10^{10/10}$ mW = **10** mW. (g) $\sqrt{1\text{ mW} \times 50\ \Omega}$ = **0.2236** V rms.

### Solution 10-05.2

- **Voltage amplifier:** $R_i \to \infty$, so the divider $R_i/(R_i + R_{sig})$ passes all of the source voltage; $R_o \to 0$, so $R_L/(R_L + R_o)$ passes all of the output voltage to any load.
- **Current amplifier:** $R_i \to 0$, so the current divider between $R_{sig}$ (in a Norton source) and $R_i$ sends all the source current into the input; $R_o \to \infty$, so the Norton output sends all its current into the load rather than into $R_o$.
- **Transconductance amplifier:** $R_i \to \infty$ (voltage sensing) and $R_o \to \infty$ (current output).
- **Transresistance amplifier:** $R_i \to 0$ (current sensing) and $R_o \to 0$ (voltage output).

### Solution 10-05.3

$\frac{20}{22} \times 50 \times \frac{1}{1.5}$ = **30.30**, or **29.63** dB.

### Solution 10-05.4

(a) $A_{vo} = G_mR_o$ = **500**; $R_m = A_{vo}R_i$ = **2.5** MΩ; $A_{is} = G_mR_i$ = **100**.

(b) $\frac{5}{6} \times 500 \times \frac{25}{50}$ = **208.3**. As a check, in the Norton form the output current $G_mv_i$ divides between $R_o$ and $R_L$, which are equal, so the load voltage is $G_mv_i(R_o \parallel R_L) = 0.02 \times 12.5\text{ kΩ} \times v_i$ = 250 $v_i$, times the input factor 5/6: the same 208.3.

### Solution 10-05.5

(a) $R_o = 600 \times (1.20/0.90 - 1)$ = **200** Ω.

(b) $R_i = 47\text{ kΩ} \times 30/(50 - 30)$ = **70.5** kΩ.

### Solution 10-05.6

X → Y: $\frac{1000}{1050} \times 10 \times \frac{2}{12} \times 100 \times \frac{1}{1.1}$ = **144.3**.

Y → X: $\frac{2}{52} \times 100 \times \frac{1000}{1000.1} \times 10 \times \frac{1}{11}$ = **3.496**.

X has the high input resistance the 50 kΩ source needs; Y has the low output resistance the 1 kΩ load needs. In the wrong order, both end interfaces lose more than 90% of the signal: the factor of 41 between the two orders is entirely interface loss.

### Solution 10-05.7

(a) At 3 mA, $V_D = 12 - 6$ = 6 V. Downward room $6 - 1$ = 5 V; upward room $I_DR_D$ = 6 V. Swing **5.0** V peak; $P = 5^2/(2 \times 2\text{ kΩ})$ = **6.25** mW; $P_{DC}$ = 36 mW; η = **17.36**%.

(b) Equal room requires $V_D$ halfway between 1 V and 12 V, 6.5 V: $I_D = 5.5/2\text{ kΩ}$ = **2.75** mA, swing **5.5** V, $P = 5.5^2/4\text{ kΩ}$ = **7.5625** mW, $P_{DC}$ = 33 mW and η = **22.92**%: a lower current gives a higher efficiency, because the bias now uses all the room.

### Solution 10-05.8

(a) $1/(2\pi \times 30\text{ kΩ} \times 3.3\ \mu\text{F})$ = **1.61** Hz, the data sheet's 1.6 Hz.

(b) At 24 kΩ: **2.01** Hz.

(c) $C = 1/(2\pi \times 2 \times 24\text{ kΩ})$ = **3.32** µF: the recommended 3.3 µF is sized for the nominal impedance, and with the tolerance the corner reaches 2 Hz, still a decade below 20 Hz.

### Solution 10-05.9

(a) $10^{26/20}$ = **19.95** V/V.

(b) $\hat v = \sqrt{2PR} = \sqrt{2 \times 50 \times 4}$ = **20.0** V peak, or **14.14** V rms.

(c) $14.14/19.95$ = **0.709** V rms.

(d) $50/0.9 - 50$ = **5.56** W.

(e) At 25%, the supply delivers 200 W and the stage dissipates **150** W.

### Solution 10-05.10

(a) $v_2/v_1 = -y_{21}/(y_{22} + Y_L) = -40/(0.05 + 0.1)$ = **−266.7**. (This is exact: the input is driven directly, so $y_{12}$ does not affect it.)

(b) Unilateral: $1/y_{11}$ = **10** kΩ. Actual: $Y_{in} = 0.1 - (-0.01)(40)/0.15$ = 2.767 mS, so $R_{in}$ = **361.4** Ω. With the output open, $Y_{in} = 0.1 + 0.4/0.05$ = 8.1 mS and $R_{in}$ = **123.5** Ω.

(c) Unilateral prediction: $\frac{10}{11} \times (-266.7)$ = **−242.4**. Actual: $\frac{361.4}{1361.4} \times (-266.7)$ = **−70.8**. A feedback resistor of 100 kΩ, ten times the apparent input resistance, cuts the real input resistance by a factor of **28**, because the output swings 267 times as far as the input in the opposite direction: the current through the feedback resistor is \$(v_1 - v_2)/100\text{ kΩ} = \$ **267.7**$\,v_1/100\text{ kΩ}$, as if a **374** Ω resistor were across the input. This is the Miller effect (12-03).

### Solution 10-05.11

(a) G-G-G: $\frac{5}{55} \times 30 \times \frac{5}{8} \times 30 \times \frac{5}{8} \times 30 \times \frac{2}{5}$ = **383.5** (**51.68** dB). B-G-G-B: **421.4** (**52.49** dB). G-G-G-B: **825.6** (**58.34** dB).

(b) B-G-G-G: **3670** (**71.29** dB).

(c) Two gain stages give 900 before any interface loss, and every interface loses something: even with a buffer at every interface, B-G-B-G-B reaches only **614.0**. So three gain stages are needed. With three, the largest single loss is the first interface, 5 kΩ against a 50 kΩ source (factor 0.091). An output buffer fixes the smaller loss (3 kΩ into 2 kΩ, factor 0.4) and still falls short; the input buffer fixes the larger one and clears the specification by 11 dB.

### Solution 10-05.12

(a) Output power scales with amplitude squared and supply power is constant: η = **2.5**%.

(b) At 1 W: $1/(1 + 0.24 + 0.111)$ = **74.0**%. At 10 W: $10/(10 + 0.24 + 1.111)$ = **88.1**%.

(c) $1/(1 + 0.24)$ = **80.6**%. This simple model is ours, not the data sheet's; the data sheet's efficiency curves show the same shape, falling at low output, for the same reason.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-05.1a | power ratio 2 | 3.01 | dB |
| 10-05.1b | voltage ratio 2 | 6.02 | dB |
| 10-05.1c | power ratio 1000 | 30 | dB |
| 10-05.1d | voltage ratio 1/√2 | -3.01 | dB |
| 10-05.1e | 26 dB as a ratio | 19.95 | — |
| 10-05.1f | 10 dBm | 10 | mW |
| 10-05.1g | 0 dBm in 50 Ω | 0.2236 | V rms |
| 10-05.3a | overall gain | 30.30 | — |
| 10-05.3b | overall gain | 29.63 | dB |
| 10-05.4a | A_vo | 500 | — |
| 10-05.4b | R_m | 2.5 | MΩ |
| 10-05.4c | A_is | 100 | — |
| 10-05.4d | overall gain | 208.3 | — |
| 10-05.5a | R_o | 200 | Ω |
| 10-05.5b | R_i | 70.5 | kΩ |
| 10-05.6a | gain X then Y | 144.3 | — |
| 10-05.6b | gain Y then X | 3.496 | — |
| 10-05.7a | swing at 3 mA | 5.0 | V |
| 10-05.7b | signal power | 6.25 | mW |
| 10-05.7c | efficiency | 17.36 | % |
| 10-05.7d | best bias current | 2.75 | mA |
| 10-05.7e | best swing | 5.5 | V |
| 10-05.7f | signal power | 7.5625 | mW |
| 10-05.7g | efficiency | 22.92 | % |
| 10-05.8a | corner, nominal | 1.61 | Hz |
| 10-05.8b | corner, minimum impedance | 2.01 | Hz |
| 10-05.8c | capacitor for 2 Hz | 3.32 | µF |
| 10-05.9a | voltage gain | 19.95 | — |
| 10-05.9b | peak output | 20.0 | V |
| 10-05.9c | rms output | 14.14 | V |
| 10-05.9d | rms input | 0.709 | V |
| 10-05.9e | class-D dissipation | 5.56 | W |
| 10-05.9f | class-A dissipation | 150 | W |
| 10-05.10a | voltage gain | -266.7 | — |
| 10-05.10b | unilateral R_in | 10 | kΩ |
| 10-05.10c | actual R_in | 361.4 | Ω |
| 10-05.10d | R_in with output open | 123.5 | Ω |
| 10-05.10e | unilateral overall gain | -242.4 | — |
| 10-05.10f | actual overall gain | -70.8 | — |
| 10-05.10g | reduction in R_in | 28 | — |
| 10-05.10h | (v_1 − v_2)/v_1 | 267.7 | — |
| 10-05.10i | equivalent shunt resistor | 374 | Ω |
| 10-05.11a | G-G-G | 383.5 | — |
| 10-05.11b | G-G-G | 51.68 | dB |
| 10-05.11c | B-G-G-B | 421.4 | — |
| 10-05.11d | B-G-G-B | 52.49 | dB |
| 10-05.11e | G-G-G-B | 825.6 | — |
| 10-05.11f | G-G-G-B | 58.34 | dB |
| 10-05.11g | B-G-G-G | 3670 | — |
| 10-05.11h | B-G-G-G | 71.29 | dB |
| 10-05.11i | B-G-B-G-B | 614.0 | — |
| 10-05.12a | class A at a tenth of full power | 2.5 | % |
| 10-05.12b | class-D model at 1 W | 74.0 | % |
| 10-05.12c | class-D model at 10 W | 88.1 | % |
| 10-05.12d | idle-loss limit at 1 W | 80.6 | % |
