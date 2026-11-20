<!-- status: reviewed -->
# 15-03 · Time Response and Specifications

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The time-response material of a first course in feedback control: first- and second-order step responses, rise time, overshoot, settling time, pole locations and dominant poles, effects of extra poles and zeros (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3; Nise, *Control Systems Engineering*, ch. 4; Ogata, *Modern Control Engineering*, ch. 5) |
| **Prerequisites** | [15-02 Transfer Functions and Block Diagrams](15-02-transfer-functions-and-block-diagrams.md), [02-03 Second-Order Linear ODEs](../../02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md), [07-03 Second-Order RLC Transients](../../07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Compute the rise time, settling time and bandwidth of a first-order system from its time constant, and the time it needs to settle to a given number of bits.
2. Derive the underdamped second-order step response and, from it, the peak time and the overshoot formula.
3. Translate time-domain specifications into a permitted region of the s-plane, and choose a loop gain that meets them.
4. Judge when a pair of poles dominates a higher-order response, and estimate how an extra pole, a zero or a pole–zero doublet changes overshoot and settling.
5. Read a settling-time specification critically, separating slewing from linear settling.

---

## 1. Big picture

A closed loop's transfer function (15-02) says everything about its response, but customers and specifications speak in time: how fast the output gets there, how far it overshoots, how long until it stays within tolerance. This chapter connects the two languages. For first- and second-order systems the connection is exact and fits on an index card. Real loops have more poles and zeros, but often one pair of poles dominates, and the index card still works if you know when to distrust it. The skill is moving freely between "poles at −3 ± j2" and "1% overshoot, settled in 1.1 s".

- **Data converters live on settling time.** An ADC driver must settle to half a least-significant bit before the sampling instant; a 16-bit converter needs about 12 time constants (§7).
- **Power delivery is specified in the time domain.** A regulator's load-transient response is overshoot and recovery time; a DVFS voltage step must settle before the clock speeds up (22-07, 15-12).
- **PLL lock time and hop time are settling times** of the loop's phase and frequency (15-12).
- **Specifications become pole locations.** Overshoot fixes a damping ratio, settling time fixes the real part of the poles, and the design job becomes placing poles in a region (15-06, 15-09).

## 2. Intuition first

**Two clocks in every response.** An underdamped response does two things at once: it oscillates, at the damped frequency $\omega_d$, and it decays, at rate $\sigma$. The oscillation sets when the first peak comes (half a period). The decay sets how long the ringing lasts. Their ratio, how much the oscillation decays during one swing, sets the overshoot. A pole at $-\sigma + j\omega_d$ carries both clocks in its two coordinates.

**An analogy: settling a trade.** Think of a fund rebalancing toward a target allocation. A patient manager closes a fixed fraction of the gap each day: the gap shrinks geometrically, with no overshoot, like a first-order system. An aggressive manager reacts to the gap and to its momentum, overshooting and coming back, like a second-order system. Aggressiveness buys an earlier arrival at the cost of overshoot and some back-and-forth. The analogy breaks down in two ways. Real trading has fixed costs, which make the response discontinuous. And a manager can see the future target, while a causal loop reacts only to what has already happened.

**Where the poles sit.** Every specification reads off one coordinate of the dominant pole pair $-\sigma \pm j\omega_d$ (Figure 1, left):

| Pole feature | Specification it sets | Relation (§3.3) |
|---|---|---|
| Height $\omega_d$ | Peak time | $t_p = \pi/\omega_d$ |
| Depth $\sigma$ | Settling time | $t_s \approx 4/\sigma$ |
| Angle $\theta$ from the negative real axis ($\cos\theta = \zeta$) | Overshoot | $M_p = e^{-\pi\cot\theta}$ |
| Distance $\omega_n$ from the origin | Rise time | $t_r \approx 1.8/\omega_n$ |

![Two plots. Left: the s-plane for Example 15-03.3. Two lines from the origin at 53.8 degrees above and below the negative real axis bound the region with at most 10% overshoot; a vertical line at sigma = -10 bounds the region that settles within 0.4 s. The permitted region, left of the vertical line and inside the wedge, is shaded. The closed-loop poles of s^2 + 25s + K move from 0 and -25 along the real axis, meet at -12.5 and rise vertically; the poles for K = 434 are marked at -12.5 plus and minus j16.7, inside the region. Right: unit-step responses of the standard second-order system against omega_n t for damping ratios 0.2, 0.5, 0.707 and 1, with a 2% band around 1. The 0.2 response overshoots by about 53% and rings for many cycles; the 0.707 response overshoots by about 4%; the critically damped one rises slowly without overshoot.](../../../assets/figures/15-03/specs.svg)

*Figure 1. Left: time-domain specifications as an s-plane region (Example 15-03.3). Right: the shape of the second-order step response depends only on $\zeta$; $\omega_n$ only scales time.*

## 3. Theory

### 3.1 Test inputs and what they reveal

A **unit step** (a switch closing, a setpoint change, a load step) is the standard test because it is easy to apply and it exercises both the transient and the steady state. Its response splits into a **transient**, which decays if the system is stable, and a **steady state**, whose value is the DC gain $T(0)$ (15-02). Ramps test tracking of moving targets (15-04); impulses reveal the natural modes directly. Because differentiation is linear, the impulse response is the derivative of the step response, a fact used repeatedly below.

### 3.2 First-order systems

For $T(s) = K/(\tau s + 1)$, a single pole at $-1/\tau$, the step response is

$$
y(t) = K\left(1 - e^{-t/\tau}\right) .
$$

- After one time constant it has covered $1 - e^{-1}$ = 63.2% of the way.
- The **10–90% rise time** solves $e^{-t_1/\tau} = 0.9$ and $e^{-t_2/\tau} = 0.1$: $t_r = t_2 - t_1 = \tau\ln 9 = 2.197\tau$.
- The **settling time** to within a fraction $\epsilon$ of the final value (here $\epsilon$ is a dimensionless tolerance such as 0.02, not a permittivity) solves $e^{-t_s/\tau} = \epsilon$: $t_s = \tau\ln(1/\epsilon)$. For 2%, $t_s = \tau\ln 50 = 3.912\tau$; for 0.1%, $6.908\tau$.
- The **bandwidth**, where $\lvert T(j\omega)\rvert$ falls 3 dB, is $\omega_B = 1/\tau$, so $f_B = 1/(2\pi\tau)$ and

$$
t_rf_B = \frac{\ln 9}{2\pi} = 0.350 .
$$

This product is why a 350 MHz oscilloscope shows about a 1 ns rise time: speed in time and bandwidth in frequency are two views of one pole.

**Settling to $n$ bits.** An ADC with $n$ bits needs the error below half an LSB, a fraction $2^{-(n+1)}$ of full scale, so $t_s = (n + 1)\tau\ln 2$: 9.0τ for 12 bits and 11.8τ for 16 bits.

### 3.3 The second-order step response, derived

The standard second-order system (02-03, 07-03, 15-01) is

$$
T(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_ns + \omega_n^2}, \qquad p_{1,2} = -\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2} = -\sigma \pm j\omega_d ,
$$

