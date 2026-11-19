<!-- status: verified -->
# 06-11 · Practical DC Circuits and Measurement

| | |
|---|---|
| **Course** | [06 · Circuit Analysis I (DC)](../README.md) |
| **University equivalent** | The DC measurement laboratory that accompanies a sophomore Circuits course (meter loading, ammeter burden, four-wire resistance), with the measurement-uncertainty and wiring material of an introductory instrumentation course |
| **Prerequisites** | [06-02](06-02-circuit-elements-and-ohms-law.md) (resistivity, sheet resistance, temperature coefficients), [06-07](06-07-linearity-and-superposition.md) (tolerance, worst case and RSS), [06-08](06-08-thevenin-and-norton.md) (Thévenin equivalents and loading), [06-10](06-10-ideal-op-amp.md) (feedback). Each fact used is restated where it is needed. |
| **Estimated study hours** | 4 |
| **Last verified** | 2026-11-19 |

**Learning objectives.** After this chapter you can:

1. Calculate the loading error of a voltmeter and the burden of an ammeter from the circuit's Thévenin resistance, and correct a reading for them.
2. Compute a measurement's uncertainty from a meter's accuracy specification, choose the range that minimizes it, and combine independent errors by worst case and by RSS.
3. Explain four-terminal (Kelvin) measurement of resistance and current, and quantify the lead, contact and copper errors it removes.
4. Calculate wire and trace resistance and its temperature drift, and use remote sensing to regulate the voltage at a load.
5. Carry out a worst-case analysis of a complete measurement chain: sensor, divider, wiring and converter.

## 1. Big picture

Every measurement is a circuit. A voltmeter connected across two nodes is a resistor added to the network; an ammeter inserted in a branch is a resistor added in series; the wires to both are resistors too. The ideal-instrument assumption of earlier chapters (infinite voltmeter resistance, zero ammeter resistance, zero-ohm wires) is a limit, and this chapter asks when the limit is good enough and what to do when it is not. The tools are the ones already built: Thévenin equivalents (06-08) to see what the instrument sees, superposition and worst-case analysis (06-07) to combine errors, and feedback (06-10) to cancel the drop in a wire. The payoff is practical judgment: reading a datasheet's accuracy line, laying out a current shunt, and knowing which digit of a reading to believe.

- **Bench and field measurement:** a 10 MΩ handheld meter reads the midpoint of a megohm divider 4.76% low; a "0.05%" meter is 0.38% uncertain low on its range (Examples 06-11.1 and 06-11.3).
- **Current sensing in products:** battery gauges, motor drives, server power supplies and electric vehicles measure current through milliohm shunts, where a tenth of a milliohm of copper in the wrong place is a 10% error (Example 06-11.5).
- **Power delivery:** a 12 V supply delivering 10 A through 1.5 m of cable loses 0.4 V before the load; remote sensing puts it back (Example 06-11.6), the same idea that regulates a processor's core voltage at the die.
- **Production test and characterization:** four-wire (Kelvin) contacts measure milliohms reliably on testers and probe cards, where contact resistance alone exceeds the quantity measured.

## 2. Intuition first

### The instrument joins the circuit

A voltmeter must take a little current to sense a voltage, and an ammeter must drop a little voltage to sense a current. Each therefore changes what it measures. The size of the change depends on a comparison: the instrument's resistance against the circuit's Thévenin resistance at the point of measurement. A 10 MΩ voltmeter on a 1 kΩ source is invisible (0.01%); on a 1 MΩ source it is not (9%). A 1 Ω ammeter in a 1 kΩ branch is invisible; in a 10 Ω branch it is not.

![Left: a voltmeter, modeled as its input resistance R_in, across a Thévenin source V_th, R_th, reading V_th R_in/(R_th + R_in). Right: an ammeter, modeled as its internal resistance R_A, inserted in series with a Thévenin source, reading V_th/(R_th + R_A)](../../../assets/figures/06-11/meter-models.svg)

*Figure 1. A voltmeter is a large resistor in parallel; an ammeter is a small resistor in series. What matters is how each compares with the circuit's Thévenin resistance at the point of connection.*

### The finance analogy, and where it breaks

Measuring a circuit with a meter is like discovering a stock's price by trading it: a small trade in a liquid market (a low-resistance source) learns the price without moving it, while a large trade in an illiquid one (a high-resistance source) moves the price it is trying to learn. The fix is the same in spirit too: trade smaller (a higher-resistance voltmeter), or estimate the market impact and correct for it (the loading correction of Section 3.1). *Where it breaks:* market impact is uncertain and often permanent; a meter's loading error is deterministic, exactly computable from two resistances, and disappears when the meter is removed.

### Separate the wire that carries current from the wire that senses voltage

Any wire carrying current has a voltage drop along it. If the same wire is also used to sense a voltage, its drop is added to the reading. The cure, invented in the nineteenth century for measuring small resistances and used today in every precision current shunt, is to use separate wires: one pair to **force** the current and another pair, carrying almost no current, to **sense** the voltage. With no current in the sense wires, their resistance drops nothing. That is the whole idea of four-terminal (Kelvin) measurement and of remote sensing.

## 3. Theory

### 3.1 The voltmeter and loading error

