# Lab 00-04 · Your Toolchain, End to End

**Chapter:** [00-04](../../chapters/00-04-toolchain-walkthrough.md) · **Notebook:** [00-04-toolchain.ipynb](00-04-toolchain.ipynb) · **Time:** about 1 hour (plus installation)

## Objective

Install the tools, prove they work, and learn to read and trust (or distrust) their output.

## Files

| File | Purpose | Checked against |
|---|---|---|
| [divider.cir](divider.cir) | DC operating point of two dividers, one with the "M" typo, plus Problem 00-04.4 | Examples 00-04.1–2, Problem 00-04.4 |
| [rc_ac.cir](rc_ac.cir) | AC sweep of two RC low-pass filters | Example 00-04.5, Problem 00-04.5 |
| [mux2.v](mux2.v), [mux2_tb.v](mux2_tb.v) | A 2:1 multiplexer and its exhaustive self-checking testbench | Example 00-04.4 |
| [00-04-toolchain.ipynb](00-04-toolchain.ipynb) | Floating-point experiments, a Newton–Raphson diode solver, and running the tools from Python | Built-in asserts |

## Procedure

1. Install the toolchain following [SETUP.md](../../../../SETUP.md), then run the smoke tests from the repository root:

   ```bash
   python tools/run_spice.py smoke
   ```

   ```bash
   python tools/run_hdl.py
   ```

2. Run this lab's netlists and testbench. **Predict each result first.**

   ```bash
   python tools/run_spice.py 00-04
   ```

   To see the raw simulator output, run `ngspice -b divider.cir` from this folder.
3. Open the notebook and run all cells. Work through the predict prompts.
4. **Break something on purpose.**
   - Edit [../../chapters/00-04-toolchain-walkthrough.md](../../chapters/00-04-toolchain-walkthrough.md): in the answer key, change the value for `Ex 00-04.1a` from `2.000` to `2.010`.
   - Run `python tools/run_verify.py 00-04` and read the failure message.
   - Then restore the value: run `git checkout -- courses/00-orientation/chapters/00-04-toolchain-walkthrough.md`.

   You have just seen how this repository protects every number.
5. If GTKWave is installed, open `mux2_tb.vcd` (created by the testbench) and look at the eight input combinations.

## Expected results

| Exercise | Expected |
|---|---|
| `divider.cir` | vout = 2 V; isrc = −0.001 A; vtypo = 5 V (the "M" trap); vb4 = 2.5 V |
| `rc_ac.cir` | f3db_1 = 159.2 Hz; f3db_2 = 1.592 kHz; db_10k_2 = −16.07 dB |
| `mux2_tb.v` | "Checked 8 vectors, 0 errors" and TEST PASSED |
| Newton from 0.70 V | converges to $|\Delta V| < 1$ nV in 5 iterations; $V_D = 0.6925$ V |
| Deliberate break (step 4) | the verify script prints `FAIL Ex 00-04.1a computed 2, published 2.010 (±0.0005)` and exits with an error |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 00-04.1 | Newton iterations from 0.70 V to 1 nV | 5 | — |

## Discussion questions

1. The "M" typo produced a perfectly plausible-looking 5 V. What habits catch errors like this before they reach a design review?
2. Why does Newton–Raphson converge so quickly near the answer, yet badly from 0.60 V? Sketch $g(V)$ and the tangent line at 0.60 V.
3. What is the relationship between an answer key in this repository and a testbench in a chip project?

## Optional hardware version

1. Build the divider of Example 00-04.1 with 3 kΩ and 2 kΩ (use 3.3 kΩ and 2.2 kΩ if those are what you have), and measure $V_{out}$ with a multimeter.
2. Compare with the simulation using your actual measured resistances. Agreement within about 1% is normal for 1% resistors, and this is your first model-to-hardware correlation.
