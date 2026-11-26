# C1 Option B · Reference Design Report: a 1.2 V Synchronous Buck with Type III Control

This is the reference solution to [Capstone C1, option B](../README.md): a 2 MHz synchronous buck from one lithium-ion cell to a 1.2 V core rail, with voltage-mode control. Work the capstone yourself first. Every hand-calculated number below is recomputed by [verify_c1b.py](verify_c1b.py). Every simulated number comes from the netlists in this folder, which CI re-runs, and is tabulated in [results.md](results.md).

**Prerequisites used:** [22-02](../../../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md) (buck steady state), [22-06](../../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md) (losses), [22-07](../../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md) (dynamics and control) and [15-09](../../../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md) (compensation).

---

## 1. Specification and models

The brief's requirements: output 1.2 V within ±1%; ripple ≤ 10 mV peak-to-peak at 4.2 V, 1 A; a 0.1 → 0.6 A load step in 100 ns deviating ≤ 36 mV and recovering to within 1% in ≤ 30 µs at every input voltage; crossover from 50 kHz to $f_{sw}/10$ = 200 kHz, phase margin ≥ 45° and gain margin ≥ 10 dB at every corner; efficiency ≥ 85% at 0.5 A, 3.6 V; peak inductor current ≤ 1.5 A.

Two models carry the verification, and they answer different questions:

- **[buck_avg.sub](buck_avg.sub), the averaged model.** It replaces the switches with their cycle averages ([22-07](../../../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)), so it gives the loop gain directly in an AC analysis and runs a load step in milliseconds. It includes the conduction drops, and the dead times with the body diode chosen by the sign of the current at each edge (§6).
- **[buck_sw.sub](buck_sw.sub), the switching model.** It simulates every cycle: a sawtooth PWM, 10 ns dead times, both body diodes, gate-drive and quiescent losses, and a soft-start. It is the reference for ripple, efficiency, peak current and the load step, and it checks the averaged model.

## 2. Power stage

**Duty cycle.** Ideally $D = V_o/V_{in}$: **0.400**, **0.333** and **0.286** at 3.0, 3.6 and 4.2 V. The losses add a few percent, which the loop supplies.

**Inductor.** The ripple $\Delta I = V_o(1 - D)/(Lf_{sw})$ is largest at the highest input. A ripple of 40% of the 1 A full load at 4.2 V needs $L = V_o(1 - D)/(0.4 \times 1\ \text{A} \times f_{sw})$ = **1.07** µH, so the design uses a standard 1.0 µH. The ripple is then **0.360**, **0.400** and **0.429** A at the three inputs. The worst case for the peak current is 4.2 V with $L$ −20%: $\Delta I$ = **0.536** A, so the inductor current swings from **0.732** to **1.27** A, inside the 1.5 A saturation rating.

**Output capacitor: sized by the load step, not the ripple.** A loop that crosses over at $f_c$ lets the capacitor carry a load step for about a quarter of a loop period. A first-order estimate of the dip is $\Delta V \approx \Delta I_{step}/(2\pi f_cC)$. With a 0.5 A step, an 85 kHz crossover (§3) and a 25 mV target (leaving room for corners), $C \ge 0.5/(2\pi \times 85\ \text{kHz} \times 25\ \text{mV})$ = **37.4** µF. Two 22 µF ceramics give 44 µF, with 1.5 mΩ combined ESR, and an estimated dip of **21.3** mV.

The ripple is then tiny. At the worst corner (4.2 V, $L$ and $C$ both −20%), the capacitive term $\Delta I/(8f_{sw}C)$ is **0.951** mV and the ESR term $\Delta I \cdot \text{ESR}$ is **0.804** mV. Their sum, **1.75** mV, is an upper bound, because the two are 90° apart. Against a 10 mV limit, ripple does not constrain the design.

**Resonance and ESR zero.** $f_0 = 1/(2\pi\sqrt{LC})$ = **24.0** kHz, and the ESR zero $1/(2\pi\,\text{ESR}\,C)$ is at **2.41** MHz, above the switching frequency. Below the ESR zero the plant falls at −40 dB/decade with −180° of phase. A Type II compensator cannot recover enough phase for that; a Type III, with two zeros, can.