with natural frequency $\omega_n$ (rad/s), damping ratio $\zeta$ (dimensionless), decay rate $\sigma = \zeta\omega_n$ and damped frequency $\omega_d = \omega_n\sqrt{1 - \zeta^2}$. Note $\sigma^2 + \omega_d^2 = \omega_n^2$: the poles lie on a circle of radius $\omega_n$, at angle $\theta = \arccos\zeta$ from the negative real axis. For $\zeta > 1$ the poles are real (overdamped), at $\zeta = 1$ they coincide (critically damped), and for $0 < \zeta < 1$ they are complex (underdamped).

**The step response for $0 < \zeta < 1$.** With $Y(s) = T(s)/s$, partial fractions give

$$
Y(s) = \frac1s - \frac{s + 2\sigma}{(s + \sigma)^2 + \omega_d^2} = \frac1s - \frac{s + \sigma}{(s + \sigma)^2 + \omega_d^2} - \frac{\sigma}{\omega_d}\cdot\frac{\omega_d}{(s + \sigma)^2 + \omega_d^2} .
$$

(Check: recombining over the common denominator gives $[(s + \sigma)^2 + \omega_d^2 - s(s + 2\sigma)]/[s(\ldots)] = \omega_n^2/[s(\ldots)]$.) The shifted cosine and sine transforms (02-05) invert this to

$$
y(t) = 1 - e^{-\sigma t}\left(\cos\omega_dt + \frac{\sigma}{\omega_d}\sin\omega_dt\right) = 1 - \frac{e^{-\sigma t}}{\sqrt{1 - \zeta^2}}\sin(\omega_dt + \phi), \qquad \phi = \arccos\zeta ,
$$

where the second form uses $\sigma/\omega_d = \zeta/\sqrt{1 - \zeta^2}$ and combines the sine and cosine into one sinusoid.

**Peak time and overshoot.** Differentiate the first form. The cosine terms cancel, leaving

$$
\dot y(t) = e^{-\sigma t}\left(\frac{\sigma^2}{\omega_d} + \omega_d\right)\sin\omega_dt = \frac{\omega_n}{\sqrt{1 - \zeta^2}}\,e^{-\sigma t}\sin\omega_dt ,
$$

which is also the impulse response. It is first zero for $t > 0$ when $\omega_dt = \pi$, so the **peak time** is

$$
t_p = \frac{\pi}{\omega_d} .
$$

There $\cos\omega_dt_p = -1$ and $\sin\omega_dt_p = 0$, so $y(t_p) = 1 + e^{-\sigma\pi/\omega_d}$, and the **fractional overshoot** is

$$
M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}}, \qquad \zeta = \frac{-\ln M_p}{\sqrt{\pi^2 + \ln^2 M_p}} .
$$

Overshoot depends on $\zeta$ alone, that is, on the angle of the poles, not on how fast they are.

**Settling time.** The response stays within the envelope $1 \pm e^{-\sigma t}/\sqrt{1 - \zeta^2}$. The envelope enters a 2% band at $t = \ln[1/(0.02\sqrt{1 - \zeta^2})]/\sigma$, which is close to the common rule

$$
t_s \approx \frac{4}{\sigma} = \frac{4}{\zeta\omega_n} .
$$

The envelope is a bound. The actual response crosses into the band earlier when the last crossing falls between envelope peaks, so the exact settling time jumps as $\zeta$ changes (the table below shows a drop from 5.96/$\omega_n$ to 3.76/$\omega_n$ between $\zeta$ = 0.707 and 0.8).

**Rise time** has no closed form for the underdamped case; it is computed numerically. The rule of thumb $t_r \approx 1.8/\omega_n$ is accurate near $\zeta$ = 0.6 and within about 25% of the exact value for $0.4 \le \zeta \le 0.7$ (23% high at $\zeta$ = 0.4, 15% low at 0.7). This chapter quotes such errors as the rule's deviation from the exact value.

