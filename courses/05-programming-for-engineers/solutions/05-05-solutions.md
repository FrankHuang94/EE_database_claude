# Solutions 05-05 · C Fundamentals

Problems: [05-05 problems](../problems/05-05-problems.md) · Chapter: [05-05](../chapters/05-05-c-fundamentals.md). Every C block below is compiled with `-Wall -Wextra -Wpedantic -Werror` and the address and undefined-behavior sanitizers, and run, by [verify_05_05.py](../verify/verify_05_05.py), which checks that it prints exactly what is shown (or, where stated, that the sanitizer catches it) and recomputes every number in the answer key independently in Python.

---

## Solutions

### Solution 05-05.1

1. **Preprocessor.** `#include "ema.h"` names a file it cannot find: the header is missing, misspelled, or its folder is not on the include path (`-I`).
2. **Compiler.** A syntax error: usually a missing semicolon at the end of the *previous* statement, which the compiler notices only when it reaches `return`.
3. **Linker.** `ema_alpha` was declared (so the call compiled) but no object file passed to the linker defines it: `ema.c` was left out of the build, or the definition's name differs, or it is `static`.
4. **Run time** (reported by UBSan, the undefined-behavior sanitizer). The program computed `INT_MAX + 1` in `int`; without the sanitizer this would silently produce a wrong value.

### Solution 05-05.2

```c
#include <stdio.h>

int main(void)
{
    printf("%d %d %d %d\n", 17 / 5, 17 % 5, -17 / 5, -17 % 5);
    printf("%.1f %d %.1f\n", 17 / 5.0, (int)-3.7, 1 / 2 * 4.0);
    return 0;
}
```

```text
3 2 -3 -2
3.4 -3 0.0
```

(a) **3** and (b) **2**: $3 \times 5 + 2 = 17$. (c) **−3** and (d) **−2**: truncation toward zero, with $(-3)(5) + (-2) = -17$ ✓ (Python would give −4 and 3). (e) **3.4**: one operand is `double`, so the division is floating. (f) **−3**: conversion truncates toward zero, not down. (g) **0.0**: `1 / 2` is evaluated first, in integers, and is 0.

### Solution 05-05.3

(a) **`uint16_t`**: codes 0 to 4095 need 12 bits, and the smallest standard type that holds them is 16 bits; unsigned because a code is never negative.

(b) **`uint32_t`**: register contents are bit patterns, exactly 32 bits, and bit operations on unsigned types are well defined (05-07).

(c) **`int16_t`**: −40.00 °C to +125.00 °C in hundredths is −4000 to 12,500, inside the 16-bit signed range −32,768 to 32,767. Storing scaled integers instead of floats is called fixed point (05-07).

(d) **`uint64_t`**: a year is $3.15\times10^{10}$ ms, more than a 32-bit counter can hold. A `uint32_t` millisecond counter wraps after $2^{32}$ ms $= 4.295\times10^9$ ms $= 4.295\times10^6$ s, which is **49.71 days**: a device that is never restarted meets this within two months (Problem 05-05.11 shows how to make elapsed-time arithmetic survive the wrap).

### Solution 05-05.4

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    uint8_t t = (uint8_t)(200 + 100);
    uint8_t a = 200, b = 100;
    printf("%d %d %d\n", -1 < (int)0u, (int)t, a + b);
    printf("%d %d\n", -1 < (int)sizeof(int), (size_t)-1 < sizeof(int));
    return 0;
}
```

```text
1 44 300
1 0
```

(a) Written as `-1 < 0u`, the comparison converts −1 to `unsigned`, giving $2^{32} - 1$, so the result is **0** (false); the program shows the corrected signed comparison, which is true (1). (b) $300 \bmod 256$ = **44**: the `int` 300 is reduced when stored in 8 bits (without the explicit cast, GCC warns, even without `-Wall`, that the conversion changes the value from 300 to 44). (c) **300**: both operands are promoted to `int` before adding. (d) `sizeof` has the unsigned type `size_t`, so `-1 < sizeof(int)` compares $2^{64} - 1$ (for a 64-bit `size_t`) with 4 and is false; the program prints that comparison with the conversion made explicit, `(size_t)-1 < sizeof(int)`, because `-Wextra` rejects the implicit mixed-sign comparison. Casting `sizeof` to `int` gives the intended true.

### Solution 05-05.5

(a) Exactly, $700 \times 5000/1024$ = **3417.97 mV**.

```c
#include <stdio.h>

