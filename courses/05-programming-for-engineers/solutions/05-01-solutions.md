# Solutions 05-01 · Python Fundamentals for Engineers

Problems: [05-01 problems](../problems/05-01-problems.md) · Chapter: [05-01](../chapters/05-01-python-fundamentals.md). Every code block below is run by [verify_05_01.py](../verify/verify_05_01.py), which checks that it prints exactly what is shown and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-01.1

```python
for expr in ('7 / 2', '7 // 2', '7 % 3', '2 ** 10', 'int("42") + 1', 'len("VDD_core")'):
    value = eval(expr)
    print(f"{expr:16} -> {value!r:6} {type(value).__name__}")
```

```text
7 / 2            -> 3.5    float
7 // 2           -> 3      int
7 % 3            -> 1      int
2 ** 10          -> 1024   int
int("42") + 1    -> 43     int
len("VDD_core")  -> 8      int
```

True division always returns a float (**3.5**), even when it divides evenly. Floor division of positive integers is ordinary integer division (**3**), the remainder is **1**, $2^{10}$ = **1024**, `int("42")` converts text before the addition (**43**), and the string has **8** characters. (`eval` evaluates text as code; it is used here only to print each expression beside its value, and should never be applied to untrusted input.)

### Solution 05-01.2

```python
a, b = -17, 5
print(a // b, a % b, (a // b) * b + a % b == a)
q, r = divmod(17, -5)
print(q, r, q * -5 + r == 17)
```

```text
-4 3 True
-4 -3 True
```

$-17/5 = -3.4$ rounds *down* to **−4**, so the remainder is $-17 - (-4)(5) =$ **3**. With a negative divisor, $17/(-5) = -3.4$ again floors to **−4**, and the remainder $17 - (-4)(-5) =$ **−3** takes the divisor's sign. In both cases the identity holds. (C truncates toward zero instead and would give −3 and −2 for the first pair.)

### Solution 05-01.3

```python
from fractions import Fraction

print(f"{0.1 * 3 - 0.3:.4e}", round(2.675, 2), f"{2.675:.20f}")
```

```text
5.5511e-17 2.67 2.67499999999999982236
```

(a) **5.551×10⁻¹⁷**: the same one-step rounding difference as $0.1 + 0.2 - 0.3$ in Example 05-01.2.

(b) The decimal 2.675 has no exact binary form; the nearest float is 2.67499999999999982236…, slightly *below* 2.675, so rounding to two decimals correctly gives **2.67**. `round` is not wrong; the number it was given is not the one written. Where exact decimal rounding matters (money), use `decimal.Decimal("2.675")`.

### Solution 05-01.4

```python
import math

def db_from_voltage_ratio(r):
    """20 log10 of a voltage (amplitude) ratio."""
    if r <= 0:
        raise ValueError("ratio must be positive")
    return 20 * math.log10(r)

def db_from_power_ratio(r):
    """10 log10 of a power ratio."""
    if r <= 0:
        raise ValueError("ratio must be positive")
    return 10 * math.log10(r)

def dbm(p_watts):
    """Power in dBm (decibels relative to 1 mW)."""
    if p_watts <= 0:
        raise ValueError("power must be positive")
    return db_from_power_ratio(p_watts / 1e-3)

print(f"{db_from_voltage_ratio(1000):.2f} {db_from_power_ratio(0.5):.3f} {dbm(1):.2f} {dbm(1e-6):.2f}")
```

```text
60.00 -3.010 30.00 -30.00
```

A voltage ratio of 1000 is **60.00 dB**; halving power is **−3.010 dB**; 1 W is **30.00 dBm** and 1 µW **−30.00 dBm**. Building `dbm` on top of `db_from_power_ratio` keeps the formula in one place.

### Solution 05-01.5

```python
samples = list(range(0, 100, 7))
every_fourth = samples[::4]
print(len(samples), samples[-1], every_fourth, sum(every_fourth))
```

```text
15 98 [0, 28, 56, 84] 168
```

(a) `range(0, 100, 7)` runs 0, 7, …, 98: **15** values. (b) The last is **98**. (c) `[::4]` takes indices 0, 4, 8, 12: `[0, 28, 56, 84]`. (d) Their sum is **168**.

### Solution 05-01.6

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
bad = sum(row.count(1) for row in grid)
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
good = sum(row.count(1) for row in grid)
print(bad, good)
```

```text
3 1
```

(a) **3**: `[[0] * 3] * 3` makes an outer list holding three references to the *same* inner list, so changing "row 0" changes every row. (`[0] * 3` is fine because integers are immutable.) (b) The comprehension evaluates `[0] * 3` afresh for each row, giving three independent lists and **1** one.

### Solution 05-01.7

```python
def log_bad(msg, history=[]):
    history.append(msg)
    return history

def log_good(msg, history=None):
    if history is None:
        history = []
    history.append(msg)
    return history

for m in ("a", "b", "c"):
    bad, good = log_bad(m), log_good(m)
