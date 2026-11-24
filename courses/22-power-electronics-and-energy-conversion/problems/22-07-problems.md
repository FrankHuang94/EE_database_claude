# Problems 22-07 · Converter Dynamics and Control

Chapter: [22-07](../chapters/22-07-converter-dynamics-and-control.md) · Worked solutions: [22-07 solutions](../solutions/22-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Ideal, lossless converters in continuous conduction; averaged small-signal models. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-07-lab/control.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-07.1 [A]

**A 48 V buck's plant.** A buck from 48 V has $L$ = 10 µH, $C$ = 100 µF and a 1.2 Ω load. Find (a) $f_0$, (b) $Q$ and (c) the low-frequency control-to-output gain in dB.

### Problem 22-07.2 [A]

**The output impedance at resonance.** Show that the buck's open-loop output impedance at $\omega_0$ equals the load resistance $R$, and evaluate it for Problem 22-07.1.

### Problem 22-07.3 [B]

**A high-ratio boost.** A boost converts 12 V to 48 V with $L$ = 22 µH. Find the right-half-plane zero at (a) 1 A and (b) 5 A of output current, and (c) the crossover limit at 5 A if the crossover must stay below a fifth of it.

### Problem 22-07.4 [A]

**The k-factor.** A voltage-mode loop needs a 45° phase margin; the plant phase at the chosen crossover is −170°. Find (a) the type-III boost needed and (b) $k$.

### Problem 22-07.5 [B]

**Type II for a current-mode buck.** *(lab)* With ideal current-mode control, Example 22-07.1's buck has the plant $(R/R_i)/(1 + sRC)$ with $R$ = 0.12 Ω and $C$ = 62.5 µF. For a 60 kHz crossover and 60° phase margin with a type-II compensator ($\omega_I/s$ times one zero and one pole placed a factor $k$ either side of $f_c$), find (a) the plant pole, (b) the plant phase at 60 kHz, (c) the required boost, (d) $k$, and the (e) zero and (f) pole frequencies.

### Problem 22-07.6 [B]

**Slope compensation for a boost.** *(lab)* In a peak current-mode boost the inductor current rises at $m_1 = V_g/L$ and falls at $m_2 = (V - V_g)/L$. For 12 V to 48 V with $L$ = 22 µH, find (a) $m_1$, (b) $m_2$, (c) the perturbation ratio without compensation, (d) the minimum $m_a$ for stability and (e) $\alpha$ with $m_a = m_2/2$.

### Problem 22-07.7 [A]

**Capacitance for a processor rail.** A 0.8 V rail sees a 100 A step and may droop 30 mV. With a 200 kHz crossover, estimate the output capacitance needed.

### Problem 22-07.8 [B]

**Digital delay budget.** A digital controller at 1 MHz has 1 µs of loop delay. Find (a) the crossover at which the delay costs 30°, and (b) the phase margin left at 100 kHz if the analog design had 60°.

### Problem 22-07.9 [B]

**Rejecting input ripple.** A buck at $D$ = 0.25 has a loop-gain magnitude of 300 at 100 Hz, well below $f_0$. Estimate the closed-loop line-to-output gain at 100 Hz (a) as a ratio and (b) in dB.

### Problem 22-07.10 [C]

**The buck-boost's RHP zero.** (a) Derive the inverting buck-boost's control-to-output transfer function from its averaged equations, $L\,d\langle i_L\rangle/dt = d\,v_g + (1 - d)\langle v\rangle$ and $C\,d\langle v\rangle/dt = -(1 - d)\langle i_L\rangle - \langle v\rangle/R$ (with $v < 0$), and show that its RHP zero is at $\omega_z = D'^2R/(DL)$. (b) Evaluate it for 12 V to −12 V with $L$ = 10 µH and $R$ = 6 Ω, and (c) find the magnitude of the low-frequency gain $|V_g/D'^2|$.

### Problem 22-07.11 [C]

**Component values.** *(lab)* Realize a type-III compensator with $k$ = 4, $f_c$ = 50 kHz and $\omega_I$ = 5000 rad/s using $R_1$ = 20 kΩ. Find (a) $C_1 + C_2$, (b) $C_1$, (c) $C_2$, (d) $R_2$, (e) $R_3$ and (f) $C_3$.

### Problem 22-07.12 [C]

**When the droop estimate fails.** Take Problem 22-07.1's buck with a loop gain $T(s) = \omega_c/s$, $f_c$ = 20 kHz (an integrator crossing at 20 kHz). Compute (a) $|Z_{out}|$ open loop at 20 kHz, (b) the closed-loop $|Z_{out}/(1 + T)|$ at 20 kHz, (c) the estimate $1/(2\pi f_cC)$, and (d) the peak of the closed-loop output impedance and (e) the frequency where it occurs. What does this say about the estimate?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Averaging and linearization | 1, 10 |
| 2. Buck and boost transfer functions, RHP zero, output impedance | 1, 2, 3, 10, 12 |
| 3. Compensator design and realization | 4, 5, 11 |
| 4. Current mode and slope compensation | 5, 6 |
| 5. Load transients, line rejection and digital delay | 7, 8, 9, 12 |
