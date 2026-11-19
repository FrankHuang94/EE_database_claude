# Problems 09-13 · Compound and Wide-Bandgap Semiconductors

Chapter: [09-13](../chapters/09-13-compound-and-wide-bandgap-semiconductors.md) · Worked solutions: [09-13 solutions](../solutions/09-13-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 300 K unless stated; $V_T$ = 25.852 mV. Material values as in the chapter's §3.1 table: 4H-SiC $\varepsilon_r$ = 9.96 and $\mu_n$ = 1000 cm²/V·s; silicon $\varepsilon_r$ = 11.7 with the handbook mobility model of 09-03; GaN and AlN constants from Vurgaftman's Table X (chapter §3.4). Breakdown uses the ionization integral of 09-06 with the fits of chapter §3.3, and $V_B = \mathcal E_mW/2$ (built-in potential neglected). "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-13.1 [A]

**GaN's intrinsic carriers.** From the gaps alone (3.435 eV and 1.12 eV), estimate $n_i$(GaN)/$n_i$(Si) at 300 K.

### Problem 09-13.2 [A]

**GaN's gap against temperature.** Using Vurgaftman's Varshni parameters for wurtzite GaN ($E_g(0)$ = 3.507 eV, α = 0.909 meV/K, β = 830 K), find the gap at 400 K and at 77 K, and the shift from 300 K to 400 K.

### Problem 09-13.3 [B]

**A 3.3 kV drift layer, closed form.** Take a fixed critical field of 2.5 MV/cm for 4H-SiC. For a 3300 V device with a triangular field, find the drift doping, thickness and specific on-resistance, and check the last with Baliga's formula.

### Problem 09-13.4 [B]

**650 V designs (numerical).** Repeat Example 09-13.3 for a 650 V blocking voltage in silicon and in 4H-SiC: doping, critical field, thickness, silicon mobility, specific on-resistance and the ratio.

### Problem 09-13.5 [B]

**How on-resistance scales with voltage.** From the 650 V and 1200 V designs (Problem 09-13.4 and Example 09-13.3), find the exponent $n$ in $R_{on,sp} \propto V_B^n$ for each material. Why is it above 2?

### Problem 09-13.6 [B]

**Less aluminum.** Find the polarization bound charge and the sheet density for an Al₀.₁₅Ga₀.₈₅N barrier on gallium-face GaN, using the method of Example 09-13.4.

### Problem 09-13.7 [A]

**A HEMT's current ceiling.** A 2DEG of 10¹³ cm⁻² carries electrons at an average velocity of 10⁷ cm/s (assumed). Find the current per centimeter and per millimeter of gate width.

### Problem 09-13.8 [A]

**How much heterojunction?** What gap difference multiplies the attainable HBT gain by 100 at 300 K, and at 400 K?

### Problem 09-13.9 [B]

**Hot SiC against cool silicon.** From the gaps alone, compare the intrinsic concentration of 4H-SiC at 600 K with that of silicon at 300 K.

### Problem 09-13.10 [B]

**From 200 mm to 300 mm.** Using the gross-die estimate, find the dies per wafer on 200 mm and 300 mm wafers for 25 mm² and 100 mm² dies, and the die ratio in each case. Why does the larger die gain more?

### Problem 09-13.11 [B]

**A normally-on HEMT.** The AlGaN barrier of Example 09-13.4 is 20 nm thick, with a relative permittivity of 9 (assumed). Treating it as a parallel-plate capacitor, find its capacitance per area, the change in sheet density per volt of gate bias, and the gate voltage needed to empty a 1.39 × 10¹³ cm⁻² channel.

### Problem 09-13.12 [C]

**Does 200 mm pay?** A 150 mm SiC wafer costs 1.0 (in arbitrary units) and a 200 mm wafer 1.4. Using the die counts of Example 09-13.7, find the ratio of cost per die (200 mm to 150 mm) at equal yield. If the new 200 mm line yields 70% against 85% on 150 mm, what is the ratio of cost per good die, and what 200 mm yield breaks even?

---

## Objective coverage

| Learning objective (chapter 09-13) | Problems |
|---|---|
| 1. Material properties and their roles | 1, 2, 9 |
| 2. Breakdown and Baliga's limit | 3, 4, 5 |
| 3. AlGaN/GaN polarization | 6, 11 |
| 4. HEMT and HBT | 7, 8, 11 |
| 5. Substrates, wafers and cost | 10, 12 |
