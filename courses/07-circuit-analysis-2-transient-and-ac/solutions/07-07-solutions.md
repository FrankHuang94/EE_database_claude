# Solutions 07-07 · Frequency Response and Bode Plots

Problems: [07-07 problems](../problems/07-07-problems.md) · Chapter: [07-07](../chapters/07-07-frequency-response-and-bode-plots.md). Every number below is recomputed by [verify_07_07.py](../verify/verify_07_07.py), mostly from state-space models and numerical searches that do not use the chapter's formulas; values marked † are also confirmed by ngspice in [labs/07-07-lab](../labs/07-07-lab/README.md).

---

## Solutions

### Solution 07-07.1

(a) $10\lg 2$ = **3.010 dB**, $10\lg 0.5$ = **−3.010 dB**, $10\lg 1000$ = **30.00 dB**.

(b) $20\lg 2$ = **6.021 dB**, $20\lg 0.1$ = **−20.00 dB**, $20\lg\sqrt2$ = **3.010 dB**. A voltage ratio of √2 is a power ratio of 2 across equal resistances, so it is the same 3.010 dB.

(c) $10\lg(1\ \text{W}/1\ \text{mW})$ = **30.00 dBm**; $10\lg(1\ \text{µW}/1\ \text{mW})$ = **−30.00 dBm**; $20\lg(1\ \text{mV}/1\ \text{V})$ = **−60.00 dBV**.

(d) $10^{-6/20}$ = **0.5012** (−6 dB is almost exactly half the voltage); $10^{13/10}$ = **19.95** (13 dB is almost exactly 20 times the power).

### Solution 07-07.2

(a) $1\ \text{Np} = 20/\ln 10$ = **8.686 dB**. $20\ \text{dB} = 20\times(\ln 10/20) = \ln 10$ = **2.303 Np**: a voltage ratio of 10 is $\ln 10$ nepers.

