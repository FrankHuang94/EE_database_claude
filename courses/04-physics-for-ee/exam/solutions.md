# Course 04 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_04_exam.py](../verify/verify_04_exam.py), and the circuit answers to Questions 4 and 14 are confirmed in ngspice by [exam_circuits.cir](exam_circuits.cir), and those to Question 13 by [exam_coils.cir](exam_coils.cir). Each solution names the chapter to revisit if you lost points.

**1.** *(04-01)* (a) $f_0 = \frac{1}{2\pi}\sqrt{k_s/m} = \frac{1}{2\pi}\sqrt{2.0/1.0\times10^{-9}} = 44{,}721/2\pi$ = **7118 Hz**.

(b) $x = mg/k_s = 1.0\times10^{-9}\times9.80665/2.0 = 4.903\times10^{-9}$ m = **4.903 nm**. A displacement of a few nanometers per g is why MEMS accelerometers need capacitive readout with attofarad resolution.

(c) $\zeta = 1/(2Q)$ = **0.7143**, close to the 0.707 that gives the flattest frequency response.

**2.** *(04-02)* (a) Each charge is 2.0 cm away: $E = 8.98755\times10^9\times2.0\times10^{-9}/(0.02)^2 = 4.494\times10^4$ V/m. The positive charge pushes away from itself (+x) and the negative charge pulls toward itself (+x), so the fields add: **8.988×10⁴ V/m along +x**.

