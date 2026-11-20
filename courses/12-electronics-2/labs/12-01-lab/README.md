# Lab 12-01 · Differential Pairs

Chapter: [12-01 Differential Pairs](../../chapters/12-01-differential-pairs.md)

## Objective

Solve both pairs' large-signal transfer from their device equations and compare with the closed forms; compute differential gain, common-mode gain and CMRR from the full circuit rather than from half-circuits; check an offset budget by Monte Carlo; and see why a resistor-ratio trim removes a bipolar pair's drift while a fixed voltage trim does not. Confirm the MOS pair's split, gain and common-mode behavior in ngspice.

## Background

The BJT pair's tanh characteristic (§3.1), the MOS pair's square-law characteristic (§3.2), half-circuits and CMRR (§3.3), offset from mismatch and Pelgrom's law (§3.5), and drift (§3.5).

## Files

- [12-01-differential-pairs.ipynb](12-01-differential-pairs.ipynb): the notebook (Parts 1–4).
- [diffpair.cir](diffpair.cir): ngspice netlist of the MOS pair of Examples 12-01.2 and 12-01.3, with ideal loads for the current split, resistor loads for the differential gain, and a 50 kΩ tail, with and without 1% load mismatch, for the common-mode gains. Run with `ngspice -b diffpair.cir`, or `python tools/run_spice.py 12-01` from the repository root.

## Procedure

1. **Large-signal transfer (Part 1).** Solve each pair's split for inputs from −0.6 V to 0.6 V by finding the shared-node voltage that satisfies the tail constraint. Compare with $\tanh(v_{id}/2V_T)$ and with the square-law formula.
2. **Gains and CMRR (Part 2).** Build the small-signal circuit (two transconductances, two drain loads, the tail resistance) as a nodal matrix and solve it for a differential and a common-mode drive, with load mismatch of 0.1%, 1% and 5%.
3. **Monte Carlo offset (Part 3, the chapter's guided exercise).** *Predict first:* in Example 12-01.4's budget, what does halving the overdrive (four times the width) do to σ($V_{OS}$)? Then draw 4000 sets of threshold, current-factor and load mismatch, solve each mismatched pair for its balancing input, and compare the spread with the budget. Repeat at half the overdrive.
4. **Drift and trim (Part 4).** For a bipolar pair with a 1.0 mV offset at 300 K, compute the offset from 250 K to 400 K untrimmed, trimmed by a collector-resistor ratio, and trimmed by a fixed voltage.
5. **ngspice.** Run `diffpair.cir` and compare the split at 0.2 V, the differential gain and the two common-mode gains with Examples 12-01.2 and 12-01.3.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Solved splits against the formulas | Agreement to rounding |
| 2 | Gains and single-ended CMRR | 6.325, 3.162, 0.09844; 32.12 (30.1 dB) |
| 2 | Differential CMRR against mismatch | Falls 20 dB per decade of mismatch; 76.2 dB at 1% |
| 3 | Monte Carlo against the budget | Agreement within the sampling error (about 1%) |
| 4 | Drift | Untrimmed offset proportional to $T$; ratio trim null at every temperature; voltage trim leaves 3.33 µV/K |
| ngspice | Split, gain, common-mode gains | 160 and 40 µA; 6.325; 0.09844 and 9.844 × 10⁻⁴ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-01.a | offset budget, Example 12-01.4 | 2.086 | mV |
| Lab 12-01.b | Monte Carlo σ of the offset | 2.08 | mV |
| Lab 12-01.c | budget at half the overdrive | 0.985 | mV |

*Lab 12-01.a and .c are recomputed by [verify_12_01.py](../../verify/verify_12_01.py) from offset sensitivities; .b is checked against the verify script's own independent Monte Carlo run within 4%, about four times its sampling error.*

## Discussion questions

1. The MOS pair's split in Part 1 assumes both transistors stay saturated. What happens with Example 12-01.2's 10 kΩ loads at $v_{id}$ = 0.2 V, and what kind of load avoids it?
2. Part 2's differential CMRR depends on mismatch, not on the tail. Is the tail resistance then irrelevant for a fully differential circuit?
3. In Part 3, why does the Monte Carlo spread match a budget built from first-order (linearized) sensitivities so well?

### Answers

1. The 160 µA in M1 would drop 1.6 V across its load and pull its drain to 0.2 V, far below its gate minus $V_{TN}$: M1 would enter triode, its current would fall, and the split would differ from the formula. Loads that keep the drains high while passing large currents, such as current mirrors (12-02), or a smaller $R_D$ avoid it. The netlist measures the split with ideal ammeter loads for that reason.
2. No. The differential CMRR is $(R_D/\Delta R_D)(1 + 2g_mR_{SS})$: the tail still multiplies it, and a large common-mode signal on a weak tail also moves the operating point and can push the pair out of its common-mode range.
3. The offsets are a few millivolts, far below the overdrive, so the balancing input depends on each mismatch almost linearly, and independent normal contributions to a linear function add in variance exactly.

## Optional hardware extension

Build a pair from a matched-transistor array (for example a five-transistor array in one package) with 10 kΩ collector resistors and a resistor tail. Measure the offset by finding the input that balances the collectors, then warm the package with a hair dryer and watch the offset change; compare the change with $V_{OS}/T$.
