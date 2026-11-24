<!-- status: reviewed -->
# 20-08 · Oversampling and Sigma-Delta Converters

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The oversampling-converter material of a graduate data-converter course: oversampling, noise shaping, loop order and stability, multi-bit and cascaded (MASH) modulators, continuous-time modulators and decimation (Schreier, Pavan and Temes, *Understanding Delta-Sigma Data Converters*, 2nd ed.; Johns and Martin, *Analog Integrated Circuit Design*, the oversampling chapter) |
| **Prerequisites** | [20-06](20-06-data-converter-fundamentals.md) (quantization noise, SQNR, processing gain), [20-05](20-05-comparators-and-sample-and-hold.md) (kT/C noise, jitter), [11-09](../../11-signals-and-systems/chapters/11-09-z-transform.md) (z-transform), [16-09](../../16-digital-signal-processing/chapters/16-09-multirate-dsp.md) (decimation and CIC filters) |
| **Estimated study hours** | 9 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Compute the in-band quantization noise of an oversampled quantizer and of an $L$-th-order delta-sigma modulator, and derive the $(6L + 3)$ dB-per-octave law.
2. Trace a first-order modulator by hand, prove that its output average equals its input, and predict its idle tones.
3. Explain why high-order single-bit loops go unstable, apply Lee's rule and place noise-transfer-function zeros optimally.
4. Derive the noise cancellation of a MASH modulator and the op-amp gain it requires, and contrast it with a single loop.
5. Analyze a continuous-time modulator's anti-aliasing, excess loop delay and clock-jitter sensitivity.
6. Size a modulator (order, quantizer, oversampling ratio, sampling capacitor) for a resolution and bandwidth target.

## 1. Big picture

A Nyquist-rate converter (20-07) buys resolution with precision: matched capacitors, accurate amplifiers, low-offset comparators. An oversampling converter buys it with speed instead. It samples far faster than the signal requires, uses a coarse quantizer (often a single comparator) inside a feedback loop, and arranges the loop so that most of the quantization noise lands at frequencies above the signal band, where a digital filter removes it. The loop's analog accuracy requirements collapse: a 1-bit quantizer is perfectly linear, and the integrators need only modest gain. That trade (speed and digital filtering for analog precision) is why delta-sigma (ΔΣ, also written sigma-delta) converters dominate wherever bandwidth is modest and resolution is high.

- **Audio** ADCs and DACs in phones, headsets, cars and studios are almost all ΔΣ.
- **Precision measurement** (weigh scales, thermocouples, metering, test equipment) uses ΔΣ converters with 24-bit output words.
- **Sensors and biopotential front ends** in wearables and medical devices digitize slow signals with very low power.
- **Digital microphones** send the raw 1-bit modulator output (a pulse-density-modulated stream) over a two-wire interface.
- **Wireless receivers** use continuous-time ΔΣ modulators with tens of megahertz of bandwidth, and fractional-N frequency synthesizers use digital ΔΣ modulators to dither a divider ratio (20-10).

## 2. Intuition first

```text
          x ──►(+)──► ∫ (integrator) ──► quantizer ──┬──► y (coarse, fast) ──► digital low-pass + decimate ──► fine, slow
                ▲ −                                   │
                └──────────────── DAC ◄───────────────┘
```

*Figure 1. A delta-sigma modulator. The integrator accumulates the difference between the input and the fed-back output; the quantizer rounds it coarsely; feedback forces the output to track the input on average.*

**A running-balance analogy, and its limits.** Suppose you must pay a stream of bills of arbitrary amounts, but you may only pay in whole hundreds of dollars. Rounding each bill independently leaves an error of up to 50 dollars every time, and the errors never cancel. Instead, keep a running balance of what you owe: pay 100 whenever the balance is positive, nothing otherwise. Each payment is still coarse, but the balance never drifts far from zero, so over any long period your total payments match your total bills to within one payment. A ΔΣ modulator does exactly this. The integrator is the running balance; the quantizer is the coarse payment; the output's *average* over many samples equals the input with an error that shrinks as the averaging window grows. The error is not removed but pushed to high frequencies (rapid alternation of over- and underpayment), where the digital filter averages it out. The analogy breaks in three places. The input changes while you average, so the converter only works for signals much slower than the sample rate. The averaging is a filter whose design matters (§3.8). And with more than one level of "balance" (higher-order loops) the bookkeeping can run away entirely, which has no counterpart in a sensible accountant (§3.4).

## 3. Theory

> **Conventions.** The quantizer's output levels span $[-1, +1]$: a 1-bit quantizer outputs ±1, so its step is Δ = 2; an $M$-level quantizer has Δ = $2/(M - 1)$. A full-scale (0 dBFS) sine has amplitude 1. $f_s$ is the modulator sample rate, $f_B$ the signal bandwidth, and the **oversampling ratio** is $\text{OSR} = f_s/(2f_B)$. Normalized frequency ω = $2\pi f/f_s$ (radians per sample), so the band edge is $\omega_B = \pi/\text{OSR}$.

### 3.1 Oversampling alone

20-06 modeled quantization error as white noise of variance $\Delta^2/12$, spread evenly from 0 to $f_s/2$ (valid for a busy signal or with dither, 16-10). If the signal occupies only $[0, f_B]$, a digital low-pass filter can discard all noise above $f_B$, keeping the fraction $f_B/(f_s/2) = 1/\text{OSR}$:

$$
P_{q,\text{in-band}} = \frac{\Delta^2}{12}\cdot\frac{1}{\text{OSR}}, \qquad
\text{SQNR} = 6.02N + 1.76 + 10\log_{10}\text{OSR} \text{ dB}.
$$

This is 20-06's processing gain: 3 dB, half a bit, per doubling of the sample rate. It is a poor bargain. Gaining four bits (24 dB) needs OSR = 4⁴ = 256 (Example 20-08.1); gaining twelve would need 4¹² ≈ **1.7×10⁷**. The noise is spread evenly, so most of it is discarded only in proportion to bandwidth. Noise shaping does better by moving the noise itself.

### 3.2 The first-order modulator

**The loop.** Let $u[n]$ be the integrator's value at sample $n$. The quantizer outputs $y[n] = \text{sign}(u[n])$ (±1), and the integrator accumulates the input minus the output:

$$
u[n + 1] = u[n] + x[n] - y[n] .
$$

**Linear model.** Write the quantizer as an error source, $y[n] = u[n] + e[n]$. In the z-domain, $zU = U + X - Y$, so $U = z^{-1}(X - Y)/(1 - z^{-1})$. Substituting $U = Y - E$:

$$
(Y - E)(1 - z^{-1}) = z^{-1}(X - Y) \;\Rightarrow\; Y = z^{-1}X + (1 - z^{-1})E .
$$

The **signal transfer function** (STF) is a one-sample delay; the **noise transfer function** (NTF) is $1 - z^{-1}$, a differentiator. On the unit circle, $\lvert\text{NTF}(e^{j\omega})\rvert = \lvert 1 - e^{-j\omega}\rvert = 2\lvert\sin(\omega/2)\rvert$: zero at DC, rising to 2 at $f_s/2$. The quantization error is still there, but it is high-pass filtered: **noise shaping**.

**In-band noise.** With $e$ white of variance $\sigma_e^2 = \Delta^2/12$, its two-sided spectral density is $\sigma_e^2/2\pi$ per radian per sample on $(-\pi, \pi)$. The in-band output noise is

$$
P_q = \frac{\sigma_e^2}{\pi}\int_0^{\omega_B}\lvert\text{NTF}(e^{j\omega})\rvert^2\,d\omega
= \frac{\sigma_e^2}{\pi}\int_0^{\omega_B}\left(2 - 2\cos\omega\right)d\omega
= \frac{2\sigma_e^2}{\pi}\left(\omega_B - \sin\omega_B\right) ,
$$

using $4\sin^2(\omega/2) = 2 - 2\cos\omega$. For a large OSR the band edge is a small angle, and $\omega_B - \sin\omega_B \approx \omega_B^3/6$, so

$$
P_q \approx \frac{\sigma_e^2\,\omega_B^3}{3\pi} = \frac{\sigma_e^2\,\pi^2}{3\,\text{OSR}^3} .
$$

Doubling the OSR now cuts the noise eightfold: 9 dB, 1.5 bits per octave.

> **Math refresher — small-angle expansions.** $\sin\theta = \theta - \theta^3/6 + \theta^5/120 - \cdots$, so $\theta - \sin\theta = \theta^3/6 - \cdots$. Equivalently, $4\sin^2(\omega/2) \approx \omega^2$ for small ω, and $\int_0^{\omega_B}\omega^2\,d\omega = \omega_B^3/3$ gives the same leading term. The approximation is excellent in band: at OSR = 16 the exact and approximate integrals differ by **0.2**%.

