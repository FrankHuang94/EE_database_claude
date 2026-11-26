# Problems 25-03 · Deposition, Etch, CMP, Implant and Metrology

Chapter: [25-03](../chapters/25-03-deposition-etch-cmp-implant-metrology.md) · Worked solutions: [25-03 solutions](../solutions/25-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- $k$ = 8.617 × 10⁻⁵ eV/K; $q$ = 1.602 × 10⁻¹⁹ C; Faraday's constant 96,485 C/mol; 1 psi = 6,895 Pa.
- Boron diffusivity $D = 0.76\,e^{-3.46/kT}$ cm²/s; implanted profiles are Gaussian and spread as $\Delta R_p'^2 = \Delta R_p^2 + 2Dt$, ignoring the surface.
- A 300 mm wafer is 707 cm².
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-03-lab/units.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-03.1 [A]

**Which resistance wins?** A CVD process has $h_g$ = 1.0 cm/s and $k_s$ = 20 cm/s (assumed). Find the effective rate constant. Which regime is this, and which knob would you turn to raise the rate?

### Problem 25-03.2 [B]

**The CVD series law.** *(lab)* (a) Derive $v = (C_g/N)\,k_sh_g/(k_s + h_g)$ from the supply and reaction fluxes, and give its two limits. (b) Show that when $k_s = h_g$ the effective constant is half of either. (c) For Example 25-03.1's reaction ($k_s$ = 0.050 cm/s at 650 °C, $E_a$ = 1.5 eV) and $h_g$ = 2.0 cm/s, at what temperature are the two equal?

### Problem 25-03.3 [A]

**A thinner gate dielectric.** An ALD process grows 0.09 nm per 3.0 s cycle (assumed). How many whole cycles reach at least 3.0 nm, and how long do they take?

### Problem 25-03.4 [B]

**Faster plating.** Copper is plated at 20 mA/cm² (assumed). Find (a) the deposition rate in nm/s, (b) the time for 1.5 µm and (c) the total charge for a 300 mm wafer.

### Problem 25-03.5 [B]

**How selective must it be?** An 80 nm film etches at 60 nm/min with ±8% non-uniformity, and the recipe runs 30% past the nominal clearing time (all assumed). What selectivity keeps the stop-layer loss at the fastest point to 1.0 nm or less?

### Problem 25-03.6 [A]

**Wet-etch undercut.** A 300 nm oxide is wet-etched through a resist mask with 10% overetch; the etch is isotropic. (a) How far does it undercut each mask edge? (b) What width remains under a 1.0 µm mask line? (c) Why is wet etching not used for fine patterns?

### Problem 25-03.7 [B]

**Changing the CMP recipe.** With Example 25-03.5's $K_p$, find (a) the removal rate at 3.0 psi and 1.5 m/s and (b) the time to remove 400 nm.

### Problem 25-03.8 [B]

**A denser region.** *(lab)* With Example 25-03.5's blanket conditions, raised features cover 50% of a region (assumed). (a) At what rate are they removed at first? (b) Approximately how long does it take to remove a 300 nm step, if only the raised features are polished until the surface is flat?

### Problem 25-03.9 [B]

**A heavier dose.** A source/drain implant needs 5 × 10¹⁵ cm⁻² on a 300 mm wafer with a 5.0 mA beam, and its straggle is 20 nm (assumed). Find (a) the implant time and (b) the peak concentration.

### Problem 25-03.10 [B]

**A deeper junction.** For Problem 25-03.9's implant with $R_p$ = 50 nm (assumed) into a 10¹⁷ cm⁻³ background, find the junction depth.

### Problem 25-03.11 [C]

**Equivalent thermal budgets.** *(lab)* A furnace step at 1000 °C for 30 min must move to 950 °C. (a) Find the boron diffusivity at 950 °C. (b) How long at 950 °C gives the same $Dt$? (c) Why might a process engineer still prefer the lower temperature?

### Problem 25-03.12 [B]

**Buying a better gauge.** For Example 25-03.8's specification (20.0 ± 1.5 nm) and process (σ = 0.40 nm), (a) what measurement noise gives $P/T$ = 0.10? (b) What spread would the process then appear to have?

### Problem 25-03.13 [A]

**Backing out the base year.** SEMI forecast 2026 DRAM equipment at $38.8 B (+39.0%) and foundry/logic at $78.0 B (+18.9%) [R-568]. Find (a) each segment's 2025 value and (b) the increase in total WFE from 2025 to 2026.

### Problem 25-03.14 [B]

**Strained SiGe.** Using Vegard's law with $a_{Si}$ = 0.5431 nm and $a_{Ge}$ = 0.5658 nm, find (a) the relaxed lattice constant of Si₀.₇Ge₀.₃ and (b) its mismatch to silicon in percent. (c) Is a SiGe film grown on silicon under tension or compression in the plane?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. CVD regimes and ALD | 1, 2, 3 |
| 2. Plating, etch, overetch and selectivity | 4, 5, 6 |
| 3. CMP and pattern density | 7, 8 |
| 4. Implant, junctions and thermal budget | 9, 10, 11 |
| 5. Measurement noise and gauges | 12 |
| 6. The equipment market | 13 |
| (Epitaxy and strain, §3.3) | 14 |
