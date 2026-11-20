<!-- status: reviewed -->
# 15-07 · Frequency-Domain Design: Bode, Nyquist and Margins

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The frequency-response material of a first course in feedback control: Bode plots of the loop gain, the Nyquist stability criterion, gain and phase margins, their relation to damping and bandwidth, time delay, and sensitivity limits (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 6; Nise, *Control Systems Engineering*, ch. 10; Åström & Murray, *Feedback Systems*, ch. 9–11) |
| **Prerequisites** | [15-05 Stability and the Routh–Hurwitz Criterion](15-05-stability-routh-hurwitz.md), [15-06 Root Locus](15-06-root-locus.md), [07-07 Frequency Response and Bode Plots](../../07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Plot a loop gain's Bode diagram and read the crossover frequency, the phase margin and the gain margin.
2. State the Nyquist criterion, derive it from the argument principle, and apply it to loops with open-loop poles on the axis or in the right half-plane.
3. Relate phase margin to damping ratio and overshoot, and crossover frequency to closed-loop bandwidth.
4. Treat a time delay exactly and compute a loop's delay margin.
5. Explain the sensitivity peak and Bode's sensitivity integral, and use margins to judge an op-amp, a PLL and a regulator.

---

## 1. Big picture

The root locus and Routh need a model's poles and zeros. Many real loops come instead with a *measured* frequency response: a network analyzer sweeps a sine through the loop and records gain and phase. Frequency-domain design works directly with that data. It asks two questions about the loop gain $L(j\omega)$: at the frequency where the loop gain falls to 1 (the crossover), how far is the phase from −180°? And at the frequency where the phase reaches −180°, how far is the gain below 1? Those distances, the **phase margin** and the **gain margin**, measure how close the loop is to oscillating. They are the most widely quoted stability numbers in analog and power design. The Nyquist criterion makes the reasoning rigorous, handles time delays exactly (which Routh cannot), and leads to the deepest result in classical control: Bode's integral, which shows that feedback can only move sensitivity around, not remove it.

- **Op-amps are specified by phase margin**, typically 45° to 70° at unity gain, and are compensated to reach it (12-06).
- **Regulator and converter loops are tuned on a Bode plot** of measured loop gain, with crossover and margins as the specifications (22-07, 15-12).
- **PLL loop filters are designed for phase margin**, which sets peaking in the jitter transfer and the lock transient (15-12).
- **Delays are everywhere in digital control**: sampling, computation and communication. Their only effect is phase lag that grows with frequency, and the delay margin says how much a loop tolerates (15-11).

## 2. Intuition first

**Why −180° is the danger point.** In a negative-feedback loop, the controller subtracts the fed-back signal. A sinusoid that goes around the loop and comes back delayed by half a cycle (180°) has its sign flipped, so subtracting it *adds* it. If its amplitude has also not shrunk (loop gain at least 1), a sinusoid at that frequency can sustain itself without any input: the loop oscillates. Stability needs the loop gain to have fallen below 1 by the time the phase lag reaches 180°.

**Margins as safety buffers.** Phase margin is how much additional lag the loop could tolerate at crossover before it oscillates; gain margin is how much additional gain it could tolerate at the 180° frequency. They are like a bank's capital ratios: a buffer against things the model got wrong, such as an extra pole, a delay, or a component that drifts. The analogy breaks down because margins are not additive: a loop can have a large gain margin and a large phase margin and still be fragile, if its Nyquist plot passes close to −1 somewhere between the two frequencies. The sensitivity peak (§3.7) measures that distance directly.

**The Nyquist plot.** Draw $L(j\omega)$ as a curve in the complex plane as $\omega$ sweeps from $-\infty$ to $\infty$. The point −1 is where $1 + L = 0$, the closed loop's characteristic equation. How the curve winds around −1 tells you how many closed-loop poles are unstable (§3.3).

## 3. Theory

### 3.1 The loop gain's frequency response

For a loop with loop gain $L(s)$, evaluate $L(j\omega)$ as in 07-07: magnitude in decibels, $20\log_{10}\lvert L\rvert$, and phase in degrees, against $\log\omega$. Each factor contributes independently:

- an integrator $1/s$: −20 dB/decade, −90°;
- a pole $1/(1 + s/p)$: flat, then −20 dB/decade above $p$; phase from 0° to −90°, −45° at $p$;
- a zero $(1 + s/z)$: +20 dB/decade above $z$; phase 0° to +90°;
- a right-half-plane zero $(1 - s/z)$: the same magnitude as a left-half-plane zero, but phase from 0° to **−90°**;
- a delay $e^{-sT}$: magnitude 1 (0 dB) at all frequencies; phase $-\omega T$ radians, growing without bound.

The **gain crossover frequency** $\omega_c$ is where $\lvert L(j\omega_c)\rvert = 1$ (0 dB). The **phase crossover frequency** $\omega_{180}$ is where $\angle L(j\omega_{180}) = -180°$.

### 3.2 Gain margin, phase margin and delay margin

$$
\text{PM} = 180° + \angle L(j\omega_c), \qquad \text{GM} = \frac{1}{\lvert L(j\omega_{180})\rvert}\ \ (\text{or }-20\log_{10}\lvert L(j\omega_{180})\rvert\text{ dB}) .
$$

For the common case of a stable open loop whose magnitude falls through 0 dB once and whose phase falls through −180° once, the closed loop is stable when both margins are positive (PM > 0°, GM > 1, that is, above 0 dB). A pure delay $T$ adds phase $-\omega T$ without changing the magnitude, so the loop tolerates an additional delay up to the **delay margin**

$$
T_{dm} = \frac{\text{PM (in radians)}}{\omega_c} .
$$

Loops with an unstable open loop, several crossovers, or conditionally stable gain ranges need the full Nyquist criterion.

### 3.3 The Nyquist criterion

> **Math refresher — the argument principle.** Let $F(s)$ be a rational function and $C$ a closed contour, traversed clockwise, that passes through no pole or zero of $F$. As $s$ goes once around $C$, the image $F(s)$ winds clockwise around the origin $N = Z - P$ times, where $Z$ and $P$ are the numbers of zeros and poles of $F$ inside $C$. Reason: $F(s) = K\prod(s - z_i)/\prod(s - p_j)$, so $\angle F = \sum\angle(s - z_i) - \sum\angle(s - p_j)$. A factor whose root is inside $C$ turns through a full −360° (clockwise) as $s$ goes around; a factor whose root is outside returns to its starting angle.

Apply it to $F(s) = 1 + L(s)$, with $C$ the **Nyquist contour**: up the imaginary axis from $-jR$ to $+jR$ and back around a semicircle of radius $R \to \infty$ in the right half-plane, enclosing the whole right half-plane, with small detours (indentations) to the right of any poles of $L$ on the imaginary axis.

- The zeros of $1 + L$ are the closed-loop poles; $Z$ counts the unstable ones.
- The poles of $1 + L$ are the poles of $L$; $P$ counts the open-loop poles in the right half-plane.
- The image of $C$ under $1 + L$ winding around the origin is the same as the image under $L$ winding around **−1**.

> **Nyquist criterion.** Let $N$ be the number of clockwise encirclements of −1 by the Nyquist plot of $L(s)$ (the image of the Nyquist contour). Then the number of unstable closed-loop poles is
>
> $$Z = N + P .$$
>
> The closed loop is stable if and only if $N = -P$: the plot encircles −1 counterclockwise exactly as many times as $L$ has open-loop poles in the right half-plane. For an open-loop stable $L$ ($P$ = 0), the plot must not encircle −1 at all.

For a strictly proper $L$ the large semicircle maps to the origin, so the plot is just $L(j\omega)$ for $\omega$ from $-\infty$ to $\infty$, and the negative frequencies are the mirror image of the positive ones. An integrator ($1/s$) maps the small indentation around the origin to a large semicircle swinging clockwise through 180° per integrator, closing the plot.

![Two panels. Left: Bode plot of the loop gain 8.30/[s(s+2)(s+4)] from 0.01 to 100 rad/s. The magnitude falls at 20 dB per decade at low frequency, crosses 0 dB near 0.92 rad/s and falls faster above; at 2.83 rad/s, where the phase is -180 degrees, it is 15.2 dB below 0 dB, marked as the gain margin. The phase starts at -90 degrees and falls toward -270 degrees; at the 0 dB crossover it is 52.4 degrees above -180 degrees, marked as the phase margin. Right: Nyquist plots near the point -1 of K(s+1)/[s(s-1)(s+6)] for K = 10 and K = 5, positive frequencies solid and negative frequencies dashed. The K = 10 curve crosses the negative real axis at -1.33, to the left of -1, and loops around -1 once counterclockwise; the K = 5 curve crosses at -0.67, to the right of -1, and the encirclement reverses.](../../../assets/figures/15-07/margins.svg)

*Figure 1. Left: gain and phase margins read from a Bode plot (Example 15-07.2). Right: the Nyquist criterion with an unstable plant (Example 15-07.5). With one open-loop pole in the right half-plane, stability needs one counterclockwise encirclement of −1, which happens only when the real-axis crossing at $-K/7.5$ lies left of −1.*

### 3.4 Phase margin and damping

For the standard loop $L(s) = \omega_n^2/[s(s + 2\zeta\omega_n)]$, whose closed loop is the standard second-order system (15-03), the margins can be computed exactly. Setting $\lvert L(j\omega_c)\rvert = 1$:

$$
\omega_c^2(\omega_c^2 + 4\zeta^2\omega_n^2) = \omega_n^4 \;\Rightarrow\; \frac{\omega_c}{\omega_n} = \sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2} .
$$

