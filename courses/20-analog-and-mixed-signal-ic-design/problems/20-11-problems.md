# Problems 20-11 · Layout, Matching and PVT Variation

Chapter: [20-11](../chapters/20-11-layout-matching-pvt.md) · Worked solutions: [20-11 solutions](../solutions/20-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Pelgrom coefficients describe the difference of a pair: σ(ΔV_TH) = $A_{VT}/\sqrt{WL}$, σ(Δβ/β) = $A_\beta/\sqrt{WL}$. Mirror: σ(ΔI/I)² = $(g_m/I_D)^2\sigma(\Delta V_{TH})^2 + \sigma(\Delta\beta/\beta)^2$. Pair: σ(V_os)² = σ(ΔV_TH)² + [σ(Δβ/β)/(g_m/I_D)]². Problems marked *(lab)* can be checked with `labs/20-11-lab/matching.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-11.1 [A]

**A smaller process.** With $A_{VT}$ = 2.5 mV·µm, find σ(ΔV_TH) for a pair of 4 µm × 0.5 µm devices.

### Problem 20-11.2 [A]

**Area for a quarter.** By what factor must the gate area grow to cut a pair's random mismatch to a quarter?

### Problem 20-11.3 [B]

**A mirror.** A mirror's devices have σ(ΔV_TH) = 2 mV and σ(Δβ/β) = 0.5% and run at $g_m/I_D$ = 8 V⁻¹. Find σ(ΔI/I).

### Problem 20-11.4 [B]

**A pair.** The same devices form a differential pair at $g_m/I_D$ = 15 V⁻¹. Find σ(V_os).

### Problem 20-11.5 [A]

**One device or two?** A pair has σ(ΔV_TH) = 1.77 mV. What is the standard deviation of one device's threshold from the mean?

### Problem 20-11.6 [B] *(lab)*

**Gradients on a 5 µm pitch.** A threshold gradient of 0.02 mV/µm runs along a row with a 5 µm pitch. Find the systematic offset of AB placement and of ABBA placement; then add a quadratic term of 2 × 10⁻⁴ mV/µm² and find ABBA's residual.

### Problem 20-11.7 [B] *(lab)*

**Eight cells.** Show that the pattern ABBABAAB cancels both linear and quadratic gradients: compute the difference of the cells' average positions and of their average squared positions (in pitches).

### Problem 20-11.8 [B]

**Yield.** An offset with σ = 0.8 mV must stay within ±2 mV. What fraction of parts fail?

### Problem 20-11.9 [B]

**Two more bits.** A mismatch-limited converter goes from 8-bit to 10-bit accuracy at the same speed and swing. By what factor does the power of its mismatch-limited stages grow?

### Problem 20-11.10 [B]

**A rarer failure.** How many failure-free Monte Carlo runs demonstrate a failure rate below 0.1% with 95% confidence? Compare with the rule of three.

### Problem 20-11.11 [A] *(lab)*

**Fifty runs.** What is the 95% confidence interval of a standard deviation estimated from 50 runs?

### Problem 20-11.12 [C]

**Trim or drift?** A 1.2 V bandgap is trimmed at 25 °C in steps of 0.5 mV. Its temperature drift after trimming is 10 ppm/°C. Find the trim's residual error (standard deviation, uniform within ±½ step) and the drift over −40 °C to 125 °C. Which dominates?

### Problem 20-11.13 [A]

**IR drop in a mirror.** A 1:1 current mirror carries 1 mA per side at $g_m/I_D$ = 8 V⁻¹. The output device's source wiring has 5 Ω more resistance to ground than the reference device's.
(a) What gate–source voltage error does the drop create, and what current error results to first order?
(b) Find the exact current error, including the degeneration the extra resistance provides.
(c) For a 0.1% error, how many squares of 0.05 Ω/sq metal may the unmatched part of the wiring have? What is the better fix?

### Problem 20-11.14 [B]

**Latch-up and a guard ring.** In a CMOS layout the parasitic NPN (n+ source, p-substrate, n-well) has β = 5 and the PNP (p+ source, n-well, p-substrate) has β = 2. The substrate resistance from the injection point to the nearest substrate tap is 500 Ω; a bipolar's base–emitter junction turns on at about 0.7 V.
(a) Can the parasitic thyristor sustain itself once triggered? Explain with the loop gain.
(b) What current injected into the substrate turns the NPN on?
(c) A guard ring cuts the substrate resistance to 20 Ω. What injected current is now needed?
(d) An I/O pin overshoots its supply and injects 10 mA through its ESD diode. Which layout latches? Why do guard rings also help analog blocks that never see injection?

### Problem 20-11.15 [C]

**Design a matched mirror array.** A 1:1 bias mirror must reach σ(ΔI/I) ≤ 0.1% from random mismatch and a systematic gradient error below 0.05%, with only 0.3 V of headroom for each device ($V_{DS,sat} \approx 2/(g_m/I_D)$). The process has $A_{VT}$ = 3.5 mV·µm and $A_\beta$ = 1 %·µm; across the array the threshold has a linear gradient of 0.05 mV/µm and a quadratic term of 5 × 10⁻⁴ mV/µm².
(a) Write the gate area each device needs as a function of $g_m/I_D$. Evaluate it at 5 and 10 V⁻¹, then choose the $g_m/I_D$ the headroom allows and find the area.
(b) Each device is split into 4 unit cells in one row with a 10 µm pitch. Placed side by side (AAAABBBB), what is the gradient error in current?
(c) Find the error of ABBAABBA. Does it meet the budget?
(d) Choose a pattern that meets the budget and justify it. What is the total active area, and what else belongs at the ends of the row?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Pelgrom's law and sizing | 1, 2, 5, 15 |
| 2. Mirrors and pairs | 3, 4, 15 |
| 3. Speed–accuracy–power | 9 |
| 4. Gradients and placement | 6, 7, 15 |
| 5. Corners, Monte Carlo, yield and trim | 8, 10, 11, 12 |
| 6. Guard rings, latch-up and extraction | 13, 14 |
