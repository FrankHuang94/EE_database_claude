<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 16 · Digital Signal Processing

Discrete-time signal processing for engineers who will build or buy DSP hardware: DTFT, DFT/FFT, spectral analysis, FIR and IIR design, multirate systems, quantization and fixed-point effects, and DSP hardware architectures.

| | |
|---|---|
| **Term** | 5 |
| **Study hours** | ≈ 83 |
| **University equivalents** | Digital Signal Processing (senior); MIT 6.341; Berkeley EE123 |
| **Textbook alignment** | Oppenheim & Schafer, *Discrete-Time Signal Processing*; Lyons, *Understanding Digital Signal Processing* |
| **Free courses** | MIT OCW 6.341 Discrete-Time Signal Processing; NPTEL digital signal processing courses |
| **Prerequisites** | [11 · Signals and Systems](../11-signals-and-systems/README.md), [05 · Programming for Engineers](../05-programming-for-engineers/README.md) |
| **FE areas** | Signal Processing |

## Learning objectives

1. Compute and interpret the DTFT, DFT and FFT, including leakage, windowing and resolution.
2. Design FIR filters (window method, Parks–McClellan) and IIR filters (bilinear transform) to specifications.
3. Design decimators and interpolators, including polyphase implementations.
4. Quantify quantization noise and fixed-point effects (coefficient quantization, overflow, limit cycles).
5. Map DSP algorithms onto hardware (MAC units, pipelining, CORDIC) and estimate their cost.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [16-01 · Discrete-Time Signals and Systems Review](chapters/16-01-discrete-time-systems-review.md) | 5 | ✅ verified | [problems](problems/16-01-problems.md) · [solutions](solutions/16-01-solutions.md) · [lab](labs/16-01-lab/README.md) · [verify](verify/verify_16_01.py) |
| [16-02 · DTFT and z-Transform for DSP](chapters/16-02-dtft-and-z-transform-for-dsp.md) | 6 | ✅ verified | [problems](problems/16-02-problems.md) · [solutions](solutions/16-02-solutions.md) · [lab](labs/16-02-lab/README.md) · [verify](verify/verify_16_02.py) |
| [16-03 · The DFT and Its Properties](chapters/16-03-the-dft.md) | 8 | ✅ verified | [problems](problems/16-03-problems.md) · [solutions](solutions/16-03-solutions.md) · [lab](labs/16-03-lab/README.md) · [verify](verify/verify_16_03.py) |
| [16-04 · The FFT Algorithm](chapters/16-04-the-fft.md) | 7 | ✅ verified | [problems](problems/16-04-problems.md) · [solutions](solutions/16-04-solutions.md) · [lab](labs/16-04-lab/README.md) · [verify](verify/verify_16_04.py) |
| [16-05 · Spectral Analysis and Windowing](chapters/16-05-spectral-analysis-and-windowing.md) | 7 | ✅ verified | [problems](problems/16-05-problems.md) · [solutions](solutions/16-05-solutions.md) · [lab](labs/16-05-lab/README.md) · [verify](verify/verify_16_05.py) |
| [16-06 · FIR Filter Design](chapters/16-06-fir-filter-design.md) | 9 | ✅ verified | [problems](problems/16-06-problems.md) · [solutions](solutions/16-06-solutions.md) · [lab](labs/16-06-lab/README.md) · [verify](verify/verify_16_06.py) |
| [16-07 · IIR Filter Design](chapters/16-07-iir-filter-design.md) | 8 | ✅ verified | [problems](problems/16-07-problems.md) · [solutions](solutions/16-07-solutions.md) · [lab](labs/16-07-lab/README.md) · [verify](verify/verify_16_07.py) |
| [16-08 · Filter Structures and Implementation](chapters/16-08-filter-structures.md) | 6 | ✅ verified | [problems](problems/16-08-problems.md) · [solutions](solutions/16-08-solutions.md) · [lab](labs/16-08-lab/README.md) · [verify](verify/verify_16_08.py) |
| [16-09 · Multirate DSP: Decimation, Interpolation and Polyphase](chapters/16-09-multirate-dsp.md) | 8 | ✅ verified | [problems](problems/16-09-problems.md) · [solutions](solutions/16-09-solutions.md) · [lab](labs/16-09-lab/README.md) · [verify](verify/verify_16_09.py) |
| [16-10 · Quantization and Fixed-Point Effects](chapters/16-10-quantization-and-fixed-point.md) | 7 | ✅ verified | [problems](problems/16-10-problems.md) · [solutions](solutions/16-10-solutions.md) · [lab](labs/16-10-lab/README.md) · [verify](verify/verify_16_10.py) |
| [16-11 · DSP Hardware Architectures](chapters/16-11-dsp-hardware-architectures.md) | 7 | ✅ verified | [problems](problems/16-11-problems.md) · [solutions](solutions/16-11-solutions.md) · [lab](labs/16-11-lab/README.md) · [verify](verify/verify_16_11.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/16-digital-signal-processing.csv) · [Equation sheet](../../reference/equation-sheets/16-digital-signal-processing.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 16 is planned at about 83 hours: the chapters' own estimates add to 78, plus 5 hours of review and the exam. Course 11 gave you the DTFT, the z-transform and sampling as analysis tools. This course turns them into engineering: compute spectra you can trust, design filters to a written specification, change sample rates cheaply, survive finite word lengths, and map the arithmetic onto silicon at a known cost in multipliers, bits, latency and energy. These are the trades behind every audio codec, radio front end, sensor hub and ADC data sheet in a semiconductor portfolio.

The eleven chapters fall into four blocks:

- **Foundations (16-01 to 16-02).** Discrete-time systems with the moving average and the EMA as running examples, and pole–zero design: notches, resonators, group delay, all-pass and minimum-phase filters.
- **Transforms and spectra (16-03 to 16-05).** The DFT and fast convolution; the FFT, counted exactly and built as hardware; windows, processing gain and the FFT test of an ADC (SNR, SINAD, SFDR, ENOB).
- **Filter design and implementation (16-06 to 16-09).** FIR design by windows, Kaiser's formulas and Parks–McClellan; IIR design from analog prototypes by the bilinear transform; structures, sensitivity and lattices; and multirate systems with polyphase filters, half-band stages and CIC decimators.
- **Finite precision and hardware (16-10 to 16-11).** Quantization noise, loading, noise gain, limit cycles and scaling; then MAC datapaths, folding, the iteration bound, look-ahead, multiplierless constants and CORDIC, with the energy numbers that decide between a processor and a datapath.

Work at least the [A] and [B] problems of every chapter (101 of the 134 problems; the 33 [C] problems are the stretch). The labs form a toolkit that later chapters import:

- `dtsys.py` (16-01) and `pz.py` (16-02) simulate difference equations and place poles and zeros; `dft.py` (16-03), `fft.py` (16-04) and `spectral.py` (16-05) implement the DFT, a counted radix-2 FFT, windows and the ADC test;
- `firdesign.py` (16-06) and `iirdesign.py` (16-07) design to a specification and measure the result; `structures.py` (16-08) implements every structure, the lattice recursions and a bit-exact fixed-point biquad;
- `multirate.py` (16-09), `quant.py` (16-10) and `hwarch.py` (16-11) cover polyphase and CIC filters, quantizers and limit cycles, and MAC sizing, look-ahead, CSD and CORDIC;
- five Verilog designs, each with a self-checking testbench against vectors generated by the Python models: a moving sum (16-01), an 8-point FFT (16-04), a DF I biquad with saturation (16-08), a CIC decimator with wrap-around integrators (16-09) and a 14-stage CORDIC (16-11).

The verify scripts recompute the chapters' numbers, mostly by a route independent of the lab code (SciPy's designs, direct evaluation, simulation), and check prose claims as well as answer keys, so a mismatch in your own work usually means a wrong method, not rounding.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/16-digital-signal-processing.md) collects the relations; these are the ideas behind them:

