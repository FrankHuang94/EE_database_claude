# Lab 19-07 · Timing Budgets and Metastability

Chapter: [19-07 · Sequential Circuits, Timing and Clocking](../../chapters/19-07-sequential-timing-and-clocking.md)

## Objective

- Apply setup and hold constraints with skew and jitter, and find a path's allowed skew window.
- See the diminishing returns of pipelining.
- Watch a cross-coupled inverter pair resolve from metastability, in Python and ngspice, and extract its time constant.
- Compute synchronizer MTBF and how it grows with resolution time.

## Background

Setup: $T_c \ge t_{pcq} + t_{pd} + t_{setup} + t_{jitter} - \delta$; hold: $t_{ccq} + t_{cd} \ge t_{hold} + \delta$ (§3.2). A pipeline of $N$ stages has $T_c = t_L/N + t_o$ (§3.3). A metastable pair resolves as $\Delta v_0e^{t/\tau}$ with $\tau = C/g_m$ (§3.5), and a synchronizer's MTBF is $e^{t_r/\tau}/(T_0f_{clk}f_{data})$.

Files:

- `meta.cir`: two cross-coupled inverter pairs (level-1 model, 10 fF per node) released with 1 mV and 1 µV offsets.
- `timing.py`: `min_period`, `hold_slack`, `pipeline_period`, `max_borrow`, `two_phase_min_period`, `resolve_time` (the pair as square-law ODEs), `tau_small_signal` and `mtbf`.
- `19-07-timing-lab.ipynb`: the procedure below.

## Procedure

1. **Metastability.** Predict the resolution times for 1 mV and 1 µV offsets from τ = 100 ps. Run `ngspice -b meta.cir` and Part 1, which sweeps the offset from 1 nV to 10 mV.
2. **Time constant.** Predict τ with twice the node capacitance and with twice the transistor width; check with `resolve_time` (Part 2).
3. **Skew windows.** Plot setup and hold slack against skew for Example 19-07.3 (Part 3).
4. **Pipelining.** Plot throughput, latency and overhead share against depth for overheads of 30, 60 and 120 ps (Part 4).
5. **MTBF.** Plot MTBF against resolution time for Example 19-07.6(b) and Problem 19-07.10 (Part 5).

## Expected results

- Part 1: 643.9 ps for 1 mV and 1334.6 ps for 1 µV in both ngspice and Python; plotted against $\ln(1/\Delta v_0)$ the resolution time is a straight line of slope τ = 100 ps.
- Part 2: τ doubles to 200 ps with twice the capacitance and halves to 50 ps with twice the width.
- Part 3: the window runs from −50 ps (setup) to +35 ps (hold).
- Part 4: with 60 ps overhead, throughput rises from 0.485 GHz (1 stage) to 5.41 GHz (16 stages), while overhead grows to 32.4% of the cycle.
- Part 5: each extra τ of resolution time multiplies MTBF by $e$; the 10-year target in Problem 10 needs 500.8 ps.

## Discussion

1. Why is the resolution time a straight line against the logarithm of the initial offset?
2. Why does the same edge not suffer from jitter in the hold check?
3. Why do two flip-flops in series make a much better synchronizer than one, even though the second is identical?
4. In `meta.cir`, why do the two pairs need such tight simulator tolerances?

**Answers.**

1. Near the metastable point the difference grows as $e^{t/\tau}$, so the time to reach a fixed level is $\tau\ln(\Delta V/\Delta v_0)$: linear in $\ln(1/\Delta v_0)$, until the pair leaves the small-signal region near the end.
2. The hold check compares the launch and capture of the same clock edge at two registers; whatever that edge's timing error, both see it.
3. The first flip-flop gets a whole clock period to resolve before the second samples it, and the probability of still being unresolved falls exponentially with that time; the second flip-flop then almost always samples a clean level.
4. A 1 µV offset is far below default absolute and voltage tolerances; with loose tolerances, numerical error acts as a random initial offset and the measured resolution time becomes meaningless.

## Optional hardware

Two inverters of a CD4069 cross-coupled into a latch, with a weak resistive path to force it toward balance, show slow, noise-dependent resolution on an oscilloscope; an RS latch made from a CD4011 driven by two nearly simultaneous edges from a function generator shows occasional long settling or runt pulses.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-07.a | tau with twice the capacitance | 200 | ps |
| Lab 19-07.b | tau with twice the width | 50 | ps |
