<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 07 · Circuit Analysis II (Transient and AC)

Circuits with memory. Capacitors and inductors, first- and second-order transients, Laplace-domain analysis, sinusoidal steady state with phasors and impedance, AC power, frequency response and filters, transformers, two-port networks and three-phase power.

| | |
|---|---|
| **Term** | 2 |
| **Study hours** | ≈ 103 |
| **University equivalents** | Circuits II (sophomore/junior); MIT 6.002 (second half); Berkeley EE16B (circuits/transients portion) |
| **Textbook alignment** | Nilsson & Riedel, *Electric Circuits*; Alexander & Sadiku, *Fundamentals of Electric Circuits* |
| **Free courses** | MIT OCW 6.002 Circuits and Electronics; Berkeley EE16B |
| **Prerequisites** | [02 · Complex Numbers, Differential Equations and Linear Algebra](../02-complex-numbers-des-and-linear-algebra/README.md), [06 · Circuit Analysis I (DC)](../06-circuit-analysis-1-dc/README.md) |
| **FE areas** | Circuit Analysis (DC and AC Steady State), Linear Systems, Power Systems |

## Learning objectives

1. Analyze first- and second-order transients from initial conditions, final values and characteristic roots.
2. Analyze circuits in the s-domain, including initial conditions, and extract transfer functions, poles and zeros.
3. Solve sinusoidal steady-state circuits with phasors and impedance, and compute real, reactive, apparent and complex power.
4. Sketch Bode plots, design simple passive and active filters, and characterize resonance by ω0, Q and bandwidth.
5. Analyze magnetically coupled circuits, ideal transformers, two-port networks and balanced three-phase systems.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [07-01 · Capacitors and Inductors](chapters/07-01-capacitors-and-inductors.md) | 7 | 🏁 reviewed | [problems](problems/07-01-problems.md) · [solutions](solutions/07-01-solutions.md) · [lab](labs/07-01-lab/README.md) · [verify](verify/verify_07_01.py) |
| [07-02 · First-Order RC and RL Transients](chapters/07-02-first-order-rc-rl-transients.md) | 10 | 🏁 reviewed | [problems](problems/07-02-problems.md) · [solutions](solutions/07-02-solutions.md) · [lab](labs/07-02-lab/README.md) · [verify](verify/verify_07_02.py) |
| [07-03 · Second-Order RLC Transients](chapters/07-03-second-order-rlc-transients.md) | 10 | 🏁 reviewed | [problems](problems/07-03-problems.md) · [solutions](solutions/07-03-solutions.md) · [lab](labs/07-03-lab/README.md) · [verify](verify/verify_07_03.py) |
| [07-04 · Laplace-Domain Circuit Analysis](chapters/07-04-laplace-domain-circuit-analysis.md) | 12 | 🏁 reviewed | [problems](problems/07-04-problems.md) · [solutions](solutions/07-04-solutions.md) · [lab](labs/07-04-lab/README.md) · [verify](verify/verify_07_04.py) |
| [07-05 · Sinusoidal Steady State, Phasors and Impedance](chapters/07-05-sinusoidal-steady-state-and-impedance.md) | 10 | 🏁 reviewed | [problems](problems/07-05-problems.md) · [solutions](solutions/07-05-solutions.md) · [lab](labs/07-05-lab/README.md) · [verify](verify/verify_07_05.py) |
| [07-06 · AC Power and Power Factor](chapters/07-06-ac-power-and-power-factor.md) | 8 | 🏁 reviewed | [problems](problems/07-06-problems.md) · [solutions](solutions/07-06-solutions.md) · [lab](labs/07-06-lab/README.md) · [verify](verify/verify_07_06.py) |
| [07-07 · Frequency Response and Bode Plots](chapters/07-07-frequency-response-and-bode-plots.md) | 10 | 🏁 reviewed | [problems](problems/07-07-problems.md) · [solutions](solutions/07-07-solutions.md) · [lab](labs/07-07-lab/README.md) · [verify](verify/verify_07_07.py) |
| [07-08 · Filters and Resonance](chapters/07-08-filters-and-resonance.md) | 10 | 🏁 reviewed | [problems](problems/07-08-problems.md) · [solutions](solutions/07-08-solutions.md) · [lab](labs/07-08-lab/README.md) · [verify](verify/verify_07_08.py) |
| [07-09 · Mutual Inductance and Transformers](chapters/07-09-mutual-inductance-and-transformers.md) | 8 | 🏁 reviewed | [problems](problems/07-09-problems.md) · [solutions](solutions/07-09-solutions.md) · [lab](labs/07-09-lab/README.md) · [verify](verify/verify_07_09.py) |
| [07-10 · Two-Port Networks](chapters/07-10-two-port-networks.md) | 7 | 🏁 reviewed | [problems](problems/07-10-problems.md) · [solutions](solutions/07-10-solutions.md) · [lab](labs/07-10-lab/README.md) · [verify](verify/verify_07_10.py) |
| [07-11 · Three-Phase Circuits](chapters/07-11-three-phase-circuits.md) | 5 | 🏁 reviewed | [problems](problems/07-11-problems.md) · [solutions](solutions/07-11-solutions.md) · [lab](labs/07-11-lab/README.md) · [verify](verify/verify_07_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/07-circuit-analysis-2-transient-and-ac.csv) · [Equation sheet](../../reference/equation-sheets/07-circuit-analysis-2-transient-and-ac.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 07 continues Term 2 and is planned at about 103 hours: the chapters' own estimates add to 97, plus review and the exam. It adds memory to Course 06's circuits. Capacitors and inductors make circuits depend on their history, and sinusoids make them depend on frequency. Almost every later course rests on one of those two views: transistor amplifiers, power converters, filters, communication links and the power grid.

The eleven chapters fall into three blocks:

- **Time domain (07-01 to 07-04).** The storage elements; first-order transients and the initial–final–τ method; second-order ringing and damping; and the Laplace transform, which turns all of it into algebra, including convolution and the sinusoidal steady state.
- **Frequency domain (07-05 to 07-08).** Phasors and impedance; AC power and power factor; Bode plots, gain–bandwidth and phase margin; and resonance and filters, passive and active (Sallen–Key, multiple-feedback, high-pass and band-pass sections).
- **Systems (07-09 to 07-11).** Coupled coils and transformers; two-port networks and S-parameters, with matching and mismatch loss; and three-phase power, including unbalanced loads, phase sequence and transformer phase shifts.

Work at least the [A] and [B] problems of every chapter (165 problems in all). Every lab pairs a notebook with ngspice netlists whose results are checked against the answer keys, so you can predict, then simulate, every circuit.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- continuity of $v_C$ and $i_L$, and the decoupling and inductive-kick consequences (07-01);
- the initial–final–τ formula, rise time, settling and the ½CV² charging loss (07-02);
- α, ω0, ζ, $Q$, $Z_0$, overshoot and damper design (07-03);
- s-domain models with initial-condition sources, poles and zeros, stability, and the initial- and final-value theorems (07-04);
- impedance, phasor nodal analysis and Thévenin equivalents with dependent sources (07-05);
- $S = P + jQ$, power-factor correction, THD and the conjugate match (07-06);
- Bode asymptotes, GBW, phase margin and right-half-plane zeros (07-07);
- resonance, Butterworth design, active sections and resonator $Q$ against insertion loss (07-08);
- the dot convention, reflected impedance, the ideal transformer and the efficiency curve (07-09);
- z, y, h and ABCD parameters, S-parameters, matching and VSWR (07-10);
- √3∠30°, per-phase analysis, two wattmeters and a floating star point (07-11).

The [equation sheet](../../reference/equation-sheets/07-circuit-analysis-2-transient-and-ac.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions and takes 240 minutes. It allows a calculator and the equation sheet, but not Python or a simulator. Aim for at least 70%. Questions 13 and 14 are synthesis problems: a buck converter's output filter and a 2.4 GHz antenna match. Question 15 is a short-answer diligence question about four product claims. The course maps onto the FE Electrical and Computer exam's circuit-analysis, linear-systems and power areas. The [flashcards](../../flashcards/07-circuit-analysis-2-transient-and-ac.csv) (134 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Many headline specifications are frequency-domain or transient numbers in disguise:

- a "clean" power rail is an impedance profile;
- a fast buffer is a phase margin;
- a filter's selectivity is a resonator $Q$;
- a link budget is a stack of S-parameters;
- a rack's power rating is $\sqrt3V_LI_L$ times a power factor and a derating.

This course gives you the tools to unpack each one, and the Marketing vs Reality sections practice it on MLCCs, hot-plug ringing, bioimpedance wearables, power-factor tariffs, oscilloscope bandwidth, acoustic filters, transformer efficiency rules, SerDes channels and data-center distribution voltages.

**Perishable content.** The circuit theory is timeless. The dated facts are in the practitioner sections, logged as [R-110](../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share) to [R-142](../../reference/research-log.md#r-142--three-phase-distribution-voltages) in the research log. These are the most likely to move:

- MLCC counts and market shares (R-110);
- GaN switching and layout figures (R-115);
- 80 PLUS and utility power-factor rules (R-122);
- RF filter markets and bands (R-134);
- US transformer efficiency standards, under review in 2026 (R-135);
- Ethernet and PCIe channel budgets (R-141);
- data-center distribution practice (R-142).

Check those entries once a year.