- a frequency in DSP is a fraction of the sample rate, $\omega = 2\pi f/f_s$, and everything above $f_s/2$ folds back (16-01);
- a pole at radius $r$ buys a bandwidth of about $2(1 - r)$ rad/sample and costs a time constant of about $1/(1 - r)$ samples: narrow filters ring (16-02);
- the DFT samples the DTFT, so resolution, leakage and circular wrap are properties of the record and the window, not of the signal (16-03, 16-05);
- the FFT turns $N^2$ multiplications into about $\frac N2\log_2N$, and its fixed-point cost is word growth of up to one bit per stage (16-04);
- a spectrum's floor is the SNR plus the processing gain: never read it as the noise level (16-05);
- FIR filters buy linear phase and robustness with length, which scales as $1/\Delta\omega$; IIR filters buy sharpness cheaply with nonlinear phase and recursive arithmetic (16-06, 16-07);
- structures that are equivalent on paper differ in delay registers, critical path, coefficient sensitivity and overflow behaviour: biquads, transposed forms and lattices exist for these reasons (16-08);
- filter at the lowest rate you can: polyphase decomposition and the noble identities cut the work by the rate-change factor, and CIC filters decimate without multipliers (16-09);
- each bit is worth 6.02 dB, and every rounding point's noise is multiplied by the noise gain to the output; recursive filters must saturate (16-10);
- a datapath's cost is multiplications per second divided by the clock, its speed limit is the iteration bound of its loops, and its energy is dominated by data movement and instruction overhead, not arithmetic (16-11).

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes, with a calculator and the equation sheet but no Python or simulator. Aim for at least 70%. Questions 1 to 11 follow the chapters; Question 12 compares the FIR and IIR filters that meet one specification and asks why the usual IIR advantage disappears; Question 13 asks for three short derivations (the 6.02N + 1.76 dB rule, the forced zero of a type II filter, the decimation noble identity); Question 14 is a diligence question about an audio-DSP start-up's power, noise and latency claims, partly graded against a rubric. The course maps onto the FE Electrical and Computer exam's Signal Processing area, 5–8 questions ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/16-digital-signal-processing.csv) (86 cards) are for spaced review alongside the chapters.
