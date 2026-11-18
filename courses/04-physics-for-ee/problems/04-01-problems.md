# Problems 04-01 · Mechanics Essentials for EE

Chapter: [04-01](../chapters/04-01-mechanics-essentials.md) · Worked solutions: [04-01 solutions](../solutions/04-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $g = 9.80665$ m/s²; $k = 1.380649\times10^{-23}$ J/K; $e = 1.602176634\times10^{-19}$ C; room temperature 300 K; 1 hp = 745.7 W; a year is 365.25 days. Neglect air resistance unless stated. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-01.1 [A]

**Units.** (a) Show that a joule per coulomb is a volt, and write the ohm in SI base units. (b) Show that $\tfrac12Li^2$ has units of joules and $L/R$ units of seconds. (c) A student writes $x = \tfrac12at^3$ for motion from rest at constant acceleration. Show by dimensions that it is wrong.

### Problem 04-01.2 [A]

**Conversions.** (a) Express 1 kWh in electronvolts. (b) Express a 75 Wh laptop battery in kJ. (c) Express a 2.5 *g* acceleration in m/s². (d) Express a 1.12 eV photon energy in joules.

### Problem 04-01.3 [A]

**A pendulum by dimensions.** A pendulum of length $L$ swings in gravity $g$; its bob has mass $m$. (a) Use dimensional analysis to show that its period is proportional to $\sqrt{L/g}$ and cannot depend on $m$. (b) The full analysis gives a period of $2\pi\sqrt{L/g}$ for small swings. Evaluate it for $L = 1$ m.

### Problem 04-01.4 [B]

**An accelerometer in an elevator.** A phone lies flat on the floor of an elevator; its accelerometer reports the vertical specific force. Find the reading, in m/s² and in *g*, when the elevator (a) accelerates upward at 2 m/s²; (b) moves upward while slowing at 1.5 m/s²; (c) falls freely after its cable breaks. (d) Why can the phone not tell case (a) apart from standing still on a planet with a stronger gravity?

### Problem 04-01.5 [B]

**A spring launcher.** A spring with $k_s = 200$ N/m is compressed 5 cm and launches a 20 g ball horizontally. (a) How much energy does the spring store? (b) What is the launch speed? (c) If 10% of the stored energy is lost to friction, what is the speed?

### Problem 04-01.6 [B]

**Elevator power and the counterweight.** A 1000 kg elevator car rises at a constant 2 m/s. (a) What mechanical power does the hoist deliver if there is no counterweight? (b) With an 800 kg counterweight descending at the same speed? (c) What electrical input power does case (b) need if the drive is 85% efficient?

### Problem 04-01.7 [B]

**A collision.** A 2 kg cart moving at 3 m/s hits a 1 kg cart at rest, and they stick together. (a) Find the final speed. (b) Find the kinetic energy before and after, and the percentage lost. (c) Where did the lost energy go, and why is momentum still conserved?

### Problem 04-01.8 [B]

**Flywheel energy storage.** A uniform disk of 100 kg and radius 0.3 m spins at 20,000 rpm. (a) Find its moment of inertia, angular speed and stored energy, in MJ and kWh. (b) For how long could it supply 50 kW? (c) What fraction of its energy has it delivered when it has slowed to half speed?

### Problem 04-01.9 [B]

**A simple harmonic oscillator.** A 0.5 kg mass on a spring of $k_s = 200$ N/m oscillates with an amplitude of 3 cm. Find (a) the angular frequency, frequency and period; (b) the maximum speed and the maximum acceleration; (c) the total energy.

### Problem 04-01.10 [B]

**Q from a ring-down.** After being excited, a 100 kHz MEMS resonator's amplitude falls to half in 500 cycles. (a) Find the decay rate α. (b) Find its Q. (c) What fraction of its stored energy does it lose per cycle? (d) What is the half-power bandwidth of its resonance?

### Problem 04-01.11 [B]

**Springs and capacitors.** Springs of 100 N/m and 300 N/m are combined. (a) Find the stiffness when they are connected end to end (in series) and side by side (in parallel). (b) In the force–voltage analogy, what capacitance represents each spring, and how must the capacitors be connected to represent the springs in series? Check that the total matches (a).

### Problem 04-01.12 [B]

**Sensitivity against bandwidth.** For proof-mass accelerometers with $Q = 1/\sqrt2$ and resonant frequencies of 1, 4 and 16 kHz: (a) find the deflection per *g*; (b) find the bandwidth of each; (c) how small a displacement must the 16 kHz sensor's readout resolve for 1 m*g*?

### Problem 04-01.13 [C]

**Designing for a noise floor.** A tilt sensor needs a thermomechanical noise floor of 20 µ*g*/√Hz at 300 K, with $f_0 = 2$ kHz and $Q = 2$. (a) Find the minimum proof mass. (b) Find the spring constant and the deflection per *g*. (c) If the same structure were sealed in vacuum so that $Q = 1000$, by what factor would the noise floor fall, and what new problem would appear?

### Problem 04-01.14 [C]

**Equipartition and the $4kTb$ force noise.** A mass–spring–damper at temperature $T$ is driven only by a random force of one-sided density $G_F$ (N²/Hz). (a) Write $\overline{x^2}$ as an integral over frequency. (b) Using $\int_0^\infty\frac{d\omega}{(k_s - m\omega^2)^2 + b^2\omega^2} = \frac{\pi}{2k_sb}$, show that $\overline{x^2} = G_F/(4k_sb)$. (c) Equipartition says $\tfrac12k_s\overline{x^2} = \tfrac12kT$. Deduce $G_F$. (d) Find the rms thermal motion for $k_s = 1$ N/m and for $k_s = 1000$ N/m. Why does the mass not appear?

### Problem 04-01.15 [C]

**Cushioning for a drop.** A device survives a half-sine shock of at most 1500 *g* peak. It may be dropped from 1.2 m. (a) Find the impact speed. (b) Find the shortest allowable pulse duration. (c) For a half-sine pulse, show that the stopping distance is $v\Delta t/2$ and evaluate it: how much must the cushioning compress?

### Problem 04-01.16 [C]

**A watch crystal's temperature error.** A 32.768 kHz tuning-fork crystal's frequency follows a parabola, $\Delta f/f = \beta(T - T_0)^2$, with $\beta = -0.035$ ppm/°C² and turnover $T_0 = 25$ °C (a typical datasheet value; see §9). (a) Find the fractional frequency error at −10 °C and at 60 °C. (b) How many seconds per day, and minutes per year, does a clock lose at −10 °C? (c) A wearable sits at 32 °C on the skin. How many seconds does it lose in 30 days? (d) Why do oscillators that must be accurate over temperature compensate electronically?

---

## Objective coverage

| Learning objective (chapter 04-01) | Problems |
|---|---|
| 1. SI units, dimensional analysis, energy units | 1, 2, 3 |
| 2. Newton's laws, impulse, momentum, shocks | 4, 7, 15 |
| 3. Work, energy, power, rotation | 5, 6, 8 |
| 4. Oscillator, Q as an energy ratio, force–voltage analogy | 9, 10, 11, 14, 16 |
| 5. MEMS accelerometer: sensitivity, bandwidth, noise | 12, 13, 14 |
