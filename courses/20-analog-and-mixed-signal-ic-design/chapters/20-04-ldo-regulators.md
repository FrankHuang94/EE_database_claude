<!-- status: verified -->
# 20-04 · Low-Dropout Regulators

| | |
|---|---|
| **Course** | [20 · Analog and Mixed-Signal IC Design](../README.md) |
| **University equivalent** | The linear-regulator material of a graduate analog or power-management IC course: LDO architecture and pass devices, dropout, load and line regulation, stability across load, power-supply rejection, load transients, capacitor-less and digital LDOs (Rincón-Mora, *Analog IC Design with Low-Dropout Regulators*, 2nd ed.; Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., the regulator sections) |
| **Prerequisites** | [15-12](../../15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) (the LDO loop and its ESR window), [20-01](20-01-analog-design-fundamentals-gm-id.md) (charge-based model), [20-02](20-02-two-stage-op-amp-design.md) (op-amp compensation, PSRR), [20-03](20-03-bandgap-references.md) (the reference), [09-10](../../09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) (velocity saturation) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Explain an LDO's architecture, compare PMOS and NMOS pass devices, and compute its efficiency and headroom.
2. Size a PMOS pass device for a dropout specification with the charge-based model, including velocity saturation.
3. Derive load regulation, line regulation and DC accuracy from the loop gain, and compute them across the load range.
4. Analyze an LDO's stability as the load current moves its poles by orders of magnitude, with external and on-chip output capacitors.
5. Derive power-supply rejection against frequency and explain why the pass device's gate must track the supply.
6. Estimate load-transient droop, and explain why capacitor-less and digital LDOs make different trade-offs.

## 1. Big picture

A **low-dropout regulator** (LDO) turns a noisy or variable input voltage into a clean, fixed output by burning the difference across a transistor. It is the opposite of a switching regulator: inefficient when the input is far above the output, but simple, small, quiet and fast. Almost every mixed-signal chip contains several. They isolate a PLL's oscillator from digital supply noise, give an ADC a quiet supply, power always-on domains in microcontrollers, and, in modern processors, trim each core's supply below a shared rail. 15-12 analyzed the LDO as a control loop. This chapter designs one, transistor by transistor, in the illustrative T130 process.

- **Dropout sets efficiency.** An LDO's efficiency is at most $V_{out}/V_{in}$; regulating with only 150 mV of headroom instead of 600 mV raises it from 67% to 89% (Example 20-04.1).
- **The load moves everything.** The pass device's transconductance and output resistance change by two orders of magnitude between light and full load, so the loop's poles, gain and margins do too.
- **Supply rejection is the reason many LDOs exist.** A regulator placed after a switching converter must reject its ripple at hundreds of kilohertz to megahertz, where the loop gain is falling.
- **On-chip LDOs changed the design space.** Without a microfarad output capacitor, the loop itself must respond in nanoseconds or less.

## 2. Intuition first

```text
 V_in ─────────────────┬──────────────────────────────
                       │ S
                    ┌──┴──┐
          gate  ────┤ MP  │  PMOS pass device (millimeters wide)
            ▲       └──┬──┘
            │          │ D
            │          ●───────────────┬─────────●── V_out ──► I_L (load)
            │          │               │
   ┌────────┴──────┐ R_top            ESR
   │ error amp     │   │               │
   │ + gate buffer │   ●── V_FB       C_L
   └──┬─────────┬──┘   │               │
      │ −       │ +  R_bot            GND
      │         │      │
    V_FB      V_REF   GND

   V_FB = β·V_out, β = R_bot/(R_top + R_bot)
```

*Figure 1. An LDO. The error amplifier compares a fraction β of the output with the reference and drives the gate of a wide PMOS pass device. The output capacitor $C_L$ (with its equivalent series resistance) holds the output during fast load changes.*

**A water analogy, and its limits.** Picture a valve between a high-pressure main and a household line, with a float that senses the household pressure and opens the valve when it drops. The valve wastes the pressure difference as turbulence (heat), more of it when the main pressure is high. If the main pressure falls almost to the household's, even a fully open valve cannot keep up: that is **dropout**. The float's speed matters when a tap is opened suddenly, and a tank on the household side (the output capacitor) carries the demand until the valve responds. The analogy breaks where the valve's own behavior changes with flow: a transistor's gain grows with its current, so the "float and valve" loop is fast and stiff at heavy flow and slow and soft at a trickle. A mechanical valve has no such dependence, and this one is the central difficulty of LDO design.

**Why a PMOS.** With a PMOS pass device, the gate can be pulled all the way to ground, giving the largest possible $V_{SG}$ and the smallest possible voltage drop. An NMOS source follower would need its gate a $V_{GS}$ *above* the output, so its input must exceed the output by a threshold plus overdrive, unless a charge pump or a second supply provides the gate drive. The NMOS follower's advantages, a low output impedance and good supply rejection, are why it reappears in designs that can afford the gate drive.

## 3. Theory

> **Conventions.** $V_{in}$ input, $V_{out}$ output, $I_L$ load current, $I_Q$ quiescent current (everything the regulator draws that does not reach the load), $\beta = V_{REF}/V_{out}$ the divider ratio. Pass device: a T130 PMOS (20-02's PMOS: μ = 100 cm²/V·s, $v_{sat}$ = 6 × 10⁶ cm/s, $n$ = 1.3, $\lvert V_{TH}\rvert$ = 0.45 V, $V_A'$ = 8 V/µm) at $L$ = 0.15 µm, so $r_{ds} = V_A'L/I_D$ = 1.2 V/$I_D$. The running design: $V_{out}$ = 1.2 V from $V_{REF}$ = 0.6 V (20-03's sub-1 V reference, β = 0.5), $I_L$ from 100 µA to 100 mA, a 1 µF ceramic output capacitor with 5 mΩ ESR, nominal $V_{in}$ = 1.8 V and 150 mV dropout at 100 mA.

### 3.1 Efficiency, headroom and the pass device

Power in is $V_{in}(I_L + I_Q)$ and power out $V_{out}I_L$, so

$$
\eta = \frac{V_{out}I_L}{V_{in}(I_L + I_Q)} \le \frac{V_{out}}{V_{in}} .
$$

The first factor ($V_{out}/V_{in}$) is the price of linear regulation; the second ($I_L/(I_L + I_Q)$) is the **current efficiency**, which matters at light load. A regulator that spends 120 µA to deliver 100 µA is at best 45% current-efficient. The minimum input at which the LDO still regulates is $V_{out} + V_{DO}$, where the **dropout voltage** $V_{DO}$ is the pass device's drop when its gate is driven fully on.

### 3.2 Sizing the pass device for dropout

