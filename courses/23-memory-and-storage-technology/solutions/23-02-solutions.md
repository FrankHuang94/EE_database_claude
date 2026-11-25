# Solutions 23-02 · SRAM Technology

Problems: [23-02 problems](../problems/23-02-problems.md) · Chapter: [23-02](../chapters/23-02-sram-technology.md)

Every number is recomputed by [verify_23_02.py](../verify/verify_23_02.py).

---

## Solutions

### Solution 23-02.1

(a) $1/0.0312$ = **32.1** × 10⁶ bits/mm²; (b) $1/0.024$ = **41.7** × 10⁶ bits/mm²; (c) $1 - 0.024/0.0312$ = **23.1** %. Intel 4's cell shrank 23% in one step; TSMC's high-density cell has not shrunk at all from N5 to N2.

### Solution 23-02.2

(a) $38.1 \times 2^{20}/10^6$ = **39.95** × 10⁶ bits/mm².

(b) $39.95/(1/0.021)$ = **83.9** %. The unit convention alone moves the efficiency noticeably, so compare densities only when both sides use the same megabit.

### Solution 23-02.3

$Q(k) = -\ln 0.999/2^{21}$, so $k$ = **6.12**. A tighter yield target on a smaller array needs about as many sigmas as a looser one on a much larger array.

### Solution 23-02.4

(a) $0.55/1.05 + 0.45/1.7$ = **78.9** % of the old area. (b) The SRAM part is $0.55/1.05$, so its share is $(0.55/1.05)/0.7885$ = **66.4** %. (c) $1/0.7885$ = **1.27** times.

Two thirds of the shrunk die is cache; the next node will help it even less.

### Solution 23-02.5

(a) $(0.8 - 0.32)(1 - 1/\sqrt2)$ = **0.141** V.

(b) With $k_{PD} = 2k_{PG}$, solve $\tfrac12(0.48 - V)^2 = 2\left[0.48V - \tfrac12V^2\right]$, that is $3V^2 - 2.88V + 0.2304 = 0$: $V$ = **0.0881** V. (c) Doubling the pull-down cuts the disturbance by $1 - 0.0881/0.141$ = **37** %, at twice the pull-down's area.

### Solution 23-02.6

(a) $r = \sqrt{120/60} = \sqrt2$, so $V_M = (0.75 - 0.3 + \sqrt2 \times 0.3)/(1 + \sqrt2)$ = **0.362** V.

(b) The pass gate (overdrive 0.45 V) is linear and the pull-up (overdrive 0.45 V) saturated: $120\left[0.45V_w - \tfrac12V_w^2\right] = \tfrac12 \times 60 \times 0.45^2$, so $V_w^2 - 0.9V_w + 0.10125 = 0$ and $V_w$ = **0.132** V.

(c) Raise δ until the written node reaches $V_M$; root finding on the balance gives δ = **85.8** mV.

(d) At δ = 100 mV the pull-up wins, the pass gate saturates and the pull-up is linear: $\tfrac12 \times 120 \times 0.35^2 = 60\left[0.55\,(0.75 - V_w) - \tfrac12(0.75 - V_w)^2\right]$ gives $V_w$ = **0.440** V, so the write fails.

(e) Driving the bitline to **−21.6** mV pulls the node back to $V_M$. This cell is far more writable than the chapter's (its pull-up is half the pass gate's strength), so a small assist covers a large mismatch.

### Solution 23-02.7

(a) $(1024 \times 0.08 + 4)\ \text{fF} \times 80\ \text{mV}/25\ \mu\text{A}$ = **275** ps.

(b) $I = C\Delta V/t = (1024 \times 0.08 + 4)\ \text{fF} \times 80\ \text{mV}/150\ \text{ps}$ = **45.8** µA; (c) **1.83** times the current. That is the kind of gain nanosheets' extra drive has to deliver to keep long bitlines fast.

### Solution 23-02.8

(a) $0.021 + 0.8/128 + 0.0015$ = **0.02875** µm², (b) **34.8** Mb/mm²; (c) $0.021 + 0.8/256 + 0.0015$ = **0.02563** µm², (d) **39.0** Mb/mm²; (e) **12.2** %.

Doubling the bitline helps more here than in Example 23-02.6 because, at 128 cells, the column periphery is a larger share of the area.

### Solution 23-02.9

(a) $Q(k) = -\ln 0.99/2^{28}$: $k$ = **6.51**.

(b) $V_{min} = 0.2 + 6.51 \times 0.5 \times 0.022/0.25$ = **0.486** V.

(c) $0.2 + 4.5 \times 0.5 \times 0.022/0.25$ = **0.398** V. (d) ECC that tolerates one bad bit per word lowers the per-cell requirement by about two sigma, worth **88** mV here.

### Solution 23-02.10

(a) $2^{28} \times 8\ \text{pA}$ = **2.15** mA; (b) × 0.75 V = **1.61** mW.

(c) $2^{-250/90}$ = **0.146**; (d) (a) × (c) = **0.313** mA; (e) × 0.50 V = **0.157** mW; (f) (b)/(e) = **10.3** times.

### Solution 23-02.11

