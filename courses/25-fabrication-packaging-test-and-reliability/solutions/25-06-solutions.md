# Solutions 25-06 · Packaging I: Wire Bond, Flip-Chip, Substrates, SiP and PoP

Problems: [25-06 problems](../problems/25-06-problems.md) · Chapter: [25-06](../chapters/25-06-packaging-fundamentals.md)

Every number is recomputed by [verify_25_06.py](../verify/verify_25_06.py).

---

## Solutions

### Solution 25-06.1

(a) $4 \times 5/0.050$ = **400** pads; $(5/0.130)^2$ = **1.48e3** bumps.

(b) $4 \times 0.130^2/0.050$ = **1.35** mm.

### Solution 25-06.2

$n = \lfloor(150 - 80 - 12)/24\rfloor$ = **2**, so 3 rows per layer and $\lceil 15/3\rceil$ = **5** layers. Smaller pads buy the same layer saving as finer lines.

### Solution 25-06.3

$n = \lfloor(110 - 70 - 10)/20\rfloor$ = **1**: 2 rows per layer, $\lceil 20/2\rceil$ = **10** layers, double Example 25-06.2(b)'s five. A finer bump pitch adds bumps and rows but leaves less room between pads: substrate wiring must shrink with the bump pitch or the layer count explodes, which is what pushes the finest pitches onto silicon interposers (25-07).

### Solution 25-06.4

(a) $1500/0.70$ = **2.14e3** A.

(b) $2.14 \times 10^3/0.2$ = **1.07e4** bumps.

(c) **2.14e4** bumps.

(d) $2.14 \times 10^4 \times 0.130^2$ = **362** mm².

### Solution 25-06.5

$\Delta T$ = 165 K: $\gamma = 13.4 \times 10^{-6} \times 165 \times 10/0.070$ = **0.32**. Strain scales with $\Delta T$, so life falls by $(100/165)^2$ = **0.37**, to about a third. Automotive temperature ranges are a large part of why automotive qualification (25-10) is hard for large flip-chip packages.

### Solution 25-06.6

$\gamma = 13.4 \times 10^{-6} \times 100 \times 14.14/0.070$ = **0.27**; life relative to the midline joint $(10/14.14)^2$ = **0.50**. The true corner lives half as long.

### Solution 25-06.7

$\gamma$ = **0.13**; life gain $(100/70)^2$ = **2.0**.

### Solution 25-06.8

(a) Joints fail independently, so the package survives $N$ cycles only if every joint does:

$$
R_{pkg}(N) = \prod_{i=1}^{M} e^{-(N/\eta_i)^\beta} = \exp\!\Big(-N^\beta\sum_i \eta_i^{-\beta}\Big) = e^{-(N/\eta_{pkg})^\beta},
$$

with $\eta_{pkg} = (\sum_i \eta_i^{-\beta})^{-1/\beta}$: a Weibull distribution with the same shape.

(b) With $M$ equal scales $\eta$: $\eta_{pkg} = \eta\,M^{-1/\beta} = 1000^{-1/4}\,\eta$ = **0.178** $\eta$, more than five times shorter. A steep Weibull (large $\beta$) softens the penalty; scattered lives (small $\beta$) sharpen it.

### Solution 25-06.9

$3 \times 3$ = **9** substrates; area **1.40** times a 110 mm substrate.

### Solution 25-06.10

$(18.54 + 6.32 + 5.00 + 3.32 + 2.28)/41.56$ = **85.3**%.

### Solution 25-06.11

(a) $L = 2$ nH; $V = L \times 8 \times 0.020/(1.0 \times 10^{-9})$ = **0.32** V.

(b) **8.0** mV. A 40-fold reduction: area-array power and ground bumps, many in parallel, are what keep supply noise in hand on fast, wide interfaces.

### Solution 25-06.12

Five layers for 20 rows need 4 rows per layer, so $n \ge 3$ traces between pads: $3w + 4s \le 130 - 80 = 50$ µm. With $w = s$, $7w \le 50$, so $w \le$ **7.14** µm: about 7 µm line and space, finer than most organic substrates in production today, which again points toward silicon interposers or bridges for the densest routing.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-06.1a | peripheral pads | 400 | |
| 25-06.1a1 | area bumps | 1.48e3 | |
| 25-06.1b | crossover die size | 1.35 | mm |
| 25-06.2a | traces between pads | 2 | |
| 25-06.2b | layers | 5 | |
| 25-06.3a | traces between pads | 1 | |
| 25-06.3b | layers | 10 | |
| 25-06.4a | current | 2.14e3 | A |
| 25-06.4b | power bumps | 1.07e4 | |
| 25-06.4c | power and ground bumps | 2.14e4 | |
| 25-06.4d | area | 362 | mm² |
| 25-06.5a | strain, 165 K cycle | 0.32 | |
| 25-06.5b | life ratio | 0.37 | |
| 25-06.6a | diagonal corner strain | 0.27 | |
| 25-06.6b | life ratio | 0.50 | |
| 25-06.7a | strain, 100 µm joint | 0.13 | |
| 25-06.7b | life gain | 2.0 | |
| 25-06.8b | package scale factor | 0.178 | |
| 25-06.9a | 130 mm substrates per panel | 9 | |
| 25-06.9b | area ratio | 1.40 | |
| 25-06.10a | top-five share | 85.3 | % |
| 25-06.11a0 | wire inductance | 2 | nH |
| 25-06.11a | bounce with wire | 0.32 | V |
| 25-06.11b | bounce with bump | 8.0 | mV |
| 25-06.11c | reduction factor | 40 | |
| 25-06.12a | largest line width | 7.14 | µm |
