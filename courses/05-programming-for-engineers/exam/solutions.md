# Course 05 · Final Exam — Solutions

Exam: [README.md](README.md). Every code block below is executed by [verify_05_exam.py](../verify/verify_05_exam.py) (C under `-Werror` and the sanitizers), which checks its output exactly and recomputes every number in the answer key independently. On the exam itself none of this code was available; it is here to confirm the hand answers. Each solution names the chapter to revisit if you lost points.

---

**1.** *(05-01)* `b = a` makes `b` a second name for the same list, so `append` changes `a`; `a[:]` copies, so changing `c` leaves `a` alone. Floor division rounds toward −∞.

```python
a = [1, 2, 3]
b = a
b.append(4)
c = a[:]
c[0] = 99
print(a, c, len(a), 7 // 2, -7 // 2, 0.1 + 0.2 == 0.3)
```

```text
[1, 2, 3, 4] [99, 2, 3, 4] 4 3 -4 False
```

`a` is `[1, 2, 3, 4]` (length **4**), `c` is `[99, 2, 3, 4]`, `7 // 2` is **3**, `-7 // 2` is **−4**, and `0.1 + 0.2 == 0.3` is `False` (the sum is 0.30000000000000004).

**2.** *(05-02)* (a) Shapes (3, 1) and (4,) broadcast to (3, 4): **12** elements. (b) `uint8` arithmetic wraps modulo 256: $300 - 256$ = **44** (NumPy also warns about the overflow). (c) Under NEP 50 the Python integer 50 adopts the array's `int8` type, so $100 + 50 = 150$ wraps to $150 - 256$ = **−106**. (d) `float32` has 24 significand bits: $\varepsilon = 2^{-23}$ = **1.19×10⁻⁷**.

```python
import warnings
import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter("ignore", RuntimeWarning)
    s = np.uint8(200) + np.uint8(100)
r = np.ones((3, 1)) + np.arange(4)
print(r.shape, r.size, int(s), int((np.array([100, 100], dtype=np.int8) + 50)[0]), float(np.finfo(np.float32).eps))
```

```text
(3, 4) 12 44 -106 1.1920928955078125e-07
```

**3.** *(05-01, 05-03)* (a) After $n$ steps the bracket is $2^{-n}$ wide; $2^{-n} < 10^{-6}$ needs $n > 19.93$: **20** steps. (b) $x_{k+1} = x_k - (x_k^2 - 2)/(2x_k)$: $x_1$ = **1.500000**, $x_2 = 1.5 - 0.25/3$ = **1.416667**, $x_3$ = **1.414216** (correct to 5 decimals: the number of correct digits roughly doubles each step). (c) With $\bar x = 1.5$ and $\bar y = 4.0$: $S_{xy} = \sum(x - \bar x)(y - \bar y) = 4.5 + 0.55 + 0.55 + 4.5 = 10.1$ and $S_{xx} = 5$, so $m = 10.1/5$ = **2.02** and $b = 4.0 - 2.02 \times 1.5$ = **0.97**.

```python
x = 1.0
for _ in range(3):
    x = x - (x * x - 2) / (2 * x)
    print(f"{x:.6f}")
xs, ys = [0, 1, 2, 3], [1.0, 2.9, 5.1, 7.0]
mx, my = sum(xs) / 4, sum(ys) / 4
m = sum((u - mx) * (w - my) for u, w in zip(xs, ys)) / sum((u - mx) ** 2 for u in xs)
print(f"m = {m:.2f}, b = {my - m * mx:.2f}")
```

```text
1.500000
1.416667
1.414216
m = 2.02, b = 0.97
```

**4.** *(05-04)* (a) Half of 0.01: **0.005**. (b) $P(|Z| > 3) = 2[1 - \Phi(3)]$ = **0.0027**; for 200 tests, $1 - (1 - 0.0027)^{200}$ = **0.418**: such a suite fails spuriously in about two runs out of five. (c) $n \approx \sqrt{2 \times 2^{28} \ln 2}$ ≈ **1.93×10⁴** commits.

