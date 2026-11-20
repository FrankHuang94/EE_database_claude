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
4. **Buck converter (Part 4).** For Example 15-09.6, sweep the Type III zero frequency from $0.3f_0$ to $1.5f_0$ with crossover held at 60 kHz. Plot the phase margin, check that the loop gain crosses 0 dB only once, and plot the lowest phase reached anywhere $\lvert L\rvert > 1$: if it falls below −180°, the loop is **conditionally stable** (15-07), and a large drop in gain, such as an amplifier saturating during a big transient, could destabilize it. Also record $\lvert L\rvert$ at 1 kHz. *Predict first:* which way does each quantity move as the zeros go down?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Lead network | 54.9° at 5.59 kHz (the geometric mean of 1.77 and 17.7 kHz) |
| 2 | Lead vs lag | similar margins (49.8° and 49.7°); settling 1.23 s against 19.7 s |
| 3 | Zero sweep | a zero nearer the origin adds more angle at $s_d$ (98.2° from −1.5, 73.9° from −3), so the pole must take more back and sits closer: −4.70 against −8.57. $K_v$ falls (5.78 against 10.4 s⁻¹), and the third closed-loop pole moves in beside the zero (−1.70 against −5.57) |
| 4 | Type III | margin rises as the zeros move down (25.6° at $1.5f_0$, 39.3° at $f_0$, 53.9° at $f_0/2$, 59.9° at $0.3f_0$), but $\lvert L\rvert$ at 1 kHz falls (34.8 dB at $f_0$, 14.7 dB at $0.3f_0$); one 0 dB crossing throughout; conditionally stable for zeros above $1.36f_0$ |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-09.a | maximum phase of the network | 54.9 | ° |
| Lab 15-09.b | frequency of maximum phase | 5.59 | kHz |
| Lab 15-09.c | 0 dB crossings of the Type III loop | 1 | — |
| Lab 15-09.d | lead pole for a zero at −1.5 | −4.70 | s⁻¹ |
| Lab 15-09.e | lead pole for a zero at −3 | −8.57 | s⁻¹ |
| Lab 15-09.f | $K_v$ for a zero at −1.5 | 5.78 | s⁻¹ |
| Lab 15-09.g | $K_v$ for a zero at −3 | 10.4 | s⁻¹ |
| Lab 15-09.h | third closed-loop pole, zero at −1.5 | −1.70 | s⁻¹ |
| Lab 15-09.i | third closed-loop pole, zero at −3 | −5.57 | s⁻¹ |
| Lab 15-09.j | angle of the zero at −1.5, seen from $s_d$ | 98.2 | ° |
| Lab 15-09.k | angle of the zero at −3, seen from $s_d$ | 73.9 | ° |
| Lab 15-09.l | Type III phase margin, zeros at $1.5f_0$ | 25.6 | ° |
| Lab 15-09.m | Type III phase margin, zeros at $0.3f_0$ | 59.9 | ° |
| Lab 15-09.n | $\lvert L\rvert$ at 1 kHz, zeros at $f_0$ | 34.8 | dB |
| Lab 15-09.o | $\lvert L\rvert$ at 1 kHz, zeros at $0.3f_0$ | 14.7 | dB |
| Lab 15-09.p | zero frequency above which the loop is conditionally stable | 1.36 | × $f_0$ |
| Lab 15-09.q | fall of $\lvert L\rvert$ at 1 kHz, zeros from $f_0$ to $0.3f_0$ | 20.0 | dB |
| Lab 15-09.r | smallest gain reduction that destabilizes the loop, zeros at $1.5f_0$ | 15.4 | dB |
| Lab 15-09.s | largest gain reduction that leaves it unstable | 30.7 | dB |
| Lab 15-09.t | lower −180° crossing frequency, zeros at $1.5f_0$ | 17.9 | kHz |
| Lab 15-09.u | upper −180° crossing frequency, zeros at $1.5f_0$ | 25.6 | kHz |

## Discussion

1. Why is the passive network's DC gain 1/10, and what must follow it in a real loop?
2. In Part 2, the lead and lag loops have nearly the same overshoot. Why are their settling times so different?
3. In Part 3, what goes wrong if the lead zero is placed very close to the origin?
4. In Part 4, why does placing the Type III zeros below $f_0$ add margin, what does it cost, and what goes wrong if they are placed well above $f_0$?

### Answers

1. At DC the capacitor is open, so the network is a 10:1 divider ($R_1 : R_2$ = 9 : 1). A gain stage of 10 restores the loop gain; otherwise $K_v$ falls tenfold. Active (op-amp) realizations avoid the loss.
2. The overshoot is set mostly by the margin, which is similar. Settling depends on speed: the lead raised crossover to 4.42 rad/s, while the lag lowered it to 0.70 rad/s and left a slow pole–zero pair near 0.07 rad/s whose tail decays with a 14 s time constant.
3. A zero near the origin nearly cancels the plant's integrator, and the closed loop then has a slow pole near that zero: a slow tail, as with a lag. The deficiency is met, but the response is not.
4. The zeros' phase lead builds up over about a decade above them; placing them below $f_0$ means their full lead is available near crossover, where the plant's phase has reached −180°. The cost is low-frequency gain. Between the zeros and the high-frequency poles the compensator behaves like $\omega_I s/\omega_z^2$, so holding crossover at 60 kHz forces $\omega_I$ down roughly as $\omega_z^2$, and the loop gain below the resonance falls with it: 20.0 dB less at 1 kHz when the zeros move from $f_0$ to $0.3f_0$, which means a slower recovery from slow line and load changes. Placed above $f_0$, the zeros arrive late: just above the resonance the plant's phase is already near −180° while the zeros have not yet lifted the phase, so the loop phase dips below −180° while $\lvert L\rvert$ is still above 1 (from about $1.36f_0$ up). That loop is conditionally stable: it is stable as designed, but with the zeros at $1.5f_0$ any fall in loop gain between 15.4 dB and 30.7 dB makes it unstable. Those are the loop gains at the two −180° crossings below crossover (25.6 and 17.9 kHz): once the gain has fallen enough to put either crossing at the 0 dB line, the Nyquist plot encircles −1 (closed-loop roots confirm the interval). Saturation is the usual way that happens: an error amplifier or modulator that clips during a big transient has a lower effective gain (the describing-function idea of 15-08), so the loop can break into a large oscillation that a small-signal analysis never shows.

## Optional hardware

Build the passive lead network with 1% parts and measure its phase with a function generator and a two-channel oscilloscope at 1, 2, 5, 10 and 20 kHz; compare with the curve from ngspice.