**The output average equals the input.** Summing the loop equation over $N_s$ samples, $\sum_{n=0}^{N_s-1}(x[n] - y[n]) = u[N_s] - u[0]$. If the integrator stays bounded, the average of $y$ equals the average of $x$ with an error of at most $(\max\lvert u\rvert \cdot 2)/N_s$. It does stay bounded for $\lvert x\rvert \le 1$: if $0 \le u \le 1 + \lvert x\rvert$, the output is +1 and the next value $u + x - 1$ lies between $x - 1 \ge -(1 + \lvert x\rvert)$ and $\lvert x\rvert + x \le 1 + \lvert x\rvert$; the case $u < 0$ is symmetric. So $\lvert u\rvert \le 1 + \lvert x\rvert$ forever, and a first-order loop cannot overload for inputs inside the DAC's range.

**Idle tones.** The linear model assumes the error is white, which fails badly for a first-order loop with a constant or slowly varying input. A DC input $x$ produces a periodic output (Example 20-08.2): for $x = 0.2$ the pattern repeats every five samples. For a small DC input the output alternates +1, −1 and slips (two +1s in a row) once every $1/\lvert x\rvert$ samples; that slip train is a periodic signal, and the lab's simulation shows tones at multiples of $\lvert x\rvert f_s$ with amplitude $2\lvert x\rvert$. They fall in the signal band when $\lvert x\rvert f_s < f_B$, that is when $\lvert x\rvert < 1/(2\,\text{OSR})$: small inputs, exactly where an audio converter is listened to most critically. These **idle tones** (also called limit cycles) were reported in the very first ΔΣ papers as "periodical noise which are inherent to the proposed system" [1]; they are why first-order modulators are rarely used alone, and why practical designs add dither or use higher-order loops, whose error is much closer to white.

### 3.3 Higher-order noise shaping

An $L$-th-order modulator places $L$ integrators in the loop to obtain $\text{NTF}(z) = (1 - z^{-1})^L$, with $\lvert\text{NTF}\rvert^2 = (2\sin(\omega/2))^{2L} \approx \omega^{2L}$ in band:

$$
P_q \approx \frac{\sigma_e^2}{\pi}\int_0^{\omega_B}\omega^{2L}\,d\omega
= \frac{\sigma_e^2}{\pi}\cdot\frac{\omega_B^{2L + 1}}{2L + 1}
= \frac{\Delta^2}{12}\cdot\frac{\pi^{2L}}{(2L + 1)\,\text{OSR}^{2L + 1}} .
$$

For a sine of amplitude $A_x$ (power $A_x^2/2$):

$$
\text{SQNR} = 10\log_{10}\frac{A_x^2/2}{\Delta^2/12} - 10\log_{10}\frac{\pi^{2L}}{2L + 1} + (20L + 10)\log_{10}\text{OSR} \text{ dB} .
$$

Each doubling of the OSR gains $(20L + 10)\log_{10}2 = (6.02L + 3.01)$ dB: **9.0**, **15.1**, **21.1** and **27.1** dB per octave for $L$ = 1 to 4. The first term is the quantizer's own SQNR; with a 1-bit quantizer and $A_x = 1$ it is 10 log₁₀(1.5) = 1.76 dB, and an $M$-level quantizer gains $20\log_{10}(M - 1)$ on it: about 6 dB per extra bit once there are several bits. The middle term is a penalty: the NTF's gain grows towards the band edge, and $\pi^{2L}/(2L + 1)$ is 5.2 dB for $L = 1$, 12.9 dB for $L = 2$.

![Output power spectra of first- and second-order one-bit modulators with a minus 6 dBFS sine, on a logarithmic frequency axis: the signal line near 0.003 of the sample rate, the noise floor rising at about 20 dB per decade for first order and 40 dB per decade for second order from very low levels up to about minus 30 dBFS near half the sample rate, with the OSR-64 band edge marked](../../../assets/figures/20-08/spectra.svg)

*Figure 2. The lab's 1-bit modulators at OSR = 64 and −6 dBFS. Shaping lowers the noise in band and raises it out of band; the second-order loop's noise rises twice as steeply (40 against 20 dB per decade), so far less of it lies below the band edge. The first-order spectrum's comb of lines is the tonal behavior of §3.2.*

**A second-order loop.** Two delaying integrators with feedback coefficients 1 and 2,

$$
u_1[n + 1] = u_1[n] + x[n] - y[n], \qquad u_2[n + 1] = u_2[n] + u_1[n] - 2y[n], \qquad y[n] = Q(u_2[n]),
$$

produce the required NTF. To see why, let the feedback coefficients be $a_1$ and $a_2$, so $U_1 = z^{-1}(X - a_1Y)/(1 - z^{-1})$ and $U_2 = z^{-1}(U_1 - a_2Y)/(1 - z^{-1})$. Substituting $U_2 = Y - E$ and multiplying by $(1 - z^{-1})^2$:

$$
Y\left[(1 - z^{-1})^2 + a_2z^{-1} + (a_1 - a_2)z^{-2}\right] = z^{-2}X + (1 - z^{-1})^2E .
$$

The bracket is $1 + (a_2 - 2)z^{-1} + (1 + a_1 - a_2)z^{-2}$, which equals 1 only for $a_2 = 2$ and $a_1 = 1$. So STF = $z^{-2}$ and NTF = $(1 - z^{-1})^2$. With a 1-bit quantizer the loop's scale is arbitrary, because $\text{sign}(ku) = \text{sign}(u)$ for $k > 0$; real designs scale the integrators to keep their outputs within the op-amps' swing.

**What the linear model gets wrong.** A 1-bit quantizer has no well-defined gain: its error is not bounded by Δ/2 and is correlated with its input. The linear model is still the right tool for design, but simulation is the arbiter. At OSR = 64 and −6 dBFS the model predicts 44.8 dB (first order) and 73.2 dB (second order); the lab measures 47.7 and 70.3 dB (Example 20-08.3). Near full scale the model is optimistic: Schreier's simulations at OSR = 128 give 55 dB (first order, full-scale input) and 86 dB (second order, 75% of full scale), where the model predicts **59.8** and **91.7** dB [5].

> **Two conventions.** Textbooks often write the peak SQNR as $6.02N + 1.76 - 10\log_{10}[\pi^{2L}/(2L + 1)] + (20L + 10)\log_{10}\text{OSR}$ for an $N$-bit quantizer [6]. That formula takes full scale as a sine of amplitude $2^N\Delta/2$, which for a 1-bit quantizer is Δ, twice the DAC's ±1 levels. This chapter references 0 dBFS to the DAC levels, as Schreier's toolbox does, so for 1-bit loops its SQNRs are 20 log₁₀ 2 = **6.02** dB lower for the same noise. Check which convention a quoted number uses before comparing it.

![SQNR against oversampling ratio from 16 to 256 for first- and second-order one-bit modulators at minus 6 dBFS: straight lines for the linear model rising 9 and 15 dB per octave, and simulated points lying within a few dB of the lines, first-order points slightly above and second-order points slightly below](../../../assets/figures/20-08/sqnr_osr.svg)

*Figure 3. The noise-shaping law against simulation. The slopes match (9 and 15 dB per octave); the offsets differ by a few decibels because a 1-bit quantizer's error is neither white nor of variance exactly Δ²/12. At OSR = 64 the simulated values are 47.7 and 70.3 dB.*

**Multi-bit quantizers.** An $M$-level quantizer reduces Δ from 2 to $2/(M - 1)$, gaining $20\log_{10}(M - 1)$ dB, and makes the loop far more stable (§3.4). The price is the feedback DAC: its errors enter at the input, unshaped, exactly like the input signal (the DAC output is subtracted from $x$), so the converter is only as linear as its DAC however good the loop is. Multi-bit designs therefore shuffle which DAC elements are used each sample (**dynamic element matching**, for example data-weighted averaging), which converts the mismatch into noise that is itself shaped out of band.

### 3.4 Stability and NTF design

**Why high-order loops overload.** $\lvert(1 - z^{-1})^L\rvert$ reaches $2^L$ at $f_s/2$: 2, 4, 8 and 16 for $L$ = 1 to 4. The quantizer error, of order ±1, is amplified by up to $2^L$ and fed back into the integrators. For $L \ge 3$ with a 1-bit quantizer, the quantizer input grows without bound: the loop is unstable, and once the integrators saturate the converter's output is garbage until it is reset. The lab shows a pure $(1 - z^{-1})^3$ loop diverging from a −6 dBFS input.

**Lee's rule.** The practical remedy is to give the NTF poles that flatten its out-of-band gain, $\text{NTF}(z) = (1 - z^{-1})^L/D(z)$, keeping the peak gain $\lVert\text{NTF}\rVert_\infty$ to about 1.5. W. L. Lee (1987) proposed limiting the peak gain to 2 for 1-bit loops; designers use about 1.5 as a margin. The criterion is neither necessary (the second-order loop is stable with a peak gain of 4) nor sufficient, but loops with $\lVert\text{NTF}\rVert_\infty \approx 1.5$ are usually stable for inputs up to some **maximum stable amplitude** below full scale [5]. Candy saw this in 1985: such loops "can latch into undesirable overloading modes" [2]. The cost is in-band noise: in band, $\lvert\text{NTF}\rvert \approx \omega^L/\lvert D(1)\rvert$, so the noise rises by $20\log_{10}(1/\lvert A(1)\rvert)$ dB. A Butterworth high-pass denominator scaled to a 1.5 peak gives penalties of 26.9 dB for $L = 3$ and 44.1 dB for $L = 4$ (Example 20-08.5). Higher order still wins once the OSR is large, because the slope grows by 6 dB per octave per order, but the gain from going to high order is far less than the naive formula suggests.

