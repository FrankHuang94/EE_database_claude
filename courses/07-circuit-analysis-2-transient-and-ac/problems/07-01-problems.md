# Problems 07-01 · Capacitors and Inductors

Chapter: [07-01](../chapters/07-01-capacitors-and-inductors.md) · Worked solutions: [07-01 solutions](../solutions/07-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention throughout (current into the + terminal). Components are ideal unless parasitics are given. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-01.1 [A]

**A capacitor driven at 50 Hz.** The voltage across a 47 µF capacitor is $v(t) = 5\sin(2\pi\cdot50\,t)$ V. Find $i(t)$, its peak value, and the largest energy the capacitor stores.

### Problem 07-01.2 [A]

**An inductor charging.** The current in a 10 mH inductor is $i(t) = 2\bigl(1 - e^{-t/\tau}\bigr)$ A with $\tau$ = 1 ms, for $t \ge 0$. Find $v(t)$, its value at $t = 0^+$ and at $t$ = 1 ms, and the final stored energy.

### Problem 07-01.3 [A]

**The integral form.** A 100 µF capacitor starts at 2 V. It receives 10 mA for 30 ms, then −5 mA for the next 20 ms. Find its voltage at the end of each interval.

### Problem 07-01.4 [A]

**Combinations.** Find the equivalent of (a) a 2 mH inductor in series with the parallel pair 3 mH ∥ 6 mH; (b) a 3 µF capacitor in parallel with the series pair 6 µF and 3 µF.

### Problem 07-01.5 [B]

**A capacitive divider and its leakage.** A 1 µF and a 2 µF capacitor, both uncharged, are connected in series across a 9 V supply. (a) Find each capacitor's voltage just after connection. (b) Each capacitor has a 10 MΩ leakage resistance in parallel. What does each voltage settle to after a long time, and why?

### Problem 07-01.6 [B]

**Sharing charge.** A 4.7 µF capacitor charged to 12 V is connected to an uncharged 2.2 µF capacitor through a resistor. Find the final voltage, the energy before and after, and the energy lost. Does the loss depend on the resistor's value?

### Problem 07-01.7 [B]

**Volt-second balance in a buck converter.** A buck converter's 10 µH inductor sees $12 - 3.3 = 8.7$ V while its switch is on and −3.3 V while it is off, at 500 kHz. (a) Use volt-second balance to find the fraction of each period the switch is on (the duty cycle). (b) Find the on-time and the peak-to-peak ripple current.

### Problem 07-01.8 [B]

**A solenoid and its clamp.** A 50 mH solenoid carries 0.5 A. (a) If the current is forced to zero in 10 µs, what voltage develops? (b) How much energy must be absorbed? (c) A 30 V clamp (a TVS diode) holds the coil voltage at −30 V while the current falls. Ignoring the coil's resistance, how long does the current take to reach zero? Why do designers sometimes prefer this to a plain flyback diode?

### Problem 07-01.9 [C]

**Decoupling a processor rail.** A load step of 5 A arrives in 2 ns, and the regulator responds after 50 ns. The rail may droop by 30 mV from charge drawn and by 20 mV from inductive spikes. Each available capacitor is 22 µF nominal, retains 35% at the working voltage, and has 0.3 nH of ESL. (a) Find the capacitance needed for the charge and how many capacitors provide it. (b) Find the largest total inductance allowed and how many capacitors that requires. (c) Which requirement sets the design?

### Problem 07-01.10 [B]

**A small capacitor's self-resonance.** A 100 nF capacitor in an 0402 package has 0.4 nH of ESL. Find its self-resonant frequency and its approximate impedance at 1 GHz. Is it a capacitor at 1 GHz?

### Problem 07-01.11 [B]

**An integrator and its offset.** An op-amp integrator has $R$ = 100 kΩ and $C$ = 1 µF, with its output initially at 0 V. (a) A 0.5 V input is applied for 2 s. Find the output. (b) With the input grounded, the op-amp's 1 mV input offset acts like a 1 mV input. How far does the output drift in 10 s, and how long until it reaches a −12 V rail?

### Problem 07-01.12 [B]

**Power into an inductor at AC.** A 1 mH inductor carries $i(t) = 2\sin(\omega t)$ A at 1 kHz. (a) Find $v(t)$ and its peak. (b) Find $p(t)$, its peak, its average and its frequency. (c) Find the peak stored energy, and explain how energy can flow in and out while the average power is zero.

### Problem 07-01.13 [C]

**A saturating inductor.** A 10 µH inductor has a saturation current of 3 A; above it, model its inductance as falling abruptly to 2 µH. In a converter it starts the on-time at 2.5 A with 8.7 V across it, for 1 µs. (a) Find the final current if the inductor did not saturate. (b) Find the time to reach 3 A, and the final current with saturation. (c) What does this mean for the switch?

### Problem 07-01.14 [B]

**DC steady state with both elements.** A 12 V source feeds node a through 2 kΩ. From node a, a 1 µF capacitor goes to ground, and a 10 mH inductor in series with 4 kΩ also goes to ground. After a long time, find the inductor current, the capacitor voltage and the energy each element stores.

### Problem 07-01.15 [B]

**Pre-charged capacitors in series.** A 2 µF capacitor charged to 5 V and a 3 µF capacitor charged to 2 V are connected in series, aiding (the + terminal of one to the − terminal of the other). At $t = 0$ the pair is connected across a 10 kΩ resistor. (a) Find the equivalent capacitance and its initial voltage. (b) Find the energy stored in the two capacitors, and the energy the equivalent capacitor would store. (c) Find the time constant and the final voltage on each capacitor. (d) Find the energy dissipated in the resistor and the energy left in the capacitors. Explain why the equivalent capacitor describes the terminal behavior but not the stored energy.

---

## Objective coverage

| Learning objective (chapter 07-01) | Problems |
|---|---|
| 1. Element laws in differential and integral form | 1, 2, 3, 11, 12 |
| 2. Stored energy; zero average power in steady state | 1, 2, 6, 7, 12, 14, 15 |
| 3. Continuity, DC behavior and the inductive kick | 6, 8, 14 |
| 4. Series and parallel combinations, including initial conditions; the capacitive divider | 4, 5, 6, 15 |
| 5. Real capacitors and inductors; decoupling | 9, 10, 13 |
