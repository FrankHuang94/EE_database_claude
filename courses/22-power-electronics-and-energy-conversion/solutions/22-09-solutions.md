# Solutions 22-09 · Batteries, Charging and Fuel Gauging

Problems: [22-09 problem set](../problems/22-09-problems.md) · Chapter: [22-09](../chapters/22-09-batteries-charging-fuel-gauging.md). Every number below is recomputed by [verify_22_09.py](../verify/verify_22_09.py).

---

## Solutions

### Solution 22-09.1

(a) $4.5\ \text{Ah} \times 3.87\ \text{V}$ = **17.4** Wh; (b) $17.415/0.070$ = **249** Wh/kg; (c) $0.7 \times 4.5$ = **3.15** A.

### Solution 22-09.2

(a) $-\Delta G = nFE = 96\,485 \times 3.3$ = **318** kJ/mol.

(b) $q_{th} = F/(3.6M) = 96\,485/(3.6 \times 157.76)$ = **170** mAh/g, less than half of graphite's 372 mAh/g, which is one reason LFP cells store less energy per kilogram.

### Solution 22-09.3

$\tau_1 = R_1C_1$ = 20 s, and at 10 s, $1 - e^{-0.5}$ = 0.3935.

(a) $3.75 - 2 \times 0.08$ = **3.590** V.

(b) $3.75 - 2(0.08 + 0.05 \times 0.3935)$ = **3.551** V.

(c) $R_0$'s drop vanishes at once, but $v_1 = 2 \times 0.05 \times 0.3935$ = **39.3** mV remains: **3.711** V.

