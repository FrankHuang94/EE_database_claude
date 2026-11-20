<!-- status: verified -->
# 12-07 · Output Stages and Power Amplifiers

| | |
|---|---|
| **Course** | [12 · Electronics II](../README.md) |
| **University equivalent** | The output-stage chapter of a second electronics course: class A, B and AB stages, their power efficiency and transistor dissipation, crossover distortion and its cure, biasing with a $V_{BE}$ multiplier, thermal design and thermal runaway, and an introduction to class D (Sedra & Smith, *Microelectronic Circuits*, the output stages and power amplifiers chapter; Gray, Hurst, Lewis & Meyer, ch. 5) |
| **Prerequisites** | [10-07 BJT Single-Stage Amplifiers](../../10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md) (the emitter follower), [12-05 Feedback: Theory and the Four Topologies](12-05-feedback-topologies.md) (distortion reduction), [07-06 AC Power](../../07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) (average and RMS power) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the maximum efficiency of class A and class B output stages and the signal level at which a class B stage dissipates most.
2. Explain crossover distortion, compute its effect with and without feedback, and bias a class AB stage with a $V_{BE}$ multiplier.
3. Calculate the currents of a class AB pair from the translinear relation, and its output resistance at idle.
4. Size a heat sink from a thermal-resistance chain, and test a stage for thermal runaway.
5. Estimate the efficiency of a class D amplifier from its conduction and fixed losses, and explain why class D dominates audio and power delivery.

---

## 1. Big picture

Every signal chain ends by delivering power to something that is not a transistor's drain: a loudspeaker, a motor, an antenna, a cable, a laser. The **output stage** does that job. It must swing large voltages into low impedances with low distortion, and do so efficiently: every watt it dissipates must be removed as heat, and in a battery product every wasted watt shortens the battery's life. Output stages are classified by how much of each cycle their transistors conduct. Class A is linear and wasteful; class B is efficient but distorts near zero; class AB is the practical compromise for linear amplifiers; and class D switches its transistors fully on or off, reaching efficiencies above 90%.

- **Op-amp and line-driver outputs** are class AB stages; their idle current and crossover behaviour show up as distortion specifications.
- **Audio power amplifiers** in phones, earbuds, laptops and televisions are now almost all class D.
- **Thermal limits set power ratings.** A part's maximum output often comes from its package's ability to shed heat, not from its transistors.
- **The same ideas recur** in RF power amplifiers (Course 21) and switching converters (Course 22).

## 2. Intuition first

**Three ways to fill a bucket at a varying rate.** Class A leaves a hose running at full flow all the time and diverts what is not needed down a drain: the bucket gets exactly what it should, but most water is wasted, even when nothing is needed. Class B uses two valves, one to fill and one to drain, each opening only as far as needed: little waste, but there is a moment around "no flow" where neither valve has quite opened and the response stutters. Class AB keeps both valves cracked open slightly so the handover is smooth. Class D opens a valve fully or not at all, many times a second, and lets the bucket's size average the pulses: almost no waste, at the cost of a filter (the bucket) and some ripple.

**The analogy and its limits.** Water flow has no equivalent of the transistor's 0.6 V turn-on, which is what makes class B's handover stutter; and a valve that is fully open dissipates nothing, while a real switch has a small on-resistance and loses energy each time it changes state. Those two effects set the numbers in §3.

**Why efficiency matters so much.** For an output stage, efficiency $\eta = P_L/P_S$ also fixes the heat: the dissipation is $P_S - P_L = P_L(1/\eta - 1)$. At 25% efficiency, 10 W of output means 30 W of heat; at 90%, about 1.1 W. That factor of 27 is the difference between a heat sink the size of a book and a bare chip.

```mermaid
flowchart LR
    A[class A: conducts 360°, η ≤ 25%] --> B[class B: each device 180°, η ≤ 78.5%, crossover]
    B --> C[class AB: slightly more than 180°, small idle current]
    C --> D[class D: switches, η above 90%, needs an LC filter]
```

*Figure 1. Output-stage classes by conduction angle, with their efficiency limits.*

## 3. Theory

> **Conventions.** Supplies are $\pm V_{CC}$; the load $R_L$ is resistive; the output is a sine of peak amplitude $V_{op}$; $P_L = V_{op}^2/(2R_L)$ is the average load power, $P_S$ the average power drawn from the supplies, $\eta = P_L/P_S$ and $P_D = P_S - P_L$ the total transistor dissipation. $V_{CE,sat}$ and the base drive's headroom are neglected unless stated, so the maximum swing is $V_{CC}$.

