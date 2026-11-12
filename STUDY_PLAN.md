# Study Plan

This is how to get through the Self-Taught BSEE at about **10–12 hours per week**, with no instructor. The schedule below is computed from the chapter hour estimates in [CURRICULUM.md](CURRICULUM.md). Treat it as a pacing guide, not a contract. A chapter is done when you can solve its problems, not when its week ends.

## An honest calendar

ABET requires an accredited engineering program to include at least 30 semester credit hours of mathematics and basic science and at least 45 of engineering topics ([R-013](reference/research-log.md#r-013--abet-curriculum-minimums-and-semester-credit-workload)). A semester credit traditionally represents about 45 hours of student work (one class hour plus two hours of outside work per week for about 15 weeks), so the technical core of a BSEE is at least ≈ 3,400 hours, delivered over four full-time years alongside general-education courses. This curriculum's ≈ 2,700 hours is leaner, because self-study drops lectures, commuting and logistics, but it covers more electives than any single student would take. At 11 hours per week, that is a **multi-year** program, about five and a half calendar years for the full path at 46 study weeks per year. Three things shorten it:

- **Use the practitioner fast track first.** It reaches conversation fluency in about a fifth of the time. Then back-fill chapters at full depth as your coverage areas demand. Nothing on the fast track has to be re-done later.
- **Raise the weekly hours during lighter work periods.** At 15 h/week the full path takes about four years.
- **Skip what you already know.** Course 03 (probability) is already accelerated for your background. If a chapter's [A] and [B] problems are easy on a cold attempt, move on.

## The weekly rhythm (≈ 11 h)

| Session | When | Duration | What |
|---|---|---|---|
| Core 1 | Weekday evening | 2 h | Read the next chapter section; re-derive every derivation on paper |
| Core 2 | Weekday evening | 2 h | Worked examples (attempt first, then compare), concept check |
| Lab | Weekday evening | 1.5 h | Run the lab notebook / netlist; do the "predict, then run" exercises |
| Problems | Weekend block | 4 h | Problem set: all [A] and [B], then [C] as time allows; check worked solutions only after an honest attempt |
| Review | Daily, 10–15 min | ≈ 1.5 h/week | Anki flashcards; re-do one old problem from your error log |

Keep an **error log**: every problem you got wrong, why, and the fix. Before each checkpoint, re-solve everything in the log.

## Review cadence

- **Daily:** 10–15 minutes of Anki (each course ships 50–150 cards in [flashcards/](flashcards/README.md)).
- **Weekly:** re-solve two problems from earlier chapters, chosen from the error log.
- **End of course:** one full review week built into the hours, then the course final exam under timed conditions. Score ≥ 70% before moving on; otherwise revisit the chapters behind your misses.
- **End of term:** the FE-style [checkpoint](checkpoints/README.md) for that term. It is the forcing function for long-term retention.
- **Every six months:** one "practitioner" exercise. Read a recent Hot Chips or ISSCC paper abstract in your coverage area and write a one-page memo in the style of [capstone C4](capstones/README.md). It will get visibly better each time.

## Checkpoints (relative dates)

| Checkpoint | Covers | Taken at the end of |
|---|---|---|
| Term 1 | Mathematics, Probability & Statistics, Software Engineering (intro), Materials (physics) | Term 1 (see schedule) |
| Term 2 | Circuit Analysis, Digital Systems, Linear Systems (intro) | Term 2 |
| Term 3 | Electronics, Materials, Linear Systems, Signal Processing | Term 3 |
| Term 4 | Electronics, Electromagnetics, Computer Systems | Term 4 |
| Term 5 | Control Systems, Signal Processing, Communications, Computer Networks, Computer Systems, Software Engineering | Term 5 |
| Term 6 | Power Systems, Electronics, Materials, Digital Systems | Term 6 |
| Term 7 | Ethics & Professional Practice, Engineering Economics, plus a full-length mixed FE practice exam | Term 7 |

The program-week number for each checkpoint is in the schedule below.

<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

## Term-by-term schedule

Computed at **11 hours per week**, in the recommended order. "Week" is the program week, counted from the day you start. Each course row includes its review and final exam. Expand a term to see chapter-level weeks.

### Term 1 — Foundations

≈ 473 hours · ≈ 43 weeks · ends around program week 43 (≈ 0.9 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 1 | [00 · Orientation](courses/00-orientation/README.md) | 10 |
| 1–4 | [05 · Programming for Engineers](courses/05-programming-for-engineers/README.md) (chapters 05-01–05-04) | 30 |
| 4–15 | [01 · Calculus for Engineers](courses/01-calculus-for-engineers/README.md) | 116 |
| 15–25 | [02 · Complex Numbers, Differential Equations and Linear Algebra](courses/02-complex-numbers-des-and-linear-algebra/README.md) | 110 |
| 25–29 | [03 · Probability, Statistics and Random Variables for EE](courses/03-probability-statistics-and-random-variables/README.md) | 43 |
| 29–38 | [04 · Physics for EE](courses/04-physics-for-ee/README.md) | 106 |
| 38–43 | [05 · Programming for Engineers](courses/05-programming-for-engineers/README.md) (chapters 05-05–05-09) | 50 |
| 43 | **Term 1 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 1 | 00-01 The Map of Electrical Engineering | 2 |
| 1 | 00-02 The Abstraction Stack: Physics to Software | 2 |
| 1 | 00-03 How to Study This Curriculum | 1.5 |
| 1 | 00-04 Toolchain Setup Walkthrough | 2.5 |
| 1 | 00-05 How Chip Companies' Engineering Organizations Work | 2 |
| 1–2 | 05-01 Python Fundamentals for Engineers | 8 |
| 2–3 | 05-02 NumPy, Vectorization and Numerical Computing | 8 |
| 3–4 | 05-03 SciPy, SymPy and Matplotlib | 8 |
| 4 | 05-04 Jupyter, Testing and Reproducible Workflows | 6 |
| 4–5 | 01-01 Functions, Models and Units | 8 |
| 5–6 | 01-02 Limits and Continuity | 8 |
| 6–7 | 01-03 Derivatives: Rates of Change in Circuits | 12 |
| 7–8 | 01-04 Applications of Derivatives | 12 |
| 8–9 | 01-05 Integrals: Accumulating Charge and Energy | 12 |
| 9–10 | 01-06 Techniques of Integration | 12 |
| 10–11 | 01-07 Applications of Integration | 10 |
| 11–12 | 01-08 Sequences, Series and Taylor Expansions | 12 |
| 12–13 | 01-09 Multivariable Calculus I: Partial Derivatives and Gradients | 12 |
| 13–14 | 01-10 Multivariable Calculus II: Multiple, Line and Surface Integrals | 12 |
| 14–15 | 01 review + final exam | 6 |
| 15–16 | 02-01 Complex Numbers, Euler's Formula and Phasors | 10 |
| 16 | 02-02 First-Order Linear ODEs | 10 |
| 17–18 | 02-03 Second-Order Linear ODEs and the Characteristic Equation | 12 |
| 18 | 02-04 Forced Response and Resonance | 10 |
| 19 | 02-05 The Laplace Transform for ODEs | 10 |
| 19–20 | 02-06 Vectors, Matrices and Linear Systems | 12 |
| 21 | 02-07 Determinants, Inverses, Rank and Vector Spaces | 10 |
| 21–22 | 02-08 Eigenvalues and Eigenvectors | 12 |
| 23 | 02-09 Systems of Linear ODEs and the Matrix Exponential | 10 |
| 23–24 | 02-10 Numerical Methods for Engineers | 8 |
| 24–25 | 02 review + final exam | 6 |
| 25 | 03-01 Probability in EE Language | 6 |
| 25–26 | 03-02 Random Variables and Distributions | 8 |
| 26 | 03-03 Expectation, Variance and Functions of Random Variables | 6 |
| 27 | 03-04 Joint Distributions, Correlation and the CLT | 8 |
| 27–28 | 03-05 Estimation and Hypothesis Testing for Engineers | 6 |
| 28 | 03-06 Random Processes Preview: Noise | 6 |
| 28–29 | 03 review + final exam | 3 |
| 29 | 04-01 Mechanics Essentials for EE | 8 |
| 29–30 | 04-02 Charge, Coulomb's Law and Electric Fields | 10 |
| 30–31 | 04-03 Gauss's Law | 8 |
| 31–32 | 04-04 Electric Potential, Capacitance and Dielectrics | 10 |
| 32–33 | 04-05 Current, Resistance and Conduction | 8 |
| 33 | 04-06 Magnetic Fields and Forces | 10 |
| 34 | 04-07 Faraday's Law, Lenz's Law and Inductance | 10 |
| 34–35 | 04-08 Energy in Fields and Maxwell's Equations (Preview) | 6 |
| 35–36 | 04-09 Waves and Optics Basics | 10 |
| 36–37 | 04-10 Introduction to Quantum Mechanics | 10 |
| 37–38 | 04-11 Introduction to Solid-State Physics | 10 |
| 38 | 04 review + final exam | 6 |
| 38–39 | 05-05 C Fundamentals | 10 |
| 39–40 | 05-06 C Pointers, Arrays and Memory | 10 |
| 40–41 | 05-07 Bit Manipulation and Fixed-Width Integers | 8 |
| 41–42 | 05-08 Data Structures and Algorithms You Will Need | 12 |
| 42 | 05-09 Software Engineering Practices | 6 |
| 42–43 | 05 review + final exam | 4 |
| 43 | Term 1 checkpoint | 8 |

</details>

### Term 2 — Circuits and Digital Logic

≈ 303 hours · ≈ 28 weeks · ends around program week 71 (≈ 1.5 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 44–51 | [06 · Circuit Analysis I (DC)](courses/06-circuit-analysis-1-dc/README.md) | 86 |
| 51–61 | [07 · Circuit Analysis II (Transient and AC)](courses/07-circuit-analysis-2-transient-and-ac/README.md) | 103 |
| 61–70 | [08 · Digital Logic Design](courses/08-digital-logic-design/README.md) | 106 |
| 70–71 | **Term 2 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 44 | 06-01 Charge, Current, Voltage, Power and the Lumped Circuit Abstraction | 6 |
| 44–45 | 06-02 Circuit Elements and Ohm's Law | 6 |
| 45 | 06-03 Kirchhoff's Laws, Series/Parallel and Dividers | 8 |
| 45–46 | 06-04 Nodal Analysis | 10 |
| 46–47 | 06-05 Mesh Analysis | 8 |
| 47–48 | 06-06 Dependent Sources | 8 |
| 48 | 06-07 Linearity and Superposition | 6 |
| 48–49 | 06-08 Thevenin and Norton Equivalents | 10 |
| 49 | 06-09 Maximum Power Transfer | 4 |
| 50 | 06-10 The Ideal Op-Amp | 10 |
| 50–51 | 06-11 Practical DC Circuits and Measurement | 4 |
| 51 | 06 review + final exam | 6 |
| 51–52 | 07-01 Capacitors and Inductors | 7 |
| 52–53 | 07-02 First-Order RC and RL Transients | 10 |
| 53–54 | 07-03 Second-Order RLC Transients | 10 |
| 54–55 | 07-04 Laplace-Domain Circuit Analysis | 12 |
| 55–56 | 07-05 Sinusoidal Steady State, Phasors and Impedance | 10 |
| 56 | 07-06 AC Power and Power Factor | 8 |
| 57 | 07-07 Frequency Response and Bode Plots | 10 |
| 57–58 | 07-08 Filters and Resonance | 10 |
| 58–59 | 07-09 Mutual Inductance and Transformers | 8 |
| 59–60 | 07-10 Two-Port Networks | 7 |
| 60 | 07-11 Three-Phase Circuits | 5 |
| 60–61 | 07 review + final exam | 6 |
| 61 | 08-01 Number Systems and Codes | 7 |
| 61–62 | 08-02 Boolean Algebra and Logic Gates | 8 |
| 62–63 | 08-03 Logic Minimization: K-Maps and Beyond | 8 |
| 63–64 | 08-04 Combinational Building Blocks | 10 |
| 64–65 | 08-05 Introduction to Verilog/SystemVerilog and Testbenches | 12 |
| 65 | 08-06 Latches, Flip-Flops and Sequential Timing | 8 |
| 66 | 08-07 Registers, Counters and Shift Registers | 7 |
| 66–67 | 08-08 Finite State Machines | 12 |
| 67–68 | 08-09 Arithmetic Circuits | 8 |
| 68–69 | 08-10 Timing, Metastability and Clock-Domain Crossing | 10 |
| 69 | 08-11 Memories and Programmable Logic | 5 |
| 69–70 | 08-12 FPGA Implementation Flow | 5 |
| 70 | 08 review + final exam | 6 |
| 70–71 | Term 2 checkpoint | 8 |

</details>

### Term 3 — Devices, Electronics I, Signals and Systems

≈ 329 hours · ≈ 30 weeks · ends around program week 101 (≈ 2.2 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 71–82 | [09 · Semiconductor Devices](courses/09-semiconductor-devices/README.md) | 116 |
| 82–91 | [10 · Electronics I (Microelectronic Circuits)](courses/10-electronics-1/README.md) | 99 |
| 91–100 | [11 · Signals and Systems](courses/11-signals-and-systems/README.md) | 106 |
| 100–101 | **Term 3 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 71–72 | 09-01 Crystals, Energy Bands and the Semiconductor | 8 |
| 72–73 | 09-02 Carriers, Doping and the Fermi Level | 9 |
| 73 | 09-03 Carrier Transport: Drift and Diffusion | 8 |
| 73–74 | 09-04 Generation, Recombination and the Continuity Equation | 7 |
| 74–75 | 09-05 PN Junction Electrostatics | 8 |
| 75 | 09-06 PN Junction I–V, Capacitance and Breakdown | 9 |
| 76 | 09-07 The Bipolar Junction Transistor | 9 |
| 76–77 | 09-08 The MOS Capacitor | 9 |
| 77–78 | 09-09 The Long-Channel MOSFET | 10 |
| 78–79 | 09-10 Short-Channel Effects and Leakage | 8 |
| 79 | 09-11 CMOS and Scaling: Moore, Dennard and Beyond | 6 |
| 79–80 | 09-12 Advanced Transistors: FinFET, GAA, CFET and Backside Power | 6 |
| 80 | 09-13 Compound and Wide-Bandgap Semiconductors | 6 |
| 80–81 | 09-14 Optoelectronic Devices | 7 |
| 81–82 | 09 review + final exam | 6 |
| 82 | 10-01 Diodes and Diode Circuits | 10 |
| 83 | 10-02 MOSFET DC Operation and Biasing | 10 |
| 83–84 | 10-03 BJT DC Operation and Biasing | 9 |
| 84–85 | 10-04 Small-Signal Models | 10 |
| 85–86 | 10-05 Amplifier Fundamentals | 6 |
| 86–87 | 10-06 MOS Single-Stage Amplifiers | 12 |
| 87–88 | 10-07 BJT Single-Stage Amplifiers | 10 |
| 88 | 10-08 Current Sources and Current Mirrors | 8 |
| 88–89 | 10-09 Real Op-Amps: Non-Idealities | 10 |
| 89–90 | 10-10 Op-Amp Application Circuits | 8 |
| 90–91 | 10 review + final exam | 6 |
| 91 | 11-01 Signals: Classification and Operations | 8 |
| 91–92 | 11-02 Systems and Their Properties | 7 |
| 92–93 | 11-03 Convolution | 10 |
| 93–94 | 11-04 LTI Systems and Differential/Difference Equations | 8 |
| 94 | 11-05 Fourier Series | 10 |
| 95–96 | 11-06 The Continuous-Time Fourier Transform | 12 |
| 96 | 11-07 The Discrete-Time Fourier Transform | 8 |
| 96–97 | 11-08 The Laplace Transform and System Functions | 10 |
| 97–98 | 11-09 The z-Transform | 10 |
| 98–99 | 11-10 Sampling, Aliasing and Reconstruction | 10 |
| 99–100 | 11-11 Modulation and Filtering Applications | 7 |
| 100 | 11 review + final exam | 6 |
| 100–101 | Term 3 checkpoint | 8 |

</details>

### Term 4 — Electronics II, Electromagnetics, Computer Architecture

≈ 340 hours · ≈ 31 weeks · ends around program week 132 (≈ 2.9 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 101–110 | [12 · Electronics II](courses/12-electronics-2/README.md) | 104 |
| 110–120 | [13 · Electromagnetics](courses/13-electromagnetics/README.md) | 106 |
| 120–131 | [14 · Computer Organization and Architecture](courses/14-computer-organization-and-architecture/README.md) | 122 |
| 131–132 | **Term 4 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 101–102 | 12-01 Differential Pairs | 10 |
| 102–103 | 12-02 Active Loads, Cascodes and Multistage Amplifiers | 10 |
| 103–104 | 12-03 Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros | 12 |
| 104–105 | 12-04 High-Frequency Analysis Methods | 8 |
| 105–106 | 12-05 Feedback: Theory and the Four Topologies | 12 |
| 106–107 | 12-06 Stability and Frequency Compensation | 10 |
| 107 | 12-07 Output Stages and Power Amplifiers | 8 |
| 107–108 | 12-08 Op-Amp Internals | 10 |
| 108–109 | 12-09 Oscillators | 8 |
| 109–110 | 12-10 Noise in Circuits | 10 |
| 110 | 12 review + final exam | 6 |
| 110–111 | 13-01 Vector Calculus Refresher | 10 |
| 111–112 | 13-02 Electrostatics: Boundary Conditions and Boundary-Value Problems | 10 |
| 112–113 | 13-03 Magnetostatics and Inductance | 8 |
| 113–114 | 13-04 Maxwell's Equations and Time-Varying Fields | 10 |
| 114–115 | 13-05 Plane Waves in Lossless and Lossy Media | 10 |
| 115 | 13-06 Reflection and Transmission of Waves | 8 |
| 116 | 13-07 Transmission Lines: Time Domain | 10 |
| 116–117 | 13-08 Transmission Lines: Sinusoidal Steady State | 10 |
| 117–118 | 13-09 The Smith Chart and Impedance Matching | 10 |
| 118–119 | 13-10 Waveguides and Resonators | 6 |
| 119 | 13-11 Radiation and Antenna Fundamentals | 8 |
| 120 | 13 review + final exam | 6 |
| 120–121 | 14-01 Performance, Power and the Iron Law | 7 |
| 121–122 | 14-02 Instruction Set Architecture: RISC-V, Arm and x86 | 10 |
| 122 | 14-03 Assembly and the Compilation Stack | 8 |
| 122–123 | 14-04 Computer Arithmetic and Number Formats | 7 |
| 123–124 | 14-05 Single-Cycle Datapath and Control | 8 |
| 124–125 | 14-06 Pipelining and Hazards | 10 |
| 125 | 14-07 Branch Prediction and Speculation | 7 |
| 125–126 | 14-08 Out-of-Order and Superscalar Execution | 9 |
| 126–127 | 14-09 Memory Hierarchy and Caches | 10 |
| 127–128 | 14-10 Virtual Memory, TLBs and the OS Interface | 7 |
| 128 | 14-11 I/O, Buses and Interconnect | 5 |
| 128–129 | 14-12 Multicore, Coherence and Memory Consistency | 8 |
| 129 | 14-13 GPUs and SIMT | 7 |
| 129–130 | 14-14 AI Accelerators: Systolic Arrays, Dataflow and Low Precision | 9 |
| 130–131 | 14-15 The Roofline Model, Benchmarks and How They Are Gamed | 4 |
| 131 | 14 review + final exam | 6 |
| 131–132 | Term 4 checkpoint | 8 |

</details>

### Term 5 — Systems Core

≈ 366 hours · ≈ 33 weeks · ends around program week 165 (≈ 3.6 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 132–140 | [15 · Control Systems](courses/15-control-systems/README.md) | 89 |
| 140–147 | [16 · Digital Signal Processing](courses/16-digital-signal-processing/README.md) | 83 |
| 148–157 | [17 · Communication Systems](courses/17-communication-systems/README.md) | 103 |
| 157–164 | [18 · Embedded Systems and Microcontrollers](courses/18-embedded-systems-and-microcontrollers/README.md) | 83 |
| 164–165 | **Term 5 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 132–133 | 15-01 Modeling Dynamic Systems | 8 |
| 133 | 15-02 Transfer Functions and Block Diagrams | 7 |
| 133–134 | 15-03 Time Response and Specifications | 7 |
| 134 | 15-04 Feedback Properties and Steady-State Error | 7 |
| 135 | 15-05 Stability and the Routh–Hurwitz Criterion | 5 |
| 135–136 | 15-06 Root Locus | 8 |
| 136–137 | 15-07 Frequency-Domain Design: Bode, Nyquist and Margins | 10 |
| 137 | 15-08 PID Control | 6 |
| 137–138 | 15-09 Lead and Lag Compensation | 7 |
| 138 | 15-10 State-Space Introduction | 8 |
| 139 | 15-11 Digital Control | 5 |
| 139 | 15-12 Applications: PLLs, Voltage Regulators and Thermal Management | 6 |
| 140 | 15 review + final exam | 5 |
| 140 | 16-01 Discrete-Time Signals and Systems Review | 5 |
| 140–141 | 16-02 DTFT and z-Transform for DSP | 6 |
| 141–142 | 16-03 The DFT and Its Properties | 8 |
| 142 | 16-04 The FFT Algorithm | 7 |
| 142–143 | 16-05 Spectral Analysis and Windowing | 7 |
| 143–144 | 16-06 FIR Filter Design | 9 |
| 144 | 16-07 IIR Filter Design | 8 |
| 145 | 16-08 Filter Structures and Implementation | 6 |
| 145–146 | 16-09 Multirate DSP: Decimation, Interpolation and Polyphase | 8 |
| 146 | 16-10 Quantization and Fixed-Point Effects | 7 |
| 146–147 | 16-11 DSP Hardware Architectures | 7 |
| 147 | 16 review + final exam | 5 |
| 148 | 17-01 Random Processes and Power Spectral Density | 9 |
| 148–149 | 17-02 Noise and SNR in Communication Systems | 6 |
| 149 | 17-03 Analog Modulation (Brief) | 5 |
| 149–150 | 17-04 Baseband Digital Transmission | 8 |
| 150–151 | 17-05 Matched Filters and Optimal Detection | 8 |
| 151–152 | 17-06 Bandpass Digital Modulation and BER | 10 |
| 152 | 17-07 Information Theory and Shannon Capacity | 8 |
| 152–153 | 17-08 Channel Coding | 9 |
| 153–154 | 17-09 Wireless Channels: Fading and Multipath | 6 |
| 154 | 17-10 OFDM | 7 |
| 154–155 | 17-11 MIMO and Beamforming Basics | 6 |
| 155–156 | 17-12 Multiple Access, Cellular and Wi-Fi Systems | 8 |
| 156 | 17-13 Computer Networks Fundamentals | 8 |
| 156–157 | 17 review + final exam | 5 |
| 157 | 18-01 Microcontroller Architecture | 7 |
| 158 | 18-02 Bare-Metal C and the Build Toolchain | 8 |
| 158–159 | 18-03 Interrupts, Exceptions and Timers | 8 |
| 159 | 18-04 DMA and Data Movement | 5 |
| 159–160 | 18-05 Peripherals and Serial Buses: GPIO, UART, SPI, I²C | 8 |
| 160–161 | 18-06 Analog Interfaces: ADC, DAC and PWM | 6 |
| 161 | 18-07 RTOS Concepts | 8 |
| 161–162 | 18-08 Boot, Bootloaders and Firmware Update | 5 |
| 162–163 | 18-09 Ultra-Low-Power Design | 9 |
| 163 | 18-10 Sensors: IMU, PPG, MEMS and Audio | 7 |
| 163–164 | 18-11 Hardware Security | 7 |
| 164 | 18 review + final exam | 5 |
| 164–165 | Term 5 checkpoint | 8 |

</details>

### Term 6 — Senior Electives (semiconductor-industry tracks)

≈ 602 hours · ≈ 55 weeks · ends around program week 220 (≈ 4.8 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 165–175 | [19 · Digital VLSI Design](courses/19-digital-vlsi-design/README.md) | 112 |
| 175–185 | [20 · Analog and Mixed-Signal IC Design](courses/20-analog-and-mixed-signal-ic-design/README.md) | 104 |
| 185–193 | [21 · RF and Microwave Engineering](courses/21-rf-and-microwave-engineering/README.md) | 91 |
| 193–201 | [22 · Power Electronics and Energy Conversion](courses/22-power-electronics-and-energy-conversion/README.md) | 92 |
| 201–206 | [23 · Memory and Storage Technology](courses/23-memory-and-storage-technology/README.md) | 53 |
| 206–212 | [24 · High-Speed I/O, Signal Integrity and Photonics](courses/24-high-speed-io-signal-integrity-and-photonics/README.md) | 59 |
| 212–219 | [25 · Semiconductor Fabrication, Packaging, Test and Reliability](courses/25-fabrication-packaging-test-and-reliability/README.md) | 83 |
| 219–220 | **Term 6 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 165–166 | 19-01 The CMOS Inverter: Static Characteristics | 8 |
| 166–167 | 19-02 The CMOS Inverter: Dynamic Behavior and Delay | 8 |
| 167 | 19-03 Combinational Logic Families | 8 |
| 167–168 | 19-04 Transistor Sizing and Logical Effort | 9 |
| 168–169 | 19-05 Interconnect | 8 |
| 169–170 | 19-06 Power and Low-Power Design | 9 |
| 170 | 19-07 Sequential Circuits, Timing and Clocking | 9 |
| 171 | 19-08 SRAM Design | 8 |
| 171–172 | 19-09 Layout, Design Rules and Standard Cells | 6 |
| 172–173 | 19-10 The ASIC Flow I: Synthesis and Static Timing Analysis | 9 |
| 173 | 19-11 The ASIC Flow II: Floorplan, Place and Route, Signoff | 10 |
| 174 | 19-12 Design for Test: Scan, BIST and ATPG | 6 |
| 174–175 | 19-13 Verification: Simulation, UVM, Formal and Emulation | 8 |
| 175 | 19 review + final exam | 6 |
| 175–176 | 20-01 Analog Design Fundamentals in Nanometer CMOS | 8 |
| 176–177 | 20-02 Two-Stage Op-Amp Design | 12 |
| 177–178 | 20-03 Bandgap and Voltage References | 8 |
| 178–179 | 20-04 Low-Dropout Regulators | 8 |
| 179 | 20-05 Comparators and Sample-and-Hold Circuits | 8 |
| 179–180 | 20-06 Data Converter Fundamentals | 7 |
| 180–181 | 20-07 Nyquist ADCs: Flash, SAR and Pipeline | 10 |
| 181–182 | 20-08 Oversampling and Sigma-Delta Converters | 9 |
| 182 | 20-09 DACs | 6 |
| 182–183 | 20-10 PLLs and Jitter | 10 |
| 183–184 | 20-11 Layout, Matching and PVT Variation | 7 |
| 184 | 20-12 Why Analog Does Not Scale Like Digital | 5 |
| 184–185 | 20 review + final exam | 6 |
| 185 | 21-01 S-Parameters and Network Analysis | 8 |
| 186 | 21-02 Impedance Matching Networks | 7 |
| 186–187 | 21-03 Noise Figure and Linearity | 8 |
| 187 | 21-04 Low-Noise Amplifiers | 7 |
| 188 | 21-05 Mixers | 6 |
| 188–189 | 21-06 Oscillators and VCOs | 6 |
| 189 | 21-07 Power Amplifiers | 9 |
| 189–190 | 21-08 Transceiver Architectures | 7 |
| 190–191 | 21-09 The RF Front End: Filters, Switches and Modules | 6 |
| 191 | 21-10 Antennas, Arrays, Beamforming and mmWave | 8 |
| 191–192 | 21-11 Link Budgets | 5 |
| 192–193 | 21-12 Modem Baseband Architecture and Wireless Standards | 9 |
| 193 | 21 review + final exam | 5 |
| 193–194 | 22-01 Power Conversion Principles | 6 |
| 194 | 22-02 Steady-State Analysis and the Buck Converter | 9 |
| 194–195 | 22-03 Boost, Buck-Boost and Other Topologies | 7 |
| 195–196 | 22-04 Isolated Converters: Flyback and Forward | 6 |
| 196 | 22-05 Magnetics Design | 7 |
| 196–197 | 22-06 Converter Losses and Wide-Bandgap Switches | 7 |
| 197–198 | 22-07 Converter Dynamics and Control | 9 |
| 198 | 22-08 PMICs and Power Management for SoCs | 6 |
| 198–199 | 22-09 Batteries, Charging and Fuel Gauging | 8 |
| 199–200 | 22-10 Datacenter Power Delivery | 8 |
| 200 | 22-11 Electric Machines and Drives | 6 |
| 200–201 | 22-12 Power Systems Fundamentals | 8 |
| 201 | 22 review + final exam | 5 |
| 201–202 | 23-01 The Memory Hierarchy and the Memory Wall | 4 |
| 202 | 23-02 SRAM Technology | 4 |
| 202–203 | 23-03 DRAM Cells, Arrays and Refresh | 7 |
| 203 | 23-04 DRAM Interfaces: DDR, LPDDR and GDDR | 6 |
| 203–204 | 23-05 HBM in Depth | 7 |
| 204–205 | 23-06 NAND Flash and 3D NAND | 7 |
| 205 | 23-07 SSD Controllers and Storage Systems | 5 |
| 205 | 23-08 Emerging Memories: MRAM, ReRAM, PCM, FeRAM | 5 |
| 206 | 23-09 Compute-in-Memory and Near-Memory Computing | 5 |
| 206 | 23 review + final exam | 3 |
| 206–207 | 24-01 Signal Integrity Fundamentals | 7 |
| 207 | 24-02 Eye Diagrams, Jitter and BER | 6 |
| 207–208 | 24-03 SerDes Architecture and Equalization | 8 |
| 208–209 | 24-04 DSP-Based SerDes and FEC | 5 |
| 209 | 24-05 Interconnect Standards: PCIe, CXL and Ethernet | 6 |
| 209–210 | 24-06 Die-to-Die Links, Memory PHYs and Scale-Up Fabrics | 6 |
| 210 | 24-07 Photonics Fundamentals | 8 |
| 210–211 | 24-08 Silicon Photonics and Optical Transceivers | 6 |
| 211 | 24-09 Linear-Drive and Co-Packaged Optics | 4 |
| 211–212 | 24 review + final exam | 3 |
| 212 | 25-01 Process Flow Overview: FEOL, MOL and BEOL | 7 |
| 212–213 | 25-02 Lithography: DUV, Multipatterning, EUV and High-NA | 8 |
| 213–214 | 25-03 Deposition, Etch, CMP, Implant and Metrology | 8 |
| 214 | 25-04 Yield Models and Die Cost | 7 |
| 214–215 | 25-05 Foundries, PDKs and Specialty Processes | 6 |
| 215 | 25-06 Packaging I: Wire Bond, Flip-Chip, Substrates, SiP and PoP | 6 |
| 215–216 | 25-07 Packaging II: 2.5D, 3D, Hybrid Bonding and Chiplets | 7 |
| 216–217 | 25-08 Thermal Engineering | 6 |
| 217 | 25-09 Reliability Physics | 8 |
| 217–218 | 25-10 Qualification and Functional Safety | 5 |
| 218 | 25-11 Test: ATE, Wafer Sort, Burn-In and Binning | 6 |
| 218–219 | 25-12 Post-Silicon Validation and Bring-Up | 4 |
| 219 | 25 review + final exam | 5 |
| 219–220 | Term 6 checkpoint | 8 |

</details>

### Term 7 — Design Practice, Systems and Practitioner Layer

≈ 332 hours · ≈ 30 weeks · ends around program week 250 (≈ 5.4 years in, at 46 study weeks/year)

| Weeks | Course | Hours |
|---|---|---|
| 220–224 | [26 · Engineering Design and Professional Practice](courses/26-engineering-design-and-professional-practice/README.md) | 42 |
| 224–227 | Capstone C1: Analog: two-stage op-amp or buck converter in ngspice | 40 |
| 227–232 | Capstone C2: Digital: RTL to layout (OpenLane/Sky130) or Verilator + synthesis | 50 |
| 232–237 | [27 · System Architectures (Case-Study Course)](courses/27-system-architectures/README.md) | 60 |
| 237–240 | Capstone C3: Embedded/system: wearable sensor node design | 35 |
| 241–246 | [28 · Technical Diligence and Engineering Leadership Fluency](courses/28-technical-diligence-and-leadership-fluency/README.md) | 62 |
| 246–249 | Capstone C4: Practitioner: technical diligence memo on a public chip product | 35 |
| 249–250 | **Term 7 checkpoint** (FE-style exam + error log review) | 8 |

<details><summary>Chapter-level weeks</summary>

| Weeks | Item | Hours |
|---|---|---|
| 220 | 26-01 Requirements, Specifications and the Design Process | 5 |
| 220–221 | 26-02 Design Reviews, Documentation and Standards Bodies | 4 |
| 221 | 26-03 Engineering Economics I: NRE, Die Cost, ASP and Gross Margin | 7 |
| 221–222 | 26-04 Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant | 8 |
| 222–223 | 26-05 Schedule and Risk: Why Respins Happen | 6 |
| 223 | 26-06 Engineering Team Structures and Sizing | 5 |
| 223 | 26-07 Engineering Ethics and Professional Responsibility | 5 |
| 224 | 26 review + final exam | 2 |
| 224–227 | Capstone C1 | 40 |
| 227–232 | Capstone C2 | 50 |
| 232 | 27-01 Method: Analyzing a System End to End | 4 |
| 232–233 | 27-02 The Smartphone SoC | 8 |
| 233–234 | 27-03 Wearables I: The Smartwatch | 7 |
| 234 | 27-04 Wearables II: Earbuds and Smart Glasses / XR | 8 |
| 234–235 | 27-05 The PC SoC | 6 |
| 235–236 | 27-06 Automotive E/E Architecture and ADAS Compute | 9 |
| 236–237 | 27-07 The AI Datacenter Server and Rack | 10 |
| 237 | 27-08 Edge AI and IoT | 6 |
| 237 | 27 review + final exam | 2 |
| 237–240 | Capstone C3 | 35 |
| 241 | 28-01 A Framework for Evaluating a Chip Company's Technology | 6 |
| 241–242 | 28-02 Validating Claims: TOPS/W, Benchmarks, Tapeout Status | 6 |
| 242 | 28-03 Maturity Scales for Silicon | 4 |
| 242 | 28-04 Domain Question Banks I: Digital/CPU, AI Accelerators, Memory, Interconnect and Optics | 6 |
| 243 | 28-05 Domain Question Banks II: Analog/Mixed-Signal, RF, Power, Packaging, Embedded | 6 |
| 243 | 28-06 Red Flags and Green Flags | 4 |
| 243–244 | 28-07 Evaluating Engineering Teams | 5 |
| 244 | 28-08 Post-Acquisition Integration Risk | 5 |
| 244–245 | 28-09 The Business ↔ Engineering Translation Table | 3 |
| 245–246 | 28-10 Conversation Scenarios | 15 |
| 246 | 28 review + final exam | 2 |
| 246–249 | Capstone C4 | 35 |
| 249–250 | Term 7 checkpoint | 8 |

</details>

### Totals

- **Total:** ≈ 2740 hours ≈ 250 study weeks.
- **Calendar time:** at 46 study weeks per year (6 weeks of breaks), ≈ **5.4 years** at 11 h/week.
- **Faster pace:** at 15 h/week it is ≈ 4.0 years.

## Practitioner fast track

The minimum path to fluent, skeptical conversations with engineering leaders. In fast-track mode you read each chapter, work its examples, do the concept check and the **[A]** problems, and skip the [B]/[C] sets. That is estimated at 60% of the full chapter hours. Courses 26, 27, 28 are done in full.

| Course | Chapters | Fast-track hours |
|---|---|---|
| 00 · Orientation | [00-01](courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md), [00-02](courses/00-orientation/chapters/00-02-the-abstraction-stack.md), [00-03](courses/00-orientation/chapters/00-03-how-to-study-this-curriculum.md), [00-04](courses/00-orientation/chapters/00-04-toolchain-walkthrough.md), [00-05](courses/00-orientation/chapters/00-05-how-chip-companies-are-organized.md) | 6 |
| 01 · Calculus for Engineers | [01-01](courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md), [01-03](courses/01-calculus-for-engineers/chapters/01-03-derivatives.md), [01-05](courses/01-calculus-for-engineers/chapters/01-05-integrals.md) | 19 |
| 02 · Complex Numbers, Differential Equations and Linear Algebra | [02-01](courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) | 6 |
| 04 · Physics for EE | [04-05](courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md), [04-11](courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md) | 11 |
| 06 · Circuit Analysis I (DC) | [06-01](courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md), [06-02](courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md), [06-03](courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md), [06-08](courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md), [06-10](courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) | 24 |
| 07 · Circuit Analysis II (Transient and AC) | [07-01](courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md), [07-02](courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md), [07-05](courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md), [07-07](courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md) | 22 |
| 08 · Digital Logic Design | [08-01](courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md), [08-02](courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md), [08-06](courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md), [08-10](courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) | 20 |
| 09 · Semiconductor Devices | [09-09](courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md), [09-10](courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md), [09-11](courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md), [09-12](courses/09-semiconductor-devices/chapters/09-12-finfet-gaa-cfet-backside-power.md), [09-13](courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md) | 22 |
| 10 · Electronics I (Microelectronic Circuits) | [10-05](courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md), [10-09](courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md) | 10 |
| 11 · Signals and Systems | [11-06](courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md), [11-10](courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) | 13 |
| 12 · Electronics II | [12-10](courses/12-electronics-2/chapters/12-10-noise-in-circuits.md) | 6 |
| 14 · Computer Organization and Architecture | [14-01](courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md), [14-02](courses/14-computer-organization-and-architecture/chapters/14-02-isa-risc-v-arm-x86.md), [14-09](courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md), [14-13](courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md), [14-14](courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md), [14-15](courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md) | 28 |
| 17 · Communication Systems | [17-06](courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md), [17-07](courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md), [17-10](courses/17-communication-systems/chapters/17-10-ofdm.md) | 15 |
| 18 · Embedded Systems and Microcontrollers | [18-01](courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md), [18-09](courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md), [18-11](courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md) | 14 |
| 19 · Digital VLSI Design | [19-06](courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md), [19-10](courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md), [19-11](courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) | 17 |
| 20 · Analog and Mixed-Signal IC Design | [20-06](courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md), [20-12](courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md) | 7 |
| 21 · RF and Microwave Engineering | [21-03](courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md), [21-07](courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md), [21-12](courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) | 16 |
| 22 · Power Electronics and Energy Conversion | [22-01](courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md), [22-09](courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md), [22-10](courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md) | 13 |
| 23 · Memory and Storage Technology | [23-01](courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md), [23-05](courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md) | 7 |
| 24 · High-Speed I/O, Signal Integrity and Photonics | [24-03](courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md), [24-05](courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md), [24-06](courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md), [24-09](courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) | 14 |
| 25 · Semiconductor Fabrication, Packaging, Test and Reliability | [25-02](courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md), [25-04](courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md), [25-07](courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md), [25-11](courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md) | 17 |
| 26 · Engineering Design and Professional Practice | all (full depth) | 42 |
| 27 · System Architectures (Case-Study Course) | all (full depth) | 60 |
| 28 · Technical Diligence and Engineering Leadership Fluency | all (full depth) | 62 |
| **Total** | | **≈ 470** |

At 11 h/week that is ≈ 43 weeks (≈ 0.9 years). Chapters skipped on the fast track can be back-filled later without re-doing anything.

## FE preparation path

All courses in Terms 1, 2, 3, 4, 5, plus the chapters [09-01](courses/09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md), [22-01](courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md), [22-11](courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md), [22-12](courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md), [25-09](courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md), [26-03](courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md), [26-07](courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md) (power systems, materials, economics and ethics), plus checkpoints 1, 2, 3, 4, 5. Total ≈ **1860 hours**, then a full-length practice exam under exam conditions.

<!-- END GENERATED -->

## Adapting the plan

- **Behind schedule:** don't skip problem sets; skip [C] problems and labs' optional extensions instead. Hours are estimates; an over-run on Course 01–02 is normal and repays itself later.
- **Ahead of schedule:** do the [C] problems and the optional hardware labs ([SETUP.md](SETUP.md#7-optional-hardware-kit)).
- **Work demands a topic now** (e.g., a diligence on an RF front-end company): jump to the relevant fast-track chapters of that course, then return. The prerequisite graph in [CURRICULUM.md](CURRICULUM.md#prerequisite-graph) tells you what you'll need to skim first.
