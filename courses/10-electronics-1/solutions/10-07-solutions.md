# Solutions 10-07 · BJT Single-Stage Amplifiers

Problems: [10-07 problems](../problems/10-07-problems.md) · Chapter: [10-07](../chapters/10-07-bjt-single-stage-amplifiers.md). Every number below is recomputed by [verify_10_07.py](../verify/verify_10_07.py), which solves each hybrid-π circuit by modified nodal analysis with test sources.

---

## Solutions

### Solution 10-07.1

(a) $g_m$ = 38.68 mS, so $r_\pi = 120/g_m$ = **3.102** kΩ, and $r_\pi + 121 \times 220\ \Omega$ = **29.72** kΩ.

(b) $r_e = (120/121)/g_m$ = **25.64** Ω, and $r_e + 12\text{ kΩ}/121$ = **124.8** Ω.

### Solution 10-07.2

(a) $|A_v| = V_{RC}/V_T = 2/0.025852$ = **77.36** at either current: the gain depends on the voltage across $R_C$, not on how it is split between current and resistance.

(b) $2 \times 2/0.2$ = **20**.

### Solution 10-07.3

$r_e = (150/151) \times 25.852/2$ = **12.84** Ω. Gain $500/(500 + 12.84)$ = **0.9750**. $R_{in} = 151 \times 512.84\ \Omega$ = **77.44** kΩ. $R_{out} = 500 \parallel 12.84$ = **12.52** Ω.

### Solution 10-07.4

(a) $r_e$ = **12.80** Ω and $\alpha R_C/10$ = **217.8** Ω, so $R_{E1}$ = **205.0** Ω.

(b) $(\beta + 1)(r_e + R_{E1}) = \beta R_C/10$ = **22.0** kΩ (neatly, because $\alpha(\beta + 1) = \beta$); with $R_B$: 10 ∥ 22 = **6.875** kΩ.

### Solution 10-07.5

(a) $g_m$ = **19.34** mS, $r_\pi$ = **10.34** kΩ, $r_o$ = **160** kΩ.

(b) $R_E \parallel r_\pi$ = 1.676 kΩ, so $R_{out} = 160\text{ kΩ} \times (1 + 19.34 \times 1.676) + 1.676\text{ kΩ}$ = **5348** kΩ.

(c) $(\beta + 1)r_o + r_\pi$ = **32170** kΩ, about 32 MΩ.

### Solution 10-07.6

