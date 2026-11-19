# Problems 05-04 · Jupyter, Testing and Reproducible Workflows

Chapter: [05-04](../chapters/05-04-reproducible-workflows.md) · Worked solutions: [05-04 solutions](../solutions/05-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** Python 3.10 or later with pytest and git installed. Where a problem runs git, use a fixed author name and date as in chapter Section 3.2 so that your hashes match the solutions. Give every probability to the stated precision.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-04.1 [A]

**Reading execution counts.** A saved notebook shows three cells, top to bottom:

| Cell | Code | Execution count |
|---|---|---|
| A | `v = 5.0` | 1 |
| B | `i = v / 1e3` | 4 |
| C | `v = 3.3` | 3 |

Count 2 belongs to a cell that has since been deleted; it contained `v = 12.0`. (a) What value of `i` does the kernel hold? (b) What value will *Restart & Run All* give? Express both in milliamperes.

### Problem 05-04.2 [A]

**Assertion or exception?** For each check, say whether it should be an `assert` or a raised exception, and why.

1. A function `rc_cutoff(r, c)` receives a negative capacitance from its caller.
2. Inside a sorting routine, after the main loop, the list should be in non-decreasing order.
3. A file named by the user does not exist.
4. A computed probability should lie between 0 and 1.
5. In a test file: the divider output for 10 kΩ over 10 kΩ should be half the input.

### Problem 05-04.3 [A]

**A git hash by hand.** Compute git's blob hash of a file containing exactly `R = 4.7e3` followed by a newline, using `hashlib`, and confirm it with `git hash-object`. How many bytes does the file contain?

### Problem 05-04.4 [B]

**A default that is too loose.** A test checks a simulated leakage current: `assert i_leak == pytest.approx(2.0e-12)`, where currents are in amperes. (a) Using pytest's default tolerances, what absolute deviation does this test allow? (b) As a percentage of the expected value? (c) Rewrite the comparison to allow a relative error of 10⁻⁶, and show that a value of 2.9×10⁻¹² A now fails.

### Problem 05-04.5 [B]

**Testing a parallel-resistance function.** Write `parallel(*resistors)` for any number of resistors. It must raise `ValueError` if no resistors are given or any is not positive. Write pytest tests covering a hand-worked case (three 3 kΩ resistors), order independence, the bound "below the smallest resistor", and both error cases; run them. What does the hand-worked case give?

### Problem 05-04.6 [B]

**A test that cannot see the bug.** A function meant to convert a voltage ratio to decibels was written as `10 * math.log10(ratio)` instead of `20 * math.log10(ratio)`. Two tests are proposed: (i) `db(10)` equals 20; (ii) `db(a * b)` equals `db(a) + db(b)` for several pairs. Which test catches the bug, and why does the other pass? Give the buggy and the correct `db(10)`.

### Problem 05-04.7 [B]

**How long can a short hash be?** Use the birthday approximation $P \approx n^2/(2N)$ (and $n \approx \sqrt{2N\ln2}$ for a 50% chance).

1. For full 160-bit SHA-1 hashes, how many objects give an accidental-collision probability of 10⁻⁹?
2. For 7-hex-digit short hashes (28 bits), how many commits give a 50% chance that two share a short hash?
3. For 100,000 commits, how many pairs of commits are expected to share a 7-digit short hash?

### Problem 05-04.8 [B]

**A tolerance for a Monte Carlo yield.** A Monte Carlo simulation estimates a circuit's yield from $n$ = 2500 random samples; the true yield is 0.9. A test asserts that the estimate lies within $\pm k$ standard errors of 0.9. (a) Find the standard error. (b) Choose $k$ so that a correct run fails with probability 10⁻⁶ (two-sided, normal approximation). (c) What half-width of the yield interval does that give?

### Problem 05-04.9 [B]

**Half a unit in the last digit.** (a) What tolerance does this curriculum's checker apply to a value published as 2.20? To one published as 6.32×10⁻³? (b) For each published value and computed value, does the check pass: 2.20 against 2.2049; 2.20 against 2.2051; 4.7 against 4.7368; 1.0551 against 1.05510204?

### Problem 05-04.10 [C]

**Finding the bad commit by bisection.** Build a repository of 16 commits, each recording a filter gain in `gain.py`; commit number 11 introduces a wrong value. Use `git bisect run` with a small check script to find the first bad commit automatically. (a) Which commit does git report? (b) In general, how many tests does bisection need at most to search 1000 commits?

### Problem 05-04.11 [C]

**A flaky suite.** A suite contains 400 independent statistical tests, each with ±3-standard-error limits and a fresh random seed on every run. (a) What is the probability that a run of the suite fails even though the code is correct? (b) What per-test false-failure probability keeps the suite's false-failure probability at 1%? (c) What limit, in standard errors, does that require?

### Problem 05-04.12 [C]

**A notebook checker.** Write a function `ran_in_order(nb)` that takes a notebook (as read by `nbformat`) and returns `True` only if every code cell has been run and the execution counts, read from top to bottom, are exactly 1, 2, 3, … . Test it on three notebooks you build with `nbformat`: one run cleanly, one run out of order, and one with an unrun cell. Why is this check weaker than re-executing the notebook?

---

## Objective coverage

| Learning objective (chapter 05-04) | Problems |
|---|---|
| 1. Notebooks and hidden state | 1, 12 |
| 2. Git: history, differences and hashes | 3, 7, 10 |
| 3. Unit tests and float tolerances | 4, 5, 6, 9 |
| 4. Assertions versus exceptions; tests of random code | 2, 8, 11 |
| 5. Reproducibility and verification | 9, 10, 12 |