print(len(bad), len(good))
```

```text
3 1
```

The shared default list grows to **3** entries; `log_good` creates a new list each call, so it returns **1**.

### Solution 05-01.8

```python
values = [100, 220, 4700, 1000, 47000, 330, 2200, 10000, 68]
by_decade = {}
for r in values:
    exponent = math.floor(math.log10(r))
    by_decade[exponent] = by_decade.get(exponent, 0) + 1
print(dict(sorted(by_decade.items())), len(by_decade), by_decade[3])
```

```text
{1: 1, 2: 3, 3: 3, 4: 2} 4 3
```

**4** decades appear, and **3** values (1000, 2200, 4700) lie in the $10^3$ decade. `dict.get(key, 0)` supplies 0 the first time a decade is seen. (For exact powers of ten such as 1000, `log10` returns exactly 3.0 here; for values computed from arithmetic, guard against results like 2.9999999999999996 with a small tolerance or integer methods.)

### Solution 05-01.9

```python
def future_value(principal, rate, years, periods_per_year=1):
    """Value after compounding `rate` (a fraction per year) `periods_per_year` times a year."""
    if periods_per_year < 1:
        raise ValueError("need at least one compounding period per year")
    return principal * (1 + rate / periods_per_year) ** (periods_per_year * years)

annual, monthly = future_value(1000, 0.06, 10), future_value(1000, 0.06, 10, 12)
print(f"{annual:.2f} {monthly:.2f} {monthly - annual:.2f}")
```

```text
1790.85 1819.40 28.55
```

Annual compounding gives **1790.85**, monthly **1819.40**, a difference of **28.55**. More frequent compounding approaches a limit, continuous compounding, $1000e^{0.06\times10}$ = **1822.12**: this limit is where the number $e$ comes from.

### Solution 05-01.10

```python
def parse_ohms(text):
    """Convert strings such as '4.7k', '220', '1M', '2.2G' or '10m' to ohms."""
    scale = {"m": 1e-3, "k": 1e3, "M": 1e6, "G": 1e9}
    try:
        if text[-1] in scale:
            return float(text[:-1]) * scale[text[-1]]
        return float(text)
    except (ValueError, IndexError):
        raise ValueError(f"not a resistance: {text!r}") from None

total = sum(parse_ohms(t) for t in ["4.7k", "220", "1M", "68"])
print(round(total))
try:
    parse_ohms("4.7K")
except ValueError as err:
    print("error:", err)
```

```text
1004988
error: not a resistance: '4.7K'
```

The total is **1,004,988 Ω**. `"4.7K"` fails because `K` is not in the table, so `float("4.7K")` raises and the function re-raises a clear message. Rejecting it is deliberate: in SI, lowercase `m` (milli) and uppercase `M` (mega) differ by $10^9$, so a parser should not guess at letter case.

### Solution 05-01.11

```python
def bisect(f, lo, hi, tol=1e-10):
    """Root of f in [lo, hi], where f(lo) and f(hi) have opposite signs."""
    f_lo = f(lo)
    if f_lo * f(hi) > 0:
        raise ValueError("root not bracketed")
    steps = 0
    while hi - lo > tol:
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if f_lo * f_mid <= 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
        steps += 1
    return (lo + hi) / 2, steps

tau = 2e-3
t, steps = bisect(lambda t: 3.3 * math.exp(-t / tau) - 1.8, 0.0, 10e-3, tol=1e-9)
print(f"{t * 1e3:.4f} ms after {steps} halvings; exact {tau * math.log(3.3 / 1.8) * 1e3:.4f} ms")
```

```text
1.2123 ms after 24 halvings; exact 1.2123 ms
```

The voltage reaches 1.8 V at **1.2123 ms**, after **24** halvings: the interval shrinks from $10^{-2}$ s to below $10^{-9}$ s when $2^n > 10^7$, i.e. $n = \lceil\log_2 10^7\rceil = 24$. The exact answer, $\tau\ln(3.3/1.8)$, agrees to the printed digits. Bisection needs only the ability to evaluate the function, not to rearrange the equation.

### Solution 05-01.12

```python
import csv
from pathlib import Path