**5.** *(05-05)* (a) Truncation toward zero: **−4** and **−1** (check: $(-4)(4) + (-1) = -17$). (b) $2^{32} - 2$ = **4294967294**. (c) Promotion to `int`: **260**; stored in 8 bits: $260 - 256$ = **4**. (d) `1 / 3` is 0 in integers: **0.0**. (e) Truncated: $\lfloor 700 \times 3300/1024 \rfloor = \lfloor 2255.86 \rfloor$ = **2255 mV**; rounded, adding 512 first: **2256 mV**.

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    uint8_t a = 250, b = 10;
    int k = 700;
    printf("%d %d %u %d %d %.1f %d %d\n", -17 / 4, -17 % 4, (unsigned)-2, a + b, (uint8_t)(a + b), 1 / 3 * 3.0,
           k * 3300 / 1024, (k * 3300 + 512) / 1024);
    return 0;
}
```

```text
-4 -1 4294967294 260 4 0.0 2255 2256
```

**6.** *(05-06)* `p` starts at `a[1]`. `*p += 5` makes `a[1]` = **25**. `p[2]` is `a[3]`, set to `*(p - 1) + 1 = a[0] + 1` = **11**. `p++` moves `p` to `a[2]`, so `*p` = **30**. `sizeof a` = $5 \times 4$ = **20** (an array); `sizeof p` = **8** (a pointer); `(a + 4) - p` = $4 - 2$ = **2** elements.

```c
#include <stdio.h>

int main(void)
{
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a + 1;
    *p += 5;
    p[2] = *(p - 1) + 1;
    p++;
    printf("%d %d %d %zu %zu %td\n", a[1], a[3], *p, sizeof a, sizeof p, (a + 4) - p);
    return 0;
}
```

```text
25 11 30 20 8 2
```

**7.** *(05-06)* (a) `a` at 0–1, 2 padding bytes, `b` at **4**–7, `c` at 8, 3 padding bytes: **12** bytes. (b) Order `b, a, c`: 4 + 2 + 1 + 1 padding = **8** bytes; for 2000 records that saves $2000 \times 4$ = **8000** bytes. (c) The full text `V=3.300V` has 8 characters, so `snprintf` returns **8**, which is ≥ 8 and signals truncation; `buf` holds the first **7** characters and the terminator. (d) A **use after free** through a dangling pointer: `realloc` may move the block, after which `first` points to freed memory (05-06, Example 05-06.5). Keep an index instead, or re-derive the pointer after the call.

```c
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

struct rec { uint16_t a; uint32_t b; uint8_t c; };
struct tight { uint32_t b; uint16_t a; uint8_t c; };

int format_volts(char *dst, size_t size, double v) { return snprintf(dst, size, "V=%.3fV", v); }