int main(void)
{
    int k = 700;
    printf("%d %d %ld\n", k * 5000 / 1024, (k * 5000 + 512) / 1024, 1023L * 5000 + 512);
    return 0;
}
```

```text
3417 3418 5115512
```

(b) Truncating: **3417 mV**. (c) Rounding (add half of 1024): **3418 mV**. (d) The largest intermediate is $1023 \times 5000 + 512$ = **5,115,512**, far above the 32,767 of a 16-bit `int`. On a microcontroller with 16-bit `int`, write `(int32_t)k * 5000`.

### Solution 05-05.6

```c
// file: clamp.h
#ifndef CLAMP_H
#define CLAMP_H

/* Limit x to the closed range [lo, hi]; requires lo <= hi. */
int clamp(int x, int lo, int hi);

#endif /* CLAMP_H */
```

```c
// file: clamp.c
#include "clamp.h"

int clamp(int x, int lo, int hi)
{
    if (x < lo) {
        return lo;
    }
    if (x > hi) {
        return hi;
    }
    return x;
}
```

```c
// with: clamp.c
#include <stdio.h>
#include "clamp.h"
#include "clamp.h"                             /* a second include is harmless: the guard skips it */

int main(void)
{
    printf("%d %d %d\n", clamp(-5, 0, 255), clamp(50, 0, 255), clamp(500, 0, 255));
    return 0;
}
```

```text
0 50 255
```

The results are **0, 50 and 255**. The include guard defines `CLAMP_H` the first time the header is read; on any later inclusion in the same translation unit, `#ifndef CLAMP_H` is false and the contents are skipped. Without it, a header that defines types (05-06) would cause "redefinition" errors when included twice, which happens easily through nested includes.

### Solution 05-05.7

Textual substitution gives `2 + 1 * 2 + 1 * 2 + 1` = **7** (not 27) and `10 + 4 / 2` = **12** (not 7).

```c
#include <stdio.h>

#define CUBE_BAD(x) x * x * x
#define HALF_BAD(x) x / 2
#define CUBE(x) ((x) * (x) * (x))
#define HALF(x) ((x) / 2)

static inline int cube(int x) { return x * x * x; }
static inline int half(int x) { return x / 2; }

int main(void)
{
    printf("%d %d\n", CUBE_BAD(2 + 1), HALF_BAD(10 + 4));
    printf("%d %d %d %d\n", CUBE(2 + 1), HALF(10 + 4), cube(2 + 1), half(10 + 4));
    return 0;
}
```

```text
7 12
27 7 27 7
```

Parenthesizing each argument and the whole body gives **27** and **7**. The `static inline` functions give the same results, check their argument types, and evaluate `x` once, so `cube(i++)` increments `i` once, whereas `CUBE(i++)` would modify `i` three times in one expression (undefined behavior).

### Solution 05-05.8

```c
#include <stdio.h>

double running_average(double x)
{
    static double sum = 0.0;                   /* persist between calls */
    static int count = 0;
    sum += x;
    count++;
    return sum / count;
}

int main(void)
{
    double a = running_average(3.0);
    double b = running_average(5.0);
    double c = running_average(10.0);
    printf("%.1f %.1f %.1f\n", a, b, c);
    return 0;
}
```

```text
3.0 4.0 6.0
```

The averages are **3.0**, **4.0** and **6.0**: $3$, $(3+5)/2$, $(3+5+10)/3$. The hidden state makes the function hard to test: its result depends on every earlier call, there is no way to reset it, and tests that call it affect one another. A testable design passes the state in explicitly (a struct holding `sum` and `count`, 05-06), the same reason Example 05-04.1's notebook state was dangerous.

