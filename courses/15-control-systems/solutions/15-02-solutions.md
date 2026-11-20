# Solutions 15-02 · Transfer Functions and Block Diagrams

Problems: [15-02 problems](../problems/15-02-problems.md) · Chapter: [15-02](../chapters/15-02-transfer-functions-and-block-diagrams.md)

Every number below is recomputed by [verify_15_02.py](../verify/verify_15_02.py): by sympy algebra on the block diagrams, by a linear solve of each signal-flow graph's node equations, by eigenvalues of the state matrices, and by simulated step responses.

---

## Solutions

### Solution 15-02.1

Transforming with zero initial conditions, $(s^2 + 7s + 10)Y = 5U$, so

$$
G(s) = \frac{5}{s^2 + 7s + 10} = \frac{5}{(s + 2)(s + 5)} .
$$

The poles are **−2** and **−5** s⁻¹ (both decaying modes), there are no finite zeros, the DC gain is 5/10 = **0.5**, and the relative degree is 2 − 0 = **2**, so the gain falls as $1/\omega^2$ at high frequency.

**Check.** A constant input $u = 1$ gives $10y = 5$ in steady state: $y$ = 0.5.

### Solution 15-02.2

**(a) Series.** Multiply:

$$
G_2G_1 = \frac{2}{(s + 1)(s + 3)}, \qquad \text{DC gain} = \frac{2}{3} = \mathbf{0.667},
$$

with no finite zeros.

**(b) Parallel.** Add over a common denominator:

$$
G_1 + G_2 = \frac{(s + 3) + 2(s + 1)}{(s + 1)(s + 3)} = \frac{3s + 5}{(s + 1)(s + 3)} .
$$

The DC gain is 5/3 = **1.667** (the sum of the two DC gains, 1 + 0.667), and there is a zero at $s = -5/3$ = **−1.667**. Neither block has a zero; the zero appears because the two paths' outputs cancel at that complex frequency: $G_1(-5/3) = -1.5$ and $G_2(-5/3) = +1.5$. Parallel paths create zeros, which is why feedforward paths and capacitive coupling in amplifiers (12-03) introduce zeros.

### Solution 15-02.3

**(a) Negative feedback:** $G/(1 + GH)$ = 4/(1 + 0.8) = **2.222**.

**(b) Positive feedback:** $G/(1 - GH)$ = 4/(1 − 0.8) = **20**.

**(c)** The gain is infinite when $GH = 1$, that is, at $H$ = 1/4 = **0.25**. A finite output then exists with zero input: the loop sustains its own signal. In a real circuit, with some delay or bandwidth limit in the loop, any noise grows until something saturates. Positive feedback with loop gain at or above 1 is how latches (08-06), Schmitt triggers (10-10) and oscillators (12-09) work, and why it must be avoided in an amplifier.

### Solution 15-02.4

**(a)** $T_1 = G/(1 + G\beta) = 10^5/(1 + 1000)$ = **99.90**. The ideal is $1/\beta$ = 100.

**(b)** $T_2 = 8 \times 10^4/(1 + 800)$ = **99.88**. The exact fractional change is

$$
\frac{T_2}{T_1} - 1 = \frac{8 \times 10^4 \times 1001}{801 \times 10^5} - 1 = \frac{800.8}{801} - 1 = -2.497 \times 10^{-4} = \mathbf{-0.0250}\% .
$$

**(c)** The estimate is $-20\%/1001$ = **−0.0200**%. The estimate is a derivative, valid for small changes. For a finite change the exact result is

$$
\frac{\Delta T}{T_1} = \frac{\Delta G/G_1}{1 + G_2\beta} ,
$$

which uses the new loop gain, 801, rather than the old one, 1001. Either way, a 20% change in the amplifier moves the closed-loop gain by about 0.02%: the desensitivity factor $1 + L$ (12-05) at work.

### Solution 15-02.5

From 15-01.13 the state equations are $L\,di/dt = v_s - Ri - v_C$ and $C\,dv_C/dt = i$, so with $\mathbf{x} = [i,\ v_C]^T$,