| $\zeta$ | Overshoot | $\omega_nt_r$ (10–90%) | $\omega_nt_s$ (2%, exact) | $4/\zeta$ |
|---|---|---|---|---|
| 0.3 | 37.2% | 1.32 | 11.2 | 13.3 |
| 0.5 | 16.3% | 1.64 | 8.08 | 8 |
| 0.707 | 4.32% | 2.15 | 5.96 | 5.66 |
| 0.8 | 1.52% | 2.47 | 3.76 | 5 |
| 1.0 | 0 | 3.36 | 5.83 | 4 |

The critically damped response ($\zeta$ = 1) is not the fastest to settle: a little overshoot that stays inside the band lets the response arrive sooner.

> **Math refresher — combining a sine and a cosine.** $a\cos x + b\sin x = R\sin(x + \phi)$ with $R = \sqrt{a^2 + b^2}$, $\sin\phi = a/R$ and $\cos\phi = b/R$. Here $a = 1$ and $b = \zeta/\sqrt{1 - \zeta^2}$, so $R = 1/\sqrt{1 - \zeta^2}$, $\sin\phi = \sqrt{1 - \zeta^2}$ and $\cos\phi = \zeta$.

### 3.4 Specifications as regions of the s-plane

Each specification constrains one geometric feature of the dominant poles:

- **Overshoot** $\le M_{max}$ requires $\zeta \ge \zeta_{min}$: the poles lie inside a wedge of half-angle $\arccos\zeta_{min}$ about the negative real axis.
- **Settling time** $\le t_{s,max}$ requires $\sigma \ge 4/t_{s,max}$: the poles lie left of a vertical line.
- **Peak time** $\le t_{p,max}$ requires $\omega_d \ge \pi/t_{p,max}$: the poles lie outside a horizontal band.
- **Rise time** $\le t_{r,max}$ requires roughly $\omega_n \ge 1.8/t_{r,max}$: the poles lie outside a circle.

The permitted region is the intersection. Design then means choosing a controller that puts the closed-loop poles there (15-06, 15-09). Because the rules are approximate, a design near a boundary must be checked by simulation. Problem 15-03.5 shows a pole pair that passes the rise-time rule yet fails the exact rise time.

### 3.5 Dominant poles and extra poles

A higher-order response is a sum of modes, one per pole (02-09). A mode with a large decay rate dies quickly and affects only the first moments. If one pair of poles is much closer to the imaginary axis than all others, that pair **dominates**: the response looks second-order with those poles. A common rule is that other poles should be at least five times farther left than the dominant pair's real part.

An extra real pole at $-p$ in $T(s)\,p/(s + p)$ acts as a low-pass filter on the second-order response: it slows the rise, delays the peak and usually lowers the overshoot. Example 15-03.4 measures the effect for $p$ from 20 times $\sigma$ down to $2\sigma$. When approximating, keep the DC gain: replace $p/(s + p)$ by 1. Replacing $1/(s + p)$ by 1 instead would change the DC gain by a factor of $p$.

### 3.6 Zeros, right-half-plane zeros and doublets

**A left-half-plane zero.** Multiply $T(s)$ by $(1 + s/z)$:

$$
y_z(t) = y(t) + \frac1z\,\dot y(t) .
$$

The added term is proportional to the impulse response, which is positive during the first half-cycle. So a zero speeds the rise and raises the peak, and the closer the zero is to the origin, the larger the effect. A zero at four times $\sigma$ raises the overshoot modestly; a zero at $\sigma$ more than quadruples it (Example 15-03.5). This is why the PLL of Problem 15-02.13 overshoots by 21% at $\zeta$ = 0.707.

**A right-half-plane zero** ($1 - s/z$, $z > 0$) subtracts the derivative term instead: $y_z = y - \dot y/z$. By the initial-value theorem the initial slope is $\lim_{s\to\infty}sT(s) = -\omega_n^2/z$, negative, so the response first moves the wrong way (**undershoot**). Such systems are called **non-minimum-phase**. A boost converter's control-to-output transfer function has a right-half-plane zero: asked for more output voltage, it first delivers less, because the inductor is connected to the output for a shorter fraction of each cycle (22-07). A right-half-plane zero limits how fast any controller can make the loop.

**A pole–zero doublet** is a pole and a zero very close together, with $T_d(s) = (1 + s/z)/(1 + s/p)$. On a Bode plot it is nearly invisible, but its step response is

$$
\frac{T_d(s)}{s} = \frac1s - \left(1 - \frac pz\right)\frac{1}{s + p} \quad\Longrightarrow\quad y_d(t) = 1 - \left(1 - \frac pz\right)e^{-pt} .
$$

The fast part of the loop gets within a small fraction $1 - p/z$ of the target quickly, but the last part creeps in with the doublet's slow time constant $1/p$. In amplifiers, doublets appear wherever the signal divides into a fast path and a slow path that later recombine, as in feedforward-compensated stages; slow thermal effects in the input devices produce similar tails. They wreck precision settling (Example 15-03.6).

> **Going deeper — why the impulse response is the derivative of the step response.** The step response is the impulse response convolved with a unit step, $y(t) = \int_0^th(\tau)\,d\tau$ (11-03). Differentiating gives $\dot y = h$. In the s-domain, $Y = T/s$ and $sY = T$: multiplying by $s$ is differentiation with zero initial conditions. So zeros, which multiply $T$ by polynomials in $s$, add weighted derivatives of the zero-free response.

### 3.7 Slewing: when the linear model stops applying

An amplifier's output can change only so fast: its **slew rate** SR (V/s) is set by the current available to charge the compensation capacitor. A large step first slews at SR, then settles linearly once the remaining error is small enough for the input stage to be linear. A simple model places the transition where the linear response's slope equals SR, at an error of $V_L = \mathrm{SR}\cdot\tau$. The total settling time is then

