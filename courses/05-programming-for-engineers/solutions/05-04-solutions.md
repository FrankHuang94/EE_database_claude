# Solutions 05-04 · Jupyter, Testing and Reproducible Workflows

Problems: [05-04 problems](../problems/05-04-problems.md) · Chapter: [05-04](../chapters/05-04-reproducible-workflows.md). Every code block below is run by [verify_05_04.py](../verify/verify_05_04.py), which checks that it prints exactly what is shown and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-04.1

The kernel ran the cells in execution-count order: A (1), the deleted cell (2), C (3), then B (4). Simulating a kernel with a dictionary:

```python
cells = {"A": "v = 5.0", "deleted": "v = 12.0", "C": "v = 3.3", "B": "i = v / 1e3"}

def run(order):
    kernel = {}
    for name in order:
        exec(cells[name], kernel)
    return round(kernel["i"] * 1e3, 6)       # in mA

print(run(["A", "deleted", "C", "B"]), run(["A", "B", "C"]))
```

```text
3.3 5.0
```

(a) When B ran, `v` was 3.3 (from C), so the kernel holds $i$ = **3.3 mA**, although the cell directly above B says `v = 5.0`. (b) *Restart & Run All* runs A, B, C, giving $i$ = **5.0 mA**; C then changes `v` without affecting `i`. The saved page is misleading in both directions: B's output disagrees with the cell above it, and C's assignment looks as if it should matter. Units: V / Ω = A, ×10³ for mA ✓.

### Solution 05-04.2

1. **Exception** (`ValueError`): the caller supplied invalid input, which can happen however correct `rc_cutoff` is. It must always be checked, so it cannot be an `assert` (which `python -O` removes).
2. **Assert:** sortedness after the loop is an invariant of the routine's own logic; if it fails, the routine has a bug.
3. **Exception:** a missing file is an external condition, not a bug; Python already raises `FileNotFoundError`, and the caller should handle or report it.
4. **Usually assert:** if the probability is computed by your own code from valid inputs, being outside [0, 1] means a bug. If it comes from outside (a file, a user), validate it and raise.
5. **Assert:** in a test file, `assert` is the standard way to state the expected result; pytest reports the values when it fails, and tests are never run with `-O`.

### Solution 05-04.3

```python
import hashlib
import subprocess

content = b"R = 4.7e3\n"
by_hand = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
by_git = subprocess.run(["git", "hash-object", "--stdin"], input=content, capture_output=True).stdout.decode().strip()
print(len(content), by_hand, by_hand == by_git)
```

```text
10 096e0b63a883aa557de557743bbf48e39c8674c8 True
```

The file is **10 bytes** (nine visible characters and the newline), and the hand computation matches git exactly. The header `blob 10\0` is part of what is hashed, which is why the hash differs from a plain SHA-1 of the file's bytes.

### Solution 05-04.4

(a) `pytest.approx(expected)` allows $\max(10^{-6}\lvert\text{expected}\rvert,\ 10^{-12})$ = $\max(2\times10^{-18},\ 10^{-12})$ = **1×10⁻¹² A**. The absolute floor dominates completely.

(b) That is $10^{-12}/(2\times10^{-12})$ = **50%** of the expected value: the test accepts anything from 1 pA to 3 pA.

(c) Remove the absolute floor (or set it far below the signal):

```python
import pytest

print(2.9e-12 == pytest.approx(2.0e-12), 2.9e-12 == pytest.approx(2.0e-12, rel=1e-6, abs=0.0),
      2.0000001e-12 == pytest.approx(2.0e-12, rel=1e-6, abs=0.0))
```

```text
True False True
```

With the default, 2.9 pA "equals" 2.0 pA; with `abs=0.0` the comparison is purely relative and correctly rejects it while still accepting a 5×10⁻⁸ relative difference. Defaults are tuned for quantities of order 1; picoamperes, femtofarads and gigahertz need tolerances chosen from their own scale.

### Solution 05-04.5

