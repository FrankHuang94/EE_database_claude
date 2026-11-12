# Problems 00-02 · The Abstraction Stack

Chapter: [00-02](../chapters/00-02-the-abstraction-stack.md) · Worked solutions: [00-02 solutions](../solutions/00-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design. Use $c = 2.998\times10^8$ m/s unless told otherwise. $Q(x)$ is the upper-tail probability of the standard normal distribution (Python: `scipy.stats.norm.sf(x)`).

---

## Problems

### Problem 00-02.1 [A]

For each abstraction, state what it hides and one condition under which it fails:

(a) the lumped-circuit abstraction; (b) the digital abstraction; (c) the instruction-set architecture; (d) the process design kit (PDK).

### Problem 00-02.2 [A]

Compute the free-space wavelength at (a) 50 Hz (in km), (b) 2.4 GHz (Wi-Fi, in cm) and (c) 77 GHz (automotive radar, in mm). (d) What frequency, in THz, corresponds to green light at 500 nm?

### Problem 00-02.3 [A]

A 1.0 V logic family has $V_{OL} = 0.1$ V, $V_{OH} = 0.9$ V, $V_{IL} = 0.35$ V and $V_{IH} = 0.65$ V.

(a) Compute $NM_L$ and $NM_H$.
(b) What would it mean if a datasheet listed $V_{IL} > V_{IH}$?

### Problem 00-02.4 [B]

Decide whether each is lumped ($\ell < \lambda/10$), giving its length in wavelengths:

(a) a 1 m audio cable at 20 kHz, wave speed $2\times10^8$ m/s;
(b) a 30 cm board trace carrying a 16 GHz component, $v = 1.5\times10^8$ m/s;
(c) a 5 mm package trace at 1 GHz, $v = 1.5\times10^8$ m/s.

### Problem 00-02.5 [B]

A digital signal has a 100 ps rise time and travels on a board at $1.5\times10^8$ m/s. Using the rule "treat as a transmission line once the one-way delay exceeds $t_r/6$", find the longest trace that can be treated as lumped. Repeat with the stricter $t_r/10$ rule.

### Problem 00-02.6 [B]

Family C has $V_{OL} = 0.3$ V, $V_{OH} = 3.0$ V, $V_{IL} = 1.0$ V and $V_{IH} = 2.3$ V. Family B (Example 00-02.2) has $V_{OL} = 0.2$ V, $V_{OH} = 1.6$ V, $V_{IL} = 0.6$ V and $V_{IH} = 1.2$ V.

Compute both noise margins for C driving B and for B driving C. Which connection works logically, and what other concern remains?

### Problem 00-02.7 [B] (design)

A digital chain must make a mid-swing decision at each of $10^9$ stages (swing 1 V, threshold distance 0.5 V), with a total error probability below $10^{-12}$. Using $P_{total} \approx Np$, what per-stage error probability is required, and what is the largest allowable per-stage noise σ?

### Problem 00-02.8 [B]

An analog signal passes through $N$ identical stages, each adding independent noise of the same power.

(a) By how many dB does the signal-to-noise ratio degrade after 100 stages?
(b) After how many stages has it degraded by 10 dB?

### Problem 00-02.9 [B]

At a 5 GHz clock, how far can a signal travel in half a clock cycle at $1.5\times10^8$ m/s? Compare with the size of a large die (about 25 mm).

### Problem 00-02.10 [C]

Repeat Example 00-02.5 with source resistance $R_s = 25\ \Omega$ ($Z_0 = 50\ \Omega$, 1 ns line, open end, 1 V step). Find the source reflection coefficient, the launched wave, and the far-end voltage after the first three arrivals. Is the ringing better or worse than with 10 Ω, and why? (The lab's ngspice netlist checks your answer.)

### Problem 00-02.11 [C] (security)

A 32-bit register is written once per operation. Each bit's output node has about 10 fF of capacitance, and the supply is 0.8 V. A bit that rises from 0 to 1 draws $CV^2$ from the supply; a bit that falls draws nothing from the supply (it dumps its stored charge to ground).

(a) The register holds 0x00000000. What is the difference in supply energy between writing 0xFFFFFFFF (all 32 bits rise) and writing 0x00000000 again (no bit changes)?
(b) If a data-dependent difference of this size occurs on each of $10^8$ operations per second, what average power difference does that make?
(c) Explain how an attacker measuring supply current could exploit this, and name one countermeasure.

### Problem 00-02.12 [C]

A synchronous design must fit all logic between two flip-flops into one clock period. Flip-flop overhead (clock-to-output delay plus setup time) is 60 ps, and each gate adds 15 ps.

(a) How many gate delays fit in a cycle at 3 GHz? At 4 GHz?
(b) A signal must also cross 5 mm of wire. Even at $1.5\times10^8$ m/s (ignoring the wire's RC delay), how many gate delays does that consume?
(c) What does this imply about why clock frequencies stopped rising rapidly?

---

## Objective coverage

| Learning objective (chapter 00-02) | Problems |
|---|---|
| 1. Levels of the stack and what each hides | 1 |
| 2. Lumped abstraction; wavelength and edge-rate tests | 2, 4, 5, 10 |
| 3. Noise margins and interfacing | 3, 6 |
| 4. Regeneration versus accumulation | 7, 8 |
| 5. Where abstractions leak, and who owns them | 9, 11, 12 |