(b) $F = eE$ = **1.440×10⁻¹⁴ N along −x** (the electron's charge is negative).

(c) $p = qd = 2.0\times10^{-9}\times0.04$ = **8.000×10⁻¹¹ C·m**, pointing from − to + (along −x).

(d) On the axis, $E = 2pk_e/r^3 = 2\times8.0\times10^{-11}\times8.98755\times10^9/1$ = **1.438 V/m**. The $1/r^3$ fall-off is why distant dipoles (and well-paired differential signals) couple so weakly.

**3.** *(04-03)* (a) Inside a uniform sphere $E = k_eQr/R^3 = 8.98755\times10^9\times10^{-8}\times0.005/10^{-6}$ = **4.494×10⁵ V/m**; outside, $E = k_eQ/r^2 = 89.8755/0.0004$ = **2.247×10⁵ V/m**.

(b) Take a pillbox of face area $A$ with one face in the neutral p region (where $E = 0$) and the other at the junction. Only that face has flux, $EA$, and the box encloses the depleted acceptors' charge $-eN_Ax_pA$; Gauss's law $\varepsilon EA = -eN_Ax_pA$ gives a field of magnitude $eN_Ax_p/\varepsilon$ pointing from n to p. Numerically, $E_{\max} = eN_Ax_p/\varepsilon = 1.602\times10^{-19}\times10^{23}\times5\times10^{-8}/(11.7\times8.854\times10^{-12})$ = **7.733×10⁶ V/m** (77 kV/cm).

(c) The field rises linearly across the region, so the drop is the triangle's area: $\tfrac12E_{\max}x_p$ = **0.1933 V**.

**4.** *(04-04)* (a) $\text{EOT} = 0.6 + 1.5\times3.9/25$ = **0.8340 nm**, from 2.1 nm of physical thickness.

(b) $C/A = 3.9\varepsilon_0/\text{EOT} = 3.453\times10^{-11}/8.34\times10^{-10} = 0.04140$ F/m² = **4.140 µF/cm²**.

(c) Charge is conserved: $V = (10\times1.0 + 60\times0.5)/70$ = **0.5714 V**, a signal of **71.43 mV** for the sense amplifier.

(d) $\tfrac12\frac{C_1C_2}{C_1+C_2}(\Delta V)^2 = \tfrac12\times8.571\ \text{fF}\times(0.5\ \text{V})^2$ = **1.071 fJ**, independent of the switch's resistance.

**5.** *(04-05)* (a) $R = \rho L/A = 5.0\times10^{-8}\times10^{-4}/(20\times10^{-9}\times40\times10^{-9})$ = **6250 Ω**; $C = 0.20\times100$ = **20 fF**.

(b) $t_{50}\approx0.38RC = 0.38\times6250\times20\times10^{-15}$ = **47.50 ps**.

(c) $R$ and $C$ both fall to a third, so the delay falls ninefold: **5.278 ps**. Delay ∝ $L^2$ is why long wires get repeaters.

(d) $J = 20\times10^{-6}/(8\times10^{-16}\ \text{m}^2) = 2.5\times10^{10}$ A/m² = **2.500 MA/cm²**, the range where electromigration limits must be checked.

**6.** *(04-06)* (a) $r = mv/(eB) = \sqrt{2mV/e}/B$. For ¹¹B⁺: $\sqrt{2\times11\times1.66054\times10^{-27}\times4\times10^4/1.602\times10^{-19}}/0.80$ = **11.94 cm**; for BF₂⁺: **25.20 cm**.

(b) $r\propto\sqrt m$, so ¹⁰B⁺ runs at 11.38 cm, a difference of **5.555 mm**: a slit selects one isotope.

**7.** *(04-06)* (a) $B = \mu_0I/(2\pi r)$ = **2.000×10⁻⁴ T** (0.2 mT).

(b) $V_H = IB/(nqt)$, so $V_H/B = 10^{-3}/(10^{22}\times1.602\times10^{-19}\times10^{-6})$ = **0.6242 V/T**.

(c) **0.1248 mV** in 0.2 mT and **31.21 mV** in 50 mT. The small-field signal shows why current sensors use a concentrator core or sit on the busbar, and why semiconductors (low $n$) rather than metals make Hall plates.

**8.** *(04-07)* (a) $L = \mu_0N^2A/\ell = 1.25664\times10^{-6}\times4\times10^4\times10^{-4}/0.02$ = **251.3 µH** (long-solenoid approximation; a coil this short has somewhat less).

(b) $\tfrac12LI^2$ = **31.42 µJ**.

(c) $|{\mathcal E}| = L\,\Delta I/\Delta t = 2.513\times10^{-4}\times0.5/10^{-5}$ = **12.57 V**.

(d) $\delta = \sqrt{\rho/(\pi f\mu_0)} = \sqrt{1.68\times10^{-8}/(\pi\times2\times10^5\times1.25664\times10^{-6})}$ = **145.9 µm**.

**9.** *(04-08)* (a) $v = c/\sqrt{\varepsilon_r}$ = **1.499×10⁸ m/s**; 10 cm takes **0.6671 ns** (about 6.7 ps/mm).

(b) $\eta_0 = \sqrt{\mu_0/\varepsilon_0}$ = **376.7 Ω**; in the dielectric $\eta_0/\sqrt{\varepsilon_r}$ = **188.4 Ω**.

(c) $\lambda = v/f$ = **1.499 cm**, so a 10 cm trace is several wavelengths long and must be treated as a transmission line.

(d) $I = E_0^2/(2\eta_0) = 100/753.5$ = **0.1327 W/m²**.

**10.** *(04-09)* (a) $\text{NA} = \sqrt{n_1^2 - n_2^2} = \sqrt{2.10250 - 2.08716}$ = **0.1239**; acceptance half-angle $\sin^{-1}(\text{NA})$ = **7.115°**; critical angle $\sin^{-1}(n_2/n_1)$ = **85.10°** from the normal.

(b) $\text{CD} = k_1\lambda/\text{NA}$: **13.09 nm** at NA 0.33 and **7.855 nm** at NA 0.55.

**11.** *(04-10)* (a) $E = 1239.84/1550$ = **0.7999 eV**; responsivity $\eta e/E_{ph} = 0.8/0.7999$ = **1.000 A/W**.

(b) $E_1 = h^2/(8m^*L^2)$ = **87.69 meV**; $E_2 - E_1 = 3E_1$ = **263.1 meV**; $\lambda = 1239.84/263.1$ nm = **4.713 µm**, in the mid-infrared (the principle of quantum-well infrared detectors).

(c) $\kappa = \sqrt{2m_0\times2.1\ \text{eV}}/\hbar = 7.42\times10^9$ m⁻¹; the factor is $e^{2\kappa\times0.5\ \text{nm}} = e^{7.424}$ = **1676**: half a nanometer cuts tunneling more than a thousandfold.

**12.** *(04-11)* (a) Periodic boundary conditions allow $\vec k = (2\pi/L)(n_x, n_y, n_z)$, one state per volume $(2\pi/L)^3$ of $k$-space. Filling the $N$ electrons two per state up to $k_F$: $N = 2\cdot\tfrac43\pi k_F^3/(2\pi/L)^3 = Vk_F^3/(3\pi^2)$, so $k_F = (3\pi^2n)^{1/3}$ and $E_F = \hbar^2k_F^2/2m = \frac{\hbar^2}{2m}(3\pi^2n)^{2/3}$. For silver, $k_F = (3\pi^2n)^{1/3} = 1.2018\times10^{10}$ m⁻¹, $E_F = \hbar^2k_F^2/2m_0$ = **5.501 eV**, $v_F = \hbar k_F/m_0$ = **1.391×10⁶ m/s**.

(b) $(\pi^2/3)(kT/E_F) = 3.290\times0.025852/5.501$ = **0.01546**.

(c) $T$ = 398.15 K: $(398.15/300)^{2.54} = 2.0523$, $e^{-6726/398.15} = 4.607\times10^{-8}$, so $n_i$ = **5.001×10¹² cm⁻³**, **515.8** times its 300 K value.

(d) Equal exponents need equal $E_g/T$: $398.15\times3.26/1.12$ = **1159 K**.

(e) A silicon device at 125–150 °C has hundreds of times its room-temperature intrinsic carriers, so junction leakage (∝ $n_i$ or $n_i^2$) climbs steeply and can threaten thermal runaway; margins and derating are essential. For SiC the same leakage mechanism would not matter until roughly 1,100 K, so the semiconductor is not the limit at 150 °C; packaging, gate-oxide reliability and contacts are. *Rubric for (e), 4 points:* 1.5 for the silicon leakage argument, 1.5 for the SiC contrast, 1 for naming the real limit (package or oxide). For (a), 1 point for the counting derivation and 1 for the numbers.

**13.** *(04-07)* (a) $M = k\sqrt{L_1L_2}$ = **9.600 µH**.

(b) $\omega = 2\pi\times128$ kHz $= 8.042\times10^5$ rad/s. $V_{oc} = \omega MI$ = **15.44 V**; the transmitter's own $\omega L_1I$ = **38.60 V**.

(c) $C = 1/(\omega^2L_2)$ = **64.42 nF**.

(d) $\tfrac12L_1I^2 = \tfrac12\times24\ \mu\text{H}\times(2.0\ \text{A})^2$ = **48.00 µJ**.

(e) $V_{oc}\propto M\propto k$: it halves to **7.721 V**. The receiver's voltage, and the power it can draw, collapse with misalignment, so chargers add magnets (Qi's magnetic power profile) to hold $k$ high and repeatable.