At dropout the error amplifier pulls the PMOS gate to ground, so $V_{SG} = V_{in}$, and the device runs in triode with $V_{SD} = V_{DO}$. 20-02 §3.9 wrote the charge-based model's current as a forward minus a reverse term; with the source at $V_{in}$:

$$
I_D = I_{spec}\left[(q_s^2 + q_s) - (q_d^2 + q_d)\right], \qquad \frac{V_P}{V_T} = 2q_s + \ln q_s, \qquad \frac{V_P - V_{SD}}{V_T} = 2q_d + \ln q_d ,
$$

with $V_P = (V_{SG} - \lvert V_{TH}\rvert)/n$ and $I_{spec} \propto W/L$. Given $V_{SG}$, $V_{SD}$ and the required current, this fixes $W$.

**Velocity saturation.** The long-channel model ignores the carriers' speed limit (09-10). The lateral field along the channel is about $V_{SD}/L$; when it approaches the critical field $E_{sat} = v_{sat}/\mu$, the current falls by roughly the factor $1/(1 + V_{SD}/(E_{sat}L))$, the standard first-order correction. For T130's PMOS, $E_{sat}$ = **6.0** V/µm, and 150 mV across 0.15 µm is 1 V/µm, so the width must grow by **1.167** (Example 20-04.2).

**Consequences of a wide device.** A pass device delivering 100 mA from 150 mV of headroom is millimeters wide. Its gate capacitance (picofarads) must be driven over a large swing: from near $V_{in}$ minus a threshold at light load down to ground at dropout. The gate driver's current, set by how fast the gate must move, is a large part of $I_Q$.

### 3.3 Regulation from the loop gain

With error-amplifier gain $A_{EA}$, pass-device transconductance $g_{mp}$ and output resistance $R_{out} = r_{ds} \parallel R_L \parallel R_{div}$, the DC loop gain is

$$
L_0 = A_{EA}\,\beta\,g_{mp}R_{out} .
$$

**Load regulation.** The closed-loop output impedance is the open-loop one divided by $1 + L$ (15-04, 15-12): at DC, $R_{out}/(1 + L_0) \approx 1/(A_{EA}\beta g_{mp})$ when $L_0 \gg 1$. It depends on the load through $g_{mp}$: the regulator is stiffer at heavy load. For a large change of load the small-signal value is not enough. The gate must move by the change in $V_{SG}$ between the two currents, which the error amplifier supplies by an input error of $\Delta V_{SG}/A_{EA}$, so the output moves by

$$
\Delta V_{out} \approx -\frac{\Delta V_{SG}}{A_{EA}\,\beta} .
$$

**Line regulation.** Input ripple reaches the output through the pass device (§3.5); at DC its effect is divided by $1 + L_0$ as well.

**DC accuracy.** The output is $V_{REF}/\beta$ plus the error amplifier's offset divided by β, plus the regulation errors above. The reference's accuracy (20-03), the divider's ratio error and the offset usually dominate the error budget.

### 3.4 Stability across the load range

15-12 §3.3 set up the loop; here are its poles in the running design. The error amplifier (transconductance $g_{ma}$ = 1 mS, output resistance $R_a$ = 100 kΩ, so $A_{EA}$ = 100) drives a buffer whose output conductance $g_{mb}$ = 2 mS charges the pass device's gate capacitance $C_g$:

$$
L(s) = \frac{A_{EA}\,\beta\,g_{mp}\,Z_{out}(s)}{(1 + s/p_a)(1 + s/p_g)}, \qquad Z_{out} = R_{out} \parallel \left(R_{ESR} + \frac{1}{sC_L}\right), \qquad p_a = \frac{1}{R_aC_a},\ p_g = \frac{g_{mb}}{C_g} .
$$

With a microfarad output capacitor, the output pole $1/(R_{out}C_L)$ is far below the others: this is **output-pole-dominant** compensation. Above that pole, $|L| \approx A_{EA}\beta g_{mp}/(\omega C_L)$, so the crossover is

$$
\omega_c \approx \frac{A_{EA}\,\beta\,g_{mp}}{C_L} ,
$$

proportional to the pass device's $g_m$. **The crossover rises with load current**: from **22.5** kHz at 100 µA to **2.39** MHz at 100 mA in the running design, while $p_a$ (7.96 MHz) and $p_g$ (197 MHz) stay put. The phase margin is therefore worst at *full* load, where the crossover approaches the error amplifier's pole: 77.5°, against 89.9° at 100 µA (Example 20-04.4). Two consequences:

- **The output capacitor is part of the compensation.** Making it smaller raises the crossover. With 0.1 µF the full-load margin falls to **31.2**° (Example 20-04.4). Data sheets therefore specify a minimum output capacitance, and 15-12's ESR window applies when the compensation relies on the capacitor's ESR zero.
- **Light load is slow.** The low crossover at light load means the regulator responds slowly to a load step that *starts* from light load; §3.6 checks whether that matters.

![Loop-gain magnitude and phase of the running design at 100 microamperes, 1, 10 and 100 milliamperes: the low-frequency gain falls from about 58 to 40 decibels as load rises, but the crossover moves up from 22.5 kilohertz to 2.39 megahertz, and the phase at crossover falls from about minus 90 degrees toward minus 102 degrees at full load](../../../assets/figures/20-04/loop.svg)

*Figure 2. The running design's loop gain at four load currents (1 µF, 5 mΩ ESR). The output pole moves with load, the crossover follows $g_{mp}$, and the error amplifier's pole at 7.96 MHz and the gate pole at 197 MHz stay fixed.*

### 3.5 Power-supply rejection

Supply ripple $v_{in}$ reaches the output through the pass device in two ways: directly through its output conductance, $g_{ds}v_{in}$, and through its gate–source voltage if the gate does not follow the ripple. Let the gate carry a fraction $k$ of the input ripple. The current injected into the output node is then $[g_{mp}(1 - k) + g_{ds}]v_{in}$; it develops a voltage across $Z_{out}$, and the loop suppresses it by $1 + L$:

$$
\frac{1}{\text{PSRR}(s)} = \frac{v_{out}}{v_{in}} = \frac{\left[g_{mp}(1 - k) + g_{ds}\right]Z_{out}(s)}{1 + L(s)} .
$$

