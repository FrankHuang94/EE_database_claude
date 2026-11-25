# Solutions 22-10 · Datacenter Power Delivery

Problems: [22-10 problem set](../problems/22-10-problems.md) · Chapter: [22-10](../chapters/22-10-datacenter-power-delivery.md). Every number below is recomputed by [verify_22_10.py](../verify/verify_22_10.py).

---

## Solutions

### Solution 22-10.1

(a) $1\ \text{MW}/54\ \text{V}$ = **18519** A; (b) $1\ \text{MW}/800\ \text{V}$ = **1250** A; (c) $(800/54)^2$ = **219**. At 54 V a megawatt needs more than eighteen kiloamperes, which is why NVIDIA counts the copper in hundreds of kilograms.

### Solution 22-10.2

(a) $1000^2 \times 100\ \mu\Omega$ = **100** W; (b) a third, **33.3** W; (c) the full current flows over half the length: **50** W.

### Solution 22-10.3

$n_cV_{DC}/(2\sqrt3V_{LL}\cos\varphi)$: (a) $3 \times 800/(2\sqrt3 \times 480 \times 0.95)$ = **1.52**; (b) $4 \times 800/(\ldots)$ = **2.03**. A lower power factor favours DC further, because the AC conductors carry reactive current that delivers no power.

### Solution 22-10.4

(a) $0.975 \times 0.98 \times 0.90$ = **86.0** % and (b) $0.985 \times 0.975 \times 0.90$ = **86.4** %; (c) **1.163** MW and (d) **1.157** MW; (e) **5.9** kW per megawatt of chip power. The conversion stages differ little in this example; the larger gains of 800 V come from distribution loss and copper (Example 22-10.2), and the VRM still dominates.

### Solution 22-10.5

(a) $1.0/12$ = **0.0833**; (b) $12 \times 0.0833 \times 0.9167/(150\ \text{nH} \times 800\ \text{kHz})$ = **7.64** A.

(c) $ND$ = 0.5, $m$ = 0: $\Delta I_\Sigma = (12/(150\ \text{nH} \times 800\ \text{kHz}))(0.5)(0.5)/6$ = **4.17** A.

(d) $ND$ = 1: **0** A. With 12 phases the falling slopes of eleven phases cancel the rising slope of one at every instant.

### Solution 22-10.6

(a) $1200/(0.8 \times 70)$ = 21.4, so **22** phases; (b) $1200/22$ = **54.5** A.

### Solution 22-10.7

(a) $R_{LL} = 80\ \text{mV}/600\ \text{A}$ = **0.133** mΩ, from 1.04 V at no load to 0.96 V at 600 A; (b) $1.04 - 0.133\ \text{m}\Omega \times 300$ = **1.00** V; (c) $(1.00 - 0.96) \times 600$ = **24** W.

### Solution 22-10.8

(a) $1/(2\pi\sqrt{3\ \text{pH} \times 30\ \mu\text{F}})$ = **16.8** MHz; (b) $\sqrt{3\ \text{pH}/30\ \mu\text{F}}$ = **316** µΩ; (c) $150 \times 316\ \mu\Omega$ = **47.4** mV.

(d) $Z_0$ must fall to $30\ \text{mV}/150\ \text{A}$ = 200 µΩ, so $L = Z_0^2C = (200\ \mu\Omega)^2 \times 30\ \mu\text{F}$ = **1.2** pH, less than half the present value.

### Solution 22-10.9

(a) $\tfrac12 \times 2\ \text{pH} \times 100^2$ = **10** nJ; (b) $\tfrac12 \times 20\ \mu\text{F} \times (31.6\ \text{mV})^2$ = **10** nJ. At the first droop the inductor's current has caught up with the load, so the energy the capacitor gave up to cover the gap equals the energy the inductor gained: $\tfrac12Cv^2 = \tfrac12L\Delta I^2$ gives $v = \Delta I\sqrt{L/C}$.

### Solution 22-10.10

(a) $1.72 \times 10^{-8}/35 \times 10^{-6}$ = **0.491** mΩ per square; (b) 0.75 squares: **0.369** mΩ; (c) $2 \times 0.369/6$ = **0.123** mΩ; (d) $800^2 \times 0.123\ \text{m}\Omega$ = **78.6** W; (e) **7.86** W.

### Solution 22-10.11

(a) $50/40$ = **1.25**; (b) **0.25** of the IT power goes to overhead; (c) **0.16** higher; (d) at 40 MW of IT load that gap is **6.4** MW.

