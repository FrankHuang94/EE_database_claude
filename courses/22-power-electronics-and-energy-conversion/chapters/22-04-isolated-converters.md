<!-- status: verified -->
# 22-04 · Isolated Converters: Flyback and Forward

| | |
|---|---|
| **Course** | [22 · Power Electronics and Energy Conversion](../README.md) |
| **University equivalent** | The transformer-isolated converter weeks of a senior power-electronics course: the transformer model for converters (magnetizing and leakage inductance), core reset, the flyback in CCM and DCM, leakage energy and the RCD clamp, the forward converter with tertiary reset, bridge and push-pull converters, and insulation requirements (Erickson & Maksimović, *Fundamentals of Power Electronics*, ch. 6; Mohan, Undeland & Robbins, the switch-mode dc power supply chapter) |
| **Prerequisites** | [22-03](22-03-boost-buck-boost-topologies.md) (buck-boost, topology stress), [22-02](22-02-buck-converter-steady-state.md) (volt-second balance, DCM), [07-09](../../07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) (transformers and mutual inductance) |
| **Estimated study hours** | 6 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Model a transformer for converter analysis with an ideal transformer, a magnetizing inductance and a leakage inductance, and explain why the core must be reset every cycle.
2. Derive the flyback converter's conversion ratio, switch voltage and peak current in CCM and DCM, and size its magnetizing inductance for a given power.
3. Derive the energy and power lost to leakage inductance in an RCD clamp, and explain why quasi-resonant and active-clamp flybacks exist.
4. Derive the forward converter's ratio, its reset condition and maximum duty cycle with a tertiary winding, and its switch voltage; compare bridge converters for higher power.
5. Explain why converters are isolated, and apply basic insulation rules: insulation grades, creepage and clearance, and the touch-current limit on Y-capacitors.

## 1. Big picture

Every phone charger, laptop adapter and server power supply contains a transformer. It is there for two reasons. Safety: the user must never touch anything connected to the mains, so the output must be galvanically isolated, with no conducting path back to the line, by an insulation barrier rated for thousands of volts. Ratio: converting 400 V to 12 V or 1 V with a single switch duty cycle would need impossible duty cycles (22-02's minimum on-time), while a turns ratio does most of the work and lets the switch run near the middle of its range. The **flyback** is a buck-boost whose inductor has a second winding; it dominates below about 100–150 W because it needs only one magnetic part. The **forward** converter is a buck behind a transformer; it and its bridge relatives (half bridge, full bridge, push-pull) take over at higher power. This chapter builds both from the transformer model, shows where their energy goes astray (leakage inductance, magnetizing current), and sets out the insulation rules that make a converter safe to touch.

- **USB-C chargers and adapters:** quasi-resonant flybacks, increasingly with GaN switches, from 20 W to well over 100 W (22-01, 22-06).
- **Server and telecom supplies:** forward and full-bridge converters, and resonant LLC converters (22-06, 22-10), behind a PFC boost.
- **Isolated gate drivers, sensors and industrial I/O:** small flybacks and push-pull converters that move a few watts across an isolation barrier.
- **Regulation and certification:** insulation, creepage and touch-current limits are pass/fail items in every safety certification.

## 2. Intuition first

**A transformer that cannot store energy, and one that must.** An ideal transformer multiplies voltage by its turns ratio and divides current by the same ratio; it stores nothing. A real transformer also has a **magnetizing inductance**: the primary winding by itself is an inductor, and some current must flow in it to set up the core's flux. That current rises while the primary sees a positive voltage and must be brought back down (the core **reset**) before the next cycle, or it ratchets up each cycle until the core saturates. A transformer cannot pass DC, so a switching converter must apply positive *and* negative volt-seconds to it, the same volt-second balance as 22-02 applied to the magnetizing inductance.

The **forward** converter uses the transformer as a transformer: power flows through it during the on-time, and the magnetizing current is a nuisance to be reset. The **flyback** turns this around: its "transformer" is really two coupled inductors. Energy is stored in the magnetizing inductance during the on-time (the secondary diode blocks) and released to the output through the secondary during the off-time. The magnetizing inductance *is* the energy store, exactly like the buck-boost's inductor of 22-03.

**An analogy and its limits.** A forward converter is a gearbox (a transformer) feeding a buck converter. A flyback is a rechargeable battery that is charged from one circuit and discharged into another that never touches the first. The battery analogy captures why the flyback's output is isolated and why its energy per cycle is limited by what the "battery" (the core's gap) can hold. It misses that the flyback's "battery" is charged and emptied a hundred thousand times a second, and that some energy is stuck in the leakage inductance, which belongs to neither circuit and must be dumped somewhere.

![The flyback converter: a primary winding switched from the input bus, a coupled secondary winding with a diode and output capacitor, and the transformer model drawn as an ideal transformer with magnetizing inductance on the primary and a series leakage inductance](../../../assets/figures/22-04/flyback.svg)

