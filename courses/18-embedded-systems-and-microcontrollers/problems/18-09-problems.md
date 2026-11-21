# Problems 18-09 · Ultra-Low-Power Design

Chapter: [18-09](../chapters/18-09-ultra-low-power-design.md) · Worked solutions: [18-09 solutions](../solutions/18-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Currents are battery currents unless stated. A month is 30 days, a year 365 days. Self-discharge is modelled as a constant equivalent current equal to the stated fraction of the nominal capacity per period. Sleep current flows whenever no active phase does. Problems marked *(lab)* can be checked with `labs/18-09-lab/ulp.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-09.1 [A]

**Units of a battery.** A 1000 mAh Li-ion cell has a nominal 3.7 V. (a) How much charge does it hold, in coulombs? (b) How much energy, in joules? (c) How long does it run a device that averages 15 mW?

### Problem 18-09.2 [A]

**Scaling dynamic power.** A core's dynamic current is 3 mA at 48 MHz and 1.2 V. (a) What is its dynamic power? (b) What current does it draw at 24 MHz and 1.2 V? (c) At 24 MHz and 0.9 V (current scales with $Vf$)? (d) What power then, and what fraction of (a)?

### Problem 18-09.3 [A]

**A wearable's budget.** *(lab)* A wristband sleeps at 4 µA. Each second it takes 25 heart-rate samples (1 ms at 1.2 mA each), services 10 Bluetooth connection events (1.2 ms at 5 mA each) and updates its display once (15 ms at 3 mA). (a) Find the average current. (b) How long does a 150 mAh battery last? (c) Rank the four contributions.

### Problem 18-09.4 [B]

**Stop or standby?** An MCU's stop mode draws 5 µA; standby draws 0.4 µA but waking from it costs 3 ms at 1.5 mA more than waking from stop. (a) Find the break-even idle time. (b) For a device that samples every 10 s, compare the charge per period in each mode (ignore the sampling itself). (c) And for every 0.5 s?

### Problem 18-09.5 [B]

**Voltage ranges.** *(lab)* An MCU offers range 1 (1.2 V, up to 80 MHz: 50 µA/MHz plus 600 µA fixed) and range 2 (1.0 V, up to 26 MHz: 35 µA/MHz plus 300 µA fixed), and sleeps at 1 µA. A task of 2 million cycles runs once a second. (a) Find the charge per second at 80 MHz in range 1 and at 26 MHz in range 2. (b) Which wins, and by how much? (c) Reconcile this with "race to idle".

### Problem 18-09.6 [B]

**A regulator across the discharge.** A Li-ion cell discharges from 4.2 V to 3.0 V while supplying a 1.8 V load of 10 mA. (a) What battery current does an LDO draw? (b) What does a 90%-efficient buck draw at 4.2 V and at 3.0 V? (c) Why does the buck's advantage shrink as the cell discharges?

### Problem 18-09.7 [B]

**When self-discharge dominates.** A meter averages 3 µA from a 1000 mAh cell. (a) Ignoring self-discharge, how long does it last? (b) With a primary lithium cell losing 1% of its capacity a year? (c) Also with only 85% of the capacity usable? (d) With a Li-ion cell losing 3% a month instead (full capacity usable)? What equivalent current is that?

### Problem 18-09.8 [B]

**Pull-up currents.** At 3.3 V: (a) a push button with a 10 kΩ pull-up is held down. What current flows? (b) With the MCU's internal 40 kΩ pull-up instead? (c) An I²C bus with 2.2 kΩ pull-ups hangs with SDA held low. What does that line draw? (d) Propose two firmware fixes for the button.

### Problem 18-09.9 [B]

**A cold coin cell.** *(lab)* A coin cell (3.0 V) has 30 Ω internal resistance at room temperature and 150 Ω when cold. A radio burst draws 10 mA for 3 ms, and the supply must stay within 0.3 V of 3.0 V. (a) Is a reservoir capacitor needed at room temperature? (b) What capacitance does the cold case need?

### Problem 18-09.10 [C]

**An asset tracker.** Every hour, a tracker takes a satellite fix (30 s at 25 mA) and reports over LTE-M (5 s at 120 mA plus 2 s at 200 mA). It sleeps at 3 µA. Its 2400 mAh primary cell has 80% usable capacity. (a) Find the charge per hour, the average current and the life in days. (b) Which activity dominates? (c) The product team proposes reporting every 4 hours with assisted fixes of 5 s. Recompute the average current and the life in years. (d) What would you check before promising that figure?

### Problem 18-09.11 [C]

**Indoor solar.** A 5 cm² indoor solar cell delivers 10 µW/cm² under office light, through a harvesting converter of 75% efficiency. (a) What average power can the electronics use, and what average current at 3 V? (b) Over a 64-hour dark weekend, how much energy must storage supply at that power? (c) What supercapacitor, used between 3.3 V and 2.0 V, stores it?

---

## Objective coverage

| Learning objective (chapter 18-09) | Problems |
|---|---|
| 1. Where the current goes | 1, 2 |
| 2. Power modes and break-even | 4 |
| 3. Duty-cycled budgets and battery life | 3, 7, 10, 11 |
| 4. Race to idle and voltage scaling | 2, 5 |
| 5. Regulators and reservoir capacitors | 6, 9 |
| 6. Board-level currents | 8 |
