# Solutions 15-04 · Feedback Properties and Steady-State Error

Problems: [15-04 problems](../problems/15-04-problems.md) · Chapter: [15-04](../chapters/15-04-feedback-and-steady-state-error.md)

Every number below is recomputed by [verify_15_04.py](../verify/verify_15_04.py): limits by sympy, steady-state and peak errors by simulating the closed loops (lsim and solve_ivp), and stability from the closed-loop roots.

---

## Solutions

### Solution 15-04.1

$L = GH$ = 100, so $T = 2000/101$ = **19.80** and $S_G^T = 1/101$ = **0.00990**. If $G$ halves to 1000, $T = 1000/51$ = 19.61, a change of

$$
\frac{1000/51}{2000/101} - 1 = \frac{-0.5}{1 + 50} = \mathbf{-0.980}\% .
$$

A 50% loss of forward gain costs under 1% of closed-loop gain. The exact formula uses the new loop gain, 50.

### Solution 15-04.2

**(a)** Closed loop: $(s + 2)(s + 5) + 50 = s^2 + 7s + 60$, stable. Type **0**; $K_p = 50/10$ = **5**, $K_v = K_a = 0$. Errors: step $1/(1 + 5)$ = **0.167**; ramp and parabola ∞.

**(b)** Closed loop $s^2 + 4s + 10$, stable. Type **1**; $K_p = \infty$, $K_v = 10/4$ = **2.5** s⁻¹, $K_a$ = 0. Errors: step 0, ramp $1/2.5$ = **0.4**, parabola ∞.

**(c)** Closed loop $s^2(s + 5) + 4(s + 1) = s^3 + 5s^2 + 4s + 4$. All coefficients are positive and $5 \times 4 > 1 \times 4$, so it is stable (the Routh test of 15-05; the roots are −4.28 and −0.36 ± j0.90). Type **2**; $K_a = 4 \times 1/5$ = **0.8** s⁻². Errors: step 0, ramp 0, parabola $1/0.8$ = **1.25**.

### Solution 15-04.3

**(a)** An output disturbance reaches the output through $S$: $S(0) = 1/(1 + 99)$ = **0.01**, so 1% remains.

**(b)** A sensor offset $n$ reaches the output through $-T$: $T(0) = 99/100$ = **0.99**, so 99% of the offset appears (with opposite sign) in the true output.

The loop corrects anything that makes the *measurement* differ from the reference. A real disturbance changes the measurement, so it is corrected. A sensor offset is part of the measurement, so the loop faithfully moves the true output to cancel it.

### Solution 15-04.4

**(a)** $K_p = K/3$, and the step error $1/(1 + K/3) \le 0.02$ requires $K/3 \ge 49$: $K$ = **147**.

**(b)** The closed loop is $K/(s^2 + 4s + 3 + K) = 147/(s^2 + 4s + 150)$, so $\omega_n$ = 12.25 rad/s and $\zeta = 4/(2 \times 12.25)$ = **0.163**, an overshoot of **59.5**%.

**(c)** For this plant, accuracy and damping pull the same knob in opposite directions: raising $K$ to cut the error moves the poles up the vertical line at $\sigma$ = −2 and lowers $\zeta$. Integral action (zero error at any $K$) or a lag compensator (raising $K_p$ only at low frequency) breaks the conflict (15-08, 15-09).

### Solution 15-04.5

$K_v = K/10$ and the ramp error is $10/K$ = 0.05, so $K$ = **200** s⁻². The closed loop is $s^2 + 10s + 200$: $\zeta = 10/(2\sqrt{200})$ = **0.354**, an overshoot of **30.5**%. The same conflict as Problem 15-04.4 appears: the gain that gives the accuracy also lowers the damping.

### Solution 15-04.6

**(a)** Open loop, the 20 W step raises the temperature by $P(0) \times 20$ = 0.5 × 20 = **10** K.

**(b)** With $C$ = 20 W/K, $L(0) = 20 \times 0.5$ = 10, so the rise is $\dfrac{P(0)}{1 + L(0)} \times 20 = \dfrac{10}{11}$ = **0.909** K.

**(c)** An integrator in the controller, for example PI control, makes $C(0)$ infinite and the steady rise **0**. The integrator sits between the error and the disturbance's entry point, as §3.4 requires.

