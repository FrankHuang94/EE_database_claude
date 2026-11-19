<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 06 · Circuit Analysis I (DC)

The foundation of circuit theory: elements, Kirchhoff's laws, systematic nodal and mesh analysis, network theorems, and the ideal op-amp, all with DC sources so that the methods are learned before time and frequency enter.

| | |
|---|---|
| **Term** | 2 |
| **Study hours** | ≈ 86 |
| **University equivalents** | Circuits I (sophomore); MIT 6.002 (first half); Berkeley EE16A (circuits portion) |
| **Textbook alignment** | Nilsson & Riedel, *Electric Circuits*; Alexander & Sadiku, *Fundamentals of Electric Circuits*; Agarwal & Lang, *Foundations of Analog and Digital Electronic Circuits* (MIT 6.002 text) |
| **Free courses** | MIT OCW 6.002 Circuits and Electronics; Berkeley EE16A |
| **Prerequisites** | [01 · Calculus for Engineers](../01-calculus-for-engineers/README.md), [02 · Complex Numbers, Differential Equations and Linear Algebra](../02-complex-numbers-des-and-linear-algebra/README.md), [04 · Physics for EE](../04-physics-for-ee/README.md) |
| **FE areas** | Circuit Analysis (DC and AC Steady State) |

## Learning objectives

