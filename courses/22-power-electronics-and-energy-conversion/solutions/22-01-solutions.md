# Solutions 22-01 · Power Conversion Principles

Problems: [22-01 problem set](../problems/22-01-problems.md) · Chapter: [22-01](../chapters/22-01-power-conversion-principles.md). Every number below is recomputed by [verify_22_01.py](../verify/verify_22_01.py).

---

## Solutions

### Solution 22-01.1

(a) $P_{loss} = P_{out}(1/\eta - 1)$ with $P_{out}$ = 2000 W:

- 80%: $2000 \times 0.25$ = **500** W;
- 85%: $2000 \times 0.17647$ = **352.9** W;
- 97%: $2000 \times 0.030928$ = **61.86** W;
- 98%: $2000 \times 0.020408$ = **40.82** W.

(b) 80 → 85% saves 500 − 352.9 = **147.1** W; 97 → 98% saves 61.86 − 40.82 = **21.04** W. The low-efficiency upgrade saves seven times the watts.

(c) 147.1/500 = **29.4** % of the loss, against 21.04/61.86 = **34.0** %. The single point at the top removes a larger *share* of the heat than five points at the bottom, which is what matters when the cooling, not the electricity bill, is the constraint.

### Solution 22-01.2

(a) $\eta = 0.98 \times 0.95 \times 0.92$ = **85.65** %.

(b) $P_{in} = 50/0.85652$ = **58.38** W.

(c) Work back from the load:

- the 92% stage draws 50/0.92 = 54.35 W and loses **4.35** W;
- the 95% stage draws 54.35/0.95 = 57.21 W and loses **2.86** W;
- the 98% stage draws 58.38 W and loses **1.17** W.

The total is 8.38 W = 58.38 − 50, as it must be.

(d) The last stage, the 92% one, holds **52** % of the loss, although it handles the least power.

### Solution 22-01.3

(a) $I_{in} = 200 + 0.05$ mA = 200.05 mA, so $\eta = 3.3 \times 0.2/(5.0 \times 0.20005)$ = **65.98** %, just below the 66.0% ceiling.

(b) $P_{loss} = 5.0 \times 0.20005 - 0.66$ = **0.340** W.

(c) $T_J = 25 + 50 \times 0.340$ = **42.0** °C.

(d) $V_{in,min} = 3.3 + 0.27$ = **3.57** V.

### Solution 22-01.4

(a) A linear regulator passes its load current: **2.000** mA.

(b) $I_{in} = 1.2 \times 2/(0.85 \times 3.8)$ = **0.743** mA.

(c) Battery life scales inversely with battery current: 2.000/0.743 = **2.69** times longer with the buck.

(d) $1.2/3.8$ = **31.6** %.

### Solution 22-01.5

(a) $\eta = V_{out}I_{out}/[V_{in}(I_{out} + I_Q)] = (V_{out}/V_{in}) \times I_{out}/(I_{out} + I_Q)$. The second factor is the fraction of the ceiling.

(b) Within 1% means $I_{out}/(I_{out} + I_Q) \ge 0.99$, so $I_{out} \ge 99I_Q$ = **2.475** µA for 25 nA.

(c) $99 \times 5\ \mu\text{A}$ = **495** µA.

(d) At 3 µA: $3/3.025$ = **99.2** % of the ceiling for 25 nA, and $3/8$ = **37.5** % for 5 µA. The 5 µA regulator would spend more than the load on itself.

### Solution 22-01.6

(a) Step $k$ raises the source from $(k - 1)V/N$ to $kV/N$, so the capacitor charges across a difference of $V/N$. By §3.4, charging across a difference $\Delta V$ through any resistance loses $\tfrac12C\,\Delta V^2$ (the derivation depends only on the difference). The total over $N$ steps is $N \times \tfrac12C(V/N)^2 = \tfrac12CV^2/N$.