The phase is $-90° - \arctan(\omega_c/2\zeta\omega_n)$, so

$$
\text{PM} = 90° - \arctan\frac{\omega_c}{2\zeta\omega_n} = \arctan\frac{2\zeta}{\sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2}} .
$$

For $\zeta$ up to about 0.7, $\text{PM} \approx 100\zeta$ degrees. So a phase margin of 45° corresponds to $\zeta \approx$ **0.42** (about **23**% overshoot), 60° to $\zeta \approx$ **0.61** (about **9**%), and 65.5° to $\zeta$ = 0.707 (4.3%). The gain margin of this loop is infinite: its phase never reaches −180°.

The **closed-loop bandwidth** is related to crossover: for this loop it lies between $\omega_c$ and $2\omega_c$ (1.62$\omega_c$ at $\zeta$ = 0.5, Example 15-07.1). So crossover sets speed: rise time roughly $1.8/\omega_n$, with $\omega_n$ a little above $\omega_c$.

### 3.5 Time delay

A delay $T$ multiplies $L$ by $e^{-sT}$: unity magnitude, phase $-\omega T$. It moves no poles of $L$ but shifts every point of the Nyquist plot clockwise by $\omega T$ radians. The phase margin falls by $\omega_cT$ (in radians), and the loop goes unstable when $T$ exceeds the delay margin. Unlike Routh, the frequency domain handles the delay exactly, with no Padé approximation (15-05 §3.7).

