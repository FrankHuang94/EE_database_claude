<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 24 · High-Speed I/O, Signal Integrity and Photonics

Moving bits between chips at hundreds of gigabits per second: loss, reflection and crosstalk; eye diagrams and jitter; SerDes architecture and equalization; PCIe, CXL, Ethernet, UCIe and NVLink/UALink; and the photonics (lasers, modulators, silicon photonics, linear-drive and co-packaged optics) that take over when copper runs out.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 59 |
| **University equivalents** | High-Speed Digital Design / Signal Integrity + Optoelectronics (senior/graduate elective); Stanford EE273 (historical); Berkeley EE290 high-speed links |
| **Textbook alignment** | Bogatin, *Signal and Power Integrity — Simplified*; Hall & Heck, *Advanced Signal Integrity for High-Speed Digital Designs*; Dally & Poulton, *Digital Systems Engineering*; Saleh & Teich, *Fundamentals of Photonics* |
| **Free courses** | MIT OCW 6.776 (links material); Texas A&M ECEN 720 High-Speed Links (public lecture notes, Palermo) |
| **Prerequisites** | [13 · Electromagnetics](../13-electromagnetics/README.md), [17 · Communication Systems](../17-communication-systems/README.md), [12 · Electronics II](../12-electronics-2/README.md) |
| **FE areas** | Electromagnetics, Communications, Digital Systems |
| **Deeper** | Companion repo(s): datacenter networking |

## Learning objectives