int main(void)
{
    char buf[8];
    int ret = format_volts(buf, sizeof buf, 3.3);
    printf("%zu %zu %zu %d \"%s\"\n", sizeof(struct rec), offsetof(struct rec, b), sizeof(struct tight), ret, buf);
    return 0;
}
```

```text
12 4 8 8 "V=3.300"
```

**8.** *(05-07)* `0x3A5C` = `0011 1010 0101 1100`. (a) Bits 11:8 are `1010` = **10**. (b) Clear bits 7:4 (`0x3A5C & ~0xF0` = `0x3A0C`) and OR in `0x30`: **`0x3A3C`** = **14908**. (c) `0xE70` = 3696 has bit 11 set, so its value is $3696 - 4096$ = **−400**, and the temperature is $-400 \times 0.0625$ = **−25.0 °C**. (d) Least significant byte first: **`44 33 22 11`**.

```c
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    uint32_t reg = 0x3A5Cu, v = 0x11223344u;
    uint32_t newreg = (reg & ~(0xFu << 4)) | (3u << 4);
    int16_t t = (int16_t)((0xE70u ^ 0x800u) - 0x800u);
    uint8_t bytes[4] = {(uint8_t)v, (uint8_t)(v >> 8), (uint8_t)(v >> 16), (uint8_t)(v >> 24)};
    printf("%u 0x%04X %u %d %.1f %02X %02X %02X %02X\n", (unsigned)((reg >> 8) & 0xFu), (unsigned)newreg, (unsigned)newreg,
           t, t * 0.0625, bytes[0], bytes[1], bytes[2], bytes[3]);
    return 0;
}
```

```text
10 0x3A3C 14908 -400 -25.0 44 33 22 11
```

**9.** *(05-07)* (a) **Derivation.** For an $n$-bit pattern $x$, the complement $\sim x$ has a 1 exactly where $x$ has a 0, so $x + \sim x$ has all $n$ bits set: $x + \sim x = 2^n - 1$. Rearranging, $\sim x + 1 = 2^n - x$. Hardware arithmetic on $n$ bits is modulo $2^n$, and $2^n - x \equiv -x \pmod{2^n}$. In two's complement the pattern congruent to $-x$ modulo $2^n$ *is* the representation of $-x$ (whenever $-x$ is in range, that is for every $x$ except $-2^{n-1}$), so $\sim x + 1$ represents $-x$. (Full marks need the all-ones sum, the modular step, and the range exception.)

(b) $0.6 \times 32768 = 19660.8 \to$ **19661**; $-0.4 \times 32768 = -13107.2 \to$ **−13107**. The product is $-257{,}696{,}727$; adding $2^{14}$ and shifting right by 15 (an arithmetic shift, which rounds toward −∞) gives **−7864**, representing $-7864/32768 = -0.239990$: an error of **9.8×10⁻⁶** (+0.32 of a Q15 step), from rounding both inputs and the product.

(c) $\Delta/\sqrt{12} = 2^{-15}/\sqrt{12}$ = **8.81×10⁻⁶**. Four more bits gain $4 \times 6.02$ = **24.08 dB**.

```c
#include <math.h>
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    int16_t a = (int16_t)lround(0.6 * 32768), b = (int16_t)lround(-0.4 * 32768);
    int32_t prod = (int32_t)a * b;
    int32_t q = (prod + (1 << 14)) >> 15;
    printf("%d %d %ld %ld %.6f %.2e\n", a, b, (long)prod, (long)q, q / 32768.0, q / 32768.0 + 0.24);
    return 0;
}
```

```text
19661 -13107 -257696727 -7864 -0.239990 9.77e-06
```

**10.** *(05-08)* (a) $\lfloor\log_2 5000\rfloor + 1 = 12 + 1$ = **13**. (b) $64\log_2 64$ = **384**. (c) $\lceil\log_2 8!\rceil = \lceil\log_2 40320\rceil = \lceil 15.30\rceil$ = **16**. (d) $(5 - 4294967294) \bmod 2^{32}$ = **7**: the counters wrapped, but unsigned subtraction still gives the count.

**11.** *(05-08)* (a) Key 1 → slot 3 (1 probe); key 2 → 5 (1); key 3, home 3 taken → **4** (2); key 4, home 4 taken, 5 taken → **6** (3); key 5 → 7 (1); key 6, home 7 taken, wraps → **0** (2). Total **10** probes; average **1.67** per successful search. (b) Load factor $6/8 = 0.75$: $\tfrac12(1 + 1/0.25^2)$ = **8.5** probes. (c) 9; 4 rises above 9: `[4, 9]`; 7 stays: `[4, 9, 7]`; 1 enters at index 3, swaps with 9 (index 1), then with 4 (index 0): **`[1, 4, 7, 9]`**.

```python
homes = [3, 5, 3, 4, 7, 7]
slots, placed, probes = [None] * 8, [], 0
for k, h in enumerate(homes, 1):
    i, p = h, 1
    while slots[i] is not None:
        i, p = (i + 1) % 8, p + 1
    slots[i] = k
    placed.append(i)
    probes += p
print(placed, probes, f"{probes / 6:.2f}")
```

```text
[3, 5, 4, 6, 7, 0] 10 1.67
```

**12.** *(05-09)* (a) Decisions: the `for` (1), the `if` (1) and its `&&` (1), and the `else if` (1): $M = 4 + 1$ = **5**. (b) $N + 1$ = **5** tests for 4 conditions (one minimal set is found below). (c) **9, 10, 11, 199, 200, 201** (6 tests). (d) $40 \times 0.5 \times 0.6 \times 0.4$ = **4.8** defects.

```python
from itertools import combinations, product

f = lambda a, b, c, d: a and (b or c) and d
cases = list(product([0, 1], repeat=4))
def ok(s):
    return all(any(all(x[i] == y[i] for i in range(4) if i != k) and x[k] != y[k] and f(*x) != f(*y)
                   for x, y in combinations(s, 2)) for k in range(4))
