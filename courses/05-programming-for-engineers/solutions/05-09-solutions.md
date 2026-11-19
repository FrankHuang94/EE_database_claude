# Solutions 05-09 · Software Engineering Practices

Problems: [05-09 problems](../problems/05-09-problems.md) · Chapter: [05-09](../chapters/05-09-software-engineering-practices.md). Every code block below is run by [verify_05_09.py](../verify/verify_05_09.py), which checks that it prints exactly what is shown and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-09.1

(a) **Functional** and testable as written (check that every stored record has a timestamp; better still, state the timestamp's resolution and time base). (b) **Non-functional** and untestable: rewrite with a measurable bound, for example "The firmware shall process each ADC sample within 50 µs of the conversion-complete interrupt, on the target at 48 MHz." (c) **Non-functional** and testable: a current, a mode and a temperature. (d) **Non-functional** and untestable: rewrite in observable terms, for example "Every public function shall be documented with an example; a new engineer shall complete the getting-started task within 30 minutes in a usability test of five people."

### Solution 05-09.2

(a) **V-model** (possibly with internal iterations): safety-critical, regulated by ISO 26262, needing requirements, traceability and coverage evidence at each level. (b) **Agile** (iterative, with short sprints and continuous deployment): low risk per change, requirements in flux, users available for feedback. (c) **Waterfall/V-model with exhaustive verification:** a mask ROM cannot be patched, so all verification must happen before the irreversible release, like a tape-out. (d) **Continuous delivery with staged rollouts:** a service, frequently updated, where safe releases come from automation, monitoring and the ability to roll back (Problem 05-09.12), and whose integrity matters because it distributes firmware.

### Solution 05-09.3

(a) No decisions: **M = 1**. (b) One `if`: **M = 2**. (c) The `if` (1), its two `and` operators (2 more: three conditions) and the `while` (1): 4 decisions, **M = 5**. (d) The `for` (1) and the `if`/`elif`/`elif` (3; the `else` adds no decision): 4 decisions, **M = 5**.

```python
import ast

def cyclomatic(source):
    d = 0
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.IfExp)):
            d += 1
        elif isinstance(node, ast.BoolOp):
            d += len(node.values) - 1
    return d + 1

bodies = {
    "a": "x = 1\ny = 2\nz = 3\nu = 4\nw = 5\n",
    "b": "if x:\n    y = 1\nelse:\n    y = 2\n",
    "c": "if a and b and c:\n    x = 1\nwhile x < 5:\n    x += 1\n",
    "d": "for v in vals:\n    if v < 0:\n        n = 1\n    elif v < 5:\n        n = 2\n    elif v < 9:\n        n = 3\n    else:\n        n = 4\n",
}
print({k: cyclomatic(src) for k, src in bodies.items()})
```

```text
{'a': 1, 'b': 2, 'c': 5, 'd': 5}
```

### Solution 05-09.4

(a) Channel: **−1, 0, 1, 14, 15, 16**; sample rate: **0, 1, 2, 999, 1000, 1001** Hz. (The out-of-range values −1, 16, 0 and 1001 must be rejected; the others accepted.) (b) **12** single-parameter tests, varying one parameter while the other stays at a nominal valid value (for example channel 7, rate 100 Hz). (c) All combinations: $6 \times 6$ = **36**. Testing each parameter's boundaries separately is the usual compromise; combinations matter only where the parameters interact (for example, if some channels support only lower rates), and then *pairwise* testing, which covers every pair of values at least once, keeps the count manageable.

### Solution 05-09.5

A tracer built on `sys.settrace` records which lines of the function execute:

```python
import sys

def clamp_gain(g):
    if g < 1:
        g = 1
    if g > 16:
        g = 16
    return g

def lines_run(func, *args_list):
    hit = set()
    def tracer(frame, event, arg):
        if frame.f_code is func.__code__ and event == "line":
            hit.add(frame.f_lineno - func.__code__.co_firstlineno)
        return tracer
    sys.settrace(tracer)
    try:
        for args in args_list:
            func(*args)
    finally:
        sys.settrace(None)
    return sorted(hit)

body = [1, 2, 3, 4, 5]                          # line offsets of the five body lines
first = lines_run(clamp_gain, (5,), (20,))
second = lines_run(clamp_gain, (5,), (20,), (0,))
print(first, f"{100 * len(first) / len(body):.0f}%", second, f"{100 * len(second) / len(body):.0f}%")
```

```text
[1, 3, 4, 5] 80% [1, 2, 3, 4, 5] 100%
```

The tests 5 and 20 run 4 of the 5 body lines, **80%**: the assignment `g = 1` never runs, because no test has `g < 1`. Adding `clamp_gain(0)` reaches **100%** line coverage. For branch coverage, each `if` must also be both true and false: `g < 1` is false for 5 and 20 and true for 0; `g > 16` is false for 5 and 0 and true for 20. So the **three** tests {0, 5, 20} give full branch coverage too. Add boundary tests (1, 16, 17) for a test set that also catches off-by-one errors, which coverage alone would not demand.

### Solution 05-09.6

```python
from itertools import combinations, product

def minimal_mcdc(decision, n):
    def ok(tests):
        return all(any(all(a[i] == b[i] for i in range(n) if i != k) and a[k] != b[k] and decision(*a) != decision(*b)
                       for a, b in combinations(tests, 2)) for k in range(n))
    cases = list(product([0, 1], repeat=n))
    for size in range(1, len(cases) + 1):
        for s in combinations(cases, size):
            if ok(s):
                return list(s)

print(minimal_mcdc(lambda a, b: a and b, 2))
print(minimal_mcdc(lambda a, b: a or b, 2))
print(minimal_mcdc(lambda a, b, c: (a and b) or c, 3))
```

```text
[(0, 1), (1, 0), (1, 1)]
[(0, 0), (0, 1), (1, 0)]
[(0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0)]
```

(a) `a and b`: **{(0,1), (1,0), (1,1)}**: (1,1) against (0,1) shows `a` matters, against (1,0) shows `b` matters. (b) `a or b`: **{(0,0), (0,1), (1,0)}**, the mirror image: the base case is (0,0). (c) `(a and b) or c`: **4** tests, e.g. the set printed: (0,1,0) and (1,1,0) for `a`, (1,0,0) and (1,1,0) for `b`, and (0,1,0) and (0,1,1) for `c`. Each case meets the $N + 1$ minimum.

### Solution 05-09.7

(a) $80 \times 0.5^3$ = **10** escapes. (b) Halving to 5 needs $f = 0.0625 = 0.5 \times 0.5 \times (1 - p)$, so $1 - p = 0.25$: one filter must reach **75%**. (c) A fourth filter must satisfy $0.125\,(1 - p_4) = 0.0625$: **50%**, the same as each existing filter. Improving an existing filter from 50% to 75% and adding a new 50% filter have the same effect on paper; in practice the new filter is usually the better buy if it is *different in kind* (for example, static analysis added to tests), because it is less correlated with the existing ones (Example 05-09.4).

### Solution 05-09.8

(a) **2.7.4** (PATCH), (b) **2.8.0** (MINOR, with PATCH reset), (c) **3.0.0** (MAJOR, with MINOR and PATCH reset), because removing a function breaks callers. (d):

```python
versions = ["1.10.0", "1.9.0", "1.2.0", "2.0.0"]
print(sorted(versions))
print(sorted(versions, key=lambda v: tuple(int(x) for x in v.split("."))))
```

```text
['1.10.0', '1.2.0', '1.9.0', '2.0.0']
['1.2.0', '1.9.0', '1.10.0', '2.0.0']
```

As text, "1.10.0" sorts before "1.2.0" and "1.9.0", because the character `1` precedes `2` and `9`. Comparing numeric tuples gives the true order. (Production code should use a version-parsing library, which also handles pre-release tags such as `2.0.0-rc.1`.)

### Solution 05-09.9

```python
traces = {"T1": {"R1"}, "T2": {"R1", "R2"}, "T3": {"R3"}, "T4": {"R3"}, "T5": set(), "T6": {"R2"}}
requirements = {"R1", "R2", "R3", "R4", "R5"}
covered = set().union(*traces.values())
untested = sorted(requirements - covered)
orphans = sorted(t for t, rs in traces.items() if not rs)
print(untested, orphans, f"{100 * len(covered) / len(requirements):.0f}%")
```

```text
['R4', 'R5'] ['T5'] 60%
```

**R4 and R5** have no tests; **T5** traces to no requirement (an orphan: either the requirement it verifies is missing from the specification, or the test is obsolete). Requirement coverage is $3/5$ = **60%**. R1 and R3 have two tests each, which is fine; the matrix's job is to expose the gaps.

### Solution 05-09.10

Requirement: assert after 3 consecutive samples below 3.30 V; deassert at or above 3.40 V; otherwise hold. The consecutive counter resets on any sample not below 3.30 V.

```python
def monitor(samples, reset_on_band=True):
    state, count, history = False, 0, []
    for v in samples:
        if v < 3.30:
            count += 1
            if count >= 3:
                state = True
        else:
            if reset_on_band or v >= 3.40:
                count = 0                      # the buggy version keeps counting through the band
            if v >= 3.40:
                state = False
        history.append(state)
    return history

seq = [3.25, 3.25, 3.31, 3.25, 3.25, 3.25, 3.35, 3.41]
good = monitor(seq)
bad = monitor(seq, reset_on_band=False)
print("asserts at sample", good.index(True) + 1, "clears at sample", len(good) - good[::-1].index(True) + 1)
print("buggy version asserts at sample", bad.index(True) + 1)
```

```text
asserts at sample 6 clears at sample 8
buggy version asserts at sample 4
```

(a) Samples 1 and 2 are low (count 2); sample 3 (3.31 V) is not below 3.30 V, so the count resets; samples 4, 5 and 6 are low, and the alarm **asserts at sample 6**. Sample 7 (3.35 V) is in the hysteresis band: the alarm holds. Sample 8 (3.41 V) **clears it at sample 8**. (b) The buggy version keeps the count through 3.31 V and asserts at sample **4**, after only one sample of the second low run; a test that checks the state after sample 4 (or simply compares the whole history with the expected one) catches it. The requirement's word "consecutive" is exactly what this test pins down.

### Solution 05-09.11

The **Lincoln–Petersen** capture–recapture estimate, borrowed from ecology (estimating fish in a lake by tagging), treats reviewer A's finds as "tagged": B found 15 of A's 25, so B finds about $15/25 = 60\%$ of all defects, and B's 30 defects imply about

$$
\hat N = \frac{n_A\, n_B}{m} = \frac{25 \times 30}{15} = 50
$$

defects in total. Together the reviewers found $25 + 30 - 15 = 40$ distinct defects, so about **10** remain undiscovered: **50** estimated in total.

```python
nA, nB, both = 25, 30, 15
total = nA * nB / both
print(total, total - (nA + nB - both))
```

```text
50.0 10.0
```

Assumptions: the reviewers work independently, and every defect is equally likely to be found by a given reviewer. Both fail in practice: some defects are easy for everyone and some hard for everyone, which inflates the overlap and makes the estimate *too low*. It is a lower-bound-flavored sanity check, not a guarantee.

### Solution 05-09.12

(a) $P(\text{at least one}) = 1 - (1 - 0.001)^{1000}$ = **0.632**: a canary of 1000 devices misses a 0.1% defect more than a third of the time. (b) Require $(0.999)^n \le 0.05$: $n \ge \ln 0.05/\ln 0.999 = 2994.2$, so **2995** devices (about $3/p$, the "rule of three"). (c) A canary only reliably exposes defects whose rate is above roughly $3/n$; rarer defects reach the full fleet. That is why rollouts are staged (1%, 10%, 100%) with monitoring and automatic rollback at each stage, and why field telemetry is part of the test strategy for connected devices.

```python
import math

print(f"{1 - 0.999 ** 1000:.3f} {math.ceil(math.log(0.05) / math.log(0.999))}")
```

```text
0.632 2995
```

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-09.3a | M, function (c) | 5 | — |
| 05-09.3b | M, function (d) | 5 | — |
| 05-09.4a | single-parameter boundary tests | 12 | — |
| 05-09.4b | all combinations | 36 | — |
| 05-09.5a | line coverage of the first two tests | 80 | % |
| 05-09.5b | tests for full branch coverage | 3 | — |
| 05-09.6a | MC/DC tests for (a and b) or c | 4 | — |
| 05-09.7a | escapes with three 50% filters | 10 | — |
| 05-09.7b | improved catch rate of one filter | 75 | % |
| 05-09.7c | catch rate of a fourth filter | 50 | % |
| 05-09.9a | requirement coverage | 60 | % |
| 05-09.10a | sample at which the alarm asserts | 6 | — |
| 05-09.10b | sample at which it clears | 8 | — |
| 05-09.10c | sample at which the buggy version asserts | 4 | — |
| 05-09.11a | estimated total defects | 50 | — |
| 05-09.11b | estimated undiscovered defects | 10 | — |
| 05-09.12a | detection probability, 1000 canaries | 0.632 | — |
| 05-09.12b | canaries for 95% detection | 2995 | — |