### 3.6 The minimum-phase connection

For a **minimum-phase** loop (no right-half-plane poles or zeros, no delay), Bode showed that the phase is fixed by the magnitude curve: a slope of $-20n$ dB/decade held over a wide range implies a phase near $-90n°$. That is why a good crossover has a slope near −20 dB/decade (phase near −90°, margin near 90° minus the extra lags) and why crossing at −40 dB/decade leaves almost no margin. Right-half-plane zeros and delays add phase lag without changing the magnitude, so they limit the achievable crossover frequency.

### 3.7 Sensitivity peak and Bode's integral

The distance from a point $L(j\omega)$ to −1 is $\lvert 1 + L(j\omega)\rvert = 1/\lvert S(j\omega)\rvert$. The **sensitivity peak**

$$
M_s = \max_\omega\lvert S(j\omega)\rvert = \frac{1}{\min_\omega\lvert 1 + L(j\omega)\rvert}
$$

is the reciprocal of the closest approach of the Nyquist plot to −1: a single robust margin. $M_s$ of 1.3 to 2 is a common design target. It guarantees $\text{GM} \ge M_s/(M_s - 1)$ and $\text{PM} \ge 2\arcsin[1/(2M_s)]$.

Feedback reduces $\lvert S\rvert$ where the loop gain is large, but it cannot do so everywhere:

> **Bode's sensitivity integral.** If $L(s)$ has relative degree at least 2 and the closed loop is stable, then
>
> $$\int_0^\infty\ln\lvert S(j\omega)\rvert\,d\omega = \pi\sum_k\mathrm{Re}(p_k) ,$$
>
> where the $p_k$ are the open-loop poles in the right half-plane (the sum is zero for a stable open loop).

The area of sensitivity reduction ($\ln\lvert S\rvert < 0$) is balanced by an equal area of amplification ($\ln\lvert S\rvert > 0$), the "waterbed effect". An unstable plant makes things worse: the net area is positive. This is a conservation law of feedback. Disturbance rejection at low frequency is paid for by disturbance amplification near crossover.

> **Going deeper — where the integral comes from.** $\ln S(s)$ is analytic in the right half-plane (for a stable closed loop) except where $S$ has zeros, at the open-loop right-half-plane poles. Integrating $\ln S$ around the Nyquist contour and using Cauchy's theorem, the large semicircle contributes a term set by the relative degree (zero for degree ≥ 2), and each right-half-plane zero of $S$ contributes $\pi\,\mathrm{Re}(p_k)$ (Freudenberg and Looze, 1985; Åström and Murray, ch. 11). The lab checks the result numerically for Examples 15-07.2 and 15-07.5.

### 3.8 Chip loops in the frequency domain

- **Op-amps.** With feedback factor $\beta$, the loop gain is $\beta A(s)$. A two-pole amplifier with dominant pole $p_1$ and second pole $p_2$ crosses over at a frequency $f_c$ a little below $\beta\cdot\text{GBW}$, with phase margin $90° - \arctan(f_c/f_2)$, all in hertz (the first pole, far below crossover, contributes its full 90°). Using the estimate $f_c \approx \beta\cdot\text{GBW}$ in the arctangent is slightly pessimistic, because the second pole pulls the true crossover down: at unity gain it gives 63.4°, 76.0° and 45.0° for $f_2$ = 2, 4 and 1 × GBW, against exact margins of 65.5°, 76.3° and 51.8°. Unity gain ($\beta$ = 1) is the hardest case, which is why amplifiers are specified "unity-gain stable" or, if decompensated, stable above a minimum gain (Problem 15-06.11).
- **PLLs.** For the third-order loop $K(1 + s\tau_z)/[s^2(1 + s\tau_p)]$, the phase is $-180° + \arctan(\omega\tau_z) - \arctan(\omega\tau_p)$, so the phase margin peaks at $\omega = 1/\sqrt{\tau_z\tau_p}$, with value $\arctan[(b - 1)/(2\sqrt b)]$ for $b = \tau_z/\tau_p$. Placing crossover there maximizes the margin (Problem 15-07.11).
- **Regulators.** An LDO's two low-frequency poles leave little phase at crossover (15-02, 15-05); compensation places a dominant pole or uses the output capacitor's ESR zero to restore it (15-12).

## 4. Worked examples

### Example 15-07.1 · Margins of a servo loop (tier A)

**Setup.** $L(s) = 100/[s(s + 10)]$. Find the crossover, phase margin, gain margin, the closed-loop damping and the closed-loop bandwidth.