## 3. Compensator

The Type III network around the error amplifier ([buck_avg.sub](buck_avg.sub) shows the topology) has an integrator, two zeros and two poles:

$$
G_c(s) = \frac{\omega_i}{s}\cdot\frac{(1 + s/\omega_{z1})(1 + s/\omega_{z2})}{(1 + s/\omega_{p1})(1 + s/\omega_{p2})},
\qquad
\omega_{z1} = \frac{1}{R_2C_1},\ \omega_{z2} = \frac{1}{(R_1 + R_3)C_3},\ \omega_{p1} = \frac{1}{R_3C_3},\ \omega_{p2} = \frac{C_1 + C_2}{R_2C_1C_2},
$$

with $\omega_i = 1/[R_1(C_1 + C_2)]$. The modulator gain is $V_{in}/V_{ramp}$, so the loop gain scales with the input voltage.

**Placement.** The two zeros go at 0.7 $f_0$ = **16.8** kHz, a little below the resonance, so that their phase lead is already working when the LC pair's −180° arrives. The two poles go at 1 MHz, half the switching frequency, to roll the gain off before the switching ripple reaches the modulator. The integrator gain is then set so that the loop crosses over at 85 kHz at 3.6 V and 0.1 A (§3.1 explains the choice). With $R_1$ = 10 kΩ (and a 10 kΩ bottom resistor for $V_{ref}$ = 0.6 V), the exact values are $R_2$ = **6291** Ω, $C_1$ = **1506** pF, $C_2$ = **25.7** pF, $R_3$ = **171** Ω and $C_3$ = **932** pF.

**Standard values.** The design rounds them to $R_2$ = 6.34 kΩ, $C_1$ = 1.5 nF, $C_2$ = 27 pF, $R_3$ = 169 Ω, $C_3$ = 910 pF. That moves the zeros to **16.74** and **17.20** kHz, the poles to **1.035** and **0.946** MHz, and the integrator to $f_i$ = **10.42** kHz. Every later number uses the rounded values.

### 3.1 Two iterations that failed, and why

The first design aimed at a 100 kHz crossover ($R_2$ = 7.68 kΩ, $C_1$ = 1.2 nF, $C_2$ = 22 pF). It met phase margin everywhere but not gain margin: the analytic model below gives a worst case of **8.4** dB, and the simulation agreed. An ideal error amplifier would have given **30.4** dB.

The cause is the error amplifier, not the power stage. A Type III network needs high-frequency gain $R_2(R_1 + R_3)/(R_1R_3)$, which is **38.1** (**31.6** dB) in the final design and more in the first one. The specified amplifier has 80 dB and 10 MHz of gain-bandwidth, so it has only about 20 dB of open-loop gain at 1 MHz. Near the phase-crossover frequency it cannot realize the network's transfer function, and its own pole adds lag exactly where the gain margin is measured.

Two other fixes were tried analytically and rejected:

- Lowering the poles to 500 kHz reduced the high-frequency gain but cost phase margin faster than it gained gain margin.
- Adding a third 22 µF capacitor made the margin *worse*: more capacitance means more compensator gain for the same crossover.

The second iteration lowered the target crossover to 80 kHz. That restored the gain margin, but the load step at 3.0 V with $L$ +20% and $C$ −20% then landed at the 36 mV limit in the switching model. The brief requires the step only with nominal parts, but a design with no margin at a plausible tolerance stack is fragile. The final 85 kHz target splits the difference: 1.6 dB of gain-margin margin and 2.0 mV of step margin at their worst corners (§5). **The lesson:** in voltage-mode control, the error amplifier's bandwidth is part of the plant, and the crossover is set by a tradeoff between two corners, not by one.

### 3.2 Predicted loop

An analytic model has the averaged plant (with DCR, switch resistance, ESR and load) and the rounded compensator around a single-pole error amplifier (80 dB, 1 kHz pole). It predicts the following over all 30 corners (three inputs, five $L$–$C$ combinations, light-and-cold and full-and-hot):

- crossover from **62.9** to **151.0** kHz;
- worst phase margin **61.6**°;
- worst gain margin **11.4** dB, against **31.9** dB with an ideal amplifier.

