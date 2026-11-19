# Problems 05-05 · C Fundamentals

Chapter: [05-05](../chapters/05-05-c-fundamentals.md) · Worked solutions: [05-05 solutions](../solutions/05-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** C17 with 32-bit `int` (as on desktop systems and 32-bit microcontrollers), compiled with `-Wall -Wextra -Wpedantic` and, for testing, `-fsanitize=address,undefined`. Work each answer by hand first, then confirm it with a program.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-05.1 [A]

**Which stage?** For each message, name the build stage (preprocessor, compiler, linker) or say that it comes from running the program, and give a likely cause.

1. `fatal error: ema.h: No such file or directory`
2. `error: expected ';' before 'return'`
3. `undefined reference to 'ema_alpha'`
4. `runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'`

### Problem 05-05.2 [A]

**Integer and mixed arithmetic.** Evaluate in C: (a) `17 / 5`, (b) `17 % 5`, (c) `-17 / 5`, (d) `-17 % 5`, (e) `17 / 5.0`, (f) `(int)-3.7`, (g) `1 / 2 * 4.0`.

### Problem 05-05.3 [A]

**Choosing types.** Choose a fixed-width type for each quantity and justify it: (a) a 12-bit ADC code; (b) a 32-bit peripheral register; (c) a temperature from −40 °C to +125 °C stored in hundredths of a degree; (d) milliseconds since power-on, for a device that must run for a year without restarting. For (d), after how many days does a `uint32_t` millisecond counter wrap?

### Problem 05-05.4 [B]

**Conversions that surprise.** Predict, then check: (a) `-1 < 0u`; (b) the value stored by `uint8_t t = 200 + 100;`; (c) `a + b` for `uint8_t a = 200, b = 100;`; (d) `-1 < (int)sizeof(int)` and `-1 < sizeof(int)`. Explain each.

### Problem 05-05.5 [B]

**A 10-bit ADC.** A 10-bit ADC with a 5.000 V reference reports codes 0 to 1023, with $V = k \times 5000\text{ mV}/1024$. For $k$ = 700, find the millivolt value (a) exactly, (b) with truncating integer arithmetic, (c) rounded to nearest in integer arithmetic. (d) What is the largest intermediate product, and does it fit in a 16-bit `int`?

### Problem 05-05.6 [B]

**A function in its own module.** Write `clamp.h` and `clamp.c` providing `int clamp(int x, int lo, int hi)`, which limits `x` to the range [`lo`, `hi`], and a `main` in a separate file that prints `clamp` of −5, 50 and 500 to [0, 255]. Explain what the header's include guard does.

### Problem 05-05.7 [B]

**Macros gone wrong.** Given `#define CUBE(x) x * x * x` and `#define HALF(x) x / 2`, evaluate `CUBE(2 + 1)` and `HALF(10 + 4)`. Fix both macros, give the corrected values, and write `static inline` replacements.

### Problem 05-05.8 [B]

**A running average with static state.** Write `double running_average(double x)` that returns the mean of every value passed so far, using `static` local variables. What does it return for the inputs 3, 5 and 10 in turn? Why is such a function hard to test?

### Problem 05-05.9 [B]

**Settling of a faster filter.** The moving-average filter of chapter Section 3.6 runs with $T_s$ = 0.5 ms and τ = 2 ms. Find α, and the number of samples until a unit step is within 0.1% of its final value. Confirm by simulation in C.

### Problem 05-05.10 [C]

**A 24-bit audio accumulator.** A 24-bit audio ADC produces signed samples up to $2^{23} - 1$ = 8,388,607 in magnitude. (a) Does one full-scale square fit in an `int32_t`? (b) How many full-scale squares fit in an `int64_t`? (c) How many seconds of continuous full-scale audio at 48 kHz is that? (d) Write the accumulation so that no intermediate overflows.

### Problem 05-05.11 [C]

**Elapsed time across a counter wrap.** A `uint32_t` counter increments every millisecond. (a) After how many days does it wrap? (b) A measurement starts at count 4,294,967,000 and ends after the counter has wrapped, at count 704. Show that `end - start` computed in `uint32_t` gives the correct elapsed time, and find it. (c) Why would the same code with `int32_t` be wrong? (d) A widely reported aircraft software fault involved a counter overflowing after about 248 days. Show that a signed 32-bit counter of 10 ms ticks would overflow after about that time.

### Problem 05-05.12 [C]

**Averaging two integers safely.** `int avg(int a, int b) { return (a + b) / 2; }` is used on large readings. (a) Show that it overflows for `a = b = 2000000000` and confirm with UBSan. (b) The alternative `a + (b - a) / 2` avoids that overflow when `a` and `b` have the same sign. Evaluate both formulas for `a = -7, b = 2`: do they agree? (c) Write a version that is correct for all `int` inputs and rounds toward zero.

---

## Objective coverage

| Learning objective (chapter 05-05) | Problems |
|---|---|
| 1. The build stages | 1, 6 |
| 2. Types, arithmetic and conversions | 2, 3, 4, 5, 10, 11 |
| 3. Functions, headers and `static` | 6, 8, 9 |
| 4. The preprocessor | 6, 7 |
| 5. Undefined behavior and its detection | 4, 10, 11, 12 |
