# Problems 00-04 · Toolchain Setup Walkthrough

Chapter: [00-04](../chapters/00-04-toolchain-walkthrough.md) · Worked solutions: [00-04 solutions](../solutions/00-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design. Several answers can be checked by running the lab files. Do the hand calculation first.

---

## Problems

### Problem 00-04.1 [A]

Convert each SPICE value to an ordinary number in SI units: (a) `4.7k` ohms, (b) `10u` farads, (c) `2.2n` farads, (d) `1meg` ohms, (e) `3m` amperes, (f) `1M` ohms.

### Problem 00-04.2 [A]

A 12 V source drives $R_1 = 10$ kΩ in series with $R_2 = 5$ kΩ to ground. Find the output voltage across $R_2$, the current, and the total power delivered by the source. What sign will SPICE report for the source current?

### Problem 00-04.3 [A]

(a) In Python, does `0.1 + 0.2 == 0.3` evaluate to True?
(b) Compute the relative difference $\lvert(0.1 + 0.2) - 0.3\rvert/0.3$ using the value of `0.1 + 0.2 - 0.3` from Example 00-04.3.
(c) Is `1.0 + eps/4 == 1.0` True or False, where `eps` is machine epsilon? Why?

### Problem 00-04.4 [B]

Write (on paper) a netlist for this circuit and predict its `.op` results:

- a 10 V source from node `n1` to ground;
- $R_1 = 1$ kΩ from `n1` to node `a`, and $R_2 = 2$ kΩ from `a` to ground;
- $R_3 = 1$ kΩ from `a` to node `b`, and $R_4 = 1$ kΩ from `b` to ground.

Find $V_a$, $V_b$ and the source current. (The lab netlist `divider.cir` contains this circuit as a check.)

### Problem 00-04.5 [B]

An RC low-pass has $R = 10$ kΩ and $C = 10$ nF. (a) Find its −3 dB frequency. (b) Find its gain in dB at 10 kHz. (Confirm both with `rc_ac.cir`.)

### Problem 00-04.6 [B]

For $x = 10^8$, the expression $\sqrt{x^2 + 1} - x$ evaluates to 0.0 in double precision.

(a) Explain why.
(b) Rewrite it in a mathematically equivalent but numerically stable form (hint: multiply and divide by $\sqrt{x^2 + 1} + x$), and evaluate it.

### Problem 00-04.7 [B]

At $10^9$ test vectors per second, how long does exhaustive testing take for (a) an 8-bit adder (two 8-bit inputs), (b) a 16-bit multiplier (two 16-bit inputs) and (c) a 32-bit adder? What does (c) tell you about how processors are verified?

### Problem 00-04.8 [B]

A transient simulation covers 1 ms with a fixed 1 ns time step. (a) How many time steps is that? (b) If each step takes 10 µs of computer time, how long does the simulation take? (c) Repeat (b) for a 1 ps step. What does this suggest about simulating a whole chip at transistor level?

### Problem 00-04.9 [C] (how SPICE solves nonlinear circuits)

A 5 V source drives a diode through 1 kΩ. The diode current is $I_D = I_s(e^{V_D/V_T} - 1)$ with $I_s = 10^{-14}$ A and $V_T = 25.852$ mV. KCL gives $g(V_D) = \frac{5 - V_D}{1000} - I_s(e^{V_D/V_T} - 1) = 0$.

(a) Write the Newton–Raphson update $V_{k+1} = V_k - g(V_k)/g'(V_k)$ explicitly.
(b) Starting from $V_0 = 0.70$ V, perform three iterations (use Python or a calculator), and report the converged $V_D$ and diode current.
(c) Starting from $V_0 = 0.60$ V, plain Newton takes 32 iterations to converge to 1 nV. Compute the first iterate from 0.60 V and explain what goes wrong. What safeguard does SPICE add?

### Problem 00-04.10 [C] (auditing a number)

A verify script computes 2.2046 for a quantity published as "2.21" in an answer key. The checker allows a difference of half a unit in the last published digit.

(a) Does the check pass? Show the comparison.
(b) What should the published value be?
(c) Would publishing "2.2" pass? What is the trade-off in publishing fewer digits?

---

## Objective coverage

| Learning objective (chapter 00-04) | Problems |
|---|---|
| 1. Install and smoke-test the toolchain; read the checks | 10 (and the lab) |
| 2. Write and read SPICE netlists (.op, .ac); unit suffixes | 1, 2, 4, 5 |
| 3. Self-checking testbenches; exhaustive testing limits | 7 |
| 4. Floating-point limits and tolerant comparison | 3, 6, 10 |
| 5. How simulators solve circuits; convergence; cost | 8, 9 |
