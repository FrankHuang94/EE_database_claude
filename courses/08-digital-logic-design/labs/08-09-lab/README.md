# Lab 08-09 · Arithmetic Circuits

**Chapter:** [08-09](../../chapters/08-09-arithmetic-circuits.md) · **Notebook:** [08-09-arithmetic.ipynb](08-09-arithmetic.ipynb) · **Time:** about 2.5 hours

## Objective

1. Build ripple-carry, Brent–Kung, Sklansky and Kogge–Stone adders as prefix networks, check them, and compare their delay, operator count and fan-out from 4 to 64 bits.
2. Build Dadda multipliers bit by bit and confirm the chapter's adder count.
3. Recode multipliers in radix-4 Booth digits and measure how many partial products remain.
4. Measure the bias of truncation against rounding, and the SQNR of quantized sines against $6.02b + 1.76$ dB.
5. Write and test adders, a multiplier, a barrel shifter and a saturating Q1.15 multiplier in Verilog.

## Background

Chapter sections 3.1 to 3.8 and Examples 08-09.1 to 08-09.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-09-arithmetic.ipynb](08-09-arithmetic.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [arith.v](arith.v) | Full adder `fa`, ripple-carry adder `rca`, 16-bit Kogge–Stone adder `ks16` (generate loops, one vector per prefix level), 8 × 8 array multiplier `mul8`, 32-bit barrel shifter `barrel32`, Q1.15 multiplier `q15_mul` with rounding and saturation | `arith_tb.v` |
| [arith_top.v](arith_top.v) | A top level for lint tools | Lint only |
| [arith_tb.v](arith_tb.v) | Random tests of both adders and the shifter against `+` and `<<`, all 65 536 multiplier input pairs against `*`, and the Q1.15 multiplier against an integer reference including Example 08-09.7 and the saturation corner | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_notebooks.py 08-09
```

```bash
python tools/run_hdl.py
```

## Procedure

1. **Prefix adders (Part 1, the chapter's guided exercise).** *Predict first:* from 16 to 64 bits, how do a Kogge–Stone adder's delay and operator count grow? The notebook checks every network on random additions and times it in the unit-delay model.
2. **Dadda multipliers (Part 2).** Run the bit-level construction for 4 to 32 bits and compare its full-adder count with $n^2 - 4n + 3$.
3. **Booth recoding (Part 3).** *Predict first:* how many of the 4 Booth digits of a random signed 8-bit multiplier are nonzero on average?
4. **Fixed point (Part 4).** Compare truncation and rounding on 200 000 random Q1.15 products, and measure the SQNR of 8-, 12- and 16-bit sines.
5. **Verilog.** Run `arith_tb.v`. Then change `q15_mul` to truncate (delete the `+ 32'sd16384`) and predict which check fails first.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | prefix adders | the chapter's table; Kogge–Stone's delay grows 1.4 times and its operators 6.55 times from 16 to 64 bits; Sklansky's fan-out reaches 32 at 64 bits |
| 2 | Dadda | full adders exactly $n^2 - 4n + 3$, half adders $n - 1$, levels 2 to 8 for 4 to 32 bits |
| 3 | Booth | an average of 3.000 nonzero digits of 4 (and 4 of 8 bits are 1 on average) |
| 4 | fixed point | truncation biased by about −0.5 LSB, rounding by almost 0; SQNR within a few hundredths of a dB of the formula |
| Verilog | testbench | `TEST PASSED`; with truncation, the first failure is the half-LSB case $1 \times 16384$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-09.a | Kogge–Stone delay growth, 16 to 64 bits | 1.40 | — |
| Lab 08-09.b | Kogge–Stone operator growth, 16 to 64 bits | 6.55 | — |
| Lab 08-09.c | Sklansky fan-out at 64 bits | 32 | — |
| Lab 08-09.d | Dadda 32 × 32 full adders | 899 | — |
| Lab 08-09.e | Dadda 32 × 32 levels | 8 | — |
| Lab 08-09.f | average nonzero Booth digits, signed 8-bit | 3.000 | — |
| Lab 08-09.g | measured truncation bias | -0.50 | LSB |
| Lab 08-09.h | measured SQNR, 16 bits | 98.07 | dB |
| Lab 08-09.i | multiplier input pairs tested | 65536 | — |

**Reading the key.** Kogge–Stone's delay goes from 10 to 14 units ($14/10 = 1.40$) while its operators go from 49 to 321 ($n\log_2 n - n + 1$; $321/49 = 6.55$). The Booth average follows from each digit being zero for exactly a quarter of the multipliers. The measured SQNR uses a sine of amplitude $2^{15} - 1$ codes with 1031 cycles in $2^{16}$ samples; it sits within 0.01 dB of the formula's 98.08 dB.

## Discussion questions

1. Why does the Kogge–Stone adder in `arith.v` keep each prefix level in its own vector, rather than one long vector holding all levels?
2. Which test in `arith_tb.v` would catch a Kogge–Stone adder that ignored the carry-in, and which would catch one that got the carries right but the sum wrong?
3. Why does the testbench check the multiplier exhaustively but the 32-bit adder only on random inputs?
4. What fails first when `q15_mul` truncates instead of rounding, and why does that one case reveal it?
5. A 64-bit Kogge–Stone adder has 321 operators against 63 for ripple carry. In which products would you still choose Kogge–Stone, and in which ripple carry?

<details><summary>Answers to the discussion questions</summary>

1. With one vector, a bit of level 2 is computed from other bits of the same vector, and Verilator's lint reports `UNOPTFLAT`, a possible combinational loop through the vector (there is none, but the tool reasons about whole signals). Separate vectors per level make the level-by-level structure explicit, lint cleanly, and match the diagram of the network.
2. Ignoring the carry-in fails the random tests about half the time (whenever `cin` = 1) and the directed test 0xFFFF + 0 + 1, which needs the carry-in to ripple through all 16 bits. A wrong sum with right carries fails the random comparisons of `s` even when `cout` matches; checking `{cout, s}` together catches both.
3. The 8 × 8 multiplier has $2^{16}$ = 65 536 input pairs, which Icarus simulates in moments. The 32-bit adder with carry-in has $2^{65}$, far too many; random tests plus directed corner cases (all-ones propagation) give confidence, and formal equivalence checking against a reference would give a proof ([19-13](../../../19-digital-vlsi-design/chapters/19-13-verification-methods.md)).
4. The check `1 × 16384` (that is, $2^{-15} \times 0.5$, exactly half an output LSB) fails first: rounding gives 1 and truncation gives 0. Random operands would find the bias eventually, but this directed case isolates it, which is why testbenches include the rounding boundary explicitly.
5. Kogge–Stone (or a sparse prefix network) where the adder limits the clock: CPU integer pipelines, address generation, floating-point units at high frequency. Ripple carry where area and power matter more than speed and the clock is slow: always-on counters and timers in low-power MCUs, or small adders whose delay is not critical. Synthesis tools make this choice automatically from the timing constraint, which is why the same RTL `+` becomes different circuits in different products.

</details>

## Optional hardware

On an FPGA board, synthesize `rca #(.N(32))` and a `+` of the same width, and compare the timing reports: FPGAs contain dedicated carry chains, so their ripple-carry adders are much faster than LUT-based logic would suggest, and the synthesized `+` uses those chains. This is a case where the platform changes the best architecture ([08-12](../../chapters/08-12-fpga-implementation-flow.md)).
