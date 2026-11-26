# Problems 25-11 · Test: ATE, Wafer Sort, Burn-In and Binning

Chapter: [25-11](../chapters/25-11-test-ate-sort-burn-in.md) · Worked solutions: [25-11 solutions](../solutions/25-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Cost per die $r(T_N + t_i)/N$; per good die divide by yield; multisite efficiency $\eta = 1 - (T_N - T_1)/((N - 1)T_1)$.
- Weak subpopulation $F_w(t) = 1 - \exp[-(t/\eta_w)^\beta]$; burn-in ages parts by $AF\,t_b$; target $AF\,t_b = \eta_w[\ln(p_w/q)]^{1/\beta}$.
- Speed bins and guard bands as in Examples 25-11.5 and 25-11.6 unless stated.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-11-lab/testcost.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-11.1 [A]

**Measured multisite.** A die tests in 1.5 s alone and eight dies test in 2.4 s together (assumed). Find the multisite efficiency and the throughput gain.

### Problem 25-11.2 [B]

**Eight sites.** At $300 per hour with 0.5 s of index time (assumed), what does Problem 25-11.1's eight-site setup cost per die?

### Problem 25-11.3 [A]

**A test-time budget.** A single-site test cell costs $250 per hour. What is the longest test (ignoring index time) that keeps test cost below 2 cents per die?

### Problem 25-11.4 [B]

**Burn-in acceleration.** Burn-in raises the junction from 55 to 125 °C (activation energy 0.7 eV) and the supply by 0.2 V with a voltage acceleration of $e^{\gamma\Delta V}$, γ = 5 V⁻¹ (assumed). Find (a) the thermal factor, (b) the total factor and (c) the burn-in hours equivalent to 1,200 use hours.

### Problem 25-11.5 [C]

**A shallower weak population.** *(lab)* Repeat Example 25-11.3 with β = 0.3. Find (a) the fraction removed by 1,200 use-equivalent hours, (b) the weak parts shipped, and (c) the burn-in hours at AF = 50 needed for 100 ppm. Comment.

### Problem 25-11.6 [A]

**The yield cost of burn-in.** What fraction of all production does Example 25-11.3's burn-in remove?

### Problem 25-11.7 [B]

**Tighter process.** *(lab)* Repeat Example 25-11.5(a, b) with σ = 0.10 GHz. Why does revenue rise even though the top bin shrinks?

### Problem 25-11.8 [C]

**Setting a guard band.** *(lab)* For Example 25-11.6's population and tester, what guard band limits escapes to 100 ppm, and what overkill results?

### Problem 25-11.9 [A]

**Advantest.** From R-616: FY2024 sales ¥779.7 billion, FY2025 ¥1,128.6 billion with operating income ¥499.1 billion, and an FY2026 forecast of ¥1,863.0 billion. Find (a) FY2025 growth, (b) the operating margin and (c) the forecast growth for FY2026.

### Problem 25-11.10 [A]

**Teradyne.** Q3 2026 revenue was $1,306 million, against $769 million a year earlier, with $1,072 million from semiconductor test [R-617]. Find the growth and the semiconductor-test share.

### Problem 25-11.11 [A]

**The ATE market.** If the CY2025 ATE market was $9.0 billion after 50% growth [R-618], what was CY2024's?

### Problem 25-11.12 [B]

**Why sort?** A wafer has 1,000 dies at 86% yield; packaging costs $3 per die; sort costs $0.05 per die and catches 95% of bad dies (all assumed). Find the packaging money wasted per wafer without sort, the cost with sort (sort plus wasted packaging), and the saving.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Test flow | 12 |
| 2. Test cost and multisite | 1, 2, 3 |
| 3. Burn-in | 4, 5, 6 |
| 4. Binning, guard bands, escapes and overkill | 7, 8 |
| 5. Test market data | 9, 10, 11 |
