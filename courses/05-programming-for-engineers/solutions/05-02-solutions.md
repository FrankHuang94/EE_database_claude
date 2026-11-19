# Solutions 05-02 · NumPy, Vectorization and Numerical Computing

Problems: [05-02 problems](../problems/05-02-problems.md) · Chapter: [05-02](../chapters/05-02-numpy-and-vectorization.md). Every code block below is run by [verify_05_02.py](../verify/verify_05_02.py), which checks that it prints exactly what is shown and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-02.1

```python
import math
import warnings
import numpy as np

print(np.linspace(0, 1, 11)[1], np.arange(0, 1, 0.1).size, np.zeros((3, 4)).size)
```

```text
0.1 10 12
```

(a) Eleven points from 0 to 1 inclusive have **0.1** spacing. (b) `arange` stops *before* 1, giving **10** elements. (c) A 3 × 4 array has **12**. `linspace` fixes the number of points and includes both ends; `arange` with a float step decides whether to include the end by comparing accumulated floats, so rounding can add or drop a point unexpectedly.

### Solution 05-02.2

```python
for a, b in [((4, 1), (3,)), ((2, 3), (2,)), ((2, 3), (2, 1)), ((5,), (1, 5))]:
    try:
        print(a, b, "->", (np.ones(a) + np.ones(b)).shape)
    except ValueError:
        print(a, b, "-> error")
```

```text
(4, 1) (3,) -> (4, 3)
(2, 3) (2,) -> error
(2, 3) (2, 1) -> (2, 3)
(5,) (1, 5) -> (1, 5)
```

Compare trailing axes: (a) 1 stretches to 3 and the missing leading axis to 4, giving `(4, 3)`, **12** elements; (b) error, because the trailing sizes 3 and 2 differ; (c) `(2, 3)`, the size-1 axis stretching; (d) `(1, 5)`.

### Solution 05-02.3

```python
with warnings.catch_warnings():
    warnings.simplefilter("ignore")            # NumPy warns about scalar overflow; the result is the point
    print(np.uint8(250) + np.uint8(10), np.int8(127) + np.int8(1))
```

```text
4 -128
```

`uint8` holds 0 to 255, so 260 wraps to $260 - 256 =$ **4**. `int8` holds −128 to 127, so 128 wraps to **−128**: in two's complement (05-07) the bit pattern 1000 0000 is −128. NumPy warns for scalar overflow but not, by default, for array overflow, which is why such bugs go unnoticed.

### Solution 05-02.4

```python
t = np.linspace(0, 1, 10_000, endpoint=False)
tri = 1 - 4 * np.abs(t - 0.5)                  # rises from -1 to +1 and back over one period
rms = float(np.sqrt(np.mean(tri ** 2)))
print(f"{rms:.4f} {1 / math.sqrt(3):.4f} {np.abs(tri).max() / rms:.4f} {math.sqrt(3):.4f}")
```

```text
0.5774 0.5774 1.7321 1.7321
```

RMS **0.5774** and crest factor **1.732**, matching $1/\sqrt3$ and $\sqrt3$ to four figures. (A square wave has crest factor 1 and a sine $\sqrt2$; the crest factor tells you how much headroom a signal needs above its RMS level, which matters for amplifiers and ADCs.)

### Solution 05-02.5

```python
from statistics import NormalDist

rng = np.random.default_rng(7)
leak = rng.normal(10.0, 2.0, 5_000)                 # microamperes
q2 = 1 - NormalDist().cdf(2.0)
print(int((leak > 14.0).sum()), f"{q2:.5f}", f"{5_000 * q2:.1f}")
```

```text
118 0.02275 113.8
```