(b) $\tfrac12 \times 100\ \text{nF} \times 3.3^2$ = **544.5** nJ; (c) **181.5** nJ; (d) **54.45** nJ.

(e) Charging from 0 to $V$ takes charge $CV$ from the supply at voltage $V$, energy $CV^2$. Half of it is lost in the driver's pull-up resistance; the other half is stored on the gate. Discharging dissipates the stored half in the pull-down resistance. Every cycle therefore costs $CV^2$, and the power is $CV^2f$ = $2\ \text{nF} \times 25 \times 10^6$ = **50.0** mW, whatever the driver's resistances. In data-sheet terms this is the gate charge times the drive voltage times the frequency, $Q_gV_{dr}f_s$, and it belongs to $P_0$.

### Solution 22-01.7

(a) When connected to $V_1$ the capacitor charges to $V_1$; when connected to $V_2$ it discharges to $V_2$. The charge moved per cycle is $q = C(V_1 - V_2)$, so $I = fC(V_1 - V_2)$.

(b) Each connection changes the capacitor's voltage by $V_1 - V_2$ through a resistance and loses $\tfrac12C(V_1 - V_2)^2$ (§3.4). There are two connections per cycle, so
$$P = 2f\cdot\tfrac12C(V_1 - V_2)^2 = fC(V_1 - V_2)^2 .$$
Substituting $V_1 - V_2 = I/(fC)$ gives $P = I^2/(fC)$, the loss of a resistance $R_{eq} = 1/(fC)$ carrying $I$.

(c) $1/(10^6 \times 10^{-6})$ = **1.00** Ω. (d) $I/(fC)$ = **0.100** V. (e) $I^2R_{eq}$ = **10.0** mW.

(f) $C = I/(f\Delta V) = 0.1/(10^6 \times 0.018)$ = **5.56** µF. This is the switched-capacitor converter's "slow-switching" output resistance in its simplest form: more capacitance or a faster clock lowers it.

### Solution 22-01.8

(a) $DV_{in}$ = **2.00** V.

(b) $a_1 = (2 \times 5/\pi)\sin(0.4\pi) = 3.1831 \times 0.95106$ = **3.027** V.

(c) $a_2 = (2 \times 5/2\pi)\lvert\sin(0.8\pi)\rvert = 1.5915 \times 0.58779$ = **0.935** V.

(d) At $f_s = 20f_0$ the attenuation is $1/\lvert 1 - 400\rvert$ = 1/399, so the ripple is about $2 \times 3.027/399$ = **15.2** mV peak to peak.

(e) At $2f_s = 40f_0$: $0.935/\lvert 1 - 1600\rvert$ = **0.585** mV amplitude, about a thirteenth of the fundamental's 7.6 mV amplitude ($3.027/399$): the fundamental dominates.

### Solution 22-01.9

(a) $0.08 + 0.02 \times 3 + 0.01 \times 9$ = **0.230** W. (b) $5.4/5.63$ = **95.91** %.

(c) At 1 MHz, $P_0$ = 0.16 W and $a$ = 0.04 W/A: $0.16 + 0.12 + 0.09$ = **0.370** W. (d) $5.4/5.77$ = **93.59** %.

(e) $0.370/0.230$ = **1.61**: doubling the frequency raised the loss by 61%, not 100%, because the conduction loss did not change.

(f) $0.16 + 0.12 + 0.063$ = 0.343 W, so η = $5.4/5.743$ = **94.03** %. Part of the frequency penalty is recovered by the smaller magnetics, which is exactly the optimization of §3.6.

### Solution 22-01.10

(a) The losses are $P_{in} - P_{out}$: 0.227, 0.375 and 1.500 W. Write $P_0 + aI + RI^2$ at the three loads:
$$
\begin{aligned}
P_0 + a + R &= 0.227,\\
P_0 + 5a + 25R &= 0.375,\\
P_0 + 20a + 400R &= 1.500 .
\end{aligned}
$$
Subtracting the first from the second gives $4a + 24R = 0.148$, so $a = 0.037 - 6R$. Subtracting the second from the third gives $15a + 375R = 1.125$. Substituting, $0.555 - 90R + 375R = 1.125$, so $R$ = **2.0** mΩ, $a$ = **25** mW/A and $P_0$ = **200** mW.

