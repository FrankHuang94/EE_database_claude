# Problems 07-03 · Second-Order RLC Transients

Chapter: [07-03](../chapters/07-03-second-order-rlc-transients.md) · Worked solutions: [07-03 solutions](../solutions/07-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention throughout. Switches are ideal and act at $t = 0$; "a long time" means DC steady state. Answers to 3 or 4 significant figures unless exact. Problems marked *(numerical)* need the lab notebook's state-space simulator or ngspice for one part.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-03.1 [A]

**Series RLC parameters.** A series RLC has $L$ = 2 mH, $C$ = 50 nF and $R$ = 150 Ω. Find $\omega_0$, $f_0$, $Z_0$, α, ζ, $Q$ and $\omega_d$, classify the response, and give the resistance for critical damping.

### Problem 07-03.2 [A]

**Parallel RLC parameters.** A parallel RLC has $L$ = 50 µH and $C$ = 200 nF. (a) Find $Z_0$ and the resistance for critical damping. (b) With $R$ = 50 Ω, find ζ, $Q$, α and $\omega_0$. (c) Should $R$ be made larger or smaller to reduce the ringing?

### Problem 07-03.3 [A]

**Initial conditions.** A series loop contains a 10 V source, $R$ = 20 Ω, $L$ = 5 mH and $C$ = 2 µF. Before $t = 0$ the source is disconnected (a switch in the loop is open), the capacitor holds 4 V and no current flows. The switch closes at $t = 0$. Find $i(0^+)$, $di/dt(0^+)$, $v_C(0^+)$, $dv_C/dt(0^+)$, $v_L(0^+)$, $v_R(0^+)$ and $dv_R/dt(0^+)$, and the final values $v_C(\infty)$ and $i(\infty)$.

### Problem 07-03.4 [B]

**A pulse discharge.** A 10 µF capacitor charged to 100 V is discharged at $t = 0$ through a series loop of $L$ = 1 mH and $R$ = 2 Ω (the core of a pulsed-power or flash circuit). (a) Find α, $\omega_d$, ζ and $Z_0$. (b) Write $i(t)$. (c) Find the peak current and when it occurs. (d) Find the capacitor voltage when the current first returns to zero, and the fraction of the energy still stored then. (e) Why do pulse-discharge capacitors carry a "voltage reversal" rating?

### Problem 07-03.5 [B]

**Designing for critical damping.** A series RLC with $L$ = 10 µH and $C$ = 1 µF is driven by a 1 V step from rest. (a) Find the resistance for critical damping. (b) With that resistance, find the time for $v_C$ to reach 90% of its final value. (c) The resistance is doubled (ζ = 2). Find the new 90% time and the ratio to (b). What does heavy damping cost?

### Problem 07-03.6 [B]

**A current step into a parallel RLC.** A current source steps from 0 to 2 mA at $t = 0$ into a parallel combination of $R$ = 2 kΩ, $L$ = 10 mH and $C$ = 10 nF, all at rest. (a) Find $\omega_0$, $Z_0$, ζ and α. (b) Show that the inductor current obeys the standard all-pole step response, and find its peak and the time of the peak. (c) Find the peak of the voltage $v$ across the tank, and when it occurs. (d) Compare (c) with the series-RLC result of chapter §3.7: what is the dual statement?

### Problem 07-03.7 [B]

**A switched circuit.** A 12 V source feeds node a through $R_1$ = 2 Ω in series with $L$ = 0.5 mH. From node a to ground are $C$ = 50 µF and, through a switch, $R_2$ = 4 Ω. The circuit has been in steady state with the switch closed. At $t = 0$ the switch opens, disconnecting $R_2$. (a) Find $i_L(0^-)$ and $v_C(0^-)$. (b) Identify the circuit for $t > 0$ and find α, $\omega_0$, ζ and $\omega_d$. (c) Find $v_C(0^+)$, $dv_C/dt(0^+)$ and $v_C(\infty)$. (d) Write $v_C(t)$ and evaluate it at 0.5 ms. (e) Find the peak value of $v_C$ and when it occurs.

### Problem 07-03.8 [B]

**State variables, and a variable with a zero.** An 11 V step is applied at $t = 0$ to this circuit, at rest: the source feeds node a through $R_1$ = 100 Ω; from node a to ground is $C$ = 1 µF; also from node a to ground is $L$ = 10 mH in series with $R_2$ = 10 Ω. (a) With $\mathbf{x} = (v, i_L)$, $v$ the voltage at node a, write the state equations and the matrix $\mathbf{A}$. (b) Find α, $\omega_0$, ζ and $\omega_d$. (c) Find the final values of $v$ and $i_L$, and $dv/dt(0^+)$. (d) Write $v(t)$ and find its peak and when it occurs. (e) Compare the peak with what the 02-03 overshoot formula would predict for this ζ, and explain the difference.

### Problem 07-03.9 [B]

**An unequal RC ladder.** A step drives $R_1$ = 1 kΩ to node 1 ($C_1$ = 2 µF to ground), then $R_2$ = 2 kΩ to node 2 ($C_2$ = 0.5 µF to ground). (a) Write $\mathbf{A}$ and find its roots and ζ. (b) Check that the sum of the time constants equals $R_1(C_1 + C_2) + R_2C_2$. (c) Prove that for **any** positive $R_1$, $R_2$, $C_1$, $C_2$ this circuit is overdamped.

### Problem 07-03.10 [B]

**Measuring a parasitic tank, then snubbing it.** A switch node rings at 120 MHz. A 470 pF capacitor added across the switch lowers the ringing to 60 MHz. (a) Find the parasitic capacitance $C$, the loop inductance $L$ and $Z_0$. (b) Choose a snubber with $R_d \approx Z_0$ and $C_d \approx 4C$, rounded to standard values (E12 resistors; 470 pF, 560 pF, 680 pF capacitors). (c) The converter switches 400 V at 100 kHz. Find the snubber's power. (d) Comment on whether this is acceptable, and what else a designer could do.

### Problem 07-03.11 [C] (design: hot-plug damping; numerical)

Example 07-03.3's input (12 V, cable $L$ = 1 µH and $R$ = 50 mΩ, a 10 µF ceramic capacitor) overshoots to 21.35 V. A 47 µF electrolytic capacitor with equivalent series resistance $R_b$ is added across the ceramic.

(a) Explain why the electrolytic acts as an RC damper, and state the rule of thumb for $R_b$ in terms of the original tank.
(b) Write the three state equations with $\mathbf{x} = (i_L, v_C, v_b)$, where $v_b$ is the voltage on the electrolytic's ideal capacitance.
(c) Using the lab notebook or ngspice, find the peak input voltage for $R_b$ = 0.1 Ω, 0.3 Ω and 1.0 Ω, and the time to settle within ±2% for $R_b$ = 0.3 Ω.
(d) Compare the best of these with the rule in (a), and explain why both too little and too much ESR damp poorly.
(e) A colleague proposes a 0.3 Ω resistor in series with the cable instead. Find the peak it gives (hand calculation), and its DC drop and power at a 2 A load. Which fix do you prefer?

### Problem 07-03.12 [B]

**Gate-loop ringing.** A gate driver steps from 0 to 12 V into a MOSFET whose input capacitance is $C_{iss}$ = 2 nF, through a loop inductance of 8 nH. The driver's output resistance plus the transistor's internal gate resistance total 1 Ω. (a) Find $Z_0$, ζ and the peak gate voltage. (b) What total resistance gives critical damping? (c) With critical damping, find the 10–90% rise time of the gate voltage. (d) The gate is rated ±20 V. Is the 1 Ω design safe, and what would you change?

### Problem 07-03.13 [C]

**Resonant charging.** A 400 V supply charges a 1 µF capacitor through a 10 mH inductor and a diode, which stops the current when it tries to reverse. Neglect resistance. (a) Starting from 0 V, find the capacitor's final voltage, the time to reach it and the peak current. (b) Repeat if the capacitor starts at −200 V (left over from a previous discharge). (c) Where does the energy come from, and why is this technique used to charge pulse-forming networks to more than the supply voltage?

### Problem 07-03.14 [B]

**Every variable of a step response.** A 5 V step is applied to a series RLC at rest with $R$ = 10 Ω, $L$ = 1 mH and $C$ = 1 µF. (a) Find $Z_0$, ζ, α and $\omega_d$. (b) Give the value at $0^+$ and the slope at $0^+$ of $v_C$, $i$, $v_L$ and $v_R$. (c) Find the peak current. (d) Find the most negative value of $v_L$ and when it occurs. (e) Why does $v_L$ go negative at all, when the source only pushes forward?

### Problem 07-03.15 [C]

**Negative damping: an oscillator starting up.** An amplifier presents a negative conductance $-g$ in parallel with a tank of $L$ = 1 µH, $C$ = 1 nF and a loss resistance $R$ = 10 kΩ. (a) Find $f_0$. (b) Write α for the combination and find it for $g$ = 0.2 mS. What does a negative α mean? (c) Find the time constant of the growth, and the time for an oscillation to grow from 1 mV to 1 V. About how many cycles is that? (d) What value of $g$ just sustains the oscillation, and what stops the growth in a real oscillator?

### Problem 07-03.16 [B]

**Is it the circuit or the probe?** A 10× passive probe has 10.8 pF of input capacitance (its 10 MΩ input resistance is negligible here) and a 6-inch ground lead of about 150 nH. It measures a fast edge from a 50 Ω source. Treat the source resistance, the ground lead and the probe capacitance as a series RLC driven by the edge. (a) Find $f_0$, $Z_0$ and ζ. (b) What overshoot does the probe itself add to an ideal step? (c) A ground spring cuts the inductance to 15 nH. Repeat (a) and (b). (d) Would a 100 MHz oscilloscope show the ringing of (a) clearly? A 500 MHz one? (e) Describe a quick bench test that tells probe ringing from circuit ringing.

---

## Objective coverage

| Learning objective (chapter 07-03) | Problems |
|---|---|
| 1. Derive the equation of series, parallel and general circuits; α, $\omega_0$, ζ, $Q$, $Z_0$ | 1, 2, 8, 9, 11, 15 |
| 2. Initial conditions $x(0^+)$, $\dot x(0^+)$ and final values | 3, 7, 8, 14 |
| 3. Natural and step responses in all three cases; peaks and zero crossings | 4, 5, 6, 7, 8, 13, 14 |
| 4. Reading and specifying ringing; when the formulas apply | 4, 6, 8, 12, 14, 16 |
| 5. Damping design; why RC circuits cannot ring | 5, 9, 10, 11, 12 |
| 6. Ringing in hardware and evaluating claims | 10, 11, 12, 13, 15, 16 |
