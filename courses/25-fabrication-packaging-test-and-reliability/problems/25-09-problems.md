# Problems 25-09 · Reliability Physics

Chapter: [25-09](../chapters/25-09-reliability-physics.md) · Worked solutions: [25-09 solutions](../solutions/25-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- $k$ = 8.617 × 10⁻⁵ eV/K and $T$ = °C + 273.15 unless a problem says otherwise.
- Black's equation $MTTF = Aj^{-n}e^{E_a/kT}$; two-phase local exponent $n = (2 + x)/(1 + x)$ with $x = j/j^*$.
- TDDB: E model $e^{-\gamma E}$, 1/E model $e^{G/E}$, power law $E^{-m}$; chip percentile life $\eta(A_{chip}/A_{test})^{-1/\beta}(-\ln(1 - F))^{1/\beta}$.
- HTOL bound $\lambda_U = \chi^2_{CL,\,2f+2}/(2NtAF)$; HBM 100 pF and 1.5 kΩ.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-09-lab/reliability.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-09.1 [A]

**Acceleration.** Find the acceleration factor from 85 °C use to a 150 °C stress for activation energies of (a) 0.7 eV and (b) 1.0 eV.

### Problem 25-09.2 [B]

**A power-grid wire.** An EM test at 300 °C and 5 MA/cm² gives a 200 h median; the use condition is 110 °C at 0.5 MA/cm² (assumed). With $E_a$ = 0.9 eV and $n$ = 2, find (a) the total acceleration factor and (b) the use median in hours and years. (c) If lives are lognormal with σ = 0.4 (assumed), how long until 0.01% of such lines fail?

### Problem 25-09.3 [C]

**The exponent.** (a) Derive the local exponent $n(j)$ of the two-phase model $MTTF = Bj^{-2} + Cj^{-1}$. (b) At what $j/j^*$ does a test measure $n$ = 1.25? (c) $n$ = 1.75?

### Problem 25-09.4 [B]

**A short stub.** With $(jL)_c$ = 3,000 A/cm, what current density can an 8 µm via-to-via segment carry without electromigration? How many times a 1 MA/cm² long-line limit (assumed) is that?

### Problem 25-09.5 [B]

**Different data.** *(lab)* Test capacitors give 10 s at 10 MV/cm and 1,000 s at 8 MV/cm (assumed). Fit (a) γ, (b) G and (c) m, and extrapolate each model to 5 MV/cm (d).

### Problem 25-09.6 [C]

**A shallower Weibull.** *(lab)* Repeat Example 25-09.5 with β = 1.2. Find (a) the scale factor and (b) the required characteristic life, and (c) say which of Example 25-09.4's extrapolations pass.

### Problem 25-09.7 [B]

**A longer BTI test.** Extend Example 25-09.6's test to 100,000 s. What shift does each exponent ($n_t$ = 1/6 and 1/4) predict there? Why does the longer test help?

### Problem 25-09.8 [B]

**A 4 kV zap.** Repeat Example 25-09.7 for 4 kV: find (a) the peak current, (b) the peak pad voltage, and (c) the largest clamp on-resistance for an 8 V limit.

### Problem 25-09.9 [A]

**Latch-up loop gain.** A parasitic thyristor has an npn current gain of 5 and a pnp gain of 0.5 (assumed). (a) Is the loop gain above one? (b) If taps and guard rings reduce both effective gains by the same factor, what factor brings the product to one?

### Problem 25-09.10 [B]

**Other outcomes.** For TI's HTOL test (7,859 units, 1,000 h, AF = 78.6), find the FIT bound (a) with one failure at 60% confidence and (b) with no failures at 90% confidence.

### Problem 25-09.11 [B]

**Sizing the test.** How many units must a 1,000 h, zero-failure HTOL at AF = 78.6 include to demonstrate 10 FIT at 60% confidence?

### Problem 25-09.12 [B]

**Hotter still.** Repeat Example 25-09.9 at 105 °C: find the total and the single-0.7 eV estimate, and the underestimate.

### Problem 25-09.13 [A]

**What 60% means.** *(lab)* For a zero-failure HTOL, what is the probability of passing if the true rate (a) equals the 60% bound and (b) is half of it?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Electromigration, Black and Blech | 2, 3, 4 |
| 2. TDDB models | 5 |
| 3. Weibull scaling to chips and ppm | 2, 6 |
| 4. BTI extrapolation | 7 |
| 5. ESD clamps and latch-up | 8, 9 |
| 6. HTOL FIT and summing mechanisms | 1, 10, 11, 12, 13 |
