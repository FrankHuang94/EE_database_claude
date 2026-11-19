# Problems 10-03 · BJT DC Operation and Biasing

Chapter: [10-03](../chapters/10-03-bjt-dc-operation-and-biasing.md) · Worked solutions: [10-03 solutions](../solutions/10-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $V_{BE}$ = 0.7 V (active), $V_{CE,sat}$ = 0.2 V, edge of saturation at $V_{CE}$ = 0.3 V, $V_T$ = 25.852 mV, $V_{BE}$ temperature coefficient −2 mV/K; no Early effect unless stated. Data-sheet values are those quoted in the chapter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-03.1 [A]

**Which region?** (a) NPN with $V_{BE}$ = 0.7 V, $V_{CE}$ = 3 V. (b) NPN with $V_{BE}$ = 0.72 V, $V_{CE}$ = 0.1 V. (c) NPN with $V_{BE}$ = 0.3 V. (d) PNP with $V_{EB}$ = 0.7 V and $V_{EC}$ = 0.2 V.

### Problem 10-03.2 [A]

**α and β.** Find α for β = 50, 100 and 300, and β for α = 0.995. Why does a small change in α mean a large change in β?

### Problem 10-03.3 [A]

**An active stage.** The base is driven from 3 V through 200 kΩ; $R_C$ = 3 kΩ to 9 V; β = 120. Find $I_B$, $I_C$ and $V_C$, and check the region.

### Problem 10-03.4 [B]

**Designing a four-resistor bias.** With $V_{CC}$ = 9 V, design for $I_C$ = 1 mA, $V_E$ = 1.5 V and $V_{CE} \ge$ 3 V, with a divider current of 0.1 mA (ten times the base current at β = 100), treating $I_E \approx I_C$ and neglecting base current in the divider. (a) Find $R_E$ and the largest $R_C$. (b) Find $V_B$, the divider's total resistance and $R_1$, $R_2$. (c) Now include the base current with β = 100: find $R_{Th}$ and the actual $I_C$, and the error against the 1 mA target.

### Problem 10-03.5 [B]

**Sensitivity of that design.** For Problem 10-03.4's circuit, find $I_C$ (a) with β = 300 and its change from β = 100, and (b) with $V_{BE}$ = 0.6 V (a hot junction) and its change.

### Problem 10-03.6 [B]

**Collector-to-base feedback.** $R_C$ = 2 kΩ from 5 V to the collector (carrying $I_C + I_B$) and $R_B$ = 200 kΩ from collector to base. (a) Show that $I_E = (V_{CC} - V_{BE})/(R_C + R_B/(\beta + 1))$. (b) With β = 100 find $I_E$, $I_C$ and $V_C$. (c) With β = 300 find $I_C$ and its change. Compare with the four-resistor bias.

### Problem 10-03.7 [B]

**A PNP high-side switch.** A 2N3906 switches a 50 mA load from 5 V; the base is pulled to 0 V through $R_B$ by a logic output. Using a forced β of 10, $V_{EB(sat)}$ ≤ 0.95 V and $V_{EC(sat)}$ ≤ 0.4 V at 50 mA [2]: (a) find the base current and the largest $R_B$; (b) with 750 Ω, find $I_B$ and the forced β; (c) find the collector dissipation.

### Problem 10-03.8 [B]

**Mirror errors.** A BJT mirror with β = 50 copies $I_{ref}$ = 0.5 mA. (a) Find $I_{out}$ and its error. (b) A third transistor (the "buffer") supplies the two base currents from the reference node, so the reference loses only the buffer's base current. Show that $I_{out} = I_{ref}/[1 + 2/(\beta(\beta + 1))]$, and evaluate it.

### Problem 10-03.9 [B]

**Over temperature.** For Example 10-03.3's bias (β = 100), find $I_C$ at −40 °C and at 85 °C (relative to 0.7 V at 25 °C), and the percentage change across the range.

### Problem 10-03.10 [C]

**Where runaway begins.** For a transistor with $V_{CE}$ = 5 V and $R_{\theta JA}$ = 200 K/W and a fixed $V_{BE}$, find the collector current at which the thermal loop gain reaches 1. With $R_E$ = 10 Ω, what is the largest loop gain possible at any current?

### Problem 10-03.11 [C]

**Driving an LED from 1.8 V logic.** A 2N3904 sinks 20 mA through an LED (2.0 V drop) and a series resistor from 5 V. (a) With a forced β of 10 and $V_{BE(sat)}$ = 0.85 V, find $I_B$ and $R_B$. (b) At −40 °C, $V_{BE(sat)}$ is about 130 mV higher; find $I_B$ and the forced β. Is the transistor still saturated? (c) Find the LED's series resistor, with $V_{CE(sat)}$ = 0.2 V.

### Problem 10-03.12 [B]

**Base resistor with emitter degeneration.** $R_B$ = 330 kΩ from 9 V to the base and $R_E$ = 1 kΩ. (a) Find $I_C$ for β = 100 and 300. (b) Why is this much worse than the four-resistor bias of Example 10-03.3, although both have an emitter resistor?

---

## Objective coverage

| Learning objective (chapter 10-03) | Problems |
|---|---|
| 1. Terminal relations and regions | 1, 2, 3 |
| 2. Operating points and forced β | 3, 7, 11 |
| 3. Four-resistor bias and sensitivity | 4, 5, 6, 9, 12 |
| 4. Current mirror errors | 8 |
| 5. Saturated switch design | 7, 11 |
| 6. Thermal loop gain | 10 |
