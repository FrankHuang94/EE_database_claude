<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 19 · Digital VLSI Design

Designing digital chips: the CMOS inverter, logic families, sizing and logical effort, interconnect, power, SRAM, timing and clocking, and the full ASIC flow (synthesis, place and route, static timing, signoff) using open-source Yosys/OpenROAD/OpenLane on the SkyWater 130 nm PDK, plus design-for-test and verification.

| | |
|---|---|
| **Term** | 6 |
| **Study hours** | ≈ 112 |
| **University equivalents** | Digital VLSI / Digital Integrated Circuits (senior); MIT 6.374; Berkeley EECS151/251A; Stanford EE271 |
| **Textbook alignment** | Weste & Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*; Rabaey, Chandrakasan & Nikolić, *Digital Integrated Circuits: A Design Perspective*; Sutherland, Sproull & Harris, *Logical Effort* |
| **Free courses** | MIT OCW 6.374 Analysis and Design of Digital Integrated Circuits; Berkeley EECS151 (public lecture materials) |
| **Prerequisites** | [08 · Digital Logic Design](../08-digital-logic-design/README.md), [09 · Semiconductor Devices](../09-semiconductor-devices/README.md), [10 · Electronics I (Microelectronic Circuits)](../10-electronics-1/README.md), [14 · Computer Organization and Architecture](../14-computer-organization-and-architecture/README.md) |
| **FE areas** | Digital Systems, Electronics |

## Learning objectives

