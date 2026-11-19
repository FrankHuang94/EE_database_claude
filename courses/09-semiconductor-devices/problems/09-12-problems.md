# Problems 09-12 · Advanced Transistors: FinFET, GAA, CFET and Backside Power

Chapter: [09-12](../chapters/09-12-finfet-gaa-cfet-backside-power.md) · Worked solutions: [09-12 solutions](../solutions/09-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 300 K; $\varepsilon_s/\varepsilon_{ox}$ = 3 (11.7/3.9); oxide thicknesses are SiO₂-equivalent. Use the scale-length model of chapter §3.2 with $a$ = 0.2 V at the source, and define DIBL between $V_{DS}$ = 0.05 V and 0.7 V unless stated. "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-12.1 [A]

**Counting fins.** A fin is 45 nm tall and 7 nm wide. Find its effective width. How many fins does a transistor need for at least 400 nm of width, and what width does it then have?

### Problem 09-12.2 [A]

**A scale length.** Find $\lambda$ for a double-gate body 6 nm thick with a 0.8 nm oxide.

### Problem 09-12.3 [C]

**The single-gate scale length.** A thin body of thickness $t_{si}$ has one gate (oxide $t_{ox}$) on top, at $y$ = 0, and a thick insulator below, which you may model as zero normal field at $y = t_{si}$. (a) Using $\phi = c_0(x) + c_1(x)y + c_2(x)y^2$, the gate boundary condition and the back condition, and applying Laplace's equation at the back surface (the worst leakage path), show that $\lambda^2 = (\varepsilon_s/\varepsilon_{ox})t_{si}t_{ox} + t_{si}^2/2$. (b) Evaluate it for $t_{si}$ = 7 nm and 4 nm with a 1 nm oxide, and compare with the double-gate value at 4 nm.

### Problem 09-12.4 [B]

**Minimum gate length (numerical).** For the double-gate body of Problem 09-12.2, find the gate length at which DIBL equals 30 mV/V, and express it as $L/\lambda$.

### Problem 09-12.5 [B]

**Hu's rule at 20 nm (numerical).** A 20 nm double-gate transistor with a 1.0 nm oxide uses Hu's maximum body thickness, $T_{si} = L/2$. Find $\lambda$, $L/\lambda$ and the DIBL. Then find the body thickness that brings DIBL down to 50 mV/V, and its $\lambda$.

### Problem 09-12.6 [B]

**Sheets against fins.** (a) Find the effective width of a stack of four nanosheets 25 nm wide and 5 nm thick, and of three sheets 35 nm wide and 5 nm thick. (b) How many fins (50 nm tall, 6 nm wide) would match 240 nm? What widths do the nearest whole-fin choices give?

### Problem 09-12.7 [B]

**A real swing.** A short GAA transistor has an effective $m$ of 1.05. Find its swing at 300 K and at 85 °C, and the factor by which heating raises its off-current at a fixed current-defined threshold of 0.25 V.

### Problem 09-12.8 [B]

**IR drop along a rail.** (a) A rail of total resistance $R$ carries a uniformly distributed load current $I$. Derive the maximum drop when it is fed from one end and when it is fed from both ends. (b) Evaluate both for $R$ = 400 Ω and $I$ = 0.3 mA.

### Problem 09-12.9 [B]

**Cell height from backside power.** A standard cell is 6 routing tracks tall at a 24 nm metal pitch. If moving the power rails to the backside lets the cell drop to 5 tracks, what are the old and new cell heights, and what is the logic-density gain at the same gate pitch?

### Problem 09-12.10 [B]

**What "less than 25%" compounds to.** The IRDS 2024 roadmap expects SoC area to improve by less than 25% per node on average. Find the area factor and the density gain after six nodes at 20% and at 25% per node, and compare with the classical halving per node.

### Problem 09-12.11 [B]

**Confinement in a thin body.** In a (100) silicon body, the lowest electron subband comes from the two valleys whose heavy mass ($m_l$ = 0.98 $m_0$) points across the body. Treating the body as an infinite well (04-10), find the confinement energy $E_1 = h^2/8m_lt_{si}^2$ for 5 nm, 4 nm and 3 nm, the shift from 5 to 4 nm, and $|dE_1/dt_{si}|$ at 5 nm and at 3 nm. What does this mean for threshold variation in very thin bodies?

### Problem 09-12.12 [C]

**CFET cell height.** In a side-by-side GAA inverter cell, the height is 18 nm (half power rail and spacing) + 30 nm (n-sheet) + 40 nm (n–p spacing) + 30 nm (p-sheet) + 18 nm. A CFET stacks the p-sheet under the n-sheet: 18 + 30 + 18 nm. But the cell must also hold 4 routing tracks at an 18 nm metal pitch. Find both cell heights (taking the larger of the device and track limits for the CFET) and the density gain.

---

## Objective coverage

| Learning objective (chapter 09-12) | Problems |
|---|---|
| 1. Thin-body and multigate electrostatics | 7, 11 |
| 2. Scale length, roll-off and DIBL | 2, 3, 4, 5 |
| 3. Effective width and quantization | 1, 6 |
| 4. CFET and backside power | 8, 9, 12 |
| 5. Roadmap and production status | 10 |
