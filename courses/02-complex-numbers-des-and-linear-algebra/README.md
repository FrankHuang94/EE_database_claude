<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 02 · Complex Numbers, Differential Equations and Linear Algebra

The three mathematical workhorses of EE. Complex numbers and phasors turn sinusoids into algebra; linear ODEs describe every circuit with memory; linear algebra solves large circuits and underpins state-space, signal processing and machine learning hardware.

| | |
|---|---|
| **Term** | 1 |
| **Study hours** | ≈ 110 |
| **University equivalents** | Differential Equations + Linear Algebra (sophomore math); MIT 18.03 / 18.06; Berkeley EE16A/B (linear-algebra and ODE content) |
| **Textbook alignment** | Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*; Strang, *Introduction to Linear Algebra*; Kreyszig, *Advanced Engineering Mathematics* (complex numbers, ODE and linear-algebra parts) |
| **Free courses** | MIT OCW 18.03SC Differential Equations; MIT OCW 18.06SC Linear Algebra; Berkeley EE16A/EE16B course notes |
| **Prerequisites** | [01 · Calculus for Engineers](../01-calculus-for-engineers/README.md) |
| **FE areas** | Mathematics, Linear Systems |

## Learning objectives

1. Work fluently with complex numbers in rectangular, polar and exponential form, and represent sinusoids as phasors.
2. Solve first- and second-order linear constant-coefficient ODEs (homogeneous and forced) and interpret the characteristic roots physically.
3. Use the Laplace transform to solve linear ODEs with initial conditions.
4. Solve linear systems by elimination; compute determinants, inverses and rank; reason about solution existence and uniqueness.
5. Compute eigenvalues and eigenvectors and use them to decouple systems of ODEs.
6. Apply basic numerical methods (Newton, Euler/Runge–Kutta, numerical linear algebra) and recognize ill-conditioning.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [02-01 · Complex Numbers, Euler's Formula and Phasors](chapters/02-01-complex-numbers-euler-and-phasors.md) | 10 | ✅ verified | [problems](problems/02-01-problems.md) · [solutions](solutions/02-01-solutions.md) · [lab](labs/02-01-lab/README.md) · [verify](verify/verify_02_01.py) |
| [02-02 · First-Order Linear ODEs](chapters/02-02-first-order-linear-odes.md) | 10 | ✅ verified | [problems](problems/02-02-problems.md) · [solutions](solutions/02-02-solutions.md) · [lab](labs/02-02-lab/README.md) · [verify](verify/verify_02_02.py) |
| [02-03 · Second-Order Linear ODEs and the Characteristic Equation](chapters/02-03-second-order-linear-odes.md) | 12 | ✅ verified | [problems](problems/02-03-problems.md) · [solutions](solutions/02-03-solutions.md) · [lab](labs/02-03-lab/README.md) · [verify](verify/verify_02_03.py) |
| [02-04 · Forced Response and Resonance](chapters/02-04-forced-response-and-resonance.md) | 10 | ✅ verified | [problems](problems/02-04-problems.md) · [solutions](solutions/02-04-solutions.md) · [lab](labs/02-04-lab/README.md) · [verify](verify/verify_02_04.py) |
| [02-05 · The Laplace Transform for ODEs](chapters/02-05-laplace-transform-for-odes.md) | 10 | ✅ verified | [problems](problems/02-05-problems.md) · [solutions](solutions/02-05-solutions.md) · [lab](labs/02-05-lab/README.md) · [verify](verify/verify_02_05.py) |
| [02-06 · Vectors, Matrices and Linear Systems](chapters/02-06-vectors-matrices-and-linear-systems.md) | 12 | ✅ verified | [problems](problems/02-06-problems.md) · [solutions](solutions/02-06-solutions.md) · [lab](labs/02-06-lab/README.md) · [verify](verify/verify_02_06.py) |
| [02-07 · Determinants, Inverses, Rank and Vector Spaces](chapters/02-07-determinants-inverses-and-vector-spaces.md) | 10 | ✅ verified | [problems](problems/02-07-problems.md) · [solutions](solutions/02-07-solutions.md) · [lab](labs/02-07-lab/README.md) · [verify](verify/verify_02_07.py) |
| [02-08 · Eigenvalues and Eigenvectors](chapters/02-08-eigenvalues-and-eigenvectors.md) | 12 | ✅ verified | [problems](problems/02-08-problems.md) · [solutions](solutions/02-08-solutions.md) · [lab](labs/02-08-lab/README.md) · [verify](verify/verify_02_08.py) |
| [02-09 · Systems of Linear ODEs and the Matrix Exponential](chapters/02-09-systems-of-odes-and-matrix-exponential.md) | 10 | ✅ verified | [problems](problems/02-09-problems.md) · [solutions](solutions/02-09-solutions.md) · [lab](labs/02-09-lab/README.md) · [verify](verify/verify_02_09.py) |
| [02-10 · Numerical Methods for Engineers](chapters/02-10-numerical-methods.md) | 8 | ✅ verified | [problems](problems/02-10-problems.md) · [solutions](solutions/02-10-solutions.md) · [lab](labs/02-10-lab/README.md) · [verify](verify/verify_02_10.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/02-complex-numbers-des-and-linear-algebra.csv) · [Equation sheet](../../reference/equation-sheets/02-complex-numbers-des-and-linear-algebra.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 02 takes about 104 hours and has three blocks. Complex numbers and phasors (02-01) come first, because everything after uses them. The differential-equations block (02-02 to 02-05) runs from first-order circuits through resonance to the Laplace transform. The linear-algebra block (02-06 to 02-08) runs from elimination and nodal analysis to eigenvalues and the SVD. Two chapters join the blocks: 02-09 treats a system of ODEs as one matrix equation, and 02-10 shows how a computer (and SPICE in particular) actually carries out the arithmetic. Doing the chapters in order is simplest. If you want variety, 02-06 needs only 02-01 and Course 01, so you can interleave the two blocks, but 02-08 needs 02-03 and 02-09 needs both blocks. Work at least the [A] and [B] problems of every chapter before moving on. Nine of the ten labs pair a notebook with ngspice netlists, so you can watch each equation become a circuit.

**What to master cold.** Phasor arithmetic and impedance (02-01); the first-order step and ramp responses (02-02); ζ, $Q$, overshoot and settling (02-03); complex replacement and the resonance and bandwidth formulas (02-04); Laplace inversion by partial fractions and the transfer function (02-05); elimination, LU and nodal stamping (02-06); rank, null space and least squares (02-07); eigenvalues, diagonalization and the SVD (02-08); state space and $e^{\mathbf{A}t}$ (02-09); and floating point, Newton's method, stiffness and conditioning (02-10). Courses 06–07 (circuits), 11 (signals and systems) and 15 (control) build directly on them. The [equation sheet](../../reference/equation-sheets/02-complex-numbers-des-and-linear-algebra.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions, takes 210 minutes, and allows a calculator and the equation sheet but not Python. Aim for at least 70%. Question 15(c) is a short-answer diligence question about a low-precision solver claim. The [flashcards](../../flashcards/02-complex-numbers-des-and-linear-algebra.csv) (140 cards) are for spaced review alongside the chapters.

**Perishable content.** The mathematics is timeless. The dated facts are in the practitioner sections, logged as [R-029](../../reference/research-log.md#r-029--jedec-thermal-test-environments-jesd51-2a) to [R-057](../../reference/research-log.md#r-057--patriot-missile-timing-error) in the research log. The ones most likely to move are the supercomputer and accelerator figures ([R-038](../../reference/research-log.md#r-038--hpl-and-the-top500-list), [R-040](../../reference/research-log.md#r-040--nvidia-h100-and-rubin-arithmetic-and-memory-figures), [R-055](../../reference/research-log.md#r-055--hpl-mxp-mixed-precision-benchmark)), the wireless standards ([R-041](../../reference/research-log.md#r-041--5g-nr-mimo-layers), [R-042](../../reference/research-log.md#r-042--wi-fi-spatial-streams-80211ax-and-80211be), [R-045](../../reference/research-log.md#r-045--5g-nr-type-ii-csi-and-eigenvector-feedback)) and the simulator defaults ([R-053](../../reference/research-log.md#r-053--ngspice-numerical-defaults-and-junction-limiting)). Check those entries once a year.
