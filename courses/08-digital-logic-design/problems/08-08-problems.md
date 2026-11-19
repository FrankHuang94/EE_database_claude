# Problems 08-08 · Finite State Machines

Chapter: [08-08](../chapters/08-08-finite-state-machines.md) · Worked solutions: [08-08 solutions](../solutions/08-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** cycles are numbered from 0, starting in the reset state; the input of cycle $t$ is sampled at the clock edge that ends cycle $t$. State codes are written $q_1q_0$. A Moore output is listed for the cycle in which the machine is in the state; a Mealy output for the cycle in which the input arrives. "Literals" counts the variable appearances in a minimized sum of products.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-08.1 [A]

**Recognizing the kind of machine.** (a) An FSM's output is $z = q_1 q_0$. Is it Moore or Mealy? What if it is $z = q_1 x$? (b) A machine has 9 states. How many flip-flops and how many illegal codes does it have with binary encoding? With one-hot encoding?

### Problem 08-08.2 [A]

**How many arrows?** How many transitions must be specified for (a) a 6-state machine with 2 input bits, and (b) a 12-state machine with 4 input bits?

### Problem 08-08.3 [A]

**Tracing a detector.** The Mealy 101 detector of chapter §3.3 (overlapping) receives $x$ = 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1 in cycles 0 to 10. (a) In which cycles is its output 1? (b) How many detections does a non-overlapping Mealy detector make on the same input? (c) In which cycle does the Moore 101 detector first output 1?

### Problem 08-08.4 [B]

**A 110 detector.** Design a detector whose output is 1 when the last three inputs were 1, 1, 0 (overlapping occurrences count). (a) How many states do the Moore and Mealy versions need? Draw the Moore state diagram. (b) For the input 1, 1, 1, 0, 1, 1, 0, 0 in cycles 0 to 7, in which cycles is the Moore output 1?

### Problem 08-08.5 [B]

**Encoding matters.** Encode the Moore 110 detector of Problem 08-08.4 (states S0 "seen nothing", S1 "seen 1", S2 "seen 11", S3 "seen 110") in two ways: (A) S0 = 00, S1 = 01, S2 = 10, S3 = 11; (B) S0 = 00, S1 = 01, S2 = 11, S3 = 10. For each, derive minimized $q_1^{+}$, $q_0^{+}$ and $z$, and count the total literals.

### Problem 08-08.6 [B]

**Edge detectors.** (a) A Mealy machine outputs 1 in any cycle whose input differs from the previous cycle's input. How many states does it need, and what is its output equation? (b) How many states does the equivalent Moore machine need? (c) Repeat (a) and (b) for a rising-edge detector (output 1 when the input is 1 and was 0 in the previous cycle).

### Problem 08-08.7 [B]

**Minimizing a Mealy machine.** Minimize this machine (entries are next state / output):

| state | $x = 0$ | $x = 1$ |
|---|---|---|
| A | B / 0 | C / 0 |
| B | A / 0 | D / 1 |
| C | A / 0 | E / 1 |
| D | F / 0 | D / 1 |
| E | F / 0 | E / 1 |
| F | A / 0 | C / 0 |

(a) Give the partitions until refinement stops, with the number of blocks in each. (b) How many states does the minimal machine have, and how many flip-flops does binary encoding save?

### Problem 08-08.8 [B]

**One-hot equations.** (a) Write the one-hot next-state and output equations of the Moore 110 detector of Problem 08-08.4. (b) Written as one AND term (state AND input condition) per arrow, how many AND terms are there? (c) How many two-input OR gates combine them?

### Problem 08-08.9 [B]

**FSM timing.** An FSM's flip-flops have $t_{pcq}$ = 70 ps, $t_{ccq}$ = 40 ps, $t_{\text{setup}}$ = 50 ps and $t_{\text{hold}}$ = 30 ps. The next-state logic has a longest path of 260 ps and a shortest of 20 ps. (a) What are the minimum clock period and maximum frequency? (b) What is the hold slack? (c) If clock skew delays the capturing flip-flop's clock by 50 ps relative to the launching one, what is the hold slack?

### Problem 08-08.10 [B]

**Upsets in a 6-state machine.** A 6-state FSM uses binary codes 000 to 101. (a) How many illegal codes are there? (b) Of the single-bit flips possible from legal states, how many are there in total, and how many land on an illegal code? What fraction is that? (c) With one-hot encoding, how many illegal codes are there and what fraction of single flips are detectable?

### Problem 08-08.11 [C]

**A UART receiver as datapath and control.** A UART receiver at 115 200 baud oversamples the line 16 times per bit and receives frames of 1 start bit, 8 data bits and 1 stop bit. (a) What sample-clock frequency does it need? (b) How long is a frame? (c) The receiver confirms a start bit by sampling it again in the middle of the bit, 8 sample ticks after the falling edge. How long after the edge is that? (d) The controller is an FSM with states IDLE, START, DATA, STOP plus a sample counter (0 to 15), a bit counter (0 to 7) and an 8-bit shift register. How many flip-flops in total, with a binary-encoded FSM?

### Problem 08-08.12 [C]

**A debouncer.** A push button is sampled every 1 ms. The debounced output changes only after 8 consecutive samples agree with the new level. (a) Built as a pure FSM (a stable-low state, 7 states counting consecutive 1s, a stable-high state and 7 states counting consecutive 0s), how many states and binary flip-flops does it need? (b) Built as a 4-state controller plus a counter that counts consecutive samples up to 8, how many flip-flops? (c) If the button settles exactly at a sample instant, how long after that first stable sample does the output change?

### Problem 08-08.13 [C]

**Moore to Mealy, then minimize.** (a) Convert the Moore 101 detector to a Mealy machine with the same states using $\lambda'(s, x) = \lambda(\delta(s, x))$, and write its table. (b) Which states become equivalent, and how many states remain after merging? (c) On the input of Example 08-08.1, in which cycle does the converted machine first output 1?

### Problem 08-08.14 [C]

**Encodings that detect and correct upsets.** A safe 4-state machine needs codes with a minimum Hamming distance between any two states. (a) What is the fewest bits for minimum distance 2 (single flips detectable)? Give such a code. (b) What is the fewest bits for minimum distance 3 (single flips correctable)? Use the Hamming bound to show that fewer bits are impossible, and give a code.

### Problem 08-08.15 [C]

**What one-hot costs across a chip.** A 20-state controller is built in SKY130 with flip-flops with reset (25.024 µm²; a NAND2 is 3.7536 µm²). (a) How many flip-flops does it use in binary and in one-hot encoding? (b) What is the extra flip-flop area of one-hot, in µm² and NAND2 equivalents? (c) A chip has 50 copies of this controller. What is the total extra area in mm²?

### Problem 08-08.16 [B]

**Analyzing a JK circuit.** A circuit has two JK flip-flops $A$ and $B$ and an input $x$, with $J_A = Bx$, $K_A = \overline{x}$, $J_B = x$ and $K_B = A$. (a) Derive the next-state equations for $A$ and $B$. (b) Write the state table. (c) Starting from $AB$ = 00, apply $x$ = 1, 1, 1, 0, 1 and list the states. (d) Which states does $x$ = 0 send to 00?

### Problem 08-08.17 [B]

**A mod-3 counter with T and JK flip-flops.** A counter cycles $AB$ = 00 → 01 → 10 → 00; the state 11 is unused. (a) Using T flip-flops and treating 11 as a don't care, find minimal equations for $T_A$ and $T_B$. (b) Repeat with JK flip-flops. (c) For each design, where does the unused state 11 go at the next edge? Is each design self-correcting?

### Problem 08-08.18 [C]

**Writing and verifying an FSM in Verilog.** Write a synthesizable Moore machine `det110` (inputs `clk`, `rst`, `x`; output `z`) that raises `z` in the cycle after the last three inputs were 1, 1, 0 (overlapping allowed), in the three-block style with a synchronous reset and a safe default. Then write a self-checking testbench that drives at least 2000 random input bits, compares `z` every cycle with a reference model (a shift register of the last three inputs, delayed one cycle), uses `!==`, and prints `TEST PASSED` or `TEST FAILED`. Check that a deliberately broken transition makes it fail.

---

## Objective coverage

| Learning objective (chapter 08-08) | Problems |
|---|---|
| 1. FSM model; analysis; Moore and Mealy | 1, 2, 3, 6, 13, 16 |
| 2. State diagrams from specifications | 3, 4, 6, 11, 12 |
| 3. State encoding and logic (D, JK and T flip-flops) | 1, 5, 8, 10, 14, 15, 17 |
| 4. State minimization | 7, 13 |
| 5. FSM timing | 9, 12 |
| 6. FSMs in Verilog and verification | 3, 4, 18 |
