# Lab 08-06 · Latches, Flip-Flops and Sequential Timing

**Chapter:** [08-06](../../chapters/08-06-latches-and-flip-flops.md) · **Notebook:** [08-06-sequential-timing.ipynb](08-06-sequential-timing.ipynb) · **Time:** about 2.5 hours

## Objective

1. See bistability: draw a cross-coupled inverter pair's "butterfly" curve and find its three equilibrium points.
2. Watch a cross-coupled pair resolve from near its metastable point, and compare the time with the loop-gain theory.
3. Build an SR latch, a D latch and a master–slave flip-flop from gates in Verilog, and check them against their definitions.
4. Map the setup and hold constraints of a register-to-register path.

## Background

Chapter sections 3.1 to 3.8 and Examples 08-06.1 to 08-06.7. You need Python with NumPy, SciPy and Matplotlib, ngspice and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-06-sequential-timing.ipynb](08-06-sequential-timing.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [inverter_vm.cir](inverter_vm.cir) | A self-biased inverter settles at $V_M$; a DC sweep of a second inverter finds where its transfer curve crosses $V_{out} = V_{in}$ | Chapter answer key (Th 08-06.c) |
| [latches.v](latches.v) | Gate-level SR latch, D latch and master–slave flip-flop; behavioral flip-flops with enable and synchronous or asynchronous reset | `latches_tb.v` |
| [latches_top.v](latches_top.v) | A top level for lint tools | Lint only |
| [latches_tb.v](latches_tb.v) | Checks the SR latch (Example 08-06.1), the D latch and the master–slave flip-flop on random stimulus, and the two kinds of reset | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_spice.py 08-06
```

```bash
python tools/run_hdl.py
```

## Procedure

1. **Bistability (Part 1).** *Predict first:* where do the transfer curve and its mirror image cross? The notebook computes the square-law transfer curve and draws the butterfly.
2. **Resolution (Part 2, the chapter's guided exercise).** *Predict first:* starting 1 mV from $V_M$, how many time constants until the two nodes are 0.9 V apart? The notebook integrates the full nonlinear circuit with 10 fF on each node and compares with the small-signal prediction $\tau \ln(0.9\ \text{V}/1\ \text{mV})$, where $\tau = C/g_m$.
3. **ngspice.** Run `inverter_vm.cir` and compare both measurements with $V_M$ from the formula.
4. **Latch versus flip-flop (Part 3).** Replay Example 08-06.2 and Problem 08-06.2, then run random waveforms and count how often a latch and a flip-flop disagree.
5. **Timing map (Part 4).** For a path with given flip-flop parameters, shade the region of (clock period, logic delay) where setup holds, and see that hold does not depend on the period.
6. **Verilog.** Run `latches_tb.v`. Then swap the clocks of the master and slave latches in `dff_ms` and predict what the testbench will report.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | butterfly crossings | three: the two rail states and $V_M$ = 0.846 V |
| 2 | resolution from 1 mV | see the key: about 6.8 time constants; the nonlinear circuit takes slightly longer than the small-signal estimate because the gain falls as the nodes leave $V_M$ |
| 3 | ngspice | both measurements equal $V_M$ to within 0.1% |
| 4 | latch versus flip-flop | they agree only when $D$ is stable while the latch is transparent |
| Verilog | testbench | `TEST PASSED`; with the latch clocks swapped, the flip-flop triggers on the falling edge and the comparison with `dff_rtl` fails |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-06.a | nMOS transconductance at $V_M$ | 0.429 | mS |
| Lab 08-06.b | pMOS transconductance at $V_M$ | 0.336 | mS |
| Lab 08-06.c | time constant $\tau = C/(g_{mn} + g_{mp})$, 10 fF | 13.07 | ps |
| Lab 08-06.d | time constants to grow 1 mV to 0.9 V | 6.80 | — |
| Lab 08-06.e | small-signal resolution time | 88.9 | ps |
| Lab 08-06.f | resolution time, nonlinear simulation | 89.9 | ps |

**Reading the key.** Linearize each inverter at $V_M$: a small change $v$ at its input drives a current $-(g_{mn} + g_{mp})v$ into its output node, where $g_{mn} = \beta_n(V_M - V_{Tn})$ and $g_{mp} = \beta_p(V_{DD} - V_M - |V_{Tp}|)$ are the transistors' transconductances in saturation (with $\lambda = 0$ there is no output conductance). For the two nodes of the pair, $C\,dv_1/dt = -g_m v_2$ and $C\,dv_2/dt = -g_m v_1$. Subtracting, the difference $\Delta = v_1 - v_2$ obeys $C\,d\Delta/dt = g_m\Delta$, so it grows as $e^{t/\tau}$ with $\tau = C/g_m$. The full simulation takes about 1 ps longer because, far from $V_M$, the transistors leave saturation and the gain drops.

## Discussion questions

1. Why does the self-biased inverter in `inverter_vm.cir` settle at exactly $V_M$, while a cross-coupled pair never stays there?
2. What would happen to the resolution time if the node capacitance doubled? If the supply voltage dropped so that $V_M - V_T$ halved?
3. In `latches_tb.v`, why does the testbench change $D$ only while the clock is low when comparing the master–slave flip-flop with `dff_rtl`?
4. The testbench never releases $S = R = 1$ to $0, 0$ simultaneously. What would a zero-delay simulator do, and what would real hardware do?
5. Why do asynchronous-reset flip-flops need `posedge rst` in the sensitivity list rather than just `rst`?

<details><summary>Answers to the discussion questions</summary>

1. The self-biased inverter is a single stage with negative feedback (its output drives its own input through a wire), which is stable: any deviation is opposed. The cross-coupled pair has two inversions around the loop, which is positive feedback with gain above 1 at $V_M$, so deviations grow. The same transistors, wired differently, give a stable bias point or a bistable memory.
2. Doubling $C$ doubles $\tau$ and therefore the resolution time. Halving $V_M - V_T$ halves both transconductances and doubles $\tau$ too: low-voltage operation makes latches and synchronizers slower to resolve, a real concern for always-on chips running near threshold ([08-10](../../chapters/08-10-timing-metastability-cdc.md)).
3. The gate-level flip-flop has zero-delay gates, so a change of $D$ exactly at the clock edge would race with the master latch closing; real flip-flops would violate setup or hold. So the testbench never changes $D$ at an edge. It changes $D$ twice per cycle instead: while the clock is low, to set up the next edge, and in the middle of the high phase, well clear of both edges. A flip-flop must ignore the second change, while a latch would pass it straight to $Q$, so the test tells the two apart (a latch substituted for `dff_ms` fails it).
4. With this lab's zero-delay gates the simulator does not oscillate: it processes the two input changes in some order, and whichever is processed first decides the state. Releasing with `s = 0; r = 0;` leaves $Q$ = 0, while `r = 0; s = 0;` leaves $Q$ = 1, a race decided by statement order. Give both NOR gates the same delay (`nor #1`) and the simulation instead oscillates between 00 and 11 forever. Real gates are never perfectly matched, so hardware falls into one state or the other, possibly after lingering near the metastable point, and which one is unpredictable.
5. `always @(posedge clk or rst)` would re-run the block on *both* edges of `rst`, including its release, and at the release `if (rst)` is false, so the register would load $D$ at a moment that is not a clock edge. With `posedge rst` the block runs on the rising edge of reset (asserting it) and otherwise only on clock edges, which is what synthesis maps to an asynchronous-reset flip-flop.

</details>

## Optional hardware

A 74HC00 (quad NAND) on a breadboard makes an $\overline{S}\,\overline{R}$ latch with two push buttons and an LED; a 74HC74 dual D flip-flop with a push button as the clock shows edge triggering, and also shows switch bounce: one press can produce several clock edges, so the flip-flop toggles unpredictably unless the button is debounced (an RC filter with a Schmitt trigger, or a debouncing state machine, [08-08](../../chapters/08-08-finite-state-machines.md)).
