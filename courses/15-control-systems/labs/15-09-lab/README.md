# Lab 15-09 · Lead and Lag Compensation

Chapter: [15-09 Lead and Lag Compensation](../../chapters/15-09-lead-lag-compensation.md)

## Objective

Design lead and lag compensators with the Bode-plot and root-locus recipes, compare their time responses, measure a passive lead network in ngspice, and compensate an LC double pole as in a buck converter.

## Background

Read §3 of the chapter. `compensate.design_lead` and `design_lag` follow the recipes of §3.3 and §3.4 step by step, using `labs/15-07-lab/freqdomain.py` for margins. `lead_rc` returns the components of the passive lead network of §3.6.

## Files

- [compensate.py](compensate.py): `lead_phase`, `lead_alpha`, `design_lead`, `design_lag`, `lead_rc` and `with_comp`.
- [15-09-compensation-lab.ipynb](15-09-compensation-lab.ipynb): the notebook (Parts 1–4).
- [lead_network.cir](lead_network.cir): a passive lead with $\alpha$ = 10 (9 kΩ ∥ 10 nF in series, 1 kΩ to ground), swept in frequency.

## Procedure

1. **A lead network (Part 1).** Run `lead_network.cir` and compare its maximum phase and peak frequency with §3.1. *Predict first:* both numbers.
2. **Lead against lag (Part 2).** Design both for Example 15-09.2's specification, then overlay Bode plots and step responses, and plot the error on a log scale to see the lag's tail.
3. **Root locus (Part 3).** Reproduce Example 15-09.4 and move the lead zero from −1.5 to −3, recording the pole location, gain, overshoot and $K_v$.
4. **Buck converter (Part 4).** For Example 15-09.6, sweep the Type III zero frequency from $0.3f_0$ to $1.5f_0$ and plot the phase margin; check that the loop gain crosses 0 dB only once.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Lead network | 54.9° at 5.59 kHz (the geometric mean of 1.77 and 17.7 kHz) |
| 2 | Lead vs lag | similar margins (49.8° and 49.7°); settling 1.23 s against 19.7 s |
| 3 | Zero sweep | zeros closer to the origin need less phase from the pole but leave a slower closed-loop pole |
| 4 | Type III | margin rises as the zeros move below $f_0$: 39.3° at $f_0$, 53.9° at $f_0/2$; one crossover |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-09.a | maximum phase of the network | 54.9 | ° |
| Lab 15-09.b | frequency of maximum phase | 5.59 | kHz |
| Lab 15-09.c | 0 dB crossings of the Type III loop | 1 | — |

## Discussion

1. Why is the passive network's DC gain 1/10, and what must follow it in a real loop?
2. In Part 2, the lead and lag loops have nearly the same overshoot. Why are their settling times so different?
3. In Part 3, what goes wrong if the lead zero is placed very close to the origin?
4. In Part 4, why does placing the Type III zeros below $f_0$ add margin, and what limits how far below they can go?

### Answers

1. At DC the capacitor is open, so the network is a 9:1 divider. A gain stage of 10 restores the loop gain; otherwise $K_v$ falls tenfold. Active (op-amp) realizations avoid the loss.
2. The overshoot is set mostly by the margin, which is similar. Settling depends on speed: the lead raised crossover to 4.42 rad/s, while the lag lowered it to 0.70 rad/s and left a slow pole–zero pair near 0.07 rad/s whose tail decays with a 14 s time constant.
3. A zero near the origin nearly cancels the plant's integrator, and the closed loop then has a slow pole near that zero: a slow tail, as with a lag. The deficiency is met, but the response is not.
4. The zeros' phase lead builds up over about a decade above them; placing them below $f_0$ means their full lead is available near crossover, where the plant's phase has reached −180°. Placed too low, they raise the mid-band loop gain around the resonance (the conditionally stable region grows) and make the loop sensitive to $Q$ and component tolerance.

## Optional hardware

Build the passive lead network with 1% parts and measure its phase with a function generator and a two-channel oscilloscope at 1, 2, 5, 10 and 20 kHz; compare with the curve from ngspice.
