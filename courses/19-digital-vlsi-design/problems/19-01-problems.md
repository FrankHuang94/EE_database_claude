# Problems 19-01 · The CMOS Inverter: Static Characteristics

Chapter: [19-01](../chapters/19-01-cmos-inverter-static.md) · Worked solutions: [19-01 solutions](../solutions/19-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Square-law transistors of equal length unless stated, with $k = \mu C_{ox}W/L$ and $I_{D,sat} = \tfrac12kV_{ov}^2(1 + \lambda V_{DS})$; λ = 0 unless given; $r = k_n/k_p$. Noise margins use the unity-gain points, with $V_{OL}$ = 0 and $V_{OH} = V_{DD}$. Thermal voltage $V_T = kT/q$ (25.85 mV at 300 K). Problems marked *(lab)* can be checked with `labs/19-01-lab/inverter.py` or `vtc.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-01.1 [A]

**Which region?** An inverter has $V_{DD}$ = 1.0 V and $V_{TN} = \lvert V_{TP}\rvert$ = 0.3 V. For each input, say whether each transistor is off, linear or saturated, and give the output if it is exact: (a) $V_{in}$ = 0.2 V; (b) $V_{in}$ = 0.5 V for a symmetric inverter (λ = 0); (c) $V_{in}$ = 0.8 V.

### Problem 19-01.2 [A]

**Switching threshold.** $V_{DD}$ = 1.8 V, $V_{TN} = \lvert V_{TP}\rvert$ = 0.5 V and $k_n/k_p$ = 3. Find $V_M$.

### Problem 19-01.3 [A]

**Sizing.** A process has $V_{TN}$ = 0.45 V, $\lvert V_{TP}\rvert$ = 0.5 V and $\mu_n/\mu_p$ = 2.8, with $V_{DD}$ = 1.8 V. What $k_n/k_p$ and what $W_p/W_n$ put $V_M$ at 0.9 V?

### Problem 19-01.4 [B]

**Symmetric noise margins.** A symmetric inverter has $V_{DD}$ = 1.8 V and $V_{TN} = \lvert V_{TP}\rvert$ = 0.45 V. Find $V_{IL}$, $V_{IH}$, the noise margins and the width of the region of gain.

### Problem 19-01.5 [B]

**An unbalanced inverter.** *(lab)* The inverter of Problem 4 is built with $r$ = 4. Find $V_M$, $V_{IL}$, $V_{IH}$ and both noise margins. Which margin limits the gate?

### Problem 19-01.6 [B]

**Unequal channel-length modulation.** *(lab)* A symmetric inverter ($V_{DD}$ = 1.2 V, $V_{TN} = \lvert V_{TP}\rvert$ = 0.35 V, $k_n = k_p$) has $\lambda_n$ = 0.15 V⁻¹ and $\lambda_p$ = 0.2 V⁻¹. (a) Estimate the gain at $V_M$ with $g_{ds} \approx \lambda I_D$ and $V_M$ = 0.6 V. (b) Find $V_M$ and the gain numerically. (c) Why does $V_M$ move slightly?

### Problem 19-01.7 [B]

**Variation.** Each transistor's threshold varies independently with σ = 25 mV. Find the sensitivities $\partial V_M/\partial V_{TN}$ and $\partial V_M/\partial\lvert V_{TP}\rvert$ and the standard deviation of $V_M$ (a) for $r$ = 1 and (b) for $r$ = 4.

### Problem 19-01.8 [B]

**Regeneration.** *(lab)* A degraded level of 0.55 V drives a chain of symmetric inverters ($V_{DD}$ = 1.2 V, $V_{TN} = \lvert V_{TP}\rvert$ = 0.35 V, λ = 0.05 V⁻¹). Find the first two stage outputs. Why does the second stage's output reach the rail exactly?

### Problem 19-01.9 [A]

**The peak through-current.** In the symmetric inverter of Example 19-01.1 ($k_n = k_p$ = 200 µA/V²), what current flows from $V_{DD}$ to ground when $V_{in} = V_M$? Where else on the transfer curve is the current zero?

### Problem 19-01.10 [C]

**Deriving $V_{IL}$.** Starting from the region-B current balance, derive the closed form $V_{IL} = V_{TN} + \tfrac{t}{1 + t}(V_{DD} - V_{TN} - \lvert V_{TP}\rvert)$ with $t = (2\sqrt{r^2 + 3r} - r)/(r(r + 4))$, check that it gives $(3V_{DD} + 2V_T)/8$ for the symmetric inverter, and evaluate it for $V_{DD}$ = 1.0 V, $V_{TN} = \lvert V_{TP}\rvert$ = 0.3 V and $r$ = 2.

### Problem 19-01.11 [C]

**Velocity-saturated sizing.** A process has $V_{DD}$ = 1.0 V, $V_{TN}$ = 0.30 V and $\lvert V_{TP}\rvert$ = 0.35 V, and at equal widths the NMOS delivers 1.8 times the PMOS's saturated current. Find the $W_p/W_n$ that puts $V_M$ at 0.5 V (a) if the transistors follow the square law and (b) if they follow the alpha-power law with α = 1.4. Explain the difference.

### Problem 19-01.12 [C]

**A subthreshold design.** A symmetric subthreshold inverter has $n$ = 1.3. (a) What supply gives a gain of magnitude 10 at 300 K? (b) What is its minimum supply for gain at 300 K and at 85 °C? (c) Why do practical subthreshold circuits run well above these values?

---

## Objective coverage

| Learning objective (chapter 19-01) | Problems |
|---|---|
| 1. Operating regions of the transfer curve | 1, 9 |
| 2. Switching threshold and sizing | 2, 3, 11 |
| 3. Unity-gain points and noise margins | 4, 5, 10 |
| 4. Gain and regeneration | 6, 8 |
| 5. Variation and the minimum supply | 7, 12 |
