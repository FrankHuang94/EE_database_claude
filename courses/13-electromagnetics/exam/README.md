# Course 13 · Final Exam (Electromagnetics)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 13 equation sheet](../../../reference/equation-sheets/13-electromagnetics.md) printed without its chapter links. No notes, no Python, no simulator, no Smith-chart software (a printed Smith chart is allowed).

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8, and Questions 13 and 14 [C] 12 each (4 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Within a question the lettered parts carry equal weight.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- $c$ = 2.998 × 10⁸ m/s, $\varepsilon_0$ = 8.854 × 10⁻¹² F/m, $\mu_0$ = 4π × 10⁻⁷ H/m, $\eta_0$ = 376.7 Ω.
- Phasors use $e^{j\omega t}$ and peak amplitudes; time-average power density is $\tfrac12\operatorname{Re}(\tilde{\vec{E}} \times \tilde{\vec{H}}^*)$.
- Materials are nonmagnetic ($\mu = \mu_0$) unless stated; lines are lossless unless stated; antennas are matched and co-polarized.

---

**1 [A] · Vector calculus.** (13-01)
(a) For $\vec{A} = xy\,\hat{x} + yz\,\hat{y} + zx\,\hat{z}$, find $\nabla\cdot\vec{A}$ and $\nabla\times\vec{A}$ at the point (1, 2, 3).
(b) For $V = x^2yz$, find $\nabla V$ and its magnitude at (1, 2, 3).
(c) In spherical coordinates $\vec{D} = 2r^2\,\hat{r}$ nC/m² ($r$ in metres). Find the charge density at $r$ = 1 m, and the total charge inside $r$ = 2 m by the divergence theorem.
(d) Use Stokes's theorem to find the circulation of $\vec{F} = -y\,\hat{x} + x\,\hat{y}$ counter-clockwise around the circle of radius 2 m centred on the origin in the $xy$-plane.

**2 [B] · Electrostatics.** (13-02)
(a) A parallel-plate capacitor of area 10 cm² has two dielectric layers between its plates: 1 mm of $\varepsilon_r$ = 2 and 1 mm of $\varepsilon_r$ = 6. With 100 V applied, find the capacitance, the field in each layer and the flux density $D$ (fringing neglected).
(b) A coaxial cable has an inner conductor of radius 0.45 mm and an outer conductor of inner radius 1.5 mm, filled with polyethylene ($\varepsilon_r$ = 2.25). Find its capacitance per metre and the largest field in the dielectric at 1 kV.
(c) A 1 nC point charge sits 1 cm above a large grounded conducting plane. Find the force on it.

**3 [B] · Magnetostatics and inductance.** (13-03)
A laminated silicon-steel core of relative permeability 1200 (saturating near 1.5 T), mean path length 10 cm and cross-section 10 mm², has a 1 mm air gap and is wound with 250 turns. Neglect fringing and leakage.
(a) Find the inductance, the flux density at 2 A, and the fraction of the magnetic circuit's reluctance in the gap.
(b) Find the stored energy at 2 A and the fraction of it stored in the gap. Why do power inductors have gaps?
(c) Find the magnetic flux density at the centre of a single circular loop of radius 1 cm carrying 1 A.

**4 [B] · Maxwell's equations.** (13-04)
(a) $\vec{E} = 100\cos(2\pi \times 10^9t - 30z)\,\hat{x}$ V/m in a lossless nonmagnetic dielectric. Find its relative permittivity, its intrinsic impedance, the amplitude and direction of $\vec{H}$, the time-average power density and the wavelength.
(b) Moist soil has σ = 2 mS/m and $\varepsilon_r$ = 4. Find the ratio of conduction to displacement current density at 1 MHz and at 1 GHz, and say how the soil behaves at each.
(c) Find the soil's charge relaxation time.

**5 [B] · Skin depth and lossy media.** (13-05)
(a) For aluminium (σ = 3.5 × 10⁷ S/m) at 300 MHz, find the skin depth and the surface resistance. Find the resistance of 1 m of 1 mm diameter aluminium wire at 300 MHz (good-conductor approximation, current in a skin of depth δ) and at DC, and their ratio.
(b) For seawater (σ = 4 S/m, $\varepsilon_r$ = 81) at 40 kHz, check that it is a good conductor, and find the skin depth, the attenuation in dB/m, the wavelength in the water, and the depth at which the signal has lost 80 dB.

**6 [B] · Reflection and transmission.** (13-06)
(a) A plane wave in air strikes a nonmagnetic dielectric of $\varepsilon_r$ = 9 at normal incidence. Find the reflection and transmission coefficients for $E$, and the fractions of power reflected and transmitted.
(b) A camera lens uses a high-index glass ($n$ = 1.8). Find the ideal index and thickness of a single-layer quarter-wave antireflection coating for it at 550 nm. A quarter-wave layer of magnesium fluoride ($n$ = 1.38) is used instead: find the reflectance at 550 nm, and compare it with the uncoated glass.
(c) Find the Brewster angle for light passing from air into fused silica ($n$ = 1.45), and the critical angle for light passing from the silica into air.

**7 [B] · Transmission lines in the time domain.** (13-07)
(a) A 2 V step source with 25 Ω internal resistance drives a 50 Ω line of one-way delay $T$ terminated in 200 Ω. Find the launched voltage and the source and load reflection coefficients; the load voltage just after $t = T$, $3T$ and $5T$; and its final value.
(b) A matched source drives a 50 Ω line terminated in a 2 pF capacitor (a receiver input). Find the time constant of the load voltage and its 10–90% rise time for an ideal step.

**8 [B] · Line parameters and stubs.** (13-08)
A lossless line has $L'$ = 300 nH/m and $C'$ = 120 pF/m.
(a) Find its characteristic impedance, phase velocity and effective relative permittivity.
(b) A 1 cm length of it is left open at the far end. Find its input impedance at 1 GHz and the equivalent capacitance, and compare with the lumped estimate $C'\ell$.
(c) Design a quarter-wave transformer from a line with the same phase velocity that matches a 100 Ω load to 50 Ω at 2.5 GHz: give its characteristic impedance and length.

**9 [B] · Standing waves.** (13-08)
A load $Z_L$ = 20 − j10 Ω terminates a 50 Ω line.
(a) Find the input impedance a quarter-wavelength from the load.
(b) Find the magnitude of the reflection coefficient, the VSWR, the return loss and the mismatch loss.
(c) Find the distances from the load, in wavelengths, of the first voltage minimum and the first voltage maximum.
(d) Using a Smith chart (or the single-stub formula of 13-09), design both shorted-stub shunt matches for this load: the distance from the load to the stub and the stub length, in wavelengths.

**10 [B] · Matching.** (13-09)
A power amplifier's output looks like 12.5 Ω and must be matched to a 50 Ω antenna at 900 MHz with a low-pass L-network (series inductor on the 12.5 Ω side, shunt capacitor on the 50 Ω side).
(a) Find the network's Q and the two component values.
(b) With these components, find the impedance seen from the 50 Ω side at 800 MHz, the reflection coefficient magnitude there and the mismatch loss.

**11 [B] · Waveguides and cavities.** (13-10)
WR-75 waveguide is 19.05 mm × 9.525 mm, air-filled.
(a) Find the cutoff frequencies of the TE₁₀, TE₂₀ and TE₀₁ modes, and the single-mode band.
(b) At 13 GHz, find the TE₁₀ phase constant, guide wavelength, wave impedance, group velocity (as a fraction of $c$), and the group delay through 1 m.
(c) A 2 cm length of the guide is closed at both ends with metal walls. Find its TE₁₀₁ resonant frequency.

**12 [B] · A wireless link.** (13-11)
A 5.8 GHz point-to-point link spans 2 km. The transmitter delivers 20 dBm to a 9 dBi antenna; the receive antenna is identical.
(a) Find the EIRP, the free-space path loss and the received power.
(b) Find the receive antenna's effective aperture.
(c) The receiver needs −90 dBm. Find the link margin and the free-space range at which the margin falls to zero.

**13 [C] · Derivations.**
(a) Starting from Maxwell's equations in a source-free, lossless, linear, homogeneous and isotropic medium, derive the wave equation for $\vec{E}$, and show that a uniform plane wave travels at $1/\sqrt{\mu\varepsilon}$ with $\lvert\vec{E}\rvert/\lvert\vec{H}\rvert = \sqrt{\mu/\varepsilon}$.
(b) A lossless line of characteristic impedance $Z_0$ and phase constant β is terminated in $Z_L$. From the line's voltage and current waves, derive the input impedance a distance ℓ from the load, and show that a quarter-wave line turns $Z_L$ into $Z_0^2/Z_L$.
(c) A short dipole of length ℓ ≪ λ carries a uniform current $I$ (peak). Its far field is $E_\theta = j\eta_0kI\ell\sin\theta\,e^{-jkr}/(4\pi r)$. Derive its radiated power and radiation resistance, and evaluate the resistance for ℓ = λ/25. If the antenna also has 1 Ω of loss resistance, what fraction of the input power does it radiate?

**14 [C] · Diligence: "39 dBm EIRP, 24 to 40 GHz, ±60°".**
A start-up's 16-element millimetre-wave array module claims "39 dBm EIRP across ±60° of scan, one antenna design covering 24 to 40 GHz, 5 mm element spacing, no grating lobes". Each element is driven with 10 dBm and has 5 dBi gain at broadside.
(a) Find the broadside EIRP. If each element's power gain falls as $\cos\theta$ off broadside, find the EIRP at 60° of scan. If the power amplifiers are 15% efficient, what DC power do they draw?
(b) For 5 mm spacing and scans to ±60°, find the highest frequency free of grating lobes. What spacing would 40 GHz require? What fractional bandwidth is 24 to 40 GHz?
(c) Name three questions you would ask the start-up, and what a strong and an evasive answer to each would look like.
