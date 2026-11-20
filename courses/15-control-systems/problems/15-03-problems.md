# Problems 15-03 · Time Response and Specifications

Chapter: [15-03](../chapters/15-03-time-response.md) · Worked solutions: [15-03 solutions](../solutions/15-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Rise time is 10–90% of the final value; settling time is to within 2% of the final value unless stated; overshoot is relative to the final value. "Exact" means computed from the true step response, by hand or by simulation; "rule" means $t_s \approx 4/\sigma$ and $t_r \approx 1.8/\omega_n$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-03.1 [A]

**A first-order response from data.** A 1 V step applied to a system produces an output that rises without overshoot to 5 V and reaches 3.16 V after 4 ms. Find the DC gain, time constant, pole, rise time, settling time and bandwidth.

### Problem 15-03.2 [A]

**From a measured overshoot.** A second-order loop's step response overshoots by 25% and peaks at 2 ms. Find $\zeta$, $\omega_d$, $\omega_n$, the poles and the settling time by the rule.

### Problem 15-03.3 [A]

**Classify by damping.** For each characteristic polynomial, find $\omega_n$ and $\zeta$ and say whether the system is underdamped, critically damped, overdamped, undamped or unstable: (a) $s^2 + 4s + 20$; (b) $s^2 + 6s + 9$; (c) $s^2 + 5s + 4$; (d) $s^2 + 16$; (e) $s^2 - 2s + 5$.

### Problem 15-03.4 [B]

**Derive and apply.** (a) Starting from $Y(s) = \omega_n^2/[s(s^2 + 2\zeta\omega_ns + \omega_n^2)]$, derive $y(t)$ for $0 < \zeta < 1$. (b) Derive $t_p$ and $M_p$. (c) For $\zeta$ = 0.3 and $\omega_n$ = 10 rad/s, find the overshoot, the peak time, the settling time by the rule and by the envelope, and the exact settling time.

### Problem 15-03.5 [B]

**Which poles meet the specification?** A loop must have overshoot at most 5%, settling time at most 2 s and rise time at most 0.6 s. (a) Convert each specification into a constraint on $\zeta$, $\sigma$ or $\omega_n$ using the rules. (b) Test the pole pairs A: $-2 \pm j2$, B: $-3 \pm j2$, C: $-1 \pm j1$, D: $-4 \pm j5$ and E: $-4 \pm j3$ against the rules. (c) Check the pairs that pass with their exact responses.

### Problem 15-03.6 [B]

**A position loop.** A motor position loop has $L(s) = K/[s(s + 40)]$ with unity feedback. Choose $K$ for $\zeta$ = 0.7. Find $\omega_n$, the overshoot, the peak time, the settling time by the rule, and the exact settling time.

### Problem 15-03.7 [B]

**Settling an ADC input.** A sensor channel driving an ADC behaves as a first-order system. (a) It must settle to 0.1% within 10 µs. Find the largest allowed time constant and the smallest bandwidth. (b) Repeat for settling to half an LSB of a 16-bit converter.

### Problem 15-03.8 [B]

**Is critical damping best?** Compare $\zeta$ = 1 and $\zeta = 1/\sqrt2$ at $\omega_n$ = 100 rad/s: overshoot, exact rise time and exact settling time. Which settles first, and why?

### Problem 15-03.9 [B]

**Dominant poles.** $T(s) = 100/[(s + 10)(s^2 + 2s + 10)]$. (a) Identify the dominant poles and write a second-order approximation with the same DC gain. (b) Compare the overshoot, peak time and settling time of the approximation with the exact response.

### Problem 15-03.10 [C]

**Tuning a zero.** $T(s) = 4(1 + s/z)/(s^2 + 2s + 4)$. (a) Find the overshoot and rise time for $z$ = 3 and compare with the zero-free response. (b) Find the zero location that gives exactly 25% overshoot.

### Problem 15-03.11 [C]

**A right-half-plane zero.** $T(s) = 4(1 - s/z)/(s^2 + 2s + 4)$ models a converter's control-to-output response. (a) Find the initial slope for $z$ = 8 and $z$ = 1. (b) Find the undershoot and its time for each. (c) Why does a right-half-plane zero limit how fast any controller can make the loop?

### Problem 15-03.12 [C]

**Checking a datasheet's settling time.** The TO-99 version of TI's OPA627 is specified (datasheet SBOS165C, Jan 2025) with 16 MHz gain-bandwidth, 55 V/µs slew rate, and a settling time of 550 ns to 0.01% for a 10 V step at a gain of −1. Model the closed loop as a single pole at $\beta \cdot$GBW, with $\beta$ = 0.5 at a gain of −1. (a) Estimate the settling time as full-step slewing plus linear settling. (b) Refine it with the slewing-to-linear transition at $V_L = \mathrm{SR}\cdot\tau$ (§3.7). (c) Compare both with the specification and explain the difference.

### Problem 15-03.13 [C]

**How well must a doublet match?** In Example 15-03.6 ($\omega_c$ = 2π × 100 MHz, doublet pole at 1 MHz), let the zero sit a fraction $\delta$ above the pole, $z = p(1 + \delta)$. (a) Find the 0.1% settling time for $\delta$ = 0.05, 0.01 and 0.002. (b) Find the largest $\delta$ for which the response settles to 0.1% within 50 ns.

### Problem 15-03.14 [B]

**Identifying a model.** A unit step applied to a system produces a response that peaks at 2.4 at 0.5 s and settles at 2. Assuming a standard second-order system with DC gain $K$, find $K$, $\zeta$, $\omega_n$ and the transfer function.

---

## Objective coverage

| Learning objective (chapter 15-03) | Problems |
|---|---|
| 1. First-order rise time, settling, bandwidth and bits | 1, 7 |
| 2. Derive the second-order response, peak time and overshoot | 2, 3, 4, 14 |
| 3. Specifications as s-plane regions; choosing a gain | 5, 6, 8 |
| 4. Dominant poles, extra poles, zeros and doublets | 9, 10, 11, 13 |
| 5. Slewing against linear settling | 12 |
