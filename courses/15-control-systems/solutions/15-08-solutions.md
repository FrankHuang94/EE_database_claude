# Solutions 15-08 · PID Control

Problems: [15-08 problems](../problems/15-08-problems.md) · Chapter: [15-08](../chapters/15-08-pid-control.md)

Every number below is recomputed by [verify_15_08.py](../verify/verify_15_08.py): closed-loop responses by simulation (`labs/15-08-lab/pid.py`, with step-halving checks), margins by root finding, and pole placements by comparing polynomial coefficients.

---

## Solutions

### Solution 15-08.1

$K_i = K_p/T_i$ = **4** s⁻¹ and $K_d = K_pT_d$ = **0.2** s. The zeros are the roots of $T_iT_ds^2 + T_is + 1 = 0.05s^2 + 0.5s + 1$: $s = (-0.5 \pm\sqrt{0.25 - 0.2})/0.1$, that is **−2.764** and **−7.236** s⁻¹. They are real because $T_i = 0.5 \ge 4T_d = 0.4$.

### Solution 15-08.2

$L(0) = K_pK = 14 \times 0.5 = 7$, so the step error is $1/(1 + 7)$ = **0.125**: the temperature settles 12.5% short of the setpoint. An integrator makes it zero (15-04).

### Solution 15-08.3

$\arctan(1/3)$ = **18.4**°, $\arctan(1/5)$ = **11.3**°, $\arctan(1/10)$ = **5.7**°. A factor of 5 is a common compromise between phase cost and how quickly the integral removes errors.

### Solution 15-08.4

With $K$ = 50 and $\tau$ = 0.025 s, §3.3 gives $K_p = (2 \times 0.7 \times 100 \times 0.025 - 1)/50$ = **0.05** V·s/rad and $K_i = 100^2 \times 0.025/50$ = **5** V/rad. The PI zero is at $-K_i/K_p$ = **−100** s⁻¹, at the same distance from the origin as the poles. Simulating, the overshoot is **11.2**% (against **4.60**% for $\zeta$ = 0.7 without the zero) and the 2% settling time is **50.7** ms.

### Solution 15-08.5

SIMC with $\tau_c = \theta$ = 1 s: $K_p = 10/[2(1 + 1)]$ = **2.5** and $T_i = \min(10, 8)$ = **8** s. The loop gain $2.5(8s + 1)/(8s) \times 2e^{-s}/(10s + 1)$ has crossover at **0.505** rad/s with phase margin **58.3**°, gain margin **3.11** (**9.84** dB) and delay margin **2.02** s. The default SIMC setting gives margins similar to a careful manual design.

### Solution 15-08.6

The characteristic polynomial with proportional gain is $s^3 + 3s^2 + 2s + K$; the cubic test gives $K_u$ = **6**, oscillating at $\omega = \sqrt2$, so $P_u = 2\pi/\sqrt2$ = **4.443** s. Ziegler–Nichols: $K_p$ = **3.6**, $T_i$ = **2.221** s, $T_d$ = **0.555** s. The resulting phase margin is only **24.3**° and the setpoint overshoot **61.7**%: the rule is aggressive, and with an integrating plant (already type 1) the added integral makes it more so.

### Solution 15-08.7

$K_p(1 + N)$: with $N$ = 10, **52.8** (**34.5** dB); with $N$ = 5, **28.8**. Halving $N$ almost halves the noise reaching the actuator, at the cost of less phase lead near crossover.

### Solution 15-08.8

Simulating with back-calculation:

- $T_t$ = 1.4 s: overshoot **0.43**%, settling **15.6** s.
- $T_t$ = 5.6 s: overshoot **7.67**%, settling **24.6** s.

A shorter tracking time resets the integrator faster while saturated, so less excess integral accumulates; a long $T_t$ approaches no anti-windup at all (Example 15-08.4: 23.6%). Too short a $T_t$ can make the integrator follow noise in the saturation signal, which is why $T_t$ is usually chosen between $T_d$ and $T_i$.

### Solution 15-08.9

With $C = K_p + K_i/s + K_ds$, the characteristic polynomial is $s(s + 1)(0.2s + 1) + K_ds^2 + K_ps + K_i$. Divided by 0.2: $s^3 + (6 + 5K_d)s^2 + (5 + 5K_p)s + 5K_i$. Matching $(s + 5)^3 = s^3 + 15s^2 + 75s + 125$: $K_d$ = **1.8**, $K_p$ = **14**, $K_i$ = **25**.