$$
t_s \approx \frac{V_{step} - V_L}{\mathrm{SR}} + \tau\ln\frac{V_L}{\epsilon V_{step}} .
$$

Datasheet settling times include slewing, linear settling and any doublet tail. Problem 15-03.12 compares this estimate with a published specification.

## 4. Worked examples

### Example 15-03.1 · A sensor filter (tier A)

**Setup.** An on-die temperature sensor feeds a single-pole RC filter with $\tau$ = 1 ms. Find its 10–90% rise time, its settling time to 2% and to 0.1%, its bandwidth, and the product of rise time and bandwidth.

**Solution.** $t_r = \tau\ln 9$ = **2.20** ms. $t_s(2\%) = \tau\ln 50$ = **3.91** ms. $t_s(0.1\%) = \tau\ln 1000$ = **6.91** ms. $f_B = 1/(2\pi\tau)$ = **159.2** Hz. $t_rf_B$ = **0.350**.

**Units check.** $\tau$ in seconds; $\ln$ of a ratio is dimensionless; $f_B$ in 1/s = Hz; the product is dimensionless.

**Sanity check.** A thermal throttling loop that samples this sensor every 10 ms sees it settled to better than 0.1% between samples, so the filter does not limit the loop. A 1 ms sampling interval would see only 63% of a step.

### Example 15-03.2 · Reading the specs from the poles (tier B)

**Setup.** Example 15-02.3's closed loop is $T(s) = 10/(s^2 + 3s + 12)$. Find $\sigma$, $\omega_d$, the rise time, peak time, overshoot and the 2% settling time, by the formulas and exactly.

**Solution.** From 15-02, $\omega_n$ = 3.464 rad/s and $\zeta$ = 0.433, so $\sigma = 3/2$ = **1.5** s⁻¹ and $\omega_d = \sqrt{12 - 2.25}$ = **3.122** rad/s. Then

$$
t_p = \frac{\pi}{\omega_d} = \mathbf{1.006}\ \text{s}, \qquad M_p = e^{-\pi \times 0.433/0.901} = \mathbf{22.1}\% .
$$

The settling-time rule gives $4/\sigma$ = **2.67** s, and the envelope gives $\ln[1/(0.02 \times 0.901)]/1.5$ = **2.68** s. Solving the exact response numerically gives a rise time of **0.438** s and a 2% settling time of **2.42** s. The DC gain is 0.833, so all percentages are relative to 0.833, not to 1.

**Units check.** $\sigma$ and $\omega_d$ in 1/s; their ratio, in the exponent, is dimensionless.

**Sanity check.** The rule $1.8/\omega_n$ gives 0.52 s for the rise time, 19% above the exact value, as expected for $\zeta$ = 0.43. The exact settling time is shorter than the envelope bound, because at 2.42 s the response is between envelope peaks.

### Example 15-03.3 · Choosing a gain from specifications (tier B)

**Setup.** A positioning loop has $L(s) = K/[s(s + 25)]$ with unity feedback. The specification is overshoot at most 10% and 2% settling time at most 0.4 s. Find the range of $K$ that meets the overshoot specification, choose $K$ for $\zeta$ = 0.6, and give the resulting specs.

**Solution.** The closed loop is $T = K/(s^2 + 25s + K)$, so $\omega_n = \sqrt K$ and $2\zeta\omega_n = 25$. The real part of the poles is fixed: $\sigma$ = 12.5 s⁻¹, whatever $K$. The settling rule gives $4/12.5$ = **0.32** s for every underdamped $K$, which suggests the settling specification is met whatever the gain. The rule only bounds the envelope, though. Exactly, the 2% settling time jumps around between about 0.23 and 0.47 s as $K$ varies (the response re-enters the band at different points of its oscillation, §3.3), and it exceeds 0.4 s for $K \lesssim 173$ ($\zeta \gtrsim 0.95$), where the nearly critically damped response creeps into the band slowly.

For overshoot at most 10%, $\zeta \ge -\ln 0.1/\sqrt{\pi^2 + \ln^2 0.1}$ = **0.591**. Since $\zeta = 12.5/\sqrt K$, that means $K \le (12.5/0.591)^2$ = **447**.

For $\zeta$ = 0.6: $\omega_n = 12.5/0.6$ = 20.83 rad/s and $K = \omega_n^2$ = **434**. Then the overshoot is **9.48**%, $\omega_d = \omega_n \times 0.8$ = 16.67 rad/s, and $t_p = \pi/16.67$ = **0.188** s. The exact response gives a rise time of **0.0890** s and a 2% settling time of **0.285** s.

**Units check.** $K$ has units of 1/s² (it equals $\omega_n^2$), consistent with $L$ being dimensionless.

**Sanity check.** The poles move along the vertical line $\sigma$ = 12.5 as $K$ rises (15-06 calls this the root locus). Raising $K$ raises $\omega_d$ and the overshoot but cannot change the envelope's decay rate $\sigma$, so it cannot improve the settling *bound*; the exact settling time only wanders within it. To settle reliably faster, the plant pole at −25 must move, which needs a different controller (15-09).

### Example 15-03.4 · How much does an extra pole matter? (tier C)

**Setup.** The base system $1/(s^2 + s + 1)$ has $\omega_n$ = 1 rad/s, $\zeta$ = 0.5 and $\sigma$ = 0.5. Add a real pole, $T_p(s) = \dfrac{p}{(s + p)(s^2 + s + 1)}$, for $p$ = 10, 3 and 1. Compare overshoot, rise time and 2% settling time.

**Solution.** Simulating the exact responses (the lab does this):

