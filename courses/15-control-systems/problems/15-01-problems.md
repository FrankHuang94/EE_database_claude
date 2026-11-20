# Problems 15-01 · Modeling Dynamic Systems

Chapter: [15-01](../chapters/15-01-modeling-dynamic-systems.md) · Worked solutions: [15-01 solutions](../solutions/15-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $g$ = 9.81 m/s². Temperatures in °C; temperature differences in K. Thermal values marked illustrative are chosen for the exercise, not taken from a product.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-01.1 [A]

**Counting states.** How many state variables does each system need? (a) A ladder circuit: a voltage source, a series inductor, a shunt capacitor, a second series resistor and a second shunt capacitor. (b) Two masses on a frictionless track, each tied to its own wall by a spring and a damper, and tied to each other by a third spring.

### Problem 15-01.2 [A]

**Analogue values.** A mass of 2 kg rides on a spring with $k$ = 800 N/m and a damper with $b$ = 10 N·s/m. Find $\omega_n$ and $\zeta$, and the element values of its force–voltage analogue circuit.

### Problem 15-01.3 [A]

**A torsional system.** A flywheel with $J$ = 0.01 kg·m² sits on a shaft of torsional stiffness $K$ = 4 N·m/rad, with rotary damping $B$ = 0.02 N·m·s/rad. Find $\omega_n$, $\zeta$ and the steady twist under a constant 0.2 N·m torque.

### Problem 15-01.4 [B]

**A one-node chip.** A chip dissipates 15 W through a thermal resistance of 4 K/W to ambient at 40 °C, and its thermal capacitance is 2 J/K (illustrative). It starts at ambient. Find the time constant, the final temperature and the time to reach 90 °C.

### Problem 15-01.5 [B]

**Where the temperature drops.** Heat of 50 W crosses an 8 mm × 8 mm silicon die 0.5 mm thick ($k$ = 140 W/(m·K)), then a 50 µm layer of thermal interface material ($k$ = 5 W/(m·K)) of the same area. Find each layer's thermal resistance and temperature drop. Which layer matters more, and why?

### Problem 15-01.6 [B]

**Motor characteristics.** A DC motor has $R$ = 1 Ω, $K$ = 0.02 V·s/rad and $J$ = 10⁻⁵ kg·m², with negligible friction and inductance, on 6 V. Find (a) the no-load speed, (b) the stall current and torque, (c) the mechanical time constant, and (d) the speed and current with a 0.03 N·m load.

### Problem 15-01.7 [B]

**When can you drop the inductance?** The motor of Problem 15-01.6 has $L$ = 2 mH. Find the exact time constants of its speed response, and compare the slow one with the first-order model's 25 ms. Would you use the first-order model to design a speed controller with a 5 ms response?

### Problem 15-01.8 [B]

**Two coupled masses.** A 1 kg mass is tied to a wall by a spring of 100 N/m, and a second 1 kg mass is tied to the first by another 100 N/m spring. With no damping, find the two natural frequencies. Sketch the force–current analogue circuit.

### Problem 15-01.9 [B]

**Magnetic levitation.** An electromagnet holds a steel ball below it, with force $F = ki^2/x^2$ upward, where $x$ is the gap. The ball's equation is $m\ddot x = mg - ki^2/x^2$, taking $x$ positive downward. (a) Find the relation between $i^*$ and $x^*$ at equilibrium. (b) Linearize about $x^*$ = 10 mm and show the open-loop pole. (c) How fast does a small error double?

### Problem 15-01.10 [C]

**Close to runaway.** A chip has $P_d$ = 40 W and leakage $2\ \text{W} \times e^{(T - 25\,°\text{C})/25\ \text{K}}$, a thermal resistance of 0.8 K/W, a capacitance of 20 J/K and ambient at 35 °C (illustrative). Find the operating temperature, the leakage, the loop gain and the effective time constant. Find the critical thermal resistance. How much margin does the design have?

### Problem 15-01.11 [C]

**How long does the burst last?** A phone processor idles at 2 W and then bursts to 15 W. Its illustrative thermal network is $C_J$ = 0.5 J/K, $R_{JC}$ = 2 K/W, $C_H$ = 30 J/K and $R_{HA}$ = 8 K/W to ambient at 25 °C. Starting from the idle steady state, how long can the burst run before the junction reaches 95 °C? What would the junction reach if the burst never stopped?

### Problem 15-01.12 [C]

**A fan motor.** The motor of Problem 15-01.6 drives a fan whose load torque is $c\omega^2$ with $c$ = 2 × 10⁻⁷ N·m·s². At 6 V, find (a) the operating speed, and (b) the small-signal gain from voltage to speed and the time constant there. Why is the time constant shorter than the no-load 25 ms?

### Problem 15-01.13 [B]

**State-space form.** Write the state equations of a series RLC circuit with $R$ = 10 Ω, $L$ = 1 mH and $C$ = 1 µF, with states $i$ and $v_C$, and find $\omega_n$, $\zeta$ and the eigenvalues of $A$.

### Problem 15-01.14 [B]

**Reading a thermal data sheet.** A regulator's data sheet gives $R_{\theta JA}$ = 40 °C/W (JEDEC test board) and $\Psi_{JT}$ = 2 °C/W. (a) Estimate $T_J$ at 2 W and 85 °C ambient from $R_{\theta JA}$. (b) On your board, a thermocouple on top of the package reads 120 °C at 2 W. Estimate $T_J$ from $\Psi_{JT}$. (c) Which estimate would you trust, and why?

---

## Objective coverage

| Learning objective (chapter 15-01) | Problems |
|---|---|
| 1. Write equations from element and interconnection laws | 1, 3, 8, 9 |
| 2. Analogies and their limits | 2, 8 |
| 3. State-variable and transfer-function forms | 1, 7, 13 |
| 4. DC motor | 6, 7, 12 |
| 5. Lumped thermal models | 4, 5, 11, 14 |
| 6. Linearization and runaway | 9, 10, 12 |
