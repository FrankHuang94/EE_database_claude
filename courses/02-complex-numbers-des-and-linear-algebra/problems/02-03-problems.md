# Problems 02-03 · Second-Order Linear ODEs and the Characteristic Equation

Chapter: [02-03](../chapters/02-03-second-order-linear-odes.md) · Worked solutions: [02-03 solutions](../solutions/02-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** answers to 4 significant figures unless stated; passive sign convention; $\omega_0$, α, ζ and $Q$ as in [reference/notation.md](../../../reference/notation.md). Check every solution against both initial conditions.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-03.1 [A]

**Standard form.** Find α, $\omega_0$ and ζ, and classify each system:

(a) a series RLC with $R = 50$ Ω, $L = 10$ mH and $C = 1$ µF;
(b) a parallel RLC with $R = 1$ kΩ, $L = 10$ mH and $C = 1$ µF;
(c) a mass of 0.2 kg on a spring of stiffness 80 N/m with damping 2 N·s/m.

### Problem 02-03.2 [A]

**Characteristic roots.** Find the roots, classify the damping and write the general real solution:

(a) $y'' + 5y' + 6y = 0$; (b) $y'' + 4y' + 4y = 0$; (c) $y'' + 2y' + 10y = 0$.

### Problem 02-03.3 [A]

Solve $y'' + 5y' + 6y = 0$ with $y(0) = 1$ and $y'(0) = 0$, and evaluate $y(1)$.

### Problem 02-03.4 [B]

**The slow root of a heavily damped system.** Show that for $\zeta \gg 1$ the root closer to zero is $s_1 \approx -\omega_0/(2\zeta)$. (Hint: write $\sqrt{\zeta^2 - 1} = \zeta\sqrt{1 - 1/\zeta^2}$ and use a first-order Taylor approximation.) Evaluate the exact and approximate $s_1/\omega_0$ for ζ = 5, and the relative error.

### Problem 02-03.5 [B]

Solve $y'' + 4y' + 4y = 0$ with $y(0) = 2$ and $y'(0) = -1$. Evaluate $y(1)$. Does $y$ ever cross zero for $t > 0$?

### Problem 02-03.6 [B]

**Critically damped step response.** For $y'' + 2\omega_0y' + \omega_0^2y = \omega_0^2X$ with $y(0) = y'(0) = 0$:

(a) Derive $y(t) = X\big[1 - (1 + \omega_0t)e^{-\omega_0t}\big]$.
(b) For $\omega_0 = 10^4$ rad/s, find the time to reach 90% of the final value.

### Problem 02-03.7 [B]

**Peak time and overshoot.** For the underdamped step response of chapter §3.8:

(a) Show that $y'(t) = X\dfrac{\omega_0^2}{\omega_d}e^{-\alpha t}\sin\omega_dt$, and hence that the first peak is at $t_p = \pi/\omega_d$.
(b) For ζ = 0.3 and $\omega_0 = 1000$ rad/s, find $\omega_d$, $t_p$ and the overshoot.

### Problem 02-03.8 [B]

**Energy transfer from L to C.** A series RLC has $L = 1$ mH, $C = 10$ µF and $R = 2$ Ω. At $t = 0$ the capacitor is uncharged and the inductor carries 1 A (flowing into the capacitor's positive terminal).

(a) Find α, $\omega_0$, $\omega_d$, and the initial conditions $v_C(0)$ and $v_C'(0)$.
(b) Find $v_C(t)$.
(c) Find the time and value of the first peak of $v_C$, and the fraction of the inductor's initial energy then stored in the capacitor.

### Problem 02-03.9 [B]

**A parallel RLC.** A parallel RLC has $R = 200$ Ω, $L = 10$ mH and $C = 1$ µF, with $v(0) = 10$ V and $i_L(0) = 0$.

(a) Find α, $\omega_0$, ζ and $\omega_d$.
(b) Find $v'(0)$ from KCL.
(c) Find $v(t)$.

### Problem 02-03.10 [B]

**Wronskians.** Compute the Wronskian of each pair and show that it is never zero:

(a) $e^{s_1t}$ and $e^{s_2t}$ with $s_1 \ne s_2$; (b) $e^{-\alpha t}$ and $te^{-\alpha t}$; (c) $e^{-\alpha t}\cos\omega_dt$ and $e^{-\alpha t}\sin\omega_dt$. Evaluate (c) at $t = 0$ for α = 1 and $\omega_d = 3$.

### Problem 02-03.11 [B]

**From a scope trace to a model.** A PLL's frequency step response overshoots by 10%, with its first peak 50 µs after the step. Find ζ, $\omega_d$, $\omega_0$ and $Q$.

### Problem 02-03.12 [B]

**Q and ring-down.** A series RLC has $L = 100$ µH, $C = 100$ nF and $R = 0.5$ Ω.

(a) Find $\omega_0$ and $Q$.
(b) How many cycles does the amplitude take to fall by a factor $e$?
(c) What fraction of the stored energy is lost per cycle, exactly? Compare with the light-damping estimate $2\pi/Q$.

### Problem 02-03.13 [C]

**Bond-wire ringing.** A 2 nH bond wire connects a driver with 10 Ω output resistance to a pad with 2 pF of pad and ESD capacitance (illustrative values).

(a) Find $\omega_0$, $f_0$ and ζ.
(b) For a fast step from the driver, find the overshoot at the pad.
(c) What driver resistance gives ζ = 0.7, and what overshoot then? What does the higher resistance cost?

### Problem 02-03.14 [C]

**A power-delivery budget.** A 0.8 V rail must stay within ±5% during a 50 A load step. The die has 1 µF of decoupling capacitance and the effective package loop inductance is 5 pH (illustrative values).

(a) Find the target impedance and the characteristic impedance $\sqrt{L/C}$. Does the design meet the target?
(b) Estimate the first droop, and its percentage of the rail. At what frequency does the network resonate?
(c) Keeping $L$, how much capacitance would meet the target? Keeping $C$, how small must $L$ be?

### Problem 02-03.15 [C]

**Negative resistance and oscillation.** An active circuit presents a resistance of −2 Ω in series with $L = 1$ mH and $C = 10$ µF.

(a) Find the characteristic roots. Where do they lie in the complex plane?
(b) Find the oscillation frequency in hertz and the time constant of the growing envelope.
(c) How long, and how many cycles, does a small disturbance take to grow 1000-fold?
(d) What net resistance gives a steady oscillation? Explain why a real oscillator's amplitude stops growing.

---

## Objective coverage

| Learning objective (chapter 02-03) | Problems |
|---|---|
| 1. Standard form; α, $\omega_0$, ζ, $Q$ | 1, 12, 13 |
| 2. Characteristic equation; three cases; repeated root | 2, 3, 4, 5 |
| 3. Initial conditions from circuit states; natural response | 3, 5, 8, 9 |
| 4. Step-response specifications; inferring ζ and $\omega_0$ | 6, 7, 11, 13 |
| 5. Roots in the complex plane; stability; Wronskian; energy | 8, 10, 12, 15 |
| 6. Ringing and droop in real systems | 13, 14 |
