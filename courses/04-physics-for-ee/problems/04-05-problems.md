# Problems 04-05 · Current, Resistance and Conduction

Chapter: [04-05](../chapters/04-05-current-resistance-and-conduction.md) · Worked solutions: [04-05 solutions](../solutions/04-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $e = 1.602176634\times10^{-19}$ C; $m_e = 9.1093837139\times10^{-31}$ kg; $\varepsilon_0 = 8.8541878188\times10^{-12}$ F/m. Copper: $\rho = 1.68$ µΩ·cm at 20 °C, $n = 8.49\times10^{28}$ m⁻³ (from 8.96 g/cm³ and 63.546 g/mol), α = 0.00393 /°C, Fermi speed $1.57\times10^6$ m/s. Lightly doped silicon: µₙ = 1400 and µₚ = 470 cm²/V·s. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-05.1 [A]

**Counting current.** (a) 3 C passes a point in 2 s. Find the current. (b) How many electrons per second make 1.5 A? (c) How many coulombs does a 3000 mAh battery deliver from full to empty?

### Problem 04-05.2 [A]

**Drift in a house wire.** A copper wire of 2.5 mm² cross-section carries 10 A. Find (a) the current density in A/mm² and (b) the drift speed in µm/s.

### Problem 04-05.3 [A]

**Resistance from geometry.** (a) Find the resistance of 100 m of copper wire with a 1.5 mm² cross-section. (b) Find the resistance of 1 m of nichrome heater wire 0.5 mm in diameter (take ρ = 1.10 µΩ·m).

### Problem 04-05.4 [B]

**Copper when hot.** Assume copper's resistivity follows ρ₀[1 + α(T − 20 °C)]. At 100 °C, find (a) the resistivity, (b) the Drude mean free time and (c) the mean free path.

### Problem 04-05.5 [B]

**A diffused resistor.** An n-type silicon layer 2 µm thick has $10^{15}$ donors per cm³ (take $n = 10^{15}$ cm⁻³ and neglect holes). Find (a) its resistivity, (b) its sheet resistance and (c) the resistance of a 10-square resistor. (d) Find the resistivity of p-type silicon with $10^{15}$ acceptors per cm³.

### Problem 04-05.6 [A]

**Counting squares.** (a) A thin-film resistor in a layer of 100 Ω/□ is 1 µm wide and 50 µm long. Find its resistance. (b) To make 10 kΩ in the same film with 2 µm width, how long must it be?

### Problem 04-05.7 [B]

**A hot coil.** A copper coil reads 4.00 Ω at 20 °C and 4.80 Ω after an hour of operation. What is its average temperature?

### Problem 04-05.8 [B]

**Power limits.** (a) A 10 Ω resistor is rated 0.25 W. Find the largest current and voltage it can take. (b) Find the Joule power density in copper carrying 4 A/mm², and the heat produced per meter of a 2.5 mm² wire.

### Problem 04-05.9 [B]

**When KCL fails.** A circuit node has 3 mA flowing in and 1 mA and 1.5 mA flowing out. (a) What is the net current into the node? (b) If the node has 10 pF of capacitance to ground, how fast does its voltage change, in V/µs? (c) What does this say about KCL?

### Problem 04-05.10 [B]

**IR drop in power delivery.** A processor draws 100 A from a 1 V rail through a total path resistance of 0.2 mΩ. Find (a) the voltage drop, (b) the power lost in the path, and (c) the path resistance needed to hold the drop to 1% of the rail.

### Problem 04-05.11 [C]

**A tapered trace.** A 1 oz copper trace (34.06 µm thick) narrows linearly from 0.5 mm to 0.25 mm over 50 mm. (a) By integrating $dR = \rho\,dx/(tw(x))$, find its resistance. (b) Compare with a uniform trace at the average width.

### Problem 04-05.12 [C]

**Leakage through a cable's insulation.** A coaxial cable 1.5 m long has an inner radius of 0.45 mm and an insulation outer radius of 1.475 mm; the insulation has ρ = 10¹³ Ω·m and $\varepsilon_r$ = 2.25. (a) Find the leakage resistance between the conductors (current flows radially). (b) Find the capacitance. (c) Show that $RC = \rho\varepsilon$ for any shape of electrodes filled with one material, and evaluate it.

### Problem 04-05.13 [C]

**Copper with a barrier against barrierless molybdenum.** Compare the resistance per µm of the 20 nm × 40 nm line of Example 04-05.6 made (i) of copper in a 562.5 nm² core inside a 2.5 nm barrier, and (ii) of barrierless molybdenum filling all 800 nm². (a) Use bulk resistivities (Cu 1.68, Mo 5.3 µΩ·cm). (b) Suppose instead that size effects raise the effective resistivities to 6.0 µΩ·cm (Cu) and 9.0 µΩ·cm (Mo), illustrative values. (c) Above what effective copper resistivity does molybdenum win in case (b)?

### Problem 04-05.14 [C]

**Sizing a power rail.** A power rail 100 nm thick must carry 2 mA DC, with an electromigration limit of 1 MA/cm². (a) What is its minimum width? (b) Find the resistance of 100 µm of it and the voltage drop at 2 mA.

### Problem 04-05.15 [C]

**When Ohm's law stops at high frequency.** With a sinusoidal field, the Drude equation gives $\sigma(\omega) = \sigma_0/(1 + j\omega\tau)$. (a) Derive this from $m\,dv/dt = -eE - mv/\tau$ using phasors. (b) At what frequency is the current's phase lag 45° in copper? (c) What does this mean for circuits at gigahertz frequencies?

### Problem 04-05.16 [C]

**Repeaters.** A 1 mm wire has $RC$ = 3.702 ns. Split it into $k$ equal segments with a repeater of delay 10 ps driving each, and take each segment's delay as $0.38RC/k^2$. (a) Show that the total delay $k\cdot10\ \text{ps} + 0.38RC/k$ is minimized at $k = \sqrt{0.38RC/10\ \text{ps}}$, and find $k$. (b) Find the total delay with 12 repeaters. (c) Compare with the unrepeated wire.

---

## Objective coverage

| Learning objective (chapter 04-05) | Problems |
|---|---|
| 1. Current, current density, drift and continuity | 1, 2, 9 |
| 2. Drude model, conductivity, mobility | 4, 5, 15 |
| 3. Resistance, sheet resistance, temperature and size effects | 3, 5, 6, 7, 11, 12, 13 |
| 4. Joule heating, IR drop and electromigration | 8, 10, 14 |
| 5. RC delay and interconnect tradeoffs | 13, 16 |
