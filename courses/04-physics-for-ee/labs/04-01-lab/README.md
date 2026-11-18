# Lab 04-01 · Mechanics Essentials for EE

**Chapter:** [04-01](../../chapters/04-01-mechanics-essentials.md) · **Notebook:** [04-01-mechanics.ipynb](04-01-mechanics.ipynb) · **Netlist:** [msd_analog.cir](msd_analog.cir) · **Time:** about 75 minutes

## Objective

1. See why the choice of numerical integrator matters for a conservative system.
2. Watch energy slosh between kinetic and potential stores, and measure Q from the energy lost per cycle.
3. Measure Q two ways: from a ring-down and from a resonance width.
4. Quantify an accelerometer's sensitivity–bandwidth tradeoff.
5. Simulate the Brownian motion of a proof mass and check equipartition.
6. Apply a drop-test shock to a MEMS proof mass.

## Background

Chapter sections 3.3 (energy), 3.4 (impulse), 3.6 (the oscillator and Q), 3.7 (the force–voltage analogy) and 3.8 (the accelerometer), and Examples 04-01.3 and 04-01.5 to 04-01.7. The notebook uses `scipy.integrate.solve_ivp` for accurate integration and a fixed random seed (2026) for Part 5, so the printed numbers match the ones below.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict whether forward Euler's energy drifts up or down, and roughly how far.
3. **Part 2:** predict the fraction of energy lost per cycle at Q = 7.906.
4. **Part 3:** predict whether ring-down and resonance width give the same Q.
5. **Part 4:** predict the deflection per *g* at 4 kHz and the effect of Q on bandwidth.
6. **Part 5:** predict the rms thermal displacement of the proof mass.
7. **Part 6:** predict whether the drop shock deflects the proof mass more or less than the quasi-static value.
8. From the repository root, run `python tools/run_spice.py 04-01` to simulate the RLC twin of Example 04-01.5.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | energy after 100 periods (50 mJ initially, 200 steps per period) | forward Euler $1.851\times10^{10}$ mJ, a factor $(1 + (\omega_0\Delta t)^2)^n$ = $3.702\times10^8$ too large; semi-implicit Euler 49.96 mJ; adaptive RK45 50.00 mJ |
| 2 | energy lost per cycle, Q = 7.906 | 0.5490 every cycle, equal to $1 - e^{-2\alpha T_d}$; the light-damping estimate $2\pi/Q$ = 0.7948 is too large at this low Q |
| 3 | Q from ring-down and from bandwidth | log decrement 0.3982, so Q = 7.906 (π/δ gives 7.890); half-power width 6.366 Hz, so Q = 7.906 |
| 4 | accelerometer, Q = 0.707 | 248.4, 15.53 and 0.9703 nm per *g* at 1, 4 and 16 kHz, with bandwidth equal to $f_0$; Q = 0.5 narrows the bandwidth to 0.6436 $f_0$, Q = 2 widens it to 1.485 $f_0$ with a 2.066-fold peak |
| 5 | Brownian motion, 5 µg at 4 kHz, 300 K | seeded ensemble rms 36.12 pm against equipartition's 36.21 pm |
| 6 | drop shock, 4344 *g* half-sine for 0.2 ms | quasi-static deflection 67.44 µm; simulated peak 60.31 µm: tens of micrometers, so the mass would hit its stops |
| netlist | RLC twin of Example 04-01.5 | half-power frequencies 47.25 and 53.61 Hz; resonant capacitor gain 7.906 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-01.a | forward Euler energy growth factor | 3.702×10^8 | — |
| Lab 04-01.b | energy lost per cycle, exact | 0.5490 | — |
| Lab 04-01.c | light-damping estimate 2π/Q | 0.7948 | — |
| Lab 04-01.d | logarithmic decrement | 0.3982 | — |
| Lab 04-01.e | Q from π/δ | 7.890 | — |
| Lab 04-01.f | bandwidth ratio at Q = 0.5 | 0.6436 | — |
| Lab 04-01.g | bandwidth ratio at Q = 2 | 1.485 | — |
| Lab 04-01.h | peak over DC at Q = 2 | 2.066 | — |
| Lab 04-01.i | quasi-static shock deflection | 67.44 | µm |
| Lab 04-01.j | simulated peak shock deflection | 60.31 | µm |
| Lab 04-01.k | equipartition rms displacement | 36.21 | pm |
| Lab 04-01.l | Q at which 2π/Q is 10% too large | 32.39 | — |

## Discussion questions

1. Part 1's forward Euler result is absurd after 100 periods. Circuit simulators integrate LC tanks every day. What property of the integration method matters for an undamped oscillator, and how would you check a simulator's choice?
2. Part 2 shows that $2\pi/Q$ overstates the energy lost per cycle at Q ≈ 8. Below what Q would you stop using the energy definition of Q as an approximation?
3. Part 6's ordinary drop would push the proof mass far past its gaps. What does that imply about how accelerometer datasheets specify shock, and what would you ask a supplier?

<details><summary>Answers to the discussion questions</summary>

1. Whether it conserves (or bounds) energy for a lossless system. Forward Euler multiplies the energy by $1 + (\omega_0\Delta t)^2$ every step; symplectic (semi-implicit) and trapezoidal methods do not add energy. Check it by simulating an ideal LC tank for many periods and watching the amplitude: it should neither grow nor decay.
2. The fraction lost per cycle is exactly $1 - e^{-2\pi/Q_d}$ with $Q_d = \omega_d/(2\alpha)$, and $2\pi/Q$ is its first-order expansion. The relative error is about $\pi/Q$ and reaches 10% at Q = 32.39; below a few tens, use the exact form.
3. Datasheets specify survival of a shock (a peak in *g* and a pulse duration) rather than accurate measurement during it: the mass is expected to hit stops. Ask for the shock-survival rating and pulse duration, how many shocks it was tested for, the post-shock offset shift, and whether stiction (the mass sticking to a stop) was tested.

</details>

## Optional hardware version

Any phone or development board with a MEMS accelerometer can be used. Log the accelerometer at its highest rate while the board rests on a table (it should read about 1 *g*), then compute the standard deviation of the readings and divide by the square root of the output bandwidth to estimate the noise density. Compare it with the datasheet and with the thermomechanical floor of Example 04-01.7. Then tap the table and look for the ring-down of the board or its mounting, and estimate its frequency and Q with the logarithmic decrement.
