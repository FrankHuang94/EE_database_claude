# Problems 19-13 · Verification: Simulation, UVM, Formal and Emulation

Chapter: [19-13](../chapters/19-13-verification-methods.md) · Worked solutions: [19-13 solutions](../solutions/19-13-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Coverage bins are hit independently by each sample unless stated. ROBDD node counts exclude the two terminals. A path of length $k$ has $k$ transitions. Problems marked *(lab)* can be checked with `labs/19-13-lab/verif.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-13.1 [A]

**Verification, validation or test?** (a) Classify each activity: (i) a logic equivalence check of the RTL against the synthesized netlist; (ii) booting an operating system on first silicon in the lab; (iii) running scan patterns on every die at wafer sort; (iv) a nightly constrained-random regression on the RTL; (v) confirming with a customer that the specified latency meets their application; (vi) a functional test of packaged parts after burn-in. (b) Map each part of the lab's arbiter testbench (the LFSR that decides when requests rise, the code that holds each request until it is granted, the four per-cycle checks, the coverage counters) to the UVM component that plays the same role.

### Problem 19-13.2 [A] *(lab)*

**Coupon collecting.** (a) How many uniformly random samples are expected to fill a 32-bin coverpoint? (b) A cross of 16 request patterns with 4 arbiter-pointer values has 64 bins; assuming all 64 combinations equally likely and independent from sample to sample, how many samples are expected to fill it? (c) How many of the 64 bins are expected to be still empty after 64 samples?

### Problem 19-13.3 [A]

**Confidence of closure.** An 8-bin coverpoint has equally likely bins. (a) What is the probability that 30 samples fill every bin? (b) What is the smallest number of samples that fills every bin with at least 99 % probability?

### Problem 19-13.4 [B] *(lab)*

**Unequal bins.** A coverpoint has four bins hit with probabilities 0.5, 0.3, 0.15 and 0.05 per sample. (a) Derive the expected number of samples to fill all four from the inclusion–exclusion formula, and compare it with $1/p_{\min}$. (b) If the constraints are re-weighted so that all four bins are equally likely, what is the expected number?

### Problem 19-13.5 [B] *(lab)*

**Arbiter fairness.** (a) What is the worst number of grants to others that a pending requester sees in a 6-requester round-robin arbiter? (b) An 8-requester round-robin bus arbiter re-arbitrates only between bursts, and every burst holds the bus for 16 cycles. Counting from the first arbitration a requester loses, how many cycles can pass before its own burst starts? (c) A fixed-priority arbiter (requester 0 always wins) replaces the round-robin one. From cycle 1 on, requesters 0 and 1 both request on every cycle. On which cycle does `req[1] |-> ##[0:3] gnt[1]` first fail? (d) Which of the assertions `a_onehot`, `a_subset` and `a_busy` of the chapter does the fixed-priority arbiter pass, and what does that say about writing specifications as assertions?

### Problem 19-13.6 [A]

**Reading an assertion.** The property `req |-> ##[1:2] ack` is checked on cycles 1 to 10. `req` is high only on cycles 2 and 6, and `ack` only on cycles 4 and 9. (a) Does the attempt that starts on cycle 2 pass? (b) On which cycle does the attempt that starts on cycle 6 fail? (c) How many failures would `req |=> ##[1:2] ack` report on the same trace? (d) How many of the ten cycles give vacuous passes of the original property?

### Problem 19-13.7 [A] *(lab)*

**BDDs by hand.** (a) Draw the ROBDD of the 3-input majority function $ab + ac + bc$ with order $a, b, c$, and count its nodes. (b) Show that the parity function $x_1 \oplus \cdots \oplus x_n$ has $2n - 1$ nodes in any order, and give the count for $n = 5$.

### Problem 19-13.8 [B] *(lab)*

**An equality comparator.** $E = \prod_{i=1}^{n} \overline{a_i \oplus b_i}$ tests whether two $n$-bit words are equal. (a) Show that the interleaved order $a_1, b_1, \ldots, a_n, b_n$ gives $3n$ nodes. (b) Show that the order $a_1, \ldots, a_n, b_1, \ldots, b_n$ gives $3 \cdot 2^n - 3$ nodes. (c) Evaluate both for $n = 4$ and $n = 16$.

### Problem 19-13.9 [B]

**Random simulation against a rare bug.** In an $n$-bit carry-lookahead adder, a bug drops the $g_0$ term from the carry into bit $k$, so it shows only when $a_0 = b_0 = 1$ and bits 1 to $k-1$ all propagate. (a) Show that a uniformly random input pair exposes it with probability $2^{-(k+1)}$. (b) For $k = 15$, how many random vectors give 99 % confidence of catching it, and how long does that take at an assumed $10^6$ vectors per second? (c) For $k = 63$ in a 64-bit adder, how many vectors are needed, and how many years at the same rate?

### Problem 19-13.10 [B] *(lab)*

**Mutual exclusion.** Two processes share a resource. Each is idle (I), requesting (R) or in its critical section (C), and a bit `turn` (0 or 1) breaks ties. All moves happen together on each clock: an idle process may stay idle or request; a requesting process enters C if the other is not in C and, when the other is also requesting, only if `turn` names it; otherwise it keeps requesting; a process in C may stay or leave, and leaving sets `turn` to the other process. Both start idle with `turn` = 0. (a) How many states does the model have? (b) How many are reachable? (c) Does mutual exclusion (never both in C) hold? (d) A buggy version lets a requester enter whenever the other is not in C, ignoring the other's request. Find the shortest counterexample and its length.

### Problem 19-13.11 [C] *(lab)*

**Induction on a BCD counter.** A 4-bit counter counts 0, 1, …, 9 and then returns to 0 (from 9 it goes to 0; from any other value $x$ it goes to $x + 1$ modulo 16). (a) How many of the 16 states are reachable? (b) Show that $P: x \ne 12$ is not 1-inductive and give the counterexample to induction. (c) Find the smallest $k$ for which $P$ is $k$-inductive, with a justification. (d) Give a lemma that makes the proof 1-inductive.

### Problem 19-13.12 [B]

**Planning hardware-assisted runs.** A software team needs 200 tests, each of $5 \times 10^8$ cycles. Assume an emulator at 1 MHz, an FPGA prototype at 25 MHz and RTL simulation at 100 cycles per second (illustrative speeds; vendors do not publish comparable figures). (a) How long does one test take on the emulator, and how long does the whole suite take run one at a time? (b) The same suite split evenly across 4 emulator partitions? (c) The whole suite run one at a time on the prototype, in minutes? (d) One test in RTL simulation, in days? (e) Give two reasons a team still runs some of these tests on the emulator rather than the prototype.

### Problem 19-13.13 [B]

**Writing the checks for a FIFO.** An 8-entry synchronous FIFO has inputs `push` and `pop`, an occupancy counter `count` (0 to 8) and flags `full` and `empty`. A push when full and a pop when empty are ignored; a simultaneous push and pop when neither is blocked leaves `count` unchanged; data must come out in the order it went in. (a) Write four rows of a verification plan: feature, how it is checked, and how its exercise is measured. (b) Write SVA assertions that `count` never exceeds 8, that `empty` and `full` match `count`, and that a push alone on a full FIFO leaves it full; and write an assumption that restricts a formal tool to consumers that never pop an empty FIFO. What does that assumption stop the proof from checking? (c) Write a covergroup with a coverpoint on the level (empty, partly full, full), a coverpoint on the four `{push, pop}` combinations, and their cross. How many cross bins are there, and how many can be hit when the assumption of (b) holds? (d) Which of these checks would you prove formally, and which would you leave to simulation with a scoreboard, and why?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Verification, validation, test and the plan | 1, 13 |
| 2. Testbench structure and UVM | 1, 13 |
| 3. Coverage closure and rare bins | 2, 3, 4 |
| 4. Assertions and arbiter fairness | 5, 6, 13 |
| 5. BDDs, variable order and equivalence | 7, 8, 9 |
| 6. Reachability, BMC, k-induction and platforms | 10, 11, 12 |