## 3. Theory

### 3.1 The transformer model for converters

A two-winding transformer with $N_1$ primary and $N_2$ secondary turns is modelled, referred to the primary, as:

- an **ideal transformer** with turns ratio $n = N_1/N_2$, so $v_1 = nv_2$ and $i_2 = ni_1'$, where $i_1'$ is the part of the primary current that is transferred;
- a **magnetizing inductance** $L_m$ across the ideal transformer's primary, carrying the magnetizing current $i_m$ that sets up the core flux;
- a **leakage inductance** $L_{lk}$ in series, representing flux that links one winding but not the other.

The flux in the core is proportional to $i_m$, and $v_1 = L_m\,di_m/dt$ across the magnetizing branch. Volt-second balance (22-02) applied to $L_m$ is the **core-reset** condition: the magnetizing current must return to its starting value every cycle, so the primary's volt-seconds must average to zero. The peak flux density follows from Faraday's law, $v_1 = N_1A_e\,dB/dt$, where $A_e$ is the core's cross-section:

$$
\Delta B = \frac{1}{N_1A_e}\int v_1\,dt = \frac{V_{in}DT_s}{N_1A_e}
$$

for a primary that sees $V_{in}$ for $DT_s$. The design must keep $B$ below saturation (22-05).

### 3.2 The flyback converter

The primary winding connects the input $V_{in}$ to a switch to ground; the secondary connects through a diode to the output capacitor and load. The dots are arranged so that the diode blocks while the switch is on. Ignore leakage for now and treat the magnetizing inductance as the converter's inductor.

- **Subinterval 1** ($DT_s$, switch on): the primary sees $V_{in}$, so $v_{L_m} = V_{in}$. The secondary voltage is $V_{in}/n$ with the polarity that reverse-biases the diode, so no current flows to the output, and the capacitor supplies the load.
- **Subinterval 2** ($D'T_s$, switch off): the magnetizing current, which cannot stop, transfers to the secondary and flows through the diode into the output. The secondary is clamped at $V$, and the primary sees $-nV$, so $v_{L_m} = -nV$.

Volt-second balance on $L_m$:

$$
V_{in}D - nVD' = 0 \quad\Longrightarrow\quad V = \frac{V_{in}}{n}\cdot\frac{D}{D'}, \qquad M = \frac{1}{n}\cdot\frac{D}{1 - D} .
$$

This is the buck-boost ratio of 22-03 divided by the turns ratio, and without the inversion (the dots take care of polarity).

**Switch stress.** While the switch is off, its drain sits at the input plus the **reflected output voltage** $V_R = nV$:

$$
V_{DS,off} = V_{in} + nV ,
$$

plus a leakage spike (§3.3). The turns ratio trades this voltage against the duty cycle: a larger $n$ means a larger reflected voltage, so a higher switch voltage but a longer duty cycle and a lower primary current.

**Charge balance and currents.** The output current is delivered only during $D'$, as the secondary current $n\,i_m$, so charge balance gives $nI_mD' = I$: the average magnetizing current is $I_m = I/(nD')$. The input current is $i_m$ during $D$, so $I_{in} = DI_m$. Check: $V_{in}DI_m = V_{in}DI/(nD') = VI$.

**DCM and the energy view.** Most low-power flybacks run in discontinuous or **boundary (critical) conduction**: the magnetizing current falls to zero every cycle. Each cycle then stores and releases a fixed packet of energy $\tfrac12L_mI_{pk}^2$, so the power is

$$
P = \tfrac12L_mI_{pk}^2f_s ,
$$

regardless of output voltage. With $I_{pk} = V_{in}DT_s/L_m$ this is $P = (V_{in}D)^2T_s/(2L_m)$: in DCM the flyback acts as a power source set by its duty cycle, a useful property for control. A **quasi-resonant (QR)** flyback goes further. After the magnetizing current reaches zero, the drain voltage rings down through the switch's output capacitance and the magnetizing inductance, and the controller turns the switch on at the ring's valley. That cuts the capacitive turn-on loss (22-06) at the cost of a frequency that varies with line and load. A TI 65 W GaN reference design is a QR flyback with a "32:5" turns ratio and switching frequencies from "76 kHz" to "163 kHz" [1].

### 3.3 Leakage inductance and the clamp

