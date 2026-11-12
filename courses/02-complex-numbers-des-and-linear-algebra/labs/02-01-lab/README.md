# Lab 02-01 · Complex Numbers, Euler's Formula and Phasors

**Chapter:** [02-01](../../chapters/02-01-complex-numbers-euler-and-phasors.md) · **Notebook:** [02-01-phasors.ipynb](02-01-phasors.ipynb) · **Time:** about 1.5 hours (plus 1 hour for the optional hardware part)

## Objective

See, by computation rather than by algebra, that:

1. complex arithmetic and the quadrant-correct angle behave as the chapter claims;
2. the Taylor series of $e^{j\theta}$ really lands on $\cos\theta + j\sin\theta$;
3. adding phasors gives exactly the same waveform as adding sinusoids point by point;
4. a linear circuit driven by a sinusoid settles, after a transient, onto exactly the amplitude and phase predicted by $H(j\omega)$;
5. a series RLC circuit's current peaks at $\omega_0 = 1/\sqrt{LC}$, with a sharpness set by $Q$.

## Background

Read chapter sections 3.3–3.12 first. The key relations are:

- $z = x + jy = r\angle\theta$, with $\theta = \operatorname{atan2}(y, x)$;
- $e^{j\theta} = \cos\theta + j\sin\theta$;
- $v(t) = \operatorname{Re}\lbrace\mathbf{V}e^{j\omega t}\rbrace$;
- $d/dt \leftrightarrow j\omega$;
- $H = 1/(1 + j\omega RC)$ for the RC low-pass;
- $Z = R + j(\omega L - 1/(\omega C))$ for the series RLC.

## Procedure

1. Open the notebook in JupyterLab (from the repository root, run `jupyter lab`) and choose **Run → Run All Cells**. Every cell should run without errors; each part ends with an `assert` comparing simulation with theory.
2. Work through Parts A–E in order. At each **🔮 Predict** prompt:
   1. Write your prediction on paper, with the calculation that produced it.
   2. Change the parameter named in the prompt and re-run that cell.
   3. Record the result next to your prediction. If they disagree, find out why before moving on. That moment of surprise is where the learning happens.
3. Answer the discussion questions below.

## Expected results

Check your predictions against these only after you have made them.

| Part | Prediction | Expected result |
|---|---|---|
| A | Angles of $-1 - j$, $-5$, $-j3$, $2 - j2$ | −135°, 180°, −90°, −45° |
| B | Highest power $N$ needed for error < $10^{-6}$ at $\theta = \pi$ | $N = 16$, i.e. 17 terms ($n = 0, \ldots, 16$); the first omitted term, $\pi^{17}/17!$, is about $8\times10^{-7}$ |
| C | `ph2` for $v_2$ to oppose $v_1$; resulting amplitude | −60°, so $v_2 = 5\cos(\omega t - 150^\circ)$; amplitude 5 V |
| C | `ph2` for $v_2$ to align with $v_1$; resulting amplitude | 120°; amplitude 15 V |
| D | $C = 1\ \mu$F: $\omega RC$, $\lvert H\rvert$, output amplitude, phase | 6.283; 0.1572; 0.7859 V; −80.96° |
| D | $C = 1\ \mu$F: duration of the start-up transient | about $5\tau = 5$ ms |
| D | $f$ at the corner frequency: output amplitude and phase | 3.536 V (that is, $5/\sqrt{2}$); −45° |
| E | $R = 2\ \Omega$: peak current, $Q$, $\omega_0$ | 5 A; 7.071; unchanged at 707.1 rad/s (sharper peak) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-01.A1 | angle of −1 − j | −135.0 | ° |
| Lab 02-01.B1 | highest power N needed at θ = π | 16 | — |
| Lab 02-01.C1 | opposing amplitude | 5 | V |
| Lab 02-01.C2 | aligned amplitude | 15 | V |
| Lab 02-01.D1 | $\omega RC$ with 1 µF | 6.283 | — |
| Lab 02-01.D2 | $\lvert H\rvert$ with 1 µF | 0.1572 | — |
| Lab 02-01.D3 | output amplitude with 1 µF | 0.7859 | V |
| Lab 02-01.D4 | phase with 1 µF | −80.96 | ° |
| Lab 02-01.D5 | output amplitude at corner | 3.536 | V |
| Lab 02-01.E1 | peak current with R = 2 Ω | 5.000 | A |
| Lab 02-01.E2 | Q with R = 2 Ω | 7.071 | — |
| Lab 02-01.Q1 | steady-state output at t = 0 (discussion Q1) | 3.58 | V |
| Lab 02-01.H1 | amplitude ratio with 50 Ω source | 0.835 | — |
| Lab 02-01.H2 | delay with 50 Ω source | 92.8 | µs |

## Discussion questions

1. In Part D, the output starts at 0 V but the steady-state formula says the output at $t = 0$ should be $4.234\cos(-32.14^\circ) = 3.58$ V. Which part of the full solution makes up the difference, and how fast does it decay?
2. In Part B, why does convergence take more terms for larger $\theta$? What does that imply for a hardware block that must compute $e^{j\theta}$ for any angle? (Hint: real hardware first reduces the angle to a small range using symmetry.)
3. In Part E, the resistor value changes the height and sharpness of the resonance peak but not its location. Explain why, using the expression for $Z$.
4. The notebook's least-squares fit in Part D measures amplitude and phase from two cycles of data. How is this related to the way a *lock-in amplifier* or a radio's I/Q demodulator extracts a phasor from a noisy signal?

## Optional hardware version

**Equipment:** breadboard, a 1 kΩ resistor, a 100 nF capacitor, a function generator and a two-channel oscilloscope. A USB multi-instrument works; see [SETUP.md](../../../../SETUP.md#7-optional-hardware-kit).

1. Build the RC low-pass of Example 02-01.4: generator → 1 kΩ → output node → 100 nF → ground.
2. Set the generator to a 1 kHz sine of 1 V amplitude. That is safer than 5 V and makes no difference for a linear circuit.
3. Put channel 1 on the input and channel 2 on the output. Measure the amplitude ratio and the time between corresponding zero crossings.
4. **Expected:** ratio ≈ 0.847 and delay ≈ 89 µs (a 32° lag) for an ideal source. A typical function generator has a 50 Ω output resistance, which adds to the 1 kΩ: with $R = 1050\ \Omega$, expect a ratio of about 0.835 and a delay of about 92.8 µs. Typical parts are ±5% (R) and ±10% (C), so a few percent of further disagreement is normal.
5. Sweep the frequency from 100 Hz to 20 kHz and record the ratio and phase at a few points. Compare them with $\lvert H\rvert$ and $\angle H$. You have just measured a Bode plot, the subject of [07-07](../../../07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md).
