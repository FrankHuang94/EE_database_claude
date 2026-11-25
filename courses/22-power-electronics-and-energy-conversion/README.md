<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 22 · Power Electronics and Energy Conversion

Converting and delivering power efficiently, from wearables to AI racks: switching converters and magnetics, converter control, LDO vs switcher tradeoffs, PMICs, batteries, datacenter power delivery, wide-bandgap devices, plus the machines and power-system fundamentals the FE exam expects.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 92 |
| **University equivalents** | Power Electronics (senior) + Electric Machines and Power Systems (intro); MIT 6.334; Berkeley EE113; Berkeley EE137A |
| **Textbook alignment** | Erickson & Maksimović, *Fundamentals of Power Electronics*; Mohan, Undeland & Robbins, *Power Electronics: Converters, Applications, and Design*; Glover, Overbye & Sarma, *Power System Analysis and Design* (power-systems chapters); Chapman, *Electric Machinery Fundamentals* (machines chapter) |
| **Free courses** | MIT OCW 6.334 Power Electronics; University of Colorado Boulder power electronics specialization (Coursera, Erickson) |
| **Prerequisites** | [07 · Circuit Analysis II (Transient and AC)](../07-circuit-analysis-2-transient-and-ac/README.md), [10 · Electronics I (Microelectronic Circuits)](../10-electronics-1/README.md), [15 · Control Systems](../15-control-systems/README.md) |
| **FE areas** | Power Systems, Electronics |

## Learning objectives

