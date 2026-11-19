# Problems 10-01 · Diodes and Diode Circuits

Chapter: [10-01](../chapters/10-01-diodes-and-diode-circuits.md) · Worked solutions: [10-01 solutions](../solutions/10-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 300 K; $V_T$ = 25.852 mV; $n$ = 1 unless stated; the constant-drop model uses 0.7 V; 60 Hz mains. "Numerical" problems expect a short script (root finding or an ODE solver).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-01.1 [A]

**When does 0.7 V work?** A diode with $I_S$ = 10⁻¹⁴ A is in series with 1 kΩ. Find the current with the constant-drop model and exactly, and the constant-drop model's percentage error, for a supply of (a) 3 V and (b) 1 V. What does the comparison teach?

### Problem 10-01.2 [A]

**Diode logic.** Two inputs A and B each connect through a diode (anode at the input) to an output node with 10 kΩ to ground. (a) With A = 3.3 V and B = 0 V, find $V_O$, which diodes conduct, and the voltage across D_B. (b) With A = 3.3 V and B = 3.0 V, find $V_O$, D_B's forward voltage, and the fraction of D_A's current that D_B carries if both diodes are identical exponential diodes. (c) What logic function is this?

### Problem 10-01.3 [A]

**Small-signal resistance.** Find $r_d$ at 0.5 mA for a diode with $n$ = 1 and one with $n$ = 2, and the signal current each carries for a 1 mV peak signal across it.

### Problem 10-01.4 [A]

**Temperature.** A diode drops 0.650 V at 1 mA and 25 °C, with a coefficient of −2 mV/K. (a) Find its drop at 1 mA at 85 °C and at −40 °C. (b) Find $V_T\ln10$ at 85 °C. (c) If instead the diode were held at a fixed 0.650 V, by what factor would its current rise between 25 °C and 85 °C? What does this imply for biasing?

### Problem 10-01.5 [B]

**A half-wave supply.** A 10 V peak, 60 Hz source feeds a half-wave rectifier, a capacitor and a load drawing a constant 100 mA. (a) Find the peak output and the capacitance for 1 V of ripple. (b) With 2200 µF, find the ripple, the minimum output, the conduction angle and the peak diode current from §3.6. (c) Find the PIV.

### Problem 10-01.6 [B]

**Center tap or bridge?** A full-wave supply must deliver a 12 V peak at 1 A with 0.5 V of ripple, using 0.8 V diodes. (a) Find the capacitance. (b) For a center-tapped winding, find the peak of each half-winding and the PIV. (c) For a bridge, find the winding's peak and the PIV. (d) Which would you choose at 12 V, and which at 2 V output?

### Problem 10-01.7 [B]

**A 12 V Zener regulator.** A 1N4742A Zener (12 V at 21 mA, $Z_{ZT}$ = 9 Ω typical, $I_{ZM}$ = 76 mA, 1.3 W) regulates a 16–20 V supply for a 0–30 mA load, with $I_Z \ge$ 5 mA. Take $r_z$ = 9 Ω. (a) Find $V_{Z0}$ and $V_Z$ at 5 mA. (b) Find the largest $R$ and choose 110 Ω. (c) Find $V_O$ and $I_Z$ at 16 V and 30 mA. (d) Find the worst-case Zener current and power, and check them against the ratings. (e) Find the resistor's worst-case power.

### Problem 10-01.8 [B]

**Regulation.** For Problem 10-01.7's design, find (a) the line and load regulation and (b) the change in $V_O$ across the supply range at full load and across the load range at 18 V.

### Problem 10-01.9 [B]

**A biased clipper.** A 1 kΩ resistor feeds the output, which is shunted to ground by a diode (anode at the output) in series with a 2.0 V battery. (a) With the constant-drop model, find the clipping level and the output for inputs of 1 V and 5 V. (b) With the course diode ($I_S$ = 10⁻¹⁵ A), find the output for a 5 V input.

### Problem 10-01.10 [B]

**Clamp and doubler.** A 3 V peak, 1 kHz sine drives a clamp (cathode at the output) followed by a peak rectifier. (a) With 0.7 V diodes, find the clamped output's range and the doubler's output. (b) Repeat the doubler with 0.3 V Schottky diodes, and compare the losses.

### Problem 10-01.11 [B]

**Exact and iterative solutions (numerical).** For Problem 10-01.1(b), evaluate the Lambert W formula of §3.2 and confirm the current. Then find the contraction factor $V_T/RI_D$ of the fixed-point iteration for Problem 10-01.1(a) and (b), and explain the difference.

### Problem 10-01.12 [C]

**The exact half-wave ripple (numerical).** For Problem 10-01.5(b) (2200 µF, constant 100 mA load, ideal constant-drop diode), find exactly the turn-off angle after the peak, the peak-to-peak ripple, the conduction angle, the peak diode current and the average diode current during conduction. By what percentage does §3.6 overstate the ripple, and why?

### Problem 10-01.13 [B]

**Replacing an ORing diode.** A 3 A rail is ORed with an ideal-diode controller whose data sheet recommends $20\text{ mV}/I \le R_{DS(on)} \le 50\text{ mV}/I$ at the nominal current. (a) Find the range. (b) With 10 mΩ, compare the loss at 3 A with a 0.5 V Schottky and a 0.8 V PN diode. (c) In a 6 A overload, what are the MOSFET's drop and loss, and is the controller still regulating 20 mV?

### Problem 10-01.14 [B]

**ESD capacitance on a data line.** A 12 pF ESD diode loads a line driven from 50 Ω. (a) Find the RC time constant and the 3 dB bandwidth. (b) Find the 10–90% rise time, $2.2\tau$. (c) What fraction of a 400 Mbps bit period is that rise time?

---

## Objective coverage

| Learning objective (chapter 10-01) | Problems |
|---|---|
| 1. Solve diode circuits with the exponential and simpler models | 1, 4, 9, 11 |
| 2. Assumed-state method | 2, 9 |
| 3. Small-signal resistance and its limit | 3 |
| 4. Rectifiers, ripple, conduction, peak current and PIV | 5, 6, 12 |
| 5. Zener regulator design and regulation | 7, 8 |
| 6. Limiters, clamps, doublers and product context | 9, 10, 13, 14 |