| | Base | $p$ = 10 (20σ) | $p$ = 3 (6σ) | $p$ = 1 (2σ) |
|---|---|---|---|---|
| Overshoot | **16.3**% | **16.2**% | **15.2**% | **8.1**% |
| Rise time | **1.64** s | **1.65** s | **1.76** s | **2.29** s |
| 2% settling time | **8.08** s | **8.17** s | **8.35** s | **6.64** s |

At $p$ = 20σ the extra pole is invisible. At 6σ it costs 7% in rise time and lowers the overshoot by a percentage point, consistent with the five-times rule. At $p$ = 2σ the system is no longer second-order: the rise time grows 40% and the overshoot halves.

**Units check.** All times in seconds for $\omega_n$ = 1 rad/s; for another $\omega_n$, divide by $\omega_n$.

**Sanity check.** The $p$ = 1 case settles sooner because its smaller overshoot never leaves the 2% band after the first swing. "Settling time" is a threshold measure and can move either way.

### Example 15-03.5 · Zeros on either side (tier C)

**Setup.** Multiply the base system of Example 15-03.4 by $(1 + s/z)$ with $z$ = 2 and $z$ = 0.5, and by the right-half-plane factor $(1 - s/2)$. Compare the responses.

**Solution.** From $y_z = y \pm \dot y/z$ and exact simulation:

- $z$ = 2 (four times $\sigma$): overshoot **19.1**%, rise time **1.37** s, against 16.3% and 1.64 s without the zero.
- $z$ = 0.5 (equal to $\sigma$): overshoot **69.9**%, rise time **0.479** s. The derivative term now dominates.
- Right-half-plane zero at 2: the response first dips to an undershoot of **9.12**% of the final value at **0.385** s, then overshoots by **17.8**%.

**By hand.** The base response is $y = 1 - e^{-\sigma t}(\cos\omega_dt + (\sigma/\omega_d)\sin\omega_dt)$, with $\dot y = (\omega_n^2/\omega_d)e^{-\sigma t}\sin\omega_dt$ and $\ddot y = (\omega_n^2/\omega_d)e^{-\sigma t}(\omega_d\cos\omega_dt - \sigma\sin\omega_dt)$; here $\sigma$ = 0.5 and $\omega_d$ = 0.866. The peak of $y_z = y + \dot y/z$ is where $\dot y + \ddot y/z = 0$, that is $\sin\omega_dt\,(1 - \sigma/z) + (\omega_d/z)\cos\omega_dt = 0$, or

$$
\tan\omega_dt_p = -\frac{\omega_d}{z - \sigma} .
$$

For $z$ = 2 this is $-0.577$, so $\omega_dt_p = \pi - 0.524$ and $t_p$ = 3.023 s; substituting into $y_z$ gives the 19.1% overshoot. For $z = \sigma$ = 0.5 the tangent is infinite, $\omega_dt_p = \pi/2$ and $t_p$ = 1.814 s, giving 69.9%. For the right-half-plane zero, $y_z = y - \dot y/z$ and the same steps give $\tan\omega_dt = \omega_d/(z + \sigma) = 0.346$ for the first extremum: $t$ = 0.385 s, the undershoot. Rise and settling times have no such closed form; they are found by locating the level crossings, which the lab does by root-finding on the exact response (the last exit from the band, bracketed by the envelope).

**Units check.** $\dot y/z$: (1/s)/(1/s) is dimensionless, like $y$.

**Sanity check.** The initial slope with the right-half-plane zero is $-\omega_n^2/z$ = −0.5 s⁻¹, negative as predicted. All three responses settle to 1, because $(1 \pm s/z)$ is 1 at DC.

### Example 15-03.6 · A doublet ruins precision settling (tier C)

**Setup.** An amplifier in a unity-gain buffer has a closed-loop pole at $\omega_c$ = 2π × 100 MHz. A parasitic doublet adds a pole at 1 MHz and a zero at 1.05 MHz: $T(s) = \dfrac{\omega_c}{s + \omega_c}\cdot\dfrac{1 + s/z}{1 + s/p}$. Find the 0.1% settling time without and with the doublet, the amplitude of the slow tail and its time constant.

**Solution.** Without the doublet, $t_s = \ln(1000)/\omega_c$ = **11.0** ns.

With it, the partial-fraction residue of $T(s)/s$ at $s = -p$ is $-\dfrac{\omega_c}{\omega_c - p}\left(1 - \dfrac pz\right)$, a tail of amplitude 1.0101 × 0.0476 = **4.81**%. It decays with time constant $1/p$ = **159** ns. The fast pole is gone after a few nanoseconds, so the response is within 0.1% once $0.0481e^{-pt} < 0.001$, at

$$
t_s = \frac{\ln(48.1)}{p} = \mathbf{616}\ \text{ns} ,
$$

56 times longer, from a doublet that changes the frequency response by less than 0.5 dB.

**Units check.** $p$ in rad/s; $\ln$ of a ratio is dimensionless; $t$ in seconds.