**14.** *(04-02, 04-04)* (a) $I_{pk} = V/R = 2000/1500$ = **1.333 A**; $\tau = RC$ = **150.0 ns**.

(b) $\tfrac12CV^2$ = **200.0 µJ**; $Q = CV$ = **200.0 nC**.

(c) $t = \tau\ln10$ = **345.4 ns**. An amp-level pulse lasting hundreds of nanoseconds is why every I/O pin carries an ESD clamp.

**15.** *(Diligence; 04-10, 04-11, 04-10, 04-10)* Rubric: 2 points per claim, 1 for the physics and what is wrong or missing, 1 for a pointed question (8 in total).

(a) A 1550 nm photon carries 0.80 eV, below silicon's 1.12 eV gap, so silicon is transparent at 1550 nm and cannot detect it; telecom receivers use germanium or InGaAs. *Ask:* "What is the responsivity at 1550 nm, and what absorbing material is used?" (Only a germanium or III–V absorber on silicon makes the claim plausible.)

(b) A wide gap makes intrinsic carriers negligible, but leakage also flows through defects, surfaces and gate dielectrics, and those are thermally activated too. *Ask:* "Show leakage versus temperature to the maximum junction temperature, and the extracted activation energy."

(c) Capability depends on gate error rates, connectivity and error correction; more noisy qubits do not enable longer useful computations. *Ask:* "What are your two-qubit fidelities and logical error rate per cycle, and how do they change as you scale?"

