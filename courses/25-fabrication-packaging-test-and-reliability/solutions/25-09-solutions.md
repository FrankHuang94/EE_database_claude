# Solutions 25-09 · Reliability Physics

Problems: [25-09 problems](../problems/25-09-problems.md) · Chapter: [25-09](../chapters/25-09-reliability-physics.md)

Every number is recomputed by [verify_25_09.py](../verify/verify_25_09.py).

---

## Solutions

### Solution 25-09.1

$AF = \exp[(E_a/k)(1/358.15 - 1/423.15)]$: (a) **32.6**; (b) **145**. The higher activation energy gives over four times more acceleration from the same 65 K.

### Solution 25-09.2

(a) $AF_T(110 \to 300\ °\text{C}) \times (5/0.5)^2$ = **8.40e5**.

(b) $200 \times 8.40 \times 10^5$ = **1.68e8** h = **1.92e4** years.

(c) For a lognormal life, $\ln t$ is Gaussian with standard deviation σ, so the time at failure fraction $F$ is $t_{50}e^{z_F\sigma}$ with $z_F = \Phi^{-1}(F)$. For $F = 10^{-4}$, $z$ = **−3.72**, the factor is $e^{-3.72 \times 0.4}$ = **0.226**, and the time is **4.33e3** years. The ppm-level life is a quarter of the median, and a chip has many such lines.

### Solution 25-09.3

(a) $\ln MTTF = \ln(Bj^{-2} + Cj^{-1})$, so $d\ln MTTF/d\ln j = j\,(-2Bj^{-3} - Cj^{-2})/(Bj^{-2} + Cj^{-1})$, and $n = -d\ln MTTF/d\ln j = (2Bj^{-2} + Cj^{-1})/(Bj^{-2} + Cj^{-1})$. Dividing through by $Cj^{-1}$ and writing $x = jC/B = j/j^*$ gives $n = (2 + x)/(1 + x)$.

(b) $(2 + x)/(1 + x) = 1.25$ gives $x$ = **3**. (c) $1.75$ gives $x$ = **0.333**. The exponent spans most of its range within one decade of $j$ around $j^*$.

### Solution 25-09.4

$3000/(8 \times 10^{-4})$ A/cm² = **3.75** MA/cm², **3.75** times the long-line limit.

### Solution 25-09.5

(a) $\gamma = \ln 100/2$ = **2.30** (MV/cm)⁻¹. (b) $G = \ln 100/(1/8 - 1/10)$ = **184** MV/cm. (c) $m = \ln 100/\ln 1.25$ = **20.6**.

(d) E: $10e^{2.303 \times 5}$ = **1.0e6** s; power law: $10 \times 2^{20.64}$ = **1.63e7** s; 1/E: $10e^{184.2(0.2 - 0.1)}$ = **1.0e9** s. These span three decades; Example 25-09.4's narrower-range data, extrapolated to the same 5 MV/cm, span four (its 1/E model gives **1.0e10** s). Data over a wider field range narrow the spread, which is why reliability engineers push stress fields as low as test time allows.

### Solution 25-09.6

(a) $1000^{-1/1.2} \times (10^{-4})^{1/1.2}$ = **1.47e-6** (using $-\ln(1 - 10^{-4}) \approx 10^{-4}$; the verify script uses the exact value).

(b) $3.156 \times 10^8/1.47 \times 10^{-6}$ = **2.15e14** s.

(c) Only the 1/E extrapolation (10²² s) passes; the power law (2.67 × 10¹² s) now fails. A shallower Weibull slope, typical of thinner oxides, can turn a pass into a fail without any change in the median data.

### Solution 25-09.7

$3 \times 100^{1/6}$ = **6.46** mV and $3 \times 100^{1/4}$ = **9.49** mV. A test spanning more decades of time separates the exponents by a measurable margin (3 mV), so the end-of-life extrapolation rests on less.

### Solution 25-09.8

(a) $(4000 - 5)/1501$ = **2.66** A. (b) $5 + 2.66$ = **7.66** V, just inside 8 V. (c) $R_{on} \le (3 \times 1500)/(4000 - 5 - 3)$ = **1.13** Ω: doubling the zap voltage halves the allowed on-resistance, so the clamp's width roughly doubles.

