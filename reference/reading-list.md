# Reading List

The textbook and free-course alignment for every course is listed in [CURRICULUM.md](../CURRICULUM.md) and in each course README. Below, every chapter's *Further study* list is collected in course order by `tools/build_reference.py`: textbook sections, free courses and lecture videos, and the landmark papers (ISSCC, IEDM, VLSI Symposium, Hot Chips, JSSC) the chapters cite. For a single next read per course, take the first textbook entry of the course's first chapter and the paper the course's practitioner sections cite most.

<!-- BEGIN GENERATED (tools/build_reference.py): edit the chapters or glossary.yml, not this block -->

## By chapter

Each chapter's *Further study* list: textbook sections, free courses, lecture videos and landmark papers, in course order.

## [00 · Orientation](../courses/00-orientation/README.md)

### [00-01 · The Map of Electrical Engineering](../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md)

- **Hambley, *Electrical Engineering: Principles and Applications*,** chapter 1: a survey of EE's subfields from a standard introductory text.
- **IEEE Spectrum** (spectrum.ieee.org): the IEEE's general-audience magazine, the best way to watch all the subdisciplines evolve.
- **WSTS and SIA press releases:** the primary sources for market data; check them each spring and autumn.

### [00-02 · The Abstraction Stack: Physics to Software](../courses/00-orientation/chapters/00-02-the-abstraction-stack.md)

- **Agarwal & Lang, *Foundations of Analog and Digital Electronic Circuits*,** chapter 1 (the lumped-matter discipline) and chapter 5 (the digital abstraction and noise margins). This is the textbook of MIT 6.002, which this chapter follows most closely.
- **MIT OpenCourseWare 6.002, lectures 1 and 4:** the abstraction lectures, online with video.
- **Patterson & Hennessy, *Computer Organization and Design*,** chapter 1: abstraction as one of the "great ideas" of computer architecture.
- **Bogatin, *Signal and Power Integrity — Simplified*:** a readable account of when interconnects stop being "just wires".

### [00-03 · How to Study This Curriculum](../courses/00-orientation/chapters/00-03-how-to-study-this-curriculum.md)

- **Brown, Roediger & McDaniel, *Make It Stick: The Science of Successful Learning* (2014):** a readable book-length treatment of the research in §3.1.
- **Dunlosky et al. (2013)**, cited in §3.1: the source review. Its summary tables are worth reading directly.
- **Pólya, *How to Solve It* (1945):** the classic problem-solving heuristics behind §3.3.
- **The Anki manual,** on importing CSV decks and adjusting review settings (see [flashcards/README.md](../flashcards/README.md)).

### [00-04 · Toolchain Setup Walkthrough](../courses/00-orientation/chapters/00-04-toolchain-walkthrough.md)

- **ngspice User's Manual** (free, on the ngspice website): the chapters on circuit description, analyses and the `.meas` statement.
- **Harris & Harris, *Digital Design and Computer Architecture*:** the HDL chapter and its testbench section.
- **D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic,"** *ACM Computing Surveys*, 1991: the classic, readable reference.
- **L. W. Nagel, *SPICE2: A Computer Program to Simulate Semiconductor Circuits*,** UC Berkeley ERL Memo M520, 1975: the original SPICE thesis, still a clear account of how the solver works.

### [00-05 · How Chip Companies' Engineering Organizations Work](../courses/00-orientation/chapters/00-05-how-chip-companies-are-organized.md)

- **The Wilson Research Group / Siemens EDA functional verification study:** the executive summary and blog series on Siemens' *Verification Horizons* blog ([R-018](research-log.md#r-018--functional-verification-study-wilson-research-group--siemens-eda) links them).
- **Weste & Harris, *CMOS VLSI Design*,** the chapter on design methodology and the chip design flow.
- **Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*,** chapter 1 on cost and the design process.

## [01 · Calculus for Engineers](../courses/01-calculus-for-engineers/README.md)

### [01-01 · Functions, Models and Units](../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 1 (functions, exponentials, inverse functions and logarithms) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 1 and the sections on exponentials and logarithms.
- **MIT OpenCourseWare 18.01SC,** Unit 1 review sessions on exponentials and logarithms.

### [01-02 · Limits and Continuity](../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 2 (limits, limit laws, continuity, limits at infinity) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 2 (derivatives as limits) and the section on limits and continuity.
- **MIT OpenCourseWare 18.01SC,** Unit 1 sessions on limits and continuity.
- **3Blue1Brown, *Essence of Calculus*** (video series), episodes on limits and on what $e$ is, for geometric intuition.

### [01-03 · Derivatives: Rates of Change in Circuits](../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 3 (differentiation rules) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapters 2–4.
- **MIT OpenCourseWare 18.01SC,** Unit 1 (differentiation).
- **3Blue1Brown, *Essence of Calculus*,** the episodes on derivative formulas, the chain and product rules, and implicit differentiation.

### [01-04 · Applications of Derivatives](../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md)

- **Stewart, *Calculus: Early Transcendentals*,** sections on related rates, linear approximation, the mean value theorem, optimization, L'Hôpital's rule and Newton's method (chapters 3–4).
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 3 (applications of the derivative).
- **MIT OpenCourseWare 18.01SC,** Unit 2 (applications of differentiation).
- **B. Razavi, *Design of Analog CMOS Integrated Circuits*,** the opening chapters, for how the small-signal idea is used in practice (preview for Course 10).

### [01-05 · Integrals: Accumulating Charge and Energy](../courses/01-calculus-for-engineers/chapters/01-05-integrals.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 5 (integrals) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 5 (integrals).
- **MIT OpenCourseWare 18.01SC,** Unit 3 (the definite integral and its applications).
- **3Blue1Brown, *Essence of Calculus*,** episodes on integration and the fundamental theorem.

### [01-06 · Techniques of Integration](../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 7 (techniques of integration) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 7 (techniques of integration).
- **MIT OpenCourseWare 18.01SC,** Unit 4 (techniques of integration).
- **W. C. Elmore, "The transient response of damped linear networks with particular regard to wideband amplifiers,"** *Journal of Applied Physics*, vol. 19, 1948, pp. 55–63: the origin of the Elmore delay.

### [01-07 · Applications of Integration](../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md)

- **Stewart, *Calculus: Early Transcendentals*,** sections on average value, work and probability (chapters 6 and 8).
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 8 (applications of the integral).
- **W. Kester (ed.), *The Data Conversion Handbook*,** Analog Devices: the derivation and use of 6.02N + 1.76 dB and ENOB.
- **MIT OpenCourseWare 18.05,** *Introduction to Probability and Statistics*, for continuous random variables.

### [01-08 · Sequences, Series and Taylor Expansions](../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 11 (sequences and series) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 10 (infinite series).
- **MIT OpenCourseWare 18.01SC,** Unit 5 (infinite series and Taylor series).
- **B. Razavi, *RF Microelectronics*,** chapter 2 (nonlinearity: harmonics, compression, intermodulation), for the engineering use of §3.8.

### [01-09 · Multivariable Calculus I: Partial Derivatives and Gradients](../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapter 14 (partial derivatives) for more drill.
- **Strang, *Calculus* (free, MIT OpenCourseWare),** chapter 13 (partial derivatives).
- **MIT OpenCourseWare 18.02SC,** *Multivariable Calculus*, Unit 2 (partial derivatives).
- **S. Boyd and L. Vandenberghe, *Convex Optimization*** (free online), chapters 1 and 5, for where Lagrange multipliers lead.

### [01-10 · Multivariable Calculus II: Multiple, Line and Surface Integrals](../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md)

- **Stewart, *Calculus: Early Transcendentals*,** chapters 15–16 (multiple integrals and vector calculus).
- **MIT OpenCourseWare 18.02SC,** *Multivariable Calculus*, Units 3–4 (double integrals, line integrals, triple integrals, surface integrals).
- **H. M. Schey, *Div, Grad, Curl, and All That*,** an informal and very readable introduction to vector calculus through electrostatics.
- **J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*,** chapter 1 (cost of an integrated circuit: dies per wafer and yield).

## [02 · Complex Numbers, Differential Equations and Linear Algebra](../courses/02-complex-numbers-des-and-linear-algebra/README.md)

### [02-01 · Complex Numbers, Euler's Formula and Phasors](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md)

- **Kreyszig, *Advanced Engineering Mathematics*:** the opening sections of the complex-numbers chapter (complex plane, polar form, powers and roots), for more drill on the algebra.
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** the chapter "Sinusoids and Phasors" covers the same material from the circuits side, with many practice problems.
- **Nilsson & Riedel, *Electric Circuits*:** the phasor sections at the start of the sinusoidal steady-state chapter.
- **MIT OpenCourseWare 18.03SC *Differential Equations*:** Unit I sessions on complex numbers and complex exponentials, with recitation videos.
- **Berkeley EE16B course notes:** the phasor notes connect this chapter directly to circuits and to linear algebra.

### [02-02 · First-Order Linear ODEs](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md)

- Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*, chapter 2 (first-order equations: linear, separable, autonomous, existence and uniqueness, Euler's method).
- MIT OCW 18.03SC *Differential Equations*, Unit I (first-order equations), including the direction-field and integrating-factor sessions.
- Strang, *Differential Equations and Linear Algebra*, chapter 1 (first-order equations, with the growth-and-decay viewpoint used here).
- Kreyszig, *Advanced Engineering Mathematics*, chapter 1 (first-order ODEs, with the modeling examples).

### [02-03 · Second-Order Linear ODEs and the Characteristic Equation](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md)

- Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*, chapter 3 (second-order linear equations: constant coefficients, complex and repeated roots, the Wronskian, mechanical and electrical vibrations).
- MIT OCW 18.03SC *Differential Equations*, Unit II (second-order constant-coefficient linear equations, damped oscillators).
- Strang, *Differential Equations and Linear Algebra*, chapter 2 (second-order equations, with the damping and frequency viewpoint used here).
- Alexander & Sadiku, *Fundamentals of Electric Circuits*, chapter on second-order circuits (series and parallel RLC natural and step responses).

### [02-04 · Forced Response and Resonance](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md)

- Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*, chapter 3 (nonhomogeneous equations, undetermined coefficients, variation of parameters, forced vibrations).
- MIT OCW 18.03SC *Differential Equations*, Unit II sessions on the exponential response formula, complex replacement, frequency response and resonance.
- Strang, *Differential Equations and Linear Algebra*, chapter 2 (forced oscillations and the frequency response).
- Alexander & Sadiku, *Fundamentals of Electric Circuits*, chapter on frequency response (series and parallel resonance, quality factor, bandwidth).

### [02-05 · The Laplace Transform for ODEs](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md)

- Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*, chapter 6 (the Laplace transform: definition, IVPs, step functions, impulse functions, convolution).
- MIT OCW 18.03SC *Differential Equations*, Unit III (Fourier series and the Laplace transform: poles, transfer functions, convolution, the delta function).
- Kreyszig, *Advanced Engineering Mathematics*, chapter on Laplace transforms (with an extended table).
- Oppenheim & Willsky, *Signals and Systems*, chapter on the Laplace transform (the engineering view of poles, zeros and regions of convergence).

### [02-06 · Vectors, Matrices and Linear Systems](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md)

- Strang, *Introduction to Linear Algebra*, chapters 1 (vectors, lengths, dot products, matrices) and 2 (solving linear equations, elimination, $\mathbf{A} = \mathbf{L}\mathbf{U}$, transposes and permutations).
- MIT OCW 18.06 *Linear Algebra* (Strang), lectures 1–5: the geometry of linear equations, elimination, multiplication and inverses, factorization into $\mathbf{L}\mathbf{U}$, transposes and permutations.
- Trefethen and Bau, *Numerical Linear Algebra*, lectures 20–23 (Gaussian elimination, pivoting, stability, Cholesky), for the floating-point view.
- Davis, *Direct Methods for Sparse Linear Systems* (SIAM, 2006), for how sparse LU works inside circuit simulators.

### [02-07 · Determinants, Inverses, Rank and Vector Spaces](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md)

- Strang, *Introduction to Linear Algebra*: sections 2.5 (inverses), 3.1–3.5 (vector spaces, null space, rank, complete solution, independence and basis), 4.1–4.3 (orthogonal subspaces, projections, least squares), 5.1–5.3 (determinants and Cramer's rule), and the chapter section on graphs and networks.
- MIT OCW 18.06 *Linear Algebra* (Strang), lectures 3, 5–10, 15–16 and 18–20.
- Boyd and Vandenberghe, *Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares* (Cambridge University Press, 2018), chapters on least squares and data fitting, with engineering examples.
- Trefethen and Bau, *Numerical Linear Algebra*, lectures 7–11 (QR and least squares done stably).

### [02-08 · Eigenvalues and Eigenvectors](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md)

- Strang, *Introduction to Linear Algebra*, chapters 6 (eigenvalues, diagonalization, symmetric and positive definite matrices) and 7 (the singular value decomposition, principal components).
- MIT OCW 18.06 *Linear Algebra* (Strang), lectures 21–22, 24–25 and 27–30.
- Trefethen and Bau, *Numerical Linear Algebra*, lectures 4–5 (the SVD) and 24–29 (how eigenvalues are computed, including the QR algorithm).
- Tse and Viswanath, *Fundamentals of Wireless Communication* (Cambridge University Press, 2005), chapter 7, for MIMO and the SVD.

### [02-09 · Systems of Linear ODEs and the Matrix Exponential](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md)

- Boyce & DiPrima, *Elementary Differential Equations and Boundary Value Problems*, chapter 7 (systems of first-order linear equations, phase plane, fundamental matrices).
- MIT OCW 18.03SC *Differential Equations*, Unit IV, "First-Order Systems" (the matrix exponential, phase portraits).
- Strang, *Introduction to Linear Algebra*, section 6.3 (differential equations and $e^{At}$).
- Franklin, Powell and Emami-Naeini, *Feedback Control of Dynamic Systems*, chapter on state-space design, for the controls view.

### [02-10 · Numerical Methods for Engineers](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md)

- Heath, *Scientific Computing: An Introductory Survey*, chapters 1 (error and floating point), 2 (linear systems and conditioning), 5 (nonlinear equations) and 9 (initial-value problems and stiffness).
- Within this curriculum: numerical integration (quadrature) in [01-06](../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md) §3.7, and finite-difference derivatives in [01-03](../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) §3.9.
- Chapra and Canale, *Numerical Methods for Engineers*, parts on roots of equations and ordinary differential equations.
- Goldberg, D., "What Every Computer Scientist Should Know About Floating-Point Arithmetic," *ACM Computing Surveys*, 1991, the classic tutorial.
- Najm, *Circuit Simulation* (Wiley, 2010), for MNA, companion models, Newton iteration and integration inside SPICE.

## [03 · Probability, Statistics and Random Variables for EE](../courses/03-probability-statistics-and-random-variables/README.md)

### [03-01 · Probability in EE Language](../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md)

- Bertsekas, D. P. and Tsitsiklis, J. N., *Introduction to Probability*, 2nd ed., chapter 1 (sample spaces, conditioning, Bayes' rule, independence, counting).
- Leon-Garcia, A., *Probability, Statistics, and Random Processes for Electrical Engineering*, 3rd ed., chapter 2.
- MIT OpenCourseWare 6.041SC *Probabilistic Systems Analysis and Applied Probability*, lectures 1–4 and the recitations on Bayes' rule.
- Bushnell, M. L. and Agrawal, V. D., *Essentials of Electronic Testing*, chapter 3 (yield, defect level and test economics).

### [03-02 · Random Variables and Distributions](../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md)

- Bertsekas, D. P. and Tsitsiklis, J. N., *Introduction to Probability*, 2nd ed., chapters 2 (discrete random variables) and 3 (continuous random variables).
- Leon-Garcia, A., *Probability, Statistics, and Random Processes for Electrical Engineering*, 3rd ed., chapters 3 and 4.
- MIT OpenCourseWare 6.041SC, lectures 5–8.
- Keysight white paper 5989-3206EN, *Jitter Analysis: The dual-Dirac Model, RJ/DJ, and Q-Scale*, for the jitter conventions used in industry.

### [03-03 · Expectation, Variance and Functions of Random Variables](../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md)

- Bertsekas, D. P. and Tsitsiklis, J. N., *Introduction to Probability*, 2nd ed., chapters 2 and 3 (expectation and variance) and 4 (derived distributions).
- Leon-Garcia, A., *Probability, Statistics, and Random Processes for Electrical Engineering*, 3rd ed., chapters 3 and 4.
- MIT OpenCourseWare 6.041SC lectures on these topics.
- Keysight application note 5968-6875E, *Characterizing Digitally Modulated Signals with CCDF Curves*, for how PAPR is measured in practice.

### [03-04 · Joint Distributions, Correlation and the CLT](../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md)

- Bertsekas, D. P. and Tsitsiklis, J. N., *Introduction to Probability*, 2nd ed., chapters 2–4 (joint distributions, covariance, sums, conditional expectation and total variance) and 5 (limit theorems).
- Leon-Garcia, A., *Probability, Statistics, and Random Processes for Electrical Engineering*, 3rd ed., chapters 5–7.
- MIT OpenCourseWare 6.041SC lectures on these topics.
- The IEEE 802.3 contributions in Sources 3, 4 and 6, for the binomial tail in a real standard.

### [03-05 · Estimation and Hypothesis Testing for Engineers](../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md)

- Montgomery, D. C. and Runger, G. C., *Applied Statistics and Probability for Engineers*, the chapters on point estimation, confidence intervals, hypothesis tests and process capability.
- NIST/SEMATECH *e-Handbook of Statistical Methods*, chapters 6 (process capability) and 8 (reliability, including the Weibull and Arrhenius models); free online.
- Bertsekas, D. P. and Tsitsiklis, J. N., *Introduction to Probability*, 2nd ed., chapter 9 (classical statistical inference).
- MIT OpenCourseWare 6.041SC, the lectures on classical statistics.

### [03-06 · Random Processes Preview: Noise](../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md)

- Leon-Garcia, A., *Probability, Statistics, and Random Processes for Electrical Engineering*, 3rd ed., chapters 9 and 10 (random processes, power spectral density, linear systems with random inputs).
- Razavi, B., *Design of Analog CMOS Integrated Circuits*, the chapter on noise (thermal, flicker and shot noise in circuits).
- Keysight application note 5952-8255E, *Fundamentals of RF and Microwave Noise Figure Measurements*, for $kT_0$ and noise figure in practice.

## [04 · Physics for EE](../courses/04-physics-for-ee/README.md)

### [04-01 · Mechanics Essentials for EE](../courses/04-physics-for-ee/chapters/04-01-mechanics-essentials.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on Newton's laws, work and energy, momentum, rotation and oscillations.
- MIT OpenCourseWare 8.01 (Classical Mechanics), the lectures on energy, momentum and simple harmonic motion.
- Senturia, S. D., *Microsystem Design*, Kluwer, 2001, chapters on lumped modeling and the electromechanical analogies, for MEMS.
- Gabrielson, T. B., "Mechanical-thermal noise in micromachined acoustic and vibration sensors", *IEEE Transactions on Electron Devices* 40(5):903–909, 1993, the classic derivation of the $4kTb$ force noise.

### [04-02 · Charge, Coulomb's Law and Electric Fields](../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on Coulomb's law and electric fields.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapters 1 and 2.
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on charges, fields and dipoles.
- ESD Association, "Fundamentals of Electrostatic Discharge, Part Five: Device Sensitivity and Testing", 2024, for the HBM, CDM and system-level models.

### [04-03 · Gauss's Law](../courses/04-physics-for-ee/chapters/04-03-gauss-law.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapter on Gauss's law.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, sections 1.10–1.13 (flux and Gauss's law) and 3.1–3.3 (conductors).
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on Gauss's law and conductors.
- Pierret, R. F., *Semiconductor Device Fundamentals*, Addison-Wesley, 1996, the chapter on pn-junction electrostatics, for the depletion approximation developed further.

### [04-04 · Electric Potential, Capacitance and Dielectrics](../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on electric potential and capacitance.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapters 2 (potential), 3 (conductors and capacitance) and 10 (dielectrics).
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on potential, capacitors and dielectrics.
- Jenkins, M. et al., "Review—Beyond the highs and lows: a perspective on the future of dielectrics research for nanoelectronic devices", *ECS Journal of Solid State Science and Technology* 8, N159, 2019, for high-k and low-k materials in depth.

### [04-05 · Current, Resistance and Conduction](../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapter on current and resistance.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapter 4.
- Ashcroft, N. W. and Mermin, N. D., *Solid State Physics*, Saunders, 1976, chapters 1–2 (the Drude and Sommerfeld models).
- Soulié, J.-P. et al., "Selecting alternative metals for advanced interconnects", *Journal of Applied Physics* 136, 171101, 2024 (arXiv:2406.09106), a readable tutorial on the interconnect problem.

### [04-06 · Magnetic Fields and Forces](../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on magnetic fields and on magnetic fields due to currents.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapters 6 (the magnetic field) and 11 (magnetic fields in matter).
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on magnetic forces, Biot–Savart and Ampère's law.
- Allegro MicroSystems and Texas Instruments application notes on Hall-effect sensing, for practical sensor design.

### [04-07 · Faraday's Law, Lenz's Law and Inductance](../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapter on induction and inductance.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapter 7.
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on Faraday's law, inductance and transformers.
- Erickson, R. W. and Maksimović, D., *Fundamentals of Power Electronics*, the chapters on magnetics, for inductor and transformer design.

### [04-08 · Energy in Fields and Maxwell's Equations (Preview)](../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on Maxwell's equations and electromagnetic waves.
- Purcell, E. M. and Morin, D. J., *Electricity and Magnetism*, 3rd ed., Cambridge University Press, 2013, chapter 9.
- MIT OpenCourseWare 8.02 (Physics II: Electricity and Magnetism), the lectures on displacement current, Maxwell's equations and electromagnetic waves.
- Texas Instruments, *High-Speed Layout Guidelines* (SCAA082A), for a practitioner's view of propagation on boards.

### [04-09 · Waves and Optics Basics](../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on waves, interference, diffraction and refraction.
- Hecht, E., *Optics*, 5th ed., Pearson, 2017, for a complete undergraduate optics course.
- MIT OpenCourseWare 8.03 (Physics III: Vibrations and Waves).
- ASML, "The Rayleigh criterion for resolution" (Technology pages), for lithography resolution in the vendor's own terms.

### [04-10 · Introduction to Quantum Mechanics](../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md)

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on photons and matter waves.
- Griffiths, D. J. and Schroeter, D. F., *Introduction to Quantum Mechanics*, 3rd ed., Cambridge University Press, 2018, chapters 1–2, for the full treatment.
- Hu, C., *Modern Semiconductor Devices for Integrated Circuits*, Pearson, 2010, chapter 1 (free from the author's site), for quantum ideas in device language.
- MIT OpenCourseWare 8.04 (Quantum Physics I), the opening lectures.

### [04-11 · Introduction to Solid-State Physics](../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md)

- Kittel, C., *Introduction to Solid State Physics*, 8th ed., Wiley, 2005, chapters 1, 6 and 7.
- Ashcroft, N. W. and Mermin, N. D., *Solid State Physics*, Saunders, 1976, chapters 2, 8 and 9 (Sommerfeld, Bloch, nearly free electrons).
- Hu, C., *Modern Semiconductor Devices for Integrated Circuits*, Pearson, 2010, chapter 1 (free from the author's site).

## [05 · Programming for Engineers](../courses/05-programming-for-engineers/README.md)

### [05-01 · Python Fundamentals for Engineers](../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md)

- Downey, A. B., *Think Python*, 2nd or 3rd ed., Green Tea Press / O'Reilly (free online), chapters 1–11 and 14.
- The official Python Tutorial, docs.python.org, sections 3–9, especially §15, "Floating-Point Arithmetic: Issues and Limitations".
- MIT OpenCourseWare 6.0001, *Introduction to Computer Science and Programming in Python*, lectures 1–8.

### [05-02 · NumPy, Vectorization and Numerical Computing](../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md)

- VanderPlas, J., *Python Data Science Handbook*, 2nd ed., O'Reilly (free online), chapter 2, "Introduction to NumPy".
- The NumPy User Guide, numpy.org: "NumPy: the absolute basics for beginners" and "Broadcasting".
- Goldberg, D., "What every computer scientist should know about floating-point arithmetic", *ACM Computing Surveys* 23(1), 1991, sections 1–2.
- *Video:* VanderPlas, J., "Losing Your Loops: Fast Numerical Computing with NumPy", PyCon US 2015 (30 minutes; the recording is listed on pyvideo.org), a talk on replacing Python loops with whole-array operations.

### [05-03 · SciPy, SymPy and Matplotlib](../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md)

- VanderPlas, J., *Python Data Science Handbook*, 2nd ed., chapter 4, "Visualization with Matplotlib" (free online).
- The SciPy User Guide, docs.scipy.org: "Optimization", "Integration" and "Interpolation" tutorials.
- The SymPy Tutorial, docs.sympy.org: "Basic Operations", "Simplification" and "Solvers".
- *Video:* MIT OpenCourseWare 6.0002, *Introduction to Computational Thinking and Data Science* (Fall 2016), Lecture 9, "Understanding Experimental Data" (fitting models to measurements and judging the fit), and Lecture 10 (continuing the topic).

### [05-04 · Jupyter, Testing and Reproducible Workflows](../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md)

- Chacon, S. and Straub, B., *Pro Git*, 2nd ed., chapters 1–3 (basics and branching) and 10.2 ("Git Objects", how hashes name content); free online at git-scm.com.
- The pytest documentation, "Get started" and "How to use assertions" (docs.pytest.org).
- Software Carpentry lessons "Version Control with Git" and "Programming with Python" (testing and defensive programming), software-carpentry.org.
- Wilson, G. et al., "Good enough practices in scientific computing", *PLOS Computational Biology* 13(6), 2017: a short, practical checklist.

### [05-05 · C Fundamentals](../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md)

- Kernighan, B. W. and Ritchie, D. M., *The C Programming Language*, 2nd ed., chapters 1–4: the classic, compact introduction (it predates C99, so supplement it on types and `//` comments).
- King, K. N., *C Programming: A Modern Approach*, 2nd ed., chapters 1–10, 14 (the preprocessor) and 15 (multi-file programs): the most thorough textbook treatment.
- Regehr, J., "A Guide to Undefined Behavior in C and C++" (blog series, 2010): readable explanations of why UB exists and how compilers exploit it.
- The GCC and Clang documentation on warning options and sanitizers (`-fsanitize=undefined`, `-fsanitize=address`).

### [05-06 · C Pointers, Arrays and Memory](../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md)

- Kernighan and Ritchie, *The C Programming Language*, 2nd ed., chapters 5 (pointers and arrays) and 6 (structures).
- King, *C Programming: A Modern Approach*, 2nd ed., chapters 11–13 (pointers, arrays, strings) and 16–17 (structures, advanced pointers and dynamic storage).
- Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed., sections 3.8–3.10 (arrays, structures, alignment and buffer overflows in machine code) and 9.9 (dynamic memory allocation).
- The AddressSanitizer documentation (Clang and GCC) for what each report means.

### [05-07 · Bit Manipulation and Fixed-Width Integers](../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md)

- Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed., chapter 2 ("Representing and Manipulating Information"): the definitive treatment of integer representations and their arithmetic.
- Warren, H. S., *Hacker's Delight*, 2nd ed., chapters 2–5: bit-manipulation techniques with proofs.
- Valvano, J. W., *Embedded Systems: Introduction to ARM Cortex-M Microcontrollers*, the chapters on I/O registers and fixed-point numbers (free online editions exist).
- Lyons, R. G., *Understanding Digital Signal Processing*, 3rd ed., chapter 12 ("Digital Data Formats and Their Effects").

### [05-08 · Data Structures and Algorithms You Will Need](../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md)

- Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 4th ed., chapters 1–4 (analysis), 6 (heapsort), 7 (quicksort), 8 (lower bound, counting and radix sort), 10–12 (elementary data structures, hash tables, binary search trees).
- Sedgewick and Wayne, *Algorithms*, 4th ed., chapters 1–3, with the free online course and visualizations at algs4.cs.princeton.edu.
- Knuth, *The Art of Computer Programming*, Vol. 3, *Sorting and Searching*, section 6.4 (hashing and the linear-probing analysis), for the derivations behind the probe formulas.
- Bentley, *Programming Pearls*, 2nd ed.: short, practical essays on choosing algorithms and data structures.

### [05-09 · Software Engineering Practices](../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md)

- Sommerville, I., *Software Engineering*, 10th ed., chapters 2 (processes), 3 (agile), 4 (requirements), 7 (design), 8 (testing) and 25 (configuration management).
- Parnas, D. L., "On the Criteria To Be Used in Decomposing Systems into Modules", *Communications of the ACM* 15(12), 1972: the classic statement of information hiding, short and still relevant.
- Hayhurst, K. J. et al., *A Practical Tutorial on Modified Condition/Decision Coverage*, NASA/TM-2001-210876: a clear, free introduction to MC/DC.
- Bossavit, L., *The Leprechauns of Software Engineering* (Leanpub): a skeptical look at widely repeated software-engineering "facts".
- The Agile Manifesto (agilemanifesto.org) and the Semantic Versioning 2.0.0 specification (semver.org): each is one page.

## [06 · Circuit Analysis I (DC)](../courses/06-circuit-analysis-1-dc/README.md)

### [06-01 · Charge, Current, Voltage, Power and the Lumped Circuit Abstraction](../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md)

- Agarwal, A. and Lang, J. H., *Foundations of Analog and Digital Electronic Circuits*, Morgan Kaufmann, 2005, chapter 1 (the lumped matter discipline) and appendix on Maxwell's equations.
- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 1, "Circuit Variables" (SI units, voltage and current, the passive sign convention, power and energy).
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 1, "Introduction and lumped abstraction".
- Penfield, P., Spence, R. and Duinker, S., *Tellegen's Theorem and Electrical Networks*, MIT Press, 1970, for the general theorem and its applications.

### [06-02 · Circuit Elements and Ohm's Law](../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 2, "Circuit Elements" (sources, resistors, Ohm's law, construction of circuit models).
- Agarwal, A. and Lang, J. H., *Foundations of Analog and Digital Electronic Circuits*, chapters 1–2 (element laws, i–v characteristics).
- Horowitz, P. and Hill, W., *The Art of Electronics*, 3rd ed., Cambridge University Press, 2015, chapter 1 and appendix on resistor types (a practitioner's view of real resistors).
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 2, "Basic circuit analysis method".

### [06-03 · Kirchhoff's Laws, Series/Parallel and Dividers](../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 3, "Simple Resistive Circuits" (series, parallel, dividers, the Wheatstone bridge, delta-to-wye).
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 2 (nodes, branches and loops; wye–delta transformations).
- Agarwal, A. and Lang, J. H., *Foundations of Analog and Digital Electronic Circuits*, chapter 2, sections on the KVL/KCL method and on series–parallel simplification.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 2, "Basic circuit analysis method", which covers element combination rules.

### [06-04 · Nodal Analysis](../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 4, "Techniques of Circuit Analysis" (node-voltage method, supernodes).
- Agarwal, A. and Lang, J. H., *Foundations of Analog and Digital Electronic Circuits*, chapter 3, the node method.
- Ho, C.-W., Ruehli, A. E. and Brennan, P. A., "The modified nodal approach to network analysis", *IEEE Transactions on Circuits and Systems* 22(6), 504–509 (1975): the original MNA paper, short and readable.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 3, "Superposition, Thévenin and Norton", which opens by working node-method examples (the method is introduced in Lecture 2) before moving on to superposition.

### [06-05 · Mesh Analysis](../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 4, "Techniques of Circuit Analysis" (the mesh-current method, supermeshes, and choosing between the node-voltage and mesh-current methods).
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 3, "Methods of Analysis" (mesh analysis, nodal versus mesh).
- *Video:* W. McAllister, "Mesh current method" (steps 1–3 and 4–5), Spinning Numbers (spinningnumbers.org), short videos originally made for Khan Academy's electrical engineering course.

### [06-06 · Dependent Sources](../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 2 (dependent sources as circuit elements) and chapter 4 (node-voltage and mesh-current methods with dependent sources).
- Sedra, A. S. and Smith, K. C., *Microelectronic Circuits*, the chapters on MOSFET and BJT small-signal models and the basic single-stage amplifiers.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 8, "Dependent Sources and Amplifiers".

### [06-07 · Linearity and Superposition](../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 4, sections on source transformations and superposition.
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 4, "Circuit Theorems" (linearity, superposition, source transformation).
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 3, "Superposition, Thévenin and Norton".

### [06-08 · Thévenin and Norton Equivalents](../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 4, sections on Thévenin and Norton equivalents.
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 4, "Circuit Theorems".
- D. H. Johnson, "Origins of the equivalent circuit concept: the voltage-source equivalent" and "…: the current-source equivalent", *Proceedings of the IEEE* 91(4), 636–640, and 91(5), 817–821 (2003): two short, readable histories.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 3, "Superposition, Thévenin and Norton".

### [06-09 · Maximum Power Transfer](../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 4, section on maximum power transfer.
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 4, "Maximum Power Transfer".
- Pozar, D. M., *Microwave Engineering*, the chapter on transmission-line theory (coaxial line parameters and loss), for the physics behind Example 06-09.5.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 3, "Superposition, Thévenin and Norton" (Thévenin equivalents, the basis of this chapter).

### [06-10 · The Ideal Op-Amp](../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, chapter 5, "The Operational Amplifier".
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 5, "Operational Amplifiers".
- Sedra, A. S. and Smith, K. C., *Microelectronic Circuits*, chapter 2 (operational amplifiers, including DC imperfections).
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 19, "The Operational Amplifier Abstraction", and Lecture 20, op-amp circuits.

### [06-11 · Practical DC Circuits and Measurement](../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, the sections on measuring voltage and current and on the Wheatstone bridge in the chapter on simple resistive circuits.
- Horowitz, P. and Hill, W., *The Art of Electronics*, 3rd ed., chapter 1 (voltage dividers, input and output impedance) and the discussions of current sensing and remote sensing in the chapter on voltage regulation.
- Keithley Instruments (now Tektronix), *Low Level Measurements Handbook*, the sections on low-resistance (four-wire) measurement and on high-resistance sources.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), Lecture 3, "Superposition, Thévenin and Norton", for the Thévenin view of loading that this chapter applies to instruments.

## [07 · Circuit Analysis II (Transient and AC)](../courses/07-circuit-analysis-2-transient-and-ac/README.md)

### [07-01 · Capacitors and Inductors](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md)

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, the chapter on inductance, capacitance and mutual inductance.
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 6, "Capacitors and Inductors".
- Agarwal, A. and Lang, J. H., *Foundations of Analog and Digital Electronic Circuits*, chapter 9, "Energy Storage Elements".
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), the lectures introducing capacitors and inductors as energy storage elements.

### [07-02 · First-Order RC and RL Transients](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md)

- **Nilsson & Riedel, *Electric Circuits*:** the chapter on the response of first-order RL and RC circuits (natural, step and sequential-switching responses, plus the op-amp integrator). It has many additional drill problems.
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** the "First-Order Circuits" chapter, which includes singularity functions and PSpice examples.
- **Agarwal & Lang, *Foundations of Analog and Digital Electronic Circuits*:** the first-order transients chapter, the MIT 6.002 text, which frames everything around digital gate delay and is especially good on the energy argument.
- **MIT OpenCourseWare 6.002 *Circuits and Electronics*:** the lectures on first-order transients and energy/power in digital circuits.
- **Weste & Harris, *CMOS VLSI Design*:** for where this chapter goes next in chips. The RC delay model and the dynamic-power chapter build directly on §3.7–3.8.

### [07-03 · Second-Order RLC Transients](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md)

- **Nilsson & Riedel, *Electric Circuits*:** the chapter on natural and step responses of RLC circuits (parallel and series RLC, the three cases, initial conditions), with many drill problems.
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** the "Second-Order Circuits" chapter, including general second-order circuits, duality and op-amp second-order circuits.
- **Agarwal & Lang, *Foundations of Analog and Digital Electronic Circuits*:** the second-order transients chapter (the MIT 6.002 text), which motivates RLC behavior through digital-circuit parasitics.
- **MIT OpenCourseWare 6.002 *Circuits and Electronics*:** the lectures on second-order systems and their energy picture.

### [07-04 · Laplace-Domain Circuit Analysis](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md)

- **Nilsson & Riedel, *Electric Circuits*:** the two chapters on the Laplace transform and its application in circuit analysis (s-domain models, transfer functions, the impulse in circuits).
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Applications of the Laplace Transform" (circuit element models, network stability and synthesis).
- **MIT OpenCourseWare 6.003 *Signals and Systems*:** the lectures on the Laplace transform, poles and zeros.

### [07-05 · Sinusoidal Steady State, Phasors and Impedance](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md)

- **Nilsson & Riedel, *Electric Circuits*:** the chapter on sinusoidal steady-state analysis (phasors, impedance, phasor diagrams, the circuit techniques in the phasor domain).
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Sinusoids and Phasors" (including AC bridges) and "Sinusoidal Steady-State Analysis".
- **MIT OpenCourseWare 6.002 *Circuits and Electronics*:** the lectures on sinusoidal steady state and impedance.

### [07-06 · AC Power and Power Factor](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md)

- **Nilsson & Riedel, *Electric Circuits*:** "Sinusoidal Steady-State Power Calculations" (average and reactive power, complex power, maximum power transfer).
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "AC Power Analysis" (including power-factor correction and power measurement).
- **onsemi, *Power Factor Correction (PFC) Handbook* (HBD853/D):** a practical introduction to why and how power supplies correct power factor.

### [07-07 · Frequency Response and Bode Plots](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md)

- **Nilsson & Riedel, *Electric Circuits*:** "Introduction to Frequency Selective Circuits" and the appendix on Bode diagrams.
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Frequency Response" (transfer functions, the decibel scale, Bode plots, resonance).
- **MIT OpenCourseWare 6.002 *Circuits and Electronics*:** the lectures on frequency response and filters.
- **H. W. Bode, *Network Analysis and Feedback Amplifier Design* (1945):** the source, for the mathematically inclined (§9).

### [07-08 · Filters and Resonance](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md)

- **Nilsson & Riedel, *Electric Circuits*:** "Introduction to Frequency Selective Circuits" and "Active Filter Circuits" (including Butterworth filters and scaling).
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Frequency Response" (series and parallel resonance, passive and active filters, scaling).
- **MIT OpenCourseWare 6.002 *Circuits and Electronics*:** lectures on resonance and filters.

### [07-09 · Mutual Inductance and Transformers](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md)

- **Nilsson & Riedel, *Electric Circuits*:** the sections on the linear and ideal transformer in "Sinusoidal Steady-State Analysis".
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Magnetically Coupled Circuits".
- **MIT OpenCourseWare 6.061 *Introduction to Electric Power Systems*:** transformer equivalent circuits and tests.

### [07-10 · Two-Port Networks](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md)

- **Nilsson & Riedel, *Electric Circuits*:** "Two-Port Circuits".
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Two-Port Networks".
- **D. M. Pozar, *Microwave Engineering*:** the chapter on microwave network analysis (S-parameters, ABCD, conversions).

### [07-11 · Three-Phase Circuits](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md)

- **Nilsson & Riedel, *Electric Circuits*:** "Balanced Three-Phase Circuits".
- **Alexander & Sadiku, *Fundamentals of Electric Circuits*:** "Three-Phase Circuits" (including power measurement and residential wiring).
- **MIT OpenCourseWare 6.061 *Introduction to Electric Power Systems*:** the lectures on three-phase systems.

## [08 · Digital Logic Design](../courses/08-digital-logic-design/README.md)

### [08-01 · Number Systems and Codes](../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** ch. 1 (number systems, two's complement) and ch. 5 (number representations, fixed and floating point).
- **Mano & Ciletti, *Digital Design*:** ch. 1 (number systems, complements, codes, error detection).
- **MIT OCW 6.004 *Computation Structures*:** the opening lectures on information, encoding and binary representation.
- **S. Lin and D. J. Costello, *Error Control Coding*:** the chapters on linear block codes and cyclic codes, for the full theory of Hamming codes and CRCs.

### [08-02 · Boolean Algebra and Logic Gates](../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §§1.5–1.7 (logic gates, beneath the digital abstraction, CMOS transistors) and §§2.1–2.5 (Boolean equations, Boolean algebra, from logic to gates).
- **Mano & Ciletti, *Digital Design*:** ch. 2 (Boolean algebra and logic gates).
- **Weste & Harris, *CMOS VLSI Design*:** ch. 1 (MOS transistors as switches, CMOS logic, compound gates).
- **MIT OCW 6.004 *Computation Structures*:** the lectures on the digital abstraction, CMOS technology and combinational logic.
- **C. E. Shannon, "A Symbolic Analysis of Relay and Switching Circuits" (1938):** the master's thesis that founded switching theory; short and readable.

### [08-03 · Logic Minimization: K-Maps and Beyond](../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §§2.7–2.8 (Karnaugh maps, don't cares, combinational building blocks).
- **Mano & Ciletti, *Digital Design*:** ch. 3 (gate-level minimization, the map method, don't-care conditions, NAND and NOR implementation).
- **G. De Micheli, *Synthesis and Optimization of Digital Circuits*:** the chapters on two-level and multi-level combinational optimization, for the algorithms behind Espresso and multi-level synthesis.
- **R. K. Brayton et al., *Logic Minimization Algorithms for VLSI Synthesis* (1984):** the Espresso book.
- **MIT OCW 6.004 *Computation Structures*:** the lectures on combinational logic synthesis.

### [08-04 · Combinational Building Blocks](../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §2.8 (combinational building blocks), §2.9 (timing, glitches) and §5.2 (arithmetic circuits).
- **Mano & Ciletti, *Digital Design*:** ch. 4 (combinational logic: adders, subtractors, comparators, decoders, encoders, multiplexers).
- **Weste & Harris, *CMOS VLSI Design*:** the datapath chapter, for how these blocks are built and sized in real chips.
- **MIT OCW 6.004 *Computation Structures*:** the lectures on combinational building blocks and timing.

### [08-05 · Introduction to Verilog/SystemVerilog and Testbenches](../courses/08-digital-logic-design/chapters/08-05-verilog-and-testbenches.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** ch. 4 (hardware description languages), with SystemVerilog and VHDL side by side.
- **S. Sutherland, S. Davidmann and P. Flake, *SystemVerilog for Design*:** the design subset of SystemVerilog.
- **C. E. Cummings, "Nonblocking Assignments in Verilog Synthesis, Coding Styles That Kill!" (SNUG 2000):** the classic paper on the coding rules of §3.6.
- **IEEE Std 1800-2023:** the language reference itself, free through the IEEE GET program; chapter 4 defines the scheduling semantics.
- **MIT OCW 6.111 *Introductory Digital Systems Laboratory*:** lectures and labs on Verilog for FPGAs.

### [08-06 · Latches, Flip-Flops and Sequential Timing](../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §§3.1–3.3 (latches and flip-flops, synchronous logic design) and §3.5 (timing of sequential logic).
- **Mano & Ciletti, *Digital Design*:** ch. 5 (synchronous sequential logic: latches, flip-flops, analysis).
- **Weste & Harris, *CMOS VLSI Design*:** the sequential-circuits chapter (latch and flip-flop circuits, sequencing overhead, time borrowing).
- **MIT OCW 6.004 *Computation Structures*:** the lectures on sequential logic and timing.

### [08-07 · Registers, Counters and Shift Registers](../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md)

- **Mano & Ciletti, *Digital Design*:** ch. 6 (registers and counters).
- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §5.4 (sequential building blocks: counters, shift registers).
- **S. W. Golomb, *Shift Register Sequences*:** the classic treatment of m-sequences and their properties.
- **P. Alfke, Xilinx XAPP052, "Efficient Shift Registers, LFSR Counters, and Long Pseudo-Random Sequence Generators" (1996):** practical LFSR design and the tap table.

### [08-08 · Finite State Machines](../courses/08-digital-logic-design/chapters/08-08-finite-state-machines.md)

- **Mano & Ciletti, *Digital Design*:** ch. 5 (synchronous sequential logic: analysis, state reduction and assignment, design procedure).
- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §3.4 (finite state machines) and §4.6 (FSMs in HDL).
- **Kohavi & Jha, *Switching and Finite Automata Theory* (3rd ed.):** state equivalence and minimization in depth.
- **Hopcroft, Motwani & Ullman, *Introduction to Automata Theory, Languages, and Computation*:** the Myhill–Nerode theorem and DFA minimization.

### [08-09 · Arithmetic Circuits](../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §5.2 (arithmetic circuits: adders, shifters, multipliers, fixed point).
- **Weste & Harris, *CMOS VLSI Design* (4th ed.):** ch. 11 (datapath subsystems: adders including prefix networks, multipliers, shifters).
- **B. Parhami, *Computer Arithmetic: Algorithms and Hardware Designs*:** carry-lookahead and prefix adders, tree multipliers, Booth recoding in depth.
- **M. Horowitz, "Computing's energy problem (and what we can do about it)", ISSCC 2014:** the energy of operations and data movement.

### [08-10 · Timing, Metastability and Clock-Domain Crossing](../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §3.5 (timing of sequential logic: skew, metastability, synchronizers, resolution time).
- **Dally & Harting, *Digital Design: A Systems Approach*:** the chapters on timing, synchronization and asynchronous FIFOs.
- **R. Ginosar, "Metastability and Synchronizers: A Tutorial", *IEEE Design & Test*, 2011:** a readable account of synchronizer failure and design.
- **C. E. Cummings, "Simulation and Synthesis Techniques for Asynchronous FIFO Design" (SNUG 2002):** the widely used Gray-pointer FIFO design.

### [08-11 · Memories and Programmable Logic](../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md)

- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** §5.5 (memory arrays, register files, ROM as logic) and §5.6 (PLAs and FPGAs).
- **Mano & Ciletti, *Digital Design*:** ch. 7 (memory and programmable logic).
- **Weste & Harris, *CMOS VLSI Design*:** ch. 12 (array subsystems: SRAM, DRAM, ROM, register files).
- **Lattice, iCE40 UltraPlus Family Data Sheet (FPGA-DS-02008):** a compact, readable description of a real FPGA's logic cells, memories and DSP blocks.

### [08-12 · FPGA Implementation Flow](../courses/08-digital-logic-design/chapters/08-12-fpga-implementation-flow.md)

- **Yosys manual** (YosysHQ documentation): the `synth_ice40` script and the FSM, memory and technology-mapping passes.
- **nextpnr and Project IceStorm documentation** (YosysHQ repositories): the iCE40 architecture as seen by the tools.
- **Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition):** the FPGA material of §5.6 and the HDL chapter, applied to a board.
- **Lattice, iCE40 UltraPlus Family Data Sheet (FPGA-DS-02008):** configuration modes and timing.

## [09 · Semiconductor Devices](../courses/09-semiconductor-devices/README.md)

### [09-01 · Crystals, Energy Bands and the Semiconductor](../courses/09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 1 (free online from the author's site): bands, effective mass and carrier concentrations at an engineering level.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 1 (crystal properties and Miller indices) and ch. 3 (energy bands, effective mass).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 1–2; and Pierret, *Advanced Semiconductor Fundamentals*, for the Kronig–Penney model and band structures in depth.
- MIT OpenCourseWare 6.012 *Microelectronic Devices and Circuits* and 6.720J *Integrated Microelectronic Devices*: opening lectures on semiconductor physics.

### [09-02 · Carriers, Doping and the Fermi Level](../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 1 (§1.5–1.11): density of states, Fermi function, carrier concentrations and doping, written for device engineers (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 2: carrier modeling, with the clearest treatment of the temperature dependence and of degeneracy.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 3 (§3.3): carrier concentrations, compensation and temperature dependence.
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, ch. 1: Fermi–Dirac integrals, band-gap narrowing and dopant data for reference.

### [09-03 · Carrier Transport: Drift and Diffusion](../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 2 (§2.1–2.5): drift, mobility, velocity saturation, diffusion and the Einstein relation, with measured mobility curves (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 3: carrier action, with a careful treatment of signs and of the four-point probe.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 3–4: drift, diffusion, the Hall effect and built-in fields.
- M. Lundstrom, *Fundamentals of Carrier Transport*: the step from drift–diffusion to ballistic transport, for the curious.

### [09-04 · Generation, Recombination and the Continuity Equation](../courses/09-semiconductor-devices/chapters/09-04-generation-recombination-continuity.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 2 (§2.6–2.9): recombination, generation, quasi-Fermi levels and the continuity equation (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 3 (§3.3–3.4): recombination–generation and the minority-carrier diffusion equation, with many worked solutions.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 4: excess carriers, photoconductivity and diffusion lengths.
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, ch. 1 (§1.5): the Shockley–Read–Hall derivation in full.

### [09-05 · PN Junction Electrostatics](../courses/09-semiconductor-devices/chapters/09-05-pn-junction-electrostatics.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 4 (§4.1–4.4): building blocks, the depletion-layer model, reverse bias and C–V (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 5: PN junction electrostatics, with the clearest step-by-step Poisson solutions and the graded junction.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 5 (§5.2): equilibrium conditions and the space-charge region.
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, ch. 2: depletion region beyond the depletion approximation, with the Debye-length corrections.

### [09-06 · PN Junction I–V, Capacitance and Breakdown](../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 4 (§4.5–4.11 and §4.16–4.21): breakdown, carrier injection, the diode equation, charge storage, the small-signal model, Schottky diodes and ohmic contacts (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 6–8 and 14: the ideal diode, deviations from ideal, small-signal admittance (including the exact long-diode result) and transient response, and metal–semiconductor contacts.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 5 (§5.3–5.7): forward- and reverse-biased junctions, breakdown, transient and AC conditions, metal–semiconductor junctions.
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, ch. 2–3: junction breakdown with ionization integrals, and metal–semiconductor contacts in depth.

### [09-07 · The Bipolar Junction Transistor](../courses/09-semiconductor-devices/chapters/09-07-bipolar-junction-transistor.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 8: collector and base currents, Gummel numbers, band-gap narrowing and SiGe, the Early effect, Ebers–Moll, transit time and the Kirk effect, small-signal model, f_T, charge control (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 10–12: BJT fundamentals, static characteristics (with the general solution including base recombination), and dynamic response.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 7: bipolar junction transistors, including the charge-control approach and HBTs.
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, ch. 5: bipolar transistors, heterojunction devices and high-frequency figures of merit.

### [09-08 · The MOS Capacitor](../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 5 (the MOS capacitor, C–V, oxide charge, poly depletion, inversion-layer thickness, CCD and CMOS imagers) and §7.4 (gate leakage, high-k, metal gate) (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 16 (MOS fundamentals, including the exact charge solution) and ch. 18 (nonideal MOS: oxide charges, interface traps).
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 6 (§6.4–6.5: the MOS capacitor and C–V analysis).
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, ch. 4: the MIS capacitor in depth, including interface-trap measurement.

### [09-09 · The Long-Channel MOSFET](../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, ch. 6 (§6.3 surface mobility, §6.4 body effect, §6.5–6.6 the basic I–V model, §6.13–6.14 output conductance and high-frequency performance) and §7.2 (subthreshold current) (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 17: MOSFET static characteristics, including the square-law and bulk-charge theories derived side by side.
- B. G. Streetman and S. K. Banerjee, *Solid State Electronic Devices*, ch. 6 (§6.5): the MOS field-effect transistor.
- Y. Tsividis and C. McAndrew, *Operation and Modeling of the MOS Transistor*: the standard graduate text on charge-sheet models and the weak-to-strong-inversion transition.

### [09-10 · Short-Channel Effects and Leakage](../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, §6.8–6.12 (velocity saturation, series resistance, overshoot and the injection limit) and ch. 7 (subthreshold current, V_TH roll-off and DIBL, reducing EOT and W_dep, shallow junctions, the I_on–I_off trade-off, thin-body and multigate devices) (free from the author's site).
- Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, ch. 3–4: the standard senior/graduate treatment of short-channel MOSFETs, scale length and leakage.
- R. F. Pierret, *Semiconductor Device Fundamentals*, ch. 19: MOSFETs in ICs, small-dimension effects.
- M. Lundstrom, "Elementary scattering theory of the Si MOSFET", *IEEE Electron Device Letters* (1997), and his later notes on nanoscale transistors: the backscattering view behind the injection limit (named for further reading, not used for numbers here).

### [09-11 · CMOS and Scaling: Moore, Dennard and Beyond](../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, §6.7 (CMOS inverter, delay, power) and §7.1 (technology scaling, Table 7–1) (free from the author's site).
- J. M. Rabaey, A. Chandrakasan and B. Nikolić, *Digital Integrated Circuits: A Design Perspective*, ch. 3 (devices, scaling) and ch. 5 (the CMOS inverter: transfer curve, noise margins, delay, power).
- G. E. Moore, "Cramming more components onto integrated circuits" (1965) and "Progress in digital integrated electronics" (1975): both short and readable.
- R. H. Dennard et al., "Design of ion-implanted MOSFET's with very small physical dimensions" (1974): the original scaling paper.

### [09-12 · Advanced Transistors: FinFET, GAA, CFET and Backside Power](../courses/09-semiconductor-devices/chapters/09-12-finfet-gaa-cfet-backside-power.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, §7.8 (ultra-thin-body SOI, FinFET and nanowire FET) (free from the author's site).
- Y. Taur and T. H. Ning, *Fundamentals of Modern VLSI Devices*, the sections on the scale length of double-gate MOSFETs and SOI devices.
- IEEE IRDS, *More Moore* (2024), §3–4: the device and interconnect roadmap, performance boosters, and the GAA-to-CFET transition.

### [09-13 · Compound and Wide-Bandgap Semiconductors](../courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md)

- B. J. Baliga, *Fundamentals of Power Semiconductor Devices*, ch. 1–3: breakdown, drift layers and the figure of merit.
- T. Kimoto and J. A. Cooper, *Fundamentals of Silicon Carbide Technology*: SiC materials, devices and processing.
- J. Burin et al., "TCAD Parameters for 4H-SiC: A Review" (arXiv, 2025): a critical survey of SiC material parameters, including how much they disagree.
- I. Vurgaftman, J. R. Meyer and L. R. Ram-Mohan, "Band parameters for III–V compound semiconductors and their alloys" (2001): the standard compilation, including the nitrides.

### [09-14 · Optoelectronic Devices](../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md)

- C. Hu, *Modern Semiconductor Devices for Integrated Circuits*, §4.12–4.15 (solar cells, LEDs and solid-state lighting, diode lasers, photodiodes) (free from the author's site).
- R. F. Pierret, *Semiconductor Device Fundamentals*, the chapter on optoelectronic diodes.
- U.S. Department of Energy, *Solid-State Lighting R&D Opportunities* (2022): efficiency limits and loss breakdowns for LEDs.

## [10 · Electronics I (Microelectronic Circuits)](../courses/10-electronics-1/README.md)

### [10-01 · Diodes and Diode Circuits](../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 4 (diodes: models, small-signal operation, Zener diodes, rectifiers, limiting and clamping).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 3 (diode models and circuits).
- MIT OpenCourseWare, 6.012 *Microelectronic Devices and Circuits* (Fall 2009), lecture notes on the PN diode and its circuit models.
- The data sheets cited below: reading the absolute-maximum and electrical-characteristics tables of a few real diodes is the fastest way to calibrate the numbers in this chapter.

### [10-02 · MOSFET DC Operation and Biasing](../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 5 (MOSFETs: device structure and physical operation, current–voltage characteristics, DC circuits, biasing).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 6 (physics of MOS transistors) and the biasing sections of ch. 7.
- MIT OpenCourseWare, 6.002 *Circuits and Electronics* (Spring 2007, A. Agarwal), video lectures on the MOSFET switch, the MOSFET amplifier and large-signal analysis.
- Data sheets [1]–[3]: read the electrical-characteristics table of a small-signal MOSFET and a power MOSFET side by side.

### [10-03 · BJT DC Operation and Biasing](../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 6 (BJTs: device operation, current–voltage characteristics, DC circuits, biasing, the BJT as a switch).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 4 (physics of bipolar transistors) and ch. 5 (bipolar amplifiers: biasing).
- MIT OpenCourseWare, 6.012 *Microelectronic Devices and Circuits* (Fall 2009), lecture notes on the bipolar junction transistor and its large-signal models.
- The 2N3904 and 2N3906 data sheets [1, 2]: read the β and saturation tables with this chapter's Examples 1 and 6.

### [10-04 · Small-Signal Models](../courses/10-electronics-1/chapters/10-04-small-signal-models.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 7 (small-signal operation and models; the hybrid-π and T models).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 5 and 7 (bipolar and MOS small-signal models).
- P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Circuits Using Pre-Computed Lookup Tables* (Cambridge University Press, 2017): the $g_m/I_D$ methodology.
- MIT OpenCourseWare, 6.002 *Circuits and Electronics* (Spring 2007, A. Agarwal), video lectures on small-signal models and the incremental analysis of amplifiers.

### [10-05 · Amplifier Fundamentals](../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 1 (amplifiers, the four models, frequency response).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 1 (amplifier basics and loading).
- The TPA3116D2 data sheet [1], sections 6 and 7.3: a real amplifier's gain, input impedance and efficiency specifications.

### [10-06 · MOS Single-Stage Amplifiers](../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 7 (MOS amplifier configurations).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 7 (CMOS amplifiers).
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, ch. 3 (single-stage amplifiers with body effect and cascodes).

### [10-07 · BJT Single-Stage Amplifiers](../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 7 (BJT amplifier configurations and the MOS–BJT comparison).
- B. Razavi, *Fundamentals of Microelectronics*, ch. 5 (bipolar amplifiers, with the impedance-reflection viewpoint used here).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 3 (single-transistor and two-transistor amplifiers, bipolar and MOS side by side).

### [10-08 · Current Sources and Current Mirrors](../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 8 (current sources, mirrors, cascode and Wilson mirrors).
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, ch. 5 (current mirrors, cascodes and low-voltage cascodes).
- M. J. M. Pelgrom, A. C. J. Duinmaijer and A. P. G. Welbers, "Matching properties of MOS transistors" [1].
- MIT OpenCourseWare, 6.012 *Microelectronic Devices and Circuits* (Fall 2009), lecture notes on current sources and mirrors.

### [10-09 · Real Op-Amps: Non-Idealities](../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 2 (op-amp non-idealities: finite gain, bandwidth, slew rate, DC errors).
- S. Franco, *Design with Operational Amplifiers and Analog Integrated Circuits*, ch. 5–6 (static and dynamic limitations, with data-sheet examples).
- Any of the data sheets [1–3], sections 6 (specifications) and 7–8 (application notes): reading one end to end is the best exercise in this chapter.

### [10-10 · Op-Amp Application Circuits](../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, ch. 2 (instrumentation amplifier, integrator) and ch. 18 (precision rectifiers, Schmitt triggers).
- S. Franco, *Design with Operational Amplifiers and Analog Integrated Circuits*, ch. 2 (instrumentation amplifiers), ch. 9 (comparators and Schmitt triggers).
- The INA333 [1] and TLV3201 [2] data sheets, application sections.
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), the closing operational-amplifier lectures: op-amp circuits (integrators, differentiators) and op-amps with positive feedback (comparators with hysteresis and oscillators).

## [11 · Signals and Systems](../courses/11-signals-and-systems/README.md)

### [11-01 · Signals: Classification and Operations](../courses/11-signals-and-systems/chapters/11-01-signals-classification-and-operations.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 1.1–1.4 (signals, transformations of the independent variable, exponentials and sinusoids, the unit impulse and step).
- B. P. Lathi, *Linear Systems and Signals*, ch. 1.1–1.4 (size of a signal, signal operations and classification, useful signal models).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the opening lectures on signals and their representations.
- The ADS1292R data sheet's noise tables [1]: a compact, real example of how sampling rate, gain and noise determine the useful resolution of a digital signal.

### [11-02 · Systems and Their Properties](../courses/11-signals-and-systems/chapters/11-02-system-properties.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 1.5–1.6 (interconnections of systems and the basic system properties).
- B. P. Lathi, *Linear Systems and Signals*, ch. 1.6–1.7 (classification of systems, including incrementally linear systems).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the early lectures on systems and their representations.
- The OPA333 data sheet's description of internal offset correction [4] and the ADS1292R's digital-filter section [3]: real examples of time-varying internals and filter latency.

### [11-03 · Convolution](../courses/11-signals-and-systems/chapters/11-03-convolution.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 2.1–2.3 (the convolution sum and integral, and the properties of LTI systems).
- B. P. Lathi, *Linear Systems and Signals*, ch. 2.4 (the convolution integral, with graphical convolution) and ch. 3.8 (the convolution sum).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on convolution.
- N. P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit" [2]: a readable account of how convolution and matrix arithmetic are mapped onto a MAC array, and why memory limits it.

### [11-04 · LTI Systems and Differential/Difference Equations](../courses/11-signals-and-systems/chapters/11-04-lti-systems-and-differential-equations.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 2.3–2.4 (properties of LTI systems; differential and difference equations; block diagrams) and ch. 3.2 (complex exponentials as eigenfunctions).
- B. P. Lathi, *Linear Systems and Signals*, ch. 2 (time-domain analysis of CT systems) and ch. 3 (DT systems and difference equations).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on difference equations, block diagrams and feedback.
- The CMSIS-DSP biquad documentation [2]: a concise, real specification of filter structures and their conventions.

### [11-05 · Fourier Series](../courses/11-signals-and-systems/chapters/11-05-fourier-series.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 3.2–3.5 (the CT Fourier series, convergence, properties) and 3.8–3.9 (filtering periodic signals).
- B. P. Lathi, *Linear Systems and Signals*, ch. 6 (continuous-time signal analysis: the Fourier series).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on Fourier series.
- The TPA3116D2 data sheet's sections on output filtering, ferrite beads and AM avoidance [1]: a real design discussion built entirely on harmonic placement.

### [11-06 · The Continuous-Time Fourier Transform](../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 4 (the continuous-time Fourier transform) and ch. 6.1–6.2 (magnitude and phase, group delay).
- B. P. Lathi, *Linear Systems and Signals*, ch. 7 (continuous-time signal analysis: the Fourier transform).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on the Fourier transform.
- R. N. Bracewell, *The Fourier Transform and Its Applications*: the classic reference for transform pairs, pictures of them, and their physical meaning.

### [11-07 · The Discrete-Time Fourier Transform](../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 5 (the DTFT) and ch. 6.4–6.6 (DT frequency response, first- and second-order systems).
- B. P. Lathi, *Linear Systems and Signals*, ch. 9 (DT signal analysis: the DTFT).
- A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, the chapters on filter design by windowing and on the DFT: the standard next step (Course 16).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on DT frequency response and the DTFT.

### [11-08 · The Laplace Transform and System Functions](../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 9 (the Laplace transform, the ROC, geometric evaluation, system functions).
- B. P. Lathi, *Linear Systems and Signals*, ch. 4 (the Laplace transform and frequency response from poles and zeros).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on Laplace transforms and frequency response.
- For equalization in context: the IEEE 802.3ck task force's public COM tool and presentations [1].

### [11-09 · The z-Transform](../courses/11-signals-and-systems/chapters/11-09-z-transform.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 10 (the z-transform) and §10.8 (the unilateral transform).
- B. P. Lathi, *Linear Systems and Signals*, ch. 5 (the z-transform and DT system analysis).
- A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, the chapters on filter structures (coefficient quantization) and on IIR design by the bilinear transform: the next step (Course 16).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on the z-transform.

### [11-10 · Sampling, Aliasing and Reconstruction](../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 7 (sampling).
- B. P. Lathi, *Linear Systems and Signals*, ch. 8 (sampling: the bridge from continuous to discrete).
- A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, the chapter on sampling of CT signals (DT processing of CT signals, changing the sampling rate, oversampling and noise shaping).
- MIT OpenCourseWare, 6.003 *Signals and Systems* (Fall 2011), the lectures on sampling and quantization.

### [11-11 · Modulation and Filtering Applications](../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md)

- A. V. Oppenheim and A. S. Willsky with S. H. Nawab, *Signals and Systems*, 2nd ed., ch. 8 (communication systems) and §6.4–6.5 (filters).
- B. P. Lathi, *Linear Systems and Signals*, ch. 7 (frequency-domain analysis: filtering and modulation).
- B. P. Lathi and Z. Ding, *Modern Digital and Analog Communication Systems*, the chapters on amplitude modulation and on channel capacity: the next step (Course 17).
- C. E. Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, 1948: the origin of the capacity formula.

## [12 · Electronics II](../courses/12-electronics-2/README.md)

### [12-01 · Differential Pairs](../courses/12-electronics-2/chapters/12-01-differential-pairs.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the chapter on differential and multistage amplifiers.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, ch. 4 (differential amplifiers) and the chapter on nonidealities (offset).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 3 (single-transistor and multiple-transistor amplifiers: the differential pair and offset).
- M. J. M. Pelgrom, A. C. J. Duinmaijer and A. P. G. Welbers, "Matching properties of MOS transistors," *IEEE JSSC*, 1989 [3].

### [12-02 · Active Loads, Cascodes and Multistage Amplifiers](../courses/12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the chapters on building blocks of integrated-circuit amplifiers and on differential and multistage amplifiers.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, ch. 3 (cascode stages) and ch. 5 (current mirrors and active loads), and the chapter on operational amplifiers (telescopic and two-stage designs).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 3 and 4 (multiple-transistor amplifiers and current mirrors).
- P. E. Allen and D. R. Holberg, *CMOS Analog Circuit Design*, the two-stage op-amp design procedure and its systematic-offset condition.

### [12-03 · Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros](../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the frequency-response chapter (device capacitances, the Miller theorem, CS, CG, CD and cascode high-frequency response).
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, ch. 6 (frequency response of amplifiers).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 7 (frequency response).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, the chapter on bandwidth estimation, for a practitioner's view of time-constant methods.

### [12-04 · High-Frequency Analysis Methods](../courses/12-electronics-2/chapters/12-04-high-frequency-analysis-methods.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the frequency-response chapter (open-circuit and short-circuit time constants).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 7 (zero-value time constants) and ch. 9 (frequency compensation and pole splitting).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, the chapter on bandwidth estimation (open-circuit time constants and their extensions).

### [12-05 · Feedback: Theory and the Four Topologies](../courses/12-electronics-2/chapters/12-05-feedback-topologies.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the feedback chapter.
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 8 (feedback, return ratio and Blackman's formula).
- S. Rosenstark, *Feedback Amplifier Principles* (Macmillan, 1986), for the asymptotic-gain formula.

### [12-06 · Stability and Frequency Compensation](../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md)

- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 9 (frequency response and stability of feedback amplifiers, Miller compensation, nulling resistor).
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, the stability and frequency compensation chapter.
- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the stability sections of the feedback chapter.

### [12-07 · Output Stages and Power Amplifiers](../courses/12-electronics-2/chapters/12-07-output-stages.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the output stages and power amplifiers chapter.
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 5 (output stages).
- D. Self, *Audio Power Amplifier Design* (6th ed., Focal Press, 2013), for crossover distortion and thermal compensation in practice.

### [12-08 · Op-Amp Internals](../courses/12-electronics-2/chapters/12-08-op-amp-internals.md)

- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 6 (amplifiers with active loads, the folded cascode) and ch. 12 (fully differential op-amps and CMFB).
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, the operational amplifier chapter.
- D. A. Johns and K. Martin, *Analog Integrated Circuit Design*, the basic and advanced op-amp chapters.

### [12-09 · Oscillators](../courses/12-electronics-2/chapters/12-09-oscillators.md)

- A. S. Sedra and K. C. Smith, *Microelectronic Circuits*, the signal generators and waveform-shaping chapter.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, the oscillators chapter (ring and LC oscillators, VCOs).
- E. A. Vittoz, "Low-power crystal and MEMS oscillators" (Springer, 2010), for crystal oscillator design in depth.

### [12-10 · Noise in Circuits](../courses/12-electronics-2/chapters/12-10-noise-in-circuits.md)

- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, ch. 11 (noise in integrated circuits).
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, the noise chapter.
- H. W. Ott, *Electromagnetic Compatibility Engineering* (Wiley, 2009), the intrinsic noise sources chapter, for a practical view.

## [13 · Electromagnetics](../courses/13-electromagnetics/README.md)

### [13-01 · Vector Calculus Refresher](../courses/13-electromagnetics/chapters/13-01-vector-calculus-refresher.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 3 (vector analysis).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 2.
- D. J. Griffiths, *Introduction to Electrodynamics*, ch. 1 and appendix A (curvilinear coordinates, the Helmholtz theorem).
- MIT OpenCourseWare 6.013 *Electromagnetics and Applications*.

### [13-02 · Electrostatics: Boundary Conditions and Boundary-Value Problems](../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 4 (electrostatics, boundary conditions, images, capacitance).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 3–4 (including the solution of electrostatic boundary-value problems).
- D. J. Griffiths, *Introduction to Electrodynamics*, ch. 3 (Laplace's equation, uniqueness, images, separation of variables).
- MIT OpenCourseWare 6.013 *Electromagnetics and Applications*, the electrostatics lectures.

### [13-03 · Magnetostatics and Inductance](../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 5 (magnetostatics, inductance, magnetic materials).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 6 (including magnetic circuits).
- D. J. Griffiths, *Introduction to Electrodynamics*, ch. 5–6 (vector potential, magnetization).
- C. R. Paul, *Inductance: Loop and Partial*, Wiley, 2010 (partial inductance in practice).

### [13-04 · Maxwell's Equations and Time-Varying Fields](../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 6 (Maxwell's equations for time-varying fields).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 7 (time-varying fields, Poynting theorem).
- D. J. Griffiths, *Introduction to Electrodynamics*, ch. 7–8 (electrodynamics, conservation laws).
- MIT OpenCourseWare 6.013, *Electromagnetics and Applications* (lecture notes on Maxwell's equations and power).

### [13-05 · Plane Waves in Lossless and Lossy Media](../courses/13-electromagnetics/chapters/13-05-plane-waves.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 7 (plane-wave propagation).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 8 (plane electromagnetic waves).
- D. M. Pozar, *Microwave Engineering*, ch. 1 (plane waves, surface resistance).
- MIT OpenCourseWare 6.013, *Electromagnetics and Applications*, lectures on waves in media.

### [13-06 · Reflection and Transmission of Waves](../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 8 (wave reflection and transmission).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 8 (normal and oblique incidence).
- E. Hecht, *Optics*, ch. 4 (Fresnel equations, total internal reflection).
- H. W. Ott, *Electromagnetic Compatibility Engineering*, ch. 6 (shielding and apertures).

### [13-07 · Transmission Lines: Time Domain](../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2 (transmission lines, including transients).
- H. Johnson and M. Graham, *High-Speed Digital Design: A Handbook of Black Magic*, ch. 4 (transmission lines and terminations).
- E. Bogatin, *Signal and Power Integrity — Simplified*, chapters on reflections and TDR.
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 9.

### [13-08 · Transmission Lines: Sinusoidal Steady State](../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2.
- D. M. Pozar, *Microwave Engineering*, ch. 2 (transmission-line theory) and ch. 5 (quarter-wave transformers).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 9.

### [13-09 · The Smith Chart and Impedance Matching](../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md)

- D. M. Pozar, *Microwave Engineering*, ch. 2 (Smith chart) and ch. 5 (impedance matching, Bode–Fano).
- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2.
- R. M. Fano, "Theoretical limitations on the broadband matching of arbitrary impedances," *Journal of the Franklin Institute* 249 (1950) (the original limit).

### [13-10 · Waveguides and Resonators](../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md)

- D. M. Pozar, *Microwave Engineering*, ch. 3 (waveguides) and ch. 6 (resonators).
- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 8 (waveguides and cavities).
- B. E. A. Saleh and M. C. Teich, *Fundamentals of Photonics*, 2nd ed. (Wiley, 2007), ch. 9 (fiber optics; ch. 10 in the 3rd ed.).
- MIT OpenCourseWare 6.013, *Electromagnetics and Applications*: the lecture notes and videos on waveguides and resonators.
- D. Marcuse, "Loss analysis of single-mode fiber splices," *Bell System Technical Journal* 56 (1977) (the Gaussian MFD formula).

### [13-11 · Radiation and Antenna Fundamentals](../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md)

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 9 (radiation, antennas and arrays).
- MIT OpenCourseWare 6.013, *Electromagnetics and Applications*: the lecture notes and videos on radiation, antennas and arrays.
- C. A. Balanis, *Antenna Theory: Analysis and Design*, ch. 2 (parameters), 4 (wire antennas) and 6 (arrays).
- J. D. Kraus and R. J. Marhefka, *Antennas*, ch. 2–5.

## [14 · Computer Organization and Architecture](../courses/14-computer-organization-and-architecture/README.md)

### [14-01 · Performance, Power and the Iron Law](../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design* (RISC-V Edition), ch. 1 (performance, power wall, Amdahl's law, fallacies and pitfalls).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 1 (quantitative principles, power and energy, measuring and summarizing performance).
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on performance and power.
- J. L. Gustafson, "Reevaluating Amdahl's law", *Communications of the ACM* 31(5), 1988.

### [14-02 · Instruction Set Architecture: RISC-V, Arm and x86](../courses/14-computer-organization-and-architecture/chapters/14-02-isa-risc-v-arm-x86.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 2 (instructions: language of the computer).
- S. L. Harris and D. M. Harris, *Digital Design and Computer Architecture*, RISC-V Edition, ch. 6 (architecture).
- The RISC-V Instruction Set Manual, Volume I: Unprivileged Architecture (RISC-V International), chapters on RV32I and the compressed extension.
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on the RISC-V ISA and assembly.
- D. Patterson and A. Waterman, *The RISC-V Reader: An Open Architecture Atlas* (Strawberry Canyon, 2017).

### [14-03 · Assembly and the Compilation Stack](../courses/14-computer-organization-and-architecture/chapters/14-03-assembly-and-the-compilation-stack.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §§2.7–2.13 (decisions, procedures, compiling, linking and loading).
- S. L. Harris and D. M. Harris, *Digital Design and Computer Architecture*, RISC-V Edition, §§6.3–6.6.
- R. E. Bryant and D. R. O'Hallaron, *Computer Systems: A Programmer's Perspective*, ch. 3 (machine-level programs, x86-64) and ch. 7 (linking).
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on procedures and the stack.
- The RISC-V ELF psABI specification ([2], [3]), and LLVM's documentation for clang, llvm-mc and LLD.

### [14-04 · Computer Arithmetic and Number Formats](../courses/14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 3 (arithmetic for computers).
- D. Goldberg, "What every computer scientist should know about floating-point arithmetic," *ACM Computing Surveys* 23(1), 1991.
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002, ch. 2–4 (rounding error, summation).
- H. S. Warren, *Hacker's Delight*, 2nd ed., ch. 10 (division by constants).
- The OCP MX and OFP8 specifications ([4] and 08-01's sources), and the RISC-V M and F chapters ([1], [2]).

### [14-05 · Single-Cycle Datapath and Control](../courses/14-computer-organization-and-architecture/chapters/14-05-single-cycle-datapath.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §§4.1–4.4.
- S. L. Harris and D. M. Harris, *Digital Design and Computer Architecture*, RISC-V Edition, §§7.1–7.4 (single-cycle and multicycle processors, with HDL).
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on the single-cycle RISC-V processor.
- The RISC-V Instruction Set Manual, Volume I, chapter on RV32I, for the exact semantics every datapath must implement.

### [14-06 · Pipelining and Hazards](../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §§4.5–4.9.
- S. L. Harris and D. M. Harris, *Digital Design and Computer Architecture*, RISC-V Edition, §7.5 (with HDL).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, appendix C (pipelining basics).
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on pipelined processors.

### [14-07 · Branch Prediction and Speculation](../courses/14-computer-organization-and-architecture/chapters/14-07-branch-prediction-and-speculation.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §4.9 (control hazards and dynamic prediction).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, §3.3 (advanced branch prediction).
- S. McFarling, "Combining Branch Predictors," DEC WRL Technical Note TN-36, 1993 (gshare).
- A. Seznec and P. Michaud, "A case for (partially) TAgged GEometric history length branch prediction," *Journal of Instruction-Level Parallelism*, 2006 (TAGE).
- P. Kocher et al., "Spectre Attacks: Exploiting Speculative Execution," IEEE Symposium on Security and Privacy, 2019; M. Lipp et al., "Meltdown: Reading Kernel Memory from User Space," USENIX Security, 2018.

### [14-08 · Out-of-Order and Superscalar Execution](../courses/14-computer-organization-and-architecture/chapters/14-08-out-of-order-and-superscalar.md)

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 3 (instruction-level parallelism and its exploitation).
- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §4.11 (multiple issue).
- R. M. Tomasulo, "An Efficient Algorithm for Exploiting Multiple Arithmetic Units," *IBM Journal of Research and Development* 11(1), 1967.
- J. E. Smith and A. R. Pleszkun, "Implementing Precise Interrupts in Pipelined Processors," *IEEE Transactions on Computers*, 1988 (the reorder buffer).
- D. W. Wall, "Limits of Instruction-Level Parallelism," DEC WRL Research Report 93/6, 1993.

### [14-09 · Memory Hierarchy and Caches](../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 5 (large and fast: exploiting memory hierarchy).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, App. B (review of memory hierarchy) and ch. 2 (memory hierarchy design).
- R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, "Evaluation Techniques for Storage Hierarchies," *IBM Systems Journal* 9(2), 1970 (stack distances).
- M. D. Hill, "Aspects of Cache Memory and Instruction Buffer Performance," PhD thesis, UC Berkeley, 1987 (the three Cs).
- U. Drepper, "What Every Programmer Should Know About Memory," 2007 (a long practical tour; some numbers are dated).

### [14-10 · Virtual Memory, TLBs and the OS Interface](../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §5.7 (virtual memory) and §4.9 (exceptions).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, App. B.4–B.5 (virtual memory and its protection).
- *The RISC-V Instruction Set Manual, Volume II: Privileged Architecture*, the supervisor chapter (Sv32–Sv57) and the machine chapter (traps).
- A. Silberschatz, P. B. Galvin and G. Gagne, *Operating System Concepts*, the chapters on main memory and virtual memory (paging, replacement, thrashing).
- L. A. Belady, R. A. Nelson and G. S. Shedler, "An Anomaly in Space-Time Characteristics of Certain Programs Running in a Paging Machine," *Communications of the ACM* 12(6), 1969.

### [14-11 · I/O, Buses and Interconnect](../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md)

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, the online chapter on storage and other I/O topics.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, App. D (storage systems) and App. F (interconnection networks).
- W. J. Dally and B. Towles, *Principles and Practices of Interconnection Networks*, Morgan Kaufmann, 2004 (topologies, routing, flow control).
- Arm, *AMBA AXI Protocol Specification* (IHI 0022), the handshake and channel chapters.

### [14-12 · Multicore, Coherence and Memory Consistency](../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md)

- D. J. Sorin, M. D. Hill and D. A. Wood, *A Primer on Memory Consistency and Cache Coherence*, Synthesis Lectures on Computer Architecture (2nd ed., with V. Nagarajan, 2020).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 5 (thread-level parallelism).
- L. Lamport, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs," *IEEE Transactions on Computers* C-28(9), 1979.
- S. V. Adve and K. Gharachorloo, "Shared Memory Consistency Models: A Tutorial," *IEEE Computer* 29(12), 1996.

### [14-13 · GPUs and SIMT](../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md)

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 4 (data-level parallelism in vector, SIMD and GPU architectures).
- D. B. Kirk and W. W. Hwu, *Programming Massively Parallel Processors* (coalescing, shared memory, occupancy).
- NVIDIA, *CUDA C++ Programming Guide* and *CUDA C++ Best Practices Guide* (the programming model, memory hierarchy and performance guidelines).
- E. Lindholm, J. Nickolls, S. Oberman and J. Montrym, "NVIDIA Tesla: A Unified Graphics and Computing Architecture," *IEEE Micro* 28(2), 2008 (the SIMT design).

### [14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision](../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md)

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 7 (domain-specific architectures).
- V. Sze, Y.-H. Chen, T.-J. Yang and J. S. Emer, *Efficient Processing of Deep Neural Networks*, Morgan & Claypool, 2020 (dataflows, reuse, energy).
- H. T. Kung, "Why Systolic Architectures?", *IEEE Computer* 15(1), 1982.
- N. P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit," ISCA 2017, and "TPU v4," ISCA 2023.

### [14-15 · The Roofline Model, Benchmarks and How They Are Gamed](../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md)

- S. Williams, A. Waterman and D. Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures," *Communications of the ACM* 52(4), 2009.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 1 (measuring and summarizing performance) and ch. 4 (the roofline model, applied to SIMD and GPU architectures).
- P. J. Fleming and J. J. Wallace, "How Not to Lie with Statistics: The Correct Way to Summarize Benchmark Results," *Communications of the ACM* 29(3), 1986.
- SPEC CPU and MLPerf documentation (Sources).

## [15 · Control Systems](../courses/15-control-systems/README.md)

### [15-01 · Modeling Dynamic Systems](../courses/15-control-systems/chapters/15-01-modeling-dynamic-systems.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 2 (dynamic models of mechanical, electrical, electromechanical and heat-flow systems) and the linearization section of ch. 9.
- K. Ogata, *Modern Control Engineering*, ch. 3 (mathematical modeling of mechanical and electrical systems) and ch. 4 (fluid and thermal systems).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 2–3 (system modeling and examples; free online).
- MIT OpenCourseWare 2.04A, *Systems and Controls*: the modeling lectures.

### [15-02 · Transfer Functions and Block Diagrams](../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3 (transfer functions, block diagrams, the effect of pole and zero locations; Mason's rule in an appendix).
- N. S. Nise, *Control Systems Engineering*, ch. 5 (reduction of multiple subsystems, signal-flow graphs and Mason's rule).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 8–9 (transfer functions and the standard loop; free online).
- MIT OpenCourseWare 6.302, *Feedback Systems*: lectures on block diagrams and loop gain.

### [15-03 · Time Response and Specifications](../courses/15-control-systems/chapters/15-03-time-response.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3 (time-domain specifications, effects of zeros and extra poles).
- N. S. Nise, *Control Systems Engineering*, ch. 4 (time response, pole locations, higher-order approximations).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, the chapters on frequency response and feedback (doublets and settling time).
- MIT OpenCourseWare 6.302, *Feedback Systems*: lectures on second-order systems and time-domain specifications.

### [15-04 · Feedback Properties and Steady-State Error](../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 4 (the basic equations of control, sensitivity, steady-state tracking and system type).
- N. S. Nise, *Control Systems Engineering*, ch. 7 (steady-state errors, error constants, disturbances).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 11–12 (sensitivity functions and robustness; free online).
- B. A. Francis and W. M. Wonham, "The internal model principle of control theory," *Automatica* 12(5), 1976 (for the curious; beyond BSEE).

### [15-05 · Stability and the Routh–Hurwitz Criterion](../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 3 (stability, the Routh criterion and its special cases).
- N. S. Nise, *Control Systems Engineering*, ch. 6 (Routh–Hurwitz criterion, special cases, stability design via gain).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 5 (stability of linear systems; free online).
- F. R. Gantmacher, *The Theory of Matrices*, vol. 2, ch. 15 (the proof of the Routh–Hurwitz theorem; beyond BSEE).

### [15-06 · Root Locus](../courses/15-control-systems/chapters/15-06-root-locus.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 5 (the root-locus rules, design with dynamic compensation).
- N. S. Nise, *Control Systems Engineering*, ch. 8–9 (root-locus techniques and design via root locus).
- W. R. Evans, "Control system synthesis by root locus method," *Transactions of the AIEE* 69(1), 1950 (the method's original exposition).
- MIT OpenCourseWare 6.302, *Feedback Systems*: lectures on root locus.

### [15-07 · Frequency-Domain Design: Bode, Nyquist and Margins](../courses/15-control-systems/chapters/15-07-frequency-domain-design.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 6 (Bode and Nyquist, margins, the relation to damping).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 9–11 (Nyquist, robustness, the Bode integral and fundamental limits; free online).
- J. S. Freudenberg and D. P. Looze, "Right half plane poles and zeros and design tradeoffs in feedback systems," *IEEE Transactions on Automatic Control* 30(6), 1985.
- R. D. Middlebrook, "Measurement of loop gain in feedback systems," *International Journal of Electronics* 38(4), 1975.

### [15-08 · PID Control](../courses/15-control-systems/chapters/15-08-pid-control.md)

- K. J. Åström and T. Hägglund, *Advanced PID Control* (ISA, 2006): tuning, windup, filtering and setpoint weighting in depth.
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 11 (PID control; free online).
- J. G. Ziegler and N. B. Nichols, "Optimum settings for automatic controllers," *Transactions of the ASME* 64, 1942.
- S. Skogestad, "Simple analytic rules for model reduction and PID controller tuning," *Journal of Process Control* 13(4), 2003 (the SIMC rules).

### [15-09 · Lead and Lag Compensation](../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 5–6 (lead and lag design by root locus and frequency response).
- N. S. Nise, *Control Systems Engineering*, ch. 9 and 11 (design via root locus and via frequency response).
- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, ch. 9 (controller design for converters, including lead and Type III style compensators).

### [15-10 · State-Space Introduction](../courses/15-control-systems/chapters/15-10-state-space-introduction.md)

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 7 (state-space design: pole placement, estimators, the separation principle, integral control).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 6–8 (linear systems, state feedback, output feedback; free online).
- N. S. Nise, *Control Systems Engineering*, ch. 12 (design via state space).
- MIT OpenCourseWare 16.30/16.31, *Feedback Control Systems*: state-space lectures.

### [15-11 · Digital Control](../courses/15-control-systems/chapters/15-11-digital-control.md)

- G. F. Franklin, J. D. Powell and M. Workman, *Digital Control of Dynamic Systems* (the standard reference on sampled-data design).
- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 8 (digital control).
- K. J. Åström and B. Wittenmark, *Computer-Controlled Systems* (sampling, discretization, implementation).

### [15-12 · Applications: PLLs, Voltage Regulators and Thermal Management](../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md)

- F. M. Gardner, *Phaselock Techniques*, 3rd ed. (Wiley, 2005): loop analysis, the charge-pump PLL and its sampling limit.
- F. M. Gardner, "Charge-Pump Phase-Lock Loops," *IEEE Transactions on Communications*, 1980: the original stability analysis of the sampled charge-pump loop.
- B. Razavi, *Design of CMOS Phase-Locked Loops* (Cambridge University Press, 2020): loop dynamics, noise and digital PLLs.
- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., ch. 9 (controller design, output impedance).
- G. A. Rincón-Mora, *Analog IC Design with Low-Dropout Regulators* (McGraw-Hill): LDO compensation and ESR.
- Linux kernel documentation, *Power allocator governor tunables*; UEFI Forum, *ACPI Specification* 6.5 and 6.6, ch. 11 (Thermal Management) (see Sources).

## [16 · Digital Signal Processing](../courses/16-digital-signal-processing/README.md)

### [16-01 · Discrete-Time Signals and Systems Review](../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 2 (discrete-time signals and systems, convolution, difference equations, stability).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 1 (discrete sequences), ch. 5 (FIR filters and the moving average) and ch. 11 (signal averaging, including exponential averagers).
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), lectures 1–2.
- Horowitz, "Computing's energy problem" [1], for why data movement dominates energy.

### [16-02 · DTFT and z-Transform for DSP](../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 5 (transform analysis of LTI systems: frequency response from poles and zeros, all-pass and minimum-phase systems, linear phase).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 6 (IIR filters, pole-zero placement) and ch. 13 (DSP tricks, including DC removal and notch filters).
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), lectures on transform analysis and minimum-phase systems.

### [16-03 · The DFT and Its Properties](../courses/16-digital-signal-processing/chapters/16-03-the-dft.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 8 (the DFT, its properties, circular convolution, linear convolution with the DFT).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 3 (the DFT, leakage, zero padding) and ch. 13 (fast convolution).
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), lectures on the DFT and block convolution.

### [16-04 · The FFT Algorithm](../courses/16-digital-signal-processing/chapters/16-04-the-fft.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 9 (FFT algorithms: decimation in time and frequency, in-place computation, general N).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 4 (the FFT, butterflies, bit reversal).
- J. W. Cooley and J. W. Tukey [1], the paper that started it, three pages long.
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), FFT lectures.

### [16-05 · Spectral Analysis and Windowing](../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md)

- F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform" [1], the standard reference on windows and their figures of merit.
- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 10 (Fourier analysis of signals using the DFT, periodogram, averaging).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 3 (leakage, windows) and ch. 11 (signal averaging).

### [16-06 · FIR Filter Design](../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 7 (window and Kaiser design, optimal equiripple design, the alternation theorem).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 5 (FIR filters: window, Remez and frequency-sampling designs, with practical advice).
- T. W. Parks and J. H. McClellan, "Chebyshev approximation for nonrecursive digital filters with linear phase" [1], the paper behind every equiripple tool.

### [16-07 · IIR Filter Design](../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 7 (impulse invariance, the bilinear transform, Butterworth, Chebyshev and elliptic designs).
- Proakis & Manolakis, *Digital Signal Processing*, 4th ed., ch. 10 (IIR design by analog-to-digital mapping, with worked designs).
- R. Bristow-Johnson's cookbook, now the W3C *Audio EQ Cookbook* [5], for practical biquad formulas.

### [16-08 · Filter Structures and Implementation](../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 6 (structures, transposition, lattice, finite-precision effects).
- Proakis & Manolakis, *Digital Signal Processing*, 4th ed., ch. 9 (implementation of discrete-time systems, including lattice structures).
- K. K. Parhi, *VLSI Digital Signal Processing Systems*, Wiley, 1999 (retiming, pipelining and systolic structures, for the hardware view).

### [16-09 · Multirate DSP: Decimation, Interpolation and Polyphase](../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., §4.6–4.7 (changing the sampling rate, multirate signal processing, polyphase).
- P. P. Vaidyanathan, *Multirate Systems and Filter Banks*, Prentice Hall, 1993, ch. 4 (the standard reference on multirate theory).
- E. B. Hogenauer [1], the paper that introduced CIC filters, including register-growth and pruning analysis.

### [16-10 · Quantization and Fixed-Point Effects](../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md)

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., §4.8 (analysis of quantization errors) and §6.7–6.10 (finite-precision effects in filters, limit cycles).
- Proakis & Manolakis, *Digital Signal Processing*, 4th ed., ch. 9 (quantization effects in digital filters).
- R. M. Gray and D. L. Neuhoff, "Quantization", *IEEE Transactions on Information Theory* 44(6), 1998: a survey of when the additive-noise model holds.

### [16-11 · DSP Hardware Architectures](../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md)

- K. K. Parhi, *VLSI Digital Signal Processing Systems*, Wiley, 1999 (iteration bound, retiming, folding, unfolding, look-ahead, CSD).
- R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 13 (DSP tricks, including CORDIC-style rotations and multiplierless methods).
- M. Horowitz, "Computing's energy problem (and what we can do about it)", ISSCC 2014 [3].

## [17 · Communication Systems](../courses/17-communication-systems/README.md)

### [17-01 · Random Processes and Power Spectral Density](../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md)

- Gallager, *Principles of Digital Communication* (Cambridge, 2008), the chapter on random processes and noise; the MIT OCW 6.450 lecture notes it grew from are free.
- Proakis & Salehi, *Communication Systems Engineering*, the random-processes chapter, for worked problems at this level.
- Lathi & Ding, *Modern Digital and Analog Communication Systems*, random processes and spectral analysis, including the PSD of line codes.
- Papoulis & Pillai, *Probability, Random Variables and Stochastic Processes*, for the measure-theoretic details behind §3.3–§3.4.
- MIT OCW 6.450 *Principles of Digital Communication I* (Gallager), lectures on random processes.

### [17-02 · Noise and SNR in Communication Systems](../courses/17-communication-systems/chapters/17-02-noise-and-snr.md)

- Pozar, *Microwave and RF Design of Wireless Systems*, the chapter on noise in microwave circuits and receivers, for noise temperature, lossy lines and cascades.
- Haykin & Moher, *Communication Systems*, the chapters on noise and on noise in receivers.
- Proakis & Salehi, *Communication Systems Engineering*, the effect of noise on analog and digital systems.
- H. T. Friis, "Noise figures of radio receivers," *Proc. IRE*, 1944: the original four-page paper is still the clearest statement of the cascade formula.
- Keysight's noise-figure measurement fundamentals application note (AN 57-1), for the Y-factor method used to measure noise figure (now behind a registration form).
- MIT OCW 6.450 (Gallager), the lectures on the AWGN channel, for the signal-space view used in 17-05.

### [17-03 · Analog Modulation (Brief)](../courses/17-communication-systems/chapters/17-03-analog-modulation.md)

- Proakis & Salehi, *Communication Systems Engineering*, the chapters on analog modulation and on the effect of noise on analog systems.
- Haykin & Moher, *Communication Systems*, angle modulation and noise in CW modulation systems, including the FM threshold.
- Lathi & Ding, *Modern Digital and Analog Communication Systems*, angle modulation and Bessel spectra.
- S. O. Rice, "Statistical properties of a sine wave plus random noise," *Bell System Technical Journal*, 1948, for the theory behind FM clicks.
- MIT OCW 6.02 and 6.450 lecture notes, for the transition from analog to digital modulation.

### [17-04 · Baseband Digital Transmission](../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md)

- Proakis & Salehi, *Communication Systems Engineering*, the chapter on digital transmission through band-limited AWGN channels (Nyquist criterion, raised cosine, equalization).
- Gallager, *Principles of Digital Communication*, the chapter on the Nyquist criterion and degrees of freedom.
- Lathi & Ding, *Modern Digital and Analog Communication Systems*, line coding and pulse shaping.
- Dally & Poulton, *Digital Systems Engineering*, for signalling, equalization and timing in chip-to-chip links.
- H. Nyquist, "Certain topics in telegraph transmission theory," *Transactions of the AIEE*, 1928, the original statement of the criterion.

### [17-05 · Matched Filters and Optimal Detection](../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md)

- Proakis & Salehi, *Communication Systems Engineering*, the chapter on optimum receivers for the AWGN channel.
- Gallager, *Principles of Digital Communication*, the chapters on detection and on signal space (with the theorem of irrelevance done carefully).
- Wozencraft & Jacobs, *Principles of Communication Engineering* (1965), the classic source of the signal-space approach.
- Richards, *Fundamentals of Radar Signal Processing*, for matched filtering and pulse compression in radar.
- MIT OCW 6.450 (Gallager), lectures on detection and the AWGN channel.

### [17-06 · Bandpass Digital Modulation and BER](../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md)

- Proakis & Salehi, *Communication Systems Engineering*, the chapters on digital modulation in AWGN.
- Goldsmith, *Wireless Communications*, the chapter on digital modulation and its performance, including Craig's formula.
- Sklar, *Digital Communications*, for constellation geometry and error-rate curves.
- J. W. Craig, "A new, simple and exact result for calculating the probability of error for two-dimensional signal constellations," IEEE MILCOM, 1991.
- MIT OCW 6.450 (Gallager), lectures on QAM and the complex baseband.

### [17-07 · Information Theory and Shannon Capacity](../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md)

- Cover & Thomas, *Elements of Information Theory*, 2nd ed., chapters 2 (entropy), 5 (data compression), 7 (channel capacity) and 9 (Gaussian channel).
- MacKay, *Information Theory, Inference, and Learning Algorithms* (free online), for an intuitive and computational treatment.
- C. E. Shannon, "A mathematical theory of communication," *Bell System Technical Journal*, 1948, still readable and remarkably modern.
- Proakis & Salehi, *Communication Systems Engineering*, the chapter on information sources and channel capacity.
- MIT OCW 6.441 (Information Theory) lecture notes.

### [17-08 · Channel Coding](../courses/17-communication-systems/chapters/17-08-channel-coding.md)

- Lin & Costello, *Error Control Coding* (2nd ed.): chapters 3–5 (linear and cyclic codes), 7 (Reed–Solomon), 12 (Viterbi), 17 (LDPC).
- Moon, *Error Correction Coding*: a programmer-friendly treatment with algorithms for every decoder here.
- Richardson & Urbanke, *Modern Coding Theory*: density evolution and LDPC thresholds.
- MacKay, *Information Theory, Inference, and Learning Algorithms*, chapters 1, 47–50: free online; an intuitive path from Hamming codes to LDPC.
- Arıkan, "Channel Polarization", *IEEE Trans. Information Theory*, 2009: the original polar-code paper, readable after §3.8.
- MIT OpenCourseWare 6.02, *Introduction to EECS II: Digital Communication Systems*: lectures on block codes, convolutional codes and Viterbi decoding.

### [17-09 · Wireless Channels: Fading and Multipath](../courses/17-communication-systems/chapters/17-09-wireless-channels.md)

- Rappaport, *Wireless Communications: Principles and Practice* (2nd ed.): chapters 4 (large-scale path loss, two-ray model, log-distance and shadowing) and 5 (small-scale fading, delay spread, Doppler, Clarke's model, level crossings).
- Goldsmith, *Wireless Communications*: chapters 2–3 (path loss, shadowing, statistical multipath) and 6 (performance in fading).
- Tse & Viswanath, *Fundamentals of Wireless Communication*: chapter 2 (physical modelling) and chapter 3 (detection, diversity); free online from the authors.
- 3GPP TR 38.901: §7.4 (path loss, shadowing) and §7.5 (fast-fading model), for anyone building a system simulator.
- MIT OpenCourseWare 6.450, *Principles of Digital Communication I*: lectures on wireless channels.

### [17-10 · OFDM](../courses/17-communication-systems/chapters/17-10-ofdm.md)

- Goldsmith, *Wireless Communications*, chapter 12 (multicarrier modulation): the matrix view of the cyclic prefix, PAPR, and frequency-offset effects.
- Dahlman, Parkvall & Sköld, *5G NR: The Next Generation Wireless Access Technology*: the NR numerology, resource grid and transform precoding.
- Tse & Viswanath, *Fundamentals of Wireless Communication*, §3.4: OFDM as a diagonalization of the circulant channel.
- Proakis & Salehi, *Digital Communications*: multicarrier systems and their performance.
- 3GPP TS 38.211, clauses 4 and 5.3: the definitive NR timing definitions used in this chapter.

### [17-11 · MIMO and Beamforming Basics](../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md)

- Tse & Viswanath, *Fundamentals of Wireless Communication*: chapter 3 (diversity, Alamouti), chapter 7 (MIMO channel modelling, degrees of freedom), chapter 8 (MIMO capacity, receivers); free from the authors.
- Heath & Lozano, *Foundations of MIMO Communication*: a modern, thorough treatment including massive MIMO.
- Goldsmith, *Wireless Communications*: chapter 7 (diversity) and chapter 10 (MIMO).
- Marzetta, Larsson, Yang & Ngo, *Fundamentals of Massive MIMO*: channel hardening and favourable propagation.
- Van Trees, *Optimum Array Processing*: array factors, beam patterns and nulling.

### [17-12 · Multiple Access, Cellular and Wi-Fi Systems](../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md)

- Rappaport, *Wireless Communications*: chapter 3 (cellular concept, reuse, trunking and Erlang B) and chapter 9 (multiple access).
- Goldsmith, *Wireless Communications*: chapters 13 (spread spectrum), 14 (multiuser systems) and 15 (cellular systems).
- Bertsekas & Gallager, *Data Networks*: chapter 4 (multiaccess communication: ALOHA, CSMA, stability).
- Tse & Viswanath, *Fundamentals of Wireless Communication*, chapter 6: multi-user capacity and opportunistic (multi-user-diversity) scheduling.
- Dahlman, Parkvall & Sköld, *5G NR*: scheduling, HARQ and the overall NR architecture.

### [17-13 · Computer Networks Fundamentals](../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md)

- Kurose & Ross, *Computer Networking: A Top-Down Approach*: chapters 1 (layers, delay), 3 (TCP, congestion control), 4–5 (IP, routing algorithms), 6 (link layer, Ethernet, switching) and 8 (security).
- Peterson & Davie, *Computer Networks: A Systems Approach*: free online; strong on congestion control and switching.
- The RFCs themselves (RFC 9293, 5681, 6298, 8200, 8446) are readable and authoritative.
- MIT OpenCourseWare 6.829, *Computer Networks*: congestion control and routing at graduate depth.
- NCEES FE Reference Handbook: the computer-networks section used on the exam.

## [18 · Embedded Systems and Microcontrollers](../courses/18-embedded-systems-and-microcontrollers/README.md)

### [18-01 · Microcontroller Architecture](../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md)

- Yiu, *The Definitive Guide to Arm Cortex-M3 and Cortex-M4 Processors*, 3rd ed.: chapters 2–6 (architecture, programmer's model, memory system).
- Valvano, *Embedded Systems: Introduction to ARM Cortex-M Microcontrollers*: chapters on the memory map and I/O.
- Arm, *Armv7-M Architecture Reference Manual* and *Armv8-M Architecture Reference Manual*: the authoritative memory map and exception model.
- The reference manual of any one MCU you might use: read its memory map, clock tree and flash interface chapters alongside this one.
- Lee & Seshia, *Introduction to Embedded Systems* (free online): chapter on memory architectures.

### [18-02 · Bare-Metal C and the Build Toolchain](../courses/18-embedded-systems-and-microcontrollers/chapters/18-02-bare-metal-c-and-toolchain.md)

- Yiu, *The Definitive Guide to Arm Cortex-M3 and Cortex-M4 Processors*, 3rd ed.: chapters on the programmer's model, exceptions and the software development flow.
- Valvano, *Embedded Systems: Introduction to ARM Cortex-M Microcontrollers*: chapters on I/O registers and the build process.
- The GNU `ld` manual, "Linker Scripts" chapter (memory regions, `AT`, `LOADADDR`, `KEEP`); LLD accepts the same syntax.
- Arm, *Procedure Call Standard for the Arm Architecture* (AAPCS32) and the *Armv7-M Architecture Reference Manual*, chapters on the exception model and stack frames.
- Arm, *CMSIS-Core* documentation: the device header conventions (`__IO`, `__I`) and startup templates.

### [18-03 · Interrupts, Exceptions and Timers](../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md)

- Yiu, *The Definitive Guide to Arm Cortex-M3 and Cortex-M4 Processors*, 3rd ed.: chapters on exceptions and interrupts, the NVIC, fault exceptions and SysTick.
- Arm, *Armv7-M Architecture Reference Manual*: the exception model, priority grouping and fault status registers.
- Liu, C. L. and Layland, J. W., "Scheduling algorithms for multiprogramming in a hard-real-time environment", *Journal of the ACM*, 1973: the origin of fixed-priority analysis.
- Any MCU reference manual's general-purpose timer chapter (counting modes, capture/compare, PWM) and watchdog chapter.

### [18-04 · DMA and Data Movement](../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md)

- Yiu, *The Definitive Guide to Arm Cortex-M3 and Cortex-M4 Processors*: the memory system and bus interfaces; Arm's application notes on cache maintenance for the Cortex-M7.
- Valvano, *Embedded Systems: Real-Time Interfacing to ARM Cortex-M Microcontrollers*: FIFOs and DMA.
- Any MCU reference manual's DMA chapter (channel registers, request mapping, circular and double-buffer modes) and its bus-matrix chapter.
- Arm, *PrimeCell µDMA Controller (PL230) Technical Reference Manual*: a complete, readable description of one DMA controller.

### [18-05 · Peripherals and Serial Buses: GPIO, UART, SPI, I²C](../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md)

- NXP, *UM10204 I²C-bus specification and user manual*, Rev. 7.0: the protocol, timing and electrical tables.
- MIPI Alliance, *I3C Basic* specification (public) and the I3C FAQ.
- Horowitz & Hill, *The Art of Electronics*, 3rd ed., chapter 14 (digital interfacing, level translation).
- Any MCU reference manual's GPIO, USART, SPI and I²C chapters, together with the data sheet's electrical tables.

### [18-06 · Analog Interfaces: ADC, DAC and PWM](../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md)

- Horowitz & Hill, *The Art of Electronics*, 3rd ed., chapter 13 (digital meets analog: converters, sampling, references).
- Kester, W. (ed.), *The Data Conversion Handbook*, Analog Devices / Newnes, 2005: chapters on ADC specifications and driving ADC inputs.
- Any MCU's ADC chapter and electrical tables, read together with its vendor's application note on input impedance and sampling time.
- Valvano, *Embedded Systems: Real-Time Interfacing to ARM Cortex-M Microcontrollers*, data-acquisition chapters.

### [18-07 · RTOS Concepts](../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md)

- Buttazzo, G., *Hard Real-Time Computing Systems*, 3rd ed., Springer, 2011: chapters 4 (periodic scheduling, RM and EDF) and 7 (resource-access protocols).
- Liu, C. L. and Layland, J. W., "Scheduling algorithms for multiprogramming in a hard-real-time environment", *Journal of the ACM* 20(1), 1973.
- Barry, R., *Mastering the FreeRTOS Real Time Kernel* (free tutorial book, freertos.org).
- The Zephyr Project documentation: kernel services and scheduling.

### [18-08 · Boot, Bootloaders and Firmware Update](../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md)

- IETF RFC 9019, *A Firmware Update Architecture for Internet of Things* (2021), and RFC 9124, *A Manifest Information Model for Firmware Updates in IoT Devices* (2022).
- The MCUboot design document (docs.mcuboot.com/design.html): image format, swap algorithms and their recovery logic.
- Arm, *PSA Certified Firmware Update API* 1.0.
- Any MCU's reference manual chapter on its ROM bootloader and boot configuration.

### [18-09 · Ultra-Low-Power Design](../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md)

- Any ULP MCU's data-sheet tables of mode currents and wake-up times, read together with its reference manual's power-control chapter.
- Vendor application notes on battery-life estimation and on measuring low currents.
- EEMBC's ULPMark documentation for how standardized low-power benchmarks are defined.

### [18-10 · Sensors: IMU, PPG, MEMS and Audio](../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md)

- Kaajakari, V., *Practical MEMS*, Small Gear Publishing, 2009: accelerometers, gyroscopes, noise.
- Fraden, J., *Handbook of Modern Sensors*, 5th ed., Springer, 2016.
- Allen, J., "Photoplethysmography and its application in clinical physiological measurement", *Physiological Measurement* 28(3), 2007.
- Any IMU, PPG AFE and MEMS microphone data sheet, read alongside its application notes on FIFOs and low-power modes.

### [18-11 · Hardware Security](../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md)

- Mangard, S., Oswald, E. and Popp, T., *Power Analysis Attacks: Revealing the Secrets of Smart Cards*, Springer, 2007.
- Tehranipoor, M. and Wang, C. (eds.), *Introduction to Hardware Security and Trust*, Springer, 2012.
- Arm's TrustZone for Armv8-M documentation and the Trusted Firmware-M project documentation.
- The PSA Certified and SESIP documents, and the text of the EU Cyber Resilience Act.

## [19 · Digital VLSI Design](../courses/19-digital-vlsi-design/README.md)

### [19-01 · The CMOS Inverter: Static Characteristics](../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md)

- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits: A Design Perspective*, 2nd ed., ch. 5 (the CMOS inverter, static behavior).
- Weste & Harris, *CMOS VLSI Design*, 4th ed., §2.5 (DC transfer characteristics) and §2.6 (switch-level and noise margins).
- Sedra & Smith, *Microelectronic Circuits*, the CMOS inverter chapter (voltage transfer characteristic and noise margins).
- MIT OCW 6.374, *Analysis and Design of Digital Integrated Circuits*, the CMOS inverter lectures.

### [19-02 · The CMOS Inverter: Dynamic Behavior and Delay](../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md)

- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., §5.4 (dynamic behavior and the propagation delay).
- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 4 (delay, RC models and the FO4 metric).
- Kang & Leblebici, *CMOS Digital Integrated Circuits*, the inverter switching chapter (exact delay by integration).
- Harris, Ho, Wei & Horowitz, "The fanout-of-4 inverter delay metric": why the FO4 delay normalizes process and operating conditions.
- MIT OCW 6.374, the inverter-delay lectures.

### [19-03 · Combinational Logic Families](../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md)

- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 6 (static CMOS, ratioed, pass-transistor and dynamic logic).
- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 9 (combinational circuit families) and §4.3 (the Elmore delay).
- W. C. Elmore, "The transient response of damped linear networks with particular regard to wideband amplifiers", *J. Applied Physics*, 1948: the original definition.
- MIT OCW 6.374, the lectures on combinational logic and dynamic circuits.

### [19-04 · Transistor Sizing and Logical Effort](../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md)

- Sutherland, Sproull & Harris, *Logical Effort: Designing Fast CMOS Circuits*, Morgan Kaufmann, 1999, ch. 1–4 (the method, with many worked designs).
- Weste & Harris, *CMOS VLSI Design*, 4th ed., §4.5 (logical effort and transistor sizing).
- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., §5.4.3 (sizing a chain of inverters) and §6.2.1 (logical effort).
- MIT OCW 6.374, the lectures on logical effort.

### [19-05 · Interconnect](../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md)

- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 4 (the wire) and ch. 9 (coping with interconnect).
- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 6 (interconnect).
- R. Ho, K. Mai and M. Horowitz, "The future of wires", *Proc. IEEE*, 2001.
- H. B. Bakoglu, *Circuits, Interconnections, and Packaging for VLSI*, Addison-Wesley, 1990.

### [19-06 · Power and Low-Power Design](../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)

- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., §5.5 (power dissipation of the inverter) and ch. 11 (low-power design).
- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 5 (power).
- A. Chandrakasan, S. Sheng and R. Brodersen, "Low-power CMOS digital design", *IEEE J. Solid-State Circuits*, 1992: the voltage-scaling and parallelism argument.
- H. J. M. Veendrick, "Short-circuit dissipation of static CMOS circuitry and its impact on the design of buffer circuits", *IEEE J. Solid-State Circuits*, 1984.

### [19-07 · Sequential Circuits, Timing and Clocking](../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md)

- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 10 (sequential circuit design) and ch. 13 (clocking).
- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 7 (sequential logic) and ch. 10 (timing issues).
- D. Harris, *Skew-Tolerant Circuit Design*, Morgan Kaufmann, 2001: latches, time borrowing and skew tolerance in depth.
- C. Dike and E. Burton, "Miller and noise effects in a synchronizing flip-flop", *IEEE J. Solid-State Circuits*, 1999: measured metastability.

### [19-08 · SRAM Design](../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md)

- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 12 (array subsystems).
- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 12 (memories).
- E. Seevinck, F. List and J. Lohstroh, "Static-noise margin analysis of MOS SRAM cells", *IEEE J. Solid-State Circuits*, 1987: the SNM definition and its computation.

### [19-09 · Layout, Design Rules and Standard Cells](../courses/19-digital-vlsi-design/chapters/19-09-layout-and-standard-cells.md)

- Weste & Harris, *CMOS VLSI Design*, 4th ed., §1.5 (layout and design rules) and ch. 3 (CMOS processing technology).
- Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 2 (the manufacturing process and design rules).
- The SkyWater SKY130 PDK documentation: its design-rule pages and standard-cell library descriptions are a rare open view of a real process.
- D. Harris, lecture slides for *CMOS VLSI Design*, the lecture on circuits and layout (stick diagrams, design rules, cell pitch).

### [19-10 · The ASIC Flow I: Synthesis and Static Timing Analysis](../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md)

- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 14 (design methodology and tools) and §10.2 (sequencing static circuits, for the timing constraints).
- J. Bhasker and R. Chadha, *Static Timing Analysis for Nanometer Designs* (Springer, 2009): the practitioner's reference for Liberty, SDC, OCV and CRPR.
- G. De Micheli, *Synthesis and Optimization of Digital Circuits* (McGraw-Hill, 1994), ch. 10 (library binding by tree covering).
- K. Keutzer, "DAGON: technology binding and local optimization by DAG matching", *Proc. 24th Design Automation Conference*, 1987: the tree-covering method of §3.2.
- The OpenSTA and Yosys documentation, for open-source tools that implement the methods of this chapter.
- R. Rutenbar, *VLSI CAD Part I: Logic* (University of Illinois, Coursera), the lectures on technology mapping, and *VLSI CAD Part II: Layout*, the lectures on static timing analysis.

### [19-11 · The ASIC Flow II: Floorplan, Place and Route, Signoff](../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md)

- A. B. Kahng, J. Lienig, I. L. Markov and J. Hu, *VLSI Physical Design: From Graph Partitioning to Timing Closure*, 2nd ed. (Springer, 2022): partitioning, floorplanning, placement, routing and clock trees with algorithms.
- Weste & Harris, *CMOS VLSI Design*, 4th ed., §13.4 (clock distribution), §13.3 (power distribution) and ch. 14.
- The OpenROAD and OpenROAD-flow-scripts documentation, for an open flow whose every step can be inspected.
- R. Rutenbar, *VLSI CAD Part II: Layout* (University of Illinois, Coursera): video lectures on partitioning, placement, routing and interconnect timing.

### [19-12 · Design for Test: Scan, BIST and ATPG](../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md)

- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 15 (testing, debugging and verification).
- M. L. Bushnell and V. D. Agrawal, *Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits* (Springer, 2000): fault models, ATPG, BIST and memory test in depth.
- L.-T. Wang, C.-W. Wu and X. Wen (eds.), *VLSI Test Principles and Architectures: Design for Testability* (Morgan Kaufmann, 2006): scan, compression and BIST architectures.

### [19-13 · Verification: Simulation, UVM, Formal and Emulation](../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md)

- C. Spear and G. Tumbush, *SystemVerilog for Verification*, 3rd ed. (Springer, 2012): classes, constrained randomization, coverage and assertions, the language layer under UVM.
- E. Seligman, T. Schubert and M. V. A. K. Kumar, *Formal Verification: An Essential Toolkit for Modern VLSI Design* (Morgan Kaufmann): practical property checking, equivalence checking and formal apps.
- E. M. Clarke, O. Grumberg, D. Kroening, D. Peled and H. Veith, *Model Checking*, 2nd ed. (MIT Press, 2018): the theory of transition systems, temporal logic and symbolic algorithms.
- R. E. Bryant, "Graph-based algorithms for Boolean function manipulation," *IEEE Trans. Computers*, 1986: the original ROBDD paper, short and readable.
- Weste & Harris, *CMOS VLSI Design*, 4th ed., ch. 15 (testing, debugging and verification).

## [20 · Analog and Mixed-Signal IC Design](../courses/20-analog-and-mixed-signal-ic-design/README.md)

### [20-01 · Analog Design Fundamentals in Nanometer CMOS](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md)

- P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Circuits Using Pre-Computed Lookup Tables* (Cambridge University Press): the method in full, with lookup tables for real processes.
- C. C. Enz and E. A. Vittoz, *Charge-Based MOS Transistor Modeling: The EKV Model for Low-Power and RF IC Design* (Wiley, 2006): the model of §3.2–3.4, derived from the charge sheet.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed. (McGraw-Hill, 2017): the device-physics and nanometer-design chapters, for the same trade-offs in a design-oriented setting.
- B. Razavi's analog circuit design lectures (UCLA, public video), and B. Murmann's analog IC design course materials (Stanford EE214).

### [20-02 · Two-Stage Op-Amp Design](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md)

- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the chapters on operational amplifiers and on stability and frequency compensation.
- T. C. Carusone, D. A. Johns and K. W. Martin, *Analog Integrated Circuit Design*, 2nd ed., Wiley, 2012: the chapters on basic and advanced op-amp design.
- P. G. A. Jespers and B. Murmann, *Systematic Design of Analog CMOS Circuits*, Cambridge University Press, 2017: the $g_m/I_D$-based two-stage design, with the lookup-table version of §3.3's optimization.
- Lecture videos: Ali Hajimiri's Caltech analog circuit design lectures and Razavi's UCLA lecture series (both on YouTube) cover op-amp compensation; Murmann's Stanford EE 214B materials cover $g_m/I_D$-based amplifier design.

### [20-03 · Bandgap and Voltage References](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md)

- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the bandgap references chapter (PTAT generation, curvature, startup, sub-1 V references).
- P. R. Gray, P. J. Hurst, S. H. Lewis and R. G. Meyer, *Analysis and Design of Analog Integrated Circuits*, 5th ed., Wiley, 2009: the current-source and reference chapter (Widlar, Brokaw, curvature analysis).
- G. A. Rincón-Mora, *Voltage References: From Diodes to Precision High-Order Bandgap Circuits*, Wiley–IEEE Press, 2002: a book-length treatment of curvature correction and trimming.
- Lecture videos: Razavi's UCLA analog lectures on bandgap references (YouTube) and the bandgap lectures in Ali Hajimiri's Caltech analog series.

### [20-04 · Low-Dropout Regulators](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md)

- G. A. Rincón-Mora, *Analog IC Design with Low-Dropout Regulators*, 2nd ed., McGraw-Hill, 2014: the book-length treatment of LDO design.
- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the voltage-regulator sections.
- Texas Instruments application notes on LDO terms, PSRR and stability (cited in §14) for how specifications are defined and measured.
- Lecture videos: power-management IC lectures from university courses on analog IC design (search for "LDO regulator design lecture"), and vendor training series on LDO fundamentals.

### [20-05 · Comparators and Sample-and-Hold Circuits](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md)

- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the switched-capacitor and comparator chapters.
- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the sample-and-hold and comparator chapters.
- B. Razavi, "The StrongARM latch," *IEEE Solid-State Circuits Magazine*, 2015, and "The bootstrapped switch," *IEEE Solid-State Circuits Magazine*, 2015: short, clear tutorials (cited in §14).
- Lecture videos: data-converter lectures from university courses on mixed-signal IC design (search for "sample and hold kT/C lecture" and "StrongARM latch lecture").

### [20-06 · Data Converter Fundamentals](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md)

- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapters on converter specifications and quantization.
- F. Maloberti, *Data Converters*, Springer, 2007: specifications and testing.
- IEEE Std 1241-2023, *Terminology and Test Methods for Analog-to-Digital Converters* (cited in §14), for the formal definitions and test procedures.
- B. Murmann, "ADC Performance Survey" (github.com/bmurmann/ADC-survey): download the spreadsheet and plot the figures of merit yourself.

### [20-07 · Nyquist ADCs: Flash, SAR and Pipeline](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md)

- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapters on Nyquist converters.
- B. Razavi, "A tale of two ADCs: Pipelined versus SAR," *IEEE Solid-State Circuits Magazine*, 2015, and "Design considerations for interleaved ADCs," *IEEE JSSC*, 2013 (§14 [5], [6]): short, rigorous treatments; both are posted on the author's UCLA page.
- B. Murmann, ADC Performance Survey (github.com/bmurmann/ADC-survey): filter the spreadsheet by architecture and plot figure of merit against speed.

### [20-08 · Oversampling and Sigma-Delta Converters](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md)

- R. Schreier, S. Pavan and G. C. Temes, *Understanding Delta-Sigma Data Converters*, 2nd ed., Wiley-IEEE Press, 2017, DOI 10.1002/9781119258308: the standard text; chapters on first- and second-order modulators, higher-order design and continuous-time loops.
- B. Razavi, "The delta-sigma modulator," *IEEE Solid-State Circuits Magazine*, Spring 2016 (§14 [10]): a six-page history and tour, posted on the author's UCLA page.
- R. Schreier, "Oversampling Delta-Sigma Data Converters: The One-Page Story" and his University of Toronto ECE1371 slides (§14 [5]): the noise-shaping law, Lee's rule and toolbox practice in compact form.
- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapter on sigma-delta modulation.
- R. Schreier's Delta Sigma Toolbox (MATLAB, BSD-style licence): synthesize NTFs (its `synthesizeNTF` defaults to Lee's 1.5), simulate modulators and find the maximum stable amplitude.

### [20-09 · DACs](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md)

- D. Johns and K. Martin, *Analog Integrated Circuit Design*, Wiley, 1997 (2nd ed. with T. Chan Carusone, 2012): the chapter on D/A converters.
- M. Pelgrom, *Analog-to-Digital Conversion*, 4th ed., Springer, 2022: the chapter on digital-to-analog conversion.
- The papers in §14 on segmented current-steering design and output-impedance limits.

### [20-10 · PLLs and Jitter](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md)

- B. Razavi, *Design of CMOS Phase-Locked Loops: From Circuit Level to Architecture Level*, Cambridge University Press, 2020.
- D. Banerjee, *PLL Performance, Simulation and Design*: a practitioner's book on loop-filter design and noise, available free from the author and Texas Instruments.
- The papers in §14 on charge-pump loops, oscillator phase noise and fractional-N synthesis.

### [20-11 · Layout, Matching and PVT Variation](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md)

- A. Hastings, *The Art of Analog Layout*, 2nd ed., Prentice Hall, 2005: the standard text on matching layout, guard rings and latch-up.
- M. J. M. Pelgrom, A. C. J. Duinmaijer and A. P. G. Welbers, "Matching properties of MOS transistors," *IEEE J. Solid-State Circuits*, 1989: the original area law.
- P. R. Kinget, "Device mismatch and tradeoffs in the design of analog circuits," *IEEE J. Solid-State Circuits*, 2005: the speed–accuracy–power limit.

### [20-12 · Why Analog Does Not Scale Like Digital](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md)

- B. Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd ed., McGraw-Hill, 2017: the chapter on nanometer design studies.
- P. R. Kinget, "Device mismatch and tradeoffs in the design of analog circuits," *IEEE J. Solid-State Circuits*, 2005.
- B. Murmann, "Digitally assisted analog circuits," *IEEE Micro*, 2006, and his public ADC performance survey (20-06).

## [21 · RF and Microwave Engineering](../courses/21-rf-and-microwave-engineering/README.md)

### [21-01 · S-Parameters and Network Analysis](../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md)

- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the chapters on microwave network analysis and on microwave amplifier design (stability and gain).
- Hewlett-Packard Application Note 95-1, *S-Parameter Techniques for Faster, More Accurate Network Design* [3], and Application Note 1287-3, *Applying Error Correction to Network Analyzer Measurements* [9]: the classic practical introductions to S-parameters and VNA calibration. D. F. Williams, "Traveling Waves and Power Waves" [2], for the subtleties of wave definitions.

### [21-02 · Impedance Matching Networks](../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md)

- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the impedance-matching chapter (L-sections, stubs, multi-section transformers, Bode–Fano).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge, 2004: the chapters on passive components and matching.
- R. M. Fano's 1950 paper [2] for the full broadband-matching theory, and Mohan et al. [8] for spiral-inductance formulas that are accurate enough for hand design.

### [21-03 · Noise Figure and Linearity](../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md)

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the chapter on basic concepts (nonlinearity, noise, sensitivity and dynamic range).
- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the chapter on noise and nonlinear distortion, and the amplifier-design chapter for noise circles.
- Agilent Application Note 57-1, *Fundamentals of RF and Microwave Noise Figure Measurements* [5]: the Y-factor method and its corrections, clearly explained.

### [21-04 · Low-Noise Amplifiers](../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md)

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the LNA chapter (topologies, inductive degeneration, noise cancelling, linearity).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004: the LNA chapter, including induced gate noise and the power-constrained optimum.

### [21-05 · Mixers](../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md)

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the mixer chapter and the transceiver-architecture chapter (image-reject and zero-IF receivers).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004: the mixer chapter.
- A. Ghaffari et al. [9] for a clear model of N-path filters, and C. Andrews and A. C. Molnar [11] for the mixer-first receiver.

### [21-06 · Oscillators and VCOs](../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md)

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the oscillator chapter (cross-coupled and Colpitts oscillators, phase noise, quadrature oscillators) [15].
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004: the oscillator and phase-noise chapters, the most readable account of the ISF.
- T. H. Lee and A. Hajimiri, "Oscillator phase noise: A tutorial" [2], and B. Razavi, "A study of injection locking and pulling in oscillators" [5]: both clear enough to read straight after this chapter.

### [21-07 · Power Amplifiers](../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md)

- S. C. Cripps, *RF Power Amplifiers for Wireless Communications*, 2nd ed., Artech House, 2006 [14]: load-line design, reduced conduction angle, class E and F, Doherty and linearization; the practitioner's reference.
- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012 [15]: the power-amplifier and transmitter chapters, with CMOS-specific techniques.
- The Doherty and class-E original papers [1, 3] are readable after this chapter, and Raab et al.'s 2002 survey [3] maps the whole field.

### [21-08 · Transceiver Architectures](../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md)

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012 [12]: the transceiver-architecture chapter.
- S. Mirabbasi and K. Martin, "Classical and modern receiver architectures" [12], a compact survey; A. A. Abidi, "The path to the software-defined radio receiver" [5].
- V. Bhagavatula, "Exploring multimode cellular transceiver design: A short tutorial" [12], for how a modern cellular transceiver is organized.

### [21-09 · The RF Front End: Filters, Switches and Modules](../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md)

- A. Hagelauer et al., "From microwave acoustic filters to millimeter-wave operation and new applications" [19], an open-access survey of SAW, BAW and XBAR technology by the field's leading authors.
- C. C. W. Ruppel, "Acoustic wave filter technology–a review" [1], and R. Aigner, "SAW and BAW technologies for RF filter applications" [19], two compact reviews from inside the industry.
- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012 [19]: the microwave-filters chapter, for the classical filter theory that acoustic ladders approximate.

### [21-10 · Antennas, Arrays, Beamforming and mmWave](../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md)

- C. A. Balanis, *Antenna Theory: Analysis and Design*, 4th ed., Wiley, 2016: the microstrip-antenna and array chapters.
- R. J. Mailloux, *Phased Array Antenna Handbook*, Artech House: scan loss, grating lobes, quantization and true-time delay in depth.
- B. Sadhu et al. [6], for how a production-grade millimetre-wave phased-array IC is organized, and T. S. Rappaport et al. [5], for the measurements that started 5G millimetre-wave.

### [21-11 · Link Budgets](../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md)

- T. S. Rappaport, *Wireless Communications: Principles and Practice*, 2nd ed., Prentice Hall, 2002: the propagation chapters, including the edge-to-area coverage derivation.
- W. C. Jakes (ed.), *Microwave Mobile Communications*, Wiley, 1974, the origin of the area-coverage formula, and H. Suzuki [10] for combined shadowing and fading.
- 3GPP TR 38.913 [5], whose coupling-loss template is the industry's standard one-page budget.

### [21-12 · Modem Baseband Architecture and Wireless Standards](../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md)

- E. Dahlman, S. Parkvall and J. Sköld, *5G NR: The Next Generation Wireless Access Technology*, Academic Press: the physical-layer and HARQ chapters.
- E. D. Kaplan and C. J. Hegarty (eds.), *Understanding GPS/GNSS: Principles and Applications*, Artech House: signal structure and dual-frequency processing.
- D. Coppens et al. [6], an open review of UWB standards and ranging.

## [22 · Power Electronics and Energy Conversion](../courses/22-power-electronics-and-energy-conversion/README.md)

### [22-01 · Power Conversion Principles](../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 1 (introduction: why switching, efficiency and size) and ch. 2 (principles of steady-state analysis).
- J. G. Kassakian, D. J. Perreault, G. C. Verghese and M. F. Schlecht, *Principles of Power Electronics*, 2nd ed., Cambridge University Press, 2023: the opening chapters on switching conversion and averaging.
- MIT OpenCourseWare, 6.334 *Power Electronics*: the first lectures on switching power conversion.
- University of Colorado Boulder, *Introduction to Power Electronics* (Coursera, R. W. Erickson): the first module.

### [22-02 · Steady-State Analysis and the Buck Converter](../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 2 (volt-second and charge balance, the small-ripple approximation), ch. 3 (equivalent circuits with losses) and ch. 5 (the discontinuous conduction mode).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the step-down converter, including the CCM–DCM boundary.
- University of Colorado Boulder, *Converter Circuits* and *Introduction to Power Electronics* (Coursera, R. W. Erickson): the steady-state and DCM modules.

### [22-03 · Boost, Buck-Boost and Other Topologies](../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 2 (boost and buck-boost by volt-second balance), ch. 3 (the boost with inductor resistance), ch. 5 (DCM) and ch. 6 (converter circuits: Ćuk, SEPIC and the evaluation of switch stresses).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the step-up, buck-boost and Ćuk converters.
- University of Colorado Boulder, *Converter Circuits* (Coursera, R. W. Erickson): the topology modules.

### [22-04 · Isolated Converters: Flyback and Forward](../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 6 (transformer-isolated converters: forward, flyback, bridge, push-pull, and the transformer model).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the switch-mode dc power supplies chapter.
- TI Power Supply Design Seminar papers on clearance and creepage, and on flyback design (see Sources).

### [22-05 · Magnetics Design](../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: ch. 10 (basic magnetics theory, including the proximity effect and Dowell's analysis), ch. 11 (inductor design, the $K_g$ method) and ch. 12 (transformer design, the optimum flux density).
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics: Converters, Applications, and Design*, 3rd ed., Wiley, 2003: the chapters on magnetic components and on inductor and transformer design.
- C. W. T. McLyman, *Transformer and Inductor Design Handbook*: the area-product method with core tables.
- Vendor design tools and loss curves for the core family you use; the MagNet database for measured loss data [6].

### [22-06 · Converter Losses and Wide-Bandgap Switches](../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020, ch. 4 (switch realization: switching loss, diode recovery, device types) [15].
- B. J. Baliga, *Fundamentals of Power Semiconductor Devices*, 2nd ed., Springer, 2019: unipolar limits, superjunctions and IGBTs.
- N. Mohan, T. M. Undeland and W. P. Robbins, *Power Electronics*, 3rd ed., Wiley, 2003: the chapters on power devices and on resonant converters.
- Device vendors' application notes on reading data sheets (for example Infineon's on the CoolSiC 1200 V data sheet [3]).

### [22-07 · Converter Dynamics and Control](../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: the chapters on AC equivalent-circuit modeling, converter transfer functions, controller design and current-programmed control.
- R. D. Middlebrook and S. Ćuk's state-space averaging paper [11], V. Vorpérian's PWM-switch model [12] and R. B. Ridley's current-mode model [13], the three classic papers behind this chapter.
- Vendor compensation notes such as TI SLVA662 [3] and Renesas TB417 [2].

### [22-08 · PMICs and Power Management for SoCs](../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md)

- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*, 3rd ed., Springer, 2020: the chapters on discontinuous conduction and light-load operation.
- J. Rabaey, *Low Power Design Essentials*, Springer, 2009: supply-voltage scaling, power gating and adaptive techniques from the logic designer's side.
- The data sheets of a full PMIC (TPS65219 [3] or TPS6594-Q1 [4]) and a wearable PMIC (nPM1300 [5]): read the sequencing, DVS and low-power-state sections against this chapter.
- D. Ernst et al., the Razor paper [9], for how timing speculation removes voltage guardband.

### [22-09 · Batteries, Charging and Fuel Gauging](../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md)

- G. L. Plett, *Battery Management Systems, Volume I: Battery Modeling* (Artech House, 2015) and *Volume II: Equivalent-Circuit Methods* (2016): equivalent-circuit models, OCV and parameter identification, and Kalman-filter SOC estimation, the natural next step after §3.6.
- *Linden's Handbook of Batteries*, 5th ed., K. W. Beard (ed.), McGraw-Hill, 2019: the chemistries and their ratings.
- TI's Impedance Track and gauging comparison notes [6], [7] for how commercial gauges combine the methods of §3.6.

### [22-10 · Datacenter Power Delivery](../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)

- M. Swaminathan and A. E. Engin, *Power Integrity Modeling and Design for Semiconductors and Systems*, Prentice Hall, 2007: PDN modeling, target impedance and decoupling.
- L. D. Smith and E. Bogatin, *Principles of Power Integrity for PDN Design—Simplified*, Prentice Hall, 2017: an intuitive treatment of the first droop, damping and the role of each capacitor level.
- K. Radhakrishnan's 2022 IEEE seminar on microprocessor power delivery [24] and Intel's 2026 white paper [25] for an industry view from regulator to die.
- The OCP specifications cited here [6], [7], [19], [26]: they are public and show what hyperscalers actually require.

### [22-11 · Electric Machines and Drives](../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md)

- S. J. Chapman, *Electric Machinery Fundamentals*, 5th ed., McGraw-Hill, 2012: the DC, induction and synchronous machine chapters, at exactly this chapter's level.
- N. Mohan, *Electric Machines and Drives: A First Course*, Wiley, 2012: machines taught from the drive's point of view, with space vectors and field-oriented control.
- A. E. Fitzgerald, C. Kingsley and S. D. Umans, *Electric Machinery*, 7th ed., McGraw-Hill, 2014: deeper derivations of the rotating field and machine inductances.

### [22-12 · Power Systems Fundamentals](../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md)

- J. D. Glover, T. J. Overbye and M. S. Sarma, *Power System Analysis and Design*, 6th ed., Cengage, 2017: per unit, lines, power flow, faults and symmetrical components at this chapter's level.
- P. Kundur, *Power System Stability and Control*, McGraw-Hill, 1994: the swing equation, governors and frequency control in depth.
- The NERC reports cited here [8], [9], [10], [11]: real events explained by the people who investigate them.

## [23 · Memory and Storage Technology](../courses/23-memory-and-storage-technology/README.md)

### [23-01 · The Memory Hierarchy and the Memory Wall](../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md)

- B. Jacob, S. W. Ng and D. T. Wang, *Memory Systems: Cache, DRAM, Disk*, Morgan Kaufmann, 2008, ch. 1 (the hierarchy) and the DRAM energy chapters.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., ch. 2 (memory hierarchy design) and ch. 7 (domain-specific architectures).
- V. Sze, Y.-H. Chen, T.-J. Yang and J. S. Emer, *Efficient Processing of Deep Neural Networks*, Morgan & Claypool, 2020: why data movement dominates and how dataflows reduce it. MIT 6.5930 lecture slides [2] follow it.
- O. Mutlu, ETH Zürich *Computer Architecture* lectures on memory systems (freely available online).
- M. Horowitz's ISSCC 2014 plenary [1]: five pages that frame the whole course.

### [23-02 · SRAM Technology](../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md)

- J. M. Rabaey, A. Chandrakasan and B. Nikolić, *Digital Integrated Circuits*, 2nd ed., ch. 12 (memories): the cell, assists and periphery.
- A. Pavlov and M. Sachdev, *CMOS SRAM Circuit Design and Parametric Test in Nano-Scaled Technologies*, Springer, 2008: margins, variation and test.
- E. Seevinck, F. J. List and J. Lohstroh's static-noise-margin paper [6], the origin of the butterfly-curve method used in 19-08.
- The ISSCC SRAM session papers each February and the IEDM platform papers each December, reported in IEEE Spectrum [1], [2].

### [23-03 · DRAM Cells, Arrays and Refresh](../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md)

- B. Keeth, R. J. Baker, B. Johnson and F. Lin, *DRAM Circuit Design: Fundamental and High-Speed Topics*, 2nd ed., Wiley-IEEE Press, 2008: the array, sense amplifiers and peripheral circuits from the designers' side.
- B. Jacob, S. W. Ng and D. T. Wang, *Memory Systems: Cache, DRAM, Disk*, Morgan Kaufmann, 2008: DRAM device organization, timing and controller policies.
- Y. Kim et al. [5] and J. S. Kim et al. [6], the two row-hammer characterization papers, and O. Mutlu's lecture series on memory systems (ETH Zürich, freely online).
- A DRAM data sheet read cover to cover, such as [2]: the command truth table, timing tables and refresh section.

### [23-04 · DRAM Interfaces: DDR, LPDDR and GDDR](../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md)

- B. Jacob, S. W. Ng and D. T. Wang, *Memory Systems: Cache, DRAM, Disk*, Morgan Kaufmann, 2008: DRAM interfaces, signaling and controllers.
- S. H. Hall and H. L. Heck, *Advanced Signal Integrity for High-Speed Digital Designs*, Wiley-IEEE Press, 2009: transmission lines, termination, equalization.
- W. J. Dally and J. W. Poulton, *Digital Systems Engineering*, Cambridge University Press, 1998: signaling conventions and their energy.
- A DRAM data sheet's sections on ODT, write leveling and DBI, such as [2].

### [23-05 · HBM in Depth](../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)

- J. H. Lau, *Chiplet Design and Heterogeneous Integration Packaging*, Springer, 2023: TSVs, interposers, hybrid bonding and HBM packaging.
- The JEDEC HBM3 and HBM4 announcements [1], [2], and the vendor HBM papers presented each year at ISSCC (DRAM session) and in the packaging sessions of ECTC.
- SK hynix's Hot Chips 2026 tutorial on HBM packaging, as summarized in [9].

### [23-06 · NAND Flash and 3D NAND](../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md)

- R. Micheloni, L. Crippa and A. Marelli, *Inside NAND Flash Memories*, Springer, 2010: cells, arrays, ISPP and reliability.
- J. E. Brewer and M. Gill (eds.), *Nonvolatile Memory Technologies with Emphasis on Flash*, Wiley-IEEE Press, 2008.
- The ISSCC NAND session each February, where each maker's newest die is presented [2], [6].

### [23-07 · SSD Controllers and Storage Systems](../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md)

- R. Micheloni, A. Marelli and K. Eshghi, *Inside Solid State Drives (SSDs)*, 2nd ed., Springer, 2018: controller architecture, FTL and ECC.
- P. Desnoyers, "Analytic Modeling of SSD Write Performance," SYSTOR 2012 [1]: the write-amplification models of §3.3.
- Y. Cai et al., "Error Characterization, Mitigation, and Recovery in Flash-Memory-Based Solid-State Drives," *Proc. IEEE*, 2017 [2]: errors, read-retry and LDPC flows.
- M. Bjørling et al., "ZNS: Avoiding the Block Interface Tax for Flash-based SSDs," USENIX ATC 2021 [12].

### [23-08 · Emerging Memories: MRAM, ReRAM, PCM, FeRAM](../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md)

- M. Hellenbrand, I. Teck and J. L. MacManus-Driscoll, "Progress of emerging non-volatile memory technologies in industry," *MRS Communications* 14, 1099–1112 (2024) [1]: the industry state of the four technologies.
- S. Yu (ed.), *Semiconductor Memory Devices and Circuits*, CRC Press, 2022: device physics and circuits for each technology.
- H.-S. P. Wong et al., "Phase change memory," *Proc. IEEE* 98(12), 2010, and "Metal–oxide RRAM," *Proc. IEEE* 100(6), 2012: classic tutorial reviews.

### [23-09 · Compute-in-Memory and Near-Memory Computing](../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md)

- V. Sze, Y.-H. Chen, T.-J. Yang and J. S. Emer, "How to Evaluate Deep Neural Network Processors: TOPS/W (Alone) Considered Harmful," *IEEE Solid-State Circuits Magazine* 12(3), 2020 [8].
- S. K. Gonugondla, C. Sakr, H. Dbouk and N. R. Shanbhag, "Fundamental Limits on Energy-Delay-Accuracy of In-memory Architectures in Inference Applications," arXiv:2012.13645 [10].
- M. Le Gallo et al., "A 64-core mixed-signal in-memory compute chip based on phase-change memory for deep neural network inference," *Nature Electronics*, 2023 (arXiv:2212.02872) [4].
- J. Gómez-Luna et al., "Benchmarking a New Paradigm: An Experimental Analysis of a Real Processing-in-Memory Architecture," arXiv:2105.03814 [3].

## [24 · High-Speed I/O, Signal Integrity and Photonics](../courses/24-high-speed-io-signal-integrity-and-photonics/README.md)

### [24-01 · Signal Integrity Fundamentals](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md)

- E. Bogatin, *Signal and Power Integrity — Simplified*, 3rd ed., chapters on lossy lines, S-parameters, crosstalk and power delivery.
- S. H. Hall and H. L. Heck, *Advanced Signal Integrity for High-Speed Digital Designs*, chapters on coupled lines, conductor and dielectric loss and causal models.
- W. J. Dally and J. W. Poulton, *Digital Systems Engineering*, chapters on transmission lines and noise.
- S. Palermo, Texas A&M ECEN 720 *High-Speed Links* lecture notes (channel modeling).

### [24-02 · Eye Diagrams, Jitter and BER](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md)

- W. J. Dally and J. W. Poulton, *Digital Systems Engineering*, chapters on noise, timing and signalling.
- S. Palermo, Texas A&M ECEN 720 *High-Speed Links* lecture notes: link modeling, statistical BER and jitter.
- E. Bogatin, *Signal and Power Integrity — Simplified*, chapters on eyes and the interconnect's impact on jitter.
- Teledyne LeCroy and Keysight application notes on the dual-Dirac model and Q-scale extrapolation [1], [2].

### [24-03 · SerDes Architecture and Equalization](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md)

- S. Palermo, Texas A&M ECEN 720 *High-Speed Links* lecture notes: transmitter equalization, CTLE, DFE, CDR.
- B. Razavi, *Design of Integrated Circuits for Optical Communications*, 2nd ed., chapters on CDR and equalization.
- W. J. Dally and J. W. Poulton, *Digital Systems Engineering*, chapters on signalling and timing.
- A. Chan Carusone, T. Dickson, S. Palermo, S. Shekhar and M. Mansuri, "Modern Wireline Transceivers," *IEEE JSSC*, 2026, doi:10.1109/JSSC.2025.3642231 (tutorial review, open access; not read here).

### [24-04 · DSP-Based SerDes and FEC](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md)

- S. Palermo, Texas A&M ECEN 720 *High-Speed Links* lecture notes: ADC-based receivers.
- J. G. Proakis and M. Salehi, *Digital Communications*, chapters on MMSE equalization and maximum-likelihood sequence estimation.
- S. Lin and D. J. Costello, *Error Control Coding*, chapters on Reed–Solomon and concatenated codes.
- A. Chan Carusone et al., "Modern Wireline Transceivers," *IEEE JSSC*, 2026 [R-511] (tutorial review; not read here).

### [24-05 · Interconnect Standards: PCIe, CXL and Ethernet](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md)

- W. J. Dally and B. Towles, *Principles and Practices of Interconnection Networks*, chapters on flow control and Clos networks.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, appendix on interconnection networks.
- D. Das Sharma, articles and talks on PCIe 6.0 and 7.0 design (see [R-059], [R-216]).
- T. Hoefler et al., "Ultra Ethernet's Design Principles and Architectural Innovations," arXiv:2508.08906 [R-517].

### [24-06 · Die-to-Die Links, Memory PHYs and Scale-Up Fabrics](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)

- W. J. Dally and J. W. Poulton, *Digital Systems Engineering*, chapters on signalling energy and parallel links.
- D. Das Sharma et al., "High-performance, power-efficient three-dimensional system-in-package designs with universal chiplet interconnect express," *Nature Electronics*, 2024 [R-524].
- The OCP ODSA Bunch of Wires PHY specification draft [R-525].
- NVIDIA's Hot Chips 2024 Blackwell presentation [R-521].

### [24-07 · Photonics Fundamentals](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md)

- G. P. Agrawal, *Fiber-Optic Communication Systems*, chapters on fibers, transmitters, receivers and system design.
- B. E. A. Saleh and M. C. Teich, *Fundamentals of Photonics*, chapters on electro-optics and photodetectors.
- A. Rahim et al., "Taking silicon photonics modulators to a higher performance level," *Advanced Photonics*, 2021 [R-530].
- B. Razavi, *Design of Integrated Circuits for Optical Communications*, chapters on TIAs.

### [24-08 · Silicon Photonics and Optical Transceivers](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md)

- L. Chrostowski and M. Hochberg, *Silicon Photonics Design* (Cambridge, 2015): chapters on waveguides, grating and edge couplers, modulators and detectors.
- G. P. Agrawal, *Fiber-Optic Communication Systems*: chapters on optical transmitters and receivers.
- S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*: band-gap data and photodetectors.
- A. Rahim et al., "Taking silicon photonics modulators to a higher performance level," *Advanced Photonics*, 2021 [R-530].
- V. Stojanović, "A UCIe Optical I/O Retimer Chiplet for AI Scale-up," Hot Chips 2025 [R-540].

### [24-09 · Linear-Drive and Co-Packaged Optics](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md)

- OIF, *External Laser Small Form Factor Pluggable (ELSFP) Implementation Agreement*, OIF-ELSFP-02.0, 2025 [R-548].
- LPO MSA specifications page [R-541].
- S. Ramachandra and F. Rezaie, "Linear Pluggable Optics – An Overview," IEEE EPS, 2026 [R-535].
- Y. Yi and D. Wilkerson, "3D optoelectronics and co-packaged optics: when solving the wrong problems stalls deployment," arXiv:2603.21313 [R-549].
- 03-05 of this curriculum for confidence bounds; any reliability-engineering text for the chi-square method.

## [25 · Semiconductor Fabrication, Packaging, Test and Reliability](../courses/25-fabrication-packaging-test-and-reliability/README.md)

### [25-01 · Process Flow Overview: FEOL, MOL and BEOL](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md)

- J. D. Plummer, M. D. Deal and P. B. Griffin, *Silicon VLSI Technology: Fundamentals, Practice and Modeling*: the CMOS process-flow chapter and the thermal-oxidation chapter (Deal–Grove derivation and coefficient tables).
- B. E. Deal and A. S. Grove, "General Relationship for the Thermal Oxidation of Silicon," *Journal of Applied Physics* 36, 3770 (1965).
- MIT OpenCourseWare 6.152J, *Micro/Nano Processing Technology*: oxidation and process-integration lectures.
- Berkeley EE143 public materials: the process-flow and oxidation units.
- G. S. May and C. J. Spanos, *Fundamentals of Semiconductor Manufacturing and Process Control*: yield, cycle time and fab operations.

### [25-02 · Lithography: DUV, Multipatterning, EUV and High-NA](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md)

- C. A. Mack, *Fundamental Principles of Optical Lithography: The Science of Microfabrication*: imaging theory, depth of focus, resists and stochastics.
- J. D. Plummer, M. D. Deal and P. B. Griffin, *Silicon VLSI Technology*: the lithography chapter.
- H. J. Levinson, *Principles of Lithography*: industrial practice, overlay and multipatterning.
- MIT OpenCourseWare 6.152J and Berkeley EE143: lithography lectures.
- ASML's product pages for current scanner specifications [R-560] to [R-562].

### [25-03 · Deposition, Etch, CMP, Implant and Metrology](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md)

- J. D. Plummer, M. D. Deal and P. B. Griffin, *Silicon VLSI Technology*: chapters on dopant diffusion, ion implantation, thin-film deposition and etching (diffusivity tables, range tables, CVD regimes).
- G. S. May and C. J. Spanos, *Fundamentals of Semiconductor Manufacturing and Process Control*: metrology, statistical process control and gauge studies.
- M. A. Lieberman and A. J. Lichtenberg, *Principles of Plasma Discharges and Materials Processing*: plasma sheaths and etching.
- MIT OpenCourseWare 6.152J and Berkeley EE143: deposition, etch and implantation lectures.

### [25-04 · Yield Models and Die Cost](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md)

- G. S. May and C. J. Spanos, *Fundamentals of Semiconductor Manufacturing and Process Control*: the yield chapter (Poisson, Murphy, Seeds and negative-binomial models, critical area).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*: the section on the cost of an integrated circuit.
- C. H. Stapper's papers on defect clustering and the negative-binomial yield model (IBM Journal of Research and Development).
- S. M. Khan and A. Mann, "AI Chips: What They Are and Why They Matter," CSET (2020): a transparent wafer-cost model [R-576].

### [25-05 · Foundries, PDKs and Specialty Processes](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md)

- N. H. E. Weste and D. M. Harris, *CMOS VLSI Design*: the chapters on design rules, process variation and corners.
- J.-P. Colinge, *Silicon-on-Insulator Technology: Materials to VLSI*: FD-SOI devices and back-gate coupling (the Lim–Fossum model).
- Europractice's published MPW schedules and SkyWater's open SKY130 PDK documentation: what a PDK and a shuttle look like in practice [R-581].
- TSMC's annual Form 20-F: process portfolio and node mix [R-579].

### [25-06 · Packaging I: Wire Bond, Flip-Chip, Substrates, SiP and PoP](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md)

- R. R. Tummala, *Fundamentals of Microsystems Packaging*: package functions, substrates and thermomechanical reliability.
- J. H. Lau, *Flip Chip Technologies* and later books on fan-out and chiplet packaging.
- W. Engelmaier's solder-joint fatigue papers: the strain and Coffin–Manson models used in industry.
- IEEE Electronic Components and Technology Conference (ECTC) proceedings: the main venue for packaging results.

### [25-07 · Packaging II: 2.5D, 3D, Hybrid Bonding and Chiplets](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md)

- J. H. Lau, *Chiplet Design and Heterogeneous Integration Packaging* (Springer, 2023): chapters on 2.5D, bridges and hybrid bonding.
- R. Tummala (ed.), *Fundamentals of Device and Systems Packaging*, 2nd ed. (McGraw-Hill, 2019): the chapters on 3D and heterogeneous integration.
- Q.-Y. Tong and U. Gösele, *Semiconductor Wafer Bonding: Science and Technology* (Wiley, 1999): the surface science of direct bonding and why particles create voids.
- The IEEE Electronic Components and Technology Conference (ECTC) proceedings, for current hybrid-bonding and bridge results.

### [25-08 · Thermal Engineering](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md)

- T. L. Bergman, A. S. Lavine, F. P. Incropera and D. P. DeWitt, *Fundamentals of Heat and Mass Transfer*, 8th ed. (Wiley, 2017): chapter 3 (conduction and extended surfaces), chapter 4 (two-dimensional conduction and shape factors) and chapter 8 (internal flow).
- M. M. Yovanovich and E. E. Marotta, "Thermal spreading and contact resistances," in *Heat Transfer Handbook* (Wiley, 2003): spreading-resistance solutions for disks and rectangles.
- Y. Cengel and A. Ghajar, *Heat and Mass Transfer: Fundamentals and Applications* (McGraw-Hill): a gentler second text with electronics-cooling examples.

### [25-09 · Reliability Physics](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md)

- J. W. McPherson, *Reliability Physics and Engineering: Time-to-Failure Modeling*, 3rd ed. (Springer, 2019): acceleration models for every mechanism in this chapter.
- J. R. Black, "Electromigration — a brief survey and some recent results," *IEEE Trans. Electron Devices* 16(4), 1969; I. A. Blech, "Electromigration in thin aluminum films on titanium nitride," *J. Appl. Phys.* 47, 1976.
- E. Y. Wu and J. H. Stathis' review chapters on gate-dielectric breakdown, and T. Grasser (ed.), *Bias Temperature Instability for Devices and Circuits* (Springer, 2014).
- A. Amerasekera and C. Duvvury, *ESD in Silicon Integrated Circuits*, 2nd ed. (Wiley, 2002).

### [25-10 · Qualification and Functional Safety](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md)

- AEC, *AEC-Q100 Rev J: Failure Mechanism Based Stress Test Qualification for Integrated Circuits in Automotive Applications* (2023): the stress tables and grade definitions.
- ISO 26262-5:2018 (hardware) and ISO 26262-10:2018 (guidelines): metric definitions and worked examples.
- Vendor safety manuals (for example, those of automotive MCU families) for real FMEDA structures.
- J. W. McPherson, *Reliability Physics and Engineering* (Springer): the acceleration models behind qualification.

### [25-11 · Test: ATE, Wafer Sort, Burn-In and Binning](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md)

- M. L. Bushnell and V. D. Agrawal, *Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits* (Springer, 2000): test economics, ATE and parametric test.
- W. Kuo and Y. Kuo, "Facing the headaches of early failures: a state-of-the-art review of burn-in decisions," *Proc. IEEE* 71(11), 1983: the classic treatment of burn-in.
- SemiEngineering's test coverage (2020–2026) for the changing economics of test.

### [25-12 · Post-Silicon Validation and Bring-Up](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md)

- S. Mitra, S. A. Seshia and N. Nicolici, "Post-Silicon Validation Opportunities, Challenges and Recent Advances," DAC 2010.
- P. Mishra and F. Farahmandi (eds.), *Post-Silicon Validation and Debug* (Springer, 2019).
- A. L. Goel and K. Okumoto, "Time-dependent error-detection rate model for software reliability and other performance measures," *IEEE Trans. Reliability* R-28(3), pp. 206–211, 1979: the reliability-growth model used here.
- The Siemens EDA / Wilson Research Group functional verification study series (2024 and 2026 editions).

## [26 · Engineering Design and Professional Practice](../courses/26-engineering-design-and-professional-practice/README.md)

### [26-01 · Requirements, Specifications and the Design Process](../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md)

- NASA, *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2 (free PDF): chapters on technical requirements definition and product verification and validation, and Appendix C, "How to Write a Good Requirement—Checklist."
- Ulrich and Eppinger, *Product Design and Development*: the chapters on identifying customer needs, product specifications and concept selection (decision matrices).
- Royce, "Managing the Development of Large Software Systems" (1970), for what the waterfall's supposed originator actually recommended; Boehm, "A Spiral Model of Software Development and Enhancement" (1988).
- MIT OpenCourseWare, product-development and senior-design course materials (for example 2.009) for worked requirement and selection exercises.

### [26-02 · Design Reviews, Documentation and Standards Bodies](../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md)

- NASA, *Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2 (free PDF): technical reviews, peer reviews and configuration management.
- IEEE SA Standards Board Bylaws (clause 6, patent policy) and Operations Manual (balloting), both free on the IEEE SA website.
- ETSI IPR Policy (Annex 6 of the ETSI Rules of Procedure), free.
- For capture–recapture in inspections, the software-engineering literature on estimating remaining defects from inspection data (search "capture-recapture software inspection").

### [26-03 · Engineering Economics I: NRE, Die Cost, ASP and Gross Margin](../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md)

- Newnan, Eschenbach and Lavelle, *Engineering Economic Analysis*: interest and equivalence, present and annual worth, rate of return, depreciation (the FE exam's economics follows this material closely).
- NCEES, *FE Reference Handbook*, engineering economics section: the factor table (including the gradient factors), benefit–cost ratio, capitalized cost and MACRS depreciation tables used on the exam.
- MIT OpenCourseWare, 15.401 *Finance Theory I* (video lectures): present value, capital budgeting and the NPV rule, from a finance perspective.
- 25-04 and its lab for the die-cost model this chapter builds on.

### [26-04 · Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant](../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md)

- Newnan, Eschenbach and Lavelle, *Engineering Economic Analysis*: incremental analysis of alternatives, break-even and sensitivity, and probabilistic risk with decision trees.
- L. Trigeorgis, *Real Options: Managerial Flexibility and Strategy in Resource Allocation* (MIT Press, 1996), for the option view of staged decisions.
- S. Naffziger et al., "Pioneering Chiplet Technology and Design for the AMD EPYC and Ryzen Processor Families", ISCA 2021 (DOI 10.1109/ISCA52012.2021.00014), for a vendor's chiplet cost analysis [R-360].
- 25-07 and its lab for the single-product chiplet model; 26-03's lab for the time-value tools reused here.

### [26-05 · Schedule and Risk: Why Respins Happen](../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md)

- F. S. Hillier and G. J. Lieberman, *Introduction to Operations Research*: the project-management chapter on PERT/CPM, three-point estimates and the probability of meeting a deadline.
- Newnan, Eschenbach and Lavelle, *Engineering Economic Analysis*: probabilistic risk analysis and expected value.
- The Wilson Research Group functional verification studies (Siemens Verification Horizons blog), for the survey data and its caveats [R-018, R-321].
- 19-13 and 25-12 for the verification and bring-up practice behind the models here.

### [26-06 · Engineering Team Structures and Sizing](../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md)

- F. P. Brooks, *The Mythical Man-Month: Essays on Software Engineering* (anniversary edition, 1995): the essays on team size, communication and adding people to late projects.
- M. E. Conway, "How Do Committees Invent?", *Datamation*, April 1968: the original statement of Conway's law.
- F. S. Hillier and G. J. Lieberman, *Introduction to Operations Research*: the newsvendor model in the inventory chapter.
- 28-07 for how these questions are asked in a diligence setting.

### [26-07 · Engineering Ethics and Professional Responsibility](../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md)

- NSPE, *Code of Ethics for Engineers* (rev. July 2019), with the NSPE Board of Ethical Review's case collection for worked applications.
- N. G. Leveson and C. S. Turner, "An Investigation of the Therac-25 Accidents," *IEEE Computer*, July 1993 [R-656].
- *Report of the Presidential Commission on the Space Shuttle Challenger Accident* (1986), chapters IV and V [R-657].
- NCEES, *FE Reference Handbook*, ethics section, and the FE specification [R-655].
- The Bureau of Industry and Security's pages on advanced computing rules, read with a compliance professional [R-659].

## [27 · System Architectures (Case-Study Course)](../courses/27-system-architectures/README.md)

### [27-01 · Method: Analyzing a System End to End](../courses/27-system-architectures/chapters/27-01-system-analysis-method.md)

- Hennessy and Patterson, *Computer Architecture: A Quantitative Approach*: the chapters on quantitative design principles (Amdahl's law, power and energy) and on domain-specific architectures (the roofline in practice).
- S. Williams, A. Waterman and D. Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures," *Communications of the ACM*, 2009 (the original roofline paper, 14-15).
- 22-08 and its lab for PMIC power trees, and 25-08 for thermal resistance networks.
- Lecture videos: MIT OpenCourseWare 6.004 *Computation Structures* for the processor and memory-system basics behind the bottleneck models, and Onur Mutlu's *Computer Architecture* lectures at ETH Zürich (recorded and public) for quantitative design and the memory system.

### [27-02 · The Smartphone SoC](../courses/27-system-architectures/chapters/27-02-smartphone-soc.md)

- Hennessy and Patterson, *Computer Architecture: A Quantitative Approach*: the sections on energy efficiency, heterogeneous and domain-specific architectures.
- Arm's public documentation of heterogeneous (big.LITTLE and DynamIQ) CPU clusters and energy-aware scheduling, for how operating systems use the crossover.
- Apple, "Apple Intelligence Foundation Language Models Tech Report 2025" (arXiv 2507.13575) for a vendor's account of fitting a model to a phone's memory and bandwidth [R-668].
- Lecture videos: Onur Mutlu's *Computer Architecture* lectures at ETH Zürich (recorded and public) on heterogeneous multicore and the memory system, and MIT OpenCourseWare 6.004 *Computation Structures* for the basics.

### [27-03 · Wearables I: The Smartwatch](../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md)

- Chapter 18-09 (ultra-low-power design) and 22-08 (PMICs) of this curriculum for the circuit-level derivations this chapter applies.
- A photometry chapter of any optics or display-technology text for luminance, luminous intensity and Lambertian emission (look for the derivation of $\Phi = \pi L A$).
- The Bluetooth Core Specification, Vol 6 (Low Energy Controller), Part B (Link Layer): packet format, connection events and window widening; vendor application notes on BLE power estimation (Nordic's online power profiler, TI and Silicon Labs app notes) give measured event-current profiles.
- 3GPP TS 36.304 and TS 38.304 (idle-mode procedures) for DRX and eDRX paging.
- Teardown reports (iFixit, TechInsights) of recent watches to see the battery, PMIC and SoC partitioning in hardware.
- Lecture videos: the HarvardX *Tiny Machine Learning (TinyML)* series on edX for always-on sensing on microcontrollers, and MIT OpenCourseWare 6.004 *Computation Structures* for the processor side of the power budget.

### [27-04 · Wearables II: Earbuds and Smart Glasses / XR](../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md)

- An acoustics or audio-engineering text's chapter on active noise control (for example, the feedforward and feedback ANC structures and the filtered-x LMS algorithm) for the adaptive filters this chapter treats as ideal.
- Vendor application notes on LE Audio and LC3 (Bluetooth SoC vendors publish power estimates for isochronous streams) and the LC3 specification for the codec's frame structure.
- Survey papers on mixed-reality rendering (foveated rendering, reprojection, split and remote rendering) in ACM SIGGRAPH and IEEE VR proceedings, and on waveguide displays in optics journals.
- Chapter 25-08 of this curriculum for convection and radiation coefficients behind $hA\Delta T$.
- Lecture videos: MIT OpenCourseWare RES.6-008 *Digital Signal Processing* (Alan Oppenheim's recorded lectures) for the filtering and delay ideas behind ANC.

### [27-05 · The PC SoC](../courses/27-system-architectures/chapters/27-05-pc-soc.md)

- Hennessy and Patterson, *Computer Architecture: A Quantitative Approach*, the chapters on memory hierarchy and domain-specific architectures.
- Vendor architecture presentations at Hot Chips and ISSCC (client SoCs are presented most years) for tile partitioning, power management and memory systems.
- Operating-system documentation on idle states and modern standby (for example, Microsoft's hardware design guidance) for how software decides residency.
- Chapters 25-07 and 26-04 of this curriculum for the packaging and economic side of chiplets.
- Lecture videos: Onur Mutlu's *Computer Architecture* lectures at ETH Zürich (recorded and public) on the memory system and heterogeneous processors.

### [27-06 · Automotive E/E Architecture and ADAS Compute](../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md)

- R. I. Davis, A. Burns, R. J. Bril and J. J. Lukkien, "Controller Area Network (CAN) schedulability analysis: Refuted, revisited and revised", *Real-Time Systems* 35 (2007): the standard reference for CAN response-time analysis and the worst-case stuffing bound.
- ISO 26262 (road vehicles, functional safety), parts 1, 5 and 9, for ASIL determination and hardware metrics; ISO 21448 (SOTIF) for performance limitations of sensing and perception.
- SAE J3016 for the levels of driving automation.
- Vendor technical documentation for central compute platforms and zonal controllers, and the IEEE 802.3 automotive Ethernet amendments (802.3bw, 802.3bp, 802.3cg, 802.3ch).
- Lecture videos: we have not verified an open university lecture series on vehicle E/E architecture; CiA's "CAN knowledge" pages [R-689] are a free primer on CAN, CAN FD and CAN XL, and 18-07's references cover response-time analysis.

### [27-07 · The AI Datacenter Server and Rack](../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md)

- L. A. Barroso, U. Hölzle and P. Ranganathan, *The Datacenter as a Computer: Designing Warehouse-Scale Machines*, 3rd ed. (Morgan & Claypool, 2018): power, cooling, efficiency and cost at datacenter scale.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed. (2017), chapters 6 (warehouse-scale computers) and 7 (domain-specific architectures, including the TPU).
- P. Patarasuk and X. Yuan, "Bandwidth optimal all-reduce algorithms for clusters of workstations", *Journal of Parallel and Distributed Computing* 69 (2009): the ring all-reduce and its bandwidth bound.
- J. W. Young, "A first order approximation to the optimum checkpoint interval", *Communications of the ACM* 17 (1974); J. T. Daly, "A higher order estimate of the optimum checkpoint interval for restart dumps", *Future Generation Computer Systems* 22 (2006).
- J. Kaplan et al., "Scaling Laws for Neural Language Models", arXiv:2001.08361 (2020): the $6N$ FLOPs-per-token rule.
- D. Narayanan et al., "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM", SC21 (arXiv:2104.04473): tensor, pipeline and data parallelism combined, and pipeline schedules.
- The Llama 3 paper's infrastructure section [R-694]: a rare public account of a 16K-GPU training system, its parallelism and its failures.
- Lecture videos: MIT 6.5940 *TinyML and Efficient Deep Learning Computing* (Song Han; recorded lectures are public) for its lectures on distributed training and efficient inference, and Onur Mutlu's *Computer Architecture* lectures at ETH Zürich for the memory-system side.

### [27-08 · Edge AI and IoT](../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md)

- C. Banbury et al., "MLPerf Tiny Benchmark", arXiv:2106.07597 (2021) [R-696]: the benchmark tasks, reference models and energy measurement.
- P. Warden and D. Situnayake, *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers* (O'Reilly, 2019): a practical introduction to models on microcontrollers.
- A. G. Howard et al., "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications", arXiv:1704.04861 (2017): depthwise-separable convolutions and their cost.
- Semtech SX1276/77/78/79 data sheet, §4.1 (LoRa modem, time on air) [R-697]; the LoRa Alliance's LoRaWAN Regional Parameters (RP002) for each region's channels and limits.
- Arm's Ethos-U and Cortex-M documentation, and the PSA Certified and Cyber Resilience Act materials cited in 18-11 [R-312].
- Lecture videos: the HarvardX *Tiny Machine Learning (TinyML)* series on edX, and MIT 6.5940 *TinyML and Efficient Deep Learning Computing* (Song Han; recorded lectures are public).

## [28 · Technical Diligence and Engineering Leadership Fluency](../courses/28-technical-diligence-and-leadership-fluency/README.md)

### [28-01 · A Framework for Evaluating a Chip Company's Technology](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md)

- R. T. Clemen and T. Reilly, *Making Hard Decisions with DecisionTools*: the chapters on multi-attribute decisions (swing weights, trade-offs) and on the value of information.
- R. A. Howard, "Information Value Theory", *IEEE Transactions on Systems Science and Cybernetics* SSC-2 (1966): the origin of the value of information in decision analysis.
- D. Kahneman, *Thinking, Fast and Slow* (2011): base-rate neglect and the halo effect, the two biases this chapter's tools are built to resist.
- Lecture videos: MIT OpenCourseWare 6.041SC *Probabilistic Systems Analysis and Applied Probability* (John Tsitsiklis's recorded lectures) for Bayes' rule and inference.

### [28-02 · Validating Claims: TOPS/W, Benchmarks, Tapeout Status](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md)

- V. Sze, Y.-H. Chen, T.-J. Yang and J. S. Emer, "How to Evaluate Deep Neural Network Processors: TOPS/W (Alone) Considered Harmful," *IEEE Solid-State Circuits Magazine* 12(3), 2020 [R-492].
- M. Horowitz, "Computing's energy problem (and what we can do about it)," ISSCC 2014 [R-208]: the reference table of energy per operation and per access.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*: chapter 1 on measuring, reporting and summarizing performance (the geometric mean and its pitfalls).
- MLCommons inference and training rules (MLPerf) and the SPEC CPU run and reporting rules [R-223, R-224].
- Lecture videos: MIT 6.5930 *Hardware Architectures for Deep Learning* (Sze and Emer) course materials, from which [R-458]'s energy table is reproduced, and Onur Mutlu's *Computer Architecture* lectures at ETH Zürich for performance evaluation.

### [28-03 · Maturity Scales for Silicon](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md)

- A. L. Goel and K. Okumoto, "Time-Dependent Error-Detection Rate Model for Software Reliability and Other Performance Measures," *IEEE Transactions on Reliability* R-28(3), 206–211, 1979 (doi:10.1109/TR.1979.5220566).
- JEDEC JESD47 (stress-test-driven qualification), JESD85 (failure-rate calculation methods) and JEP122 (failure mechanisms and activation energies) [R-609, R-610, R-611]; AEC-Q100 for automotive [R-612].
- NASA's technology readiness levels page [R-701] and the NASA Systems Engineering Handbook (Rev 2) [R-626].
- Lecture videos: MIT OpenCourseWare 6.041SC *Probabilistic Systems Analysis and Applied Probability* (John Tsitsiklis's recorded lectures) for Poisson processes and confidence bounds.

### [28-04 · Domain Question Banks I: Digital/CPU, AI Accelerators, Memory, Interconnect and Optics](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md)

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*: chapter 1 (performance, power and their measurement) and the chapters on memory hierarchy and domain-specific architectures.
- The primary sources behind each bank: JEDEC's HBM4 standard [R-520]; the ISSCC and VLSI SerDes papers of [R-509]; UCIe's key-metric targets [R-524]; OIF's ELSFP agreement [R-548].
- Lecture videos: Onur Mutlu's *Computer Architecture* lectures at ETH Zürich (recorded and public) on memory systems and accelerators.

### [28-05 · Domain Question Banks II: Analog/Mixed-Signal, RF, Power, Packaging, Embedded](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md)

- D. A. Johns, K. Martin and T. Chan Carusone, *Analog Integrated Circuit Design*: the chapters on data-converter fundamentals and performance metrics.
- B. Razavi, *RF Microelectronics*: the chapters on power amplifiers (efficiency, back-off, Doherty) and transceiver specifications.
- R. W. Erickson and D. Maksimović, *Fundamentals of Power Electronics*: the chapters on converter losses and efficiency.
- B. Murmann's ADC performance survey (public on GitHub) [R-336]: plot your own claims against it.
- Lecture videos: Ali Hajimiri's Caltech analog circuit lectures and Tony Chan Carusone's data-converter lectures (both recorded and public).

### [28-06 · Red Flags and Green Flags](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md)

- D. G. Altman and J. M. Bland, "Diagnostic tests 1: sensitivity and specificity," *BMJ* 308:1552 (1994), and J. J. Deeks and D. G. Altman, "Diagnostic tests 4: likelihood ratios," *BMJ* 329:168–169 (2004): short statistics notes on the diagnostic-test algebra this chapter applies to diligence flags.
- D. Kahneman, *Thinking, Fast and Slow*: the chapters on base-rate neglect and the narrative fallacy.
- The Wilson Research Group functional verification studies (Siemens EDA, public reports and blog series) [R-621], [R-645].
- Lecture videos: MIT OpenCourseWare 6.041/6.431 *Probabilistic Systems Analysis and Applied Probability* (recorded and public), the lectures on Bayes' rule and the binomial distribution.

### [28-07 · Evaluating Engineering Teams](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md)

- A. Gelman et al., *Bayesian Data Analysis*: the chapter on single-parameter models (the beta-binomial model and conjugate priors).
- F. P. Brooks, *The Mythical Man-Month* (anniversary edition), chapters 2 and 3 [R-650].
- B. Flyvbjerg's published work on reference-class forecasting in large projects (journal articles are public).
- Lecture videos: MIT OpenCourseWare 6.041/6.431 *Probabilistic Systems Analysis and Applied Probability* (recorded and public), the lectures on Bayesian statistical inference.

### [28-08 · Post-Acquisition Integration Risk](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md)

- R. A. Brealey, S. C. Myers and F. Allen, *Principles of Corporate Finance*: the chapters on mergers and on real options.
- Company filings and releases cited here [R-204], [R-547], [R-639], for how licensing and earn-out terms are described in practice.
- The Federal Register texts of the US advanced-computing export rules [R-659] (read the current rule, not a summary).
- Lecture videos: MIT OpenCourseWare 15.401 *Finance Theory I* (recorded and public), the lectures on present value and capital budgeting.

### [28-09 · The Business ↔ Engineering Translation Table](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md)

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*: the section on the cost of an integrated circuit.
- R. A. Brealey, S. C. Myers and F. Allen, *Principles of Corporate Finance*: the chapters on project analysis and sensitivity analysis.
- LBNL's United States Data Center Energy Usage Report (public) [R-452].
- Lecture videos: MIT OpenCourseWare 15.401 *Finance Theory I* (recorded and public), lectures on capital budgeting.

### [28-10 · Conversation Scenarios](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md)

- D. Kahneman, *Thinking, Fast and Slow*: anchoring, the narrative fallacy and base-rate neglect.
- P. E. Tetlock and D. Gardner, *Superforecasting*: calibration, Brier scores and updating.
- Your own debrief sheets: after each real meeting, compare the ratios you wrote with what the follow-up artifacts showed.
- Lecture videos: MIT OpenCourseWare 6.041/6.431 *Probabilistic Systems Analysis and Applied Probability* (recorded and public), the lectures on Bayesian inference, for the debrief arithmetic.

<!-- END GENERATED -->
