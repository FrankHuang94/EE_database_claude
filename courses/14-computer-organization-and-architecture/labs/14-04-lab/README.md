# Lab 14-04 · Computer Arithmetic and Number Formats

Chapter: [14-04 Computer Arithmetic and Number Formats](../../chapters/14-04-computer-arithmetic-and-number-formats.md)

## Objective

See the rules of computer arithmetic at work. Run integer corner cases on an RV32IM simulator and find division "magic numbers" by search. Build a floating-point adder out of integer operations and check it bit for bit against the hardware. Measure how summation error grows with the number of terms. Quantize data to INT8, INT4 and a block-scaled 4-bit format and measure what each costs in accuracy.

## Background

Integer arithmetic, multiplication and division (§3.1–3.2), floating-point rounding (§3.3), error in sums (§3.4) and narrow formats (§3.5).

## Tools

Python with NumPy and Matplotlib. Part 1 also uses the LLVM tools of [Lab 14-03](../14-03-lab/README.md#tools) (`clang`, `llvm-mc`, `ld.lld`) and the course's RV32IM simulator, [verify/_rv32.py](../../verify/_rv32.py).

## Files

- [14-04-arithmetic-lab.ipynb](14-04-arithmetic-lab.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Integers (Part 1).** Run MUL, MULH, MULHU, DIV and REM on the simulator for the cases of Example 14-04.2. Write a search for the smallest shift $k$ for which $M = \lceil 2^{32+k}/d \rceil$ divides exactly ($7M - 2^{32+k} \le 2^k$ for $d$ = 7, in general $dM - 2^{32+k} \le 2^k$). Run it for $d$ = 3, 7, 10 and 1000 and compare with clang's output.
2. **A floating-point adder from integers (Part 2).** Implement addition of two positive FP32 numbers: unpack the fields, align with guard, round and sticky bits, add, normalize, and round to nearest even. *Predict first:* if you drop the sticky bit, will your adder still agree with the hardware?
3. **Summation (Part 3).** Plot the relative error of sequential, pairwise and Kahan summation of the FP32 value 0.1 for $n$ from 10 to $10^6$.
4. **Quantization (Part 4).** Quantize 4096 Gaussian samples to INT8, INT4 and MX-style FP4 (blocks of 32 with a power-of-two scale), and compare SQNR and bits per element.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Magic numbers | $d$ = 3: 0xAAAAAAAB, shift 33; $d$ = 7: needs 33 bits (clang's fix-up sequence); $d$ = 10: 0xCCCCCCCD, shift 35; $d$ = 1000: 0x10624DD3, shift 38 |
| 2 | Hand adder | Zero mismatches against the hardware on 100,000 random pairs. Without the sticky bit, some results differ by one ulp |
| 3 | Summation | Sequential error grows with $n$ and changes sign from binade to binade (−0.0144% at $10^5$, +0.958% at $10^6$); pairwise stays near $10^{-7}$ or below; Kahan stays at the final rounding |
| 4 | Quantization | About 6 dB of SQNR per bit for INT; MX FP4 at 4.25 bits per element beats per-tensor INT4 on Gaussian data |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-04.a | magic number for ÷ 1000 | 0x10624DD3 | — |
| Lab 14-04.b | total shift for ÷ 1000 | 38 | bits |
| Lab 14-04.c | hand-adder mismatches in 100,000 pairs | 0 | — |
| Lab 14-04.d | sequential relative error, n = 10⁵ | −0.0144 | % |

*These are recomputed by [verify_14_04.py](../../verify/verify_14_04.py), which compiles `x / 1000` with clang, runs its own integer-only FP32 adder against NumPy, and repeats the summation in FP32.*

## Discussion questions

1. Why does the sequential sum come out low at $n = 10^5$ but high at $n = 10^6$?
2. Your adder needed only three extra bits below the significand. Why not keep all the shifted-out bits?
3. Why does block scaling beat a single per-tensor scale on Gaussian data, even with fewer element bits?

### Answers

1. The error of each addition depends on the binade of the running sum. Each added 0.1 is rounded to a whole number of the sum's ulps, so the rounding goes the same way for every addition within a binade. Between 8192 and 16384 the ulp is $2^{-10}$, and $0.1/2^{-10} = 102.4$ rounds down to 102: each addition there adds slightly less than 0.1. Between 65,536 and 131,072 the ulp is $2^{-7}$, and 12.8 rounds up to 13: each adds slightly more. The total is a sum of these per-binade biases, so its sign depends on where the sum stops.
2. Only three things can affect the rounded result: the bit just below the last place (guard), the next one (round, needed if normalization shifts by one), and whether anything at all lies further down (sticky). Keeping 24 or more shifted-out bits would cost a wider adder for no change in the answer.
3. A per-tensor scale must cover the largest sample in 4096, about four standard deviations, so most samples fall in the coarse low end of the INT4 grid. A block of 32 has a smaller maximum, typically two to two and a half standard deviations, so its scale fits the data more tightly. The 8-bit scale per block adds only a quarter of a bit per element.

## Optional hardware extension

On any RISC-V board with the F extension, time a loop of `fdiv.s` against a loop of `fmul.s`, and a loop of `divu` against the MULHU sequence for $d$ = 10, using the cycle counter. The ratios show why compilers work so hard to avoid division.
