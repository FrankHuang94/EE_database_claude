# Course 04 · Final Exam (Physics for EE)

**Time limit:** 180 minutes. **Allowed:** a scientific calculator and the [Course 04 equation sheet](../../../reference/equation-sheets/04-physics-for-ee.md) printed without its chapter links. No notes, no Python.
**Instructions:** answer all 15 questions and show every step. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (119 points in total; 83 or more, about 70%, is a strong pass). Within a question, the lettered parts carry equal weight. Give numerical answers to 4 significant figures unless told otherwise, with units and, for vectors, directions. Question 15 is a short-answer diligence question graded against the rubric in the solutions. Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Constants:** $h = 6.62607015\times10^{-34}$ J·s, $\hbar = h/2\pi$, $e = 1.602176634\times10^{-19}$ C, $c = 299\,792\,458$ m/s, $k = 1.380649\times10^{-23}$ J/K (all exact); $m_0 = 9.1093837139\times10^{-31}$ kg; $\varepsilon_0 = 8.8541878188\times10^{-12}$ F/m, $\mu_0 = 1.25663706127\times10^{-6}$ H/m, $1/(4\pi\varepsilon_0) = 8.98755\times10^9$ N·m²/C²; 1 u = $1.66054\times10^{-27}$ kg; $g = 9.80665$ m/s²; $R = 8.314462618$ J/(mol·K); $hc$ = 1239.84 eV·nm; $kT$ = 25.85 meV at 300 K.

---

**1 [A] · A MEMS accelerometer.** A proof mass of 1.0 µg hangs on a spring of stiffness 2.0 N/m, with quality factor $Q$ = 0.7.
(a) Find the undamped resonant frequency.
(b) Find the static deflection under 1 g, in nm.
(c) Find the damping ratio ζ.

**2 [A] · A dipole.** A +2.0 nC charge sits at the origin and a −2.0 nC charge at $x$ = 4.0 cm.
(a) Find the electric field (magnitude and direction) at the midpoint.
(b) Find the force on an electron placed there.
(c) Find the dipole moment.
(d) Find the field magnitude on the $x$-axis 1.0 m away, using the far-field dipole formula.

**3 [B] · Gauss's law twice.** (a) A sphere of radius 1.0 cm carries 10 nC spread uniformly through its volume. Find the field at 0.5 cm and at 2.0 cm from its center.
(b) On the p side of a silicon pn junction ($\varepsilon_r$ = 11.7), acceptors at $10^{17}$ cm⁻³ are fully depleted over $x_p$ = 50 nm. Find the peak field at the junction.
(c) Find the potential drop across the p-side depletion region.

**4 [B] · Gate stacks and DRAM reads.** (a) A gate stack has 0.6 nm of SiO₂ ($\varepsilon_r$ = 3.9) under 1.5 nm of HfO₂ ($\varepsilon_r$ = 25). Find its equivalent oxide thickness.
(b) Find its capacitance per area in µF/cm².
(c) A 10 fF DRAM cell holding 1.0 V is connected to a 60 fF bit line precharged to 0.50 V. Find the final bit-line voltage and the signal (change from 0.50 V) in mV.
(d) Find the energy dissipated in the connecting switch, in fJ.

**5 [B] · A thin wire.** A copper interconnect is 100 µm long, 20 nm wide and 40 nm tall, with an effective resistivity of 5.0 µΩ·cm (size effect included; take as given) and capacitance 0.20 fF/µm.
(a) Find its resistance and total capacitance.
(b) Estimate its 50% delay as a distributed RC line.
(c) Find the delay if the wire were half as long.
(d) Find the current density, in MA/cm², when it carries 20 µA.

**6 [A] · An implanter magnet.** Singly charged ions are accelerated through 40 kV and enter a 0.80 T analyzer field at right angles. Take masses of 11 u for ¹¹B⁺, 10 u for ¹⁰B⁺ and 49 u for BF₂⁺.
(a) Find the orbit radius of ¹¹B⁺ and of BF₂⁺.
(b) Find the difference in radius between ¹¹B⁺ and ¹⁰B⁺, in mm.