```python
import os
import sys
import textwrap
from pathlib import Path

Path("parallel.py").write_text(textwrap.dedent('''
    def parallel(*resistors):
        """Equivalent resistance of resistors in parallel, in ohms."""
        if not resistors:
            raise ValueError("need at least one resistor")
        if any(r <= 0 for r in resistors):
            raise ValueError("resistances must be positive")
        return 1.0 / sum(1.0 / r for r in resistors)
'''))
Path("test_parallel.py").write_text(textwrap.dedent('''
    import pytest
    from parallel import parallel

    def test_three_equal():
        assert parallel(3e3, 3e3, 3e3) == pytest.approx(1e3)

    def test_order_independent():
        assert parallel(1e3, 4.7e3, 22e3) == pytest.approx(parallel(22e3, 1e3, 4.7e3))

    @pytest.mark.parametrize("rs", [(1e3, 1e3), (10.0, 1e6), (4.7e3, 10e3, 22e3)])
    def test_below_smallest(rs):
        assert parallel(*rs) < min(rs)

    def test_empty_rejected():
        with pytest.raises(ValueError):
            parallel()

    def test_non_positive_rejected():
        with pytest.raises(ValueError):
            parallel(1e3, 0.0)
'''))

def pytest_run(*files):
    env = {**os.environ, "COLUMNS": "80", "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([sys.executable, "-m", "pytest", "-qq", "--tb=no", "-rf", "--color=no", "-p", "no:cacheprovider", *files],
                            capture_output=True, text=True, env=env)
    return result.stdout.rstrip()

print(pytest_run("test_parallel.py"))
sys.path.insert(0, os.getcwd())            # so that this session can import parallel.py too
from parallel import parallel

print(round(parallel(3e3, 3e3, 3e3), 9))
```

```text
.......                                                                  [100%]
1000.0
```

All seven tests pass (the bound test runs three times). Three 3 kΩ resistors in parallel give **1000 Ω** = 1 kΩ: $1/(3 \times 1/3000)$ ✓. The conductance form `1 / sum(1/r)` generalizes to any number of resistors, and the checks make an empty call or a zero resistor fail loudly instead of returning a meaningless number or dividing by zero.

### Solution 05-04.6

```python
import math

def db_buggy(ratio):
    return 10 * math.log10(ratio)

def db(ratio):
    return 20 * math.log10(ratio)

pairs = [(2.0, 5.0), (0.5, 8.0), (3.3, 1.2)]
for f in (db_buggy, db):
    known = math.isclose(f(10), 20.0)
    additive = all(math.isclose(f(a * b), f(a) + f(b)) for a, b in pairs)
    print(f.__name__, f(10), known, additive)
```

```text
db_buggy 10.0 False True
db 20.0 True True
```

Test (i), the **known case**, catches the bug: the buggy function gives **10 dB** for a ratio of 10 instead of **20 dB**. Test (ii) passes for both, because $k\log_{10}(ab) = k\log_{10}a + k\log_{10}b$ holds for *any* constant $k$: the property is shared by the bug and the fix, so it cannot tell them apart. Property tests are powerful, but only when the property fails for the plausible mistakes. A known case pins down the constant.

### Solution 05-04.7

1. Solving $P = n^2/(2N)$ for $n$: $n = \sqrt{2NP} = \sqrt{2 \times 2^{160} \times 10^{-9}}$ = **5.4×10¹⁹** objects, far beyond any repository.
2. With $N = 2^{28}$ = 268,435,456: $n \approx \sqrt{2 \times 2^{28} \times \ln2}$ = **1.93×10⁴** commits, about 19,000. This is why git lengthens abbreviated hashes as a repository grows, and why scripts should use full hashes.
3. Expected colliding pairs $= \binom{n}{2}/N \approx n^2/(2N) = 10^{10}/(2 \times 2^{28})$ = **18.6** pairs.

```python
import math

print(f"{math.sqrt(2 * 2**160 * 1e-9):.2e} {math.sqrt(2 * 2**28 * math.log(2)):.0f} {1e5**2 / (2 * 2**28):.1f}")
```

```text
5.41e+19 19291 18.6
```

The expected number of pairs, $\binom{n}{2}/N$, needs no approximation; it is exact for random hashes because each of the $\binom n2$ pairs collides with probability $1/N$ (linearity of expectation, 03-03).

### Solution 05-04.8

(a) A yield estimate is a sample proportion, so (03-05) $\text{SE} = \sqrt{p(1-p)/n} = \sqrt{0.9 \times 0.1/2500}$ = **0.006**.