### Solution 22-10.12

(a) $0.60 \times 1200 \times 0.020$ = **14.4** J; (b) $2 \times 14.4/(54^2 - 48^2)$ = **0.0471** F.

### Solution 22-10.13

(a) $0.03 \times 0.75/400$ = **56.25** µΩ; (b) $2\ \text{m}\Omega/56.25\ \mu\Omega$ = 35.6, so **36** capacitors. In practice capacitors of several values are mixed so that their resonances cover a band, and their mounting inductance, not ESR alone, decides how many are needed at high frequency.

### Solution 22-10.14

(a) With every phase on, each inductor current rises at $(V_{in} - V_o)/L$, so the total rises at $N(V_{in} - V_o)/L = 16 \times 11.25/120\ \text{nH}$ = **1500** A/µs. (b) A 600 A step takes 600/1500 = **0.40** µs. (c) The deficit between the stepped load and the ramping regulator is a triangle: $\tfrac12 \times 600 \times 0.40\ \mu\text{s}$ = **120** µC. (d) $C \ge Q/\Delta V = 120\ \mu\text{C}/30\ \text{mV}$ = **4.0** mF. (e) Eight phases halve the slew: **0.80** µs and **8.0** mF. The charge, and so the capacitance, grows as the square of the pick-up time, which is why fast transient response is bought with phases or with smaller inductance (at the cost of ripple).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-10.1a | current at 54 V | 18519 | A |
| 22-10.1b | current at 800 V | 1250 | A |
| 22-10.1c | cross-section factor | 219 | |
| 22-10.2a | far-end load | 100 | W |
| 22-10.2b | uniform load | 33.3 | W |
| 22-10.2c | midpoint load | 50 | W |
| 22-10.3a | ratio, three AC conductors | 1.52 | |
| 22-10.3b | ratio, four AC conductors | 2.03 | |
| 22-10.4a | 48 V chain efficiency | 86.0 | % |
| 22-10.4b | 800 V chain efficiency | 86.4 | % |
| 22-10.4c | 48 V input power | 1.163 | MW |
| 22-10.4d | 800 V input power | 1.157 | MW |
| 22-10.4e | difference | 5.9 | kW |
| 22-10.5a | duty cycle | 0.0833 | |
| 22-10.5b | single-phase ripple | 7.64 | A |
| 22-10.5c | summed ripple, 6 phases | 4.17 | A |
| 22-10.5d | summed ripple, 12 phases | 0 | A |
| 22-10.6a | phase count | 22 | |
| 22-10.6b | current per phase | 54.5 | A |
| 22-10.7a | load line | 0.133 | mΩ |
| 22-10.7b | voltage at 300 A | 1.00 | V |
| 22-10.7c | power saved | 24 | W |
| 22-10.8a | resonant frequency | 16.8 | MHz |
| 22-10.8b | characteristic impedance | 316 | µΩ |
| 22-10.8c | first droop | 47.4 | mV |
| 22-10.8d | package inductance for 30 mV | 1.2 | pH |
| 22-10.9a | inductor energy | 10 | nJ |
| 22-10.9b | capacitor energy | 10 | nJ |
| 22-10.10a | sheet resistance | 0.491 | mΩ |
| 22-10.10b | one plane over the path | 0.369 | mΩ |
| 22-10.10c | loop resistance | 0.123 | mΩ |
| 22-10.10d | loss | 78.6 | W |
| 22-10.10e | vertical loss | 7.86 | W |
| 22-10.11a | PUE | 1.25 | |
| 22-10.11b | overhead fraction | 0.25 | |
| 22-10.11c | gap to 1.09 | 0.16 | |
| 22-10.11d | gap in power at 40 MW | 6.4 | MW |
| 22-10.12a | swing energy | 14.4 | J |
| 22-10.12b | capacitance | 0.0471 | F |
| 22-10.13a | target impedance | 56.25 | µΩ |
| 22-10.13b | capacitor count | 36 | |
| 22-10.14a | maximum slew rate | 1500 | A/µs |
| 22-10.14b | pick-up time | 0.40 | µs |
| 22-10.14c | charge supplied by the capacitors | 120 | µC |
| 22-10.14d | capacitance | 4.0 | mF |
| 22-10.14e | pick-up time, 8 phases | 0.80 | µs |
| 22-10.14f | capacitance, 8 phases | 8.0 | mF |