1. Apply KVL, KCL and element laws with the passive sign convention to any lumped circuit.
2. Solve circuits with independent and dependent sources by nodal and mesh analysis, setting them up as matrix equations.
3. Use superposition, source transformation and Thevenin/Norton equivalents to simplify circuits.
4. Find the load that receives maximum power, and the efficiency at that point.
5. Analyze ideal op-amp circuits (inverting, non-inverting, summing, difference, buffer).

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [06-01 · Charge, Current, Voltage, Power and the Lumped Circuit Abstraction](chapters/06-01-charge-current-voltage-power.md) | 6 | ✅ verified | [problems](problems/06-01-problems.md) · [solutions](solutions/06-01-solutions.md) · [lab](labs/06-01-lab/README.md) · [verify](verify/verify_06_01.py) |
| [06-02 · Circuit Elements and Ohm's Law](chapters/06-02-circuit-elements-and-ohms-law.md) | 6 | ✅ verified | [problems](problems/06-02-problems.md) · [solutions](solutions/06-02-solutions.md) · [lab](labs/06-02-lab/README.md) · [verify](verify/verify_06_02.py) |
| [06-03 · Kirchhoff's Laws, Series/Parallel and Dividers](chapters/06-03-kirchhoffs-laws.md) | 8 | ✅ verified | [problems](problems/06-03-problems.md) · [solutions](solutions/06-03-solutions.md) · [lab](labs/06-03-lab/README.md) · [verify](verify/verify_06_03.py) |
| [06-04 · Nodal Analysis](chapters/06-04-nodal-analysis.md) | 10 | ✅ verified | [problems](problems/06-04-problems.md) · [solutions](solutions/06-04-solutions.md) · [lab](labs/06-04-lab/README.md) · [verify](verify/verify_06_04.py) |
| [06-05 · Mesh Analysis](chapters/06-05-mesh-analysis.md) | 8 | ✅ verified | [problems](problems/06-05-problems.md) · [solutions](solutions/06-05-solutions.md) · [lab](labs/06-05-lab/README.md) · [verify](verify/verify_06_05.py) |
| [06-06 · Dependent Sources](chapters/06-06-dependent-sources.md) | 8 | ✅ verified | [problems](problems/06-06-problems.md) · [solutions](solutions/06-06-solutions.md) · [lab](labs/06-06-lab/README.md) · [verify](verify/verify_06_06.py) |
| [06-07 · Linearity and Superposition](chapters/06-07-linearity-and-superposition.md) | 6 | ✅ verified | [problems](problems/06-07-problems.md) · [solutions](solutions/06-07-solutions.md) · [lab](labs/06-07-lab/README.md) · [verify](verify/verify_06_07.py) |
| [06-08 · Thevenin and Norton Equivalents](chapters/06-08-thevenin-and-norton.md) | 10 | ✅ verified | [problems](problems/06-08-problems.md) · [solutions](solutions/06-08-solutions.md) · [lab](labs/06-08-lab/README.md) · [verify](verify/verify_06_08.py) |
| [06-09 · Maximum Power Transfer](chapters/06-09-maximum-power-transfer.md) | 4 | ✅ verified | [problems](problems/06-09-problems.md) · [solutions](solutions/06-09-solutions.md) · [lab](labs/06-09-lab/README.md) · [verify](verify/verify_06_09.py) |
| [06-10 · The Ideal Op-Amp](chapters/06-10-ideal-op-amp.md) | 10 | ✅ verified | [problems](problems/06-10-problems.md) · [solutions](solutions/06-10-solutions.md) · [lab](labs/06-10-lab/README.md) · [verify](verify/verify_06_10.py) |
| [06-11 · Practical DC Circuits and Measurement](chapters/06-11-practical-dc-circuits-and-measurement.md) | 4 | ✅ verified | [problems](problems/06-11-problems.md) · [solutions](solutions/06-11-solutions.md) · [lab](labs/06-11-lab/README.md) · [verify](verify/verify_06_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/06-circuit-analysis-1-dc.csv) · [Equation sheet](../../reference/equation-sheets/06-circuit-analysis-1-dc.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 06 opens Term 2 and is planned at about 86 hours (the chapters' own estimates add to 79, before the exam). It is the foundation of everything electrical that follows: every later circuit, from a transistor amplifier to a power converter to a high-speed link, is analyzed with the laws and methods built here, first with DC so that the methods are learned before time and frequency enter (Course 07). The eleven chapters fall into four blocks. 06-01 to 06-03 set up the variables, the elements and Kirchhoff's laws, with dividers and bridges. 06-04 to 06-06 are the systematic methods: nodal analysis (what every simulator does), mesh analysis, and dependent sources, the bridge to transistor and op-amp models. 06-07 to 06-09 are the network theorems: superposition and its use for tolerance and error budgets, Thévenin and Norton equivalents, and maximum power transfer. 06-10 and 06-11 apply them: the ideal op-amp, and measurement with real instruments and real wires. Work at least the [A] and [B] problems of every chapter (146 problems in all). Every lab pairs a notebook with an ngspice netlist whose results are checked against the answer keys, so you can predict, then simulate, every circuit.

**What to master cold.** The passive sign convention and Tellegen's power check (06-01); $R = \rho L/A$, sheet resistance and copper's +0.39%/°C (06-02); dividers, loading and the bridge (06-03); writing $\mathbf{G}\mathbf{v} = \mathbf{i}$ by inspection, supernodes and MNA (06-04); mesh equations and supermeshes, and when to choose them (06-05); the four dependent sources and the test-source method (06-06); superposition, the fact that power does not superpose, source transformation, and worst-case versus RSS budgets (06-07); finding $V_{th}$, $R_{th}$ three ways and using them for loading (06-08); $R_L = R_{th}$, $4\eta(1 - \eta)$ and when not to match (06-09); the two ideal op-amp rules, the standard configurations, noise gain, CMRR and the DC error budget (06-10); loading, burden, accuracy specifications, Kelvin sensing and remote sensing (06-11). The [equation sheet](../../reference/equation-sheets/06-circuit-analysis-1-dc.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions, takes 180 minutes, and allows a calculator and the equation sheet but not Python or a simulator. Aim for at least 70%. Question 15 is a short-answer diligence question about four measurement and precision claims. This course maps directly onto the FE Electrical and Computer exam's circuit-analysis area, so its problems double as FE practice. The [flashcards](../../flashcards/06-circuit-analysis-1-dc.csv) (122 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Most claims about chips and systems eventually reduce to a circuit: where the power goes ($I^2R$ in a rack's busbar, the drop between a regulator and a die), what limits a measurement (a shunt's layout, an op-amp's offset, a meter's loading), and what an equivalent source can deliver. The habit this course builds, of reducing a system to a Thévenin equivalent and an error budget and checking the power balance, is the fastest way to test whether a number in a pitch is physically possible. The Marketing vs Reality sections practice it on resistors, simulators, PoE, 50 Ω, op-amps and meters.

**Perishable content.** The circuit theory is timeless. The dated facts are in the practitioner sections, logged mainly as [R-098](../../reference/research-log.md#r-098--usb-power-delivery-rack-power-distribution-and-ai-rack-power) to [R-109](../../reference/research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts) in the research log. The ones most likely to move are AI rack power and datacenter power distribution ([R-098](../../reference/research-log.md#r-098--usb-power-delivery-rack-power-distribution-and-ai-rack-power), [R-099](../../reference/research-log.md#r-099--data-centre-electricity-use-iea)), simulator capacity claims ([R-103](../../reference/research-log.md#r-103--modified-nodal-analysis-and-simulator-capacity)), Power over Ethernet ([R-105](../../reference/research-log.md#r-105--thevenin-and-norton-history-and-power-over-ethernet)), analog companies' revenues ([R-107](../../reference/research-log.md#r-107--op-amp-datasheets-and-analog-revenue)) and instrument specifications ([R-108](../../reference/research-log.md#r-108--digital-multimeter-specifications)). Check those entries once a year.