**Sanity check.** If the zero matched the pole exactly, the tail would vanish. The tail amplitude scales with the mismatch $(z - p)/z$, so Problem 15-03.13 asks how close the match must be.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Txt 15-03.a | overshoot at ζ = 0.3 | 37.2 | % |
| Txt 15-03.b | overshoot at ζ = 0.5 | 16.3 | % |
| Txt 15-03.c | overshoot at ζ = 0.707 | 4.32 | % |
| Txt 15-03.d | overshoot at ζ = 0.8 | 1.52 | % |
| Txt 15-03.e | ωn·tr at ζ = 0.3 | 1.32 | — |
| Txt 15-03.f | ωn·tr at ζ = 0.5 | 1.64 | — |
| Txt 15-03.g | ωn·tr at ζ = 0.707 | 2.15 | — |
| Txt 15-03.h | ωn·tr at ζ = 0.8 | 2.47 | — |
| Txt 15-03.i | ωn·tr at ζ = 1 | 3.36 | — |
| Txt 15-03.j | ωn·ts at ζ = 0.3 | 11.2 | — |
| Txt 15-03.k | ωn·ts at ζ = 0.5 | 8.08 | — |
| Txt 15-03.l | ωn·ts at ζ = 0.707 | 5.96 | — |
| Txt 15-03.m | ωn·ts at ζ = 0.8 | 3.76 | — |
| Txt 15-03.n | ωn·ts at ζ = 1 | 5.83 | — |
| Txt 15-03.o | settling for 12 bits | 9.0 | τ |
| Txt 15-03.p | settling for 16 bits | 11.8 | τ |
| Ex 15-03.1a | rise time | 2.20 | ms |
| Ex 15-03.1b | 2% settling time | 3.91 | ms |
| Ex 15-03.1c | 0.1% settling time | 6.91 | ms |
| Ex 15-03.1d | bandwidth | 159.2 | Hz |
| Ex 15-03.1e | rise time × bandwidth | 0.350 | — |
| Ex 15-03.2a | σ | 1.5 | 1/s |
| Ex 15-03.2b | ωd | 3.122 | rad/s |
| Ex 15-03.2c | peak time | 1.006 | s |
| Ex 15-03.2d | overshoot | 22.1 | % |
| Ex 15-03.2e | settling rule 4/σ | 2.67 | s |
| Ex 15-03.2f | envelope settling time | 2.68 | s |
| Ex 15-03.2g | exact rise time | 0.438 | s |
| Ex 15-03.2h | exact settling time | 2.42 | s |
| Ex 15-03.3a | settling rule | 0.32 | s |
| Ex 15-03.3b | minimum ζ | 0.591 | — |
| Ex 15-03.3c | maximum K | 447 | 1/s² |
| Ex 15-03.3d | K for ζ = 0.6 | 434 | 1/s² |
| Ex 15-03.3e | overshoot | 9.48 | % |
| Ex 15-03.3f | peak time | 0.188 | s |
| Ex 15-03.3g | rise time | 0.0890 | s |
| Ex 15-03.3h | settling time | 0.285 | s |
| Ex 15-03.4a | overshoot, base | 16.3 | % |
| Ex 15-03.4b | overshoot, p = 10 | 16.2 | % |
| Ex 15-03.4c | overshoot, p = 3 | 15.2 | % |
| Ex 15-03.4d | overshoot, p = 1 | 8.1 | % |
| Ex 15-03.4e | rise time, base | 1.64 | s |
| Ex 15-03.4f | rise time, p = 10 | 1.65 | s |
| Ex 15-03.4g | rise time, p = 3 | 1.76 | s |
| Ex 15-03.4h | rise time, p = 1 | 2.29 | s |
| Ex 15-03.4i | settling time, base | 8.08 | s |
| Ex 15-03.4j | settling time, p = 10 | 8.17 | s |
| Ex 15-03.4k | settling time, p = 3 | 8.35 | s |
| Ex 15-03.4l | settling time, p = 1 | 6.64 | s |
| Ex 15-03.5a | overshoot, z = 2 | 19.1 | % |
| Ex 15-03.5b | rise time, z = 2 | 1.37 | s |
| Ex 15-03.5c | overshoot, z = 0.5 | 69.9 | % |
| Ex 15-03.5d | rise time, z = 0.5 | 0.479 | s |
| Ex 15-03.5e | undershoot, RHP zero | 9.12 | % |
| Ex 15-03.5f | time of the undershoot | 0.385 | s |
| Ex 15-03.5g | overshoot, RHP zero | 17.8 | % |
| Ex 15-03.5h | initial slope, RHP zero | −0.5 | 1/s |
| Ex 15-03.6a | settling without doublet | 11.0 | ns |
| Ex 15-03.6b | tail amplitude | 4.81 | % |
| Ex 15-03.6c | tail time constant | 159 | ns |
| Ex 15-03.6d | settling with doublet | 616 | ns |

## 5. Simulate it

The lab, [labs/15-03-lab](../labs/15-03-lab/README.md), provides `specs.py`: exact step and impulse responses through the matrix exponential, and `step_specs`, which measures rise time, peak, overshoot, undershoot and settling time with crossing times refined by root finding. You:

1. **Sweep $\zeta$** for the standard second-order system and reproduce the table in §3.3, including the jumps in settling time.
2. **Run `rlc_step.cir`**, a series RLC low-pass with $\zeta$ = 0.5, in ngspice, and compare its measured rise time, peak time, overshoot and settling time with `step_specs`.
3. **Add poles, zeros and a doublet** to see Examples 15-03.4 to 15-03.6 develop.
4. **Map specifications onto the s-plane** and test candidate pole pairs against both the rules and the exact responses.

