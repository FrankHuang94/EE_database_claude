# Problems 19-10 · The ASIC Flow I: Synthesis and Static Timing Analysis

Chapter: [19-10](../chapters/19-10-synthesis-and-sta.md) · Worked solutions: [19-10 solutions](../solutions/19-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Times in ns or ps as stated, capacitances in pF, areas in µm². Liberty values are SKY130 `sky130_fd_sc_hd` at the typical corner (tt, 25 °C, 1.80 V). Setup slack is required minus arrival; hold slack is arrival minus required; negative means failing. Cell areas and mapping delays are those of Example 19-10.3. Problems marked *(lab)* can be checked with `labs/19-10-lab/sta.py` or `techmap.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-10.1 [A] *(lab)*

**A NAND2 table lookup.** The `cell_fall` table of `nand2_1` (input A to Y) has, at input slews 0.0531329 and 0.122474 ns and loads 0.00346659 and 0.00912787 pF, the values 0.0504824 and 0.0797753 ns (first slew) and 0.0698132 and 0.1038626 ns (second slew). Find the falling-output delay at an input slew of 0.100 ns and a load of 0.0060 pF.

### Problem 19-10.2 [A] *(lab)*

**A linear model from the table.** On the same arc, the `cell_rise` row at input slew 0.0531329 ns has 0.0970882 ns at 0.00912787 pF and 0.4287654 ns at 0.0632852 pF. (a) Fit $D = D_0 + R_{\text{eff}}C_L$ through these two points. (b) Predict the delay at 0.030 pF. (c) The table's bilinear interpolation gives 225.05 ps at that point. How good is the linear model, and why?

### Problem 19-10.3 [A]

**A two-output block.** Inputs p, q and r arrive at 0, 10 and 30 ps. Gates (one delay each): H1 = NAND(p, q), 35 ps; H2 = NOR(q, r), 50 ps; H3 = INV(H1), 20 ps; H4 = NAND(H1, H2), 45 ps; H5 = NAND(H3, H4), 40 ps, driving output z (required at 150 ps); and W = INV(H2), 25 ps, driving output w (required at 120 ps). (a) Find all arrival times, required times and slacks. (b) Identify the critical path and its slack. (c) How many input-to-output paths are there? (d) By how much must H2 be sped up to meet timing, and does any other path then fail?

### Problem 19-10.4 [B]

**Edges through unate arcs.** A signal x drives an inverter (output rising 30 ps, falling 20 ps), then a NAND2 whose other input is tied high (rising 40 ps, falling 35 ps), then a buffer (rising 50 ps, falling 45 ps). The rising edge of x arrives at 0 ps and the falling edge at 8 ps. (a) Find the arrival times of the rising and falling output edges. (b) What would a tool that ignored edges, adding each gate's worst delay to the latest input arrival, report? (c) Which arcs are negative unate and which positive?

### Problem 19-10.5 [B] *(lab)*

**Mapping two AOI-type functions.** Using the library and delays of Example 19-10.3, plus `a22oi_1` (7.5072 µm², worst arc 207.0 ps): (a) list every cover of the subject tree `INV(NAND(NAND(A, B), NAND(C, D)))` for $\overline{AB + CD}$, with area and delay, and pick the best for each objective; (b) do the same for $(A + B)C$, written as `INV(NAND(NAND(INV A, INV B), C))`; (c) why does the complex cell win on both counts in (a)?

### Problem 19-10.6 [B]

**A faster clock on SKY130.** Two `dfxtp_1` flip-flops on a 1.5 ns clock. Launch latency 0.25 ns, capture latency 0.20 ns. Q rises with $t_{pcq} = t_{ccq} = 0.307$ ns, the logic does not invert, so D rises: setup 0.051 ns, hold −0.029 ns (clock-to-Q at 0.053 ns clock slew and 3.4 fF load; setup and hold at 0.01 ns clock and data slews). Logic delay is 0.85 ns maximum, 0.10 ns minimum. Uncertainty 0.08 ns (setup), 0.04 ns (hold). (a) Find the setup slack and the maximum frequency. (b) Find the hold slack. (c) If the logic inverted instead (D falling, setup 0.103 ns), what would the setup slack be?

### Problem 19-10.7 [B]

**I/O budgets.** A block runs on a 2.5 ns clock with 0.1 ns setup uncertainty. Its constraints set a 0.6 ns input delay and a 0.7 ns output delay. Treat the clock at the source as ideal (zero latency) except where stated. Find the slack of: (a) a combinational path from an input port to an output port with 1.0 ns of logic; (b) an input-to-register path with 1.5 ns of logic into a flip-flop with 0.1 ns setup and 0.3 ns clock latency; (c) a register-to-output path from a flip-flop with 0.3 ns clock latency and 0.3 ns clock-to-Q through 1.2 ns of logic. (d) Why does clock latency help in (b) and hurt in (c)?

### Problem 19-10.8 [B]

**A two-cycle path.** On a 1.5 ns clock, a path's logic takes 2.5 ns (maximum) and 0.4 ns (minimum); the registers have $t_{pcq} = t_{ccq} = 0.30$ ns, setup 0.10 ns and hold 0.05 ns; there is no skew or uncertainty. The capture register is enabled only every second cycle. (a) Find the single-cycle setup slack. (b) Find the setup slack with `set_multicycle_path 2 -setup`. (c) Find the hold slack if only the setup multicycle is declared. (d) Find the hold slack after adding `set_multicycle_path 1 -hold`.

### Problem 19-10.9 [B]

**OCV and CRPR for hold.** A hold check: common clock segment 0.50 ns, launch branch 0.10 ns, capture branch 0.30 ns; $t_{ccq} = 0.25$ ns, shortest logic 0.05 ns, hold time 0.02 ns. Derates: early 0.92 (launch clock, clock-to-Q and data), late 1.08 (capture clock); the hold time is not derated. Find the hold slack (a) without derates, (b) with derates and no CRPR, (c) with CRPR.

### Problem 19-10.10 [C]

**When statistics beat flat derates.** Each stage of a path has delay variation σ/μ = 4 %, and the signoff criterion is mean + 3σ. (a) What flat per-stage derate does this imply? (b) If stages are independent, what is the effective path-level derate for paths of 4, 16 and 64 stages, and from what depth is it at most 4 %? (c) With a pairwise correlation of 0.2, what is the effective derate at 16 and 64 stages, and what is its limit for very deep paths? (d) What does (c) say about which variation a statistical model can and cannot remove?

### Problem 19-10.11 [C]

**Graph-based against path-based slews.** A gate G has two inputs: A arrives at 100 ps with a 20 ps slew; B arrives at 60 ps with a 120 ps slew. G's delay is $30 + 0.3\,s_{in}$ ps and its output slew $25 + 0.2\,s_{in}$ ps. G drives a gate H whose delay is $40 + 0.3\,s_G$ ps. (a) Using graph-based analysis (the latest arrival and the worst slew at G's output, from whichever inputs), find the arrival time at H's output. (b) Re-time each path with its own slew (path-based). (c) How much pessimism did graph-based analysis add, and why is it always on the safe side here?

### Problem 19-10.12 [C]

**Hold at the slow corner.** At the typical corner a register-to-register path has launch latency 0.20 ns, capture latency 0.60 ns, $t_{ccq} = 0.25$ ns, shortest logic 0.20 ns and hold time 0.02 ns (no uncertainty). At the slow corner the clock-tree buffers slow by a factor of 1.5, while the flip-flop and the data-path cells slow by 1.3. (a) Find the hold slack at both corners. (b) Explain why the slow corner can be the hold-limiting one. (c) What delay must a hold buffer add at the slow corner, and how much will it add at the typical corner if it scales by 1.3?

### Problem 19-10.13 [B]

**Writing the constraints.** A block has a clock port `clk` at 500 MHz, data inputs `din[7:0]` and `en`, and outputs `dout[7:0]`. The inputs arrive 0.80 ns after the clock edge at the source (the clock with zero latency); the outputs must reach the next block 0.60 ns before the next clock edge, because that block needs this time for its own logic and setup; each output drives 0.01 pF, and each input is driven by a `sky130_fd_sc_hd__buf_2`. Reserve 0.05 ns of clock uncertainty. (a) Write the SDC (units ns and pF). (b) Find the slack of an input-to-register path with 1.05 ns of logic into a flip-flop with 0.06 ns setup and an ideal clock. (c) Find the slack of a register-to-output path with 0.31 ns clock-to-Q and 0.60 ns of logic. (d) The downstream team revises its need to 1.10 ns. What is the new slack of the path in (c), and how much logic can that path have? (e) The SDC writer forgot the `set_input_delay` for `en`. What happens to the paths that start at `en`?

### Problem 19-10.14 [B]

**Recognizing a false path.** A register R1 (clock-to-Q 0.30 ns) drives two multiplexers in series, ending at a register R2 (setup 0.08 ns) on a 2.0 ns clock with no skew or uncertainty. Each multiplexer adds 0.15 ns. M1 passes its 1-input, which comes from R1 through block X (1.20 ns), when $s = 1$, and its 0-input, a 0.10 ns bypass from R1, when $s = 0$. M1's output feeds block Y (1.00 ns), which goes to M2's 1-input, and a 0.10 ns bypass to M2's 0-input. M2's select is $ar{s}$. The select $s$ comes from a configuration register that is written only while the block is idle. (a) List the four structural paths from R1 to R2 with their logic delays and the value of $s$ each needs. (b) What setup slack does STA report without exceptions? (c) How many of the paths are false, and what is the true worst setup slack? (d) Write an exception that removes only the false path that matters for setup. (e) A colleague writes `set_false_path -through [get_pins u_x/Z]`, where `u_x/Z` is the output of block X. What slack does STA now report, and what has gone wrong? (f) Why does the exception depend on $s$ being static?

### Problem 19-10.15 [C]

**A half-cycle path.** A rising-edge flip-flop launches data through combinational logic to a falling-edge flip-flop. The clock has a 2.0 ns period and a 50 % duty cycle, and is ideal (zero latency at both flip-flops). Both flip-flops have $t_{pcq} = t_{ccq} = 0.30$ ns, setup 0.10 ns and hold 0.04 ns. Uncertainty is 0.05 ns for setup and 0.02 ns for hold. The logic delay is 0.45 ns maximum and 0.05 ns minimum. (a) Find the setup slack. (b) Find the hold slack, stating which pair of edges the hold check uses. (c) Repeat (a) and (b) if the clock's high time shrinks to 45 % of the period. (d) At a 50 % duty cycle, what is the highest clock frequency this path allows, and what would it be for the same logic between two rising-edge flip-flops? (e) Give two reasons designers use half-cycle paths despite this cost.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. The synthesis flow and its inputs | 5, 7 |
| 2. Technology mapping by tree covering | 5 |
| 3. Liberty lookup and timing propagation | 1, 2, 3, 4, 11 |
| 4. Setup, hold and I/O slack; SDC | 6, 7, 8, 13, 15 |
| 5. Corners, OCV, CRPR and statistics | 9, 10, 12 |
| 6. False and multicycle paths | 8, 14 |
