# Lab 08-12 · The FPGA Implementation Flow

**Chapter:** [08-12](../../chapters/08-12-fpga-implementation-flow.md) · **Notebook:** [08-12-fpga-flow.ipynb](08-12-fpga-flow.ipynb) · **Time:** about 2 hours (plus 1 hour if you run the tools yourself)

## Objective

1. Run (or read the results of) a complete open-source FPGA flow, from Verilog to bitstream, for six designs on a Lattice iCE40 UltraPlus UP5K.
2. Read utilization and timing reports, and break critical paths into logic and routing delay.
3. Measure how coding style changes the result: carry chain against gates, DSP block against LUTs, one-hot against binary FSM encoding.
4. Compute slack against different clock constraints, and measure the effect of the placement seed.
5. Verify the cores functionally before trusting their timing.

## Background

Chapter sections 3.1 to 3.9 and Examples 08-12.1 to 08-12.7. To read the reports you need only Python; to regenerate them, `pip install yowasp-yosys yowasp-nextpnr-ice40` (WebAssembly builds of Yosys 0.71 and nextpnr 0.11.1, a few hundred MB). Icarus Verilog runs the testbench (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-12-fpga-flow.ipynb](08-12-fpga-flow.ipynb) | The guided notebook (Parts 1 to 4), reading `reports/` | Its own `assert`s and this handout's key |
| [flow_designs.v](flow_designs.v) | The cores (`add32_plus`, `add32_rca`, `mul16`), the harness LFSR and the three place-and-route harnesses | `flow_tb.v`; the flow |
| [flow_top.v](flow_top.v) | A top level for lint tools | Lint only |
| [flow_tb.v](flow_tb.v) | Checks both adders and the multiplier against `+` and `*` on 3000 random inputs (and the corner cases), and the LFSR against Python-computed values | Prints `TEST PASSED` |
| [run_flow.py](run_flow.py) | Runs Yosys, nextpnr-ice40 and icepack on six designs (the 08-08 traffic-light controller twice) and a seed sweep, writing `reports/` | Reproduces the committed reports exactly |
| [reports/](reports/) | nextpnr's JSON reports (frequency, utilization, critical paths), Yosys summaries and the seed sweep | Read by the notebook and by `verify_08_12.py` |

Run from the repository root:

```bash
python tools/run_notebooks.py 08-12
```

```bash
python tools/run_hdl.py
```

Optional, to regenerate the reports:

```bash
pip install yowasp-yosys yowasp-nextpnr-ice40
```

```bash
python courses/08-digital-logic-design/labs/08-12-lab/run_flow.py
```

## Procedure

1. **Verify first.** Run `flow_tb.v`: the cores must be correct before their speed means anything.
2. **Utilization and frequency (Part 1, the chapter's guided exercise).** *Predict first:* the speed ratio of the carry-chain adder to the gate-level adder, and the routing share of the slow path. Then read the reports.
3. **Critical paths (Part 2).** Break each path into clock-to-Q, logic, routing and setup, and count its LUTs and routing hops.
4. **Constraints (Part 3).** Compute every design's slack at 12, 24, 48 and 96 MHz.
5. **Synthesis decisions and seeds (Part 4).** Read the FSM recoding lines and the seed sweep.
6. **Optional: run the flow.** Install the tools, run `run_flow.py`, and confirm the reports are reproduced byte for byte. Then change `mul16` to multiply 18-bit operands and predict what happens to the DSP version (the UP5K's DSP blocks are 16 × 16).

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | coding style | the §3.7 table: carry chain 2.99 times faster than gates; DSP multiplier 3.87 times faster than LUTs with a tenth of the cells; one-hot FSM smaller and faster than binary |
| 2 | critical paths | routing is the largest component of every path except the carry-chain adder's; the gate-level adder's path crosses 20 LUTs and 21 hops |
| 3 | slack | at 48 MHz, 4 designs pass and 2 fail; at 96 MHz only the DSP multiplier passes |
| 4 | synthesis and seeds | "mapping auto encoding to one-hot" for the automatic FSM; seeds change the gate-level adder by about 3% |
| Verilog | testbench | `TEST PASSED` |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-12.a | carry chain over gates, speed ratio | 2.99 | — |
| Lab 08-12.b | routing share, gate-level adder path | 64.5 | % |
| Lab 08-12.c | designs meeting 48 MHz | 4 | — |
| Lab 08-12.d | designs meeting 96 MHz | 1 | — |
| Lab 08-12.e | LUTs on the LUT multiplier's critical path | 27 | — |
| Lab 08-12.f | DSP multiplier slack at 96 MHz | 0.50 | ns |
| Lab 08-12.g | random input sets in the testbench | 3000 | — |

**Reading the key.** At 96 MHz the period is 10.42 ns and the DSP multiplier's critical path is 9.91 ns, leaving 0.50 ns; every other design's path is longer than 10.42 ns. The LUT multiplier's path counts 27 logic segments, one per LUT the signal passes through.

## Discussion questions

1. Why does every design register its inputs and outputs before being measured?
2. Why do the adder and multiplier need a test harness on the UP5K, and why do the harnesses not distort the comparison?
3. The DSP multiplier's path is 65% routing. What would you do to make it faster?
4. Why can the same RTL give different maximum frequencies on two runs, and how does `run_flow.py` make its results reproducible?
5. What would happen if you changed the operands of `mul16` to 18 bits?

<details><summary>Answers to the discussion questions</summary>

1. The reported maximum frequency is set by register-to-register paths. Without input and output registers, the paths from the pins through the logic would be timed against unknown external delays (unconstrained I/O), and the core's own speed would not be measured.
2. A 32 + 32-bit adder needs 98 pins and the SG48 package has 39. The harness generates operands inside the chip and reduces the result to one pin; it is identical in all three harnesses, so its cells and its effect on timing are the same baseline for every core, and the differences between rows belong to the cores.
3. Registering the DSP block's inputs and outputs inside the block (the iCE40's SB_MAC16 has optional internal registers), placing the harness registers next to the block, or simply accepting it: 100 MHz is already far beyond what the design needs. The general lesson is that once the hard block is used, the fabric around it limits the speed.
4. Placement uses randomized algorithms, so different seeds (or tool versions) give different placements and timing. `run_flow.py` fixes the seed (1), the constraint (12 MHz), the device and package, and the tool versions are recorded; the script reproduces the committed reports byte for byte (the Yosys summaries drop their run-time lines, which vary).
5. Synthesis must split each 18-bit multiplication across several 16 × 16 DSP blocks plus logic to combine partial products (08-09), so DSP use rises (likely to several blocks per multiplier) and the extra adders lengthen the critical path. The prediction is the point of the exercise; running the flow checks it.

</details>

## Optional hardware

Any iCE40 UltraPlus board (several open-hardware and commercial boards exist) can be programmed with the bitstreams `run_flow.py` writes to `build/`, using the open-source `iceprog` or the board vendor's tool. Add a pin constraint file (PCF) for your board's LEDs and clock, run the 08-08 traffic-light controller from the 48 MHz internal oscillator with a divided-down tick, and watch the phases on three LEDs.
