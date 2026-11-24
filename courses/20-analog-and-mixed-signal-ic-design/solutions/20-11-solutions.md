# Solutions 20-11 · Layout, Matching and PVT Variation

Problems: [20-11 problem set](../problems/20-11-problems.md) · Chapter: [20-11](../chapters/20-11-layout-matching-pvt.md). Every number below is recomputed by [verify_20_11.py](../verify/verify_20_11.py).

---

## Solutions

### Solution 20-11.1

$2.5\text{ mV·µm}/\sqrt{2\text{ µm}^2}$ = **1.77** mV.

### Solution 20-11.2

σ ∝ $1/\sqrt{\text{area}}$, so a quarter of the mismatch needs $4^2$ = **16** times the area.

### Solution 20-11.3

$\sqrt{(8 \times 0.002)^2 + 0.005^2}$ = **1.68**%: the threshold term (1.6%) dominates.

### Solution 20-11.4

$\sqrt{(2\text{ mV})^2 + (0.005/15\text{ V}^{-1})^2} = \sqrt{2^2 + 0.333^2}$ mV = **2.03** mV.

### Solution 20-11.5

$1.77/\sqrt2$ = **1.25** mV: the pair difference adds the variances of two devices.

### Solution 20-11.6

- AB (centers 5 µm apart): $0.02 \times 5$ = **0.1** mV.
- ABBA, linear: **0**.
- ABBA with the quadratic term: $2g_2p^2 = 2 \times 2 \times 10^{-4} \times 25$ = **0.01** mV.

### Solution 20-11.7

Positions −3.5 to +3.5 pitches; A occupies −3.5, −0.5, 1.5, 2.5 and B occupies −2.5, −1.5, 0.5, 3.5. Average positions: A $(−3.5 − 0.5 + 1.5 + 2.5)/4 = 0$, B $(−2.5 − 1.5 + 0.5 + 3.5)/4 = 0$: difference **0**. Average squares: A $(12.25 + 0.25 + 2.25 + 6.25)/4 = 5.25$, B $(6.25 + 2.25 + 0.25 + 12.25)/4 = 5.25$: difference **0**.

### Solution 20-11.8

2 mV is 2.5σ: $2[1 - \Phi(2.5)]$ = **1.24**% fail.

### Solution 20-11.9

Two bits is a factor of 4 in accuracy; speed × accuracy² / power is fixed, so power grows **16**-fold.

### Solution 20-11.10

$(1 - 0.001)^n \le 0.05$ gives $n \ge$ **2995**; the rule of three gives 3/0.001 = **3000**.

### Solution 20-11.11

$\sqrt{49/\chi^2_{0.975,49}}$ to $\sqrt{49/\chi^2_{0.025,49}}$: **0.835** to **1.246** times the estimate.

### Solution 20-11.12

Trim residual: $0.5/\sqrt{12}$ = **0.144** mV. Drift: $1.2\text{ V} \times 10^{-5}/°\text{C} \times 165\text{ °C}$ = **1.98** mV, fourteen times larger: after trimming, temperature drift sets the accuracy (20-03).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-11.1a | σ(ΔV_T) | 1.77 | mV |
| 20-11.2a | area factor | 16 | — |
| 20-11.3a | mirror σ(ΔI/I) | 1.68 | % |
| 20-11.4a | pair σ(V_os) | 2.03 | mV |
| 20-11.5a | single-device σ | 1.25 | mV |
| 20-11.6a | AB offset | 0.1 | mV |
| 20-11.6b | ABBA linear offset | 0 | mV |
| 20-11.6c | ABBA quadratic residual | 0.01 | mV |
| 20-11.7a | linear difference | 0 | pitch |
| 20-11.7b | quadratic difference | 0 | pitch² |
| 20-11.8a | failure fraction | 1.24 | % |
| 20-11.9a | power factor | 16 | — |
| 20-11.10a | runs, exact | 2995 | — |
| 20-11.10b | runs, rule of three | 3000 | — |
| 20-11.11a | CI low | 0.835 | — |
| 20-11.11b | CI high | 1.246 | — |
| 20-11.12a | trim residual | 0.144 | mV |
| 20-11.12b | drift | 1.98 | mV |
| 20-11.12c | drift to trim ratio | 14 | — |
