<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 04 · Physics for EE

Calculus-based electricity and magnetism with the mechanics, waves and modern physics that EE depends on, ending with an introduction to quantum mechanics and solid-state physics so that semiconductor devices make sense.

| | |
|---|---|
| **Term** | 1 |
| **Study hours** | ≈ 106 |
| **University equivalents** | University Physics II (E&M) + Modern Physics; MIT 8.02 / 8.04 (intro) |
| **Textbook alignment** | Halliday, Resnick & Walker, *Fundamentals of Physics*; Purcell & Morin, *Electricity and Magnetism*; Griffiths, *Introduction to Quantum Mechanics* (first chapters, optional) |
| **Free courses** | MIT OCW 8.02 Physics II: Electricity and Magnetism; MIT OCW 8.04 Quantum Physics I (first lectures) |
| **Prerequisites** | [01 · Calculus for Engineers](../01-calculus-for-engineers/README.md) |
| **FE areas** | Electromagnetics, Properties of Electrical Materials |
| **Deeper** | Companion repo(s): quantum computing |

## Learning objectives

1. Compute electric fields, potentials and capacitance for simple charge distributions using Coulomb's and Gauss's laws.
2. Compute magnetic fields of simple current distributions and the EMF induced by changing flux (Faraday/Lenz), and derive inductance.
3. Relate microscopic conduction (drift, mobility) to Ohm's law and resistivity.
4. Describe wave propagation (speed, wavelength, impedance, interference) and basic optics.
5. Explain quantization, tunneling and energy bands, and why semiconductors differ from metals and insulators.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [04-01 · Mechanics Essentials for EE](chapters/04-01-mechanics-essentials.md) | 8 | ✅ verified | [problems](problems/04-01-problems.md) · [solutions](solutions/04-01-solutions.md) · [lab](labs/04-01-lab/README.md) · [verify](verify/verify_04_01.py) |
| [04-02 · Charge, Coulomb's Law and Electric Fields](chapters/04-02-charge-coulomb-and-electric-fields.md) | 10 | ✅ verified | [problems](problems/04-02-problems.md) · [solutions](solutions/04-02-solutions.md) · [lab](labs/04-02-lab/README.md) · [verify](verify/verify_04_02.py) |
| [04-03 · Gauss's Law](chapters/04-03-gauss-law.md) | 8 | ✅ verified | [problems](problems/04-03-problems.md) · [solutions](solutions/04-03-solutions.md) · [lab](labs/04-03-lab/README.md) · [verify](verify/verify_04_03.py) |
| [04-04 · Electric Potential, Capacitance and Dielectrics](chapters/04-04-potential-capacitance-and-dielectrics.md) | 10 | ✅ verified | [problems](problems/04-04-problems.md) · [solutions](solutions/04-04-solutions.md) · [lab](labs/04-04-lab/README.md) · [verify](verify/verify_04_04.py) |
| [04-05 · Current, Resistance and Conduction](chapters/04-05-current-resistance-and-conduction.md) | 8 | ✅ verified | [problems](problems/04-05-problems.md) · [solutions](solutions/04-05-solutions.md) · [lab](labs/04-05-lab/README.md) · [verify](verify/verify_04_05.py) |
| [04-06 · Magnetic Fields and Forces](chapters/04-06-magnetic-fields-and-forces.md) | 10 | ✅ verified | [problems](problems/04-06-problems.md) · [solutions](solutions/04-06-solutions.md) · [lab](labs/04-06-lab/README.md) · [verify](verify/verify_04_06.py) |
| [04-07 · Faraday's Law, Lenz's Law and Inductance](chapters/04-07-faraday-lenz-and-inductance.md) | 10 | ✅ verified | [problems](problems/04-07-problems.md) · [solutions](solutions/04-07-solutions.md) · [lab](labs/04-07-lab/README.md) · [verify](verify/verify_04_07.py) |
| [04-08 · Energy in Fields and Maxwell's Equations (Preview)](chapters/04-08-maxwell-preview.md) | 6 | ✅ verified | [problems](problems/04-08-problems.md) · [solutions](solutions/04-08-solutions.md) · [lab](labs/04-08-lab/README.md) · [verify](verify/verify_04_08.py) |
| [04-09 · Waves and Optics Basics](chapters/04-09-waves-and-optics.md) | 10 | ✅ verified | [problems](problems/04-09-problems.md) · [solutions](solutions/04-09-solutions.md) · [lab](labs/04-09-lab/README.md) · [verify](verify/verify_04_09.py) |
| [04-10 · Introduction to Quantum Mechanics](chapters/04-10-intro-quantum-mechanics.md) | 10 | ✅ verified | [problems](problems/04-10-problems.md) · [solutions](solutions/04-10-solutions.md) · [lab](labs/04-10-lab/README.md) · [verify](verify/verify_04_10.py) |
| [04-11 · Introduction to Solid-State Physics](chapters/04-11-intro-solid-state-physics.md) | 10 | ✅ verified | [problems](problems/04-11-problems.md) · [solutions](solutions/04-11-solutions.md) · [lab](labs/04-11-lab/README.md) · [verify](verify/verify_04_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/04-physics-for-ee.csv) · [Equation sheet](../../reference/equation-sheets/04-physics-for-ee.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 04 takes about 106 hours, the longest of Term 1. It is calculus-based physics taught for chips: every law is derived, then applied to a device you will meet again (a MEMS accelerometer, an ESD clamp, a gate stack, an interconnect, a Hall sensor, a power inductor, a board trace, an optical link, a flash cell, a power transistor). The eleven chapters run in order and fall into four blocks. 04-01 is the mechanics the rest borrows (energy, oscillators, Q). 04-02 to 04-05 are electrostatics and conduction: Coulomb, Gauss, potential and capacitance, then current and resistance. 04-06 to 04-08 are magnetism, induction and Maxwell's equations, ending with electromagnetic waves. 04-09 to 04-11 are waves and optics, quantum mechanics and solid-state physics, the bridge into Course 09's semiconductor devices. Work at least the [A] and [B] problems of every chapter. Every lab is a notebook that checks a derivation numerically (field maps, ODE integrations, FDTD, matrix eigenproblems), and seven chapters add ngspice netlists.

**What to master cold.** Oscillator $Q$ and the accelerometer's $1/\omega_0^2$ (04-01); Coulomb superposition and the dipole's $1/r^3$ (04-02); choosing a Gaussian surface (04-03); $V = -\int E\,dl$, the capacitance formulas, EOT and charge-sharing loss (04-04); $\sigma = nq\mu$, Drude, $R = \rho L/A$ and wire delay ∝ $L^2$ (04-05); the Lorentz force, Ampère's law and the Hall voltage (04-06); Faraday, inductance, coupling and skin depth (04-07); displacement current, $c$, η₀ and the Poynting vector (04-08); interference, diffraction, Snell and $k_1\lambda/\text{NA}$ (04-09); $E = hc/\lambda$, box energies and exponential tunneling (04-10); the Fermi energy, Fermi–Dirac, bands, effective mass and $n_i\propto e^{-E_g/2kT}$ (04-11). The [equation sheet](../../reference/equation-sheets/04-physics-for-ee.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions, takes 180 minutes, and allows a calculator and the equation sheet but not Python. Aim for at least 70%. Question 15 is a short-answer diligence question about four technical claims. The [flashcards](../../flashcards/04-physics-for-ee.csv) (150 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Physics sets the hard limits that roadmaps run into: tunneling sets the gate-oxide floor, the wire's $RC$ sets interconnect delay, skin depth and core saturation size power magnetics, photon energy against band gap decides which material can detect which wavelength, and the band gap decides whether a power device can run hot. When a pitch claims to beat one of these, the first question is which physical limit moved, and how. The chapters' Marketing vs Reality sections practice exactly that.

**Perishable content.** The physics is timeless. The dated facts are in the practitioner sections, logged as [R-073](../../reference/research-log.md#r-073--codata-2022-fundamental-constants) to [R-086](../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) in the research log. The ones most likely to move are market forecasts ([R-076](../../reference/research-log.md#r-076--mems-market-size), [R-086](../../reference/research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets)), interconnect metals and backside power ([R-080](../../reference/research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power)), wireless-charging standards ([R-082](../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)), optical-interconnect standards, lithography tools and co-packaged optics ([R-084](../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)) and quantum-computing roadmaps ([R-085](../../reference/research-log.md#r-085--quantum-effects-in-devices-and-quantum-computing)). Check those entries once a year.