1. Analyze buck, boost, buck-boost and flyback converters in steady state with volt-second and charge balance.
2. Design inductors and transformers for converters and estimate losses.
3. Model converter dynamics and design voltage- and current-mode control loops.
4. Compare LDOs and switching regulators, and explain PMIC, battery-charging and fuel-gauge architecture.
5. Analyze datacenter power delivery (48 V distribution, VRMs, PDN impedance, IR drop) and the role of GaN and SiC.
6. Solve FE-level machines and power-systems problems (three-phase, per-unit, transformers, transmission, power flow, faults).

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [22-01 · Power Conversion Principles](chapters/22-01-power-conversion-principles.md) | 6 | ✅ verified | [problems](problems/22-01-problems.md) · [solutions](solutions/22-01-solutions.md) · [lab](labs/22-01-lab/README.md) · [verify](verify/verify_22_01.py) |
| [22-02 · Steady-State Analysis and the Buck Converter](chapters/22-02-buck-converter-steady-state.md) | 9 | ✅ verified | [problems](problems/22-02-problems.md) · [solutions](solutions/22-02-solutions.md) · [lab](labs/22-02-lab/README.md) · [verify](verify/verify_22_02.py) |
| [22-03 · Boost, Buck-Boost and Other Topologies](chapters/22-03-boost-buck-boost-topologies.md) | 7 | ✅ verified | [problems](problems/22-03-problems.md) · [solutions](solutions/22-03-solutions.md) · [lab](labs/22-03-lab/README.md) · [verify](verify/verify_22_03.py) |
| [22-04 · Isolated Converters: Flyback and Forward](chapters/22-04-isolated-converters.md) | 6 | ✅ verified | [problems](problems/22-04-problems.md) · [solutions](solutions/22-04-solutions.md) · [lab](labs/22-04-lab/README.md) · [verify](verify/verify_22_04.py) |
| [22-05 · Magnetics Design](chapters/22-05-magnetics-design.md) | 7 | ✅ verified | [problems](problems/22-05-problems.md) · [solutions](solutions/22-05-solutions.md) · [lab](labs/22-05-lab/README.md) · [verify](verify/verify_22_05.py) |
| [22-06 · Converter Losses and Wide-Bandgap Switches](chapters/22-06-converter-losses-and-wide-bandgap.md) | 7 | ✅ verified | [problems](problems/22-06-problems.md) · [solutions](solutions/22-06-solutions.md) · [lab](labs/22-06-lab/README.md) · [verify](verify/verify_22_06.py) |
| [22-07 · Converter Dynamics and Control](chapters/22-07-converter-dynamics-and-control.md) | 9 | ✅ verified | [problems](problems/22-07-problems.md) · [solutions](solutions/22-07-solutions.md) · [lab](labs/22-07-lab/README.md) · [verify](verify/verify_22_07.py) |
| [22-08 · PMICs and Power Management for SoCs](chapters/22-08-pmics.md) | 6 | ✅ verified | [problems](problems/22-08-problems.md) · [solutions](solutions/22-08-solutions.md) · [lab](labs/22-08-lab/README.md) · [verify](verify/verify_22_08.py) |
| [22-09 · Batteries, Charging and Fuel Gauging](chapters/22-09-batteries-charging-fuel-gauging.md) | 8 | ✅ verified | [problems](problems/22-09-problems.md) · [solutions](solutions/22-09-solutions.md) · [lab](labs/22-09-lab/README.md) · [verify](verify/verify_22_09.py) |
| [22-10 · Datacenter Power Delivery](chapters/22-10-datacenter-power-delivery.md) | 8 | ✅ verified | [problems](problems/22-10-problems.md) · [solutions](solutions/22-10-solutions.md) · [lab](labs/22-10-lab/README.md) · [verify](verify/verify_22_10.py) |
| [22-11 · Electric Machines and Drives](chapters/22-11-electric-machines.md) | 6 | ✅ verified | [problems](problems/22-11-problems.md) · [solutions](solutions/22-11-solutions.md) · [lab](labs/22-11-lab/README.md) · [verify](verify/verify_22_11.py) |
| [22-12 · Power Systems Fundamentals](chapters/22-12-power-systems-fundamentals.md) | 8 | ✅ verified | [problems](problems/22-12-problems.md) · [solutions](solutions/22-12-solutions.md) · [lab](labs/22-12-lab/README.md) · [verify](verify/verify_22_12.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/22-power-electronics-and-energy-conversion.csv) · [Equation sheet](../../reference/equation-sheets/22-power-electronics-and-energy-conversion.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 22 is planned at about 92 hours: the chapters' own estimates add to 87, plus 5 hours of review and the exam. Course 07 gave you transients, phasors, AC power and three-phase circuits; Course 10 diodes and MOSFETs; Course 15 transfer functions, Bode plots and phase margin; and 09-13 the wide-bandgap materials. This course turns them into the power path of every product, from a ring's battery to an AI rack: how converters work and are built, how they are controlled, how a battery and a PMIC run a wearable, how a datacenter delivers a kiloampere to a die, and the machines and grid that the FE exam expects.

The twelve chapters fall into five blocks:

- **Converters (22-01 to 22-04).** Why switching beats linear regulation and the two rules no topology may break; volt-second and charge balance, the buck in continuous and discontinuous conduction, ripple and RMS ratings; the boost, buck-boost, SEPIC and Ćuk, and the boost's gain limit; flyback, forward and bridge converters, leakage and reset.
- **Building them (22-05 and 22-06).** Gapped cores, saturation, core loss from Steinmetz to the iGSE, skin and proximity effects, area-product design; overlap, output-charge, recovery and gate losses, the device-size optimum, wide-bandgap switches and zero-voltage switching.
- **Control (22-07).** Averaged models, the boost's right-half-plane zero, type-III compensation by the k-factor method, peak current mode and slope compensation, load steps and digital delay.
- **Products (22-08 to 22-10).** PMIC rail allocation, PFM and PWM, usage-profile battery life, DVS, AVS, soft start and power gating; lithium-ion cells, their equivalent circuit, CC/CV charging, fuel gauging and aging; the datacenter chain from grid to transistor, higher distribution voltages, multiphase regulators, load lines, target impedance and the first droop.
- **Machines and the grid (22-11 and 22-12).** DC, induction and synchronous machines, V/f and field weakening, inverter voltage limits; per-unit analysis, line parameters and SIL, two-bus power flow, faults, inertia, droop and the large-load problem.

Work at least the [A] and [B] problems of every chapter. The labs are of two kinds, both run in CI (the verify scripts, `run_spice.py` for the netlists' EXPECT lines, and `run_notebooks.py` for the notebooks):

- ngspice netlists: an ideal buck, capacitor charging and an LDO (22-01), a buck in continuous and discontinuous conduction (22-02), boosts and a SEPIC (22-03), a flyback and a forward converter with reset winding (22-04), a saturating gapped core and leakage tests (22-05), a half bridge's hard turn-on and a ZVS transition (22-06), a closed type-III loop and the averaged boost (22-07), a DVS ramp and a domain's soft start (22-08), a load pulse and a CC/CV charge (22-09), the package resonance and four interleaved phases (22-10), an induction motor's equivalent circuit and a DC motor start (22-11), and two-bus power flow and a frequency excursion (22-12);
- Python models imported by their notebooks: `power.py`, `buck.py`, `topologies.py`, `isolated.py`, `magnetics.py`, `losses.py`, `control.py`, `pmic.py`, `battery.py`, `pdn.py`, `machines.py` and `grid.py`.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/22-power-electronics-and-energy-conversion.md) collects the relations; these are the ideas behind them:

- loss, not efficiency, is what you design and cool; an LDO can never beat $V_{out}/V_{in}$; switches must never short a capacitor or open an inductor (22-01);
- every DC ratio comes from volt-second and charge balance; ripple sets $L$ and $C$, RMS current sets heating, and light load changes the mode (22-02);
- a boost's currents grow as $1/D'$ and its gain is capped by resistance; the buck-boost family pays for flexibility in switch stress (22-03);
- a flyback stores energy and a forward converter transfers it; leakage costs more than its own energy, and every core must be reset (22-04);
- the gap stores the energy; core loss depends on waveform as well as peak flux; proximity effect, not skin effect, dominates multilayer windings; the optimum puts $P_{fe}/P_{cu} = 2/\beta$ (22-05);
- a hard turn-on costs $Q_{oss}V$, recovery $Q_{rr}V$; the best switch size balances conduction and charge losses, so only the figure of merit $R \cdot Q$ lowers the minimum; ZVS removes switching loss at the price of circulating current (22-06);
- a buck's plant is a double pole, a boost's adds a right-half-plane zero; type III buys the phase; above $D$ = 0.5 peak current mode needs slope compensation; delay eats phase margin (22-07);
- a PMIC is an energy budget: the right converter per rail and mode per load, battery life from the usage profile, and every voltage step or power gate a capacitor to charge (22-08);
- a cell is an OCV curve behind resistances; CV charging is an RC decay with a thousand-farad capacitor; gauges drift and re-anchor at rest; calendar fade follows $\sqrt t$ (22-09);
- loss falls as $1/V^2$, so distribution voltage rises; interleaving divides ripple, load lines use the whole window, and the package resonance sets the first droop (22-10);
- $ei = T\omega$ in every machine; slip carries an induction motor's torque and its rotor loss; a synchronous machine's angle sets power and its field sets reactive power; V/f holds flux (22-11);
- per-unit removes transformers; angle moves real power and voltage magnitude moves reactive power; faults scale as $1/Z$; inertia sets the first second and droop the minutes after (22-12).

**Course resources.** The [final exam](exam/README.md) (14 questions, 120 points, 240 minutes) has fully worked [solutions](exam/solutions.md) checked by `verify/verify_22_exam.py`; the [flashcards](../../flashcards/22-power-electronics-and-energy-conversion.csv) cover every chapter.