Model a voltmeter as an ideal voltage sensor in parallel with its input resistance $R_{in}$ (Ω). Connected to a circuit whose Thévenin equivalent at the two nodes is $V_{th}$ (V) behind $R_{th}$ (Ω), it forms a divider (06-03) and reads

$$
V_m = V_{th}\,\frac{R_{in}}{R_{th} + R_{in}}.
$$

The relative **loading error** is

$$
\varepsilon_V = \frac{V_m - V_{th}}{V_{th}} = -\frac{R_{th}}{R_{th} + R_{in}} \approx -\frac{R_{th}}{R_{in}} \quad (R_{th} \ll R_{in}).
$$

Two consequences follow. First, the error depends only on the *ratio* of resistances, so the question "is my meter good enough?" is answered by finding $R_{th}$ at the measurement point (06-08). Second, because the error is deterministic, a reading can be corrected exactly when $R_{th}$ and $R_{in}$ are known:

$$
V_{th} = V_m\Bigl(1 + \frac{R_{th}}{R_{in}}\Bigr).
$$

A typical handheld multimeter presents about 10 MΩ on its DC voltage ranges; the original Fluke 87's manual states "approximately 10 MΩ in parallel with less than 100 pF" and that the loading error is "negligible (0.1% or less)" when the source resistance is 10 kΩ or less, which is just $R_{th}/R_{in}$ = 10 kΩ/10 MΩ ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)). Precision bench meters offer a high-impedance mode, above 10 GΩ, on their low ranges (Section 7).

When $R_{th}$ is unknown, two readings with different input resistances determine both unknowns, exactly as the two-load method of 06-08 did (Problem 06-11.4). Loading also makes measurements look inconsistent: three equal high-value resistors across a battery each read less than a third of its voltage, so the three readings do not add up to the total (Problem 06-11.12). KVL is not violated; each reading was taken on a different circuit.

### 3.2 The ammeter and burden voltage

Model an ammeter as an ideal current sensor in series with its internal resistance $R_A$ (Ω): the shunt resistor it measures across, plus its fuse, switch contacts and test leads. Breaking a branch to insert it adds $R_A$ to that branch. If the rest of the circuit, seen from the break, has Thévenin equivalent $V_{th}$ and $R_{th}$, the current without the meter is $I_0 = V_{th}/R_{th}$ and with it

$$
I_m = \frac{V_{th}}{R_{th} + R_A} = \frac{I_0}{1 + R_A/R_{th}},
\qquad
\varepsilon_I \approx -\frac{R_A}{R_{th}}.
$$

The voltage the meter drops, $I_mR_A$, is its **burden voltage**. It is the ammeter's mirror image of loading: good ammeters have small burden voltages, and the error is again a resistance ratio, now the meter's over the circuit's. The correction is $I_0 = I_m(1 + R_A/R_{th})$. Multimeters provide several current inputs because a single shunt cannot serve all currents: a shunt large enough to give a measurable voltage at microamps would drop volts at amps.

### 3.3 Accuracy specifications and uncertainty

A meter's datasheet states its accuracy as a band around the reading, valid for stated conditions: a temperature range, a time since calibration and often a humidity limit (the original Fluke 87's manual, for example, specifies 18 °C to 28 °C and one year after calibration, [R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)). Two forms are common:

$$
\pm(\text{a}\%\ \text{of reading} + n\ \text{counts})
\qquad\text{or}\qquad
\pm(\text{a}\%\ \text{of reading} + \text{b}\%\ \text{of range}),
$$

where a **count** is one unit of the least significant displayed digit on the range in use. The first term scales with the reading (a gain error); the second is fixed for the range (an offset). The fixed term is why **range matters**: the same meter that is 0.08% uncertain at 3.3 V is 0.38% uncertain at 0.3 V on the same range, and 0.08% again on a range ten times more sensitive (Example 06-11.3). Two related words are often confused:

- **Resolution** is the smallest change the display can show (one count).
- **Accuracy** is how far the reading may be from the true value. A 6½-digit display does not make a reading accurate to 6½ digits.

When a result combines several measured quantities, their errors combine as 06-07 showed. For a product or quotient such as $P = VI$ or $R = V/I$, relative errors add to first order: worst case $|\varepsilon_P| \le |\varepsilon_V| + |\varepsilon_I|$, while for independent errors the root-sum-square $\sqrt{\varepsilon_V^2 + \varepsilon_I^2}$ is a more realistic typical figure (with the caveat from 06-07 that the RSS of uniform limits is exceeded by a few percent of units).

> **Math refresher — relative error of a product.** If $P = VI$ and the measurements are $V(1 + \varepsilon_V)$ and $I(1 + \varepsilon_I)$, then the computed product is $VI(1 + \varepsilon_V)(1 + \varepsilon_I) = VI(1 + \varepsilon_V + \varepsilon_I + \varepsilon_V\varepsilon_I)$. With errors of a fraction of a percent, the cross term is negligible (0.1% × 0.5% = 0.0005%), so relative errors add. For a quotient $V/I$, $1/(1 + \varepsilon_I) \approx 1 - \varepsilon_I$, and the relative errors subtract, which in a worst case is the same as adding their magnitudes.

### 3.4 Four-terminal (Kelvin) measurement

A two-wire ohmmeter forces a known current $I$ through the leads and the resistor and measures the voltage at its own terminals. It therefore reads the resistor plus both leads and both contacts:

