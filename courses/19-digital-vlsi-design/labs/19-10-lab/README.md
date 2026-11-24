# Lab 19-10 · A Timing Engine and a Mapper on Real Liberty Data

Chapter: [19-10 · The ASIC Flow I: Synthesis and Static Timing Analysis](../../chapters/19-10-synthesis-and-sta.md)

## Objective

- Read delays and slews from real Liberty tables by bilinear interpolation, and see where extrapolation begins.
- Propagate rise and fall arrival times and slews through a netlist, and watch an input slew's effect die out.
- See why graph-based analysis scales and how much it gives away against path-based analysis.
- Map logic onto cells by dynamic programming for area and for delay.
- Measure what OCV derates and CRPR do to slack.

## Background

The chapter's §3.3 explains NLDM tables and interpolation, §3.4 the timing graph, §3.5 the clocked checks and §3.7 OCV and CRPR; §3.2 explains tree covering.

The data file `sky130_hd_subset.json` holds a subset of SkyWater's open SKY130 standard-cell library (`sky130_fd_sc_hd`, Apache License 2.0), extracted unchanged from the per-cell Liberty JSON files at <https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd/tree/main/cells> (read 24 Nov 2026). It contains, at the typical corner `tt_025C_1v80`, the area, pin capacitances, Liberty function and four NLDM tables per arc of `inv_1`, `buf_1`, `nand2_1`, `nor2_1`, `nand3_1`, `nand4_1`, `and2_1`, `a21oi_1`, `a22oi_1` and `o21ai_1`, and the clock-to-Q, setup and hold tables of the flip-flop `dfxtp_1`; plus `inv_1` at the slow corner `ss_100C_1v60`. Times are in ns, capacitances in pF, areas in µm². These are pre-layout models.

Files:

- `sta.py`: `interp2` (bilinear, with linear extrapolation), `arc_delay`, `clk_to_q`, `ff_check`; a `Netlist` class with `analyze` (graph-based late or early arrival and slew), `required`, `worst_path`, `count_paths` and `path_based` (enumerate and re-time every path); `setup_slack`, `hold_slack`, `ocv_setup_slack`, `path_sigma`, `count_paths`.
- `techmap.py`: subject trees (`IN`, `INV`, `NAND`), SKY130 cell patterns, `matches`, `min_area`, `min_delay` and `truth_table`.
- `19-10-sta-lab.ipynb`: the procedure below.

There is no circuit simulation here: the delays are the foundry's characterized tables. Open-source tools that do the same at full scale are Yosys (synthesis, with ABC for mapping) and OpenSTA (timing); see Optional extensions.

## Procedure

1. **Tables.** Plot `inv_1`'s rising delay against load for each input slew. Predict the delay at 0.25 pF, beyond the last load point (0.181 pF), then compute it (Part 1). Compare the typical and slow corners at one operating point.
2. **Slew propagation.** Build a chain of four `inv_1` cells driving 0.01 pF. Predict how the output arrival changes when the input slew rises from 0.01 ns to 0.5 ns, and which stages absorb the change (Part 2).
3. **Path explosion.** Build chains of "diamonds" (each stage splits into an `inv_1` and a `buf_1` that reconverge in a `nand2_1`). Predict the number of paths for 10 diamonds and whether graph-based analysis can be beaten by path-based analysis here (Part 3).
4. **Mapping.** Map Example 19-10.3's tree and the AOI22 tree for minimum area and minimum delay (Part 4).
5. **Derates.** For Example 19-10.5, sweep a symmetric derate $1 \pm d$ and find where the slack reaches zero with and without CRPR (Part 5).

## Expected results