Now every closed-loop pole is at −5, including the one that was the plant's slow pole. A unit input disturbance peaks at **0.0541** at **0.4** s (against 0.120 for the cancelling design), and at 3 s it is below $10^{-5}$, effectively zero (against **0.0156**). The setpoint overshoot is **8.43**%, from the controller's zeros; setpoint weighting can remove it without affecting the disturbance response.

### Solution 15-08.10

Searching for the weight that gives 10% overshoot (by repeated simulation): $b$ = **0.371**. It is below Example 15-08.5's $b$ = 0.5, which gave 16.6%: less proportional action on the setpoint means less overshoot, while the disturbance response is unchanged.

### Solution 15-08.11

$\omega_c = (\pi/6)/0.3$ = **1.745** rad/s, $K_p = \omega_c \times 2/0.5$ = **6.98** W/K and $K_i = K_p/2$ = **3.49** W/(K·s). The loop is exactly three times slower, because with the PI zero on the plant pole the crossover is set by the delay alone: $\omega_c \propto 1/T$.

### Solution 15-08.12

$K_u \approx 4/(\pi \times 0.159)$ = **8.01**, against the exact **8** from Routh (15-05). The describing-function estimate is close because the plant's three poles filter the relay's square wave into a nearly sinusoidal output. The period (3.63 s) also matches $P_u = 2\pi/\sqrt3$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-08.1a | Ki | 4 | 1/s |
| 15-08.1b | Kd | 0.2 | s |
| 15-08.1c | slower zero | −2.764 | 1/s |
| 15-08.1d | faster zero | −7.236 | 1/s |
| 15-08.2a | step error | 0.125 | — |
| 15-08.3a | phase cost, f = 3 | 18.4 | ° |
| 15-08.3b | phase cost, f = 5 | 11.3 | ° |
| 15-08.3c | phase cost, f = 10 | 5.7 | ° |
| 15-08.4a | Kp | 0.05 | V·s/rad |
| 15-08.4b | Ki | 5 | V/rad |
| 15-08.4c | closed-loop zero | −100 | 1/s |
| 15-08.4d | overshoot | 11.2 | % |
| 15-08.4e | settling time | 50.7 | ms |
| 15-08.4f | overshoot without the zero | 4.60 | % |
| 15-08.5a | Kp | 2.5 | — |
| 15-08.5b | Ti | 8 | s |
| 15-08.5c | phase margin | 58.3 | ° |
| 15-08.5d | gain margin | 3.11 | — |
| 15-08.5e | gain margin | 9.84 | dB |
| 15-08.5f | delay margin | 2.02 | s |
| 15-08.5g | crossover | 0.505 | rad/s |
| 15-08.6a | ultimate gain | 6 | — |
| 15-08.6b | ultimate period | 4.443 | s |
| 15-08.6c | Kp | 3.6 | — |
| 15-08.6d | Ti | 2.221 | s |
| 15-08.6e | Td | 0.555 | s |
| 15-08.6f | phase margin | 24.3 | ° |
| 15-08.6g | overshoot | 61.7 | % |
| 15-08.7a | high-frequency gain, N = 10 | 52.8 | — |
| 15-08.7b | high-frequency gain, N = 10 | 34.5 | dB |
| 15-08.7c | high-frequency gain, N = 5 | 28.8 | — |
| 15-08.8a | overshoot, Tt = 1.4 s | 0.43 | % |
| 15-08.8b | settling, Tt = 1.4 s | 15.6 | s |
| 15-08.8c | overshoot, Tt = 5.6 s | 7.67 | % |
| 15-08.8d | settling, Tt = 5.6 s | 24.6 | s |
| 15-08.9a | Kd | 1.8 | — |
| 15-08.9b | Kp | 14 | — |
| 15-08.9c | Ki | 25 | 1/s |
| 15-08.9d | disturbance peak | 0.0541 | — |
| 15-08.9e | cancelling design at 3 s | 0.0156 | — |
| 15-08.9f | setpoint overshoot | 8.43 | % |
| 15-08.9g | time of the disturbance peak | 0.4 | s |
| 15-08.10a | setpoint weight b | 0.371 | — |
| 15-08.11a | crossover | 1.745 | rad/s |
| 15-08.11b | Kp | 6.98 | W/K |
| 15-08.11c | Ki | 3.49 | W/(K·s) |
| 15-08.12a | estimated ultimate gain | 8.01 | — |
| 15-08.12b | exact ultimate gain | 8 | — |