$$
R_{2w} = R + 2R_{lead} + 2R_{contact}.
$$

Test leads are typically tens of milliohms each and contacts vary from milliohms to more, so a two-wire reading of a 1 Ω resistor can be 10% or more high (Example 06-11.4), and of a 10 mΩ shunt, many times too high. Shorting the leads and subtracting (the "relative" or "null" function) removes the lead resistance but not the contact resistance, which changes every time the probes are placed.

A four-wire measurement uses one pair of leads to **force** the current and a second pair, connected at the resistor's own terminals, to **sense** the voltage (Figure 2). The force leads' resistance does not matter, because a current source delivers $I$ whatever resistance is in series. The sense leads carry only the voltmeter's input current, $V/(R_{in} + 2R_{lead})$, so their drop is negligible. To see how small the residual is, let the voltmeter of input resistance $R_{in}$ sense through two leads of total resistance $R_s$. The voltmeter's branch, $R_{in} + R_s$, is in parallel with $R$ and takes a little of the forced current, and the leads drop a little of the voltage. The reading $V_m/I$ is

$$
R_{4w} = \frac{R\,(R_{in} + R_s)}{R + R_{in} + R_s}\cdot\frac{R_{in}}{R_{in} + R_s} = \frac{R\,R_{in}}{R + R_{in} + R_s} \approx R\Bigl(1 - \frac{R + R_s}{R_{in}}\Bigr),
$$

a relative error of about $(R + R_s)/R_{in}$: parts per billion for ohm-level resistors and a 10 MΩ input.

