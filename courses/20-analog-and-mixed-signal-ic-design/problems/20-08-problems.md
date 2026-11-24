# Problems 20-08 · Oversampling and Sigma-Delta Converters

Chapter: [20-08](../chapters/20-08-sigma-delta-converters.md) · Worked solutions: [20-08 solutions](../solutions/20-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Quantizer levels span [−1, +1]: a 1-bit quantizer has step Δ = 2, an $M$-level quantizer Δ = $2/(M - 1)$. 0 dBFS is a sine of amplitude 1; −6 dBFS means amplitude 0.5. Linear-model in-band noise: $(\Delta^2/12)\,\pi^{2L}/[(2L + 1)\,\text{OSR}^{2L+1}]$. $kT$ = 4.1419 × 10⁻²¹ J. Problems marked *(lab)* can be checked with `labs/20-08-lab/dsm.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-08.1 [A]

**Oversampling a 10-bit quantizer.** A 10-bit quantizer runs at OSR = 16 without noise shaping. What in-band SQNR does a full-scale sine reach, and how many bits is that equivalent to at the Nyquist rate?

### Problem 20-08.2 [A] *(lab)*

**A negative input.** A first-order modulator ($u[n + 1] = u[n] + x - y[n]$, $y = \text{sign}(u)$) starts at $u[0]$ = 0.3 with $x$ = −0.4. Find $u[1]$ to $u[4]$, the long-run fraction of +1 outputs and the period of the output pattern.

### Problem 20-08.3 [A] *(lab)*

**An idle tone.** A first-order modulator runs at $f_s$ = 2.56 MHz with OSR = 64. For a DC input of 0.004, where is the lowest strong idle tone and what is its amplitude (use the chapter's $2\lvert x\rvert$ rule)? What is the band edge, and below what input do idle tones fall in band?

### Problem 20-08.4 [B]

**Third order, linear model.** Ignoring stability, find the linear-model SQNR of a third-order modulator ($\text{NTF} = (1 - z^{-1})^3$) at OSR = 32 for a −6 dBFS sine, with a 1-bit and with a 16-level quantizer.

### Problem 20-08.5 [B]

**Order against oversampling.** For a 1-bit quantizer and a −6 dBFS sine, what OSR does the linear model require for 90 dB with a first-order and with a second-order loop?

### Problem 20-08.6 [B]

**Optimal zeros.** Show that the in-band noise of a second-order NTF with zeros at $\pm\omega_z$ is minimized for $\omega_z = \omega_B/\sqrt3$. Where are the zeros for a 24 kHz band, and how much noise do they save?

### Problem 20-08.7 [B]

**Reading an NTF.** For $\text{NTF} = (1 - z^{-1})^2$, find the noise power gain $\lvert\text{NTF}\rvert^2$ at $f_s/4$, the magnitude gain at $f_s/2$, and the power gain at the band edge for OSR = 64 (in dB).

### Problem 20-08.8 [B]

**A 2-1 MASH.** The first stage is the second-order loop of §3.3 (STF $z^{-2}$, NTF $(1 - z^{-1})^2$); the second stage is a first-order loop driven by $-E_1$. Find digital filters $D_1$, $D_2$ that cancel $E_1$ in $Y = D_1Y_1 + D_2Y_2$, the order of the resulting NTF, and its linear-model SQNR at OSR = 64 for a −6 dBFS sine (1-bit second stage).

### Problem 20-08.9 [B]

**Capacitor for a precision converter.** A ΔΣ ADC must keep its in-band kT/C noise (single-ended, one sampling event per period) 120 dB below a full-scale sine of 2.5 V amplitude. Find the sampling capacitor at OSR = 256 and at OSR = 64.

### Problem 20-08.10 [B]

**Op-amp gain.** (a) A first-order single loop at OSR = 128 has $C_s/C_i$ = 0.5. Below what op-amp gain does integrator leakage dominate? (b) A 1-1 MASH at OSR = 128 has $C_s = C_i$. What gain does it need, in V/V and dB?

### Problem 20-08.11 [B]

**A quarter-period delay.** A first-order continuous-time loop has an excess loop delay of a quarter of a clock period. Find the radius of its NTF poles and its NTF magnitude at $f_s/2$, and compare with no delay.

### Problem 20-08.12 [B]

**Jitter budget.** A second-order CT modulator with NRZ feedback runs at $f_s$ = 640 MHz with OSR = 16 and a −6 dBFS input. Using $E[(\Delta y)^2]$ = 2.36 (1-bit) and 0.0298 (16 levels), find the largest rms clock jitter that keeps the jitter noise 70 dB below the signal for each.

### Problem 20-08.13 [C]

**Anti-aliasing for free.** A first-order CT modulator runs at OSR = 32. How much does it attenuate an interferer at $f_s - f_B$, which would alias onto the band edge? What does a discrete-time modulator do with the same interferer?

### Problem 20-08.14 [C]

**Choosing the decimator.** A third-order modulator at OSR = 128 feeds a CIC that decimates by 32, followed by half-band filters. What is the minimum CIC order, its droop at the band edge, and its register growth?

### Problem 20-08.15 [C]

**A 20 MHz receiver ADC.** A receiver needs 70 dB peak SQNR (linear model, −6 dBFS) in a 20 MHz band. Compare a second-order 1-bit loop with a third-order 16-level loop (pure differentiator NTFs): minimum OSR and modulator clock rate for each. Which would you choose, given Example 20-08.7?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. In-band noise and the $(6L + 3)$ dB law | 1, 4, 5, 7 |
| 2. First-order loop, averaging and idle tones | 2, 3 |
| 3. Stability and NTF zeros | 6, 7 |
| 4. MASH and op-amp gain | 8, 10 |
| 5. Continuous-time loops: aliasing, delay, jitter | 11, 12, 13 |
| 6. Sizing a modulator and its decimator | 9, 14, 15 |