At the nominal point (3.6 V, 0.1 A) it predicts a crossover of **85.4** kHz, a phase margin of **65.2**° and a gain margin of **17.0** dB. Below crossover the loop phase never falls below **−125**°, so the loop is unconditionally stable in the small-signal sense.

## 4. Efficiency budget

At 3.6 V and 27 °C, with $D$ = 1/3 and $I_{rms}^2 = I^2 + \Delta I^2/12$:

| Loss | 0.1 A | 0.5 A | 1 A |
|---|---|---|---|
| Conduction: $(DR_{HS} + (1 - D)R_{LS} + \text{DCR})I_{rms}^2$ | **1.32** mW | **14.9** mW | **57.4** mW |
| Dead-time diodes: $V_Ft_{dead}f_{sw}(\lvert I_{pk}\rvert + \lvert I_{v}\rvert)$ | **5.60** mW | **14.0** mW | **28.0** mW |
| Gate drive and controller: $(Q_g \cdot 2f_{sw} + I_q)V_{in}$ | **32.4** mW | **32.4** mW | **32.4** mW |
| Efficiency | **75.3**% | **90.7**% | **91.1**% |

The switching model gives **75.5**%, **90.6**% and **91.0**% (§5). The fixed gate-drive and controller losses dominate at light load; a real design would add pulse skipping or discontinuous mode below about 0.2 A. The ideal switches have no voltage–current overlap loss, which the brief excludes. At 2 MHz a real converter would lose several more percent to it ([22-06](../../../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md)).

## 5. Simulated results against the specification

Full tables are in [results.md](results.md). The worst case of each requirement:

| Requirement | Worst case (where) | Limit | Margin |
|---|---|---|---|
| Output regulation | **1.1998** V (3.6 V, 0.1 A, switching) | 1.188 to 1.212 V | 11.8 mV |
| Crossover | **62.6** to **150** kHz | 50 to 200 kHz | 12.6 kHz at the low end |
| Phase margin | **61.0**° (3.0 V, $L$ +20%, 0.1 A) | ≥ 45° | 16.0° |
| Gain margin | **11.6** dB (4.2 V, $L$ and $C$ −20%, 0.1 A) | ≥ 10 dB | 1.6 dB |
| Load-step deviation, nominal parts | **30.4** mV (3.0 V, switching) | ≤ 36 mV | 5.6 mV |
| Load-step deviation, $L$ +20% and $C$ −20% (beyond the brief) | **34.0** mV (3.0 V, switching) | ≤ 36 mV | 2.0 mV |
| Recovery to within 1% | **21.8** µs (3.0 V, switching) | ≤ 30 µs | 8.2 µs |
| Ripple | **1.23** mV (4.2 V, 1 A, $L$ and $C$ −20%) | ≤ 10 mV | 8.8 mV |
| Efficiency, 0.5 A, 3.6 V | **90.6**% | ≥ 85% | 5.6 points |
| Peak inductor current | **1.28** A (4.2 V, 1 A, $L$ −20%) | ≤ 1.5 A | 0.22 A |

**Every requirement is met at every corner simulated**, including a load-step corner beyond the brief. The tightest margins are the load step at 3.0 V with high $L$ and low $C$, and the gain margin at low $L$ and low $C$. They are coupled: raising the crossover would help the first and hurt the second. That is the central tradeoff of this design, and the report would flag both to a reviewer as the specifications most at risk.

**Hand against simulation:**

| Quantity | Hand | Simulated |
|---|---|---|
| Crossover range | 62.9–151.0 kHz | 62.6–150 kHz |
| Worst phase margin | 61.6° | 61.0° |
| Worst gain margin | 11.4 dB | 11.6 dB |
| Peak inductor current | 1.27 A | 1.28 A |
| Ripple | ≤ 1.75 mV (bound) | 1.23 mV |
| Efficiency, 0.5 A | 90.7% | 90.6% |
| Load-step dip, 3.6 V | 21.3 mV (first-order) | 24.7 mV (averaged), 29.3 mV (switching) |

