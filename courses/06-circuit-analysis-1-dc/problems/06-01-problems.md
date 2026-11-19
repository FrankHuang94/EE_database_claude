# Problems 06-01 · Charge, Current, Voltage, Power and the Lumped Circuit Abstraction

Chapter: [06-01](../chapters/06-01-charge-current-voltage-power.md) · Worked solutions: [06-01 solutions](../solutions/06-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $e = 1.602176634\times10^{-19}$ C; $c$ = 299 792 458 m/s; copper $n = 8.491\times10^{28}$ m⁻³ (04-05). A year is 365 days unless stated (365.25 days, 8766 h, where marked). Use the passive sign convention unless a problem says otherwise. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-01.1 [A]

**Units of a budget.** (a) A phone cell is rated 3.7 V, 4000 mAh. How much charge does it hold, in coulombs, and how much energy, in Wh and in kJ? (b) A leakage current of 50 µA flows for one year. How much charge is that, in coulombs and in mAh? (c) How many joules are in 1 kWh, and for how long can it run a 10 W lamp?

### Problem 06-01.2 [A]

**Current from charge.** The charge that has passed a point in a wire is $q(t) = 5(1 - e^{-t/2\ \text{ms}})$ µC for $t \ge 0$. (a) Find $i(t)$. (b) Evaluate $i(0)$ and $i(2\ \text{ms})$. (c) How much charge passes in total as $t \to \infty$?

### Problem 06-01.3 [A]

**Absorbed or delivered?** For each element, find the power it absorbs and say whether it absorbs or delivers power. (a) $v = 10$ V, with a current of 2 A referenced *into* the + terminal. (b) $v = 10$ V, with a current of 2 A referenced *out of* the + terminal. (c) $v = -5$ V, with a current of −3 A referenced into the + terminal. (d) $v = 3$ V across terminals A (+) and B (−), with a current of −4 A referenced out of terminal A.

### Problem 06-01.4 [A]

**The slow electrons and the fast signal.** A copper wire of 1.0 mm² cross-section carries 1.0 A. (a) Find the electrons' drift speed. (b) How long does one electron take to travel 1 m along the wire? (c) How long does a change in the current take to travel 1 m along a cable in which signals move at two-thirds of $c$? (d) Explain in two sentences why a lamp lights at once even though the electrons in its wire crawl.

### Problem 06-01.5 [B]

**Balancing the books.** A circuit has five elements. The table gives each element's voltage (with its + terminal named) and a current with its reference direction.

| Element | Voltage | Current reference | Current |
|---|---|---|---|
| A | 12 V | out of the + terminal | 3 A |
| B | 4 V | into the + terminal | 3 A |
| C | 8 V | into the + terminal | 1 A |
| D | 8 V | out of the + terminal | −1.5 A |
| E | 2 V | into the + terminal | unknown |

(a) Find the power absorbed by A to D. (b) Use Tellegen's theorem to find the power absorbed by E. (c) Find E's current. (d) Which elements are sources of energy?

### Problem 06-01.6 [B]

**Two sources sharing a load.** A 9 V source with a 1 Ω series resistance and a 12 V source with a 2 Ω series resistance both feed node A, which connects to ground through 4 Ω (the topology of Example 06-01.2). (a) Find $v_A$ and the three branch currents. (b) Find the power absorbed by each of the five elements and check the power balance. (c) For what value of the second source's voltage does the 9 V source neither deliver nor absorb power? (d) What happens to the 9 V source above that value?

### Problem 06-01.7 [B]

**A flashing beacon.** A beacon's LED driver absorbs 2.0 W for 0.10 s, then its power falls linearly to zero over 0.20 s; the pattern repeats every 2.0 s. (a) How much energy does each flash take? (b) What is the average power? (c) How much energy does the beacon use per day, in J and in Wh?

### Problem 06-01.8 [B]

**The average of a product.** A voltage is a square wave: 5 V for the first half of each 1 ms period and 0 V for the second half. Find the average power and the product of the average voltage and the average current when the current is (a) 2 A during the first half and 0 during the second; (b) 0 during the first half and 2 A during the second; (c) a constant 1 A. Explain why $\overline{vi}$ and $\overline{v}\,\overline{i}$ differ.

### Problem 06-01.9 [B]

**An IoT node on two AA cells.** Two alkaline AA cells in series supply 3.0 V and are rated 2500 mAh. A sensor node sleeps at 5 µA; every 60 s it measures for 50 ms at 10 mA; every 15 minutes it transmits for 1.0 s at 40 mA. The sleep current is always present. (a) Find the average current. (b) Estimate the battery life in hours and in years (use 8766 h per year). (c) What share of the charge does the radio use? (d) How long would the batteries last if the node transmitted once an hour instead? (e) Name one effect that would make the real life shorter than (d).

### Problem 06-01.10 [B]

**How long may a wire be?** Use the rule $t_d < t_r/6$. (a) An FR-4 stripline has a delay of 7.154 ps/mm. What is the longest trace that is lumped for 1 ns edges? (b) For 100 ps edges? (c) On a chip, a wire runs in a dielectric with $\varepsilon_r$ = 3.0. What is its delay per millimeter, and the longest wire that is lumped (by this rule alone) for 20 ps edges? (d) On-chip wires are usually limited by something else before this rule bites. What? (Hint: 04-05.)

### Problem 06-01.11 [C]

**Why USB went to 48 volts.** USB Power Delivery delivers up to 100 W as 20 V at 5 A, and since revision 3.1 (2021) its Extended Power Range delivers up to 240 W as 48 V at 5 A ([R-098](../../../reference/research-log.md#r-098--usb-power-delivery-rack-power-distribution-and-ai-rack-power)). Model a cable as a round-trip resistance of 0.20 Ω (illustrative). (a) For 100 W at 20 V, find the cable loss and the voltage drop as a fraction of the supply. (b) Repeat for 240 W at 48 V. (c) Repeat for 240 W delivered at 20 V. (d) Explain, with the square law, why the higher-power mode raised the voltage instead of the current.

### Problem 06-01.12 [C]

**Copper for an AI rack.** A rack draws 120 kW (illustrative of current AI racks; chapter §9). (a) Find the current if power is distributed along the rack at 54 V, and at 800 V. (b) Find the busbar loss at each voltage for a busbar resistance of 50 µΩ. (c) For the *same* loss, the busbar's resistance can scale as $V^2$. By what factor can its copper cross-section shrink when moving from 54 V to 800 V? (d) Name two costs of the higher voltage.

### Problem 06-01.13 [C]

**Tellegen across two circuits.** Circuit 1 is Example 06-01.2. Circuit 2 has the same graph and reference directions but different elements: $V_1'$ = 6 V, $R_1'$ = 1 Ω, $V_2'$ = 0 V, $R_2'$ = 1 Ω, $R_3'$ = 1 Ω. (a) Solve circuit 2 for its node voltage and branch currents. (b) Compute $\sum_k v_k i'_k$, the sum over the five elements of circuit 1's voltage times circuit 2's current, each with the passive convention. (c) Explain, from the proof in §3.5, why the result had to come out as it did, although it is not a power.

### Problem 06-01.14 [C]

**Where the heater's power comes in.** A nichrome heater wire is 0.50 m long with radius 0.25 mm and carries 2.0 A with 10 V across it. (a) Find the axial electric field at its surface and the magnetic field strength $H$ at its surface. (b) Find the magnitude and direction of the Poynting vector $\vec S = \vec E\times\vec H$ at the surface. (c) Integrate it over the wire's surface and compare with $VI$. (d) What does this say about how energy reaches a resistor?

### Problem 06-01.15 [B]

**Reading the simulator.** A battery is modeled in ngspice as `VBAT bp 0 DC 3.7`. (a) The operating point reports `i(vbat) = 1.5`. Is the battery charging or discharging, and at what power? (b) In another run, `@vbat[p] = -2.0`. What is happening, and what is the current? (c) Why does SPICE's convention make a normal, discharging battery show a negative current?

---

## Objective coverage

| Learning objective (chapter 06-01) | Problems |
|---|---|
| 1. Quantities and units | 1, 2, 4 |
| 2. Lumped matter discipline, KCL and KVL | 4, 10, 14 |
| 3. Reference directions and the passive sign convention | 3, 5, 6, 15 |
| 4. Power balance (Tellegen) | 5, 6, 13 |
| 5. Energy, average power, efficiency and distribution loss | 7, 8, 9, 11, 12 |
