# Problems 14-01 · Performance, Power and the Iron Law

Chapter: [14-01](../chapters/14-01-performance-power-iron-law.md) · Worked solutions: [14-01 solutions](../solutions/14-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** instruction counts are dynamic (as executed); "speedup" is old time over new time; dynamic power is $\alpha CV^2f$ with $\alpha C$ the effective switched capacitance; leakage power is $VI_{leak}$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-01.1 [A]

**The iron law.** A program executes 4 × 10⁹ instructions at a CPI of 0.8 on a 4 GHz processor. Find the execution time and the IPC.

### Problem 14-01.2 [A]

**Faster by how much?** (a) A program that took 10 s runs "30% faster". How long does it take now? (b) Another program's time falls from 10 s to 7 s. Find the speedup and express it as "percent faster".

### Problem 14-01.3 [A]

**CPI from a mix.** A program is 50% ALU instructions (CPI 1), 30% memory instructions (CPI 3) and 20% branches (CPI 2). Find the CPI and the fraction of time spent on memory instructions.

### Problem 14-01.4 [B]

**Clock against CPI.** Design X runs at 3 GHz with CPI 1.0. Design Y uses a deeper pipeline to reach 4 GHz, but its CPI rises to 1.3 because of more stall cycles. With the same instruction count, which is faster, and by how much?

### Problem 14-01.5 [B]

**Which enhancement?** Floating-point work is 40% of a program's time. Option 1 makes floating point 4× faster. Option 2 makes everything else 1.2× faster. Find each overall speedup.

### Problem 14-01.6 [B]

**What it takes.** 60% of a program's time can be accelerated. How fast must that part become for the whole program to run 1.5× faster? What overall speedup is impossible to reach?

### Problem 14-01.7 [B]

**Parallel efficiency.** A job is 95% parallelizable. Find its speedup and parallel efficiency ($S/N$) on 8 and on 64 processors, and its ceiling.

### Problem 14-01.8 [B]

**Average rate.** Three benchmarks each perform 10⁹ floating-point operations, at 100, 200 and 400 MFLOPS. Find the total time, the true average rate, and the arithmetic mean of the rates. Which mean gives the true rate?

### Problem 14-01.9 [B]

**A phone block.** A block of a phone processor has an effective switched capacitance of 0.5 nF and executes one operation per cycle. Find its dynamic power and energy per operation at 0.8 V and 2.0 GHz, and at 0.6 V and 1.5 GHz. By what factor does the energy per operation fall?

### Problem 14-01.10 [A]

**The cube law.** A core runs at 3 GHz and 1.0 V, and its maximum frequency is proportional to its supply voltage. If it is slowed to 2 GHz with the voltage reduced in proportion, find the ratio of dynamic power, the ratio of dynamic energy per operation, and the ratio of run time.

### Problem 14-01.11 [C]

**The energy-optimal clock.** A core needs $V = 0.3 + 0.2f$ volts to run at $f$ GHz, has an effective switched capacitance of 1 nF and a leakage current of 0.5 A. For a task of 10⁹ cycles, write the energy as a function of $f$, find the frequency that minimizes it, the voltage there and the minimum energy, and compare with running at 3 GHz.

### Problem 14-01.12 [C]

**When racing wins.** For the core and task of Example 14-01.5: (a) how large would the leakage power at 0.9 V have to be for racing to idle to use less energy than running at 0.75 V and 2.4 GHz? (b) Keep the leakage at 1.2 W, but suppose the rest of the system (memory, display, radios) draws a constant power while the task runs and can sleep when it ends. Above what system power does racing to idle win?

### Problem 14-01.13 [C]

**The reference does not matter.** Three benchmarks have reference times 100, 200 and 400 s. Machine A runs them in 20, 50 and 200 s; machine B in 25, 40 and 100 s. (a) Find each machine's geometric mean of speed ratios to the reference and their ratio. (b) Find the ratio of total times. (c) Find the arithmetic means of the speed ratios and their ratio. (d) Normalize B's times to A's instead of the reference and recompute both means of B's speed ratios. Which summary is unchanged?

### Problem 14-01.14 [C]

**Two serial fractions.** A run on 64 processors spends 5% of its time in serial code. (a) Find the scaled (Gustafson) speedup. (b) For the same problem, find the serial fraction of the single-processor run, and show that Amdahl's law gives the same 64-processor speedup. (c) What would 128 processors give on this same problem?

### Problem 14-01.15 [B]

**Comparing architectures.** Chip A runs a task in 1 s using 2 J; chip B takes 1.5 s and 1.2 J. (a) Find each chip's EDP and ED²P. (b) Assuming energy scales as $1/T^2$ when a chip is voltage-scaled (dynamic energy only), how much energy would A use if slowed to B's 1.5 s? Which is the better architecture?

---

## Objective coverage

| Learning objective (chapter 14-01) | Problems |
|---|---|
| 1. Iron law and CPI from a mix | 1, 2, 3, 4 |
| 2. Amdahl's and Gustafson's laws | 5, 6, 7, 14 |
| 3. Choosing the right mean | 8, 13 |
| 4. Dynamic and leakage power, energy and DVFS | 9, 10, 11, 12 |
| 5. Performance per watt and the delay products | 12, 15 |
