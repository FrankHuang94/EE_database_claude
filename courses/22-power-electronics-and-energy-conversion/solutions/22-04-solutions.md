# Solutions 22-04 · Isolated Converters: Flyback and Forward

Problems: [22-04 problem set](../problems/22-04-problems.md) · Chapter: [22-04](../chapters/22-04-isolated-converters.md). Every number below is recomputed by [verify_22_04.py](../verify/verify_22_04.py).

---

## Solutions

### Solution 22-04.1

(a) $D/D' = nV/V_{in} = 24/48 = 0.5$, so $D$ = **0.333**.

(b) $48 + 2 \times 12$ = **72** V.

### Solution 22-04.2

(a) $I_{pk} = V_{in}DT_s/L_m = 300 \times 0.3 \times 15.38\ \mu\text{s}/1\ \text{mH}$ = **1.38** A.

(b) $P = \tfrac12L_mI_{pk}^2f_s = 0.5 \times 1\ \text{mH} \times 1.917 \times 65\ \text{kHz}$ = **62.3** W.

### Solution 22-04.3

(a) $D = nV/V_{in} = 16 \times 12/400$ = **0.48**, just under the 0.5 limit.

(b) $2 \times 400$ = **800** V: a forward converter from a 400 V bus needs 800 V-class switches, or a two-switch forward, which clamps each switch to $V_{in}$.

### Solution 22-04.4

(a) $373.4 + 180$ = **553.4** V.

(b) $650 - 553.4$ = **96.6** V; (c) **14.9** % of the rating. Whether that is enough depends on the spike above the clamp level, on production spread and on the design's derating policy.

### Solution 22-04.5

(a) $D = 128/278 = 0.4604$, so $\Delta i_m = 150 \times 0.4604 \times 10\ \mu\text{s}/500\ \mu\text{H}$ = **1.38** A.

