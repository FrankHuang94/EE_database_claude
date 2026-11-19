# Course 05 · Final Exam (Programming for Engineers)

**Time limit:** 180 minutes. **Allowed:** a scientific calculator and the [Course 05 reference sheet](../../../reference/equation-sheets/05-programming-for-engineers.md) printed without its chapter links. No computer: trace code by hand and write code on paper, as in an interview or on the FE exam.
**Instructions:** answer all 15 questions and show your reasoning. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (127 points in total; 89 or more, about 70%, is a strong pass). Within a question, the lettered parts carry equal weight unless stated otherwise. Assume 32-bit `int`, 64-bit pointers and `size_t`, IEEE 754 doubles, and C17. Question 9(a) asks for a derivation; Question 13 asks you to write C; Question 15 is a short-answer diligence question graded against the rubric in the solutions. Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

---

**1 [A] · Python semantics (05-01).** What does this print?

```python
# not run
a = [1, 2, 3]
b = a
b.append(4)
c = a[:]
c[0] = 99
print(a, c, len(a), 7 // 2, -7 // 2, 0.1 + 0.2 == 0.3)
```

**2 [A] · NumPy types and shapes (05-02).** (a) How many elements has `np.ones((3, 1)) + np.arange(4)`, and what is its shape? (b) What is `np.uint8(200) + np.uint8(100)`? (c) Under NumPy 2's promotion rules, what is the first element of `np.array([100, 100], dtype=np.int8) + 50`? (d) What is the machine epsilon of `float32`?

**3 [B] · Numerical methods by hand (05-01, 05-03).** (a) How many bisection steps shrink the bracket [0, 1] below a width of $10^{-6}$? (b) Apply Newton's method to $f(x) = x^2 - 2$ from $x_0 = 1$: give $x_1$, $x_2$ and $x_3$ (6 decimals). (c) Fit $y = mx + b$ by least squares to the points (0, 1.0), (1, 2.9), (2, 5.1), (3, 7.0).

**4 [A] · Testing and reproducibility (05-04).** (a) What tolerance does a half-unit-in-the-last-digit check give a value published as 2.50? (b) A statistical test fails when its estimate is more than 3 standard errors from the truth. What is its false-failure probability, and the probability that at least one of 200 such independent tests fails with correct code? (c) About how many commits give a 50% chance that two share a 7-hex-digit short hash?

**5 [B] · C arithmetic (05-05).** Evaluate in C: (a) `-17 / 4` and `-17 % 4`; (b) `(unsigned)-2`; (c) `a + b` and `(uint8_t)(a + b)` for `uint8_t a = 250, b = 10;`; (d) `1 / 3 * 3.0`. (e) A 10-bit ADC with a 3300 mV reference reads 700. Give the millivolts computed as `k * 3300 / 1024` and with rounding.

**6 [B] · Tracing pointers (05-06).** After the following code, give `a[1]`, `a[3]`, `*p`, `sizeof a`, `sizeof p` and `(a + 4) - p`.

```c
// fragment
int a[5] = {10, 20, 30, 40, 50};
int *p = a + 1;
*p += 5;
p[2] = *(p - 1) + 1;
p++;
```

**7 [B] · Memory layout and strings (05-06).** (a) Give `sizeof` for `struct { uint16_t a; uint32_t b; uint8_t c; }` and the offset of `b`. (b) What is the smallest size after reordering, and how much RAM does that save for 2000 records? (c) `snprintf(buf, 8, "V=%.3fV", 3.3)` with `char buf[8]`: what does it return, and how many characters does `buf` hold? (d) Name the bug: a function saves `int *first = &log->data[0];`, then calls a function that may `realloc(log->data, ...)`, then reads `*first`.

**8 [B] · Bits and bytes (05-07).** A register reads `0x3A5C`. (a) Extract bits 11:8. (b) Write 3 into bits 7:4 without changing other bits; give the result in hex and decimal. (c) A sensor returns the 12-bit two's-complement field `0xE70` with 0.0625 °C per count; give the signed value and the temperature. (d) List the bytes of `0x11223344` in memory on a little-endian machine, lowest address first.

**9 [C] · Two's complement and Q15 (05-07).** (a) Derive why `~x + 1` equals `-x` in $n$-bit two's complement. (b) Convert 0.6 and −0.4 to Q15 (rounded), multiply them with the rounded Q15 multiply, and give the integer result, the value it represents and its error from −0.24. (c) What is the RMS rounding error of Q15, and how many decibels of SNR does a 16-bit quantizer gain over a 12-bit one?

**10 [B] · Algorithms (05-08).** (a) What is the maximum number of comparisons for binary search in 5000 sorted items? (b) Solve $T(n) = 2T(n/2) + n$, $T(1) = 0$, for $n = 64$. (c) What is the minimum worst-case number of comparisons any comparison sort needs for 8 items? (d) A ring buffer's free-running `uint32_t` counters read `head = 5`, `tail = 4294967294`. How many items does it hold?

**11 [B] · Hash table and heap (05-08).** (a) Six keys with home slots 3, 5, 3, 4, 7, 7 are inserted, in that order, into an empty 8-slot linear-probing table. Give each key's final slot, the total probes, and the average probes per successful search. (b) What does the linear-probing formula predict for an unsuccessful search at this load factor? (c) Insert 9, 4, 7 and 1, in that order, into an empty min-heap; give the array.

**12 [B] · Software engineering (05-09).** (a) Give the cyclomatic complexity of the function below. (b) What is the minimum number of MC/DC tests for `a && (b || c) && d`? (c) A parameter is valid from 10 to 200; list the boundary-value tests. (d) 40 defects pass through review (50%), unit tests (40%) and system tests (60%), assumed independent; how many are expected to escape?

```c
// fragment
int count_bad(const int *x, size_t n, int lo, int hi)
{
    int bad = 0;
    for (size_t i = 0; i < n; i++) {
        if (x[i] < lo && x[i] != -1) {
            bad++;
        } else if (x[i] > hi) {
            bad++;
        }
    }
    return bad;
}
```

**13 [C] · Writing C (05-05, 05-06, 05-08).** Write `size_t count_runs(const int16_t *x, size_t n, int16_t thr, size_t min_len)` that returns the number of maximal runs of consecutive samples strictly above `thr` whose length is at least `min_len`. Then state its result for `x = {5, 12, 13, 4, 15, 16, 17, 3, 11, 2, 14, 15}`, `thr = 10`, `min_len = 2`, name the classic bug that would give a different answer, and give its Big-O cost.

**14 [C] · Trust, but verify (05-03).** (a) A current is sampled every 1 ms as 0, 2, 3, 2, 1, 0 mA. Estimate the charge it delivers with the trapezoidal rule. (b) A colleague's solver reports that the diode in a 5 V, 1 kΩ circuit ($I_s = 10^{-14}$ A, $V_T$ = 25.852 mV) sits at 0.70 V. Compute the residual of $f(V) = (5 - V)/1000 - I_s(e^{V/V_T} - 1)$ at 0.70 V, and say whether you trust the answer. (c) Explain the habit that (b) illustrates, and one way the solver could have stopped at a non-root.

**15 [C] · Diligence (05-04 to 05-09).** A target's firmware lead says: "Our code is MISRA-compliant, has 100% test coverage, has never had a memory bug, and we can ship updates to the whole fleet in an hour." (a) Write four probing questions, one per claim, and describe what a strong answer would contain. (b) The company's canary group is 500 devices. What is the probability that a defect affecting 0.2% of devices shows up in the canary at least once? (c) What does (b) imply about "ship to the whole fleet in an hour"?