With the wordline at $V_{DD}$, the pass gate (drain at the $V_{DD}$ bitline) is saturated and the pull-down linear. Write $a = V_{DD} - V_{TN}$ and $V$ for the 0 node:

$$
\tfrac12k_{PG}(a - V)^2 = k_{PD}\left(aV - \tfrac12V^2\right) .
$$

Divide by $k_{PG}$ and multiply by 2: $(a - V)^2 = \beta(2aV - V^2)$. Expanding, $(1 + \beta)V^2 - 2a(1 + \beta)V + a^2 = 0$, so $V^2 - 2aV + a^2/(1 + \beta) = 0$ and the smaller root is

$$
V_{rd} = a\left(1 - \sqrt{\frac{\beta}{1 + \beta}}\right) .
$$

For β = 1, $\sqrt{1/2}$ gives §3.4's $a(1 - 1/\sqrt2)$. ✓

(a) **0.117** V; (b) **0.0902** V; (c) **0.0734** V.

(d) $1 - \sqrt{\beta/(1 + \beta)} \le 0.2$ needs $\beta/(1 + \beta) \ge 0.64$, so β ≥ **1.78**. In a FinFET cell, ratios come in whole fins, so the nearest available ratio is 2. A nanosheet cell can be sized at 1.78.

### Solution 23-02.12

(a) $Q(k) = -\ln 0.99/2^{30}$: $k$ = **6.72**; (b) $V_{min} = 0.25 + 6.72 \times 0.6 \times 0.025/0.2$ = **0.754** V.

(c) The array works if $P(\text{Poisson}(\lambda) \le 100) \ge 0.99$; root finding on the Poisson CDF gives λ = **79.1**.

(d) $p = \lambda/N$, so $k = Q^{-1}(79.1/2^{30})$ = **5.26**.

(e) $0.25 + 5.26 \times 0.6 \times 0.025/0.2$ = **0.644** V; (f) **109** mV saved.

(g) Allowing 100 bad cells out of a billion sounds trivial, but it buys **1.5** sigma and over 100 mV of Vmin. That is why every large SRAM has repair.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-02.1a | Intel 7 raw density | 32.1 | 10⁶/mm² |
| 23-02.1b | Intel 4 raw density | 41.7 | 10⁶/mm² |
| 23-02.1c | area shrink | 23.1 | % |
| 23-02.2a | density in decimal megabits | 39.95 | 10⁶/mm² |
| 23-02.2b | array efficiency | 83.9 | % |
| 23-02.3 | sigma for 256 KiB at 99.9% | 6.12 | |
| 23-02.4a | new die area | 78.9 | % |
| 23-02.4b | SRAM share | 66.4 | % |
| 23-02.4c | effective shrink | 1.27 | |
| 23-02.5a | read disturb, β = 1 | 0.141 | V |
| 23-02.5b | read disturb, β = 2 | 0.0881 | V |
| 23-02.5c | disturbance reduction from β = 2 | 37 | % |
| 23-02.6a | switching threshold | 0.362 | V |
| 23-02.6b | written node, nominal | 0.132 | V |
| 23-02.6c | failing mismatch | 85.8 | mV |
| 23-02.6d | written node at 100 mV mismatch | 0.440 | V |
| 23-02.6e | negative bitline needed | -21.6 | mV |
| 23-02.7a | bitline time | 275 | ps |
| 23-02.7b | current for 150 ps | 45.8 | µA |
| 23-02.7c | current ratio | 1.83 | |
| 23-02.8a | area per bit, 128 cells | 0.02875 | µm² |
| 23-02.8b | density, 128 cells | 34.8 | Mb/mm² |
| 23-02.8c | area per bit, 256 cells | 0.02563 | µm² |
| 23-02.8d | density, 256 cells | 39.0 | Mb/mm² |
| 23-02.8e | density gain | 12.2 | % |
| 23-02.9a | sigma for 32 MiB | 6.51 | |
| 23-02.9b | Vmin | 0.486 | V |
| 23-02.9c | Vmin with ECC | 0.398 | V |
| 23-02.9d | Vmin saved by ECC | 88 | mV |
| 23-02.10a | leakage current | 2.15 | mA |
| 23-02.10b | leakage power | 1.61 | mW |
| 23-02.10c | leakage factor | 0.146 | |
| 23-02.10d | retention current | 0.313 | mA |
| 23-02.10e | retention power | 0.157 | mW |
| 23-02.10f | saving | 10.3 | |
| 23-02.11a | read disturb, β = 1 | 0.117 | V |
| 23-02.11b | read disturb, β = 1.5 | 0.0902 | V |
| 23-02.11c | read disturb, β = 2 | 0.0734 | V |
| 23-02.11d | cell ratio for 80 mV | 1.78 | |
| 23-02.12a | sigma without repair | 6.72 | |
| 23-02.12b | Vmin without repair | 0.754 | V |
| 23-02.12c | largest Poisson mean | 79.1 | |
| 23-02.12d | sigma with repair | 5.26 | |
| 23-02.12e | Vmin with repair | 0.644 | V |
| 23-02.12f | Vmin saved | 109 | mV |
| 23-02.12g | sigma saved by repair | 1.5 | |