### 3.1 Class A: the emitter follower

An NPN emitter follower biased by a current source $I_Q$ from the negative supply (10-07) can drive a load in both directions as long as its emitter current stays positive: the load current $v_o/R_L$ may not exceed $I_Q$ in the negative direction, so the swing is limited to $V_{op} \le I_QR_L$ as well as to $V_{CC}$. Both the transistor and the current source draw $I_Q$ on average from their supplies, whatever the signal, so

$$
P_S = 2V_{CC}I_Q, \qquad \eta = \frac{V_{op}^2/(2R_L)}{2V_{CC}I_Q} .
$$

The best case sets $I_Q = V_{CC}/R_L$ and $V_{op} = V_{CC}$:

$$
\eta_{max} = \frac{V_{CC}^2/(2R_L)}{2V_{CC}^2/R_L} = \frac14 = 25\% .
$$

Worse, the efficiency falls with the square of the amplitude, and the transistor dissipates the most, $V_{CC}I_Q$, with **no signal at all**. Class A survives where linearity matters more than power: small-signal stages, some high-end audio, and the driver stages ahead of a power output.

### 3.2 Class B: the complementary push-pull stage

Two emitter followers, an NPN to $+V_{CC}$ and a PNP to $-V_{CC}$, share the input and the output. With no bias, the NPN conducts on positive half-cycles and the PNP on negative ones; each carries a half-sine of peak $V_{op}/R_L$. The average of a half-sine current over a full cycle is $(V_{op}/R_L)/\pi$, so each supply delivers $V_{CC}V_{op}/(\pi R_L)$ and

$$
P_S = \frac{2V_{CC}V_{op}}{\pi R_L}, \qquad \eta = \frac{V_{op}^2/(2R_L)}{2V_{CC}V_{op}/(\pi R_L)} = \frac{\pi}{4}\,\frac{V_{op}}{V_{CC}} ,
$$

which reaches **π/4 = 78.54%** at full swing. Efficiency now falls only linearly with amplitude, and with no signal nothing is drawn.

**When does a class B stage get hottest?** The dissipation is

$$
P_D(V_{op}) = \frac{2V_{CC}V_{op}}{\pi R_L} - \frac{V_{op}^2}{2R_L} .
$$

Setting $dP_D/dV_{op} = 2V_{CC}/(\pi R_L) - V_{op}/R_L = 0$ gives $V_{op} = 2V_{CC}/\pi$ (64% of full swing), where

$$
P_{D,max} = \frac{2V_{CC}^2}{\pi^2R_L}, \qquad \text{or } \frac{V_{CC}^2}{\pi^2R_L} \text{ per transistor},
$$

and the efficiency there is exactly 50%. The heat sink must be sized for this point, not for full output: the stage runs **cooler** at full power than at 64% of full swing.

![Efficiency and transistor dissipation against output amplitude for a plus-or-minus 15 V, 8 ohm stage in class A, class B and a class D model: class A stays below 25% and dissipates most at idle, class B rises linearly to 78.5% with a dissipation peak at two-thirds of full swing, and class D climbs fastest with nearly constant dissipation](../../../assets/figures/12-07/efficiency.svg)

*Figure 2. Efficiency (left) and transistor dissipation (right) against output amplitude for a ±15 V stage driving 8 Ω: class A biased for full swing, ideal class B, and a class D model with two 85 mΩ switches in the current path and 2.5 W of fixed loss. Class B's dissipation peaks at $2V_{CC}/\pi$ (dashed); class D's barely changes with level, so its efficiency is set by its fixed losses at low output.*

**Crossover distortion.** Neither transistor conducts until its $\lvert v_{BE} \rvert$ reaches about 0.6 V, so for inputs within ±0.6 V the output stays near zero. The transfer characteristic has a dead band, and every zero crossing of the signal is notched. Small signals suffer most: a 1 V-peak sine through a ±0.6 V dead band loses most of its waveform (Example 12-07.3), while a 10 V sine loses a little near each crossing. Crossover distortion is particularly objectionable in audio because it does not fall with signal level the way clipping does.

**Feedback helps, but not completely.** Placed inside a loop with gain $A$ ahead of it, the dead band referred to the input shrinks by $A$ (an op-amp must move its output by only 0.6 V/$A$ of input to cross it), so distortion falls dramatically. But the loop gain falls with frequency (12-05), and while the output stage is cut off the loop is open and the op-amp's output must slew across the dead band, so crossover distortion rises at high frequency. Removing the dead band at its source is better.

### 3.3 Class AB and the $V_{BE}$ multiplier

