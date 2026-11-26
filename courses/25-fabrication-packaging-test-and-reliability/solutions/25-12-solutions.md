# Solutions 25-12 · Post-Silicon Validation and Bring-Up

Problems: [25-12 problems](../problems/25-12-problems.md) · Chapter: [25-12](../chapters/25-12-post-silicon-validation.md)

Every number is recomputed by [verify_25_12.py](../verify/verify_25_12.py).

---

## Solutions

### Solution 25-12.1

$D = 50 \times 10^{-6} \times 2 \times 10^9$ = **1.0e5** entries; $256 \times 10^5$ bits = **3.05** MiB. That is a large on-chip memory just for debug, which is why designs trace selected events rather than raw cycles over long windows.

### Solution 25-12.2

Solving $F_{max}(V) = F$: (a) **0.565** V; (b) **0.841** V. The curve flattens at high voltage, so each extra gigahertz costs more voltage, and power rises as $V^2f$.

### Solution 25-12.3

$m(6)/m(3) = 1 + e^{-3b} = 1.75$, so $e^{-3b} = 0.75$.

(a) $b = -\ln 0.75/3$ = **0.0959** per week. (b) $a = 40/0.25$ = **160**. (c) $160 - 70$ = **90** still hidden. (d) $\ln 10/0.0959$ = **24.0** weeks. A slower discovery rate both raises the estimated total and stretches the schedule.

### Solution 25-12.4

Metal ECO: $2 + 10 \times 2 + 0.2 \times (25 + 20 \times 2)$ = **$35 M**. Full respin: $25 + 40$ = **$65 M**. Break-even: $22 + (1 - p) \times 65 = 65$, $p$ = **0.338**. Cheaper delay makes the mask cost a larger share, but the metal ECO still wins easily.

### Solution 25-12.5

$n = 1 + 1.96^2/(2 \times 0.05^2)$ = **769** parts: halving the tolerance quadruples the sample.

### Solution 25-12.6

46/320 = 14.4%; Wilson interval **11.0**% to **18.6**%, which does not overlap 2026's 3.1–8.0%. Under these assumptions the drop is larger than sampling noise, but the counts, self-selection and the sample mix still limit what it means.

### Solution 25-12.7

(a) $20/650$ = **3.1**% to $40/650$ = **6.2**%. (b) $20/75$ = **27**% to $40/50$ = **80**%. For a large company a mask set is a modest share of the program; for a startup a respin can consume most of its budget.

### Solution 25-12.8

(a) If each remaining bug is found at rate $b$, then $dm/dt = b(a - m)$ with $m(0) = 0$. Separating, $dm/(a - m) = b\,dt$, so $-\ln(a - m) = bt - \ln a$, giving $a - m = ae^{-bt}$ and $m = a(1 - e^{-bt})$.

(b) The remaining bugs halve every $\ln 2/b = \ln 2/0.173$ = **4.0** weeks.

### Solution 25-12.9

Each entry is $256 + 32 = 288$ bits, so $1{,}048{,}576/288$ = **3.64e3** entries. At one entry per 20 cycles they span 72,800 cycles, a window of **36.4** µs: event-driven storage stretches the window about eighteenfold for this activity level.

### Solution 25-12.10

Solving $K(V - 0.33)^{1.3}/V = 2.5$ gives **0.702** V, **51** mV above 0.651 V. Low-temperature corners can set $V_{min}$ in modern processes where threshold voltage rises in the cold, which is why characterization sweeps temperature as well as voltage.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-12.1a | trace depth | 1.0e5 | entries |
| 25-12.1b | storage | 3.05 | MiB |
| 25-12.2a | voltage for 2.0 GHz | 0.565 | V |
| 25-12.2b | voltage for 3.4 GHz | 0.841 | V |
| 25-12.3a | discovery rate | 0.0959 | 1/week |
| 25-12.3b | total bugs | 160 | |
| 25-12.3c | remaining at week 6 | 90 | |
| 25-12.3d | time to 90% | 24.0 | weeks |
| 25-12.4a | metal ECO expected cost | 35 | $M |
| 25-12.4b | full respin cost | 65 | $M |
| 25-12.4c | break-even probability | 0.338 | |
| 25-12.5a | parts for ±5% | 769 | |
| 25-12.6a | Wilson lower, 46/320 | 11.0 | % |
| 25-12.6b | Wilson upper, 46/320 | 18.6 | % |
| 25-12.7a | share of $650 M, low | 3.1 | % |
| 25-12.7a1 | share of $650 M, high | 6.2 | % |
| 25-12.7b | share of startup budget, low | 27 | % |
| 25-12.7b1 | share of startup budget, high | 80 | % |
| 25-12.8b | half-life of remaining bugs | 4.0 | weeks |
| 25-12.9a | entries | 3.64e3 | |
| 25-12.9b | window | 36.4 | µs |
| 25-12.9c | window gain | 18 | |
| 25-12.10a | voltage for 2.5 GHz, cold | 0.702 | V |
| 25-12.10b | increase | 51 | mV |
