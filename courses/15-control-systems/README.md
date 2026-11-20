<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 15 · Control Systems

Feedback control from modeling to design: transfer functions, time response, root locus, Bode/Nyquist stability, PID and lead/lag compensation, state space and digital control, applied to PLLs, voltage regulators and thermal management.

| | |
|---|---|
| **Term** | 5 |
| **Study hours** | ≈ 89 |
| **University equivalents** | Feedback Control Systems (junior/senior); MIT 6.302; Berkeley EE C128 |
| **Textbook alignment** | Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*; Ogata, *Modern Control Engineering*; Åström & Murray, *Feedback Systems* (free online) |
| **Free courses** | MIT OCW 6.302 Feedback Systems; MIT OCW 2.04A Systems and Controls |
| **Prerequisites** | [07 · Circuit Analysis II (Transient and AC)](../07-circuit-analysis-2-transient-and-ac/README.md), [11 · Signals and Systems](../11-signals-and-systems/README.md) |
| **FE areas** | Control Systems |

## Learning objectives

1. Model electrical, mechanical and thermal systems as transfer functions and block diagrams.
2. Relate pole locations to time-response specifications and compute steady-state error.
3. Design controllers with root locus and with Bode/Nyquist methods (phase margin, gain margin).
4. Tune PID and design lead/lag compensators to meet specifications.
5. Formulate state-space models, test controllability/observability and place poles.
6. Discretize controllers and analyze PLLs and regulators as feedback systems.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [15-01 · Modeling Dynamic Systems](chapters/15-01-modeling-dynamic-systems.md) | 8 | ✅ verified | [problems](problems/15-01-problems.md) · [solutions](solutions/15-01-solutions.md) · [lab](labs/15-01-lab/README.md) · [verify](verify/verify_15_01.py) |
| [15-02 · Transfer Functions and Block Diagrams](chapters/15-02-transfer-functions-and-block-diagrams.md) | 7 | ✅ verified | [problems](problems/15-02-problems.md) · [solutions](solutions/15-02-solutions.md) · [lab](labs/15-02-lab/README.md) · [verify](verify/verify_15_02.py) |
| [15-03 · Time Response and Specifications](chapters/15-03-time-response.md) | 7 | ✅ verified | [problems](problems/15-03-problems.md) · [solutions](solutions/15-03-solutions.md) · [lab](labs/15-03-lab/README.md) · [verify](verify/verify_15_03.py) |
| [15-04 · Feedback Properties and Steady-State Error](chapters/15-04-feedback-and-steady-state-error.md) | 7 | ✅ verified | [problems](problems/15-04-problems.md) · [solutions](solutions/15-04-solutions.md) · [lab](labs/15-04-lab/README.md) · [verify](verify/verify_15_04.py) |
| [15-05 · Stability and the Routh–Hurwitz Criterion](chapters/15-05-stability-routh-hurwitz.md) | 5 | ✅ verified | [problems](problems/15-05-problems.md) · [solutions](solutions/15-05-solutions.md) · [lab](labs/15-05-lab/README.md) · [verify](verify/verify_15_05.py) |
| [15-06 · Root Locus](chapters/15-06-root-locus.md) | 8 | ✅ verified | [problems](problems/15-06-problems.md) · [solutions](solutions/15-06-solutions.md) · [lab](labs/15-06-lab/README.md) · [verify](verify/verify_15_06.py) |
| [15-07 · Frequency-Domain Design: Bode, Nyquist and Margins](chapters/15-07-frequency-domain-design.md) | 10 | ✅ verified | [problems](problems/15-07-problems.md) · [solutions](solutions/15-07-solutions.md) · [lab](labs/15-07-lab/README.md) · [verify](verify/verify_15_07.py) |
| [15-08 · PID Control](chapters/15-08-pid-control.md) | 6 | ✅ verified | [problems](problems/15-08-problems.md) · [solutions](solutions/15-08-solutions.md) · [lab](labs/15-08-lab/README.md) · [verify](verify/verify_15_08.py) |
| [15-09 · Lead and Lag Compensation](chapters/15-09-lead-lag-compensation.md) | 7 | ✅ verified | [problems](problems/15-09-problems.md) · [solutions](solutions/15-09-solutions.md) · [lab](labs/15-09-lab/README.md) · [verify](verify/verify_15_09.py) |
| [15-10 · State-Space Introduction](chapters/15-10-state-space-introduction.md) | 8 | ✅ verified | [problems](problems/15-10-problems.md) · [solutions](solutions/15-10-solutions.md) · [lab](labs/15-10-lab/README.md) · [verify](verify/verify_15_10.py) |
| [15-11 · Digital Control](chapters/15-11-digital-control.md) | 5 | ✅ verified | [problems](problems/15-11-problems.md) · [solutions](solutions/15-11-solutions.md) · [lab](labs/15-11-lab/README.md) · [verify](verify/verify_15_11.py) |
| [15-12 · Applications: PLLs, Voltage Regulators and Thermal Management](chapters/15-12-control-applications-pll-regulators-thermal.md) | 6 | ✅ verified | [problems](problems/15-12-problems.md) · [solutions](solutions/15-12-solutions.md) · [lab](labs/15-12-lab/README.md) · [verify](verify/verify_15_12.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/15-control-systems.csv) · [Equation sheet](../../reference/equation-sheets/15-control-systems.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 15 is planned at about 89 hours: the chapters' own estimates add to 84, plus 5 hours of review and the exam. Courses 07 and 11 gave you transfer functions, Laplace and z-transforms, and Bode plots as tools for analyzing circuits and signals. This course turns them into a discipline for *designing* behaviour: wrap a measurement around a plant, decide how much gain and phase to spend where, and prove that the result is stable, fast and accurate. The same few ideas reappear in every loop on a chip, from an op-amp to a PLL to a thermal limiter.

The twelve chapters fall into four blocks:

- **Models and loops (15-01 to 15-04).** Mechanical, electrical, motor and thermal models and their linearization; transfer functions, block diagrams and Mason's formula; time-domain specifications from pole locations; and what feedback buys: sensitivity, disturbance rejection and steady-state error.
- **Stability (15-05 to 15-07).** The Routh–Hurwitz criterion; the root locus as a picture of how poles move with gain; and the frequency-domain view, with Bode margins, the Nyquist criterion, delay and Bode's sensitivity integral.
- **Design (15-08 to 15-11).** PID control with its practical fixes (windup, derivative filtering, setpoint weighting, tuning rules); lead and lag compensation; state feedback, observers and integral action; and digital implementation, with the hold's delay and discrete stability.
- **Applications (15-12).** The charge-pump PLL, LDO and switching-regulator loops, DVFS and thermal throttling, analyzed with the tools of the whole course.

Work at least the [A] and [B] problems of every chapter (120 of the 159 problems; the 39 [C] problems are the stretch). The labs form a toolkit that later chapters import:

- `plants.py` (15-01) and `blocks.py` (15-02) model plants and combine transfer functions, with a general Mason's-formula solver;
- `specs.py` (15-03) measures step specifications exactly, `steady.py` (15-04) predicts and simulates steady errors, `routh.py` (15-05) builds Routh arrays with both special cases, and `rlocus.py` (15-06) draws loci with every sketching rule;
- `freqdomain.py` (15-07) finds margins, Nyquist encirclements and Bode's integral; `pid.py` (15-08) simulates PID loops with saturation, anti-windup, filtering and noise; `compensate.py` (15-09) designs lead and lag networks;
- `statespace.py` (15-10), `digital.py` (15-11) and `loops.py` (15-12) handle pole placement and observers, sampled loops simulated exactly between samples, and the PLL, regulator and thermal loops;
- fourteen ngspice netlists confirm the circuit examples, among them a mass–spring–damper analogue, a ring oscillator, an op-amp loop measured by Middlebrook injection, an anti-windup integrator, a lead network, a switch-and-capacitor sampler, a phase-domain PLL and an LDO with ESR.

The verify scripts recompute the chapters' numbers, mostly by a route independent of the lab code (closed forms, a second integrator, symbolic algebra), and check prose claims as well as answer keys, so a mismatch in your own work usually means a wrong method, not rounding.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/15-control-systems.md) collects the relations; these are the ideas behind them:

- a loop's behaviour is set by its loop gain $L$: $S = 1/(1 + L)$ measures how much disturbances and plant errors survive, and $T = L/(1 + L)$ how faithfully the output follows the reference (15-02, 15-04);
- pole locations are specifications: $\zeta$ sets overshoot, $\sigma$ sets settling, and zeros and extra poles modify both (15-03);
- integrators where they matter give zero steady error, and the internal model principle says which you need (15-04);
- stability can be decided without solving for roots: Routh for polynomials, the root locus for a gain sweep, Nyquist for any loop including delays and unstable plants (15-05 to 15-07);
- phase margin is the currency of design: about 100ζ degrees, spent by delays, holds and extra poles, bought back by zeros and lead (15-07, 15-09, 15-11);
- PID is three ideas (present, past, trend) plus three practical fixes (anti-windup, derivative filtering, setpoint weighting) (15-08);
- state feedback places every pole if the plant is controllable, and an observer supplies states you cannot measure (15-10);
- going digital costs about half a sample of delay plus computation time, and the discretization method matters at coarse sampling (15-11);
- PLLs, regulators and thermal limiters are ordinary loops: their bandwidths trade noise against speed, capacitance against droop, and burst against sustained performance (15-12).

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes, with a calculator and the equation sheet but no Python or simulator. Aim for at least 70%. Questions 1 to 12 follow the chapters; Question 7 includes a Nyquist encirclement count; Question 13 asks for three short derivations (the ramp error of a type-1 loop, the lead compensator's maximum phase, the zero-order hold's frequency response); Question 14 is a diligence question about a power-management start-up's claims, partly graded against a rubric. The course maps onto the FE Electrical and Computer exam's Control Systems area, 6–9 questions ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/15-control-systems.csv) (82 cards) are for spaced review alongside the chapters.
