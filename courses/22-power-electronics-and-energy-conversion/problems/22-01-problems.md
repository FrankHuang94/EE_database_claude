# Problems 22-01 · Power Conversion Principles

Chapter: [22-01](../chapters/22-01-power-conversion-principles.md) · Worked solutions: [22-01 solutions](../solutions/22-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Efficiencies are ratios of cycle-averaged powers. "Loss" means $P_{in} - P_{out}$. The loss model is $P_{loss} = P_0 + aI + RI^2$ (§3.5). Values marked "assumed" are illustrative, not data-sheet figures. Problems marked *(lab)* can be checked with `labs/22-01-lab/power.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-01.1 [A]

**Where the watts are.** A supply delivers 2 kW. (a) Find its loss at 80%, 85%, 97% and 98% efficiency. (b) Which upgrade saves more watts, 80 → 85% or 97 → 98%? (c) What fraction of the loss does each upgrade remove?

### Problem 22-01.2 [A]

**A three-stage chain.** Three converters in series, at 98%, 95% and 92% from source to load, deliver 50 W. Find (a) the chain efficiency, (b) the input power, (c) the loss in each stage and (d) the stage that holds the most loss.

### Problem 22-01.3 [A]

**An LDO's heat.** An LDO makes 3.3 V at 200 mA from 5.0 V with 50 µA of quiescent current (assumed). Find (a) its efficiency and (b) its dissipation. (c) With a junction-to-ambient thermal resistance of 50 K/W in 25 °C air, what is the junction temperature? (d) If its dropout is 270 mV at this load, what is the lowest input at which it regulates?

### Problem 22-01.4 [A]

**Battery charge, not power.** A 1.2 V, 2 mA rail runs from a 3.8 V cell. Compare an LDO (negligible quiescent current) with an 85%-efficient buck: find (a) the LDO's battery current, (b) the buck's battery current, (c) the ratio of battery lives and (d) the LDO's efficiency.

### Problem 22-01.5 [B]

**When quiescent current matters.** (a) Show that a linear regulator's efficiency is the fraction $I_{out}/(I_{out} + I_Q)$ of its ceiling $V_{out}/V_{in}$. (b) Above what load is a regulator with $I_Q$ = 25 nA within 1% of its ceiling, and (c) one with $I_Q$ = 5 µA (assumed)? (d) A wearable's rail sleeps at 3 µA: what fraction of the ceiling does each regulator reach?

### Problem 22-01.6 [B]

**Staircase charging and gate drive.** (a) Show that charging a capacitor $C$ from 0 to $V$ in $N$ equal voltage steps, each through a resistance and allowed to settle, loses $\tfrac12CV^2/N$. Evaluate the loss for $C$ = 100 nF and $V$ = 3.3 V with (b) one, (c) three and (d) ten steps. (e) A driver charges a switch's effective gate capacitance of 2 nF (assumed) to 5 V and discharges it to 0 V a million times a second. Show that the drive power is $CV^2f$ and evaluate it.

### Problem 22-01.7 [B]

**A capacitor that acts like a resistor.** A capacitor $C$ is connected alternately to an ideal source $V_1$ and to an ideal source $V_2 < V_1$, $f$ times per second, settling fully each time. (a) Find the charge moved per cycle and the average current $I$. (b) Show that the power lost is $fC(V_1 - V_2)^2 = I^2/(fC)$, so the circuit behaves as a resistance $R_{eq} = 1/(fC)$. For $C$ = 1 µF, $f$ = 1 MHz and $I$ = 100 mA, find (c) $R_{eq}$, (d) $V_1 - V_2$ and (e) the loss. (f) What $C$ keeps the drop at 18 mV (1% of a 1.8 V rail) at the same current and frequency?

### Problem 22-01.8 [B]

**The switch node's spectrum.** A buck switches a 5 V input at 2 MHz with $D$ = 0.4. Find (a) the average output, and the amplitudes of (b) the fundamental and (c) the second harmonic at the switch node. With an LC filter whose corner is $f_s/20$, use the unloaded response $\lvert 1 - (f/f_0)^2\rvert^{-1}$ to estimate (d) the peak-to-peak ripple from the fundamental and (e) the second harmonic's contribution to the output amplitude.

### Problem 22-01.9 [B]

**The price of frequency.** A 1.8 V, 3 A converter at 500 kHz has $P_0$ = 80 mW and $a$ = 20 mW/A, both proportional to switching frequency, and $R$ = 10 mΩ (all assumed). Find (a) its loss and (b) its efficiency. At 1 MHz with the same $R$, find (c) the loss and (d) the efficiency, and (e) the ratio of the losses. (f) Halving $L$ allows an inductor with less winding resistance, cutting $R$ to 7 mΩ. What is the efficiency at 1 MHz then?

### Problem 22-01.10 [B]

**Fitting a loss model.** A 1.0 V converter draws 1.227 W at 1 A, 5.375 W at 5 A and 21.5 W at 20 A. (a) Find $P_0$, $a$ and $R$. (b) At what load does its efficiency peak, and (c) what is the peak? (d) Find the efficiency at 1, 5 and 20 A, and explain why two of them are equal.

### Problem 22-01.11 [B]

**Shedding phases in a VRM.** Each phase of a four-phase 0.8 V regulator has a fixed loss of 0.25 W and a resistance of 1 mΩ (assumed; take $a$ = 0). (a) At what loads should the second, third and fourth phases turn on? At 30 A, find the efficiency (b) with two phases and (c) with all four. (d) What is the efficiency at 80 A with four phases?

### Problem 22-01.12 [B]

**A charger that must not burn the hand.** A 65 W charger is built in a 50 × 40 × 25 mm case. (a) Find its power density in W/in³. (b) Assume its surface sheds heat at 10 W/m²·K (natural convection plus radiation, an illustrative figure) and may run 40 K above ambient. What loss can it dissipate, and (c) what minimum efficiency does that require? (d) At 93% efficiency, how hot would the case run above ambient?

### Problem 22-01.13 [C]

**Hold-up against input range.** A 3 kW supply must hold up for 10 ms. Its bus is 390 V, and its DC-DC stage is 97% efficient. Find (a) the bus power and (b) the capacitance if the DC-DC stage regulates down to 300 V. (c) What capacitance is needed if it can only regulate down to 330 V, and (d) by what factor is that larger? (e) What capacitance meets a 20 ms hold-up with the 300 V stage?

### Problem 22-01.14 [C]

**Which point to buy.** A chain of a 94% supply, a 96% bus converter and an 88% VRM delivers 1 kW. Find (a) the chain efficiency, (b) the input power and (c) the total loss. How much input power does (d) raising the VRM to 90% save, and (e) raising the supply to 96%? (f) Express each as watts saved per point of efficiency.

### Problem 22-01.15 [C]

**A density claim under diligence.** A start-up claims a "3 kW, 99% efficient, 150 W/in³" converter. (a) Find the implied loss, (b) the volume and (c) the heat density. (d) It emerges that the 99% is the PFC stage and the DC-DC stage is 98%: find the overall efficiency, (e) the real loss, (f) the real heat density and (g) the factor by which the heat was understated. (h) If the box can reject 3 W/in³ (assumed), what overall efficiency would 150 W/in³ require?

### Problem 22-01.16 [B]

**A light-load mode.** A 1.8 V wearable buck's loss is $P_0 + aI + RI^2$ with $P_0$ = 6 mW, $a$ = 20 mW/A and $R$ = 0.25 Ω in forced PWM. In pulse-frequency mode, $P_0$ falls to 20 µW, but the larger current pulses raise the effective $R$ to 0.60 Ω. Find the efficiency (a) in PWM and (b) in PFM at 1 mA, and (c) in PWM and (d) in PFM at 50 mA. (e) Above what load does PWM become the better mode?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Efficiency, loss, leverage and chains | 1, 2, 14, 15 |
| 2. Linear regulators and the LDO-or-switcher decision | 3, 4, 5 |
| 3. Lossless switching, the ½CV² loss and filter size | 6, 7, 8, 9 |
| 4. Loss models, peak efficiency and light-load techniques | 9, 10, 11, 16 |
| 5. Power density, its thermal limit and hold-up energy | 12, 13, 15 |
