# Problems 15-09 · Lead and Lag Compensation

Chapter: [15-09](../chapters/15-09-lead-lag-compensation.md) · Worked solutions: [15-09 solutions](../solutions/15-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Lead $C = (1 + \alpha Ts)/(1 + Ts)$ and lag $C = (1 + s/z)/(1 + s/p)$, both with unity DC gain; the static gain $K$ is set separately. Use the recipes of §3.3 (10° extra lead) and §3.4 (5° allowance, zero a decade below crossover) unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-09.1 [A]

**How much α?** Find the lead ratio $\alpha$ that gives a maximum phase of 30°, 45° and 60°.

### Problem 15-09.2 [A]

**The cost of a lag.** A lag with $\beta$ = 10 has its zero a factor $f$ below the crossover frequency. Find its phase at crossover for $f$ = 10 and $f$ = 5.

### Problem 15-09.3 [A]

**Building a lead.** Choose $R_1$ and $C_1$ for a passive lead network with $\alpha$ = 4, maximum phase at 1000 rad/s, and $R_2$ = 10 kΩ.

### Problem 15-09.4 [B]

**Lead design.** $P = 1/[s(s + 2)]$ must have $K_v$ = 20 s⁻¹ and at least 50° of phase margin. Find $K$, the uncompensated margin, and design a lead. Give $\alpha$, the zero, the pole, the new crossover, the phase margin, the overshoot and the settling time.

### Problem 15-09.5 [B]

**Lag design.** Meet Problem 15-09.4's specification with a lag instead. Give $\beta$, the zero, the pole, the new crossover, the phase margin, the overshoot and the settling time, and compare with the lead.

### Problem 15-09.6 [B]

**Root-locus lead.** For $P = 1/[s(s + 2)]$, place the dominant closed-loop poles at $-3 \pm j4$ with a lead whose zero is at −3. Find the angle deficiency, the lead pole, the gain, the third closed-loop pole and $K_v$.

### Problem 15-09.7 [B]

**Adding a lag for accuracy.** Example 15-06.1's servo, $L = 8/[s(s + 4)]$, has $K_v$ = 2 s⁻¹ and a 65.5° phase margin. Add a lag with $\beta$ = 10 and its zero a decade below crossover. Find the zero and pole, the new $K_v$ and the new phase margin.

### Problem 15-09.8 [C]

**Two stages of lead.** $L = K/[s(s + 1)(s + 5)]$ needs $K_v$ = 10 s⁻¹. (a) Show that the uncompensated loop is unstable. (b) Design two identical lead stages, each with ratio $\alpha$ and its peak at the new crossover where the uncompensated gain is $1/\alpha$, for a 45° phase margin. Give $\alpha$, each stage's phase, the zero and pole, the crossover and the gain margin.

### Problem 15-09.9 [C]

**Capacitor derating.** In Example 15-09.6's buck converter with zeros at $f_0/2$, the 100 µF output capacitor loses 30% of its value under DC bias, to 70 µF, while the compensator stays the same. Find the new $f_0$ and $Q$, the new crossover, phase margin and gain margin.

### Problem 15-09.10 [A]

**Noise penalty.** By how many dB does Example 15-09.2's lead raise the loop's high-frequency gain, and what does that mean for sensor noise?

---

## Objective coverage

| Learning objective (chapter 15-09) | Problems |
|---|---|
| 1. Lead and lag anatomy | 1, 2, 10 |
| 2. Bode-plot design | 4, 5, 7, 8 |
| 3. Root-locus design | 6 |
| 4. Lead–lag trades | 5, 7 |
| 5. Realization and converter compensation | 3, 9 |