**Biasing out the dead band.** Insert a voltage $V_{BB}$ between the two bases so that both transistors conduct a small **quiescent current** $I_Q$ with no signal. For matched devices with saturation current $I_S$, each $V_{BE} = V_{BB}/2$ and

$$
I_Q = I_Se^{V_{BB}/(2V_T)} \quad\Longleftrightarrow\quad V_{BB} = 2V_T\ln\frac{I_Q}{I_S} .
$$

**The translinear relation.** With a signal, the two base–emitter voltages still sum to $V_{BB}$, so the product of the two collector currents is fixed:

$$
v_{BEN} + v_{EBP} = V_{BB} \quad\Rightarrow\quad i_N\,i_P = I_S^2e^{V_{BB}/V_T} = I_Q^2 .
$$

Together with $i_N - i_P = i_L$ (KCL at the output, neglecting base currents), this gives

$$
i_N = \frac{i_L}{2} + \sqrt{\frac{i_L^2}{4} + I_Q^2}, \qquad i_P = i_N - i_L .
$$

One transistor takes over smoothly as the other fades: neither is ever cut off, so there is no dead band. At idle, both devices conduct $I_Q$ and their emitter resistances $V_T/I_Q$ appear in parallel, so the output resistance is $V_T/(2I_Q)$. The cost is a quiescent dissipation $2V_{CC}I_Q$, usually a small fraction of the output power.

**The $V_{BE}$ multiplier.** $V_{BB}$ must track the output devices' $V_{BE}$ with temperature. A transistor $Q_M$ with resistor $R_2$ across its base–emitter junction and $R_1$ from collector to base sets the current in $R_2$ to $V_{BE,M}/R_2$; neglecting base current, the same current flows in $R_1$, so

$$
V_{BB} = V_{BE,M}\left(1 + \frac{R_1}{R_2}\right) .
$$

Mounting $Q_M$ on the output devices' heat sink makes $V_{BB}$ fall about $(1 + R_1/R_2) \times 2$ mV/°C as they heat, which is what keeps $I_Q$ from rising (§3.4).

### 3.4 Thermal design and thermal runaway

**The thermal resistance chain.** Heat flows from the junction to the case, through the mounting interface to the heat sink, and from the heat sink to the air. Each step has a thermal resistance θ in °C/W, and like resistors in series

$$
T_J = T_A + P_D\,(\theta_{JC} + \theta_{CS} + \theta_{SA}) .
$$

A data sheet gives $T_{J,max}$ (typically 150 °C for silicon) and $\theta_{JC}$; the designer picks $\theta_{SA}$ to keep $T_J$ below the limit at the worst-case dissipation and ambient (Example 12-07.5).

**Thermal runaway.** A bipolar transistor's $V_{BE}$ at constant current falls by about 2 mV/°C. If its base voltage is held fixed, a temperature rise $\Delta T$ acts like a 2 mV/°C increase in drive, raising the current, which raises the dissipation, which raises the temperature: a positive feedback loop. Going around it once:

