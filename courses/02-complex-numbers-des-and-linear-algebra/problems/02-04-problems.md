# Problems 02-04 · Forced Response and Resonance

Chapter: [02-04](../chapters/02-04-forced-response-and-resonance.md) · Worked solutions: [02-04 solutions](../solutions/02-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** answers to 4 significant figures unless stated; phases in degrees, measured as the output's phase relative to the input; $\omega_0$, ζ and $Q$ as in [reference/notation.md](../../../reference/notation.md).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-04.1 [A]

**Choosing the guess.** Write the form of a particular solution, with undetermined coefficients, without solving:

(a) $y'' + 4y = t^2$; (b) $y'' + 4y = e^{2t}$; (c) $y'' + 4y = \sin2t$; (d) $y'' - 2y' + y = e^t$; (e) $y'' + 2y' + 5y = e^{-t}\cos2t$.

### Problem 02-04.2 [A]

Solve $y'' + 4y = 8$ with $y(0) = 0$ and $y'(0) = 0$. What is the largest value of $y$, and when is it first reached? Why does an undamped system overshoot a step by 100%?

### Problem 02-04.3 [A]

Use the exponential response formula to find a particular solution of $y'' + 2y' + 5y = 10e^{-3t}$.

### Problem 02-04.4 [B]

Use complex replacement to find the steady-state response of $y'' + 2y' + 5y = \cos t$: its amplitude and its phase relative to the input.

### Problem 02-04.5 [B]

**The resonant response formula.**

(a) Find a particular solution of $y'' + 9y = 6\cos3t$. What is its envelope at $t = 4$?
(b) Find a particular solution of $y'' - y' - 2y = e^{2t}$.

### Problem 02-04.6 [B]

Solve $y'' + 3y' + 2y = 10\cos t$ with $y(0) = 0$ and $y'(0) = 0$. Identify the transient and the steady state, give the steady-state amplitude, and evaluate $y(1)$.

### Problem 02-04.7 [B]

**A lightly damped low-pass.** For $H = 1/(1 - r^2 + j2\zeta r)$ with ζ = 0.1:

(a) Find the frequency ratio $r$ of the peak and the peak gain, as a ratio and in dB.
(b) Find the gain at $r = 1$.
(c) Find the gain at $r = 10$, in dB, and compare with the −40 dB/decade asymptote.

### Problem 02-04.8 [B]

**A band-pass filter.** A series RLC has $R = 10$ Ω, $L = 1$ mH and $C = 10$ nF, with the output across the resistor.

(a) Find $\omega_0$, $f_0$ and $Q$.
(b) Find the half-power bandwidth in hertz and the two half-power frequencies.
(c) Show that the two half-power frequencies multiply to $f_0^2$.

### Problem 02-04.9 [B]

**Parallel resonance and current step-up.** An ideal 1 mA (peak) sinusoidal current source drives a parallel RLC with $R = 10$ kΩ, $L = 100$ µH and $C = 1$ nF, at the resonant frequency.

(a) Find $\omega_0$, $f_0$ and $Q = R\sqrt{C/L}$.
(b) What voltage appears across the tank, and what current flows in the capacitor? Explain why the capacitor's current can exceed the source's.

### Problem 02-04.10 [B]

**Beats.** Two equal tones, $\cos(2\pi\cdot440t)$ and $\cos(2\pi\cdot442t)$, are added.

(a) Write the sum as a product of two cosines.
(b) What is the pitch you hear, and how many times per second does the loudness swell?

### Problem 02-04.11 [B]

**Variation of parameters.**

(a) Derive $y_p = \cos t\,\ln(\cos t) + t\sin t$ for $y'' + y = \sec t$ on $(-\pi/2, \pi/2)$, and evaluate $y_p(\pi/4)$.
(b) Find a particular solution of $y'' + y = \tan t$ on the same interval, and evaluate it at $\pi/4$.

### Problem 02-04.12 [B]

**Resonant voltage step-up.** A 10 V (rms) source at the resonant frequency drives a series RLC with $R = 5$ Ω, $L = 1$ mH and $C = 1$ µF.

(a) Find $f_0$ and $Q$.
(b) Find the current, the power delivered, and the rms voltage across the capacitor.
(c) The capacitor is rated for 50 V. Is that adequate?

### Problem 02-04.13 [B]

**A MEMS gyroscope's drive resonator.** A MEMS gyroscope's proof mass is driven at the resonance of its drive mode, $f_0 = 25$ kHz with $Q = 10\,000$ (illustrative values).

(a) Find the half-power bandwidth.
(b) Driven at resonance from rest, how long does the amplitude take to reach 99% of its final value?
(c) If the drive frequency is 1 Hz away from resonance, what fraction of the resonant amplitude results?
(d) Explain why such sensors use a feedback loop that tracks the resonance instead of a fixed drive frequency.

### Problem 02-04.14 [C]

**Selecting a harmonic.** A ±1 V square wave at 10 kHz drives a series RLC band-pass (output across the resistor) tuned to 30 kHz with $Q = 10$. The square wave's Fourier series is $\sum_{n\text{ odd}}\frac{4}{n\pi}\sin(n\omega t)$ (01-06).

(a) Find the output amplitude of the 1st, 3rd, 5th and 7th harmonics.
(b) What does the output look like? How large is the strongest unwanted component relative to the wanted one?
(c) How would a higher $Q$ change the result?

### Problem 02-04.15 [C]

**A workload that excites the supply.** Use the power-delivery network of Example 02-03.5 ($L = 25$ pH and $R = 1$ mΩ in series from the regulator, $C = 100$ nF at the die). A processor's current has a component of 1 A amplitude that oscillates sinusoidally at frequency $f$ (for example, a loop that alternately wakes and idles a large unit).

(a) Show that the impedance the load sees is $Z = (R + j\omega L)\parallel\dfrac{1}{j\omega C}$, and that at $\omega_0$ it is approximately $\dfrac{L/C}{R} = Q\sqrt{L/C}$.
(b) Find $f_0$ and $\lvert Z\rvert$ at $f_0$, at 50 MHz and at DC.
(c) What voltage ripple does the 1 A component cause at each of those frequencies? What does this imply for software and hardware design?

### Problem 02-04.16 [B]

**Variation of parameters with a changing Wronskian.** Solve $y'' - 3y' + 2y = \dfrac{1}{1 + e^{-t}}$ (a smooth "soft-start" input).

(a) Find two homogeneous solutions and their Wronskian.
(b) Use variation of parameters to find a particular solution, and evaluate it at $t = 0$.
(c) Why would undetermined coefficients not work here?

### Problem 02-04.17 [B]

**A product input.** Find a particular solution of $y'' + 4y = t\sin t$ by undetermined coefficients, and evaluate it at $t = \pi/2$. Explain why no factor of $t$ beyond the input's own is needed.

---

## Objective coverage

| Learning objective (chapter 02-04) | Problems |
|---|---|
| 1. Homogeneous + particular; superposition; transient and steady state | 2, 6, 14 |
| 2. Undetermined coefficients, the duplication rule; variation of parameters | 1, 2, 5, 11, 16, 17 |
| 3. Exponential response formula; complex replacement | 3, 4, 5, 6 |
| 4. Frequency response; peak; half-power bandwidth | 7, 8, 9, 14 |
| 5. Undamped resonance, beats, build-up; Q versus settling | 5(a), 10, 13 |
| 6. Resonance in products | 9, 12, 13, 15 |
