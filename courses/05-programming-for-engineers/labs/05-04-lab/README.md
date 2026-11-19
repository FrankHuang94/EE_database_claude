# Lab 05-04 · Jupyter, Testing and Reproducible Workflows

**Chapter:** [05-04](../../chapters/05-04-reproducible-workflows.md) · **Notebook:** [05-04-workflows.ipynb](05-04-workflows.ipynb) · **Time:** about 75 minutes

## Objective

1. Catch hidden state in a saved notebook by re-executing it from a clean kernel.
2. See which tests catch which bugs, and why a suite needs tests of several kinds.
3. Search a git history for the commit that introduced a wrong value, and recover the earlier file.
4. Watch this repository's checker reject a wrongly published number, and relate its sensitivity to the number of published digits.

## Background

Chapter sections 3.1 to 3.6 and Examples 05-04.1, 05-04.2 and 05-04.4. Everything runs in a temporary folder; git uses a fixed author and clock, so your commit hashes will match the expected results below. You need git on your PATH and the packages in `requirements.txt` (pytest, nbconvert via JupyterLab).

## Procedure

1. Run **Restart & Run All** once, then work cell by cell, writing each prediction first.
2. **Part 1:** predict what a fresh run of the saved notebook prints.
3. **Part 2:** for each broken decoder, predict which of the four tests fail before running.
4. **Part 3:** predict whether git can find the commit that introduced `20.0` without you reading the diffs.
5. **Part 4:** predict which published values the checker accepts for 3.19728 kΩ.
6. Do the "Your turn" exercises.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | cell 3 output and counts | saved: τ = 2.000 ms, counts 1, 2, 4, 3; fresh: τ = 1.000 ms, counts 1, 2, 3, 4 |
| 2 | failing tests per version | correct 0; multiplier off by one 3 (all known cases); digits swapped 2 (1 kΩ and 47 kΩ, not 22 Ω); no validation 1 (the unknown-color test) |
| 3 | pickaxe search | `091cff7 Tidy README and update gain`; `gain.py` before it reads `gain = 2.0` |
| 4 | checker verdicts for 3.19728 kΩ | 3.197 pass; 3.198 fail (±0.0005 kΩ); 3.20 pass; 3.1973 pass |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-04.a | τ from a fresh run | 1.000 | ms |
| Lab 05-04.b | tests failed by the multiplier bug | 3 | — |
| Lab 05-04.c | tests failed by the swapped-digits bug | 2 | — |
| Lab 05-04.d | tests failed by the missing validation | 1 | — |
| Lab 05-04.e | smallest error detectable in 3.197 kΩ | 0.5 | Ω |

## Discussion questions

1. Part 1's saved notebook was internally consistent cell by cell; every output was really produced by its cell. Why is it still wrong, and what in the file gave it away?
2. The swapped-digits bug passed the 22 Ω test. Design a rule for choosing known-case tests that avoids this blind spot.
3. In Part 3, the commit that changed the gain was titled "Tidy README and update gain". What does this suggest about commit size and messages?
4. Why does publishing 3.20 kΩ instead of 3.197 kΩ make the curriculum's check weaker, even though both pass?

<details><summary>Answers to the discussion questions</summary>

1. Each output was produced by its cell, but in a kernel whose state came from running the cells in a different order (1, 2, 4, 3), so the page as a whole describes a computation that its code, read top to bottom, does not perform: $r$ = 1000 Ω and $C$ = 1 µF cannot give τ = 2 ms. The execution counts 1, 2, 4, 3 gave it away. Only re-execution from a clean kernel tells you what the code on the page actually produces.
2. A known case can only expose a bug that changes its answer. Swapping two equal digits changes nothing, so choose test values whose digits are all different (and different from zero), a multiplier other than ×1, and, in general, inputs with no symmetry that a plausible bug could hide behind. Combine several such cases with error cases; Part 2 shows that each test catches a different class of mistake.
3. The functional change (the gain) was buried in a commit described mainly as a documentation tidy-up, so a reader scanning the history would not suspect it. Commits should be small and do one thing, with a message that states the change and the reason ("Raise gain to 20 for the 3.3 V sensor"). Then both people and tools like `git log -S` and `git bisect` find problems quickly.
4. The checker's tolerance is half a unit in the last published digit: ±5 Ω for 3.20 kΩ, ±0.5 Ω for 3.197 kΩ. With 3.20, any computed value from 3.195 to 3.205 kΩ passes, so an error of several ohms would go unnoticed: using 4.71 kΩ instead of 4.7 kΩ by mistake gives 3.2019 kΩ, which passes against 3.20 but fails against 3.197. Fewer digits means a coarser check.

</details>

## Optional hardware version

Build a divider from two 10 kΩ, 5% resistors on a 5 V supply. Write a pytest test whose expected value is the nominal 2.5 V and whose tolerance you *derive* from the resistor tolerances (worst case: $5 \times 10.5/(9.5 + 10.5)$ = 2.625 V, so ±0.125 V), then record the measured voltage in a CSV, commit the CSV, the test and a note of the meter used, and confirm the test passes on the measured value.