- Part 1: the extrapolated delay at 0.25 pF (input slew 0.0531329 ns) is 1.451 ns, continuing the last segment's slope; at Example 1's point the slow corner is 1.33 (rise) and 1.62 (fall) times slower.
- Part 2: with a 0.01 ns input slew the chain's output rises at 160.42 ps and falls at 147.01 ps; with 0.5 ns, 244.35 and 282.08 ps. Almost all the difference is in the first stage and the second; by the third stage the slews have returned to within a few picoseconds of the fast-input case, because each stage's output slew depends mostly on its own load.
- Part 3: 10 diamonds have 1024 paths; graph-based analysis gives a rising arrival of 1407.19 ps and path-based analysis 1407.15 ps. The gap is tiny here because at each NAND the latest-arriving input (through the buffer) also produces the worst output slew, or one within about 0.1 ps of it; Problem 19-10.11 shows a case where the two differ.
- Part 4: Example 3's minimum area is 16.2656 µm² (`and2_1` + `nand4_1` + `inv_1`), its minimum delay 248.9 ps (`inv_1` + `nand2_1` + `nand4_1` + `inv_1`); the AOI22 tree maps to `a22oi_1` for both objectives.
- Part 5: without CRPR the slack reaches zero at $d$ = 19.8 %; with CRPR at 28.6 %.

## Discussion

1. Why do Liberty tables have more points at small slews and loads than at large ones?
2. In Part 2, why does a slow input edge stop mattering after two stages?
3. Why does graph-based analysis stay in use if path-based analysis is more accurate?
4. In Part 4, why is the delay-optimal cover not simply the one with the fewest cells?

**Answers.**

1. The index values are spaced roughly geometrically (0.01 to 1.5 ns, 0.0005 to 0.18 pF), so that interpolation error stays small where delay changes fastest relative to its size and where most real operating points lie; large values are mainly there to bound extrapolation.
2. An inverter's output slew is set mostly by its drive strength and its load; the input slew enters only weakly (the rows of the transition table change much less than the columns). So a slow edge is "re-sharpened" by each stage, and the stage after next sees nearly the usual slew.
3. Graph-based analysis is linear in the circuit size and always pessimistic (safe); path-based analysis is exponential in the worst case. Tools use graph-based analysis everywhere and path-based re-timing only on the few paths that fail, to recover margin where it matters.
4. Cells differ in delay: a two-stage cell such as `and2_1` is slower than an `inv_1`–`nand2_1` pair at this load even though it is one cell, and a deep stack (`nand4_1`) is slower per cell but saves a stage. The cover's delay is the slowest chain of cells, not their count.

## Optional extensions

- With Yosys installed (it is packaged by most Linux distributions), synthesize a small Verilog module against a SKY130 Liberty file with `read_verilog`, `synth -top`, `dfflibmap -liberty` and `abc -liberty`, and compare the cells it chooses with Part 4.
- With OpenSTA installed, read the same Liberty file, the netlist and a two-line SDC file (`create_clock`, `set_input_delay`), and compare `report_checks` with this lab's engine on the same circuit.

## Optional hardware

None: timing analysis is a software activity. For a full open-source flow on SKY130, see OpenROAD-flow-scripts, introduced in 19-11.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-10.a | inv_1 rise delay extrapolated to 0.25 pF | 1.451 | ns |
| Lab 19-10.b | four-inverter chain, rising output, 0.01 ns input slew | 160.42 | ps |
| Lab 19-10.c | four-inverter chain, falling output, 0.01 ns input slew | 147.01 | ps |
| Lab 19-10.d | four-inverter chain, rising output, 0.5 ns input slew | 244.35 | ps |
| Lab 19-10.e | four-inverter chain, falling output, 0.5 ns input slew | 282.08 | ps |
| Lab 19-10.f | graph-based rising arrival, 10 diamonds | 1407.19 | ps |
| Lab 19-10.g | path-based rising arrival, 10 diamonds | 1407.15 | ps |
| Lab 19-10.h | paths through 10 diamonds | 1024 | — |
| Lab 19-10.i | symmetric derate for zero slack, no CRPR | 19.8 | % |
| Lab 19-10.j | symmetric derate for zero slack, with CRPR | 28.6 | % |
