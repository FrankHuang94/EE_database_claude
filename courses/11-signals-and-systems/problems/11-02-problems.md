# Problems 11-02 · Systems and Their Properties

Chapter: [11-02](../chapters/11-02-system-properties.md) · Worked solutions: [11-02 solutions](../solutions/11-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $y = \mathcal{T}\{x\}$; systems start at rest unless an initial condition is given; "stable" means BIBO-stable; to prove a property, argue for every input; to disprove it, give one specific counterexample with numbers.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-02.1 [A]

**Memory and causality.** For each system, say whether it is memoryless and whether it is causal. For each noncausal system, name a time at which the output needs a future value of the input. (a) $y(t) = 3x(t) - 2$; (b) $y(t) = x(t - 1) + x(1 - t)$; (c) $y[n] = \sum_{k=-\infty}^{n+1}x[k]$; (d) $y[n] = x[n]\,x[n - 1]$; (e) $y(t) = \int_{t-1}^{t}x(\tau)\,d\tau$; (f) $y(t) = x(t/2)$.

### Problem 11-02.2 [A]

**Linear or not?** Prove linearity, or give a numerical counterexample. (a) $y = x^2$ (use constant inputs 1 and 2). (b) $y = \lvert x\rvert$ (test additivity with 1 and −1). (c) $y[n] = x[n] + x[n - 1]$. (d) $y(t) = x(t)\cos t$. (e) A rounding quantizer $y = \operatorname{round}(x)$ with step 1 (test additivity with 0.4 and 0.4).

### Problem 11-02.3 [A]

**Time-invariant or not?** Prove time invariance, or give a counterexample. (a) $y[n] = x[n] - x[n - 1]$. (b) Time reversal $y(t) = x(-t)$, using the pulse $p(t) = u(t) - u(t - 1)$ and a delay of 2 s: find the interval on which $\mathcal{T}\{p(t - 2)\}$ is nonzero and the interval on which $y(t - 2)$ is nonzero. (c) A switch that closes at $t = 0$, $y(t) = x(t)\,u(t)$, with the input $u(t + 1)$ delayed by 2 s: at what time does each path's output switch on? (d) $y[n] = (-1)^n\,x[n]$ with the input $\delta[n]$ delayed by one sample: compare the weights.

### Problem 11-02.4 [A]

**Bounded or not?** Inputs satisfy $\lvert x\rvert \le 3$. For each system, find an output bound or show that none exists. (a) $y = x^2$. (b) $y(t) = e^{x(t)}$. (c) $y[n] = \sum_{k=n-4}^{n}x[k]$. (d) $y(t) = \int_{-\infty}^{t}x(\tau)\,d\tau$. (e) $y[n] = n\,x[n]$. (f) $y(t) = x(t)/(1 + t^2)$.

### Problem 11-02.5 [B]

**Inverses.** Find the inverse system, or show that none exists; for each inverse, say whether it is stable. (a) $y[n] = x[n] - 0.5\,x[n - 1]$; also find the sum of the inverse's impulse-response magnitudes. (b) $y = x^3$. (c) $y(t) = dx/dt$. (d) $y[n] = x[2n]$. (e) $y[n] = x[n] + x[n - 1]$: find the causal inverse, and its output at $n = 9$ for the bounded input $(-1)^nu[n]$.

### Problem 11-02.6 [B]

**Distortion of a bipolar transistor.** A transistor biased at collector current $I_C$ has $i_C = I_Ce^{v/V_T}$ for a small signal $v$ added to its base–emitter bias, with $V_T$ = 25.852 mV. (a) Expand $i_C$ to third order in $v$ and identify $a_1$, $a_2$ and $a_3$. (b) Show that $\text{HD2} \approx A/(4V_T)$ and $\text{HD3} \approx A^2/(24V_T^2)$ for $v = A\cos\omega t$, and explain why $I_C$ does not appear. (c) Evaluate both in percent for $A$ = 1 mV and $A$ = 5 mV. (d) Find the amplitude that gives 1% HD2. (e) Using $e^{x\cos\theta} = I_0(x) + 2\sum_{k\ge1}I_k(x)\cos k\theta$ (modified Bessel functions), the exact HD2 is $I_2(x)/I_1(x)$ with $x = A/V_T$. Evaluate it at 5 mV and compare.

### Problem 11-02.7 [B]

**Interconnections.** Prove: (a) a cascade of two linear systems is linear; (b) a cascade of two time-invariant systems is time-invariant; (c) the parallel combination $y = \mathcal{T}_1\{x\} + \mathcal{T}_2\{x\}$ of two linear systems is linear; (d) the inverse of an invertible linear system is linear.

### Problem 11-02.8 [B]

**Order matters, except for LTI systems.** (a) A squarer and a gain of 2 in cascade: find the output for the constant input 3 in each order. (b) A one-sample delay and the decimator $y[n] = x[2n]$, with the input $x[n] = n$: find the output at $n = 3$ for "decimate, then delay" and for "delay, then decimate". (c) Show that a gain of 3 and a delay of two samples give the same output in either order, for every input.

### Problem 11-02.9 [B]

**An accumulator that is not at rest.** $y[n] = y[n - 1] + x[n]$ for $n \ge 0$, with $y[-1] = 5$. (a) Find $y[3]$ for $x = u[n]$ and for $x = 2u[n]$, and twice the first answer. (b) Split each output into its zero-input and zero-state parts. (c) Is the system linear? Incrementally linear?

### Problem 11-02.10 [B]

**A resonator is not BIBO-stable.** A series LC circuit, $L$ = 1 mH and $C$ = 1 µF, starts at rest and is driven by $v_s = \cos\omega_0t$ V at its resonant frequency, so that $LC\,\ddot v_C + v_C = v_s$. (a) Find $\omega_0$ and $f_0$. (b) Verify that $v_C(t) = \tfrac12\omega_0t\sin\omega_0t$ satisfies the equation and the initial conditions, and find the amplitude of $v_C$ at 1 ms and at 10 ms. (c) A 1 Ω resistor is added in series. Find $Q = \tfrac1R\sqrt{L/C}$ and the steady-state capacitor amplitude $Q \times 1$ V.

### Problem 11-02.11 [B]

**A chopper.** A chopper multiplies its input by a square wave $s(t)$ of period 8 µs, with $s = +1$ for the first half of each period (starting at $t = 0$) and $-1$ for the second. (a) Is $y(t) = x(t)\,s(t)$ linear? (b) Show that it is not time-invariant by comparing $\mathcal{T}\{u(t - 4\ \mu\text{s})\}$ with $y(t - 4\ \mu\text{s})$ at $t$ = 5 µs, for the input $u(t)$. (c) Which delays do commute with it? (d) Is it invertible, and what is the inverse? (e) Find the chopping frequency.

### Problem 11-02.12 [C]

**How tight is the bound?** $y[n] = 0.99\,y[n - 1] + x[n]$ starts at rest, with $\lvert x\rvert \le 1$. (a) Find the stability bound. (b) For a step input, find the first $n$ at which $y[n] \ge 99$, and the time at a 1 kHz sample rate (with $n = 0$ at $t = 0$). (c) For $a = -0.99$, which bounded input gives the largest $\lvert y[N]\rvert$ at a chosen time $N$? (d) Show that no bound exists for $a = 1$ or $a = -1$.

### Problem 11-02.13 [C]

**A latency budget.** A guitar effects processor sampling at 48 kHz must keep its total latency to at most 2 ms. Its converters' decimation and interpolation filters already use 40 samples. (a) What is the total budget in samples? (b) What is the longest symmetric (linear-phase) FIR filter, with an odd number of taps, that fits? (c) An envelope follower designed offline uses a centered window that looks 10 ms ahead. How many samples is that, and can it be used live?

### Problem 11-02.14 [C]

**Diligence: "it's an LTI system".** A hearing-aid chip vendor says that its signal path "is LTI, so one impulse response characterizes it". The path contains a chopper-stabilized preamplifier (chopping at 125 kHz), a decimating ADC and an automatic gain control (AGC) that slowly adjusts its gain to hold the output at 0.5 V rms. (a) For steady sine inputs of 10 mV rms and 20 mV rms, find the AGC's settled gain in each case. Which property fails? (b) Is the AGC time-invariant? Explain. (c) Which properties do the chopper and the decimator break? (d) Propose three measurements that would test the vendor's claim, and say what result would support or refute it.

---

## Objective coverage

| Learning objective (chapter 11-02) | Problems |
|---|---|
| 1. Classify systems by the six properties, with proofs or counterexamples | 1, 2, 3, 4, 5, 7, 8, 11, 14 |
| 2. Linear versus incrementally linear; zero-input and zero-state responses | 9, 14 |
| 3. Harmonic and intermodulation distortion from polynomial coefficients | 6 |
| 4. Stability bounds; accumulators, integrators and resonators | 4, 10, 12 |
| 5. Inverse systems and unstable inverses | 5, 11 |
| 6. Latency imposed by causality | 1, 13 |