### Solution 05-05.9

$\alpha = 1 - e^{-T_s/\tau} = 1 - e^{-0.25}$ = **0.221199**. The error after $n$ samples is $e^{-0.25n}$; requiring $e^{-0.25n} \le 10^{-3}$ gives $n \ge \ln(1000)/0.25 = 27.63$, so **28 samples** (14 ms, 6.9 time constants).

```c
#include <math.h>
#include <stdio.h>

int main(void)
{
    double alpha = 1.0 - exp(-0.5e-3 / 2e-3), y = 0.0;
    int n = 0;
    while (1.0 - y > 1e-3) {
        y += alpha * (1.0 - y);
        n++;
    }
    printf("alpha = %.6f, %d samples, y = %.5f\n", alpha, n, y);
    return 0;
}
```

```text
alpha = 0.221199, 28 samples, y = 0.99909
```

Settling to 0.1% takes $\ln 1000 \approx 6.9$ time constants for any first-order system, independent of the sample rate; the sample rate only sets how many samples that is.

### Solution 05-05.10

(a) One full-scale square is $(2^{23} - 1)^2$ = 70,368,727,400,449 ≈ $7.04\times10^{13}$, about 33,000 times the `int32_t` maximum of $2^{31} - 1$: **no**, not even one fits.

(b) $\lfloor (2^{63} - 1)/(2^{23} - 1)^2 \rfloor$ = **131,072** squares (just over $2^{17}$, since $(2^{23})^2 = 2^{46}$).

(c) $131{,}072/48{,}000$ = **2.731 s**. A 64-bit accumulator holds under three seconds of full-scale 24-bit audio energy, so a long-term power meter must scale samples down, accumulate in blocks, or use floating point.

(d) Widen *before* multiplying, and check the budget:

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    const int32_t full_scale = (1 << 23) - 1;
    int64_t energy = 0;
    for (int n = 0; n < 131072; n++) {
        energy += (int64_t)full_scale * full_scale;   /* the product is computed in 64 bits */
    }
    printf("%lld %lld\n", (long long)energy, (long long)(INT64_MAX - energy));
    return 0;
}
```

```text
9223369837831651328 2199023124479
```

After 131,072 full-scale samples the accumulator is within $2.2\times10^{12}$ of its limit, far less than one more full-scale square ($7.04\times10^{13}$). Without the cast, `full_scale * full_scale` would be computed in 32-bit `int` and overflow on the first sample.

### Solution 05-05.11

(a) $2^{32}$ ms $= 4{,}294{,}967{,}296$ ms = **49.71 days**.

(b) Unsigned subtraction is arithmetic modulo $2^{32}$, so it "unwraps" automatically:

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    uint32_t start = 4294967000u, end = 704u;
    uint32_t elapsed = end - start;            /* modulo 2^32: correct across one wrap */
    printf("%u ms\n", elapsed);
    return 0;
}
```

```text
1000 ms
```

$704 - 4{,}294{,}967{,}000 \equiv 704 + (2^{32} - 4{,}294{,}967{,}000) = 704 + 296$ = **1000 ms** ✓. This works for any interval shorter than one full wrap (49.7 days), which is why firmware stores tick counts in unsigned types and only ever subtracts them; comparing them directly (`end > start`) fails at the wrap.

(c) With `int32_t`, the counter itself overflows past $2^{31} - 1$, which is undefined behavior, and even on hardware that wraps, the subtraction can overflow again. Signed types are the wrong tool for wrapping counters.

(d) A signed 32-bit counter overflows after $2^{31}$ ticks; with 10 ms ticks that is $2^{31}\times 0.01$ s = 21,474,836 s = **248.55 days**. The FAA's 2015 airworthiness directive for Boeing 787 generator control units states that "a software counter internal to the GCUs ... will overflow after 248 days of continuous power", and required the electrical power to be cycled at least every 120 days ([R-093](../../../reference/research-log.md#r-093--software-failures-from-numeric-conversions-and-counters)). The directive does not state the counter's width or tick period; $2^{31} \times 10$ ms matching 248 days is an inference, consistent but unconfirmed **[Contested]**.

