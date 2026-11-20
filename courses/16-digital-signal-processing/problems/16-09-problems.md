# Problems 16-09 · Multirate DSP: Decimation, Interpolation and Polyphase

Chapter: [16-09](../chapters/16-09-multirate-dsp.md) · Worked solutions: [16-09 solutions](../solutions/16-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $\downarrow M$ keeps samples $0, M, 2M, \dots$; $\uparrow L$ inserts $L - 1$ zeros after each sample. Polyphase components are $E_k[n] = h[nM + k]$. Multiplication counts ignore symmetry unless "folded" is stated. CIC filters have differential delay 1. Problems marked *(lab)* need the lab's `multirate.py`, SciPy's `remez`, or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-09.1 [A]

**Aliases.** A 48 kHz signal is downsampled by 3 without filtering. Where do components at 7, 9 and 13 kHz appear?

### Problem 16-09.2 [A]

**Images.** A 1 kHz tone sampled at 8 kHz is upsampled by 4 by inserting zeros. List every frequency present between 0 and 16 kHz.

### Problem 16-09.3 [A]

**A noble identity by hand.** Let $x = (1, 2, 3, 4, 5, 6)$ and $h = (1, 1)$. Compute (a) the output of $H(z^2)$ followed by $\downarrow 2$, and (b) the output of $\downarrow 2$ followed by $H(z)$. (Keep the first three outputs.)

### Problem 16-09.4 [B]

**Polyphase components.** For $h = (1, 2, 3, 4, 5, 6, 7)$ and $M = 3$, write $E_0$, $E_1$ and $E_2$. If this filter decimates a 30 kHz signal by 3, how many multiplications per second does the polyphase form need, against filtering at the input rate?

### Problem 16-09.5 [B]

**44.1 kHz to 48 kHz.** (a) Find the smallest $L$ and $M$ and the intermediate rate. (b) A 3200-tap prototype filter runs at the intermediate rate. How many multiplications per second does a naive implementation need, and how many does a polyphase converter (one phase per output) need?

### Problem 16-09.6 [B]

**Half-band polyphase.** A 59-tap half-band filter decimates by 2 from 96 kHz to 48 kHz. Write its two polyphase components in terms of its taps, count nonzero taps and folded multipliers, and give the multiplications per second.

### Problem 16-09.7 [B]

**A CIC decimator.** A three-stage CIC decimates by 16 from 1.6 MHz to 100 kHz. Find its DC gain and register growth, its passband droop at 10 kHz, and its attenuation at 90 kHz. What does the 90 kHz figure protect?

### Problem 16-09.8 [A]

**CIC register width.** A five-stage CIC decimates a 16-bit input by 64. How wide must every register be, and what must the integrators do on overflow?

### Problem 16-09.9 [B]

**An interpolator's cost.** Audio at 48 kHz is interpolated by 4 to 192 kHz, keeping 0–20 kHz with $\delta_p = 10^{-3}$ and suppressing images from 28 kHz by 80 dB. Estimate the filter order with Kaiser's formula (16-06), then give the multiplications per second computed naively at 192 kHz and in polyphase form.

### Problem 16-09.10 [C]

**Two half-bands or one filter?** *(lab)* Decimate 192 kHz to 48 kHz with a 20 kHz passband, $\delta_p = 10^{-3}$, 80 dB alias protection for the passband. Find the shortest single-stage equiripple filter and the shortest half-band stages (each with $\delta = 10^{-4}$ in both bands), and compare folded multiplications per second.

### Problem 16-09.11 [C]

**Check a data sheet.** The ADS127L11's sinc4 filter at OSR 64 in high-speed mode ($f_{MOD}$ = 12.8 MHz) lists a data rate of 200 kSPS, a −3 dB frequency of 45.5 kHz and a latency of 20.63 µs (R-243). Predict the −3 dB frequency and the impulse-response span from CIC theory and compare.

### Problem 16-09.12 [B]

**A polyphase interpolator by hand.** Interpolate $x = (2, 4, 6)$ by $L = 2$ with $h = (0.5, 1, 0.5)$. Find $E_0$ and $E_1$, compute both output phases, interleave them, and interpret the result.

---

## Objective coverage

| Learning objective (chapter 16-09) | Problems |
|---|---|
| 1. Spectra of down- and upsampled signals | 1, 2 |
| 2. Decimation, interpolation and rational filters | 5, 9 |
| 3. Noble identities and polyphase structures | 3, 4, 6, 12 |
| 4. Multistage and half-band designs | 6, 10 |
| 5. CIC filters | 7, 8, 11 |
| 6. Sample-rate conversion design | 5, 9 |
