<!-- status: verified -->
# 22-03 · Boost, Buck-Boost and Other Topologies

| | |
|---|---|
| **Course** | [22 · Power Electronics and Energy Conversion](../README.md) |
| **University equivalent** | The non-isolated topology weeks of a senior power-electronics course: the boost and inverting buck-boost converters, the Ćuk and SEPIC capacitor-coupled converters, conversion ratios by volt-second and charge balance, ripples and switch stresses, the effect of inductor resistance on gain and efficiency, discontinuous conduction in the boost, and topology selection (Erickson & Maksimović, *Fundamentals of Power Electronics*, ch. 2, 3, 5 and 6) |
| **Prerequisites** | [22-02](22-02-buck-converter-steady-state.md) (volt-second and charge balance, small ripple, DCM), [22-01](22-01-power-conversion-principles.md) (efficiency and loss) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Derive the conversion ratios of the boost, inverting buck-boost, Ćuk and SEPIC converters from volt-second and charge balance.
2. Find their inductor currents, ripples, output-capacitor demands and switch voltage and current stresses.
3. Add inductor and switch resistance to the boost, derive its efficiency and maximum gain, and explain why high step-up ratios are inefficient.
4. Find the boost's CCM–DCM boundary and its conversion ratio in discontinuous conduction.
5. Choose a topology for a given input range, output voltage and polarity, using switch stress, ripple and the right-half-plane-zero preview as criteria.

## 1. Big picture

A buck can only step down. Many products need more: a single alkaline or Li-ion cell must make 5 V for USB or an LED string; a lithium battery that swings from 4.2 to 3.0 V must hold a 3.3 V rail through the whole discharge; a car's 9–16 V bus must make a steady 12 V; a power-factor corrector must turn rectified mains into a 400 V bus. The same three parts (a switch, a diode or second switch, an inductor) rearranged give the **boost**, which steps up, and the **buck-boost**, which does both at the price of inverting. Capacitor-coupled variants (Ćuk, SEPIC) fix the polarity or smooth the currents. Every one of them yields to the two balances of 22-02, so this chapter is mostly an exercise in applying a method you already have. It also shows where the topologies differ in what matters commercially: how hard they stress their switches and capacitors, how efficient they can be at high ratios, and how hard they are to control.

- **Battery and supercapacitor products:** boost converters run displays, LEDs and USB ports from cells below the load voltage.
- **Phones and wearables:** four-switch buck-boost converters hold a 3.3 V rail across a Li-ion discharge that crosses it.
- **Power supplies:** the power-factor-correction stage at the front of almost every supply above about 75 W is a boost (22-01, 22-10).
- **Automotive:** SEPIC and buck-boost converters ride through cold-crank dips and load-dump surges.
- **Control:** boost-derived converters have a right-half-plane zero that limits how fast their loops can be (22-07).

## 2. Intuition first

**The boost as a pump.** Connect an inductor from the input to ground through a switch, and its current rises: energy flows from the input into the inductor's magnetic field. Open the switch, and the inductor's current cannot stop (22-01's Rule 2). It forces the switch node up until a diode conducts into the output capacitor, which must therefore sit above the input. The inductor is charged from the input for a fraction $D$ of the time and discharged into the output for the rest. Volt-second balance says the small push ($V_{in}$ for $DT_s$) must equal the pull ($V - V_{in}$ for $D'T_s$), so the output must exceed the input by a factor $1/D'$.

**The buck-boost as a store-and-release.** Put the inductor between the switch node and ground instead, and it charges from the input during the on-time and then dumps its energy into an output connected the other way round, with no direct path from input to output. Because all the energy passes through the inductor's field, any output magnitude is possible, but the output is negative, and every component sees the sum of input and output voltages.

**An analogy and its limits.** A boost is like a hydraulic ram: a flow of water is stopped abruptly, and the pressure spike lifts some of it higher than the source. The analogy captures why interrupting a current raises a voltage. It misses that the boost does this smoothly and losslessly every cycle through a diode into a capacitor, with no hammer blow, and that the "height" is set by duty cycle, not by how fast the flow stops.

![Three non-isolated converters drawn with the same parts: a boost with the inductor in series with the input, the switch to ground and the diode to the output; an inverting buck-boost with the switch from the input, the inductor to ground and the diode reversed to a negative output; and a SEPIC with an input inductor, a series coupling capacitor, a second inductor to ground and a diode to a positive output](../../../assets/figures/22-03/topologies.svg)

## 3. Theory

### 3.1 The boost converter

The inductor $L$ runs from $V_{in}$ to the switch node. A switch (low side) connects the switch node to ground for $DT_s$, and a diode (or high-side synchronous switch) connects it to the output for $D'T_s$. The output capacitor $C$ and the load $R$ sit across the output $V$.