(b) A decade is $\log_2 10 = 3.322$ octaves, so 10 dB/octave is **33.22 dB/decade**. In units of 6.021 dB/octave, $k = 10/6.021$ = **1.661**. (Bode's paper gives 1.67, using 6 dB per octave.)

(c) A constant slope $k$ gives a phase of $k\times90°$ (§3.6): **149.5°** of lag, leaving a phase margin of $180 - 149.5$ = **30.5°**, Bode's "phase margin of 30°". A steeper roll-off would leave less margin.

### Solution 07-07.3

With $x = \omega/\omega_p$: magnitude $-10\lg(1 + x^2)$; asymptote 0 dB for $x \le 1$ and $-20\lg x$ above; phase $-\arctan x$; straight-line phase 0° at $x \le 0.1$, $-45°(1 + \lg x)$ between, −90° at $x \ge 10$.

| $x$ | Magnitude (dB) | Asymptote error (dB) | Phase | Straight-line phase error |
|---|---|---|---|---|
| 0.1 | **−0.04** | −0.04 | **−5.71°** | **−5.71°** |
| 0.5 | **−0.97** | −0.97 | **−26.57°** | **+4.89°** |
| 1 | **−3.01** | −3.01 | **−45.00°** | 0.00° |
| 2 | **−6.99** | **−0.97** | **−63.43°** | −4.89° |
| 10 | **−20.04** | −0.04 | **−84.29°** | +5.71° |

The magnitude errors are symmetric about the corner, as are the phase errors (with opposite sign). The largest phase error, 5.71°, sits at the ends of the straight segment.

### Solution 07-07.4

(a) Divide each factor by its constant: $(s + 10) = 10(1 + s/10)$, $(s + 100) = 100(1 + s/100)$, $(s + 10^4) = 10^4(1 + s/10^4)$. Then

$$
H = \frac{1000\times10}{100\times10^4}\cdot\frac{1 + s/10}{(1 + s/100)(1 + s/10^4)} = 0.01\,\frac{1 + s/10}{(1 + s/100)(1 + s/10^4)} ,
$$

so $K$ = 0.01, a low-frequency gain of **−40.00 dB**.

(b) Flat at −40 dB to 10 rad/s, then +20 dB/decade to 100 rad/s (reaching −20 dB), flat at −20 dB to $10^4$ rad/s, then −20 dB/decade. Asymptotic values: **−40.00 dB** at 1 rad/s, $-40 + 20\lg 5$ = **−26.02 dB** at 50 rad/s, **−20.00 dB** at 1000 rad/s, and **−40.00 dB** at $10^5$ rad/s.

(c) Exact:

| ω (rad/s) | Magnitude | Phase |
|---|---|---|
| 1 | **−39.96 dB** | **5.132°** |
| 50 | **−26.82 dB** | **51.84°** |
| 1000 | **−20.09 dB** | **−0.5729°** |
| $10^5$ | **−40.04 dB** | **−84.24°** |

At 50 rad/s the exact value is **0.80 dB** below the asymptote because two corners (10 and 100 rad/s) are within a decade of it.

(d) The phase is $\arctan(\omega/10) - \arctan(\omega/100) - \arctan(\omega/10^4)$. Maximizing numerically gives **54.72°** at **31.41 rad/s**. The isolated-pair formula, with α = 10, gives $\arcsin(9/11)$ = **54.90°** at $\sqrt{10\times100}$ = 31.62 rad/s. The distant pole at $10^4$ rad/s costs **0.18°** and shifts the maximum slightly.

### Solution 07-07.5

(a) Let $Z_1 = R_1\parallel(1/sC) = R_1/(1 + sR_1C)$. The divider gives

$$
H = \frac{R_2}{R_2 + Z_1} = \frac{R_2(1 + sR_1C)}{R_2(1 + sR_1C) + R_1} = \frac{R_2}{R_1 + R_2}\cdot\frac{1 + sR_1C}{1 + s(R_1\parallel R_2)C} .
$$

(b) Zero at $1/(2\pi R_1C)$ = **1.768 kHz**; pole at $1/(2\pi(R_1\parallel R_2)C)$, with $R_1\parallel R_2$ = 900 Ω, = **17.68 kHz**. Low-frequency gain $R_2/(R_1 + R_2)$ = 0.1, **−20.00 dB**; high-frequency gain 1 (the capacitor shorts $R_1$), **0.00 dB**.

(c) The pole is ten times the zero (α = 10), so the maximum lead is $\arcsin(9/11)$ = **54.90°** at $\sqrt{1.768\times17.68}$ kHz = **5.592 kHz**, where the gain is the geometric mean of −20 and 0 dB: **−10.00 dB**.

(d) Near a loop's crossover, the lead network adds positive phase (up to 55° here) and so increases phase margin (§3.9). The price is its attenuation at low frequency, which the loop must make up with gain. This is the classic "lead compensator" of control design ([15-07](../../15-control-systems/chapters/15-07-frequency-domain-design.md)).

### Solution 07-07.6

(a) At $f_0$, $\lvert H\rvert = 1/(2\zeta)$: **13.98 dB** for ζ = 0.1 (13.98 dB above the asymptotes, which meet at 0 dB), **0.00 dB** for ζ = 0.5 (no error) and **−3.01 dB** for ζ = 0.707.

(b) The phase is $-\operatorname{atan2}(2\zeta r, 1 - r^2)$:

| ζ | Phase at 500 Hz | Phase at 2 kHz |
|---|---|---|
| 0.1 | **−7.595°** | **−172.41°** |
| 0.5 | **−33.69°** | **−146.31°** |
| 0.707 | **−43.31°** | **−136.69°** |

The phases at $f_0/2$ and $2f_0$ sum to −180° in each case, a symmetry of the second-order phase on a log axis.

(c) Peak $1/(2\zeta\sqrt{1 - \zeta^2})$ = **5.025**, or **14.02 dB**, at $f_0\sqrt{1 - 2\zeta^2}$ = **989.9 Hz**.

### Solution 07-07.7

(a) A flat 32 dB with a −20 dB/decade bend near 2 kHz (phase −45° there) and a further bend to −40 dB/decade near 50 kHz (phase −135° there) is two real poles:

$$
H(jf) = \frac{K}{(1 + jf/2\ \text{kHz})(1 + jf/50\ \text{kHz})}, \qquad K = 10^{32/20} = 39.81 .
$$

The phase confirms it is minimum-phase: −45° at the first corner, then −135° near the second.

(b) Asymptote at 10 kHz: $32 - 20\lg(10/2)$ = **18.02 dB**. Exact: **17.68 dB**, phase **−90.00°** (10 kHz is the geometric center of the two corners, where the two phase contributions sum to exactly −90°).

(c) The asymptote at 50 kHz is $32 - 20\lg 25$ = 4.04 dB; falling at −40 dB/decade it reaches 0 dB at $50\ \text{kHz}\times10^{4.04/40}$ = **63.10 kHz**. Solving $\lvert H\rvert = 1$ numerically gives **54.04 kHz**, with phase **−135.10°**. The asymptotic estimate is **16.8%** high because the crossover lies near the second corner, where the asymptote is 3 dB optimistic.

(d) Phase margin $180 - 135.10$ = **44.90°**: adequate but not generous (§3.9).

### Solution 07-07.8

(a) $A_0 = 10^5$, so $f_a$ = 1 MHz/$10^5$ = 10 Hz. Non-inverting +10: β = 1/10, bandwidth $f_a(1 + A_0\beta) = 10\times10\,001$ = **100.0 kHz**. Inverting −10: noise gain 11, β = 1/11, bandwidth $10\times(1 + 10^5/11)$ = **90.92 kHz**.

(b) $t_r = 0.3497/100.0\ \text{kHz}$ = **3.497 µs**.

(c) Bandwidth ≈ GBW/(noise gain) ≥ 20 kHz requires a noise gain of at most **50**.

### Solution 07-07.9

(a) $\sqrt{2^{1/n} - 1}$: **0.6436** for $n$ = 2, **0.5098** for 3 and **0.4350** for 4.

(b) Each stage needs $f_c \ge 1\ \text{MHz}/0.5098$ = **1.961 MHz**.

### Solution 07-07.10

(a) $\phi = -360°\,fT$: **−7.200°** at 10 MHz, **−72.00°** at 100 MHz and **−360.0°** at 500 MHz (a full cycle: the output is one period late and in phase again, which the phase alone cannot reveal).

(b) $\tau_g = (1/\omega_p)/(1 + (\omega/\omega_p)^2)$. At DC, $1/\omega_p = 1/(2\pi\times1\ \text{kHz})$ = **159.2 µs**, the time constant. At the corner it halves to **79.58 µs**.

### Solution 07-07.11

(a) Exact: solve $(1 + (f/350)^2)(1 + (f/500)^2) = 2$ (f in MHz): **263.3 MHz**. Estimate: $1/\sqrt{1/350^2 + 1/500^2}$ = **286.7 MHz**.

(b) The step response of two cascaded poles (Example 07-07.6) gives an exact rise time of **1.308 ns**. The single-pole rise times are $0.3497/350\ \text{MHz}$ = **0.9991 ns** and $0.3497/500\ \text{MHz}$ = **0.6994 ns**, whose root-sum-square is **1.220 ns**.

(c) Both estimates are optimistic (too much bandwidth, too short a rise time): the system's bandwidth is **8.2%** lower than the estimate, and its rise time **7.2%** longer. The quadrature rules are exact for Gaussian-shaped responses; single poles are not Gaussian (§3.7). A probe matters even when it is "faster" than the scope.

### Solution 07-07.12

(a) $\lvert Z\rvert = \sigma/\sqrt\omega$: at 1 Hz, $10^{-3}/\sqrt{2\pi}$ = **0.3989 mΩ**; at 100 Hz, **0.03989 mΩ**.

(b) A factor of 100 in frequency divides $\lvert Z\rvert$ by 10, which is −20 dB per two decades: **−10 dB/decade**. The phase of $(j)^{-1/2} = e^{-j\pi/4}$ is **−45°** at every frequency.

(c) In Bode's terms the slope is $k = -1/2$ (half of 20 dB/decade), so the constant-slope relation gives $k\times90° = -45°$, exactly as found. Because the phase is constant, $\operatorname{Re}Z = -\operatorname{Im}Z$ at every frequency, so on a Nyquist plot ($-\operatorname{Im}Z$ against $\operatorname{Re}Z$) the diffusion region is a straight line at 45°. A battery engineer reading such a line is reading a −10 dB/decade Bode slope.

### Solution 07-07.13

(a) $\lvert T(j\omega_c)\rvert = 1$ gives $x\sqrt{1 + x^2} = 1$ with $x = \omega_c/\omega_t$: $x^2 = (\sqrt5 - 1)/2$, $x$ = **0.7862**. The phase is $-90° - \arctan x$, so PM = $90° - \arctan(0.7862)$ = **51.83°**. Closed loop: $\omega_0 = \sqrt{\omega_t\omega_2} = \omega_t$ and ζ = $\tfrac12\sqrt{\omega_2/\omega_t}$ = **0.5000**. Peak $1/(2\zeta\sqrt{1 - \zeta^2})$ = **1.155**, or **1.249 dB**, at $\omega_0\sqrt{1 - 2\zeta^2}$ = **0.7071** $\omega_0$.

(b) $x\sqrt{1 + x^2/4} = 1$ gives $x^2 = 2(\sqrt2 - 1)$, $x$ = 0.9102, PM = $90° - \arctan(0.4551)$ = **65.53°**, ζ = $\tfrac12\sqrt2$ = **0.7071**: no peak (0 dB), the maximally flat response.

(c) 55° lies between the two cases. Solving this model for a 55° margin gives ζ = **0.541**, a closed-loop peak of **0.82 dB** and a step overshoot of **13.3%**. A unity-gain buffer with that op-amp overshoots slightly on small steps, and more with capacitive load.

### Solution 07-07.14

(a) $R_d = \sqrt{4.7\ \text{µH}/22\ \text{µF}}$ = **0.4622 Ω**. Without $C_d$, $R_d$ would sit directly across the output and burn DC power ($V^2/R_d$ = 54 W at 5 V). $C_d$ blocks DC, so the damper dissipates only at AC, and at the resonance its impedance is mostly resistive, which absorbs the tank's energy.

(b) Without the damper the gain at 15.68 kHz is **19.07 dB** (Example 07-07.3). With it, solving the divider $Z_p/(R_s + j\omega L + Z_p)$ with $Z_p = R_L\parallel(1/j\omega C)\parallel(R_d + 1/j\omega C_d)$ gives **−0.70 dB**.

(c) Sweeping numerically, the damped response peaks at **2.27 dB** at **8.67 kHz**. The peak moves down because at low frequency $C_d$ adds to $C$ (the effective capacitance approaches 5C, lowering the resonance by about $\sqrt5$).

(d) At 500 kHz the gain is **−60.17 dB**, the same as without the damper. Far above resonance $C$ already shorts the output and the inductor sets the attenuation; the damper's branch, at 0.46 Ω, is in parallel with $C$'s **0.0145 Ω** and changes almost nothing. The damper trades a larger capacitor and a resistor for a **16.8 dB** reduction in peaking without losing high-frequency attenuation.

### Solution 07-07.15

(a) The zero factors are $1 \pm j\omega/10^4$, whose magnitudes are both $\sqrt{1 + (\omega/10^4)^2}$. Everything else is shared, so $\lvert H_1(j\omega)\rvert = \lvert H_2(j\omega)\rvert$ at every frequency. A magnitude plot cannot tell them apart.

(b) Each phase is the zero's angle minus the two poles' angles. The left-half-plane zero contributes $+\arctan(\omega/10^4)$; the right-half-plane zero contributes $-\arctan(\omega/10^4)$.

| ω (rad/s) | zero | poles | $H_1$ | $H_2$ |
|---|---|---|---|---|
| $10^3$ | ±5.71° | −45° − 0.57° | **−39.86°** | **−51.28°** |
| $10^4$ | ±45° | −84.29° − 5.71° | **−45.00°** | **−135.0°** |
| $10^5$ | ±84.29° | −89.43° − 45° | **−50.14°** | **−218.7°** |

(c) $H_1$ goes from 0° to $-90°$ (two poles, one zero: $-180° + 90°$). $H_2$ goes from 0° to **−270°**: its zero *adds* lag, just like a third pole, while raising the gain like a zero. In a loop, the extra lag arrives at frequencies where the gain is still high, so the phase reaches −180° while the loop gain is still large. Phase margin is lost, and compensation cannot recover it by cancelling the zero, because a cancelling pole would have to sit in the right half-plane, where it would be unstable itself. This is the "non-minimum-phase" limitation of boost converters (Course 22) and of some transistor stages (Course 12).

(d) For a 1 V step, $Y(s) = H_2(s)/s$:

- $y(0^+) = \lim_{s\to\infty}sY = H_2(\infty) = $ **0**, since the denominator's degree is higher;
- the initial slope is $\lim_{s\to\infty}s^2Y = \lim sH_2(s)$, which tends to $10\times(-1/10^4)/(10^{-3}\times10^{-5}) = $ **−100 000 V/s**;
- the final value is $H_2(0) = $ **10 V**.

The response starts by heading the wrong way, below zero, before turning round and rising to +10 V: the time-domain signature of a right-half-plane zero (07-04 §9). $H_1$'s slope starts at +100 000 V/s and heads straight for 10 V.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-07.1a | power ratio 2 | 3.010 | dB |
| 07-07.1b | power ratio 0.5 | −3.010 | dB |
| 07-07.1c | power ratio 1000 | 30.00 | dB |
| 07-07.1d | voltage ratio 2 | 6.021 | dB |
| 07-07.1e | voltage ratio 0.1 | −20.00 | dB |
| 07-07.1f | voltage ratio √2 | 3.010 | dB |
| 07-07.1g | 1 W | 30.00 | dBm |
| 07-07.1h | 1 µW | −30.00 | dBm |
| 07-07.1i | 1 mV | −60.00 | dBV |
| 07-07.1j | −6 dB as a voltage ratio | 0.5012 | — |
| 07-07.1k | 13 dB as a power ratio | 19.95 | — |
| 07-07.2a | 1 Np | 8.686 | dB |
| 07-07.2b | 20 dB | 2.303 | Np |
| 07-07.2c | 10 dB/octave | 33.22 | dB/decade |
| 07-07.2d | slope k | 1.661 | — |
| 07-07.2e | phase lag | 149.5 | ° |
| 07-07.2f | phase margin | 30.5 | ° |
| 07-07.3a | magnitude at 0.1 | −0.04 | dB |
| 07-07.3b | magnitude at 0.5 | −0.97 | dB |
| 07-07.3c | magnitude at 1 | −3.01 | dB |
| 07-07.3d | magnitude at 2 | −6.99 | dB |
| 07-07.3e | magnitude at 10 | −20.04 | dB |
| 07-07.3f | asymptote error at 2 | −0.97 | dB |
| 07-07.3g | phase at 0.1 | −5.71 | ° |
| 07-07.3h | phase at 0.5 | −26.57 | ° |
| 07-07.3i | phase at 1 | −45.00 | ° |
| 07-07.3j | phase at 2 | −63.43 | ° |
| 07-07.3k | phase at 10 | −84.29 | ° |
| 07-07.3l | straight-line phase error at 0.1 | −5.71 | ° |
| 07-07.3m | straight-line phase error at 0.5 | 4.89 | ° |
| 07-07.4a | low-frequency gain | −40.00 | dB |
| 07-07.4b | asymptote at 50 rad/s | −26.02 | dB |
| 07-07.4c | asymptote at 1000 rad/s | −20.00 | dB |
| 07-07.4d | asymptote at 10⁵ rad/s | −40.00 | dB |
| 07-07.4e | exact magnitude at 1 rad/s | −39.96 | dB |
| 07-07.4f | exact magnitude at 50 rad/s | −26.82 | dB |
| 07-07.4g | exact magnitude at 1000 rad/s | −20.09 | dB |
| 07-07.4h | exact magnitude at 10⁵ rad/s | −40.04 | dB |
| 07-07.4i | phase at 1 rad/s | 5.132 | ° |
| 07-07.4j | phase at 50 rad/s | 51.84 | ° |
| 07-07.4k | phase at 1000 rad/s | −0.5729 | ° |
| 07-07.4l | phase at 10⁵ rad/s | −84.24 | ° |
| 07-07.4m | maximum lead | 54.72 | ° |
| 07-07.4n | frequency of maximum lead | 31.41 | rad/s |
| 07-07.4o | isolated-pair formula | 54.90 | ° |
| 07-07.4p | exact below asymptote at 50 rad/s | 0.80 | dB |
| 07-07.4q | lead lost to the distant pole | 0.18 | ° |
| 07-07.5a | zero | 1.768 | kHz |
| 07-07.5b | pole | 17.68 | kHz |
| 07-07.5c | low-frequency gain | −20.00 | dB |
| 07-07.5d | high-frequency gain | 0.00 | dB |
| 07-07.5e | maximum lead | 54.90 | ° |
| 07-07.5f | frequency of maximum lead | 5.592 | kHz |
| 07-07.5g | gain there | −10.00 | dB |
| 07-07.6a | magnitude at $f_0$, ζ = 0.1 | 13.98 | dB |
| 07-07.6b | magnitude at $f_0$, ζ = 0.5 | 0.00 | dB |
| 07-07.6c | magnitude at $f_0$, ζ = 0.707 | −3.01 | dB |
| 07-07.6d | phase at 500 Hz, ζ = 0.1 | −7.595 | ° |
| 07-07.6e | phase at 2 kHz, ζ = 0.1 | −172.41 | ° |
| 07-07.6f | phase at 500 Hz, ζ = 0.5 | −33.69 | ° |
| 07-07.6g | phase at 2 kHz, ζ = 0.5 | −146.31 | ° |
| 07-07.6h | phase at 500 Hz, ζ = 0.707 | −43.31 | ° |
| 07-07.6i | phase at 2 kHz, ζ = 0.707 | −136.69 | ° |
| 07-07.6j | peak, ζ = 0.1 | 14.02 | dB |
| 07-07.6k | peak frequency, ζ = 0.1 | 989.9 | Hz |
| 07-07.6l | peak ratio, ζ = 0.1 | 5.025 | — |
| 07-07.7a | K | 39.81 | — |
| 07-07.7b | asymptote at 10 kHz | 18.02 | dB |
| 07-07.7c | exact gain at 10 kHz | 17.68 | dB |
| 07-07.7d | phase at 10 kHz | −90.00 | ° |
| 07-07.7e | asymptotic 0 dB frequency | 63.10 | kHz |
| 07-07.7f | exact 0 dB frequency | 54.04 | kHz |
| 07-07.7g | phase at the 0 dB frequency | −135.10 | ° |
| 07-07.7h | phase margin | 44.90 | ° |
| 07-07.7i | asymptotic estimate's excess | 16.8 | % |
| 07-07.8a | bandwidth at +10 | 100.0 | kHz |
| 07-07.8b | bandwidth at −10 | 90.92 | kHz |
| 07-07.8c | rise time at +10 | 3.497 | µs |
| 07-07.8d | largest noise gain for 20 kHz | 50 | — |
| 07-07.9a | factor, 2 stages | 0.6436 | — |
| 07-07.9b | factor, 3 stages | 0.5098 | — |
| 07-07.9c | factor, 4 stages | 0.4350 | — |
| 07-07.9d | corner per stage | 1.961 | MHz |
| 07-07.10a | delay phase at 10 MHz | −7.200 | ° |
| 07-07.10b | delay phase at 100 MHz | −72.00 | ° |
| 07-07.10c | delay phase at 500 MHz | −360.0 | ° |
| 07-07.10d | group delay at DC | 159.2 | µs |
| 07-07.10e | group delay at the corner | 79.58 | µs |
| 07-07.11a | exact system bandwidth | 263.3 | MHz |
| 07-07.11b | reciprocal-quadrature estimate | 286.7 | MHz |
| 07-07.11c | exact rise time | 1.308 | ns |
| 07-07.11d | root-sum-square rise time | 1.220 | ns |
| 07-07.11e | bandwidth shortfall versus estimate | 8.2 | % |
| 07-07.11f | rise time excess versus estimate | 7.2 | % |
| 07-07.11g | scope rise time alone | 0.9991 | ns |
| 07-07.11h | probe rise time alone | 0.6994 | ns |
| 07-07.12a | impedance magnitude at 1 Hz | 0.3989 | mΩ |
| 07-07.12b | impedance magnitude at 100 Hz | 0.03989 | mΩ |
| 07-07.12c | slope | −10 | dB/decade |
| 07-07.12d | phase | −45 | ° |
| 07-07.13a | crossover ratio, $\omega_2 = \omega_t$ | 0.7862 | — |
| 07-07.13b | phase margin, $\omega_2 = \omega_t$ | 51.83 | ° |
| 07-07.13c | ζ, $\omega_2 = \omega_t$ | 0.5000 | — |
| 07-07.13d | peak, $\omega_2 = \omega_t$ | 1.249 | dB |
| 07-07.13e | peak frequency / $\omega_0$ | 0.7071 | — |
| 07-07.13k | peak ratio, $\omega_2 = \omega_t$ | 1.155 | — |
| 07-07.13f | phase margin, $\omega_2 = 2\omega_t$ | 65.53 | ° |
| 07-07.13g | ζ, $\omega_2 = 2\omega_t$ | 0.7071 | — |
| 07-07.13h | ζ for a 55° margin | 0.541 | — |
| 07-07.13i | peak for a 55° margin | 0.82 | dB |
| 07-07.13j | overshoot for a 55° margin | 13.3 | % |
| 07-07.14a | $R_d$ | 0.4622 | Ω |
| 07-07.14b | gain at $f_0$, undamped | 19.07 | dB |
| 07-07.14c | gain at $f_0$, damped | −0.70 | dB |
| 07-07.14d | damped peak | 2.27 | dB |
| 07-07.14e | damped peak frequency | 8.67 | kHz |
| 07-07.14f | gain at 500 kHz, damped | −60.17 | dB |
| 07-07.14g | DC power $R_d$ alone would burn at 5 V | 54 | W |
| 07-07.14h | reduction in peaking | 16.8 | dB |
| 07-07.14i | reactance of C at 500 kHz | 0.0145 | Ω |
| 07-07.15a | phase of $H_1$ at $10^3$ | −39.86 | ° |
| 07-07.15b | phase of $H_2$ at $10^3$ | −51.28 | ° |
| 07-07.15c | phase of $H_1$ at $10^4$ | −45.00 | ° |
| 07-07.15d | phase of $H_2$ at $10^4$ | −135.0 | ° |
| 07-07.15e | phase of $H_1$ at $10^5$ | −50.14 | ° |
| 07-07.15f | phase of $H_2$ at $10^5$ | −218.7 | ° |
| 07-07.15g | total phase of $H_2$ | −270 | ° |
| 07-07.15h | step response at $0^+$ | 0 | V |
| 07-07.15i | initial slope of the step response | −100000 | V/s |
| 07-07.15j | final value | 10 | V |