**Solution.** $\lvert L(j\omega)\rvert = 1$ means $\omega^2(\omega^2 + 100) = 10^4$, a quadratic in $\omega^2$: $\omega^2 = (-100 + \sqrt{10^4 + 4 \times 10^4})/2 = 61.8$, so $\omega_c$ = **7.86** rad/s. The phase there is $-90° - \arctan(0.786) = -128.2°$, so PM = **51.8**°. The phase approaches −180° only as $\omega \to \infty$, so the gain margin is infinite. The closed loop is $100/(s^2 + 10s + 100)$, with $\zeta$ = **0.5**: the §3.4 formula for $\zeta$ = 0.5 gives exactly 51.8°. The closed-loop −3 dB bandwidth is **12.72** rad/s, 1.62 times the crossover.

**Units check.** $L$ is dimensionless; $\omega$ in rad/s.

**Sanity check.** The rule PM ≈ 100ζ gives 50°, close to 51.8°.

### Example 15-07.2 · Margins of a three-pole loop (tier B)

**Setup.** The three-pole loop of 15-06, $L = K/[s(s + 2)(s + 4)]$, at the gain $K$ = 8.30 chosen there for $\zeta$ = 0.5. Find both margins and the sensitivity peak, and compare with Routh.

**Solution.** The phase is $-90° - \arctan(\omega/2) - \arctan(\omega/4)$; it reaches −180° when $\arctan(\omega/2) + \arctan(\omega/4) = 90°$, that is $\omega^2 = 8$: $\omega_{180}$ = **2.828** rad/s, where $\lvert L\rvert = K/48$. So GM = 48/8.30 = **5.79**, or **15.2** dB. Solving $\lvert L\rvert = 1$ numerically gives $\omega_c$ = **0.919** rad/s and PM = **52.4**°. The closest approach of the Nyquist plot to −1 gives $M_s$ = **1.59**.

**Units check.** As above.

**Sanity check.** The gain margin says $K$ could rise by 5.79 times to 48, exactly Routh's limit from 15-05. A PM of 52° predicts $\zeta \approx 0.5$, and 15-06 measured 15.5% overshoot, close to the 16.3% of $\zeta$ = 0.5.

### Example 15-07.3 · Phase margin against damping (tier B)

**Setup.** Tabulate the exact phase margin and the normalized crossover $\omega_c/\omega_n$ of the standard loop for $\zeta$ = 0.3, 0.5 and 0.7, and compare with PM ≈ 100ζ.

**Solution.** From §3.4:

| $\zeta$ | $\omega_c/\omega_n$ | PM (exact) | 100ζ |
|---|---|---|---|
| 0.3 | **0.914** | **33.3**° | 30° |
| 0.5 | **0.786** | **51.8**° | 50° |
| 0.7 | **0.648** | **65.2**° | 70° |

The rule is within 5° up to $\zeta$ = 0.7.

**Units check.** Ratios and degrees.

**Sanity check.** More damping lowers the crossover relative to $\omega_n$: the loop gain falls through 1 earlier, where the second pole has added less lag.

### Example 15-07.4 · A loop with a delay (tier B)

**Setup.** $L(s) = Ke^{-sT}/s$ with $T$ = 1 s and $K$ = 0.5 s⁻¹. Find the crossover, phase margin, gain margin and delay margin, and the largest stable $K$.

**Solution.** $\lvert L\rvert = K/\omega$, so $\omega_c = K$ = **0.5** rad/s. The phase is $-90° - \omega T$ (in degrees, $-90° - 57.3\omega T$), so at crossover it is $-90° - 28.65° = -118.65°$ and PM = **61.4**°. The phase reaches −180° when $\omega T = \pi/2$: $\omega_{180}$ = **1.571** rad/s, where $\lvert L\rvert = 0.5/1.571$, so GM = **3.14** (**9.94** dB). The largest stable gain is therefore $\pi/2$ = 1.571, the exact limit quoted in 15-05. The delay margin is $1.0708\ \text{rad}/0.5\ \text{rad/s}$ = **2.14** s: the loop tolerates 2.14 s of extra delay.

**Units check.** PM in radians divided by rad/s gives seconds.

**Sanity check.** 15-05's Padé approximation gave a limit of 2, 27% too optimistic; the frequency-domain answer is exact.

### Example 15-07.5 · Nyquist with an unstable plant (tier C)

**Setup.** 15-05's loop $L = K(s + 1)/[s(s - 1)(s + 6)]$ has one open-loop pole in the right half-plane. Use the Nyquist criterion to decide stability at $K$ = 10 and $K$ = 5, and interpret the margins at $K$ = 10.

**Solution.** $P$ = 1, so stability needs one counterclockwise encirclement of −1 ($N$ = −1). First find where the plot goes. With $s = j\omega$ the denominator is $j\omega(j\omega - 1)(j\omega + 6) = -5\omega^2 - j\omega(\omega^2 + 6)$. Multiplying the numerator and denominator by its conjugate,

$$
L(j\omega) = K\,\frac{-(\omega^4 + 11\omega^2) + j\omega(6 - 4\omega^2)}{\omega^2\left[25\omega^2 + (\omega^2 + 6)^2\right]}
$$