- **Subinterval 1** ($DT_s$): $v_L = V_{in}$, and the capacitor alone supplies the load, $i_C = -V/R$.
- **Subinterval 2** ($D'T_s$): $v_L = V_{in} - V$, and $i_C = i_L - V/R$.

Volt-second balance:

$$
V_{in}D + (V_{in} - V)D' = 0 \quad\Longrightarrow\quad V = \frac{V_{in}}{D'}, \qquad M(D) = \frac{1}{1 - D} .
$$

Charge balance:

$$
-\frac{V}{R}D + \left(I_L - \frac{V}{R}\right)D' = 0 \quad\Longrightarrow\quad I_L = \frac{V}{D'R} = \frac{I}{D'} .
$$

The inductor current is the input current, $I_{in} = I_L$, so $V_{in}I_{in} = (VD')(I/D') = VI$: the lossless balance again. The inductor carries more current than the load, by $1/D'$, which already hints at higher conduction loss for high ratios.

**Ripples.** During subinterval 1 the inductor current rises at $V_{in}/L$, so

$$
\Delta i_L = \frac{V_{in}DT_s}{L} .
$$

The output capacitor is the boost's weak point. During the whole on-time it supplies the full load current, losing charge $IDT_s$, and it is recharged during the off-time by pulses of inductor current. Its peak-to-peak ripple is therefore

$$
\Delta v = \frac{IDT_s}{C} = \frac{ID}{f_sC} ,
$$

which is linear in $T_s$, not quadratic as for the buck, because the output current is pulsed rather than smoothed by the inductor. The capacitor's RMS current follows the same way as the buck's input capacitor. It carries $I_L - I$ for $D'$ of the time and $-I$ for $D$, which gives $I\sqrt{D/D'}$ for small ripple. In the boost, the *output* capacitor is the hot one.

**Stresses.** The switch and diode each block the full output voltage $V$ and carry the inductor's peak current $I/D' + \Delta i_L/2$.

**The right-half-plane zero (preview).** Suppose the controller wants more output and raises $D$. For the next few cycles, the diode conducts for less time, so less current reaches the output and the output first *drops*. Only as the inductor current builds up does the output rise. A system that initially moves the wrong way has a zero in the right half of the s-plane. For the boost it sits at $\omega_z = D'^2R/L$, which 22-07 derives from the averaged model, and it limits the control bandwidth to a fraction of that frequency. The buck has no such zero, because its output current comes from the inductor all the time.

### 3.2 The boost with resistance: efficiency and maximum gain

Add the inductor's winding resistance $R_L$ (keep the switches ideal for the moment). Volt-second balance becomes

$$
D(V_{in} - I_LR_L) + D'(V_{in} - I_LR_L - V) = 0 \quad\Longrightarrow\quad V_{in} - I_LR_L = D'V .
$$

Charge balance is unchanged, $I_L = V/(D'R)$. Substituting,

$$
\frac{V}{V_{in}} = \frac{1}{D'}\cdot\frac{1}{1 + \dfrac{R_L}{D'^2R}}, \qquad \eta = \frac{VI}{V_{in}I_L} = \frac{D'V}{V_{in}} = \frac{1}{1 + \dfrac{R_L}{D'^2R}} .
$$

The winding resistance appears to the load as $R_L/D'^2$, because the inductor carries $1/D'$ times the load current and the conversion ratio reflects its drop by another $1/D'$. At high duty cycle, $D'^2$ becomes tiny and the resistance's effect explodes.

