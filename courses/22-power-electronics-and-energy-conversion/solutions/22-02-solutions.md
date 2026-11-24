# Solutions 22-02 · Steady-State Analysis and the Buck Converter

Problems: [22-02 problem set](../problems/22-02-problems.md) · Chapter: [22-02](../chapters/22-02-buck-converter-steady-state.md). Every number below is recomputed by [verify_22_02.py](../verify/verify_22_02.py).

---

## Solutions

### Solution 22-02.1

(a) The inductor sees $24 - V$ for $DT_s$ and $-V$ for $D'T_s$. Volt-second balance gives $(24 - V)(0.25) = V(0.75)$, so $V = 0.25 \times 24$ = **6.0** V.

(b) Charge balance on the output capacitor makes the average inductor current equal the 3 A load. The input current is the inductor current while the high-side switch is on and zero otherwise, so $I_{in} = DI_L = 0.25 \times 3$ = **0.75** A. Power balance: 24 × 0.75 = 18 W = 6 × 3 W.

### Solution 22-02.2

(a) $D = 1.8/5$ = **0.36**.

(b) $\Delta i_L = V(1 - D)/(f_sL) = 1.8 \times 0.64/(2\ \text{MHz} \times 1\ \mu\text{H})$ = **0.576** A.

(c) $r = 0.576/2$ = **0.288**.

(d) $2 + 0.288$ = **2.29** A.

(e) $\Delta v = \Delta i_L/(8f_sC) = 0.576/(8 \times 2 \times 10^6 \times 22 \times 10^{-6})$ = **1.64** mV.

### Solution 22-02.3

(a) $2\sqrt{1 + 0.288^2/12}$ = **2.007** A.

(b) $\sqrt{0.36} \times 2.007$ = **1.204** A; (c) $\sqrt{0.64} \times 2.007$ = **1.606** A.

(d) $2\sqrt{0.36 \times 0.64 + 0.36 \times 0.288^2/12}$ = **0.965** A, or 0.960 A without the small ripple term.

(e) $0.576/(2\sqrt3)$ = **0.166** A.

### Solution 22-02.4

(a) $2/(8 \times 100\ \text{kHz} \times 220\ \mu\text{F})$ = **11.4** mV.

(b) $0.030 \times 2$ = **60** mV.

(c) **71.4** mV: the ESR term is five times the capacitive one, so this capacitor's ripple is ESR-dominated and more capacitance would hardly help.

(d) $(20 - 11.36)/2$ = **4.32** mΩ, which a polymer or ceramic bank, not a single electrolytic, achieves.

### Solution 22-02.5

(a) $1.0 = 5D - 6[0.020D + 0.010(1 - D) + 0.005] = 5D - 6(0.010D + 0.015)$, so $D(5 - 0.06) = 1.09$ and $D$ = **0.2206**.

(b) $R_{eq} = 0.2206 \times 20 + 0.7794 \times 10 + 5$ = **17.21** mΩ.

(c) $36 \times 0.01721$ = **0.619** W.

(d) $6/(6 + 0.619)$ = **90.64** %.

### Solution 22-02.6

(a) With the diode, $5 = 12D - (1 - D)0.45$, so $D = 5.45/12.45$ = **0.4378**.

(b) $0.5622 \times 0.45 \times 3$ = **0.759** W.

(c) $(7/12) \times 9 \times 0.015$ = **0.0788** W.

(d) **9.64** times.

(e) $0.759/15$ = **5.06** %; (f) $0.0788/15$ = **0.53** %. At 5 V a diode is tolerable for a cost-driven design; at 1 V it would not be (Example 22-02.4).

### Solution 22-02.7

(a) $D = 5/24$, so $\Delta i_L = 5 \times (19/24)/(300\ \text{kHz} \times 22\ \mu\text{H})$ = **0.600** A.

(b) $I_{crit} = \Delta i_L/2$ = **0.300** A.

(c) $K = 2 \times 22\ \mu\text{H}/(50 \times 3.333\ \mu\text{s})$ = **0.264**.

(d) $K_{crit} = 1 - 5/24$ = **0.792** > 0.264: discontinuous. Equivalently, 0.1 A is below the 0.3 A critical current.

### Solution 22-02.8

(a) $M = 2/(1 + \sqrt{1 + 4K/D^2})$ with $D^2 = 0.04340$: $4K/D^2$ = 24.33, $\sqrt{25.33}$ = 5.033, so $M$ = **0.332**.