**7 [B] · Sensing a current.** (a) Find the magnetic field 1.0 cm from a long straight wire carrying 10 A.
(b) A Hall plate 1.0 µm thick has $10^{22}$ carriers per m³ and is biased at 1.0 mA. Find its sensitivity in V/T.
(c) Find its Hall voltage in the field of (a), in mV, and in a 50 mT field.

**8 [B] · A solenoid.** An air-core solenoid has 200 turns, cross-section 1.0 cm² and length 2.0 cm.
(a) Find its inductance.
(b) Find the energy stored at 0.50 A.
(c) Find the EMF if the current falls linearly from 0.50 A to zero in 10 µs.
(d) Find copper's skin depth (ρ = 1.68 µΩ·cm) at 200 kHz, in µm.

**9 [B] · Waves on a board.** A stripline runs through a dielectric with $\varepsilon_r$ = 4.0 (non-magnetic).
(a) Find the wave speed and the delay of a 10 cm trace.
(b) Find the free-space wave impedance η₀ and the wave impedance in the dielectric.
(c) Find the wavelength of a 10 GHz signal in the board, in cm.
(d) A plane wave in air has a peak electric field of 10 V/m. Find its intensity.

**10 [B] · Fibers and lithography.** (a) A fiber has core index 1.4500 and cladding index 1.4447. Find its numerical aperture, its acceptance half-angle in air, and the critical angle at the core–cladding boundary.
(b) With $k_1$ = 0.32, find the critical dimension printable with 13.5 nm light at NA 0.33 and at NA 0.55.

**11 [B] · Quantum in devices.** (a) Find the photon energy at 1550 nm, and the responsivity of an InGaAs photodiode with 80% quantum efficiency there.
(b) Model a GaAs quantum well as an infinite well 8.0 nm wide with $m^*$ = 0.067 $m_0$ (take as given). Find $E_1$, the 2→1 spacing and the emitted wavelength.
(c) Using $T\propto e^{-2\kappa d}$ for an electron 2.1 eV below the top of an oxide barrier (free-electron mass), by what factor does tunneling fall when the oxide thickens from 1.5 to 2.0 nm?

**12 [C] · Free electrons and intrinsic carriers.** (a) Silver has $n = 5.86\times10^{28}$ conduction electrons per m³ (take as given). Find its Fermi energy and Fermi speed.
(b) Find the ratio of its electronic heat capacity to Drude's classical prediction at 300 K.
(c) Using $n_i = 5.29\times10^{19}(T/300)^{2.54}e^{-6726/T}$ cm⁻³, find silicon's $n_i$ at a junction temperature of 125 °C and its ratio to the 300 K value.
(d) At what temperature does 4H-SiC's factor $e^{-E_g/2kT}$ ($E_g$ = 3.26 eV) equal silicon's ($E_g$ = 1.12 eV) at 125 °C?
(e) In two or three sentences, explain what (c) and (d) imply for designing a 150 °C automotive power device.

**13 [C] · A wireless-power link.** Transmitter and receiver coils each have 24 µH with coupling coefficient $k$ = 0.40. The transmitter carries a 2.0 A-amplitude sinusoid at 128 kHz; the receiver is open-circuited.
(a) Find the mutual inductance.
(b) Find the amplitude of the open-circuit receiver voltage and of the transmitter coil's own voltage.
(c) Find the capacitance that resonates the receiver coil at 128 kHz.
(d) Find the peak magnetic energy stored in the transmitter coil.
(e) The phone shifts and $k$ falls to 0.20. What happens to the received voltage, and why do chargers add alignment magnets?

**14 [B] · An ESD pulse.** A human-body-model tester charges 100 pF to 2.0 kV and discharges it through 1.5 kΩ into a short circuit.
(a) Find the peak current and the time constant.
(b) Find the stored energy and the charge delivered.
(c) Find the time for the current to fall to 10% of its peak.

**15 [B] · Diligence: four claims.** For each claim, say in two or three sentences what physics it rests on, what is wrong or missing, and the one question you would ask.
(a) "Our new silicon photodiode is ideal for 1550 nm datacenter receivers."
(b) "Because SiC's band gap is wide, our device's leakage does not depend on temperature."
(c) "Our quantum computer has the most qubits, so it is the most capable on the market."
(d) "A 1.2 nm SiO₂ gate oxide is fine; we will just make it thinner at the next node."