**118** devices exceed 14 µA, against an expected **113.8** ($5000\times Q(2)$, with $Q(2)$ = **0.02275**). The standard deviation of such a count is about $\sqrt{113.8} \approx 10.7$ (03-02's Poisson approximation), so 118 is well within chance.

### Solution 05-02.6

```python
x = np.arange(6.0)
x[1:4] *= 2
y = np.arange(6.0)
y[[1, 2, 3]] *= 2
print(x, x.sum(), np.array_equal(x, y))
```

```text
[0. 2. 4. 6. 4. 5.] 21.0 True
```

`x` becomes `[0, 2, 4, 6, 4, 5]`, sum **21.0**. The index-array version gives the same result: augmented assignment (`*=`) on an indexed selection writes back into the original even though plain index-array *selection* returns a copy. The difference matters when you assign the selection to a new name and modify that.

### Solution 05-02.7

```python
a = np.full(1_000_000, 0.1, dtype=np.float32)
s = np.float32(0.0)
for value in a:
    s += value
print(f"{float(s):.2f} {float(a.sum()):.2f} {math.fsum(a.astype(np.float64)):.5f} {float(np.float32(0.1)):.10f}")
```

```text
100958.34 100000.01 100000.00149 0.1000000015
```

(a) The loop gives **100958.34**, almost 1% high: once the float32 total reaches tens of thousands, the gap between float32 values near it is 0.004–0.008, so each addition of 0.1 is rounded by up to half a gap, 2–4% of the addend. Within one binade (a range between consecutive powers of two) the gap is fixed and 0.1 sits at the same position relative to it, so every rounding has the same sign: the errors add coherently instead of cancelling, and accumulate to about 1%. (b) `np.sum` adds pairwise and gives **100000.01**. (c) `math.fsum` gives the exact sum of the stored values, **100000.00149**, which differs from $10^5$ only because float32 stores 0.1 as 0.1000000015. Lesson: accumulate float32 data in float64 (`a.sum(dtype=np.float64)`) or with pairwise or compensated summation.

### Solution 05-02.8

```python
log = np.array([1, 2, np.nan, 4])
print(np.mean(log), f"{np.nanmean(log):.4f}", int(np.count_nonzero(~np.isnan(log))))
```

```text
nan 2.3333 3
```

`np.mean` returns **nan**; `np.nanmean` ignores the gap and returns **2.3333**, from **3** valid entries. Returning NaN by default is the safe behavior: it forces you to notice the missing value and decide whether skipping it is right. A silently skipped reading can bias a result (if, say, the sensor drops out only when hot).

### Solution 05-02.9

```python
f_ratio = np.array([1.0, 10.0])
h = 1 / (1 + 1j * f_ratio)
print(np.round(np.abs(h), 4), np.round(np.degrees(np.angle(h)), 2))
```

```text
[0.7071 0.0995] [-45.   -84.29]
```

At the corner, $|H|$ = **0.7071** (−3 dB) with phase **−45°**; a decade above, $|H|$ = **0.0995** (about −20 dB) with phase **−84.29°**. One complex expression gives the whole frequency response.

### Solution 05-02.10

```python
d = np.array([1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16])
one_pass = np.mean(d ** 2) - np.mean(d) ** 2
two_pass = np.mean((d - d.mean()) ** 2)
print(one_pass, two_pass)
```

```text
-128.0 22.5
```

The one-pass formula gives **−128.0**, an impossible negative variance; the two-pass formula gives the correct **22.5**. The squares are about $10^{18}$, where float64 values are spaced 128 apart, so the subtraction $\overline{x^2} - \bar x^2$ of two nearly equal numbers near $10^{18}$ is pure rounding noise: catastrophic cancellation. Subtracting the mean first works with small numbers. (Statistics libraries use two-pass or Welford's one-pass update for this reason.)

### Solution 05-02.11

```python
a_, b_, c_ = 1.0, -1e8, 1.0
disc = math.sqrt(b_ * b_ - 4 * a_ * c_)
x_large = (-b_ + disc) / (2 * a_)
print(f"{(-b_ - disc) / (2 * a_):.6e} {c_ / (a_ * x_large):.6e}")
```

```text
7.450581e-09 1.000000e-08
```

The textbook formula gives **7.450581×10⁻⁹**, wrong in the first digit; the stable form gives **1.000000×10⁻⁸**, correct. The product of the roots is $c/a = 1$ and the large root is $10^8$, so the small one is $10^{-8}$. In the textbook formula $-b$ and $\sqrt{b^2 - 4ac}$ are both about $10^8$ and nearly equal, so their difference cancels catastrophically; computing the large root (an addition) and dividing avoids any subtraction.

### Solution 05-02.12

```python
t_ms = np.arange(6.0)
v = 5.0 * np.exp(-t_ms / 2.0)
slope, intercept = np.polyfit(t_ms, np.log(v), 1)
print(f"tau {-1 / slope:.4f} ms, v0 {math.exp(intercept):.4f} V")
```

```text
tau 2.0000 ms, v0 5.0000 V
```

$\ln v = \ln v_0 - t/\tau$ is a straight line in $t$, so the slope is $-1/\tau$ and the intercept $\ln v_0$: **τ = 2.0000 ms** and **$v_0$ = 5.0000 V**. With noisy data, fitting $\ln v$ weights the small late samples heavily (a log stretches small values); a direct nonlinear fit (05-03) treats all samples equally.

### Solution 05-02.13

```python
e6 = np.array([1.0, 1.5, 2.2, 3.3, 4.7, 6.8])
r = e6[:, None] * 1e3            # ohms, shape (6, 1)
c = e6[None, :] * 10e-9          # farads, shape (1, 6)
fc = 1 / (2 * np.pi * r * c)     # shape (6, 6)
rows, cols = np.nonzero(np.abs(fc - 1000) / 1000 < 0.05)
for i, j in zip(rows, cols):
    print(f"R = {r[i, 0]:.0f} ohm, C = {c[0, j] * 1e9:.0f} nF, fc = {fc[i, j]:.1f} Hz")
```

```text
R = 3300 ohm, C = 47 nF, fc = 1026.1 Hz
R = 4700 ohm, C = 33 nF, fc = 1026.1 Hz
```

**2** pairs qualify: 3.3 kΩ with 47 nF and 4.7 kΩ with 33 nF, both giving $RC$ = 155.1 µs and **$f_c$ = 1026.1 Hz**, 2.6% high. The target needs $RC = 1/(2\pi\times1000) = 159.2$ µs; E6 is coarse, so tighter targets need E12 or E24 values.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-02.1a | linspace spacing | 0.1 | — |
| 05-02.1b | arange element count | 10 | — |
| 05-02.1c | zeros((3, 4)) size | 12 | — |
| 05-02.2a | elements of the (4, 3) result | 12 | — |
| 05-02.3a | uint8 250 + 10 | 4 | — |
| 05-02.3b | int8 127 + 1 | −128 | — |
| 05-02.4a | triangle RMS | 0.5774 | — |
| 05-02.4b | triangle crest factor | 1.732 | — |
| 05-02.5a | devices above 14 µA | 118 | — |
| 05-02.5b | Q(2) | 0.02275 | — |
| 05-02.5c | expected count | 113.8 | — |
| 05-02.6a | sum after scaling the view | 21.0 | — |
| 05-02.7a | float32 loop sum | 100958.34 | — |
| 05-02.7b | np.sum | 100000.01 | — |
| 05-02.7c | exact sum of stored values | 100000.00149 | — |
| 05-02.8a | nanmean | 2.3333 | — |
| 05-02.8b | valid entries | 3 | — |
| 05-02.9a | magnitude at the corner | 0.7071 | — |
| 05-02.9b | magnitude a decade above | 0.0995 | — |
| 05-02.9c | phase at the corner | −45.00 | ° |
| 05-02.9d | phase a decade above | −84.29 | ° |
| 05-02.10a | one-pass variance | −128.0 | — |
| 05-02.10b | two-pass variance | 22.5 | — |
| 05-02.11a | textbook small root | 7.450581×10^-9 | — |
| 05-02.11b | stable small root | 1.000000×10^-8 | — |
| 05-02.12a | fitted time constant | 2.0000 | ms |
| 05-02.12b | fitted initial voltage | 5.0000 | V |
| 05-02.13a | pairs within 5% | 2 | — |
| 05-02.13b | their corner frequency | 1026.1 | Hz |