- $\partial I/\partial T = g_m \times (2\ \text{mV/°C})/(1 + g_mR_E)$, with $R_E$ an emitter resistor (10-07's degeneration);
- $\partial P/\partial I = V_{CE}$;
- $\partial T/\partial P = \theta$, the total thermal resistance.

The loop gain is therefore

$$
L = \frac{V_{CE}\,\theta\,g_m\,(2\ \text{mV/°C})}{1 + g_mR_E} ,
$$

and if $L \ge 1$ the current runs away until something fails. Emitter resistors of a fraction of an ohm, a $V_{BE}$ multiplier coupled to the heat sink (which lowers $V_{BB}$ as it warms), and a sufficient heat sink all lower $L$. MOSFETs at high current have a negative temperature coefficient of drain current (mobility falls with temperature) and are less prone to runaway, though below a crossover current they too have a positive coefficient.

### 3.5 Class D: switching instead of throttling

A class D stage drives its output to $+V_{DD}$ or to ground (or $-V_{DD}$) with switches, at a frequency $f_s$ far above the signal. The fraction of each period spent high, the **duty cycle**, follows the signal (pulse-width modulation, PWM). An LC low-pass filter, or the loudspeaker's own inductance, removes the switching frequency and leaves the average, which is the signal. In a **bridge-tied load** (BTL) arrangement, two half-bridges drive the two ends of the load in opposite phase, doubling the voltage swing and quadrupling the power from one supply.

**Why the efficiency is high.** An ideal switch dissipates nothing: when on, it has no voltage across it; when off, no current through it. Real losses fall into three groups:

- **Conduction:** $I_{rms}^2R_{DS(on)}$ for each switch in the current path.
- **Switching:** energy lost while each transition passes through the region where voltage and current are both present, plus the energy to charge the gates and the switching node's capacitance, all proportional to $f_s$.
- **Fixed (idle):** gate drivers, the modulator, and the output inductor's ripple current, present even with no signal.

At high output, conduction losses dominate and efficiencies of 90% or more are typical; at low output, the fixed losses dominate and efficiency falls (Problem 12-07.11), which is why the idle loss is a headline specification for battery products.

**The filter.** A second-order LC filter with corner $f_0 = 1/(2\pi\sqrt{LC})$ attenuates the switching component by about $(f_s/f_0)^2$, that is 40 dB per decade, while passing the audio band. Its inductor must carry the full load current without saturating, and the switching edges are a source of electromagnetic interference that board design must contain.

> **Going deeper — linearity of class D.** The output is only as linear as the timing of the switch transitions. Dead time (the brief interval with both switches off, to avoid shoot-through), finite switching speed and supply ripple all distort; modern class D amplifiers close a feedback loop around the switching stage, sometimes including the filter, to correct them. The modulator itself is a mixed-signal circuit, closely related to the delta-sigma converters of Course 20.

## 4. Worked examples

### Example 12-07.1 · A class A emitter follower (tier A)

**Setup.** A class A follower runs from ±10 V with $I_Q$ = 100 mA into $R_L$ = 100 Ω. Find the maximum output power, the supply power, the efficiency, the transistor's idle dissipation, and the efficiency at half amplitude.

**Solution.** $I_QR_L$ = 10 V matches $V_{CC}$, so the full ±10 V swing is available: $P_L = 10^2/200$ = **0.5** W. $P_S = 2 \times 10 \times 0.1$ = **2** W regardless of signal, so η = **25**%. At idle the transistor dissipates $V_{CC}I_Q$ = **1** W (and the current source another 1 W). At 5 V peak, $P_L$ = 0.125 W and η = **6.25**%.

**Sanity check.** At its best this stage turns 2 W into 0.5 W; at typical levels it is a heater.

### Example 12-07.2 · A class B stage (tier A)

**Setup.** A class B stage runs from ±15 V into 8 Ω. Find the maximum output power, the supply power and the efficiency at full swing; then the amplitude of worst-case dissipation, the total and per-transistor dissipation there, and the efficiency at that point.

**Solution.** $P_L = 15^2/16$ = **14.06** W. $P_S = 2 \times 15 \times 15/(8\pi)$ = **17.90** W, so η = **78.54**%. The worst dissipation is at $V_{op} = 30/\pi$ = **9.549** V, where $P_{D,max} = 2 \times 225/(8\pi^2)$ = **5.699** W in total, **2.850** W per transistor, at an efficiency of **50**%.

**Sanity check.** At full output the dissipation is only $17.90 - 14.06$ = 3.84 W, less than at 9.5 V: heat sinks are sized for the middle of the range.

### Example 12-07.3 · Crossover distortion with and without feedback (tier B)

**Setup.** Model a class B stage as a ±0.6 V dead band: $v_o = v_i - 0.6$ for $v_i > 0.6$ V, $v_i + 0.6$ for $v_i < -0.6$ V, and zero between. Find the total harmonic distortion (THD) of the output for 1 V and 10 V peak sine inputs. Then put the stage inside a loop with an op-amp of gain $A$ = 10⁴ and unity feedback, and find the THD at the same input amplitudes.

**Solution.** By FFT of the clipped-at-zero waveform, the open stage gives THD = **46.53**% at 1 V and **3.731**% at 10 V: the dead band takes most of the small signal. Inside the loop, the op-amp drives the stage's input to $A(v_i - v_o)$, and solving $v_o = \text{dz}(A(v_i - v_o))$ gives $v_o = (Av_i \mp 0.6)/(1 + A)$ outside an input dead band of only ±60 µV. The THD falls to about **0.0037**% at 1 V and **0.00037**% at 10 V.

**Sanity check.** The improvement, about 12,600 times at 1 V, is not simply $1 + T$ because the dead band's distortion is strongly nonlinear in its width; and at high frequency, where $A$ falls, it shrinks. Class AB bias removes the dead band itself.

### Example 12-07.4 · Biasing a class AB stage (tier B)

**Setup.** Matched output transistors have $I_S$ = 10⁻¹³ A. Find the $V_{BB}$ for $I_Q$ = 20 mA, the resistor ratio of a $V_{BE}$ multiplier whose transistor has $V_{BE}$ = 0.65 V, the two transistors' currents when the load draws 100 mA, and the output resistance at idle.

**Solution.** $V_{BB} = 2 \times 25.852\ \text{mV} \times \ln(2 \times 10^{11})$ = **1.345** V, so $R_1/R_2 = 1.345/0.65 - 1$ = **1.070**. With $i_L$ = 100 mA, $i_N = 50 + \sqrt{2500 + 400}$ mA = **103.9** mA and $i_P$ = **3.852** mA: the PNP has not cut off. At idle, $R_{out} = V_T/(2I_Q)$ = **0.6463** Ω.

**Sanity check.** $i_Ni_P = 103.85 \times 3.852 = 400\ \text{mA}^2 = I_Q^2$: the translinear relation holds.

### Example 12-07.5 · Heat sink and thermal runaway (tier B)

**Setup.** (a) Each transistor of Example 12-07.2 dissipates up to 2.850 W, with $\theta_{JC}$ = 1.5 °C/W, $\theta_{CS}$ = 0.5 °C/W and $\theta_{SA}$ = 10 °C/W at 40 °C ambient. Find $T_J$, and the largest $\theta_{SA}$ that keeps $T_J \le$ 125 °C. (b) A transistor biased at 100 mA with fixed base voltage has $V_{CE}$ = 15 V and a total θ of 12 °C/W. Find the thermal loop gain without and with a 0.47 Ω emitter resistor.

**Solution.** (a) $T_J = 40 + 2.850 \times 12$ = **74.2** °C. The limit allows $\theta_{total} = (125 - 40)/2.850$ = 29.83 °C/W, so $\theta_{SA} \le$ **27.83** °C/W.

(b) $g_m = 100\ \text{mA}/25.852\ \text{mV}$ = **3.868** A/V, so $L = 15 \times 12 \times 3.868 \times 0.002$ = **1.393**: the transistor runs away. With $R_E$ = 0.47 Ω, $1 + g_mR_E$ = 2.818 and $L$ = **0.4942**, safely below one.

**Sanity check.** A 0.47 Ω resistor drops only 47 mV at 100 mA, yet it more than halves the thermal loop gain: degeneration is cheap insurance.

### Example 12-07.6 · Class D against class B at 100 W (tier C)

**Setup.** A class D amplifier in BTL drives 4 Ω from 51 V with switches of 85 mΩ on-resistance (two in the current path) and fixed losses of 2.5 W. Find its efficiency at 100 W. Compare with a class B stage on ±51 V rails at the same output. Then find the corner of a 10 µH, 1 µF output filter and its attenuation at a 450 kHz switching frequency.

**Solution.** $I_{rms} = \sqrt{100/4}$ = **5** A, conduction loss $25 \times 0.17$ = **4.25** W, so η = 100/106.75 = **93.68**%. The class B stage needs $V_{op} = \sqrt{2 \times 100 \times 4}$ = **28.28** V, so η = $(\pi/4)(28.28/51)$ = **43.56**% and it dissipates **129.6** W. The filter's corner is $1/(2\pi\sqrt{10\ \mu\text{H} \times 1\ \mu\text{F}})$ = **50.33** kHz, and at 450 kHz it attenuates by about $40\log_{10}(450/50.33)$ = **38.06** dB.

**Sanity check.** The class B stage would need a heat sink for 130 W; the class D stage sheds under 7 W. Switching losses, neglected here, typically add a few watts.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 12-07.a | class A maximum efficiency | 25 | % |
| T 12-07.b | class B maximum efficiency | 78.54 | % |
| T 12-07.c | worst-dissipation swing fraction | 64 | % |
| T 12-07.d | efficiency at worst dissipation | 50 | % |
| Ex 12-07.1a | maximum output power | 0.5 | W |
| Ex 12-07.1b | supply power | 2 | W |
| Ex 12-07.1c | efficiency | 25 | % |
| Ex 12-07.1d | idle transistor dissipation | 1 | W |
| Ex 12-07.1e | efficiency at half amplitude | 6.25 | % |
| Ex 12-07.1f | load power at half amplitude | 0.125 | W |
| Ex 12-07.2a | maximum output power | 14.06 | W |
| Ex 12-07.2b | supply power | 17.90 | W |
| Ex 12-07.2c | efficiency | 78.54 | % |
| Ex 12-07.2d | amplitude of worst dissipation | 9.549 | V |
| Ex 12-07.2e | total worst dissipation | 5.699 | W |
| Ex 12-07.2f | per-transistor worst dissipation | 2.850 | W |
| Ex 12-07.2g | efficiency there | 50 | % |
| Ex 12-07.2h | dissipation at full output | 3.84 | W |
| Ex 12-07.3a | THD at 1 V, open | 46.53 | % |
| Ex 12-07.3b | THD at 10 V, open | 3.731 | % |
| Ex 12-07.3c | input dead band in the loop | 60 | µV |
| Ex 12-07.3d | THD at 1 V, in the loop | 0.0037 | % |
| Ex 12-07.3e | THD at 10 V, in the loop | 0.00037 | % |
| Ex 12-07.3f | improvement at 1 V | 1.26 × 10⁴ | — |
| Ex 12-07.4a | bias voltage | 1.345 | V |
| Ex 12-07.4b | resistor ratio | 1.070 | — |
| Ex 12-07.4c | NPN current | 103.9 | mA |
| Ex 12-07.4d | PNP current | 3.852 | mA |
| Ex 12-07.4e | idle output resistance | 0.6463 | Ω |
| Ex 12-07.5a | junction temperature | 74.2 | °C |
| Ex 12-07.5b | allowed total θ | 29.83 | °C/W |
| Ex 12-07.5c | largest θ_SA | 27.83 | °C/W |
| Ex 12-07.5d | g_m | 3.868 | A/V |
| Ex 12-07.5e | loop gain without R_E | 1.393 | — |
| Ex 12-07.5f | 1 + g_m R_E | 2.818 | — |
| Ex 12-07.5g | loop gain with R_E | 0.4942 | — |
| Ex 12-07.6a | load current | 5 | A |
| Ex 12-07.6b | conduction loss | 4.25 | W |
| Ex 12-07.6c | class D efficiency | 93.68 | % |
| Ex 12-07.6d | class B amplitude | 28.28 | V |
| Ex 12-07.6e | class B efficiency | 43.56 | % |
| Ex 12-07.6f | class B dissipation | 129.6 | W |
| Ex 12-07.6g | filter corner | 50.33 | kHz |
| Ex 12-07.6h | attenuation at 450 kHz | 38.06 | dB |
| Sim 12-07.a | ideal load power at 10 V | 6.25 | W |
| Sim 12-07.b | ideal efficiency at 10 V | 52.36 | % |
| Sim 12-07.c | simulated load power | 5.098 | W |
| Sim 12-07.d | simulated efficiency | 48.82 | % |
| Sim 12-07.e | V_BE at the peak | 0.778 | V |
| Sim 12-07.f | peak load current | 1.153 | A |
| Sim 12-07.g | peak output | 9.222 | V |
| Prac 12-07.a | largest undistorted BTL sine power | 299 | W |
| Prac 12-07.b | ideal BTL limit | 325.1 | W |

*Every value is recomputed by [verify_12_07.py](../verify/verify_12_07.py): efficiencies and dissipations by numerical integration of the device currents over a cycle (not from the closed forms), the worst dissipation by bounded optimization, THD by FFT of the solved waveforms, the class AB currents by solving the exponential device equations, and the filter attenuation from the LC transfer function. The class B stage is also simulated in ngspice with real transistor models.*

## 5. Simulate it

The lab, [labs/12-07-lab](../labs/12-07-lab/README.md), has a notebook and an ngspice netlist:

1. Plots efficiency and dissipation against amplitude for class A, class B and a class D model, and marks the class B dissipation peak.
2. Computes crossover distortion against amplitude for a class B dead band, inside and outside a feedback loop, and with class AB bias.
3. Plots the class AB currents against load current from the translinear relation.
4. Steps a thermal model of a transistor with and without an emitter resistor and shows runaway.

The netlist [class_b.cir](../labs/12-07-lab/class_b.cir) simulates a ±15 V class B stage with bipolar transistor models driving 8 Ω and measures load power, supply power and efficiency.

**Guided exercise (predict, then run).** **Before running the netlist**, predict: a 10 V-peak input drives the ±15 V class B stage into 8 Ω. The ideal formulas give $P_L$ = **6.25** W and η = **52.36**%. Will the real stage deliver more or less, and why? Then run it. (Less: about **5.098** W at **48.82**% efficiency, because each transistor's $V_{BE}$ is lost from the swing (**0.778** V at the **1.153** A peak, so the output reaches only **9.222** V), and the dead band removes the signal near zero.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Class A bias current | Linearity, no crossover at all | Efficiency ≤ 25%, heat at idle | Analog designer |
| Class AB quiescent current $I_Q$ | Crossover distortion, output resistance | Idle power, thermal-runaway risk | Analog designer |
| Emitter resistors $R_E$ | Thermal stability, current sharing | Swing, output resistance, efficiency | Analog designer |
| Class D switching frequency | Smaller filter, lower ripple, more loop bandwidth | Switching loss, EMI | Product architect |
| Heat sink size | Higher continuous power | Cost, volume | Mechanical and product |
| BTL connection | 4× power from one supply | Two half-bridges, floating load | Product architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Class A efficiency | ≤ 25% (resistive load) | Worst at idle |
| Class B efficiency | $(\pi/4)V_{op}/V_{CC}$, ≤ 78.54% | Linear in amplitude |
| Class B worst dissipation | $2V_{CC}^2/(\pi^2R_L)$ at $V_{op} = 2V_{CC}/\pi$ | 50% efficiency there |
| Crossover dead band | about ±0.6 V for bipolar stages | Fixed by class AB bias |
| Class AB translinear | $i_Ni_P = I_Q^2$ | Output resistance $V_T/(2I_Q)$ at idle |
| $V_{BE}$ multiplier | $V_{BB} = V_{BE}(1 + R_1/R_2)$ | Tracks −2 mV/°C × $(1 + R_1/R_2)$ |
| Junction temperature | $T_J = T_A + P_D\sum\theta$ | $T_{J,max}$ ≈ 150 °C for silicon |
| Class D efficiency | > 90% at high output | Fixed losses dominate at low output |
| Class D audio switching | hundreds of kHz | e.g. 450 kHz in the TPA3255 [1] |

## 8. Common mistakes

- **Sizing the class B heat sink at full output.** The worst dissipation is at 64% of full swing.
- **Forgetting the quiescent current in class A dissipation.** The transistor is hottest with no signal.
- **Assuming feedback removes crossover distortion completely.** It shrinks with loop gain, which falls with frequency; bias is the real cure.
- **Treating a $V_{BE}$ multiplier as a fixed voltage.** Its value tracks temperature, which is the point; it must be thermally coupled to the output devices.
- **Quoting class D efficiency at full power only.** At typical listening levels, fixed losses dominate.
- **Ignoring the class D filter.** Its inductor must not saturate at peak current, and switching edges radiate.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Class D audio at hundreds of watts.** TI's TPA3255 (data sheet SLASEA8A, revised Oct 2016) is a class D stage specified for 315 W per channel into 4 Ω at 10% THD+N and 255 W at 1% THD+N (bridge-tied), from supplies of 18 to 53.5 V, with "90% efficient class-D operation (4 Ω)", 85 mΩ typical output MOSFETs, idle losses of 2.5 W with four channels switching, a nominal 450 kHz PWM frequency and 0.006% THD+N at 1 W [1] **[Established]** (data sheet). Its front page lists 260 W per channel at 1% THD+N where the electrical table lists 255 W; the table is the specification.
- **A sanity check on the headline power.** From 51 V into 4 Ω in BTL, the largest undistorted sine is about $(51 \times 4/4.17)^2/8$ = **299** W after the two 85 mΩ switches' drop (the ideal limit is $51^2/8$ = **325.1** W). The 315 W figure is reached only at 10% THD+N, that is with the waveform visibly clipped **[Established]** (arithmetic from [1]).

### Why it matters commercially

- **Class D won audio.** Phones, earbuds, televisions, smart speakers and cars use class D because battery life and heat matter more than the last fraction of a decibel of distortion.
- **Output stages decide thermal design and package cost.** A package's θ sets how much power a chip can deliver continuously; product power ratings are thermal ratings.
- **Linear output stages persist** where switching noise is unacceptable: op-amp outputs, headphone drivers in high-end products, and sensitive RF and instrumentation front ends.

### Marketing vs Reality

- **"315 W per channel."** *Reality:* at 10% THD+N, which is audibly clipped; the 1% figure (255 W) is closer to usable power, and the continuous rating depends on cooling. *Sanity check:* compute $V_{DD}^2/(8R_L)$ for BTL and ask for the THD level and duration.
- **"90% efficient."** *Reality:* at high output; at the watt or two of typical listening, idle losses can halve the efficiency. *Sanity check:* ask for efficiency at 1 W and the idle loss.
- **"Class A sound."** *Reality:* a marketing label for linearity; any good class AB or class D amplifier with enough loop gain matches it on measurable distortion. *Sanity check:* ask for THD+N against frequency and power.

### Questions for engineering leaders

1. **"What sets your output power rating: supply, current or thermal limits?"**
   *Strong:* a clear limiting factor with the numbers. *Evasive:* a peak number without conditions.
2. **"What is your efficiency at typical operating power, not just at maximum?"**
   *Strong:* a curve or numbers at 1%, 10% and 100% of full power, plus idle loss. *Evasive:* the peak efficiency only.
3. **"How do you guarantee the output stage cannot run away thermally?"**
   *Strong:* emitter or source degeneration, thermal tracking of the bias, protection and characterization over temperature. *Evasive:* "the heat sink is big enough."

## 10. Concept check

**Q1.** Why can class A efficiency never exceed 25% with a resistive load and a current-source bias?

<details><summary>Answer</summary>

The supplies always deliver $2V_{CC}I_Q$, and the largest sine the stage can deliver, with $V_{op} = V_{CC} = I_QR_L$, has power $V_{CC}^2/(2R_L)$, a quarter of the supply power.

</details>

**Q2.** At what amplitude does a class B stage dissipate the most, and what is its efficiency there?

<details><summary>Answer</summary>

At $V_{op} = 2V_{CC}/\pi$, about 64% of full swing, where the efficiency is exactly 50%.

</details>

**Q3.** What causes crossover distortion, and how does class AB bias remove it?

<details><summary>Answer</summary>

Neither transistor conducts until $\lvert v_{BE}\rvert$ reaches about 0.6 V, leaving a dead band around zero; a bias voltage $V_{BB}$ between the bases keeps both conducting a small current so one takes over smoothly as the other fades.

</details>

**Q4.** Why must a $V_{BE}$ multiplier be mounted on the output transistors' heat sink?

<details><summary>Answer</summary>

So that its $V_{BE}$, and hence $V_{BB}$, falls as the output devices heat, holding their quiescent current roughly constant and preventing thermal runaway.

</details>

**Q5.** What makes a transistor thermally unstable, and what does an emitter resistor do?

<details><summary>Answer</summary>

With fixed base voltage, heating raises current, which raises dissipation and temperature; if the loop gain $V_{CE}\theta g_m(2\ \text{mV/°C})$ exceeds one, it runs away. An emitter resistor divides the loop gain by $1 + g_mR_E$.

</details>

**Q6.** Why is class D efficient, and where does it lose efficiency?

<details><summary>Answer</summary>

Its switches are either fully on (little voltage) or off (no current); it loses power in on-resistance, during transitions, in gate and capacitance charging, and in fixed idle losses that dominate at low output.

</details>

[Problem set for this chapter](../problems/12-07-problems.md)

## 11. Key terms

[Class-A amplifier](../../../reference/glossary.md#class-a-amplifier) · [Class-B amplifier](../../../reference/glossary.md#class-b-amplifier) · [Class-AB amplifier](../../../reference/glossary.md#class-ab-amplifier) · [Class-D amplifier](../../../reference/glossary.md#class-d-amplifier) · [Crossover distortion](../../../reference/glossary.md#crossover-distortion) · [VBE multiplier](../../../reference/glossary.md#vbe-multiplier) · [Thermal resistance](../../../reference/glossary.md#thermal-resistance) · [Thermal runaway](../../../reference/glossary.md#thermal-runaway) · [Bridge-tied load](../../../reference/glossary.md#bridge-tied-load) · [Conduction angle](../../../reference/glossary.md#conduction-angle)

## 12. Connections

- **Builds on:** the emitter follower from [10-07](../../10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md); distortion reduction by feedback from [12-05](12-05-feedback-topologies.md); average power from [07-06](../../07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md).
- **Next:** [12-08 Op-Amp Internals](12-08-op-amp-internals.md) puts a class AB output stage behind the two-stage amplifier of 12-06.
- **Used later:** switching converters and power semiconductors in [Course 22](../../22-power-electronics-and-energy-conversion/README.md); RF power amplifier classes in [Course 21](../../21-rf-and-microwave-engineering/README.md); delta-sigma modulators in [Course 20](../../20-analog-and-mixed-signal-ic-design/README.md).

## 13. Further study

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the output stages and power amplifiers chapter.
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 5 (output stages).
- D. Self, *Audio Power Amplifier Design* (6th ed., Focal Press, 2013), for crossover distortion and thermal compensation in practice.

## 14. Sources

1. Texas Instruments, *TPA3255 315-W Stereo, 600-W Mono PurePath Ultra-HD Analog-Input Class-D Amplifier*, SLASEA8A (Feb 2016, revised Oct 2016): features, §7.5 electrical characteristics and §7.6 audio characteristics: [data sheet](https://www.ti.com/lit/ds/symlink/tpa3255.pdf). [R-191](../../../reference/research-log.md#r-191--high-power-class-d-audio-amplifier-data-sheet).
