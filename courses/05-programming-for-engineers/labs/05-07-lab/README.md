# Lab 05-07 · Bit Manipulation and Fixed-Width Integers

**Chapter:** [05-07](../../chapters/05-07-bit-manipulation.md) · **Files:** [bits.h](bits.h), [bits.c](bits.c), [bits_test.c](bits_test.c) · **Time:** about 75 minutes

## Objective

1. Manipulate register bit fields, and see how a naive read-modify-write damages a write-1-to-clear status register.
2. Serialize and parse values in both byte orders without depending on the host's order.
3. Implement Q15 conversion, multiplication and saturating addition, and measure quantization error against theory.
4. Validate bit tricks exhaustively against slow reference implementations.

## Background

Chapter sections 3.2 to 3.7 and Examples 05-07.2 to 05-07.4. The test runs in CI through [`tools/run_c.py`](../../../../tools/run_c.py) with strict warnings and sanitizers. The status register here is *simulated* by a struct whose write function behaves like write-1-to-clear hardware: every bit written as 1 clears that pending flag, and bits written as 0 are ignored.

## Procedure

1. **Run the tests.**

   ```bash
   cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined bits_test.c bits.c -lm -o bits_test
   ./bits_test
   ```

2. **Write-1-to-clear.** Read part 2 of `bits_test.c`. Flags A (bit 0) and B (bit 1) are pending. *Predict:* after the "naive" `status_write(&st, status_read(&st) | 0x1u)`, which flags remain?
3. **Byte order.** *Predict:* on your machine, does the `memcpy` into `host` equal `get_le32(b)` or `get_be32(b)`? Add a `printf` to find out.
4. **Q15.** Change `q15_mul` to truncate (remove `+ (1 << 14)`), rebuild and run. *Predict:* which checks fail?
5. **Exhaustive checks.** Part 5 compares the fast functions with slow ones over all 65,536 16-bit values. *Predict:* how many of those values are powers of two, and how many 1 bits do they contain in total?
6. **Extend.** Add `int16_t q15_sub_sat(int16_t a, int16_t b)` with tests, including `q15_sub_sat(INT16_MIN, 1)`.

## Expected results

| Step | Expected |
|---|---|
| 1 | `TEST PASSED` |
| 2 | no flags remain (`0x0`): the read returned both pending bits, the OR kept them, and writing them back cleared both, so flag B's event is lost. Writing only `0x1` leaves `0x2` (B still pending) |
| 3 | on x86 and Arm-based computers, `get_le32(b)`: both are little-endian; the check passes on either kind of host |
| 4 | `FAIL: check on line 59`, one failure: `q15_mul(22938, 22938)` now gives 16056 instead of 16057; the exact product −12288 on the same line and the saturation check are unaffected |
| 5 | 16 powers of two ($2^0$ to $2^{15}$); 524,288 ones in total ($16 \times 2^{15}$: each of 16 bit positions is 1 in half of the values) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-07.a | pending flags after the naive read-modify-write | 0 | — |
| Lab 05-07.b | pending flags after writing only bit 0 | 2 | — |
| Lab 05-07.c | Q15 0.7² with truncation instead of rounding | 16056 | — |
| Lab 05-07.d | powers of two among 16-bit values | 16 | — |
| Lab 05-07.e | total 1 bits over all 16-bit values | 524288 | — |
| Lab 05-07.f | q15_add_sat(30000, 10000) | 32767 | — |

## Discussion questions

1. Why do hardware designers use write-1-to-clear status bits at all, given the read-modify-write trap?
2. The byte-order check in part 3 passes on any host. Why is that a better test than asserting that the host is little-endian?
3. Why does the quantization-error check use a tolerance of 3% rather than requiring the RMS error to equal $\Delta/\sqrt{12}$?
4. Part 5 tests 65,536 inputs. Why is exhaustive testing feasible here but not for a function of two 32-bit inputs?

<details><summary>Answers to the discussion questions</summary>

1. With write-1-to-clear, software can acknowledge exactly the events it has handled, without a read-modify-write, and without disturbing flags that hardware raised in the meantime: writing `0x1` clears only flag A even if B arrived a nanosecond earlier. A plain read/write register would force a read-modify-write, which races with the hardware setting new flags. The trap appears only when software treats the register as ordinary memory.
2. The property that matters is that the serialization functions are correct regardless of the host; a test that asserted little-endian would fail on a big-endian host even though the code is correct there, and would say nothing about the code. The check here asserts what is true everywhere (the host's order is one of the two) and lets the real tests, which never depend on the host, do the work.
3. The measured RMS is a statistic of 10,000 random errors, so it fluctuates around the theoretical value. For a uniform error, the relative standard deviation of the mean square over $n$ samples is about $\sqrt{0.8/n}$ (the variance of $e^2$ is $4/5$ of the square of its mean), so about 0.9% for the mean square and 0.45% for the RMS; 3% is several standard deviations wide, so a correct implementation essentially never fails, while a truncating one (RMS doubled) always does. This is Example 05-04.5's lesson applied.
4. A function of 16 bits has 65,536 inputs, which run in milliseconds. Two 32-bit inputs give $2^{64} \approx 1.8\times10^{19}$ combinations, which at $10^9$ tests per second would take about 585 years (00-04). Then one tests boundaries, random samples and properties instead, or proves correctness formally.

</details>

## Optional hardware version

On a microcontroller board, find one peripheral's status register in the reference manual, note which bits are write-1-to-clear, and write a small program that raises two of its flags and clears one correctly; confirm with a debugger that the other flag survives.