(b) Two-sided: $2[1 - \Phi(k)] = 10^{-6}$, so $k = \Phi^{-1}(1 - 5\times10^{-7})$ = **4.892**.

(c) Half-width $= k \times \text{SE}$ = 4.8916 × 0.006 = **0.0293**: the test passes when the estimate lies between 0.8707 and 0.9293.

```python
from scipy.stats import norm

se = math.sqrt(0.9 * 0.1 / 2500)
k = norm.isf(0.5e-6)
print(f"{se:.4f} {k:.3f} {k * se:.4f}")
```

```text
0.0060 4.892 0.0293
```

The normal approximation is adequate here because $np$ = 2250 and $n(1-p)$ = 250 are both large. The price of so few false alarms is a wide interval: a real yield drop from 0.90 to 0.88 would usually pass unnoticed. A test that must detect small changes needs more samples ($\text{SE} \propto 1/\sqrt n$).

### Solution 05-04.9

```python
from decimal import Decimal

def tolerance(published):
    return 0.5 * 10.0 ** Decimal(published).as_tuple().exponent

for shown, computed in (("2.20", 2.2049), ("2.20", 2.2051), ("4.7", 4.7368), ("1.0551", 1.05510204)):
    print(shown, computed, abs(float(shown) - computed) <= tolerance(shown))
print(tolerance("2.20"), tolerance("6.32e-3"))
```

```text
2.20 2.2049 True
2.20 2.2051 False
4.7 4.7368 True
1.0551 1.05510204 True
0.005 5e-06
```

(a) A value published as 2.20 is checked to ±**0.005**; one published as 6.32×10⁻³ to ±0.005×10⁻³ = **5×10⁻⁶**. (b) 2.2049 rounds to 2.20 and passes; 2.2051 rounds to 2.21, so publishing 2.20 would be wrong, and the check fails; 4.7368 passes against 4.7 (it rounds to 4.7), though only to two significant figures; 1.05510204 passes against 1.0551. The trailing zero in 2.20 matters: it claims a third significant figure, and the checker holds the author to it.

### Solution 05-04.10

```python
GIT_ENV = {**os.environ,
           "GIT_AUTHOR_NAME": "Ada Learner", "GIT_AUTHOR_EMAIL": "ada@example.com",
           "GIT_COMMITTER_NAME": "Ada Learner", "GIT_COMMITTER_EMAIL": "ada@example.com",
           "GIT_AUTHOR_DATE": "2026-11-18T09:00:00+00:00", "GIT_COMMITTER_DATE": "2026-11-18T09:00:00+00:00",
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "PYTHONDONTWRITEBYTECODE": "1"}

def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True, env=GIT_ENV)
    return (result.stdout + result.stderr).rstrip()

Path("filter-project").mkdir()
os.chdir("filter-project")
git("init", "-q", "-b", "main")
for step in range(1, 17):
    gain = 20.0 if step >= 11 else 2.0                       # step 11 introduces the wrong value
    Path("gain.py").write_text(f"gain = {gain}\n")
    Path("log.txt").write_text("".join(f"step {k}\n" for k in range(1, step + 1)))
    git("add", "gain.py", "log.txt")
    git("commit", "-q", "-m", f"Update filter (step {step})")
Path("check.py").write_text("exec(open('gain.py').read())\nraise SystemExit(0 if gain == 2.0 else 1)\n")
first = git("rev-list", "--max-parents=0", "HEAD")
git("bisect", "start", "HEAD", first)
git("bisect", "run", sys.executable, "check.py")
print(git("log", "-1", "--format=%s", "refs/bisect/bad"))
git("bisect", "reset")
os.chdir("..")
print(math.ceil(math.log2(1000)))
```

```text
Update filter (step 11)
10
```

(a) Git reports **step 11** as the first bad commit. The check script is the test: exit status 0 means "good", 1 means "bad", and `git bisect run` checks out the midpoint of the remaining range, runs the script, and halves the range each time. Here, with 15 candidate commits after the known-good first one, it needs 4 tests.

(b) Each test halves the candidates, so $n$ commits need at most $\lceil\log_2 n\rceil$ tests: **10** for 1000 commits. Bisection (the same algorithm as Example 05-01.7) turns "something broke in the last thousand commits" into ten automated runs, *provided* each commit can be built and tested on its own. That is one more reason for small commits that each leave the project working.