- **The gate must track the supply.** With $k$ = 0 (the gate held steady relative to ground), the injected current is dominated by $g_{mp}v_{in}$, and at DC $1/\text{PSRR} \approx 1/(A_{EA}\beta)$: only the error amplifier's gain helps. With $k$ = 1 (the gate driver referenced to $V_{in}$, so $v_{sg}$ sees no ripple), only $g_{ds}$ injects, and $1/\text{PSRR} \approx 1/(A_{EA}\beta g_{mp}r_{ds})$: better by the pass device's intrinsic gain. In the running design at full load, **45.6** dB against **32.0** dB (Example 20-04.5).
- **Frequency behavior.** While $|L| \gg 1$, $Z_{out}/(1 + L) \approx 1/(A_{EA}\beta g_{mp})\cdot(1 + s/p_a)(1 + s/p_g)$, which grows above the error amplifier's pole: supply rejection degrades from $p_a$ until the crossover. Above the crossover the output capacitor's impedance $1/(\omega C_L)$ takes over and rejection improves again. The worst rejection sits between the error amplifier's pole and the crossover, which is why LDOs following switching converters are designed with wide-bandwidth error amplifiers or large output capacitors. In the running design $p_a$ lies above the crossover, so rejection stays near its DC value up to the megahertz range.
- **What the model leaves out.** At high frequency the pass device's own capacitances (gate–drain, source–drain, and the gate's coupling to the supply) and the board's parasitics carry ripple around the loop. They set the real high-frequency floor, typically in the tens of megahertz, so the rising curves at the right of Figure 3 are an artifact of the simple model, not a promise.

![PSRR against ripple frequency for the running design at 100 milliamperes and 100 microamperes, with the gate tracking the supply and with a ground-referenced gate: the tracking gate is about 14 decibels better at full load and about 31 decibels better at light load at low frequency; all curves rise above their crossovers as the output capacitor shorts the ripple](../../../assets/figures/20-04/psrr.svg)

*Figure 3. Supply rejection of the running design. A gate that tracks the supply ($k$ = 1) is better by the pass device's intrinsic gain; the curves rise where the output capacitor takes over. Parasitic capacitive paths, not modeled here, limit real LDOs at high frequency.*

### 3.6 Load transients

When the load current jumps by $\Delta I$, the output capacitor supplies the difference until the loop responds. A first estimate of the dip is

$$
\Delta V \approx \frac{\Delta I}{\omega_c C_L} + \Delta I\,R_{ESR} ,
$$

the charge drawn from $C_L$ in about one loop time constant $1/\omega_c$, plus the ESR drop. For the running design at full load this is **6.64** mV + **0.50** mV. Notice what the first term is: with output-pole-dominant compensation, $\omega_cC_L \approx A_{EA}\beta g_{mp}$, so $\Delta I/(\omega_cC_L) \approx \Delta I/(A_{EA}\beta g_{mp})$, which is the small-signal load-regulation error of §3.3. A well-damped loop of this kind does not overshoot its final value by much; the dip *is* the regulation error. For a large step the final value is the large-signal error $\Delta V_{SG}/(A_{EA}\beta)$, **13.4** mV for a step from 100 µA to 100 mA, bigger than 6.64 mV because $g_{mp}$ is smaller at the lower currents the gate passes through on the way. A nonlinear simulation of the whole loop (Example 20-04.6) shows that this regulator's dip never exceeds its final error by more than a few tens of microvolts: as soon as the output sags, the error amplifier drives the gate harder, the pass device's $g_m$ rises, and the loop speeds up. With a microfarad of output capacitance, droop here is set by DC loop gain, not by speed.

### 3.7 Capacitor-less LDOs

An on-chip regulator cannot have a microfarad; its output capacitance $C_o$ is the load's decoupling, tens to hundreds of picofarads. The loop is then a two-stage amplifier (20-02) whose second stage is the pass device and whose load is $C_o$: Miller compensation across the pass device splits the poles, and the second pole is about $g_{mp}/C_o$. Here is the light-load problem in its capless form: at 100 µA, $g_{mp}/(2\pi C_o)$ is **4.50** MHz for 100 pF, against **0.499** GHz at 100 mA, so the loop's bandwidth must be designed for the lightest load. Designers bound the minimum load, bias the error amplifier adaptively with the load current, or add fast local feedback around the pass device.

**Transients set the real limit.** Without a large capacitor, $\Delta V \approx \Delta I\,t_{resp}/C_o$. Keeping a 100 mA step to a 100 mV dip with 100 pF needs a response time of **0.1** ns: a loop bandwidth in the gigahertz range, which is why fast capless designs use local loops around the pass device rather than relying on the error amplifier.

### 3.8 Digital LDOs

At very low supplies an analog error amplifier runs out of headroom. A **digital LDO** replaces it with a clocked comparator and replaces the single pass device with an array of $N$ identical PMOS switches; each clock cycle, a controller turns one more switch on if the output is low, or one off if it is high. It works down to supplies too low for an analog error amplifier, and it scales with digital processes. It has three characteristic limits:

- **Resolution and ripple.** The output current moves in steps of one switch's current $I_u$, so the output settles into a **limit cycle**, a small oscillation of order $I_u/(f_{clk}C_o)$.
- **Speed.** A one-switch-per-cycle controller can follow load changes only at $I_uf_{clk}$ amperes per second; faster designs use coarse/fine arrays and event-driven control.
- **Supply rejection.** A switch in triode is a resistor from $V_{in}$ to $V_{out}$, so input ripple passes through until the controller reacts.

## 4. Worked examples

All examples use the running design of §3: T130 PMOS pass device at $L$ = 0.15 µm, $V_{out}$ = 1.2 V, β = 0.5, $C_L$ = 1 µF with 5 mΩ ESR, $R_{div}$ = 1.2 MΩ, $g_{ma}$ = 1 mS, $R_a$ = 100 kΩ, $C_a$ = 0.2 pF, $g_{mb}$ = 2 mS, $I_Q$ = 120 µA, unless stated.

### Example 20-04.1 · Efficiency and headroom (tier A)

**Setup.** Find the efficiency at 100 mA from 1.8 V and from 1.35 V, and at 100 µA from 1.8 V.

**Solution.** $\eta = V_{out}I_L/[V_{in}(I_L + I_Q)]$:

- 1.8 V, 100 mA: 1.2 × 0.1/(1.8 × 0.10012) = **66.6**%.
- 1.35 V, 100 mA: **88.8**%.
- 1.8 V, 100 µA: 1.2 × 10⁻⁴/(1.8 × 2.2 × 10⁻⁴) = **30.3**%.

**Sanity check.** At full load the efficiency is nearly $V_{out}/V_{in}$ (66.7% and 88.9%); at light load the quiescent current dominates. Low dropout pays only if the input really sits close to the output, for example after a switching converter set just above the LDO's output.

### Example 20-04.2 · Sizing the pass device (tier B)

**Setup.** Size the PMOS pass device for 150 mV of dropout at 100 mA with $V_{in}$ = 1.35 V. Then find its gate capacitance $\tfrac23WLC_{ox}$, and its $V_{SG}$, $g_m/I_D$ and inversion coefficient at 100 µA and 100 mA when $V_{in}$ = 1.8 V.

