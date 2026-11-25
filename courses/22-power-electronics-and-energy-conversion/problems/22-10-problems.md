# Problems 22-10 · Datacenter Power Delivery

Chapter: [22-10](../chapters/22-10-datacenter-power-delivery.md) · Worked solutions: [22-10 solutions](../solutions/22-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Copper resistivity 1.72 × 10⁻⁸ Ω·m. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-10-lab/pdn.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-10.1 [A]

**A megawatt rack.** A rack draws 1 MW. Find the distribution current at (a) 54 V and (b) 800 V, and (c) the factor by which the conductor cross-section can shrink at 800 V for the same loss fraction.

### Problem 22-10.2 [A]

**Where the load sits on the bar.** A busbar loop of 100 µΩ carries 1000 A. Find its loss if the load is (a) all at the far end, (b) spread uniformly along the bar, and (c) all at the midpoint.

### Problem 22-10.3 [B]

**AC or DC, with real power factor.** Compare 800 V DC on two conductors with 480 V three-phase AC at a power factor of 0.95, per conductor of the same current rating, with the AC on (a) three conductors and (b) four.

### Problem 22-10.4 [B]

**Two chains.** A 48 V chain has a 97.5% PSU, a 98% bus converter and a 90% VRM; an 800 V chain has a 98.5% rectifier stage, a 97.5% 64:1 converter and the same VRM (all assumed). Find the efficiency of (a) the 48 V chain and (b) the 800 V chain, the input power per megawatt of chip power for (c) the 48 V and (d) the 800 V chain, and (e) the difference in kilowatts.

### Problem 22-10.5 [B]

**Choosing the phase count.** *(lab)* A regulator converts 12 V to 1.0 V with 150 nH per phase at 800 kHz. Find (a) the duty cycle, (b) the single-phase ripple, and the summed ripple with (c) 6 phases and (d) 12 phases.

### Problem 22-10.6 [A]

**Phases from a current rating.** A 1200 A rail uses power stages rated 70 A continuous, derated to 80% of rating. Find (a) the minimum phase count and (b) the current per phase.

### Problem 22-10.7 [B]

**A load line for a 1.0 V rail.** A rail must stay within 1.0 V ± 40 mV from 0 to 600 A. With AVP using the whole window, find (a) the load line, (b) the voltage at 300 A, and (c) the power saved at 600 A against a fixed 1.0 V.

### Problem 22-10.8 [C]

**Package inductance budget.** *(lab)* A die has 30 µF of capacitance behind 3 pH and sees a fast 150 A step. Find (a) the resonant frequency, (b) $Z_0$ and (c) the undamped first droop. (d) What package inductance would hold the first droop to 30 mV with the same capacitance?

### Problem 22-10.9 [A]

**Energy view of the first droop.** For Example 22-10.6, compute (a) the energy $\tfrac12L\Delta I^2$ and (b) the energy $\tfrac12C(\Delta IZ_0)^2$, and explain why they are equal.

### Problem 22-10.10 [B]

**Thinner copper, longer path.** A lateral path 30 mm long and 40 mm wide uses 1 oz (35 µm) planes, 6 each for supply and return, at 800 A. Find (a) the sheet resistance, (b) one plane's resistance over the path, (c) the loop resistance and (d) the loss. (e) If vertical delivery cuts the path resistance tenfold, what is the loss?

### Problem 22-10.11 [A]

**PUE.** A facility draws 50 MW in total and delivers 40 MW to IT equipment. Find (a) its PUE, (b) its overhead fraction, (c) how much higher its PUE is than Google's 2025 fleet average of 1.09, and (d) what that gap means in megawatts at this IT load.

### Problem 22-10.12 [B]

**Smoothing a swing.** A 1200 W GPU's power swings by 60% for 20 ms. Find (a) the energy the swing needs and (b) the capacitance at 54 V that supplies it while drooping to 48 V.

### Problem 22-10.13 [C]

**Decoupling count.** A 0.75 V rail allows 3% for a 400 A step. (a) What is the target impedance? (b) How many ceramic capacitors with 2 mΩ ESR must be paralleled for their combined ESR to meet it at their resonance?

### Problem 22-10.14 [B]

**Slew rate and pick-up time.** A 16-phase regulator converts 12 V to 0.75 V with 120 nH per phase. The load steps by 600 A instantly, and the controller turns every phase on until the regulator's current catches up. Find (a) the maximum slew rate of the total current, (b) the time to pick up the step, (c) the charge the output capacitors must supply meanwhile, treating the regulator's current as a linear ramp, and (d) the capacitance that keeps the droop within 30 mV. (e) Repeat (b) and (d) with 8 phases of the same inductance.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Conversion chain, efficiency and PUE | 4, 11 |
| 2. Distribution voltage, conductor loss, AC and DC | 1, 2, 3, 10 |
| 3. Multiphase regulators and load lines | 5, 6, 7, 14 |
| 4. Target impedance, resonance and decoupling | 8, 9, 13 |
| 5. Vertical delivery and energy storage | 10, 12 |
