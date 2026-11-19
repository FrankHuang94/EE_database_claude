# Lab 05-05 · C Fundamentals

**Chapter:** [05-05](../../chapters/05-05-c-fundamentals.md) · **Files:** [adc.h](adc.h), [adc.c](adc.c), [adc_test.c](adc_test.c), [ub_demo.c](ub_demo.c) · **Time:** about 90 minutes

## Objective

1. Watch a C program pass through the preprocessor, compiler, assembler and linker, and inspect each stage's output.
2. Read and extend a small, tested C module: ADC-to-millivolt conversion with rounding, and a first-order digital filter.
3. See undefined behavior pass silently without a sanitizer and get caught with one.
4. Recognize a linker error by provoking one.

## Background

Chapter sections 3.1 (build stages), 3.3 (integer arithmetic), 3.6 (multi-file programs) and 3.8 (undefined behavior), and Examples 05-05.1 and 05-05.4. You need a C compiler (`cc`, GCC or Clang) on Linux, macOS or WSL; see [SETUP.md](../../../../SETUP.md). The test runs automatically in CI through [`tools/run_c.py`](../../../../tools/run_c.py), which compiles `adc_test.c` with `adc.c` under `-Werror` and the address and undefined-behavior sanitizers, and requires the output `TEST PASSED`.

## Procedure

Work in this folder in a terminal. Write each prediction down before running the command.

1. **Run the tests.**

   ```bash
   cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined -fno-sanitize-recover=all \
      adc_test.c adc.c -lm -o adc_test
   ./adc_test
   ```

2. **The four stages, one at a time.** *Predict:* `adc.c` is about 50 lines; how long is its preprocessed form?

   ```bash
   cc -E adc.c | wc -l          # preprocessed text: headers pasted in
   cc -S adc.c                  # compiler output: adc.s (assembly)
   cc -c adc.c                  # assembler output: adc.o (object code)
   nm adc.o                     # symbols defined (T) and needed (U) by the object file
   ```

   In `nm`'s listing, `adc_to_mv` and the `ema_` functions are marked `T` (defined here), and `exp` is `U` (undefined here, to be supplied by the math library at link time).

3. **Remove the rounding.** In a copy of `adc.c`, delete `+ full / 2` from `adc_to_mv`, rebuild and rerun the tests. *Predict:* which checks fail?
4. **Undefined behavior, silent and caught.** *Predict:* what does `ub_demo.c` print?

   ```bash
   cc -std=c17 -O1 ub_demo.c -o ub_plain && ./ub_plain
   cc -std=c17 -O1 -fsanitize=undefined ub_demo.c -o ub_checked && ./ub_checked
   cc -std=c17 -O1 -fsanitize=undefined -fno-sanitize-recover=all ub_demo.c -o ub_stop && ./ub_stop; echo "exit status $?"
   ```

5. **A linker error on purpose.** Build without `adc.c`: `cc adc_test.c -lm -o broken`. Read the message and identify the stage.
6. **Extend the module.** Add `int adc_from_mv(int mv, int bits, int vref_mv)`, the inverse conversion (rounded), declare it in `adc.h`, and add at least three checks to `adc_test.c`, including one invalid input.

## Expected results

| Step | Expected |
|---|---|
| 1 | `TEST PASSED` (12 checks, including two inputs that would never settle) |
| 2 | about 1,200 lines on 64-bit Linux with glibc (the exact count depends on the system's headers); `adc.s` and `adc.o` created; `nm` lists `T adc_to_mv`, `T ema_alpha`, `T ema_settle_samples`, `T ema_step`, `U exp` |
| 3 | `FAIL: check on line 25` and `line 27` (the 1000-code and 700-code cases), then `TEST FAILED (2 failures)` |
| 4 | without the sanitizer: `counter = -2147483648`, exit status 0; with it: `runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'` and the program continues, printing `counter = -2147483648`; with `-fno-sanitize-recover=all`, the same report and then the program stops with a nonzero exit status, as this course's builds do |
| 5 | `undefined reference to 'adc_to_mv'` (and the other functions) from the linker (`ld`) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-05.a | full-scale code 4095 (12-bit, 3.3 V), rounded | 3299 | mV |
| Lab 05-05.b | code 1000, rounded | 806 | mV |
| Lab 05-05.c | samples to settle within 1% (1 ms, 10 ms) | 47 | — |
| Lab 05-05.d | checks that fail without rounding | 2 | — |
| Lab 05-05.e | value printed by ub_demo without a sanitizer | −2147483648 | — |

## Discussion questions

1. Why do only two of the five conversion checks fail when the rounding term is removed?
2. `ub_plain` printed −2147483648 and exited normally. Why is that worse than a crash, and why is it still not "the correct two's-complement answer"?
3. `adc_to_mv` multiplies in `int64_t`. Is that necessary for a 16-bit ADC with a 3300 mV reference? For what inputs would 32-bit arithmetic overflow?
4. The tests compare `ema_alpha` with a tolerance of 10⁻⁶ but `ema_settle_samples` exactly. Why is each choice appropriate?

<details><summary>Answers to the discussion questions</summary>

1. Rounding changes the result only when the exact value's fractional part is at least 0.5. Code 0 and mid-scale 2048 are exact (0 and 1650 mV); 4095 gives 3299.19, which truncates and rounds to the same 3299. Only 1000 (805.66) and 700 at 10 bits (3417.97) round up, so only those two checks detect the missing term. This is why test values should be chosen to exercise each behavior, not just picked at random.
2. A crash is noticed; a plausible wrong number propagates into decisions. It is not "the correct" answer because the C standard defines no answer: the hardware happened to wrap, but the compiler was entitled to assume the overflow cannot happen and to optimize accordingly (for example, deleting an overflow check), so the same source can behave differently at another optimization level or compiler version.
3. Not for 16 bits and 3300 mV: the largest product is $65{,}535 \times 3300 + 32{,}768 \approx 2.16\times10^8$, within the 32-bit limit of $2.15\times10^9$. It would overflow 32 bits once `code × vref_mv` exceeds about $2.1\times10^9$, for example a 16-bit code with a reference above 32,767 mV, which the function's interface allows. Using 64 bits makes the function correct for every input it accepts, at negligible cost, so no caller has to know the limit.
4. `ema_alpha` returns a floating-point value computed through `exp`, which may differ in the last bits between math libraries, so it is compared with a tolerance well below the precision the test cares about. `ema_settle_samples` returns an integer count, which is either right or wrong; but it is derived from floating-point comparisons, so a test value should not sit on a knife edge: here $\ln(100)\tau/T_s = 46.05$ and $\ln(1000)\tau/T_s = 27.63$ are comfortably away from integers.

</details>

## Optional hardware version

On a microcontroller board (any Arduino-compatible or STM32 board), compile `adc.c` into a sketch, read a potentiometer with the board's ADC, print the code and `adc_to_mv` result over the serial port, and compare with a multimeter. Note the board's ADC resolution and reference voltage, and whether the board's `int` is 16 or 32 bits (`sizeof(int)`).
