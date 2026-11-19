# Lab 05-01 · Python Fundamentals for Engineers

**Chapter:** [05-01](../../chapters/05-01-python-fundamentals.md) · **Notebook:** [05-01-python.ipynb](05-01-python.ipynb) · **Time:** about 75 minutes

## Objective

1. Predict, then check, the values of short Python expressions, and explain each surprise.
2. Measure floating-point rounding: accumulated error in a running sum, careful summation, and machine epsilon.
3. See aliasing of mutable objects directly, using object identities.
4. Write a small function with input validation and test it with `assert`.
5. Time three ways of writing the same loop and learn what does and does not matter for speed in pure Python.

## Background

Chapter sections 3.2 to 3.9 and Examples 05-01.2 and 05-01.4; Problems 05-01.3 and 05-01.6. You need a working Python environment with Jupyter (set up in [00-04](../../../00-orientation/chapters/00-04-toolchain-walkthrough.md)); the notebook uses only the standard library. Part 5's timings depend on your computer; every other result is deterministic.

## Procedure

1. Open the notebook, then **Kernel → Restart & Run All** once to confirm it runs; then clear outputs and work through it cell by cell.
2. **Part 1:** write down your prediction for each of the twenty expressions before running the cell. Score yourself.
3. **Part 2:** predict the error after a million additions of 0.1, and the smallest power of two `x` with `1.0 + x != 1.0`.
4. **Part 3:** predict how many ones each grid contains after one assignment.
5. **Part 4:** predict what the decoder should do with an invalid color, then run the tests.
6. **Part 5:** predict the ranking of the three timing methods.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | expressions | `-7 // 2` → −4; `7 % -2` → −1; `round(0.5)` → 0 and `round(1.5)` → 2 (round half to even); `[1, 2] is [1, 2]` → `False`; `sorted(['10', '9', '100'])` → `['10', '100', '9']` |
| 2 | running sum of a million 0.1s | 100000.00000133288, an error of 1.333×10⁻⁶; `math.fsum` gives exactly 100000.0 |
| 2 | machine epsilon by halving | 2.220×10⁻¹⁶ = 2⁻⁵², equal to `sys.float_info.epsilon` |
| 2 | stored 0.1 minus one tenth | 5.551×10⁻¹⁸ |
| 3 | grids | shared rows: three ones (one object); independent rows: one |
| 4 | decoder | yellow–violet–red = 4700 Ω, brown–black–orange = 10 000 Ω; "purple" rejected with a clear message |
| 5 | timing | all three within about a factor of two; the order depends on the machine and Python version |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-01.a | error of the loop sum | 1.333×10^-6 | — |
| Lab 05-01.b | machine epsilon by halving | 2.220×10^-16 | — |
| Lab 05-01.c | representation error of 0.1 | 5.551×10^-18 | — |
| Lab 05-01.d | yellow–violet–red | 4700 | Ω |
| Lab 05-01.e | brown–black–orange | 10000 | Ω |

## Discussion questions

1. The loop's error (1.3×10⁻⁶) is about 240 times the representation error of 0.1 multiplied by a million (5.6×10⁻¹²). Where does the extra error come from, and why does it grow with the size of the running total?
2. Python's `round` uses round-half-to-even. Why might a finance or measurement system prefer that to always rounding halves up?
3. In Part 4, why is it better for `decode` to raise a `ValueError` for "purple" than to return 0 or `None`?
4. Part 5 shows the three loop styles performing similarly. If your analysis of a million test records takes too long, what would you check first before rewriting it?

<details><summary>Answers to the discussion questions</summary>

1. Each addition rounds the running total to the nearest float. As the total grows, the spacing between floats near it grows in proportion (Figure 2 of the chapter), so each rounding can be larger: near 100000 the spacing is about $1.5\times10^{-11}$, and a million roundings of a fraction of that accumulate to about $10^{-6}$. The representation error of 0.1 is tiny by comparison. Summing small numbers into a large total loses the low-order bits of each addend; `math.fsum` keeps them.
2. Always rounding halves up biases totals upward: over many values that end in exactly 5, the errors all point the same way. Rounding half to even sends half of them up and half down, so the average error is zero. (Note that most decimal "halves" such as 2.675 are not exactly representable in binary anyway, so the rule matters most for values that are, like 0.5 and 1.5.)
3. A plausible return value lets a wrong result flow silently into a total or a bill of materials. An exception stops the program at the point of the mistake, with a message naming the bad input, so the error is found and fixed instead of propagated.
4. Profile first: find where the time actually goes (often reading files or parsing text, not arithmetic). Then move numerical inner loops into vectorized NumPy operations (05-02) or library functions, which run in compiled code and are typically tens to hundreds of times faster than any pure-Python loop style.

</details>

## Optional hardware version

None is needed for this lab. If you have a USB-connected instrument (a multimeter or power supply with a USB or LAN interface), read its manual's programming section and use Python to send one identification query and print the reply: the same pattern of strings in, numbers out, conversions and error handling as Part 4.
