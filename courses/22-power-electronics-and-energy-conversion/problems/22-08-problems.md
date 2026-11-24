# Problems 22-08 · PMICs and Power Management for SoCs

Chapter: [22-08](../chapters/22-08-pmics.md) · Worked solutions: [22-08 solutions](../solutions/22-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Values marked "assumed" are illustrative; efficiencies and quiescent currents are given in each problem. Problems marked *(lab)* can be checked with `labs/22-08-lab/pmic.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-08.1 [A]

**Headroom for post-regulation.** A 92%-efficient buck feeds an LDO that makes 1.0 V with 150 mV of dropout. What is the best efficiency of the chain?

### Problem 22-08.2 [A]

**An always-on LDO.** An always-on 0.9 V rail draws 10 µA through an LDO with 0.5 µA of quiescent current, from a 3.8 V battery. Find (a) the battery current, (b) the efficiency and (c) the battery power.

### Problem 22-08.3 [B]

**Another PFM–PWM crossover.** *(lab)* A buck from 3.8 V has PWM losses of 12 mW plus $0.15I^2$, and PFM losses of $3.8\ \text{V} \times 0.5\ \mu\text{A}$ plus $0.10I$ plus $0.45I^2$ (assumed). Find the crossover current.

### Problem 22-08.4 [B]

**A sensor node that sleeps most of the time.** *(lab)* A node on a 220 mAh, 3.0 V battery sleeps 99.9% of the time at 2 µW of regulated power (70% efficient) and is active 0.1% of the time at 30 mW (85% efficient); its PMIC draws 300 nA (all assumed). Find (a) the battery energy, (b) the average battery power, (c) the battery life in days, and the shares of the average power due to (d) sleep and (e) the PMIC's quiescent draw.

### Problem 22-08.5 [A]

**A DVS ramp.** A rail with 470 µF is ramped from 0.5 V to 0.8 V at 5 mV/µs. Find (a) the ramp time, (b) the capacitor charging current and (c) the energy stored.

### Problem 22-08.6 [A]

**A slow way down.** The rail of Problem 22-08.5 is lowered back to 0.5 V in PFM with a 0.5 A load. How long does it take?

### Problem 22-08.7 [A]

**AVS on a 0.9 V rail.** A rail at 0.9 V nominal carries a 75 mV guardband; AVS reduces it to 25 mV. Find (a) the dynamic-power ratio and (b) the saving.

### Problem 22-08.8 [B]

**Ramp tracking in the type-III loop.** *(lab)* For the loop of Example 22-07.3 ($\omega_I$ = 8396 rad/s, $V_g/V_M$ = 12), find the steady lead during a DVS ramp of (a) 0.2 mV/µs and (b) 1 mV/µs. What does (b) suggest?

### Problem 22-08.9 [B]

**Soft start against a current limit.** A 1.8 V domain with 47 µF of decoupling is switched on from a supply that may deliver at most 0.5 A of inrush. Find (a) the shortest soft-start time and (b) the energy dissipated in the switch.

### Problem 22-08.10 [A]

**Sequencing time.** Five rails each need a 400 µs soft start and a 100 µs power-good delay. Find the power-up time if they come up (a) one after another and (b) in two groups, the second starting when the first is good.

### Problem 22-08.11 [C]

**Gating when hot.** A domain has 50 nF at 0.75 V, needs 0.5 µJ of state save and restore, and leaks 2 mW at 25 °C, doubling every 25 K (assumed). Find (a) the recharge energy, the break-even time (b) at 25 °C and, with (c) the leakage at 85 °C, (d) the break-even time at 85 °C.

### Problem 22-08.12 [C]

**The cost of a lazy LDO.** A 1.8 V I/O rail draws 200 mA for 2 hours a day from a 3.8 V battery. Find the loss (a) with an LDO and (b) with a 90%-efficient buck, (c) the difference, (d) the energy wasted per day by the LDO choice and (e) that energy as a share of the 4158 J battery of Example 22-08.3.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Rail allocation and cascaded efficiency | 1, 2, 12 |
| 2. PFM/PWM crossover and battery life | 3, 4 |
| 3. DVS transitions and ramp tracking | 5, 6, 8 |
| 4. AVS, soft start and sequencing | 7, 9, 10 |
| 5. Power gating break-even | 11 |
