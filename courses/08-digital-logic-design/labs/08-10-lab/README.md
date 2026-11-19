# Lab 08-10 · Timing, Metastability and Clock-Domain Crossing

**Chapter:** [08-10](../../chapters/08-10-timing-metastability-cdc.md) · **Notebook:** [08-10-timing-cdc.ipynb](08-10-timing-cdc.ipynb) · **Time:** about 3 hours

## Objective

1. Run static timing analysis on a small netlist and confirm it against brute-force path enumeration.
2. Simulate metastability resolution, and recover $\tau$ and $T_W$ from the simulated failure fractions.
3. Explore synchronizer MTBF against the number of stages, the clock frequency and $\tau$.
4. Show by enumeration why binary counters cannot cross clock domains bit by bit and Gray counters can.
5. Verify a two-flip-flop synchronizer, a toggle pulse synchronizer, a reset synchronizer and an asynchronous FIFO in Verilog between unrelated clocks.

## Background

Chapter sections 3.1 to 3.9 and Examples 08-10.1 to 08-10.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-10-timing-cdc.ipynb](08-10-timing-cdc.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [cdc.v](cdc.v) | `sync2`, `pulse_sync` (toggle), `reset_sync`, and `async_fifo` (Gray-coded pointers, two-flip-flop pointer synchronizers, conservative full and empty flags) | `cdc_tb.v` |
| [cdc_top.v](cdc_top.v) | A top level for lint tools | Lint only |
| [cdc_tb.v](cdc_tb.v) | Fills and drains the FIFO, streams 3000 words between 100 MHz and about 137 MHz with random stalls on both sides, sends 200 pulses from 400 MHz to about 98 MHz, and checks the reset synchronizer | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_notebooks.py 08-10
```

```bash
python tools/run_hdl.py
```

## Procedure

1. **STA (Part 1).** Compute arrival times in topological order, find the critical path and the slack at 3 GHz, and check against all 10 launch-to-capture paths.
2. **Metastability (Part 2).** *Predict first:* what does the fraction of unresolved samples look like against time on a semilog plot? The notebook simulates ten million samples and fits a line.
3. **MTBF (Part 3, the chapter's guided exercise).** *Predict first:* how much does a two-flip-flop synchronizer's MTBF change from 500 MHz to 1 GHz?
4. **Counters across domains (Part 4).** Count the impossible values a bit-by-bit sample can produce for binary and Gray counters.
5. **Verilog.** Run `cdc_tb.v`. Then make the FIFO's full flag compare *binary* pointers synchronized bit by bit instead of Gray pointers, and explain why the testbench may still pass (and why that proves nothing).

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | STA | critical arrival 275 ps through R1 or R2, g1, g2, g5, g6; $f_{\max}$ 3.28 GHz; slack at 3 GHz 28.3 ps |
| 2 | metastability | a straight line on a semilog plot; fitted $\tau$ and $T_W$ within about 1% of 20 ps |
| 3 | MTBF | about $10^{22}$ times higher at 500 MHz; at 2 GHz two flip-flops fail every few minutes |
| 4 | counters | binary 48 impossible values per 16-count cycle, Gray 0 |
| Verilog | testbench | `TEST PASSED`; 16 words accepted until full, 16 read until empty, 3016 words in order, 200 pulses out for 200 in |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-10.a | critical arrival time | 275 | ps |
| Lab 08-10.b | maximum frequency | 3.28 | GHz |
| Lab 08-10.c | slack at 3 GHz | 28.3 | ps |
| Lab 08-10.d | launch-to-capture paths | 10 | — |
| Lab 08-10.e | fitted τ | 19.94 | ps |
| Lab 08-10.f | log10 of the MTBF ratio, 500 MHz over 1 GHz | 22.0 | — |
| Lab 08-10.g | impossible binary samples per cycle | 48 | — |
| Lab 08-10.h | impossible Gray samples per cycle | 0 | — |
| Lab 08-10.i | FIFO words in the testbench | 3016 | — |
| Lab 08-10.j | pulses through the toggle synchronizer | 200 | — |

**Reading the key.** The critical path is $50 + 40 + 60 + 55 + 70 = 275$ ps (launch, g1, g2, g5, g6). The MTBF ratio is $2e^{50}$: the factor 2 from $F_C$ in the denominator and $e^{50}$ from 1000 ps more resolution time at $\tau$ = 20 ps. A transition that changes $k$ bits can be sampled in $2^k$ ways, of which $2^k - 2$ are impossible; over a 4-bit binary cycle the changes are 1, 2, 1, 3, 1, 2, 1, 4, ... bits, giving $8 \times 0 + 4 \times 2 + 2 \times 6 + 2 \times 14 = 48$.

## Discussion questions

1. Why does the STA in Part 1 not need to enumerate paths, and why would enumeration fail on a real chip?
2. In the chapter's resolution figure (the same simulation), the simulated fraction of unresolved samples drifts above the theory line beyond about 230 ps. Is the model wrong there?
3. The testbench passes even though Icarus never models metastability. What does it prove, and what does it not?
4. If the FIFO compared binary pointers synchronized bit by bit, why might `cdc_tb.v` still pass?
5. Why does `pulse_sync` require pulses to be spaced several destination cycles apart, and what happens if they are not?

<details><summary>Answers to the discussion questions</summary>

1. Arrival times propagate: each gate's arrival depends only on its inputs' arrivals, so one pass in topological order handles every path at once, in time proportional to the number of gates. The number of paths, by contrast, can double with every level of reconvergent logic; a real chip has far more paths than could ever be listed.
2. No. With $10^7$ samples, a fraction near $10^{-7}$ means one or two samples, so the measurement is dominated by counting noise (03-02's Poisson statistics). The points near the line, where hundreds or thousands of samples remain, are the ones that test the model.
3. It proves the crossing *logic* is right: Gray pointers advance correctly, the flags are conservative, no word is lost or duplicated whatever the relative clock phases, every pulse is regenerated once, and the reset synchronizer releases on a clock edge. It does not prove the synchronizers are long enough: in simulation a flip-flop never goes metastable and a binary bit-by-bit crossing never samples mid-transition inconsistently, so MTBF must come from analysis (Parts 2 and 3), and structural CDC tools must check that every crossing uses a proper scheme.
4. In simulation all bits of a binary pointer change at the same instant and each synchronizer flip-flop samples a clean old or new value, consistently across bits, so the destination sees a valid pointer. Real flip-flops sampling during the transition can disagree bit by bit, which the simulator never shows. That is exactly why CDC bugs escape simulation and need structural checks.
5. Each pulse toggles the source level once; the destination detects a change by comparing successive synchronized samples. If two pulses arrive within one destination sampling interval, the level toggles twice and returns to its old value before being sampled, so the destination sees no change and both pulses are lost. The testbench spaces pulses 30 to 61 ns apart, roughly three to six destination cycles.

</details>

## Optional hardware

On an FPGA board, run a fast counter from one clock and sample it with an unrelated clock (for example, two oscillators or a PLL output with a slightly different frequency), first with binary values synchronized bit by bit and then with Gray-coded values. Log the differences between consecutive samples with an embedded logic analyzer: the binary version eventually shows large jumps, while the Gray version never moves by more than one. The vendor tools' clock-domain-crossing and metastability reports should also flag the binary crossing.
