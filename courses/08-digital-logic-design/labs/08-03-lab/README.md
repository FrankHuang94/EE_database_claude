# Lab 08-03 · Logic Minimization

**Chapter:** [08-03](../../chapters/08-03-logic-minimization.md) · **Notebook:** [08-03-logic-minimization.ipynb](08-03-logic-minimization.ipynb) · **Time:** about 2 hours

## Objective

1. Draw Karnaugh maps automatically and read groups from them.
2. Implement the Quine–McCluskey method and Petrick's method, and check them against brute force.
3. See how fast exact minimization slows down as the number of inputs grows.
4. Measure, over every three-variable function with don't cares, how much the don't cares save.
5. Confirm in Verilog that minimized circuits agree with the specification on legal inputs, and see what they do on the don't-care inputs.

## Background

Chapter sections 3.1 to 3.7 and Examples 08-03.1 to 08-03.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)). The Verilog uses only `assign` statements with `&`, `|` and `~`, as in Lab 08-02.

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-03-logic-minimization.ipynb](08-03-logic-minimization.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [bcd_ge5.v](bcd_ge5.v) | Example 08-03.4 three ways: canonical SOP, minimal SOP without don't cares, minimal SOP with them | `bcd_ge5_tb.v` |
| [bcd_ge5_top.v](bcd_ge5_top.v) | A top level instantiating all three, for lint tools | Lint only |
| [bcd_ge5_tb.v](bcd_ge5_tb.v) | Self-checking testbench: all three equal "code ≥ 5" on codes 0 to 9; their outputs on codes 10 to 15 are printed and counted | Prints `TEST PASSED` |

Run the testbench from the repository root:

```bash
python tools/run_hdl.py
```

## Procedure

1. **Maps (Part 1).** *Predict first:* on a four-variable map, which cell is adjacent to $m_0$ through the top–bottom wrap, and which through the left–right wrap? The notebook draws the maps of the chapter's examples with their minterm numbers.
2. **Quine–McCluskey (Part 2).** Run the tabulation on Example 08-03.6 and compare every intermediate list with the chapter's steps. Then run Petrick's method on the cyclic function of Problem 08-03.13.
3. **Brute force and timing (Part 3).** *Predict first:* if exact minimization of a random 4-input function takes a fraction of a millisecond, how many times longer does a random 6-input function take? Then time the notebook's implementation.
4. **Don't cares (Part 4, the chapter's guided exercise).** Every three-variable function in which each row is 1, 0 or don't care: $3^8$ = 6561 of them. *Predict first:* by what percentage do the don't cares cut the average minimal literal count, compared with treating them as 0s?
5. **Verilog.** Run the testbench and read the printed outputs on codes 10 to 15. Then add a fourth module with the segment-*a* logic of Problem 08-03.7, $A + C + BD + \overline{B}\,\overline{D}$, and predict its outputs on codes 10 to 15 before simulating.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | wrap-around neighbors of $m_0$ | $m_8$ (top–bottom) and $m_2$ (left–right) |
| 2 | Example 08-03.6 | 6 primes, 1 essential ($BD$), a unique minimum with 8 literals |
| 3 | timing | several times longer per added input (machine-dependent); the number of prime implicants roughly doubles per input, and the candidate covers grow faster still |
| 4 | don't-care payoff | see the key: about a 41% cut |
| Verilog | testbench | `TEST PASSED`; the don't-care version outputs 1 on every illegal code, the other two output 0 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-03.a | three-variable functions with don't cares | 6561 | — |
| Lab 08-03.b | mean minimal literals, don't cares as 0 | 4.360 | — |
| Lab 08-03.c | mean minimal literals, don't cares used | 2.555 | — |
| Lab 08-03.d | reduction from using the don't cares | 41.4 | % |
| Lab 08-03.e | illegal codes giving 1, canonical SOP | 0 | — |
| Lab 08-03.f | illegal codes giving 1, minimized without don't cares | 0 | — |
| Lab 08-03.g | illegal codes giving 1, minimized with don't cares | 6 | — |

**Reading the key.** In Part 4 each row is a don't care with probability 1/3, so a typical function has two or three free cells out of eight. Each free cell next to a group can double that group's size and delete a literal, and a function whose 1s and don't cares fill a whole half of the map collapses to a single literal. Hence the large average saving. The cost is the last three lines of the key: the circuit built from don't cares has definite, unrequested outputs on the "impossible" codes.

## Discussion questions

1. Why does the Quine–McCluskey method compare only terms whose numbers of 1s differ by exactly one?
2. In Part 3, what grows faster with the number of inputs: the number of prime implicants or the number of candidate covers? Why does that matter for tool design?
3. The don't-care implementation of Example 08-03.4 outputs 1 on all six illegal codes. Construct a scenario in a real product where that would be a bug, and say how a specification would prevent it.
4. Why might a synthesis tool *not* use a don't care even when it would save area?
5. The testbench checks the three implementations only on codes 0 to 9. What would a formal equivalence checker report if asked to compare `bcd_ge5_canon` with `bcd_ge5_dc` on all 16 codes, and how do engineers tell the checker about don't cares?

<details><summary>Answers to the discussion questions</summary>

1. Two terms can merge only if they differ in exactly one bit, which changes the count of 1s by exactly one. Pairs from groups two or more apart differ in at least two bits and can be skipped without testing.
2. Candidate covers grow much faster: they are subsets of the primes, so their number is exponential in the number of primes, which is itself exponential in the number of inputs in the worst case. Tools therefore spend their effort on the covering step, with pruning and heuristics such as Espresso's expand–irredundant–reduce loop.
3. Suppose the digit comes from a sensor interface that can glitch to 1111 at power-up, and the output enables a motor when the reading is 5 or more: the don't-care design would start the motor on a power-up glitch. A specification that defines the response to illegal codes ("codes 10 to 15: output 0 and raise an error flag") makes the behavior deliberate; the extra logic is small.
4. Because a don't care might really be reachable (through a corner case in another block, a reset sequence or a later change), because safety rules require defined behavior, or because a different choice is better for timing or testability. Tools also only know the don't cares they are told about; unreachable states that are not declared are not exploited.
5. It would report the two as different, with a counterexample such as code 10 (outputs 0 and 1). Engineers either restrict the comparison to the legal input space with constraints (assumptions) or declare the don't-care conditions to the tool, so that only differences on care inputs count as mismatches.

</details>

## Optional hardware

Build `bcd_ge5_dc` and `bcd_ge5_nodc` on a breadboard from a 74HC08 (quad AND2), a 74HC32 (quad OR2) and a 74HC04 (hex inverter), with four DIP switches for the code and two LEDs for the outputs. Step through all 16 switch settings and record where the LEDs disagree: exactly the six illegal codes. A 74HC4511 BCD-to-seven-segment decoder chip shows how one commercial part handles illegal codes (its datasheet describes the display for inputs 10 to 15).
