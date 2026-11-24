# Solutions 22-06 · Converter Losses and Wide-Bandgap Switches

Problems: [22-06 problem set](../problems/22-06-problems.md) · Chapter: [22-06](../chapters/22-06-converter-losses-and-wide-bandgap.md). Every number below is recomputed by [verify_22_06.py](../verify/verify_22_06.py).

---

## Solutions

### Solution 22-06.1

$P_g = Q_gV_{drv}f_s$: (a) $22\ \text{nC} \times 18 \times 100\ \text{kHz}$ = **39.6** mW; (b) **0.198** W.

### Solution 22-06.2

$\tfrac12 \times 48 \times 15 \times 10\ \text{ns} \times 1\ \text{MHz}$ = **3.6** W.

### Solution 22-06.3

(a) $Q = CV$ = **40** nC; (b) $E = \tfrac12CV^2$ = **8.0** µJ; (c) $Q_{oss}V$ = **16** µJ, exactly $2E_{oss}$ for a linear capacitor.

### Solution 22-06.4

(a) $L\,di/dt = 1.5\ \text{nH} \times 30/3\ \text{ns}$ = **15** V; (b) $48 + 15$ = **63** V; (c) **37** V.

(d) $L \le 20 \times 1.5\ \text{ns}/30$ = **1.0** nH. Halving the fall time halves the allowed loop inductance: faster devices need tighter layouts.

### Solution 22-06.5

$2V_{SD}It_df_s$: (a) $2 \times 4.3 \times 20 \times 100\ \text{ns} \times 100\ \text{kHz}$ = **1.72** W; (b) **0.516** W. SiC's 4.3 V diode drop makes long dead times expensive, and shorter ones also cut its recovery charge (§3.4).

### Solution 22-06.6

(a) $2.4 \times 43$ = **103.2** mΩ·nC.

(b) $R^* = \sqrt{(RQ_{oss})Vf_s}/I = \sqrt{103.2 \times 10^{-12} \times 48 \times 10^6}/10$ = **7.04** mΩ.

(c) $P_{min} = 2 \times 10 \times 0.07038$ = **1.41** W.

### Solution 22-06.7

(a) $(82 - 50)/150$ = **0.213** mΩ/K.

(b) With $R_{th}I^2$ = 1500 K/Ω: $T_j = (50 + 1500 \times (0.050 - 25 \times 0.0002133))/(1 - 1500 \times 0.0002133)$ = **172.1** °C, close to the 175 °C at which the data sheet specifies $R_{DS(on)}$.

(c) $50 + 0.2133 \times 147.1$ = **81.4** mΩ; (d) $100 \times 0.0814$ = **8.14** W.

(e) $I = 1/\sqrt{15 \times 0.0002133}$ = **17.7** A.

### Solution 22-06.8

(a) $3.6\ \mu\text{C} \times 400 \times 65\ \text{kHz}$ = **93.6** W: impossible in a kilowatt-class PFC.

(b) $30\ \text{nC} \times 400 \times 65\ \text{kHz}$ = **0.78** W. This is why CCM PFC boosts use SiC Schottky diodes or, in the totem-pole form, SiC or GaN switches.

### Solution 22-06.9

$\varepsilon\mu\mathcal{E}_c^3$ with $\varepsilon_r$ in place of $\varepsilon$ (the $\varepsilon_0$ cancels in ratios):

- Si: $11.9 \times 1240 \times 0.3^3 = 398.4$;
- SiC: $9.7 \times 980 \times 3.1^3 = 2.832 \times 10^5$;
- GaN: $10.4 \times 1000 \times 4.9^3 = 1.224 \times 10^6$.

(a) **711**; (b) **3071**. (c) $R_{on,sp} \propto V_B^2/(\varepsilon\mu\mathcal{E}_c^3)$, so SiC's is lower by the same **711** times. (Tsao's tabulated figures of merit give **712.5** and **3170**, because the table's inputs are rounded and GaN's mobility and field are given to two figures.)

### Solution 22-06.10

