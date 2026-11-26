# Solutions 25-10 · Qualification and Functional Safety

Problems: [25-10 problems](../problems/25-10-problems.md) · Chapter: [25-10](../chapters/25-10-qualification-and-functional-safety.md)

Every number is recomputed by [verify_25_10.py](../verify/verify_25_10.py).

---

## Solutions

### Solution 25-10.1

(a) Range $125 - (-55)$ = **180** K; $AF = (180/60)^2$ = **9.0**; $1000 \times 9.0/365.25$ = **24.6** years.

(b) $2000 \times 11.67/365.25$ = **63.9** years, against 47.9 years for today's 1,500 cycles: revision J's cut removed a quarter of the cycles.

### Solution 25-10.2

Fifteen years is $15 \times 365.25$ = **5.48e3** cycles, so $(205/60)^n \ge 5.479$, $n \ge \ln 5.479/\ln 3.417$ = **1.38**. Solder fatigue ($n \approx 2$) is covered; a mechanism with a smaller exponent would not be.

### Solution 25-10.3

Segment by segment at 0.5 eV, the acceleration factors to 150 °C are **7.1e4** (−40 °C), **24.5** (70 °C), **4.19** (110 °C) and **2.37** (125 °C), so the segments need **0.014**, **532**, **956** and **845** stress hours. In total **2.33e3** h are needed, so 1,000 h covers **43**% of the profile. A lower activation energy makes the hot test accelerate less, so more test time is needed.

### Solution 25-10.4

$SPFM = 1 - (1 - DC) \times 120/220$.

(a) $(1 - DC) \le 0.01 \times 220/120 = 0.0183$: $DC \ge$ **98.2**%.

(b) $(1 - DC) \le 0.03 \times 220/120 = 0.055$: $DC \ge$ **94.5**%. Because 100 of the 220 FIT in the SPFM denominator are not dangerous (the core's 80 FIT of safe faults and the comparator's 20 FIT of multiple-point faults), 45% of the total, the lockstep needs less than 99% coverage to reach a 99% SPFM.

### Solution 25-10.5

(a) $1 - 30/(230 - 1.2)$ = **86.9**%: below 90%.

(b) $30(1 - x) \le 0.10 \times 228.8$ gives $x \ge$ **23.7**%. Even a modest self-test of the checker restores the margin; without one, ASIL D fails.

### Solution 25-10.6

With a test that reveals every comparator fault, $\tau = 1000/2$ = 500 h: $20 \times 10^{-9} \times 118.8 \times 10^{-9} \times 500 \times 10^9$ = **0.00119** FIT, fifteen times less than never testing.

### Solution 25-10.7

The allocation is $0.10 \times 10$ = **1.0** FIT, and 1.20 FIT exceeds it: **no**. The residual faults must be cut (higher coverage or fewer dangerous faults) or the budget renegotiated.

### Solution 25-10.8

$1 - (1 - 10^{-7})^{20{,}000}$ = **0.200**%, still two vehicles per thousand.

### Solution 25-10.9

$100 \times 10^{-9} \times 10^4$ = **1.0e-3**.

### Solution 25-10.10

$n = \ln 0.1/\ln(1 - 10^{-4})$ = **2.30e4** units, about 100 times a 231-unit qualification. ppm-level quality is demonstrated by production volume, screening and field data, not by qualification samples.

### Solution 25-10.11

Raw: $4 \times 1000$ = **4.0e3** FIT. Residual, counting every multi-bit event: $0.001 \times 4000$ = **4.0** FIT, 40% of an entire ASIL D item's budget. This is an upper bound: SEC-DED detects double-bit errors, and a detected error that drives the system to a safe state is not a residual fault, so only undetected events (three or more bits, or miscorrections) belong here. Raw soft errors alone would be 400 times the budget, which is why safety-critical SRAM always carries ECC, often with interleaving so that physically adjacent upsets land in different words.

### Solution 25-10.12

(a) High severity (possible fatal crash), high exposure (highway driving is common) and low controllability (the driver cannot avoid the sudden stop or the car behind): all three push the ASIL up, toward the most demanding levels. (b) Severity is lower at parking speed, exposure is moderate and most drivers can still steer, more heavily: the ASIL is lower. (c) No injury can result, so severity is minimal: QM, ordinary quality management. The assignment comes from the item's hazard analysis, not from the chip; the chip supports whatever ASIL the safety goal carries.

### Solution 25-10.13

(a) A time $t$ after the last test, a latent fault is present with probability $1 - e^{-\lambda_L(t \bmod T)} \approx \lambda_L(t \bmod T)$, because it may have arrived at any moment since the test. A covered dangerous fault then violates the goal at rate $\lambda_{DD}$, so the instantaneous violation rate is $\lambda_{DD}\lambda_L(t \bmod T)$. Its average over one interval is $\lambda_L\lambda_{DD}\frac1T\int_0^Tt\,dt = \lambda_L\lambda_{DD}T/2$, and every interval repeats it.

(b) $20 \times 10^{-9} \times 118.8 \times 10^{-9} \times 360 \times 10^9$ = **8.55e-4** FIT.

(c) Never testing gives an exposure of 7,500 h against 360 h: **20.8** times better. At these small rates both are negligible against the residual faults, so the test matters mostly for the LFM.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-10.1a | Grade 2 range | 180 | K |
| 25-10.1a1 | AF | 9.0 | |
| 25-10.1a2 | field years | 24.6 | years |
| 25-10.1b | old Grade 0 field years | 63.9 | years |
| 25-10.2a | field cycles in 15 years | 5.48e3 | |
| 25-10.2b | minimum exponent | 1.38 | |
| 25-10.3a | stress hours at 150 °C, 0.5 eV | 2.33e3 | h |
| 25-10.3b | coverage of 1,000 h | 43 | % |
| 25-10.4a | coverage for 99% SPFM | 98.2 | % |
| 25-10.4b | coverage for 97% SPFM | 94.5 | % |
| 25-10.5a | LFM without self-test | 86.9 | % |
| 25-10.5b | self-test coverage needed | 23.7 | % |
| 25-10.6a | dual-point rate | 0.00119 | FIT |
| 25-10.6b | improvement over never testing | 15 | |
| 25-10.7a | SoC allocation | 1.0 | FIT |
| 25-10.8a | vehicles affected | 0.200 | % |
| 25-10.9a | violation probability | 1.0e-3 | |
| 25-10.10a | units needed | 2.30e4 | |
| 25-10.10b | ratio to 231 units | 100 | |
| 25-10.11a | raw rate | 4.0e3 | FIT |
| 25-10.11b | residual rate | 4.0 | FIT |
| 25-10.11c | raw over budget | 400 | |
| 25-10.3s1 | AF −40 → 150 °C, 0.5 eV | 7.1e4 | |
| 25-10.3s2 | AF 70 → 150 °C, 0.5 eV | 24.5 | |
| 25-10.3s3 | AF 110 → 150 °C, 0.5 eV | 4.19 | |
| 25-10.3s4 | AF 125 → 150 °C, 0.5 eV | 2.37 | |
| 25-10.3s5 | hours, −40 °C segment | 0.014 | h |
| 25-10.3s6 | hours, 70 °C segment | 532 | h |
| 25-10.3s7 | hours, 110 °C segment | 956 | h |
| 25-10.3s8 | hours, 125 °C segment | 845 | h |
| 25-10.13b | dual-point rate, monthly test | 8.55e-4 | FIT |
| 25-10.13c | improvement over never testing | 20.8 | |