$$
A = \begin{bmatrix} -R/L & -1/L \\ 1/C & 0 \end{bmatrix}, \quad B = \begin{bmatrix} 1/L \\ 0 \end{bmatrix}, \quad \det(sI - A) = s^2 + \frac{R}{L}s + \frac{1}{LC} = s^2 + 10^4s + 10^9 .
$$

The adjugate of $sI - A$ is $\begin{bmatrix} s & -1/L \\ 1/C & s + R/L \end{bmatrix}$, and $(sI - A)^{-1}B$ is its first column times $1/L$: $[s/L,\ 1/(LC)]^T$ over the determinant.

**(a)** $C_{out} = [0,\ 1]$ picks the second entry:

$$
\frac{V_C}{V_s} = \frac{1/(LC)}{s^2 + (R/L)s + 1/(LC)} = \frac{10^9}{s^2 + 10^4s + 10^9} .
$$

**(b)** $C_{out} = [1,\ 0]$ picks the first:

$$
\frac{I}{V_s} = \frac{s/L}{s^2 + (R/L)s + 1/(LC)} = \frac{1000\,s}{s^2 + 10^4s + 10^9}\ \text{A/V} .
$$

Both have the poles $-5000 \pm j31{,}225$ s⁻¹, so the real part is **−5000** and the imaginary part **31,225** rad/s. $\omega_n = \sqrt{10^9}$ = **3.162 × 10⁴** rad/s and $\zeta = 10^4/(2 \times 3.162 \times 10^4)$ = **0.158**, as in Problem 15-01.13. The DC gain of (a) is **1** (the capacitor charges to the source voltage); that of (b) is **0**, because the zero at $s$ = 0 means no DC current flows through a capacitor.

**Why.** The poles are the eigenvalues of $A$, a property of the circuit alone. The zeros depend on which signal is called the output ($C_{out}$), so different outputs of the same circuit share poles but not zeros.

### Solution 15-02.6

**(a) Reduction.** The $H_1$ loop picks off between $G_2$ and $G_3$; the $H_2$ loop starts at the output and returns between $G_1$ and $G_2$. The loops overlap on $G_2$, so neither can be closed first as drawn. Move the $H_1$ pickoff from the input of $G_3$ to the output $Y$. The signal there is $Y$ rather than $Y/G_3$, so the branch must become $H_1/G_3$ to carry the same value. Now the $H_2$ loop sits inside the $H_1$ loop. Close the inner loop:

$$
\frac{G_2G_3}{1 + G_2G_3H_2} .
$$

Then close the outer loop, forward path $G_1$ times that, feedback $H_1/G_3$:

$$
\frac{Y}{R} = \frac{G_1G_2G_3/(1 + G_2G_3H_2)}{1 + G_1G_2G_3H_1/[G_3(1 + G_2G_3H_2)]} = \frac{G_1G_2G_3}{1 + G_2G_3H_2 + G_1G_2H_1} .
$$

Substituting $G_2G_3 = 1/[s(s + 1)]$, $G_1G_2H_1 = 2/(s + 1)$ and multiplying through by $s(s + 1)$:

$$
\frac{Y}{R} = \frac{5}{s(s + 1) + 2 + 2s} = \frac{5}{s^2 + 3s + 2} = \frac{5}{(s + 1)(s + 2)} .
$$

**(b) Mason.** One forward path, $P_1 = G_1G_2G_3$. Two loops, $L_1 = -G_1G_2H_1$ and $L_2 = -G_2G_3H_2$; they share $G_2$, so they touch, and the path touches both. Then $\Delta = 1 + G_1G_2H_1 + G_2G_3H_2$ and $\Delta_1 = 1$, giving the same $P_1/\Delta$.

**(c)** The poles are **−1** and **−2**, and the DC gain is 5/2 = **2.5**.

### Solution 15-02.7

**(a)**