so $\mathrm{Re}\,L = -K(\omega^2 + 11)/[25\omega^2 + (\omega^2 + 6)^2]$ is negative at every frequency, and $\mathrm{Im}\,L = K(6 - 4\omega^2)/\{\omega[25\omega^2 + (\omega^2 + 6)^2]\}$ changes sign only at $\omega^2 = 3/2$.

- **$\omega \to 0^+$:** $\mathrm{Re}\,L \to -11K/36$ and $\mathrm{Im}\,L \to +\infty$ (the integrator): the plot starts at the top of the plane, left of −1.
- **The crossing:** at $\omega = \sqrt{3/2}$ = **1.225** rad/s, $L = -K(25/2)/(75/2 + 225/4) = -K/7.5$. Below this frequency $\mathrm{Im}\,L > 0$; above it, $\mathrm{Im}\,L < 0$.
- **$\omega \to \infty$:** $L \approx -K/\omega^2$, so the plot reaches the origin from the left (relative degree 2).
- **Negative frequencies** give the mirror image in the real axis, traversed from the origin back to $-j\infty$.
- **The indentation** $s = \varepsilon e^{j\theta}$, $\theta$ from −90° to +90°, around the pole at the origin: there $L \approx K/[s(-1)(6)] = -(K/6\varepsilon)e^{-j\theta}$, an arc of infinite radius from $-j\infty$ through $-\infty$ to $+j\infty$, clockwise.

The curve therefore has two parts (sketch below, not to scale): a small lobe between $-K/7.5$ and the origin, traversed counterclockwise (out along the lower arc, back along the upper), and a large region to the left of $-K/7.5$, closed by the indentation arc and traversed clockwise. To count encirclements without drawing, use the crossings of the real axis to the left of −1: a clockwise loop around −1 crosses there going upward, so $N$ = (upward crossings) − (downward crossings). Both branches cross at $-K/7.5$ going downward (from $\mathrm{Im}\,L > 0$ to $< 0$), and the indentation arc crosses at $-\infty$ going upward.

```text
                      Im L
  ω → 0+               ^
     |                 |
     v                 |
      \     .---<---.  |      upper arc: ω < 0 (mirror image), traversed leftward
       \   /         \ |
  ------*------x------\o------> Re L
       /   \         / |
      /     '--->---'  |      lower arc: ω > 0, traversed rightward
     v                 |
     |                 |
  ω → 0−               |

  * = −K/7.5, crossed by both branches    x = −1 (here K = 10)    o = origin (ω → ±∞)
  The indentation closes the curve far to the left: −j∞ → −∞ → +j∞, clockwise.
```

- $K$ = 10: the crossing is at −1.333, to the left of −1, so all three crossings count: $N = 1 - 2 = -1$. The point −1 sits inside the counterclockwise lobe, $Z = N + P$ = **0**, stable.
- $K$ = 5: the crossing is at −0.667, to the right of −1, so only the arc counts: $N = +1$. The point −1 now sits in the clockwise region, and $Z$ = **2**: two unstable poles.

Stability needs $K/7.5 > 1$, the condition that puts −1 inside the lobe.

At $K$ = 10, the "gain margin" is the factor by which the gain may *fall*: 1/1.333 = **0.75** (−2.50 dB), matching Routh's lower limit $K$ > 7.5. The phase margin at $\omega_c$ = 1.61 rad/s is only **11.3**°. Both margins are small: an open-loop unstable plant is hard to stabilize robustly. Bode's integral confirms the cost: numerically, $\int_0^\infty\ln\lvert S\rvert\,d\omega$ = **3.142** = $\pi \times 1$, the open-loop pole's real part times π.

**Units check.** $\omega$ in rad/s; the integral has units of rad/s.

**Sanity check.** The closed-loop roots at $K$ = 10 are −4.60 and $-0.199 \pm j1.46$ (stable); at $K$ = 5 they include $0.180 \pm j0.949$ (unstable), as Nyquist said.

### Example 15-07.6 · An op-amp's phase margin, measured by injection (tier C)

**Setup.** An op-amp has $A(s) = A_0/[(1 + s/p_1)(1 + s/p_2)]$ with $A_0 = 10^5$, $f_1$ = 100 Hz (gain-bandwidth 10 MHz) and $f_2$ = 20 MHz. Find the crossover and phase margin in a unity-gain buffer ($\beta$ = 1) and at a gain of 2 ($\beta$ = 0.5), the buffer's step overshoot, and show how to measure the loop gain without opening the loop.

**Solution.** With $\beta$ = 1, solving $\lvert A(j\omega)\rvert = 1$ gives $f_c$ = **9.10** MHz, a little below the 10 MHz GBW because the second pole has begun to cut the gain. The phase is $-\arctan(f_c/f_1) - \arctan(f_c/f_2) = -89.99° - 24.47°$, so PM = **65.5**°. Indeed the closed loop's damping is $\zeta = (p_1 + p_2)/[2\sqrt{(1 + A_0)p_1p_2}]$ = 0.707, and its step overshoot is **4.32**%. With $\beta$ = 0.5, crossover falls to **4.86** MHz and PM rises to **76.3**°.