![Magnitude of noise transfer functions against frequency on a log axis: the pure differentiators of order 1, 2 and 4 rise at 20, 40 and 80 dB per decade to peaks of 2, 4 and 16 at half the sample rate; the third- and fourth-order Lee-rule NTFs rise steeply in band and flatten at 1.5 above about a tenth of the sample rate, sitting above the pure fourth-order curve in band](../../../assets/figures/20-08/ntf.svg)

*Figure 4. Pure differentiator NTFs reach a gain of $2^L$ at $f_s/2$; a 1-bit loop with $L \ge 3$ cannot tolerate that. Butterworth poles hold the peak to 1.5 (dashed line), at the price of in-band suppression: inside the OSR-64 band edge (vertical line) the Lee-rule curves sit 26.9 and 44.1 dB above the pure third- and fourth-order differentiators (the pure third-order curve is not drawn).*

**Optimized zeros.** Placing all $L$ zeros at DC wastes them: the noise is largest near the band edge. Spreading the zeros across the band minimizes the integral of $\lvert\text{NTF}\rvert^2$. For $L = 2$ with zeros at $\pm\omega_z$, the in-band integrand is $(\omega^2 - \omega_z^2)^2$; with $t = \omega/\omega_B$ and $a = \omega_z/\omega_B$,

$$
\int_0^1(t^2 - a^2)^2\,dt = \frac15 - \frac{2a^2}{3} + a^4 ,
$$

which is smallest at $a^2 = 1/3$, where it equals $1/5 - 1/9 = 4/45$, against $1/5$ with both zeros at DC. The noise falls by a factor $9/4$: **3.5** dB, with the zeros at $f_B/\sqrt3$. For $L = 3$, zeros at 0 and $\pm\sqrt{3/5}\,f_B$ give $4/175$ against $1/7$: **8.0** dB. In a circuit, an off-DC zero pair is a small local feedback around two integrators (a resonator).

### 3.5 Circuit realization and integrator leakage