$$
T = \frac{L}{1 + L} = \frac{8}{s^2 + 2s + 8}, \qquad \omega_n = \sqrt 8 = \mathbf{2.828}\ \text{rad/s}, \qquad \zeta = \frac{2}{2\sqrt 8} = \mathbf{0.354} .
$$

**(b)** At $\omega$ = 0.5 rad/s: $L(j0.5) = 8/[j0.5(2 + j0.5)] = 8/(-0.25 + j1)$, so $\lvert L\rvert$ = 7.76. Then $S = (-0.25 + j1)/(7.75 + j1)$ and $T = 8/(7.75 + j1)$:

$$
\lvert S\rvert = \frac{1.031}{7.814} = \mathbf{0.132}, \qquad \lvert T\rvert = \frac{8}{7.814} = \mathbf{1.024} .
$$

At $\omega$ = 10 rad/s: $s(s + 2) = -100 + j20$, so $S = (-100 + j20)/(-92 + j20)$ and $T = 8/(-92 + j20)$:

$$
\lvert S\rvert = \frac{102.0}{94.15} = \mathbf{1.083}, \qquad \lvert T\rvert = \frac{8}{94.15} = \mathbf{0.0850} .
$$

**(c)** The magnitudes add to 1.156 at 0.5 rad/s and 1.168 at 10 rad/s, not 1. The identity $S + T = 1$ holds for the complex values: at 0.5 rad/s, $S$ and $T$ point in different directions in the complex plane, and their vector sum is exactly 1. Two points worth noting: $\lvert T\rvert$ slightly exceeds 1 at low frequency (the resonant peak of an underdamped loop begins), and $\lvert S\rvert$ exceeds 1 at 10 rad/s, so disturbances there are amplified, not rejected. Feedback cannot attenuate disturbances at all frequencies (15-07).

### Solution 15-02.8

With $\tau_m = RJ/K^2 = 10^{-5}/(4 \times 10^{-4})$ = 25 ms and $V = K_p(\Omega_{ref} - \Omega)$:

$$
(\tau_ms + 1)\Omega = \frac{K_p}{K}(\Omega_{ref} - \Omega) - \frac{R}{K^2}T_L
\;\Longrightarrow\;
\Omega = \frac{(K_p/K)\,\Omega_{ref} - (R/K^2)\,T_L}{\tau_ms + 1 + K_p/K} .
$$

**(a)** The DC loop gain is $K_p/K$ = 0.2/0.02 = **10**.

**(b)** The DC tracking gain is 10/11 = **0.909**: a 1% shortfall would need $L_0$ = 99.

**(c)** $R/K^2$ = 1/(4 × 10⁻⁴) = 2500 rad/s per N·m. Without feedback a 0.01 N·m load slows the motor by 2500 × 0.01 = **25** rad/s. With feedback the droop is divided by $1 + L_0$ = 11: 25/11 = **2.27** rad/s.

**(d)** The closed-loop pole is at $-(1 + K_p/K)/\tau_m$, so the time constant is 25 ms/11 = **2.27** ms.

**Units check.** $K_p/K$: (V·s/rad)/(V·s/rad) is dimensionless, as a loop gain must be.

### Solution 15-02.9

**Paths and loops.** $P_1 = 1 \cdot G_1G_2$ = 4 (nodes $R, x_1, x_2, Y$) and $P_2 = 1 \cdot G_3G_4$ = 20 (nodes $R, x_3, x_4, Y$). Loops: $L_1 = -G_1H_1$ = −2 on $x_1, x_2$, and $L_2 = -G_3H_2$ = −1 on $x_3, x_4$. The loops share no node.

$$
\Delta = 1 - (L_1 + L_2) + L_1L_2 = 1 + 3 + 2 = \mathbf{6} .
$$

Path 1 does not touch $L_2$, so $\Delta_1 = 1 - L_2$ = **2**. Path 2 does not touch $L_1$, so $\Delta_2 = 1 - L_1$ = **3**. Then

$$
\frac{Y}{R} = \frac{P_1\Delta_1 + P_2\Delta_2}{\Delta} = \frac{8 + 60}{6} = \mathbf{11.33} .
$$