(b) $I^* = \sqrt{0.2/0.002}$ = **10.0** A. (c) The loss there is 0.2 + 0.25 + 0.2 = 0.65 W, so η = 10/10.65 = **93.90** %.

(d) $1/1.227$ = **81.50** %, $5/5.375$ = **93.02** % and $20/21.5$ = **93.02** %. The loss per unit output, $P_0/I + a + RI$, is $0.04 + 0.025 + 0.01$ = 0.075 at 5 A and $0.01 + 0.025 + 0.04$ = 0.075 at 20 A. The two loads sit symmetrically about the peak: $5 \times 20 = I^{*2}$.

### Solution 22-01.11

(a) From §3.5, $I_{N\to N+1} = \sqrt{N(N + 1)P_0/R}$ with $P_0$ = 0.25 W and $R$ = 1 mΩ:

- 1 → 2: $\sqrt{2 \times 250}$ = **22.4** A;
- 2 → 3: $\sqrt{6 \times 250}$ = **38.7** A;
- 3 → 4: $\sqrt{12 \times 250}$ = **54.8** A.

(b) Two phases at 30 A: loss $2 \times 0.25 + 0.001 \times 900/2$ = 0.95 W, so η = $24/24.95$ = **96.19** %.

(c) Four phases: $1.0 + 0.225$ = 1.225 W, so η = $24/25.225$ = **95.14** %. Running all four at 30 A costs a point.

(d) At 80 A: $1.0 + 0.001 \times 6400/4$ = 2.6 W, so η = $64/66.6$ = **96.10** %.

### Solution 22-01.12

(a) $50 \times 40 \times 25$ = 50 000 mm³ = 3.051 in³, so 65/3.051 = **21.3** W/in³.

(b) The surface is $2(50 \cdot 40 + 50 \cdot 25 + 40 \cdot 25)$ = 8500 mm² = 8.5 × 10⁻³ m². It can shed $10 \times 0.0085 \times 40$ = **3.40** W.

(c) $65/(65 + 3.4)$ = **95.0** %.

(d) At 93%, the loss is $65(1/0.93 - 1)$ = **4.89** W, so the case runs $4.89/(10 \times 0.0085)$ = **57.6** K above ambient: too hot to hold. The case would have to be bigger, the converter more efficient, or the charger allowed to throttle.

### Solution 22-01.13

(a) $P_{bus} = 3000/0.97$ = **3093** W.

(b) $C = 2P_{bus}t/(V_1^2 - V_2^2) = 2 \times 3093 \times 0.010/(390^2 - 300^2)$ = 61.86/62 100 = **0.996** mF.

(c) $61.86/(390^2 - 330^2)$ = 61.86/43 200 = **1.43** mF.

(d) $62\,100/43\,200$ = **1.44** times larger: the narrower input range wastes the bottom of the capacitor's energy.

(e) Twice the energy: **1.99** mF.

### Solution 22-01.14

(a) $0.94 \times 0.96 \times 0.88$ = **79.41** %. (b) $1000/0.79411$ = **1259.3** W. (c) **259.3** W.

(d) With the VRM at 90%, the chain is 81.22%, and the input is 1231.3 W: a saving of **28.0** W.

(e) With the supply at 96%, the chain is 81.10%, and the input is 1233.0 W: a saving of **26.2** W.

(f) Both upgrades are two points: **14.0** W per point at the VRM against **13.1** W per point at the supply. They are close for a general reason: raising stage $k$ by Δη saves $P_{in}\Delta\eta/(\eta_k + \Delta\eta)$, so a point is worth about $P_{in}/\eta_k$ at any stage and the stages differ only through $1/\eta_k$.