**Solution.**

*Dropout.* With $V_{SG}$ = 1.35 V and $V_{SD}$ = 0.15 V, the long-channel model needs $W$ = **1.609** mm. The field 0.15 V/0.15 µm = 1 V/µm against $E_{sat}$ = 6.0 V/µm gives a factor of **1.167**, so $W$ = **1.877** mm.

*Gate capacitance.* $\tfrac23(1.877\text{ mm})(0.15\text{ µm})(8.6\text{ fF/µm}^2)$ = **1.614** pF.

*Operating points* (saturation, with 20-01's velocity-saturation term):

| $I_L$ | $V_{SG}$ | $g_m/I_D$ | $IC$ |
|---|---|---|---|
| 100 µA | **0.353** V | **28.3** S/A | **0.0535** |
| 100 mA | **1.028** V | **3.14** S/A | **53.5** |

The gate therefore sits at **1.447** V at light load and **0.772** V at full load (from 1.8 V), and must reach 0 V at dropout.

**Sanity check.** The device spans weak to strong inversion across the load range, so its $g_m$ changes by a factor of about 111 while the current changes by 1000. The error amplifier's output must swing over most of the supply.

### Example 20-04.3 · Loop gain and regulation (tier B)

**Setup.** At 100 µA and at 100 mA, find $g_{mp}$, $r_{ds}$, $R_{out}$, the DC loop gain, the closed-loop output impedance and the line regulation (gate tracking the supply). Then find the DC output change when the load steps from 100 µA to 100 mA.

**Solution.**

| | 100 µA | 100 mA |
|---|---|---|
| $g_{mp}$ | **2.83** mS | **0.3136** S |
| $r_{ds}$ = 1.2 V/$I_L$ | **12.0** kΩ | **12.0** Ω |
| $R_{out} = r_{ds} \parallel R_L \parallel R_{div}$ | **5.97** kΩ | **6.00** Ω |
| $L_0 = A_{EA}\beta g_{mp}R_{out}$ | **844** (**58.5** dB) | **94.1** (**39.5** dB) |
| Output impedance $R_{out}/(1 + L_0)$ | **7.07** Ω | **63.1** mΩ |
| Line regulation $g_{ds}R_{out}/(1 + L_0)$ | **0.589** mV/V | **5.26** mV/V |

*Large step.* $\Delta V_{SG}$ = 1.028 − 0.353 = 0.675 V, so $\Delta V_{out} \approx -0.675/(100 \times 0.5)$ = **−13.5** mV. Solving the DC equations exactly (including the pass device's output conductance) gives **−13.4** mV.

**Sanity check.** The loop gain *falls* with load, because $R_{out}$ falls faster than $g_{mp}$ rises; yet the output impedance improves, because it depends on $1/g_{mp}$. Forty decibels of error-amplifier gain buys about 1% load regulation; better regulators use more gain and must then work harder for stability (§3.4).

### Example 20-04.4 · Stability across load and capacitor (tier B)

**Setup.** Find the crossover and phase margin at 100 µA, 1 mA, 10 mA and 100 mA. Then repeat the 100 µA and 100 mA cases with a 0.1 µF and with a 10 µF output capacitor (5 mΩ ESR).

**Solution.** With $p_a/2\pi$ = **7.96** MHz and $p_g/2\pi$ = **197** MHz:

| $I_L$ | Crossover | Phase margin |
|---|---|---|
| 100 µA | **22.5** kHz | **89.9**° |
| 1 mA | **169** kHz | **89.1**° |
| 10 mA | **780** kHz | **85.8**° |
| 100 mA | **2.39** MHz | **77.5**° |

With 0.1 µF: **225** kHz and **88.4**° at 100 µA, but **13.0** MHz and **31.2**° at 100 mA. With 10 µF: **2.25** kHz and **90.1**° at 100 µA, **250** kHz and **93.2**° at 100 mA (the ESR zero at 3.18 MHz adds lead).

**Sanity check.** The crossover scales with $g_{mp}/C_L$ (§3.4): ten times less capacitance gives ten times the crossover, which at full load lands above the error amplifier's 7.96 MHz pole. "Use at least 1 µF" in an LDO data sheet is a stability requirement, not a suggestion.

### Example 20-04.5 · Supply rejection (tier B)

**Setup.** At 100 mA, find the PSRR at DC, 1 MHz and 10 MHz with the gate tracking the supply ($k$ = 1) and with a ground-referenced gate ($k$ = 0). Also find the DC PSRR at 100 µA ($k$ = 1).

**Solution.** From §3.5's expression:

| | DC | 1 MHz | 10 MHz |
|---|---|---|---|
| $k$ = 1 | **45.6** dB | **45.9** dB | **56.3** dB |
| $k$ = 0 | **32.0** dB | **32.3** dB | **42.8** dB |

At 100 µA, $k$ = 1: **64.6** dB.

**Sanity check.** The 13.6 dB difference is $20\log[(g_{mp} + g_{ds})/g_{ds}]$, the pass device's intrinsic gain plus one, about 4.8 at full load (where $g_{mp}r_{ds}$ = 3.76). Rejection improves at 10 MHz because the capacitor shorts the output; it is worse at full load because $r_{ds}$ is smallest there.

### Example 20-04.6 · A large load step (tier C)

**Setup.** The load steps from 100 µA to 100 mA in 1 ns. (a) Estimate the dip from §3.6 at the full-load operating point. (b) Simulate the nonlinear loop (pass-device current from the charge-based model, linear error amplifier and buffer) and find the minimum output deviation, its time and the final deviation. (c) For an on-chip capacitor of 100 pF, what response time would keep the same 100 mA step to a 100 mV dip?

**Solution.**

(a) $\Delta I/(\omega_cC_L)$ = 0.0999/(2π × 2.39 MHz × 1 µF) = **6.64** mV, plus **0.50** mV of ESR drop.

(b) The simulated output reaches **−13.43** mV at **0.304** µs and settles at **−13.41** mV: the dip is essentially the DC load-regulation error, with no transient overshoot of consequence. (The simulation omits the ESR; its drop vanishes near the minimum, where the capacitor current is nearly zero.)

(c) $t_{resp} = C_o\Delta V/\Delta I$ = (100 pF)(0.1 V)/(0.1 A) = **0.1** ns.

**Sanity check.** Even starting from light load, where the small-signal crossover is only 22.5 kHz, the loop speeds up as the gate moves and the pass device's $g_m$ grows; the 1 µF capacitor gives it time to do so. Remove the capacitor and the same physics demands a sub-nanosecond loop: the capless designer's problem. The simulation treats the error amplifier and buffer as linear; real ones have finite output current and slew-limit when the gate must move 0.675 V at once, which lengthens the response and deepens the dip by roughly $\Delta I$ times the extra delay divided by $C_L$.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 20-04.1a | efficiency, 1.8 V, 100 mA | 66.6 | % |
| Ex 20-04.1b | efficiency, 1.35 V, 100 mA | 88.8 | % |
| Ex 20-04.1c | efficiency, 1.8 V, 100 uA | 30.3 | % |
| Ex 20-04.1d | V_out/V_in at 1.8 V | 66.7 | % |
| Ex 20-04.1e | V_out/V_in at 1.35 V | 88.9 | % |
| Ex 20-04.2a | long-channel width | 1.609 | mm |
| Ex 20-04.2b | velocity-saturation factor | 1.167 | — |
| Ex 20-04.2c | width | 1.877 | mm |
| Ex 20-04.2d | gate capacitance | 1.614 | pF |
| Ex 20-04.2e | V_SG at 100 uA | 0.353 | V |
| Ex 20-04.2f | V_SG at 100 mA | 1.028 | V |
| Ex 20-04.2g | g_m/I_D at 100 uA | 28.3 | S/A |
| Ex 20-04.2h | g_m/I_D at 100 mA | 3.14 | S/A |
| Ex 20-04.2i | IC at 100 uA | 0.0535 | — |
| Ex 20-04.2j | IC at 100 mA | 53.5 | — |
| Ex 20-04.2k | gate voltage at light load | 1.447 | V |
| Ex 20-04.2l | gate voltage at full load | 0.772 | V |
| Ex 20-04.2m | E_sat | 6.0 | V/µm |
| Ex 20-04.2n | g_m ratio, full to light load | 111 | — |
| Ex 20-04.3a | g_mp at 100 uA | 2.83 | mS |
| Ex 20-04.3b | g_mp at 100 mA | 0.3136 | S |
| Ex 20-04.3c | r_ds at 100 uA | 12.0 | kΩ |
| Ex 20-04.3d | r_ds at 100 mA | 12.0 | Ω |
| Ex 20-04.3e | R_out at 100 uA | 5.97 | kΩ |
| Ex 20-04.3f | R_out at 100 mA | 6.00 | Ω |
| Ex 20-04.3g | L_0 at 100 uA | 844 | — |
| Ex 20-04.3h | L_0 at 100 uA in dB | 58.5 | dB |
| Ex 20-04.3i | L_0 at 100 mA | 94.1 | — |
| Ex 20-04.3j | L_0 at 100 mA in dB | 39.5 | dB |
| Ex 20-04.3k | output impedance at 100 uA | 7.07 | Ω |
| Ex 20-04.3l | output impedance at 100 mA | 63.1 | mΩ |
| Ex 20-04.3m | line regulation at 100 uA | 0.589 | mV/V |
| Ex 20-04.3n | line regulation at 100 mA | 5.26 | mV/V |
| Ex 20-04.3o | Delta V_SG | 0.675 | V |
| Ex 20-04.3p | estimated output change | −13.5 | mV |
| Ex 20-04.3q | exact output change | −13.4 | mV |
| Ex 20-04.4a | p_a/2 pi | 7.96 | MHz |
| Ex 20-04.4b | p_g/2 pi | 197 | MHz |
| Ex 20-04.4c | crossover, 100 uA | 22.5 | kHz |
| Ex 20-04.4d | PM, 100 uA | 89.9 | ° |
| Ex 20-04.4e | crossover, 1 mA | 169 | kHz |
| Ex 20-04.4f | PM, 1 mA | 89.1 | ° |
| Ex 20-04.4g | crossover, 10 mA | 780 | kHz |
| Ex 20-04.4h | PM, 10 mA | 85.8 | ° |
| Ex 20-04.4i | crossover, 100 mA | 2.39 | MHz |
| Ex 20-04.4j | PM, 100 mA | 77.5 | ° |
| Ex 20-04.4k | crossover, 0.1 uF, 100 uA | 225 | kHz |
| Ex 20-04.4l | PM, 0.1 uF, 100 uA | 88.4 | ° |
| Ex 20-04.4m | crossover, 0.1 uF, 100 mA | 13.0 | MHz |
| Ex 20-04.4n | PM, 0.1 uF, 100 mA | 31.2 | ° |
| Ex 20-04.4o | crossover, 10 uF, 100 uA | 2.25 | kHz |
| Ex 20-04.4p | PM, 10 uF, 100 uA | 90.1 | ° |
| Ex 20-04.4q | crossover, 10 uF, 100 mA | 250 | kHz |
| Ex 20-04.4r | PM, 10 uF, 100 mA | 93.2 | ° |
| Ex 20-04.4s | ESR zero, 10 uF | 3.18 | MHz |
| Ex 20-04.5a | PSRR k = 1, DC | 45.6 | dB |
| Ex 20-04.5b | PSRR k = 1, 1 MHz | 45.9 | dB |
| Ex 20-04.5c | PSRR k = 1, 10 MHz | 56.3 | dB |
| Ex 20-04.5d | PSRR k = 0, DC | 32.0 | dB |
| Ex 20-04.5e | PSRR k = 0, 1 MHz | 32.3 | dB |
| Ex 20-04.5f | PSRR k = 0, 10 MHz | 42.8 | dB |
| Ex 20-04.5g | PSRR k = 1, DC, 100 uA | 64.6 | dB |
| Ex 20-04.5h | difference k = 1 vs k = 0 | 13.6 | dB |
| Ex 20-04.5i | (g_mp + g_ds)/g_ds | 4.8 | — |
| Ex 20-04.5j | g_mp r_ds at 100 mA | 3.76 | — |
| Ex 20-04.6a | linear dip estimate | 6.64 | mV |
| Ex 20-04.6b | ESR drop | 0.50 | mV |
| Ex 20-04.6c | simulated minimum deviation | −13.43 | mV |
| Ex 20-04.6d | time of the minimum | 0.304 | µs |
| Ex 20-04.6e | final deviation | −13.41 | mV |
| Ex 20-04.6f | capless response time | 0.1 | ns |
| Txt 20-04.a | velocity-saturation factor | 1.167 | — |
| Txt 20-04.b | E_sat | 6.0 | V/µm |
| Txt 20-04.c | crossover at 100 uA | 22.5 | kHz |
| Txt 20-04.d | crossover at 100 mA | 2.39 | MHz |
| Txt 20-04.e | PM with 0.1 uF at 100 mA | 31.2 | ° |
| Txt 20-04.f | PSRR k = 1 at 100 mA | 45.6 | dB |
| Txt 20-04.g | PSRR k = 0 at 100 mA | 32.0 | dB |
| Txt 20-04.h | linear dip | 6.64 | mV |
| Txt 20-04.i | ESR drop | 0.50 | mV |
| Txt 20-04.j | DC regulation error | 13.4 | mV |
| Txt 20-04.k | capless second pole at 100 uA | 4.50 | MHz |
| Txt 20-04.l | capless second pole at 100 mA | 0.499 | GHz |
| Txt 20-04.m | capless response time | 0.1 | ns |
| Txt 20-04.n | efficiency with 600 mV headroom | 67 | % |
| Txt 20-04.o | efficiency with 150 mV headroom | 89 | % |
| Txt 20-04.p | current efficiency, 100 uA load, 120 uA I_Q | 45 | % |

## 5. Simulate it

The lab ([labs/20-04-lab](../labs/20-04-lab/README.md)) implements the running design in `ldo.py` (pass-device sizing, operating points, loop gain, output impedance, supply rejection, linear step response) and confirms the loop in ngspice.

**Predict, then run.**

1. Predict the pass-device width for 100 mV of dropout, then size it (Part 1).
2. Predict how the crossover and phase margin change from 100 µA to 100 mA, then plot the loop gain at four loads and run `ngspice -b ldo_loop.cir` (Part 2).
3. Predict the PSRR at DC with $k$ = 1 and $k$ = 0, then plot PSRR against frequency and run `ngspice -b ldo_psrr.cir` (Part 3).
4. Predict the dip for a 100 µA → 100 mA step, then run the nonlinear simulation, and again with 0.1 µF (Part 4).
5. Make the error amplifier ten times slower ($C_a$ = 2 pF) and predict what happens to the margin and to the PSRR between 10 kHz and 1 MHz (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Lower dropout (wider pass device) | Efficiency, headroom | Area; gate capacitance (slower gate, more driver current) | Power-management architect with the analog designer |
| Higher error-amplifier gain | Load and line regulation, PSRR | Stability margin, or bandwidth if compensated harder | Analog designer |
| Larger output capacitor | Stability (output-pole dominant), transient dip, high-frequency PSRR | Board area and cost, start-up inrush; ESR constraints | System designer with the LDO vendor |
| Gate driver referenced to $V_{in}$ ($k$ → 1) | Low-frequency PSRR by the pass device's intrinsic gain | Driver design and headroom | Analog designer |
| Higher quiescent current | Faster loop, better transients and PSRR | Light-load (current) efficiency, battery life | Product definition (wearables vs infrastructure) |
| Capacitor-less (on-chip) design | No external part, per-domain regulation on chip | Large droop unless the loop is extremely fast; light-load stability | SoC power architect |
| Digital LDO | Operation at very low supply, process scalability | Limit-cycle ripple, poor high-frequency PSRR, quantized response | SoC power architect |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Efficiency bound | $V_{out}/V_{in}$ | exact; times the current efficiency $I_L/(I_L + I_Q)$ |
| PMOS LDO dropout at rated current (as of Nov 2026) | about 100–300 mV | TI TPS7A20: 140 mV max at 300 mA; TLV755P: 215 mV max at 500 mA; TPS7A83A: 200 mV max at 2 A [R-330] |
| Quiescent current of discrete LDOs (as of Nov 2026) | 25 nA to 15 mA | TPS7A02 nanopower (25 nA typ) to TPS7A94 ultra-low-noise (15 mA ground current) [R-330] |
| PSRR of good discrete LDOs (as of Nov 2026) | 55–110 dB at 1 kHz; about 45–50 dB at 1 MHz | TPS7A20: 45 dB at 1 MHz (20 mA); TPS7A94: 51 dB at 1 MHz (750 mA) [R-330] |
| Output noise, 10 Hz–100 kHz (as of Nov 2026) | 0.46 µVrms to 130 µVrms | TPS7A94 vs TPS7A02 [R-330] |
| Minimum output capacitor, discrete LDOs | 1 µF (general purpose) to 10–22 µF (high current, low noise) | data-sheet requirements [R-330] |
| On-chip output capacitance | tens of pF to about 1 nF | 100 pF (Milliken et al., 2007), 0.6 nF (Hazucha et al., 2005) [R-328] |
| Response time $C\Delta V/\Delta I$ of a fast on-chip LDO | about 0.5 ns | 0.54 ns: 90 mV droop, 100 mA step, 0.6 nF, 90 nm (Hazucha et al., 2005) [R-328] |
| Processor digital LDO current density (as of Nov 2026) | tens to hundreds of A/mm² | 40 A/mm² (5 nm, 2021), 263 A/mm² (3 nm, 2024) [R-329] |

## 8. Common mistakes

- **Checking stability at one load.** The loop's crossover moves with load current by two decades; check the lightest and the heaviest loads, and every output capacitor the data sheet allows.
- **Sizing the pass device for saturation.** At dropout it is in triode with its gate at ground; size it there, and add the velocity-saturation correction.
- **Quoting PSRR at DC.** The useful number is at the frequency of the ripple being rejected, typically hundreds of kilohertz to a few megahertz after a switching regulator.
- **A ground-referenced gate driver.** It costs the pass device's intrinsic gain in supply rejection (§3.5).
- **Forgetting quiescent current at light load.** A regulator that idles at 120 µA is useless for a wearable that spends most of its life drawing microamps.
- **Treating a capless LDO like an external-capacitor one.** Without the capacitor, droop is $\Delta I\,t_{resp}/C_o$; the response time, not the loop gain, decides it.
- **Ignoring the reference.** The regulator's output is no more accurate or quieter than its reference times $1/\beta$ (20-03).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The classic designs [Established].** Rincón-Mora and Allen (1998) built a CMOS LDO that runs from a 1 V input with 23 µA of zero-load quiescent current, by exploiting the load dependence of the loop's poles that §3.4 derived [1]. Hazucha et al. (2005) put a regulator for a microprocessor on a 90 nm die: 1.2 V in, 0.9 V out, 0.54 ns response time with 0.6 nF of on-chip capacitance, a 90 mV droop for a 100 mA step, and 94% current efficiency [2]. Milliken et al. (2007) removed the external capacitor entirely, stable from 0 to 50 mA with up to 100 pF of load [3]. Okuma et al. (2010) replaced the error amplifier with digital control to regulate from a 0.5 V input at 2.7 µA quiescent current [4]; it is widely cited as the first digital LDO, though earlier digitally controlled linear regulators exist [R-328].
- **Research has moved to supply rejection and speed without a capacitor [Established].** Feed-forward ripple cancellation reached more than 60 dB of PSRR over a 10 MHz range and a 100 mA load range (Jiang, Shu and Chang, 2018); an adaptive ripple-cancellation capless design kept PSR better than −36 dB from 10 kHz to 1 GHz with 240 pF (Lim et al., 2018). A digitally assisted 500 mA capless LDO with 250 pF dips 55 mV for a 450 mA step with 100 ns edges at 120 µA quiescent current (Chen, Lu and Mok, 2021) [5], [R-328].
- **Processors regulate per core [Established for the existence; details mostly not public].** AMD's Zen core paper states that "each core has a digital low drop-out (LDO) voltage regulator" for per-core voltage and frequency (ISSCC 2017) [6]. IBM's POWER8 uses distributed, digitally controlled microregulators that function as a fast LDO, with 90.5% peak efficiency, "only 3.1% worse than an ideal LDO," and a bypass mode at maximum performance [6]. Intel and Samsung circuit papers report on-die LDOs up to 4 A (Intel 4, 2022) and a 10 A digital LDO at 263 A/mm² in a 3 nm GAAFET process (2024), but do not name shipping products [R-329]. Their measured performance in products is not public **[Contested]**.
- **Discrete LDOs span six orders of magnitude in quiescent current [Established].** TI's TPS7A02 idles at 25 nA with 130 µVrms of noise; the TPS7A94 reaches 0.46 µVrms and 110 dB at 1 kHz, but draws 15 mA of ground current at light load (data sheets revised 2022–2026) [7].

### Why it matters commercially

LDOs are the most common power block on a mixed-signal chip and among the most common catalog parts, so the commercial question is rarely "LDO or not" but "which trade-off". In wearables and IoT, quiescent current and light-load efficiency decide battery life: a nanopower LDO at 25 nA exists because an always-on domain spends most of its life drawing microamps, and an LDO in the wrong place can cost more average power than the domain it supplies (Problem 20-04.13). In AI accelerators and server processors, per-core LDOs under a shared rail let each core run at its own minimum voltage. They are efficient only when the cores' voltages are close to the rail's, which is why POWER8's regulator has a bypass mode [6]. In automotive, RF and data-converter products, LDOs after switching converters set the noise floor of PLLs and ADCs, so the PSRR at the converter's switching frequency is a system specification. For an acquirer, a power-management team's value is in what it knows about these trade-offs (stability across load and capacitor corners, PSRR at megahertz, droop with on-chip capacitance), not in the LDO topology, which is textbook.

### Marketing vs Reality

- **"110 dB PSRR."** At 1 kHz under headline conditions. The same TPS7A94 data sheet lists 51 dB at 1 MHz in its electrical-characteristics table [7]. TI's own application note shows PSRR falling with load current and headroom and changing character above the loop's unity-gain frequency [8]. Ask for the value at your ripple frequency, load and headroom.
- **"Ultra-low noise."** The 0.46 µVrms part draws 15 mA of ground current [7]. Low noise is bought with current, like everything in analog (20-01).
- **"25 nA quiescent current."** At no load. The same part's PSRR is 55 dB at 1 kHz and its noise 130 µVrms [7]. Fine for a sensor hub, not for a PLL supply.
- **Monotonic PSRR curves.** The TLV755P's PSRR is 52 dB at 1 kHz, 46 dB at 100 kHz and 52 dB at 1 MHz [7]: the dip where the loop gain has fallen but the output capacitor has not yet taken over, as §3.5 predicts.
- **Transient figures of merit.** Response time $C\Delta V/\Delta I$ and quiescent-current-weighted FoMs are defined differently from paper to paper; recomputing one recent paper's FoM from its abstract with the common formula gives 0.0082 ps against the 0.0073 ps it reports [R-328]. Compare the raw numbers instead: $\Delta I$, edge rate, droop, on-chip capacitance and $I_Q$.
- **Sanity check.** Efficiency is at most $V_{out}/V_{in}$ whatever the brochure says; droop is at least $\Delta I\,t_{resp}/C$; and a stability claim without a load range and an output-capacitor range (after DC-bias derating) is incomplete.

### Questions for engineering leaders

1. **"What are your phase margins at minimum and maximum load, with the smallest and largest output capacitance you allow?"** Strong: a corner table, with capacitance derated for DC bias and temperature. Evasive: "it's stable with 1 µF".
2. **"What is the PSRR at our switching converter's frequency, at our load and headroom?"** Strong: measured curves at those conditions, and an explanation of which region (loop gain or output capacitor) sets it. Evasive: the 1 kHz number.
3. **"How far does the output dip for our load step, at our edge rate, with the on-chip capacitance we actually have?"** Strong: a $C\Delta V/\Delta I$ budget backed by silicon data at a stated edge rate. Evasive: a figure of merit.
4. **"What does the per-core LDO cost in efficiency compared with an integrated buck or a switched-capacitor converter, across the voltage range we run?"** Strong: efficiency ≈ $V_{out}/V_{in}$, how often cores sit far below the rail, bypass and power-gate modes. Evasive: peak efficiency only.
5. **"For your digital LDO, what are the limit-cycle ripple and the supply rejection at high frequency?"** Strong: measured ripple against clock rate and unit size, and how ripple from the input is handled. Evasive: "it's digital, so it scales".

## 10. Concept check

**Q1.** Why is an LDO's efficiency bounded by $V_{out}/V_{in}$, and when is it far below that bound?

<details><summary>Answer</summary>

The full load current flows from $V_{in}$ through the pass device to $V_{out}$, so the power delivered is at most $V_{out}/V_{in}$ of the power drawn. At light load the quiescent current becomes comparable to the load current, and the current efficiency $I_L/(I_L + I_Q)$ pulls the efficiency far below the bound.

</details>

**Q2.** Why is the pass device sized in triode rather than in saturation?

<details><summary>Answer</summary>

At dropout the error amplifier has pulled the gate to ground and the device has only $V_{DO}$ across it, much less than its overdrive, so it operates in triode. That is the worst case for current capability, so the width must be chosen there.

</details>

**Q3.** In an LDO with a large output capacitor, why is the phase margin worst at full load?

<details><summary>Answer</summary>

The crossover is about $A_{EA}\beta g_{mp}/C_L$, proportional to the pass device's transconductance, which is largest at full load. The crossover then approaches the error amplifier's and gate's poles, which stay put, and their phase lag erodes the margin.

</details>

**Q4.** Why does the gate driver's reference (ground or $V_{in}$) change the supply rejection by the pass device's intrinsic gain?

<details><summary>Answer</summary>

If the gate is fixed relative to ground, supply ripple appears directly as $v_{sg}$ and injects $g_{mp}v_{in}$ into the output. If the gate follows $V_{in}$, $v_{sg}$ sees no ripple and only $g_{ds}v_{in}$ is injected. The ratio of the two injections is $(g_{mp} + g_{ds})/g_{ds}$, the intrinsic gain plus one.

</details>

**Q5.** Why does supply rejection usually get worse in the tens of kilohertz to megahertz range?

<details><summary>Answer</summary>

Rejection is the injection divided by $1 + L$. Above the error amplifier's dominant pole the loop gain falls while the injection does not, so the ripple reaching the output grows until the crossover. Above the crossover the output capacitor shorts the ripple and rejection improves again.

</details>

**Q6.** A capless LDO must handle a 50 mA load step with at most 50 mV of droop on 100 pF. What response time does that imply, and what does it say about its loop?

<details><summary>Answer</summary>

$t_{resp} = C_o\Delta V/\Delta I$ = 100 pF × 50 mV/50 mA = 0.1 ns. The loop must act within about a tenth of a nanosecond, which needs a local fast loop around the pass device; an error amplifier with megahertz bandwidth cannot do it.

</details>

**Q7.** What sets the output ripple of a digital LDO in steady state?

<details><summary>Answer</summary>

The controller can only change the current in steps of one switch, so it hunts between two states, a limit cycle. The ripple is of order one unit current times one clock period divided by the output capacitance, $I_u/(f_{clk}C_o)$.

</details>

Problems: [20-04 problem set](../problems/20-04-problems.md) · Worked solutions: [20-04 solutions](../solutions/20-04-solutions.md)

## 11. Key terms

[Low-dropout regulator (LDO)](../../../reference/glossary.md#low-dropout-regulator-ldo) · [Dropout voltage](../../../reference/glossary.md#dropout-voltage) · [Pass device](../../../reference/glossary.md#pass-device) · [Load regulation](../../../reference/glossary.md#load-regulation) · [Line regulation](../../../reference/glossary.md#line-regulation) · [Current efficiency](../../../reference/glossary.md#current-efficiency) · [Capacitor-less LDO](../../../reference/glossary.md#capacitor-less-ldo) · [Digital LDO](../../../reference/glossary.md#digital-ldo) · [Power-supply rejection ratio (PSRR)](../../../reference/glossary.md#power-supply-rejection-ratio-psrr) · [Quiescent current](../../../reference/glossary.md#quiescent-current)

## 12. Connections

- **Previous:** [20-03](20-03-bandgap-references.md) supplies the reference; its 0.6 V current-mode output is the running design's $V_{REF}$.
- **Builds on:** [15-12](../../15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) (the LDO loop, ESR window), [20-01](20-01-analog-design-fundamentals-gm-id.md) (the charge-based model), [20-02](20-02-two-stage-op-amp-design.md) (compensation, PSRR, the two-stage view of capless LDOs), [09-10](../../09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) (velocity saturation).
- **Next:** [20-05](20-05-comparators-and-sample-and-hold.md) begins the data-converter building blocks, whose accuracy depends on clean supplies and references.
- **Used later:** [20-10](20-10-plls-and-jitter.md) (supply noise and oscillator jitter), [18-09](../../18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md) (power domains in microcontrollers), and the capstones' power-delivery discussions.

## 13. Further study

- G. A. Rincón-Mora, *Analog IC Design with Low-Dropout Regulators*, 2nd ed., McGraw-Hill, 2014: the book-length treatment of LDO design.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the voltage-regulator sections.
- Texas Instruments application notes on LDO terms, PSRR and stability (cited in §14) for how specifications are defined and measured.
- Lecture videos: power-management IC lectures from university courses on analog IC design (search for "LDO regulator design lecture"), and vendor training series on LDO fundamentals.

## 14. Sources

1. G. A. Rincón-Mora and P. E. Allen, "A low-voltage, low quiescent current, low drop-out regulator," *IEEE J. Solid-State Circuits*, vol. 33, no. 1, pp. 36–44, Jan. 1998, DOI 10.1109/4.654935 [R-328].
2. P. Hazucha, T. Karnik, B. A. Bloechel, C. Parsons, D. Finan and S. Borkar, "Area-efficient linear regulator with ultra-fast load regulation," *IEEE J. Solid-State Circuits*, vol. 40, no. 4, pp. 933–940, Apr. 2005, DOI 10.1109/JSSC.2004.842831 [R-328].
3. R. J. Milliken, J. Silva-Martínez and E. Sánchez-Sinencio, "Full on-chip CMOS low-dropout voltage regulator," *IEEE Trans. Circuits Syst. I*, vol. 54, no. 9, pp. 1879–1890, Sep. 2007, DOI 10.1109/TCSI.2007.902615 [R-328].
4. Y. Okuma et al., "0.5-V input digital LDO with 98.7% current efficiency and 2.7-µA quiescent current in 65nm CMOS," *Proc. IEEE CICC*, Sep. 2010, DOI 10.1109/CICC.2010.5617586 [R-328].
5. Recent LDO research: Leung and Mok (JSSC, Oct. 2003); Guo and Leung (JSSC, Sep. 2010); Jiang, Shu and Chang (JSSC, Aug. 2018); Lim et al. (JSSC, Sep. 2018); Chen, Lu and Mok (JSSC, Feb. 2021); Park et al. (JSSC, Oct. 2023); An et al. (JSSC, May 2026) [R-328].
6. Processor regulators: T. Singh et al., "Zen: A next-generation high-performance ×86 core," *ISSCC* 2017, paper 3.2, DOI 10.1109/ISSCC.2017.7870256; Z. Toprak-Deniz et al., "Distributed system of digitally controlled microregulators enabling per-core DVFS for the POWER8 microprocessor," *ISSCC* 2014, paper 5.2, DOI 10.1109/ISSCC.2014.6757354; Intel and Samsung circuit papers (ISSCC 2015, 2016, 2021, 2022, 2024; JSSC 2016, 2020, 2021) [R-329].
7. Texas Instruments data sheets TPS7A02 (SBVS277C), TPS7A20 (SBVS338H), TPS7A94 (SBVS336C), TPS7A47 (SBVS204G), TPS7A83A (SBVS304B), TLV755P (SBVS320D) [R-330].
8. TI application notes: B. S. Lee, "Understanding the terms and definitions of LDO voltage regulators," SLVA079, Oct. 1999; J. C. Teel, "Understanding power supply ripple rejection in linear regulators," *Analog Applications Journal* SLYT202, 2Q 2005; S. Pithadia, S. Lester and A. Verma, "LDO PSRR measurement simplified," SLAA414A, rev. Aug. 2017; "Linear regulators: theory of operation and compensation," SNVA020B (AN-1148), rev. May 2013 [R-330].
9. G. A. Rincón-Mora, *Analog IC Design with Low-Dropout Regulators*, 2nd ed., McGraw-Hill, 2014; B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017.
10. Course chapters [15-12](../../15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) (the LDO loop), [20-01](20-01-analog-design-fundamentals-gm-id.md) (charge-based model) and [20-02](20-02-two-stage-op-amp-design.md) (compensation).