**Check.** Each channel is a block with its own feedback: $4/(1 + 2) = 1.333$ and $20/(1 + 1) = 10$, which add to 11.33. Here $\Delta = (1 + G_1H_1)(1 + G_3H_2)$ factors, because the loops are independent.

### Solution 15-02.10

**Mason.** Nodes: $R$, the junction $e$, the output of $G_2$ (call it $x$), and $Y$. Branches: $R \to e$ ($G_1$), $e \to x$ ($G_2$), $x \to e$ ($-H$), $x \to Y$ (1), $R \to Y$ ($G_3$). One loop, $L_1 = -G_2H$ on nodes $e, x$. Path 1 is $G_1G_2$ through $e, x$ and touches it ($\Delta_1$ = 1). Path 2 is $G_3$, through nodes $R$ and $Y$ only, which does not touch it ($\Delta_2 = 1 + G_2H$). So

$$
\frac{Y}{R} = \frac{G_1G_2 + G_3(1 + G_2H)}{1 + G_2H} = \frac{G_1G_2}{1 + G_2H} + G_3 ,
$$

which is the block-algebra result (closed loop plus a parallel feedforward). With numbers:

$$
\frac{Y}{R} = \frac{2}{s + 4} + \frac12 = \frac{0.5s + 4}{s + 4} = \frac{s + 8}{2(s + 4)} .
$$

The pole is **−4**, the zero **−8**, the DC gain 4/4 = **1** and the high-frequency gain **0.5** (only the feedforward path passes high frequencies).

### Solution 15-02.11

**(a)** $L = CP = \dfrac{s - 1}{s + 2}\cdot\dfrac{1}{s - 1} = \dfrac{1}{s + 2}$ after cancellation, and $T = L/(1 + L) = 1/(s + 3)$. On paper the loop has one pole at −3 and looks stable.

**(b)** The disturbance enters before the plant, not through the controller:

$$
\frac{Y}{D} = \frac{P}{1 + L} = \frac{1}{s - 1}\cdot\frac{s + 2}{s + 3} = \frac{s + 2}{(s - 1)(s + 3)} .
$$

The pole at +1 is still there.

**(c)** For a unit step, $Y = (s + 2)/[s(s - 1)(s + 3)]$. Partial fractions: the residue at $s = 1$ is $3/(1 \times 4) = 3/4$; at 0, $2/[(-1)(3)] = -2/3$; at −3, $(-1)/[(-3)(-4)] = -1/12$. So

$$
y(t) = \frac34e^{t} - \frac23 - \frac{1}{12}e^{-3t}, \qquad y(0) = 0, \qquad y(5\ \text{s}) = \mathbf{110.6} .
$$

The output grows without bound: the closed loop is internally unstable.

**(d)** The cancellation removed the unstable mode from the reference-to-output path only. It is still in the plant, excited by any disturbance, noise or initial condition, and never perfectly cancelled in practice. Never cancel a right-half-plane pole (or zero) with the controller; stabilize the plant by moving its pole with feedback instead (15-05, 15-06). Checking every closed-loop transfer function, $T$, $S$, $PS$ and $CS$, exposes such hidden modes.

### Solution 15-02.12

**(a)** The forward path at DC is $G_0 = A_0g_mR_L$ = 1000 × 0.5 × 10 = 5000, so the DC loop gain is $L_0 = G_0\beta$ = **2500**. The output is

$$
V_{out} = V_{ref}\frac{G_0}{1 + L_0} = 1.2 \times \frac{5000}{2501} = \mathbf{2.3990}\ \text{V},
$$

against the ideal $V_{ref}/\beta$ = 2.4 V: a fractional error of $1/(1 + L_0)$ = **0.0400**%.

**(b)** A load current step $i_L$ drawn from the output: open loop, with the gate drive fixed, the output moves by $i_LR_L$ = 0.1 × 10 = **1.0** V. Closed loop, $V_{out} = -R_Li_L + G\beta(-V_{out})$ at DC, so the output resistance becomes $R_L/(1 + L_0)$ = 10/2501 = **4.00** mΩ and the change is 0.1 × 0.004 = **0.400** mV.

