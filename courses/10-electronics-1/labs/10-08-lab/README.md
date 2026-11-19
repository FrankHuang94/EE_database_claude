# Lab 10-08 · Current Sources and Current Mirrors

Chapter: [10-08 Current Sources and Current Mirrors](../../chapters/10-08-current-sources-and-mirrors.md)

## Objective

Measure the output characteristics of basic and cascode mirrors with the full square law, see how random threshold mismatch spreads mirror ratios, compare the bipolar mirrors' base-current errors across β, and measure a resistor reference's supply sensitivity.

## Background

Mirror errors and output resistance (§3.2–3.4), mismatch and Pelgrom's area law (§3.5) and bias distribution (§3.6). Part 1 uses the large-signal model, including triode operation and channel-length modulation, so its output resistance differs somewhat from the small-signal estimate $2r_o + g_mr_o^2$ with $r_o = 1/(\lambda I)$.

## Files

- [10-08-mirrors.ipynb](10-08-mirrors.ipynb): the notebook (Parts 1–4).
- [mirrors.cir](mirrors.cir): ngspice checks of Examples 10-08.1 and 10-08.7.

## Procedure

1. **Output characteristics (Part 1).** *Predict first:* at what output voltage does the cascode mirror reach 99% of $I_{ref}$? Then sweep both mirrors from 0 to 3 V and differentiate to get output resistance.
2. **Mismatch Monte Carlo (Part 2, the chapter's guided exercise).** *Predict first:* the fraction of 10,000 pairs ($WL$ = 10 µm², $V_{ov}$ = 0.2 V) with more than 2% current error. Then sample threshold differences and count.
3. **Bipolar mirrors across β (Part 3).** Plot the ratio error of the basic, β-helper and Wilson mirrors from β = 20 to 500.
4. **Supply sensitivity (Part 4).** Sweep Example 10-08.7's supply from 2.5 to 4 V and plot the reference current and its sensitivity.
5. **ngspice.** Run `python tools/run_spice.py 10-08`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Cascode | flat above about 0.9 V; output resistance in megohms |
| 2 | Monte Carlo | close to the normal-distribution prediction of about 7% |
| 3 | β errors | basic falls as 2/β; helper and Wilson as about 2/β² |
| 4 | Supply | about 37%/V at 3.3 V |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-08.a | cascode R_out at 2 V, large-signal | 3044 | kΩ |
| Lab 10-08.b | output voltage for 99% of I_ref | 0.894 | V |
| Lab 10-08.c | Monte Carlo fraction above 2% | 6.58 | % |
| Lab 10-08.d | normal-distribution prediction | 7.08 | % |
| Lab 10-08.e | basic error at β = 20 | -9.09 | % |
| Lab 10-08.f | β-helper error at β = 20 | -0.474 | % |
| Lab 10-08.g | Wilson error at β = 20 | -0.452 | % |
| Lab 10-08.h | supply sensitivity at 3.3 V | 37.20 | %/V |

## Discussion questions

1. The cascode reaches 99% of $I_{ref}$ at 0.89 V, below the chapter's compliance estimate of 1.17 V. Why, and which number should a designer use?
2. The Monte Carlo gives 6.58%, the formula 7.08%. Is the difference significant?
3. Why do the β-helper and Wilson errors nearly coincide at low β but differ in output resistance?

### Answers

1. Below $V_{TN} + 2V_{ov}$ the upper transistor M4 enters triode, but a triode device still carries current; the output current sags gradually rather than collapsing. The compliance estimate marks where the output resistance is high, not where the current first reaches a given fraction. A designer should use the voltage at which the *output resistance* (or gain, for an active load) still meets its specification, usually close to the estimate.
2. With 10,000 samples, the count's standard deviation is $\sqrt{N p(1 - p)}$ ≈ 26 pairs, or 0.26 percentage points; 0.5 points is about two standard errors, so a difference this size occurs by chance only a few percent of the time. Another seed gives a different value; the formula is the expectation (03-05).
3. Both reduce the reference's base-current loss to about $2/\beta^2$, so their ratio errors agree. Only the Wilson has a feedback loop that holds the output transistor's emitter current, which raises its output resistance to about $\beta r_o/2$; the helper does not change the output transistor.

## Optional hardware extension

Build a basic mirror from two transistors of a matched pair (a dual-transistor package) and from two separate transistors, feed 1 mA, and compare the output currents at a few output voltages. The packaged pair shares temperature and process; the separate devices show both mismatch and Early-effect error.