**Measuring it.** Insert a small AC voltage source in series in the feedback path, between the amplifier output (node $x$) and the inverting input (node $y$). The loop stays closed and biased; the source injects a test signal. Since $v_x = -A v_y$, the loop gain is $L = -v_x/v_y$ (for the buffer, $L = \beta A$ with $\beta$ = 1). The lab runs this in ngspice (`opamp_loop.cir`): an AC sweep of $-v(x)/v(y)$ gives 9.10 MHz and 65.5°, matching the calculation. This is Middlebrook's injection method (15-02 §9); it is accurate when the injection point has a low-impedance source on one side and a high-impedance load on the other, as here.

**Units check.** Frequencies in Hz (divide rad/s by 2π).

**Sanity check.** The rule PM = 90° − arctan($f_c/f_2$) = 90° − 24.5° = 65.5° holds here because the first pole is far below crossover and contributes its full 90°. With the quick estimate $f_c \approx$ GBW = 10 MHz in the arctangent it gives **63.4**°, a slightly pessimistic answer, because the second pole pulls the true crossover down to 9.10 MHz.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Txt 15-07.a | ζ for 45° phase margin | 0.42 | — |
| Txt 15-07.b | overshoot for 45° | 23 | % |
| Txt 15-07.c | ζ for 60° phase margin | 0.61 | — |
| Txt 15-07.d | overshoot for 60° | 9 | % |
| Txt 15-07.e | op-amp PM with f2 = 4 GBW | 76.3 | ° |
| Txt 15-07.f | op-amp PM with f2 = GBW | 51.8 | ° |
| Txt 15-07.g | estimated PM with fc ≈ GBW, f2 = 2 GBW | 63.4 | ° |
| Txt 15-07.h | estimated PM with fc ≈ GBW, f2 = 4 GBW | 76.0 | ° |
| Txt 15-07.i | estimated PM with fc ≈ GBW, f2 = GBW | 45.0 | ° |
| Ex 15-07.1a | crossover | 7.86 | rad/s |
| Ex 15-07.1b | phase margin | 51.8 | ° |
| Ex 15-07.1c | closed-loop ζ | 0.5 | — |
| Ex 15-07.1d | closed-loop bandwidth | 12.72 | rad/s |
| Ex 15-07.2a | phase crossover | 2.828 | rad/s |
| Ex 15-07.2b | gain margin | 5.79 | — |
| Ex 15-07.2c | gain margin | 15.2 | dB |
| Ex 15-07.2d | crossover | 0.919 | rad/s |
| Ex 15-07.2e | phase margin | 52.4 | ° |
| Ex 15-07.2f | sensitivity peak | 1.59 | — |
| Ex 15-07.3a | ωc/ωn at ζ = 0.3 | 0.914 | — |
| Ex 15-07.3b | PM at ζ = 0.3 | 33.3 | ° |
| Ex 15-07.3c | ωc/ωn at ζ = 0.5 | 0.786 | — |
| Ex 15-07.3d | PM at ζ = 0.5 | 51.8 | ° |
| Ex 15-07.3e | ωc/ωn at ζ = 0.7 | 0.648 | — |
| Ex 15-07.3f | PM at ζ = 0.7 | 65.2 | ° |
| Ex 15-07.4a | crossover | 0.5 | rad/s |
| Ex 15-07.4b | phase margin | 61.4 | ° |
| Ex 15-07.4c | phase crossover | 1.571 | rad/s |
| Ex 15-07.4d | gain margin | 3.14 | — |
| Ex 15-07.4e | gain margin | 9.94 | dB |
| Ex 15-07.4f | delay margin | 2.14 | s |
| Ex 15-07.5a | negative-real-axis crossing | 1.225 | rad/s |
| Ex 15-07.5b | unstable poles at K = 10 | 0 | — |
| Ex 15-07.5c | unstable poles at K = 5 | 2 | — |
| Ex 15-07.5d | gain-reduction margin | 0.75 | — |
| Ex 15-07.5e | gain-reduction margin | −2.50 | dB |
| Ex 15-07.5f | phase margin | 11.3 | ° |
| Ex 15-07.5g | Bode integral | 3.142 | rad/s |
| Ex 15-07.6a | crossover, β = 1 | 9.10 | MHz |
| Ex 15-07.6b | phase margin, β = 1 | 65.5 | ° |
| Ex 15-07.6c | buffer overshoot | 4.32 | % |
| Ex 15-07.6d | crossover, β = 0.5 | 4.86 | MHz |
| Ex 15-07.6e | phase margin, β = 0.5 | 76.3 | ° |

## 5. Simulate it

The lab, [labs/15-07-lab](../labs/15-07-lab/README.md), provides `freqdomain.py`: frequency responses with delay, margins found by root finding on a continuous phase, Nyquist encirclement counting along an indented contour, the sensitivity peak and a numerical Bode integral. You:

1. **Plot Bode and Nyquist diagrams** for Examples 15-07.1, 15-07.2 and 15-07.4, and mark the margins.
2. **Count encirclements** for Example 15-07.5 at several gains and compare $Z = N + P$ with the closed-loop roots.
3. **Check Bode's integral** numerically for a stable and an unstable open loop, and watch the waterbed: raise the gain and see the sensitivity rise near crossover.
4. **Measure an op-amp's loop gain by injection** in ngspice (`opamp_loop.cir`), and change $f_2$ to see the phase margin move.