The switch node must swing $2Q_{oss}$ in the dead time: $I = 2 \times 43\ \text{nC}/t_d$.

(a) **17.2** A; (b) **8.6** A; (c) **4.3** A.

For a 20 A converter, even 4 A of negative current per cycle raises the inductor's ripple and RMS current substantially. At 48 V the hard-switching loss is modest (Example 22-06.6), so point-of-load bucks usually hard-switch and rely on low $Q_{oss}$ instead.

### Solution 22-06.11

(a) $I \ge 2 \times 88\ \text{pF} \times 400/30\ \text{ns}$ = **2.35** A.

(b) $L_m \le V/(4f_sI) = 400/(4 \times 500\ \text{kHz} \times 2.347)$ = **85.2** µH.

(c) $2.347/\sqrt{3}$ = **1.35** A.

### Solution 22-06.12

The switching-related loss at 500 kHz is the total minus conduction.

(a) $(10.53 - 0.72)/0.5$ = **19.62** W/MHz; (b) $(4.487 - 0.96)/0.5$ = **7.05** W/MHz.

2% of 240 W is 4.8 W: (c) $(4.8 - 0.72)/19.62$ = **0.208** MHz; (d) $(4.8 - 0.96)/7.054$ = **0.544** MHz.

At the same loss, GaN runs **2.6** times faster, which is the density argument of 22-01 in one number.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-06.1a | gate power at 100 kHz | 39.6 | mW |
| 22-06.1b | gate power at 500 kHz | 0.198 | W |
| 22-06.2 | overlap loss | 3.6 | W |
| 22-06.3a | output charge | 40 | nC |
| 22-06.3b | stored energy | 8.0 | µJ |
| 22-06.3c | hard turn-on loss | 16 | µJ |
| 22-06.4a | overshoot | 15 | V |
| 22-06.4b | peak drain voltage | 63 | V |
| 22-06.4c | margin | 37 | V |
| 22-06.4d | allowed loop inductance | 1.0 | nH |
| 22-06.5a | dead-time loss, 100 ns | 1.72 | W |
| 22-06.5b | dead-time loss, 30 ns | 0.516 | W |
| 22-06.6a | R·Q_oss | 103.2 | mΩ·nC |
| 22-06.6b | optimal on-resistance | 7.04 | mΩ |
| 22-06.6c | minimum loss | 1.41 | W |
| 22-06.7a | resistance slope | 0.213 | mΩ/K |
| 22-06.7b | junction temperature | 172.1 | °C |
| 22-06.7c | hot resistance | 81.4 | mΩ |
| 22-06.7d | loss | 8.14 | W |
| 22-06.7e | runaway current | 17.7 | A |
| 22-06.8a | superjunction recovery loss | 93.6 | W |
| 22-06.8b | Schottky capacitive loss | 0.78 | W |
| 22-06.9a | SiC figure of merit relative to Si | 711 | |
| 22-06.9b | GaN figure of merit relative to Si | 3071 | |
| 22-06.9c | specific on-resistance ratio | 711 | |
| 22-06.9d | Tsao table ratio, SiC | 712.5 | |
| 22-06.9e | Tsao table ratio, GaN | 3170 | |
| 22-06.10a | negative current, 5 ns | 17.2 | A |
| 22-06.10b | negative current, 10 ns | 8.6 | A |
| 22-06.10c | negative current, 20 ns | 4.3 | A |
| 22-06.11a | minimum switching current | 2.35 | A |
| 22-06.11b | largest magnetizing inductance | 85.2 | µH |
| 22-06.11c | RMS magnetizing current | 1.35 | A |
| 22-06.12a | Si switching-loss slope | 19.62 | W/MHz |
| 22-06.12b | GaN switching-loss slope | 7.05 | W/MHz |
| 22-06.12c | Si frequency at 2% loss | 0.208 | MHz |
| 22-06.12d | GaN frequency at 2% loss | 0.544 | MHz |
| 22-06.12e | frequency ratio | 2.6 | |
