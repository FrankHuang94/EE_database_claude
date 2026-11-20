<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 13 · Electromagnetics

Maxwell's equations and their engineering consequences: waves, reflection, transmission lines and the Smith chart, waveguides and antennas. The basis for RF, signal integrity and photonics.

| | |
|---|---|
| **Term** | 4 |
| **Study hours** | ≈ 106 |
| **University equivalents** | Electromagnetics I–II (junior); MIT 6.013; Berkeley EE117 |
| **Textbook alignment** | Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*; Cheng, *Field and Wave Electromagnetics*; Griffiths, *Introduction to Electrodynamics* (physics perspective) |
| **Free courses** | MIT OCW 6.013 Electromagnetics and Applications; NPTEL electromagnetic theory courses |
| **Prerequisites** | [01 · Calculus for Engineers](../01-calculus-for-engineers/README.md), [04 · Physics for EE](../04-physics-for-ee/README.md), [07 · Circuit Analysis II (Transient and AC)](../07-circuit-analysis-2-transient-and-ac/README.md) |
| **FE areas** | Electromagnetics |

## Learning objectives

1. Use vector calculus (gradient, divergence, curl and the integral theorems) in Cartesian, cylindrical and spherical coordinates.
2. Solve electrostatic and magnetostatic boundary-value problems and compute capacitance and inductance of structures.
3. Derive plane-wave solutions from Maxwell's equations and compute propagation, attenuation, skin depth and power flow.
4. Analyze transmission lines in time and frequency domain, including reflections, standing waves and input impedance.
5. Use the Smith chart for impedance matching.
6. Explain waveguide modes and antenna fundamentals (radiation patterns, gain, effective aperture).

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [13-01 · Vector Calculus Refresher](chapters/13-01-vector-calculus-refresher.md) | 10 | ✅ verified | [problems](problems/13-01-problems.md) · [solutions](solutions/13-01-solutions.md) · [lab](labs/13-01-lab/README.md) · [verify](verify/verify_13_01.py) |
| [13-02 · Electrostatics: Boundary Conditions and Boundary-Value Problems](chapters/13-02-electrostatics-boundary-value-problems.md) | 10 | ✅ verified | [problems](problems/13-02-problems.md) · [solutions](solutions/13-02-solutions.md) · [lab](labs/13-02-lab/README.md) · [verify](verify/verify_13_02.py) |
| [13-03 · Magnetostatics and Inductance](chapters/13-03-magnetostatics-and-inductance.md) | 8 | ✅ verified | [problems](problems/13-03-problems.md) · [solutions](solutions/13-03-solutions.md) · [lab](labs/13-03-lab/README.md) · [verify](verify/verify_13_03.py) |
| [13-04 · Maxwell's Equations and Time-Varying Fields](chapters/13-04-maxwells-equations.md) | 10 | ✅ verified | [problems](problems/13-04-problems.md) · [solutions](solutions/13-04-solutions.md) · [lab](labs/13-04-lab/README.md) · [verify](verify/verify_13_04.py) |
| [13-05 · Plane Waves in Lossless and Lossy Media](chapters/13-05-plane-waves.md) | 10 | ✅ verified | [problems](problems/13-05-problems.md) · [solutions](solutions/13-05-solutions.md) · [lab](labs/13-05-lab/README.md) · [verify](verify/verify_13_05.py) |
| [13-06 · Reflection and Transmission of Waves](chapters/13-06-reflection-and-transmission.md) | 8 | ✅ verified | [problems](problems/13-06-problems.md) · [solutions](solutions/13-06-solutions.md) · [lab](labs/13-06-lab/README.md) · [verify](verify/verify_13_06.py) |
| [13-07 · Transmission Lines: Time Domain](chapters/13-07-transmission-lines-time-domain.md) | 10 | ✅ verified | [problems](problems/13-07-problems.md) · [solutions](solutions/13-07-solutions.md) · [lab](labs/13-07-lab/README.md) · [verify](verify/verify_13_07.py) |
| [13-08 · Transmission Lines: Sinusoidal Steady State](chapters/13-08-transmission-lines-sinusoidal-steady-state.md) | 10 | ✅ verified | [problems](problems/13-08-problems.md) · [solutions](solutions/13-08-solutions.md) · [lab](labs/13-08-lab/README.md) · [verify](verify/verify_13_08.py) |
| [13-09 · The Smith Chart and Impedance Matching](chapters/13-09-smith-chart-and-matching.md) | 10 | ✅ verified | [problems](problems/13-09-problems.md) · [solutions](solutions/13-09-solutions.md) · [lab](labs/13-09-lab/README.md) · [verify](verify/verify_13_09.py) |
| [13-10 · Waveguides and Resonators](chapters/13-10-waveguides-and-resonators.md) | 6 | ✅ verified | [problems](problems/13-10-problems.md) · [solutions](solutions/13-10-solutions.md) · [lab](labs/13-10-lab/README.md) · [verify](verify/verify_13_10.py) |
| [13-11 · Radiation and Antenna Fundamentals](chapters/13-11-radiation-and-antennas.md) | 8 | ✅ verified | [problems](problems/13-11-problems.md) · [solutions](solutions/13-11-solutions.md) · [lab](labs/13-11-lab/README.md) · [verify](verify/verify_13_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/13-electromagnetics.csv) · [Equation sheet](../../reference/equation-sheets/13-electromagnetics.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 13 is planned at about 106 hours: the chapters' own estimates add to 100, plus review and the exam. Course 04 met the field laws one at a time, in integral form and with symmetry doing the work. This course writes them as differential equations, solves them where symmetry is absent, and follows their consequences into the things a chip company sells: packages and boards whose wires are transmission lines, RF front ends that must be matched, and antennas and optics that send signals through space and glass.

The eleven chapters fall into four blocks:

- **Static fields (13-01 to 13-03).** The vector calculus the rest of the course is written in; electrostatic boundary-value problems, images and the capacitance of real structures; magnetostatics, magnetic materials, inductance and magnetic circuits.
- **Maxwell's equations and waves (13-04 to 13-06).** Faraday's law and the displacement current complete the equations; plane waves follow from them, with loss, skin depth and dispersion; at a boundary, waves reflect and refract, which gives coatings, total internal reflection and shielding.
- **Transmission lines (13-07 to 13-09).** Lines in the time domain (reflections, ringing, termination, TDR), in sinusoidal steady state (input impedance, standing waves, stubs, quarter-wave transformers), and the Smith chart and matching networks, with the Bode–Fano limit on what any match can do.
- **Guided and radiated waves (13-10 and 13-11).** Waveguides, cavities and optical fibre; then radiation, antennas, the Friis link equation and phased arrays.

Work at least the [A] and [B] problems of every chapter (113 of the 152 problems; the 39 [C] problems are the stretch). Every lab has a notebook that runs top to bottom and an ngspice netlist. The notebooks solve fields numerically (finite differences for Laplace's equation, a one-dimensional FDTD wave simulation, a skin-effect diffusion ladder, a mode solver for the guide and the fibre, and direct summation of array fields), so you see the field shapes that the formulas summarize. The netlists confirm the circuit side: ground bounce, a skin-effect ladder, line reflections and TDR, matching networks, a cavity's RLC model and a small antenna's radiation resistance. Most verify scripts recompute the chapters' numbers by a different route from the text (numerical integration, finite-difference solutions, eigenvalue solvers, ABCD matrices, simulation), so a mismatch in your own work usually means a wrong method rather than a rounding difference.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- divergence measures sources and curl measures circulation, and the integral theorems turn local laws into statements about surfaces and loops (13-01);
- a boundary-value problem has one answer, so any construction that meets the boundaries (an image, a series, a numerical grid) is the answer (13-02);
- inductance is stored magnetic energy per current squared, set by geometry; in a gapped core the gap stores most of the energy (13-03);
- a changing magnetic field makes a curling electric field and a changing electric field acts as a current; together they make waves, and $\sigma/\omega\varepsilon$ decides whether a material conducts or insulates at a given frequency (13-04);
- in a good conductor fields die within a skin depth, $1/\sqrt{\pi f\mu\sigma}$, so high-frequency current crowds into the surface (13-05);
- reflection is impedance mismatch: the same formula, $(Z - Z_0)/(Z + Z_0)$, works for plane waves, lines and loads (13-06, 13-07, 13-08);
- a wire is a transmission line once its delay is comparable to the signal's rise time, and termination is how you stop the reflections (13-07);
- a quarter-wave line inverts impedance and a half-wave line repeats it, and matching trades bandwidth for the size of the impedance step (13-08, 13-09);
- a waveguide is a high-pass filter whose cutoff is set by its width, and a fibre is a waveguide for light (13-10);
- an antenna's gain and effective aperture are two views of one quantity, $A_e = G\lambda^2/4\pi$, and an array of $N$ coherent elements gains $N$ in directivity and $N^2$ in EIRP (13-11).

The [equation sheet](../../reference/equation-sheets/13-electromagnetics.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes. It allows a calculator, the equation sheet and a printed Smith chart, but not Python or a simulator. Aim for at least 70%. Questions 1 to 12 follow the chapters; Question 13 asks for three short derivations (the wave equation, line input impedance, and a short dipole's radiation resistance); Question 14 is a diligence question built around a millimetre-wave array start-up's claims, graded against a rubric. The course maps onto the FE Electrical and Computer exam's Electromagnetics area ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/13-electromagnetics.csv) (101 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Electromagnetic claims hide their geometry, their frequency and their conditions. This course teaches you to ask:

- whether a speed or bandwidth claim for a package, board or cable accounts for loss, reflections and the skin effect at the frequencies the signal actually contains;
- what an RF or antenna figure (gain, EIRP, range, efficiency) assumes about matching, scan angle, band edge and the user's hand and head;
- whether a link budget is free-space arithmetic or includes fading, blockage and margin;
- whether an array, filter or matching network can physically cover the bandwidth claimed (grating lobes, Bode–Fano, the Q of a resonator);
- which parts of a product's performance come from physics that will not change and which from engineering that a competitor can copy.
