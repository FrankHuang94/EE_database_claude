<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 08 · Digital Logic Design

From number systems and Boolean algebra to finite state machines, timing and FPGA implementation, written in Verilog/SystemVerilog with self-checking testbenches, the way digital design is actually done.

| | |
|---|---|
| **Term** | 2 |
| **Study hours** | ≈ 106 |
| **University equivalents** | Digital Design / Digital Logic (sophomore); MIT 6.004 (first half), MIT 6.111; Berkeley CS61C (logic portion), EECS 151 (intro) |
| **Textbook alignment** | Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition); Mano & Ciletti, *Digital Design* |
| **Free courses** | MIT OCW 6.004 Computation Structures; MIT OCW 6.111 Introductory Digital Systems Laboratory |
| **Prerequisites** | [05 · Programming for Engineers](../05-programming-for-engineers/README.md) |
| **FE areas** | Digital Systems, Computer Systems |

## Learning objectives

1. Convert between number systems and perform two's-complement and fixed-point arithmetic.
2. Simplify Boolean functions algebraically and with K-maps, and implement them with gates and standard combinational blocks.
3. Design synchronous sequential circuits and FSMs (Moore and Mealy) from a specification.
4. Write synthesizable Verilog/SystemVerilog and self-checking testbenches, and simulate them.
5. Analyze timing (propagation and contamination delay, setup/hold, maximum clock frequency) and explain metastability and clock-domain crossing.
6. Take a design through an open-source FPGA flow.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [08-01 · Number Systems and Codes](chapters/08-01-number-systems-and-codes.md) | 7 | ✅ verified | [problems](problems/08-01-problems.md) · [solutions](solutions/08-01-solutions.md) · [lab](labs/08-01-lab/README.md) · [verify](verify/verify_08_01.py) |
| [08-02 · Boolean Algebra and Logic Gates](chapters/08-02-boolean-algebra-and-gates.md) | 8 | ✅ verified | [problems](problems/08-02-problems.md) · [solutions](solutions/08-02-solutions.md) · [lab](labs/08-02-lab/README.md) · [verify](verify/verify_08_02.py) |
| [08-03 · Logic Minimization: K-Maps and Beyond](chapters/08-03-logic-minimization.md) | 8 | ✅ verified | [problems](problems/08-03-problems.md) · [solutions](solutions/08-03-solutions.md) · [lab](labs/08-03-lab/README.md) · [verify](verify/verify_08_03.py) |
| [08-04 · Combinational Building Blocks](chapters/08-04-combinational-building-blocks.md) | 10 | ✅ verified | [problems](problems/08-04-problems.md) · [solutions](solutions/08-04-solutions.md) · [lab](labs/08-04-lab/README.md) · [verify](verify/verify_08_04.py) |
| [08-05 · Introduction to Verilog/SystemVerilog and Testbenches](chapters/08-05-verilog-and-testbenches.md) | 12 | ✅ verified | [problems](problems/08-05-problems.md) · [solutions](solutions/08-05-solutions.md) · [lab](labs/08-05-lab/README.md) · [verify](verify/verify_08_05.py) |
| [08-06 · Latches, Flip-Flops and Sequential Timing](chapters/08-06-latches-and-flip-flops.md) | 8 | ✅ verified | [problems](problems/08-06-problems.md) · [solutions](solutions/08-06-solutions.md) · [lab](labs/08-06-lab/README.md) · [verify](verify/verify_08_06.py) |
| [08-07 · Registers, Counters and Shift Registers](chapters/08-07-registers-counters-shift-registers.md) | 7 | ✅ verified | [problems](problems/08-07-problems.md) · [solutions](solutions/08-07-solutions.md) · [lab](labs/08-07-lab/README.md) · [verify](verify/verify_08_07.py) |
| [08-08 · Finite State Machines](chapters/08-08-finite-state-machines.md) | 12 | ✅ verified | [problems](problems/08-08-problems.md) · [solutions](solutions/08-08-solutions.md) · [lab](labs/08-08-lab/README.md) · [verify](verify/verify_08_08.py) |
| [08-09 · Arithmetic Circuits](chapters/08-09-arithmetic-circuits.md) | 8 | ✅ verified | [problems](problems/08-09-problems.md) · [solutions](solutions/08-09-solutions.md) · [lab](labs/08-09-lab/README.md) · [verify](verify/verify_08_09.py) |
| [08-10 · Timing, Metastability and Clock-Domain Crossing](chapters/08-10-timing-metastability-cdc.md) | 10 | ✅ verified | [problems](problems/08-10-problems.md) · [solutions](solutions/08-10-solutions.md) · [lab](labs/08-10-lab/README.md) · [verify](verify/verify_08_10.py) |
| [08-11 · Memories and Programmable Logic](chapters/08-11-memories-and-programmable-logic.md) | 5 | ✅ verified | [problems](problems/08-11-problems.md) · [solutions](solutions/08-11-solutions.md) · [lab](labs/08-11-lab/README.md) · [verify](verify/verify_08_11.py) |
| [08-12 · FPGA Implementation Flow](chapters/08-12-fpga-implementation-flow.md) | 5 | ✅ verified | [problems](problems/08-12-problems.md) · [solutions](solutions/08-12-solutions.md) · [lab](labs/08-12-lab/README.md) · [verify](verify/verify_08_12.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/08-digital-logic-design.csv) · [Equation sheet](../../reference/equation-sheets/08-digital-logic-design.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 08 closes Term 2 and is planned at about 106 hours: the chapters' own estimates add to 100, plus review and the exam. It leaves the continuous world of Courses 06 and 07 for the discrete one. Signals become 1s and 0s, circuits become equations in Boolean algebra, and designs are written as code (Verilog) and checked by testbenches. Every digital chip, from a hearing-aid controller to an AI accelerator, is built from what this course teaches: gates, flip-flops, state machines, adders and memories, held together by timing.

The twelve chapters fall into four blocks:

- **Combinational logic (08-01 to 08-04).** Number systems and codes (two's complement, fixed and floating point, Gray, Hamming and CRC); Boolean algebra and CMOS gates; minimization with K-maps and its hazards; and the standard blocks: multiplexers, decoders, adders and comparators.
- **Describing and storing (08-05 to 08-07).** Verilog and self-checking testbenches; latches, flip-flops and the setup and hold constraints; and registers, counters and LFSRs.
- **Design (08-08 to 08-10).** Finite state machines; fast arithmetic (prefix adders, multipliers, fixed-point datapaths); and timing at the system level: skew, jitter, pipelining, metastability and clock-domain crossing.
- **Implementation (08-11 and 08-12).** Memories and programmable logic, and a complete open-source FPGA flow from Verilog to bitstream.

Work at least the [A] and [B] problems of every chapter (176 problems in all). Every lab pairs a notebook with Verilog designs and self-checking testbenches (run under Icarus Verilog and linted with Verilator), so you can predict, then simulate, every circuit. The 08-12 lab adds measured place-and-route reports from Yosys and nextpnr on a real FPGA family.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- two's complement, overflow, sign extension, Q formats and the width rules for products and sums; Gray codes and Hamming syndromes (08-01);
- De Morgan, consensus and the Shannon expansion; why CMOS gates invert (08-02);
- K-maps, prime and essential implicants, don't cares, and why the minimal cover can have hazards (08-03, 08-04);
- the full adder, ripple-carry delay $2n$, subtraction as $A + \overline{B} + 1$, and functions from multiplexers and decoders (08-04);
- Verilog sizing and signedness rules, blocking versus nonblocking assignment, inferred latches, and what makes a testbench self-checking (08-05);
- the setup and hold constraints, and why hold cannot be fixed by the clock (08-06);
- ring, Johnson, binary and LFSR state counts; primitive polynomials and m-sequences (08-07);
- Moore versus Mealy, state encoding, illegal states and the three-block FSM style (08-08);
- prefix adders and their tradeoffs, Dadda and Booth multipliers, saturation and guard bits (08-09);
- skew, jitter and useful skew; the MTBF formula; Gray-pointer FIFOs and conservative flags (08-10);
- memory organization, ROM, PLA and LUT costs, FPGA resources and the FPGA-or-ASIC break-even (08-11);
- the flow's steps, reading utilization and critical paths, and the value of hard blocks over seed sweeps (08-12).

The [equation sheet](../../reference/equation-sheets/08-digital-logic-design.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 15 questions and takes 240 minutes. It allows a calculator and the equation sheet, but not Python or a simulator. Aim for at least 70%. Questions 8, 13 and 14 are design problems: a sequence detector, a multiply-accumulate unit for always-on audio, and a clock-domain crossing. Question 15 is a short-answer diligence question about four product claims. The exam's Verilog answers are confirmed by a self-checking testbench, like the labs. The course maps onto the FE Electrical and Computer exam's digital-systems and computer-systems areas. The [flashcards](../../flashcards/08-digital-logic-design.csv) (106 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Many headline digital specifications hide an assumption that this course teaches you to ask about:

- a TOPS figure is a count of multipliers times a clock, at some operand width and sparsity, and says nothing about the memory traffic that dominates energy;
- "timing closed at 2 GHz" holds only at a corner, with a constraint and a margin;
- a metastability "fix" is a failure rate, not an impossibility;
- an FPGA prototype's frequency says little about an ASIC's, and the reverse.

The Marketing vs Reality sections practice this on accelerator FLOPS and on-die ECC, transistor and gate counts, synthesis and EDA-market claims, data-sheet delays, simulator speed and code coverage, clock-rate and setup-time claims, "error-free" PRBS tests, state coverage and formal verification, INT8 accuracy, synchronizer MTBF, FPGA capacity and speed, and open-source tools.

**Perishable content.** The logic is timeless. The dated facts are in the practitioner sections, logged as [R-143](../../reference/research-log.md#r-143--block-scaled-ai-number-formats) to [R-160](../../reference/research-log.md#r-160--open-source-fpga-and-asic-flows) in the research log. These are the most likely to move:

- block-scaled AI number formats (R-143);
- chip transistor counts (R-149);
- EDA revenues and industry structure (R-151);
- HDL standard and tool versions (R-153);
- FPGA devices, vendors and market estimates (R-159);
- open-source FPGA and ASIC flows, and the tool versions behind the 08-12 lab (R-160).

Check those entries once a year.