**(c)** The loop gain is $L(s) = L_0/[(1 + s/\omega_a)(1 + s/\omega_L)]$ with $\omega_L = 1/(R_LC_L)$ = 10⁵ rad/s. Setting $1 + L = 0$ and multiplying out:

$$
s^2 + (\omega_a + \omega_L)s + (1 + L_0)\omega_a\omega_L = 0 ,
$$

with $\omega_a$ = 6.283 × 10⁴ rad/s. So $\omega_n = \sqrt{2501 \times 6.283 \times 10^4 \times 10^5}$ = **3.964 × 10⁶** rad/s, which is **631** kHz; $\zeta = (\omega_a + \omega_L)/(2\omega_n) = 1.628 \times 10^5/(7.928 \times 10^6)$ = **0.0205**. The poles are $-8.14 \times 10^4 \pm j3.963 \times 10^6$ s⁻¹. The step overshoot, $e^{-\pi\zeta/\sqrt{1-\zeta^2}}$, is **93.75**%.

**(d)** The DC numbers look excellent, but the loop barely damps itself: a load step would ring at about 630 kHz for many cycles. Two poles at low frequency and a large loop gain push the closed-loop poles toward the imaginary axis. The fix is compensation, such as a dominant pole far below the others or a zero from the output capacitor's ESR, chosen with the frequency-domain tools of 15-07 and the regulator models of 15-12. DC accuracy and dynamic stability must be checked separately.

### Solution 15-02.13

**(a)**

$$
\omega_n = \sqrt{\frac{I_{cp}K_v}{2\pi NC}} = \sqrt{\frac{2 \times 10^{-4} \times 2\pi \times 5 \times 10^7}{2\pi \times 50 \times 4 \times 10^{-9}}} = \sqrt{5 \times 10^{10}} = \mathbf{2.236 \times 10^5}\ \text{rad/s},
$$

so $f_n = \omega_n/2\pi$ = **35.6** kHz.

**(b)** From $\zeta = RC\omega_n/2$: $R = 2\zeta/(C\omega_n) = \sqrt 2/(4 \times 10^{-9} \times 2.236 \times 10^5)$ = **1581** Ω.

**(c)** The closed-loop transfer function $\omega_n^2(1 + sRC)/(s^2 + 2\zeta\omega_ns + \omega_n^2)$ has its zero at $s = -1/(RC) = -\omega_n/(2\zeta)$ = **−1.581 × 10⁵** s⁻¹, below $\omega_n$ in magnitude.

**(d)** Simulating the step response of $T(s)$ gives a peak of 1.208, an overshoot of **20.8**%, at **9.93** µs. A second-order system with $\zeta$ = 0.707 and no zero overshoots by 4.3%. The zero adds a term proportional to the derivative of the zero-free response, which pushes the early response up. This is why PLL designers quote phase margin rather than reading overshoot from $\zeta$ alone (15-07, 15-12).

### Solution 15-02.14

**(a)** $L = 2K_I/[s(s + 4)]$, so

$$
T = \frac{2K_I}{s^2 + 4s + 2K_I} .
$$

**(b)** Matching $2\zeta\omega_n = 4$ with $\zeta = 1/\sqrt2$: $\omega_n = 4/\sqrt2$ = **2.828** rad/s, and $2K_I = \omega_n^2$ = 8, so $K_I$ = **4** s⁻¹.

