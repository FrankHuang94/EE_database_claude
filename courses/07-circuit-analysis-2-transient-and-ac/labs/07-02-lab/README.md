# Lab 07-02 · First-Order RC and RL Transients

**Chapter:** [07-02](../../chapters/07-02-first-order-rc-rl-transients.md) · **Notebook:** [07-02-transients.ipynb](07-02-transients.ipynb) · **Time:** about 2 hours (plus 1 hour for the optional hardware part)

## Objective

1. Confirm by simulation that every first-order response follows the same exponential curve, and measure its landmarks (50% delay, 10–90% rise, settling to N bits).
2. Watch non-state variables jump at switching instants while $v_C$ and $i_L$ stay continuous, and see τ change when the circuit changes.
3. Convince yourself numerically that the charging loss is ½CV² for **every** resistance, and that stepwise charging reduces it.
4. Find the periodic steady state of an RC low-pass driven by a square wave.
5. Compare resistor and diode flyback paths for an inductive load.
6. Run real circuit-simulator (ngspice) netlists whose results are checked automatically against the chapter's published answers.

## Background

Read chapter sections 3.1–3.12. The one formula to have in front of you is the master formula,

$$
x(t) = x(\infty) + \big[x(t_0^+) - x(\infty)\big]e^{-(t - t_0)/\tau},
$$

with $\tau = R_{Th}C$ or $L/R_{Th}$.

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-02-transients.ipynb](07-02-transients.ipynb) | Python simulations of each circuit, built by integrating KCL/KVL numerically | Built-in `assert`s |
| [ex2_ex3_switched_rc.cir](ex2_ex3_switched_rc.cir) | Switched RC with a second switching event | Examples 07-02.2–3 |
| [ex4_rl_kick.cir](ex4_rl_kick.cir) | Inductive kick through a 20 Ω flyback resistor | Example 07-02.4 |
| [ex5_adc_settling.cir](ex5_adc_settling.cir) | 16-bit settling of a 100 Ω / 20 pF sampling network | Example 07-02.5 |
| [p11_integrators.cir](p11_integrators.cir) | Ideal and leaky op-amp integrators (op-amp = VCVS, gain 10⁶) | Problem 07-02.11 |
| [p12_square_wave.cir](p12_square_wave.cir) | Square-wave periodic steady state at τ = T/2 and τ = 5T | Problem 07-02.12 |
| [p14_relay_flyback.cir](p14_relay_flyback.cir) | Relay release with resistor vs diode flyback | Problem 07-02.14 |
| [p19_differentiator.cir](p19_differentiator.cir) | Practical differentiator driven by a step, a ramp and a fast noise edge | Problem 07-02.19 |

Each netlist begins with `* EXPECT` lines naming the measurement and the published answer it must reproduce. Most point directly into an answer-key table, e.g. `key:../../chapters/07-02-....md#Ex_07-02.2e`. Run them all from the repository root:

```bash
python tools/run_spice.py 07-02
```

To look at waveforms yourself, run a netlist interactively (`ngspice ex2_ex3_switched_rc.cir`) and type `plot v(a)` at the ngspice prompt.

## Procedure

1. Run every notebook cell once (*Run → Run All Cells*). All asserts should pass.
2. For each **🔮 Predict** prompt:
   1. Write down your prediction and the formula you used.
   2. Change the parameter and re-run the cell.
   3. Reconcile any difference before moving on.
3. Run `python tools/run_spice.py 07-02` and confirm that all seven netlists pass.
4. Open `ex2_ex3_switched_rc.cir` and make your own change, for example $R_2 = 6$ kΩ. Predict the new measurements, run ngspice, and compare.
5. Answer the discussion questions.

## Expected results

Check these only after making your predictions.

| Exercise | Expected |
|---|---|
| Part 1: settling to 12-bit accuracy | $13\ln 2 = 9.01$ time constants |
| Part 2 with $R_2 = 6$ kΩ: $V_{Th}$, $R_{Th}$, τ, time to 7 V | 12.0 V; 3.00 kΩ; 6.00 ms; 5.253 ms |
| Part 2 with $R_2 = 6$ kΩ: still climbing at 10 ms? | Yes: $v_C(10\text{ ms}) = 9.733$ V, only 81% of the way to 12 V |
| Part 3: loss for R = 10 Ω, 1 kΩ, 100 kΩ | 12.5 µJ every time (½CV² with C = 1 µF, V = 5 V) |
| Part 3: loss with N = 10 steps | 1.25 µJ (one tenth) |
| Part 5 with $R_f = 1$ kΩ | Switch sees 12 + 0.06 × 1000 = 72 V, which would destroy a 30 V transistor; fast release (τ = 83 µs) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-02.1 | $V_{Th}$ with $R_2$ = 6 kΩ | 12.0 | V |
| Lab 07-02.2 | $R_{Th}$ with $R_2$ = 6 kΩ | 3.00 | kΩ |
| Lab 07-02.3 | τ with $R_2$ = 6 kΩ | 6.00 | ms |
| Lab 07-02.4 | time to 7 V with $R_2$ = 6 kΩ | 5.253 | ms |
| Lab 07-02.5 | charging loss, any R | 12.5 | µJ |
| Lab 07-02.6 | loss with 10 steps | 1.25 | µJ |
| Lab 07-02.7 | $v_C(10\text{ ms})$ with $R_2$ = 6 kΩ | 9.733 | V |
| Lab 07-02.8 | switch voltage with $R_f$ = 1 kΩ | 72 | V |
| Lab 07-02.9 | τ with $R_f$ = 1 kΩ | 83 | µs |
| Lab 07-02.10 | settling-time ratio, 16-bit to 12-bit | 1.308 | — |

