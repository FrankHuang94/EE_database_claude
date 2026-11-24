<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 21 · RF and Microwave Engineering

Radio hardware from S-parameters to standards: matching, noise figure and linearity, LNAs, mixers, VCOs and power amplifiers, transceiver architectures, the RF front end, antennas and beamforming, link budgets, modem baseband architecture and today's wireless standards.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 91 |
| **University equivalents** | RF/Microwave Engineering + RF IC Design (senior/first-year graduate); Berkeley EE142; Stanford EE314A; MIT 6.776 |
| **Textbook alignment** | Pozar, *Microwave Engineering*; Razavi, *RF Microelectronics*; Lee, *The Design of CMOS Radio-Frequency Integrated Circuits* |
| **Free courses** | MIT OCW 6.776 High Speed Communication Circuits; Berkeley EE142 (public materials) |
| **Prerequisites** | [12 · Electronics II](../12-electronics-2/README.md), [13 · Electromagnetics](../13-electromagnetics/README.md), [17 · Communication Systems](../17-communication-systems/README.md) |
| **FE areas** | Electromagnetics, Communications, Electronics |

## Learning objectives

1. Use S-parameters and design lumped and distributed matching networks.
2. Compute cascaded noise figure, P1dB, IP3 and dynamic range of a receiver chain.
3. Analyze LNAs, mixers, VCOs and PAs and the efficiency–linearity tradeoff (including envelope tracking and DPD).
4. Compare transceiver architectures and front-end components (filters, switches, duplexers).
5. Compute link budgets and explain antenna arrays, beamforming and mmWave constraints.
6. Map modem architecture and wireless standards (cellular, Wi-Fi, BLE, UWB, GNSS, NTN) to the underlying RF and comms concepts.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [21-01 · S-Parameters and Network Analysis](chapters/21-01-s-parameters.md) | 8 | ✅ verified | [problems](problems/21-01-problems.md) · [solutions](solutions/21-01-solutions.md) · [lab](labs/21-01-lab/README.md) · [verify](verify/verify_21_01.py) |
| [21-02 · Impedance Matching Networks](chapters/21-02-impedance-matching-networks.md) | 7 | ✅ verified | [problems](problems/21-02-problems.md) · [solutions](solutions/21-02-solutions.md) · [lab](labs/21-02-lab/README.md) · [verify](verify/verify_21_02.py) |
| [21-03 · Noise Figure and Linearity](chapters/21-03-noise-figure-and-linearity.md) | 8 | ✅ verified | [problems](problems/21-03-problems.md) · [solutions](solutions/21-03-solutions.md) · [lab](labs/21-03-lab/README.md) · [verify](verify/verify_21_03.py) |
| [21-04 · Low-Noise Amplifiers](chapters/21-04-low-noise-amplifiers.md) | 7 | ✅ verified | [problems](problems/21-04-problems.md) · [solutions](solutions/21-04-solutions.md) · [lab](labs/21-04-lab/README.md) · [verify](verify/verify_21_04.py) |
| [21-05 · Mixers](chapters/21-05-mixers.md) | 6 | ✅ verified | [problems](problems/21-05-problems.md) · [solutions](solutions/21-05-solutions.md) · [lab](labs/21-05-lab/README.md) · [verify](verify/verify_21_05.py) |
| [21-06 · Oscillators and VCOs](chapters/21-06-oscillators-and-vcos.md) | 6 | ✅ verified | [problems](problems/21-06-problems.md) · [solutions](solutions/21-06-solutions.md) · [lab](labs/21-06-lab/README.md) · [verify](verify/verify_21_06.py) |
| [21-07 · Power Amplifiers](chapters/21-07-power-amplifiers.md) | 9 | ✅ verified | [problems](problems/21-07-problems.md) · [solutions](solutions/21-07-solutions.md) · [lab](labs/21-07-lab/README.md) · [verify](verify/verify_21_07.py) |
| [21-08 · Transceiver Architectures](chapters/21-08-transceiver-architectures.md) | 7 | ✅ verified | [problems](problems/21-08-problems.md) · [solutions](solutions/21-08-solutions.md) · [lab](labs/21-08-lab/README.md) · [verify](verify/verify_21_08.py) |
| [21-09 · The RF Front End: Filters, Switches and Modules](chapters/21-09-rf-front-end.md) | 6 | ✅ verified | [problems](problems/21-09-problems.md) · [solutions](solutions/21-09-solutions.md) · [lab](labs/21-09-lab/README.md) · [verify](verify/verify_21_09.py) |
| [21-10 · Antennas, Arrays, Beamforming and mmWave](chapters/21-10-antennas-arrays-mmwave.md) | 8 | ✅ verified | [problems](problems/21-10-problems.md) · [solutions](solutions/21-10-solutions.md) · [lab](labs/21-10-lab/README.md) · [verify](verify/verify_21_10.py) |
| [21-11 · Link Budgets](chapters/21-11-link-budgets.md) | 5 | ✅ verified | [problems](problems/21-11-problems.md) · [solutions](solutions/21-11-solutions.md) · [lab](labs/21-11-lab/README.md) · [verify](verify/verify_21_11.py) |
| [21-12 · Modem Baseband Architecture and Wireless Standards](chapters/21-12-modem-baseband-and-standards.md) | 9 | ✅ verified | [problems](problems/21-12-problems.md) · [solutions](solutions/21-12-solutions.md) · [lab](labs/21-12-lab/README.md) · [verify](verify/verify_21_12.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/21-rf-and-microwave-engineering.csv) · [Equation sheet](../../reference/equation-sheets/21-rf-and-microwave-engineering.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 21 is planned at about 91 hours: the chapters' own estimates add to 86, plus 5 hours of review and the exam. Course 12 gave you differential pairs, frequency response, output stages and oscillators; Course 13 transmission lines, the Smith chart and antennas; Course 17 noise, modulation, OFDM, MIMO and wireless channels; and Course 20 phase noise, PLLs and data-converter metrics. This course turns them into radios: how RF signals are measured and matched, how each block of a transceiver is designed and where it fails, how the blocks are arranged, and how a link and a standard set the specifications in the first place.

The twelve chapters fall into five blocks:

- **Waves and matching (21-01 and 21-02).** Power waves and S-parameters, conversions, VNA calibration and de-embedding, stability and maximum gain; L, π and multi-section matching, component loss and the Bode–Fano limit.
- **Receiver building blocks (21-03 to 21-06).** Noise figure, noise parameters and the Friis cascade; compression, intercept points, blocking and dynamic range; LNAs from resistive termination to inductive degeneration and noise cancelling; switching mixers, image rejection, harmonic rejection and N-path filters; LC oscillators, phase noise from Leeson to the ISF, tuning, quadrature and injection locking.
- **The transmitter (21-07).** Load lines, conduction-angle classes A to C, switching classes E and F, PAPR and back-off, ACLR from IIP3, Doherty, envelope tracking and digital predistortion.
- **Systems (21-08 and 21-09).** Superheterodyne, zero-IF, low-IF and direct-sampling architectures with their frequency plans; acoustic filters, duplexers, SOI switches, tuners and front-end modules.
- **The air interface and standards (21-10 to 21-12).** Patches, the Chu limit, phased arrays, squint, quantization and the DC-optimal array; link budgets from BLE to satellite and GNSS; modem datapaths, peak-rate and buffer arithmetic, Wi-Fi rates, UWB and Bluetooth ranging, GNSS and NTN.

Work at least the [A] and [B] problems of every chapter. The labs are of two kinds, both run in CI (the verify scripts, `run_spice.py` for the netlists' EXPECT lines, and `run_notebooks.py` for the notebooks):

- ngspice netlists: three two-ports by `.sp` analysis (21-01), three matching networks (21-02), a bipolar transistor's distortion (21-03), the noise figure of four LNA inputs (21-04), commutating mixers and a 4-path filter (21-05), an LC oscillator and an RC-CR quadrature network (21-06), an ideal class-E PA and a symmetric Doherty (21-07), a Butterworth preselector and a complex filter (21-08), an acoustic ladder filter and an RF switch (21-09), and a squinting array (21-10);
- Python models imported by their notebooks: `sparam.py`, `match.py`, `rfnl.py`, `lna.py`, `mixer.py`, `vco.py`, `pa.py`, `trx.py`, `frontend.py`, `antenna.py`, `linkbudget.py` and `modem.py`.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/21-rf-and-microwave-engineering.md) collects the relations; these are the ideas behind them:

- S-parameters are ratios of waves into matched loads; reciprocity and losslessness check data, and K, Δ and μ decide whether any passive termination can make a device oscillate (21-01);
- an L-network's Q is fixed by the resistance ratio and sets its bandwidth; component Q sets its loss; Bode–Fano bounds every network (21-02);
- the first stage sets the noise figure and the last stages the linearity; a third-order intercept sits about 9.6 dB above P1dB, and blockers set both linearity and phase-noise specifications (21-03);
- inductive degeneration makes a 50 Ω input without a resistor; the gate inductor's loss, not the transistor, often limits the noise figure (21-04);
- a switching mixer's gain is 2/π; image rejection is limited by I/Q matching to about $4/(\varepsilon^2 + \theta^2)$ (21-05);
- phase noise falls with tank Q squared and with signal power; dividing by N improves it by 20 log N (21-06);
- PA efficiency collapses in back-off; Doherty and envelope tracking recover it, DPD buys back linearity, and neither exceeds saturation (21-07);
- architectures trade image, DC-offset, I/Q and ADC problems against each other; frequency plans are checked for images and spurs before anything is designed (21-08);
- acoustic coupling sets filter bandwidth, TCF eats duplex gaps, and an SOI switch is judged by $R_{on}C_{off}$ and its stack (21-09);
- EIRP grows as $N^2$; phase shifters squint, bits set a scattered-power floor, and the DC-optimal array balances PA and overhead power (21-10);
- a budget is a ledger: each dB is worth $10^{1/(10n)}$ in range, margins dominate, and cellular is uplink-limited (21-11);
- peak rates, buffers and ranging errors follow from a few formulas, and every headline number has a matching memory, power or clock-accuracy cost (21-12).

**Course resources.** The [final exam](exam/README.md) (14 questions, 120 points, 240 minutes) has fully worked [solutions](exam/solutions.md) checked by `verify/verify_21_exam.py`; the [flashcards](../../flashcards/21-rf-and-microwave-engineering.csv) cover every chapter.
