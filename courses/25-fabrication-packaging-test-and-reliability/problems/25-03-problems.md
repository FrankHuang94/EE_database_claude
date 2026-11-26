# Problems 25-03 · Deposition, Etch, CMP, Implant and Metrology

Chapter: [25-03](../chapters/25-03-deposition-etch-cmp-implant-metrology.md) · Worked solutions: [25-03 solutions](../solutions/25-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- $k$ = 8.61733 × 10⁻⁵ eV/K; $q$ = 1.6022 × 10⁻¹⁹ C; Faraday's constant 96,485 C/mol; 1 psi = 6,895 Pa.
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

### Problem 25-03.15 [C]

**Two-step diffusion: predeposition and drive-in.** Before ion implantation, junctions were made by diffusion from the surface, and the same mathematics still describes in-diffusion from doped films and gas-phase doping. A boron predeposition holds the surface at solid solubility, $C_s$ = 2.5 × 10²⁰ cm⁻³ (assumed), for 20 min at 950 °C into an n-type wafer with $N_B$ = 1.0 × 10¹⁶ cm⁻³. The source is then removed and the wafer is driven in for 60 min at 1100 °C, with the surface treated as reflecting (no dopant leaves). Use the intrinsic boron diffusivity of the conventions throughout.

(a) Show that $C(x,t) = C_s\,\operatorname{erfc}[x/(2\sqrt{Dt})]$ solves the diffusion equation $\partial C/\partial t = D\,\partial^2C/\partial x^2$ with $C(0,t) = C_s$ and $C(x,0) = 0$ for $x > 0$, and that the dose it puts in is $Q = 2C_s\sqrt{Dt/\pi}$.

(b) Find $D$, $\sqrt{Dt}$, the dose and the junction depth after the predeposition.

(c) Find $D$ during the drive-in and the ratio of the drive-in $Dt$ to the predeposition $Dt$. Why does that ratio justify treating the predeposited dose as a sheet at the surface?

(d) For that sheet, the drive-in profile is $C(x,t) = [Q/\sqrt{\pi Dt}]\,e^{-x^2/4Dt}$. Find the surface concentration and the junction depth after the drive-in.

(e) Name two reasons the real junction would be deeper than (d) predicts.

### Problem 25-03.16 [B]

**Did the anneal activate the implant?** A boron implant of 2.0 × 10¹⁵ cm⁻² into an n-type wafer is measured with a collinear four-point probe ([09-03](../../09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md) derives $R_s = (\pi/\ln 2)\,V/I$ for a sheet much thinner than the probe spacing and much wider than the array). At a forced current of 1.00 mA the inner probes read 41.7 mV after a low-temperature anneal and 16.2 mV after a spike anneal. Assume an average hole mobility of 50 cm²/V·s in the layer and that only active (substitutional) boron conducts.

(a) Find the sheet resistance after each anneal.

(b) Show that a layer with active dose $Q_a$ (cm⁻²) and uniform mobility has $R_s = 1/(q\mu Q_a)$, then find the active dose and the activated fraction after each anneal.

(c) A resistor 1.0 µm wide and 20 µm long is made in the spike-annealed layer. Find its resistance, ignoring the contacts.

(d) Why does the fab use four probes rather than measuring $V/I$ across two?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. CVD regimes and ALD | 1, 2, 3 |
| 2. Plating, etch, overetch and selectivity | 4, 5, 6 |
| 3. CMP and pattern density | 7, 8 |
| 4. Implant, junctions and thermal budget | 9, 10, 11, 15, 16 |
| 5. Measurement noise and gauges | 12, 16 |
| 6. The equipment market | 13 |
| (Epitaxy and strain, §3.3) | 14 |
