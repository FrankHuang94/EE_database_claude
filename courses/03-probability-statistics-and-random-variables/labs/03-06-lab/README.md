# Lab 03-06 · Random Processes Preview: Noise

**Chapter:** [03-06](../../chapters/03-06-random-processes-preview.md) · **Notebook:** [03-06-noise.ipynb](03-06-noise.ipynb) · **Netlist:** [rc_noise.cir](rc_noise.cir) · **Time:** about 75 minutes

## Objective

1. Compare ensemble and time averages for an ergodic process (random-phase sinusoid) and a non-ergodic one (unit offsets).
2. Estimate an autocorrelation and a PSD from data and match them to $e^{-|\tau|/\tau_c}$ and the Lorentzian.
3. Recover kT/C by simulating a resistor's $4kT/R$ noise current charging a capacitor, and confirm it with an ngspice noise analysis.
4. Recover the shot-noise density $2qI$ from Poisson electron arrivals.
5. Measure how the scatter of an average depends on record length, not sample rate.
6. See 1/f noise and a random walk defeat averaging.

## Background

Chapter sections 3.1–3.7 and Examples 03-06.1 to 03-06.7. The notebook is seeded (2026). The netlist runs in ngspice; from the repository root, `python tools/run_spice.py 03-06` checks it against the chapter's answer key.

## Procedure

1. Run `python tools/run_spice.py 03-06`, or `ngspice -b rc_noise.cir`, and note the density at 1 kHz and the total noise for 10 kΩ and 1 MΩ.
2. Run the notebook's cells in order, writing a prediction before each **🔮 Predict** cell.
3. **Part 2:** predict the PSD corner for $\tau_c$ = 1 ms.
4. **Part 3:** predict the rms voltage for 10 kΩ and for 100 kΩ.
5. **Part 5:** predict whether a tenfold higher sample rate shrinks the scatter of a 100 ms average.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| ngspice | RC noise, 10 kΩ and 10 pF at 300 K | 12.87 nV/√Hz at 1 kHz; 20.35 µV total; 20.35 µV again with 1 MΩ |
| 1 | random-phase sinusoid | ensemble mean near 0, power near 2 V²; every single waveform's time-averaged power exactly 2 V² |
| 1 | offset population | ensemble power near 1.01 mV² (seeded 1.0415); a unit's time average equals its own offset; about 4.6% of units beyond ±2 mV (seeded 0.0425) |
| 2 | Gauss–Markov noise, $\tau_c$ = 1 ms | $R(1\text{ ms}) \approx e^{-1} = 0.3679$ (seeded 0.3692); corner 159.2 Hz; area under the PSD ≈ 1 |
| 3 | kT/C | about 20.4–20.5 µV for both resistors against $\sqrt{kT/C}$ = 20.35 µV |
| 4 | shot noise at 1 nA, 1 ns bins | 6.242 electrons per bin on average; current variance $qI/\Delta t = 1.602\times10^{-19}$ A² |
| 5 | averaging | scatter ≈ $\sqrt{2\tau_c/T}$: 0.4472 at 10 ms and 0.1414 at 100 ms, the same at either sample rate (exact value at $T = 10\tau_c$: 0.4243) |
| 6 | 1/f and random walk | white-noise window means shrink fourfold per 16× window; 1/f window means barely shrink; random-walk spread grows as $\sqrt n$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 03-06.a | kT/C at 10 pF, 300 K | 20.35 | µV |
| Lab 03-06.b | Lorentzian corner, 1 ms | 159.2 | Hz |
| Lab 03-06.c | autocorrelation at one correlation time | 0.3679 | — |
| Lab 03-06.d | mean electrons per 1 ns bin at 1 nA | 6.242 | — |
| Lab 03-06.e | shot-noise current variance | 1.602×10^-19 | A² |
| Lab 03-06.f | averaging scatter, T = 10 ms | 0.4472 | — |
| Lab 03-06.g | averaging scatter, T = 100 ms | 0.1414 | — |
| Lab 03-06.h | exact scatter at T = 10 τc | 0.4243 | — |
| Lab 03-06.i | fraction of offsets beyond ±2 mV | 0.04550 | — |

## Discussion questions

1. Part 1's offset population is stationary but not ergodic. Name a production-test situation where treating a long recording of one unit as representative would mislead you.
2. Part 3's simulation gives the same voltage for 10 kΩ and 100 kΩ. Where does the extra noise density of the larger resistor go?
3. Part 6 shows that 1/f noise defeats averaging. What circuit techniques remove it, and what do they cost?

## Optional hardware version

With an oscilloscope or audio interface and a high-gain, low-noise amplifier, record the noise of a resistor (or the amplifier with its input shorted) for a long time. Estimate its PSD with Welch's method, locate the 1/f corner, and compare the white floor with $\sqrt{4kTR}$ referred through the amplifier's gain. Then average the record over increasing windows and see where averaging stops helping.