(b) The average magnetizing current is $I/(nD')$, and the boundary is where it equals half the ripple: $I_{crit} = nD'\Delta i_m/2 = 6.4 \times 0.5396 \times 1.381/2$ = **2.38** A. Below about 2.4 A of output current (48 W at 20 V), the converter is in DCM.

### Solution 22-04.6

(a) $\tfrac12 \times 3\ \mu\text{H} \times 4$ = **6.0** µJ.

(b) $6\ \mu\text{J} \times 100\ \text{kHz}$ = **0.60** W.

(c) $0.6 \times 150/50$ = **1.8** W; (d) $0.6 \times 200/100$ = **1.2** W; (e) $0.6 \times 300/200$ = **0.9** W.

A loose clamp halves the loss compared with a tight one, but raises the drain voltage by 150 V. The trade is switch voltage rating against efficiency.

### Solution 22-04.7

(a) $D_{max} = 1/(1 + 0.5)$ = **0.667**.

(b) $V_{in}(1 + N_1/N_3) = V_{in}(1 + 2)$ = **3** $V_{in}$. Fewer tertiary turns allow a longer duty cycle but reset with a higher voltage.

### Solution 22-04.8

(a) $\Delta B = V_{in}DT_s/(N_1A_e) = 48 \times 0.4 \times 4\ \mu\text{s}/(6 \times 40\ \text{mm}^2)$ = **0.32** T, too much for a ferrite at this frequency (22-05).

(b) $N_1 = 48 \times 0.4 \times 4\ \mu\text{s}/(0.2 \times 40\ \text{mm}^2)$ = **9.6**, so 10 turns.

### Solution 22-04.9

(a) $n \le D_{eff}V_{in,min}/V = 0.8 \times 340/12$ = **22.7**.

(b) $12 \times 22/380$ = **0.695**.

(c) $100\ \text{A}/22$ = **4.55** A.

### Solution 22-04.10

(a) $2\pi \times 50 \times 4.7\ \text{nF} \times 264$ = **0.390** mA; (b) at 60 Hz, **0.468** mA. Both are within 0.5 mA, the 60 Hz case by little: this is about the largest single Y-capacitor such a product can use.

### Solution 22-04.11

IEC 60664-1: $3.0 \times 1.48$ = **4.44** mm. IEC 62368-1: $3.8 \times 1.48$ = **5.62** mm (the source rounds up to 5.7 mm [4]).

### Solution 22-04.12

(a) $n = V_R/V = 100/12$ = **8.33**.

(b) $D = V_R/(V_{in} + V_R) = 100/200$ = **0.5** at 100 V. (c) At 373 V the frequency is still 65 kHz, so the converter runs in discontinuous conduction and the CCM relation no longer applies. In DCM it delivers $P_{in} = (V_{in}D)^2T_s/(2L_m)$, so the volt-seconds per cycle $V_{in}DT_s = \sqrt{2L_mP_{in}T_s}$ are fixed by the power; with $L_m$ and $P_{in}$ from (g) and (e), $V_{in}D = \sqrt{2L_mP_{in}f_s}$ = 50.0 V, the same as at 100 V, and $D = 50.0/373$ = **0.134**. Check: the reset takes $D_2 = V_{in}D/V_R$ = 0.50, and $D + D_2$ = 0.634 < 1, so it is discontinuous. (A quasi-resonant flyback that stays at the boundary would instead raise its frequency here.)

(d) $373 + 100$ = **473** V, plus the clamp's excursion.

(e) $24/0.88$ = **27.3** W.

(f) $I_{pk} = 2P_{in}/(V_{in}D) = 2 \times 27.27/(100 \times 0.5)$ = **1.09** A.

(g) $L_m = V_{in}DT_s/I_{pk} = 100 \times 0.5 \times 15.38\ \mu\text{s}/1.091$ = **705** µH.

### Solution 22-04.13

(a) $2 \times 4.0$ = **8.0** mm. (b) Group I needs $2 \times 2.0$ = 4.0 mm, **4.0** mm shorter. (c) Reinforced creepage is 4.0 mm for group I, 5.6 mm for group II and 8.0 mm for group III, so a 6.0 mm path serves groups I and II but not III: either a better-tracking bobbin material, or slots and barriers that lengthen the path.

### Solution 22-04.14

(a) In DCM the energy stored each cycle, $\tfrac12L_mI_{pk}^2$ with $I_{pk} = V_{in}DT_s/L_m$, is all delivered to the output, so $(V_{in}D)^2T_s/(2L_m) = V^2/R$ and $M = V/V_{in} = D\sqrt{RT_s/(2L_m)}$. With $R$ = 2.5 Ω and $T_s$ = 6.667 µs, $\sqrt{RT_s/(2L_m)}$ = 0.527, so $D = (5/48)/0.527$ = **0.198**. (b) In CCM, $D/D' = nV/V_{in} = 20/48$ gives $D$ = 0.294 and $D'^2$ = 0.498, while $2L_m/(n^2RT_s)$ = **0.225**: below $D'^2$, so discontinuous. (c) $I_{pk} = V_{in}DT_s/L_m = 48 \times 0.198 \times 6.667\ \mu\text{s}/30\ \mu\text{H}$ = **2.11** A; check: $\tfrac12L_mI_{pk}^2f_s$ = 10.0 W. ✓ (d) The boundary is at $2L_m/(n^2RT_s) = D'^2$: $L_m = 0.498 \times 16 \times 2.5 \times 6.667\ \mu\text{s}/2$ = **66.4** µH.

### Solution 22-04.15

(a) $D = nV/V_{in}$: **0.4125** at 36 V and **0.206** at 72 V, both below $D_{max}$ = 0.5. (b) The ripple is $\Delta i = (V_{in}/n - V)DT_s/L = V(1 - D)/(f_sL)$, largest at the lowest $D$, so at 72 V: $L = 3.3 \times (1 - 0.206)/(300\ \text{kHz} \times 4.5\ \text{A})$ = **1.940** µH. (c) $C = \Delta i/(8f_s\Delta v) = 4.5/(8 \times 300\ \text{kHz} \times 20\ \text{mV})$ = **93.75** µF. (d) $\Delta B = V_{in}DT_s/(N_1A_e) = nVT_s/(N_1A_e) = 14.85 \times 3.333\ \mu\text{s}/(9 \times 60\ \text{mm}^2)$ = **0.0917** T, independent of the input voltage because $V_{in}D = nV$ in steady state.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-04.1a | duty cycle | 0.333 | |
| 22-04.1b | switch voltage | 72 | V |
| 22-04.2a | peak magnetizing current | 1.38 | A |
| 22-04.2b | DCM power | 62.3 | W |
| 22-04.3a | forward duty cycle | 0.48 | |
| 22-04.3b | forward switch voltage | 800 | V |
| 22-04.4a | worst-case drain voltage | 553.4 | V |
| 22-04.4b | margin | 96.6 | V |
| 22-04.4c | margin as a share of rating | 14.9 | % |
| 22-04.5a | magnetizing ripple | 1.38 | A |
| 22-04.5b | DCM boundary output current | 2.38 | A |
| 22-04.6a | leakage energy | 6.0 | µJ |
| 22-04.6b | leakage power | 0.60 | W |
| 22-04.6c | clamp loss at 150 V | 1.8 | W |
| 22-04.6d | clamp loss at 200 V | 1.2 | W |
| 22-04.6e | clamp loss at 300 V | 0.9 | W |
| 22-04.7a | maximum duty cycle | 0.667 | |
| 22-04.7b | switch voltage multiple | 3 | |
| 22-04.8a | flux swing with 6 turns | 0.32 | T |
| 22-04.8b | turns for 0.2 T | 9.6 | |
| 22-04.9a | largest turns ratio | 22.7 | |
| 22-04.9b | effective duty at 380 V | 0.695 | |
| 22-04.9c | switch current | 4.55 | A |
| 22-04.10a | Y-capacitor current at 50 Hz | 0.390 | mA |
| 22-04.10b | Y-capacitor current at 60 Hz | 0.468 | mA |
| 22-04.11a | clearance at 5000 m, IEC 60664-1 | 4.44 | mm |
| 22-04.11b | clearance at 5000 m, IEC 62368-1 | 5.62 | mm |
| 22-04.12a | turns ratio | 8.33 | |
| 22-04.12b | duty at 100 V | 0.5 | |
| 22-04.12c | duty at 373 V | 0.134 | |
| 22-04.12d | drain voltage at 373 V | 473 | V |
| 22-04.12e | input power | 27.3 | W |
| 22-04.12f | peak primary current | 1.09 | A |
| 22-04.12g | magnetizing inductance | 705 | µH |
| 22-04.13a | reinforced creepage, group III | 8.0 | mm |
| 22-04.13b | saving with group I | 4.0 | mm |
| 22-04.14a | DCM duty cycle | 0.198 | |
| 22-04.14b | conduction parameter | 0.225 | |
| 22-04.14c | peak primary current | 2.11 | A |
| 22-04.14d | boundary magnetizing inductance | 66.4 | µH |
| 22-04.15a | duty cycle at 36 V | 0.4125 | |
| 22-04.15b | duty cycle at 72 V | 0.206 | |
| 22-04.15c | output inductance | 1.940 | µH |
| 22-04.15d | output capacitance | 93.75 | µF |
| 22-04.15e | flux swing | 0.0917 | T |
