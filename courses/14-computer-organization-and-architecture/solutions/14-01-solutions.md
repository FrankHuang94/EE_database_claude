# Solutions 14-01 · Performance, Power and the Iron Law

Problems: [14-01 problems](../problems/14-01-problems.md) · Chapter: [14-01](../chapters/14-01-performance-power-iron-law.md). Every number below is recomputed by [verify_14_01.py](../verify/verify_14_01.py), which counts cycles over generated instruction streams, simulates parallel execution with a scheduler, minimizes energy numerically and computes means directly from the data.

---

## Solutions

### Solution 14-01.1

$T = \text{IC} \times \text{CPI}/f = 4 \times 10^9 \times 0.8/(4 \times 10^9)$ = **0.8** s, and IPC = 1/0.8 = **1.25**.

### Solution 14-01.2

(a) "30% faster" means speedup 1.3, so the new time is 10/1.3 = **7.692** s (not 7 s). (b) The speedup is 10/7 = **1.4286**, so the program is **42.86**% faster.

### Solution 14-01.3

$\text{CPI} = 0.5(1) + 0.3(3) + 0.2(2)$ = **1.8**. Memory instructions take $0.9/1.8$ = **50**% of the cycles, hence of the time, though they are 30% of the instructions.

### Solution 14-01.4

Time per instruction is CPI/$f$: X takes 1.0/3 = 0.3333 ns, Y takes 1.3/4 = 0.325 ns. Y is faster by $0.3333/0.325$ = **1.026**: a 33% faster clock bought only 2.6%, because the deeper pipeline gave back most of it in stalls.

### Solution 14-01.5

Option 1: $S = 1/(0.6 + 0.4/4)$ = **1.4286**. Option 2: $S = 1/(0.4 + 0.6/1.2)$ = **1.111**. The bigger improvement to the smaller part wins here, because 4× on 40% removes 30% of the time while 1.2× on 60% removes only 10%.

### Solution 14-01.6

Solve $1/(0.4 + 0.6/s) = 1.5$: $0.4 + 0.6/s = 0.6667$, so $s$ = **2.25**. The ceiling is $1/0.4$ = 2.5, reached only as $s \to \infty$: any overall speedup of 2.5 or more is impossible.

### Solution 14-01.7

$S(8) = 1/(0.05 + 0.95/8)$ = **5.926**, efficiency **74.1**%; $S(64) = 1/(0.05 + 0.95/64)$ = **15.42**, efficiency **24.10**%. The ceiling is $1/0.05$ = **20**. Going from 8 to 64 processors (8× the hardware) gains only 2.6×.

### Solution 14-01.8

The total time is 10 + 5 + 2.5 = **17.5** s for 3 × 10⁹ operations, a true average of **171.4** MFLOPS. The arithmetic mean of the rates is **233.3** MFLOPS, too high because the fast benchmark finishes quickly and contributes little time. The harmonic mean, $3/(1/100 + 1/200 + 1/400)$ = 171.4, gives the true rate, as §3.4 shows for equal work per benchmark.

### Solution 14-01.9

At 0.8 V and 2.0 GHz: $P = 0.5 \times 10^{-9} \times 0.64 \times 2 \times 10^9$ = **0.64** W and $E = \alpha CV^2$ = **0.32** nJ per operation. At 0.6 V and 1.5 GHz: $P$ = **0.27** W and $E$ = **0.18** nJ. The energy per operation falls by $(0.6/0.8)^2$ = **0.5625**, independent of frequency; power falls further because the operations also come less often.

### Solution 14-01.10

The voltage falls in proportion to the frequency, to 0.6667 V. Power ratio $(V^2f)_{new}/(V^2f)_{old} = (2/3)^3$ = **0.2963**; energy per operation $\propto V^2$, ratio $(2/3)^2$ = **0.4444**; run time ratio 3/2 = **1.5**.

### Solution 14-01.11

For $N_c$ = 10⁹ cycles, dynamic energy is $\alpha CV^2N_c = 10^{-9} \times 10^9 \times V^2 = V^2$ J, and leakage energy is $VI_{leak}t = V \times 0.5 \times 10^9/(f \times 10^9) = 0.5V/f$ J with $f$ in GHz. So

$$
E(f) = (0.3 + 0.2f)^2 + \frac{0.5(0.3 + 0.2f)}{f}\ \text{J} .
$$

Setting $dE/df = 0.4(0.3 + 0.2f) - 0.15/f^2 = 0$ gives the cubic $0.08f^3 + 0.12f^2 - 0.15 = 0$, whose positive root is $f$ = **0.8864** GHz, at $V$ = **0.4773** V. The minimum energy is **0.4970** J. At 3 GHz (0.9 V), $E$ = 0.81 + 0.15 = **0.96** J, so the energy-optimal point saves **48.23**% of the energy but takes 1.128 s instead of 0.333 s. Below the optimum, leakage over the longer run outweighs the dynamic saving.

### Solution 14-01.12

(a) With leakage power $P_L$ at 0.9 V (current $P_L/0.9$), racing costs $3.888 + P_L \times 1$ J, and the slow run costs $2.7 + (P_L \times 0.75/0.9) \times 1.333 = 2.7 + 1.111P_L$ J. They are equal when $0.1111P_L = 1.188$: racing wins once $P_L$ exceeds **10.69** W, far above the 1.2 W here. (b) A system power $P_s$ adds $P_s \times 1$ J to the race and $P_s \times 1.333$ J to the slow run. Equality: $5.088 + P_s = 4.033 + 1.333P_s$, so racing wins once $P_s$ exceeds **3.164** W. In a phone, whose display and radios can draw that much while a task runs, racing to idle is often the better policy; for a core on its own, DVFS is.

### Solution 14-01.13