![Two-wire measurement reading R + 2R_lead, and four-wire measurement with force leads carrying the current I and separate sense leads, connected at the resistor's terminals, carrying almost none](../../../assets/figures/06-11/four-wire.svg)

*Figure 2. Two-wire versus four-wire (Kelvin) resistance measurement. The sense leads attach at the resistor itself, inside the force connections.*

The same principle governs **current shunts** on circuit boards. A shunt of resistance $R_{sh}$ converts current to voltage, $v = iR_{sh}$; the measurement is only as good as the definition of where that voltage is taken. A four-terminal shunt has separate current pads and sense pads, and the sense traces leave from the sense pads as a pair that carries no current. If instead the sense traces tap the current-carrying copper outside the resistive element, the copper and solder in the current path between the taps add to $R_{sh}$, with copper's large temperature coefficient (+0.393 %/°C, 06-02). At milliohm values this can dominate both the value and its drift (Example 06-11.5).

> **Going deeper — why low-value shunts have worse TCR.** The resistive element of a metal-strip shunt is an alloy (nickel-chrome or manganese-copper) with a temperature coefficient below about 20 ppm/°C, yet one four-terminal family is specified at ±35 ppm/°C from 5 mΩ upward but ±350 ppm/°C at 0.5–0.99 mΩ ([R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)). A plausible explanation (our inference; the datasheet does not give one) is that the copper terminations, at about 3900 ppm/°C, are a fixed small resistance in series, which becomes a larger fraction of the total as the element shrinks. The same arithmetic explains Example 06-11.5.

### 3.5 Wires, traces and remote sensing

**Resistance of wires and traces.** A conductor of length $L$ (m), cross-section $A$ (m²) and resistivity $\rho$ (Ω·m) has $R = \rho L/A$, rising with temperature as $R(T) = R_0\,[1 + \alpha(T - T_0)]$ (06-02). For copper, $\rho$ = 1.7241 × 10⁻⁸ Ω·m and $\alpha$ = 0.00393 /°C at 20 °C. A board trace of thickness $t$ has sheet resistance $R_\square = \rho/t$, about 0.49 mΩ per square for 1 oz copper (35 µm), so a trace of length $L$ and width $W$ has $R = R_\square L/W$ (06-02). A TI layout note gives the handy figure of about 1 mΩ per centimeter of length for a 0.5 cm wide trace in 1 oz copper, which is just two squares per centimeter at 0.49 mΩ/□ ([R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)).

Round wire is sized by gauge. The American Wire Gauge defines the diameter of gauge $n$ as

$$
d_n = 0.127\ \text{mm}\times92^{(36 - n)/39},
$$

so every 6 gauges halve the diameter and every 3 gauges roughly halve the area ([R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)). A 16 AWG wire is 1.291 mm in diameter and has 13.17 mΩ per meter (Example 06-11.6).

**Remote sensing.** A supply that regulates the voltage at its own terminals delivers that voltage minus the drop in the wires to the load, $I(R_{w+} + R_{w-})$. Remote sensing applies Section 3.4's idea to regulation. Two extra wires connect the supply's sense inputs to the load's terminals, and the supply's feedback loop (06-10) regulates the voltage *there*:

$$
v_{load} = V_{set}, \qquad v_{supply} = V_{set} + I\,(R_{w+} + R_{w-}).
$$

The sense wires carry only the sense inputs' small current, so they drop almost nothing. The supply's output rises by the cable drop, which it must have the headroom to deliver (supplies specify how much lead drop they can compensate), and the cable still dissipates $I^2(R_{w+} + R_{w-})$.

![A supply with output terminals and sense terminals; force wires R_w+ and R_w- carry the load current I to the load, and separate sense wires from the load terminals return to the supply's sense inputs, so the feedback loop regulates the voltage at the load](../../../assets/figures/06-11/remote-sense.svg)

*Figure 3. Remote sensing: the supply regulates the voltage where the sense wires attach, at the load, and raises its own output by the drop in the force wires.*

**Shared returns.** When two circuits share a return conductor, one circuit's current develops a voltage in the shared resistance that appears in the other's signal: common-impedance coupling (06-05). A 3 A motor current in a 20 mΩ shared ground is 60 mV of error in a sensor signal referenced to the far end (Problem 06-11.7). The cures are the ones of this chapter: separate return paths (a star ground), and differential or Kelvin sensing of the signal at its source.

### 3.6 Worst-case analysis of a measurement chain

A real measurement passes through several stages, each with its own errors: a sensor, a divider or shunt, wiring, an amplifier and a converter. The procedure is the error budget of 06-07 and 06-10:

1. Write the measured quantity as a function of every component value, including the instrument's resistances.
2. Separate **systematic** errors that are known and can be corrected (loading by a known input resistance, nominal lead resistance) from **uncertain** errors bounded by tolerances (resistor tolerance, TCR, meter accuracy).
3. Correct the systematic errors in the calculation or by calibration.
4. Bound the uncertain errors by worst case (every error at its limit, in the unfavorable direction) and, where the errors are independent and a statistical statement is acceptable, estimate the typical spread by RSS or Monte Carlo.

Problem 06-11.9 applies this to a 48 V bus monitor: two 1% resistors alone give almost ±1.9% worst case, the converter's input resistance a 0.9% systematic error, and 0.1% resistors cut the total to about ±0.7%.

## 4. Worked examples

### Example 06-11.1 · Loading a high-resistance divider (tier A)

**Setup.** A 10 V source drives a divider of two 1 MΩ resistors. The midpoint is measured with (a) a handheld meter with 10 MΩ input resistance and (b) a bench meter in its high-impedance mode, 10 GΩ. Find each reading and its error, and correct reading (a).

**Solution.** At the midpoint, $V_{th} = 5$ V and $R_{th} = 1\ \text{MΩ}\parallel1\ \text{MΩ} = $ **500 kΩ**.

(a) $V_m = 5\times10/(0.5 + 10) = $ **4.762 V**, an error of $-0.5/10.5 = $ **−4.76%**.

(b) $V_m = 5\times10{,}000/(0.5 + 10{,}000) = $ **4.99975 V**, an error of **−50 ppm**.

Correction of (a): $4.7619\times(1 + 0.5/10) = $ **5.000 V**.

**Units check.** MΩ/MΩ is dimensionless; V × ratio = V ✓.

**Sanity check.** The rule of thumb $-R_{th}/R_{in}$ gives −5% for (a) and −50 ppm for (b), both close to the exact values; the approximation is good when the ratio is small ✓.

### Example 06-11.2 · Ammeter burden on a low-voltage rail (tier B)

**Setup.** A 3.3 V rail supplies a 33 Ω load. A multimeter is inserted to measure the current, first on its milliamp input, whose internal resistance (shunt, fuse and leads) is 1.8 Ω, then on its amp input, 0.05 Ω. Find the current without the meter, the reading and burden voltage on each input, and correct the milliamp reading.

**Solution.** Without the meter, $I_0 = 3.3/33 = $ **100 mA**.

Milliamp input: $I_m = 3.3/(33 + 1.8) = $ **94.83 mA**, an error of **−5.17%**; the burden voltage is $94.83\ \text{mA}\times1.8\ \Omega = $ **170.7 mV**.

Amp input: $I_m = 3.3/33.05 = $ **99.85 mA**, burden **4.99 mV**.

Correction: $94.83\times(1 + 1.8/33) = $ **100.0 mA**.

**Units check.** V/Ω = A; A × Ω = V ✓.

**Sanity check.** The error is about $-R_A/R_{th} = -1.8/33 = -5.5\%$, close to the exact −5.17%. The milliamp input's higher resolution is useless here: its burden changes the current by more than the reading's precision. On a 3.3 V rail, 171 mV of burden could also push a digital circuit below its minimum supply voltage ✓.

### Example 06-11.3 · Reading an accuracy specification (tier B)

**Setup.** A handheld meter's DC voltage accuracy is ±(0.05% + 1), the headline specification of the Fluke 87V ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)). Real meters often specify their most sensitive range differently, so read the per-range table; here, assume a meter with this specification on every range. Find the uncertainty of (a) a 3.300 V reading on a range with 1 mV resolution; (b) a 0.300 V reading on the same range; (c) a 0.3000 V reading on a range with 0.1 mV resolution. (d) A power $P = VI$ is computed from reading (a) and a current measured to ±0.5%. Find the worst-case and RSS uncertainty of $P$.

**Solution.** One count is the resolution of the range in use.

(a) $0.0005\times3.300 + 0.001 = $ **±2.65 mV**, or **0.080%** of the reading.

(b) $0.0005\times0.300 + 0.001 = $ **±1.15 mV**, or **0.38%**: the fixed count now dominates.

(c) $0.0005\times0.3000 + 0.0001 = $ **±0.25 mV**, or **0.083%**.

(d) Worst case $0.080\% + 0.5\% = $ **0.58%**; RSS $\sqrt{0.080^2 + 0.5^2}\,\% = $ **0.51%**.

**Units check.** % of V + V = V; relative errors are dimensionless ✓.

**Sanity check.** The "0.05%" headline holds only near full scale; low on a range, the count term dominates. Choose the most sensitive range that does not overload. In (d) the current error dominates both combinations, so improving the voltmeter would not help ✓.

### Example 06-11.4 · Two-wire versus four-wire resistance (tier B)

**Setup.** A 1.000 Ω resistor is measured with leads and contacts totalling 0.08 Ω on each side. (a) What does a two-wire ohmmeter read? (b) A four-wire measurement forces 10 mA and senses with a 10 MΩ voltmeter through sense leads of 0.08 Ω each. Find the sensed voltage and the reading, and the relative error.

**Solution.** (a) $R_{2w} = 1 + 2\times0.08 = $ **1.16 Ω**, **16%** high.

(b) From Section 3.4 with $R_s$ = 0.16 Ω: the sensed voltage is $10\ \text{mA}\times R_{4w}$, with $R_{4w} = 1\times10^7/(1 + 10^7 + 0.16) = $ **1.0000 Ω**, so the sensed voltage is **10.00 mV**. The relative error is $-(1 + 0.16)/10^7$, **−0.12 ppm**.

**Units check.** Ω·Ω/Ω = Ω ✓.

**Sanity check.** The sense leads carry $10\ \text{mV}/10\ \text{MΩ} = 1$ nA, which drops 0.16 nV in 0.16 Ω: nothing. Four-wire removes the leads and the contacts, which a lead-nulling two-wire measurement cannot ✓.

### Example 06-11.5 · A milliohm shunt with and without Kelvin connections (tier C)

**Setup.** A 1 mΩ four-terminal metal-strip shunt in a 2512 package measures a 20 A load current. Its datasheet gives ±250 ppm/°C for values from 1 to 2.9 mΩ and a 1.0 W rating at 70 °C ([R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)). (a) Find the sense voltage and dissipation. (b) A layout error taps the sense traces from the current-carrying copper, so that about a tenth of a square of 1 oz copper (0.05 mΩ) at each end is included between the taps. Find the measured resistance and the error if the firmware assumes 1 mΩ. (c) After a one-time calibration at 25 °C, the board heats by 50 °C. Find the worst-case drift with Kelvin connections and with the layout error, and the layout's effective temperature coefficient.

**Solution.** (a) $20\ \text{A}\times1\ \text{mΩ} = $ **20 mV**; $20^2\times0.001 = $ **0.4 W**, within the rating.

(b) $1 + 2\times0.05 = $ **1.1 mΩ**, so the reading is **10%** high.

(c) Kelvin: $250\ \text{ppm/°C}\times50\ \text{°C} = $ **1.25%** worst case. With the copper included, the resistance changes by $1\ \text{mΩ}\times250\times10^{-6}\times50 + 0.1\ \text{mΩ}\times0.00393\times50 = 12.5 + 19.65$ µΩ, which is **2.92%** of 1.1 mΩ: the copper's share is larger than the shunt's. The effective coefficient is $(0.25 + 0.393)\ \text{µΩ/°C}\,/\,1.1\ \text{mΩ} = $ **585 ppm/°C**.

**Units check.** A × mΩ = mV; A² × Ω = W; mΩ × (1/°C) × °C = mΩ ✓.

**Sanity check.** Calibration removes the 10% offset but not the drift. A tenth of a milliohm is invisible on a schematic and nearly impossible to measure with two wires, yet at this current it is a 2 mV error source with copper's temperature coefficient. This is why shunt datasheets show recommended Kelvin pad layouts ✓.

### Example 06-11.6 · Remote sensing over a cable (tier B)

**Setup.** A 12 V bench supply feeds an electronic load set to draw 10 A through 1.5 m of 16 AWG copper wire each way, at 20 °C. Find (a) the wire's diameter and resistance per meter, (b) the round-trip resistance, the load voltage and the cable's dissipation without remote sensing, and (c) the supply's output voltage with remote sensing.

**Solution.** (a) $d = 0.127\times92^{20/39} = $ **1.291 mm**, so $A = \pi d^2/4 = 1.309\ \text{mm}^2$ and $\rho/A = 1.7241\times10^{-8}/1.309\times10^{-6} = $ **13.17 mΩ/m**.

(b) Round trip 3 m: **39.52 mΩ**. Load voltage $12 - 10\times0.03952 = $ **11.605 V** (3.3% low); cable dissipation $10^2\times0.03952 = $ **3.95 W**.

(c) The supply regulates the load at 12.000 V and its output rises to $12 + 0.395 = $ **12.395 V**.

**Units check.** Ω·m/m² = Ω/m; A × Ω = V; A² × Ω = W ✓.

**Sanity check.** At 3.95 W the cable is warm, and its resistance rises 0.39% per °C, so without sensing the load voltage would sag further as it heats; with sensing the supply tracks the change. The sense wires carry microamps or less, so they can be thin ✓.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 06-11.1a | Thévenin resistance at the midpoint | 500 | kΩ |
| Ex 06-11.1b | reading with 10 MΩ | 4.762 | V |
| Ex 06-11.1c | error with 10 MΩ | −4.76 | % |
| Ex 06-11.1d | reading with 10 GΩ | 4.99975 | V |
| Ex 06-11.1e | error with 10 GΩ | −50 | ppm |
| Ex 06-11.1f | corrected reading | 5.000 | V |
| Ex 06-11.2a | current without the meter | 100 | mA |
| Ex 06-11.2b | reading on the milliamp input | 94.83 | mA |
| Ex 06-11.2c | error on the milliamp input | −5.17 | % |
| Ex 06-11.2d | burden voltage, milliamp input | 170.7 | mV |
| Ex 06-11.2e | reading on the amp input | 99.85 | mA |
| Ex 06-11.2f | burden voltage, amp input | 4.99 | mV |
| Ex 06-11.2g | corrected milliamp reading | 100.0 | mA |
| Ex 06-11.3a | uncertainty at 3.300 V | 2.65 | mV |
| Ex 06-11.3b | relative uncertainty at 3.300 V | 0.080 | % |
| Ex 06-11.3c | uncertainty at 0.300 V | 1.15 | mV |
| Ex 06-11.3d | relative uncertainty at 0.300 V | 0.38 | % |
| Ex 06-11.3e | uncertainty at 0.3000 V on the sensitive range | 0.25 | mV |
| Ex 06-11.3f | relative uncertainty on the sensitive range | 0.083 | % |
| Ex 06-11.3g | power uncertainty, worst case | 0.58 | % |
| Ex 06-11.3h | power uncertainty, RSS | 0.51 | % |
| Ex 06-11.4a | two-wire reading | 1.16 | Ω |
| Ex 06-11.4b | two-wire error | 16 | % |
| Ex 06-11.4c | four-wire reading | 1.0000 | Ω |
| Ex 06-11.4d | sensed voltage | 10.00 | mV |
| Ex 06-11.4e | four-wire error | −0.12 | ppm |
| Ex 06-11.5a | sense voltage | 20 | mV |
| Ex 06-11.5b | shunt dissipation | 0.4 | W |
| Ex 06-11.5c | resistance between misplaced taps | 1.1 | mΩ |
| Ex 06-11.5d | error from the misplaced taps | 10 | % |
| Ex 06-11.5e | worst-case drift, Kelvin | 1.25 | % |
| Ex 06-11.5f | worst-case drift, misplaced taps | 2.92 | % |
| Ex 06-11.5g | effective temperature coefficient | 585 | ppm/°C |
| Ex 06-11.6a | 16 AWG diameter | 1.291 | mm |
| Ex 06-11.6b | resistance per meter | 13.17 | mΩ/m |
| Ex 06-11.6c | round-trip resistance | 39.52 | mΩ |
| Ex 06-11.6d | load voltage without sensing | 11.605 | V |
| Ex 06-11.6e | cable dissipation | 3.95 | W |
| Ex 06-11.6f | supply output with sensing | 12.395 | V |

## 5. Simulate it

Open [labs/06-11-lab/](../labs/06-11-lab/README.md): a notebook and an ngspice netlist that models each instrument as the resistor it is.

1. **Loading curves.** Plot the loading error against source resistance for 10 MΩ and 10 GΩ meters, and check Example 06-11.1 in ngspice. *Predict first:* at what source resistance does a 10 MΩ meter read 1% low?
2. **Range choice.** Plot the relative uncertainty of a ±(0.05% + 1) meter across three ranges. *Predict first:* where on each range is the relative uncertainty worst?
3. **Kelvin versus misplaced taps over temperature.** Sweep the board temperature in ngspice (resistors with temperature coefficients) and compare the two connections of Example 06-11.5. *Predict first:* at what temperature rise does the misplaced-tap drift reach 5%?
4. **A measurement chain by Monte Carlo.** Simulate many 48 V bus monitors built from 1% resistors and a ±0.5% converter (Problem 06-11.9). *Predict first:* what fraction of units exceeds ±1.5%?

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Higher voltmeter input resistance | Lower loading error | Higher sensitivity to leakage and pickup; slower settling with cable capacitance | Test engineer |
| Larger current shunt | Larger signal, smaller amplifier error | $I^2R$ loss, heating (and TCR drift), voltage lost to the load | Power or system designer |
| Smaller current shunt | Lower loss and burden | Smaller signal; worse TCR at the lowest values; layout copper matters more | Power or system designer |
| Four-terminal shunt and Kelvin layout | Removes copper and solder from the measurement | Extra pads and routing, a slightly more expensive part | Board designer |
| Remote sensing | Exact voltage at the load | Two more wires, supply headroom, loop stability with long leads | System designer |
| Higher-accuracy meter or calibration | Smaller uncertainty | Cost, calibration interval, slower readings | Test or quality engineer |
| Thicker copper or wider traces | Lower drop and heating | Board cost, area, finer-pitch routing limits | Board designer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Loading error of a voltmeter | $\approx -R_{th}/R_{in}$ | ammeter: $\approx -R_A/R_{th}$ |
| Handheld DMM input resistance | ≈ 10 MΩ ∥ < 100 pF | original Fluke 87 manual ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)) |
| Bench DMM high-impedance mode | > 10 GΩ on the 100 mV to 10 V ranges | Keysight 34465A, search excerpts ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)) |
| Handheld DMM DC accuracy | ±(0.05% + 1 count) | Fluke 87V, as of Nov 2026 ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)) |
| 6½-digit bench DMM, basic DC accuracy | about 30 ppm, 1 year | Keysight 34465A, search excerpts ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)) |
| Copper | 1.7241 µΩ·cm, +0.393%/°C at 20 °C | IACS (06-02) |
| 1 oz PCB copper | 35 µm, ≈ 0.49 mΩ/□; 0.5 cm wide trace ≈ 1 mΩ/cm | TI SNVA054C ([R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)) |
| 16 AWG copper wire | 1.291 mm, 13.17 mΩ/m at 20 °C | AWG formula (Example 06-11.6) |
| Four-terminal shunt (Vishay WSK2512) | 0.5 mΩ to 0.2 Ω; ±0.1% to ±1%; ±35 to ±350 ppm/°C by value; 1 W at 70 °C | datasheet, Dec 2023 ([R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)) |