The loop and loss predictions are within about 1%. The load-step estimate is about 14% optimistic against the averaged model. The $\Delta I/(2\pi f_cC)$ rule assumes a single-pole closed loop, and the real loop's phase margin of about 65° gives a slower, partly underdamped recovery.

## 6. Two lessons from the simulations

**Dead time depends on the sign of the current.** At 0.1 A the ripple (0.4 A peak-to-peak) takes the inductor current negative at the valley. In the dead time before the high side turns on, the *high-side* body diode then conducts and lifts the switch node to $V_{in} + V_F$, instead of the low-side diode holding it at $-V_F$. A load step that lifts the valley above zero removes that boost, which acts as a sudden duty-cycle disturbance of about 2–3%.

The first averaged model, which always assumed the low-side diode, underestimated the switching model's dip by more than a third. Modeling the diode choice from the current at each edge (in [buck_avg.sub](buck_avg.sub)) closed most of the gap. The switching model is still about 19% larger at 3.6 V (29.3 against 24.7 mV), from the PWM's sampling delay and the switching ripple on the error-amplifier output.

**Start-up needs a soft-start.** Started from 0 V with a full reference, the error amplifier saturates, its integrator winds up, and the output overshoots to more than 2 V; the loop then falls into a large-signal limit cycle instead of settling. A 100 µs reference ramp (in [buck_sw.sub](buck_sw.sub)) prevents it. Production controllers add amplifier output clamps with anti-windup and cycle-by-cycle current limiting for the same reason.

## 7. Tradeoffs

| Knob | Improves | Costs |
|---|---|---|
| Higher crossover | Load-step deviation, recovery | Gain margin (limited by the error amplifier), noise sensitivity |
| More output capacitance | Load-step deviation (at fixed crossover) | Board area, cost; more compensator gain, so less margin |
| Larger inductor | Ripple, peak current | Slower current slew, lower $f_0$, size |
| Faster error amplifier | Gain margin, so a higher crossover | Controller current |
| Current-mode control | Removes the LC double pole from the loop; inherent current limit | Slope compensation, current sensing, subharmonic risk above $D$ = 0.5 |

