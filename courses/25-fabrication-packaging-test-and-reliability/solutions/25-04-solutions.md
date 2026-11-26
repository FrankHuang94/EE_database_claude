# Solutions 25-04 · Yield Models and Die Cost

Problems: [25-04 problems](../problems/25-04-problems.md) · Chapter: [25-04](../chapters/25-04-yield-and-die-cost.md)

Every number is recomputed by [verify_25_04.py](../verify/verify_25_04.py).

---

## Solutions

### Solution 25-04.1

(a) $e^{-0.1}$ = **0.905**.

(b) $e^{-0.8}$ = **0.449**. Eight times the area costs half the yield.

### Solution 25-04.2

(a) The triangular density is $f(D) = D/D_0^2$ on $[0, D_0]$ and $(2D_0 - D)/D_0^2$ on $[D_0, 2D_0]$. Write $x = AD_0$ and $u = D/D_0$, so $AD = xu$ and $f(D)\,dD = g(u)\,du$ with $g(u) = u$ on $[0, 1]$ and $2 - u$ on $[1, 2]$. Then

$$
Y = \int_0^1 u\,e^{-xu}\,du + \int_1^2 (2 - u)\,e^{-xu}\,du .
$$

The triangle is the convolution of two uniform densities on $[0, 1]$, so $g(u) = \int_0^1\!\int_0^1 \delta(u - s - t)\,ds\,dt$, and

$$
Y = \int_0^1\!\!\int_0^1 e^{-x(s + t)}\,ds\,dt = \left(\int_0^1 e^{-xs}\,ds\right)^2 = \left(\frac{1 - e^{-x}}{x}\right)^2 .
$$

(b) $(1 - e^{-2})/2$ = **0.432**, squared **0.187**.

### Solution 25-04.3

Seeds: $1/(1 + 2)$ = **0.333**. Negative binomial ($\alpha$ = 3): $(5/3)^{-3}$ = **0.216**. Poisson: $e^{-2}$ = **0.135**. At this die size the model choice changes the yield 2.5-fold.

### Solution 25-04.4

$A$ = 750 mm²: $70{,}686/750$ = **94.2** minus $\pi \times 300/\sqrt{1500}$ = **24.3**, giving **69.9**, about 69 whole dies.

### Solution 25-04.5

(a) $(1 + 0.75/3)^{-3}$ = **0.512**.

(b) $69.9 \times 0.512$ = **35.8**.

(c) $30{,}000/35.8$ = **$838**.

### Solution 25-04.6

(a) $187.5 \times 1.1$ = **206** mm² (206.25).

(b) $70{,}686/206.25 - \pi \times 300/\sqrt{412.5}$ = **296**.

(c) $(1 + 0.206/3)^{-3}$ = **0.819**.

(d) $30{,}000/(296 \times 0.819)$ = **$124**.

(e) Four chiplets cost **$494** of silicon against $838 monolithic, so the chiplet version can absorb up to **$344** of extra packaging, assembly and test cost per product, less any yield loss in assembly. Known-good-die testing (25-07) matters: assembling an untested bad chiplet wastes the other three.

### Solution 25-04.7

(a) $e^{-0.2}$ = **0.819**.

(b) $e^{-0.2}(1 + 0.2 + 0.2^2/2)$ = **0.9989**. Repair turns an 82% array yield into almost 100%, which is why every large memory carries spares.

### Solution 25-04.8

(a) $0.95 \times 0.97^{16}$ = **0.584**.

(b) $0.95 \times (0.614 + 16 \times 0.97^{15} \times 0.03)$ = $0.95 \times (0.614 + 0.304)$ = **0.872**.

### Solution 25-04.9

The target density is still 0.232 cm⁻², now reached when $0.42\,e^{-t/3} = 0.152$: **3.1** months. Halving the learning time halves the wait; this is the value of high wafer volume and many designs early in a ramp.

### Solution 25-04.10

(a) $20 \times 10^9/(5 \times 6.0 \times 10^5)$ = **$6,667**.

(b) $6{,}667/20{,}000$ = **33**%.

### Solution 25-04.11

**1.5**×, against the 1.15× mixed density TSMC quotes for N2 [R-552].

### Solution 25-04.12

(a) $-\ln 0.5/1.0$ = **0.69** cm⁻².

(b) $3(2^{1/3} - 1)$ = **0.78** cm⁻². The clustered model needs a higher defect density to produce the same yield. Either way, a 50% yield on a 100 mm² die implies a young process.

### Solution 25-04.13

(a) $0.3 \times 0.3 + 0.2 \times 0.5 + 0.4 \times 0.2$ = **0.27**.

(b) $e^{-0.27}$ = **0.763**.

### Solution 25-04.14

(a) $e^{-0.15}$ = **0.861**.

(b) $0.72/0.861$ = **0.837**. About a sixth of the dies fail for reasons random defects do not explain: a design-process interaction or a parametric problem worth a separate investigation.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-04.1a | yield, 0.5 cm² | 0.905 | |
| 25-04.1b | yield, 4 cm² | 0.449 | |
| 25-04.2b0 | (1 - e^-2)/2 | 0.432 | |
| 25-04.2b | Murphy yield at 2 | 0.187 | |
| 25-04.3a | Seeds | 0.333 | |
| 25-04.3b | negative binomial a=3 | 0.216 | |
| 25-04.3c | Poisson | 0.135 | |
| 25-04.3d | spread | 2.5 | |
| 25-04.4a | area term | 94.2 | |
| 25-04.4b | edge term | 24.3 | |
| 25-04.4c | dies per wafer | 69.9 | |
| 25-04.5a | yield | 0.512 | |
| 25-04.5b | good dies | 35.8 | |
| 25-04.5c | cost per good die | 838 | $ |
| 25-04.6a | chiplet area | 206 | mm² |
| 25-04.6b | chiplets per wafer | 296 | |
| 25-04.6c | chiplet yield | 0.819 | |
| 25-04.6d | cost per good chiplet | 124 | $ |
| 25-04.6e | silicon cost of four chiplets | 494 | $ |
| 25-04.6e1 | absorbable packaging cost | 344 | $ |
| 25-04.7a | array yield without repair | 0.819 | |
| 25-04.7b | array yield with repair | 0.9989 | |
| 25-04.8a | all 16 cores good | 0.584 | |
| 25-04.8b0 | core term, all good | 0.614 | |
| 25-04.8b1 | core term, one bad | 0.304 | |
| 25-04.8b | at least 15 good | 0.872 | |
| 25-04.9a | month for 80% | 3.1 | months |
| 25-04.10a | depreciation per wafer | 6667 | $ |
| 25-04.10b | share of price | 33 | % |
| 25-04.11a | break-even density gain | 1.5 | |
| 25-04.12a | Poisson defect density | 0.69 | cm⁻² |
| 25-04.12b | negative-binomial defect density | 0.78 | cm⁻² |
| 25-04.13a | expected killer defects | 0.27 | |
| 25-04.13b | yield | 0.763 | |
| 25-04.14a | random-defect yield | 0.861 | |
| 25-04.14b | systematic yield | 0.837 | |
