# Lab 07-03 · Second-Order RLC Transients

**Chapter:** [07-03](../../chapters/07-03-second-order-rlc-transients.md) · **Notebook:** [07-03-rlc.ipynb](07-03-rlc.ipynb) · **Time:** about 2 hours (plus 1 hour for the optional hardware part)

## Objective

1. Watch the characteristic roots move as a tank goes from underdamped to overdamped, and connect them to the waveform.
2. Confirm that every variable of a series RLC shares α and $\omega_0$ but not its shape, and that only the all-pole variable obeys the overshoot formula.
3. Build state equations for circuits that are not plain series or parallel loops, and simulate them.
4. Design damping: an electrolytic across a hot-plugged ceramic, and an RC snubber on a switch node.

## Background

Chapter sections 3.2 to 3.10 and Examples 07-03.1 to 07-03.6. The one tool used throughout is the state-equation form $\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{g}u$ of §3.8: the eigenvalues of $\mathbf{A}$ are the natural frequencies, and integrating the equations gives every waveform. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips them.

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-03-rlc.ipynb](07-03-rlc.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [ex2_parallel_release.cir](ex2_parallel_release.cir) | An inductor released into a parallel RC by a switch, with and without the capacitor | Example 07-03.2 |
| [ex3_hot_plug.cir](ex3_hot_plug.cir) | Hot-plugging into a ceramic capacitor, and three electrolytic dampers and a series resistor | Example 07-03.3, Problem 07-03.11 |
| [ex4_lc_filter.cir](ex4_lc_filter.cir) | An LC supply filter switched on at two loads | Example 07-03.4 |
| [ex5_snubber.cir](ex5_snubber.cir) | A switch node with no snubber and four RC snubbers | Example 07-03.5 |
| [ex6_rc_ladder.cir](ex6_rc_ladder.cir) | A loaded and a buffered two-section RC ladder | Example 07-03.6 |
| [problems.cir](problems.cir) | Problems 07-03.4, .6, .7, .8, .12, .13, .14 and .16 | Solution answer key |
| [p17_two_integrator.cir](p17_two_integrator.cir) | Problem 07-03.17: the three-op-amp two-integrator loop | Solution answer key |

Each netlist begins with `* EXPECT` lines naming the measurement and the published answer it must reproduce. Run them all from the repository root:

```bash
python tools/run_spice.py 07-03
```

## Procedure

1. **The roots (Part 1).** *Predict first:* for the 100 µH, 1 µF tank of Example 07-03.1 in series, at what resistance do the two roots meet, and where do they go above it?
2. **Every variable (Part 2).** *Predict first:* sketch $v_C$, $i$, $v_L$ and $v_R$ for Problem 07-03.14's step response, marking which ones jump at $t = 0$.
3. **State equations (Part 3).** *Predict first:* will the LC filter of Example 07-03.4 ring less at 10 Ω or at 100 Ω, and by how much?
4. **Damping design (Part 4).** *Predict first:* the electrolytic ESR that minimizes the hot-plug peak of Problem 07-03.11, and the snubber capacitance beyond which Example 07-03.5 stops improving.
5. **Guided exercise (chapter §5).** Double the hot-plug cable (2 µH, 0.1 Ω). *Predict first:* $Z_0$, ζ, the peak voltage and the peak current. Then run and compare with the table below.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | roots | meet at −100 krad/s when $R$ = 20 Ω, then split along the real axis |
| 2 | step response | only $v_L$ jumps (to 5 V); $i$ peaks at 126.1 mA; $v_L$ dips to −3.181 V |
| 3 | LC filter | ζ = 0.05548 (10 Ω) and 0.03476 (100 Ω); peaks 9.172 V and 9.480 V |
| 4 | dampers | best ESR between 0.2 and 0.3 Ω, close to $Z_0$ = 0.3162 Ω (peak just below the 13.70 V of 0.3 Ω); snubber settling stops improving beyond $C_d \approx 4C$ |
| 5 | doubled cable | see the answer key |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-03.a | $Z_0$ with the doubled cable | 0.4472 | Ω |
| Lab 07-03.b | ζ with the doubled cable | 0.1118 | — |
| Lab 07-03.c | peak voltage with the doubled cable | 20.43 | V |
| Lab 07-03.d | peak current with the doubled cable | 22.77 | A |

## Discussion questions

1. In Part 1, the series tank's roots move around a circle as $R$ grows, then split. What does the circle's radius represent, and why can the roots not leave it while they are complex?
2. In Part 2, the current reaches its peak before the capacitor voltage does. Why does that ordering make physical sense?
3. In Part 3, why does a light load hardly change the damping of the LC filter?
4. In Part 4, why does an electrolytic with too much ESR damp the hot-plug ringing poorly?
5. The doubled cable rings less (ζ rises from 0.079 to 0.112), yet nobody would recommend longer cables. Why not?

<details><summary>Answers to the discussion questions</summary>

1. The radius is $\omega_0$: for complex roots $\alpha^2 + \omega_d^2 = \omega_0^2$, and $\omega_0 = 1/\sqrt{LC}$ does not depend on $R$. Changing $R$ changes only α, so the pair slides around the circle until it reaches the real axis at $-\omega_0$ (critical damping).
2. The current is greatest when the inductor stops accelerating it, which is when $v_L = 0$, that is when $v_C + v_R$ has risen to the source voltage; the capacitor keeps charging after that, while the current falls, until the current reaches zero. So the current peaks first and the voltage peaks when the current returns to zero.
3. The load's share of ζ is $Z_0/(2R_L)$, and $Z_0 = 0.46$ Ω is tiny next to 10 Ω or 100 Ω. The damping comes almost entirely from the series resistance's share, $R_s/(2Z_0)$.
4. At the ringing frequency the electrolytic's capacitance is nearly a short, so the branch looks like its ESR in parallel with the tank. A parallel resistance damps a tank only when it is comparable with $Z_0$ (ζ = $Z_0/2R$); if it is much larger, almost no current flows through it and the ceramic rings as before.
5. The damping improved only because the cable's resistance grew faster than $Z_0$; the peak is still 20 V, the inductance stores more energy, and the cable drops more voltage and wastes more power under load. Damping should be designed in (an electrolytic or RC damper), not left to wiring.

</details>

## Optional hardware version

With a bench supply set to 12 V, a 1 m pair of wires, a 10 µF ceramic capacitor (X7R, rated 50 V or more: a hot plug can ring to twice the supply, and the chapter's §9 shows real class II parts going beyond that) and an oscilloscope with a short ground spring, plug the wires onto the capacitor while triggering on the rising edge and record the peak. Then add a 47 µF aluminum electrolytic (35 V) across the ceramic and repeat. Use a supply whose current limit is set to a few amperes, keep the voltage at or below 12 V so that even a doubled peak stays inside the capacitor's rating, and estimate the wire pair's inductance from the ringing frequency with the method of chapter §3.10. Expect the peak and the damping to differ from the ideal model, since the supply's own output capacitance and the ceramic's DC-bias loss both change the circuit.