## Discussion questions

1. In Part 2 the capacitor current reverses sign at $t = 10$ ms. Explain physically what the capacitor is doing before and after.
2. Part 3 shows the charging loss is independent of R. Why, then, do chip designers care about transistor resistance at all? (Hint: what does R control, if not energy?)
3. The ngspice netlist for Example 07-02.4 starts the simulation at $t = 0$ with the inductor current as an initial condition, instead of simulating the switch opening. Why is that legitimate? What would you need to model to see what really happens to an *unprotected* switch?
4. In Part 5, the real diode clamps at about 0.76 V rather than 0.7 V and releases slightly faster than the constant-drop model predicts. Why does a higher clamp voltage speed up the release?
5. A 16-bit ADC needs 11.8 time constants of settling; a 12-bit ADC needs 9.0. What does that ratio imply for the driver bandwidth needed per bit of resolution?

<details><summary>Answers to the discussion questions</summary>

1. Before 10 ms the switch is closed and the capacitor charges toward the Thévenin voltage of 8 V, so current flows into it, shrinking as the voltage approaches 8 V. At 10 ms the switch opens and cuts off the source. The capacitor's voltage cannot jump, but its only path is now $R_2$, so it discharges through $R_2$ with the new time constant $R_2C$ = 6 ms: current flows out of it. The voltage is continuous; the current jumps and reverses.
2. The resistance sets the *time*, not the energy. The charging time constant $RC$ sets how fast a gate's output switches, and so the clock frequency a design can reach. A lower-resistance transistor charges the same capacitance faster, while losing the same ½CV² per transition. Energy is controlled by $C$ and $V$, speed by $R$ (07-02 §3.8).
3. The inductor's current is continuous, so its value just after the switch opens equals its value before. Starting the simulation at that instant, with that current as the initial condition, reproduces the post-switching circuit exactly. What it hides is the switch itself. To see what an unprotected switch experiences, you would model its finite turn-off time or off-resistance, the parasitic capacitance across it and its breakdown. Without a flyback path, those parasitics alone limit the voltage.
4. While the diode clamps, the coil obeys $L\,di/dt = -(V_{clamp} + iR)$. A larger clamp voltage puts a larger reverse voltage across the inductance, so the current falls faster and reaches zero sooner, dumping the stored energy into the clamp more quickly. The real diode's exponential curve gives a slightly higher voltage at high current than the constant 0.7 V model, hence the slightly faster release. Relay designers use a Zener or TVS in series with the diode for exactly this reason.
5. Settling needs $(N + 1)\ln2$ time constants, so each extra bit adds only $\ln 2$ ≈ 0.69 τ. From 12 to 16 bits the time constants needed rise by the factor $17/13$ = **1.308**. For the same acquisition time, the driver and filter bandwidth must be 31% higher: the requirement grows linearly with the number of bits, not exponentially. The harder costs of more bits lie elsewhere: noise, linearity and the reference.

</details>

## Optional hardware version

**Equipment:** breadboard; 10 kΩ and 1 kΩ resistors; 1 µF, 0.47 µF, 100 nF and 47 nF capacitors; a small 5 V relay with a 1N4148 (or 1N400x) diode and a logic-level MOSFET; a function generator (square wave) and a two-channel oscilloscope. See [SETUP.md](../../../../SETUP.md#7-optional-hardware-kit).

1. **Measure τ.** Build an RC low-pass with 10 kΩ and 100 nF (τ = 1 ms). Drive it with a 0–1 V square wave at 50 Hz (period 20 ms, much longer than τ). On the scope, measure the 10–90% rise time. Expect about 2.2 ms. Check: does $t_r \approx 2.2\,RC$ hold within the component tolerances?
2. **Square-wave steady state.** Raise the frequency to 1 kHz with τ ≈ 0.5 ms (1 kΩ and 0.47 µF, or 10 kΩ and 47 nF, both giving τ = 0.47 ms; recompute the expected values for 0.47 ms). Measure $V_{max}$ and $V_{min}$ and compare with Problem 07-02.12.
3. **Flyback, safely.** Drive a small 5 V relay through a logic-level MOSFET, with a 1N4148 across the coil. Probe the MOSFET drain while switching the relay off. Expect the drain to clamp near 5.7 V. **Do not remove the diode with nothing in its place:** without a flyback path, the drain spike can exceed the MOSFET's rating. To see a larger (but still limited) spike, replace the diode with a 1 kΩ resistor across the coil. The drain then rises to about the supply plus $I_0 \times 1\text{ kΩ}$ (check that this is within the MOSFET's rating first), and the release is faster. Use a 10:1 probe.