(b) $0.332 \times 24$ = **7.96** V, far above 5 V. Open loop, light load drives the output up.

(c) Set $M$ = 5/24: $2/M - 1 = 8.6$, so $4K/D_1^2 = 8.6^2 - 1 = 72.96$ and $D_1 = \sqrt{1.056/72.96}$ = **0.120**.

### Solution 22-02.9

(a) $i_{pk} = (4.0 - 1.2) \times 200\ \text{ns}/1\ \mu\text{H}$ = **0.560** A.

(b) Volt-second balance: $T_{off} = 200 \times 2.8/1.2$ = **466.7** ns.

(c) $Q = \tfrac12 \times 0.56 \times 666.7\ \text{ns}$ = **186.7** nC.

(d) $f = 10\ \text{mA}/186.7\ \text{nC}$ = **53.6** kHz.

(e) The pulses touch when the period equals $T_{on} + T_{off}$ = 666.7 ns, a rate of **1.50** MHz. The load is then $Q/(T_{on} + T_{off}) = i_{pk}/2$ = **0.280** A, the critical current for a ripple equal to $i_{pk}$.

### Solution 22-02.10

(a) $I_{crit} = V(1 - D)T_s/(2L)$ and $I = V/R$. Then $I < I_{crit}$ means $V/R < V(1 - D)T_s/(2L)$. Multiplying both sides by $2L/(VT_s)$ gives $2L/(RT_s) < 1 - D$, which is $K < K_{crit}$.

(b) $R = V/I_{crit} = 5/0.2999$ = **16.67** Ω.

(c) $K = 2 \times 22\ \mu\text{H}/(16.67 \times 3.333\ \mu\text{s})$ = **0.792** = $1 - 5/24$.

### Solution 22-02.11

(a) $D = 0.9/20 = 0.045$, so $f_s \le 0.045/50\ \text{ns}$ = **900** kHz.

(b) $0.045/60\ \text{ns}$ = **750** kHz.

### Solution 22-02.12

(a) At $V_{in,max}$ = 13.2 V, $D_{min} = 3.3/13.2$ = **0.250**.

(b) $\Delta i_L = 0.3 \times 5 = 1.5$ A, so $L = 3.3 \times 0.75/(1\ \text{MHz} \times 1.5)$ = **1.65** µH.

(c) $5 + 0.75$ = **5.75** A.

(d) $C = 1.5/(8 \times 1\ \text{MHz} \times 0.015)$ = **12.5** µF effective; (e) $12.5/0.6$ = **20.8** µF nominal.

(f) $\text{ESR} \le 5\ \text{mV}/1.5\ \text{A}$ = **3.33** mΩ.

(g) $I\sqrt{D(1 - D)}$ grows as $D$ approaches 0.5, so the worst case is the highest duty cycle, at $V_{in,min}$ = 10.8 V ($D$ = 0.3056): $5\sqrt{0.3056 \times 0.6944}$ = **2.30** A.

(h) $D_{min}T_s$ = **250** ns, well above typical minimum on-times.

### Solution 22-02.13

(a) $3.3/4.2$ = **0.786**.

(b) In 100% mode the output is the input minus $I(R_{DS(on)} + R_L)$: $V_{in,min} = 3.3 + 0.3 \times 0.3$ = **3.39** V.

(c) $0.3 \times 0.3$ = **0.09** V: below 3.39 V the rail follows the cell, 90 mV lower.

### Solution 22-02.14

(a) $10\sqrt{0.5 \times 0.5}$ = **5.0** A.

(b) $5/4$ = **1.25** A each.

(c) Four parallel 5 mΩ capacitors have 1.25 mΩ in total: $25 \times 0.00125$ = **31.25** mW. (d) **7.8** mW each, equal to $1.25^2 \times 0.005$.

### Solution 22-02.15

(a) $L = V(1 - D)/(f_srI)$ and $I_{pk} = I(1 + r/2)$, so
$$\tfrac12LI_{pk}^2 = \frac{V(1 - D)I}{2f_s}\cdot\frac{(1 + r/2)^2}{r} .$$

(b) $g'(r) = [r(1 + r/2) - (1 + r/2)^2]/r^2 = (1 + r/2)(r/2 - 1)/r^2$, which is zero at $r$ = 2 and changes sign from negative to positive there.

