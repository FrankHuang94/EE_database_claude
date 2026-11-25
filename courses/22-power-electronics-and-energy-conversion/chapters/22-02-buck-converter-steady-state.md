<!-- status: reviewed -->
# 22-02 · Steady-State Analysis and the Buck Converter

| | |
|---|---|
| **Course** | [22 · Power Electronics and Energy Conversion](../README.md) |
| **University equivalent** | The steady-state analysis weeks of a senior power-electronics course: inductor volt-second balance, capacitor charge balance and the small-ripple approximation; the buck converter's ratio, ripples and RMS currents; conduction losses in the equivalent circuit; continuous and discontinuous conduction; and power-stage design (Erickson & Maksimović, *Fundamentals of Power Electronics*, ch. 2, 3 and 5; Mohan, Undeland & Robbins, the step-down converter chapter) |
| **Prerequisites** | [22-01](22-01-power-conversion-principles.md) (switching, averaging, losses), [07-01](../../07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) (inductor and capacitor laws), [03-03](../../03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) (mean and variance, used for RMS values) |
| **Estimated study hours** | 9 |
| **Last verified** | 2026-11-25 |

**Learning objectives.** After this chapter you can:

1. Apply inductor volt-second balance and capacitor charge balance, with the small-ripple approximation, to find a converter's conversion ratio and its average currents.
2. Derive a buck converter's inductor-current and output-voltage ripple (including the capacitor's ESR) and the RMS currents in its switches and capacitors.
3. Include conduction losses in the steady-state analysis, and show why synchronous rectification replaced the diode at low output voltages.
4. Find the boundary between continuous and discontinuous conduction, derive the buck's conversion ratio in discontinuous conduction, and explain pulse-frequency modulation as discontinuous operation.
5. Design a buck power stage: choose the switching frequency, inductor and capacitors, and check the minimum on-time, dropout, peak current and capacitor derating.

## 1. Big picture

Chapter 22-01 showed that a switch and an LC filter can step a voltage down without loss, and that the output is the switch node's average. This chapter turns that observation into an engineering method. Two balance principles, one for the inductor and one for the capacitor, give the DC operating point of any switching converter in a few lines. A small-ripple approximation then gives the ripples, and with them the sizes of the inductor and capacitors. The buck converter is the workhorse of electronics: it powers every processor core, memory rail and radio supply in a phone, every point-of-load rail on a server board, and the final stage of a GPU's power delivery. Doing its analysis properly, including what happens at light load when the inductor current runs dry, is the foundation for every topology in 22-03 and 22-04 and for the control design of 22-07.

- **Every SoC rail:** multi-phase bucks feed CPU, GPU and memory rails from a battery or a 5–12 V bus (22-08, 22-10).
- **Design numbers come from this chapter:** inductor value, capacitor count, switch current ratings and the light-load mode all follow from the formulas derived here.
- **Light load is a different regime:** below a critical current the converter enters discontinuous conduction, which is also how pulse-frequency modulation works.
- **Limits that decide architecture:** minimum on-time caps the step-down ratio at a given frequency, which is why 48 V to 1 V conversion needs more than a single buck (22-10).

## 2. Intuition first

**Two bookkeeping rules.** In steady state nothing in the converter drifts from one cycle to the next: the inductor current at the end of a period equals the one at the start, and so does the capacitor voltage. That alone fixes the DC operating point. An inductor's current changes at a rate $v_L/L$, so for its current to come back to where it started, the time-integral of its voltage over a period, the **volt-seconds**, must be zero. The inductor is pushed up during one part of the cycle and down during the other, by equal amounts. A capacitor's voltage changes at a rate $i_C/C$, so its net **charge** per period must be zero: whatever it absorbs in one part of the cycle it gives back in the other.

**An analogy, and its limits.** Think of the inductor as a flywheel and the two switch states as pushing and braking. If the flywheel's speed is the same at the start of every cycle, the push and the brake must be equal: push hard for a short time ($V_{in} - V$ for $DT_s$) and brake gently for a long time ($V$ for the rest), and the output voltage is whatever makes those two impulses equal. The analogy holds for the average behaviour. It breaks at light load, when the flywheel would have to spin backwards to keep the rule. A diode stops the current at zero instead, and the converter enters a third state, idle, which changes the arithmetic (§3.6).

