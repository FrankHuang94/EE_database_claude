# Lab 16-02 · Poles, Zeros, Phase and Equalizers

Chapter: [16-02 DTFT and z-Transform for DSP](../../chapters/16-02-dtft-and-z-transform-for-dsp.md)

## Objective

Use the z-plane as a design tool: read frequency responses off pole and zero positions, build notches and resonators and see their bandwidth–settling tradeoff, compare minimum-, linear- and maximum-phase filters with one magnitude response, and equalize a channel that is not minimum phase.

## Background

Read §3 of the chapter. `pz.py` computes frequency responses directly from coefficients and from the pole–zero vector formula of §3.2, group delay in closed form (§3.4) and numerically, and builds the filters of §3.3, §3.5 and §3.6. The equalizer helper returns the delayed, truncated anticausal inverse of §3.7.

## Files

- [pz.py](pz.py): `freq_resp`, `zpk`, `geometric`, `group_delay`, `group_delay_numeric`, `notch`, `resonator`, `dc_blocker`, `allpass1`, `minimum_phase_fir`, `partial_energy` and `anticausal_inverse`.
- [16-02-pole-zero-lab.ipynb](16-02-pole-zero-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Walk the unit circle (Part 1).** For Example 16-02.1, compare `freq_resp` and `geometric`, and plot the pole–zero diagram with the vectors to $e^{j\omega}$ at $\omega = 0$, $\pi/2$ and $\pi$.
2. **Notch the hum (Part 2).** Build a 10 Hz signal at $f_s$ = 1 kHz with 50 Hz hum that switches on at 0.5 s. Filter it with notches of $r$ = 0.9, 0.98 and 0.995 and plot the residual hum against time. *Predict first:* which notch is best 20 ms after the hum starts, and which after one second?
3. **Tune a resonator (Part 3).** For $\omega_0 = \pi/4$, sweep $r$ from 0.9 to 0.999, measure $Q$ and compare with $\omega_0/[2(1 - r)]$.
4. **Three phases, one magnitude (Part 4).** Compare $(2, -2, 0.5)$, $(1, -2.5, 1)$ and $(0.5, -2, 2)$: magnitude, impulse response, partial energy and group delay.
5. **Equalize a link (Part 5).** Send 200,000 random ±1 symbols (seed 42) through the channel $(0.8, 1)$, add Gaussian noise of standard deviation $\sigma$ = 0.1 and 0.3, and equalize with Example 16-02.5's $K$-tap filter for $K$ = 5, 10 and 21. For each $K$ record the eye opening without noise, $1 - 0.8^K$; the noise gain $\lVert e\rVert = \sqrt{\sum e[n]^2}$; and the symbol error rate after slicing at zero, taking the $K$-sample delay into account. Compare with no equalizer (slicing the main cursor directly). *Predict first:* does doubling $K$ from 10 to 21 halve the error rate?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Geometric versus direct | identical to machine precision; gain 4, 1.265 and 0 at $\omega = 0$, $\pi/2$, $\pi$ |
| 2 | Notches | $r$ = 0.9 removes the hum within a few tens of milliseconds but also dents the 10 Hz signal (gain 0.988); $r$ = 0.995 has a 1.6 Hz notch but its time constant is 199.5 ms |
| 3 | Resonator $Q$ | follows $\omega_0/[2(1 - r)]$ within about 1% for $r \ge 0.98$ |
| 4 | Phase family | same magnitude; first-sample energy 0.485, 0.121, 0.0303; DC group delay −2, 1, 4 samples |
| 5 | Equalizer | eye opening 0.672, 0.893, 0.991; noise gain 1.575, 1.657, 1.667; at $\sigma$ = 0.1 errors fall from 1.2% unequalized to essentially none; at $\sigma$ = 0.3 from 13% to 4.0%, 2.5% and 2.3%: diminishing returns, because the equalizer amplifies noise by about 1.67 whatever $K$ is |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-02.a | 10 Hz gain of the r = 0.9 notch | 0.988 | — |
| Lab 16-02.b | −3 dB width of the r = 0.995 notch | 1.6 | Hz |
| Lab 16-02.c | time constant of the r = 0.995 notch | 199.5 | ms |
| Lab 16-02.d | residual ISI, K = 21 | 0.0092 | — |
| Lab 16-02.e | eye opening, K = 5 | 0.672 | — |
| Lab 16-02.f | noise gain, K = 21 | 1.667 | — |
| Lab 16-02.g | error rate without equalizer, σ = 0.1 | 1.2 | % |
| Lab 16-02.h | error rate without equalizer, σ = 0.3 | 13 | % |
| Lab 16-02.i | error rate, K = 5, σ = 0.3 | 4.0 | % |
| Lab 16-02.j | error rate, K = 10, σ = 0.3 | 2.5 | % |
| Lab 16-02.k | error rate, K = 21, σ = 0.3 | 2.3 | % |

## Discussion

1. In Part 2, why can no choice of $r$ give a notch that is both very narrow and fast to settle?
2. In Part 3, why does the rule $Q \approx \omega_0/[2(1 - r)]$ get worse as $r$ falls?
3. In Part 4, the three filters sound identical on a steady tone. On what kind of signal would you hear a difference?
4. In Part 5, why does going from 10 to 21 taps barely improve the error rate at $\sigma$ = 0.3, and what would a decision-feedback equalizer change?

### Answers

1. The pole radius sets both: the −3 dB width is about $2(1 - r)$ rad/sample and the time constant about $1/(1 - r)$ samples, so their product is about 2 whatever $r$ is (§3.3). Narrowness in frequency is length in time.
2. The rule treats the vector to the near pole as the only thing that varies near $\omega_0$; as $r$ falls, the peak widens and the far pole and the zeros at ±1 change appreciably across it, skewing the peak and shifting it slightly off $\omega_0$.
3. On transients: clicks, drum hits, the onset of a note. Their different group delays spread a transient's frequency components differently in time; the maximum-phase version smears energy later and the linear-phase one rings symmetrically (pre-ringing).
4. Beyond about 10 taps the residual ISI is already small (0.107, then 0.009), and the errors are set by noise. The equalizer's taps $e[n] = (-0.8)^{K-1-n}$ have energy approaching $1/(1 - 0.64)$, a noise gain of 1.67, so the output noise is two-thirds larger than the input noise for any long equalizer: this is noise enhancement, the price of inverting a channel whose response dips (here to $\lvert 0.8 - 1\rvert$ = 0.2 at $\omega = \pi$, where the equalizer's gain must approach 5). A decision-feedback equalizer subtracts the contributions of *past* decisions without amplifying noise, but it cannot remove *precursor* ISI, which is the whole problem with this channel: precursors need feed-forward taps and their latency. Practical receivers combine a short FFE for precursors with a DFE for postcursors.

## Optional hardware

With an audio interface and a laptop, record a hum-contaminated signal (a guitar pickup near a transformer works), run the notches of Part 2 on the recording in Python, and listen to the residual. Then add a click track and compare the minimum- and maximum-phase filters of Part 4 by ear.