**Guided exercise (predict, then run).** **Before Part 2,** predict the RLC circuit's overshoot and peak time from $\zeta$ = 0.5 and $\omega_n$ = 31,623 rad/s. (16.3% at $\pi/\omega_d$ = 115 µs.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Lower damping ($\zeta$ toward 0.5) | Faster rise and earlier peak | Overshoot; ringing that may excite other parts of the system | Control designer, with the system owner setting overshoot limits |
| Higher damping ($\zeta \ge$ 0.8) | Little or no overshoot | Slower rise; the settling time is not necessarily better | Control designer |
| Faster poles (larger $\sigma$, $\omega_n$) | Shorter settling and rise | Larger actuator effort, more noise bandwidth, stability margins against unmodelled poles shrink | Control and analog designers |
| Precision of pole–zero matching (doublets) | Precision settling to many bits | Layout care, trimming, or architectures without the pole–zero pair | Analog designer |
| Slew rate (bias current) | Large-step settling | Power and noise in the input stage | Analog designer, with product marketing's power budget |
| Accepting a right-half-plane zero (boost topology) | Voltage step-up with few parts | Loop bandwidth limited well below the zero's frequency | Power-electronics architect |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| First-order rise time (10–90%) | 2.20 τ | §3.2 |
| First-order settling time to 2%, 0.1% | 3.91 τ, 6.91 τ | §3.2 |
| Rise time × bandwidth, first order | 0.35 | §3.2 |
| Settling to ½ LSB at 12 and 16 bits | 9.0 τ and 11.8 τ | §3.2 |
| Overshoot at $\zeta$ = 0.5, 0.707, 0.8 | 16.3%, 4.3%, 1.5% | §3.3 |
| Settling-time rule (2%) | $t_s \approx 4/\sigma$ | §3.3 |
| Rise-time rule | $t_r \approx 1.8/\omega_n$ (within about 25% of exact for $0.4 \le \zeta \le 0.7$) | §3.3 |
| Dominance rule | other poles more than 5σ to the left | §3.5 |
| A precision JFET op-amp's settling time to 0.01% (10 V step, gain −1), as of Nov 2026 | 120 ns (SOIC version) and 550 ns (TO-99 version) of the same part number | [1, R-230] |

## 8. Common mistakes

- **Measuring overshoot relative to 1** when the DC gain is not 1. Overshoot is relative to the final value.
- **Using $t_s \approx 4/\sigma$ as exact.** It is an estimate that can be off by a third either way (5 against an exact 3.76 at $\zeta$ = 0.8; 4 against 5.83 at $\zeta$ = 1, in units of $1/\omega_n$). Simulate near a specification limit.
- **Using $t_r \approx 1.8/\omega_n$ outside its range.** At $\zeta$ = 0.8 the rule is 27% below the exact rise time (the true value is 37% longer than the rule).
- **Ignoring zeros.** A zero near the dominant poles can double the overshoot; $\zeta$ alone then misleads.
- **Dropping a pole without keeping the DC gain.** Replace $p/(s + p)$ by 1, not $1/(s + p)$ by 1.
- **Reading settling time from a Bode plot.** A doublet barely shows on a Bode plot but dominates precision settling.
- **Forgetting slewing.** Small-signal settling formulas understate large-step settling time.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Settling is specified with its test conditions.** The datasheet for TI's OPA627 (revision SBOS165C, January 2025) specifies settling time for a 10 V step at a gain of −1, to 0.1% and to 0.01% [1, R-230] **[Established]**. The two package versions sharing that part number differ: the SOIC version is specified at 45 MHz gain-bandwidth, 150 V/µs slew rate and 120 ns to 0.01%; the TO-99 version at 16 MHz, 55 V/µs and 550 ns. The front page quotes 550 ns. Always read the table for the exact variant and conditions.
- **Precision settling is a design discipline in analog ICs.** Pole–zero doublets and their settling tails are textbook topics in analog IC design [2] **[Established]**. For amplifiers that drive data converters, the relevant figure is the settling time to the converter's resolution (0.01% is about 13 bits), as the OPA627 datasheet's 0.01% specification illustrates, rather than bandwidth alone.
- **Loop specifications in power and timing chips are time-domain.** Regulators state load-transient overshoot and recovery time; PLLs state lock time; both follow from the closed-loop poles and zeros of this chapter (15-12, 22-07) **[Established]**.

### Why it matters commercially

- **Throughput is often a settling time.** A multiplexed ADC channel, a DVFS step or a frequency hop cannot proceed until the analog quantity has settled; settling time is a direct limit on samples per second or on transitions per second.
- **Overshoot is a reliability and safety specification.** A voltage overshoot above a process's maximum gate voltage ages transistors (25-09); a mechanical overshoot can collide.
- **Doublets and slew limits are where competing parts differ.** Two amplifiers with the same gain-bandwidth can settle to 16 bits in very different times.

### Marketing vs Reality

- **"Settles in 100 ns."** *Reality:* to what accuracy, for what step size, gain and load? *Sanity check:* ask for the band (0.1%, 0.01%, 1 LSB), the step, the gain and the load capacitance, and compare with $t_s = (n+1)\tau\ln 2$ plus slewing.
- **"Bandwidth 100 MHz, so settling is fast."** *Reality:* bandwidth fixes the dominant pole, not doublet tails or slewing. *Sanity check:* request a long-time-scale settling plot, not just a Bode plot.
- **"No overshoot."** *Reality:* often achieved by heavy damping, which slows rise and may not shorten settling (§3.3 table). *Sanity check:* compare rise and settling times, not overshoot alone.

### Questions for engineering leaders

1. **"What is the settling time to the accuracy our system needs, and under what conditions was it measured?"**
   *Strong:* a measured number at the stated band, step and load, across temperature. *Evasive:* a typical number at a different accuracy, or a simulation only.
2. **"Is there a slow-settling tail, and what causes it?"**
   *Strong:* identifies any doublets or thermal tails and shows long-time-scale measurements. *Evasive:* "the bandwidth is high, so it settles fast".
3. **"How much of the settling time is slewing?"**
   *Strong:* separates slew-limited from linear settling and shows how each scales with step size. *Evasive:* one number for all step sizes.
4. **"Are there right-half-plane zeros in the loop, and how do they limit bandwidth?"**
   *Strong:* yes for boost-type converters, with crossover kept well below the zero. *Evasive:* unaware of the zero.