![Buck converter waveforms in continuous conduction for Example 22-02.1: the inductor voltage is +10.8 V for 10 percent of the period and −1.2 V for the rest, so its two shaded areas are equal; the inductor current ramps between 8.5 and 11.5 A; and the capacitor current is the inductor current's triangle around zero, with the charge above zero equal to the charge below](../../../assets/figures/22-02/buck-ccm-waveforms.svg)

## 3. Theory

### 3.1 Volt-second balance, charge balance and the small-ripple approximation

**Volt-second balance.** For an inductor, $v_L = L\,di_L/dt$ (07-01). Integrate over one switching period $T_s$:

$$
i_L(T_s) - i_L(0) = \frac{1}{L}\int_0^{T_s} v_L(t)\,dt .
$$

In periodic steady state the left side is zero, so

$$
\langle v_L\rangle = \frac{1}{T_s}\int_0^{T_s} v_L\,dt = 0 .
$$

The average voltage across an inductor in steady state is zero: its positive and negative volt-seconds balance. This was stated in 07-01; here it becomes the main tool.

**Charge balance.** For a capacitor, $i_C = C\,dv_C/dt$. The same argument gives $\langle i_C\rangle = 0$: its net charge per period is zero.

**The small-ripple approximation.** In a well-designed converter the output voltage's ripple is a small fraction of its DC value (Example 22-01.4 had 3.6%; real designs target well under 1%). When writing the inductor's voltage in each subinterval, we may therefore replace the output voltage $v(t)$ by its DC value $V$. That makes every inductor voltage piecewise constant, every inductor current piecewise linear, and the algebra short. The approximation is applied to the quantity that is small (the output voltage's ripple), never to the inductor current, whose ripple is deliberately large (20–40% of its DC value is typical, §3.7). The exact solutions in 22-01's lab show how little it costs.

### 3.2 The buck converter in continuous conduction

Take the synchronous buck of 22-01: the high-side switch closes for $DT_s$, connecting the switch node to $V_{in}$; the low-side switch closes for $(1 - D)T_s = D'T_s$, connecting it to ground. As long as the inductor current stays positive throughout the cycle, the converter is in **continuous conduction mode (CCM)**.

- **Subinterval 1** ($0 < t < DT_s$): $v_L = V_{in} - V$, and the capacitor current is $i_C = i_L - V/R$.
- **Subinterval 2** ($DT_s < t < T_s$): $v_L = -V$, and again $i_C = i_L - V/R$.

Volt-second balance:

$$
(V_{in} - V)D + (-V)D' = 0 \quad\Longrightarrow\quad V = DV_{in}, \qquad M(D) = \frac{V}{V_{in}} = D .
$$

Charge balance: the capacitor current is $i_L - V/R$ in both subintervals, so $\langle i_C\rangle = I_L - V/R = 0$, giving $I_L = V/R = I$, the load current. The input current is $i_L$ during subinterval 1 and zero otherwise, so $I_{in} = DI_L$, and $V_{in}I_{in} = V_{in}DI = VI$: the lossless power balance of 22-01, recovered from the two rules.

### 3.3 Ripples

**Inductor current ripple.** During subinterval 1 the inductor current rises with slope $(V_{in} - V)/L$ for $DT_s$, so its peak-to-peak ripple is

$$
\Delta i_L = \frac{(V_{in} - V)DT_s}{L} = \frac{V(1 - D)}{f_sL} ,
$$

where the second form uses $V_{in} - V = V_{in}(1 - D)$ and $DV_{in} = V$. The second form is the one designers use, because $V$ is fixed and $V_{in}$ varies: the ripple is largest at the highest input voltage (smallest $D$). The current swings between $I \pm \Delta i_L/2$. Its peak, $I + \Delta i_L/2$, sets the switch and inductor current ratings.

**Output voltage ripple.** By charge balance, all of the inductor's ripple current flows into the capacitor; the load takes the DC part. This assumes the capacitor's impedance at $f_s$ is much smaller than the load resistance, which holds in any useful design. The capacitor current is therefore a triangle of peak-to-peak height $\Delta i_L$ centred on zero. The capacitor voltage rises while that current is positive, which is half the period, from the midpoint of subinterval 1 to the midpoint of subinterval 2. The charge delivered in that half-period is the area of a triangle of base $T_s/2$ and height $\Delta i_L/2$:

$$
\Delta Q = \frac12\cdot\frac{T_s}{2}\cdot\frac{\Delta i_L}{2} = \frac{\Delta i_L T_s}{8}, \qquad \Delta v_C = \frac{\Delta Q}{C} = \frac{\Delta i_L}{8f_sC} .
$$

Applied to Example 22-01.4 ($\Delta i_L$ = 0.4785 A, 1 µF, 500 kHz), this gives **119.6** mV (Txt a), against the exact 120.3 mV. The exact value is slightly larger because the true inductor ripple is 0.482 A: the 120 mV output ripple, 3.6% of $V$, enlarges the inductor's volt-seconds in both subintervals, which the small-ripple approximation ignores. The small share of ripple current that flows in the load pulls the other way, by less.

**ESR and ESL.** A real capacitor has an **equivalent series resistance** (ESR) and an **equivalent series inductance** (ESL) (07-01). The ripple current through the ESR adds a triangular voltage $\text{ESR}\cdot\Delta i_L$ peak to peak, in phase with the current, not with the charge. The capacitive and resistive parts peak at different times, so adding their peak-to-peak values is a slightly conservative estimate. The ESL turns each switching edge into a spike $L_{ESL}\,di/dt$. Ceramic capacitors have milliohm ESR, so their ripple is capacitive; electrolytic and polymer capacitors can be ESR-dominated, and then the capacitance hardly matters.

> **Math refresher — RMS of a waveform with ripple.** The RMS value is the square root of the mean square (06-01). If a waveform is its average $I$ plus a zero-mean part with its own RMS value $\sigma$, then $\langle (I + x)^2\rangle = I^2 + 2I\langle x\rangle + \langle x^2\rangle = I^2 + \sigma^2$, because the cross term averages to zero. This is the same identity as mean and variance in 03-03. A symmetric triangle of peak-to-peak height $\Delta$ has $\sigma = \Delta/(2\sqrt3)$: it is a linear ramp from $-\Delta/2$ to $+\Delta/2$, and the mean of $x^2$ for $x$ uniform on that interval is $\Delta^2/12$.

**RMS currents.** Write the ripple ratio $r = \Delta i_L/I$. The refresher gives the inductor's RMS current:

$$
I_{L,rms} = I\sqrt{1 + \frac{r^2}{12}} .
$$

With $r$ = 0.3 the ripple adds only **0.37** % to the RMS current (Txt b), so conduction losses barely depend on ripple. The high-side switch carries the inductor current for a fraction $D$ of the time, and the low-side switch for $D'$; each switch carries a sliced piece of the same triangle-on-a-pedestal. Each subinterval spans a full ramp of the triangle, from valley to peak or back, so the mean square of the inductor current over either subinterval equals its mean square over the whole period. A waveform that equals $i_L$ for a fraction $D$ of the time (and is zero otherwise) therefore has mean square $D\,I_{L,rms}^2$, exactly, for a triangular inductor current:

$$
I_{HS,rms} = \sqrt D\,I_{L,rms}, \qquad I_{LS,rms} = \sqrt{D'}\,I_{L,rms} .
$$

The **input capacitor** supplies the high-side switch's pulsed current while the source supplies its average, $DI$. The capacitor's current is therefore the switch current minus its mean, and by the refresher its mean square is the switch's mean square minus the square of its mean:

$$
I_{C_{in},rms}^2 = D\,I_{L,rms}^2 - (DI)^2 = I^2\left[D(1 - D) + \frac{Dr^2}{12}\right] \approx D(1 - D)\,I^2 .
$$

The first form is exact for a triangular inductor current; the ripple term is small, so $I_{C_{in},rms} \approx I\sqrt{D(1 - D)}$. This is largest at $D$ = 0.5, where it equals half the load current. The input capacitor, not the output one, usually carries the larger RMS current; it heats through its ESR and must be rated for it. The **output capacitor** carries only the inductor's ripple, $\Delta i_L/(2\sqrt3)$.

### 3.4 Conduction losses in the steady-state model

Add the main resistances: the high-side switch's on-resistance $R_{HS}$, the low-side switch's $R_{LS}$ and the inductor's winding resistance $R_L$ (its DCR). In subinterval 1 the inductor voltage is $V_{in} - I R_{HS} - IR_L - V$; in subinterval 2 it is $-IR_{LS} - IR_L - V$, using the small-ripple approximation on the current as well. Volt-second balance:

$$
D(V_{in} - IR_{HS}) - D'IR_{LS} - IR_L - V = 0 \quad\Longrightarrow\quad V = DV_{in} - I\,R_{eq}, \qquad R_{eq} = DR_{HS} + D'R_{LS} + R_L .
$$

This is the DC transformer of 22-01 followed by an equivalent series resistance $R_{eq}$: the duty-weighted average of the resistances the inductor current passes through. To first order the conduction loss is $I^2R_{eq}$, and the conduction-limited efficiency is

$$
\eta = \frac{VI}{VI + I^2R_{eq}} = \frac{1}{1 + R_{eq}/R} .
$$

The ripple raises the loss by the factor $1 + r^2/12$ (the RMS current by its square root). A regulated converter's control loop raises $D$ slightly above $V/V_{in}$ to make up the drop.

**Why synchronous rectification.** The original buck used a diode for the low-side path, which needs no control. A diode conducting the inductor current drops a roughly constant forward voltage $V_F$, and the same volt-second balance gives

$$
V = DV_{in} - D'V_F - I(DR_{HS} + R_L), \qquad P_{diode} \approx D'V_FI .
$$

The diode's loss is a fixed voltage times the current, which is large compared with a low output voltage. At 1.2 V out, a 0.5 V diode drop conducting for most of the period costs over a third of the output power in the diode alone (Example 22-02.4). A MOSFET in its place drops $IR_{LS}$, millivolts at amperes. That is why every low-voltage buck is **synchronous**. The price is a controller that must drive the second switch and must leave a short **dead time** between the two switches, so that they never conduct together and short the input.

### 3.5 RMS ratings and the heat they make

Each RMS current in §3.3 maps to a component's heat: $I_{HS,rms}^2R_{HS}$ and $I_{LS,rms}^2R_{LS}$ in the switches, $I_{L,rms}^2R_L$ in the winding, and $I_{C,rms}^2\,\text{ESR}$ in each capacitor. At a small duty cycle the high-side switch carries little RMS current but blocks the full input voltage and switches it (22-06). The low-side switch carries nearly all the current. Designers therefore choose a small, fast high-side device and a large, low-resistance low-side device: the duty cycle sets the split.

### 3.6 Discontinuous conduction

**The boundary.** The inductor current's minimum is $I - \Delta i_L/2$. As the load falls, $\Delta i_L$ stays the same (it depends only on voltages, frequency and $L$), so the minimum reaches zero at the **critical current**

$$
I_{crit} = \frac{\Delta i_L}{2} = \frac{V(1 - D)}{2f_sL} .
$$

Below it, a synchronous buck in forced PWM lets the current go negative, returning energy to the input each cycle, and stays in CCM with $M = D$. A diode, or a synchronous switch that is turned off when the current reaches zero, stops the current at zero instead. The cycle then has three subintervals:

- **$D_1T_s$:** the high-side switch is on and the current ramps up from zero.
- **$D_2T_s$:** the diode (or low-side switch) conducts while the current ramps down to zero.
- **$D_3T_s$:** both are off and the current stays at zero.

This is **discontinuous conduction mode (DCM)**.

**The conversion ratio in DCM.** Volt-second balance on the inductor, with $v_L = 0$ during $D_3$:

$$
(V_{in} - V)D_1 - VD_2 = 0 \quad\Longrightarrow\quad D_2 = D_1\frac{V_{in} - V}{V} .
$$

Charge balance now needs the inductor current's average, which is the area of its triangle divided by $T_s$. The peak current is $i_{pk} = (V_{in} - V)D_1T_s/L$, so

$$
\langle i_L\rangle = \frac12\,i_{pk}(D_1 + D_2) = \frac{V}{R} .
$$

Substitute $D_2$, use $D_1 + D_2 = D_1V_{in}/V$, and write $M = V/V_{in}$:

$$
\frac12\cdot\frac{V_{in}(1 - M)D_1T_s}{L}\cdot\frac{D_1}{M} = \frac{MV_{in}}{R} \quad\Longrightarrow\quad M^2 = \frac{D_1^2(1 - M)}{K}, \qquad K = \frac{2L}{RT_s} .
$$

The dimensionless $K$ compares the inductor's time constant with the switching period. Rearranging gives the quadratic $KM^2 + D_1^2M - D_1^2 = 0$, whose positive root is

$$
M = \frac{2}{1 + \sqrt{1 + 4K/D_1^2}} .
$$

In DCM the conversion ratio depends on the load through $K$: lighter load (larger $R$, smaller $K$) raises $M$ toward 1 at fixed $D_1$. A feedback loop hides this by shortening $D_1$, but the open-loop gain and dynamics change, which 22-07 handles. The CCM–DCM boundary is where $D_3 = 0$, that is $D_1 + D_2 = 1$ with $D_1 = D$. Substituting $M = D$ into the quadratic gives $K D^2 = D^2(1 - D)$, so

$$
K_{crit} = 1 - D ,
$$

and the converter is in DCM when $K < K_{crit}$. This is the same as $I < I_{crit}$, written in dimensionless form.

![The buck's conversion ratio against the load parameter K = 2L/(RT_s) for duty cycles 0.2, 0.5 and 0.8: each curve is flat at M = D for K above 1 − D (continuous conduction) and rises toward 1 as K falls below it (discontinuous conduction); a dashed line marks the boundary K = 1 − M](../../../assets/figures/22-02/conversion-ratio.svg)

**Pulse-frequency modulation is DCM.** A light-load mode such as the TPS62840's turns the high-side switch on for a fixed time, lets the current fall to zero and then sleeps until the output droops [3]. Each pulse is one DCM triangle, with peak $i_{pk} = (V_{in} - V)T_{on}/L$ and charge

$$
Q = \tfrac12 i_{pk}\left(T_{on} + T_{off}\right) = \tfrac12 i_{pk}T_{on}\frac{V_{in}}{V} ,
$$

since $T_{off} = T_{on}(V_{in} - V)/V$ by volt-second balance. Delivering the load current $I$ needs $f = I/Q$ pulses per second. The data sheet's PFM frequency formula is exactly this expression rearranged [3]. Its stated boundary between PFM and PWM, "when the inductor current becomes discontinuous" [3], is the critical current above.

### 3.7 Designing the power stage

A buck design proceeds from the specification ($V_{in}$ range, $V$, $I_{max}$, ripple and transient limits) in a fixed order.

1. **Switching frequency.** Higher $f_s$ shrinks $L$ and $C$ (22-01) but raises switching loss (22-06). It is also capped by the controller's **minimum on-time** $t_{on,min}$: the high-side switch cannot be on for less, so $D_{min}T_s \ge t_{on,min}$, giving $f_s \le D_{min}/t_{on,min}$ at the highest input voltage. One industrial buck specifies 68 ns, and when the limit is reached it "automatically reduces the switching frequency" (frequency foldback) [2].
2. **Inductor.** Choose the ripple ratio $r = \Delta i_L/I_{max}$. A widely used application note's rule is that "a good estimation for the inductor ripple current is 20% to 40% of the output current" [1]. Then $L = V(1 - D_{min})/(f_s r I_{max})$, evaluated at the highest input voltage. The inductor must not saturate at the peak current $I_{max}(1 + r/2)$, plus margin for transients and the current limit (22-05).
3. **Output capacitor.** From the ripple target, $C \ge \Delta i_L/(8f_s\Delta v_C)$ [1], plus an ESR budget $\text{ESR} \le \Delta v_{ESR}/\Delta i_L$. The load-step response usually needs more capacitance than ripple does (22-07). Ceramic capacitors lose capacitance under DC bias: the application note insists on "X5R or better" dielectric because otherwise "the capacitor loses much of its capacitance due to dc bias or temperature" [1]. One vendor-comparison article found 35–65% losses at rated voltage for the same 10 µF, 6.3 V, 0805 X7R rating [4]. Size from the derated value.
4. **Input capacitor.** Rate it for $I\sqrt{D(1 - D)}$ RMS, and place it as close to the switches as possible: it carries the pulsed current whose loop inductance causes switching spikes (22-06).
5. **Switches.** Use RMS currents for conduction loss, peak current for ratings, and the input voltage plus spike margin for the voltage rating.
6. **Dropout.** As $V_{in}$ falls toward $V$, $D$ approaches 1. A buck with a **100% duty-cycle mode** then holds the high-side switch on continuously, so the output follows the input through the switch and inductor resistances. One data sheet states $V_{IN,min} = V_{OUT} + I_{OUT}(R_{DS(on)max} + R_L)$ [3], which is the $D = 1$ case of §3.4.

> **Going deeper — the ripple ratio as an optimization.** Raising $r$ shrinks $L$ (and the inductor's stored energy, $\tfrac12LI_{pk}^2$, falls roughly as $1/r$ for small $r$) but raises the peak current, the output-capacitor ripple current and the core loss, which grows with flux swing. The 20–40% rule sits where the inductor's volume, still large at small $r$, and the capacitor and core losses, growing at large $r$, are both moderate. With modern multiphase converters, whose phases' ripples partly cancel at the output, designers push $r$ higher. Chapter 22-05 makes the inductor side quantitative.

## 4. Worked examples

### Example 22-02.1 · Sizing the inductor of a 12 V to 1.2 V converter (tier A)

**Setup.** A point-of-load buck converts 12 V to 1.2 V at 10 A, switching at 600 kHz, with a 30% ripple ratio. Find (a) the duty cycle, (b) the on-time, (c) the inductor ripple, (d) the inductance, and (e) the peak and (f) the valley inductor current.

**Solution.**

- (a) $D = 1.2/12$ = **0.100**; (b) $DT_s = 0.1/600\ \text{kHz}$ = **166.7** ns.
- (c) $\Delta i_L = 0.3 \times 10$ = **3.0** A.
- (d) $L = V(1 - D)/(f_s\Delta i_L) = 1.2 \times 0.9/(600\ \text{kHz} \times 3)$ = **0.600** µH.
- (e) $10 + 1.5$ = **11.5** A; (f) $10 - 1.5$ = **8.5** A.

**Units check.** V·s/A = H: $1.08\ \text{V}/(6 \times 10^5\ \text{s}^{-1} \times 3\ \text{A}) = 6 \times 10^{-7}$ H.

**Sanity check.** A sub-microhenry inductor carrying 10 A is typical of a server point-of-load stage. The on-time of 167 ns is comfortably above the tens of nanoseconds that controllers need (Example 22-02.7). The lab's ngspice model confirms the 3.0 A ripple.

### Example 22-02.2 · Choosing the output capacitor (tier A)

**Setup.** For Example 22-02.1's converter, the ripple budget is 10 mV peak to peak from capacitance, plus at most 5 mV from ESR. Find (a) the minimum effective capacitance and (b) the largest allowable ESR. (c) If the ceramic capacitors lose 50% of their capacitance at the 1.2 V bias, what nominal capacitance is needed, and (d) how many 22 µF parts is that? (e) With exactly the effective 62.5 µF (and no ESR), what is the exact ripple?

**Solution.**

- (a) $C = \Delta i_L/(8f_s\Delta v) = 3/(8 \times 600\ \text{kHz} \times 0.01)$ = **62.5** µF.
- (b) $\text{ESR} \le 5\ \text{mV}/3\ \text{A}$ = **1.67** mΩ, for the whole bank.
- (c) $62.5/0.5$ = **125** µF nominal; (d) $\lceil 125/22\rceil$ = **6** parts.
- (e) The periodic steady-state solution, the same matrix-exponential method used in 22-01, gives **10.01** mV, confirming the formula.

**Units check.** A/(s⁻¹·V) = A·s/V = F.

**Sanity check.** Six ceramic capacitors in parallel also divide the ESR by six, so 1.67 mΩ for the bank allows 10 mΩ per part, easily met by ceramics. In practice the load-step requirement (22-07), not the ripple, usually sets the count.

### Example 22-02.3 · RMS currents (tier B)

**Setup.** For Example 22-02.1's converter, find the RMS currents in (a) the inductor, (b) the high-side switch, (c) the low-side switch, (d) the input capacitor and (e) the output capacitor.

**Solution.**

- (a) $10\sqrt{1 + 0.09/12}$ = **10.04** A.
- (b) $\sqrt{0.1} \times 10.04$ = **3.17** A; (c) $\sqrt{0.9} \times 10.04$ = **9.52** A.
- (d) $10\sqrt{0.1 \times 0.9 + 0.1 \times 0.09/12}$ = **3.01** A (3.00 A without the ripple term).
- (e) $3/(2\sqrt3)$ = **0.87** A.

**Units check.** All in amperes RMS; (b)² + (c)² = (a)², as it must, since the two switches share the inductor's current in time. The output-capacitor value is quoted to two figures because a little of the ripple current flows in the load.

**Sanity check.** The low-side switch carries three times the high-side switch's RMS current, so it should have about a ninth of the resistance for equal heat. The input capacitor carries **3.5** times the output capacitor's RMS current (f): it is the one that runs hot. The lab's ngspice model confirms (a) and (b) to within 0.2%.

### Example 22-02.4 · Conduction losses and the case for synchronous rectification (tier B)

**Setup.** The converter of Example 22-02.1 has $R_{HS}$ = 8 mΩ, $R_{LS}$ = 3 mΩ and $R_L$ = 1 mΩ. Find (a) the duty cycle that gives 1.2 V at 10 A, (b) $R_{eq}$, (c) the conduction loss and (d) the conduction-limited efficiency. Now replace the low-side switch with a diode of 0.5 V forward drop. Find (e) the new duty cycle, (f) the diode's loss and (g) the efficiency.

**Solution.**

- (a) $V = DV_{in} - I(DR_{HS} + D'R_{LS} + R_L)$, which is linear in $D$: $1.2 = 12D - 10(0.008D + 0.003(1 - D) + 0.001)$, so $D(12 - 0.05) = 1.24$ and $D$ = **0.1038**.
- (b) $R_{eq} = 0.1038 \times 8 + 0.8962 \times 3 + 1$ = **4.52** mΩ; (c) $10^2 \times 4.52\ \text{mΩ}$ = **0.452** W.
- (d) $12/(12 + 0.452)$ = **96.37** %.
- (e) $1.2 = 12D - (1 - D)0.5 - 10(0.008D + 0.001)$, so $D(12 + 0.5 - 0.08) = 1.71$ and $D$ = **0.1377**.
- (f) $0.8623 \times 0.5 \times 10$ = **4.31** W.
- (g) Adding the switch and winding loss $10^2(0.1377 \times 0.008 + 0.001)$ = 0.21 W, the efficiency is $12/(12 + 4.31 + 0.21)$ = **72.6** %.

**Units check.** A² × Ω = W; V × A = W.

**Sanity check.** The diode's loss is **36** % of the 12 W output (h), almost ten times the synchronous converter's total conduction loss. At 12 V out from a 48 V bus ($D'$ = 0.75) the same diode would cost $0.5 \times 0.75/12$ = **3.1** % of the output (i), which is why diode bucks survive only at higher output voltages or very low cost. The exact steady state of the synchronous version gives **96.34** % including the ripple's RMS effect (Lab 22-02.a), and the lab's ngspice model agrees.

### Example 22-02.5 · Light load: the critical current and discontinuous conduction (tier B)

**Setup.** The converter of Example 22-02.1 uses a diode-emulating low-side switch. Find (a) the critical load current. At 0.3 A (a 4 Ω load), find (b) $K$, (c) $K_{crit}$ and so the mode, (d) the on-time fraction $D_1$ that still gives 1.2 V, (e) the on-time, (f) $D_2$, (g) the idle fraction $D_3$ and (h) the peak inductor current.

**Solution.**

- (a) $I_{crit} = \Delta i_L/2$ = **1.5** A: below 1.5 A, the current would go negative in CCM.
- (b) $K = 2L/(RT_s) = 2 \times 0.6\ \mu\text{H}/(4 \times 1.667\ \mu\text{s})$ = **0.180**.
- (c) $K_{crit} = 1 - D$ = **0.9** > 0.18: discontinuous.
- (d) From $M = 2/(1 + \sqrt{1 + 4K/D_1^2})$ with $M$ = 0.1: $\sqrt{1 + 4K/D_1^2} = 2/M - 1 = 19$, so $4K/D_1^2 = 360$ and $D_1 = \sqrt{0.72/360}$ = **0.0447**.
- (e) $0.0447 \times 1.667\ \mu\text{s}$ = **74.5** ns.
- (f) $D_2 = D_1(V_{in} - V)/V = 0.0447 \times 9$ = **0.402**; (g) $D_3 = 1 - 0.0447 - 0.402$ = **0.553**.
- (h) $i_{pk} = (12 - 1.2)(74.5\ \text{ns})/0.6\ \mu\text{H}$ = **1.34** A.

**Units check.** $K$ is H/(Ω·s) = (V·s/A)/(V/A·s), dimensionless.

**Sanity check.** Check charge balance directly: $\tfrac12 \times 1.34 \times (0.0447 + 0.402)$ = 0.300 A, the load current. In CCM the duty cycle would have been 0.1; in DCM the controller needs less than half that on-time. The lab's diode-buck netlist, with exactly this on-time, settles within 1% of 1.2 V (the diode's small forward drop accounts for the difference) with the predicted peak current.

### Example 22-02.6 · Pulse-frequency mode in a wearable buck (tier C)

**Setup.** The TPS62840 sets its PFM on-time to $T_{on} = (V_{OUT}/V_{IN}) \times 556$ ns [3]. It converts 3.6 V to 1.8 V with a 2.2 µH inductor and a 10 µF output capacitor (both assumed for this example). Find (a) the on-time, (b) the peak current per pulse, (c) the charge per pulse, and the pulse rate at (d) 1 mA and (e) 1 µA. (f) At what load does the pulse rate reach the PWM frequency, $1/556\ \text{ns}$? (g) Estimate the output ripple per pulse at light load.

**Solution.**

- (a) $0.5 \times 556$ = **278** ns.
- (b) $i_{pk} = (3.6 - 1.8)(278\ \text{ns})/2.2\ \mu\text{H}$ = **0.227** A.
- (c) $T_{off} = T_{on}(V_{in} - V)/V$ = 278 ns, so $Q = \tfrac12 \times 0.227 \times 556\ \text{ns}$ = **63.2** nC.
- (d) $f = I/Q = 1\ \text{mA}/63.2\ \text{nC}$ = **15.8** kHz; (e) at 1 µA, **15.8** Hz.
- (f) $1.799\ \text{MHz} \times 63.2\ \text{nC}$ = **0.114** A, which equals $i_{pk}/2$, the critical current with $\Delta i_L = i_{pk}$.
- (g) At light load nearly all of each pulse's charge lands on the capacitor before the load can take it: $\Delta v \approx Q/C = 63.2\ \text{nC}/10\ \mu\text{F}$ = **6.3** mV.

**Units check.** A·s = C for the charge, and a current divided by a charge per pulse, A/C, is pulses per second.

**Sanity check.** At 1 µA the converter switches 16 times a second. The fixed loss per pulse (gate drive, controller wake-up) is paid only 16 times a second, which is how the data sheet reaches 80% efficiency at 1 µA (22-01). The cost is a 6 mV sawtooth at an audio-band, load-dependent frequency, which is why the part offers a forced-PWM pin for noise-sensitive moments [3].

### Example 22-02.7 · Minimum on-time and dropout (tier C)

**Setup.** (a) A controller's minimum on-time is 68 ns [2]. What is the highest switching frequency at which it can convert 48 V to 1.0 V, and (b) 12 V to 1.0 V? (c) A wearable buck in 100% mode has $R_{DS(on)max} + R_L$ = 0.5 Ω (assumed). What is the lowest battery voltage at which it holds 1.8 V at 0.5 A?

**Solution.**

- (a) $f_s \le D/t_{on,min} = (1/48)/68\ \text{ns}$ = **306** kHz.
- (b) $(1/12)/68\ \text{ns}$ = **1.23** MHz.
- (c) $V_{IN,min} = 1.8 + 0.5 \times 0.5$ = **2.05** V.

**Units check.** A duty cycle over a time is a frequency; volts plus amperes times ohms is volts.

**Sanity check.** Converting 48 V straight to 1 V forces the switching frequency down by a factor of four compared with a 12 V input, and with it the passives up by four. That, together with the 48 V switches' larger switching losses, is why datacenter boards convert 48 V to an intermediate bus first, or use special topologies (22-10). In (c) the regulator is no longer regulating: below 2.05 V the output follows the battery down.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 22-02.1a | duty cycle | 0.100 | |
| Ex 22-02.1b | on-time | 166.7 | ns |
| Ex 22-02.1c | inductor ripple | 3.0 | A |
| Ex 22-02.1d | inductance | 0.600 | µH |
| Ex 22-02.1e | peak inductor current | 11.5 | A |
| Ex 22-02.1f | valley inductor current | 8.5 | A |
| Ex 22-02.2a | minimum effective capacitance | 62.5 | µF |
| Ex 22-02.2b | maximum bank ESR | 1.67 | mΩ |
| Ex 22-02.2c | nominal capacitance after 50 % derating | 125 | µF |
| Ex 22-02.2d | number of 22 µF parts | 6 | |
| Ex 22-02.2e | exact ripple with 62.5 µF | 10.01 | mV |
| Ex 22-02.3a | inductor RMS current | 10.04 | A |
| Ex 22-02.3b | high-side RMS current | 3.17 | A |
| Ex 22-02.3c | low-side RMS current | 9.52 | A |
| Ex 22-02.3d | input-capacitor RMS current | 3.01 | A |
| Ex 22-02.3e | output-capacitor RMS current | 0.87 | A |
| Ex 22-02.3f | input over output capacitor RMS current | 3.5 | |
| Ex 22-02.4a | duty cycle with resistances | 0.1038 | |
| Ex 22-02.4b | equivalent resistance | 4.52 | mΩ |
| Ex 22-02.4c | conduction loss | 0.452 | W |
| Ex 22-02.4d | conduction-limited efficiency | 96.37 | % |
| Ex 22-02.4e | duty cycle with a diode | 0.1377 | |
| Ex 22-02.4f | diode loss | 4.31 | W |
| Ex 22-02.4g | efficiency with a diode | 72.6 | % |
| Ex 22-02.4h | diode loss as a share of the output | 36 | % |
| Ex 22-02.4i | diode loss share at 12 V out from 48 V | 3.1 | % |
| Ex 22-02.5a | critical current | 1.5 | A |
| Ex 22-02.5b | K at 0.3 A | 0.180 | |
| Ex 22-02.5c | critical K | 0.9 | |
| Ex 22-02.5d | DCM duty D1 | 0.0447 | |
| Ex 22-02.5e | DCM on-time | 74.5 | ns |
| Ex 22-02.5f | D2 | 0.402 | |
| Ex 22-02.5g | idle fraction D3 | 0.553 | |
| Ex 22-02.5h | DCM peak current | 1.34 | A |
| Ex 22-02.6a | PFM on-time | 278 | ns |
| Ex 22-02.6b | PFM peak current | 0.227 | A |
| Ex 22-02.6c | charge per pulse | 63.2 | nC |
| Ex 22-02.6d | pulse rate at 1 mA | 15.8 | kHz |
| Ex 22-02.6e | pulse rate at 1 µA | 15.8 | Hz |
| Ex 22-02.6f | load at the PWM frequency | 0.114 | A |
| Ex 22-02.6g | PFM ripple per pulse | 6.3 | mV |
| Ex 22-02.7a | maximum frequency, 48 V to 1 V | 306 | kHz |
| Ex 22-02.7b | maximum frequency, 12 V to 1 V | 1.23 | MHz |
| Ex 22-02.7c | 100 %-mode minimum input | 2.05 | V |
| Txt 22-02.a | formula ripple for Example 22-01.4 | 119.6 | mV |
| Txt 22-02.b | RMS increase from a 30 % ripple | 0.37 | % |

## 5. Simulate it

The lab ([labs/22-02-lab](../labs/22-02-lab/README.md)) collects the formulas in `buck.py`. It solves the exact periodic steady state of a buck with resistances, by matrix exponentials, and solves the DCM equations. Two ngspice netlists go with it:

- `buck_ccm.cir`: Examples 22-02.1 to 22-02.4, with near-ideal and with lossy switches;
- `buck_dcm.cir`: Example 22-02.5's diode buck at light load.

**Predict, then run.**

1. *Predict* the inductor ripple, output ripple and the switches' RMS currents of the 12 V to 1.2 V converter, then run `buck_ccm.cir` (Part 1).
2. *Predict* the conduction-limited efficiency with the stated resistances, and how much the ripple lowers it. Compare with ngspice (Part 2).
3. *Predict* the on-time that gives 1.2 V at 0.3 A in DCM, then run `buck_dcm.cir`. Sweep the load in the notebook to watch $M$ leave $D$ below the critical current (Part 3).
4. *Predict* the PFM pulse rate of Example 22-02.6 at 1 mA and 1 µA, then plot it against load (Part 4).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Larger ripple ratio $r$ (smaller L) | Inductor size, transient slew | Peak current, capacitor ripple current, core loss, earlier DCM | Power-stage designer |
| More output capacitance | Ripple, load-step droop | Area, cost, DC-bias derating to manage | Board power designer |
| Synchronous low-side switch | Efficiency at low output voltage | Driver, dead-time control, cost | Power IC architect |
| Forced PWM at light load | Fixed-frequency, predictable ripple; no audio-band noise | Light-load efficiency (fixed loss every cycle) | System / RF integration |
| PFM / DCM at light load | Light-load efficiency | Variable-frequency ripple, load-dependent gain (22-07) | PMIC architect |
| Higher switching frequency | Smaller L and C | Switching loss; minimum on-time limits the step-down ratio | Power IC architect |
| Larger low-side device | Conduction loss at small D | Gate charge, area, cost | Power-stage designer |

## 7. Numbers to know

| Quantity | Typical value | Source |
|---|---|---|
| Inductor ripple design rule | 20–40% of the output current | [1] |
| Output capacitance for a ripple target | $\Delta i_L/(8f_s\Delta v)$ | §3.3, [1] |
| Ceramic capacitor loss at rated DC voltage | 35–65% (10 µF, 6.3 V, X7R, 0805, three vendors) | [4] (2019) |
| Input capacitor RMS current | about $I\sqrt{D(1 - D)}$, at most about $I/2$ | §3.3 |
| Industrial buck minimum on-time | 68 ns | [2] |
| Wearable buck PFM on-time and PWM frequency | $(V_{OUT}/V_{IN}) \times 556$ ns; about 1.8 MHz | [3] |
| Wearable buck PFM pulse rate at 1 µA (3.6 V to 1.8 V, 2.2 µH) | about 16 Hz | Example 22-02.6 |
| Diode drop against synchronous switch at 1.2 V, 10 A | 4.3 W against 0.45 W total conduction loss | Example 22-02.4 |

## 8. Common mistakes

- **Applying the small-ripple approximation to the inductor current.** Its ripple is deliberately large; the approximation applies to the output voltage.
- **Sizing the inductor at nominal input.** Ripple is largest at the highest input voltage (smallest $D$); use $V_{in,max}$.
- **Sizing capacitors from their nominal value.** Ceramics lose a large fraction under DC bias; use the derated value at the operating voltage.
- **Forgetting the input capacitor's RMS current.** It is often larger than the output capacitor's and sets its rating and heat.
- **Using $M = D$ at light load with a diode or PFM.** Below the critical current the ratio depends on the load.
- **Ignoring the minimum on-time.** A large step-down ratio at high frequency asks for on-times the controller cannot produce.
- **Adding resistances without weighting by duty.** The equivalent series resistance is $DR_{HS} + D'R_{LS} + R_L$, not their sum.

## 9. Practitioner lens

**State of the art (as of Nov 2026).**

- **Design rules from vendors [Established].** TI's buck power-stage application note, revised in 2026, still gives the classic sequence used in §3.7 [1]:
  - inductor ripple of "20% to 40% of the output current";
  - $C_{OUT(min)} = \Delta I_L/(8f_S\Delta V_{OUT})$, plus an ESR term $\text{ESR} \times \Delta I_L$;
  - ceramic dielectrics of "X5R or better".
- **Ceramic derating is part-specific [Industry estimate].** A trade-press analysis found 35–65% capacitance loss at rated voltage among three vendors' parts with the same 10 µF, 6.3 V, 0805 X7R rating, and argued that data sheets should guarantee a worst-case loss [4]. Designers read each part's DC-bias curve.
- **Light-load modes [Established as data-sheet behaviour].**
  - A wearable buck runs a fixed-on-time PFM that "generates a single switching pulse to ramp up the inductor current … followed by a sleep period". It switches to PWM at the CCM boundary, and offers forced PWM for when "interference with RF and noise-sensitive circuits" matters, at the cost of light-load efficiency [3].
  - An application-processor PMIC with six bucks selects PFM or PWM automatically "over a wide load range" [5].
- **Minimum on-time sets frequency** [Established as data-sheet values]. An industrial 36 V buck specifies a 68 ns minimum on-time and folds its 2.1 MHz frequency back when it is reached [2]. This is the same arithmetic as Example 22-02.7.

**Commercial relevance.** The buck power stage is a commodity at the component level and a differentiator at the system level:

- **What makes a stage better:** the same topology, analysed here, separates a PMIC that holds 90% efficiency over five decades of load from one that does not. The difference lies in its light-load modes, its switch sizing for the duty cycle and its minimum on-time.
- **The questions that separate competitors:** for a corporate-development review of a power-IC company, the ones in this chapter. Can the part convert this ratio at this frequency? What does it do below the critical current? How much capacitance does its stability require at derated value?

**Marketing vs Reality.**

- **"Uses only 2 × 22 µF of output capacitance."** At what bias? A 50% DC-bias loss halves it; ask for the derated value and the load step it was tested with.
- **"Up to 2 MHz switching."** At which input-to-output ratio? With a 68 ns minimum on-time, a 12 V to 1 V conversion folds back below 1.23 MHz.
- **"90% efficiency."** At which load and mode? PFM and forced PWM give different curves, and a part in forced PWM for RF quietness forfeits its light-load numbers.
- **"Low output ripple."** Measured in PWM at full load, or in PFM at light load, where it is a load-dependent sawtooth of millivolts?

**Questions for engineering leaders.**

1. **"What is your ripple ratio, and why?"** *Strong:* a number with the trade against peak current, core loss and transient response, and how multiphase ripple cancellation changed it. *Evasive:* "We follow the reference design."
2. **"What happens below the critical current?"** *Strong:* the mode transition (PFM, diode emulation or forced PWM), the frequency range it produces, and how the control loop is compensated across the change. *Evasive:* "It just gets more efficient."
3. **"What effective capacitance does the loop assume?"** *Strong:* derated capacitance at the operating bias and temperature, with the ESR range and the resulting phase margin. *Evasive:* nominal values only.
4. **"Where is your minimum on-time, and what happens at the highest input voltage?"** *Strong:* the on-time, the foldback behaviour and the ripple and EMI consequences. *Evasive:* "The part supports the full input range."
5. **"How is your input capacitor sized?"** *Strong:* RMS current at the worst-case duty cycle, ESR heating and the hot-loop layout. *Evasive:* "Per the data sheet minimum."

## 10. Concept check

**Q1.** Why must the average voltage across an inductor be zero in steady state, and what does that give you?

<details><summary>Answer</summary>

Because $\int v_L\,dt = L\,\Delta i_L$ and the current returns to its starting value each period. Equating the positive and negative volt-seconds gives the conversion ratio directly: for the buck, $(V_{in} - V)D = VD'$, so $V = DV_{in}$.

</details>

**Q2.** To which quantity is the small-ripple approximation applied, and why not to the inductor current?

<details><summary>Answer</summary>

To the output (capacitor) voltage, whose ripple is a small fraction of its DC value by design. The inductor current's ripple is deliberately 20–40% of its DC value, so treating it as constant would lose the very ripple we need to size parts, although it is a fair approximation for conduction losses.

</details>

**Q3.** Why does all of the inductor's ripple current go into the output capacitor and not the load?

<details><summary>Answer</summary>

Because at the switching frequency the capacitor's impedance is far below the load resistance, so it takes the AC part, while charge balance makes the load take the DC part. If that were not true, the ripple would be large and the design poor.

</details>

**Q4.** Which carries more RMS current at $D$ = 0.1, the high-side or the low-side switch, and what does that imply for device sizing?

<details><summary>Answer</summary>

The low-side switch, by a factor of $\sqrt{0.9/0.1}$ = 3. It should have the lower on-resistance (a larger device), while the high-side switch, which carries less current but switches the full input voltage, can be smaller and faster.

</details>

**Q5.** A buck with a diode enters discontinuous conduction at light load. What happens to its conversion ratio at a fixed duty cycle?

<details><summary>Answer</summary>

It rises above $D$ toward 1 as the load gets lighter, $M = 2/(1 + \sqrt{1 + 4K/D^2})$ with $K = 2L/(RT_s)$, because the idle interval removes the low-side volt-seconds that held the output down. The feedback loop compensates by shortening the on-time.

</details>

**Q6.** Why is pulse-frequency modulation efficient at light load, and what does it cost?

<details><summary>Answer</summary>

Each pulse delivers a fixed charge, so the pulse rate, and with it the fixed switching and wake-up losses, falls in proportion to the load. The cost is a load-dependent ripple frequency, which can land in audio or RF bands, and a larger ripple per pulse than in PWM.

</details>

**Q7.** Why does a 48 V to 1 V conversion struggle at high switching frequency?

<details><summary>Answer</summary>

The duty cycle is about 2%, so the on-time is 2% of the period. With a minimum on-time of tens of nanoseconds, the period must be several microseconds: a few hundred kilohertz at most, and correspondingly large passives.

</details>

Now work the [problem set](../problems/22-02-problems.md).

## 11. Key terms

[Volt-second balance](../../../reference/glossary.md#volt-second-balance) · [Charge balance](../../../reference/glossary.md#charge-balance) · [Small-ripple approximation](../../../reference/glossary.md#small-ripple-approximation) · [Continuous conduction mode (CCM)](../../../reference/glossary.md#continuous-conduction-mode-ccm) · [Discontinuous conduction mode (DCM)](../../../reference/glossary.md#discontinuous-conduction-mode-dcm) · [Critical current](../../../reference/glossary.md#critical-current) · [Ripple ratio](../../../reference/glossary.md#ripple-ratio) · [Equivalent series resistance (ESR)](../../../reference/glossary.md#equivalent-series-resistance-esr) · [Synchronous rectification](../../../reference/glossary.md#synchronous-rectification) · [Dead time](../../../reference/glossary.md#dead-time) · [Minimum on-time](../../../reference/glossary.md#minimum-on-time) · [Dropout mode (100% duty cycle)](../../../reference/glossary.md#dropout-mode-100-duty-cycle) · [Forced PWM](../../../reference/glossary.md#forced-pwm) · [DC-bias derating](../../../reference/glossary.md#dc-bias-derating)

## 12. Connections

- **Previous:** [22-01](22-01-power-conversion-principles.md) showed why switching is lossless and introduced the buck's averaging; [07-01](../../07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md) gave the element laws and stated volt-second balance.
- **Next:** [22-03](22-03-boost-buck-boost-topologies.md) applies the same two balances to the boost, buck-boost, Ćuk and SEPIC converters.
- **Used later:**
  - [22-04](22-04-isolated-converters.md) (transformers add a turns ratio to the same analysis);
  - [22-05](22-05-magnetics-design.md) (the inductor's peak current and ripple set its core and winding);
  - [22-06](22-06-converter-losses-and-wide-bandgap.md) (switching losses and the devices behind $R_{HS}$ and $R_{LS}$);
  - [22-07](22-07-converter-dynamics-and-control.md) (averaged models built from the same subinterval equations, and DCM's different dynamics);
  - [22-08](22-08-pmics.md) (PFM and forced PWM in PMICs);
  - [22-10](22-10-datacenter-power-delivery.md) (multiphase VRMs and the 48 V problem).

## 13. Further study

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 2 (volt-second and charge balance, the small-ripple approximation), ch. 3 (equivalent circuits with losses) and ch. 5 (the discontinuous conduction mode).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the step-down converter, including the CCM–DCM boundary.
- University of Colorado Boulder, *Converter Circuits* and *Introduction to Power Electronics* (Coursera, R. W. Erickson): the steady-state and DCM modules.

## 14. Sources

1. B. Hauke, *Basic Calculation of a Buck Converter's Power Stage*, Texas Instruments application note SLVA477C (Dec 2011, revised Sep 2026) [R-424].
2. Texas Instruments, *LMR33630* data sheet, SNVSAN3F (Aug 2017, revised Nov 2020): minimum on-time and frequency foldback [R-424].
3. Texas Instruments, *TPS62840* data sheet, SLVSEC6D: PFM on-time, PFM frequency, forced PWM and 100% mode [R-424].
4. "High CV MLCC DC BIAS Capacitance Loss Explained," EEPower, 31 Jul 2019 [R-424].
5. Renesas (Dialog), DA9063 product page: six buck converters with automatic PFM/PWM selection [R-424].