size = next(n for n in range(1, 17) if any(ok(s) for s in combinations(cases, n)))
print(size, next(s for s in combinations(cases, size) if ok(s)))
```

```text
5 ((0, 0, 1, 1), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1), (1, 1, 0, 1))
```

**13.** *(05-05, 05-06, 05-08)* A single pass tracks the current run's length and counts a run when it ends, including at the end of the array:

```c
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

size_t count_runs(const int16_t *x, size_t n, int16_t thr, size_t min_len)
{
    size_t runs = 0, len = 0;
    for (size_t i = 0; i < n; i++) {
        if (x[i] > thr) {
            len++;
        } else {
            if (len >= min_len && len > 0) runs++;   /* a run just ended */
            len = 0;
        }
    }
    if (len >= min_len && len > 0) runs++;           /* a run that reaches the end of the array */
    return runs;
}

int main(void)
{
    const int16_t x[] = {5, 12, 13, 4, 15, 16, 17, 3, 11, 2, 14, 15};
    printf("%zu %zu\n", count_runs(x, sizeof x / sizeof x[0], 10, 2), count_runs(x, 0, 10, 2));
    return 0;
}
```

```text
3 0
```

Runs above 10: {12, 13} (length 2), {15, 16, 17} (3), {11} (1, too short) and {14, 15} (2, at the very end): **3** qualifying runs. The classic bug is forgetting the final check after the loop, which misses the run that reaches the end of the array and returns **2**; the test data were chosen to end inside a run for exactly that reason. The `len > 0` guard keeps `min_len = 0` from counting empty "runs". The function makes one pass: **$O(n)$** time and $O(1)$ memory. (Grading: correct loop and end-of-array handling 6 points, `const` and `size_t` usage 2, the answer 3 with the bug named 2, Big-O 1; partial credit for a correct algorithm with minor syntax errors.)

**14.** *(05-03)* (a) Trapezoidal rule with $h$ = 1 ms: $h\,[\tfrac12(0) + 2 + 3 + 2 + 1 + \tfrac12(0)] = 8$ mA·ms = **8 µC**. (b) At $V$ = 0.70 V the resistor carries $(5 - 0.70)/1000 = 4.300$ mA but the diode equation demands $10^{-14}e^{0.70/0.025852} = 10^{-14}e^{27.077} = 5.748$ mA, so the residual is **−1.448 mA**, about a third of the current itself: 0.70 V is **not** the operating point (the true root is 0.6925 V, 05-03). Do not trust it. (c) **Always substitute a numerical answer back into the equation it claims to solve**, and check that the residual is small *relative to the problem's scale*. Solvers that stop when successive steps are small (rather than when the function is near zero) can stop at non-roots, as SciPy's secant `newton` did in Lab 05-03; or a user may simply have rounded too coarsely, as here: 0.70 differs from 0.6925 by only 7.5 mV, but the exponential turns that into a 33% current error.

```python
import math

