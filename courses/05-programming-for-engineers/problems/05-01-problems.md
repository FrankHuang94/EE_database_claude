# Problems 05-01 · Python Fundamentals for Engineers

Chapter: [05-01](../chapters/05-01-python-fundamentals.md) · Worked solutions: [05-01 solutions](../solutions/05-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** Python 3.12 or later. For "predict" problems, write your answer *before* running the code; then run it and explain any difference. Where a problem asks for a function, include a docstring and validate inputs.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-01.1 [A]

**Predict the values.** What do these expressions evaluate to, and what is the type of each? `7 / 2`, `7 // 2`, `7 % 3`, `2 ** 10`, `int("42") + 1`, `len("VDD_core")`.

### Problem 05-01.2 [A]

**Negative numbers and floor division.** Predict `-17 // 5`, `-17 % 5` and `divmod(17, -5)`, and check each against the identity `a == (a // b) * b + a % b`.

### Problem 05-01.3 [A]

**Float surprises.** (a) Compute `0.1 * 3 - 0.3`. (b) `round(2.675, 2)` returns 2.67, not 2.68. Explain why, using `Fraction(2.675)` or `f"{2.675:.20f}"`.

### Problem 05-01.4 [B]

**Decibel helpers.** Write `db_from_voltage_ratio(r)` returning $20\log_{10}r$, `db_from_power_ratio(r)` returning $10\log_{10}r$, and `dbm(p_watts)` returning $10\log_{10}(P/1\ \text{mW})$, each raising `ValueError` for a non-positive input. Evaluate a voltage ratio of 1000, a power ratio of 0.5, and 1 W and 1 µW in dBm.

### Problem 05-01.5 [B]

**Slicing a sample buffer.** `samples = list(range(0, 100, 7))`. Find (a) how many samples there are, (b) the last sample, (c) the list of every fourth sample starting from the first, and (d) the sum of that list.

### Problem 05-01.6 [B]

**The shared-row bug.** A student builds a 3 × 3 grid with `grid = [[0] * 3] * 3`, sets `grid[0][0] = 1`, and counts the ones. (a) How many ones are there, and why? (b) Build the grid correctly with a comprehension and count again.

### Problem 05-01.7 [B]

**The mutable default.** Run `log_bad` and `log_good` from §3.6 three times each with the default history, and report the length of the list each returns on the third call.

### Problem 05-01.8 [B]

**Counting by decade.** Given resistor values `[100, 220, 4700, 1000, 47000, 330, 2200, 10000, 68]` in ohms, build a dict mapping each decade exponent ($\lfloor\log_{10}R\rfloor$) to the number of resistors in it. How many decades appear, and how many values fall in the $10^3$ decade?

### Problem 05-01.9 [B]

**Compounding frequency.** Write `future_value(principal, rate, years, periods_per_year)` and compare 1000 at 6% for 10 years compounded annually and monthly. Find both values and the difference.

### Problem 05-01.10 [B]

**Parsing component values.** Extend `parse_ohms` from §3.9 to accept the prefixes `m` (milli), `k`, `M` and `G`. Find the total resistance of `["4.7k", "220", "1M", "68"]` in series, and show that `"4.7K"` (capital K) is rejected with a clear message.

### Problem 05-01.11 [C]

**When does the capacitor reach 1.8 V?** A capacitor discharges as $v(t) = 3.3e^{-t/\tau}$ V with τ = 2 ms. Using the `bisect` function of Example 05-01.7, find the time at which $v$ falls to 1.8 V, searching $[0, 10\ \text{ms}]$ with a tolerance of $10^{-9}$ s. Report the time in ms, the number of halvings, and compare with the exact $\tau\ln(3.3/1.8)$.

### Problem 05-01.12 [C]

**A temperature log.** Write a CSV file with columns `hour` and `temp_c` for hours 0 to 23, where `temp_c = 20 + hour % 12`. Read it back with `csv.DictReader` and report the mean temperature, the maximum, and the number of hours above 28 °C.

### Problem 05-01.13 [C]

**Counting set bits.** Using `bin(x).count("1")`, find (a) the total number of 1 bits in all integers from 0 to 255, and (b) how many of those integers have exactly four 1 bits. Explain both answers by counting.

### Problem 05-01.14 [C]

**How good is the rule of 72?** For whole-number growth rates from 1% to 20%, compare the exact doubling time $\ln2/\ln(1 + r)$ with $72/(100r)$. (a) At which whole-number rate is the rule most accurate? (b) Using bisection, find the rate (in percent) at which the rule is exact.

---

## Objective coverage

| Learning objective (chapter 05-01) | Problems |
|---|---|
| 1. Running Python, environments | 7, 12 |
| 2. Core types, division, floats, aliasing | 1, 2, 3, 5, 6, 8, 13 |
| 3. Control flow, comprehensions, functions | 4, 6, 7, 8, 9, 11, 14 |
| 4. Modules, files, exceptions | 4, 10, 12 |
| 5. Predicting output and debugging | 1, 2, 3, 6, 7 |