(a) A's speed ratios are 100/20 = 5, 200/50 = 4 and 400/200 = 2, with geometric mean $40^{1/3}$ = **3.420**; B's are 4, 5 and 4, with geometric mean $80^{1/3}$ = **4.309**. B/A = **1.260** ($= 2^{1/3}$). (b) Total times: A 270 s, B 165 s, a ratio of **1.636**. (c) Arithmetic means: A **3.667**, B **4.333**, ratio **1.182**. (d) Normalized to A, B's speed ratios are 20/25 = 0.8, 50/40 = 1.25 and 200/100 = 2. Their geometric mean is $2^{1/3}$ = 1.260, the same as in (a); their arithmetic mean is **1.35**, not 1.182. The geometric mean is unchanged by the choice of reference; the arithmetic mean is not, and neither equals the 1.636 that a workload running each benchmark once would see.

### Solution 14-01.14

(a) $S_{scaled} = 0.05 + 0.95 \times 64$ = **60.85**. (b) In units of the 64-processor run time, the serial part takes 0.05 and the parallel part 0.95 × 64 = 60.8 on one processor, so the single-processor serial fraction is $0.05/60.85$ = **0.08217**%. Amdahl's law with $1 - p$ = 0.0008217 gives $S(64) = 1/(0.0008217 + 0.9991783/64)$ = 60.85: the same number, since it is the same problem and the same two run times. The two laws differ only in which machine the "serial fraction" is measured on. (c) $S(128) = 1/(0.0008217 + 0.9991783/128)$ = **115.9** for this problem size.

### Solution 14-01.15

(a) EDP: A = 2 × 1 = **2** J·s, B = 1.2 × 1.5 = **1.8** J·s. ED²P: A = 2 × 1² = **2** J·s², B = 1.2 × 1.5² = **2.7** J·s². B wins EDP, A wins ED²P. (b) Slowing A to 1.5 s scales its energy by $(1/1.5)^2$, to **0.8889** J: less than B's 1.2 J at the same speed. A is the better architecture; B only looked more efficient because it was measured at a slower operating point. ED²P, being invariant to voltage scaling in this model, exposed that.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-01.1a | execution time | 0.8 | s |
| 14-01.1b | IPC | 1.25 | — |
| 14-01.2a | time after "30% faster" | 7.692 | s |
| 14-01.2b | speedup | 1.4286 | — |
| 14-01.2c | percent faster | 42.86 | % |
| 14-01.3a | CPI | 1.8 | — |
| 14-01.3b | time in memory instructions | 50 | % |
| 14-01.4a | speedup of Y over X | 1.026 | — |
| 14-01.4b | gain from the faster clock | 2.6 | % |
| 14-01.5a | speedup, option 1 | 1.4286 | — |
| 14-01.5b | speedup, option 2 | 1.111 | — |
| 14-01.6a | required speedup of the part | 2.25 | — |
| 14-01.6b | ceiling | 2.5 | — |
| 14-01.7a | speedup on 8 processors | 5.926 | — |
| 14-01.7b | efficiency on 8 processors | 74.1 | % |
| 14-01.7c | speedup on 64 processors | 15.42 | — |
| 14-01.7d | efficiency on 64 processors | 24.10 | % |
| 14-01.7e | ceiling | 20 | — |
| 14-01.7f | gain from 8 to 64 processors | 2.6 | — |
| 14-01.8a | total time | 17.5 | s |
| 14-01.8b | true average rate | 171.4 | MFLOPS |
| 14-01.8c | arithmetic mean of rates | 233.3 | MFLOPS |
| 14-01.9a | power at 0.8 V, 2 GHz | 0.64 | W |
| 14-01.9b | energy per operation at 0.8 V | 0.32 | nJ |
| 14-01.9c | power at 0.6 V, 1.5 GHz | 0.27 | W |
| 14-01.9d | energy per operation at 0.6 V | 0.18 | nJ |
| 14-01.9e | energy ratio | 0.5625 | — |
| 14-01.10a | power ratio | 0.2963 | — |
| 14-01.10b | energy-per-operation ratio | 0.4444 | — |
| 14-01.10c | run-time ratio | 1.5 | — |
| 14-01.11a | energy-optimal frequency | 0.8864 | GHz |
| 14-01.11b | voltage there | 0.4773 | V |
| 14-01.11c | minimum energy | 0.4970 | J |
| 14-01.11d | energy at 3 GHz | 0.96 | J |
| 14-01.11e | energy saved | 48.23 | % |
| 14-01.11f | run time at the optimum | 1.128 | s |
| 14-01.12a | leakage for racing to win | 10.69 | W |
| 14-01.12b | system power for racing to win | 3.164 | W |
| 14-01.13a | A's geometric mean | 3.420 | — |
| 14-01.13b | B's geometric mean | 4.309 | — |
| 14-01.13c | ratio of geometric means | 1.260 | — |
| 14-01.13d | ratio of total times | 1.636 | — |
| 14-01.13e | A's arithmetic mean | 3.667 | — |
| 14-01.13f | B's arithmetic mean | 4.333 | — |
| 14-01.13g | ratio of arithmetic means | 1.182 | — |
| 14-01.13h | arithmetic mean with A as reference | 1.35 | — |
| 14-01.14a | scaled speedup | 60.85 | — |
| 14-01.14b | single-processor serial fraction | 0.08217 | % |
| 14-01.14c | speedup on 128 processors | 115.9 | — |
| 14-01.15a | EDP of A | 2 | J·s |
| 14-01.15b | EDP of B | 1.8 | J·s |
| 14-01.15c | ED²P of A | 2 | J·s² |
| 14-01.15d | ED²P of B | 2.7 | J·s² |
| 14-01.15e | A's energy at 1.5 s | 0.8889 | J |