(c) $g(0.3) = 1.3225/0.3$ = **4.41**. (d) $g(2) = 4/2$ = **2.00**.

(e) **2.20**: at $r$ = 0.3 the inductor stores 2.2 times the minimum energy.

(f) A ripple ratio of 2 would make the output capacitor carry ripple current comparable to the load current (a larger capacitor bank), push the core into large flux swings (core loss), raise the switches' RMS and peak currents, and put the converter at the edge of DCM at any load below full. Designers trade some inductor size for all of those.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-02.1a | output voltage | 6.0 | V |
| 22-02.1b | average input current | 0.75 | A |
| 22-02.2a | duty cycle | 0.36 | |
| 22-02.2b | inductor ripple | 0.576 | A |
| 22-02.2c | ripple ratio | 0.288 | |
| 22-02.2d | peak inductor current | 2.29 | A |
| 22-02.2e | output ripple | 1.64 | mV |
| 22-02.3a | inductor RMS | 2.007 | A |
| 22-02.3b | high-side RMS | 1.204 | A |
| 22-02.3c | low-side RMS | 1.606 | A |
| 22-02.3d | input-capacitor RMS | 0.965 | A |
| 22-02.3e | output-capacitor RMS | 0.166 | A |
| 22-02.4a | capacitive ripple | 11.4 | mV |
| 22-02.4b | ESR ripple | 60 | mV |
| 22-02.4c | conservative total | 71.4 | mV |
| 22-02.4d | ESR for 20 mV | 4.32 | mΩ |
| 22-02.5a | duty cycle | 0.2206 | |
| 22-02.5b | equivalent resistance | 17.21 | mΩ |
| 22-02.5c | conduction loss | 0.619 | W |
| 22-02.5d | efficiency | 90.64 | % |
| 22-02.6a | duty cycle with a diode | 0.4378 | |
| 22-02.6b | diode loss | 0.759 | W |
| 22-02.6c | synchronous loss | 0.0788 | W |
| 22-02.6d | ratio | 9.64 | |
| 22-02.6e | diode loss share | 5.06 | % |
| 22-02.6f | synchronous loss share | 0.53 | % |
| 22-02.7a | inductor ripple | 0.600 | A |
| 22-02.7b | critical current | 0.300 | A |
| 22-02.7c | K at 50 Ω | 0.264 | |
| 22-02.7d | critical K | 0.792 | |
| 22-02.8a | open-loop DCM ratio | 0.332 | |
| 22-02.8b | open-loop output | 7.96 | V |
| 22-02.8c | duty for 5 V | 0.120 | |
| 22-02.9a | peak current | 0.560 | A |
| 22-02.9b | off-time | 466.7 | ns |
| 22-02.9c | charge per pulse | 186.7 | nC |
| 22-02.9d | pulse rate at 10 mA | 53.6 | kHz |
| 22-02.9e | pulse rate at the boundary | 1.50 | MHz |
| 22-02.9f | load at the boundary | 0.280 | A |
| 22-02.10a | boundary load resistance | 16.67 | Ω |
| 22-02.10b | K at the boundary | 0.792 | |
| 22-02.11a | frequency limit | 900 | kHz |
| 22-02.11b | frequency limit with margin | 750 | kHz |
| 22-02.12a | smallest duty cycle | 0.250 | |
| 22-02.12b | inductance | 1.65 | µH |
| 22-02.12c | peak current | 5.75 | A |
| 22-02.12d | effective capacitance | 12.5 | µF |
| 22-02.12e | nominal capacitance | 20.8 | µF |
| 22-02.12f | ESR budget | 3.33 | mΩ |
| 22-02.12g | worst input-capacitor RMS | 2.30 | A |
| 22-02.12h | smallest on-time | 250 | ns |
| 22-02.13a | duty at 4.2 V | 0.786 | |
| 22-02.13b | dropout input | 3.39 | V |
| 22-02.13c | drop in 100 % mode | 0.09 | V |
| 22-02.14a | total input-capacitor RMS | 5.0 | A |
| 22-02.14b | RMS per capacitor | 1.25 | A |
| 22-02.14c | bank heat | 31.25 | mW |
| 22-02.14d | heat per capacitor | 7.8 | mW |
| 22-02.15a | g(0.3) | 4.41 | |
| 22-02.15b | g(2) | 2.00 | |
| 22-02.15c | energy ratio | 2.20 | |
