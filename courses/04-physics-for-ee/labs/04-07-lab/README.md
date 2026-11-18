# Lab 04-07 · Faraday's Law, Lenz's Law and Inductance

**Chapter:** [04-07](../../chapters/04-07-faraday-lenz-and-inductance.md) · **Notebook:** [04-07-induction.ipynb](04-07-induction.ipynb) · **Netlist:** [coupled_coils.cir](coupled_coils.cir) · **Time:** about 60 minutes

## Objective

1. Compute an induced EMF by differentiating flux, and see what speed changes and what it does not.
2. Compute the exact skin-effect resistance of a round wire against frequency.
3. Find a real solenoid's inductance from ring-by-ring mutual inductances (Nagaoka's correction).
4. Compute the mutual inductance of two loops by Neumann's formula and see its $1/d^3$ fall-off.
5. Size a gapped core for a target inductance.
6. Simulate coupled coils in ngspice.

## Background

Chapter sections 3.1 to 3.7 and Examples 04-07.3 to 04-07.5 and 04-07.7; Problems 04-07.12 and 04-07.15. The notebook has no random elements.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how the peak EMF and the area under the EMF pulse change when the magnet moves twice as fast.
3. **Part 2:** predict the frequency at which a 1 mm copper wire's resistance doubles.
4. **Part 3:** predict whether a 10 cm, 1 cm-radius coil's inductance is above or below the long-solenoid value.
5. **Part 4:** predict how mutual inductance falls with separation.
6. **Part 5:** predict whether 100 µH needs a larger or smaller gap than 0.5 mm.
7. From the repository root, run `python tools/run_spice.py 04-07` to simulate Example 04-07.7.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | magnet through a 1 cm loop | peak EMF 5.395 mV at 1 m/s and 10.79 mV at 2 m/s; the area under the approach pulse is 62.77 µWb at both speeds |
| 2 | 1 mm copper wire | $R_{ac}/R_{dc}$ = 1.466 at 100 kHz and 4.094 at 1 MHz; doubles at 202.7 kHz |
| 3 | 500-turn, 10 cm × 1 cm-radius coil | 0.9081 mH against 0.9870 mH for the long formula: Nagaoka's K = 0.9201 |
| 4 | coaxial 5 cm loops 5 cm apart | M = 24.70 nH by both methods; $1/d^3$ far away |
| 5 | gapped core for 100 µH | gap 0.1761 mm, saturating at 3.120 A at 100 °C |
| netlist | coupled coils at 360 kHz | 11.31 V open-circuit at the receiver, 22.62 V across the transmitter |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-07.a | peak EMF at 1 m/s | 5.395 | mV |
| Lab 04-07.b | frequency at which a 1 mm wire's resistance doubles | 202.7 | kHz |
| Lab 04-07.c | Nagaoka's coefficient | 0.9201 | — |
| Lab 04-07.d | finite-solenoid inductance | 0.9081 | mH |
| Lab 04-07.e | mutual inductance of the loops | 24.70 | nH |
| Lab 04-07.f | gap for 100 µH | 0.1761 | mm |
| Lab 04-07.g | saturation current at that gap | 3.120 | A |

## Discussion questions

1. Part 1 shows the area under the EMF pulse depends only on the flux change. A current-transformer clamp around a wire measures a fast current pulse. Why must its output be integrated to recover the current, and what limits it at low frequency?
2. Part 2 shows that resistance doubles at about 200 kHz in a 1 mm wire. A buck converter switches at 500 kHz with a large DC current and a smaller ripple. Which current component is affected by the skin effect, and how would you pick the winding?
3. Part 3 gives an 8% end correction. Why do circuit-board and on-chip inductors need field solvers rather than formulas at all?
4. Part 4 shows mutual inductance falling as $1/d^3$. What does that imply for crosstalk between adjacent traces on a board, compared with distant ones?

<details><summary>Answers to the discussion questions</summary>

1. The coil's output is $M\,di/dt$, proportional to the *rate of change* of current, so it must be integrated (by a circuit or in software) to give the current itself. At low frequency $di/dt$ is small and the signal sinks into noise and offset; Rogowski coils and current transformers cannot measure DC, which is why Hall sensors (04-06) are used when DC matters.
2. Only the AC ripple sees the skin effect; the DC component spreads over the whole conductor. With a large DC and small ripple, a single conductor sized for DC resistance may be fine; when ripple loss matters, use foil, litz or several thinner parallel wires whose size is comparable to the skin depth at the switching frequency (about 0.09 mm at 500 kHz).
3. Real inductors are short, flat or spiral, sit near ground planes and other conductors, and have currents that redistribute with frequency (skin and proximity effects). No closed-form formula captures these; field solvers compute the actual current distribution and flux, as Part 3 did for the simplest case.
4. Coupling between traces falls steeply with distance. Small coaxial loops (dipoles) follow the $1/d^3$ law of Part 4, but long parallel traces over a return plane at height $h$ couple roughly as $1/(1 + (s/h)^2)$: doubling the spacing of two distant traces cuts their mutual inductance (and inductive crosstalk) by about four. Close neighbors and traces sharing a return path dominate crosstalk, so spacing and a solid nearby return plane are the main remedies.

</details>

## Optional hardware version

Wind 20–50 turns of thin wire on a cardboard tube, connect the ends to an oscilloscope (or a sound-card oscilloscope), and drop or push a small neodymium magnet through the tube at different speeds. Measure the peak voltage and the area of the pulse. Then drop the same magnet through a copper pipe and time its fall against a plastic pipe of the same length: Lenz's law made visible.
