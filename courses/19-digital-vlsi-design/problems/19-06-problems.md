# Problems 19-06 · Power and Low-Power Design

Chapter: [19-06](../chapters/19-06-power-and-low-power-design.md) · Worked solutions: [19-06 solutions](../solutions/19-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $P_{dyn} = \alpha CV_{DD}^2f$ with α the 0→1 probability per cycle. Subthreshold current $I = I_0e^{(V_{GS} - V_T + \eta V_{DS})/(nV_{th})}(1 - e^{-V_{DS}/V_{th}})$ with $V_{th} = kT/q$ (25.85 mV at 300 K). Alpha-power delay $\propto V_{DD}/(V_{DD} - V_T)^\alpha$. Problems marked *(lab)* can be checked with `labs/19-06-lab/power.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-06.1 [A]

**One node.** A 5 fF node at 0.9 V switches with α = 0.15 at 1.5 GHz. Find the energy per full charge–discharge cycle, the energy dissipated while charging, and the average power.

### Problem 19-06.2 [A]

**Clock power.** A clock network of 200 pF runs at 2 GHz and 0.9 V. (a) What is its power? (b) Clock gating disables 40% of its capacitance on average. What does that save?

### Problem 19-06.3 [A]

**Subthreshold slope.** With $n$ = 1.4, find the subthreshold slope at 300 K and at 380 K.

### Problem 19-06.4 [B]

**Slow edges.** Repeat Example 19-06.2 with 200 ps input ramps. (a) What are the short-circuit power and its share of the 7.2 µW dynamic power? (b) What is the short-circuit power with 200 ps ramps at $V_{DD}$ = 0.8 V?

### Problem 19-06.5 [B]

**Hot leakage.** Assume a transistor's threshold falls by 0.8 mV/K from 0.35 V at 300 K, $n$ = 1.3, and the prefactor $I_0$ does not change. By what factor does its off-current ($V_{GS}$ = 0) rise from 300 K to 380 K?

### Problem 19-06.6 [B] *(lab)*

**DIBL and stacks.** Repeat Example 19-06.4 with η = 0.05 and η = 0.2. What are the intermediate-node voltages and the stack's leakage reduction?

### Problem 19-06.7 [B]

**One-third speed.** For Example 19-06.5's design (1.0 V, $V_T$ = 0.35 V, α = 1.3), find the supply that allows one-third of the frequency, and the power and energy per operation relative to full speed.

### Problem 19-06.8 [B]

**Power-gating break-even.** A block leaks 2 mW. Waking it requires recharging 500 pF of internal capacitance to 0.8 V plus 0.08 nJ for control and state restore. (a) What is the wake-up energy? (b) What is the break-even sleep time? (c) Repeat (b) if the sleep transistor still leaks 1% of the block's leakage.

### Problem 19-06.9 [B]

**Multi-threshold mix.** Low-threshold cells leak 12.9 times as much as high-threshold cells (Example 19-06.3). By what factor does a design's leakage grow if 10% of its cells are low-threshold, and if 30% are?

### Problem 19-06.10 [C]

**Veendrick's formula.** (a) Derive the short-circuit charge per transition of an unloaded symmetric inverter driven by a ramp of duration τ, and state why it is exact for that circuit. (b) Evaluate it for β = 100 µA/V², $V_{DD}$ = 1.0 V, $V_T$ = 0.3 V and τ = 100 ps. *(lab)*

### Problem 19-06.11 [C]

**The minimum-energy point.** (a) From $E/(NC) = V^2[\alpha + L_de^{-V/(nV_{th})}]$, show that at the minimum the leakage share of the energy is $2/x$, where $x = V/(nV_{th})$. (b) Show that $V_{min}$ depends on α and $L_d$ only through $L_d/\alpha$. (c) Find $V_{min}$ for α = 0.02 and $L_d$ = 10 ($n$ = 1.3, 300 K).

### Problem 19-06.12 [C]

**How far does parallelism go?** For Example 19-06.5's design: (a) up to what capacitance overhead does two-way parallelism still save power at the same throughput? (b) For four-way parallelism, find the supply and the power ratio with no overhead and with 30% overhead.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Switching energy and dynamic power | 1, 2 |
| 2. Short-circuit power | 4, 10 |
| 3. Leakage and the stack effect | 3, 5, 6, 9 |
| 4. Voltage scaling, parallelism, gating and multi-$V_T$ | 2, 7, 8, 9, 12 |
| 5. The minimum-energy point | 11 |
