# Lab 08-01 · Number Systems and Codes

**Chapter:** [08-01](../../chapters/08-01-number-systems-and-codes.md) · **Notebook:** [08-01-number-systems.ipynb](08-01-number-systems.ipynb) · **Time:** about 2 hours

## Objective

1. Convert between bases in code, and see why 0.1 has no finite binary form.
2. Test the two's-complement overflow rules on every pair of 4-bit numbers, not just a few examples.
3. Enumerate every value of the FP8 formats and compare their spacing with FP16 and bfloat16.
4. Measure how often parity, Hamming SEC, SEC-DED and a CRC let a corrupted word through, and see how those rates scale with the bit-error probability.
5. Build and test Gray-code converters and a Hamming(7,4) encoder and decoder in Verilog.

## Background

Chapter sections 3.1 to 3.8 and Examples 08-01.1 to 08-01.7. You need Python with NumPy and Matplotlib, and Icarus Verilog for the hardware part (see [SETUP.md](../../../../SETUP.md)). This is the curriculum's first Verilog lab: you only need to read the modules, not write them. Verilog itself is taught in [08-05](../../chapters/08-05-verilog-and-testbenches.md). Read `assign g = b ^ (b >> 1);` as "the output wire g always equals b XOR (b shifted right by one)".

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-01-number-systems.ipynb](08-01-number-systems.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [gray.v](gray.v) | `bin2gray` and `gray2bin`, parameterized by width | `codes_tb.v` |
| [hamming74.v](hamming74.v) | `hamming74_enc` (4 data bits to a 7-bit word) and `hamming74_dec` (syndrome, single-error correction) | `codes_tb.v` |
| [codes_top.v](codes_top.v) | A top level wiring the converters and a Hamming channel together, with an injectable error mask | Lint only |
| [codes_tb.v](codes_tb.v) | Self-checking testbench: every 4-bit Gray round trip, every data word with every single-bit error | Prints `TEST PASSED` |

Run the testbench from the repository root:

```bash
python tools/run_hdl.py
```

or directly:

```bash
iverilog -g2012 -o /tmp/codes courses/08-digital-logic-design/labs/08-01-lab/codes_tb.v courses/08-digital-logic-design/labs/08-01-lab/gray.v courses/08-digital-logic-design/labs/08-01-lab/hamming74.v && vvp /tmp/codes
```

## Procedure

1. **Bases (Part 1).** *Predict first:* how many of the decimal fractions 0.1, 0.2, …, 0.9 have a terminating binary expansion? Then run the converter and check.
2. **Overflow (Part 2).** *Predict first:* of the 256 ordered pairs of 4-bit two's-complement numbers, how many sums overflow? (Hint: count the pairs whose true sum is above 7 or below −8.) The notebook tests the rules "overflow iff the operands share a sign that the result lacks" and "overflow iff $c_{n-1} \ne c_n$" on all 256 pairs.
3. **Floating point (Part 3).** *Predict first:* how many of E4M3's 256 bit patterns are finite numbers, and where on the number line is its spacing equal to 1? Then enumerate both FP8 formats and plot the spacing of every format against magnitude.
4. **Noisy channel (Part 4, the chapter's guided exercise).** Four schemes each protect one code word sent over a channel that flips each bit independently with probability $p$:
   - **parity**: 8 data bits plus an even-parity bit (9 bits), detection only;
   - **SEC**: Hamming(7,4), always correcting whatever the syndrome points at;
   - **SEC-DED**: Hamming(7,4) plus an overall parity bit (8 bits), correcting single errors and flagging double errors;
   - **CRC**: the same 7-bit words read as a CRC with $g(x) = x^3 + x + 1$ (Example 08-01.7), used for detection only.

   A word is a **silent failure** if the receiver delivers wrong data without raising a flag. *Predict first:* when $p$ rises from $10^{-3}$ to $10^{-2}$, by what factor does each scheme's silent-failure probability rise? Then compute it exactly (the notebook sums over every possible error pattern), and confirm by Monte Carlo at larger $p$.
5. **Verilog.** Read `gray.v` and `hamming74.v`, run the testbench, then edit the testbench to inject a *double* error and watch the decoder report a wrong data word with `corrected = 1`, the silent failure of Part 4.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | terminating fractions | only 0.5 (= 1/2) among the nine; the others repeat forever |
| 2 | overflowing pairs | 64 of 256 (28 too positive, 36 too negative); both overflow rules agree with the true sum on every pair |
| 3 | E4M3 | 254 finite bit patterns, +0 and −0 counted separately (126 positive values, the largest 448); spacing 1 between 8 and 16 |
| 4 | silent failures | see the key; the factors are close to 100 for parity and SEC and close to 1000 for SEC-DED and the CRC |
| Verilog | testbench | `TEST PASSED`; with a double error injected, the decoder "corrects" a third bit and outputs wrong data |

Part 4's exact silent-failure probabilities per code word:

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-01.a | parity (9 bits), p = 10⁻³ | 3.575e-5 | — |
| Lab 08-01.b | parity (9 bits), p = 10⁻² | 3.357e-3 | — |
| Lab 08-01.c | parity, ratio of b to a | 93.9 | — |
| Lab 08-01.d | SEC Hamming(7,4), p = 10⁻³ | 2.093e-5 | — |
| Lab 08-01.e | SEC Hamming(7,4), p = 10⁻² | 2.031e-3 | — |
| Lab 08-01.f | SEC, ratio of e to d | 97.0 | — |
| Lab 08-01.g | SEC-DED (8,4), p = 10⁻³ | 5.573e-8 | — |
| Lab 08-01.h | SEC-DED (8,4), p = 10⁻² | 5.340e-5 | — |
| Lab 08-01.i | SEC-DED, ratio of h to g | 958 | — |
| Lab 08-01.j | CRC x³ + x + 1 (7 bits), detection only, p = 10⁻³ | 6.979e-9 | — |
| Lab 08-01.k | CRC x³ + x + 1 (7 bits), detection only, p = 10⁻² | 6.792e-6 | — |
| Lab 08-01.l | CRC, ratio of k to j | 973 | — |
| Lab 08-01.m | SEC-DED words flagged uncorrectable, p = 10⁻³ | 2.783e-5 | — |
| Lab 08-01.n | overflowing 4-bit pairs | 64 | — |
| Lab 08-01.o | finite E4M3 bit patterns, +0 and −0 counted separately | 254 | — |

**Reading the key.** Each scheme's silent failures start at a particular number of bit errors $w$, and their probability is then about $A\,p^{w}$, where $A$ counts the bad patterns of that weight. Parity fails on 2 errors ($A = \binom{9}{2} = 36$) and SEC miscorrects every 2-error pattern ($A = \binom{7}{2} = 21$): both scale as $p^2$, so a tenfold rise in $p$ costs about 100×. SEC-DED fails first on 3 errors ($A = \binom{8}{3} = 56$) and the CRC on the 7 weight-3 code words, so both scale as $p^3$: about 1000×. The ratios fall a little short of 100 and 1000 because of the $(1-p)^{n-w}$ factors and, slightly, the higher-weight terms. Lines g and m together show SEC-DED's real bargain: at $p = 10^{-3}$ about 500 times as many words are flagged (2.783e-5) as slip through (5.573e-8), and a flagged word can be re-read or reported, which a silent one cannot.

## Discussion questions

1. The CRC and the SEC code here use the *same* 16 code words, yet the CRC's silent-failure rate is about 3000 times lower at $p = 10^{-3}$. Why?
2. At $p = 10^{-3}$, parity lets through about 640 times as many bad words as SEC-DED. Parity spends 1 bit in 9 on checking and SEC-DED 4 bits in 8. Is the extra redundancy the whole explanation?
3. Server memory uses SEC-DED rather than plain SEC. Using lines d, g and m, explain why.
4. The Monte Carlo estimate at $p = 10^{-3}$ for SEC-DED would need about how many simulated words to see 100 failures, and what does that say about measuring very reliable systems?
5. In the Verilog decoder, an error in a check bit (positions 1, 2 or 4) leaves the data output untouched. Why is that correct?

<details><summary>Answers to the discussion questions</summary>

1. A detector only needs the received word to be a non-code word, which fails only when the error pattern *is* a code word (weight 3 or more, since $d_{min} = 3$). A corrector must also guess which code word was sent; any 2-error pattern lands at distance 1 from a wrong code word, and the decoder confidently moves there. Correction spends the code's distance on fixing errors; detection spends all of it on noticing them. Hence $21p^2$ against $7p^3$, a ratio of $3/p$ ≈ 3000 at $p = 10^{-3}$.
2. No. What matters is the minimum distance the redundancy buys. Parity has $d_{min} = 2$, so every 2-error pattern escapes, and a 9-bit word has 36 of them. SEC-DED has $d_{min} = 4$, so a silent failure needs at least 3 errors. Redundancy spent badly buys little: repeating each data bit twice doubles the word yet still gives $d_{min} = 2$. Spent well, it is cheap: the (72,64) SEC-DED code of the chapter reaches $d_{min} = 4$ with 12.5% overhead.
3. Plain SEC turns every double error into a silent failure (line d, $2.093 \times 10^{-5}$). SEC-DED, for one more bit, converts nearly all of those into flagged events (line m, $2.783 \times 10^{-5}$) and leaves only triple errors silent (line g, $5.573 \times 10^{-8}$). A flagged memory error can crash the job cleanly or trigger a retry; silent data corruption propagates into results.
4. About $100 / (5.573 \times 10^{-8}) \approx 1.8 \times 10^{9}$ words. Very reliable systems cannot be qualified by brute-force counting alone; engineers combine analysis (as in this key), accelerated testing at high error rates (as the notebook's Monte Carlo does at larger $p$) and field data.
5. The data bits are positions 3, 5, 6 and 7. A syndrome of 1, 2 or 4 names a check-bit position, so the decoder knows the data bits arrived intact and has nothing to fix in them; it flags `corrected` so the event can still be logged.

</details>

## Optional hardware

Any FPGA board with four switches and seven LEDs can host `codes_top.v`: wire the data switches to `d`, set the error mask from four more switches (or a push button that flips one chosen bit), and show `d_out`, `syndrome` and `corrected` on LEDs. A no-board alternative is a breadboard with 74HC86 quad XOR gates: three of them compute the Hamming check bits of a 4-bit DIP-switch input, and LEDs show the 7-bit code word.