### Solution 25-09.9

(a) $5 \times 0.5$ = **2.5** > 1: it can latch. (b) Each gain must fall by $\sqrt{2.5}$ = **1.58**. In practice the shunt resistances of well and substrate taps divert base current, lowering the effective gains far more than this.

### Solution 25-09.10

(a) $\chi^2_{0.60,\,4}$ = **4.045**; $4.045 \times 10^9/(2 \times 1000 \times 7859 \times 78.6)$ = **3.27** FIT.

(b) $\chi^2_{0.90,\,2}$ = **4.605**; **3.73** FIT. One failure more than doubles the bound; higher confidence raises it by a similar factor.

### Solution 25-09.11

$N = 1.833/(2 \times 1000 \times 78.6 \times 10^{-8})$ = 1165.8, so **1166** units.

### Solution 25-09.12

Total **224** FIT; single-$E_a$ estimate **158** FIT; underestimate **29**%. The error grows with the distance from the reference temperature.

### Solution 25-09.13

The number of failures is Poisson with mean $\lambda NtAF$. At the bound, $\lambda NtAF = \chi^2/2$ = 0.916, so (a) $P(0) = e^{-0.916}$ = **0.40**. (b) At half the bound, $e^{-0.458}$ = **0.632**. A product with exactly the claimed rate passes 40% of the time; 60% confidence is not a strong statement.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-09.1a | AF, 0.7 eV | 32.6 | |
| 25-09.1b | AF, 1.0 eV | 145 | |
| 25-09.2a | total AF | 8.40e5 | |
| 25-09.2b | use median | 1.68e8 | h |
| 25-09.2b1 | use median | 1.92e4 | years |
| 25-09.2c0 | z at 1e-4 | -3.72 | |
| 25-09.2c1 | lognormal factor | 0.226 | |
| 25-09.2c | time to 0.01% | 4.33e3 | years |
| 25-09.3b | x for n = 1.25 | 3 | |
| 25-09.3c | x for n = 1.75 | 0.333 | |
| 25-09.4a | stub current density | 3.75 | MA/cm² |
| 25-09.4b | ratio to long-line limit | 3.75 | |
| 25-09.5a | gamma | 2.30 | cm/MV |
| 25-09.5b | G | 184 | MV/cm |
| 25-09.5c | m | 20.6 | |
| 25-09.5d | E-model life | 1.0e6 | s |
| 25-09.5d1 | power-law life | 1.63e7 | s |
| 25-09.5d2 | 1/E life | 1.0e9 | s |
| 25-09.5e | Example 4 1/E life at 5 MV/cm | 1.0e10 | s |
| 25-09.6a | scale factor | 1.47e-6 | |
| 25-09.6b | required characteristic life | 2.15e14 | s |
| 25-09.7a | shift at 1e5 s, 1/6 | 6.46 | mV |
| 25-09.7b | shift at 1e5 s, 1/4 | 9.49 | mV |
| 25-09.7c | separation | 3 | mV |
| 25-09.8a | peak current | 2.66 | A |
| 25-09.8b | pad voltage | 7.66 | V |
| 25-09.8c | largest on-resistance | 1.13 | Ω |
| 25-09.9a | loop gain | 2.5 | |
| 25-09.9b | gain reduction factor | 1.58 | |
| 25-09.10a0 | chi-square, 60%, 4 dof | 4.045 | |
| 25-09.10a | FIT, one failure | 3.27 | FIT |
| 25-09.10b0 | chi-square, 90%, 2 dof | 4.605 | |
| 25-09.10b | FIT, 90% | 3.73 | FIT |
| 25-09.11a | units needed | 1166 | |
| 25-09.12a | total at 105 °C | 224 | FIT |
| 25-09.12b | single-Ea estimate | 158 | FIT |
| 25-09.12c | underestimate | 29 | % |
| 25-09.13a | pass probability at bound | 0.40 | |
| 25-09.13a0 | Poisson mean at bound | 0.916 | |
| 25-09.13b | pass probability at half | 0.632 | |
