# Lab 19-13 · Testbenches, Coverage, BDDs and Model Checking

Chapter: [19-13 · Verification: Simulation, UVM, Formal and Emulation](../../chapters/19-13-verification-methods.md)

## Objective

- Run a constrained-random, self-checking Verilog testbench with functional coverage, and watch it catch a deliberately unfair arbiter.
- Measure coverage closure against the coupon-collector predictions, including a rare bin.
- Build ROBDDs, see variable order change their size, and find a bug in an adder with a miter.
- Prove and refute invariants of small state machines by reachability, bounded model checking and k-induction.

## Background

The chapter's §3.2–3.4 cover testbenches, coverage and assertions, §3.6 equivalence checking and BDDs, and §3.7 model checking.

Files:

- `rr_arbiter.v`: a four-way round-robin arbiter; the parameter `FIXED_PRIORITY = 1` turns it into a fixed-priority arbiter.
- `rr_arbiter_tb.v`: drives the round-robin arbiter and a fixed-priority copy with the same LFSR-generated requests (each held until granted), checks every cycle that grants are one-hot or zero, go only to requesters and never leave a pending request idle, measures each requester's wait in grants to others, and counts 9 coverage bins. It prints TEST PASSED when the round-robin arbiter passes every check with full coverage and the fixed-priority copy breaks the fairness bound. Run with `iverilog -g2012 -o sim rr_arbiter_tb.v rr_arbiter.v && vvp sim` (or `python tools/run_hdl.py` from the repository root).
- `verif.py`: `expected_to_cover` ($nH_n$), `expected_to_cover_exact` (inclusion–exclusion), `simulate_cover`; a `BDD` class (unique table, `apply`, `size`, `satisfy_one`), `ripple_adder`, `lookahead_adder` (with an optional injected bug), `equivalent` (miter); `reachable`, `check_invariant`, `bmc`, `k_inductive`; and example machines `fifo_counter`, `step_by_two`, `bcd_counter`, `mutex`, plus `arbiter_worst_wait`, an exhaustive search over every request pattern.
- `19-13-verification-lab.ipynb`: the procedure below.

## Procedure

1. **A testbench in Verilog.** Predict the worst wait (in grants to others) the testbench will see for the round-robin arbiter, and whether the fixed-priority copy will break the bound of 3. Run it and read the coverage report. Then confirm the worst case exhaustively with `arbiter_worst_wait` for 2 to 5 requesters (Part 1).
2. **Coverage closure.** Predict the mean number of random samples to fill 16 equal bins, and 8 bins with one bin of probability 0.01. Simulate 2000 closures of each and compare with the formulas (Part 2).
3. **BDDs and variable order.** Predict the ROBDD sizes of $\sum x_iy_i$ and of the equality comparator $a = b$ for $n = 3$ to 8 under the interleaved and separated orders, then build them. Build the BDDs of an 8-bit ripple adder and look at the size of each output bit (Part 3).
4. **Equivalence checking.** Compare a ripple adder with a lookahead adder, then inject the bug of Example 19-13.3 and check the counterexample with integer arithmetic (Part 4).
5. **Model checking.** For the FIFO counter, predict the reachable states and the BMC depth that exposes the overflow bug; for the add-by-two counter, predict the smallest $k$ that proves $x \ne 7$; for the two-process protocol, predict whether mutual exclusion holds and how fast the buggy version fails (Part 5).

## Expected results

- Part 1: the testbench reports 0 errors, 0 fairness violations, a worst wait of 3 grants and all 9 coverage bins hit, with grants spread almost evenly over the four requesters; the fixed-priority copy breaks the fairness bound on many cycles, and the testbench prints TEST PASSED. The exhaustive search gives a worst wait of $N - 1$ for $N$ = 2 to 5, and reaches its cap (unbounded starvation) for fixed priority.
- Part 2: the formulas give 54.09 samples for 16 bins and 101.9 for the rare-bin case (Example 19-13.1); 2000 simulated closures land within a few percent of both.
- Part 3: $\sum x_iy_i$ gives $2n$ against $2^{n+1} - 2$ nodes; the comparator gives $3n$ against $3 \cdot 2^n - 3$ (24 against 765 at $n = 8$). Sum bit $i$ of the adder has $3i + 3$ nodes, 24 for bit 7.
- Part 4: the correct adders are equivalent (the miter is the constant 0); the buggy one fails on $A = 7$, $B = 1$, where it outputs 0 instead of 8.
- Part 5: the FIFO counter reaches 5 of 8 states and the invariant holds; the buggy version reaches all 8, and BMC finds the overflow at depth 5. $x \ne 7$ fails 1-, 2- and 3-induction and is 4-inductive. Mutual exclusion holds in all 16 reachable states of 18; the buggy protocol fails after 2 steps.

## Discussion

1. The testbench's fairness check counts grants to others, not cycles. Why does that make the check independent of how long each requester holds its request?
2. Why did 2000 random cycles hit every coverage bin here, and what change to the stimulus would make the "all four requesting" bin rare?
3. Why does interleaving the operand bits keep adder BDDs small?
4. BMC with depth 4 reports no violation for the buggy FIFO counter. What may you conclude, and what may you not?

**Answers.**

1. A requester's wait depends on what the arbiter does while it waits. Counting grants to others measures exactly the arbiter's decisions; the number of cycles would also depend on whether other requesters happened to be requesting, which is the stimulus, not the design.
2. Each idle requester raises a request with probability 1/2 per cycle and keeps it until served, so requests pile up and all-four-requesting is the most common case. If requests were rare (say probability 1/16 per cycle and dropped after one cycle), all four would request together with probability $(1/16)^4 = 1.53 \times 10^{-5}$ per cycle, and that bin would need a directed test.
3. Each output bit depends on the inputs through the carry chain, and a BDD read in bit order needs to remember only the carry, one bit of state, so each level holds a constant number of nodes. With all $a$ bits first, the diagram must remember the whole of $A$ before it sees $B$.
4. That no input sequence of 4 or fewer cycles from reset violates the invariant. It does not show that the invariant holds: the first violation needs 5 cycles. A bounded result is a proof only if the bound reaches the diameter or an induction step completes it.

## Optional extensions

- Write the arbiter's four properties as SVA and check them with an open-source formal tool such as SymbiYosys (`bmc` and `prove` modes); note that full SVA support may need a commercial front end.
- Add a weighted round-robin mode to `rr_arbiter.v` and change the fairness bound in the testbench accordingly.

## Optional hardware

Load the arbiter onto any FPGA board with switches for the requests and LEDs for the grants; holding several switches on shows the grant rotating, and the fixed-priority build shows requester 0 starving the others.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-13.a | worst wait, round-robin, 4 requesters | 3 | grants |
| Lab 19-13.b | coverage bins hit | 9 | — |
| Lab 19-13.c | comparator nodes, separated order, n = 8 | 765 | — |
| Lab 19-13.d | comparator nodes, interleaved order, n = 8 | 24 | — |
| Lab 19-13.e | BDD nodes of sum bit 7, 8-bit adder | 24 | — |
| Lab 19-13.f | smallest k proving x ≠ 7 | 4 | — |
| Lab 19-13.g | reachable states of the protocol | 16 | — |
| Lab 19-13.h | probability all four rare requests coincide | 1.53e-5 | — |
| Lab 19-13.i | expected samples, 16 equal bins | 54.09 | — |
| Lab 19-13.j | expected samples with the rare bin | 101.9 | — |
