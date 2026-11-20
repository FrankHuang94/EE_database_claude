# Lab 13-07 · Transmission Lines: Time Domain

Chapter: [13-07 Transmission Lines: Time Domain](../../chapters/13-07-transmission-lines-time-domain.md)

## Objective

Solve the telegrapher's equations numerically and watch steps travel, reflect and settle; check the bounce diagram against the simulation; find how overshoot grows with the ratio of line delay to rise time; and read a simulated TDR trace. Then confirm ringing and a TDR via in ngspice.

## Background

The telegrapher's equations (§3.1), launching and reflections (§3.2–3.3), bounce diagrams (§3.4), reactive discontinuities (§3.5), terminations and critical length (§3.6) and TDR (§3.7).

## Files

- [13-07-transmission-lines.ipynb](13-07-transmission-lines.ipynb): the notebook (Parts 1–4).
- [ringing.cir](ringing.cir): Example 13-07.3, a 10 Ω driver on an open 50 Ω line.
- [tdr_via.cir](tdr_via.cir): Example 13-07.5, a TDR step on a matched line with a 2 pF via.

Run either with `ngspice -b <file>`, or `python tools/run_spice.py 13-07` from the repository root.

## Procedure

1. **A step on a line (Part 1).** Plot the voltage along the line at 0.5, 1.5, 2.5 and 3.5 ns. *Predict first:* the height and position of the front at each time.
2. **Bounce diagram (Part 2).** Overlay the bounce-diagram sum on the simulated receiver voltage for an open line driven through 10 Ω and for a 100 Ω source into a 25 Ω load.
3. **Critical length (Part 3).** Plot the overshoot against the line delay divided by a 100 ps rise time.
4. **TDR (Part 4).** Simulate a TDR of a line with a 1 pF via and a 45 Ω section; extract both.
5. **ngspice (the chapter's guided exercise).** Predict, then run, `ringing.cir` and `tdr_via.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Profiles | A 0.833 V front moving at one line-length per nanosecond, doubling at the open end, then a −0.556 V correction travelling back |
| 2 | Bounce diagram | The sum and the simulation coincide; the first case rings, the second creeps |
| 3 | Overshoot | Small for delays below about a tenth of the rise time, 67% once the delay reaches half of it |
| 4 | TDR | Dip area −25 ps (1 pF); a flat shelf of ρ = −0.0526 (45 Ω) |
| ngspice | Ringing, via | 1.667, 0.5556 and 1.296 V; area −50 ps |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-07.a | overshoot with delay = rise time / 10 | 9.1 | % |
| Lab 13-07.b | overshoot with delay = rise time / 6 | 17.2 | % |
| Lab 13-07.c | overshoot with delay = rise time | 66.7 | % |

*These are recomputed by [verify_13_07.py](../../verify/verify_13_07.py) with its own telegrapher's-equation solver (10 Ω source, open end, 100 ps linear edge).*

## Discussion questions

1. Why does the overshoot stop growing once the delay exceeds about half the rise time?
2. Why does the simulation agree with the bounce-diagram sum exactly when the time step equals one cell's delay?
3. A colleague proposes a stronger driver to "overpower" the ringing on an unterminated net. What do you tell them?

### Answers

1. Once the round trip $2T_D$ exceeds the rise time, the first reflection returns after the edge has finished, so the receiver sees the full doubled step $2v^+$ before any correction arrives: the bounce-diagram overshoot, $2v^+ - V_s$, which no longer depends on the delay. For shorter lines the correction arrives while the edge is still rising and cuts the peak.
2. At that time step, central differences in space and time have errors that cancel exactly for the one-dimensional wave equation: each update moves the wave one cell per step with no dispersion, which is the bounce diagram's assumption.
3. A stronger driver has a lower output resistance, so $\Gamma_S$ moves toward −1 and the reflections return to the receiver almost undiminished: the ringing gets worse. The cure is to match one end (a series resistor bringing the source to $Z_0$, or an end termination), or to slow the edge.

## Optional hardware extension

Connect a fast pulse generator (or a fast logic gate) through a 50 Ω coaxial cable of a few metres to an oscilloscope input set to 1 MΩ, and observe the steps at the generator end with a T connector. Then terminate the far end in 50 Ω, a short and an open, and compare the reflections. Measure the round-trip time and compute the cable's velocity factor.
