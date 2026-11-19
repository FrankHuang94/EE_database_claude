# Problems 09-09 · The Long-Channel MOSFET

Chapter: [09-09](../chapters/09-09-long-channel-mosfet.md) · Worked solutions: [09-09 solutions](../solutions/09-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** n-channel devices at 300 K unless stated; $n_i$ = 1.0 × 10¹⁰ cm⁻³, $V_T$ = 25.852 mV, $\varepsilon_s$ = 11.7ε₀, $\varepsilon_{ox}$ = 3.9ε₀. Oxide thicknesses are SiO₂-equivalent. Use the bulk-charge model of chapter §3.2–3.3 with $m = 1 + 3T_{ox}/W_{d\max}$ unless a problem gives $m$ or says "square law" ($m$ = 1). Surface mobility, where needed, follows Hu's fit $\mu_{ns} = 540/[1 + (\mathcal E_{\text{eff}}/0.9\text{ MV/cm})^{1.85}]$ cm²/V·s with $\mathcal E_{\text{eff}} = (V_{GS} + V_{TH} + 0.2\text{ V})/6T_{ox}$. "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-09.1 [A]

**Regions and currents.** A square-law NMOS has $\mu_nC_{ox}(W/L)$ = 1.0 mA/V² and $V_{TH}$ = 0.5 V. Find the region and the drain current for ($V_{GS}$, $V_{DS}$) = (a) (0.4 V, 1 V); (b) (1.5 V, 0.2 V); (c) (1.5 V, 2 V).

### Problem 09-09.2 [A]

**Sizing a switch.** With a 2 nm oxide and a channel mobility of 300 cm²/V·s, what $W/L$ gives an on-resistance of 100 Ω (small $V_{DS}$) at 0.7 V overdrive?

### Problem 09-09.3 [A]

**Matching an NMOS and a PMOS.** The NMOS of the worked examples has a channel mobility of 315.1 cm²/V·s. A PMOS of the same length, oxide and overdrive has a hole mobility of 100 cm²/V·s. How much wider must it be to carry the same saturation current (same $m$)?

### Problem 09-09.4 [B]

**The bulk-charge factor at higher doping.** A device has $N_A$ = 10¹⁸ cm⁻³ and a 2 nm oxide. Find $\phi_B$, $W_{d\max}$ and $m$, then $V_{Dsat}$ at 0.6 V overdrive. By what factor does the square law overestimate $I_{Dsat}$?

### Problem 09-09.5 [B]

**Body effect.** For $N_A$ = 10¹⁷ cm⁻³ and a 5 nm oxide, find $C_{ox}$, $\gamma$ and the linear body-effect coefficient, and the threshold shift at $V_{SB}$ = 0.5, 1 and 2 V.

### Problem 09-09.6 [B]

**Mobility degradation.** A device with a 2 nm oxide and $V_{TH}$ = 0.35 V is operated at $V_{GS}$ = 0.8, 1.2 and 1.8 V. (a) Find the effective field and the electron surface mobility at each. (b) By what factor does $I_{Dsat}$ rise from 0.8 V to 1.8 V with the varying mobility, against a constant mobility?

### Problem 09-09.7 [B]

**Is it long?** Using the worked-example transistor's $\mu_{ns}$, $C_{ox}$ and $m$, what width gives 1 mA at 0.8 V overdrive with $L$ = 0.5 µm? By what factor is the average field at saturation below $2v_{sat}/\mu_{ns}$ ($v_{sat}$ = 8 × 10⁶ cm/s, Hu's inversion-layer value)? Is the long-channel model still adequate?

### Problem 09-09.8 [B]

**Channel-length modulation against length.** With $N_A$ = 5 × 10¹⁷ cm⁻³ and $V_{DS} - V_{Dsat}$ = 0.5 V, estimate the pinched-off length, and its fraction of $L$ for $L$ = 0.5, 1 and 2 µm.

### Problem 09-09.9 [B]

**Transconductance efficiency.** For a square-law device in strong inversion, find $g_m/I_D$ at overdrives of 0.1, 0.2 and 0.5 V. For $m$ = 1.3, find the weak-inversion limit $1/(mV_T)$ and the overdrive at which the strong-inversion formula would reach it.

### Problem 09-09.10 [B]

**Cutoff frequency against length.** With $\mu_n$ = 300 cm²/V·s, $m$ = 1.2 and 0.5 V overdrive, find the long-channel $f_T$ for $L$ = 2, 1 and 0.5 µm.

### Problem 09-09.11 [B]

**Leakage and threshold.** (a) Find the subthreshold swing for $m$ = 1.1 and 1.3. (b) For $m$ = 1.3, $W/L$ = 10 and Hu's current-defined threshold, find $I_{off}$ for $V_{TH}$ = 0.3 V. (c) By what factor does raising $V_{TH}$ to 0.45 V cut the leakage?

### Problem 09-09.12 [C]

**Hot leakage.** The device of Problem 09-09.11(b) ($m$ = 1.3, $V_{TH}$ = 0.3 V at 300 K) is heated to 85 °C. Assume the threshold falls by 1 mV/K and that the current-defined threshold convention still holds. Find the swing at 85 °C, the new threshold, the off-current at each temperature, and the ratio.

### Problem 09-09.13 [B]

**Gate capacitance and Miller.** The worked-example transistor ($W$ = 10 µm, $L$ = 1 µm, $C_{ox}$ = 863.3 nF/cm²) has 2 fF of gate–drain overlap and 2 fF of gate–source overlap. In saturation, find $C_{gs}$. If it drives a load giving a voltage gain of −10, find the input capacitance, including the Miller multiplication of $C_{gd}$.

### Problem 09-09.14 [C]

**Exact bulk charge at heavy doping (numerical).** Repeat Example 09-09.4 with $N_A$ = 2 × 10¹⁸ cm⁻³ (4 nm oxide, $V_{TH}$ = 0.4 V, $V_{GS}$ = 1.2 V). Find $m$, $\gamma$, $V_{Dsat}$ from both models, and how far the $m$-model underestimates $I_{Dsat}$.

### Problem 09-09.15 [C]

**An amplifier transistor.** Design an NMOS for 100 µA at 0.2 V overdrive with $L$ = 1 µm, $\mu_nC_{ox}$ = 272.0 µA/V² ($C_{ox}$ = 863.3 nF/cm²) and $m$ = 1.25. Take $\lambda$ = 0.04 V⁻¹. Find $W$, $g_m$, $r_o$, the intrinsic gain, $C_{gs}$ and $f_T$.

---

## Objective coverage

| Learning objective (chapter 09-09) | Problems |
|---|---|
| 1. Gradual-channel I–V, linear and saturation | 1, 2, 3, 4, 7 |
| 2. Body effect and exact bulk charge | 4, 5, 14 |
| 3. Surface mobility | 6 |
| 4. Channel-length modulation, output resistance | 8, 15 |
| 5. Small-signal parameters | 9, 10, 13, 15 |
| 6. Subthreshold conduction and leakage | 11, 12 |