### Solution 05-04.11

(a) One test fails by chance with probability $2[1 - \Phi(3)]$ = 0.0027. With 400 independent tests:

$$
P(\text{suite fails}) = 1 - (1 - 0.0027)^{400} = 0.661,
$$

so about **66%** of runs fail with correct code. Such a suite is worse than useless: people learn to re-run until it passes, and real failures get ignored.

(b) Require $1 - (1 - p)^{400} = 0.01$: $p = 1 - 0.99^{1/400}$ = **2.51×10⁻⁵** per test.

(c) $2[1 - \Phi(k)] = 2.51\times10^{-5}$ gives $k$ = **4.21** standard errors.

```python
p3 = 2 * norm.sf(3)
p_test = 1 - 0.99 ** (1 / 400)
print(f"{1 - (1 - p3) ** 400:.3f} {p_test:.3e} {norm.isf(p_test / 2):.2f}")
```

```text
0.661 2.513e-05 4.21
```

Widening from 3 to 4.21 standard errors costs sensitivity: each test now notices only larger errors. The cleaner fix is to fix the seeds, so that results are repeatable and a failure always means something changed; then run occasional, separately reported fresh-seed sweeps to look for rare problems. This is the multiple-comparisons problem of 03-05 in software form.

### Solution 05-04.12

```python
import nbformat

def ran_in_order(nb):
    """True if every code cell has run and the counts read 1, 2, 3, ... from top to bottom."""
    counts = [cell.execution_count for cell in nb.cells if cell.cell_type == "code"]
    return all(c is not None for c in counts) and counts == list(range(1, len(counts) + 1))

def make(counts):
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_markdown_cell("# Test")]
    for k, c in enumerate(counts):
        cell = nbformat.v4.new_code_cell(f"x{k} = {k}")
        cell.execution_count = c
        nb.cells.append(cell)
    return nb

for counts in ([1, 2, 3], [1, 4, 3], [1, None, 2]):
    print(counts, ran_in_order(make(counts)))
```

```text
[1, 2, 3] True
[1, 4, 3] False
[1, None, 2] False
```

The checker accepts only the clean run. It is weaker than re-executing because counts 1, 2, 3 show only that the cells *were* run in order once; the saved outputs may still depend on things outside the notebook (a data file since changed, a package since upgraded, an environment variable), and a cell may have been edited after it ran without being re-run. The only conclusive test is to execute the notebook from a fresh kernel and compare, which is what this repository's `tools/run_notebooks.py` does. The counts check is still useful as a cheap first filter, for example in a pre-commit hook.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-04.1a | current held by the kernel | 3.3 | mA |
| 05-04.1b | current after Restart & Run All | 5.0 | mA |
| 05-04.3a | file length | 10 | bytes |
| 05-04.4a | allowed absolute deviation with defaults | 1×10^-12 | A |
| 05-04.4b | allowed deviation as a share of the value | 50 | % |
| 05-04.5a | three 3 kΩ resistors in parallel | 1000 | Ω |
| 05-04.6a | buggy db(10) | 10 | dB |
| 05-04.6b | correct db(10) | 20 | dB |
| 05-04.7a | objects for collision probability 10⁻⁹ (SHA-1) | 5.4×10^19 | — |
| 05-04.7b | commits for a 50% short-hash collision | 1.93×10^4 | — |
| 05-04.7c | expected colliding short-hash pairs, 10⁵ commits | 18.6 | — |
| 05-04.8a | standard error of the yield estimate | 0.006 | — |
| 05-04.8b | limit for a 10⁻⁶ false-failure rate | 4.892 | SE |
| 05-04.8c | half-width of the yield interval | 0.0293 | — |
| 05-04.9a | tolerance for 2.20 | 0.005 | — |
| 05-04.9b | tolerance for 6.32×10⁻³ | 5×10^-6 | — |
| 05-04.10a | first bad commit found by bisection | 11 | — |
| 05-04.10b | maximum tests for 1000 commits | 10 | — |
| 05-04.11a | suite false-failure probability | 0.661 | — |
| 05-04.11b | per-test false-failure probability for 1% | 2.51×10^-5 | — |
| 05-04.11c | required limit | 4.21 | SE |