$R_{in} = r_e$ = **102.4** Ω; gain from the emitter $g_mR_C$ = **193.4**; input factor $102.4/1102.4$ = **0.09288**; overall **17.96**. A CB stage driven from a 1 kΩ voltage source loses 91% of the signal at its input. CB stages belong after current sources (a transistor's collector, a photodiode) or on matched low-impedance lines, not after resistive voltage sources.

### Solution 10-07.7

$(r_\pi + R_{sig})/(\beta + 1) = (2.585 + 100)\text{ kΩ}/101$ = **1016** Ω, forty times $r_e$ (**25.60** Ω). From a high-resistance source, the follower's output resistance is set by the source divided by β + 1, not by its bias current.

### Solution 10-07.8

(a) At 1 mA: $r_\pi$ = **2.585** kΩ, input factor $2.585/1002.6$ = **0.002579**, and the base current of 10 µA through 1 MΩ gives a **10** V offset: the stage cannot even be biased this way.

(b) At 10 µA: $r_\pi$ = **258.5** kΩ, input factor **0.2054**, offset **0.1** V. Better, but most of the signal is still lost, and the offset drifts with β and temperature.

(c) A MOSFET gate draws no DC current and presents no $r_\pi$: input factor 1, no offset. High-impedance sensors use CMOS (or JFET) inputs (10-09).

### Solution 10-07.9

The derivation is §3.2's: with $v_e = i_xR_E'$, the base–emitter voltage is the fraction $r_\pi/(r_\pi + R_{sig})$ of $-v_e$, and the collector KCL gives the formula.

$R_{sig}$ = 0: $R_E'$ = 1 ∥ 2.585 = 721.1 Ω and $R_{out}$ = **1445** kΩ. $R_{sig}$ = 10 kΩ: $R_E'$ = 1 ∥ 12.585 = 926.4 Ω, the factor $r_\pi/(r_\pi + R_{sig})$ = 0.2054, and $R_{out}$ = **419.0** kΩ.

A resistance in the base lets the base voltage move with the emitter, so less of the emitter's movement appears across $r_\pi$ as feedback. Bipolar cascodes and current sources therefore ground their bases through low resistances.

### Solution 10-07.10

(a) The current in the transistor can fall from 1 mA to zero; the load then sees $I_E(R_E \parallel R_L) = 1\text{ mA} \times 833.3\ \Omega$ = **0.833** V of negative swing.

(b) $2\text{ V}/833.3\ \Omega$ = **2.4** mA.

(c) $V_{EE} = -(0.7 + 2.4\text{ mA} \times 5\text{ kΩ})$ = **−12.7** V. Most of that supply is wasted in $R_E$: the inefficiency of class A (10-05 §3.8), which push-pull stages remove (12-07).

### Solution 10-07.11

Degenerated: at β = 100, $R_{in}$ = 50 ∥ 47.03 = **24.23** kΩ and the overall gain is $\frac{24.23}{34.23} \times (-9.995)$ = **−7.075**; at β = 300, **36.86** kΩ and **−7.911**: an 11.8% change, against 0.63% for the stage alone.

Bypassed: at β = 100, $R_{in}$ = 50 ∥ 2.585 = **2.458** kΩ and the gain $\frac{2.458}{12.458} \times (-181.8)$ = **−35.87**; at β = 300, **6.714** kΩ and **−73.03**: a factor of two. Degeneration makes the overall gain far more predictable, but the source–input divider still carries β; feedback around the whole amplifier (Course 12) removes the rest.

### Solution 10-07.12

(a) $\frac{2.585}{52.585} \times (-193.4)$ = **−9.508**.

(b) The follower's load is the CE stage's $r_\pi$ = 2.585 kΩ. Its $r_\pi$ at 0.1 mA is 25.85 kΩ, so $R_{in} = 25.85 + 101 \times 2.585$ = **287.0** kΩ. Its gain from base to emitter is $101 \times 2.585/287.0$ = **0.9099**; the input factor is $287.0/337.0$ = **0.8516**; the overall gain is $0.8516 \times 0.9099 \times (-193.4)$ = **−149.9**, sixteen times better for 0.1 mA. Putting a follower in front is the standard way to raise a bipolar stage's input resistance.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-07.1a | r_pi | 3.102 | kΩ |
| 10-07.1b | into the base with 220 Ω | 29.72 | kΩ |
| 10-07.1c | r_e | 25.64 | Ω |
| 10-07.1d | into the emitter with 12 kΩ | 124.8 | Ω |
| 10-07.2a | BJT gain | 77.36 | — |
| 10-07.2b | MOSFET gain | 20 | — |
| 10-07.3a | r_e | 12.84 | Ω |
| 10-07.3b | gain | 0.9750 | — |
| 10-07.3c | R_in | 77.44 | kΩ |
| 10-07.3d | R_out | 12.52 | Ω |
| 10-07.4a | r_e | 12.80 | Ω |
| 10-07.4b | α R_C / 10 | 217.8 | Ω |
| 10-07.4c | R_E1 | 205.0 | Ω |
| 10-07.4d | R_in at the base | 22.0 | kΩ |
| 10-07.4e | R_in of the stage | 6.875 | kΩ |
| 10-07.5a | g_m | 19.34 | mS |
| 10-07.5b | r_pi | 10.34 | kΩ |
| 10-07.5c | r_o | 160 | kΩ |
| 10-07.5d | R_out with 2 kΩ | 5348 | kΩ |
| 10-07.5e | ceiling | 32170 | kΩ |
| 10-07.6a | R_in | 102.4 | Ω |
| 10-07.6b | gain from the emitter | 193.4 | — |
| 10-07.6c | input factor | 0.09288 | — |
| 10-07.6d | overall gain | 17.96 | — |
| 10-07.7a | R_out | 1016 | Ω |
| 10-07.7b | r_e | 25.60 | Ω |
| 10-07.8a | r_pi at 1 mA | 2.585 | kΩ |
| 10-07.8b | input factor at 1 mA | 0.002579 | — |
| 10-07.8c | offset at 1 mA | 10 | V |
| 10-07.8d | r_pi at 10 µA | 258.5 | kΩ |
| 10-07.8e | input factor at 10 µA | 0.2054 | — |
| 10-07.8f | offset at 10 µA | 0.1 | V |
| 10-07.9a | R_out, R_sig = 0 | 1445 | kΩ |
| 10-07.9b | R_out, R_sig = 10 kΩ | 419.0 | kΩ |
| 10-07.10a | negative swing | 0.833 | V |
| 10-07.10b | bias for 2 V | 2.4 | mA |
| 10-07.10c | negative supply | -12.7 | V |
| 10-07.11a | R_in, degenerated, β = 100 | 24.23 | kΩ |
| 10-07.11b | gain, degenerated, β = 100 | -7.075 | — |
| 10-07.11c | R_in, degenerated, β = 300 | 36.86 | kΩ |
| 10-07.11d | gain, degenerated, β = 300 | -7.911 | — |
| 10-07.11e | R_in, bypassed, β = 100 | 2.458 | kΩ |
| 10-07.11f | gain, bypassed, β = 100 | -35.87 | — |
| 10-07.11g | R_in, bypassed, β = 300 | 6.714 | kΩ |
| 10-07.11h | gain, bypassed, β = 300 | -73.03 | — |
| 10-07.12a | gain without follower | -9.508 | — |
| 10-07.12b | follower R_in | 287.0 | kΩ |
| 10-07.12c | follower gain | 0.9099 | — |
| 10-07.12d | input factor | 0.8516 | — |
| 10-07.12e | overall gain with follower | -149.9 | — |
