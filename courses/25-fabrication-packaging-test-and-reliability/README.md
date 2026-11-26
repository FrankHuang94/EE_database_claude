<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 25 · Semiconductor Fabrication, Packaging, Test and Reliability

How chips are made, packaged, tested and qualified: process flow, lithography through High-NA EUV, deposition/etch/CMP/implant/metrology, yield and die cost, foundries and PDKs, advanced packaging and chiplets, thermal engineering, reliability physics, qualification standards, test and post-silicon validation.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 83 |
| **University equivalents** | Microfabrication / IC Process Technology + Packaging and Reliability (senior elective); Berkeley EE143; MIT 6.152J |
| **Textbook alignment** | Plummer, Deal & Griffin, *Silicon VLSI Technology*; May & Spanos, *Fundamentals of Semiconductor Manufacturing and Process Control*; Tummala, *Fundamentals of Microsystems Packaging*; Bushnell & Agrawal, *Essentials of Electronic Testing* |
| **Free courses** | MIT OCW 6.152J Micro/Nano Processing Technology; Berkeley EE143 (public materials) |
| **Prerequisites** | [09 · Semiconductor Devices](../09-semiconductor-devices/README.md), [19 · Digital VLSI Design](../19-digital-vlsi-design/README.md) |
| **FE areas** | Properties of Electrical Materials, Ethics and Professional Practice |
| **Deeper** | Companion repo(s): semiconductor capital equipment |

## Learning objectives

