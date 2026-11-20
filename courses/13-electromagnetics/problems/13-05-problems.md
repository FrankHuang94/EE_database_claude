# Problems 13-05 · Plane Waves in Lossless and Lossy Media

Chapter: [13-05](../chapters/13-05-plane-waves.md) · Worked solutions: [13-05 solutions](../solutions/13-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\varepsilon_0$ = 8.854 × 10⁻¹² F/m; $\mu_0$ = 4π × 10⁻⁷ H/m; $c$ = 2.998 × 10⁸ m/s; $\eta_0$ = 376.7 Ω; copper σ = 5.8 × 10⁷ S/m; all media nonmagnetic unless stated; phasors are peak amplitudes with time dependence $e^{j\omega t}$; 1 Np = 8.686 dB.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-05.1 [A]

**Identify the medium.** In a lossless nonmagnetic dielectric, $\vec{E} = 5\cos(2\pi \times 10^9t - 42z)\,\hat{x}$ V/m. Find $\varepsilon_r$, the intrinsic impedance, the amplitude and direction of $\vec{H}$, and the time-average power density.

### Problem 13-05.2 [A]

**Wavelengths.** Find the free-space wavelength at 60 Hz, 2.4 GHz, 28 GHz and 193.4 THz.

### Problem 13-05.3 [A]

**Name the polarization.** For waves travelling in $+z$, classify each and give the hand where it applies: (a) $(\hat{x} + \hat{y})e^{-jkz}$; (b) $(\hat{x} + j\hat{y})e^{-jkz}$; (c) $(\hat{x} + 2j\hat{y})e^{-jkz}$, giving its axial ratio.

### Problem 13-05.4 [A]

**Fields from power density.** A plane wave in air carries 10 W/m². Find the peak $E$ and $H$. What is the intrinsic impedance of a lossless medium with $\varepsilon_r$ = 81?

### Problem 13-05.5 [B]

**Other metals.** Using conductivities of 3.5 × 10⁷ S/m for aluminium and 4.1 × 10⁷ S/m for gold (round handbook values), find each metal's skin depth at 1 GHz and the aluminium surface resistance.

### Problem 13-05.6 [B]

**How good is "good"?** Show that the ratio of the exact attenuation constant to the good-conductor value $\sqrt{\pi f\mu\sigma}$ depends only on $x = \sigma/\omega\varepsilon$. Find the $x$ at which the good-conductor value is 1% too high, and the frequency below which seawater (σ = 4 S/m, $\varepsilon_r$ = 81) meets that standard.

### Problem 13-05.7 [B]

**A low-loss coax dielectric.** Polyethylene has $\varepsilon_r$ = 2.25 and $\tan\delta$ ≈ 0.0002 at 1 GHz. Find the dielectric attenuation of a TEM wave in it, in Np/m and dB/m.

### Problem 13-05.8 [B]

**A trace's AC resistance.** A copper trace is 0.1 mm wide, 35 µm thick and 10 cm long. Find its DC resistance, and its resistance at 1 GHz assuming the current flows within a skin depth of both broad faces (ignore the edges). What is the ratio?

### Problem 13-05.9 [B]

**How deep can a submarine listen?** For seawater (σ = 4 S/m), find the attenuation in dB/m at 10 kHz, the depth at which a 10 kHz signal has lost 100 dB, and the same depth at 100 Hz.

### Problem 13-05.10 [C]

**Seawater at 1 GHz, exactly.** Compute γ and $\eta_c$ for seawater (σ = 4 S/m, $\varepsilon_r$ = 81) at 1 GHz from the exact formulas. Give α, β, $\lvert\eta_c\rvert$ and its angle.

### Problem 13-05.11 [C]

**Skin-effect loss from the fields.** In a good conductor filling $z > 0$, the current density is $\tilde J(z) = J_0e^{-(1 + j)z/\delta}$. (a) Integrate it to find the current per unit width, and show that the time-average loss per unit area equals $\tfrac12R_s\lvert H_t\rvert^2$, where $H_t$ is the tangential magnetic field at the surface. (b) Find the loss per square metre of a copper surface at 1 GHz with $\lvert H_t\rvert$ = 1 A/m.

### Problem 13-05.12 [B]

**Energy in a plane wave.** Show that the electric and magnetic energy densities of a lossless plane wave are equal, and that the time-average power density equals the time-average total energy density times the speed of light in the medium. Find the energy density of a 10 W/m² wave in air.

### Problem 13-05.13 [C]

**Which loss dominates in a coax?** For the coaxial line of Example 13-03.2 ($a$ = 0.5 mm, $b$ = 1.75 mm, $Z_0$ = 50.08 Ω), with copper conductors and a polyethylene dielectric (Problem 13-05.7), the conductor loss is $\alpha_c = R'/(2Z_0)$ with $R' = (R_s/2\pi)(1/a + 1/b)$. At 1 GHz find $R'$, $\alpha_c$ and $\alpha_d$ in dB/m, and the total.

### Problem 13-05.14 [C]

**Elliptical polarization and mismatch.** A wave has elliptical polarization with axial ratio 2. A linearly polarized antenna is rotated to find the best and worst orientations. What fractions of the wave's power does it capture at each, in dB?

---

## Objective coverage

| Learning objective (chapter 13-05) | Problems |
|---|---|
| 1. Uniform plane waves in lossless media | 1, 2, 4, 12 |
| 2. Polarization and mismatch | 3, 14 |
| 3. Lossy media: exact and approximate γ | 6, 7, 10 |
| 4. Skin depth, surface resistance, AC resistance | 5, 8, 11 |
| 5. Attenuation in laminates, cables and seawater | 7, 9, 13 |
