# Problems 04-08 · Energy in Fields and Maxwell's Equations (Preview)

Chapter: [04-08](../chapters/04-08-maxwell-preview.md) · Worked solutions: [04-08 solutions](../solutions/04-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $c = 299\,792\,458$ m/s; $\mu_0 = 1.25663706127\times10^{-6}$ N/A²; $\varepsilon_0 = 8.8541878188\times10^{-12}$ F/m; $\eta_0 = \sqrt{\mu_0/\varepsilon_0}$. Sinusoids are given by amplitude unless stated as rms. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-08.1 [A]

**Which field stores more?** Find the energy densities of a 10 kV/m electric field and a 10 mT magnetic field in air, and their ratio.

### Problem 04-08.2 [A]

**Wavelengths.** Find the vacuum wavelength at 60 Hz, 2.4 GHz (Wi-Fi), 28 GHz (5G band n261) and 193.4 THz (the 1550 nm fiber window).

### Problem 04-08.3 [A]

**Skew between layers.** A 300 mm trace is routed as stripline in a laminate with $\varepsilon_r$ = 3.66; a matching trace runs as microstrip with effective $\varepsilon_{\text{eff}}$ = 2.9. Find each delay and the skew between them.

### Problem 04-08.4 [B]

**Displacement current in a capacitor.** A 10 nF capacitor has a 1 V, 1 MHz sinusoid across it. Find the amplitude of the displacement current through its dielectric, and explain why it equals the current in its leads.

### Problem 04-08.5 [B]

**Fields of an intense beam.** A plane wave has an average intensity of 1 kW/m². Find its electric- and magnetic-field amplitudes.

### Problem 04-08.6 [B]

**Reflection at a dielectric.** A plane wave in air meets a flat dielectric with $\varepsilon_r$ = 4 at normal incidence. (a) Find the dielectric's wave impedance. (b) Using continuity of the tangential E and H at the boundary, show that the amplitude reflection coefficient is $\Gamma = (\eta_2 - \eta_1)/(\eta_2 + \eta_1)$, and evaluate it. (c) What fractions of the power are reflected and transmitted?

### Problem 04-08.7 [B]

**Power flow in a coax.** A coaxial cable (inner radius 0.45 mm, outer 1.475 mm) carries 10 V and 0.2 A to a load. (a) Find the Poynting vector at the surface of the inner conductor. (b) Integrate it over the annulus between the conductors and show that the total is $VI$.

### Problem 04-08.8 [A]

**Near a phone.** Estimate the intensity 5 cm from a source radiating 0.2 W equally in all directions, and say why this is only a rough estimate.

### Problem 04-08.9 [B]

**Millimeter-wave loss.** Find the dielectric attenuation at 28 GHz in RO4350B ($\varepsilon_r$ = 3.66; assume $\tan\delta$ stays 0.0037), in Np/m and dB/m.

### Problem 04-08.10 [B]

**When is displacement current negligible?** For a material with conductivity σ and permittivity ε, compare the displacement and conduction current densities with the ratio $\omega\varepsilon/\sigma$. Evaluate it at 1 GHz for (a) copper (σ = 5.95×10⁷ S/m, $\varepsilon_r$ ≈ 1) and (b) seawater (σ = 4 S/m, $\varepsilon_r$ = 81). What does (b) suggest about radio under the sea?

### Problem 04-08.11 [B]

**Checking the wave equation.** Show that $E = E_0\cos(kx - \omega t)$ satisfies $\partial^2E/\partial x^2 = \mu\varepsilon\,\partial^2E/\partial t^2$ only if $\omega/k = 1/\sqrt{\mu\varepsilon}$, and find $k$ at 10 GHz in a material with $\varepsilon_r$ = 4.6.

### Problem 04-08.12 [B]

**Measuring a board's effective permittivity.** A microstrip test coupon shows a delay of 5.9 ps/mm. Find $\varepsilon_{\text{eff}}$, and explain why it is lower than the laminate's $\varepsilon_r$ of 4.6.

### Problem 04-08.13 [B]

**Why the averaging mass matters.** A device deposits 20 mW in the tissue nearest it. (a) If that power spreads evenly over 10 g, find the SAR and compare with ICNIRP's 2 W/kg. (b) If 30% of it lands in the hottest 1 g, find that gram's SAR and compare with the FCC's 1.6 W/kg. (c) What does this say about comparing limits?

### Problem 04-08.14 [B]

**A magnetic field from an AC capacitor.** A 1 nF capacitor with circular plates of radius 2 cm has a 10 V, 10 MHz sinusoid across it. Find the current amplitude and the magnetic-field amplitude at the plates' edge.

### Problem 04-08.15 [C]

**Power flows through the dielectric, not the copper.** A coaxial cable (inner radius $a$ = 0.5 mm, outer radius $b$ = 2 mm, perfect conductors) connects a 10 V DC source to a resistive load drawing 2 A. (a) Write $E(r)$ and $H(r)$ between the conductors and the Poynting vector $S(r)$, and evaluate $S$ at $r$ = 1 mm. (b) Integrate $S$ over the annulus $a < r < b$ and show that the total equals $VI$. (c) Where, then, does the energy delivered to the load travel?

---

## Objective coverage

| Learning objective (chapter 04-08) | Problems |
|---|---|
| 1. Energy densities | 1, 5 |
| 2. Displacement current | 4, 10, 14 |
| 3. Maxwell's equations | 4, 10, 11 |
| 4. Waves: speed, wavelength, impedance, reflection | 2, 3, 6, 11, 12 |
| 5. Poynting vector, board loss and RF exposure | 5, 7, 8, 9, 13, 15 |
