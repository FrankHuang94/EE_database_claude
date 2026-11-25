# Solutions 22-03 · Boost, Buck-Boost and Other Topologies

Problems: [22-03 problem set](../problems/22-03-problems.md) · Chapter: [22-03](../chapters/22-03-boost-buck-boost-topologies.md). Every number below is recomputed by [verify_22_03.py](../verify/verify_22_03.py).

---

## Solutions

### Solution 22-03.1

(a) $V = V_{in}/D'$, so $D' = 5/12$ and $D$ = **0.583**.

(b) $I_L = I/D' = 0.5 \times 12/5$ = **1.2** A.

(c) The switch blocks the output when off: **12** V.

### Solution 22-03.2

(a) $D/D' = 15/5 = 3$, so $D$ = **0.75**.

(b) $5 + 15$ = **20** V.

(c) $0.1/0.25$ = **0.4** A.

### Solution 22-03.3

(a) $D/D' = 12/24$, so $D$ = **0.333** for both.

(b) Each switch blocks $V_{in} + \lvert V\rvert = 24 + 12$ = **36** V.

### Solution 22-03.4

(a) $D = 1 - 12/48$ = **0.75**.

(b) $I_L = 2/0.25$ = **8.0** A.

(c) $\Delta i_L = 12 \times 0.75 \times 4\ \mu\text{s}/33\ \mu\text{H}$ = **1.09** A.

(d) $\Delta v = 2 \times 0.75/(250\ \text{kHz} \times 47\ \mu\text{F})$ = **0.128** V.

(e) $2\sqrt{0.75/0.25}$ = **3.46** A.

### Solution 22-03.5

(a) $V_{in} - I_LR_L = D'V$ with $I_L = I/D'$: $12 - 0.04/D' = 48D'$, so $48D'^2 - 12D' + 0.04 = 0$. The larger root (the normal operating side) is $D' = (12 + \sqrt{144 - 7.68})/96$ = **0.2466**.

(b) $D$ = **0.7534**.

(c) $\eta = D'V/V_{in} = 0.2466 \times 4$ = **98.65** %.

(d) $2/0.2466$ = **8.11** A.

(e) $M_{max} = \tfrac12\sqrt{24/0.02}$ = **17.3**.

### Solution 22-03.6

(a) $D' = \sqrt{R_L/R} = \sqrt{0.0025}$ = **0.05**, that is $D$ = 0.95.

(b) $M_{max} = \tfrac12\sqrt{400}$ = **10**.

(c) $1/(D' + 0.0025/D') = 5$ gives $D'^2 - 0.2D' + 0.0025 = 0$, so $D' = (0.2 \pm \sqrt{0.03})/2$. The larger root is **0.1866**.

(d) $D$ = **0.813**.

(e) $R_L/(D'^2R) = 0.05/(0.03482 \times 20) = 0.0718$, so η = **93.30** %.

(f) The other root, $D'$ = 0.0134 ($D$ = 0.987), lies beyond the gain peak, where raising $D$ *lowers* the output. A controller that strays there sees its correction act backwards: it pushes $D$ higher, the output falls further, and the converter latches at high current and 50% or lower efficiency. Practical controllers clamp the maximum duty cycle well below the peak.

### Solution 22-03.7

(a) $K_{crit} = DD'^2 = 0.5 \times 0.25$ = **0.125**.

(b) At 10% load, $R = 24/0.1 = 240$ Ω. CCM needs $K = 2Lf_s/R \ge 0.125$, so $L \ge 0.125 \times 240/(2 \times 200\ \text{kHz})$ = **75** µH.

### Solution 22-03.8

$M = (1 + \sqrt{1 + 4 \times 0.09/0.02})/2 = (1 + \sqrt{19})/2$ = **2.68**.

### Solution 22-03.9

(a) Buck: $D = 3.3/4.2$ = **0.786**.

(b) Boost: $D = 1 - 3.0/3.3$ = **0.091**.

(c) Near **3.3** V, where neither a buck (which needs $D \to 1$) nor a boost (which needs $D \to 0$) can regulate within its minimum on- and off-times. The part then uses its mixed buck-boost mode [1].

### Solution 22-03.10

(a) Boost: the switch blocks 12 V and carries $I/D'$, so the stress is $12(I/D')/(12I) = 1/D' = 12/5$ = **2.4**.