### Solution 22-01.15

(a) $3000(1/0.99 - 1)$ = **30.3** W. (b) $3000/150$ = **20** in³. (c) $30.3/20$ = **1.52** W/in³.

(d) $0.99 \times 0.98$ = **97.02** %. (e) $3000(1/0.9702 - 1)$ = **92.1** W. (f) $92.1/20$ = **4.61** W/in³. (g) $92.1/30.3$ = **3.04**: the "99%" understated the heat threefold.

(h) From $\rho \le q\eta/(1 - \eta)$: $\eta \ge \rho/(\rho + q) = 150/153$ = **98.04** %. Unless the whole converter reaches 98%, or the cooling beats 3 W/in³ (forced air or a cold plate), the density claim does not hold for the full product. The question to ask is which box, and with what cooling.

### Solution 22-01.16

At 1 mA the output is 1.8 mW. (a) PWM loses 6 + 0.02 + 0.000\,25 = 6.020 mW: η = 1.8/7.820 = **23.02** %. (b) PFM loses 0.020 + 0.020 + 0.000\,6 = 0.0406 mW: η = **97.79** %. At 50 mA the output is 90 mW. (c) PWM loses 6 + 1 + 0.625 = 7.625 mW: **92.19** %. (d) PFM loses 0.02 + 1 + 1.5 = 2.52 mW: **97.28** %. (e) The losses are equal where $6\ \text{mW} + 0.25I^2 = 20\ \mu\text{W} + 0.60I^2$ (the $aI$ terms cancel), at $I = \sqrt{5.98\ \text{mW}/0.35\ \Omega}$ = **130.7** mA. Below it the fixed loss dominates and PFM wins by a wide margin; above it, PFM's larger pulses cost more conduction loss than PWM's fixed loss.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-01.1a | loss at 80 % | 500 | W |
| 22-01.1b | loss at 85 % | 352.9 | W |
| 22-01.1c | loss at 97 % | 61.86 | W |
| 22-01.1d | loss at 98 % | 40.82 | W |
| 22-01.1e | saving, 80 to 85 % | 147.1 | W |
| 22-01.1f | saving, 97 to 98 % | 21.04 | W |
| 22-01.1g | share removed, 80 to 85 % | 29.4 | % |
| 22-01.1h | share removed, 97 to 98 % | 34.0 | % |
| 22-01.2a | chain efficiency | 85.65 | % |
| 22-01.2b | input power | 58.38 | W |
| 22-01.2c | loss in the 92 % stage | 4.35 | W |
| 22-01.2d | loss in the 95 % stage | 2.86 | W |
| 22-01.2e | loss in the 98 % stage | 1.17 | W |
| 22-01.2f | last stage's share of the loss | 52 | % |
| 22-01.3a | LDO efficiency | 65.98 | % |
| 22-01.3b | LDO dissipation | 0.340 | W |
| 22-01.3c | junction temperature | 42.0 | °C |
| 22-01.3d | minimum input voltage | 3.57 | V |
| 22-01.4a | LDO battery current | 2.000 | mA |
| 22-01.4b | buck battery current | 0.743 | mA |
| 22-01.4c | battery-life ratio | 2.69 | |
| 22-01.4d | LDO efficiency | 31.6 | % |
| 22-01.5a | load within 1 % of the ceiling, 25 nA | 2.475 | µA |
| 22-01.5b | load within 1 % of the ceiling, 5 µA | 495 | µA |
| 22-01.5c | fraction of the ceiling at 3 µA, 25 nA | 99.2 | % |
| 22-01.5d | fraction of the ceiling at 3 µA, 5 µA | 37.5 | % |
| 22-01.6a | loss, one step | 544.5 | nJ |
| 22-01.6b | loss, three steps | 181.5 | nJ |
| 22-01.6c | loss, ten steps | 54.45 | nJ |
| 22-01.6d | gate-drive power | 50.0 | mW |
| 22-01.7a | equivalent resistance | 1.00 | Ω |
| 22-01.7b | voltage difference | 0.100 | V |
| 22-01.7c | loss | 10.0 | mW |
| 22-01.7d | capacitance for an 18 mV drop | 5.56 | µF |
| 22-01.8a | average output | 2.00 | V |
| 22-01.8b | fundamental amplitude | 3.027 | V |
| 22-01.8c | second-harmonic amplitude | 0.935 | V |
| 22-01.8d | ripple estimate | 15.2 | mV |
| 22-01.8e | second harmonic at the output | 0.585 | mV |
| 22-01.9a | loss at 500 kHz | 0.230 | W |
| 22-01.9b | efficiency at 500 kHz | 95.91 | % |
| 22-01.9c | loss at 1 MHz | 0.370 | W |
| 22-01.9d | efficiency at 1 MHz | 93.59 | % |
| 22-01.9e | loss ratio | 1.61 | |
| 22-01.9f | efficiency at 1 MHz with 7 mΩ | 94.03 | % |
| 22-01.10a | resistance | 2.0 | mΩ |
| 22-01.10b | proportional coefficient | 25 | mW/A |
| 22-01.10c | fixed loss | 200 | mW |
| 22-01.10d | peak-efficiency load | 10.0 | A |
| 22-01.10e | peak efficiency | 93.90 | % |
| 22-01.10f | efficiency at 1 A | 81.50 | % |
| 22-01.10g | efficiency at 5 A and 20 A | 93.02 | % |
| 22-01.11a | second phase on | 22.4 | A |
| 22-01.11b | third phase on | 38.7 | A |
| 22-01.11c | fourth phase on | 54.8 | A |
| 22-01.11d | efficiency, two phases at 30 A | 96.19 | % |
| 22-01.11e | efficiency, four phases at 30 A | 95.14 | % |
| 22-01.11f | efficiency, four phases at 80 A | 96.10 | % |
| 22-01.12a | charger density | 21.3 | W/in³ |
| 22-01.12b | dissipable loss | 3.40 | W |
| 22-01.12c | minimum efficiency | 95.0 | % |
| 22-01.12d | loss at 93 % | 4.89 | W |
| 22-01.12e | case temperature rise at 93 % | 57.6 | K |
| 22-01.13a | bus power | 3093 | W |
| 22-01.13b | capacitance to 300 V | 0.996 | mF |
| 22-01.13c | capacitance to 330 V | 1.43 | mF |
| 22-01.13d | capacitance ratio | 1.44 | |
| 22-01.13e | capacitance for 20 ms | 1.99 | mF |
| 22-01.14a | chain efficiency | 79.41 | % |
| 22-01.14b | input power | 1259.3 | W |
| 22-01.14c | total loss | 259.3 | W |
| 22-01.14d | saving from a 90 % VRM | 28.0 | W |
| 22-01.14e | saving from a 96 % supply | 26.2 | W |
| 22-01.14f | saving per point, VRM | 14.0 | W |
| 22-01.14g | saving per point, supply | 13.1 | W |
| 22-01.15a | implied loss | 30.3 | W |
| 22-01.15b | volume | 20 | in³ |
| 22-01.15c | implied heat density | 1.52 | W/in³ |
| 22-01.15d | overall efficiency | 97.02 | % |
| 22-01.15e | real loss | 92.1 | W |
| 22-01.15f | real heat density | 4.61 | W/in³ |
| 22-01.15g | understatement factor | 3.04 | |
| 22-01.15h | efficiency required for 150 W/in³ | 98.04 | % |
| 22-01.16a | PWM efficiency at 1 mA | 23.02 | % |
| 22-01.16b | PFM efficiency at 1 mA | 97.79 | % |
| 22-01.16c | PWM efficiency at 50 mA | 92.19 | % |
| 22-01.16d | PFM efficiency at 50 mA | 97.28 | % |
| 22-01.16e | crossover load | 130.7 | mA |
