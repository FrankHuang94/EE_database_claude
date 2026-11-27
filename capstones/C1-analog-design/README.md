# Capstone C1 · Analog Design in ngspice

**Choose one option.** Design either a two-stage CMOS op-amp (option A) or a synchronous buck converter with its control loop (option B). Verify it in ngspice against a written specification, across process, voltage and temperature, and write it up the way a design review would expect.

| | |
|---|---|
| **Prerequisites** | [Course 20](../../courses/20-analog-and-mixed-signal-ic-design/README.md) for option A, [Course 22](../../courses/22-power-electronics-and-energy-conversion/README.md) for option B; both build on [Course 12](../../courses/12-electronics-2/README.md) and [Course 15](../../courses/15-control-systems/README.md) |
| **Estimated hours** | About 40 |
| **Tools** | ngspice (the version CI uses), Python with numpy and scipy; no commercial tools or foundry kits |
| **Deliverables** | Design report, hand calculations, netlists with automated specification checks, PVT corner results |

**What it demonstrates.** That you can turn a specification into a circuit by first-principles hand analysis, predict its performance, confirm and correct the prediction in simulation, and show that it holds across corners. These are the skills a design review tests, and the ones a technical diligence conversation probes (Course 28's question banks AM1–AM8 and P1–P7).

---

## The process and models

Option A uses the C1 teaching process, [models/c1_process.lib](models/c1_process.lib): a 1.8 V, 0.18 µm-class CMOS process described by SPICE level-1 models with SS, TT, FF, SF and FS corners. They are square-law models with one channel-length modulation coefficient (characterized at $L$ = 0.5 µm), Meyer gate capacitance and junction capacitance. They have no mismatch, no flicker noise and no short-channel effects. That is deliberate: hand analysis and simulation then share the same physics, so any disagreement teaches something. Never use them to predict real silicon.

Option B uses ideal switches with on-resistance (the `sw` element), an inductor with series resistance, and a capacitor with equivalent series resistance. Loss terms are listed in the specification.

## Option A · Two-stage CMOS op-amp

**Brief.** Design a two-stage operational amplifier for a 1.8 V mixed-signal block. It drives a 2 pF on-chip load and is used as a unity-gain buffer and in switched-capacitor stages.

| Parameter | Requirement | Checked at |
|---|---|---|
| Open-loop DC gain | ≥ 65 dB | all corners |
| Unity-gain frequency | ≥ 25 MHz | all corners |
| Phase margin, unity-gain follower | ≥ 60° | all corners |
| Slew rate, both edges, 20%–80% of a 0.6 V step | ≥ 20 V/µs | all corners |
| Output range, where a gain-of-−1 stage keeps its gain within 1% | at least 0.25 V to $V_{DD}$ − 0.25 V | all corners |
| Tail-source $V_{DS} - V_{DSAT}$ at $V_{CM}$ = 0.9 V | ≥ 50 mV | all corners |
| Supply power, including the bias branch | ≤ 500 µW | all corners |
| Input-referred noise at 1 MHz | ≤ 15 nV/√Hz | TT, 27 °C, 1.8 V |
| CMRR and PSRR+ at DC | ≥ 60 dB each | TT, 27 °C, 1.8 V |

**Conditions.** $V_{DD}$ = 1.8 V ± 10%; −40 °C to 125 °C; corners SS, TT and FF, each at cold-high (−40 °C, 1.98 V), nominal (27 °C, 1.80 V) and hot-low (125 °C, 1.62 V), plus SF and FS at nominal. Load 2 pF; input common mode 0.9 V. A 20 µA reference current is available. Use $L$ = 0.5 µm for every transistor.

**Reference solution:** [design report](option-a-opamp/design-report.md), [results at eleven corners](option-a-opamp/results.md), [netlists](option-a-opamp/corners/) and the [corner generator](option-a-opamp/gen_corners.py). Open them only after your own design passes, or when you are stuck at a milestone.

## Option B · Synchronous buck converter with voltage-mode control

**Brief.** Design a 1.2 V point-of-load converter that runs from one lithium-ion cell and powers a wearable's processor core.

| Parameter | Requirement | Checked at |
|---|---|---|
| Output voltage | 1.2 V, within ±1% in steady state | all corners, 0.1 A and 1 A |
| Output ripple, peak-to-peak | ≤ 10 mV | 4.2 V input, 1 A (worst case) |
| Load step 0.1 A → 0.6 A in 100 ns | deviation ≤ 36 mV (3%); back within 1% in ≤ 30 µs | all input voltages |
| Loop crossover | 50 kHz to $f_{sw}/10$ | all corners |
| Phase margin and gain margin | ≥ 45° and ≥ 10 dB | all corners |
| Efficiency at 0.5 A, 3.6 V, 27 °C | ≥ 85% | nominal |
| Peak inductor current | ≤ 1.5 A (the inductor's saturation rating) | 1 A, worst input and inductance |

**Conditions.** Input 3.0 V to 4.2 V. Switching frequency 2 MHz, fixed. Load 0.1 A to 1 A, continuous conduction. Corners: input {3.0, 3.6, 4.2} V; inductance ±20%; output capacitance −20% (DC-bias derating) and nominal; switch on-resistance at 27 °C and at 125 °C (+40%). Losses to model: high-side switch 50 mΩ and low-side 30 mΩ at 27 °C; inductor DCR 20 mΩ; capacitor ESR 3 mΩ; gate-drive loss 2 nC per switch per cycle at 3.6 V; dead time 10 ns per edge with a 0.7 V body-diode drop; a fixed 1 mA controller quiescent current. PWM ramp amplitude 1 V. The error amplifier may be ideal with finite gain (80 dB) and a 10 MHz gain-bandwidth.

**Reference solution:** [design report](option-b-buck/design-report.md), [results](option-b-buck/results.md) (30 loop corners, load steps, switching-model efficiency, ripple and peak current), the [averaged](option-b-buck/buck_avg.sub) and [switching](option-b-buck/buck_sw.sub) models, and the [netlist generator](option-b-buck/gen_buck.py). Open them only after your own design passes, or when you are stuck at a milestone.

## Milestones

Each milestone ends with something a reviewer can check. Spend about the hours shown; if a milestone takes much longer, stop and look at the matching part of the reference.

| # | Milestone | Output | Hours |
|---|---|---|---|
| M1 | **Specification and architecture.** Restate every requirement with its test conditions; choose the topology and justify it against one alternative | One page | 3 |
| M2 | **Hand design.** Size every component from the specification, with each step derived; predict every specified quantity | Calculation sheet or script | 10 |
| M3 | **Nominal simulation.** Build testbenches that measure each specification automatically (`.meas` with pass/fail); compare with M2 and explain each difference above 10% | Netlists and a comparison table | 10 |
| M4 | **Corners.** Run every corner; find the worst corner for each specification; fix failures by redesign, not by tuning one corner | Corner table, design changes | 10 |
| M5 | **Report.** Write up M1 to M4, with tradeoffs and limitations, at design-review quality. The reference reports are condensed, about half this length, and leave out the narrative a reviewer expects; write yours in full | Report of 8 to 15 pages | 7 |

## Rubric (100 points)

| Criterion | Points | Full credit |
|---|---|---|
| Specification and architecture | 10 | Every requirement has test conditions; the topology choice weighs at least one real alternative |
| Hand analysis | 25 | Every component value is derived; predictions cover every specification; the model's assumptions are stated |
| Testbenches | 15 | Each specification is measured automatically, with the measurement definition stated (e.g., 20%–80% for slew) |
| Agreement and explanation | 15 | Hand and simulated values are compared; differences above 10% are explained physically, not just reported |
| Corners | 20 | All required corners run; the worst corner is identified per specification; every requirement passes |
| Report quality | 10 | Clear, reproducible (netlists run as delivered), with tradeoffs and limitations stated |
| Judgment | 5 | Margins are deliberate; the report says which specification is most at risk and why |

A passing project scores 70 or more and meets every requirement at every corner. A design that misses a requirement can still score well if the report diagnoses the miss correctly and shows the redesign that would fix it.

## Running the reference checks

```bash
python tools/run_spice.py C1
```

```bash
python tools/run_verify.py C1
```

The first re-runs every reference netlist and compares it with the published results; the second recomputes the hand calculations in the reports and checks every requirement at every corner. To regenerate the netlists and results after a design change, run `python gen_corners.py --run` in [option-a-opamp/](option-a-opamp/) or `python gen_buck.py --run` in [option-b-buck/](option-b-buck/).
