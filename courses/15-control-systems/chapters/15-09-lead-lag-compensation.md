<!-- status: verified -->
# 15-09 · Lead and Lag Compensation

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The compensator-design material of a first course in feedback control: lead, lag and lead-lag compensators designed on the Bode plot and with the root locus, and their circuit realizations (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 5–6; Nise, *Control Systems Engineering*, ch. 9 and 11; Ogata, *Modern Control Engineering*, ch. 6–7) |
| **Prerequisites** | [15-06 Root Locus](15-06-root-locus.md), [15-07 Frequency-Domain Design](15-07-frequency-domain-design.md), [15-08 PID Control](15-08-pid-control.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Describe lead and lag compensators by their pole–zero locations, Bode plots and maximum phase, and relate them to PD and PI control.
2. Design a lead compensator on the Bode plot for a phase-margin target, and a lag compensator to raise an error constant without moving crossover.
3. Design a lead compensator with the root locus from an angle deficiency.
4. Combine lead and lag, and predict the time-domain cost of each (overshoot, the slow tail of a lag).
5. Realize compensators with RC networks and op-amps, and design a Type III compensator for an LC double pole as in a switching regulator.

---

## 1. Big picture

Proportional gain moves a loop along its root locus and slides its Bode magnitude up and down, but it cannot reshape either. When gain alone cannot meet the specification, as in the servo of 15-06 that could not settle faster, or a loop whose accuracy needs more gain than its phase margin allows, a **compensator** reshapes the loop. Two simple building blocks cover most needs. A **lead** compensator, a zero followed by a pole, adds phase near crossover: more margin, more speed. A **lag** compensator, a pole followed by a zero, adds gain at low frequency without disturbing crossover: more accuracy. They are the filtered, practical forms of PD and PI control (15-08), and in analog and power design they appear as the "Type II" and "Type III" compensator networks around an error amplifier.

- **Switching regulators** are compensated with Type II (PI plus a pole) or Type III (two zeros, two poles) networks whose components the designer chooses (22-07, 15-12).
- **Op-amp circuits** add lead with a capacitor across the feedback resistor or a feedforward capacitor, to restore phase margin lost to load or input capacitance (12-06).
- **Servo and positioning loops** combine lead for speed with lag for accuracy.
- **Every compensator is a trade**: lead costs noise and high-frequency gain; lag costs a slow settling tail.

## 2. Intuition first

**Lead: look ahead.** A lead network's output responds to how fast its input is changing as well as to its value, so it acts a little early: it leads. On a Bode plot this is a bump of positive phase between the zero and the pole. Placed at crossover, the bump moves the phase away from −180°, adding margin and allowing a higher crossover.

**Lag: patience at low frequency.** A lag network has extra gain at low frequency and gets out of the way at high frequency. Placed well below crossover, it raises the loop gain where steady-state accuracy is decided (15-04) while leaving the crossover region, and thus the margins, almost untouched.

**An analogy: hedging a portfolio.** A lead is like a momentum overlay: it reacts to trends, improves responsiveness, but trades on noise if pushed too far. A lag is like a slow rebalancing rule that fixes long-run drift without affecting day-to-day behaviour. The analogy breaks down because these filters are linear and exact: their benefits and costs are set by pole–zero placement and can be computed in advance, which market strategies cannot.

## 3. Theory

### 3.1 The lead compensator

$$
C_{lead}(s) = \frac{1 + \alpha Ts}{1 + Ts}, \qquad \alpha > 1 ,
$$

has a zero at $-1/(\alpha T)$ and a pole $\alpha$ times farther out at $-1/T$. Its phase, $\phi(\omega) = \arctan(\alpha\omega T) - \arctan(\omega T)$, is positive and peaks at the geometric mean of the corner frequencies. Setting $d\phi/d\omega = 0$:

$$
\omega_m = \frac{1}{T\sqrt\alpha}, \qquad \sin\phi_{max} = \frac{\alpha - 1}{\alpha + 1}, \qquad \alpha = \frac{1 + \sin\phi_{max}}{1 - \sin\phi_{max}} .
$$

(The derivation: with $x = \omega T$, $\tan\phi = (\alpha - 1)x/(1 + \alpha x^2)$, which peaks at $x = 1/\sqrt\alpha$, giving $\tan\phi_{max} = (\alpha - 1)/(2\sqrt\alpha)$, equivalent to the sine form.) The magnitude rises from 1 at DC to $\alpha$ at high frequency, and equals $\sqrt\alpha$ at $\omega_m$. More than about 60° from one stage needs $\alpha > 14$ and amplifies high-frequency noise by that much; two stages are used instead.

### 3.2 The lag compensator

$$
C_{lag}(s) = \frac{1 + s/z}{1 + s/p}, \qquad z > p ,
$$

has DC gain 1 and high-frequency gain $p/z = 1/\beta$, with $\beta = z/p > 1$. Equivalently, multiply by $\beta$ to keep the high-frequency gain at 1 and raise the DC gain by $\beta$. Its phase is negative, between the pole and the zero. Placed a decade below crossover, it costs only about $\arctan(0.1) - \arctan(0.1/\beta) \approx 5°$ of phase there.

A lag compensator with $p \to 0$ becomes a PI controller; a lead with $T \to 0$ becomes a PD. The lead and lag are their **filtered** versions: finite high-frequency gain for the lead, finite DC gain for the lag.

### 3.3 Lead design on the Bode plot

1. Choose the static gain $K$ for the error constant (15-04).
2. Measure the uncompensated phase margin $\text{PM}_0$ at that gain.
3. The lead must supply $\phi_{max} = \text{PM}_{target} - \text{PM}_0 + 5°$ to $10°$ (the extra covers the crossover's move to a higher frequency, where the plant has more lag).
4. Compute $\alpha$ from $\phi_{max}$.
5. The lead raises the gain by $\sqrt\alpha$ at $\omega_m$, so place $\omega_m$ where the uncompensated $\lvert KL\rvert = 1/\sqrt\alpha$: that becomes the new crossover, and the lead's peak phase arrives exactly there.
6. $T = 1/(\omega_m\sqrt\alpha)$; check the margins and simulate.

### 3.4 Lag design on the Bode plot

1. Choose $K$ for the error constant.
2. Find the frequency $\omega_c'$ where the uncompensated phase is $-180° + \text{PM}_{target} + 5°$; it will become the new crossover.
3. Attenuate the gain there to 1: $\beta = \lvert KL(j\omega_c')\rvert$.
4. Put the lag's zero a decade below, $z = \omega_c'/10$, and its pole at $p = z/\beta$.

The lag lowers crossover, so the loop becomes slower, and its pole–zero pair near the origin is a doublet (15-03 §3.6): the response creeps the last few percent with time constant $1/z$.

### 3.5 Lead design with the root locus

To place a closed-loop pole at a desired point $s_d$ (15-06), compute the **angle deficiency**: the angle the plant misses from −180° at $s_d$,

$$
\phi = -180° - \angle P(s_d) .
$$

Choose a lead zero (often directly below $s_d$ or near the plant's second pole), then place the lead pole so that $\angle(s_d - z_c) - \angle(s_d - p_c) = \phi$. The gain follows from the magnitude condition. Check the other closed-loop poles: a pole near the compensator zero partly cancels it, but the zero still shapes the response.

### 3.6 Realization

- **Passive lead.** $R_1$ in parallel with $C_1$ in series, $R_2$ to ground: $H = \dfrac{R_2}{R_1 + R_2}\cdot\dfrac{1 + sR_1C_1}{1 + s(R_1\parallel R_2)C_1}$, with $\alpha = (R_1 + R_2)/R_2$. It attenuates by $1/\alpha$ at DC, which a following gain stage must make up.
- **Active compensators.** An inverting op-amp with RC networks in its input and feedback arms realizes lead, lag, PI and PID, and the **Type II** (integrator, one zero, one pole) and **Type III** (integrator, two zeros, two poles) compensators of switching regulators (Example 15-09.6).
- **Digital.** A microcontroller implements the same transfer functions as difference equations (15-11).

### 3.7 Compensating an LC double pole

A buck converter's control-to-output response is a second-order LC filter, $V_{in}/(LCs^2 + (L/R)s + 1)$, with a resonance at $\omega_0 = 1/\sqrt{LC}$ and quality factor $Q = R\sqrt{C/L}$. Above $\omega_0$ its phase approaches −180°, so a simple integrator controller would cross over with no margin. A **Type III** compensator, $\omega_I(1 + s/\omega_z)^2/[s(1 + s/\omega_p)^2]$, puts two zeros near $\omega_0$ to add up to 180° of lead, and two poles above crossover to restore attenuation of switching noise. Crossover is typically placed at a tenth or less of the switching frequency (22-07).

## 4. Worked examples

### Example 15-09.1 · Anatomy of a lead (tier A)

**Setup.** A lead compensator has $\alpha$ = 10. Find its maximum phase, its gain at $\omega_m$ and its high-frequency gain.

**Solution.** $\sin\phi_{max} = 9/11$, so $\phi_{max}$ = **54.9**°. At $\omega_m$ the gain is $\sqrt{10}$, or **10** dB; at high frequency it is 10, or **20** dB.

**Units check.** Ratios and degrees.

**Sanity check.** The lab's passive network with $\alpha$ = 10 measures 54.9° in ngspice at 5.59 kHz, the geometric mean of its 1.77 kHz zero and 17.7 kHz pole.

### Example 15-09.2 · Lead design on the Bode plot (tier B)

**Setup.** A servo plant $P = 1/[s(s + 1)]$ needs $K_v$ = 10 s⁻¹ and a phase margin of at least 45°. Design a lead compensator.

**Solution.** $K_v = \lim sKP = K$, so $K$ = 10. Uncompensated: $\omega_c$ = **3.08** rad/s and PM = **18.0**°, which gives **60.5**% overshoot and a 2% settling time of **7.32** s. The lead must add $45 - 18.0 + 10 = $ **37.0**°, so $\alpha$ = **4.03**. The uncompensated $\lvert 10P\rvert$ equals $1/\sqrt{4.03}$ at **4.42** rad/s; that becomes $\omega_m$ and the new crossover. Then $T = 1/(\omega_m\sqrt\alpha)$ = 0.1126 s: the zero is at **2.20** rad/s and the pole at **8.88** rad/s.

$$
C(s) = 10\,\frac{1 + 0.454s}{1 + 0.1126s} .
$$

Result: PM = **49.8**°, overshoot **22.4**%, 2% settling **1.23** s. The settling time fell sixfold and $K_v$ is unchanged.

**Units check.** $T$ in seconds; $\alpha T$ = 0.454 s.

**Sanity check.** The crossover rose from 3.08 to 4.42 rad/s: lead buys speed as well as margin.

### Example 15-09.3 · Lag design for the same specification (tier B)

**Setup.** Meet the same specification ($K_v$ = 10, PM ≥ 45°; aim for 50°) with a lag compensator instead.

**Solution.** The uncompensated phase is $-90° - \arctan\omega$; it equals $-180° + 50° + 5° = -125°$ at $\omega_c' = \tan 35°$ = **0.700** rad/s. There $\lvert 10P\rvert$ = 11.7, so $\beta$ = **11.7**. The zero goes at $\omega_c'/10$ = **0.0700** rad/s and the pole at $0.07/11.7$ = **0.00599** rad/s. Result: PM = **49.7**°, overshoot **22.3**%, but the 2% settling time is **19.7** s.

**Units check.** All frequencies in rad/s.

**Sanity check.** Lag keeps $K_v$ = 10 by restoring gain at DC; it gets its margin by lowering crossover to 0.70 rad/s, a sixth of the lead design's. The lag's doublet near the origin then drags out settling: a sixteenfold slower loop for the same margin.

### Example 15-09.4 · Lead design with the root locus (tier B)

**Setup.** For $P = 1/[s(s + 1)]$, place the dominant closed-loop poles at $s_d = -2 \pm j2\sqrt3$ ($\zeta$ = 0.5, $\omega_n$ = 4 rad/s) with a lead whose zero is at −2.

**Solution.** $\angle P(s_d) = -\angle(s_d) - \angle(s_d + 1) = -120° - 106.1° = -226.1°$, so the deficiency is **46.1**°. The zero at −2 sits directly below $s_d$ and contributes 90°; the pole must contribute $90° - 46.1° = 43.9°$, which puts it at $-2 - 3.464/\tan 43.9°$ = **−5.6**. The magnitude condition gives $K = \lvert s_d\rvert\,\lvert s_d + 1\rvert\,\lvert s_d + 5.6\rvert/\lvert s_d + 2\rvert$ = **20.8**:

$$
C(s) = 20.8\,\frac{s + 2}{s + 5.6} .
$$

The closed-loop poles are $-2 \pm j3.46$ and **−2.6**; the step response overshoots by **27.4**% (more than the 16.3% of $\zeta$ = 0.5, because of the zero at −2 and the extra pole at −2.6). The velocity constant is $K_v = 20.8 \times 2/5.6$ = **7.43** s⁻¹.

**Units check.** $K$ has units of 1/s² (as $L$ must be dimensionless with two plant poles).

**Sanity check.** The constant-sum rule: $-2 - 2 - 2.6 = -6.6 = -1 - 5.6$, the sum of the open-loop poles.

### Example 15-09.5 · Lead and lag together (tier C)

**Setup.** Keep Example 15-09.2's lead but raise $K_v$ to 50 s⁻¹ with a lag of $\beta$ = 5, its zero a decade below the 4.42 rad/s crossover.

**Solution.** The lag zero is at **0.442** rad/s and its pole at 0.442/5 = **0.0885** rad/s; the gain becomes $10 \times 5$, so $K_v$ = **50** s⁻¹. The crossover stays at 4.44 rad/s and the phase margin falls by about 5°, to **45.2**°. Overshoot rises to **30.2**%, and the 2% settling time is **1.29** s: the lag's tail is now small enough to stay inside the 2% band.

**Units check.** As before.

**Sanity check.** A lag placed a decade below crossover costs about $\arctan(0.1) \approx 5.7°$ minus a little, consistent with the 4.6° drop from 49.8° to 45.2°.

### Example 15-09.6 · A Type III compensator for a buck converter (tier C)

**Setup.** A buck converter's control-to-output response is $V_{in}/(LCs^2 + (L/R)s + 1)$ with $V_{in}$ = 5 V, $L$ = 1 µH, $C$ = 100 µF and $R$ = 1 Ω (illustrative values, with ideal components). Use a Type III compensator $\omega_I(1 + s/\omega_z)^2/[s(1 + s/\omega_p)^2]$ with poles at 300 kHz and crossover at 60 kHz. Compare zeros at $f_0$ with zeros at $f_0/2$.

**Solution.** $f_0 = 1/(2\pi\sqrt{LC})$ = **15.9** kHz and $Q = R\sqrt{C/L}$ = **10**: a sharp resonance. The phase at 60 kHz is a sum of terms: the integrator gives −90°, the plant about −178°, the two poles $-2\arctan(60/300) = -22.6°$, and the two zeros $+2\arctan(60/f_z)$.

- Zeros at $f_0$ (+150.3°): setting $\lvert L\rvert = 1$ at 60 kHz gives $\omega_I$ = **6.81 × 10⁴** s⁻¹ and PM = **39.3**°, GM = **18.9** dB.
- Zeros at $f_0/2$ (+164.9°): $\omega_I$ = **1.79 × 10⁴** s⁻¹ and PM = **53.9**°, GM = **19.5** dB.

Placing the zeros below the resonance buys about 15° of margin, because the zeros' full lead is available by the time the plant's phase has fallen to −180°.

**Units check.** $\omega_I$ in 1/s; $L$ dimensionless.

**Sanity check.** With $Q$ = 10 the plant's gain peaks 20 dB at $f_0$; the loop gain still crosses 0 dB only once, at 60 kHz (the lab checks), so the simple margins apply.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Txt 15-09.a | lead phase at α = 2 | 19.5 | ° |
| Txt 15-09.b | lead phase at α = 4 | 36.9 | ° |
| Txt 15-09.c | lead phase at α = 16 | 61.9 | ° |
| Txt 15-09.d | α for 60° | 14 | — |
| Ex 15-09.1a | maximum phase | 54.9 | ° |
| Ex 15-09.1b | gain at ωm | 10 | dB |
| Ex 15-09.1c | high-frequency gain | 20 | dB |
| Ex 15-09.2a | uncompensated crossover | 3.08 | rad/s |
| Ex 15-09.2b | uncompensated phase margin | 18.0 | ° |
| Ex 15-09.2c | uncompensated overshoot | 60.5 | % |
| Ex 15-09.2d | uncompensated settling | 7.32 | s |
| Ex 15-09.2e | required lead | 37.0 | ° |
| Ex 15-09.2f | α | 4.03 | — |
| Ex 15-09.2g | ωm (new crossover) | 4.42 | rad/s |
| Ex 15-09.2h | zero | 2.20 | rad/s |
| Ex 15-09.2i | pole | 8.88 | rad/s |
| Ex 15-09.2j | phase margin | 49.8 | ° |
| Ex 15-09.2k | overshoot | 22.4 | % |
| Ex 15-09.2l | settling | 1.23 | s |
| Ex 15-09.3a | new crossover | 0.700 | rad/s |
| Ex 15-09.3b | β | 11.7 | — |
| Ex 15-09.3c | zero | 0.0700 | rad/s |
| Ex 15-09.3d | pole | 0.00599 | rad/s |
| Ex 15-09.3e | phase margin | 49.7 | ° |
| Ex 15-09.3f | overshoot | 22.3 | % |
| Ex 15-09.3g | settling | 19.7 | s |
| Ex 15-09.4a | angle deficiency | 46.1 | ° |
| Ex 15-09.4b | lead pole | −5.6 | 1/s |
| Ex 15-09.4c | K | 20.8 | 1/s² |
| Ex 15-09.4d | third closed-loop pole | −2.6 | 1/s |
| Ex 15-09.4e | overshoot | 27.4 | % |
| Ex 15-09.4f | Kv | 7.43 | 1/s |
| Ex 15-09.5a | lag zero | 0.442 | rad/s |
| Ex 15-09.5b | lag pole | 0.0885 | rad/s |
| Ex 15-09.5c | Kv | 50 | 1/s |
| Ex 15-09.5d | phase margin | 45.2 | ° |
| Ex 15-09.5e | overshoot | 30.2 | % |
| Ex 15-09.5f | settling | 1.29 | s |
| Ex 15-09.6a | resonance | 15.9 | kHz |
| Ex 15-09.6b | Q | 10 | — |
| Ex 15-09.6c | ωI, zeros at f0 | 6.81e4 | 1/s |
| Ex 15-09.6d | phase margin, zeros at f0 | 39.3 | ° |
| Ex 15-09.6e | gain margin, zeros at f0 | 18.9 | dB |
| Ex 15-09.6f | phase margin, zeros at f0/2 | 53.9 | ° |
| Ex 15-09.6g | gain margin, zeros at f0/2 | 19.5 | dB |
| Ex 15-09.6h | ωI, zeros at f0/2 | 1.79e4 | 1/s |

## 5. Simulate it

The lab, [labs/15-09-lab](../labs/15-09-lab/README.md), provides `compensate.py`: lead and lag formulas, the Bode-plot design recipes of §3.3–3.4 as functions, and the RC values of a passive lead. You:

1. **Measure a lead network** in ngspice (`lead_network.cir`): its maximum phase and the frequency where it occurs.
2. **Design lead and lag** for Example 15-09.2's specification and overlay their Bode plots and step responses.
3. **Design by root locus** (Example 15-09.4) and watch the closed-loop pole near the compensator zero.
4. **Compensate a buck converter** (Example 15-09.6): sweep the Type III zero location and plot the phase margin.

**Guided exercise (predict, then run).** **Before Part 2,** predict which compensated loop rises faster and which settles faster. (The lead does both: higher crossover; the lag's slow doublet dominates its settling.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Lead ratio $\alpha$ | Phase margin and crossover (speed) | High-frequency gain (noise, actuator activity) rises by $\alpha$ | Control / analog designer |
| Lead placement $\omega_m$ | Margin exactly at crossover | Sensitive to plant uncertainty: a misplaced lead adds little phase | Control designer |
| Lag ratio $\beta$ | Low-frequency gain (error constants, disturbance rejection) | A slow settling tail; a few degrees of phase at crossover | Control designer |
| Lag zero placement (decade below crossover) | Little phase cost | Slower tail the lower it is placed | Control designer |
| Type III zero placement relative to $f_0$ | Phase margin with an LC double pole | Mid-band gain shape; sensitivity to $Q$ and component tolerance | Power-electronics designer |
| Compensator realization (passive, op-amp, digital) | Cost, area, flexibility | Attenuation (passive), op-amp bandwidth and noise, sampling delay (digital) | Circuit / firmware designer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Lead maximum phase | $\arcsin[(\alpha - 1)/(\alpha + 1)]$: 19.5° at α = 2, 36.9° at 4, 54.9° at 10, 61.9° at 16 | §3.1 |
| Lead frequency and gain at the peak | $\omega_m = 1/(T\sqrt\alpha)$, gain $\sqrt\alpha$ | §3.1 |
| Lag zero placement | about a decade below crossover, costing about 5° | §3.2 |
| Extra lead allowance | 5° to 10° above the computed deficiency | §3.3 |
| Type III compensator | integrator, two zeros near $f_0$, two poles above crossover; crossover ≤ $f_{sw}/10$ | §3.7 |

## 8. Common mistakes

- **Placing the lead's peak at the old crossover.** The lead raises the gain, so crossover moves; place $\omega_m$ at the new crossover (§3.3 step 5).
- **Forgetting the passive lead's attenuation.** A passive network loses a factor $\alpha$ of gain at DC; a gain stage must restore it, or $K_v$ falls.
- **Placing a lag too close to crossover.** It then costs much more than 5° of phase.
- **Ignoring the lag's slow tail.** It can dominate settling to 1% or better.
- **Asking one lead stage for more than about 60°.** Use two stages; a single huge $\alpha$ amplifies noise badly.
- **Designing around a nominal LC resonance only.** Load and capacitor tolerances move $f_0$ and $Q$; check margins at the extremes.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

These are established practice; no perishable figures are quoted.

- **Switching-regulator controllers expose their compensation.** Many voltage-mode and current-mode controllers bring the error amplifier's output to a pin, where the designer connects a Type II or Type III network; others integrate the network and let the designer choose among settings **[Established]**.
- **Op-amp circuits use feedforward and feedback capacitors** as lead compensation, and data sheets show the resulting phase margin against load capacitance **[Established]**.
- **Digital controllers implement lead–lag and PID filters in firmware or hardware**, with the sampling delay counted as phase lag (15-11) **[Established]**.

### Why it matters commercially

- **Compensation sets transient performance.** A regulator's load-step response, a servo's settling time and an amplifier's ringing are all set by the compensation, so it is often the last design step and the first suspect when something rings.
- **Customer-selected compensation shifts risk.** When customers choose compensation components, application notes and design tools become part of the product; good ones win designs.
- **Component tolerance is margin.** Capacitor values (and their ESR) vary with temperature and voltage bias; compensation must hold margins across them.

### Marketing vs Reality

- **"Internally compensated: no external components."** *Reality:* fixed compensation suits a range of output filters; outside it, margins shrink. *Sanity check:* ask for the supported range of output inductance and capacitance and the margins at the corners.
- **"Fast transient response."** *Reality:* usually means high crossover from aggressive lead; ask whether noise and stability margin were traded. *Sanity check:* ask for crossover, phase margin and output noise together.
- **"Type III for best performance."** *Reality:* it is necessary for voltage-mode control with low-ESR ceramic capacitors, but adds parts and tolerance sensitivity. *Sanity check:* ask whether current-mode control (which removes the double pole) was considered.

### Questions for engineering leaders

1. **"What does the compensator add at crossover, and how much margin is left at the worst corner?"**
   *Strong:* lead phase budget and corner analysis. *Evasive:* typical-case Bode plot only.
2. **"What limits crossover: a plant pole, a zero, delay or switching frequency?"**
   *Strong:* names it. *Evasive:* "we tuned it on the bench".
3. **"What does the lag cost in settling time to your accuracy band?"**
   *Strong:* a long-time-scale settling measurement. *Evasive:* overshoot only.
4. **"How sensitive are the margins to capacitor tolerance and DC bias?"**
   *Strong:* margins computed with derated capacitance. *Evasive:* nominal values only.

## 10. Concept check

**Q1.** Where does a lead compensator's maximum phase occur, and how big is it?

<details><summary>Answer</summary>

At the geometric mean of the zero and pole, $\omega_m = 1/(T\sqrt\alpha)$, with $\sin\phi_{max} = (\alpha - 1)/(\alpha + 1)$.

</details>

**Q2.** Why does lead design place $\omega_m$ where $\lvert KL\rvert = 1/\sqrt\alpha$?

<details><summary>Answer</summary>

The lead multiplies the gain by $\sqrt\alpha$ at $\omega_m$, so the compensated gain is exactly 1 there: the new crossover coincides with the lead's peak phase.

</details>

**Q3.** How does a lag compensator improve accuracy without destroying the phase margin?

<details><summary>Answer</summary>

It raises the loop gain at low frequency (by $\beta$) where error constants are set, and its pole–zero pair sits a decade below crossover, where it costs only about 5° of phase.

</details>

**Q4.** Why did the lag design of Example 15-09.3 settle so slowly?

<details><summary>Answer</summary>

It lowered crossover sixfold, and its pole–zero pair near the origin leaves a slow doublet tail with time constant about $1/z$ = 14 s.

</details>

**Q5.** What is the angle deficiency in root-locus lead design?

<details><summary>Answer</summary>

The extra phase needed at the desired pole location so that the angle condition (−180°) holds; the lead's zero and pole are placed to supply it.

</details>

**Q6.** Why does a buck converter in voltage mode need a Type III compensator?

<details><summary>Answer</summary>

Its LC double pole takes the plant phase to nearly −180° above $f_0$; with the integrator's −90°, the loop would have no margin. Two zeros near $f_0$ supply up to 180° of lead.

</details>

**Q7.** How are lead and lag related to PD and PI?

<details><summary>Answer</summary>

A lead is a PD with a filtering pole (finite high-frequency gain); a lag is a PI whose integrator pole is moved slightly off the origin (finite DC gain).

</details>

Practice: [Problems 15-09](../problems/15-09-problems.md) · [Solutions](../solutions/15-09-solutions.md)

## 11. Key terms

[Lead compensator](../../../reference/glossary.md#lead-compensator) · [Lag compensator](../../../reference/glossary.md#lag-compensator) · [Angle deficiency](../../../reference/glossary.md#angle-deficiency) · [Type III compensator](../../../reference/glossary.md#type-iii-compensator) · [Phase margin](../../../reference/glossary.md#phase-margin) · [Pole–zero doublet](../../../reference/glossary.md#pole-zero-doublet)

## 12. Connections

- **Builds on:** root locus ([15-06](15-06-root-locus.md)); margins ([15-07](15-07-frequency-domain-design.md)); PD and PI ([15-08](15-08-pid-control.md)); doublets ([15-03](15-03-time-response.md)).
- **Next:** [15-10 State-Space Introduction](15-10-state-space-introduction.md), which places all closed-loop poles at once.
- **Used later:** digital compensators ([15-11](15-11-digital-control.md)); regulator compensation ([15-12](15-12-control-applications-pll-regulators-thermal.md)); converter control ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)); op-amp compensation ([12-06](../../12-electronics-2/chapters/12-06-stability-and-compensation.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 5–6 (lead and lag design by root locus and frequency response).
- N. S. Nise, *Control Systems Engineering*, ch. 9 and 11 (design via root locus and via frequency response).
- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, ch. 9 (controller design for converters, including lead and Type III style compensators).

## 14. Sources

1. Franklin, Powell and Emami-Naeini; Nise (Further study): lead and lag design (textbook material).
2. Erickson and Maksimović (Further study): converter compensation.

This chapter has no perishable industry figures; its practitioner statements are tagged [Established]. Every number in the examples is recomputed by the verify script (designs by the recipes, margins by root finding, step responses exactly), and the passive lead network is confirmed in ngspice.