**The gain has a maximum.** $M(D') = 1/(D' + R_L/(D'R))$ has its denominator minimized, by the refresher in 22-01 ($a/x + bx$), at

$$
D'^* = \sqrt{\frac{R_L}{R}}, \qquad M_{max} = \frac{1}{2}\sqrt{\frac{R}{R_L}} ,
$$

where the efficiency has fallen to exactly 50%. Beyond that duty cycle, asking for more output gives *less*, and a controller that keeps pushing $D$ up latches into a low-output, high-current state. Practical boosts therefore stay at ratios of a few. For larger step-ups, designers use transformers (22-04), cascades or tapped inductors.

**With switch resistances.** If the low-side switch has $R_{LS}$ and the high-side switch (synchronous rectifier) has $R_{HS}$, the same algebra gives $V_{in} - I_L(R_L + DR_{LS} + D'R_{HS}) = D'V$. The duty-weighted resistance takes the place of $R_L$ (Example 22-03.2).

### 3.3 The inverting buck-boost

The switch connects the input to the inductor's top for $DT_s$; the inductor's bottom is grounded. During $D'T_s$ a diode connects the inductor's top to an output whose capacitor and load are referred to ground but whose voltage $V$ is negative.

- **Subinterval 1:** $v_L = V_{in}$, $i_C = -V/R$ (the capacitor supplies the load).
- **Subinterval 2:** $v_L = V$ (negative), and the inductor current flows into the output.

Volt-second balance: $V_{in}D + VD' = 0$, so

$$
V = -\frac{D}{D'}V_{in}, \qquad M(D) = -\frac{D}{1 - D} .
$$

The magnitude is below 1 for $D < 0.5$ and above 1 for $D > 0.5$. Charge balance gives $\lvert I_L\rvert = \lvert I\rvert/D'$, as for the boost. Every switching element blocks $V_{in} + \lvert V\rvert$, because during the on-time the diode sees the input on one side and the negative output on the other. The input current is pulsed (like a buck) and so is the output current (like a boost), so both capacitors work hard. The buck-boost pays for its flexibility with the highest stresses of the three (Example 22-03.6).

**The four-switch buck-boost.** Phones avoid the inversion with a non-inverting variant: a buck half bridge on the input and a boost half bridge on the output, sharing one inductor. It runs as a buck when $V_{in} > V$, as a boost when $V_{in} < V$, and in a mixed mode in between. A commercial part "automatically operates in boost, buck, or in a novel 4-cycle buck-boost mode when the input voltage is approximately equal to the output voltage" [1]. In each pure mode it has only that mode's stresses.

### 3.4 Capacitor-coupled converters: Ćuk and SEPIC

Both use two inductors and a coupling capacitor $C_1$ that carries energy from input to output.

**SEPIC** (single-ended primary-inductance converter). The input inductor $L_1$ feeds a low-side switch, as in a boost. The coupling capacitor $C_1$ connects the switch node to a second inductor $L_2$ to ground, and a diode from that node feeds a positive output. In steady state, volt-second balance on $L_2$ (whose average voltage is zero) and the DC path through $L_1$ and $L_2$ fix the coupling capacitor's average voltage at $V_{C1} = V_{in}$.

During the on-time the switch node is at ground, so $L_1$ sees $V_{in}$, and $L_2$ sees $-V_{C1} = -V_{in}$ through the closed switch and $C_1$. During the off-time the diode conducts and holds $L_2$'s top at the output, so $L_2$ sees $+V$. The switch node then sits at $V + V_{C1}$, so $L_1$ sees $V_{in} - V_{C1} - V = -V$. Volt-second balance on $L_1$ (or, equally, on $L_2$: $-V_{in}D + VD' = 0$):

$$
V_{in}D - VD' = 0 \quad\Longrightarrow\quad V = \frac{D}{D'}V_{in} .
$$

This is the same magnitude as the buck-boost, but non-inverting, with a continuous input current through $L_1$ and a DC-blocking capacitor that isolates input from output if the switch fails. The switch and diode see $V_{in} + V$. SEPICs are common in automotive supplies whose input range straddles the output.

**Ćuk.** The mirror image, with the coupling capacitor in the switch path and $L_2$ in series with the output. It gives $V = -DV_{in}/D'$ with *both* input and output currents continuous (inductor-smoothed), at the price of inverting.

### 3.5 The boost in discontinuous conduction

With a diode, the boost enters DCM when its inductor current reaches zero during the off-time. Define $K = 2L/(RT_s)$ as in 22-02. The three subintervals:

- **$D_1 = D$:** the switch is on and the current rises to $i_{pk} = V_{in}DT_s/L$.
- **$D_2$:** the diode conducts and the current falls to zero, with $v_L = V_{in} - V$.
- **$D_3$:** idle.

Volt-second balance: $V_{in}D + (V_{in} - V)D_2 = 0$, so $D_2 = V_{in}D/(V - V_{in})$. Charge balance: the diode delivers the triangle's falling part only, so

$$
\frac12 i_{pk}D_2 = \frac{V}{R} .
$$

Substituting $i_{pk}$ and $D_2$, and writing $M = V/V_{in}$:

$$
\frac{V_{in}DT_s}{2L}\cdot\frac{D}{M - 1} = \frac{MV_{in}}{R} \quad\Longrightarrow\quad M(M - 1) = \frac{D^2}{K} .
$$

The positive root is

$$
M = \frac{1 + \sqrt{1 + 4D^2/K}}{2} .
$$

The boundary is where $D_2 = D'$. Substituting $M = 1/D'$ into $M(M - 1) = D^2/K$ gives $(1/D')(D/D') = D^2/K$, so

$$
K_{crit} = DD'^2 .
$$

The boundary curve peaks at $D = 1/3$, where $K_{crit} = 4/27$: a boost with $K$ above 4/27 stays in CCM at every duty cycle. As in the buck, the DCM ratio rises at light load for a fixed $D$, and the controller must shorten $D$ to hold the output.

### 3.6 Choosing a topology

A useful single number for comparing topologies is the **switch stress**: the peak voltage across the active (controlled) switch times the peak current through it, divided by the output power. With several switches, the stresses add. A switch whose voltage and current ratings must both be large costs area or money in proportion to their product. For ideal converters at the same output power and $D$ = 0.5:

- the **buck** needs $V_{in}$ and $I$: stress $V_{in}I/(VI) = 1/D$;
- the **boost** needs $V$ and $I/D'$: stress $1/D'$;
- the **buck-boost** needs $V_{in} + \lvert V\rvert$ and $I/D'$: stress $(V_{in} + \lvert V\rvert)/(\lvert V\rvert D')$, which is twice the others at $D$ = 0.5 (Example 22-03.6).

The selection rules that follow:

1. **If the input is always above the output, use a buck;** if always below, a boost. Each is the least-stressed option for its job.
2. **If the input range straddles the output,** use a four-switch buck-boost (low voltage, integrated) or a SEPIC (automotive, discrete), or a buck followed by a boost when efficiency matters less than simplicity.
3. **For large ratios (above about 4–5),** avoid single-stage boosts and buck-boosts. Their efficiency falls with $D'^2$ (§3.2), and their extreme duty cycles meet minimum on- or off-time limits (22-02). Use a transformer (22-04) or two stages.
4. **For negative rails,** use an inverting buck-boost or a Ćuk, or a charge pump at low current.
5. **For fast load steps,** remember that the boost-derived converters (boost, buck-boost, SEPIC, Ćuk) carry a right-half-plane zero, so their loops are slower than a buck's (22-07).

## 4. Worked examples

### Example 22-03.1 · A single-cell boost to 5 V (tier A)

**Setup.** A synchronous boost converts 3.6 V to 5.0 V at 1.5 A, switching at 1 MHz with a 1 µH inductor and 22 µF of effective output capacitance (assumed values). Find (a) the duty cycle, (b) the inductor current, (c) its ripple, its (d) peak and (e) valley values, (f) the output ripple and (g) the output capacitor's RMS current. (h) Where does the right-half-plane zero sit?

**Solution.**

- (a) $D = 1 - 3.6/5$ = **0.28**.
- (b) $I_L = 1.5/0.72$ = **2.083** A.
- (c) $\Delta i_L = 3.6 \times 0.28 \times 1\ \mu\text{s}/1\ \mu\text{H}$ = **1.008** A.
- (d) $2.083 + 0.504$ = **2.587** A; (e) $2.083 - 0.504$ = **1.579** A.
- (f) $\Delta v = 1.5 \times 0.28/(1\ \text{MHz} \times 22\ \mu\text{F})$ = **19.1** mV.
- (g) $1.5\sqrt{0.28/0.72}$ = **0.935** A.
- (h) $\omega_z = D'^2R/L = 0.5184 \times 3.333\ \Omega/1\ \mu\text{H}$, so $f_z = \omega_z/2\pi$ = **275** kHz.

**Units check.** Ω/H = 1/s; A·s/F = V.

**Sanity check.** The output ripple is much larger than a buck of similar size would give, because the capacitor alone carries the load for 28% of each period. The valley current of 1.58 A sits comfortably below the 3.7 A valley current limit of a commercial 0.5 V-input boost designed for this job [2]. A loop bandwidth of a fifth of the RHP-zero frequency, about **55** kHz (i), is a common design choice (22-07).

### Example 22-03.2 · Conduction losses in the boost (tier B)

**Setup.** The boost of Example 22-03.1 has a 47 mΩ low-side switch and a 68 mΩ high-side switch, as in a commercial part [2], and a 30 mΩ inductor (assumed). Find (a) the duty cycle that holds 5.0 V at 1.5 A, (b) the inductor current, (c) the conduction loss and (d) the conduction-limited efficiency.

**Solution.**

- (a) Solve the small-ripple model $V_{in} - (I/D')(R_L + DR_{LS} + D'R_{HS}) = D'V$ numerically: $D$ = **0.3203**.
- (b) $I_L = 1.5/0.6797$ = **2.207** A.
- (c) $P_{in} - P_{out} = 3.6 \times 2.207 - 7.5$ = **0.445** W.
- (d) $\eta = D'V/V_{in}$ = **94.40** %.

**Units check.** $D'V/V_{in}$ is a ratio of volts.

**Sanity check.** The duty cycle rose from 0.28 to 0.32 to make up the resistive drops. The exact steady state, which includes the 1 A ripple's RMS effect on the conduction loss, gives **94.28** % (e). The data sheet's 94% at this operating point [2] is close to either estimate, which suggests that conduction dominates its losses here, provided the assumed 30 mΩ inductor is representative.

### Example 22-03.3 · The boost's gain limit (tier B)

**Setup.** A boost has a 0.1 Ω winding resistance and a 25 Ω load (switches ideal). Find (a) the duty cycle of maximum gain, (b) the maximum gain and (c) the efficiency there. Find the gain and efficiency at (d, e) $D$ = 0.8 and (f, g) $D$ = 0.9.

**Solution.**

- (a) $D' = \sqrt{0.1/25}$ = 0.0632, so $D$ = **0.937**.
- (b) $M_{max} = \tfrac12\sqrt{250}$ = **7.91**.
- (c) **50.0** %.
- (d) At $D'$ = 0.2: $M = 5/(1 + 0.1/(0.04 \times 25))$ = **4.55**; (e) η = **90.9** %.
- (f) At $D'$ = 0.1: $M = 10/(1 + 0.1/0.25)$ = **7.14**; (g) η = **71.4** %.

**Units check.** $R_L/(D'^2R)$ is a ratio of ohms.

**Sanity check.** The ideal gain at $D$ = 0.9 would be 10; the winding resistance, reflected as $R_L/D'^2$ = 10 Ω against a 25 Ω load, costs 29% of the power. Going from 4.5× to 7× more than triples the loss fraction. This is why 12 V to 48 V boosts are built from two stages or with coupled inductors.

### Example 22-03.4 · Negative and straddling rails (tier B)

**Setup.** (a) An inverting buck-boost makes −5 V from 12 V. Find its duty cycle, (b) the switch voltage and (c) the average inductor current at 1 A. (d, e) A SEPIC makes 12 V from an automotive bus of 9–16 V. Find its duty cycle at each extreme, and (f, g) the switch voltage at each.

**Solution.**

- (a) $D/D' = 5/12$, so $D = 5/17$ = **0.294**.
- (b) $12 + 5$ = **17** V.
- (c) $1/D' = 1/0.706$ = **1.42** A.
- (d) $D = 12/(12 + 9)$ = **0.571** at 9 V; (e) $12/28$ = **0.429** at 16 V.
- (f) $9 + 12$ = **21** V; (g) $16 + 12$ = **28** V.

**Units check.** Ratios of volts give duty cycles.

**Sanity check.** The SEPIC's duty cycle passes through 0.5 when the input equals the output (12 V), where a buck would need 100% and a boost 0%. A single fixed topology covers the whole range without changing mode. The price is a switch rated for 28 V plus margin to make 12 V.

### Example 22-03.5 · The boost at light load (tier B)

**Setup.** The boost of Example 22-03.1 has a diode-emulating rectifier and a 50 mA load (100 Ω at 5 V). Find (a) $K$, (b) $K_{crit}$ at $D$ = 0.28 and so the mode, (c) the open-loop output if $D$ stays at 0.28, and (d) the duty cycle that restores 5 V.

**Solution.**

- (a) $K = 2 \times 1\ \mu\text{H} \times 1\ \text{MHz}/100$ = **0.020**.
- (b) $K_{crit} = 0.28 \times 0.72^2$ = **0.1452** > 0.02: DCM.
- (c) $M = (1 + \sqrt{1 + 4 \times 0.0784/0.02})/2$ = 2.542, so $V$ = **9.15** V.
- (d) With $M$ = 5/3.6 = 1.389: $4D^2/K = (2M - 1)^2 - 1$ = 2.160, so $D = \sqrt{2.160 \times 0.02/4}$ = **0.104**.

**Units check.** $K$ is dimensionless (H·Hz/Ω).

**Sanity check.** Open loop, the output would nearly double at light load; the controller must cut the on-time by almost two-thirds. Commercial parts instead enter a pulse-skipping power-save mode at light load [2], the same idea as 22-02's PFM.

### Example 22-03.6 · Switch stress by topology (tier C)

**Setup.** Compare the active switch's stress, $V_{pk}I_{pk}/P_{out}$ with small ripple, for 12 W at 12 V output and $D$ = 0.5 in (a) a buck from 24 V, (b) a boost from 6 V and (c) an inverting buck-boost from 12 V (to −12 V).

**Solution.**

- (a) Buck: the switch blocks 24 V and carries the 1 A load current: $24 \times 1/12$ = **2**.
- (b) Boost: the switch blocks 12 V and carries $I/D'$ = 2 A: $12 \times 2/12$ = **2**.
- (c) Buck-boost: the switch blocks $12 + 12$ = 24 V and carries 2 A: $24 \times 2/12$ = **4**.

**Units check.** V·A/W is dimensionless.

**Sanity check.** The buck-boost's switch handles twice the volt-amperes for the same power, because all the energy is stored in the inductor and released in a separate interval. That is the price of its flexibility, and why converters that straddle use four switches that each run as a buck or a boost.

### Example 22-03.7 · The boost at the heart of power-factor correction (tier C)

**Setup.** A totem-pole PFC stage makes a 400 V bus from 230–277 V AC [3]. Treat it as a boost from the rectified line. Find the duty cycle at the peak of (a) a 230 V and (b) a 277 V line. (c) What does the duty cycle approach near the line's zero crossings?

**Solution.**

- (a) Peak $230\sqrt2$ = 325.3 V, so $D = 1 - 325.3/400$ = **0.187**.
- (b) Peak $277\sqrt2$ = 391.7 V, so $D$ = **0.021**.
- (c) As the instantaneous line voltage approaches zero, $D = 1 - v_{in}/400$ approaches **1**.

**Units check.** Ratios of volts.

**Sanity check.** At the 277 V line peak the boost barely boosts: a 400 V bus is the lowest round number above the highest line peak. The duty cycle sweeps from near 1 to near 0 twice every line cycle, so the PFC controller is in constant motion, and near the zero crossings the boost's large ratio and its right-half-plane zero matter most.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 22-03.1a | duty cycle | 0.28 | |
| Ex 22-03.1b | inductor current | 2.083 | A |
| Ex 22-03.1c | inductor ripple | 1.008 | A |
| Ex 22-03.1d | peak current | 2.587 | A |
| Ex 22-03.1e | valley current | 1.579 | A |
| Ex 22-03.1f | output ripple | 19.1 | mV |
| Ex 22-03.1g | output-capacitor RMS current | 0.935 | A |
| Ex 22-03.1h | RHP-zero frequency | 275 | kHz |
| Ex 22-03.1i | a fifth of the RHP-zero frequency | 55 | kHz |
| Ex 22-03.2a | duty cycle with resistances | 0.3203 | |
| Ex 22-03.2b | inductor current | 2.207 | A |
| Ex 22-03.2c | conduction loss | 0.445 | W |
| Ex 22-03.2d | conduction-limited efficiency | 94.40 | % |
| Ex 22-03.2e | exact efficiency including ripple | 94.28 | % |
| Ex 22-03.3a | duty cycle of maximum gain | 0.937 | |
| Ex 22-03.3b | maximum gain | 7.91 | |
| Ex 22-03.3c | efficiency at maximum gain | 50.0 | % |
| Ex 22-03.3d | gain at D = 0.8 | 4.55 | |
| Ex 22-03.3e | efficiency at D = 0.8 | 90.9 | % |
| Ex 22-03.3f | gain at D = 0.9 | 7.14 | |
| Ex 22-03.3g | efficiency at D = 0.9 | 71.4 | % |
| Ex 22-03.4a | buck-boost duty cycle | 0.294 | |
| Ex 22-03.4b | buck-boost switch voltage | 17 | V |
| Ex 22-03.4c | buck-boost inductor current | 1.42 | A |
| Ex 22-03.4d | SEPIC duty at 9 V | 0.571 | |
| Ex 22-03.4e | SEPIC duty at 16 V | 0.429 | |
| Ex 22-03.4f | SEPIC switch voltage at 9 V | 21 | V |
| Ex 22-03.4g | SEPIC switch voltage at 16 V | 28 | V |
| Ex 22-03.5a | K at 50 mA | 0.020 | |
| Ex 22-03.5b | critical K at D = 0.28 | 0.1452 | |
| Ex 22-03.5c | open-loop DCM output | 9.15 | V |
| Ex 22-03.5d | duty for 5 V in DCM | 0.104 | |
| Ex 22-03.6a | buck switch stress | 2 | |
| Ex 22-03.6b | boost switch stress | 2 | |
| Ex 22-03.6c | buck-boost switch stress | 4 | |
| Ex 22-03.7a | PFC duty at the 230 V peak | 0.187 | |
| Ex 22-03.7b | PFC duty at the 277 V peak | 0.021 | |
| Ex 22-03.7c | PFC duty near a zero crossing | 1 | |

## 5. Simulate it

The lab ([labs/22-03-lab](../labs/22-03-lab/README.md)) collects the formulas in `topologies.py` and runs two ngspice netlists:

- `boost.cir`: Example 22-03.1's boost, plus a normalized boost with winding resistance at two duty cycles;
- `sepic.cir`: a SEPIC.

**Predict, then run.**

1. *Predict* the boost's output, inductor ripple and output ripple, then run `boost.cir` (Part 1).
2. *Predict* the gain of a boost with $R_L/R$ = 0.004 at $D$ = 0.8 and 0.9, and where its gain peaks. Compare with ngspice and sweep $D$ in the notebook (Part 2).
3. *Predict* the SEPIC's output and the average voltage on its coupling capacitor, then run `sepic.cir` (Part 3).
4. *Predict* the boost's DCM output at light load for a fixed duty cycle, and plot the CCM–DCM boundary $K_{crit} = DD'^2$ (Part 4).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Boost instead of buck-boost (input always below output) | Half the switch stress, one less inverted rail | Cannot step down; no short-circuit protection through the diode path | Power architect |
| Four-switch buck-boost | Covers a straddling range with buck or boost stresses | Four switches, complex mode transitions, cost | PMIC architect |
| SEPIC | Non-inverting, continuous input current, DC isolation of output | Two inductors (or a coupled pair), coupling-capacitor ripple current | Automotive power designer |
| Higher boost ratio in one stage | Fewer parts | Efficiency falls with $D'^2$; extreme duty cycle; RHP zero slows the loop | Power architect |
| Larger output capacitor (boost) | Ripple, which is linear in $T_s$ and the load current | Area, cost, RMS rating | Board designer |
| Synchronous rectifier in a boost | Efficiency at low output voltage | Reverse current at light load unless controlled; no output disconnect without extra switch | Power IC designer |

## 7. Numbers to know

| Quantity | Typical value | Source |
|---|---|---|
| Conversion ratios (CCM) | buck $D$; boost $1/D'$; buck-boost and Ćuk $-D/D'$; SEPIC $D/D'$ | §3 |
| Boost maximum gain with winding resistance | $\tfrac12\sqrt{R/R_L}$, at 50% efficiency | §3.2 |
| Boost CCM–DCM boundary | $K_{crit} = DD'^2$, at most 4/27 at $D$ = 1/3 | §3.5 |
| Single-cell boost (commercial) | 0.5–5.5 V in, 94% at 3.6 V to 5 V, 1.5 A; 47/68 mΩ switches; 1 MHz | [2] |
| Low-voltage four-switch buck-boost | 1.3–5.5 V in, 1.8–5.2 V out, 2 A at 3.3 V; 0.47 µH; 11 µA quiescent | [1] |
| PFC boost output bus | 400 V, above the highest line peak (391.7 V at 277 V AC) | [3], Example 22-03.7 |

## 8. Common mistakes

- **Using the buck's output-ripple formula for a boost.** The boost's output current is pulsed; its ripple is $ID/(f_sC)$, linear in $T_s$.
- **Rating a buck-boost's switch for the input voltage.** It blocks $V_{in} + \lvert V\rvert$.
- **Expecting a boost to reach any gain by raising D.** Winding resistance caps the gain at $\tfrac12\sqrt{R/R_L}$, where efficiency is already 50%.
- **Forgetting that the boost inductor carries $I/D'$.** At high ratios it carries several times the load current, which sets the inductor's size and loss.
- **Ignoring the RHP zero.** A boost loop designed like a buck loop will be unstable or slow at high duty cycle.
- **Assuming a boost disconnects its load when switched off.** The inductor and diode (or body diode) leave a path from input to output; commercial parts add "true disconnection" circuitry when that matters [2].

## 9. Practitioner lens

**State of the art (as of Nov 2026).**

- **Integrated low-voltage boosts [Established as data-sheet values].** A current single-cell boost accepts "0.5 V to 5.5 V" with a "3.7-A valley switching current limit". It reaches "94% Efficiency at VIN = 3.6 V, VOUT = 5 V and IOUT = 1.5 A" at 1 MHz, offers "Pass-through mode when VIN > VOUT" and "True disconnection between input and output during shutdown", and enters a power-save mode at light load [2]. The pass-through mode is the boost's answer to an input above its output: it simply stops switching and leaves the high-side switch on.
- **Four-switch buck-boost for batteries [Established as data-sheet values].** A 2 A part covers "1.3 V to 5.5 V" input and "1.8 V to 5.2 V" output. It moves between buck, boost and "4-cycle buck-boost" modes "at defined thresholds" to avoid toggling, with a "0.47-µH inductor" and an "11-µA operating quiescent current" [1].
- **PFC boosts [Industry estimate].** The front end of a high-efficiency server supply is a boost from the rectified line to a 400 V bus. GaN totem-pole designs reach 99–99.2% peak efficiency at 230–277 V AC [3] (22-01).

**Commercial relevance.** For a corporate-development view:

- **Most of the low-voltage boost and buck-boost market is PMIC content:** wearables, IoT nodes and phones need rails that cross the battery voltage.
- **Differentiation is in the detail:** mode transitions (how smoothly a buck-boost moves through the straddle region), light-load modes, and the RHP zero's effect on transient response.
- **At high power, the boost is the PFC stage:** its efficiency and density, set by the switch technology (22-06), lead every server-supply announcement.

**Marketing vs Reality.**

- **"Wide input range, 0.5 V to 5.5 V."** True, but the switching frequency and the current limit may change across the range (one part halves its frequency below 1 V [2]). Check performance at the input you will actually see.
- **"Seamless buck-boost transition."** Ask for output ripple and efficiency across the region where input equals output, where mode logic decides behaviour.
- **"Up to 10× step-up."** Possible on paper; check efficiency at that ratio. The boost's $D'^2$ penalty (§3.2) is hard to escape without a transformer or coupled inductors.

**Questions for engineering leaders.**

1. **"What is your efficiency at the highest step-up ratio you specify?"** *Strong:* a curve against ratio, with the inductor's resistance and the switch's off-time limit named as the constraints. *Evasive:* "Peak efficiency is 95%."
2. **"How does your buck-boost behave when input equals output?"** *Strong:* the mode-transition scheme, the hysteresis, the ripple in that region and the measured efficiency dip. *Evasive:* "It's seamless."
3. **"What limits your boost's loop bandwidth?"** *Strong:* the RHP zero at $D'^2R/L$ at the worst-case load and input, and the resulting crossover frequency. *Evasive:* "We use current mode, so it's fast."
4. **"What happens when the output is shorted?"** *Strong:* a disconnect switch or current-limited start-up, because a plain boost has a direct diode path from input to output. *Evasive:* "There is overcurrent protection."

## 10. Concept check

**Q1.** Why must a boost converter's output be higher than its input?

<details><summary>Answer</summary>

Volt-second balance: the inductor sees $+V_{in}$ while the switch is on, so to return its current it must see a negative voltage while the switch is off, $V_{in} - V < 0$, so $V > V_{in}$. Quantitatively $V = V_{in}/D'$.

</details>

**Q2.** Why is a boost's output ripple worse than a buck's of similar size?

<details><summary>Answer</summary>

The output capacitor alone carries the full load during each on-time, because the diode is off, so its ripple is $ID/(f_sC)$, linear in the period. In a buck the inductor smooths the current into the output, and the capacitor sees only a small triangle.

</details>

**Q3.** What limits a boost's maximum gain, and what is the efficiency at that limit?

<details><summary>Answer</summary>

The inductor's resistance, reflected to the output as $R_L/D'^2$, which explodes as $D \to 1$. The gain peaks at $\tfrac12\sqrt{R/R_L}$ where $D' = \sqrt{R_L/R}$, and the efficiency there is exactly 50%.

</details>

**Q4.** Why does an inverting buck-boost stress its switch more than a buck or boost?

<details><summary>Answer</summary>

The switch blocks the sum of input and output magnitudes and carries the inductor current $I/D'$, because all the energy is stored and released in separate intervals. At $D$ = 0.5 its V·A stress is twice that of a buck or boost delivering the same power.

</details>

**Q5.** What does a SEPIC offer that a buck-boost does not?

<details><summary>Answer</summary>

A non-inverting output with the same $D/D'$ magnitude, a continuous (inductor-smoothed) input current, and a series capacitor that blocks DC from input to output. The price is a second inductor (often coupled) and a coupling capacitor carrying ripple current.

</details>

**Q6.** What is a right-half-plane zero, physically, in a boost?

<details><summary>Answer</summary>

When the duty cycle rises, the diode conducts for less time, so the output first gets less current and dips before the larger inductor current makes it rise. An initial move in the wrong direction is the time-domain signature of a right-half-plane zero, which limits loop bandwidth.

</details>

Now work the [problem set](../problems/22-03-problems.md).

## 11. Key terms

[Boost converter](../../../reference/glossary.md#boost-converter) · [Buck-boost converter](../../../reference/glossary.md#buck-boost-converter) · [Four-switch buck-boost](../../../reference/glossary.md#four-switch-buck-boost) · [SEPIC](../../../reference/glossary.md#sepic) · [Ćuk converter](../../../reference/glossary.md#cuk-converter) · [Right-half-plane zero](../../../reference/glossary.md#right-half-plane-zero) · [Switch stress](../../../reference/glossary.md#switch-stress) · [Power-factor correction](../../../reference/glossary.md#power-factor-correction) · [Pass-through mode](../../../reference/glossary.md#pass-through-mode) · [Conversion ratio](../../../reference/glossary.md#conversion-ratio) · [Discontinuous conduction mode (DCM)](../../../reference/glossary.md#discontinuous-conduction-mode-dcm)

## 12. Connections

- **Previous:** [22-02](22-02-buck-converter-steady-state.md) built the method (volt-second and charge balance, small ripple, DCM) applied here.
- **Next:** [22-04](22-04-isolated-converters.md) adds transformers: the flyback is a buck-boost with a coupled inductor, and the forward is a buck with a transformer.
- **Used later:**
  - [22-05](22-05-magnetics-design.md) (boost and coupled inductors);
  - [22-06](22-06-converter-losses-and-wide-bandgap.md) (the switches of a 400 V PFC boost);
  - [22-07](22-07-converter-dynamics-and-control.md) (the boost's right-half-plane zero derived from its averaged model);
  - [22-08](22-08-pmics.md) (buck-boosts in PMICs);
  - [22-09](22-09-batteries-charging-fuel-gauging.md) (rails across a battery's discharge).

## 13. Further study

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 2 (boost and buck-boost by volt-second balance), ch. 3 (the boost with inductor resistance), ch. 5 (DCM) and ch. 6 (converter circuits: Ćuk, SEPIC and the evaluation of switch stresses).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the step-up, buck-boost and Ćuk converters.
- University of Colorado Boulder, *Converter Circuits* (Coursera, R. W. Erickson): the topology modules.

## 14. Sources

1. Texas Instruments, *TPS63802* data sheet, SLVSEU9D (Nov 2018, revised Jan 2021) [R-425].
2. Texas Instruments, *TPS61023* data sheet, SLVSF14B (Sep 2019, revised Aug 2020) [R-425].
3. Texas Instruments, PMP40988 test report TIDT294 (Jun 2022) and PMP23475 test report TIDT415 (Mar 2025) [R-423].