Leakage inductance stores energy that the secondary cannot collect, because by definition its flux does not link the secondary. When the switch turns off, the leakage current $I_{pk}$ must go somewhere. Without a path it would drive the drain voltage up until something breaks (22-01's Rule 2). An **RCD clamp** (a diode from the drain to a capacitor held at a clamp voltage $V_c$ above the input, with a resistor that bleeds its energy) catches it.

During the clamp interval the leakage inductance sees $V_c - V_R$, because its far end is held at the reflected voltage by the secondary while the clamp holds the drain. Its current falls from $I_{pk}$ to zero in

$$
t_c = \frac{L_{lk}I_{pk}}{V_c - V_R} .
$$

The clamp receives the charge $\tfrac12I_{pk}t_c$ at voltage $V_c$, so the energy it absorbs per cycle is

$$
E_c = V_c\cdot\frac12I_{pk}t_c = \frac12L_{lk}I_{pk}^2\cdot\frac{V_c}{V_c - V_R} .
$$

The leakage energy itself, $\tfrac12L_{lk}I_{pk}^2$, is multiplied by $V_c/(V_c - V_R)$. During the clamp interval the magnetizing inductance keeps pushing energy into the reflected voltage, and some of that also ends up in the clamp. Pushing $V_c$ close to $V_R$ (a tight clamp) makes the multiplier large; a loose clamp needs a higher-voltage switch. Because the clamp's loss $P_c = E_cf_s$ can be several per cent of the output at typical leakage (Example 22-04.5), designers either recycle the leakage energy with an **active clamp** (a second switch and capacitor that return it) or minimize leakage with interleaved windings (22-05).

### 3.4 The forward converter

The forward converter uses the transformer as a transformer and puts a buck converter's LC filter on the secondary. During the on-time the primary sees $V_{in}$, the secondary delivers $V_{in}/n$ through a diode into the output inductor, and the converter is a buck from $V_{in}/n$. During the off-time a freewheeling diode carries the output inductor's current. Volt-second balance on the output inductor gives the buck's result scaled by the turns ratio:

$$
V = \frac{D\,V_{in}}{n} .
$$

**Reset.** The transformer's magnetizing current rose during the on-time by $V_{in}DT_s/L_m$ and must be returned to zero during the off-time. The classic method is a **tertiary winding** of $N_3$ turns wound with the primary and connected through a diode back to the input. When the switch opens, the magnetizing current transfers to the tertiary, which is clamped at $V_{in}$; the primary then sees $-V_{in}N_1/N_3$. Volt-second balance on $L_m$:

$$
V_{in}D = V_{in}\frac{N_1}{N_3}D_r \quad\Longrightarrow\quad D_r = D\frac{N_3}{N_1} .
$$

The reset must finish before the next on-time, $D + D_r \le 1$, so

$$
D_{max} = \frac{1}{1 + N_3/N_1} ,
$$

which is 0.5 for the usual $N_3 = N_1$. During reset the switch blocks the input plus the reflected tertiary voltage:

$$
V_{DS,off} = V_{in}\left(1 + \frac{N_1}{N_3}\right) = 2V_{in}\ \ (N_3 = N_1) .
$$

The magnetizing energy $\tfrac12L_mi_{m,pk}^2$ is returned to the input through the tertiary, not lost. Other reset schemes (RCD, resonant, active clamp, two-switch forward) trade duty-cycle range against switch voltage in the same way.

### 3.5 Bridge and push-pull converters

At higher power, single-switch converters waste their transformer, because they excite its core in only one direction. Converters that drive the primary alternately positive and negative reset the core automatically and use twice the flux swing:

- **Push-pull:** two switches drive a centre-tapped primary from a low-voltage input. Each switch blocks $2V_{in}$. Suits low-voltage, high-current inputs.
- **Half bridge:** two switches and a capacitor divider apply $\pm V_{in}/2$. Each switch blocks $V_{in}$.
- **Full bridge:** four switches apply $\pm V_{in}$. Each switch blocks only $V_{in}$ and carries roughly $I/n$; it suits the highest powers. Its **phase-shifted** form achieves zero-voltage switching (22-06).

With a centre-tapped rectifier and output LC filter, each of these is a buck-derived converter, $V = D_{eff}V_{in}/n$ for the full bridge, where $D_{eff}$ is the fraction of the period during which the primary is driven. Their weak point is **flux walking**: any imbalance between the positive and negative volt-seconds accumulates in the core. Designs use current-mode control (22-07) or a series blocking capacitor to prevent it.

### 3.6 Why and how converters are isolated

**Reasons.**

1. **Safety.** A mains-connected product must keep every user-touchable part at a voltage that is safe to touch. IEC 62368-1 defines the safest energy class, ES1, as "safe for all persons, including children, to touch". Per a UL brief on the standard, ES1 limits are 30 V RMS and 60 V DC, with touch current up to 0.5 mA RMS below 1 kHz [3].
2. **Ground separation.** Isolation breaks ground loops in industrial and medical equipment and lets circuits float at different potentials.
3. **Ratio and polarity.** A turns ratio handles large voltage ratios, and multiple windings give multiple or negative outputs.

**Insulation grades.** *Functional* insulation only makes the circuit work. *Basic* insulation gives one level of protection against shock. *Supplementary* insulation is a second, independent level. *Reinforced* insulation is a single system equivalent to the two. A mains-to-user barrier needs double or reinforced insulation.

**Clearance and creepage.** **Clearance** is the shortest distance through air between conductors. It must withstand the mains' transient overvoltages, which IEC 60664-1 sets by overvoltage category; for mains up to 300 V line to neutral these are 1.5, 2.5, 4.0 and 6.0 kV for categories I–IV. Reinforced insulation uses the clearance for the impulse voltage "one step higher", and clearances grow with altitude because thin air breaks down more easily [4]. **Creepage** is the shortest distance along a surface. It depends on the working voltage, the pollution degree and the surface material's tracking resistance (its material group), and reinforced creepage is twice basic [4]. These rules are why a charger's transformer has thick triple-insulated wire and its board has slots under the transformer.

**Y-capacitors.** A small capacitor across the barrier (from primary ground to secondary ground) gives common-mode switching noise a short return path and is often essential to pass EMI tests. It is called a **Y-capacitor** and is rated so that its failure cannot cause shock. One series is rated "Class Y1, 500 VAC", tested "4000 VAC" and against "3 pulses of 8 kV" [5]. But every Y-capacitor conducts line-frequency current from the mains into the user-touchable side, $I = 2\pi fCV$, so the total Y-capacitance is capped by the touch-current limit (Example 22-04.6).

## 4. Worked examples

### Example 22-04.1 · Flyback ratio and switch stress (tier A)

**Setup.** A 20 V USB-PD flyback uses a 32:5 turns ratio, as in a TI reference design [1]. Treating it as a CCM flyback, find (a) the turns ratio $n$, (b) the duty cycle from a 150 V bus and (c) the reflected voltage. Find the switch's off-state voltage (before any leakage spike) (d) at 150 V and (e) at the 373 V peak of a 264 V line.

**Solution.**

- (a) $n = 32/5$ = **6.4**.
- (b) $D/D' = nV/V_{in} = 128/150$, so $D = 128/278$ = **0.460**.
- (c) $V_R = nV$ = **128** V.
- (d) $150 + 128$ = **278** V; (e) $373.4 + 128$ = **501** V.

**Units check.** Turns ratio is dimensionless; all voltages in volts.

**Sanity check.** At high line the switch blocks about 500 V before the leakage spike, which is why adapter flybacks use 650 V-class or higher switches. A larger turns ratio would raise the duty cycle and lower the primary current, but push the drain voltage further.

### Example 22-04.2 · Sizing a boundary-conduction flyback (tier B)

**Setup.** A 65 W flyback (92% efficient, so 70.65 W of input) runs at the CCM–DCM boundary at its minimum bus of 100 V, with $n$ = 6.4, 20 V out and 100 kHz. Find (a) the duty cycle at the boundary, (b) the peak primary current, (c) the magnetizing inductance and (d) the energy stored per cycle.

**Solution.**

- (a) At the boundary the converter obeys the CCM ratio with no idle time: $D = nV/(V_{in} + nV) = 128/228$ = **0.561**.
- (b) The input current is a triangle from 0 to $I_{pk}$ during $D$, so its average is $\tfrac12I_{pk}D = P_{in}/V_{in}$, giving $I_{pk} = 2 \times 70.65/(100 \times 0.561)$ = **2.52** A.
- (c) $L_m = V_{in}DT_s/I_{pk} = 100 \times 0.561 \times 10\ \mu\text{s}/2.517$ = **223** µH.
- (d) $\tfrac12 \times 223\ \mu\text{H} \times 2.517^2$ = **0.707** mJ.

**Units check.** V·s/A = H; H·A² = J.

**Sanity check.** 0.707 mJ per cycle times 100 000 cycles per second is 70.65 W, the input power, as it must be: in a boundary-conduction flyback every joule passes through the magnetizing inductance's gap. That stored energy, not the power, sets the core size (22-05).

### Example 22-04.3 · Turns ratio and duty limit in a forward converter (tier B)

**Setup.** A telecom forward converter makes 5 V from a 36–75 V bus with a 1:1 tertiary reset ($D_{max}$ = 0.5). (a, b) With $n$ = 4, find the duty cycle at 48 V and at 36 V; is it feasible? (c, d) With $n$ = 3, find the duty cycle at 36 V and at 75 V. (e) What does the switch block at 75 V?

**Solution.**

- (a) $D = nV/V_{in} = 20/48$ = **0.417**; (b) at 36 V, $20/36$ = **0.556** > 0.5: not feasible.
- (c) $n$ = 3: $15/36$ = **0.417**; (d) $15/75$ = **0.2**.
- (e) $V_{in}(1 + N_1/N_3) = 2 \times 75$ = **150** V.

**Units check.** Ratios of volts.

**Sanity check.** The reset limit forces a lower turns ratio than the nominal input would suggest, so the primary current is higher. The switch must block twice the highest input, plus spikes. These two costs are why two-switch forward and active-clamp forward converters exist.

### Example 22-04.4 · Magnetizing current and reset energy (tier B)

**Setup.** A forward converter at 48 V, $D$ = 0.4 and 250 kHz has $L_m$ = 500 µH. Find (a) the peak magnetizing current, (b) the magnetizing energy per cycle and (c) the power that the reset circuit must handle.

**Solution.**

- (a) $\Delta i_m = 48 \times 0.4 \times 4\ \mu\text{s}/500\ \mu\text{H}$ = **0.154** A.
- (b) $\tfrac12 \times 500\ \mu\text{H} \times 0.1536^2$ = **5.90** µJ.
- (c) $5.90\ \mu\text{J} \times 250\ \text{kHz}$ = **1.47** W.

**Units check.** V·s/H = A; J × s⁻¹ = W.

**Sanity check.** A tertiary winding returns these 1.47 W to the input; an RCD reset would burn them. The magnetizing current is small compared with a typical load current reflected to the primary, which is why the forward converter's transformer is a true transformer and a large $L_m$ (an ungapped core) is good.

### Example 22-04.5 · The price of leakage inductance (tier B)

**Setup.** The flyback of Example 22-04.2 has a leakage inductance of 2% of $L_m$ and an RCD clamp at $V_c$ = 200 V (the reflected voltage is 128 V). Find (a) the leakage inductance, (b) the leakage energy per cycle, (c) the clamp multiplier $V_c/(V_c - V_R)$, (d) the clamp power and (e) its share of the input power.

**Solution.**

- (a) $0.02 \times 223$ = **4.46** µH.
- (b) $\tfrac12 \times 4.46\ \mu\text{H} \times 2.517^2$ = **14.1** µJ.
- (c) $200/72$ = **2.78**.
- (d) $14.13\ \mu\text{J} \times 2.78 \times 100\ \text{kHz}$ = **3.93** W.
- (e) $3.93/70.65$ = **5.6** %.

**Units check.** J × s⁻¹ = W.

**Sanity check.** Two per cent of leakage costs over 5% of the input, more than the whole loss budget of a 92%-efficient adapter would allow on top of its other losses. This is why chargers minimize leakage with interleaved windings (22-05), and why active-clamp and quasi-resonant designs recycle or avoid this energy.

### Example 22-04.6 · Clearance, creepage and Y-capacitance (tier C)

**Setup.** (a) A reinforced barrier needs 3.8 mm of clearance at sea level (IEC 62368-1's value for 4 kV); the altitude factor at 5000 m is 1.48 [4]. What clearance is needed at 5000 m? (b, c, d) Reinforced creepage at 400 V working voltage, pollution degree 2, is twice the basic 2.0, 2.8 and 4.0 mm for material groups I, II and III [4]: what are the reinforced values? (e) What line-frequency current does a 2.2 nF Y-capacitor pass at 264 V and 60 Hz, and (f) what total Y-capacitance keeps the touch current within 0.5 mA?

**Solution.**

- (a) $3.8 \times 1.48$ = **5.62** mm (the source rounds up to 5.7 mm [4]).
- (b) **4.0**, (c) **5.6** and (d) **8.0** mm.
- (e) $I = 2\pi \times 60 \times 2.2\ \text{nF} \times 264$ = **0.219** mA.
- (f) $C = 0.5\ \text{mA}/(2\pi \times 60 \times 264)$ = **5.02** nF.

**Units check.** Hz × F × V = A.

**Sanity check.** Most FR-4 boards are material group III, so the 8 mm reinforced creepage applies to the board, which is why chargers slot their boards under the transformer. The Y-capacitance limit of about 5 nF caps how much common-mode noise filtering can cross the barrier: EMI and safety pull in opposite directions.

### Example 22-04.7 · Why bridges win at high power (tier C)

**Setup.** Deliver 1 kW at 50 V from a 400 V bus. (a) A full bridge with $n$ = 6 needs what effective duty, (b) what does each switch block, and (c) what current (approximately $I/n$) does it carry? A DCM flyback at $D$ = 0.5 with a reflected voltage equal to the input needs (d) what switch voltage and (e) what peak current? (f, g) Compare $V \times I$ per switch.

**Solution.**

- (a) $D_{eff} = nV/V_{in} = 300/400$ = **0.75**.
- (b) **400** V; (c) $20/6$ = **3.33** A.
- (d) $400 + 400$ = **800** V; (e) $I_{pk} = 2P/(V_{in}D) = 2000/200$ = **10.0** A.
- (f) Full bridge: $400 \times 3.33$ = **1333** V·A per switch; (g) flyback: $800 \times 10$ = **8000** V·A.

**Units check.** V × A.

**Sanity check.** Even with four switches, the full bridge's total of about 5.3 kV·A is less than the flyback's single 8 kV·A switch, and its transformer uses the core in both directions. Above a few hundred watts, the flyback's simplicity no longer pays for its stresses.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 22-04.1a | turns ratio | 6.4 | |
| Ex 22-04.1b | duty cycle at 150 V | 0.460 | |
| Ex 22-04.1c | reflected voltage | 128 | V |
| Ex 22-04.1d | switch voltage at 150 V | 278 | V |
| Ex 22-04.1e | switch voltage at 373 V | 501 | V |
| Ex 22-04.2a | boundary duty cycle | 0.561 | |
| Ex 22-04.2b | peak primary current | 2.52 | A |
| Ex 22-04.2c | magnetizing inductance | 223 | µH |
| Ex 22-04.2d | energy per cycle | 0.707 | mJ |
| Ex 22-04.3a | duty at 48 V, n = 4 | 0.417 | |
| Ex 22-04.3b | duty at 36 V, n = 4 | 0.556 | |
| Ex 22-04.3c | duty at 36 V, n = 3 | 0.417 | |
| Ex 22-04.3d | duty at 75 V, n = 3 | 0.2 | |
| Ex 22-04.3e | switch voltage at 75 V | 150 | V |
| Ex 22-04.4a | peak magnetizing current | 0.154 | A |
| Ex 22-04.4b | magnetizing energy | 5.90 | µJ |
| Ex 22-04.4c | reset power | 1.47 | W |
| Ex 22-04.5a | leakage inductance | 4.46 | µH |
| Ex 22-04.5b | leakage energy | 14.1 | µJ |
| Ex 22-04.5c | clamp multiplier | 2.78 | |
| Ex 22-04.5d | clamp power | 3.93 | W |
| Ex 22-04.5e | clamp share of input | 5.6 | % |
| Ex 22-04.6a | clearance at 5000 m | 5.62 | mm |
| Ex 22-04.6b | reinforced creepage, group I | 4.0 | mm |
| Ex 22-04.6c | reinforced creepage, group II | 5.6 | mm |
| Ex 22-04.6d | reinforced creepage, group III | 8.0 | mm |
| Ex 22-04.6e | Y-capacitor current | 0.219 | mA |
| Ex 22-04.6f | Y-capacitance limit | 5.02 | nF |
| Ex 22-04.7a | full-bridge effective duty | 0.75 | |
| Ex 22-04.7b | full-bridge switch voltage | 400 | V |
| Ex 22-04.7c | full-bridge switch current | 3.33 | A |
| Ex 22-04.7d | flyback switch voltage | 800 | V |
| Ex 22-04.7e | flyback peak current | 10.0 | A |
| Ex 22-04.7f | full-bridge V·A per switch | 1333 | V·A |
| Ex 22-04.7g | flyback V·A | 8000 | V·A |

## 5. Simulate it

The lab ([labs/22-04-lab](../labs/22-04-lab/README.md)) collects the formulas in `isolated.py` and runs two ngspice netlists:

- `flyback.cir`: a CCM flyback with a coupled-inductor transformer;
- `forward.cir`: a forward converter with a three-winding transformer and tertiary reset.

**Predict, then run.**

1. *Predict* the flyback's output and its switch's off-state voltage, then run `flyback.cir` (Part 1).
2. *Predict* the forward converter's output, the peak switch voltage during reset and the magnetizing current. Run `forward.cir` and watch the magnetizing current return to zero every cycle (Part 2).
3. *Predict* the clamp power for 1%, 2% and 5% leakage, and plot it against clamp voltage (Part 3).
4. *Predict* the creepage, clearance and Y-capacitance limits for a reinforced barrier, then tabulate them against altitude and material group (Part 4).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Larger turns ratio (flyback) | Lower primary current, more duty-cycle range | Higher reflected voltage and switch voltage | Power-stage designer |
| Tighter RCD clamp voltage | Lower switch voltage | Larger clamp multiplier, more loss | Power-stage designer |
| Active clamp or quasi-resonant operation | Recycles leakage energy, soft turn-on | Extra switch or variable frequency, control complexity | Power IC architect |
| Interleaved windings | Less leakage | More insulation layers, higher interwinding capacitance (common-mode noise) | Magnetics designer |
| Forward instead of flyback | Lower peak currents, transformer not an energy store | Output inductor, reset circuit, duty limit | Power architect |
| Full bridge instead of single switch | Half the switch voltage, both flux directions, ZVS possible | Four switches and drivers, flux walking | Power architect |
| More Y-capacitance | EMI margin | Touch current; certification limit | EMC and safety engineers |

## 7. Numbers to know

| Quantity | Typical value | Source |
|---|---|---|
| Flyback ratio and switch voltage | $V = (V_{in}/n)\,D/D'$; $V_{in} + nV$ plus spike | §3.2 |
| Forward ratio and reset limit | $V = DV_{in}/n$; $D_{max} = 1/(1 + N_3/N_1)$ = 0.5 for $N_3 = N_1$; switch $2V_{in}$ | §3.4 |
| Clamp energy per cycle | $\tfrac12L_{lk}I_{pk}^2\,V_c/(V_c - V_R)$ | §3.3 |
| 65 W GaN QR flyback reference | 32:5 turns; 76–163 kHz; 92.8–94.3% at full load | [1] |
| ES1 (touch-safe) limits, IEC 62368-1 | 30 V RMS, 60 V DC; 0.5 mA RMS touch current below 1 kHz | [3] |
| Mains transient, ≤ 300 V line to neutral | 1.5 / 2.5 / 4.0 / 6.0 kV for OVC I–IV | [4] |
| Reinforced creepage, 400 V, PD2 | 4.0 / 5.6 / 8.0 mm for material groups I–III | [4] |
| Y1 capacitor rating | 500 VAC; 4000 VAC test; 8 kV impulse | [5] |

## 8. Common mistakes

- **Forgetting the reflected voltage in a flyback's switch rating.** The switch blocks $V_{in} + nV$, plus the leakage spike.
- **Treating the flyback's transformer as a transformer.** It is a coupled inductor; its gap stores the energy, and that energy sets its size.
- **Running a forward converter above its reset duty limit.** The core walks into saturation within a few cycles.
- **Ignoring leakage.** A few per cent of leakage can cost several per cent of efficiency in an RCD clamp.
- **Measuring creepage through the air.** Creepage is along surfaces, clearance is through air, and both must be met.
- **Adding Y-capacitance freely to pass EMI.** Its leakage current is a safety limit.

## 9. Practitioner lens

**State of the art (as of Nov 2026).**

- **Adapters [Industry estimate].** TI's 65 W GaN USB-PD reference is a quasi-resonant flyback with an integrated "170-mΩ GaN FET", a "32:5" turns ratio and switching from 76 to 163 kHz. It reaches 92.83–94.32% at full load and 25.29 W/in³ [1]. A GaN Systems reference argues that silicon QR flybacks were limited to "around 100KHz", against about 180 kHz for its GaN design [2]. That is a vendor framing of a real trend [Contested on the exact limit].
- **Safety standards [Established].** IEC 62368-1 replaced IEC 60950-1, which "had been withdrawn in December, 2020" [4]. Its energy-source classes replace the old SELV concept: ES1 is "safe for all persons, including children, to touch" [3]. The 2023 edition was not checked for changed limits.
- **Insulation components [Established].** Y1 capacitors rated 500 VAC with 8 kV impulse testing are standard parts [5]. Triple-insulated wire and slotted boards are common practice for reinforced barriers.

**Commercial relevance.** For a corporate-development view:

- **The charger market is flybacks:** controllers, GaN switches and synchronous-rectifier controllers for 20–240 W USB-C adapters (USB PD up to 240 W, 22-01).
- **Differentiation:** density and efficiency come from higher frequency and from recycling leakage energy (QR, active clamp), which is where GaN's low switching charge pays (22-06).
- **Above a few hundred watts:** forward, full-bridge and resonant converters take over, and the silicon content shifts to bridge drivers and controllers.

**Marketing vs Reality.**

- **"Smallest charger, highest density."** Density depends on the box (22-01), and a smaller transformer means less creepage room and harder thermals. Ask for the case temperature at full load and the certification status.
- **"GaN lets us switch faster."** It does, but leakage and clamp losses scale with frequency too. The gain comes from soft switching (QR, active clamp), not from GaN alone.
- **"Passes EMI with margin."** Ask how much Y-capacitance it uses and what touch current that implies.

**Questions for engineering leaders.**

1. **"What is your reflected voltage and your switch's voltage margin at high line, including the leakage spike?"** *Strong:* a drain-voltage budget at 264 V AC with measured spike, clamp setting and derating. *Evasive:* "We use 650 V parts."
2. **"Where does your leakage energy go?"** *Strong:* measured leakage as a percentage of $L_m$, the clamp or active-clamp scheme, and its loss at full and light load. *Evasive:* "Our transformer is well designed."
3. **"What insulation system does the transformer use, and what creepage does the board achieve?"** *Strong:* reinforced via triple-insulated wire or margin tape, creepage and clearance numbers against the standard's tables, the hipot level and altitude rating. *Evasive:* "It's certified."
4. **"Why this topology at this power?"** *Strong:* switch stresses, magnetics size and efficiency compared with the alternatives (flyback against forward against LLC). *Evasive:* "It's what we've always used."

## 10. Concept check

**Q1.** Why must a transformer's core be reset every cycle, and what principle expresses this?

<details><summary>Answer</summary>

The magnetizing current, which is proportional to the core flux, rises while the primary sees positive volts and must return to its starting value, or it ratchets up each cycle until the core saturates. This is volt-second balance applied to the magnetizing inductance: the primary's volt-seconds must average to zero.

</details>

**Q2.** Why is a flyback's "transformer" really a coupled inductor?

<details><summary>Answer</summary>

Its windings never conduct at the same time: the primary charges the magnetizing inductance while the secondary diode blocks, and the secondary discharges it while the primary is open. All the energy is stored in the core (in its gap) between the two intervals, like a buck-boost's inductor, rather than passing straight through as in a forward converter.

</details>

**Q3.** What sets the flyback's switch voltage?

<details><summary>Answer</summary>

The input plus the reflected output voltage, $V_{in} + nV$, plus the leakage-inductance spike limited by the clamp. A larger turns ratio raises the reflected voltage.

</details>

**Q4.** Why does a forward converter with a 1:1 tertiary winding have a 50% duty-cycle limit?

<details><summary>Answer</summary>

The magnetizing current rises for $DT_s$ under $V_{in}$ and is reset through the tertiary under $V_{in}N_1/N_3$, which takes $DT_s N_3/N_1$. Reset must finish within the period, so $D(1 + N_3/N_1) \le 1$, which gives $D \le 0.5$ for $N_3 = N_1$.

</details>

**Q5.** Why does an RCD clamp absorb more than the leakage energy?

<details><summary>Answer</summary>

While the leakage current is falling, the clamp holds the drain at $V_c$, and the leakage inductance sees only $V_c - V_R$. The clamp absorbs charge at $V_c$, so its energy is the leakage energy times $V_c/(V_c - V_R)$; part of it comes from the magnetizing energy that would otherwise have gone to the output.

</details>

**Q6.** Why can't a designer add as much Y-capacitance as EMI requires?

<details><summary>Answer</summary>

Y-capacitors conduct line-frequency current, $2\pi fCV$, from the mains into the user-touchable side, and the touch current is limited by the safety standard (0.5 mA for ES1 below 1 kHz). That caps the total at a few nanofarads for 264 V, 60 Hz mains.

</details>

Now work the [problem set](../problems/22-04-problems.md).

## 11. Key terms

[Galvanic isolation](../../../reference/glossary.md#galvanic-isolation) · [Magnetizing inductance](../../../reference/glossary.md#magnetizing-inductance) · [Leakage inductance](../../../reference/glossary.md#leakage-inductance) · [Core reset](../../../reference/glossary.md#core-reset) · [Flyback converter](../../../reference/glossary.md#flyback-converter) · [Reflected voltage](../../../reference/glossary.md#reflected-voltage) · [Quasi-resonant flyback](../../../reference/glossary.md#quasi-resonant-flyback) · [RCD clamp](../../../reference/glossary.md#rcd-clamp) · [Active clamp](../../../reference/glossary.md#active-clamp) · [Forward converter](../../../reference/glossary.md#forward-converter) · [Tertiary winding](../../../reference/glossary.md#tertiary-winding) · [Full-bridge converter](../../../reference/glossary.md#full-bridge-converter) · [Flux walking](../../../reference/glossary.md#flux-walking) · [Reinforced insulation](../../../reference/glossary.md#reinforced-insulation) · [Clearance](../../../reference/glossary.md#clearance) · [Creepage](../../../reference/glossary.md#creepage) · [Y-capacitor](../../../reference/glossary.md#y-capacitor)

## 12. Connections

- **Previous:** [22-03](22-03-boost-buck-boost-topologies.md) (the buck-boost, of which the flyback is the isolated form); [22-02](22-02-buck-converter-steady-state.md) (the buck, of which the forward is the isolated form); [07-09](../../07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md) (mutual inductance and the ideal transformer).
- **Next:** [22-05](22-05-magnetics-design.md) designs the cores, gaps and windings that these converters need, including leakage.
- **Used later:**
  - [22-06](22-06-converter-losses-and-wide-bandgap.md) (switching losses, soft switching, the LLC);
  - [22-07](22-07-converter-dynamics-and-control.md) (controlling across an isolation barrier);
  - [22-10](22-10-datacenter-power-delivery.md) (isolated bus converters and server supplies).

## 13. Further study

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 6 (transformer-isolated converters: forward, flyback, bridge, push-pull, and the transformer model).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the switch-mode dc power supplies chapter.
- TI Power Supply Design Seminar papers on clearance and creepage, and on flyback design (see Sources).

## 14. Sources

1. Texas Instruments, TIDA-050072 design guide TIDUF57 (Nov 2023) [R-423].
2. GaN Systems (now Infineon), *65W, 18.5W/in³ GaN-based QR Adaptor Reference Design*, GS-EVB-CHG-65WQR-GS1 manual [R-137].
3. C. Sato (UL), "Electrical Energy Source (ES) vs. SELV and LCC," IEC 62368-1 technical brief, 4 Jun 2010 [R-426].
4. W. Zhang and T. LaBella, "Demystifying clearance and creepage distance for high-voltage end equipment," TI Power Supply Design Seminar, SLUP421 (2024) [R-426].
5. Vishay, *VY1 series* data sheet (revision 28 Sep 2026) [R-426].
