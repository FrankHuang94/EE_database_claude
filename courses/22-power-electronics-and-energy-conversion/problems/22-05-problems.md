# Problems 22-05 · Magnetics Design

Chapter: [22-05](../chapters/22-05-magnetics-design.md) · Worked solutions: [22-05 solutions](../solutions/22-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unless stated, the core is the chapter's TDK ETD 34/17/11 set in N87: $\ell_e$ = 78.6 mm, $A_e$ = 97.1 mm², ungapped $A_L$ = 2600 nH (so $\ell_e/\mu_e$ = 0.0469 mm), winding area 122 mm², MLT 60.5 mm, $B_{sat}$ = 390 mT at 100 °C. Copper is at 100 °C ($\rho$ = 22.66 nΩ·m) unless stated. N87 Steinmetz exponents: $\alpha$ = 1.635, $\beta$ = 2.253. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-05-lab/magnetics.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-05.1 [A]

**Turns from $A_L$.** The ETD34 set with a 0.20 mm gap has $A_L$ = 482 nH [data sheet]. (a) How many turns give 50 µH (before rounding)? (b) What inductance do 11 turns give? (c) What $A_L$ does the ideal (no-fringing) model predict for this gap?

### Problem 22-05.2 [A]

**Where the energy lives.** For the ETD34 core, find the fraction of the stored energy in the gap for gaps of (a) 0.1 mm and (b) 1.0 mm.

### Problem 22-05.3 [A]

**Flux density from the circuit.** A 22 µH inductor has 15 turns on a core of 52 mm² cross-section. Find (a) the peak flux density at 8 A and (b) the current at which it reaches 390 mT.

### Problem 22-05.4 [B]

**Turns and gap for a 100 µH inductor.** *(lab)* Design a 100 µH inductor on the ETD34 for a peak current of 6 A and $B_{max}$ = 0.25 T. Find (a) the turns before rounding, then with 25 turns (b) $B_{pk}$, (c) the ideal-model gap, (d) the required $A_L$ and (e) the gap from TDK's fit $A_L = 153\,s^{-0.713}$ nH.

### Problem 22-05.5 [A]

**Steinmetz scaling.** With the N87 exponents, by what factor does the core loss change when (a) the frequency doubles at fixed $B_{pk}$, (b) $B_{pk}$ doubles at fixed frequency and (c) a transformer at fixed voltage and turns has its frequency doubled?

### Problem 22-05.6 [B]

**Duty cycle and core loss.** *(lab)* For the iGSE triangle-wave bracket $D^{1-\alpha} + (1 - D)^{1-\alpha}$ with the N87 $\alpha$, find the bracket at (a) $D$ = 1/12 (a 12 V to 1 V buck) and (b) $D$ = 0.75, and their ratios to the bracket at $D$ = 0.5, (c) and (d).

### Problem 22-05.7 [B]

**Laminations at 50 Hz and 20 kHz.** A silicon-steel lamination is 0.35 mm thick with resistivity 0.5 µΩ·m and density 7650 kg/m³ (both assumed). Find its classical eddy loss (a) per unit volume and (b) per kilogram at 50 Hz and 1.5 T, and (c) per unit volume at 20 kHz and 0.1 T.

### Problem 22-05.8 [A]

**Skin depth at 200 kHz.** Find (a) the skin depth in copper at 200 kHz and 100 °C and (b) the largest round-wire diameter, taken as $2\delta$, that avoids heavy skin effect.

### Problem 22-05.9 [B]

**Dowell's factor.** *(lab)* A winding section has three layers of 0.2 mm copper foil carrying a 100 kHz sinusoid at 100 °C. Find (a) $\Delta$, (b) $F_R$ from Dowell's formula and (c) $F_R$ from the thin-layer approximation.

### Problem 22-05.10 [A]

**Hot copper.** A winding measures 10 mΩ at 20 °C. Find (a) its resistance at 100 °C and (b) its loss at 5 A RMS when hot.

### Problem 22-05.11 [C]

**Eddy loss in a round pole.** (a) Derive the classical eddy-current loss density of a long round rod of diameter $d$ and resistivity $\rho$ carrying a uniform axial sinusoidal flux density of peak $B_{pk}$ at frequency $f$. (b) What is its ratio to the slab formula with $t = d$? (c) Evaluate it for the ETD34's 11.1 mm 3C95 pole at 100 kHz and 0.2 T, with $\rho$ = 5 Ω·m.

### Problem 22-05.12 [C]

**Sizing a point-of-load inductor.** A 12 V to 5 V, 10 A buck switches at 500 kHz with a 40% ripple ratio. Find (a) $L$ and (b) $I_{rms}$. With $K_u$ = 0.4, $J$ = 5 A/mm² and $B_{max}$ = 0.25 T, find (c) the required area product and (d) the $K_g$ required for 0.2 W of copper loss. (e) By what factor does the ETD34's $K_g$ (1.90 × 10⁻¹¹ m⁵) exceed (d)? What does that tell you?

### Problem 22-05.13 [C]

**Optimum flux swing.** A transformer has 0.8 W of core loss and 1.6 W of copper loss at $\Delta B$ = 0.1 T, with $\beta$ = 2.5 (assumed). Find (a) the optimum $\Delta B$, (b) the core and (c) copper losses there, (d) the total, (e) the ratio of core to copper loss and (f) the factor by which the turns change.

### Problem 22-05.14 [C]

**Leakage in the flyback of Example 22-05.3.** The 32-turn primary occupies a 1.2 mm section and the secondary 0.8 mm, separated by 0.4 mm of insulation tape across the 20.9 mm window breadth (MLT 60.5 mm). Find (a) the leakage inductance and (b) its percentage of $L_m$ = 223 µH. With 22-04's RCD clamp at 200 V and a 128 V reflected voltage, at $I_{pk}$ = 2.52 A and 100 kHz, find (c) the leakage energy per cycle and (d) the clamp loss. Repeat for P/2–S–P/2 interleaving: (e) leakage, (f) percentage, (g) energy and (h) clamp loss.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Magnetic circuit, $A_L$, effective permeability | 1, 4 |
| 2. Energy in the gap, saturation, turns and gap | 2, 3, 4 |
| 3. Core loss: Steinmetz, iGSE, eddy currents | 5, 6, 7, 11 |
| 4. Winding loss: temperature, skin, proximity | 8, 9, 10 |
| 5. Area product, $K_g$, optimum flux swing, leakage | 12, 13, 14 |
| 6. Materials and structures | 7, 11, 14 |
