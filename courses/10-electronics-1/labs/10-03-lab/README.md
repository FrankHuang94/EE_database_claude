# Lab 10-03 · BJT DC Operation and Biasing

Chapter: [10-03 BJT DC Operation and Biasing](../../chapters/10-03-bjt-dc-operation-and-biasing.md)

## Objective

Measure, by simulation, how three bias networks respond to the spread of β and $V_{BE}$ that a data sheet allows, watch thermal runaway happen when the thermal loop gain exceeds one, and see why a saturated switch turns off late.

## Background

The chapter's constant-$V_{BE}$ model (§3.1–3.2), the four-resistor bias and its sensitivities (§3.4), the mirror (§3.5), the saturated switch (§3.6) and the thermal loop (§3.7).

## Files

- [10-03-bjt-bias.ipynb](10-03-bjt-bias.ipynb): the notebook (Parts 1–4).
- [bjt_bias.cir](bjt_bias.cir): ngspice operating point of Example 10-03.3 with a Gummel–Poon transistor.

## Procedure

1. **β sweep (Part 1).** *Predict first:* which of the three bias networks of Figure 2 saturates first as β rises? Then sweep β from 50 to 400 and mark the edge of saturation for each.
2. **Monte Carlo (Part 2, the chapter's guided exercise).** *Predict first:* the ratio of the largest to the smallest $I_C$ when β is uniform between 100 and 300 and $V_{BE}$ uniform within ±20 mV. Then run 20,000 samples through Example 10-03.3's bias.
3. **Thermal runaway (Part 3).** Simulate a transistor with a thermal time constant, heated by its own dissipation, with $V_{BE}$ fixed, for collector currents on either side of the runaway current of Problem 10-03.10; then add $R_E$.
4. **Switch turn-off (Part 4).** With the charge-control model of 09-07, simulate turning off a saturated switch at forced β = 10 and forced β = 3, and compare the storage delays.
5. **ngspice.** Run `python tools/run_spice.py 10-03`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | First to saturate | base-current bias, then collector feedback; the four-resistor bias never does in this range |
| 2 | Spread | under 10% end to end |
| 3 | Runaway | the fixed-$V_{BE}$ transistor's current grows without limit above about 13 mA; $R_E$ stops it |
| 4 | Storage delay | longer with heavier overdrive |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-03.a | largest over smallest I_C | 1.089 | — |
| Lab 10-03.b | σ of I_C | 1.76 | % |
| Lab 10-03.c | mean I_C | 1.338 | mA |

## Discussion questions

1. The Monte Carlo's end-to-end spread (1.089) exceeds the chapter's 1.06 from β alone. Where does the rest come from, and why do the two effects simply add here?
2. In Part 3, why does a small change in collector current near the runaway threshold change the outcome from a stable rise to unbounded growth?
3. Why does a heavier base overdrive lengthen the storage delay?

### Answers

1. The ±20 mV of $V_{BE}$ moves the current by about ±1.4% (§5 of the chapter), and the extremes of β and $V_{BE}$ can occur together: 1.06 × (1.014/0.986) ≈ 1.09. The two effects add because each enters the denominator or numerator of $I_E = (V_{Th} - V_{BE})/(R_E + R_{Th}/(\beta + 1))$ independently, and both are small.
2. Below the threshold, each degree of heating raises the current by less than enough to cause another degree, so the series of increments converges to a slightly higher operating point. Above it, each increment causes a larger one, and the series diverges: the loop gain passing one is the boundary between the two.
3. The extra base current beyond what the collector needs ($I_B - I_C/\beta$) is stored as excess charge in the base and collector (09-07 §3.10). At turn-off that charge must be removed before the collector current can fall, so more overdrive means more stored charge and a longer delay.

## Optional hardware extension

With a 2N3904, the resistor values of Example 10-03.3 and a 12 V supply, measure $V_E$ and $V_C$, swap in transistors from several batches (or a 2N2222) to see the β spread barely move the current, then warm the transistor with a hair dryer and log $V_E$.
