# Problems 10-02 · MOSFET DC Operation and Biasing

Chapter: [10-02](../chapters/10-02-mosfet-dc-operation-and-biasing.md) · Worked solutions: [10-02 solutions](../solutions/10-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** square law with $m$ = 1; $\lambda$ = 0 unless stated; $k_n = \mu_nC_{ox}W/L$; no gate current. Device values are illustrative unless a data sheet is named.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-02.1 [A]

**Which region?** With $V_{TN}$ = 0.5 V and $|V_{TP}|$ = 0.5 V, name the region: (a) NMOS, $V_{GS}$ = 0.4 V, $V_{DS}$ = 1 V; (b) NMOS, $V_{GS}$ = 1.0 V, $V_{DS}$ = 0.3 V; (c) NMOS, $V_{GS}$ = 1.0 V, $V_{DS}$ = 0.8 V; (d) PMOS, $V_{SG}$ = 1.2 V, $V_{SD}$ = 0.5 V.

### Problem 10-02.2 [A]

**A drain resistor.** An NMOS with $k_n$ = 1 mA/V² and $V_{TN}$ = 0.4 V has $V_{GS}$ = 0.9 V and $R_D$ = 5 kΩ to 1.8 V. Find $I_D$ and $V_D$, check the region, and find the largest $R_D$ that keeps saturation.

### Problem 10-02.3 [A]

**A PMOS stage.** A PMOS with $k_p$ = 0.5 mA/V² and $|V_{TP}|$ = 0.45 V has its source at 1.8 V, its gate at 0.8 V and 2 kΩ from drain to ground. Find the overdrive, $I_D$, $V_D$ and $V_{SD}$, and check the region.

### Problem 10-02.4 [B]

**Designing a divider bias.** Design for $I_D$ = 0.5 mA with $k_n$ = 2 mA/V², $V_{TN}$ = 0.5 V, $R_S$ = 2 kΩ and $V_{DD}$ = 5 V, keeping $V_{DS} \ge$ 1.5 V. (a) Find $V_{ov}$, $V_{GS}$ and $V_G$. (b) Find the largest $R_D$. (c) Choose a divider with 1 MΩ total resistance.

### Problem 10-02.5 [B]

**Stability of that bias.** For Problem 10-02.4's design, the threshold varies by ±40 mV. (a) Find $g_m$ and $1 + g_mR_S$. (b) Find the first-order current sensitivity with and without the source resistor. (c) Find the exact currents at $V_{TN}$ = 0.46 V and 0.54 V with the source resistor.

### Problem 10-02.6 [B]

**Drain-feedback bias.** A large resistor connects drain and gate (no gate current), and $R_D$ = 10 kΩ goes to 3.3 V; $k_n$ = 1 mA/V², $V_{TN}$ = 0.5 V. (a) Why is the transistor saturated? (b) Find $V_{GS}$ and $I_D$. (c) Find $I_D$ for $V_{TN}$ = 0.45 V and 0.55 V.

### Problem 10-02.7 [B]

**A current mirror.** A 20 kΩ resistor from 5 V feeds a diode-connected M1 ($k_n$ = 2 mA/V², $V_{TN}$ = 0.6 V). M2 shares its gate and has three times its $W/L$. (a) With $\lambda$ = 0, find $V_{GS}$, $I_{ref}$ and $I_{D2}$. (b) With $\lambda$ = 0.05 V⁻¹ and M2's drain at 3 V, find $V_{GS}$, $I_{ref}$, $I_{D2}$ and the error against $3I_{ref}$.

### Problem 10-02.8 [B]

**Sizing an on-chip switch.** An NMOS switch must pass 1 A with no more than 50 mV of drop, with $V_{GS}$ = 3.3 V, $V_{TN}$ = 0.6 V and $k_n'$ = 200 µA/V². Find the required $R_{on}$, $W/L$, the width at $L$ = 0.5 µm, and the conduction loss.

### Problem 10-02.9 [B]

**Reading a power-MOSFET data sheet.** A CSD17573Q5B (1.19 mΩ typical, 1.45 mΩ maximum at $V_{GS}$ = 4.5 V) carries 30 A. Find the conduction loss with the typical and maximum values, and with the maximum raised by 1.5× for a hot junction.

### Problem 10-02.10 [C]

**A source follower with body effect.** An NMOS ($k_n$ = 1 mA/V², $V_{TN0}$ = 0.5 V, $\gamma$ = 0.5 V$^{1/2}$, $2\phi_F$ = 0.8 V, body at ground) has its gate at 3.0 V and 10 kΩ from source to ground. (a) Find $V_S$, $V_{TN}$ and $I_D$. (b) Repeat without the body effect. (c) Find the gate-to-source drop $V_G - V_S$ in each case. Why does a "follower" lose more than $V_{TN0}$?

### Problem 10-02.11 [C]

**Overdrive against variability.** A transistor must carry 0.2 mA, and its threshold has σ = 20 mV. (a) With a fixed gate voltage, what overdrive keeps the current's σ below 5%, and what $k_n$ does that imply? (b) At $V_{ov}$ = 0.2 V, find $g_m$, and the σ of the current with a 5 kΩ source resistor, and without it.

### Problem 10-02.12 [B]

**A PMOS high-side switch.** A PMOS ($k_p$ = 2 A/V², $|V_{TP}|$ = 0.8 V) switches a 3.3 V rail with its gate driven to 0 V. (a) Find $R_{on}$. (b) Find the drop and loss at 1 A. (c) Why do designers often use a PMOS here rather than a lower-resistance NMOS?

---

## Objective coverage

| Learning objective (chapter 10-02) | Problems |
|---|---|
| 1. Square-law equations and regions | 1, 2, 3 |
| 2. Operating points and root choice | 2, 3, 4, 6 |
| 3. Bias networks and their stability | 4, 5, 6, 11 |
| 4. Diode-connected transistors and mirrors | 6, 7 |
| 5. MOSFET switches and data sheets | 8, 9, 12 |
| 6. Body effect | 10 |
