<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 12 · Electronics II

Real amplifiers: differential pairs, cascodes and multistage amplifiers, high-frequency response, feedback, stability and compensation, output stages, op-amp internals, oscillators and noise. This is the bridge to analog IC design.

| | |
|---|---|
| **Term** | 4 |
| **Study hours** | ≈ 104 |
| **University equivalents** | Electronics II / Microelectronic Circuits II (junior/senior); Berkeley EE140 (intro); Stanford EE114; MIT 6.301 |
| **Textbook alignment** | Sedra & Smith, *Microelectronic Circuits* (second half); Razavi, *Design of Analog CMOS Integrated Circuits* (early chapters); Gray, Hurst, Lewis & Meyer, *Analysis and Design of Analog Integrated Circuits* (reference) |
| **Free courses** | MIT OCW 6.301 Solid-State Circuits; MIT OCW 6.012 (frequency response and feedback lectures) |
| **Prerequisites** | [10 · Electronics I (Microelectronic Circuits)](../10-electronics-1/README.md), [11 · Signals and Systems](../11-signals-and-systems/README.md) |
| **FE areas** | Electronics, Control Systems |

## Learning objectives

1. Analyze differential pairs (differential/common-mode gain, CMRR) and multistage amplifiers with active loads and cascodes.
2. Compute amplifier frequency response using device capacitances, the Miller approximation and time-constant methods.
3. Analyze the four feedback topologies and their effect on gain, bandwidth and impedances.
4. Assess stability with loop gain, phase margin and gain margin, and apply frequency compensation.
5. Analyze output stages, two-stage op-amp internals and oscillator conditions.
6. Compute input-referred noise from thermal, shot and flicker sources.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [12-01 · Differential Pairs](chapters/12-01-differential-pairs.md) | 10 | 🏁 reviewed | [problems](problems/12-01-problems.md) · [solutions](solutions/12-01-solutions.md) · [lab](labs/12-01-lab/README.md) · [verify](verify/verify_12_01.py) |
| [12-02 · Active Loads, Cascodes and Multistage Amplifiers](chapters/12-02-active-loads-cascodes-multistage.md) | 10 | 🏁 reviewed | [problems](problems/12-02-problems.md) · [solutions](solutions/12-02-solutions.md) · [lab](labs/12-02-lab/README.md) · [verify](verify/verify_12_02.py) |
| [12-03 · Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros](chapters/12-03-frequency-response-miller-poles-zeros.md) | 12 | 🏁 reviewed | [problems](problems/12-03-problems.md) · [solutions](solutions/12-03-solutions.md) · [lab](labs/12-03-lab/README.md) · [verify](verify/verify_12_03.py) |
| [12-04 · High-Frequency Analysis Methods](chapters/12-04-high-frequency-analysis-methods.md) | 8 | 🏁 reviewed | [problems](problems/12-04-problems.md) · [solutions](solutions/12-04-solutions.md) · [lab](labs/12-04-lab/README.md) · [verify](verify/verify_12_04.py) |
| [12-05 · Feedback: Theory and the Four Topologies](chapters/12-05-feedback-topologies.md) | 12 | 🏁 reviewed | [problems](problems/12-05-problems.md) · [solutions](solutions/12-05-solutions.md) · [lab](labs/12-05-lab/README.md) · [verify](verify/verify_12_05.py) |
| [12-06 · Stability and Frequency Compensation](chapters/12-06-stability-and-compensation.md) | 10 | 🏁 reviewed | [problems](problems/12-06-problems.md) · [solutions](solutions/12-06-solutions.md) · [lab](labs/12-06-lab/README.md) · [verify](verify/verify_12_06.py) |
| [12-07 · Output Stages and Power Amplifiers](chapters/12-07-output-stages.md) | 8 | 🏁 reviewed | [problems](problems/12-07-problems.md) · [solutions](solutions/12-07-solutions.md) · [lab](labs/12-07-lab/README.md) · [verify](verify/verify_12_07.py) |
| [12-08 · Op-Amp Internals](chapters/12-08-op-amp-internals.md) | 10 | 🏁 reviewed | [problems](problems/12-08-problems.md) · [solutions](solutions/12-08-solutions.md) · [lab](labs/12-08-lab/README.md) · [verify](verify/verify_12_08.py) |
| [12-09 · Oscillators](chapters/12-09-oscillators.md) | 8 | 🏁 reviewed | [problems](problems/12-09-problems.md) · [solutions](solutions/12-09-solutions.md) · [lab](labs/12-09-lab/README.md) · [verify](verify/verify_12_09.py) |
| [12-10 · Noise in Circuits](chapters/12-10-noise-in-circuits.md) | 10 | 🏁 reviewed | [problems](problems/12-10-problems.md) · [solutions](solutions/12-10-solutions.md) · [lab](labs/12-10-lab/README.md) · [verify](verify/verify_12_10.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/12-electronics-2.csv) · [Equation sheet](../../reference/equation-sheets/12-electronics-2.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 12 is planned at about 104 hours: the chapters' own estimates add to 98, plus review and the exam. Course 10 built single transistors into single stages; this course builds stages into the circuits that sit inside every chip's analog blocks, and asks the questions that decide whether they work: how much gain, how fast, how stable, how efficient and how quiet.

The ten chapters fall into four blocks:

- **Gain (12-01 and 12-02).** The differential pair, the input stage of nearly every amplifier, with common-mode rejection and mismatch; then active loads, cascodes and multistage amplifiers, where gain comes from output resistance.
- **Speed (12-03 and 12-04).** Device capacitances and $f_T$, the Miller effect and the right-half-plane zero; then the time-constant methods that estimate bandwidth without solving the circuit, and pole splitting.
- **Feedback (12-05 and 12-06).** What feedback buys (accuracy, bandwidth, linearity, impedances) and how to analyse real circuits by return ratio; then what it costs: stability, phase margin and frequency compensation.
- **Building blocks (12-07 to 12-10).** Output stages and their efficiency and thermal limits; op-amp internals (two-stage and folded cascode, slew rate, CMFB, rail-to-rail); oscillators, which are loops designed to be unstable; and noise, which sets the floor under everything.

Work at least the [A] and [B] problems of every chapter (115 of the 143 problems; the 28 [C] problems are the stretch). Every lab has a notebook that runs top to bottom and an ngspice netlist; several netlists use small-signal G-element models, which confirm the hand analysis exactly, while 12-01's and 12-02's use level-1 MOSFET models, 12-07's real bipolar transistor models, and 12-08's slew netlist and 12-09's oscillator behavioural large-signal models. Most verify scripts recompute the chapters' numbers by a different route from the text (nodal analysis, root finding, eigenvalues, numerical integration, large-signal simulation), so a mismatch in your own work usually means a wrong method rather than a rounding difference.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- a differential pair rejects what is common and amplifies what is different, and the tail's output resistance and the devices' matching set how well (12-01);
- gain is transconductance times output resistance, and cascodes multiply output resistance by $g_mr_o$ (12-02);
- every capacitor between an amplifier's input and output is multiplied by $1 + \lvert A\rvert$ as seen from the input, and every feed-forward path makes a zero (12-03, 12-04);
- feedback divides every error inside the loop by $1 + T$ and leaves those outside it alone; series connections multiply impedances, shunt connections divide them (12-05);
- a loop is as stable as its phase margin, and compensation trades bandwidth for margin; the unity-gain frequency is $g_{m1}/C_c$ in rad/s (12-06);
- output stages trade linearity for efficiency, and heat, not transistors, usually sets the power rating (12-07);
- slew rate is a current divided by a capacitance, and $\text{SR}/\omega_u$ is the input pair's overdrive for a MOS pair, $2V_T$ for a bipolar one (12-08);
- an oscillator's frequency is set where the loop phase is zero and its amplitude by a nonlinearity (12-09);
- noise power adds, the first stage dominates, and kT/C ties resolution to capacitance and power (12-10).

The [equation sheet](../../reference/equation-sheets/12-electronics-2.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes. It allows a calculator and the equation sheet, but not Python or a simulator. Aim for at least 70%. Questions 1 to 12 follow the chapters; Question 13 asks for three short derivations; Question 14 is a diligence question built around a sensor start-up's noise claim, graded against a rubric. The course maps onto the FE Electrical and Computer exam's Electronics area ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/12-electronics-2.csv) (93 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Analog claims hide their conditions. This course teaches you to ask:

- what the gain, bandwidth and margin are at the worst process corner, load and temperature, not typical;
- whether a slew-rate, settling or bandwidth claim is limited by current, and what that current costs in power;
- what limits a power amplifier's rating (supply, current or heat), and what its efficiency is at typical, not peak, output;
- whether a noise figure is physically possible for the stated current (input noise power falls only as $1/g_m$), and over what bandwidth it is integrated;
- how a frequency reference holds its accuracy over temperature and life, and where a clock's phase noise comes from.