(d) At 1.2 nm, direct tunneling through SiO₂ grows about fourfold for every 0.1 nm removed (04-10), which is why the industry moved to high-k dielectrics at 45 nm: a thicker high-k layer gives the same capacitance (EOT) with far less leakage. *Ask:* "What gate-leakage density do you project at the thinner oxide, and why not high-k?"

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X04.1a | resonant frequency | 7118 | Hz |
| X04.1b | static deflection at 1 g | 4.903 | nm |
| X04.1c | damping ratio | 0.7143 | — |
| X04.2a | field at the midpoint | 8.988×10^4 | V/m |
| X04.2b | force on an electron | 1.440×10^-14 | N |
| X04.2c | dipole moment | 8.000×10^-11 | C·m |
| X04.2d | far field at 1 m | 1.438 | V/m |
| X04.3a | field inside the sphere at 0.5 cm | 4.494×10^5 | V/m |
| X04.3b | field outside at 2.0 cm | 2.247×10^5 | V/m |
| X04.3c | peak junction field | 7.733×10^6 | V/m |
| X04.3d | p-side potential drop | 0.1933 | V |
| X04.4a | equivalent oxide thickness | 0.8340 | nm |
| X04.4b | gate capacitance per area | 4.140 | µF/cm² |
| X04.4c | final bit-line voltage | 0.5714 | V |
| X04.4d | read signal | 71.43 | mV |
| X04.4e | energy dissipated | 1.071 | fJ |
| X04.5a | wire resistance | 6250 | Ω |
| X04.5b | wire capacitance | 20 | fF |
| X04.5c | 50% delay | 47.50 | ps |
| X04.5d | delay at a third of the length | 5.278 | ps |
| X04.5e | current density | 2.500 | MA/cm² |
| X04.6a | ¹¹B⁺ radius | 11.94 | cm |
| X04.6b | BF₂⁺ radius | 25.20 | cm |
| X04.6c | ¹¹B⁺–¹⁰B⁺ radius difference | 5.555 | mm |
| X04.7a | field 1 cm from 10 A | 2.000×10^-4 | T |
| X04.7b | Hall sensitivity | 0.6242 | V/T |
| X04.7c | Hall voltage in 0.2 mT | 0.1248 | mV |
| X04.7d | Hall voltage in 50 mT | 31.21 | mV |
| X04.8a | solenoid inductance | 251.3 | µH |
| X04.8b | stored energy | 31.42 | µJ |
| X04.8c | induced EMF | 12.57 | V |
| X04.8d | skin depth at 200 kHz | 145.9 | µm |
| X04.9a | wave speed in the board | 1.499×10^8 | m/s |
| X04.9b | delay of 10 cm | 0.6671 | ns |
| X04.9c | free-space impedance | 376.7 | Ω |
| X04.9d | impedance in the dielectric | 188.4 | Ω |
| X04.9e | wavelength at 10 GHz | 1.499 | cm |
| X04.9f | plane-wave intensity | 0.1327 | W/m² |
| X04.10a | numerical aperture | 0.1239 | — |
| X04.10b | acceptance half-angle | 7.115 | ° |
| X04.10c | critical angle | 85.10 | ° |
| X04.10d | CD at NA 0.33 | 13.09 | nm |
| X04.10e | CD at NA 0.55 | 7.855 | nm |
| X04.11a | photon energy at 1550 nm | 0.7999 | eV |
| X04.11b | responsivity | 1.000 | A/W |
| X04.11c | quantum-well E₁ | 87.69 | meV |
| X04.11d | 2→1 spacing | 263.1 | meV |
| X04.11e | emitted wavelength | 4.713 | µm |
| X04.11f | tunneling reduction factor | 1676 | — |
| X04.12a | silver Fermi energy | 5.501 | eV |
| X04.12b | silver Fermi speed | 1.391×10^6 | m/s |
| X04.12c | electronic over classical heat capacity | 0.01546 | — |
| X04.12d | silicon n_i at 125 °C | 5.001×10^12 | cm⁻³ |
| X04.12e | ratio to 300 K | 515.8 | — |
| X04.12f | matching 4H-SiC temperature | 1159 | K |
| X04.13a | mutual inductance | 9.600 | µH |
| X04.13b | open-circuit receiver voltage | 15.44 | V |
| X04.13c | transmitter coil voltage | 38.60 | V |
| X04.13d | resonating capacitance | 64.42 | nF |
| X04.13e | peak stored energy | 48.00 | µJ |
| X04.13f | receiver voltage at k = 0.20 | 7.721 | V |
| X04.14a | peak current | 1.333 | A |
| X04.14b | time constant | 150.0 | ns |
| X04.14c | stored energy | 200.0 | µJ |
| X04.14d | charge delivered | 200.0 | nC |
| X04.14e | time to 10% | 345.4 | ns |