(b) Buck-boost: $D/D' = 12/5$, so $D$ = 0.706 and $D'$ = 0.294. The switch blocks 17 V and carries $I/D'$: $17/(12 \times 0.294)$ = **4.82**.

(c) $D$ = **0.706**.

The buck-boost doubles the switch stress for the same job; when the output is always above the input, the boost is the better choice.

### Solution 22-03.11

(a) At 2 A, $R$ = 12 Ω and $D'$ = 0.5: $f_z = 0.25 \times 12/(2\pi \times 22\ \mu\text{H})$ = **21.7** kHz.

(b) At 3 A, $R$ = 8 Ω: **14.5** kHz.

(c) **4.34** kHz; (d) **2.89** kHz.

(e) The heaviest load: the RHP zero falls as the load rises (smaller $R$), so the design must use the full-load value. A boost's loop is slowest exactly when the load is largest.

### Solution 22-03.12

(a) $90\sqrt2$ = **127.3** V.

(b) $D = 1 - 127.3/400$ = **0.682**.

(c) With unity power factor and no loss, the input current is a sinusoid in phase with the line. Its RMS value is $500/90$ A, so its peak is $\sqrt2 \times 500/90$ = **7.86** A, which the boost inductor carries at the line peak (averaged over a switching period).

### Solution 22-03.13

