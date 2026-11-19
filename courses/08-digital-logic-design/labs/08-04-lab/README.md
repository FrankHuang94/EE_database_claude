# Lab 08-04 · Combinational Building Blocks

**Chapter:** [08-04](../../chapters/08-04-combinational-building-blocks.md) · **Notebook:** [08-04-building-blocks.ipynb](08-04-building-blocks.ipynb) · **Time:** about 2.5 hours

## Objective

1. Check multiplexers, decoders and priority encoders against their specifications on every input.
2. Measure the settling time of a ripple-carry adder over every possible input change, and count its glitches.
3. Build a structural 4-bit ALU in Verilog and verify it, flags included, against a reference model on every input.
4. Watch a static hazard happen in a gate-delay simulation, and remove it.

## Background

Chapter sections 3.1 to 3.9 and Examples 08-04.1 to 08-04.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)). New Verilog here: `always @(*)` with a `case` statement (a combinational block whose outputs are recomputed whenever an input changes), `genvar`/`generate` loops that instantiate four full adders, and gate primitives with delays such as `and #1` (simulation only). [08-05](../../chapters/08-05-verilog-and-testbenches.md) explains all of these.

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-04-building-blocks.ipynb](08-04-building-blocks.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [alu4.v](alu4.v) | Full adder, 4-bit add/subtract unit and a 4-bit ALU (ADD, SUB, AND, OR, XOR, SLT) with Z, N, C, V flags | `alu4_tb.v` |
| [alu4_tb.v](alu4_tb.v) | Checks the ALU against a behavioral reference on all 1536 operand and operation combinations | Prints `TEST PASSED` |
| [hazard_tb.v](hazard_tb.v) | The multiplexer of Example 08-04.7 with 1 ns gate delays, minimal and with the consensus term; counts glitches | Prints `TEST PASSED` |

Run both testbenches from the repository root:

```bash
python tools/run_hdl.py
```

## Procedure

1. **Blocks (Part 1).** *Predict first:* how many of the 256 inputs of an 8:3 priority encoder produce each output code? The notebook checks the encoder equations of Problem 08-04.5 and counts.
2. **Settling time (Part 2, the chapter's guided exercise).** *Predict first:* the longest settling time of any output of a 4-bit ripple adder over every input change, and the share of output transitions that are glitches. The notebook simulates all $2^{18}$ = 262 144 transitions at once.
3. **Width (Part 3).** *Predict first:* do glitches per addition grow or shrink, relative to the needed transitions, as the adder gets wider? The notebook samples random transitions for 4, 8 and 16 bits.
4. **Hazards (Part 4).** Trace Example 08-04.7 in the notebook's unit-delay simulator, then run `hazard_tb.v` and compare the reported glitch time with your trace.
5. **ALU.** Run `alu4_tb.v`. Then introduce a bug, for example compute $V$ as `c[4]` instead of `c[4] ^ c[3]`, and see which operations and operand pairs the testbench reports.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | priority-encoder counts | 128, 64, 32, 16, 8, 4, 2, 1 for outputs 7 down to 0, plus 1 all-zero input |
| 2 | settling and glitches | see the key: sum bits settle within 8 units and the carry out within 9; more than half of all output transitions are glitches |
| 3 | width | the glitch count grows faster than the number of needed transitions as the carry chain lengthens |
| 4 | hazard | the minimal multiplexer drops to 0 from 2 to 3 units after the select falls; the consensus version never does |
| ALU | testbench | `TEST PASSED` on 1536 vectors |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-04.a | input transitions simulated | 262144 | — |
| Lab 08-04.b | longest settling time, sum bits | 8 | units |
| Lab 08-04.c | longest settling time, carry out | 9 | units |
| Lab 08-04.d | input changes after which some output glitches | 74.1 | % |
| Lab 08-04.e | mean output transitions per input change | 5.914 | — |
| Lab 08-04.f | mean glitch transitions per input change | 3.414 | — |
| Lab 08-04.g | share of output transitions that are glitches | 57.7 | % |
| Lab 08-04.h | ALU test vectors | 1536 | — |

**Reading the key.** The settling times match the static timing analysis of §3.5 exactly ($2n$ and $2n + 1$ for $n = 4$): the worst case is a carry that starts in column 0 and ripples to the top. Glitches dominate the switching because each carry that ripples through a column can flip that column's sum bit once on the way, even if it ends where it started. The unit-delay model, in which every gate passes even the shortest pulse, overstates the glitch count; real gates filter pulses shorter than their own delay.

## Discussion questions

1. Why is the settling time of a ripple-carry adder data-dependent, and why must a clocked design still allow for the worst case?
2. Writing the testbench, a first version computed the subtraction reference as `wide = a + ~b + 1;` with `a`, `b` 4 bits wide and `wide` 5 bits. It failed on every subtraction. Why? (Hint: Verilog sizes an expression from its widest operand, here the 32-bit constant `1`, before applying `~`.)
3. In `hazard_tb.v`, why do the gate delays appear only in the testbench file and not in `alu4.v`?
4. Why does the ALU compute SLT as $N \oplus V$ of a subtraction rather than by checking the sign bit alone?
5. The multiplexer glitch is only 1 ns wide. Name two places in a real system where a 1 ns glitch would cause a failure.

<details><summary>Answers to the discussion questions</summary>

1. The time depends on how far a carry has to travel: adding 0001 to 0110 settles quickly, while adding 0001 to 0111 sends a carry through every column. A clocked design samples the outputs at a fixed time after the inputs change, so that time must cover the slowest possible input change at the slowest process corner, voltage and temperature.
2. In a context with a 32-bit operand, Verilog extends `b` to 32 bits *before* inverting it, so `~b` has 28 leading 1s. The 5-bit result then receives a carry out of bit 4 that comes from those extra 1s, not from the 4-bit subtraction, and `wide[4]` is wrong. Writing `{1'b0, a} + {1'b0, ~b} + 5'd1` keeps every operand 5 bits wide. Expression widths are one of the most common sources of Verilog bugs ([08-05](../../chapters/08-05-verilog-and-testbenches.md)).
3. Synthesis ignores `#` delays: real delays come from the cells the tool chooses. Design files therefore contain only logic, and timing is studied either with explicit delay models in testbenches, as here, or with static timing analysis on the synthesized netlist.
4. With overflow, the sign bit of the difference is wrong: $-8 - 7$ gives 0001, a positive-looking result, even though $-8 < 7$. Correcting by $V$ gives the right answer in every case (Problem 08-04.11).
5. Examples: an asynchronous reset or clear input of a flip-flop or counter (it would reset the register); a clock or clock-enable path (an extra clock edge); a chip-select or write strobe going to an external memory (a spurious write); a signal sampled by another clock domain (a wrong value captured at a random moment).

</details>

## Optional hardware

A 74HC283 (4-bit adder) on a breadboard with DIP switches and LEDs lets you add and subtract by hand; add a 74HC86 (quad XOR) on the B inputs and a switch on the carry in to make the add/subtract unit of §3.6. To see a real glitch, build the multiplexer of Example 08-04.7 from a 74HC04, 74HC08 and 74HC32, drive the select with a square wave from a function generator, and look at the output with an oscilloscope; adding a long wire or extra inverters in the select path widens the glitch until it is easy to see.
