# Lab 10-09 · Real Op-Amps: Non-Idealities

Chapter: [10-09 Real Op-Amps: Non-Idealities](../../chapters/10-09-real-op-amps-nonidealities.md)

## Objective

Quantify the gap between an ideal and a real op-amp: in-band accuracy against frequency, the shape and amplitude of a slew-limited sine, a full DC error budget for a bridge amplifier with two different parts, and figures of merit across three current data sheets.

## Background

The single-pole model and GBW (§3.2), slew rate (§3.3), DC errors, CMRR and PSRR (§3.4–3.5), and the data-sheet values of the chapter's sources [1–3]. Part 3's budget uses guaranteed (maximum or minimum) values where the data sheet gives them; for the TLV9062's drift, which has only a typical value, it uses that and says so.

## Files

- [10-09-opamps.ipynb](10-09-opamps.ipynb): the notebook (Parts 1–4).
- [opamp_model.cir](opamp_model.cir): a single-pole op-amp macromodel in ngspice confirming Examples 10-09.1 and 10-09.2.
- [slew.cir](slew.cir): ngspice slew-limited follower (Part 2): an integrator whose input current is clipped at SR × C.

## Procedure

1. **In-band error (Part 1).** *Predict first:* up to what frequency does a TLV9062 at a noise gain of 10 hold 0.1% magnitude accuracy? Then plot magnitude and phase error against frequency for noise gains of 1, 10 and 100.
2. **Slew-limited sine (Part 2, the chapter's guided exercise).** *Predict first:* the output amplitude of a TLV9062 follower driven with 2.5 V peak at 800 kHz. Then simulate the slew-limited response and plot it with the input.
3. **DC budget (Part 3).** For Example 10-09.5's bridge (350 Ω arms, 2.5 V common mode on a 5 V supply, 0.1 V of supply variation, 25 to 125 °C), tabulate offset, drift, bias-current, CMRR and PSRR terms for the OPA333 and the TLV9062, and compare worst-case and root-sum-square totals.
4. **Figures of merit (Part 4).** Compute GBW per milliampere of quiescent current for the three parts.
5. **ngspice.** Run `python tools/run_spice.py 10-09`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | 0.1% bandwidth | about 4.5% of the closed-loop bandwidth |
| 2 | Output | a near-triangle with ±6.5 V/µs slopes, about 2 V peak |
| 3 | Budget | the OPA333's total is about 15 µV, dominated by offset and drift; the TLV9062's is millivolts, dominated by offset; the CMRR term is zero because the common mode sits at the data sheets' $V_S/2$ test condition |
| 4 | GBW per mA | similar for the two CMOS parts, lower for the low-noise bipolar part (noise costs current) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-09.a | 0.1% bandwidth, TLV9062 at noise gain 10 | 44.755 | kHz |
| Lab 10-09.b | slew-limited output peak | 1.982 | V |
| Lab 10-09.c | linear-model output peak | 2.492 | V |
| Lab 10-09.d | OPA333 worst-case total | 15.535 | µV |
| Lab 10-09.e | OPA333 RSS total | 11.19 | µV |
| Lab 10-09.f | TLV9062 worst-case total | 1.661 | mV |
| Lab 10-09.g | TLV9062 RSS total | 1.601 | mV |
| Lab 10-09.h | TLV9062 GBW per mA | 18.59 | MHz/mA |
| Lab 10-09.i | OPA333 GBW per mA | 20.59 | MHz/mA |
| Lab 10-09.j | OPA1611 GBW per mA | 11.11 | MHz/mA |

## Discussion questions

1. In Part 2 the output peak (1.98 V) is lower than the linear model's (2.49 V), and the waveform is no longer a sine. Which would an FFT show first as you raise the frequency: amplitude loss or harmonics?
2. Why is the root-sum-square total smaller than the worst case, and when is it the right number to quote?
3. The OPA1611 has the lowest GBW per milliampere. What does it buy with its current instead?

### Answers

1. Harmonics. Once the slope of the input exceeds the slew rate for part of each cycle, the output turns that part into a straight line, adding odd harmonics, before the fundamental's amplitude falls much; well above $f_{FP}$ the output becomes a triangle whose amplitude falls as $1/f$.
2. The terms are independent, so their extremes rarely coincide: RSS estimates a spread (if each term were a standard deviation), while the worst case bounds every unit. Quote RSS for a statistical yield estimate and worst case for a guarantee (06-07 discusses when RSS of limits is valid).
3. Low voltage noise (1.1 nV/√Hz), which needs large input-transistor $g_m$ and so current (10-04, 12-10), plus output drive (±30 mA class) and low distortion.

## Optional hardware extension

With any general-purpose op-amp on a breadboard, build a follower and drive it with a function generator's square wave: small steps show exponential edges, large steps show straight slewing ramps. Then raise a sine's frequency until it turns into a triangle and compare with $\text{SR}/(2\pi V_p)$ from the data sheet.