## 8. Common mistakes

1. **Trusting a voltmeter on a high-resistance node** (dividers of megohms, a sensor's high-impedance output, a floating input). Estimate $R_{th}/R_{in}$ first.
2. **Measuring current with the milliamp input on a low-voltage circuit** and not noticing that the burden voltage changed the current, or starved the circuit.
3. **Confusing resolution with accuracy.** Extra digits show noise and drift; the specification says how many to believe.
4. **Quoting "% of reading" alone** and forgetting the count or range term, which dominates at the bottom of a range.
5. **Two-wire measurements of small resistances.** Leads and contacts are tens of milliohms; anything below an ohm needs four wires.
6. **Sense traces that share copper with the current path.** A Kelvin part laid out without Kelvin routing is a two-terminal part.
7. **Ignoring copper's temperature coefficient,** 0.39% per °C, in wires, traces and pads that carry current.
8. **Adding errors without separating systematic from random ones.** Correct what is known (loading, nominal lead resistance) before bounding what is not.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Handheld meters:** Fluke's 87V industrial multimeter specifies DC voltage accuracy of ±(0.05% + 1) ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications), Fluke product page) **[Established]**. The original Fluke 87's manual (rev. 1997) specifies about 10 MΩ ∥ < 100 pF on its voltage ranges and a > 4000 MΩ high-impedance mode on its 400 mV range **[Established]** for that model; the 87V's own input-impedance figure was not confirmed from a primary source.
- **Bench meters:** Keysight's 34465A 6½-digit meter is reported at 30 ppm basic one-year DC voltage accuracy, with input resistance selectable between 10 MΩ and more than 10 GΩ on its 100 mV to 10 V ranges ([R-108](../../../reference/research-log.md#r-108--digital-multimeter-specifications)) **[Industry estimate]** (Keysight's documents could not be opened; figures are from search excerpts).
- **Current shunts:** four-terminal metal-strip shunts in a 2512 package reach 0.5 mΩ at ±1% and 1 mΩ at ±0.5%, rated 1.0 W at 70 °C; their temperature coefficient is banded by value from ±35 ppm/°C (5 mΩ to 0.2 Ω) to ±350 ppm/°C (0.5 to 0.99 mΩ), and the element alloy is below 20 ppm/°C (Vishay WSK2512, datasheet revision Dec 2023, [R-109](../../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)) **[Established]**.

