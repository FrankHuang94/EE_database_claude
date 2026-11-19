# Lab 08-08 · Finite State Machines

**Chapter:** [08-08](../../chapters/08-08-finite-state-machines.md) · **Notebook:** [08-08-state-machines.ipynb](08-08-state-machines.ipynb) · **Time:** about 3 hours

## Objective

1. Simulate Moore and Mealy sequence detectors and check them against a reference model and against each other.
2. Implement partition refinement and confirm, by simulation, that the minimized machine behaves like the original.
3. Measure how much the choice of state encoding changes the minimized logic of a small FSM.
4. Count illegal codes and the single-bit upsets each encoding can detect.
5. Write FSMs in Verilog in the three-block style, including a controller with a timer, and verify them with a self-checking testbench that also forces illegal states.

## Background

Chapter sections 3.1 to 3.9 and Examples 08-08.1 to 08-08.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-08-state-machines.ipynb](08-08-state-machines.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [fsm.v](fsm.v) | Moore and Mealy 101 detectors (`det101_moore`, `det101_mealy`) and the traffic-light controller of Example 08-08.6 (`traffic`), all in the three-block style | `fsm_tb.v` |
| [fsm_top.v](fsm_top.v) | A top level for lint tools | Lint only |
| [fsm_tb.v](fsm_tb.v) | Compares both detectors with a reference model on 3000 random inputs, checks the one-cycle lag, forces illegal codes, and checks every traffic-light phase and safety rule | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_notebooks.py 08-08
```

```bash
python tools/run_hdl.py
```

## Procedure

1. **Detectors (Part 1).** *Predict first:* on random input, about what fraction of cycles end a 101 pattern? The notebook runs both detectors on 10 000 random bits, compares them with a direct pattern match, and confirms the Mealy output leads the Moore output by one cycle.
2. **Minimization (Part 2).** Run partition refinement on Example 08-08.4 and Problem 08-08.7, then on random machines; every minimized machine is checked against its original on all input sequences up to length 8 (7 for the random machines).
3. **Encodings (Part 3, the chapter's guided exercise).** *Predict first:* how much can the total literal count of the Moore 110 detector vary across the 24 ways to assign its four codes? The notebook minimizes all 24 exactly and lists the best.
4. **Upsets (Part 4).** Tabulate, for 2 to 16 states, the fraction of single-bit flips that land on an illegal code with binary codes $0 \ldots N-1$, against 100% for one-hot.
5. **Verilog.** Run `fsm_tb.v`. Then delete the `default: next = S0;` line and the `next = S0;` default at the top of `det101_mealy`'s next-state block, and predict what Icarus and Verilator report.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | detectors | both match the reference on every cycle; detections in about 1/8 of cycles; the Mealy output leads by one cycle |
| 2 | minimization | Example 08-08.4: 7 states to 4; Problem 08-08.7: 6 to 4; every random machine's minimized version passes the equivalence check |
| 3 | encodings | totals from 6 to 17 literals (see the key); the straightforward assignment S0 = 00, ..., S3 = 11 needs 16 |
| 4 | upsets | binary detection is low and depends on how many codes are unused (see the key for 12 states); one-hot detects every single flip |
| Verilog | testbench | `TEST PASSED`, with detection counts for Mealy and Moore that differ by at most 1 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-08.a | encodings of the 110 detector | 24 | — |
| Lab 08-08.b | fewest total literals | 6 | — |
| Lab 08-08.c | most total literals | 17 | — |
| Lab 08-08.d | encodings achieving the fewest | 4 | — |
| Lab 08-08.e | detectable single flips, 12 states with codes 0 to 11 | 16.7 | % |
| Lab 08-08.f | traffic-light cycle in the testbench | 16 | tick |
| Lab 08-08.g | Moore lag behind Mealy | 1 | cycle |

**Reading the key.** The four best encodings share a structure. One bit gives the two states entered on input 1 ("seen 1" and "seen 11") the same value, so that bit simply records the last input (its next-state function is $x$ or $\overline{x}$, one literal). The other bit separates {S0, S1} from {S2, S3}, with {S0, S1} coded as 1. Encoding B of Problem 08-08.5 has the same structure with the second bit inverted and needs 7 literals instead of 6. With 12 states in 4 bits, the illegal codes 1100 to 1111 each have two legal neighbors (for 1100: 0100 and 1000), so 8 of the $12 \times 4 = 48$ possible single flips are detectable, 16.7%. The scaled traffic light lasts $5 + 2 + 1 + 5 + 2 + 1 = 16$ ticks.

## Discussion questions

1. Why does the testbench check the Moore output against the *previous* cycle's Mealy output, and why must it take that value before the clock edge rather than after?
2. In Part 2, about 40% of random 6-state machines could be reduced, and 12 of 300 collapsed to a single state. What makes two states of a random machine equivalent, and when does a whole machine collapse?
3. What do Icarus and Verilator report when the defaults are removed from `det101_mealy`, and what does synthesis build?
4. In `traffic`, an illegal state shows red in both directions until the next tick. Why is that a sensible failure mode, and what would make recovery faster?
5. The traffic controller's state register and timer are both registers. Which one would a synthesis tool recognize as an FSM, using the Yosys rules of §9?

<details><summary>Answers to the discussion questions</summary>

1. The Moore output in cycle $t + 1$ equals the Mealy output in cycle $t$ (chapter §3.2). The testbench reads the Mealy output in the middle of cycle $t$, after the input has settled, and stores it; after the clock edge the Mealy machine is already in its next state and its output describes cycle $t + 1$, so reading it then would compare the wrong cycles.
2. Two states are equivalent when no input sequence separates them by the outputs: they must have the same output, and so must all the states they can lead to, step for step. In a random table this typically happens to a group of states with equal outputs that lead only into each other. A machine collapses to one state exactly when all its states have the same output; with random outputs that has probability $2/2^6 = 1/32$ for 6 states, so about 9 of 300 are expected. Machines written by people are reducible for a different reason: states written separately for clarity that behave identically.
3. Without the defaults, `next` is not assigned when the state is 11, so the combinational block must remember its old value, the latch trap of 08-05. Verilator (5.020, `-Wall`) stops with a `CASEINCOMPLETE` warning, "Case values incompletely covered (example pattern 0x3)". Icarus compiles without complaint and simulates `next` holding its last value, so the forced illegal state moves to whatever state `next` last held (S1 in this testbench, not S0): the recovery check fails and the testbench prints `TEST FAILED`. A synthesis tool would build a latch, or, since code 11 is unreachable from reset, treat it as a don't care; either way the recovery is no longer guaranteed.
4. Red in both directions is the safe state for an intersection: nobody is told to go. Recovery waits for the next tick because the state register only updates on ticks; checking `legal` on every clock edge instead (outside the `if (tick)`) would recover within one clock cycle.
5. The state register: its next value comes from a multiplexer tree over constants (the phase sequence), and it is compared only with constants. The timer is loaded with constants but also decremented (`timer - 1`), which is arithmetic on the register, so it is a counter, not an FSM, to the tool.

</details>

## Optional hardware

An FPGA board with a push button, a clock and a few LEDs is enough to build the traffic light for real. Divide the board clock down to a 1 Hz tick with a counter (Example 08-08.6 used a 32.768 kHz crystal and 15 stages), and feed the push button through a two-flip-flop synchronizer and the debouncer of Problem 08-08.12 before using it as a "pedestrian request" input. Without the debouncer, one press often registers several times, which is easy to see by counting presses on the LEDs.