## 10. Concept check

**Q1.** Why does a first-order system's rise time times its bandwidth equal 0.35?

<details><summary>Answer</summary>

$t_r = \tau\ln 9$ and $f_B = 1/(2\pi\tau)$; the product is $\ln 9/(2\pi)$ = 0.350, independent of $\tau$. Rise time and bandwidth are two measures of the same pole.

</details>

**Q2.** Why does overshoot depend only on $\zeta$?

<details><summary>Answer</summary>

$M_p = e^{-\sigma t_p} = e^{-\pi\sigma/\omega_d}$, and $\sigma/\omega_d = \zeta/\sqrt{1 - \zeta^2}$ depends only on the angle of the poles. Scaling $\omega_n$ speeds up the whole response without changing its shape.

</details>

**Q3.** In Example 15-03.3, why can raising $K$ not change the decay rate $\sigma$ of the response's envelope?

<details><summary>Answer</summary>

The closed-loop characteristic polynomial is $s^2 + 25s + K$, so the sum of the poles is fixed at −25 and, once they are complex, their real part is fixed at −12.5. $K$ moves them vertically, changing $\omega_d$ and the overshoot but not $\sigma$. (The exact settling time still varies with $K$, between about 0.23 and 0.47 s, because the last exit from the 2% band falls at different points of the oscillation; only the envelope bound $4/\sigma$ is fixed.)

</details>

**Q4.** When can a third pole be ignored?

<details><summary>Answer</summary>

When it is several times farther from the imaginary axis than the dominant pair, typically more than five times their real part. Its mode then decays before the dominant response has done much. Example 15-03.4 shows the error growing as the pole approaches.

</details>

**Q5.** How does a left-half-plane zero change the step response, and why?

<details><summary>Answer</summary>

$(1 + s/z)$ adds $\dot y/z$, a multiple of the impulse response, which is positive during the first half-cycle. The response rises faster and overshoots more, the more so the closer the zero is to the origin.

</details>

**Q6.** What is the first sign of a right-half-plane zero in a step response?

<details><summary>Answer</summary>

Undershoot: the output first moves opposite to its final direction. The initial slope is $-\omega_n^2/z$ for a standard second-order system times $(1 - s/z)$.

</details>

**Q7.** Why can a doublet that barely changes the Bode plot dominate settling to 0.1%?

<details><summary>Answer</summary>

It leaves a tail of amplitude about $(z - p)/z$ decaying with the slow time constant $1/p$. A 5% mismatch is a fraction of a decibel in magnitude, but the tail must decay by a factor of 50 to reach 0.1%, which takes $\ln(50)/p$, many times the fast loop's settling time.

</details>

**Q8.** Why is a datasheet's settling time usually longer than $\tau\ln(1/\epsilon)$?

<details><summary>Answer</summary>

It includes slewing for large steps, non-dominant poles, doublet tails and the time to recover from the slewing transition, none of which the single-pole formula includes.

</details>

Practice: [Problems 15-03](../problems/15-03-problems.md) · [Solutions](../solutions/15-03-solutions.md)

## 11. Key terms

[Step response](../../../reference/glossary.md#step-response) · [Rise time](../../../reference/glossary.md#rise-time) · [Peak time](../../../reference/glossary.md#peak-time) · [Overshoot](../../../reference/glossary.md#overshoot) · [Settling time](../../../reference/glossary.md#settling-time) · [Damping ratio](../../../reference/glossary.md#damping-ratio) · [Damped natural frequency](../../../reference/glossary.md#damped-natural-frequency) · [Dominant poles](../../../reference/glossary.md#dominant-poles) · [Non-minimum-phase system](../../../reference/glossary.md#non-minimum-phase-system) · [Pole–zero doublet](../../../reference/glossary.md#pole-zero-doublet) · [Slew rate](../../../reference/glossary.md#slew-rate)

## 12. Connections

- **Builds on:** closed-loop transfer functions ([15-02](15-02-transfer-functions-and-block-diagrams.md)); second-order ODEs ([02-03](../../02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md)); RLC transients ([07-03](../../07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md)); Laplace inversion ([02-05](../../02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md)).
- **Next:** [15-04 Feedback Properties and Steady-State Error](15-04-feedback-and-steady-state-error.md), which studies the steady state this chapter set aside.
- **Used later:** pole placement with root locus ([15-06](15-06-root-locus.md)); phase margin and overshoot ([15-07](15-07-frequency-domain-design.md)); compensator design to time-domain specs ([15-09](15-09-lead-lag-compensation.md)); PLL lock and regulator transients ([15-12](15-12-control-applications-pll-regulators-thermal.md)); converter control and right-half-plane zeros ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3 (time-domain specifications, effects of zeros and extra poles).
- N. S. Nise, *Control Systems Engineering*, ch. 4 (time response, pole locations, higher-order approximations).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, the chapters on frequency response and feedback (doublets and settling time).
- MIT OpenCourseWare 6.302, *Feedback Systems*: lectures on second-order systems and time-domain specifications.

## 14. Sources

1. Texas Instruments, *OPA6x7 Precision, High-Speed JFET Operational Amplifiers*, datasheet SBOS165C (August 2000, revised January 2025). [R-230](../../../reference/research-log.md#r-230--opa627-settling-time-specifications-ti-sbos165c)
2. Gray, Hurst, Lewis and Meyer, *Analysis and Design of Analog Integrated Circuits* (Further study): pole–zero doublets and settling (textbook material).

The time-domain formulas are textbook material (Further study). Every number in the examples and the table is recomputed by the verify script from exact step responses (matrix exponential with crossings refined by root finding), and the RLC example of the lab is confirmed in ngspice.