**Guided exercise (predict, then run).** **Before Part 4,** predict the phase margin if the op-amp's second pole moves from 20 MHz down to 10 MHz. (About 52°: crossover falls to about 7.9 MHz and the second pole adds about 38° of lag; the exact value is **51.8**°, the same as $\zeta$ = 0.5, because $f_2$ = GBW makes the closed loop's damping exactly 0.5.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Higher crossover frequency | Speed, disturbance rejection over a wider band | Phase margin (more lag from parasitic poles and delay), noise bandwidth | Control / analog designer |
| More phase margin (60–75°) | Damping, robustness to model error, less peaking | Lower crossover for the same plant, or more compensation | Control designer |
| Gain margin | Tolerance to gain variation (process, temperature, load) | Lower nominal loop gain and accuracy | Control designer |
| Sensitivity peak target $M_s$ | One robust number covering both margins | Conservative designs | Control designer |
| Reducing delay (faster sampling, less computation) | Delay margin and achievable crossover | Power and silicon area | Digital / system architect |
| Second-pole placement in an op-amp ($f_2 \ge 2\,$GBW) | Unity-gain phase margin near 65° | Power in the second stage; or decompensation (stable only above a minimum gain) | Analog IC designer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Phase margin against damping | PM ≈ 100ζ (deg) up to ζ ≈ 0.7; 45° ↔ ζ ≈ 0.42; 65.5° ↔ ζ = 0.707 | §3.4 |
| Common design targets | PM 45°–70°, GM ≥ 6–10 dB, $M_s$ ≤ 1.3–2 | §3.7 and practice |
| Delay margin | PM (rad) / $\omega_c$ | §3.2 |
| Phase of a delay | $-\omega T$: −57.3° per radian of $\omega T$ | §3.5 |
| Two-pole op-amp at unity gain | PM = 90° − arctan($f_c/f_2$) with the true crossover $f_c$: 65.5° for $f_2$ = 2 GBW, 76.3° for $f_2$ = 4 GBW, 51.8° for $f_2$ = GBW (with $f_c \approx$ GBW: 63.4°, 76.0°, 45.0°) | Example 15-07.6, §3.8, lab |
| Third-order PLL, best margin | $\arctan[(b - 1)/(2\sqrt b)]$ at $\omega_c = 1/\sqrt{\tau_z\tau_p}$, $b = \tau_z/\tau_p$ | §3.8 |
| Bode's integral | 0 for stable open loops; $\pi\sum\mathrm{Re}\,p_k$ otherwise | §3.7 |

## 8. Common mistakes

- **Reading margins of an open-loop unstable or conditionally stable loop with the simple rule.** Use the Nyquist criterion; margins can mean "how far the gain may fall".
- **Forgetting the integrator's semicircle** when counting Nyquist encirclements for loops with poles at the origin.
- **Measuring phase margin on the closed-loop response.** Margins belong to the loop gain $L$, not to $T$.
- **Treating a right-half-plane zero like a left-half-plane one.** Its magnitude is the same, but its phase lags.
- **Assuming big margins mean robustness.** The plot can still pass close to −1 between the two crossover frequencies; check $M_s$.
- **Breaking the loop to measure it.** Opening a high-gain loop changes its operating point; inject instead (Example 15-07.6).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

These are established practice; no perishable figures are quoted.

- **Loop gain is measured with injection.** Network analyzers with injection transformers are standard on power-supply and regulator benches, implementing Middlebrook's method (15-02 [2]) **[Established]**.
- **Simulators compute stability directly.** Analog design flows run loop-gain ("stb") analyses that break the loop without disturbing the operating point and report margins over process, voltage and temperature corners **[Established]**.
- **Phase margin is the lingua franca of op-amp and regulator data sheets**, often with plots of phase margin against load capacitance, because a capacitive load adds a pole at the output (12-06) **[Established]**.

### Why it matters commercially

- **Margins are yield and reliability.** A loop designed with 30° of margin at the typical corner may oscillate at a slow corner; margin specifications protect production yield.
- **Load-dependent stability limits applications.** An amplifier or LDO that is stable only for certain load capacitances constrains customers' boards, which affects design wins.
- **Delay limits digital control loops.** Every microsecond of sampling and computation delay subtracts phase; faster converters and processors buy crossover bandwidth.

### Marketing vs Reality

- **"Stable with any load."** *Reality:* a capacitive load adds an output pole; stability "with any load" usually holds only above a minimum ESR or below a maximum capacitance. *Sanity check:* ask for phase margin against load capacitance and ESR.
- **"60° phase margin."** *Reality:* at which corner, which load, which gain? *Sanity check:* ask for the worst-case margin and $M_s$, and whether it was measured or simulated.
- **"Wide bandwidth for fast transient response."** *Reality:* bandwidth without margin gives ringing. *Sanity check:* ask for the step response and the phase margin together.

### Questions for engineering leaders

1. **"What are the phase and gain margins at the worst corner, and how were they measured?"**
   *Strong:* injection measurements at corners, with $M_s$. *Evasive:* typical simulation only.
2. **"What sets your crossover frequency: a plant pole, a delay or a right-half-plane zero?"**
   *Strong:* names the limit and its value. *Evasive:* "we chose it for speed".
3. **"How much delay can the loop tolerate?"**
   *Strong:* a delay margin, compared with the sampling and computation delay. *Evasive:* delay not considered.
