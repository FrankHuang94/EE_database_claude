# Lab 05-09 · Software Engineering Practices

**Chapter:** [05-09](../../chapters/05-09-software-engineering-practices.md) · **Notebook:** [05-09-practices.ipynb](05-09-practices.ipynb) · **Time:** about 60 minutes

## Objective

1. Turn a requirement into boundary tests and see each test catch a specific class of bug.
2. Build a line-coverage tool from Python's tracing hook, and use it to find untested code.
3. Find a minimal MC/DC test set for a safety interlock by search.
4. Quantify how much each defect filter in a process contributes.

## Background

Chapter sections 3.1 (requirements), 3.4 (test design and coverage) and 3.6 (defect filters), and Examples 05-09.1, 05-09.3 and 05-09.4. Coverage tools such as `coverage.py` work by asking the Python interpreter to report each executed line through `sys.settrace`; Part 2 builds a twenty-line version to show there is no magic.

## Procedure

1. Run **Restart & Run All** once, then work part by part, writing each prediction first.
2. **Part 1:** predict which of the eight boundary tests each buggy monitor fails.
3. **Part 2:** predict which lines of `debounce` the first two tests miss; then check which single sequence reaches every line.
4. **Part 3:** predict the MC/DC minimum for `power_ok and door_closed and (temp_ok or override)`.
5. **Part 4:** predict which filter's removal hurts most, then check.
6. Do the "Your turn" exercises.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | failed tests | correct 0; `<=` bug 1 (the test at exactly 3.30 V); missing hold 2 (3.39 V and 3.35 V with the alarm on) |
| 2 | line coverage | first set 9 of 11 executable lines (82%), missing `state = True` and `state = False`; the sequence 3.25, 3.25, 3.25, 3.41 V reaches 100% |
| 3 | MC/DC | 5 tests of 16 combinations; 4 different minimal sets exist |
| 4 | escapes per 100 defects | 5.88 with all five filters; without review 14.70 (×2.50), without unit tests 11.76 (×2.00), without a 30% filter 8.40 (×1.43) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-09.a | tests failed by the `<=` bug | 1 | — |
| Lab 05-09.b | tests failed by the missing hold | 2 | — |
| Lab 05-09.c | line coverage of the first test set | 82 | % |
| Lab 05-09.d | minimum MC/DC tests for the interlock | 5 | — |
| Lab 05-09.e | escapes per 100 defects, all filters | 5.88 | — |
| Lab 05-09.f | escape multiplier without review | 2.50 | — |

## Discussion questions

1. The `<=` bug failed only one of eight tests. Is that a weak test suite?
2. Part 2 reached 100% line coverage with one test sequence. Is the function now well tested?
3. Why does a safety standard accept $N + 1$ MC/DC tests instead of all $2^N$ combinations?
4. Part 4 assumes the filters are independent. In which direction does that assumption err, and what does it mean for choosing practices?

<details><summary>Answers to the discussion questions</summary>

1. No. Each test targets one behavior; a suite is strong when *every plausible bug* fails *some* test, not when each bug fails many. The `<=` slip changes behavior at exactly one input, and the suite contains exactly that input. A suite where a bug fails no test is weak; one where it fails one is doing its job.
2. No. Every line ran, but a single sequence checks few behaviors: it does not exercise the counter reset in the middle of a low run, the hold inside the band, or the exact boundaries. Coverage shows what was *not* tested; it does not show that what ran was checked, or that the right cases were chosen. Problem 05-09.10's sequence adds those cases.
3. Exhaustive testing grows as $2^N$, which is impractical for decisions with many conditions, while MC/DC still demonstrates that every condition independently influences the outcome, which is what catches wrong operators, missing conditions and conditions that are accidentally irrelevant. It is a deliberately chosen middle ground between branch coverage (too weak) and exhaustive testing (too expensive).
4. It is optimistic: real filters are positively correlated (defects that slip past one tend to be the subtle ones that slip past others), so actual escapes are higher than the product predicts (Example 05-09.4). The practical consequence is to choose practices that are different in kind (human review, static analysis, tests at several levels, fuzzing, field telemetry) rather than more of the same.

</details>

## Optional hardware version

If you have a microcontroller board, implement the debounced battery monitor in C, drive the ADC input from a bench supply (or a potentiometer divider), and run the boundary tests physically at 3.29, 3.30, 3.31, 3.39, 3.40 and 3.41 V. Note how the ADC's resolution and noise limit how precisely a boundary can be tested on real hardware.
