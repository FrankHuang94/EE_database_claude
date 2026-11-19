<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 10 · Electronics I (Microelectronic Circuits)

Turning devices into circuits: diode circuits, transistor biasing, small-signal models, single-stage MOS and BJT amplifiers, current mirrors, and the non-idealities of real op-amps.

| | |
|---|---|
| **Term** | 3 |
| **Study hours** | ≈ 99 |
| **University equivalents** | Electronics I / Microelectronic Circuits I (junior); MIT 6.012 (circuits half); Berkeley EE105 |
| **Textbook alignment** | Sedra & Smith, *Microelectronic Circuits* (first half); Razavi, *Fundamentals of Microelectronics* |
| **Free courses** | MIT OCW 6.012 Microelectronic Devices and Circuits; MIT OCW 6.002 (amplifier lectures) |
| **Prerequisites** | [07 · Circuit Analysis II (Transient and AC)](../07-circuit-analysis-2-transient-and-ac/README.md), [09 · Semiconductor Devices](../09-semiconductor-devices/README.md) |
| **FE areas** | Electronics |

## Learning objectives

1. Analyze diode circuits (rectifiers, clippers, regulators) with appropriate diode models.
2. DC-bias MOSFET and BJT circuits and verify the operating region.
3. Derive small-signal models (g_m, r_o, r_π) from large-signal equations and use them to compute gain and input/output resistance.
4. Analyze and compare all single-stage MOS and BJT amplifier configurations.
5. Design current sources and mirrors and analyze their output resistance.
6. Quantify op-amp non-idealities (finite gain, GBW, slew rate, offset, bias current, CMRR, PSRR) and their effect on circuits.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [10-01 · Diodes and Diode Circuits](chapters/10-01-diodes-and-diode-circuits.md) | 10 | ✅ verified | [problems](problems/10-01-problems.md) · [solutions](solutions/10-01-solutions.md) · [lab](labs/10-01-lab/README.md) · [verify](verify/verify_10_01.py) |
| [10-02 · MOSFET DC Operation and Biasing](chapters/10-02-mosfet-dc-operation-and-biasing.md) | 10 | ✅ verified | [problems](problems/10-02-problems.md) · [solutions](solutions/10-02-solutions.md) · [lab](labs/10-02-lab/README.md) · [verify](verify/verify_10_02.py) |
| [10-03 · BJT DC Operation and Biasing](chapters/10-03-bjt-dc-operation-and-biasing.md) | 9 | ✅ verified | [problems](problems/10-03-problems.md) · [solutions](solutions/10-03-solutions.md) · [lab](labs/10-03-lab/README.md) · [verify](verify/verify_10_03.py) |
| [10-04 · Small-Signal Models](chapters/10-04-small-signal-models.md) | 10 | ✅ verified | [problems](problems/10-04-problems.md) · [solutions](solutions/10-04-solutions.md) · [lab](labs/10-04-lab/README.md) · [verify](verify/verify_10_04.py) |
| [10-05 · Amplifier Fundamentals](chapters/10-05-amplifier-fundamentals.md) | 6 | ✅ verified | [problems](problems/10-05-problems.md) · [solutions](solutions/10-05-solutions.md) · [lab](labs/10-05-lab/README.md) · [verify](verify/verify_10_05.py) |
| [10-06 · MOS Single-Stage Amplifiers](chapters/10-06-mos-single-stage-amplifiers.md) | 12 | ✅ verified | [problems](problems/10-06-problems.md) · [solutions](solutions/10-06-solutions.md) · [lab](labs/10-06-lab/README.md) · [verify](verify/verify_10_06.py) |
| [10-07 · BJT Single-Stage Amplifiers](chapters/10-07-bjt-single-stage-amplifiers.md) | 10 | ✅ verified | [problems](problems/10-07-problems.md) · [solutions](solutions/10-07-solutions.md) · [lab](labs/10-07-lab/README.md) · [verify](verify/verify_10_07.py) |
| [10-08 · Current Sources and Current Mirrors](chapters/10-08-current-sources-and-mirrors.md) | 8 | ✅ verified | [problems](problems/10-08-problems.md) · [solutions](solutions/10-08-solutions.md) · [lab](labs/10-08-lab/README.md) · [verify](verify/verify_10_08.py) |
| [10-09 · Real Op-Amps: Non-Idealities](chapters/10-09-real-op-amps-nonidealities.md) | 10 | ✅ verified | [problems](problems/10-09-problems.md) · [solutions](solutions/10-09-solutions.md) · [lab](labs/10-09-lab/README.md) · [verify](verify/verify_10_09.py) |
| [10-10 · Op-Amp Application Circuits](chapters/10-10-op-amp-application-circuits.md) | 8 | ✅ verified | [problems](problems/10-10-problems.md) · [solutions](solutions/10-10-solutions.md) · [lab](labs/10-10-lab/README.md) · [verify](verify/verify_10_10.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/10-electronics-1.csv) · [Equation sheet](../../reference/equation-sheets/10-electronics-1.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 10 is planned at about 99 hours: the chapters' own estimates add to 93, plus review and the exam. It is where devices become circuits. Course 09 explained why a transistor conducts; this course treats it as a component with a bias point, a small-signal model and a handful of configurations, and builds every amplifier, mirror and op-amp application from those pieces. Course 12 then opens the op-amp itself.

The ten chapters fall into four blocks:

- **Bias (10-01 to 10-03).** Diodes and their circuits (rectifiers, Zener regulators, clamps); MOSFET and BJT DC operation, the bias networks that survive threshold and β spread, the switch, and thermal stability.
- **Models (10-04 and 10-05).** Linearization into small-signal models, the hybrid-π and T models, the limits of linearity, $g_m/I$; then amplifiers as two-ports, loading, decibels, cascades and efficiency.
- **Single stages and mirrors (10-06 to 10-08).** The three MOS and three bipolar configurations with $r_o$, body effect and degeneration; the MOS–BJT comparison; current sources, cascode and Wilson mirrors, and mismatch.
- **Op-amps in practice (10-09 and 10-10).** Finite gain, GBW, slew rate, offset, drift, CMRR, PSRR and ranges, read from current data sheets; then instrumentation amplifiers, integrators, precision rectifiers, comparators and Schmitt triggers, and photodiode transimpedance amplifiers.

Work at least the [A] and [B] problems of every chapter (123 problems in all). Every lab has a notebook, and every lab also has an ngspice netlist: 51 simulator expectations confirm the chapters' worked examples, several of them with model parameters solved so that the simulator's transistor has exactly the $g_m$, $r_o$ and χ of the hand analysis.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- the diode's exponential law, its small-signal resistance, and the peak rectifier's ripple and diode current (10-01);
- why fixed-voltage bias fails and degeneration works, for both devices (10-02, 10-03);
- every small-signal parameter as a derivative of a large-signal law; intrinsic gain; $g_m/I$ from bipolar to weak inversion; how small "small" is (10-04);
- loading as two dividers, bridging against matching, buffers at the worst interface, class-A efficiency (10-05);
- gain as a voltage budget ($2V_{RD}/V_{ov}$, $V_{RC}/V_T$); degeneration trading gain for linearity and output resistance; followers and their limits; the reflection rules (10-06, 10-07);
- a current source as accuracy, output resistance and compliance; the cascode's $g_mr_o^2$; Pelgrom's area law and why mirrors want large overdrive (10-08);
- noise gain, GBW over noise gain, the slew boundary $\text{SR}\cdot\tau$, full-power bandwidth, and the DC error budget (10-09);
- CMRR from resistor matching, hysteresis against noise, and the TIA as a second-order loop (10-10).

The [equation sheet](../../reference/equation-sheets/10-electronics-1.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes. It allows a calculator and the equation sheet, but not Python or a simulator. Aim for at least 70%. Questions 1 to 12 follow the chapters; Question 13 asks for three short derivations; Question 14 is a diligence question built around a biopotential front-end start-up's claims, graded against a rubric. The course maps onto the FE Electrical and Computer exam's electronics area ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/10-electronics-1.csv) (80 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Analog claims are rarely false; they are usually true under conditions that are not yours. This course teaches you to ask:

- at what gain, load, frequency and temperature a specification holds (a "10 MHz" op-amp is 100 kHz at a gain of 100; a "50 W" amplifier is 50 W at 10% distortion);
- whether a quoted number is typical or guaranteed, and what the guaranteed one is over the operating range;
- what a single stage can physically deliver (its intrinsic gain), and therefore how many stages, how much headroom and how much current a claimed performance needs;
- how much of a chip's area is spent on matching and bias rather than function, and whether calibration could replace it.

The Marketing vs Reality sections practice this on "ultra-low-power" front ends, "high-gain" amplifiers, "rail-to-rail" and "unity-gain buffer" claims, "precision" references and "matched" pairs, op-amp bandwidth and noise figures, class-D efficiency, CMRR, comparator speed and photoreceiver bandwidth.

**Perishable content.** The circuit theory is timeless. The dated facts are data-sheet specifications, logged as [R-176](../../reference/research-log.md#r-176--diode-and-protection-device-data-sheets) to [R-183](../../reference/research-log.md#r-183--instrumentation-amplifier-and-comparator-data-sheets) in the research log (diodes and protection devices, MOSFETs and load switches, bipolar transistors, a class-D amplifier, an image-sensor pixel reference, transistor matching, op-amps, an instrumentation amplifier and a comparator). Parts are revised and replaced; check those entries once a year, and treat each as an example of its class rather than a recommendation.
