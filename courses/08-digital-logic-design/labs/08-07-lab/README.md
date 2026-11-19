# Lab 08-07 · Counters, Shift Registers and LFSRs

**Chapter:** [08-07](../../chapters/08-07-registers-counters-shift-registers.md) · **Notebook:** [08-07-counters-lfsrs.ipynb](08-07-counters-lfsrs.ipynb) · **Time:** about 2.5 hours

## Objective

1. Compare the switching activity of binary, Gray, ring and Johnson counters.
2. Find which two-tap LFSRs reach maximal length by stepping them, and confirm the answer with an independent algebraic test.
3. Measure the balance, runs and autocorrelation of PRBS7 and PRBS15.
4. Count the transient states of a ripple counter.
5. Build a universal shift register, a BCD counter, a Johnson counter and two PRBS generators in Verilog, and check them with a self-checking testbench.

## Background

Chapter sections 3.2 to 3.7 and Examples 08-07.1 to 08-07.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-07-counters-lfsrs.ipynb](08-07-counters-lfsrs.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [counters.v](counters.v) | Universal shift register `usr4`, decade counter `bcd_counter`, `johnson` counter and a parameterized Fibonacci LFSR `prbs` | `counters_tb.v` |
| [counters_top.v](counters_top.v) | A top level for lint tools | Lint only |
| [counters_tb.v](counters_tb.v) | Replays Example 08-07.1, checks the BCD sequence, terminal count and enable, the Johnson sequence, and the period and balance of PRBS7 and PRBS15 | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_notebooks.py 08-07
```

```bash
python tools/run_hdl.py
```

## Procedure

1. **Switching activity (Part 1).** *Predict first:* how many bits toggle per step in each 4-bit counter? The notebook generates each counter's sequence from its next-state rule and counts the bits that differ between consecutive states, including the wrap from the last state to the first.
2. **Maximal taps (Part 2, the chapter's guided exercise).** *Predict first:* what fraction of the 25 two-tap polynomials of degree 4 to 8 give maximal length? The notebook steps every LFSR through all its nonzero states, then checks each verdict with a primitivity test done in polynomial arithmetic over GF(2). It also checks a four-tap polynomial for $n = 8$.
3. **m-sequence statistics (Part 3).** *Predict first:* the number of 1s, the number of runs and the autocorrelation of PRBS7. Then plot the bits and the autocorrelation.
4. **Ripple transients (Part 4).** *Predict first:* how many wrong values a 4-bit ripple counter shows in one 16-count cycle with 2 ns per stage. The notebook simulates each stage's toggle as an event.
5. **Verilog.** Run `counters_tb.v`. It prints the PRBS periods and counts of 1s it measures; compare them with Part 3. Then change the PRBS7 instance in the testbench to taps (7, 5) and predict what it will report before running it.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | toggles per step | binary 1.875, Gray 1, ring 2, Johnson 1 (see the key) |
| 2 | maximal two-tap polynomials | 10 of 25, in mirror pairs ($k$ and $n - k$); none for $n = 8$, where a four-tap polynomial is needed |
| 3 | PRBS7 | 64 ones and 63 zeros, 64 runs (32 of length 1), autocorrelation $-1/127$ at every nonzero shift |
| 4 | ripple counter | 14 transient states per cycle; the worst settling time, 8 ns, on the counts from 7 to 8 and from 15 to 0 |
| Verilog | testbench | `TEST PASSED`, with `PRBS7: period 127, ones 64` and `PRBS15: period 32767, ones 16384` printed |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-07.a | binary counter, toggles per step | 1.875 | — |
| Lab 08-07.b | Gray counter, toggles per step | 1 | — |
| Lab 08-07.c | ring counter, toggles per step | 2 | — |
| Lab 08-07.d | Johnson counter, toggles per step | 1 | — |
| Lab 08-07.e | two-tap polynomials tested, $n$ = 4 to 8 | 25 | — |
| Lab 08-07.f | maximal-length among them | 10 | — |
| Lab 08-07.g | irreducible trinomials of degree 8 | 0 | — |
| Lab 08-07.h | period of $x^8 + x^6 + x^5 + x^4 + 1$ | 255 | — |
| Lab 08-07.i | PRBS7 period | 127 | — |
| Lab 08-07.j | PRBS7 ones per period | 64 | — |
| Lab 08-07.k | PRBS7 runs per period | 64 | — |
| Lab 08-07.l | PRBS7 autocorrelation at a nonzero shift | -0.00787 | — |
| Lab 08-07.m | PRBS15 period | 32767 | — |
| Lab 08-07.n | PRBS15 ones per period | 16384 | — |
| Lab 08-07.o | ripple counter transient states per cycle | 14 | — |
| Lab 08-07.p | ripple counter worst settling time | 8 | ns |

**Reading the key.** A count from $c$ to $c + 1$ flips $m$ bits, where $m - 1$ is the number of trailing 1s of $c$. Over a full cycle of a 4-bit counter, bit $i$ flips $2^{4-i}$ times, so the flips total $16 + 8 + 4 + 2 = 30$: that gives Lab 08-07.a, $30/16$. In a ripple counter each of those flips happens at a different time, so a count that flips $m$ bits shows $m - 1$ wrong values on the way, and the total is $30 - 16 = 14$ (Lab 08-07.o). The PRBS7 numbers are the m-sequence properties of chapter §3.6 with $n = 7$: $2^6 = 64$ ones, $2^6 = 64$ runs, and correlation $-1/N = -1/127$.

## Discussion questions

1. Why does the testbench measure each PRBS period by waiting for the state to return to its seed, rather than waiting for the output bit pattern to repeat?
2. Why does the ring counter toggle two bits per step, and why might a designer accept that?
3. With taps (7, 5) instead of (7, 6), what does `counters_tb.v` report for PRBS7, and why?
4. Every degree-8 trinomial is reducible. Why does that not make 8-bit maximal LFSRs impossible?
5. The ripple counter's worst settling time is 8 ns, but its first stage toggles only 2 ns after the clock. Which of the two limits a clock divider built from it, and which limits a counter whose value is read?

<details><summary>Answers to the discussion questions</summary>

1. The state determines everything that follows, so the first return of the state to its seed marks the period exactly. A short stretch of output bits can repeat by coincidence long before the period ends (any 3-bit pattern recurs many times in 127 bits), so pattern matching on the output needs a window at least $n$ bits long to be unambiguous, and comparing the state is that window.
2. In a one-hot ring, every step moves the single 1 to the next flip-flop: one flip-flop falls and one rises. A designer accepts it because the outputs need no decoding (each state is one flip-flop), they cannot glitch, and the next-state logic is just wires: for a few states, as in a state machine's one-hot encoding ([08-08](../../chapters/08-08-finite-state-machines.md)), that saves more than it costs.
3. $x^7 + x^5 + 1$ is not primitive: its nonzero states fall into cycles of 3, 31 and 93 (the same as its mirror image $x^7 + x^2 + 1$ in Part 2). From the seed $Q_1 = 1$, the testbench measures whichever cycle contains that state, so the PRBS7 period and count of 1s no longer match 127 and 64, and the testbench reports the failures and `TEST FAILED`. Running it shows which of the three cycles the seed lies on.
4. Maximal length needs a primitive polynomial, not a trinomial. With four taps (a pentanomial such as $x^8 + x^6 + x^5 + x^4 + 1$, period 255) the feedback costs three XOR gates instead of one. The reason no trinomial of degree 8 works is a theorem of R. G. Swan (1962, [R-155](../../../../reference/research-log.md#r-155--prbs-and-lfsr-references)): a trinomial whose degree is a multiple of 8 always has an even number of irreducible factors, so it is never irreducible. Part 2 checks the $n = 8$ case directly.
5. A clock divider only uses the last stage as a slower clock, so only how fast each stage can toggle matters: the first stage must keep up with the input clock. The 8 ns ripple delay just shifts the divided clock's edges by a fixed amount. A counter whose value is read needs all four bits settled before the reading logic samples them, so its period must exceed the full 8 ns plus the reading logic's delay (Example 08-07.4).

</details>

## Optional hardware

A 74HC393 (dual 4-bit ripple counter) driven from a function generator, with a two-channel oscilloscope on $Q_0$ and $Q_3$, shows the ripple delay directly: trigger on the falling edge of $Q_0$ at the count from 7 to 8 and measure how much later $Q_3$ rises. A 74HC164 (8-bit serial-in, parallel-out shift register) with one XOR gate from a 74HC86 makes a working LFSR whose period can be counted on LEDs at a slow clock.