charge = 1e-3 * (0 / 2 + 2 + 3 + 2 + 1 + 0 / 2) * 1e-3          # mA * s -> C
residual = (5 - 0.70) / 1000 - 1e-14 * (math.exp(0.70 / 0.025852) - 1)
print(f"{charge * 1e6:.1f} uC, residual {residual * 1e3:.3f} mA")
```

```text
8.0 uC, residual -1.448 mA
```

**15.** *(05-04 to 05-09)* (a) **Rubric** (2 points per claim, 8 in all; credit for questions that ask for evidence, not reassurance):

| Claim | Probing question | Strong answer contains |
|---|---|---|
| MISRA-compliant | "Which MISRA edition, checked by which tool, and how many deviations do you carry?" | A named edition (2012/2023/2025), a tool, a compliance matrix and a tracked, justified deviation list |
| 100% test coverage | "Which coverage (statement, branch, MC/DC), on which code, and what do the tests assert?" | The metric, the scope (all firmware or only some modules), evidence that tests check outputs, and escaped-defect data |
| Never a memory bug | "How would you know? Do you run sanitizers, fuzzing and static analysis, and what have they found?" | Sanitizer-instrumented host tests, fuzzing of input parsers, static analysis, and a vulnerability-tracking record; "never found" backed by searching |
| Fleet update in an hour | "What happens if an update is bad, or power fails mid-update?" | Signed images, dual-bank (A/B) storage with automatic rollback, staged rollout with monitoring and a halt criterion |

(b) $1 - (1 - 0.002)^{500}$ = **0.632** (about $1 - e^{-1}$, since $500 \times 0.002 = 1$).

(c) A 500-device canary misses a 0.2% defect more than a third of the time (and rarer defects most of the time), so updating the whole fleet within an hour leaves almost no chance to detect a defect before every device has it. The strong practice is staged rollout (canary, then 1%, 10%, 100%) with time at each stage to collect telemetry, and automatic halting and rollback. Fast fleet-wide updates are a valuable capability for urgent security fixes, but as a default they convert every escaped defect into a fleet-wide incident. (4 points for (b) and (c).)

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X05.1a | len(a) | 4 | — |
| X05.1b | 7 // 2 | 3 | — |
| X05.1c | −7 // 2 | −4 | — |
| X05.2a | elements after broadcasting | 12 | — |
| X05.2b | uint8 200 + 100 | 44 | — |
| X05.2c | int8 100 + 50 | −106 | — |
| X05.2d | float32 machine epsilon | 1.19×10^-7 | — |
| X05.3a | bisection steps | 20 | — |
| X05.3b | Newton x₂ | 1.416667 | — |
| X05.3c | Newton x₃ | 1.414216 | — |
| X05.3d | fitted slope | 2.02 | — |
| X05.3e | fitted intercept | 0.97 | — |
| X05.4a | tolerance for 2.50 | 0.005 | — |
| X05.4b | false-failure probability, 3 SE | 0.0027 | — |
| X05.4c | at least one of 200 fails | 0.418 | — |
| X05.4d | commits for 50% short-hash collision | 1.93×10^4 | — |
| X05.5a | −17 / 4 | −4 | — |
| X05.5b | −17 % 4 | −1 | — |
| X05.5c | (unsigned)−2 | 4294967294 | — |
| X05.5d | a + b (uint8_t operands) | 260 | — |
| X05.5e | (uint8_t)(a + b) | 4 | — |
| X05.5f | ADC millivolts, truncated | 2255 | mV |
| X05.5g | ADC millivolts, rounded | 2256 | mV |
| X05.6a | a[1] | 25 | — |
| X05.6b | a[3] | 11 | — |
| X05.6c | *p | 30 | — |
| X05.6d | sizeof a | 20 | bytes |
| X05.6e | (a + 4) − p | 2 | — |
| X05.7a | struct size | 12 | bytes |
| X05.7b | offset of b | 4 | bytes |
| X05.7c | reordered size | 8 | bytes |
| X05.7d | saving for 2000 records | 8000 | bytes |
| X05.7e | snprintf return value | 8 | — |
| X05.8a | bits 11:8 | 10 | — |
| X05.8b | register after the write | 14908 | — |
| X05.8c | signed 12-bit value | −400 | — |
| X05.8d | temperature | −25.0 | °C |
| X05.9a | Q15 of 0.6 | 19661 | — |
| X05.9b | Q15 product | −7864 | — |
| X05.9c | product error | 9.8×10^-6 | — |
| X05.9d | Q15 RMS rounding error | 8.81×10^-6 | — |
| X05.9e | SNR gain, 12 to 16 bits | 24.08 | dB |
| X05.10a | binary-search comparisons, 5000 items | 13 | — |
| X05.10b | T(64) | 384 | — |
| X05.10c | comparison lower bound, 8 items | 16 | — |
| X05.10d | ring-buffer count | 7 | — |
| X05.11a | total probes | 10 | — |
| X05.11b | average successful probes | 1.67 | — |
| X05.11c | predicted unsuccessful probes | 8.5 | — |
| X05.12a | cyclomatic complexity | 5 | — |
| X05.12b | MC/DC tests | 5 | — |
| X05.12c | expected escaped defects | 4.8 | — |
| X05.13a | qualifying runs | 3 | — |
| X05.13b | result with the end-of-array bug | 2 | — |
| X05.14a | charge | 8 | µC |
| X05.14b | residual at 0.70 V | −1.448 | mA |
| X05.15a | canary detection probability | 0.632 | — |