**Not modeled:** switching (overlap) losses, the inductor's core loss and saturation curve, capacitor DC-bias derating beyond the −20% corner, layout parasitics, ESL, and the PWM's large-signal behavior beyond soft-start. A production design would also add current limiting and light-load pulse skipping.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| C1B.d30 | duty cycle, 3.0 V | 0.400 | — |
| C1B.d36 | duty cycle, 3.6 V | 0.333 | — |
| C1B.d42 | duty cycle, 4.2 V | 0.286 | — |
| C1B.lcalc | inductance for 40% ripple at 4.2 V | 1.07 | µH |
| C1B.di30 | ripple, 3.0 V | 0.360 | A |
| C1B.di36 | ripple, 3.6 V | 0.400 | A |
| C1B.di42 | ripple, 4.2 V | 0.429 | A |
| C1B.dilm | ripple, 4.2 V, L −20% | 0.536 | A |
| C1B.ival | valley current, 4.2 V, 1 A, L −20% | 0.732 | A |
| C1B.ipk | peak current, 4.2 V, 1 A, L −20% | 1.27 | A |
| C1B.cmin | capacitance for a 25 mV dip | 37.4 | µF |
| C1B.dev | estimated dip with 44 µF | 21.3 | mV |
| C1B.ripc | capacitive ripple term | 0.951 | mV |
| C1B.ripe | ESR ripple term | 0.804 | mV |
| C1B.ripb | ripple bound | 1.75 | mV |
| C1B.f0 | LC resonance | 24.0 | kHz |
| C1B.fesr | ESR zero | 2.41 | MHz |
| C1B.fz | zero placement | 16.8 | kHz |
| C1B.r2x | R2, exact | 6291 | Ω |
| C1B.c1x | C1, exact | 1506 | pF |
| C1B.c2x | C2, exact | 25.7 | pF |
| C1B.r3x | R3, exact | 171 | Ω |
| C1B.c3x | C3, exact | 932 | pF |
| C1B.fz1 | first zero, rounded parts | 16.74 | kHz |
| C1B.fz2 | second zero, rounded parts | 17.20 | kHz |
| C1B.fp1 | first pole, rounded parts | 1.035 | MHz |
| C1B.fp2 | second pole, rounded parts | 0.946 | MHz |
| C1B.fi | integrator frequency | 10.42 | kHz |
| C1B.gm1st | worst gain margin, first iteration | 8.4 | dB |
| C1B.gm1sti | the same with an ideal amplifier | 30.4 | dB |
| C1B.hfg | compensator high-frequency gain | 38.1 | — |
| C1B.hfgdb | compensator high-frequency gain | 31.6 | dB |
| C1B.ea1m | error-amplifier open-loop gain at 1 MHz | 20 | dB |
| C1B.fclo | predicted lowest crossover | 62.9 | kHz |
| C1B.fchi | predicted highest crossover | 151.0 | kHz |
| C1B.pmmin | predicted worst phase margin | 61.6 | ° |
| C1B.gmmin | predicted worst gain margin | 11.4 | dB |
| C1B.gmid | the same with an ideal amplifier | 31.9 | dB |
| C1B.fcn | predicted crossover, nominal | 85.4 | kHz |
| C1B.pmn | predicted phase margin, nominal | 65.2 | ° |
| C1B.gmn | predicted gain margin, nominal | 17.0 | dB |
| C1B.dip | lowest loop phase below crossover | -125 | ° |
| C1B.pc01 | conduction loss, 0.1 A | 1.32 | mW |
| C1B.pc05 | conduction loss, 0.5 A | 14.9 | mW |
| C1B.pc10 | conduction loss, 1 A | 57.4 | mW |
| C1B.pd01 | dead-time loss, 0.1 A | 5.60 | mW |
| C1B.pd05 | dead-time loss, 0.5 A | 14.0 | mW |
| C1B.pd10 | dead-time loss, 1 A | 28.0 | mW |
| C1B.pg | gate-drive and controller loss | 32.4 | mW |
| C1B.eta01 | efficiency, 0.1 A | 75.3 | % |
| C1B.eta05 | efficiency, 0.5 A | 90.7 | % |
| C1B.eta10 | efficiency, 1 A | 91.1 | % |
| SB.vomin | worst output voltage | 1.1998 | V |
| SB.vomar | margin to the 1% band | 11.8 | mV |
| SB.fclo | lowest simulated crossover | 62.6 | kHz |
| SB.fchi | highest simulated crossover | 150 | kHz |
| SB.fcmar | margin above 50 kHz | 12.6 | kHz |
| SB.pmmin | worst simulated phase margin | 61.0 | ° |
| SB.pmmar | phase-margin margin | 16.0 | ° |
| SB.gmmin | worst simulated gain margin | 11.6 | dB |
| SB.gmmar | gain-margin margin | 1.6 | dB |
| SB.devnom | worst load-step deviation, nominal parts | 30.4 | mV |
| SB.devx | load-step deviation, 3.0 V, L +20%, C −20% | 34.0 | mV |
| SB.devxmar | its margin | 2.0 | mV |
| SB.devmax | worst load-step deviation, all simulations | 34.0 | mV |
| SB.devmar | deviation margin, all simulations | 2.0 | mV |
| SB.recmax | worst recovery time | 21.8 | µs |
| SB.recmar | recovery margin | 8.2 | µs |
| SB.rip | ripple | 1.23 | mV |
| SB.ripmar | ripple margin | 8.8 | mV |
| SB.eta05 | efficiency, 0.5 A | 90.6 | % |
| SB.etamar | efficiency margin | 5.6 | points |
| SB.eta01 | efficiency, 0.1 A | 75.5 | % |
| SB.eta10 | efficiency, 1 A | 91.0 | % |
| SB.ipk | peak inductor current | 1.28 | A |
| SB.ipkmar | peak-current margin | 0.22 | A |
| SB.dev36a | load-step dip, 3.6 V, averaged | 24.7 | mV |
| SB.dev36s | load-step dip, 3.6 V, switching | 29.3 | mV |
| SB.devratio | switching over averaged dip, 3.6 V | 19 | % |
| SB.devhand | first-order estimate below the averaged dip | 14 | % |