### Solution 15-04.7

$T = G/(1 + GH) = 10/(s + 1 + 5) = 10/(s + 6)$. For a 1 V step the output settles at $T(0)$ = **1.667**. The desired output is $r/H(0)$ = **2**, so the error is 2 − 1.667 = **0.333**, or 16.7% of the desired value. Equivalently, $L(0) = G(0)H(0)$ = 5 and the fractional error is $1/(1 + 5)$.

### Solution 15-04.8

The satellite is a ramp of slope 0.5°/s, so the lag is $0.5/K_v$ = 0.5/20 = **0.025**°. A type-2 loop would have $K_v = \infty$ and track a constant angular rate with zero steady lag; it would still lag a changing rate (a parabola) by (angular acceleration)/$K_a$.

### Solution 15-04.9

$L(j\omega) = A_0\beta/(1 + j\omega/\omega_a)$ with $A_0\beta = 5 \times 10^4$ and $\omega/\omega_a$ = 1000. So $\lvert L\rvert$ = **50.0** and $\lvert S\rvert$ = **0.0200**. The closed-loop gain's magnitude is off by only **−0.0220**%, while its phase is **−1.15**°. Again (Example 15-04.6), the 2% complex error is almost all phase.

### Solution 15-04.10

**(a)** With $C$ = 100, $L = 100/(s + 10)$ and $S = (s + 10)/(s + 110)$. At $\omega_0$ = 377 rad/s, $\lvert S\rvert = \sqrt{377^2 + 10^2}/\sqrt{377^2 + 110^2}$ = **0.960**: only 4% of the hum is removed, because the loop gain at 60 Hz is only about 0.27.

**(b)** With the resonant term, $C = [100(s^2 + \omega_0^2) + K_rs]/(s^2 + \omega_0^2)$, and the characteristic equation $(s^2 + \omega_0^2)(s + 10) + 100(s^2 + \omega_0^2) + K_rs = 0$ becomes

$$
s^3 + 110s^2 + (\omega_0^2 + K_r)s + 110\omega_0^2 = 0 .
$$

Its roots are −91.7 and **−9.14** ± j412.7 s⁻¹, all in the left half-plane. Simulating, the hum's amplitude in the cycle starting at 0.5 s is **0.0088** (0.88%), and it keeps decaying with time constant 1/9.14 = 109 ms.

**(c)** $S = 1/(1 + L)$ now has zeros at $\pm j\omega_0$, because $L$ has poles there: the loop contains a model of the 60 Hz generator, so the steady response to a 60 Hz disturbance is exactly zero. The convergence rate is set by the slow pole pair. A larger $K_r$ converges faster only up to a point (about $K_r = 3 \times 10^5$ here): beyond it the real pole moves toward the origin and becomes the slow mode (at $K_r = 10^6$ it is at −13.7 s⁻¹), and the loop's dynamics change more.

### Solution 15-04.11

A frequency step is a phase ramp, and the loop is type 2, so the steady phase error is **0**. Simulating the error transfer function $s^2/(s^2 + \omega_n^2RCs + \omega_n^2)$ with a ramp input of slope $\Delta\omega = 2\pi \times 10^5$ rad/s gives a peak phase error of **0.849** rad at **3.40** µs. If the peak exceeds the phase detector's linear range (±2π for a phase–frequency detector, less for others), the linear model breaks down and the loop may cycle-slip, taking much longer to lock. Steady error describes only the end of the story.

### Solution 15-04.12

The characteristic polynomial is $0.025s^2 + (1 + 50K_P)s + 50K_I = 0.025s^2 + 11s + 50K_I$. A root at −50 requires $0.025 \times 2500 - 550 + 50K_I = 0$, so $K_I$ = **9.75** V/rad. The roots' sum is $-11/0.025 = -440$, so the other is **−390** s⁻¹. $K_v = 50K_i$ = **487.5** s⁻¹. Simulating a 0.01 N·m load step: the peak dip is **1.90** rad/s at **6.04** ms (against 2.13 rad/s at 9.10 ms with $K_i$ = 2), and the recovery time constant drops from 108 ms to 20 ms.