1. Describe a CMOS process flow (FEOL, MOL, BEOL) and the role of each unit process.
2. Explain lithography resolution limits and the economics of multipatterning, EUV and High-NA EUV.
3. Compute die cost from wafer cost, die area and yield models.
4. Compare packaging options (flip-chip, 2.5D, 3D, hybrid bonding, chiplets) and their thermal and cost implications.
5. Explain reliability mechanisms (EM, TDDB, BTI, HCI, ESD, latch-up) and qualification standards.
6. Describe the test flow (wafer sort, final test, burn-in, binning) and post-silicon validation.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [25-01 · Process Flow Overview: FEOL, MOL and BEOL](chapters/25-01-process-flow-overview.md) | 7 | 🏁 reviewed | [problems](problems/25-01-problems.md) · [solutions](solutions/25-01-solutions.md) · [lab](labs/25-01-lab/README.md) · [verify](verify/verify_25_01.py) |
| [25-02 · Lithography: DUV, Multipatterning, EUV and High-NA](chapters/25-02-lithography.md) | 8 | 🏁 reviewed | [problems](problems/25-02-problems.md) · [solutions](solutions/25-02-solutions.md) · [lab](labs/25-02-lab/README.md) · [verify](verify/verify_25_02.py) |
| [25-03 · Deposition, Etch, CMP, Implant and Metrology](chapters/25-03-deposition-etch-cmp-implant-metrology.md) | 8 | 🏁 reviewed | [problems](problems/25-03-problems.md) · [solutions](solutions/25-03-solutions.md) · [lab](labs/25-03-lab/README.md) · [verify](verify/verify_25_03.py) |
| [25-04 · Yield Models and Die Cost](chapters/25-04-yield-and-die-cost.md) | 7 | 🏁 reviewed | [problems](problems/25-04-problems.md) · [solutions](solutions/25-04-solutions.md) · [lab](labs/25-04-lab/README.md) · [verify](verify/verify_25_04.py) |
| [25-05 · Foundries, PDKs and Specialty Processes](chapters/25-05-foundries-pdks-specialty-processes.md) | 6 | 🏁 reviewed | [problems](problems/25-05-problems.md) · [solutions](solutions/25-05-solutions.md) · [lab](labs/25-05-lab/README.md) · [verify](verify/verify_25_05.py) |
| [25-06 · Packaging I: Wire Bond, Flip-Chip, Substrates, SiP and PoP](chapters/25-06-packaging-fundamentals.md) | 6 | 🏁 reviewed | [problems](problems/25-06-problems.md) · [solutions](solutions/25-06-solutions.md) · [lab](labs/25-06-lab/README.md) · [verify](verify/verify_25_06.py) |
| [25-07 · Packaging II: 2.5D, 3D, Hybrid Bonding and Chiplets](chapters/25-07-advanced-packaging-and-chiplets.md) | 7 | 🏁 reviewed | [problems](problems/25-07-problems.md) · [solutions](solutions/25-07-solutions.md) · [lab](labs/25-07-lab/README.md) · [verify](verify/verify_25_07.py) |
| [25-08 · Thermal Engineering](chapters/25-08-thermal-engineering.md) | 6 | 🏁 reviewed | [problems](problems/25-08-problems.md) · [solutions](solutions/25-08-solutions.md) · [lab](labs/25-08-lab/README.md) · [verify](verify/verify_25_08.py) |
| [25-09 · Reliability Physics](chapters/25-09-reliability-physics.md) | 8 | 🏁 reviewed | [problems](problems/25-09-problems.md) · [solutions](solutions/25-09-solutions.md) · [lab](labs/25-09-lab/README.md) · [verify](verify/verify_25_09.py) |
| [25-10 · Qualification and Functional Safety](chapters/25-10-qualification-and-functional-safety.md) | 5 | 🏁 reviewed | [problems](problems/25-10-problems.md) · [solutions](solutions/25-10-solutions.md) · [lab](labs/25-10-lab/README.md) · [verify](verify/verify_25_10.py) |
| [25-11 · Test: ATE, Wafer Sort, Burn-In and Binning](chapters/25-11-test-ate-sort-burn-in.md) | 6 | 🏁 reviewed | [problems](problems/25-11-problems.md) · [solutions](solutions/25-11-solutions.md) · [lab](labs/25-11-lab/README.md) · [verify](verify/verify_25_11.py) |
| [25-12 · Post-Silicon Validation and Bring-Up](chapters/25-12-post-silicon-validation.md) | 4 | 🏁 reviewed | [problems](problems/25-12-problems.md) · [solutions](solutions/25-12-solutions.md) · [lab](labs/25-12-lab/README.md) · [verify](verify/verify_25_12.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/25-fabrication-packaging-test-and-reliability.csv) · [Equation sheet](../../reference/equation-sheets/25-fabrication-packaging-test-and-reliability.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 25 is planned at about 83 hours: the chapters' own estimates add to 78, plus about 5 hours of review; allow a further 4 hours for the exam. It draws on several earlier courses:

- Course 09: diffusion, oxides and the MOSFET;
- Course 19: wire delay, design for test (19-12) and pre-silicon verification (19-13);
- Course 03: Bayes' rule, the normal and chi-square distributions, and confidence intervals for a proportion (03-05; 25-12 adds the Wilson interval);
- Course 15: thermal networks (15-01);
- Course 04: the HBM ESD model (04-02) and optics;
- Course 23: TSVs and HBM stacks;
- Course 24: die-to-die links (24-06).

This course follows a chip from bare wafer to shipped part: how it is patterned and built, what it costs, how it is packaged and cooled, how it wears out, and how it is qualified, tested and brought up.

The twelve chapters fall into four blocks:

- **Making the wafer (25-01 to 25-03).** The FEOL, MOL and BEOL flow, oxidation and the wire tiers; lithography from 193 nm immersion through multipatterning to EUV and High-NA EUV, with photon noise and cost per pass; deposition, etch, CMP, implant and metrology as rate equations.
- **Economics and the foundry (25-04 and 25-05).** Dies per wafer, defect-density yield models, cost per good die, harvesting and yield learning; foundry business models, PDKs, corners, FD-SOI and the specialty processes that do not follow the leading edge.
- **Packaging and heat (25-06 to 25-08).** Wire bond, flip-chip, substrates and escape routing, solder fatigue; 2.5D and 3D integration, hybrid bonding, known-good die and the chiplet cost model; conduction, spreading, fins, liquid cooling and mission-profile temperatures.
- **Making it last and proving it works (25-09 to 25-12).** Electromigration, dielectric breakdown, BTI, HCI and ESD; qualification (AEC-Q100) and functional safety (ISO 26262 metrics); ATE, sort, burn-in, binning and guard bands; post-silicon validation, shmoos, bug curves and respin decisions.

Work at least the [A] and [B] problems of every chapter. The labs are of two kinds, both run in CI (the verify scripts, `run_spice.py` for the netlists' EXPECT lines, and `run_notebooks.py` for the notebooks):

- ngspice netlists: wire delay on three metal tiers as RC ladders (25-01) and an HBM discharge into an ESD clamp (25-09);
- Python models imported by their notebooks: `process.py`, `litho.py` (aerial images from diffraction orders), `units.py` (a finite-difference diffusion solver), `yieldcost.py` (a wafer-map Monte Carlo), `foundry.py` (a 1-D Laplace solve of the FD-SOI stack), `package.py`, `chiplets.py`, `thermal.py` (an axisymmetric finite-difference spreader), `reliability.py`, `qual.py` (a Monte Carlo of latent faults), `testcost.py` and `postsi.py` (a synthetic shmoo and its fit).

**What to master cold.** The [equation sheet](../../reference/equation-sheets/25-fabrication-packaging-test-and-reliability.md) collects the relations; these are the ideas behind them:

- oxidation is reaction-limited when thin and diffusion-limited when thick; a wafer's yield is the product of 400 to 1,400 step yields, and Little's law turns cycle time into inventory (25-01);
- resolution is set by $\lambda/\text{NA}$ and depth of focus by $\lambda/\text{NA}^2$, so a higher NA buys resolution at the cost of focus; EUV is photon-starved, so dose, throughput and stochastic defects trade against each other (25-02);
- each unit process runs at a rate set by its slowest step (transport or reaction); an anneal broadens an implant while conserving its dose; a gauge's own noise adds in quadrature to the process spread it measures (25-03);
- yield falls exponentially with area × defect density, and clustering makes large dies less hopeless than Poisson predicts; cost per good die rises faster than area (25-04);
- a process corner (the P of a PVT corner) is modelled as a shift in $V_{TH}$, and delay is most sensitive to it at low supply; specialty and mature nodes win on cost, voltage and analog, not density (25-05);
- area arrays beat perimeter pads above a crossover die size; solder fatigue life scales as strain to the power −2, and a package is only as reliable as its weakest-link joints (25-06);
- bond density scales as $1/\text{pitch}^2$ but overlay must shrink with pitch; chiplets win when the yield gain exceeds the added test, package and attach cost, and escapes compound across every die in a package (25-07);
- heat flows through a series of resistances, and spreading near a small hotspot can add as much rise as conduction through the whole die (Examples 25-08.1 and 25-08.2); liquid cooling relaxes the fluid-rise and convection limits of air (25-08);
- acceleration factors are exponential in $E_a/k$, so a wrong activation energy or breakdown model can shift a lifetime by orders of magnitude; zero failures bound a failure rate only to a chi-square quantile over device-hours (25-09);
- qualification proves a mission profile with accelerated stress; ISO 26262 asks for coverage of single-point faults (SPFM) and latent faults (LFM) and a bounded residual rate (PMHF), and a chip supports an ASIL rather than being one (25-10);
- test cost is tester time × rate divided by yield; guard bands trade escapes for overkill at a price set by tester accuracy; burn-in removes a weak subpopulation at the cost of every part's stress time (25-11);
- first silicon is validated, not just tested: shmoos map the operating window, bug-discovery curves estimate what remains, and respins are decision trees under uncertainty (25-12).

**After this course.** Course 26 turns these constraints into a design process with requirements, reviews and professional practice. Course 27 assembles whole systems, where 25-07's chiplet economics and 25-08's cooling limits shape an AI accelerator. Course 28 uses 25-04's cost models, 25-09's reliability claims and 25-12's first-silicon statistics in technical diligence.

> **Deeper:** see companion repo *Semiconductor Capital Equipment* for the tools behind 25-02 and 25-03 (scanners, etch, deposition and metrology systems) and their markets.
