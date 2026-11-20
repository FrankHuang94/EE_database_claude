<!-- status: verified -->
# 16-02 · DTFT and z-Transform for DSP

| | |
|---|---|
| **Course** | [16 · Digital Signal Processing](../README.md) |
| **University equivalent** | The transform-analysis chapter of a senior DSP course: frequency response from poles and zeros, group delay, linear phase, minimum-phase and all-pass systems, inverse systems (Oppenheim & Schafer, *Discrete-Time Signal Processing*, ch. 5; Lyons, *Understanding Digital Signal Processing*, ch. 6) |
| **Prerequisites** | [16-01 Discrete-Time Signals and Systems Review](16-01-discrete-time-systems-review.md), [11-07 Discrete-Time Fourier Transform](../../11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md), [11-09 The z-Transform](../../11-signals-and-systems/chapters/11-09-z-transform.md), [02-01 Complex Numbers, Euler and Phasors](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| **Estimated study hours** | 6 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Find a filter's frequency response from its system function, and sketch its magnitude and phase from the positions of its poles and zeros.
2. Place poles and zeros to build notch, resonator and DC-blocking filters, and predict their bandwidth and settling time from the pole radius.
3. Compute group delay from pole and zero positions, and state the conditions for linear phase.
4. Explain what makes a system minimum phase, convert any rational system into a minimum-phase part times an all-pass part, and compare the energy delay and group delay of systems with the same magnitude response.
5. Design first-order all-pass filters for a given delay, and say what all-pass sections are used for.
6. Decide when a system has a causal, stable inverse, and design a delayed FIR equalizer for a channel that does not.

---

## 1. Big picture

Course 11 built the DTFT and the z-transform as mathematics. This chapter turns them into a designer's instrument panel. A rational system function $H(z)$ is fixed by a handful of poles and zeros, and their positions in the z-plane can be read like a map: the magnitude response, the phase, the delay, whether the filter is stable, whether it can be undone. Filter design in the following chapters is mostly the art of putting those few points in the right places. Much of what distinguishes a good filter from a bad one is invisible in the magnitude response alone; it lives in the phase, which this chapter makes concrete through group delay, minimum phase and all-pass systems.

- **Notches and resonators** are two-pole, two-zero filters placed by eye: mains-hum removal in medical sensors, feedback suppression in hearing aids, tone detection in modems.
- **Group delay** sets latency and waveform fidelity: audio crossovers, video, and data links all budget it.
- **Minimum phase** decides whether a channel can be inverted causally. A high-speed link's channel generally is not minimum phase, which is why link equalizers carry taps that act on *future* samples (precursor taps) and pay for them in latency.
- **All-pass filters** change phase without changing magnitude: they equalize group delay, build fractional delays for timing recovery, and form the arms of efficient filter banks.

## 2. Intuition first

**The z-plane as a rubber sheet.** Picture $\lvert H(z)\rvert$ as a sheet stretched over the z-plane, pinned to the floor at every zero and pushed up to infinity by a tent pole at every pole. The frequency response is what you see walking once around the unit circle, from $\omega = 0$ at $z = 1$, through $\omega = \pi/2$ at $z = j$, to $\omega = \pi$ at $z = -1$. Walk past a zero on the circle and the sheet touches the floor: a null. Walk past a pole just inside the circle and you climb its tent: a peak, sharper the closer the pole sits to the path. A pole and a zero close together cancel each other's effect everywhere except right next to them.

**Analogy: a bond's duration.** A finance reader knows two bonds can have the same total cash flows but different timing; duration measures *when* the money arrives. Group delay plays that role for a filter: it measures how late each frequency's energy arrives. Minimum-phase systems are the "front-loaded" bonds: of all systems with the same magnitude response (the same total "cash" at each frequency), they deliver their energy earliest. **Where the analogy breaks:** a bond's cash flows are positive, while a filter's impulse response can change sign; and group delay can even be negative at some frequencies, which has no counterpart in a plain bond's Macaulay duration.

## 3. Theory

### 3.1 From system function to frequency response

A causal LTI system described by the difference equation of 16-01 §3.4 has the **system function**

$$
H(z) = \frac{\sum_{k=0}^{M}b_kz^{-k}}{1 + \sum_{k=1}^{N}a_kz^{-k}} = b_0\,\frac{\prod_{i=1}^{M}(1 - z_iz^{-1})}{\prod_{i=1}^{N}(1 - p_iz^{-1})} ,
$$

with **zeros** $z_i$ and **poles** $p_i$ (11-09). Its **region of convergence** (ROC) is the set of $z$ where the defining sum $\sum h[n]z^{-n}$ converges: for a causal system, the outside of a circle through the outermost pole. The system is stable exactly when the ROC contains the unit circle (11-09), so a causal system is stable exactly when all its poles are inside the circle, as 16-01 §3.5 found from the impulse response.

On the unit circle, $z = e^{j\omega}$, the system function becomes the frequency response, the DTFT of $h[n]$:

$$
H(e^{j\omega}) = \sum_n h[n]e^{-j\omega n} = \lvert H(e^{j\omega})\rvert\,e^{j\phi(\omega)} .
$$

It is periodic in $\omega$ with period $2\pi$, and for a real $h[n]$ it is conjugate-symmetric, $H(e^{-j\omega}) = H^*(e^{j\omega})$, so the magnitude is even and the phase odd: plotting $0 \le \omega \le \pi$ shows everything. Engineers plot the magnitude in decibels, $20\log_{10}\lvert H\rvert$, and the phase either directly or through its derivative, the group delay (§3.4).

### 3.2 The geometric view

Multiply the numerator and denominator factors by $z$: $1 - z_iz^{-1} = (z - z_i)/z$. With $M$ zeros and $N$ poles,

$$
H(e^{j\omega}) = b_0\,e^{-j\omega(M - N)}\,\frac{\prod_{i}(e^{j\omega} - z_i)}{\prod_{i}(e^{j\omega} - p_i)} .
$$

Each factor $e^{j\omega} - c$ is the vector from the point $c$ to the point $e^{j\omega}$ on the unit circle. So

$$
\lvert H(e^{j\omega})\rvert = \lvert b_0\rvert\,\frac{\prod(\text{distances from the zeros})}{\prod(\text{distances from the poles})}, \qquad \phi(\omega) = \sum\angle(\text{zero vectors}) - \sum\angle(\text{pole vectors}) - (M - N)\omega ,
$$

plus $\pi$ if $b_0 < 0$. This is the same picture as the s-plane Bode construction of 07-07, wrapped around a circle instead of laid along the imaginary axis. It makes three rules of thumb exact:

- **A zero on the unit circle at angle $\omega_0$** makes $\lvert H\rvert = 0$ at $\omega_0$ exactly.
- **A pole at radius $r$ close to the circle** dominates the gain near its angle, because one distance becomes very small (§3.3).
- **A pole and a zero close together** have nearly equal distances to any point on the circle far from them, so they cancel there and act only nearby.

### 3.3 Placing poles and zeros: resonators, notches and DC blockers

**A pole near the circle.** Put a pole at $p = re^{j\omega_0}$ with $1 - r \ll 1$. For $\omega$ near $\omega_0$, the vector from $p$ to $e^{j\omega}$ is nearly the hypotenuse of a small right triangle with legs $1 - r$ (radial) and $\omega - \omega_0$ (along the circle, an arc of radius 1):

$$
\lvert e^{j\omega} - p\rvert^2 \approx (1 - r)^2 + (\omega - \omega_0)^2 .
$$

The squared distance doubles, so the power gain halves, when $\lvert\omega - \omega_0\rvert = 1 - r$. The **half-power (−3 dB) bandwidth** is therefore

$$
\Delta\omega_{3\,\text{dB}} \approx 2(1 - r)\ \text{rad/sample}, \qquad \Delta f_{3\,\text{dB}} \approx \frac{(1 - r)f_s}{\pi} .
$$

The same pole decays in time as $r^n = e^{-n/\tau_s}$ with $\tau_s = -1/\ln r \approx 1/(1 - r)$ samples. So $\Delta\omega_{3\,\text{dB}}\,\tau_s \approx 2$: **a narrow filter rings for a long time**. This is the discrete-time form of the bandwidth–settling tradeoff that every resonance obeys (07-08), and no clever design escapes it.

**Resonator.** Poles at $re^{\pm j\omega_0}$ give a peak at $\omega_0$. Zeros at $z = \pm1$ keep the response at DC and at the Nyquist frequency zero, which makes the peak the only feature:

$$
H_{res}(z) = \frac{1 - z^{-2}}{1 - 2r\cos\omega_0\,z^{-1} + r^2z^{-2}} .
$$

At $\omega_0$, the near pole is $1 - r$ away and dominates; the peak gain is roughly $1/(1 - r)$ times the ratio of the zero distances to the far-pole distance, and the quality factor $Q = \omega_0/\Delta\omega_{3\,\text{dB}} \approx \omega_0/[2(1 - r)]$ (Example 16-02.3).

**Notch.** Put zeros *on* the circle at $e^{\pm j\omega_0}$ and poles just inside at $re^{\pm j\omega_0}$:

$$
H_{notch}(z) = g\,\frac{1 - 2\cos\omega_0\,z^{-1} + z^{-2}}{1 - 2r\cos\omega_0\,z^{-1} + r^2z^{-2}} .
$$

Far from $\omega_0$ each zero–pole pair is a near-cancelling dipole and the gain is nearly 1 (set exactly to 1 at DC by the constant $g$); at $\omega_0$ the zero forces a perfect null. The pole radius sets the notch width by the same rule, $\Delta\omega_{3\,\text{dB}} \approx 2(1 - r)$, and the settling time by $\tau_s \approx 1/(1 - r)$ (Example 16-02.2). Five multiplies per sample buy a notch far narrower than the moving average of 16-01 could.

![Two panels. Left: the z-plane near z = 1, showing the unit circle, two zeros on it at angles plus and minus 0.1 pi, and the poles of two notches at the same angles: at radius 0.98 just inside the zeros, and at radius 0.9 farther in. Right: gain in dB from 0 to 150 Hz at fs = 1 kHz. Both notches are flat near 0 dB except for a sharp null at 50 Hz; the r = 0.98 notch is about 6 Hz wide at -3 dB and the r = 0.9 notch about 28 Hz wide. The 20-point moving average of chapter 16-01, dotted, also nulls 50 Hz but droops steadily from 0 Hz, is near -13 dB between 50 and 100 Hz, and nulls 100 Hz as well.](../../../assets/figures/16-02/notch.svg)

*Figure 1. Two 50 Hz notches at $f_s$ = 1 kHz (Example 16-02.2). The zeros sit on the circle; the pole radius sets the width. The 20-point moving average of 16-01 removes the hum too, but it is already 3 dB down at 22 Hz and attenuates everything above.*

**DC blocker.** A zero at $z = 1$ and a pole just inside it, $H(z) = (1 - z^{-1})/(1 - az^{-1})$, removes DC and passes everything above a corner near $(1 - a)$ rad/sample. Audio and sensor chains use it to strip ADC offsets.

### 3.4 Phase, group delay and linear phase

The **group delay** is

$$
\tau_g(\omega) = -\frac{d\phi(\omega)}{d\omega}\quad\text{samples}.
$$

A narrowband signal centred at $\omega$ (a short burst of a tone) emerges with its envelope delayed by $\tau_g(\omega)$ samples, which is why group delay, not phase itself, is what an engineer budgets. A pure delay $z^{-D}$ has $\phi = -D\omega$ and $\tau_g = D$ at every frequency.

**Group delay of one zero or pole.** For a factor $1 - ce^{-j\omega}$ with $c = \rho e^{j\theta}$, write $\ln(1 - ce^{-j\omega}) = \ln\lvert\cdot\rvert + j\phi_c$ and differentiate. Since $\frac{d}{d\omega}\ln(1 - ce^{-j\omega}) = \dfrac{jce^{-j\omega}}{1 - ce^{-j\omega}}$, the phase derivative is the real part of $ce^{-j\omega}/(1 - ce^{-j\omega})$. Multiplying top and bottom by the conjugate of the denominator gives

$$
\tau_{zero}(\omega) = -\frac{d\phi_c}{d\omega} = \frac{\rho^2 - \rho\cos(\omega - \theta)}{1 - 2\rho\cos(\omega - \theta) + \rho^2} .
$$

A pole contributes the same expression with the opposite sign, because it sits in the denominator. Group delays of cascaded factors add, as their phases do. Two cases to remember:

- A pole at radius $\rho$ just inside the circle, evaluated at its own angle, gives $\tau = \rho/(1 - \rho)$: large and positive, the long ringing of §3.3 seen as delay.
- A zero *inside* the circle has negative group delay near its angle, and a zero *outside* has positive group delay there. The next section builds on exactly this difference.

**Linear phase.** If $h[n]$ is real and symmetric, $h[n] = h[N - 1 - n]$, pair the terms $n$ and $N - 1 - n$:

$$
H(e^{j\omega}) = e^{-j\omega(N-1)/2}\sum_{n=0}^{N-1} h[n]\cos\bigl(\omega(n - \tfrac{N-1}{2})\bigr) ,
$$

because after factoring out $e^{-j\omega(N-1)/2}$ the sine terms of each symmetric pair cancel. The sum is real, so the phase is $-\omega(N - 1)/2$ (plus jumps of $\pi$ where the real factor changes sign): a constant group delay of $(N - 1)/2$ samples. Every frequency is delayed equally and waveshapes survive, at the cost of that fixed delay. In the z-plane, symmetry means $H(z) = z^{-(N-1)}H(1/z)$: whenever $z_0$ is a zero, so is $1/z_0$, and with real coefficients so are $z_0^*$ and $1/z_0^*$. Linear-phase zeros come in reciprocal pairs or quadruples, or sit on the unit circle (16-06 classifies the four types).

### 3.5 Minimum phase

**Reflecting a zero preserves the magnitude.** For any $z_0 \ne 0$ and any point $e^{j\omega}$ on the unit circle,

$$
\lvert e^{j\omega} - z_0\rvert = \lvert z_0\rvert\,\bigl\lvert e^{j\omega} - 1/z_0^*\bigr\rvert .
$$

*Proof:* $\lvert e^{j\omega} - z_0\rvert = \lvert e^{-j\omega}\rvert\,\lvert e^{j\omega} - z_0\rvert = \lvert 1 - z_0e^{-j\omega}\rvert = \lvert 1 - z_0^*e^{j\omega}\rvert$ (a number and its conjugate have the same magnitude), and $\lvert 1 - z_0^*e^{j\omega}\rvert = \lvert z_0^*\rvert\,\lvert 1/z_0^* - e^{j\omega}\rvert$. So moving a zero from $z_0$ to its **reflection** $1/z_0^*$ across the unit circle changes the magnitude response only by the constant factor $\lvert z_0\rvert$. A system with $M$ zeros off the circle has $2^M$ relatives with the same magnitude shape, one for each choice of inside or outside; if the coefficients must stay real, a conjugate pair must be reflected together, so $R$ real zeros and $C$ conjugate pairs give $2^{R + C}$ real-coefficient relatives.

A causal stable system is **minimum phase** if all its zeros (as well as its poles) lie inside the unit circle. Among all causal stable systems with the same magnitude response it has three properties:

1. **Least group delay.** Reflecting a zero from $1/z_0^*$ (outside) to $z_0$ (inside) lowers its group-delay contribution at every frequency by exactly the group delay of a first-order all-pass section (§3.6), which is positive everywhere. (The inside zero's own contribution is negative only near its angle: a zero at 0.5 contributes −1 sample at DC but +1/3 at π, Example 16-02.4.) So the minimum-phase member has the smallest total group delay (and the smallest phase lag) at every frequency.
2. **Fastest energy.** Its partial energy $E(n) = \sum_{k=0}^{n}\lvert h[k]\rvert^2$ is the largest of the family for every $n$: its energy arrives first (Example 16-02.4).
3. **A causal, stable inverse.** $1/H(z)$ has its poles at the zeros of $H$. If those are all inside the circle, the inverse is causal and stable. A zero outside the circle becomes an unstable pole of the causal inverse (§3.7).

> **Going deeper — why the energy arrives first.** For one zero, compare $h_{in} = (1, -a)$ with $h_{out} = (-a^*, 1)$, $\lvert a\rvert < 1$: they have the same total energy $1 + \lvert a\rvert^2$, and $E_{in}(0) = 1 > \lvert a\rvert^2 = E_{out}(0)$. For a general system, write $H = H_{rest}(z)\,(1 - az^{-1})$ against $H_{rest}(z)\,(-a^* + z^{-1})$. With $g$ the impulse response of $H_{rest}$, the two outputs are $g[n] - ag[n-1]$ and $-a^*g[n] + g[n-1]$. Subtracting their squared magnitudes term by term gives $(1 - \lvert a\rvert^2)\bigl(\lvert g[n]\rvert^2 - \lvert g[n-1]\rvert^2\bigr)$, and summing to $n$ telescopes to $(1 - \lvert a\rvert^2)\lvert g[n]\rvert^2 \ge 0$. Reflecting any zero inward never delays energy, so the all-inside member is the fastest. (Oppenheim & Schafer §5.6.)

![Three panels for the filters (2, -2, 0.5), (1, -2.5, 1) and (0.5, -2, 2), which share one magnitude response. Left: their impulse responses; the minimum-phase filter has its largest tap first, the maximum-phase filter last, and the linear-phase filter is symmetric. Middle: partial energy as a fraction of the total; at n = 0 it is 0.48 for minimum phase, 0.12 for linear phase and 0.03 for maximum phase, and the minimum-phase curve stays above the others until all reach 1 at n = 2. Right: group delay against frequency; linear phase is a constant 1 sample, minimum phase rises from -2 samples at DC toward 0.67 at pi, and maximum phase falls from 4 samples at DC toward 1.33 at pi.](../../../assets/figures/16-02/phase-family.svg)

*Figure 2. One magnitude response, three phases (Problem 16-02.9): the minimum-phase member delivers its energy first and has the least group delay at every frequency.*

### 3.6 All-pass filters

The first-order **all-pass** section with real $a$, $\lvert a\rvert < 1$, is

$$
H_{ap}(z) = \frac{z^{-1} - a}{1 - az^{-1}} .
$$

Its zero is at $1/a$, the reflection of its pole at $a$. On the unit circle the numerator is $e^{-j\omega}(1 - ae^{j\omega})$, whose magnitude equals that of the denominator $1 - ae^{-j\omega}$ (conjugates), so $\lvert H_{ap}(e^{j\omega})\rvert = 1$ at every frequency: the filter changes only phase. Its group delay, from §3.4 (the delay $z^{-1}$, plus the factor $1 - ae^{j\omega}$, minus the pole), simplifies to

$$
\tau_{ap}(\omega) = \frac{1 - a^2}{1 - 2a\cos\omega + a^2} > 0 ,
$$

which is $(1 + a)/(1 - a)$ at DC and $(1 - a)/(1 + a)$ at $\omega = \pi$. Uses:

- **Group-delay equalization.** Cascade all-pass sections after an IIR filter to flatten its group delay near the band edge, without touching its magnitude.
- **Fractional delay.** Choosing $a = (D - 1)/(D + 1)$ makes the DC group delay $(1 + a)/(1 - a)$ equal to $D$ samples, for any $D > 0$, and approximates a delay of $D$ at low frequencies: timing recovery and beam steering use this (Problem 16-02.10).
- **Decomposition.** Every rational causal stable $H(z)$ factors as $H(z) = H_{min}(z)\,H_{ap}(z)$: reflect each zero outside the circle to its mirror image (scaling by $\lvert z_0\rvert$) to form $H_{min}$, and collect the reflected pairs in $H_{ap}$. Then $\lvert H\rvert = \lvert H_{min}\rvert$ and $\tau_H = \tau_{min} + \tau_{ap} \ge \tau_{min}$: the magnitude is all in the minimum-phase part, the excess delay all in the all-pass part (Example 16-02.4).

### 3.7 Inverse systems and equalization

An **equalizer** undoes a channel: a cable, a circuit-board trace, a room's acoustics. If the channel is $C(z)$, the ideal equalizer is $E(z) = 1/C(z)$, whose poles are the channel's zeros. Three cases:

- **Zeros inside the circle (minimum phase):** $1/C$ is causal and stable. A two-tap channel $1 + cz^{-1}$ with $\lvert c\rvert < 1$ is inverted exactly by the recursion $1/(1 + cz^{-1})$, or approximately by an FIR filter holding its first few terms $(-c)^n$.
- **Zeros outside the circle:** the causal inverse is unstable. The stable inverse exists but is **anticausal**: its impulse response runs backwards in time and needs *future* inputs. A real equalizer truncates it to $K$ taps and delays the result by $K$ samples to make it causal. The delay is the price, and the truncation leaves a residual (Example 16-02.5). These future-looking taps are the **precursor taps** of a link equalizer, which cancel the energy that arrives *before* the main pulse.
- **Zeros on the circle:** the channel has destroyed those frequencies, and no stable inverse exists. Near such a zero an equalizer must apply huge gain, which amplifies noise: **noise enhancement**, the reason link receivers combine a feed-forward equalizer with a decision-feedback equalizer instead of inverting the channel blindly (Course 17).

## 4. Worked examples

### Example 16-02.1 · Reading the response off the z-plane (tier A)

**Setup.** $H(z) = (1 + z^{-1})/(1 - 0.5z^{-1})$. Find its pole, zero and ROC for a causal system, and the magnitude and phase at $\omega = 0$, $\pi/2$ and $\pi$ by the geometric method.

**Solution.** Multiply by $z/z$: $H(z) = (z + 1)/(z - 0.5)$. Zero at $z = -1$, pole at $z = 0.5$; the causal ROC is $\lvert z\rvert > 0.5$, which contains the unit circle: stable.

- $\omega = 0$ ($z = 1$): distances 2 from the zero and 0.5 from the pole: $\lvert H\rvert = 2/0.5$ = **4**, phase 0.
- $\omega = \pi/2$ ($z = j$): $\lvert j + 1\rvert = \sqrt2$, $\lvert j - 0.5\rvert = \sqrt{1.25}$, so $\lvert H\rvert = \sqrt{2/1.25}$ = **1.265**. Angles: the zero vector $1 + j$ points at 45°; the pole vector $-0.5 + j$ at $180° - \arctan 2 = 116.57°$; $M - N = 0$. Phase $45° - 116.57°$ = **−71.6**°.
- $\omega = \pi$ ($z = -1$): the point sits on the zero: $\lvert H\rvert$ = **0**.

**Units check.** Gains are ratios; angles in degrees.

**Sanity check.** At DC the difference equation $y = 0.5y + 2x$ gives $y/x = 4$; at Nyquist, $1 + z^{-1}$ with $z^{-1} = -1$ is zero. Both match.

### Example 16-02.2 · A 50 Hz notch (tier B)

**Setup.** Remove 50 Hz hum from a sensor sampled at $f_s$ = 1 kHz with a second-order notch, pole radius $r$ = 0.98. Give the coefficients (scaled for unit DC gain), the −3 dB notch width, the gain at 10 Hz and at 60 Hz, and the time constant of the notch's transient. Repeat the width and time constant for $r$ = 0.9, and compare with 16-01's 20-point moving average.

**Solution.** $\omega_0 = 2\pi \times 50/1000 = 0.1\pi$, so $2\cos\omega_0$ = **1.9021**. Numerator $1 - 1.9021z^{-1} + z^{-2}$; denominator $1 - 2r\cos\omega_0z^{-1} + r^2z^{-2} = 1 - $ **1.8641** $z^{-1} +$ **0.9604** $z^{-2}$. At DC the unscaled gain is $(2 - 1.9021)/(1 - 1.8641 + 0.9604)$ = **1.0162**, so the numerator is multiplied by $g = 1/1.0162$.

- Width: $2(1 - r) = 0.04$ rad/sample, or $0.04 \times 1000/2\pi$ = 6.37 Hz by the rule; solving $\lvert H\rvert = 1/\sqrt2$ on both sides of the notch gives **6.38** Hz.
- Gain at 10 Hz: **0.9995** (the 20-point average gave 0.936). Gain at 60 Hz: **0.956**: a notch for 50 Hz does nothing useful at 60 Hz.
- Time constant: $-1/\ln 0.98$ = **49.5** samples = **49.5** ms. The notch needs a few time constants to reach full depth after the hum appears or changes frequency.
- With $r$ = 0.9: width **28.3** Hz, time constant **9.49** ms: about 5 times faster (5.2×) and 4.4 times wider.

**Units check.** $\Delta f = \Delta\omega\,f_s/2\pi$: (rad/sample)(samples/s)/(rad/cycle) = Hz.

**Sanity check.** Width × time constant: $0.04012 \times 49.50 = 1.986 \approx 2$, the §3.3 rule.

### Example 16-02.3 · A resonator's peak and Q (tier B)

**Setup.** A tone detector uses $H_{res}$ of §3.3 with $r$ = 0.99 and $\omega_0 = \pi/4$. Find the gain at $\omega_0$ from the geometry, then the actual peak, the −3 dB bandwidth and $Q$.

**Solution.** At $e^{j\pi/4}$: the near pole is **0.0100** away; the far pole $0.99e^{-j\pi/4}$ is $\lvert e^{j\pi/4} - 0.99e^{-j\pi/4}\rvert$ = **1.4072** away; the zeros at $+1$ and $-1$ are $2\sin(\pi/8)$ = 0.7654 and $2\cos(\pi/8)$ = 1.8478 away, product $2\sin(\pi/4) = 1.4142$. So $\lvert H(e^{j\omega_0})\rvert = 1.4142/(0.0100 \times 1.4072)$ = **100.5**. A fine search finds the same peak, **100.5**, at $\omega$ = 0.7854, which is $\omega_0$ to four digits. The bandwidth found by solving for the half-power points is **0.0201** rad/sample (the rule gives 0.02), so $Q = \omega_0/\Delta\omega$ = **39.1** (the rule gives 39.3).

**Units check.** Gains and $Q$ are dimensionless.

**Sanity check.** The far pole and the zeros nearly cancel ($1.4142/1.4072 \approx 1.005$), so the peak is about $1/(1 - r) = 100$, as §3.3 predicts.

### Example 16-02.4 · Minimum phase, maximum phase and the all-pass between them (tier B)

**Setup.** Compare $h_{min} = (1, -0.5)$ and $h_{max} = (-0.5, 1)$. (a) Show they have the same magnitude response. (b) Find the fraction of energy each delivers in its first sample, and their group delays at DC and at $\pi$. (c) Write $H_{max} = H_{min}\,H_{ap}$ and check the group delays add.

**Solution.** (a) $H_{min} = 1 - 0.5z^{-1}$ has its zero at 0.5; $H_{max} = -0.5 + z^{-1} = -0.5(1 - 2z^{-1})$ has its zero at 2 = 1/0.5, the reflection, with the gain scaled by $\lvert 2\rvert \times 0.5 = 1$. By §3.5 the magnitudes are equal: at DC both are **0.5**, at $\pi$ both **1.5**.

(b) Total energy $1 + 0.25 = 1.25$ for both. First-sample fractions: $1/1.25$ = **0.8** for $h_{min}$ and $0.25/1.25$ = **0.2** for $h_{max}$. Group delays from §3.4 with $\rho$ = 0.5, $\theta = 0$: for $h_{min}$, $\tau(0) = (0.25 - 0.5)/(1 - 1 + 0.25)$ = **−1** sample and $\tau(\pi) = (0.25 + 0.5)/(2.25)$ = **0.333**. For $h_{max} = -0.5 + z^{-1}$ (one sample of delay plus the factor $1 - 0.5e^{j\omega}$), $\tau(0)$ = **2** and $\tau(\pi)$ = **0.667**.

(c) $H_{ap} = H_{max}/H_{min} = (z^{-1} - 0.5)/(1 - 0.5z^{-1})$, the §3.6 all-pass with $a$ = 0.5. Its group delay is $(1 + a)/(1 - a)$ = **3** at DC and $(1 - a)/(1 + a)$ = **0.333** at $\pi$. Check: $-1 + 3 = 2$ and $0.333 + 0.333 = 0.667$.

**Units check.** Group delay in samples.

**Sanity check.** A negative group delay at DC does not violate causality: it describes how a slowly varying envelope is shaped (the minimum-phase filter here is a mild differentiator, which "predicts" a smooth envelope), not a response before the input.

### Example 16-02.5 · Equalizing a channel that is not minimum phase (tier C)

**Setup.** A short link has the sampled pulse response $c = (0.8, 1)$: a precursor of 0.8 one symbol before the main cursor 1. (a) Where is its zero, and why is $1/C(z)$ not usable as a causal equalizer? (b) Design a $K$-tap FIR equalizer from the stable (anticausal) inverse, delayed by $K$ samples, and find the residual intersymbol interference (ISI) for $K$ = 5, 10 and 20. (c) How many taps keep the residual below 1%, and what latency does that cost? (d) Compare with the mirror channel $(1, 0.8)$.

**Solution.** (a) $C(z) = 0.8 + z^{-1} = 0.8(1 + 1.25z^{-1})$: a zero at $z$ = **−1.25**, outside the circle. The causal inverse has a pole at −1.25: unstable.

(b) Write $C(z) = z^{-1}(1 + 0.8z)$, so the stable inverse is $z/(1 + 0.8z) = z\sum_{k\ge0}(-0.8z)^k$, a series in positive powers of $z$: it uses future samples. Keep $K$ terms and delay by $K$ samples. Since $(1 + 0.8z)\sum_{k=0}^{K-1}(-0.8z)^k = 1 - (-0.8z)^K$ (a telescoping geometric sum), the channel and equalizer together give

$$
C(z)E(z) = z^{-K} - (-0.8)^K ,
$$

a main tap of 1 delayed by $K$ plus one leftover tap of size $0.8^K$ at time 0. Residual ISI: $0.8^5$ = **0.328**, $0.8^{10}$ = **0.107**, $0.8^{20}$ = **0.0115**.

(c) $0.8^K < 0.01$ needs $K > \ln 0.01/\ln 0.8 = 20.6$, so $K$ = **21** taps. The equalized main tap arrives at delay $K$ = 21, against delay 1 for the channel's own main cursor, so the equalizer adds $K - 1$ = **20** symbols of latency: one per precursor tap beyond the first.

(d) The mirror channel $1 + 0.8z^{-1}$ is minimum phase. Its inverse $1/(1 + 0.8z^{-1})$ is a causal, stable recursion with no added latency; a truncated FIR version $\sum_{k=0}^{K-1}(-0.8)^kz^{-k}$ leaves the same residual $0.8^K$, but *after* the main tap and without delaying it. The magnitude responses of the two channels are identical; only the phase, the location of the zero, decides whether the equalizer must wait for the future.

**Units check.** Taps and residuals are dimensionless; latency in symbol periods.

**Sanity check.** For $K$ = 1, the equalizer is the single tap 1 (since $1/c_1 = 1$), and the output is the channel itself: residual 0.8, matching $0.8^1$, and no added latency ($K - 1 = 0$).

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 16-02.1a | gain at DC | 4 | — |
| Ex 16-02.1b | gain at π/2 | 1.265 | — |
| Ex 16-02.1c | phase at π/2 | −71.6 | ° |
| Ex 16-02.1d | gain at π | 0 | — |
| Ex 16-02.1e | angle of the pole vector at π/2 | 116.57 | ° |
| Ex 16-02.2a | 2 cos ω0 | 1.9021 | — |
| Ex 16-02.2b | a1 magnitude, r = 0.98 | 1.8641 | — |
| Ex 16-02.2c | a2, r = 0.98 | 0.9604 | — |
| Ex 16-02.2d | unscaled DC gain | 1.0162 | — |
| Ex 16-02.2e | rule-of-thumb width | 6.37 | Hz |
| Ex 16-02.2f | exact −3 dB width, r = 0.98 | 6.38 | Hz |
| Ex 16-02.2g | gain at 10 Hz | 0.9995 | — |
| Ex 16-02.2h | gain at 60 Hz | 0.956 | — |
| Ex 16-02.2i | time constant, r = 0.98 | 49.5 | samples |
| Ex 16-02.2j | exact −3 dB width, r = 0.9 | 28.3 | Hz |
| Ex 16-02.2k | time constant, r = 0.9 | 9.49 | ms |
| Ex 16-02.2l | width × time constant | 1.99 | rad |
| Ex 16-02.3a | distance to the near pole | 0.0100 | — |
| Ex 16-02.3b | distance to the far pole | 1.4072 | — |
| Ex 16-02.3c | gain at ω0 | 100.5 | — |
| Ex 16-02.3d | −3 dB bandwidth | 0.0201 | rad/sample |
| Ex 16-02.3e | Q | 39.1 | — |
| Ex 16-02.3f | rule-of-thumb Q | 39.3 | — |
| Ex 16-02.4a | first-sample energy fraction, minimum phase | 0.8 | — |
| Ex 16-02.4b | first-sample energy fraction, maximum phase | 0.2 | — |
| Ex 16-02.4c | group delay at DC, minimum phase | −1 | samples |
| Ex 16-02.4d | group delay at π, minimum phase | 0.333 | samples |
| Ex 16-02.4e | group delay at DC, maximum phase | 2 | samples |
| Ex 16-02.4f | group delay at π, maximum phase | 0.667 | samples |
| Ex 16-02.4g | all-pass group delay at DC | 3 | samples |
| Ex 16-02.4h | all-pass group delay at π | 0.333 | samples |
| Ex 16-02.4i | magnitude at DC | 0.5 | — |
| Ex 16-02.4j | magnitude at π | 1.5 | — |
| Ex 16-02.5a | channel zero | −1.25 | — |
| Ex 16-02.5b | residual ISI, K = 5 | 0.328 | — |
| Ex 16-02.5c | residual ISI, K = 10 | 0.107 | — |
| Ex 16-02.5d | residual ISI, K = 20 | 0.0115 | — |
| Ex 16-02.5e | taps for residual below 1% | 21 | — |
| Ex 16-02.5f | added latency | 20 | symbols |
| Txt 16-02.a | Q2 notch width | 25.5 | Hz |
| Txt 16-02.b | Q2 time constant | 99.5 | samples |
| Txt 16-02.c | Q2 time constant | 12.4 | ms |
| Txt 16-02.d | Q5 all-pass delay at DC | 4 | samples |
| Txt 16-02.e | resonator peak position in Example 16-02.3 | 0.7854 | rad/sample |
| Txt 16-02.f | time constant of the r = 0.995 notch at 1 kHz | 199.5 | ms |
| Txt 16-02.g | time constant of the r = 0.9 notch at 1 kHz | 9.49 | ms |

## 5. Simulate it

The lab, [labs/16-02-lab](../labs/16-02-lab/README.md), provides `pz.py`: frequency response from coefficients and from the geometric formula, zeros and poles, group delay in closed form and numerically, and builders for notches, resonators, DC blockers, all-pass sections, minimum-phase reflection and delayed inverses. You:

1. **Walk the unit circle:** compare the geometric and direct frequency responses for Example 16-02.1, and plot the distance vectors at a few frequencies.
2. **Notch the hum:** filter a 10 Hz signal with 50 Hz hum through notches with $r$ = 0.9, 0.98 and 0.995, and watch the trade between notch width and the transient when the hum switches on.
3. **Tune a resonator:** sweep $r$ and confirm the $Q \approx \omega_0/[2(1 - r)]$ rule.
4. **Minimum, linear and maximum phase:** compare the three FIR filters with zeros at 0.5 and 2 (Problem 16-02.9) by impulse response, partial energy and group delay.
5. **Equalize a link:** apply Example 16-02.5's equalizer for $K$ = 5, 10 and 21 to a random PAM-2 sequence through the channel $(0.8, 1)$ and count symbol errors after adding noise.

**Guided exercise (predict, then run).** **Before Part 2,** predict which notch removes the hum better one second after the hum starts, and which removes it better in the first 20 ms. (After a second all three are deep; in the first 20 ms the $r$ = 0.9 notch has largely settled, about two of its **9.49** ms time constants, while the $r$ = 0.995 notch has barely begun: its time constant is **199.5** ms.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Pole radius $r$ of a notch or resonator | Closer to 1: narrower notch, higher $Q$ | Longer transient ($\approx 1/(1 - r)$ samples); more sensitivity to coefficient quantization (16-10) | DSP or firmware engineer |
| Linear phase (symmetric FIR) | Constant group delay; no phase distortion | Delay of half the length; many more taps than an IIR filter | Algorithm architect |
| Minimum phase | Least delay for a given magnitude; causal stable inverse | Phase distortion (frequency-dependent delay) | Audio or control engineer |
| All-pass group-delay equalizer | Flat group delay with the IIR magnitude kept | Added average delay; extra sections | DSP architect |
| Equalizer precursor taps $K$ | Cancel precursor ISI from non-minimum-phase channels | $K$ taps of hardware and $K - 1$ symbols of added latency | SerDes architect |
| Inverting a channel near a null | Flat overall response | Noise enhancement near the null; prefer DFE or accept the null | Link or system architect |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Pole at radius $r$ near the circle | −3 dB width $\approx 2(1 - r)$ rad/sample; time constant $\approx 1/(1 - r)$ samples; width × time constant ≈ 2 | §3.3 |
| Resonator peak and $Q$ | Peak $\approx 1/(1 - r)$ with zeros at ±1; $Q \approx \omega_0/[2(1 - r)]$ | §3.3, Example 16-02.3 |
| Group delay of a pole at its own angle | $\rho/(1 - \rho)$ samples | §3.4 |
| First-order all-pass $(z^{-1} - a)/(1 - az^{-1})$ | Delay $(1 + a)/(1 - a)$ at DC, $(1 - a)/(1 + a)$ at $\pi$ | §3.6 |
| Symmetric FIR of length $N$ | Group delay $(N - 1)/2$ samples | §3.4 |
| Delayed FIR inverse of a precursor $\rho$ | Residual $\rho^K$ after $K$ taps and $K - 1$ symbols of added delay | §3.7, Example 16-02.5 |

## 8. Common mistakes

- **Reading the magnitude from the poles alone.** Zeros matter as much; a pole–zero pair close together cancels.
- **Forgetting the $e^{-j\omega(M-N)}$ term** when counting phase from vectors.
- **Confusing phase delay $-\phi/\omega$ with group delay $-d\phi/d\omega$.** They agree only for linear phase.
- **Treating negative group delay as a causality violation.** It describes envelope shaping, not time travel.
- **Assuming "stable" means "invertible".** A stable channel with a zero outside the circle has an unstable causal inverse.
- **Equating minimum phase with "no delay".** Minimum phase is the least delay for a given magnitude, not zero.
- **Designing a notch narrower than the hum's frequency drift.** Mains frequency varies; a notch only a fraction of a hertz wide can miss it (or take seconds to settle).
- **Putting poles too close to the circle in fixed point.** Coefficient rounding can move them outside (16-08, 16-10).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Link equalizers are FIR filters with precursor taps.** ADC-based receivers for 200 Gb/s-class links equalize the digitized signal with a feed-forward equalizer (FFE) of up to about 30 taps in Intel's published 224 Gb/s design, with an optional decision-feedback equalizer (R-235, from the paper's abstract) **[Established]**. Channel pulse responses are generally not minimum phase, so some FFE taps act on samples after the one being decided: the precursor taps of §3.7, paid for in latency **[Established; textbook]**.
- **Audio equalization offers both phases.** Professional audio tools commonly offer "linear-phase" and "minimum-phase" (or "zero-latency") equalizer modes: linear phase preserves waveshape but adds latency and pre-ringing before transients; minimum phase has the least latency but phase distortion. The choice is the §3.4–3.5 tradeoff made audible **[Established; textbook]**.
- **Notches in sensing.** Biopotential and industrial sensor front ends use second-order IIR notches at the mains frequency, often switchable between 50 and 60 Hz, because a notch costs five multiplies per sample and leaves the passband nearly flat, while a hum-nulling moving average, even computed recursively at two additions per sample (16-01), attenuates everything above about 20 Hz (Example 16-02.2) **[Established; textbook]**.

### Why it matters commercially

Phase and delay are where DSP products differentiate quietly. A SerDes vendor's equalizer architecture (how many precursor and postcursor taps, FFE versus DFE, at what power) is a large part of its power per bit and its reach on lossy channels. An earbud's noise-cancellation loop lives or dies by group delay, because every sample of latency limits how high in frequency the cancellation works. A hearing-aid or voice-processing algorithm that needs linear phase spends latency budget that a minimum-phase design keeps. Diligence on any of these should ask not only "what is the magnitude response" but "what is the delay, and where are the zeros".

### Marketing vs Reality

- **"Linear phase means better sound."** Linear phase removes phase distortion but adds latency and pre-ringing (a faint echo *before* a transient), which some listeners find worse. Whether phase distortion of a minimum-phase equalizer is audible depends on how much and where. Ask for blind listening data, not adjectives.
- **"Zero-latency filtering."** A causal filter with any frequency selectivity has some group delay; "zero latency" usually means minimum phase with a small delay at the frequencies that matter.
- **"Our equalizer recovers any channel."** Equalizers cannot restore frequencies a channel has nulled, and inverting deep losses enhances noise. Ask what the noise enhancement is and where decision-feedback takes over.
- **"Infinite notch depth."** A notch's null is exact only at one frequency. Real hum drifts, and coefficient quantization shifts the null's frequency (with $b_0 = b_2$ the zeros stay exactly on the circle, but at a slightly different angle): quote the depth over the specified mains-frequency range in the actual word length.

### Questions for engineering leaders

1. **"What is the group delay of this signal path, and how does it vary with frequency?"** *Strong:* gives a plot or a number per band, and says which blocks contribute. *Evasive:* gives only the magnitude response.
2. **"Is the channel minimum phase? How many precursor taps does the equalizer use, and why that number?"** *Strong:* relates precursor energy in measured pulse responses to tap count and latency. *Evasive:* "the DSP handles it".
3. **"Why linear phase here (or why not)?"** *Strong:* names the waveshape or latency requirement that decided it. *Evasive:* "linear phase is better".
4. **"How close to the unit circle are your poles, and what word length keeps them inside?"** *Strong:* gives pole radii and the coefficient width chosen with margin. *Evasive:* "we simulated it in floating point".
5. **"What is the settling time of the narrowest filter in the chain?"** *Strong:* relates it to pole radius and to the application's response-time requirement. *Evasive:* unaware that narrow filters ring.

## 10. Concept check

**Q1.** A causal filter has poles at $0.9e^{\pm j\pi/3}$ and zeros at $e^{\pm j2\pi/3}$. Is it stable? Where does its magnitude response peak and where is it zero?

<details><summary>Answer</summary>

Stable: both poles are inside the unit circle. It peaks near $\omega = \pi/3$ (the poles' angle) and is exactly zero at $\omega = 2\pi/3$, where the zeros sit on the circle.

</details>

**Q2.** Roughly how wide is the −3 dB band of a notch whose poles are at radius 0.99, at $f_s$ = 8 kHz? How long is its transient?

<details><summary>Answer</summary>

$\Delta f \approx (1 - r)f_s/\pi = 0.01 \times 8000/\pi$ = 25.5 Hz; time constant about $1/(1 - r) = 100$ samples (exactly 99.5), 12.4 ms.

</details>

**Q3.** Why does a symmetric FIR filter have linear phase?

<details><summary>Answer</summary>

Pairing coefficients $n$ and $N - 1 - n$ makes $H(e^{j\omega}) = e^{-j\omega(N-1)/2}$ times a real function of $\omega$, so the phase is a straight line of slope $-(N - 1)/2$ (apart from sign flips of the real factor).

</details>

**Q4.** Two causal stable FIR filters have the same magnitude response. One has all its zeros inside the unit circle. Name three ways in which it differs from the others.

<details><summary>Answer</summary>

It has the least group delay (and phase lag) at every frequency, its energy accumulates fastest (largest partial energy at every $n$), and its inverse is causal and stable.

</details>

**Q5.** What is the magnitude response of $(z^{-1} - 0.6)/(1 - 0.6z^{-1})$, and its group delay at DC?

<details><summary>Answer</summary>

Exactly 1 at every frequency (an all-pass). Group delay at DC: $(1 + 0.6)/(1 - 0.6)$ = 4 samples.

</details>

**Q6.** A channel has a zero at $z = -2$. Why must its equalizer add latency?

<details><summary>Answer</summary>

The zero is outside the unit circle, so the causal inverse has an unstable pole at −2. The stable inverse is anticausal (it needs future samples); making it causal requires truncating it and delaying it by the number of taps kept.

</details>

Practice: [Problems 16-02](../problems/16-02-problems.md) · [Solutions](../solutions/16-02-solutions.md)

## 11. Key terms

[System function](../../../reference/glossary.md#system-function) · [Region of convergence (ROC)](../../../reference/glossary.md#region-of-convergence-roc) · [Poles and zeros](../../../reference/glossary.md#poles-and-zeros) · [Group delay](../../../reference/glossary.md#group-delay) · [Linear phase](../../../reference/glossary.md#linear-phase) · [Notch filter](../../../reference/glossary.md#notch-filter) · [Digital resonator](../../../reference/glossary.md#digital-resonator) · [DC blocker](../../../reference/glossary.md#dc-blocker) · [Minimum-phase system](../../../reference/glossary.md#minimum-phase-system) · [All-pass filter](../../../reference/glossary.md#all-pass-filter) · [Feed-forward equalizer (FFE)](../../../reference/glossary.md#feed-forward-equalizer-ffe) · [Decision-feedback equalizer (DFE)](../../../reference/glossary.md#decision-feedback-equalizer-dfe) · [Precursor tap](../../../reference/glossary.md#precursor-tap) · [Noise enhancement](../../../reference/glossary.md#noise-enhancement)

## 12. Connections

- **Builds on:** [16-01](16-01-discrete-time-systems-review.md) (difference equations, stability, the moving average), [11-07 DTFT](../../11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md), [11-09 The z-Transform](../../11-signals-and-systems/chapters/11-09-z-transform.md) (ROC, partial fractions), [07-07 Frequency Response and Bode Plots](../../07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) (the s-plane version of the geometric view), [07-08 Filters and Resonance](../../07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) (Q and bandwidth).
- **Next:** [16-03 The DFT and Its Properties](16-03-the-dft.md) samples the DTFT so a computer can compute it.
- **Used later:** linear-phase FIR design in [16-06](16-06-fir-filter-design.md); IIR design and phase in [16-07](16-07-iir-filter-design.md); pole sensitivity in [16-08](16-08-filter-structures.md) and [16-10](16-10-quantization-and-fixed-point.md); equalization in Course 17.

## 13. Further study

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 5 (transform analysis of LTI systems: frequency response from poles and zeros, all-pass and minimum-phase systems, linear phase).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 6 (IIR filters, pole-zero placement) and ch. 13 (DSP tricks, including DC removal and notch filters).
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), lectures on transform analysis and minimum-phase systems.

## 14. Sources

1. A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Pearson, 2010, ch. 5 (§5.6 for the minimum-energy-delay property).
2. R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed., Prentice Hall, 2011.
3. Y. Segal, A. Laufer, A. Khairi et al., ISSCC 2022, doi:10.1109/ISSCC42614.2022.9731794, and its journal version, A. Khairi et al., "A 1.41-pJ/b 224-Gb/s PAM4 6-bit ADC-Based SerDes Receiver ...", IEEE JSSC, Jan 2023, doi:10.1109/JSSC.2022.3211475; abstracts. Research log [R-235].