(a) With small ripple, the capacitor current is $I_L - I = I/D' - I = ID/D'$ for a fraction $D'$ of the time and $-I$ for a fraction $D$. Its mean is zero (charge balance), and its mean square is
$$D'\left(\frac{ID}{D'}\right)^2 + DI^2 = I^2\left(\frac{D^2}{D'} + D\right) = I^2D\,\frac{D + D'}{D'} = I^2\frac{D}{D'} .$$

(b) $\sqrt{0.75/0.25}$ = **1.73**: the capacitor carries 73% more RMS current than the load draws.

### Solution 22-03.14

(a) In DCM the inductor current rises from zero to $i_{pk} = V_{in}DT_s/L$ during the on-time and falls to zero at $\lvert V\rvert/L$ during $D_2T_s$. Volt-second balance gives $V_{in}D = \lvert V\rvert D_2$, so $D_2 = D/\lvert M\rvert$. All the inductor's off-time current flows to the output through the diode, so its average equals the load current:

$$
\frac12 i_{pk}D_2 = \frac{\lvert V\rvert}{R} \;\Rightarrow\; \frac{V_{in}DT_s}{2L}\cdot\frac{D}{\lvert M\rvert} = \frac{\lvert M\rvert V_{in}}{R} \;\Rightarrow\; \lvert M\rvert^2 = \frac{D^2RT_s}{2L} = \frac{D^2}{K} .
$$

The current stays discontinuous while $D + D_2 < 1$, that is $D + \sqrt K < 1$. At the boundary the CCM ratio $D/D'$ also holds, so $\sqrt K = D'$ there: DCM whenever $K < D'^2$. (b) $K = 2 \times 10\ \mu\text{H} \times 200\ \text{kHz}/48$ = **0.0833**. In CCM a unity ratio would need $D$ = 0.5 and $K_{crit} = D'^2$ = 0.25, so with $K$ < 0.25 the converter is discontinuous, and $D = \lvert M\rvert\sqrt K = \sqrt{0.0833}$ = **0.289**.

### Solution 22-03.15

(a) $V = (D/D')V_{in}$ gives $D = V/(V + V_{in}) = 12/21$ = **0.571**, and $V_{C1} = V_{in}$ = **9** V. (b) $L_2$ carries the load's average current, **2.00** A; power balance gives $L_1$'s, $2 \times 12/9$ = **2.67** A. (c) While the switch is on, $C_1$ carries $I_{L2}$: $\Delta V_{C1} = I_{L2}DT_s/C_1 = 2 \times 0.571 \times 3.33\ \mu\text{s}/10\ \mu\text{F}$ = **0.381** V, about 4% of its DC voltage. (d) Both inductors see $V_{in}$ during the on-time: $\Delta i = V_{in}DT_s/L = 9 \times 0.571 \times 3.33\ \mu\text{s}/20\ \mu\text{H}$ = **0.857** A each. (e) The switch carries both inductor currents when on, peaking at $2.67 + 2.00 + (0.857 + 0.857)/2$ = **5.52** A, and blocks $V_{in} + V$ = **21** V when off.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-03.1a | duty cycle | 0.583 | |
| 22-03.1b | inductor current | 1.2 | A |
| 22-03.1c | switch voltage | 12 | V |
| 22-03.2a | duty cycle | 0.75 | |
| 22-03.2b | switch voltage | 20 | V |
| 22-03.2c | inductor current | 0.4 | A |
| 22-03.3a | duty cycle | 0.333 | |
| 22-03.3b | switch voltage | 36 | V |
| 22-03.4a | duty cycle | 0.75 | |
| 22-03.4b | inductor current | 8.0 | A |
| 22-03.4c | inductor ripple | 1.09 | A |
| 22-03.4d | output ripple | 0.128 | V |
| 22-03.4e | output-capacitor RMS current | 3.46 | A |
| 22-03.5a | D' with resistance | 0.2466 | |
| 22-03.5b | duty cycle | 0.7534 | |
| 22-03.5c | efficiency | 98.65 | % |
| 22-03.5d | inductor current | 8.11 | A |
| 22-03.5e | maximum gain | 17.3 | |
| 22-03.6a | D' at peak gain | 0.05 | |
| 22-03.6b | peak gain | 10 | |
| 22-03.6c | D' for a gain of 5 | 0.1866 | |
| 22-03.6d | duty cycle | 0.813 | |
| 22-03.6e | efficiency | 93.30 | % |
| 22-03.7a | critical K at D = 0.5 | 0.125 | |
| 22-03.7b | minimum inductance | 75 | µH |
| 22-03.8a | DCM conversion ratio | 2.68 | |
| 22-03.9a | buck duty at 4.2 V | 0.786 | |
| 22-03.9b | boost duty at 3.0 V | 0.091 | |
| 22-03.9c | straddle voltage | 3.3 | V |
| 22-03.10a | boost switch stress | 2.4 | |
| 22-03.10b | buck-boost switch stress | 4.82 | |
| 22-03.10c | buck-boost duty cycle | 0.706 | |
| 22-03.11a | RHP zero at 2 A | 21.7 | kHz |
| 22-03.11b | RHP zero at 3 A | 14.5 | kHz |
| 22-03.11c | crossover limit at 2 A | 4.34 | kHz |
| 22-03.11d | crossover limit at 3 A | 2.89 | kHz |
| 22-03.12a | line peak | 127.3 | V |
| 22-03.12b | duty at the peak | 0.682 | |
| 22-03.12c | inductor current at the peak | 7.86 | A |
| 22-03.13a | RMS ratio at D = 0.75 | 1.73 | |
| 22-03.14a | K | 0.0833 | |
| 22-03.14b | duty cycle | 0.289 | |
| 22-03.15a | duty cycle | 0.571 | |
| 22-03.15b | coupling-capacitor voltage | 9 | V |
| 22-03.15c | L2 average current | 2.00 | A |
| 22-03.15d | L1 average current | 2.67 | A |
| 22-03.15e | coupling-capacitor ripple | 0.381 | V |
| 22-03.15f | inductor ripple | 0.857 | A |
| 22-03.15g | switch peak current | 5.52 | A |
| 22-03.15h | switch blocking voltage | 21 | V |