**(c)** $T(0) = 2K_I/(2K_I) = 1$, so the steady-state error to a step is **0**. In Example 15-02.4 the proportional loop always left an error of $1/(1 + K)$. The integrator has infinite gain at DC, so $S(0) = 0$: integral action removes steady-state error (15-04, 15-08).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-02.1a | first pole | −2 | 1/s |
| 15-02.1b | second pole | −5 | 1/s |
| 15-02.1c | DC gain | 0.5 | — |
| 15-02.1d | relative degree | 2 | — |
| 15-02.2a | series DC gain | 0.667 | — |
| 15-02.2b | parallel DC gain | 1.667 | — |
| 15-02.2c | parallel zero | −1.667 | 1/s |
| 15-02.3a | negative-feedback gain | 2.222 | — |
| 15-02.3b | positive-feedback gain | 20 | — |
| 15-02.3c | H for infinite gain | 0.25 | — |
| 15-02.4a | closed-loop gain | 99.90 | — |
| 15-02.4b | gain after the drop | 99.88 | — |
| 15-02.4c | exact fractional change | −0.0250 | % |
| 15-02.4d | estimated fractional change | −0.0200 | % |
| 15-02.5a | pole real part | −5000 | 1/s |
| 15-02.5b | pole imaginary part | 31225 | rad/s |
| 15-02.5c | natural frequency | 3.162e4 | rad/s |
| 15-02.5d | damping ratio | 0.158 | — |
| 15-02.5e | DC gain of V_C/V_s | 1 | — |
| 15-02.5f | DC gain of I/V_s | 0 | A/V |
| 15-02.6a | first pole | −1 | 1/s |
| 15-02.6b | second pole | −2 | 1/s |
| 15-02.6c | DC gain | 2.5 | — |
| 15-02.7a | natural frequency | 2.828 | rad/s |
| 15-02.7b | damping ratio | 0.354 | — |
| 15-02.7c | abs S at 0.5 rad/s | 0.132 | — |
| 15-02.7d | abs T at 0.5 rad/s | 1.024 | — |
| 15-02.7e | abs S at 10 rad/s | 1.083 | — |
| 15-02.7f | abs T at 10 rad/s | 0.0850 | — |
| 15-02.7g | sum of magnitudes at 0.5 rad/s | 1.156 | — |
| 15-02.7h | sum of magnitudes at 10 rad/s | 1.168 | — |
| 15-02.8a | DC loop gain | 10 | — |
| 15-02.8b | DC tracking gain | 0.909 | — |
| 15-02.8c | droop without feedback | 25 | rad/s |
| 15-02.8d | droop with feedback | 2.27 | rad/s |
| 15-02.8e | closed-loop time constant | 2.27 | ms |
| 15-02.9a | Δ | 6 | — |
| 15-02.9b | Δ₁ | 2 | — |
| 15-02.9c | Δ₂ | 3 | — |
| 15-02.9d | Y/R | 11.33 | — |
| 15-02.10a | pole | −4 | 1/s |
| 15-02.10b | zero | −8 | 1/s |
| 15-02.10c | DC gain | 1 | — |
| 15-02.10d | high-frequency gain | 0.5 | — |
| 15-02.11a | closed-loop pole of T | −3 | 1/s |
| 15-02.11b | y at 5 s | 110.6 | — |
| 15-02.12a | DC loop gain | 2500 | — |
| 15-02.12b | output voltage | 2.3990 | V |
| 15-02.12c | fractional error | 0.0400 | % |
| 15-02.12d | open-loop output change | 1.0 | V |
| 15-02.12e | closed-loop output resistance | 4.00 | mΩ |
| 15-02.12f | closed-loop output change | 0.400 | mV |
| 15-02.12g | natural frequency | 3.964e6 | rad/s |
| 15-02.12h | natural frequency | 631 | kHz |
| 15-02.12i | damping ratio | 0.0205 | — |
| 15-02.12j | overshoot | 93.75 | % |
| 15-02.13a | natural frequency | 2.236e5 | rad/s |
| 15-02.13b | natural frequency | 35.6 | kHz |
| 15-02.13c | loop-filter resistor | 1581 | Ω |
| 15-02.13d | closed-loop zero | −1.581e5 | 1/s |
| 15-02.13e | overshoot | 20.8 | % |
| 15-02.13f | time of the peak | 9.93 | µs |
| 15-02.14a | natural frequency | 2.828 | rad/s |
| 15-02.14b | integral gain | 4 | 1/s |
| 15-02.14c | steady-state step error | 0 | — |