### Solution 05-05.12

(a) $2{,}000{,}000{,}000 + 2{,}000{,}000{,}000 = 4\times10^9 > 2^{31} - 1$: the sum overflows before the division.

```c
// expect: sanitizer
#include <stdio.h>

int avg(int a, int b) { return (a + b) / 2; }

int main(void)
{
    volatile int a = 2000000000, b = 2000000000;
    printf("%d\n", avg(a, b));
    return 0;
}
```

```text
runtime error: signed integer overflow: 2000000000 + 2000000000 cannot be represented in type 'int'
```

(b) For $a = -7$, $b = 2$: $(a + b)/2 = -5/2$ = **−2** (truncation toward zero), but $a + (b - a)/2 = -7 + 9/2 = -7 + 4$ = **−3**. They disagree: the second formula rounds toward $a$, not toward zero. And when $a$ and $b$ have opposite signs and large magnitudes, $b - a$ itself can overflow. "Safe" rewrites need checking too.

(c) Do the arithmetic in a type that cannot overflow; the average of two `int` values always fits back in an `int`:

```c
#include <stdio.h>

int avg(int a, int b) { return (int)(((long long)a + b) / 2); }

int main(void)
{
    printf("%d %d %d\n", avg(2000000000, 2000000000), avg(-7, 2), avg(-2147483647 - 1, 2147483647));
    return 0;
}
```

```text
2000000000 -2 0
```

The results are **2,000,000,000**, **−2** (rounded toward zero, like `(a + b) / 2` wherever that does not overflow) and 0 for the extreme pair $-2^{31}$ and $2^{31} - 1$, whose exact average is −0.5. (`-2147483647 - 1` is how C spells the most negative `int`, because the literal `2147483648` does not fit in `int`.)

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-05.2a | 17 / 5 | 3 | — |
| 05-05.2b | 17 % 5 | 2 | — |
| 05-05.2c | −17 / 5 | −3 | — |
| 05-05.2d | −17 % 5 | −2 | — |
| 05-05.2e | 17 / 5.0 | 3.4 | — |
| 05-05.2f | (int)−3.7 | −3 | — |
| 05-05.2g | 1 / 2 * 4.0 | 0.0 | — |
| 05-05.3a | wrap time of a uint32_t millisecond counter | 49.71 | days |
| 05-05.4b | 300 stored in uint8_t | 44 | — |
| 05-05.4c | uint8_t 200 + 100 | 300 | — |
| 05-05.5a | exact value | 3417.97 | mV |
| 05-05.5b | truncated | 3417 | mV |
| 05-05.5c | rounded | 3418 | mV |
| 05-05.5d | largest intermediate product | 5115512 | — |
| 05-05.6a | clamp(500, 0, 255) | 255 | — |
| 05-05.7a | CUBE_BAD(2 + 1) | 7 | — |
| 05-05.7b | HALF_BAD(10 + 4) | 12 | — |
| 05-05.7c | corrected CUBE(2 + 1) | 27 | — |
| 05-05.8a | third running average | 6.0 | — |
| 05-05.9a | α | 0.221199 | — |
| 05-05.9b | samples to settle within 0.1% | 28 | — |
| 05-05.10a | one full-scale 24-bit square | 7.04×10^13 | — |
| 05-05.10b | full-scale squares in int64_t | 131072 | — |
| 05-05.10c | seconds at 48 kHz | 2.731 | s |
| 05-05.11a | elapsed time across the wrap | 1000 | ms |
| 05-05.11b | overflow time, signed 32-bit, 10 ms ticks | 248.55 | days |
| 05-05.12a | (a + b) / 2 for −7 and 2 | −2 | — |
| 05-05.12b | a + (b − a) / 2 for −7 and 2 | −3 | — |
