<!-- status: verified -->
# 15-11 · Digital Control

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The digital-control material of a first course in feedback control: sampling and the zero-order hold, discrete equivalents of plants and controllers (ZOH, Tustin, matched), z-plane stability, the effect of sampling on margins, and controller implementation (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 8; Franklin, Powell & Workman, *Digital Control of Dynamic Systems*; Nise, *Control Systems Engineering*, ch. 13) |
| **Prerequisites** | [15-07 Frequency-Domain Design](15-07-frequency-domain-design.md), [15-08 PID Control](15-08-pid-control.md), [11-09 The z-Transform](../../11-signals-and-systems/chapters/11-09-z-transform.md), [11-10 Sampling, Aliasing and Reconstruction](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| **Estimated study hours** | 5 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Model a sampled loop: find the zero-order-hold equivalent of a plant and map poles between the s-plane and the z-plane.
2. Discretize a controller with forward Euler, backward Euler or Tustin (with prewarping), and write it as a difference equation.
3. Decide discrete-time stability with the unit circle and the second-order Jury conditions, and find how sampling limits the stable gain.
4. Estimate the phase lost to the hold and to computation delay, and choose a sample rate.
5. Implement a digital PI or PID controller with anti-windup, and judge the effects of quantization and delay in firmware and digital power controllers.

---

## 1. Big picture

Most controllers built today are digital. A microcontroller, a DSP or a block of logic samples the measurement with an ADC, computes the control law as a difference equation, and writes the result through a DAC or a PWM generator that holds it until the next update. Digital control is flexible (gains are register values), repeatable (no drifting capacitors) and capable of logic that analog circuits cannot do. But it changes the loop in three ways. Sampling discards what happens between samples. The hold adds an average delay of half a sample period. Computation adds more. All three cost phase margin (15-07). This chapter models those effects exactly and gives the rules engineers use to choose sample rates and discretize controllers.

- **Digital power management.** Digitally controlled DC-DC converters and PMICs run their compensators in logic at the switching frequency; their delay sets the achievable crossover (Example 15-11.6, 22-07).
- **Thermal and DVFS firmware** runs PI loops at millisecond rates in microcontrollers and power-management processors (15-08, 15-12).
- **Motor drives** run current loops at tens of kilohertz in microcontrollers and FPGAs.
- **Mixed-signal loops**, such as digital PLLs, replace analog loop filters with digital ones (15-12).

## 2. Intuition first

**A controller that blinks.** A digital controller looks at the world only at sample instants and holds its output fixed in between. Between samples it is effectively open-loop. If the plant moves little in one sample period, the loop behaves almost like an analog one. If it moves a lot, the controller always acts on stale information, which is the same as adding delay.

**An analogy: monthly rebalancing.** A portfolio rebalanced monthly, using last month's prices, cannot react to intra-month moves; aggressive monthly rebalancing overshoots and oscillates in a way daily rebalancing would not. The cure is either more frequent rebalancing (a faster sample rate) or gentler trades (lower gain). The analogy breaks down because a market's "plant" changes with the trader's actions in nonlinear ways, while a sampled linear loop can be analyzed exactly, sample by sample.

**Half a sample of delay.** The zero-order hold outputs a staircase. A smooth curve drawn through the middle of each step lags the samples by $T/2$. At frequency $\omega$ that is $\omega T/2$ radians of phase lag, the dominant effect of sampling on a well-sampled loop.

## 3. Theory

### 3.1 The sampled loop and the z-plane

A sampled loop has an ADC sampling every $T$ seconds, a discrete controller $C(z)$, and a zero-order hold (ZOH) driving the continuous plant $P(s)$. The z-transform (11-09) describes the discrete signals. A continuous pole at $s$ maps to a discrete pole at

$$
z = e^{sT} .
$$

The left half-plane maps inside the unit circle: $\lvert z\rvert = e^{\sigma T} < 1$ when $\sigma < 0$. The imaginary axis maps onto the unit circle, and frequencies above the Nyquist frequency $\pi/T$ fold back (aliasing, 11-10). A discrete system is stable when **every pole lies strictly inside the unit circle**.

### 3.2 The ZOH equivalent of the plant

Because the hold makes the plant's input piecewise constant, the plant's state can be advanced exactly from sample to sample. For $\dot{\mathbf{x}} = A\mathbf{x} + Bu$ with $u$ held constant over $[kT, (k + 1)T)$:

$$
\mathbf{x}_{k+1} = e^{AT}\mathbf{x}_k + \left(\int_0^Te^{A\tau}d\tau\right)Bu_k = \Phi\mathbf{x}_k + \Gamma u_k ,
$$

the exact discretization (15-10; the lab computes $\Phi$ and $\Gamma$ from one matrix exponential). The corresponding transfer function is

$$
G(z) = (1 - z^{-1})\,\mathcal{Z}\!\left\{\frac{P(s)}{s}\right\} .
$$

For $P = a/(s + a)$: $G(z) = (1 - e^{-aT})/(z - e^{-aT})$. The ZOH equivalent is exact at the sample instants.

### 3.3 Discretizing a controller

A controller designed in continuous time must be approximated by a difference equation. Each method replaces $s$ by a function of $z$:

| Method | Substitution | Notes |
|---|---|---|
| Forward Euler | $s \leftarrow (z - 1)/T$ | Simple; can map stable poles outside the unit circle at large $T$ |
| Backward Euler | $s \leftarrow (z - 1)/(Tz)$ | Always stable for stable $C(s)$; adds lag |
| **Tustin (bilinear)** | $s \leftarrow \dfrac{2}{T}\dfrac{z - 1}{z + 1}$ | Maps the left half-plane exactly onto the unit disk; warps frequency |
| Tustin with prewarping | $s \leftarrow \dfrac{\omega_p}{\tan(\omega_pT/2)}\dfrac{z - 1}{z + 1}$ | Exact at the chosen frequency $\omega_p$ (often crossover) |
| Matched pole–zero | map each pole and zero by $z = e^{sT}$ and match the DC gain | Preserves pole and zero locations |

Tustin's frequency warping: a continuous frequency $\omega_a$ appears at the discrete frequency $\omega_d$ with $\omega_a = (2/T)\tan(\omega_dT/2)$, close to $\omega_d$ when $\omega_dT \ll 1$. Prewarping removes the error at one chosen frequency.

**A Tustin PI controller.** With $C(s) = K_p + K_i/s$, Tustin gives $C(z) = K_p + K_i\dfrac{T}{2}\dfrac{z + 1}{z - 1}$, that is

$$
u_k = u_{k-1} + \left(K_p + \frac{K_iT}{2}\right)e_k + \left(-K_p + \frac{K_iT}{2}\right)e_{k-1} ,
$$

the **velocity form**: the controller computes a change in output. It has a built-in anti-windup advantage: clamping $u_k$ to the actuator limit stops the accumulation automatically.

### 3.4 Stability of discrete loops

The closed-loop characteristic equation is $1 + C(z)G(z) = 0$, a polynomial in $z$. For a second-order polynomial $z^2 + a_1z + a_0$, the **Jury conditions** for both roots inside the unit circle are

$$
\lvert a_0\rvert < 1, \qquad 1 + a_1 + a_0 > 0, \qquad 1 - a_1 + a_0 > 0 .
$$

(The middle two say the polynomial is positive at $z = 1$ and $z = -1$; the first says the product of the roots has magnitude below 1.) Higher orders use the full Jury table or a computed root check, or the bilinear map $z = (1 + w)/(1 - w)$ followed by Routh (15-05).

A sampled loop can be unstable at gains for which the continuous loop is stable: the hold's delay subtracts phase, so a loop whose continuous phase never reaches −180° (such as the servo of Examples 15-11.4 and 15-11.5) acquires a finite gain margin once it is sampled. Example 15-11.5 shows the stable-gain limit shrinking as $T$ grows.

### 3.5 How fast to sample

Approximating the hold by a delay of $T/2$ (the hold's own phase is exactly $-\omega T/2$; its magnitude droops slightly, and aliasing adds error as $\omega$ approaches the Nyquist frequency):

$$
\Delta\phi \approx -\frac{\omega_cT}{2}\ \text{(radians)} \quad\text{at crossover} .
$$

Any computation delay $T_d$ (time from sampling to updating the output) adds $-\omega_cT_d$. Common rules of thumb follow from limiting this loss:

- sample at 10 to 30 times the closed-loop bandwidth (about 6° to 18° of lag at crossover from the hold alone);
- put an anti-aliasing filter before the ADC, whose own phase lag must also be counted;
- in digital power converters, which update once per switching period, expect total delay of 1 to 1.5 periods, which often limits crossover to well below a tenth of the switching frequency.

### 3.6 Implementation

A digital controller is a difference equation running in finite precision:

- **Quantization.** An $n$-bit ADC resolves full scale over $2^n$ steps; the controller cannot correct errors smaller than one step, and integrators may "hunt" between levels (limit cycles).
- **Coefficient precision.** Controller poles close to $z = 1$ (slow integrators, lag compensators at fast sample rates) are sensitive to coefficient rounding; the velocity form or a delta-operator form helps.
- **Overflow and saturation.** Fixed-point integrators must saturate, not wrap around; anti-windup (15-08) belongs in the code.
- **Timing.** The sample-to-output latency must be constant; jitter adds noise and effective delay.

> **Going deeper — the exact frequency response of a sampled loop.** The discrete loop gain $C(e^{j\omega T})G(e^{j\omega T})$ is the exact sampled-data frequency response at the sample instants. The approximation "continuous loop times $e^{-j\omega T/2}$" agrees with it at low frequency and deviates as $\omega$ approaches the Nyquist frequency, where aliasing makes the discrete response periodic. Example 15-11.4 compares the two.

## 4. Worked examples

### Example 15-11.1 · Mapping poles to the z-plane (tier A)

**Setup.** A continuous design has poles at $-2 \pm j2\sqrt3$ ($\zeta$ = 0.5, $\omega_n$ = 4 rad/s). Where do they map for $T$ = 0.1 s?

**Solution.** $z = e^{sT} = e^{-0.2}e^{\pm j0.3464}$: magnitude $e^{-0.2}$ = **0.819** and angle $\pm 0.3464$ rad = ±**19.8**°.

**Units check.** $sT$ is dimensionless.

**Sanity check.** The angle is $\omega_dT$; 19.8° per sample means about 18 samples per damped oscillation period, comfortably fast sampling.

### Example 15-11.2 · ZOH equivalents (tier B)

**Setup.** Find the ZOH equivalents for $T$ = 0.1 s of (a) $P = 1/(s + 1)$ and (b) the servo $P = 1/[s(s + 1)]$.

**Solution.** (a) $G(z) = (1 - e^{-0.1})/(z - e^{-0.1})$ = **0.0952**/(z − **0.905**).

(b) The general result (by $(1 - z^{-1})\mathcal{Z}\{P/s\}$, or the lab's exact discretization) is

$$
G(z) = \frac{(T - 1 + e^{-T})z + (1 - e^{-T} - Te^{-T})}{(z - 1)(z - e^{-T})} = \frac{0.00484z + 0.00468}{z^2 - 1.905z + 0.905} .
$$

The integrator maps to the pole at $z$ = 1, and the ZOH introduces a zero at $z$ = −0.967, near −1.

**Units check.** Discrete transfer functions are dimensionless ratios of sample sequences.

**Sanity check.** At DC ($z$ = 1) case (a) gives 0.0952/0.0952 = 1, the plant's DC gain, as it must.

### Example 15-11.3 · A Tustin PI controller and the effect of $T$ (tier B)

**Setup.** Discretize 15-08's thermal PI controller ($K_p$ = 14 W/K, $K_i$ = 5 W/(K·s), plant $0.5/(10s + 1)$ K/W) with Tustin at $T$ = 0.5 s and at $T$ = 2 s. Give the difference equation and compare overshoot and phase margin with the continuous design (12.6%, 72.4°).

**Solution.** With $T$ = 0.5 s: $u_k = u_{k-1} + $ **15.25** $e_k$ **− 12.75** $e_{k-1}$. Simulating the sampled loop (exactly, with the ZOH plant): overshoot **15.7**%, phase margin **61.7**° (from the discrete loop gain on the unit circle). With $T$ = 2 s: $u_k = u_{k-1} + 19e_k - 9e_{k-1}$; overshoot **72.2**% and phase margin **29.9**°.

At $T$ = 0.5 s, about 20 samples per plant time constant, the digital loop is close to the analog one (losing about 11° of margin). At $T$ = 2 s the first sample applies a 19 W step for 2 s, the hold's delay is large, and the response overshoots badly even though the closed-loop poles are well inside the unit circle.

**Units check.** $K_iT/2$ in W/K, like $K_p$.

**Sanity check.** The hold-delay estimate $\omega_cT/2$ at the continuous crossover (0.766 rad/s) predicts **11.0**° of loss at $T$ = 0.5 s, close to the **10.8**° found.

### Example 15-11.4 · Phase lost to sampling (tier B)

**Setup.** The servo $L = 100/[s(s + 10)]$ of 15-07 (crossover 7.86 rad/s, PM 51.8°) is implemented with a ZOH and $T$ = 0.05 s, with the proportional gain in the digital controller. Predict and compute the new phase margin.

**Solution.** The hold costs about $\omega_cT/2 = 7.86 \times 0.025$ rad = 11.26°, predicting 51.83° − 11.26° = **40.6**°. The exact discrete loop gain gives crossover at 7.82 rad/s and PM = **40.8**°, and now a finite gain margin of **4.36** where the continuous loop had none.

**Units check.** $\omega T$ in radians.

**Sanity check.** The $T/2$ rule is accurate here because $\omega_cT$ = 0.39 rad, well below π.

### Example 15-11.5 · Sampling shrinks the stable gain range (tier C)

**Setup.** Proportional control of $1/[s(s + 1)]$ through a ZOH is stable for every $K > 0$ in continuous time. Find the largest stable $K$ for $T$ = 0.1 s and $T$ = 1 s. Then, for $K$ = 1 and $T$ = 0.5 s, find the closed-loop poles, the overshoot and the peak time.

**Solution.** With $G(z)$ from Example 15-11.2 (in general $T$), the characteristic polynomial $z^2 + a_1z + a_0$ has $a_0 = e^{-T} + K(1 - e^{-T} - Te^{-T})$. The binding Jury condition is $a_0 < 1$, giving $K_{max} = (1 - e^{-T})/(1 - e^{-T} - Te^{-T})$: **20.3** for $T$ = 0.1 s and **2.39** for $T$ = 1 s.

For $K$ = 1 and $T$ = 0.5 s, the closed-loop poles are $0.75 \pm j0.366$ (magnitude **0.835**). Simulating: overshoot **28.7**% at **3.45** s, against 16.3% for the continuous loop. The lab's ngspice circuit, with a switch and hold capacitor as the sampler, measures 28.6% at 3.45 s.

**Units check.** $K$ in 1/s² (continuous loop gain units).

**Sanity check.** As $T \to 0$, $K_{max} \to \infty$ (expand: $K_{max} \approx 2/T$), recovering the continuous result.

### Example 15-11.6 · Delay in a digital power controller (tier C)

**Setup.** A digitally controlled buck converter samples its output once per 1 MHz switching period and updates the PWM duty cycle in the next period, a total delay of about $1.5T$ (half a period of hold plus one period of computation and update). How much phase does this cost at a 60 kHz crossover? What if the switching frequency rises to 2 MHz?

**Solution.** $\Delta\phi = 360° \times f_c \times 1.5T = 360 \times 60 \times 10^3 \times 1.5 \times 10^{-6}$ = **32.4**°. At 2 MHz the delay halves and the cost is **16.2**°.

**Units check.** Hz × s = cycles; × 360° per cycle.

**Sanity check.** Compared with Example 15-09.6's Type III budget, 32° is most of the margin. This is why digital controllers for fast converters use high sample rates, predictive (delay-compensating) control laws, or analog inner loops.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 15-11.1a | pole magnitude | 0.819 | — |
| Ex 15-11.1b | pole angle | 19.8 | ° |
| Ex 15-11.2a | gain of (a) | 0.0952 | — |
| Ex 15-11.2b | pole of (a) | 0.905 | — |
| Ex 15-11.2c | numerator z coefficient of (b) | 0.00484 | — |
| Ex 15-11.2d | numerator constant of (b) | 0.00468 | — |
| Ex 15-11.2e | zero of (b) | −0.967 | — |
| Ex 15-11.3a | b0 at T = 0.5 s | 15.25 | W/K |
| Ex 15-11.3b | b1 at T = 0.5 s | −12.75 | W/K |
| Ex 15-11.3c | overshoot at T = 0.5 s | 15.7 | % |
| Ex 15-11.3d | phase margin at T = 0.5 s | 61.7 | ° |
| Ex 15-11.3e | overshoot at T = 2 s | 72.2 | % |
| Ex 15-11.3f | phase margin at T = 2 s | 29.9 | ° |
| Ex 15-11.3g | predicted loss at T = 0.5 s | 11.0 | ° |
| Ex 15-11.3h | actual loss at T = 0.5 s | 10.8 | ° |
| Ex 15-11.4a | predicted phase margin | 40.6 | ° |
| Ex 15-11.4b | exact phase margin | 40.8 | ° |
| Ex 15-11.4c | gain margin | 4.36 | — |
| Ex 15-11.5a | largest K at T = 0.1 s | 20.3 | 1/s² |
| Ex 15-11.5b | largest K at T = 1 s | 2.39 | 1/s² |
| Ex 15-11.5c | pole magnitude at K = 1, T = 0.5 s | 0.835 | — |
| Ex 15-11.5e | overshoot | 28.7 | % |
| Ex 15-11.5f | peak time | 3.45 | s |
| Ex 15-11.6a | phase cost at 1 MHz | 32.4 | ° |
| Ex 15-11.6b | phase cost at 2 MHz | 16.2 | ° |

## 5. Simulate it

The lab, [labs/15-11-lab](../labs/15-11-lab/README.md), provides `digital.py`: ZOH and Tustin discretization, a Tustin PI difference equation, an exact sampled-loop simulator (continuous plant between samples), discrete margins on the unit circle and the second-order Jury test. You:

1. **Discretize** Example 15-11.2's plants and check them against the matrix-exponential discretization.
2. **Sweep the sample period** for Example 15-11.3's PI loop and plot overshoot and phase margin against $T$.
3. **Run `sample_hold.cir`**, a switch-and-capacitor sampler in ngspice, and compare with the ideal ZOH simulation.
4. **Compare discretization methods** (forward Euler, backward Euler, Tustin, prewarped Tustin) for a lead compensator at a coarse sample rate.

**Guided exercise (predict, then run).** **Before Part 3,** predict whether the sampled loop with $K$ = 1 overshoots more or less than the continuous loop's 16.3%, and roughly by how much, using the $T/2$ delay rule. (More: the hold costs about $0.79 \times 0.25$ rad ≈ 11° at the continuous crossover, so expect roughly 25–30%.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Faster sampling | Smaller hold delay; closer to analog behaviour | Processor or logic power; ADC speed; coefficient sensitivity near $z$ = 1 | System / firmware architect |
| Lower computation latency | Phase margin, achievable crossover | Hardware acceleration, simpler algorithms | Digital designer |
| Higher ADC resolution | Finer control, fewer limit cycles | Cost, power, conversion time | Mixed-signal architect |
| Tustin with prewarping | Exact match at the critical frequency | Slight mismatch elsewhere | Control engineer |
| Anti-aliasing filter | Rejects noise above Nyquist | Its own phase lag at crossover | Analog / system designer |
| Velocity-form PI with clamping | Simple anti-windup, bumpless transfer | Needs care with setpoint changes | Firmware engineer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Pole mapping | $z = e^{sT}$; stable means inside the unit circle | §3.1 |
| Phase lag of a ZOH | about $\omega T/2$ radians | §3.5 |
| Sample rate rule | 10 to 30 times the closed-loop bandwidth | §3.5 |
| Digital power control delay | about 1 to 1.5 switching periods | Example 15-11.6 |
| Second-order Jury test | $\lvert a_0\rvert < 1$, $1 \pm a_1 + a_0 > 0$ | §3.4 |
| Tustin PI | $u_k = u_{k-1} + (K_p + K_iT/2)e_k + (-K_p + K_iT/2)e_{k-1}$ | §3.3 |

## 8. Common mistakes

- **Ignoring the hold.** Designing in continuous time and then sampling slowly loses $\omega_cT/2$ of phase margin.
- **Forgetting computation delay.** The time from ADC sample to output update is extra delay, often as large as the hold's.
- **Forward Euler at coarse sampling.** It can turn a stable continuous controller unstable.
- **Discretizing without prewarping a notch or a lead at a critical frequency.** Tustin warps frequencies; the zero lands in the wrong place.
- **Letting fixed-point integrators wrap around.** Saturate them and add anti-windup.
- **Checking only the sample values.** A sampled loop can ring between samples (intersample ripple); simulate the continuous plant between samples, as the lab does.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

These are established practice; no perishable figures are quoted.

- **Digital controllers are the default** in motor drives, many power supplies and PMICs, and all firmware-based thermal and power management **[Established]**.
- **Digital power controllers compensate for their own delay** with high sample rates, predictive control laws or hybrid analog/digital architectures; their datasheets specify the compensator as programmable coefficients **[Established]**.
- **Controller code is generated** from continuous or discrete designs by tools that discretize, scale to fixed point and check for overflow **[Established]**.

### Why it matters commercially

- **Programmability is a product feature.** A digital controller's coefficients can be tuned per board or per customer without changing parts, which shortens design cycles.
- **Delay is the hidden cost.** The extra phase lag of a digital loop means lower bandwidth than an equivalent analog loop at the same switching frequency, unless the design spends silicon on speed.
- **Firmware loops have product-level consequences.** A thermal loop sampled too slowly lets a processor overshoot its temperature limit; one sampled too fast wastes power.

### Marketing vs Reality

- **"Digital control for faster transients."** *Reality:* digital adds delay; faster transients come from nonlinear or predictive features layered on top. *Sanity check:* ask for the loop's crossover and phase margin, and the controller's sample-to-update latency.
- **"Fully programmable compensation."** *Reality:* within limits set by the sample rate and word lengths. *Sanity check:* ask for the coefficient resolution and the maximum crossover relative to the switching frequency.
- **"1 MHz control loop."** *Reality:* the sample rate is not the bandwidth; expect a crossover a decade or more lower. *Sanity check:* ask for the measured crossover.

### Questions for engineering leaders

1. **"What is the total delay from sampling to actuation, and what does it cost at crossover?"**
   *Strong:* a number, with the phase budget. *Evasive:* "it is fast".
2. **"How was the controller discretized, and was it checked in the discrete domain?"**
   *Strong:* method, prewarping, discrete margins. *Evasive:* continuous design only.
3. **"What word lengths do the coefficients and states use, and how are overflow and windup handled?"**
   *Strong:* explicit analysis and saturation. *Evasive:* floating point assumed without checking.
4. **"Is there intersample ripple, and how was it checked?"**
   *Strong:* continuous-time simulation of the sampled loop. *Evasive:* sample values only.

## 10. Concept check

**Q1.** Where must the poles of a stable discrete system lie, and why?

<details><summary>Answer</summary>

Strictly inside the unit circle: a pole $z$ gives a mode $z^k$, which decays only if $\lvert z\rvert < 1$. Equivalently, $z = e^{sT}$ maps the left half-plane inside the circle.

</details>

**Q2.** Why is the ZOH equivalent of a plant exact at the sample instants?

<details><summary>Answer</summary>

Because the hold makes the input constant between samples, the state equations can be integrated exactly over each interval: $\mathbf{x}_{k+1} = e^{AT}\mathbf{x}_k + \Gamma u_k$.

</details>

**Q3.** How much phase does a zero-order hold cost at crossover?

<details><summary>Answer</summary>

About $\omega_cT/2$ radians, since the held staircase lags a smooth signal by half a sample on average.

</details>

**Q4.** What is the advantage of Tustin's method over forward Euler?

<details><summary>Answer</summary>

Tustin maps the stable left half-plane exactly onto the unit disk, so stable continuous controllers stay stable; forward Euler can map them outside the circle at coarse sampling.

</details>

**Q5.** Why can a sampled loop be unstable when its continuous version is stable for all gains?

<details><summary>Answer</summary>

The hold and computation add phase lag that grows with frequency, like a delay; with enough gain the loop crosses −180° with $\lvert L\rvert > 1$.

</details>

**Q6.** What is the velocity form of a PI controller, and why does it help with windup?

<details><summary>Answer</summary>

It computes the change in output, $u_k = u_{k-1} + \Delta u_k$. Clamping $u_k$ at the actuator limit stops further accumulation without a separate integrator state to manage.

</details>

**Q7.** Why does a digital buck converter's controller limit its crossover more than an analog one at the same switching frequency?

<details><summary>Answer</summary>

It adds about 1 to 1.5 switching periods of delay (sampling, computation, PWM update), costing tens of degrees of phase at a crossover near a tenth of the switching frequency.

</details>

Practice: [Problems 15-11](../problems/15-11-problems.md) · [Solutions](../solutions/15-11-solutions.md)

## 11. Key terms

[Zero-order hold](../../../reference/glossary.md#zero-order-hold) · [ZOH equivalent](../../../reference/glossary.md#zoh-equivalent) · [Tustin transformation](../../../reference/glossary.md#tustin-transformation) · [Frequency prewarping](../../../reference/glossary.md#frequency-prewarping) · [Jury stability test](../../../reference/glossary.md#jury-stability-test) · [Velocity-form PI](../../../reference/glossary.md#velocity-form-pi) · [Nyquist frequency](../../../reference/glossary.md#nyquist-frequency)

## 12. Connections

- **Builds on:** the z-transform ([11-09](../../11-signals-and-systems/chapters/11-09-z-transform.md)); sampling ([11-10](../../11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md)); margins and delay ([15-07](15-07-frequency-domain-design.md)); PID and windup ([15-08](15-08-pid-control.md)); exact discretization ([15-10](15-10-state-space-introduction.md)).
- **Next:** [15-12 Applications: PLLs, Voltage Regulators and Thermal Management](15-12-control-applications-pll-regulators-thermal.md).
- **Used later:** digital power control ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and M. Workman, *Digital Control of Dynamic Systems* (the standard reference on sampled-data design).
- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 8 (digital control).
- K. J. Åström and B. Wittenmark, *Computer-Controlled Systems* (sampling, discretization, implementation).

## 14. Sources

1. Franklin, Powell and Workman; Åström and Wittenmark (Further study): sampled-data control (textbook material).

This chapter has no perishable industry figures; its practitioner statements are tagged [Established]. Every number in the examples is recomputed by the verify script (ZOH by the matrix exponential and by scipy, discrete margins on the unit circle, sampled loops simulated exactly between samples), and Example 15-11.5's loop is confirmed with an ngspice switch-and-capacitor sampler.
