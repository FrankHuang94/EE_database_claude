# Problems 11-03 · Convolution

Chapter: [11-03](../chapters/11-03-convolution.md) · Worked solutions: [11-03 solutions](../solutions/11-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** sequences are listed from the first nonzero index stated, and are zero elsewhere; systems are LTI and at rest; for every convolution, check the length (or support) and the area.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-03.1 [A]

**By table.** $x[n] = 2, -1, 1$ for $n = 0, 1, 2$, and $h[n] = 1, 3$ for $n = 0, 1$. Find $y = x * h$ with a superposition table, then check its length and its sum.

### Problem 11-03.2 [A]

**Supports that do not start at zero.** $x[n] = 1$ for $-2 \le n \le 1$, and $h[n] = 1$ at $n = 3$, $-1$ at $n = 4$. (a) Predict the support of $y$. (b) Compute $y$. (c) Explain the result in words: what does this $h$ do to any input?

### Problem 11-03.3 [A]

**Impulses as building blocks.** (a) Simplify $x[n] * \delta[n - 3]$ and $u[n] * \delta[n + 2]$. (b) A system computes $y[n] = 2x[n - 1] - x[n - 3]$. Write its impulse response and find its DC gain. (c) What is the impulse response of a system that does nothing ($y = x$)?

### Problem 11-03.4 [A]

**Polynomials and integers.** (a) Compute $[1, 2] * [3, -1, 1]$ (both starting at $n = 0$) and check it by multiplying $(1 + 2z)(3 - z + z^2)$. (b) Compute $[1, 2] * [3, 1, 1]$ and use it to find $12 \times 311$ without carrying.

### Problem 11-03.5 [B]

**Exponential sequences.** (a) Find $y = x * h$ with $x = h = 0.5^nu[n]$, and its values at $n = 0$ to 3. (b) A four-sample boxcar $x = u[n] - u[n - 4]$ drives $h = 0.5^nu[n]$. Find $y[2]$, $y[3]$ and $y[4]$, and a formula for $n \ge 3$.

### Problem 11-03.6 [B]

**Step into an exponential.** A CT system has $h(t) = e^{-2t}u(t)$ ($t$ in seconds). Find its step response by convolution, its value at 0.5 s, and its final value. Relate the final value to $h$.

### Problem 11-03.7 [B]

**Graphical convolution.** (a) Convolve two unit-height pulses on $[0, 1)$. Find $y$ at 0.5, 1 and 1.5. (b) Convolve $x = 1$ on $[0, 1)$ with the ramp segment $h(t) = t$ on $[0, 2)$ (zero elsewhere). Find the breakpoints, the piecewise expression, $y$ at 0.5, 1.5 and 2.5, and the area.

### Problem 11-03.8 [B]

**An RC circuit with a decaying input.** An RC low-pass with $\tau$ = 1 ms ($h = \frac{1}{\tau}e^{-t/\tau}u(t)$) is driven by $x(t) = 5e^{-t/(2\,\text{ms})}u(t)$ V. (a) Find $y(t)$ by convolution. (b) Find the time and value of its peak. (c) Find its area and check it against the area rule.

### Problem 11-03.9 [B]

**From step response to impulse response.** (a) A DT system's measured step response is $s[n] = 1 - 0.5^{n+1}$ for $n \ge 0$. Find $h[n]$ and the DC gain. (b) A CT system's step response is $s(t) = 1 - (1 + t/\tau)e^{-t/\tau}$ for $t \ge 0$. Find $h(t)$ and identify the system.

### Problem 11-03.10 [B]

**Cascade and parallel.** $h_1 = 1, 1$ and $h_2 = 1, -1$ (both at $n = 0, 1$). (a) Find the impulse response of the cascade and of the parallel connection. (b) Find the cascade's step response for all $n$, and explain it. (c) Show that swapping the order of the cascade gives the same impulse response.

### Problem 11-03.11 [B]

**Stable or not?** Decide, and give $\sum\lvert h\rvert$ (or $\int\lvert h\rvert$) where it is finite: (a) $h[n] = 0.9^n\cos(\pi n/4)\,u[n]$ (a bound suffices); (b) $h[n] = u[n] - u[n - 100]$; (c) $h(t) = u(t)$; (d) $h[n] = n\,0.5^nu[n]$; (e) $h(t) = u(t)/(1 + t)$.

### Problem 11-03.12 [C]

**Overflow in a high-pass filter.** An FIR filter has $h = 0.25, -0.5, 1, -0.5, 0.25$. (a) Find its DC gain and its worst-case gain. (b) Find the input pattern that reaches the worst case, and the steady output magnitude for $x[n] = (-1)^n$. (c) How many guard bits does the accumulator need above the input's full scale?

### Problem 11-03.13 [C]

**A matched filter.** A transmitter marks the start of a packet with the three-chip pattern $p = 1, 1, -1$. (a) Write the matched filter's impulse response. (b) Find the filter's output when the input is $p$ itself, and identify the peak and the largest sidelobe. (c) Why do receivers prefer patterns whose sidelobes are small compared with the peak?

### Problem 11-03.14 [C]

**Diligence on an accelerator claim.** A start-up's accelerator has 4096 MAC units at 1 GHz. Its slides claim that a 3 × 3 convolution layer with 128 input and 128 output channels on a 28 × 28 output runs in 25 µs. (a) Count the layer's MACs. (b) Find the minimum time at 100% utilization. (c) What utilization does the claim imply, and what does that tell you? (d) Name two legitimate ways the claim could still be true, and the question that would distinguish them.

---

## Objective coverage

| Learning objective (chapter 11-03) | Problems |
|---|---|
| 1. Derive convolution; the impulse response describes an LTI system | 3, 9, 10 |
| 2. Compute DT and CT convolutions | 1, 2, 4, 5, 6, 7, 8 |
| 3. Properties: commutative, associative, distributive, shift, area, support | 2, 3, 10 |
| 4. Step and impulse responses; circuits by convolution | 6, 8, 9 |
| 5. Stability from absolute summability; worst-case gain | 11, 12 |
| 6. MAC cost; convolution versus correlation | 13, 14 |
