# Problems 19-12 · Design for Test: Scan, BIST and ATPG

Chapter: [19-12](../chapters/19-12-design-for-test.md) · Worked solutions: [19-12 solutions](../solutions/19-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Faults are single stuck-at faults unless stated; "x/0" means line x stuck-at-0. Coverage counts detectable faults. Problems marked *(lab)* can be checked with `labs/19-12-lab/dft.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-12.1 [A]

**Quality targets.** A process yields 90 %. (a) What defect level does 95 % fault coverage give, in DPPM? (b) What coverage gives 10 DPPM?

### Problem 19-12.2 [A] *(lab)*

**One NAND gate.** For a single three-input NAND gate: (a) how many stuck-at faults are there, and how many equivalence classes? (b) Find a minimal test set and explain why it cannot be smaller.

### Problem 19-12.3 [A]

**Two-pattern tests.** (a) Why can no single static pattern detect a slow-to-rise fault? (b) In a scan design, what is the difference between launch-on-shift and launch-on-capture? (c) Which is easier to apply at speed, and which is easier for timing closure?

### Problem 19-12.4 [B] *(lab)*

**The c17 benchmark.** ISCAS-85's c17 has inputs N1, N2, N3, N6, N7 and six NAND2 gates: N10 = NAND(N1, N3), N11 = NAND(N3, N6), N16 = NAND(N2, N11), N19 = NAND(N11, N7), N22 = NAND(N10, N16), N23 = NAND(N16, N19), with outputs N22 and N23. (a) Which nets fan out, and how many single stuck-at faults are there? (b) Using the lab, how many functional equivalence classes are there, and are any faults undetectable? (c) What is the smallest test set that detects every fault?

### Problem 19-12.5 [B] *(lab)*

**Tests by hand.** $F = \overline{(A + B)\,C}$ is an OR gate (output o) feeding a NAND2 with C. (a) Find every test for A/1. (b) Find every test for o/0. (c) Explain each answer in terms of activation and propagation.

### Problem 19-12.6 [B]

**Random-pattern resistance.** (a) How many random patterns give 99 % confidence of detecting the output stuck-at-0 of an 8-input AND gate? (b) Why is its output stuck-at-1 detected almost at once? (c) Suggest a test point that makes the stuck-at-0 easy.

### Problem 19-12.7 [B]

**Scan time.** A design has 500 000 scan flip-flops and needs 5000 patterns, shifted at 25 MHz. (a) Derive the cycle count $P(L + 1) + L$ for overlapped scan. (b) Find the test time with 16 chains. (c) Find it with 1600 internal chains behind a compressor on the same 16 pins. (d) What is the time ratio, and why is it not exactly 100?

### Problem 19-12.8 [B] *(lab)*

**LFSR periods.** (a) List the states of a 3-bit LFSR with feedback polynomial $x^3 + x^2 + 1$ starting from 001, and state its period. (b) What is the period of the 4-bit LFSR $x^4 + x^2 + 1$ from 0001, and why is it not 15?

### Problem 19-12.9 [B]

**Memory BIST.** (a) How many operations and how much time does March C− take on a 4 Mbit SRAM organized as 131 072 words of 32 bits, at 100 MHz? (b) Why does March C− need elements in both ascending and descending address order?

### Problem 19-12.10 [B]

**Boundary scan.** A chip has 256 boundary-scan cells and a 10 MHz TCK. (a) Ignoring TAP state transitions, how long does it take to shift one full EXTEST pattern? (b) On a board, this chip is in a chain with three other chips that are in BYPASS. How long does one pattern take now? (c) How many bits is the IDCODE register?

### Problem 19-12.11 [C]

**The defect-level model.** (a) Derive $\text{DL} = 1 - Y^{1-T}$ from independent fault sites. (b) Derive the first-order approximation and find its relative error at $Y = 0.5$, $T = 0.9$. (c) Name two ways in which real defects violate the model's assumptions, and the direction in which each one biases the estimate.

### Problem 19-12.12 [C] *(lab)*

**MISR aliasing exactly.** An $n$-bit MISR (seed 0) compacts $m$ response words. (a) Show that the signature of a faulty response equals the good signature XOR the signature of the error stream, so the fault escapes exactly when the error stream's signature is 0. (b) Show that a single-bit error can never alias. (c) Argue that the fraction of nonzero error streams that alias is $(2^{n(m-1)} - 1)/(2^{nm} - 1)$, and evaluate it for $n = 4$, $m = 3$ against $2^{-n}$. (d) Check (c) by exhaustive simulation with the lab.

### Problem 19-12.13 [B]

**Safety metrics in the field.** ISO 26262-5, as reproduced in a TI application report (R-320), requires single-point-fault metrics (SPFM) of at least 90, 97 and 99 % and latent-fault metrics (LFM) of at least 60, 80 and 90 % for ASIL B, C and D. A block's on-line checker gives an SPFM of 98 %, and start-up memory BIST plus periodic logic BIST give an LFM of 85 %. (a) Which ASILs does the block meet on each metric, and overall? (b) To reach ASIL D, by what fraction must the undetected latent faults and the uncovered single-point faults each be reduced? (c) Why are these metrics a matter of in-field self-test rather than production fault coverage, and what does a datacenter operator screen for that is analogous?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Yield, coverage and defect level | 1, 11 |
| 2. Fault models and collapsing | 2, 3, 4 |
| 3. Test generation and redundancy | 4, 5, 6 |
| 4. Scan, test time and compression | 7 |
| 5. LFSRs, MISRs and March tests | 8, 9, 12 |
| 6. Boundary scan and in-field test | 10, 13 |