with Path("temps.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["hour", "temp_c"])
    for hour in range(24):
        writer.writerow([hour, 20 + hour % 12])

with Path("temps.csv").open(newline="") as f:
    temps = [float(rec["temp_c"]) for rec in csv.DictReader(f)]
print(sum(temps) / len(temps), max(temps), sum(1 for t in temps if t > 28))
```

```text
25.5 31.0 6
```

The mean is **25.5 °C** (the values 20 to 31 appear twice each), the maximum **31 °C**, and **6** hours exceed 28 °C (29, 30 and 31, twice each).

### Solution 05-01.13

```python
ones = [bin(x).count("1") for x in range(256)]
print(sum(ones), ones.count(4), math.comb(8, 4))
```

```text
1024 70 70
```

(a) **1024**: each of the 8 bit positions is 1 in exactly half of the 256 numbers, so the total is $8\times128$. (b) **70**: choosing which 4 of 8 positions are 1 gives $\binom84 = 70$ (03-01's counting).

### Solution 05-01.14

```python
rates = range(1, 21)
errors = {p: abs(math.log(2) / math.log(1 + p / 100) - 72 / p) for p in rates}
best = min(errors, key=errors.get)
exact_rate, _ = bisect(lambda p: math.log(2) / math.log(1 + p / 100) - 72 / p, 1.0, 20.0, tol=1e-9)
print(best, f"{errors[best]:.4f}", f"{exact_rate:.3f}")
```

```text
8 0.0065 7.847
```

(a) The rule is most accurate at **8%** (error 0.0065 years). (b) It is exact at **7.847%**. Below that the rule overestimates the doubling time, above it underestimates. (`min(errors, key=errors.get)` returns the key with the smallest value; the bisection reuses the function from Solution 05-01.11 with rates in percent.)

### Solution 05-01.15

(a) Read from the bottom: the exception was raised in **`mean`, line 2**, while dividing by `len(values)`. (b) `len(values)` was 0: one channel's list of samples was **empty** (here `"vbat": []`); `summarize` (line 6) called `mean` for it, called in turn from the top-level `print` on line 10. Nothing is wrong with the arithmetic; the data violated an assumption `mean` never checked. (c) Two fixes: make `mean` reject empty input with a clear message (`if not values: raise ValueError("mean of an empty list")`), or make `summarize` skip or mark channels without data (`None` for an empty channel). For a test-equipment logger the second is usually better: a channel that recorded nothing is a fact worth reporting (perhaps a disconnected probe), and crashing the whole summary would lose the other channels' results. Whichever is chosen, the empty case should be decided deliberately, not left to a `ZeroDivisionError`.

### Solution 05-01.16

(a) On Linux or macOS (on Windows, activate with `.venv\Scripts\activate`):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install numpy
python -m pip freeze > requirements-lock.txt
```

`pip freeze` writes every installed package with its exact version, for example `numpy==2.5.4`. (b) `numpy>=2.0` accepts any version from 2.0 on, so a fresh install gets the newest release; `numpy==2.5.4` installs exactly that version. (c) Minimum versions keep the course current (bug and security fixes, new Python versions) and avoid installation failures when old versions stop being built for new platforms. The risk is that a future NumPy changes printed results: a new release may change a random-number stream, a default or an output format, and an exact printed output in a chapter could then differ on the learner's machine (05-02, 05-04). The course manages the risk by running every published output in CI on every push, so a change in a dependency shows up as a failing check rather than as a silent discrepancy, and a lock file can always pin an exact environment when bit-for-bit reproduction matters.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-01.1a | 7 / 2 | 3.5 | — |
| 05-01.1b | 7 // 2 | 3 | — |
| 05-01.1c | 7 % 3 | 1 | — |
| 05-01.1d | 2 ** 10 | 1024 | — |
| 05-01.1e | int("42") + 1 | 43 | — |
| 05-01.1f | len("VDD_core") | 8 | — |
| 05-01.2a | −17 // 5 | −4 | — |
| 05-01.2b | −17 % 5 | 3 | — |
| 05-01.2c | quotient of divmod(17, −5) | −4 | — |
| 05-01.2d | remainder of divmod(17, −5) | −3 | — |
| 05-01.3a | 0.1 × 3 − 0.3 | 5.551×10^-17 | — |
| 05-01.3b | round(2.675, 2) | 2.67 | — |
| 05-01.4a | voltage ratio 1000 in dB | 60.00 | dB |
| 05-01.4b | power ratio 0.5 in dB | −3.010 | dB |
| 05-01.4c | 1 W | 30.00 | dBm |
| 05-01.4d | 1 µW | −30.00 | dBm |
| 05-01.5a | number of samples | 15 | — |
| 05-01.5b | last sample | 98 | — |
| 05-01.5c | sum of every fourth sample | 168 | — |
| 05-01.6a | ones with the shared-row grid | 3 | — |
| 05-01.6b | ones with independent rows | 1 | — |
| 05-01.7a | log_bad length on the third call | 3 | — |
| 05-01.7b | log_good length on the third call | 1 | — |
| 05-01.8a | decades present | 4 | — |
| 05-01.8b | values in the 10³ decade | 3 | — |
| 05-01.9a | annual compounding | 1790.85 | — |
| 05-01.9b | monthly compounding | 1819.40 | — |
| 05-01.9c | difference | 28.55 | — |
| 05-01.9d | continuous-compounding limit | 1822.12 | — |
| 05-01.10a | total series resistance | 1004988 | Ω |
| 05-01.11a | time to 1.8 V | 1.2123 | ms |
| 05-01.11b | bisection halvings | 24 | — |
| 05-01.12a | mean temperature | 25.5 | °C |
| 05-01.12b | maximum temperature | 31 | °C |
| 05-01.12c | hours above 28 °C | 6 | — |
| 05-01.13a | total set bits, 0 to 255 | 1024 | — |
| 05-01.13b | bytes with four set bits | 70 | — |
| 05-01.14a | most accurate whole-number rate | 8 | % |
| 05-01.14b | rate at which the rule is exact | 7.847 | % |
