<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 20 · Analog and Mixed-Signal IC Design

Designing analog and mixed-signal blocks in CMOS: gm/ID methodology, two-stage op-amps, bandgap references, LDOs, comparators, data converters (SAR, pipeline, sigma-delta, flash, DACs), PLLs and jitter, layout and matching, and why analog does not scale like digital.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 104 |
| **University equivalents** | Analog IC Design + Data Converters (senior/first-year graduate); Berkeley EE140/240A; Stanford EE214A |
| **Textbook alignment** | Razavi, *Design of Analog CMOS Integrated Circuits*; Carusone, Johns & Martin, *Analog Integrated Circuit Design*; Pelgrom, *Analog-to-Digital Conversion* |
| **Free courses** | Razavi's analog design lectures (UCLA, public video); NPTEL analog IC design courses |
| **Prerequisites** | [12 · Electronics II](../12-electronics-2/README.md), [09 · Semiconductor Devices](../09-semiconductor-devices/README.md) |
| **FE areas** | Electronics |

## Learning objectives

1. Size transistors with the gm/ID methodology to meet gain, bandwidth and power targets.
2. Design and compensate a two-stage op-amp to a specification and verify it in simulation.
3. Analyze bandgap references, LDOs and comparators.
4. Explain data-converter specifications and compare SAR, pipeline, sigma-delta and flash ADCs and DAC architectures.
5. Analyze PLL loop dynamics and jitter.
6. Explain matching, PVT variation and layout techniques, and why analog area and power do not shrink with digital scaling.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [20-01 · Analog Design Fundamentals in Nanometer CMOS](chapters/20-01-analog-design-fundamentals-gm-id.md) | 8 | ✅ verified | [problems](problems/20-01-problems.md) · [solutions](solutions/20-01-solutions.md) · [lab](labs/20-01-lab/README.md) · [verify](verify/verify_20_01.py) |
| [20-02 · Two-Stage Op-Amp Design](chapters/20-02-two-stage-op-amp-design.md) | 12 | ✅ verified | [problems](problems/20-02-problems.md) · [solutions](solutions/20-02-solutions.md) · [lab](labs/20-02-lab/README.md) · [verify](verify/verify_20_02.py) |
| [20-03 · Bandgap and Voltage References](chapters/20-03-bandgap-references.md) | 8 | ✅ verified | [problems](problems/20-03-problems.md) · [solutions](solutions/20-03-solutions.md) · [lab](labs/20-03-lab/README.md) · [verify](verify/verify_20_03.py) |
| [20-04 · Low-Dropout Regulators](chapters/20-04-ldo-regulators.md) | 8 | ✅ verified | [problems](problems/20-04-problems.md) · [solutions](solutions/20-04-solutions.md) · [lab](labs/20-04-lab/README.md) · [verify](verify/verify_20_04.py) |
| [20-05 · Comparators and Sample-and-Hold Circuits](chapters/20-05-comparators-and-sample-and-hold.md) | 8 | ✅ verified | [problems](problems/20-05-problems.md) · [solutions](solutions/20-05-solutions.md) · [lab](labs/20-05-lab/README.md) · [verify](verify/verify_20_05.py) |
| [20-06 · Data Converter Fundamentals](chapters/20-06-data-converter-fundamentals.md) | 7 | ✅ verified | [problems](problems/20-06-problems.md) · [solutions](solutions/20-06-solutions.md) · [lab](labs/20-06-lab/README.md) · [verify](verify/verify_20_06.py) |
| [20-07 · Nyquist ADCs: Flash, SAR and Pipeline](chapters/20-07-nyquist-adcs.md) | 10 | ✅ verified | [problems](problems/20-07-problems.md) · [solutions](solutions/20-07-solutions.md) · [lab](labs/20-07-lab/README.md) · [verify](verify/verify_20_07.py) |
| [20-08 · Oversampling and Sigma-Delta Converters](chapters/20-08-sigma-delta-converters.md) | 9 | ✅ verified | [problems](problems/20-08-problems.md) · [solutions](solutions/20-08-solutions.md) · [lab](labs/20-08-lab/README.md) · [verify](verify/verify_20_08.py) |
| [20-09 · DACs](chapters/20-09-dacs.md) | 6 | ✅ verified | [problems](problems/20-09-problems.md) · [solutions](solutions/20-09-solutions.md) · [lab](labs/20-09-lab/README.md) · [verify](verify/verify_20_09.py) |
| [20-10 · PLLs and Jitter](chapters/20-10-plls-and-jitter.md) | 10 | ✅ verified | [problems](problems/20-10-problems.md) · [solutions](solutions/20-10-solutions.md) · [lab](labs/20-10-lab/README.md) · [verify](verify/verify_20_10.py) |
| [20-11 · Layout, Matching and PVT Variation](chapters/20-11-layout-matching-pvt.md) | 7 | ✅ verified | [problems](problems/20-11-problems.md) · [solutions](solutions/20-11-solutions.md) · [lab](labs/20-11-lab/README.md) · [verify](verify/verify_20_11.py) |
| [20-12 · Why Analog Does Not Scale Like Digital](chapters/20-12-why-analog-does-not-scale.md) | 5 | ⬜ planned | — |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/20-analog-and-mixed-signal-ic-design.csv) · [Equation sheet](../../reference/equation-sheets/20-analog-and-mixed-signal-ic-design.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 20 is planned at about 104 hours: the chapters' own estimates add to 98, plus 6 hours of review and the exam. Course 10 gave you the transistor's circuit models, Course 12 differential pairs, cascodes and frequency response, Course 15 feedback and phase margin, Course 16 sampling and quantization, and Course 19 the CMOS process and its layout. This course turns those into working analog and mixed-signal blocks: how to size a transistor for a specification, how to build the amplifiers, references and regulators every chip needs, how data converters and clocks work and fail, and why analog is the part of a chip that does not shrink.

The twelve chapters fall into five blocks:

- **Designing with transistors (20-01 and 20-02).** The charge-based model from weak to strong inversion, $g_m/I_D$ sizing with its speed, gain and headroom trade-offs, and a two-stage op-amp designed from a specification sheet: pole splitting, nulling resistors, nested and indirect compensation, slewing and settling.
- **References and power (20-03 and 20-04).** Bandgap references from $V_{BE}(T)$, the magic voltage, curvature and what trimming can fix; LDO regulators, their loop stability, PSRR and load-step response.
- **Data conversion (20-05 to 20-09).** Sampling and comparators (kT/C, jitter, regeneration), the metrics that describe converters, Nyquist ADCs (flash, SAR, pipeline, interleaving), sigma-delta converters and DACs.
- **Clocking (20-10).** Charge-pump and all-digital PLLs, phase noise and jitter, and fractional-N synthesis.
- **Physical reality (20-11 and 20-12).** Mismatch, layout, corners and Monte Carlo; and why analog does not scale like digital, which ties the course together.

Work at least the [A] and [B] problems of every chapter. The labs are of two kinds, both run in CI (the verify scripts and `run_spice.py` for the netlists' EXPECT lines):

- ngspice netlists: a gain stage (20-01), the op-amp's loop, compensation variants, PSRR and slewing (20-02), two bandgaps (20-03), the LDO's loop and PSRR (20-04), kT/C, a switch and a latch (20-05), a resistor-ladder converter (20-06), an MDAC (20-07), a continuous-time sigma-delta loop (20-08), an R-2R ladder and output-impedance compression (20-09), a PLL's open loop (20-10), mismatched mirrors (20-11) and a cascode's headroom (20-12);
- Python models imported by their notebooks: `gmid.py`, `opamp.py`, `bandgap.py`, `ldo.py`, `sh.py`, `adc.py`, `nyq.py`, `dsm.py`, `dac.py`, `pll.py`, `matching.py` and `scaling.py`.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/20-analog-and-mixed-signal-ic-design.md) collects the relations; these are the ideas behind them:

- $g_m/I_D$ is the designer's dial: it sets efficiency, speed, gain and headroom at once, and width then scales the current (20-01);
- a two-stage op-amp is a pole-splitting exercise: the second stage's own capacitance bounds the non-dominant pole, and the feedforward zero must be tamed (20-02);
- a bandgap adds a falling $V_{BE}$ to a rising $V_T\ln N$; errors with a PTAT shape trim out, others do not (20-03);
- an LDO's loop crossover moves with its load current, and its PSRR is only as good as its loop gain at the ripple frequency (20-04);
- kT/C noise does not depend on the switch, jitter's cost grows with input frequency, and a latch needs time to resolve small inputs (20-05);
- 6.02N + 1.76 dB is the ceiling; DNL, INL, ENOB and the figures of merit tell you how far below it a converter sits and at what energy (20-06);
- flash spends comparators, SAR spends cycles, pipelines spend amplifiers, interleaving spends calibration (20-07);
- oversampling plus feedback shapes quantization noise out of band at 6L + 3 dB per octave, limited by stability and leakage (20-08);
- DAC linearity is matching and output impedance; DAC spectra are sinc-shaped (20-09);
- a PLL multiplies reference noise by N in band and suppresses VCO noise; jitter is integrated phase noise over a stated band (20-10);
- mismatch falls as one over the square root of area, gradients are cancelled by symmetry, and corners are not the worst case of every specification (20-11);
- noise-limited analog does not gain from lower supplies, cascodes cost headroom, and the industry's answer is digital assistance (20-12).

**Course resources.** The [final exam](exam/README.md) (14 questions, 120 points, 240 minutes) has fully worked [solutions](exam/solutions.md) checked by `verify/verify_20_exam.py`; the [flashcards](../../flashcards/20-analog-and-mixed-signal-ic-design.csv) cover every chapter.