4. **"Where does the loop amplify disturbances?"**
   *Strong:* shows $\lvert S(j\omega)\rvert$ with its peak and explains the waterbed trade. *Evasive:* only low-frequency rejection numbers.

## 10. Concept check

**Q1.** Define phase margin and gain margin.

<details><summary>Answer</summary>

PM = 180° + ∠L(jω_c) at the frequency where |L| = 1; GM = 1/|L(jω₁₈₀)| at the frequency where ∠L = −180°. They measure how much extra phase lag or gain the loop tolerates before oscillating.

</details>

**Q2.** State the Nyquist criterion.

<details><summary>Answer</summary>

$Z = N + P$: the number of unstable closed-loop poles equals the clockwise encirclements of −1 by the Nyquist plot of $L$ plus the number of open-loop right-half-plane poles. Stability requires $N = -P$.

</details>

**Q3.** Why does a time delay destabilize a loop even though it does not change $\lvert L\rvert$?

<details><summary>Answer</summary>

It adds phase lag $\omega T$ that grows with frequency, so at crossover the phase moves toward −180°. When the added lag exceeds the phase margin, the loop oscillates.

</details>

**Q4.** What phase margin corresponds to $\zeta$ = 0.5, and why is the relation useful?

<details><summary>Answer</summary>

About 52° (exactly 51.8° for the standard loop). It lets a designer read expected overshoot (about 16%) from a measured Bode plot.

</details>

**Q5.** What does Bode's sensitivity integral say about disturbance rejection?

<details><summary>Answer</summary>

For a stable closed loop whose loop gain has relative degree at least 2 and no open-loop right-half-plane poles, the integral of ln|S| over frequency is zero: reducing sensitivity in one band necessarily increases it in another. With unstable open-loop poles the net area is positive.

</details>

**Q6.** Why is $M_s$ a better single robustness number than PM or GM alone?

<details><summary>Answer</summary>

It is the reciprocal of the Nyquist plot's closest approach to −1 at any frequency, so it catches near-misses between the two crossover frequencies and bounds both margins.

</details>

**Q7.** How does Middlebrook's injection method measure loop gain without opening the loop?

<details><summary>Answer</summary>

A small source in series in the loop injects a test signal; the ratio of the signals on its two sides, $-v_x/v_y$, equals the loop gain, while the loop stays closed and the operating point is undisturbed.

</details>

Practice: [Problems 15-07](../problems/15-07-problems.md) · [Solutions](../solutions/15-07-solutions.md)

## 11. Key terms

[Loop gain](../../../reference/glossary.md#loop-gain) · [Gain crossover frequency](../../../reference/glossary.md#gain-crossover-frequency) · [Phase margin](../../../reference/glossary.md#phase-margin) · [Gain margin](../../../reference/glossary.md#gain-margin) · [Delay margin](../../../reference/glossary.md#delay-margin) · [Nyquist criterion](../../../reference/glossary.md#nyquist-criterion) · [Sensitivity peak](../../../reference/glossary.md#sensitivity-peak) · [Bode's sensitivity integral](../../../reference/glossary.md#bodes-sensitivity-integral) · [Minimum-phase system](../../../reference/glossary.md#minimum-phase-system)

## 12. Connections

- **Builds on:** Bode plots ([07-07](../../07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md)); stability ([15-05](15-05-stability-routh-hurwitz.md)); root locus ([15-06](15-06-root-locus.md)); $S$ and $T$ ([15-02](15-02-transfer-functions-and-block-diagrams.md), [15-04](15-04-feedback-and-steady-state-error.md)).
- **Next:** [15-08 PID Control](15-08-pid-control.md), which tunes the most common controller using these margins.
- **Used later:** lead and lag design on the Bode plot ([15-09](15-09-lead-lag-compensation.md)); digital control and sampling delay ([15-11](15-11-digital-control.md)); PLL and regulator loops ([15-12](15-12-control-applications-pll-regulators-thermal.md)); op-amp compensation ([12-06](../../12-electronics-2/chapters/12-06-stability-and-compensation.md)); converter control ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 6 (Bode and Nyquist, margins, the relation to damping).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 9–11 (Nyquist, robustness, the Bode integral and fundamental limits; free online).
- J. S. Freudenberg and D. P. Looze, "Right half plane poles and zeros and design tradeoffs in feedback systems," *IEEE Transactions on Automatic Control* 30(6), 1985.
- R. D. Middlebrook, "Measurement of loop gain in feedback systems," *International Journal of Electronics* 38(4), 1975.

## 14. Sources

1. Franklin, Powell and Emami-Naeini; Åström and Murray (Further study): Nyquist criterion, margins and the Bode integral (textbook material).
2. J. S. Freudenberg and D. P. Looze, *IEEE TAC* 30(6), 1985: the sensitivity integral with right-half-plane poles.
3. R. D. Middlebrook, *International Journal of Electronics* 38(4), 1975: loop-gain measurement by injection.

This chapter has no perishable industry figures; its practitioner statements are tagged [Established]. Every number in the examples is recomputed by the verify script (margins by root finding, encirclements by tracing the Nyquist contour, the Bode integral by quadrature, closed-loop roots as a cross-check), and Example 15-07.6 is confirmed by an ngspice injection measurement.