### Why it matters commercially

Measurement accuracy is a product feature with a price. A battery's state-of-charge display, an electricity meter's revenue (accuracy classes in [R-028](../../../reference/research-log.md#r-028--electricity-meter-accuracy-classes-iec-62053-21)), a server power supply's telemetry and a motor drive's torque control all rest on a current measurement whose error budget is set by a shunt, its layout and an amplifier. In datacenters, the drop between a power supply and a processor's die is managed by remote sensing and by delivering power at higher voltage and lower current (Course 22, [22-10](../../22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)). In chip production, test time and contact reliability (four-wire contacts on probe cards and sockets) are a real part of a chip's cost.

### Marketing vs Reality

- **"0.05% accuracy."** *Reality:* plus counts, on the best range, near full scale, within a temperature band and calibration interval. At 10% of range the same meter may be several times worse (Example 06-11.3).
- **"6½ digits."** *Reality:* that is resolution. Accuracy is in the specification table, and the last digits often show noise unless the integration time is long.
- **"1 mΩ shunt, ±1%."** *Reality:* measured at its Kelvin terminals at 25 °C. The board's copper, the solder and the temperature rise decide what the system actually sees (Example 06-11.5).
- **"Our supply holds 12.000 V."** *Reality:* at its terminals. Ask what the load sees at full current, and whether remote sensing is used.

### Questions for engineering leaders

1. **"What is the total uncertainty of this measurement, and what dominates it?"** *Strong:* a budget with each term, its source (datasheet, calibration) and whether it is systematic or random. *Evasive:* "the meter is 0.05%".
2. **"What resistance does your instrument see at that node?"** *Strong:* the Thévenin resistance and the resulting loading error, or the reason it is negligible. *Evasive:* "the meter is high impedance".
3. **"How is current sensed, and how did you lay out the shunt?"** *Strong:* four-terminal part, Kelvin routing to the amplifier, TCR and self-heating in the budget, calibration plan. *Evasive:* a value and a tolerance only.
4. **"Where is the voltage regulated: at the supply or at the load?"** *Strong:* remote sense or point-of-load regulation, with the drop budget at maximum current and temperature. *Evasive:* "the supply is set correctly".
5. **"How do you know the test fixture is not the error?"** *Strong:* four-wire contacts, fixture compensation, golden units and gauge repeatability studies. *Evasive:* "the tester is calibrated".

## 10. Concept check

1. A 10 MΩ meter measures a node whose Thévenin resistance is 100 kΩ. About how far off is the reading?

   <details><summary>Answer</summary>

   About $-R_{th}/R_{in} = -1\%$ (exactly −0.99%).

   </details>

2. Why does an ammeter with higher resolution sometimes give a *less* accurate reading of a circuit's current?

   <details><summary>Answer</summary>

   Its more sensitive range uses a larger shunt, and the larger burden voltage changes the current being measured. The error is about $-R_A/R_{th}$, whatever the display shows.

   </details>

3. A meter specified at ±(0.1% + 2 counts) reads 1.000 V on a range with 1 mV resolution. What is the uncertainty?

   <details><summary>Answer</summary>

   $0.001\times1.000 + 2\times0.001 = $ ±3 mV, or 0.3%.

   </details>

4. Why does a four-wire measurement not care about the resistance of the force leads?

   <details><summary>Answer</summary>

   The force leads carry the current from a current source, which delivers its set current whatever resistance is in series; the voltage is sensed at the resistor itself by leads that carry almost no current.

   </details>

5. A current shunt's sense traces leave from the same pads that carry the current. What two problems does that cause?

   <details><summary>Answer</summary>

   The copper and solder between the taps add to the measured resistance (an offset), and copper's +0.39%/°C temperature coefficient adds drift that calibration at one temperature cannot remove.

   </details>

6. A supply with remote sensing feeds a 5 A load through a 60 mΩ round-trip cable. What are the load and supply voltages if it is set to 5 V?

   <details><summary>Answer</summary>

   The load is at 5.0 V; the supply's output is $5 + 5\times0.06 = 5.3$ V.

   </details>

7. Three 1 MΩ resistors in series across 9 V are each measured with a 10 MΩ meter. Why do the readings not sum to 9 V?

   <details><summary>Answer</summary>

   Each reading is taken with the meter loading that resistor (Thévenin resistance 667 kΩ), so each reads about 2.81 V. KVL holds in every configuration; the three readings simply come from three different circuits.

   </details>

Problem set: [06-11 problems](../problems/06-11-problems.md) · [solutions](../solutions/06-11-solutions.md).

## 11. Key terms

[Loading effect](../../../reference/glossary.md#loading-effect) ·
[Burden voltage](../../../reference/glossary.md#burden-voltage) ·
[Meter accuracy specification](../../../reference/glossary.md#meter-accuracy-specification) ·
[Resolution (measurement)](../../../reference/glossary.md#resolution-measurement) ·
[Four-terminal (Kelvin) measurement](../../../reference/glossary.md#four-terminal-kelvin-measurement) ·
[Current-sense shunt](../../../reference/glossary.md#current-sense-shunt) ·
[Remote sensing](../../../reference/glossary.md#remote-sensing) ·
[Sheet resistance](../../../reference/glossary.md#sheet-resistance) ·
[Common-impedance coupling](../../../reference/glossary.md#common-impedance-coupling) ·
[Worst-case analysis](../../../reference/glossary.md#worst-case-analysis)

## 12. Connections

- **Previous:** [06-02](06-02-circuit-elements-and-ohms-law.md) (resistivity, sheet resistance and temperature coefficient); [06-07](06-07-linearity-and-superposition.md) (worst case and RSS); [06-08](06-08-thevenin-and-norton.md) (Thévenin resistance, which sets loading); [06-10](06-10-ideal-op-amp.md) (feedback, which remote sensing uses).
- **Next:** [07-01 Capacitors and Inductors](../../07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md), the first chapter of Circuit Analysis II, where measurements acquire time constants (a meter's input capacitance and a cable's inductance).
- **Used later:** data converters and their input loading ([20-06](../../20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md)); layout, matching and parasitic resistance ([20-11](../../20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md)); battery fuel gauging with shunts ([22-09](../../22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md)); power delivery and remote sensing in datacenters ([22-10](../../22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)).

## 13. Further study

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, the sections on measuring voltage and current and on the Wheatstone bridge in the chapter on simple resistive circuits.
- Horowitz, P. and Hill, W., *The Art of Electronics*, 3rd ed., chapter 1 (voltage dividers, input and output impedance) and the discussions of current sensing and remote sensing in the chapter on voltage regulation.
- Keithley Instruments (now Tektronix), *Low Level Measurements Handbook*, the sections on low-resistance (four-wire) measurement and on high-resistance sources.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 3, "Superposition, Thévenin and Norton", for the Thévenin view of loading that this chapter applies to instruments.

## 14. Sources

1. Nilsson and Riedel; Horowitz and Hill, ch. 1 and the chapter on voltage regulation.
2. Fluke 87V product specifications; Fluke 87 True RMS Multimeter Users Manual, PN 834192, rev. 8 (1997); Keysight 34465A specifications (search excerpts). [R-108]
3. Texas Instruments, AN-1229 *SIMPLE SWITCHER PCB Layout Guidelines*, SNVA054C (2013); Vishay Dale, WSK2512 datasheet, document 30108 (revision 11 Dec 2023); the AWG diameter definition (ASTM B258). [R-109]
4. Copper resistivity and temperature coefficient (IACS). [R-080], [R-101]