1. Analyze the static and dynamic behavior of the CMOS inverter and of static CMOS gates.
2. Size logic paths with logical effort and estimate interconnect delay with Elmore models and repeaters.
3. Estimate and reduce dynamic and leakage power.
4. Analyze sequential timing (setup/hold, skew, jitter) and SRAM cell stability.
5. Run an RTL-to-GDS flow with open-source tools and interpret synthesis, timing and power reports.
6. Explain scan-based DFT, BIST and ATPG, and modern verification methods (UVM, formal, emulation).

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [19-01 · The CMOS Inverter: Static Characteristics](chapters/19-01-cmos-inverter-static.md) | 8 | ✅ verified | [problems](problems/19-01-problems.md) · [solutions](solutions/19-01-solutions.md) · [lab](labs/19-01-lab/README.md) · [verify](verify/verify_19_01.py) |
| [19-02 · The CMOS Inverter: Dynamic Behavior and Delay](chapters/19-02-cmos-inverter-dynamic.md) | 8 | ✅ verified | [problems](problems/19-02-problems.md) · [solutions](solutions/19-02-solutions.md) · [lab](labs/19-02-lab/README.md) · [verify](verify/verify_19_02.py) |
| [19-03 · Combinational Logic Families](chapters/19-03-logic-families.md) | 8 | ✅ verified | [problems](problems/19-03-problems.md) · [solutions](solutions/19-03-solutions.md) · [lab](labs/19-03-lab/README.md) · [verify](verify/verify_19_03.py) |
| [19-04 · Transistor Sizing and Logical Effort](chapters/19-04-sizing-and-logical-effort.md) | 9 | ✅ verified | [problems](problems/19-04-problems.md) · [solutions](solutions/19-04-solutions.md) · [lab](labs/19-04-lab/README.md) · [verify](verify/verify_19_04.py) |
| [19-05 · Interconnect](chapters/19-05-interconnect.md) | 8 | ✅ verified | [problems](problems/19-05-problems.md) · [solutions](solutions/19-05-solutions.md) · [lab](labs/19-05-lab/README.md) · [verify](verify/verify_19_05.py) |
| [19-06 · Power and Low-Power Design](chapters/19-06-power-and-low-power-design.md) | 9 | ✅ verified | [problems](problems/19-06-problems.md) · [solutions](solutions/19-06-solutions.md) · [lab](labs/19-06-lab/README.md) · [verify](verify/verify_19_06.py) |
| [19-07 · Sequential Circuits, Timing and Clocking](chapters/19-07-sequential-timing-and-clocking.md) | 9 | ✅ verified | [problems](problems/19-07-problems.md) · [solutions](solutions/19-07-solutions.md) · [lab](labs/19-07-lab/README.md) · [verify](verify/verify_19_07.py) |
| [19-08 · SRAM Design](chapters/19-08-sram-design.md) | 8 | ✅ verified | [problems](problems/19-08-problems.md) · [solutions](solutions/19-08-solutions.md) · [lab](labs/19-08-lab/README.md) · [verify](verify/verify_19_08.py) |
| [19-09 · Layout, Design Rules and Standard Cells](chapters/19-09-layout-and-standard-cells.md) | 6 | ✅ verified | [problems](problems/19-09-problems.md) · [solutions](solutions/19-09-solutions.md) · [lab](labs/19-09-lab/README.md) · [verify](verify/verify_19_09.py) |
| [19-10 · The ASIC Flow I: Synthesis and Static Timing Analysis](chapters/19-10-synthesis-and-sta.md) | 9 | ✅ verified | [problems](problems/19-10-problems.md) · [solutions](solutions/19-10-solutions.md) · [lab](labs/19-10-lab/README.md) · [verify](verify/verify_19_10.py) |
| [19-11 · The ASIC Flow II: Floorplan, Place and Route, Signoff](chapters/19-11-place-route-signoff.md) | 10 | ✅ verified | [problems](problems/19-11-problems.md) · [solutions](solutions/19-11-solutions.md) · [lab](labs/19-11-lab/README.md) · [verify](verify/verify_19_11.py) |
| [19-12 · Design for Test: Scan, BIST and ATPG](chapters/19-12-design-for-test.md) | 6 | ✅ verified | [problems](problems/19-12-problems.md) · [solutions](solutions/19-12-solutions.md) · [lab](labs/19-12-lab/README.md) · [verify](verify/verify_19_12.py) |
| [19-13 · Verification: Simulation, UVM, Formal and Emulation](chapters/19-13-verification-methods.md) | 8 | ✅ verified | [problems](problems/19-13-problems.md) · [solutions](solutions/19-13-solutions.md) · [lab](labs/19-13-lab/README.md) · [verify](verify/verify_19_13.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/19-digital-vlsi-design.csv) · [Equation sheet](../../reference/equation-sheets/19-digital-vlsi-design.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 19 is planned at about 112 hours: the chapters' own estimates add to 106, plus 6 hours of review and the exam. Course 09 gave you the MOSFET, Courses 10 and 12 its circuit models, Course 08 digital logic and Verilog, and Course 14 the processors these chips implement. This course follows a digital chip from the single transistor pair to signoff: why a CMOS gate works, how fast it switches and what it costs in power, how gates, wires, flip-flops and memories are sized and timed, and how a netlist becomes verified, testable layout.

The thirteen chapters fall into four blocks:

- **The gate (19-01 to 19-04).** The inverter's transfer curve, noise margins and gain; its delay from the square law and the RC model, intrinsic delay and FO4; static, ratioed, pass-transistor and dynamic logic with Elmore delay; and logical effort for sizing whole paths.
- **The chip's physics (19-05 to 19-08).** Wire resistance, capacitance and the distributed RC line, repeaters and crosstalk; dynamic, short-circuit and leakage power with the techniques that cut each; setup, hold, skew, pipelining and metastability; and the 6T SRAM cell, its margins, sensing and yield.
- **The flow (19-09 to 19-11).** Layout layers, design rules, Euler paths and standard cells; synthesis, technology mapping and static timing analysis on SKY130 data; and floorplanning, placement, clock trees, routing and signoff.
- **Making sure it works (19-12 and 19-13).** Manufacturing test (defect level, fault models, scan, BIST, compression) and pre-silicon verification (testbenches, coverage, assertions, UVM, equivalence and model checking, emulation).

Work at least the [A] and [B] problems of every chapter. The labs are of three kinds, each checked by its chapter's verify script:

- ngspice netlists with level-1 transistors and RC ladders: the inverter's transfer curve (19-01), step delay and a ring oscillator (19-02), pseudo-NMOS, pass gates, dynamic nodes and TG ladders (19-03), a tapered chain (19-04), a distributed wire (19-05), supply-current integration (19-06), a metastable latch (19-07), the 6T cell (19-08), and a power strap, a clock-tree merge and a routed net (19-11);
- Python models imported by their notebooks: `inverter.py`, `delay.py`, `logic.py`, `effort.py`, `wires.py`, `power.py`, `timing.py`, `sram.py`, `layout.py`, a static-timing engine and technology mapper on real SKY130 Liberty tables (`sta.py`, `techmap.py`), `pnr.py`, `dft.py` and `verif.py`;
- self-checking Verilog testbenches under Icarus Verilog: a scan chain with an injected fault (19-12) and a constrained-random arbiter testbench with coverage and fairness checks (19-13).

**What to master cold.** The [equation sheet](../../reference/equation-sheets/19-digital-vlsi-design.md) collects the relations; these are the ideas behind them:

- a CMOS gate is a pair of switches with gain: its threshold moves only with the square root of the sizing ratio, and its noise margins come from the unity-gain points (19-01);
- delay is resistance times capacitance, but a gate's own capacitance sets a floor, so whole paths, not single gates, are sized, with about four as the stage effort (19-02 to 19-04);
- wires are distributed RC lines whose unrepeated delay grows with the square of length; repeaters make it linear, and neighbours make it uncertain (19-05);
- power is $\alpha CV_{DD}^2f$ plus leakage that is exponential in threshold and temperature; supply voltage is the strongest knob, until leakage sets a minimum-energy point (19-06);
- hold does not depend on the clock period; skew helps one check and hurts the other; synchronizers make failure rare, not impossible (19-07);
- an SRAM cell must survive a read yet accept a write, and the 6σ cell, not the typical one, sets yield and minimum voltage (19-08);
- layout is ordered by Euler paths and standard-cell rows; area is cell area over utilization (19-09);
- timing is a graph: arrival forward, required backward, slack the difference, with corners, derates and statistics for margin (19-10);
- placement minimizes wirelength, clock trees balance Elmore delays, and signoff checks timing, rules, connectivity and power integrity together (19-11);
- test escapes fall tenfold per extra nine of coverage, and scan turns sequential test into combinational test (19-12);
- verification is sampling plus proof: coverage measures stimulus, not checking; formal proves what you state under what you assume; emulation buys the cycles software needs (19-13).

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 240 minutes, with a calculator and the equation sheet but no Python or simulator. Aim for at least 70%. Questions 1 to 11 follow the chapters 19-01 to 19-11 in order, and Question 12 combines test and verification (19-12, 19-13). Question 13 asks for three derivations: the inverter's switching threshold, the optimal repeaters, and the best stage effort. Question 14 is a diligence question on an AI accelerator's power, frequency, test-quality and verification claims. The exam's verify script recomputes all 150 answers, each by a route other than the one the solutions show.
