# Problems 16-11 · DSP Hardware Architectures

Chapter: [16-11](../chapters/16-11-dsp-hardware-architectures.md) · Worked solutions: [16-11 solutions](../solutions/16-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unless stated, a multiplier takes 2.0 ns and an adder 0.5 ns; each multiplier or DSP block completes one multiplication per clock. Energy figures are the 45 nm values of §3.6 (R-208). Problems marked *(lab)* need the lab's `hwarch.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-11.1 [A]

**MAC widths.** A 128-tap filter multiplies 12-bit samples by 18-bit coefficients. Give the product and accumulator widths that rule out overflow.

### Problem 16-11.2 [A]

**DSP blocks.** A 128-tap symmetric FIR filter runs at 100 MS/s on DSP blocks clocked at 500 MHz. How many blocks are needed with and without symmetry folding?

### Problem 16-11.3 [A]

**Shift-and-add constants.** How many adders or subtractors implement multiplication by 0.875 and by 0.9375 in CSD form, and how many in plain binary?

### Problem 16-11.4 [B]

**Iteration bound of a biquad.** A direct-form all-pole biquad $y[n] = x[n] - a_1y[n - 1] - a_2y[n - 2]$ is built with one multiplier in each feedback path, and both adders lie inside each loop (the products are added together, then added to $x[n]$). Identify its loops, their computation times and register counts, and its iteration bound and maximum sample rate.

### Problem 16-11.5 [B]

**Look-ahead by four.** *(lab)* Write the look-ahead-by-4 form of $y[n] = ay[n - 1] + x[n]$, confirm numerically that it produces the same output for $a = 0.9$, and give its iteration bound with the conventions above.

### Problem 16-11.6 [B]

**Folding.** A 16-tap FIR filter is built with MAC units at 400 MHz. What is the highest sample rate with one MAC, and with four?

### Problem 16-11.7 [B]

**CORDIC gain and iterations.** Compute $K_8$ and $K_{16}$. How many iterations bring the residual angle below $2^{-11}$ rad?

### Problem 16-11.8 [B]

**Vectoring.** *(lab)* Use a 16-iteration CORDIC in vectoring mode to find the magnitude and angle of $(3, 4)$.

### Problem 16-11.9 [B]

**Energy per MAC.** Using the 45 nm figures, compare the energy of an 8-bit integer MAC (an 8-bit multiply into a 32-bit accumulator), a 32-bit integer MAC and a 32-bit floating-point MAC (multiply plus add), and their power at $10^9$ MACs per second. How many 32-bit integer MACs cost as much as one 64-bit DRAM access?

### Problem 16-11.10 [C]

**A filter on a microcontroller.** A 64-tap FIR filter at 48 kHz runs on a Cortex-M55 (four 16-bit MACs per cycle, R-233) at 100 MHz. What fraction of the core's peak MAC capacity does it use? Repeat for a Cortex-M52 with single-beat Helium (two 16-bit MACs per cycle). Why is the real load higher?

### Problem 16-11.11 [C]

**Pipelining an adder tree.** A 64-tap FIR filter uses a balanced adder tree. With registers after the multipliers and after every adder level, what is the critical path, the maximum clock and the latency in cycles? Compare with the unpipelined tree (16-08 Example 16-08.2).

### Problem 16-11.12 [C]

**Fixed-point CORDIC accuracy.** *(lab)* For the lab's 14-iteration, Q2.14 CORDIC, find the worst error (in LSB) over all 65,536 input codes. Explain why it exceeds the residual-angle error of about 2 LSB, and quantify the effect of rounding the shifts, of guard bits in $x$ and $y$, and of extra angle bits.

---

## Objective coverage

| Learning objective (chapter 16-11) | Problems |
|---|---|
| 1. MAC datapaths | 1 |
| 2. MAC rates, folding and unfolding | 2, 6, 10 |
| 3. Critical paths, iteration bound, look-ahead | 4, 5, 11 |
| 4. DSP processors | 10 |
| 5. Energy and multiplierless arithmetic | 3, 9 |
| 6. CORDIC | 7, 8, 12 |