(d) $v_1$ decays by $e^{-0.5}$ to **23.9** mV: **3.726** V. The cell is still 24 mV below its OCV 10 s after the pulse, so a gauge that reads it as OCV would misjudge the SOC (§3.6). (Assuming the teaching cell's OCV slope of 0.9 V per unit SOC, the SOC drift moves the OCV by $0.9 \times 20\ \text{C}/16\,200\ \text{C}$ = **1.1** mV, negligible for this 4500 mAh cell.)

### Solution 22-09.4

$z_{end} = IR/0.90$.

(a) $0.6 \times 0.30/0.90$ = 0.20: **80** % usable.

(b) $0.6 \times 1.20/0.90$ = 0.80: **20** % usable.

(c) $z_{end}$ = 0.10 needs $IR$ = 0.09 V: $I = 0.09/1.20$ = **75** mA. A cold cell is usable only at a fraction of its warm current.

### Solution 22-09.5

(a) $z_{cv} = (4.20 - 0.15 \times 0.30 - 3.30)/0.90$ = **0.950**.

(b) $0.95 \times 1080/0.15$ = 6840 s = **114** min.

(c) $RC_{eff}$ = 360 s as before, so $360\ln(150/15)$ = 829 s = **13.8** min.

(d) **128** min.

(e) $0.950 + (0.150 - 0.015) \times 360/1080$ = **0.995**.

Halving the current from Example 22-09.4 nearly doubled the total time but ended CC at 95%; the CV time is the same because $I_{cc}/I_{term}$ is still 10.

### Solution 22-09.6

(a) $(4.20 - 0.18 - 3.30)/0.90$ = **0.800**.

(b) $0.8 \times 1080/0.3$ = 2880 s = **48.0** min.

(c) $0.60 \times 1200$ = **720** s.

(d) $720\ln 10$ = 1658 s = **27.6** min.

(e) **75.6** min.

(f) $0.800 + 0.270 \times 720/1080$ = **0.980**.

Against the new cell's 67.8 min, the aged cell charges 8 minutes slower and terminates less full, because the doubled resistance ends CC earlier and doubles the CV time constant. This is one of the signs an aged phone shows.

### Solution 22-09.7

(a) $(5.0 - 4.0) \times 0.060$ = **0.060** W; (b) $4.0/5.0$ = **80** %. Sixty milliwatts heats a small package by only a few degrees, and a linear charger saves the inductor, the switching noise and board area that a wearable cannot spare.

### Solution 22-09.8

(a) $3.8 \times 6$ = **22.8** W; (b) $22.8/0.97$ = **23.5** W; (c) **0.71** W; (d) $22.8/0.92 - 22.8$ = **1.98** W. The switched-capacitor charger dissipates about a third as much heat in the phone; the adapter, which regulates the current, takes on the conversion.

### Solution 22-09.9

The SOC error is $IR/(dV_{OC}/dz)$, with $IR$ = 0.09 V.

(a) $0.09/0.90$ = **0.10**, ten percentage points too low.

(b) $0.09/0.15$ = **0.60**: the reading is useless.

(c) A 20% error in $R$ leaves 18 mV: $0.018/0.90$ = **0.020**; (d) $0.018/0.15$ = **0.12**.

Flat curves defeat voltage gauging even with correction, which is why LFP products rely on coulomb counting and re-anchor at full charge.

### Solution 22-09.10

(a) $1\ \mu\text{V}/10\ \text{m}\Omega$ = **100** µA; (b) $100\ \mu\text{A} \times 24\ \text{h}$ = **2.4** mAh; (c) **0.80** % of 300 mAh per day.

(d) $1\ \mu\text{V}/10\ \mu\text{A}$ = **100** mΩ; (e) $0.3^2 \times 0.1$ = **9.0** mW; (f) $0.3 \times 0.1$ = **30** mV.

A larger sense resistor improves offset-limited accuracy but wastes power and steals headroom from the cell. Gauges instead measure and subtract their own offset, which lets them keep the sense resistor small.

### Solution 22-09.11

Loss $\propto \sqrt t$, and 4% at 0.5 years.

(a) $4\sqrt{2/0.5}$ = **8.0** %; (b) $4\sqrt{5/0.5}$ = **12.6** %.

(c) $\exp[(0.5\ \text{eV}/k_B)(1/298.15 - 1/308.15)]$ = **1.88**.

(d) Loss $\propto \sqrt{D't}$, so $8.0\sqrt{1.88}$ = **11.0** %. Ten degrees cost three extra points in two years.

### Solution 22-09.12

(a) $1 - 0.2 \times 730/1000$ = **85.4** %; (b) $1 - 0.2 \times 146/1000$ = **97.1** %; (c) **146** cycles.

The ring loses about 3% to cycling in two years but 8% to calendar aging (Problem 22-09.11), so time, not use, sets its battery's life.

### Solution 22-09.13

(a) $22.5 \times 0.80 \times 0.90/168$ = **96.4** µA; (b) $96.4 - 85$ = **11.4** µA, just enough for a gauge whose sleep current is about 11 µA (§9), with nothing to spare.

### Solution 22-09.14

(a) $Q_{max} = \Delta q/(z_1 - z_2) = 1.32/0.55$ = **2.40** Ah; (b) $2.40/2.6$ = **92.3** %. (c) The swing can be as small as 0.54 or as large as 0.56: $1.32/0.54$ = 2.444 Ah, **+1.85** %, and $1.32/0.56$ = 2.357 Ah, **−1.79** %. (d) The overestimate is $\Delta z/(\Delta z - 0.01) - 1 \le 0.02$, so $\Delta z \ge 1.02 \times 0.01/0.02$ = **0.51**. The error scales as the reading error over the swing: a shallow swing makes the learned capacity noisy, so gauges update only after a deep enough discharge between two rests.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-09.1a | energy | 17.4 | Wh |
| 22-09.1b | specific energy | 249 | Wh/kg |
| 22-09.1c | current at 0.7C | 3.15 | A |
| 22-09.2a | Gibbs energy per mole | 318 | kJ/mol |
| 22-09.2b | LiFePO₄ theoretical capacity | 170 | mAh/g |
| 22-09.3a | voltage at the first instant | 3.590 | V |
| 22-09.3b | voltage at 10 s | 3.551 | V |
| 22-09.3c | voltage just after removal | 3.711 | V |
| 22-09.3d | voltage 10 s after removal | 3.726 | V |
| 22-09.3e | RC-branch voltage at removal | 39.3 | mV |
| 22-09.3f | RC-branch voltage 10 s later | 23.9 | mV |
| 22-09.3g | OCV change from the SOC drift | 1.1 | mV |
| 22-09.4a | usable fraction at 25 °C | 80 | % |
| 22-09.4b | usable fraction at −10 °C | 20 | % |
| 22-09.4c | current for 90% at −10 °C | 75 | mA |
| 22-09.5a | SOC at the end of CC | 0.950 | |
| 22-09.5b | CC time | 114 | min |
| 22-09.5c | CV time | 13.8 | min |
| 22-09.5d | total time | 128 | min |
| 22-09.5e | SOC at termination | 0.995 | |
| 22-09.6a | SOC at the end of CC | 0.800 | |
| 22-09.6b | CC time | 48.0 | min |
| 22-09.6c | CV time constant | 720 | s |
| 22-09.6d | CV time | 27.6 | min |
| 22-09.6e | total time | 75.6 | min |
| 22-09.6f | SOC at termination | 0.980 | |
| 22-09.7a | dissipation | 0.060 | W |
| 22-09.7b | efficiency | 80 | % |
| 22-09.8a | battery power | 22.8 | W |
| 22-09.8b | input power | 23.5 | W |
| 22-09.8c | switched-capacitor loss | 0.71 | W |
| 22-09.8d | buck loss | 1.98 | W |
| 22-09.9a | SOC error, teaching cell | 0.10 | |
| 22-09.9b | SOC error, flat cell | 0.60 | |
| 22-09.9c | residual error, teaching cell | 0.020 | |
| 22-09.9d | residual error, flat cell | 0.12 | |
| 22-09.10a | current offset | 100 | µA |
| 22-09.10b | charge error per day | 2.4 | mAh |
| 22-09.10c | daily error share | 0.80 | % |
| 22-09.10d | sense resistance for 10 µA | 100 | mΩ |
| 22-09.10e | dissipation at 300 mA | 9.0 | mW |
| 22-09.10f | drop at 300 mA | 30 | mV |
| 22-09.11a | loss after 2 years | 8.0 | % |
| 22-09.11b | loss after 5 years | 12.6 | % |
| 22-09.11c | Arrhenius factor 25 → 35 °C | 1.88 | |
| 22-09.11d | 2-year loss at 35 °C | 11.0 | % |
| 22-09.12a | watch capacity after 2 years | 85.4 | % |
| 22-09.12b | ring capacity after 2 years | 97.1 | % |
| 22-09.12c | ring cycles in 2 years | 146 | |
| 22-09.13a | allowed average current | 96.4 | µA |
| 22-09.13b | budget left for the gauge | 11.4 | µA |
| 22-09.14a | learned capacity | 2.40 | Ah |
| 22-09.14b | state of health | 92.3 | % |
| 22-09.14c | largest overestimate | 1.85 | % |
| 22-09.14d | largest underestimate | −1.79 | % |
| 22-09.14e | smallest swing for 2% | 0.51 | |