### Solution 15-04.13

$L_0 = A_0 \times 0.5 \times 10 \times 0.5 = 2.5A_0$, and the closed-loop output resistance is $R_L/(1 + L_0)$.

- Room temperature, $A_0$ = 1000: $L_0$ = 2500, $R_{out}$ = **4.00** mΩ, and 100 mA changes the output by **0.400** mV.
- Hot, $A_0$ = 300: $L_0$ = 750, $R_{out}$ = **13.3** mΩ, and the change is **1.33** mV.

Load regulation degrades in proportion to the loss of loop gain, which is why regulator data sheets give it over temperature.

### Solution 15-04.14

**(a)** With integral control the loop drives the measurement $Hy$ to $r$ exactly, so $y = 1/0.98$ = **1.0204**: a 2.04% error.

**(b)** With $G$ = 100, $T(0) = 100/(1 + 98)$ = **1.0101**. The finite loop gain's own error (about −1%) partly cancels the sensor's +2%, but only by accident.

**(c)** The loop regulates what it measures. Since $S_H^T \approx -1$, more loop gain makes the output follow $r/H$ more closely, sensor error included; only a better sensor or calibration fixes it.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-04.1a | closed-loop gain | 19.80 | — |
| 15-04.1b | sensitivity | 0.00990 | — |
| 15-04.1c | change when G halves | −0.980 | % |
| 15-04.2a | type (a) | 0 | — |
| 15-04.2b | Kp (a) | 5 | — |
| 15-04.2c | step error (a) | 0.167 | — |
| 15-04.2d | type (b) | 1 | — |
| 15-04.2e | Kv (b) | 2.5 | 1/s |
| 15-04.2f | ramp error (b) | 0.4 | — |
| 15-04.2g | type (c) | 2 | — |
| 15-04.2h | Ka (c) | 0.8 | 1/s² |
| 15-04.2i | parabola error (c) | 1.25 | — |
| 15-04.2j | real closed-loop pole (c) | −4.28 | 1/s |
| 15-04.3a | output-disturbance fraction | 0.01 | — |
| 15-04.3b | sensor-offset fraction | 0.99 | — |
| 15-04.4a | K | 147 | — |
| 15-04.4b | ζ | 0.163 | — |
| 15-04.4c | overshoot | 59.5 | % |
| 15-04.5a | K | 200 | 1/s² |
| 15-04.5b | ζ | 0.354 | — |
| 15-04.5c | overshoot | 30.5 | % |
| 15-04.6a | open-loop rise | 10 | K |
| 15-04.6b | proportional-control rise | 0.909 | K |
| 15-04.6c | PI rise | 0 | K |
| 15-04.7a | steady output | 1.667 | V |
| 15-04.7b | desired output | 2 | V |
| 15-04.7c | steady error | 0.333 | V |
| 15-04.8a | pointing lag | 0.025 | ° |
| 15-04.9a | abs L | 50.0 | — |
| 15-04.9b | abs S | 0.0200 | — |
| 15-04.9c | magnitude error | −0.0220 | % |
| 15-04.9d | phase | −1.15 | ° |
| 15-04.10a | residual amplitude, proportional | 0.960 | — |
| 15-04.10b | slow pole real part | −9.14 | 1/s |
| 15-04.10c | residual amplitude after 0.5 s | 0.0088 | — |
| 15-04.11a | steady phase error | 0 | rad |
| 15-04.11b | peak phase error | 0.849 | rad |
| 15-04.11c | time of the peak | 3.40 | µs |
| 15-04.12a | Ki | 9.75 | V/rad |
| 15-04.12b | other pole | −390 | 1/s |
| 15-04.12c | Kv | 487.5 | 1/s |
| 15-04.12d | peak dip | 1.90 | rad/s |
| 15-04.12e | time of the dip | 6.04 | ms |
| 15-04.13a | output resistance, cool | 4.00 | mΩ |
| 15-04.13b | output change, cool | 0.400 | mV |
| 15-04.13c | output resistance, hot | 13.3 | mΩ |
| 15-04.13d | output change, hot | 1.33 | mV |
| 15-04.14a | output with integral control | 1.0204 | — |
| 15-04.14b | output with proportional gain | 1.0101 | — |