A discrete-time modulator uses switched-capacitor integrators (20-05's sampling switches and capacitors around an op-amp). With an ideal op-amp, a sampling capacitor $C_s$ and an integrating capacitor $C_i$ give $v_o[n] = v_o[n - 1] + (C_s/C_i)x[n - 1]$. With finite op-amp gain $A$, the summing node sits at $-v_o/A$, and charge conservation on that node gives

$$
v_o[n] = \frac{(1 + 1/A)\,v_o[n - 1] + (C_s/C_i)\,x[n - 1]}{1 + (1 + C_s/C_i)/A} ,
\qquad p = \frac{1 + 1/A}{1 + (1 + C_s/C_i)/A} \approx 1 - \frac{C_s/C_i}{A} .
$$

The integrator's pole moves inside the unit circle: it **leaks**, with $\varepsilon = 1 - p \approx (C_s/C_i)/A$. For a first-order loop, the NTF becomes approximately $1 - pz^{-1}$, whose value at DC is ε instead of 0. In band, $\lvert\text{NTF}\rvert^2 \approx \varepsilon^2 + \omega^2$, so

$$
P_q \approx \sigma_e^2\left(\frac{\varepsilon^2}{\text{OSR}} + \frac{\pi^2}{3\,\text{OSR}^3}\right) ,
$$

and the leakage matters only if $\varepsilon > \pi/(\sqrt3\,\text{OSR})$, that is $A < \sqrt3\,\text{OSR}/\pi$ (for $C_s = C_i$): about 35 at OSR = 64 (Example 20-08.6). Single-loop modulators tolerate low-gain op-amps; that is one reason they are so robust. Thermal noise is the other half of the design: the sampling capacitor's kT/C noise (20-05) is white, so only $1/\text{OSR}$ of it falls in band, and the capacitor can be OSR times smaller than in a Nyquist converter of the same SNR (Example 20-08.4).

### 3.6 Cascaded (MASH) modulators

A **MASH** (multi-stage noise shaping) modulator obtains high-order shaping from a cascade of stable low-order loops; Matsuya and colleagues at NTT named it and used a triple cascade for a 16-bit audio converter in 1987 [3]. In the 1-1 MASH, the first stage is a first-order modulator, $Y_1 = z^{-1}X + (1 - z^{-1})E_1$. Its quantization error, available as $-E_1 = u_1 - y_1$, is the input of a second first-order stage: $Y_2 = -z^{-1}E_1 + (1 - z^{-1})E_2$. Digital filters recombine the outputs:

$$
Y = z^{-1}Y_1 + (1 - z^{-1})Y_2
= z^{-2}X + z^{-1}(1 - z^{-1})E_1 - z^{-1}(1 - z^{-1})E_1 + (1 - z^{-1})^2E_2
= z^{-2}X + (1 - z^{-1})^2E_2 .
$$

The first stage's error cancels, and the second's is shaped to second order. Every stage is first order and unconditionally stable, so a MASH can reach high order without Lee's rule. A 2-1 cascade gives third order the same way (Problem 20-08.8). The output is multi-level ($y_1 \pm$ a difference of $y_2$ values), but it is a digital word, so no multi-bit DAC is needed in the loop.

**The catch: cancellation depends on matching.** The digital filter assumes the first stage's NTF is exactly $1 - z^{-1}$. If its integrator leaks, $\text{NTF}_1 \approx 1 - pz^{-1}$, and the $E_1$ terms leave a residue $z^{-1}[\text{NTF}_1 - (1 - z^{-1})]E_1 \approx \varepsilon z^{-2}E_1$: first-stage noise that is not shaped at all. Its in-band power $\varepsilon^2\sigma_e^2/\text{OSR}$ must stay below the ideal second-order noise $\sigma_e^2\pi^4/(5\,\text{OSR}^5)$, which requires $\varepsilon < \pi^2/(\sqrt5\,\text{OSR}^2)$. At OSR = 64 that is an op-amp gain above about 928 (59.4 dB), against about 35 for a single loop (Example 20-08.6). MASH trades loop stability for analog precision, and practical designs calibrate the digital filters or use single loops with multi-bit quantizers instead.

### 3.7 Continuous-time modulators

A **continuous-time** (CT) modulator replaces the switched-capacitor integrators with active-RC or $g_m$-C integrators and samples only at the quantizer. Its input never meets a sampling switch, which brings three advantages and three new problems.

**Equivalence.** In a first-order CT loop with integrator $1/(sT)$ ($T = 1/f_s$) and a DAC that holds $y[n]$ for one full period (non-return-to-zero, NRZ), the integrator's change over a period is $\int(x - y)\,dt/T = \bar x[n] - y[n]$, where $\bar x[n]$ is the input averaged over the period. The sampled integrator obeys exactly the discrete-time equation of §3.2. In general a CT loop filter is designed so that its sampled impulse response, with the DAC pulse, matches a discrete-time prototype (the impulse-invariant transformation).

**Implicit anti-aliasing.** The input is integrated before it is sampled. For the first-order loop the input sees an integrate-and-dump filter, $\lvert H(f)\rvert = \lvert\sin(\pi f/f_s)/(\pi f/f_s)\rvert$, with nulls at every multiple of $f_s$. An interferer at $f_s - f_B$, which would alias onto the band edge, is attenuated by $\sin(\pi/2\text{OSR})/[\pi(1 - 1/2\text{OSR})] \approx 1/(2\,\text{OSR})$: **−42.1** dB at OSR = 64 (Example 20-08.7). Higher-order CT loops attenuate more. A discrete-time modulator samples its input directly and needs an explicit anti-aliasing filter. The other two advantages: a resistive input is easy to drive, with little kickback, and with no settling requirement per clock phase, CT loops reach higher sample rates at lower power, which is why wide-bandwidth ΔΣ converters are mostly CT [10].

**Excess loop delay.** The quantizer and DAC take time to respond. If the DAC switches a fraction $d$ of a period late, the integrator sees $y[n - 1]$ for $dT$ and $y[n]$ for $(1 - d)T$:

$$
u[n + 1] = u[n] + x[n] - (1 - d)\,y[n] - d\,y[n - 1] .
$$

Repeating §3.2's algebra, $Y\left(1 - dz^{-1} + dz^{-2}\right) = z^{-1}X + (1 - z^{-1})E$. The NTF gains poles at the roots of $z^2 - dz + d = 0$, of radius $\sqrt d$ (for $0 < d < 4$ they are complex). A first-order loop stays stable for $d < 1$ and still averages correctly; at $d = 0.5$ the poles have radius **0.707**. Higher-order loops are much more sensitive: their NTF is designed for a specific delay, and an uncompensated delay of a fraction of a period can make them unstable. Designs therefore budget a fixed fraction of a period for the delay and add a direct feedback path around the quantizer to restore the intended NTF [8].

**Clock jitter.** A discrete-time modulator's DAC delivers a fixed charge per clock period, whatever the edge timing. Its input sampler is still jitter-sensitive, but gently: a sampling-time error δ gives an error $(dv/dt)\,\delta$, which is white for white jitter, so only $1/\text{OSR}$ of it falls in band and $\text{SNR}_{jit,DT} = -20\log_{10}(2\pi f_{in}\sigma_t) + 10\log_{10}\text{OSR}$. An NRZ CT DAC delivers charge for as long as it is on, so an edge that arrives δ early or late changes the charge by $(y[n] - y[n - 1])\delta$, an input-referred error $\varepsilon[n] = (y[n] - y[n - 1])\,\delta_n/T$. (This is the standard NRZ jitter model [9]: jitter matters only at edges where the data changes.) If the edge errors are white with rms $\sigma_t$, this error is white with variance $E[(\Delta y)^2]\,(\sigma_tf_s)^2$, and its in-band part is

$$
P_{jitter} = \frac{E\!\left[(y[n] - y[n - 1])^2\right]\,(\sigma_tf_s)^2}{\text{OSR}} .
$$

The shaped quantization noise makes the output jump around at high frequency, and those large, frequent jumps are what the jitter samples. For a 1-bit second-order stream $E[(\Delta y)^2]$ is 2.36; for a 16-level quantizer it is 0.0298, almost two orders of magnitude less (Example 20-08.7). Multi-bit quantizers, return-to-zero or switched-capacitor-resistor DACs and low-jitter clocks are the standard defenses.

### 3.8 Decimation

The modulator's output carries the signal plus shaped noise rising to $f_s/2$. The **decimation filter** (16-09) removes the noise above $f_B$ and reduces the rate to about $2f_B$. It is almost always a cascade: a CIC (sinc$^K$) filter decimates by a large factor cheaply, without multipliers, and one or more half-band FIR stages finish with a sharp transition band. A CIC of order $K$ decimating by $R$ has zeros of order $K$ at every multiple of $f_s/R$, exactly where the noise that would fold into the band after decimation sits. There the shaped noise is large, and it keeps rising with frequency (as $f^{2L}$ in power), while the CIC's sidelobes fall only as $f^{-2K}$. The noise folded back from all the sidelobes stays below the in-band noise only if the filter's order exceeds the modulator's: **$K \ge L + 1$**, the standard sinc$^{L+1}$ rule [6]. Hogenauer's cascaded integrator-comb structure makes such filters multiplier-free [11]. 16-09's Example 16-09.5 works through a sinc⁴ filter of a commercial ΔΣ ADC, including its droop, alias protection and latency.

### 3.9 The modern landscape

Three ideas extend the classic loop. **Noise-shaping SARs** add a loop filter around a SAR's residue (20-07), shaping its quantization and comparator noise with a few extra capacitors; they now hold the best figures of merit at low bandwidth (§9). **Incremental** ΔΣ converters reset the loop for every conversion, so they can be multiplexed across sensor channels and have no idle tones. **Digital** ΔΣ modulators shape a word's truncation error, in ΔΣ DACs (20-09) and fractional-N synthesizers, where they dither the divide ratio so that its average is fractional and its error is pushed to high offsets where the loop filters it (20-10) [12].

## 4. Worked examples

### Example 20-08.1 · Oversampling alone (tier A)

**Setup.** A 12-bit quantizer digitizes a full-scale sine. Find the SQNR at the Nyquist rate, the oversampling ratio that would give the in-band SQNR of a 16-bit converter by oversampling alone, the resulting SQNR, and the sample rate this implies for a 20 kHz audio band.

**Solution.**

- Nyquist SQNR: $20\log_{10}(2^{12}) + 1.76$ = **74.0** dB.
- Four more bits need $4 \times 6.02 = 24.08$ dB $= 10\log_{10}\text{OSR}$, so OSR = $10^{2.408} = 4^4$ = **256**.
- SQNR: $74.01 + 10\log_{10}256$ = **98.1** dB.
- Sample rate: $f_s = 2f_B\,\text{OSR} = 2 \times 20\text{ kHz} \times 256$ = **10.24** MHz.

**Units check.** OSR is a ratio of rates; $f_s$ in hertz.

**Sanity check.** 24 dB at 3 dB per octave is eight octaves, and 2⁸ = 256. A first-order loop gains 9 dB per octave, three times as much: shaping, not oversampling, is what makes the trade worthwhile.

### Example 20-08.2 · A first-order modulator by hand (tier A)

**Setup.** A first-order modulator ($u[n + 1] = u[n] + x - y[n]$, $y = \text{sign}(u)$) starts with $u[0]$ = 0.1 and has a DC input $x$ = 0.2. Trace $u$ for five samples, find the output average and period, and then find the idle tone for $x$ = 0.002 with $f_s$ = 5.12 MHz and OSR = 128.

**Solution.** Each step adds $x - y = -0.8$ when $u \ge 0$ and $+1.2$ when $u < 0$:

| $n$ | $u[n]$ | $y[n]$ |
|---|---|---|
| 0 | 0.1 | +1 |
| 1 | **−0.7** | −1 |
| 2 | **0.5** | +1 |
| 3 | **−0.3** | −1 |
| 4 | **0.9** | +1 |
| 5 | **0.1** | +1 |

$u[5] = u[0]$, so the pattern repeats with period **5**; three +1s and two −1s average to **0.2**, the input. (Starting from $u[0] = 0.1$ keeps every sample away from the ambiguous $u = 0$: the values are $0.1 + 0.2n$ modulo 1, never zero.) The output is periodic at $f_s/5$, a tone far out of band.

For $x$ = 0.002, the lab's simulation shows tones at multiples of $xf_s$ = **10.24** kHz, each of amplitude $2x$ = 0.004, or **−48.0** dBFS. The band edge is $f_s/(2\,\text{OSR})$ = 20 kHz, so this tone is audible. Tones enter the band whenever $\lvert x\rvert < 1/(2\,\text{OSR})$ = **0.0039**.

**Units check.** $x$ is in full-scale units, so $xf_s$ is in hertz.

**Sanity check.** The ngspice netlist in the lab implements this loop with a continuous-time integrator and a latch; its integrator voltages at the clock edges match the table to within 3 µV.

### Example 20-08.3 · The noise-shaping law against simulation (tier B)

**Setup.** For a 1-bit quantizer (Δ = 2), compute the linear-model SQNR of first- and second-order modulators at OSR = 64 for a full-scale sine and the gain per octave. Then compare with simulations at −6 dBFS (amplitude 0.5) on 65,536 samples.

**Solution.** The quantizer term is $10\log_{10}[(1/2)/(4/12)]$ = 1.76 dB.

- $L = 1$: $1.76 - 10\log_{10}(\pi^2/3) + 30\log_{10}64$ = 1.76 − 5.17 + 54.19 = **50.8** dB; **9.0** dB per octave.
- $L = 2$: $1.76 - 10\log_{10}(\pi^4/5) + 50\log_{10}64$ = 1.76 − 12.90 + 90.31 = **79.2** dB; **15.1** dB per octave.
- At −6 dBFS the model gives **44.8** and **73.2** dB. The lab's simulations (a sine at about a third of the band edge, Hann window) give **47.7** dB and **70.3** dB.
- The second-order simulation at OSR = 32 and 128 gives **54.3** and **84.2** dB: **14.9** dB per octave on average, matching the model's slope.
- With a 16-level quantizer the model gains $20\log_{10}15$ = **23.5** dB; the simulation gives **97.0** dB.

**Units check.** All are power ratios in dB; OSR is dimensionless.

**Sanity check.** The first-order simulation beats the model and the second-order one falls short of it, by similar amounts: the 1-bit quantizer's error is neither white nor of variance exactly 1/3. Within a few dB, the model is a design tool; the simulation decides.

### Example 20-08.4 · Sizing an audio modulator (tier B)

**Setup.** An audio ADC needs a peak SQNR of 100 dB in a 20 kHz band with the input at −6 dBFS. Using the linear model, find the minimum OSR and a power-of-two choice for a second-order loop with a 1-bit quantizer and with a 16-level quantizer. Then size the sampling capacitor so that its kT/C noise (single-ended, one sampling event per period) is 100 dB below the signal, for a 1 V full-scale amplitude at OSR = 128, and compare with a Nyquist-rate converter.

**Solution.**

- Required: $(20L + 10)\log_{10}\text{OSR} \ge 100 - 10\log_{10}[(0.25/2)/(\Delta^2/12)] + 10\log_{10}(\pi^4/5)$.
- 1-bit (Δ²/12 = 1/3): $50\log_{10}\text{OSR} \ge 100 + 4.26 + 12.90$, so OSR ≥ **220.4**; choose 256, $f_s$ = **10.24** MHz.
- 16 levels (Δ = 2/15): the quantizer term improves by 23.52 dB, so OSR ≥ **74.6**; choose 128, $f_s$ = 5.12 MHz.
- Capacitor: the signal power is $(0.5\text{ V})^2/2$ = 0.125 V², so the in-band noise must be below $1.25 \times 10^{-11}$ V². In-band kT/C noise is $kT/(C\,\text{OSR})$, so $C \ge kT/(1.25 \times 10^{-11} \times 128)$ = **2.59** pF. At the Nyquist rate (OSR = 1) the same noise needs **331** pF.

**Units check.** kT in joules (V²·F); divided by V² gives farads.

**Sanity check.** The capacitor ratio is exactly the OSR, 128: oversampling shrinks thermal noise and quantization noise alike, which is why ΔΣ converters reach high SNR with small capacitors.

### Example 20-08.5 · NTF zeros and Lee's rule (tier B)

**Setup.** Find the noise reduction from optimally placed NTF zeros for $L = 2$ and $L = 3$ and where the $L = 2$ zeros sit for a 20 kHz band. Find the peak NTF gain of $(1 - z^{-1})^L$ for $L = 2$ and 4, and the in-band penalty of a Butterworth-pole NTF with a 1.5 peak gain for $L = 3$ and 4.

**Solution.**

- $L = 2$: $\int_0^1t^4dt = 1/5$ against the minimum $4/45$ at $a^2 = 1/3$: $10\log_{10}(9/4)$ = **3.5** dB, with the zeros at $f_B/\sqrt3$ = **11.5** kHz.
- $L = 3$: $\int_0^1t^2(t^2 - a^2)^2dt = 1/7 - 2a^2/5 + a^4/3$, smallest at $a^2 = 3/5$, where it equals $1/7 - 3/25 = 4/175$: $10\log_{10}(25/4)$ = **8.0** dB.
- Peak gain at $f_s/2$ ($z = -1$): $2^2$ = **4** and $2^4$ = **16**, far above Lee's 1.5.
- Butterworth poles chosen so that $\max\lvert\text{NTF}\rvert$ = 1.5: $\lvert D(1)\rvert$ = **0.0453** and **0.00627**, in-band penalties of **26.9** and **44.1** dB.

**Units check.** Zero frequencies in hertz; gains dimensionless.

**Sanity check.** The lab confirms that the pure third- and fourth-order 1-bit loops diverge, while the Lee-rule loops stay bounded and reach about 80 and 90 dB at OSR = 64 and −6 dBFS (averaged over input phases), against 70.3 dB for the second-order loop: higher order still pays, but by far less than the 21 and 27 dB per octave slopes alone would suggest.

### Example 20-08.6 · Op-amp gain for a single loop and for a MASH (tier B)

**Setup.** With $C_s = C_i$ (so ε ≈ 1/A) and OSR = 64, find the op-amp gain at which integrator leakage starts to dominate in a first-order single loop and in a 1-1 MASH. Then compute the linear-model SQNR of the MASH at −6 dBFS for A = 100 and A = 1000.

**Solution.**

- Single loop: leakage matters when $\varepsilon > \pi/(\sqrt3\,\text{OSR})$, so $A < \sqrt3\,\text{OSR}/\pi$ = **35.3**.
- MASH: leakage matters when $\varepsilon > \pi^2/(\sqrt5\,\text{OSR}^2)$, so $A < \sqrt5\,\text{OSR}^2/\pi^2$ = **928**, or **59.4** dB.
- MASH SQNR: ideal noise $\sigma_e^2\pi^4/(5\,\text{OSR}^5)$ = 6.05 × 10⁻⁹ with $\sigma_e^2 = 1/3$; leakage noise $\sigma_e^2/(A^2\,\text{OSR})$ = 5.21 × 10⁻⁷ at A = 100 and 5.21 × 10⁻⁹ at A = 1000. Against the signal power 0.125: **53.8** dB and **70.5** dB, against **73.2** dB ideal.

**Units check.** All noise powers in full-scale units squared; gains dimensionless.

**Sanity check.** The lab's MASH simulation gives 73.2, 72.8 and 59.7 dB for infinite, 1000 and 100 gain. The direction and size of the effect match; the model is pessimistic because a first-order stage's error is not white, and less of it lies in band than the white-noise assumption puts there.

### Example 20-08.7 · A continuous-time loop: aliasing, delay and jitter (tier C)

**Setup.** (a) For a first-order CT modulator at OSR = 64, find the attenuation of an interferer at $f_s - f_B$. (b) Trace the first-order loop of Example 20-08.2 ($x = 0.2$, $u[0] = 0.1$, DAC initially at +1) with an excess loop delay of half a period, and find the NTF pole radius. (c) A CT modulator for a 20 MHz band runs at OSR = 32 ($f_s$ = 1.28 GHz) with 1 ps rms clock jitter and a −6 dBFS input. Using the lab's bitstream statistics, find the jitter-limited SNR for a 1-bit and a 16-level second-order modulator, and compare with a Nyquist-rate sampler at 20 MHz.

**Solution.**

(a) $\sin(\pi/128)/[\pi(1 - 1/128)]$ = 0.00787: **−42.1** dB.

(b) $u[n + 1] = u[n] + 0.2 - 0.5\,y[n] - 0.5\,y[n - 1]$ with $y[-1] = +1$:

| $n$ | $u[n]$ | $y[n]$ | $y[n - 1]$ |
|---|---|---|---|
| 0 | 0.1 | +1 | +1 |
| 1 | **−0.7** | −1 | +1 |
| 2 | **−0.5** | −1 | −1 |
| 3 | **0.7** | +1 | −1 |
| 4 | **0.9** | +1 | +1 |
| 5 | **0.1** | +1 | +1 |

The state returns after five samples, with three +1s: the average is still 0.2, but the pattern has changed. The poles have radius $\sqrt{0.5}$ = **0.707**.

(c) The lab finds $E[(\Delta y)^2]$ = **2.36** (1-bit) and **0.0298** (16 levels). With $\sigma_tf_s = 1.28 \times 10^{-3}$, the 1-bit jitter noise is $2.36 \times (1.28 \times 10^{-3})^2/32 = 1.21 \times 10^{-7}$ against a signal power of 0.125: **60.1** dB. With 16 levels: **79.1** dB. A Nyquist sampler at 20 MHz is limited to $-20\log_{10}(2\pi \times 20\text{ MHz} \times 1\text{ ps})$ = **78.0** dB, and a discrete-time ΔΣ at the same OSR gains $10\log_{10}32$ on that: **93.1** dB.

**Units check.** $\sigma_tf_s$ is dimensionless (seconds times per second).

**Sanity check.** At this −6 dBFS input the 1-bit NRZ loop is **17.9** dB more jitter-sensitive than a Nyquist sampler at the band edge (whose jitter SNR does not depend on the input level; at full scale, with similar bitstream statistics, the gap would be about 12 dB), because it is the DAC's large, frequent steps, not the slow input, that the jitter corrupts. A discrete-time loop is the most tolerant of the three. The ngspice netlist reproduces the delayed-loop trace.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-08.1a | Nyquist SQNR, 12 bits | 74.0 | dB |
| Ex 20-08.1b | OSR for four more bits | 256 | — |
| Ex 20-08.1c | SQNR with that OSR | 98.1 | dB |
| Ex 20-08.1d | sample rate, 20 kHz band | 10.24 | MHz |
| Ex 20-08.2a | u[1] | −0.7 | — |
| Ex 20-08.2b | u[2] | 0.5 | — |
| Ex 20-08.2c | u[3] | −0.3 | — |
| Ex 20-08.2d | u[4] | 0.9 | — |
| Ex 20-08.2e | u[5] | 0.1 | — |
| Ex 20-08.2f | output average | 0.2 | — |
| Ex 20-08.2g | period | 5 | samples |
| Ex 20-08.2h | idle tone, x = 0.002 | 10.24 | kHz |
| Ex 20-08.2i | idle tone amplitude | −48.0 | dBFS |
| Ex 20-08.2j | largest input with in-band tones | 0.0039 | — |
| Ex 20-08.3a | SQNR, L = 1, model | 50.8 | dB |
| Ex 20-08.3b | SQNR, L = 2, model | 79.2 | dB |
| Ex 20-08.3c | slope, L = 1 | 9.0 | dB/octave |
| Ex 20-08.3d | slope, L = 2 | 15.1 | dB/octave |
| Ex 20-08.3e | L = 1, model, −6 dBFS | 44.8 | dB |
| Ex 20-08.3f | L = 2, model, −6 dBFS | 73.2 | dB |
| Ex 20-08.3g | L = 1, simulated | 47.7 | dB |
| Ex 20-08.3h | L = 2, simulated | 70.3 | dB |
| Ex 20-08.3i | L = 2, simulated, OSR 32 | 54.3 | dB |
| Ex 20-08.3j | L = 2, simulated, OSR 128 | 84.2 | dB |
| Ex 20-08.3k | 16 levels, simulated | 97.0 | dB |
| Ex 20-08.3l | 16-level quantizer gain | 23.5 | dB |
| Ex 20-08.3m | simulated slope, L = 2 | 14.9 | dB/octave |
| Ex 20-08.4a | minimum OSR, 1-bit | 220.4 | — |
| Ex 20-08.4b | sample rate, OSR 256 | 10.24 | MHz |
| Ex 20-08.4c | minimum OSR, 16 levels | 74.6 | — |
| Ex 20-08.4e | sampling capacitor, OSR 128 | 2.59 | pF |
| Ex 20-08.4f | sampling capacitor, Nyquist | 331 | pF |
| Ex 20-08.5a | optimized zeros, L = 2 | 3.5 | dB |
| Ex 20-08.5b | optimized zeros, L = 3 | 8.0 | dB |
| Ex 20-08.5c | zero frequency, 20 kHz band | 11.5 | kHz |
| Ex 20-08.5d | peak NTF gain, L = 2 | 4 | — |
| Ex 20-08.5e | peak NTF gain, L = 4 | 16 | — |
| Ex 20-08.5f | Lee-rule penalty, L = 3 | 26.9 | dB |
| Ex 20-08.5g | Lee-rule penalty, L = 4 | 44.1 | dB |
| Ex 20-08.5h | magnitude of D(1), L = 3 | 0.0453 | — |
| Ex 20-08.5i | magnitude of D(1), L = 4 | 0.00627 | — |
| Ex 20-08.6a | single-loop gain threshold | 35.3 | — |
| Ex 20-08.6b | MASH gain threshold | 928 | — |
| Ex 20-08.6c | MASH gain threshold in dB | 59.4 | dB |
| Ex 20-08.6d | MASH SQNR, A = 100 | 53.8 | dB |
| Ex 20-08.6e | MASH SQNR, A = 1000 | 70.5 | dB |
| Ex 20-08.6f | MASH SQNR, ideal | 73.2 | dB |
| Ex 20-08.7a | alias attenuation, OSR 64 | −42.1 | dB |
| Ex 20-08.7b | u[1] with delay | −0.7 | — |
| Ex 20-08.7c | u[2] with delay | −0.5 | — |
| Ex 20-08.7d | u[3] with delay | 0.7 | — |
| Ex 20-08.7e | u[4] with delay | 0.9 | — |
| Ex 20-08.7f | u[5] with delay | 0.1 | — |
| Ex 20-08.7g | pole radius, d = 0.5 | 0.707 | — |
| Ex 20-08.7h | E[Δy²], 1-bit | 2.36 | — |
| Ex 20-08.7i | E[Δy²], 16 levels | 0.0298 | — |
| Ex 20-08.7j | jitter SNR, 1-bit | 60.1 | dB |
| Ex 20-08.7k | jitter SNR, 16 levels | 79.1 | dB |
| Ex 20-08.7l | Nyquist sampler jitter SNR | 78.0 | dB |
| Ex 20-08.7m | 1-bit penalty against the sampler | 17.9 | dB |
| Ex 20-08.7n | discrete-time loop jitter SNR | 93.1 | dB |
| Txt 20-08.a | slope, L = 3 | 21.1 | dB/octave |
| Txt 20-08.b | slope, L = 4 | 27.1 | dB/octave |
| Txt 20-08.c | π^(2L)/(2L+1), L = 1 | 5.2 | dB |
| Txt 20-08.d | π^(2L)/(2L+1), L = 2 | 12.9 | dB |
| Txt 20-08.e | 4^12 | 1.7×10⁷ | — |
| Txt 20-08.f | small-angle error at OSR 16 | 0.2 | % |
| Txt 20-08.g | effective bits from 111.5 dB | 18.2 | bits |
| Txt 20-08.h | PDM microphone OSR, 2.4 MHz, 20 kHz | 60 | — |
| Txt 20-08.i | ADS1298 noise step per halving | 15.5 | dB |
| Txt 20-08.j | ADS1292 decimation ratio at 500 SPS | 256 | — |
| Txt 20-08.k | model, L = 1, OSR 128, 0 dBFS | 59.8 | dB |
| Txt 20-08.l | model, L = 2, OSR 128, −2.5 dBFS | 91.7 | dB |
| Txt 20-08.m | convention offset | 6.02 | dB |
| Txt 20-08.n | ADS127L21 jitter limit with oversampling | 113.1 | dB |

## 5. Simulate it

The lab ([labs/20-08-lab](../labs/20-08-lab/README.md)) implements the modulators in `dsm.py` and confirms the first-order loop and its delayed variant in ngspice (`ct_dsm.cir`).

**Predict, then run.**

1. Predict the integrator values of Example 20-08.2, with and without half a period of loop delay, then run `ngspice -b ct_dsm.cir` (Part 1).
2. Predict where a first-order loop's idle tones sit for small DC inputs, then simulate and look at the spectrum (Part 1).
3. Predict the SQNR of first- and second-order loops at OSR = 32, 64 and 128, then simulate; plot the output spectra and see the 20 and 40 dB-per-decade slopes (Part 2).
4. Predict which third- and fourth-order loops are stable, then run pure-differentiator and Lee-rule NTFs (Part 3).
5. Predict the MASH's sensitivity to op-amp gain and the CT loop's jitter noise for 1-bit and 16-level quantizers, then simulate (Part 4).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Oversampling ratio | $(6L + 3)$ dB per octave of SQNR; smaller capacitors | Modulator clock rate and power, decimation filter length; bandwidth for a given clock | Converter architect |
| Loop order | Slope of the noise shaping | Stability (Lee's rule penalty), maximum stable amplitude, more integrators | Converter architect |
| Multi-bit quantizer | $20\log_{10}(M - 1)$ (about 6 dB per bit with several bits), stability, jitter tolerance in CT loops | A linear multi-bit DAC (dynamic element matching), more comparators | Analog designer |
| Optimized NTF zeros | 3.5 dB ($L$ = 2), 8 dB ($L$ = 3) for free | Local resonator feedback, coefficient accuracy | Analog designer |
| MASH instead of single loop | High order with stable stages | Op-amp gain and matching for noise cancellation | Converter architect |
| Continuous-time loop | Implicit anti-aliasing, easy-to-drive input, speed and power at wide bandwidth | Excess loop delay, clock-jitter sensitivity, RC time-constant variation | Converter architect |
| Decimation filter (CIC order, FIR stages) | Out-of-band rejection, passband flatness | Latency, digital area and power | Digital designer and product definition |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| SQNR gain per doubling of the OSR | 3 dB without shaping; 9.0, 15.1, 21.1, 27.1 dB for $L$ = 1 to 4 | exact; Schreier's "(6N+3) dB/octave" [5] |
| NTF penalty $10\log_{10}[\pi^{2L}/(2L + 1)]$ | 5.2 dB ($L$ = 1), 12.9 dB ($L$ = 2) | Johns and Martin's constants [6] |
| Convention offset for 1-bit SQNR formulas | 6.02 dB | full scale referenced to Δ or to the ±1 DAC levels (§3.3) |
| Linear model against simulation, 1-bit, near full scale | model optimistic by roughly 5 dB | Schreier's simulations at OSR 128 [5] |
| Lee's rule | peak NTF gain ≤ 2 (Lee, 1987); about 1.5 in practice | neither necessary nor sufficient [5] |
| Op-amp gain | about OSR for a single loop (35 at OSR 64); about OSR² for a MASH (928) | §3.5, §3.6 |
| CIC order | $K \ge L + 1$ | [6] |
| Best Schreier figure, oversampled (as of Nov 2026) | 189.2 dB (noise-shaping SAR, 1 kHz band); 185.3 dB (discrete-time ΔΣ, 20 kHz band) | Murmann survey [13], [14] [R-343] |
| Widest continuous-time ΔΣ bandwidth in the survey (as of Nov 2026) | 360 MHz at 5 GS/s, 158 mW (2022) | [13], [14] [R-343] |
| Precision ΔΣ ADC (as of Nov 2026) | third-order switched-capacitor modulator at 12.8 MHz; DR 111.5 dB at 200 kSPS (about **18.2** effective bits); THD −125 dB; 4.3–33 mW by speed mode | TI ADS127L21 [15] [R-344] |
| PDM MEMS microphone (as of Nov 2026) | 2.4–3.1 MHz clock (OSR **60** for 20 kHz at 2.4 MHz), 68–69 dB(A) SNR, 0.3–1 mA | Infineon IM69D130; TDK T5838, "a fifth order Σ-Δ modulator" [16] [R-344] |
| ECG and biopotential front end (as of Nov 2026) | second-order modulator; 0.75 mW per channel (ADS1298), 335 µW per channel (ADS1292, decimation ratio **256** at 500 SPS) | TI data sheets [15] [R-344] |

## 8. Common mistakes

- **Applying the linear model's SQNR at full scale with a 1-bit quantizer.** Real loops overload below full scale; quote the maximum stable amplitude and simulate.
- **Assuming a first-order loop's error is white.** For DC and slow inputs it produces idle tones, in band whenever $\lvert x\rvert < 1/(2\,\text{OSR})$.
- **Scaling the NTF slope without counting the stability penalty.** A Lee-rule NTF of order 3 or 4 loses tens of decibels against the pure differentiator.
- **Forgetting that the feedback DAC is not shaped.** A multi-bit modulator is only as linear as its DAC unless the DAC's mismatch is shaped by element matching.
- **Specifying MASH op-amps like single-loop ones.** The cascade needs gains near OSR², the single loop near OSR.
- **Ignoring jitter in continuous-time designs.** A 1-bit NRZ DAC can be far more jitter-sensitive than a Nyquist sampler at the same band edge (Example 20-08.7).
- **Using a CIC of order equal to the loop order.** The decimator needs $K \ge L + 1$, or aliased shaped noise sets the floor.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Noise-shaping SARs hold the efficiency record [Established].** The best Schreier figure of any converter in Murmann's survey (August 2026 revision) is 189.2 dB: a fully dynamic noise-shaping SAR with 120.6 dB SNDR in a 1 kHz band at 139 µW (Zhao et al., UESTC, ISSCC 2025). The best classic loop is a discrete-time single-loop audio modulator at 185.3 dB, 105.4 dB SNDR in 20 kHz at 203.5 µW (Lee and Moon, ISSCC 2022) [13], [14] [R-343].
- **Wide bandwidth is continuous-time [Established].** The widest CT ΔΣ in the survey covers 360 MHz at 5 GS/s with 158 mW (ISSCC 2022), and oversampled CT *pipelined* converters extend to 1 GHz of bandwidth at OSR of about 3–5 [14] [R-343].
- **Commercial precision converters are mostly discrete-time [Established].** TI's ADS127L21 states that "The modulator is a switched-capacitor, third-order architecture," and its clock specification follows the sampling law plus the oversampling gain of §3.7: "with a 200kHz signal frequency, an external clock with <10ps (rms) jitter is required," and $-20\log_{10}(2\pi \times 200\ \text{kHz} \times 10\ \text{ps}) + 10\log_{10}(12.8\ \text{MHz}/400\ \text{kSPS})$ = **113.1** dB, at or above the part's 111.5 dB dynamic range [15] [R-344].
- **Audio, microphones and biopotential [Established].** TI's 2024 continuous-time audio ADC reaches 118.5 dBA dynamic range at 3.3 mW (ISSCC 2024) [14]. TI's ADS1298 ECG front end "uses a second-order modulator optimized for low-power applications"; its noise table falls by **15.5** dB per halving of data rate between 32 and 16 kSPS, where quantization noise dominates, close to second-order shaping's 15 dB per octave (our computation) [15] [R-344].

### Why it matters commercially

Oversampling converters are where most of a consumer device's analog signals enter the digital world. Earbuds, watches and XR headsets carry ΔΣ microphones and codecs, wearables digitize biopotentials with low-power ΔΣ front ends, and IoT and industrial sensors use precision ΔΣ ADCs. In automotive and wireless receivers, continuous-time ΔΣ modulators digitize tens to hundreds of megahertz directly. In AI datacenters the honest answer is narrower: we found no ΔΣ ADC in the data path; ΔΣ appears in clock synthesis (fractional-N PLLs) and in power and condition monitoring. For a corporate-development lens, the value in this category sits in low power per channel, in the digital filters and calibration that ship with the modulator, and in specifications (dynamic range, latency, maximum stable amplitude) that are easy to quote flatteringly.

### Questions for engineering leaders

1. **"Is your headline figure SNR or dynamic range, A-weighted or not, and at what input level?"** Strong: unweighted SNR and SNDR at −1 dBFS near the band edge, with DR and A-weighted figures labelled as such. Evasive: one "SNR" number with no conditions.
2. **"What is the maximum stable amplitude, and what does the converter do on overload?"** Strong: the stable input limit, an overload flag, and the recovery time after a large out-of-band blocker. Evasive: "it's a 1-bit loop, so it's linear."
3. **"Continuous-time or discrete-time, and what limits you: jitter, loop delay or RC variation?"** Strong: a jitter budget with the clock specification it implies, a delay-compensation scheme and RC tuning or calibration. Evasive: "inherent anti-aliasing" as the only answer.
4. **"What is the latency through the decimation filter, and is there a low-latency path?"** Strong: group delay in output samples for each filter option and its effect on control loops or active noise cancellation. Evasive: output data rate only.
5. **"Does the power include the decimation filter, reference and clock?"** Strong: a breakdown that adds up to the package. Evasive: modulator-only power, which is what academic figures of merit use.

### Marketing vs Reality

- **"24-bit."** The output word is 24 bits; the information is not. The ADS127L21 specifies a 111.5 dB dynamic range at 200 kSPS, about **18.2** effective bits by $(DR - 1.76)/6.02$; the ADS1298 guarantees 24 bits with no missing codes only up to 8 kSPS and specifies 17 bits at 32 kSPS [15].
- **"110 dB SNR."** The PCM1865 audio ADC's "110-dB SNR" is specified with a "–60-dB input signal" and A-weighted: it is a dynamic range [15]. A TI application note measures an A-weighted 118 dB dynamic range as 116 dB unweighted, "about 2dB down from the A-weighted setting as expected," and quotes "123dB Dynamic Range with DRE enable and 113dB with DRE disabled" for a part that switches gain on small signals [15]. Murmann's survey excludes such gain switching [13].
- **"Inherent anti-aliasing."** A continuous-time loop does filter its input, but the alias bands do not disappear: the ADS127L21 data sheet warns that out-of-band signals can saturate the modulator, after which "the noise floor increases" [15]. Ask for the attenuation at $f_s \pm f_B$ and the overload behavior.
- **"Fast."** A ΔΣ ADC's output rate is not its latency. The ADS127L21's default FIR filter has a group delay of 34 output periods, 85 µs at 400 kSPS, against 3 µs for its low-latency sinc path [15].
- **Sanity check.** Convert any resolution claim to SNDR at full scale near the band edge; check it against $(6L + 3)$ dB per octave for the stated order and OSR, minus the NTF penalty and a few decibels for a 1-bit quantizer; and ask whether a headline number is dynamic range, weighted, or measured at low frequency only (one 2026 paper's title SNDR of 98.5 dB is 93.9 dB at its band edge in the survey) [13].

## 10. Concept check

**Q1.** Why does oversampling alone gain only 3 dB per octave, while a first-order modulator gains 9 dB?

<details><summary>Answer</summary>

Oversampling alone spreads white noise over a wider band and keeps a fraction 1/OSR: 3 dB per octave. The first-order loop also shapes the noise by $\lvert 1 - z^{-1}\rvert^2 \approx \omega^2$, so the in-band integral scales as $\omega_B^3 \propto 1/\text{OSR}^3$: 9 dB per octave.

</details>

**Q2.** Why is the average of a first-order modulator's output exactly the average of its input?

<details><summary>Answer</summary>

Summing the loop equation telescopes: $\sum(x - y) = u[N] - u[0]$. The integrator is bounded ($\lvert u\rvert \le 1 + \lvert x\rvert$ for $\lvert x\rvert \le 1$), so the difference of averages is at most a bounded quantity divided by $N$.

</details>

**Q3.** What is an idle tone, and when does it fall in band?

<details><summary>Answer</summary>

A periodic pattern in a modulator's output for a constant or slowly varying input, appearing as spectral lines instead of white noise. For a first-order loop with a small DC input $x$ the tones sit at multiples of $\lvert x\rvert f_s$, in band when $\lvert x\rvert < 1/(2\,\text{OSR})$.

</details>

**Q4.** Why does a third-order loop with NTF $(1 - z^{-1})^3$ and a 1-bit quantizer go unstable, and what is the usual fix?

<details><summary>Answer</summary>

The NTF's gain reaches 8 at $f_s/2$, so the quantizer error is amplified and fed back until the integrators run away. Adding NTF poles that limit the out-of-band gain to about 1.5 (Lee's rule) keeps it stable for inputs up to a maximum stable amplitude, at the cost of in-band noise; multi-bit quantizers also help.

</details>

**Q5.** Why does a MASH need much higher op-amp gain than a single loop of the same order?

<details><summary>Answer</summary>

In a single loop, integrator leakage only fills in the NTF's zero at DC by ε, which matters if ε exceeds about $\pi/\text{OSR}$. In a MASH, the digital filter must cancel the first stage's error exactly; leakage leaves that error unshaped at level ε, which must be below the second-order noise, about $\pi^2/\text{OSR}^2$.

</details>

**Q6.** Name one advantage and one weakness of continuous-time modulators against switched-capacitor ones.

<details><summary>Answer</summary>

Advantages: implicit anti-aliasing (the loop filters the input before sampling), a resistive input that is easy to drive, and higher speed at lower power. Weaknesses: sensitivity to clock jitter (an NRZ DAC's charge depends on edge timing), to excess loop delay, and to RC time-constant variation.

</details>

**Q7.** Why must the CIC decimator's order exceed the loop order?

<details><summary>Answer</summary>

The noise that would alias into the band lies near multiples of the decimated rate, where the shaped noise is large. A sinc$^K$ filter has $K$-th-order zeros there; to suppress noise that rises as $f^{2L}$ it needs $K \ge L + 1$.

</details>

Problems: [20-08 problem set](../problems/20-08-problems.md) · Worked solutions: [20-08 solutions](../solutions/20-08-solutions.md)

## 11. Key terms

[Oversampling](../../../reference/glossary.md#oversampling) · [Delta-sigma modulator](../../../reference/glossary.md#delta-sigma-modulator) · [Noise shaping](../../../reference/glossary.md#noise-shaping) · [Noise transfer function (NTF)](../../../reference/glossary.md#noise-transfer-function-ntf) · [Signal transfer function (STF)](../../../reference/glossary.md#signal-transfer-function-stf) · [Idle tone](../../../reference/glossary.md#idle-tone) · [Lee's rule](../../../reference/glossary.md#lees-rule) · [MASH (multi-stage noise shaping)](../../../reference/glossary.md#mash-multi-stage-noise-shaping) · [Continuous-time delta-sigma modulator](../../../reference/glossary.md#continuous-time-delta-sigma-modulator) · [Excess loop delay](../../../reference/glossary.md#excess-loop-delay) · [Dynamic element matching](../../../reference/glossary.md#dynamic-element-matching) · [CIC filter](../../../reference/glossary.md#cic-filter) · [Dither](../../../reference/glossary.md#dither)

## 12. Connections

- **Previous:** [20-07](20-07-nyquist-adcs.md) built resolution from matched components at the Nyquist rate; this chapter builds it from speed and feedback.
- **Builds on:** [20-06](20-06-data-converter-fundamentals.md) (quantization noise, processing gain), [20-05](20-05-comparators-and-sample-and-hold.md) (kT/C, jitter), [11-09](../../11-signals-and-systems/chapters/11-09-z-transform.md) (z-transform), [15-05](../../15-control-systems/chapters/15-05-stability-routh-hurwitz.md) (feedback stability), [16-09](../../16-digital-signal-processing/chapters/16-09-multirate-dsp.md) (decimation, CIC) and [16-10](../../16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) (dither).
- **Next:** [20-09](20-09-dacs.md) uses the same noise shaping in oversampling DACs and the same element matching in multi-bit DACs.
- **Used later:** [20-10](20-10-plls-and-jitter.md) (ΔΣ-modulated fractional-N synthesizers, clock jitter), [20-12](20-12-why-analog-does-not-scale.md) (digitally assisted analog).

## 13. Further study

- R. Schreier, S. Pavan and G. C. Temes, *Understanding Delta-Sigma Data Converters*, 2nd ed., Wiley-IEEE Press, 2017, DOI 10.1002/9781119258308: the standard text; chapters on first- and second-order modulators, higher-order design and continuous-time loops.
- B. Razavi, "The delta-sigma modulator," *IEEE Solid-State Circuits Magazine*, Spring 2016 (§14 [10]): a six-page history and tour, posted on the author's UCLA page.
- R. Schreier, "Oversampling Delta-Sigma Data Converters: The One-Page Story" and his University of Toronto ECE1371 slides (§14 [5]): the noise-shaping law, Lee's rule and toolbox practice in compact form.
- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapter on sigma-delta modulation.
- R. Schreier's Delta Sigma Toolbox (MATLAB, BSD-style licence): synthesize NTFs (its `synthesizeNTF` defaults to Lee's 1.5), simulate modulators and find the maximum stable amplitude.

## 14. Sources

1. H. Inose, Y. Yasuda and J. Murakami, "A telemetering system by code modulation — Δ-Σ modulation," *IRE Trans. Space Electronics and Telemetry*, vol. SET-8, no. 3, pp. 204–209, Sept. 1962, DOI 10.1109/IRET-SET.1962.5008839; H. Inose and Y. Yasuda, "A unity bit coding method by negative feedback," *Proc. IEEE*, vol. 51, no. 11, pp. 1524–1535, 1963, DOI 10.1109/PROC.1963.2622 [R-341].
2. J. C. Candy, "A use of double integration in sigma delta modulation," *IEEE Trans. Commun.*, vol. 33, no. 3, pp. 249–258, 1985, DOI 10.1109/TCOM.1985.1096276 [R-341].
3. Y. Matsuya et al., "A 16-bit oversampling A-to-D conversion technology using triple-integration noise shaping," *IEEE J. Solid-State Circuits*, vol. SC-22, no. 6, pp. 921–929, Dec. 1987, DOI 10.1109/JSSC.1987.1052839 [R-341].
4. B. E. Boser and B. A. Wooley, "The design of sigma-delta modulation analog-to-digital converters," *IEEE J. Solid-State Circuits*, vol. 23, no. 6, pp. 1298–1308, 1988, DOI 10.1109/4.90025 [R-341].
5. R. Schreier, ECE1371 *Advanced Analog Circuits* lecture slides ("Higher-Order ΔΣ Modulators and the ΔΣ Toolbox"; "MOD1 and MOD2"), University of Toronto, and "Oversampling Delta-Sigma Data Converters: The One-Page Story," Analog Devices, 1998–2008; R. Schreier, "An empirical study of high-order single-bit delta-sigma modulators," *IEEE Trans. Circuits Syst. II*, vol. 40, no. 8, pp. 461–466, 1993, DOI 10.1109/82.242348 [R-342].
6. D. Johns and K. Martin, "Oversampling Converters" lecture slides (from *Analog Integrated Circuit Design*, Wiley, 1997), University of Toronto [R-342].
7. K. C.-H. Chao, S. Nadeem, W. L. Lee and C. G. Sodini, "A higher order topology for interpolative modulators for oversampling A/D converters," *IEEE Trans. Circuits Syst.*, vol. 37, no. 3, pp. 309–318, Mar. 1990, DOI 10.1109/31.52724 [R-341].
8. J. A. Cherry and W. M. Snelgrove, "Excess loop delay in continuous-time delta-sigma modulators," *IEEE Trans. Circuits Syst. II*, vol. 46, no. 4, pp. 376–389, Apr. 1999, DOI 10.1109/82.755409, and "Clock jitter and quantizer metastability in continuous-time delta-sigma modulators," *ibid.*, vol. 46, no. 6, pp. 661–676, June 1999, DOI 10.1109/82.769775 [R-341].
9. R. Saad, S. Hoyos and S. Palermo, book chapter on clock-jitter effects in delta-sigma modulators, InTech, 2012, DOI 10.5772/46453 [R-342].
10. B. Razavi, "The delta-sigma modulator [A circuit for all seasons]," *IEEE Solid-State Circuits Magazine*, vol. 8, no. 2, pp. 10–15, Spring 2016, DOI 10.1109/MSSC.2016.2543061 [R-341].
11. E. B. Hogenauer, "An economical class of digital filters for decimation and interpolation," *IEEE Trans. Acoust., Speech, Signal Process.*, vol. 29, no. 2, pp. 155–162, Apr. 1981, DOI 10.1109/TASSP.1981.1163535 [R-341].
12. T. A. D. Riley, M. A. Copeland and T. A. Kwasniewski, "Delta-sigma modulation in fractional-N frequency synthesis," *IEEE J. Solid-State Circuits*, vol. 28, no. 5, pp. 553–559, May 1993, DOI 10.1109/4.229400 [R-341].
13. B. Murmann, "ADC Performance Survey 1997–2026," github.com/bmurmann/ADC-survey (xls/ADCsurvey_latest.xlsx, revision of Aug. 2026), accessed 24 Nov 2026 [R-343].
14. H. Zhao et al., "A fully dynamic noise-shaping SAR ADC achieving 120dB SNDR and 189dB FoMS in 1kHz BW," ISSCC 2025, pp. 306–308, DOI 10.1109/ISSCC49661.2025.10904778; C. Y. Lee and U.-K. Moon, ISSCC 2022, paper 25.3, DOI 10.1109/ISSCC42614.2022.9731606; ISSCC 2022, paper 25.4 (360 MHz CT MASH), DOI 10.1109/ISSCC42614.2022.9731789; ISSCC 2016, paper 15.5 (465 MHz CT MASH), DOI 10.1109/ISSCC.2016.7418015; ISSCC 2019, paper 20.7, DOI 10.1109/ISSCC.2019.8662317; VLSI 2025, paper C5-2, DOI 10.23919/VLSITechnologyandCir65189.2025.11074991; Subramanian et al., ISSCC 2024, pp. 176–178, DOI 10.1109/ISSCC49657.2024.10454526 [R-343].
15. Texas Instruments data sheets: ADS127L21 (SBASAK4C, rev. Aug. 2025), ADS127L11 (SBAS946C, rev. Sept. 2022), PCM186x (SLAS831D, rev. Mar. 2018), ADS1298 (SBAS459K), ADS1292 (SBAS502C, rev. Apr. 2020), LMX2594 (SNAS696C, rev. Apr. 2019); application note SLLA641, July 2024 [R-344].
16. Infineon, IM69D130 data sheet, v1.0, Dec. 2017; TDK InvenSense, T5838 data sheet DS-000383, rev. 1.2, Sept. 2025 [R-344].