1. Compute channel loss, reflections and crosstalk and read eye diagrams and BER bathtubs.
2. Explain SerDes architecture (NRZ/PAM4, CTLE/FFE/DFE equalization, CDR, DSP-based receivers, FEC).
3. Compare interconnect standards (PCIe, CXL, Ethernet, UCIe, NVLink/UALink) by reach, bandwidth, latency and energy per bit.
4. Explain photonic components (lasers, modulators, photodetectors, fiber) and silicon photonics.
5. Evaluate linear-drive and co-packaged optics against pluggable optics.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [24-01 · Signal Integrity Fundamentals](chapters/24-01-signal-integrity-fundamentals.md) | 7 | 🏁 reviewed | [problems](problems/24-01-problems.md) · [solutions](solutions/24-01-solutions.md) · [lab](labs/24-01-lab/README.md) · [verify](verify/verify_24_01.py) |
| [24-02 · Eye Diagrams, Jitter and BER](chapters/24-02-eye-diagrams-jitter-ber.md) | 6 | 🏁 reviewed | [problems](problems/24-02-problems.md) · [solutions](solutions/24-02-solutions.md) · [lab](labs/24-02-lab/README.md) · [verify](verify/verify_24_02.py) |
| [24-03 · SerDes Architecture and Equalization](chapters/24-03-serdes-architecture.md) | 8 | 🏁 reviewed | [problems](problems/24-03-problems.md) · [solutions](solutions/24-03-solutions.md) · [lab](labs/24-03-lab/README.md) · [verify](verify/verify_24_03.py) |
| [24-04 · DSP-Based SerDes and FEC](chapters/24-04-dsp-serdes-and-fec.md) | 5 | 🏁 reviewed | [problems](problems/24-04-problems.md) · [solutions](solutions/24-04-solutions.md) · [lab](labs/24-04-lab/README.md) · [verify](verify/verify_24_04.py) |
| [24-05 · Interconnect Standards: PCIe, CXL and Ethernet](chapters/24-05-pcie-cxl-ethernet.md) | 6 | 🏁 reviewed | [problems](problems/24-05-problems.md) · [solutions](solutions/24-05-solutions.md) · [lab](labs/24-05-lab/README.md) · [verify](verify/verify_24_05.py) |
| [24-06 · Die-to-Die Links, Memory PHYs and Scale-Up Fabrics](chapters/24-06-d2d-memory-phys-scale-up.md) | 6 | 🏁 reviewed | [problems](problems/24-06-problems.md) · [solutions](solutions/24-06-solutions.md) · [lab](labs/24-06-lab/README.md) · [verify](verify/verify_24_06.py) |
| [24-07 · Photonics Fundamentals](chapters/24-07-photonics-fundamentals.md) | 8 | 🏁 reviewed | [problems](problems/24-07-problems.md) · [solutions](solutions/24-07-solutions.md) · [lab](labs/24-07-lab/README.md) · [verify](verify/verify_24_07.py) |
| [24-08 · Silicon Photonics and Optical Transceivers](chapters/24-08-silicon-photonics.md) | 6 | 🏁 reviewed | [problems](problems/24-08-problems.md) · [solutions](solutions/24-08-solutions.md) · [lab](labs/24-08-lab/README.md) · [verify](verify/verify_24_08.py) |
| [24-09 · Linear-Drive and Co-Packaged Optics](chapters/24-09-lpo-and-cpo.md) | 4 | 🏁 reviewed | [problems](problems/24-09-problems.md) · [solutions](solutions/24-09-solutions.md) · [lab](labs/24-09-lab/README.md) · [verify](verify/verify_24_09.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/24-high-speed-io-signal-integrity-and-photonics.csv) · [Equation sheet](../../reference/equation-sheets/24-high-speed-io-signal-integrity-and-photonics.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 24 is planned at about 59 hours: the chapters' own estimates add to 56, plus about 3 hours of review; allow a further 4.5 hours for the exam. Course 13 gave you transmission lines, skin depth and reflections; Course 17 pulse shaping, ISI, matched filters and coding; Course 12 differential pairs and frequency response; Course 03 Gaussian tails and confidence bounds; Course 09 photodiodes and lasers; and Course 23 the memory interfaces whose wires this course generalizes. This course follows a bit from one chip to another: across a board, through a SerDes, over a standard protocol, between chiplets, and finally out onto fiber.

The nine chapters fall into four blocks:

- **The channel (24-01 and 24-02).** Conductor, dielectric and roughness loss; reflections, stubs and crosstalk; pulse responses, eyes, jitter decomposition, BER and bathtubs; why every link now runs with FEC.
- **The transceiver (24-03 and 24-04).** Drivers, transmit FFE, CTLE, DFE and CDR; ADC-and-DSP receivers, MLSD and the FEC stack, with their latency and power.
- **Protocols and fabrics (24-05 and 24-06).** PCIe, CXL and Ethernet rates, encodings, credits and retry; die-to-die links, memory PHYs and scale-up fabrics, and the energy-per-bit ladder that orders them.
- **Light (24-07 to 24-09).** Fiber, lasers, modulators, receivers and link budgets; silicon photonics, coupling, integration and pluggable transceivers; linear-drive and co-packaged optics and how to judge their claims.

Work at least the [A] and [B] problems of every chapter. The labs are of two kinds, both run in CI (the verify scripts, `run_spice.py` for the netlists' EXPECT lines, and `run_notebooks.py` for the notebooks):

- ngspice netlists: coupled-line crosstalk and a via stub (24-01), a pulse response (24-02), a CTLE (24-03), a distributed die-to-die wire (24-06), a shunt-feedback TIA (24-07) and a ring modulator driven through a wire bond and a hybrid bond (24-08);
- Python models imported by their notebooks: `si.py`, `eye.py`, `serdes.py`, `dsp.py` (with a Viterbi detector), `links.py` (with a credit simulator), `d2d.py`, `optics.py` (with an FFT fiber propagator), `siph.py` and `cpo.py` (with a Monte Carlo of zero-failure tests).

**What to master cold.** The [equation sheet](../../reference/equation-sheets/24-high-speed-io-signal-integrity-and-photonics.md) collects the relations; these are the ideas behind them:

- loss is specified at the Nyquist frequency; conductor loss grows as $\sqrt f$ and dielectric loss as $f$, so dielectric loss wins at high rates; every impedance step reflects, and every stub notches (24-01);
- an eye is set by the main cursor minus the ISI; BER falls as a Gaussian tail of the eye-to-noise ratio, so a few dB of margin are worth orders of magnitude; total jitter is quoted at a BER (24-02);
- equalizers mostly lose low-frequency gain rather than add high-frequency gain; the DFE removes post-cursors without amplifying noise but must close its loop in one UI (24-03);
- long-reach SerDes moved to ADCs and DSP because DSP scales with CMOS; MLSD and FEC buy dB at a cost in power and latency (24-04);
- protocol bandwidth is lanes × rate × efficiency; buffers scale with bandwidth × round-trip time; the PCIe cadence doubles every three years (24-05);
- short unterminated wires cost $CV^2/4$; areal density scales as $1/\text{pitch}^2$; the energy ladder runs from die-to-die links through scale-up fabrics to optics (24-06);
- light is detected in proportion to power, so optical dB are half electrical dB; dispersion spread in UI grows as the square of the symbol rate; sensitivity is $Q\sigma/\mathcal R$ plus penalties (24-07);
- silicon guides but cannot detect or lase; coupling and packaging set much of the loss and cost; retimed links add BER while linear ones add $1/Q^2$ (24-08);
- LPO and CPO cut optics power by removing the DSP and shortening the electrical path; their cost is margin, serviceability and supplier choice, and zero failures bound a failure rate only to $3/T$ (24-09).

**After this course.** Course 25 makes and packages the chips these links connect (advanced packaging, hybrid bonding, test and reliability physics). Course 27 assembles whole systems, where 24-06's energy ladder and 24-09's optics budgets decide an AI cluster's power. The companion repo *Datacenter Networking* continues from 24-05 and 24-09 into fabric design and operations.
