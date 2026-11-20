# Course 11 · Final Exam (Signals and Systems)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 11 equation sheet](../../../reference/equation-sheets/11-signals-and-systems.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 5 points, each [B] 8, and Questions 13 and 14 [C] 12 each: 117 points in total. 82 or more (about 70%) is a strong pass.
- Within a question the lettered parts carry equal weight.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- CT frequency in hertz $f$ (or rad/s ω where stated); DT frequency ω in rad/sample, with $\omega = 2\pi f/f_s$ for sampled signals.
- Systems described by differential or difference equations are causal and at rest unless stated.
- $X(s)$ and $X(z)$ are bilateral; give every transform with its ROC.
- $\operatorname{sinc}(u) = \sin(\pi u)/(\pi u)$; Butterworth filters have $\lvert H\rvert^2 = 1/[1 + (f/f_c)^{2n}]$.

---

**1 [A] · Periodicity and power.** (11-01)
$x(t) = 3\cos(200\pi t) + 2\sin(300\pi t)$.
(a) Find its fundamental period.
(b) Find its average power (in V² if $x$ is in volts across 1 Ω).

**2 [B] · System properties.** (11-02)
(a) Classify each system as linear or not, time-invariant or not, causal or not, and BIBO-stable or not, with a one-line reason each: (i) $y(t) = t\,x(t)$; (ii) $y[n] = x[2n]$; (iii) $y[n] = 0.5y[n - 1] + x[n]$ (at rest).
(b) For system (iii), find the tightest bound on $\lvert y\rvert$ when $\lvert x\rvert \le B$, and an input that reaches it.

**3 [B] · Convolution.** (11-03)
(a) $x(t) = u(t) - u(t - 2)$ drives $h(t) = e^{-t}u(t)$. Find $y(1)$ and $y(3)$.
(b) Convolve $x[n] = \{1, 2, 3\}$ with $h[n] = \{1, -1\}$ (both starting at $n = 0$).

**4 [B] · A difference equation.** (11-04)
$y[n] = 1.2y[n - 1] - 0.36y[n - 2] + x[n]$.
(a) Find the characteristic roots and the impulse response.
(b) Find $h[3]$ and $h[4]$.
(c) Find the DC gain, and say whether the system is stable.

**5 [B] · A square wave's harmonics.** (11-05)
A ±1 V square wave with 50% duty cycle has period 1 ms.
(a) Find the amplitude of its third harmonic.
(b) Find the fraction of its power in the fundamental.
(c) Find its total harmonic distortion (THD, harmonics' RMS over the fundamental's).

**6 [B] · Transforms by properties.** (11-06)
Start from the pair $e^{-t}u(t) \leftrightarrow 1/(1 + j\omega)$, with $t$ in seconds. Use properties, not new integrals, in (a) and (b).
(a) Find the Fourier transform of $y(t) = e^{-2(t - 1)}u(t - 1)$, and evaluate $\lvert Y(j\omega)\rvert$ at ω = 2 rad/s.
(b) Find the Fourier transform of $z(t) = t\,e^{-t}u(t)$.
(c) Find the energy of $z$ twice: by integrating in time, and by Parseval's relation from your answer to (b).

**7 [B] · A four-point average.** (11-07)
$h[n] = \tfrac14\{1, 1, 1, 1\}$.
(a) Find $\lvert H(e^{j\omega})\rvert$ at ω = π/4.
(b) Find its nulls in $(0, \pi]$.
(c) Find its group delay.

**8 [B] · An inverse Laplace transform.** (11-08)
$X(s) = (s + 3)/[(s + 1)(s + 2)]$ with ROC σ > −1.
(a) Find the partial-fraction residues and $x(t)$.
(b) Evaluate $x(1)$.
(c) Which other ROCs are possible, and which of the three signals has a Fourier transform?

**9 [B] · Feedback and pole positions.** (11-08)
A plant $G(s) = K/[s(s + 4)]$ is placed in a unity negative-feedback loop.
(a) For $K$ = 13, find the closed-loop poles, ω₀ and ζ.
(b) Find the step overshoot.
(c) Find the $K$ that gives ζ = 0.7071.

**10 [B] · One formula, three sequences.** (11-09)
$X(z) = \dfrac{1}{(1 - 0.8z^{-1})(1 + 1.25z^{-1})}$.
(a) Expand $X(z)$ in partial fractions.
(b) List every possible ROC. For each, say whether the sequence is causal, anticausal or two-sided, and whether it is absolutely summable.
(c) For the absolutely summable one, write $x[n]$ and evaluate $x[0]$, $x[2]$ and $x[-1]$.

**11 [B] · A sampled-data chain.** (11-07, 11-10)
A 1 kHz cosine of amplitude 1 V is sampled at 8 kHz, filtered by $y[n] = \tfrac12(x[n] + x[n - 1])$, and played out by a DAC with a zero-order hold at 8 kHz and no smoothing filter.
(a) Find the DT filter's gain at the tone.
(b) Find the hold's droop at 1 kHz and the amplitude of the 1 kHz output.
(c) Find the frequency of the first image and its amplitude relative to the 1 kHz output, in dB.
(d) With no anti-aliasing filter, a 9 kHz input tone would also be sampled. At what frequency would it come out, and could any DT filter tell it from the 1 kHz tone?

**12 [B] · An AM link.** (11-11)
A conventional AM transmitter is modulated by a 3 kHz tone at $m$ = 0.6.
(a) Find the fraction of transmitted power in the sidebands.
(b) Find the largest envelope-detector time constant that avoids diagonal clipping.
(c) A receiver with a 10.7 MHz IF and a high-side LO is tuned to 100 MHz. Find its image frequency.

**13 [C] · Derivations.** (11-03, 11-08, 11-09, 11-10)
(a) Derive the spectrum of an ideally sampled signal, $X_s(f) = f_s\sum_kX(f - kf_s)$, starting from the impulse train's Fourier series.
(b) Using the ROC properties, prove that a causal LTI system with a *proper* rational system function (numerator degree no higher than the denominator's) is BIBO-stable exactly when all its poles have negative real parts. Why is "proper" needed?
(c) Derive the stability conditions $\lvert a_2\rvert < 1$ and $\lvert a_1\rvert < 1 + a_2$ for the poles of $z^2 + a_1z + a_2$ (real coefficients) to lie inside the unit circle.

**14 [C] · Diligence: an ECG start-up's claims.** (11-07, 11-09, 11-10)
A start-up's wearable ECG samples at 250 SPS. Its deck claims: "no analog anti-aliasing filter: our digital 60 Hz notch, only 0.1 Hz wide, removes all mains interference with zero latency."
(a) Using the estimate width ≈ $2(1 - r)$ rad/sample, find the pole radius such a notch needs, and its transient time constant in samples and seconds.
(b) Mains harmonics at 180 Hz and 300 Hz reach the input. Where do they appear after sampling, and does the notch remove them?
(c) Comment on "zero latency" for a causal IIR notch, and list the three questions you would ask the CTO.
