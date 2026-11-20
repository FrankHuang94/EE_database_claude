# Solutions 15-01 · Modeling Dynamic Systems

Problems: [15-01 problems](../problems/15-01-problems.md) · Chapter: [15-01](../chapters/15-01-modeling-dynamic-systems.md). Every number below is recomputed by [verify_15_01.py](../verify/verify_15_01.py), by numerical integration of the original equations, eigenvalues of the state matrices, root finding and numerical Jacobians.

---

## Solutions

### Solution 15-01.1

(a) **3**: the inductor current and the two capacitor voltages. Resistors store no energy and add no state.

(b) **4**: each mass's position and velocity. The three springs' stretches all follow from the two positions, so they add no independent states.

### Solution 15-01.2

$\omega_n = \sqrt{k/m} = \sqrt{400}$ = **20** rad/s and $\zeta = b/(2\sqrt{km}) = 10/(2 \times 40)$ = **0.125**. In the force–voltage analogue, $L = m$ = 2 H, $R = b$ = 10 Ω and $C = 1/k$ = **1.25** mF, all in series, driven by a voltage equal to the force.

### Solution 15-01.3

The rotational equation $J\ddot\theta + B\dot\theta + K\theta = \tau$ has the same form as the translational one. $\omega_n = \sqrt{K/J} = \sqrt{400}$ = **20** rad/s, $\zeta = B/(2\sqrt{KJ}) = 0.02/(2 \times 0.2)$ = **0.05**, and the steady twist is $\tau/K = 0.2/4$ = **0.05** rad (**2.9**°). With $\zeta$ = 0.05 the flywheel rings for many cycles after a torque step.

### Solution 15-01.4

$\tau = RC$ = 4 × 2 = **8** s, and the final temperature is $40 + 15 \times 4$ = **100** °C. From $T(t) = 40 + 60(1 - e^{-t/8})$, setting $T$ = 90 gives $e^{-t/8} = 1/6$, so $t = 8\ln 6$ = **14.33** s.

### Solution 15-01.5

Both layers have area $A$ = 64 × 10⁻⁶ m².

- Silicon: $R = t/(kA) = 0.5 \times 10^{-3}/(140 \times 64 \times 10^{-6})$ = **0.0558** K/W, a drop of **2.79** K at 50 W.
- TIM: $R = 50 \times 10^{-6}/(5 \times 64 \times 10^{-6})$ = **0.156** K/W, a drop of **7.81** K.

The interface layer, one tenth as thick, has **2.8** times the resistance, because its conductivity is **28** times lower. Thin, poorly conducting layers dominate a heat path, which is why TIM quality and bond-line thickness get so much engineering attention (Course 25).

### Solution 15-01.6

(a) With no friction, the no-load speed is where back-EMF equals the supply: $V/K$ = **300** rad/s.

(b) Stall: $V/R$ = **6** A and $K \times 6$ = **0.12** N·m.

(c) $\tau_m = RJ/K^2 = 10^{-5}/(4 \times 10^{-4})$ = **25** ms.

(d) In steady state the motor torque equals the load: $Ki$ = 0.03 N·m, so $i$ = **1.5** A. The voltage equation then gives $K\omega = V - Ri$ = 6 − 1.5 = 4.5 V, so $\omega$ = **225** rad/s. The load costs **25**% of the speed, the familiar drooping torque–speed line of a DC motor.

### Solution 15-01.7

With $B$ = 0 the characteristic polynomial is $LJs^2 + RJs + K^2 = 0$:

$$
2 \times 10^{-8}s^2 + 10^{-5}s + 4 \times 10^{-4} = 0 \;\Longrightarrow\; s = -43.8,\ -456.2\ \text{s}^{-1} .
$$

The time constants are **22.81** ms and **2.19** ms. The first-order model's 25 ms is **9.6**% too long, because $\tau_e$ = 2 ms is now only **12.5** times shorter than $\tau_m$. For a speed controller aiming at a 5 ms response, the 2 ms pole is not negligible: it lies within a factor of 3 of the desired speed and would erode the phase margin (15-07). Keep the second-order model.

### Solution 15-01.8

Newton's law for each mass ($x_1$, $x_2$ measured from equilibrium):

$$
m_1\ddot x_1 = -k_1x_1 + k_2(x_2 - x_1), \qquad m_2\ddot x_2 = -k_2(x_2 - x_1) .
$$

With $m_1 = m_2$ = 1 kg, the stiffness matrix is $\begin{bmatrix} 200 & -100 \\ -100 & 100 \end{bmatrix}$ N/m. Its eigenvalues are $150 \mp \sqrt{12500}$ = **38.2** and **261.8** s⁻², so the natural frequencies are **6.18** and **16.18** rad/s. In the slow mode the masses move together; in the fast mode they move against each other.

In the force–current analogue each mass is a 1 F capacitor from its node to ground (node voltages are the two velocities). The first spring is a 10 mH inductor from node 1 to ground, and the second spring a 10 mH inductor between nodes 1 and 2. The circuit has the mechanism's topology:

```text
   node 1 (v1)          node 2 (v2)
      o------- L2 = 10 mH -------o
      |                          |
   C1 = 1 F    L1 = 10 mH     C2 = 1 F
      |          |               |
   ---+----------+---------------+---  ground (the wall's velocity, zero)
```

(L1 also runs from node 1 to ground, beside C1.) Check: node 1's KCL, $C_1\dot v_1 + (1/L_1)\int v_1\,dt + (1/L_2)\int(v_1 - v_2)\,dt = 0$, is the first mass's equation with $C = m$, $1/L = k$ and $v = \dot x$.

### Solution 15-01.9

(a) At equilibrium $mg = ki^{*2}/x^{*2}$, so $i^* = x^*\sqrt{mg/k}$: the current needed grows in proportion to the gap.

(b) With $f(x, i) = g - (k/m)i^2/x^2$:

$$
\frac{\partial f}{\partial x}\bigg|_* = \frac{2ki^{*2}}{mx^{*3}} = \frac{2g}{x^*}, \qquad \frac{\partial f}{\partial i}\bigg|_* = -\frac{2ki^*}{mx^{*2}} = -\frac{2g}{i^*} .
$$

So $\ddot{\delta x} = (2g/x^*)\,\delta x - (2g/i^*)\,\delta i$. The open-loop poles are at $\pm\sqrt{2g/x^*} = \pm\sqrt{1962}$ = ±**44.3** s⁻¹. The positive one makes the levitator unstable: if the ball drops slightly, the force weakens and it falls further.

(c) The error doubles every $\ln 2/44.3$ = **15.6** ms. A levitation controller needs a bandwidth well above that.

### Solution 15-01.10

The equilibrium solves $T = 35 + 0.8(40 + 2e^{(T - 25)/25})$. Iterating it from the no-growth guess $35 + 0.8 \times 42$ = 68.6 °C gives 76.15, 79.38, 81.09, 82.08, …, converging slowly because each step shrinks the error only by the loop gain (0.673, below); Newton's method gets there in a few steps. The limit is **83.8** °C, with leakage **21.0** W. The loop gain is $G = RP_L/T_x = 0.8 \times 21.04/25$ = **0.673**, so disturbances decay with $\tau_{\text{eff}} = RC/(1 - G) = 16/0.327$ = **49.0** s instead of 16 s.

The critical resistance, where the heat-removed line is tangent to the generation curve ($G$ = 1), follows as in Example 15-01.4: $T_{crit} = T_A + RP_d + T_x$ and $R\,e^{RP_d/T_x} = (T_x/P_{L0})e^{-(T_A - T_0 + T_x)/T_x}$, here $R\,e^{1.6R} = 12.5\,e^{-1.4} = 3.082$, so $R_{crit}$ = **0.824** K/W, reached at $35 + 0.824 \times 40 + 25$ = **93.0** °C. The design's 0.8 K/W leaves only **3.0**% margin: a little dust in the heat sink would remove the equilibrium. The large loop gain is the warning sign; a robust design keeps $G$ well below 1 at the worst ambient.

### Solution 15-01.11

At idle, $T_J = 25 + 2 \times 10$ = 45 °C and the heat-sink node ($T_C$, the node between $R_{JC}$ and $R_{HA}$) sits at $25 + 2 \times 8$ = 41 °C. Without throttling, the burst would drive the junction toward $25 + 15 \times 10$ = **175** °C.

The network's time constants are **0.984** s and **244.0** s. The junction first jumps by about $\Delta P \times R_{JC}$ = **26** K above the slowly warming case, reaching about **72** °C at 5 s, then climbs slowly as the heat sink warms. Solving $T_J(t)$ = 95 °C with the matrix exponential gives **66.0** s.

So the phone can burst for about a minute, after which it must throttle. The burst length is set by the slow (heat-sink) time constant, while the first, fast rise uses up about half of the 50 K margin.

### Solution 15-01.12

(a) In steady state the motor torque equals the fan torque: $K(V - K\omega)/R = c\omega^2$, i.e. $2 \times 10^{-7}\omega^2 + 4 \times 10^{-4}\omega - 0.12 = 0$. The positive root is **264.9** rad/s (**2530** rpm).

(b) Linearizing $J\dot\omega = (K/R)(v - K\omega) - c\omega^2$ about $\omega^*$:

$$
J\,\dot{\delta\omega} = \frac{K}{R}\delta v - \left(\frac{K^2}{R} + 2c\omega^*\right)\delta\omega .
$$

The damping is $K^2/R + 2c\omega^*$ = 4 × 10⁻⁴ + **1.06 × 10⁻⁴** = **5.06 × 10⁻⁴** N·m·s/rad, so the gain is $(K/R)/5.06 \times 10^{-4}$ = **39.5** rad/s per volt and the time constant $J/5.06 \times 10^{-4}$ = **19.8** ms. The fan adds damping: its torque rises with speed, with slope $2c\omega^*$ at the operating point, so it pulls the speed back toward equilibrium faster than back-EMF alone. The small-signal gain and time constant both depend on the operating speed.

### Solution 15-01.13

$$
\frac{d}{dt}\begin{bmatrix} i \\ v_C \end{bmatrix} = \begin{bmatrix} -R/L & -1/L \\ 1/C & 0 \end{bmatrix}\begin{bmatrix} i \\ v_C \end{bmatrix} + \begin{bmatrix} 1/L \\ 0 \end{bmatrix}v_s
= \begin{bmatrix} -10^4 & -10^3 \\ 10^6 & 0 \end{bmatrix}\begin{bmatrix} i \\ v_C \end{bmatrix} + \begin{bmatrix} 10^3 \\ 0 \end{bmatrix}v_s .
$$

$\omega_n = 1/\sqrt{LC} = 1/\sqrt{10^{-9}}$ = **31,623** rad/s and $\zeta = (R/2)\sqrt{C/L} = 5\sqrt{10^{-3}}$ = **0.158**. The eigenvalues are $-\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2}$ = −**5000** ± j**31,225** s⁻¹. (Units: R/L in Ω/H = 1/s; 1/(LC) in 1/s².)

### Solution 15-01.14

(a) $T_J = 85 + 2 \times 40$ = **165** °C, beyond a typical 150 °C limit.

(b) $T_J = T_{top} + P\Psi_{JT}$ = 120 + 2 × 2 = **124** °C.

(c) The $\Psi_{JT}$ estimate. $R_{\theta JA}$ describes the JEDEC test board, not your board, which may conduct heat away much better or worse [R-227]. $\Psi_{JT}$ combines a measurement on your own board with a small correction; because it is small, its variation with board construction and airflow (which TI's note acknowledges) matters little. TI's note recommends exactly this use, and warns that $\Psi_{JT}$ is not a true thermal resistance, so it cannot be used to design a heat path.

### Solution 15-01.15

**(a)** Let the load turn by $\theta_L$ while the motor turns $\theta_m = N\theta_L$. An ideal gearbox transmits power without loss, so the torque it delivers to the load is $N$ times the torque $\tau_g$ it takes from the motor: $\tau_L^{gear} = N\tau_g$. The load obeys $J_L\ddot\theta_L = N\tau_g$, so $\tau_g = J_L\ddot\theta_L/N = (J_L/N^2)\ddot\theta_m$: at the motor shaft the load is an inertia $J_L/N^2$. The motor accelerates $J_m + J_L/N^2 = 2 \times 10^{-5} + 0.01/100$ = **1.2 × 10⁻⁴** kg·m², six times its own rotor.

**(b)** A load torque $\tau_L$ appears at the motor shaft divided by $N$: $\tau_L/N$. (Viscous friction $b_L$ at the load reflects as $b_L/N^2$, like inertia.)

**(c)** For a motor torque $\tau$, the load's acceleration is $\ddot\theta_L = \ddot\theta_m/N = \tau/[N(J_m + J_L/N^2)] = \tau/(NJ_m + J_L/N)$. The denominator is smallest where its derivative $J_m - J_L/N^2$ vanishes: $N = \sqrt{J_L/J_m}$ = **22.4**, the ratio that matches the reflected load inertia to the rotor's (an "inertia match", the mechanical analogue of maximum power transfer, 06-09).

### Solution 15-01.16

**(a)** With states $\theta_J$, $\theta_C$ and input $P$, the transfer function $C(sI - A)^{-1}B$ (15-02) is

$$
\frac{\Theta_J}{P} = \frac{0.2s + 0.006349}{s^2 + 1.3651s + 0.012698} = \frac{(1/C_J)\,(s + 1/[C_H(R_{JC} \parallel R_{CA})])}{(s + 1.356)(s + 0.00937)} .
$$

Its DC gain is $0.006349/0.012698$ = **0.5** K/W, which is $R_{JC} + R_{CA}$ as it must be. The zero is at $-1/[C_H(R_{JC} \parallel R_{CA})] = -1/(300 \times 0.105)$ = **−0.0317** s⁻¹, and the poles at **−1.356** and **−0.00937** s⁻¹ (Example 15-01.3's two time constants). The zero sits between the poles: the fast pole's 1/s fall is undone above the slow pole by the zero, so the junction "sees" mostly $R_{JC}$ at intermediate frequencies.

**(b)** Any two of: thermal conductivity and heat capacity change with temperature (the elements are not linear); heat spreads in three dimensions through the die and spreader, so the true network is distributed rather than two lumps; convection from the fins depends on air speed and on the temperature difference itself, and radiation grows as $T^4$, so the "resistance" to ambient is not constant; hot spots on the die are hotter than the single junction node.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-01.1a | states, ladder circuit | 3 | — |
| 15-01.1b | states, two masses | 4 | — |
| 15-01.2a | natural frequency | 20 | rad/s |
| 15-01.2b | damping ratio | 0.125 | — |
| 15-01.2c | analogue capacitance | 1.25 | mF |
| 15-01.3a | natural frequency | 20 | rad/s |
| 15-01.3b | damping ratio | 0.05 | — |
| 15-01.3c | steady twist | 0.05 | rad |
| 15-01.4a | time constant | 8 | s |
| 15-01.4b | final temperature | 100 | °C |
| 15-01.4c | time to 90 °C | 14.33 | s |
| 15-01.5a | silicon resistance | 0.0558 | K/W |
| 15-01.5b | silicon drop | 2.79 | K |
| 15-01.5c | TIM resistance | 0.156 | K/W |
| 15-01.5d | TIM drop | 7.81 | K |
| 15-01.6a | no-load speed | 300 | rad/s |
| 15-01.6b | stall current | 6 | A |
| 15-01.6c | stall torque | 0.12 | N·m |
| 15-01.6d | mechanical time constant | 25 | ms |
| 15-01.6e | loaded current | 1.5 | A |
| 15-01.6f | loaded speed | 225 | rad/s |
| 15-01.7a | slow time constant | 22.81 | ms |
| 15-01.7b | fast time constant | 2.19 | ms |
| 15-01.7c | first-order model's excess | 9.6 | % |
| 15-01.8a | slow natural frequency | 6.18 | rad/s |
| 15-01.8b | fast natural frequency | 16.18 | rad/s |
| 15-01.9a | unstable pole | 44.3 | 1/s |
| 15-01.9b | doubling time | 15.6 | ms |
| 15-01.10a | operating temperature | 83.8 | °C |
| 15-01.10b | leakage | 21.0 | W |
| 15-01.10c | loop gain | 0.673 | — |
| 15-01.10d | effective time constant | 49.0 | s |
| 15-01.10e | critical resistance | 0.824 | K/W |
| 15-01.10f | temperature at the critical point | 93.0 | °C |
| 15-01.10g | margin | 3.0 | % |
| 15-01.11a | junction temperature if never throttled | 175 | °C |
| 15-01.11b | fast time constant | 0.984 | s |
| 15-01.11c | slow time constant | 244.0 | s |
| 15-01.11d | burst length to 95 °C | 66.0 | s |
| 15-01.12a | operating speed | 264.9 | rad/s |
| 15-01.12b | small-signal gain | 39.5 | rad/s/V |
| 15-01.12c | time constant | 19.8 | ms |
| 15-01.13a | natural frequency | 31623 | rad/s |
| 15-01.13b | damping ratio | 0.158 | — |
| 15-01.13c | real part of the eigenvalues | −5000 | 1/s |
| 15-01.13d | imaginary part | 31225 | rad/s |
| 15-01.14a | junction from R_θJA | 165 | °C |
| 15-01.14b | junction from Ψ_JT | 124 | °C |
| 15-01.3d | steady twist | 2.9 | ° |
| 15-01.5e | TIM against silicon resistance | 2.8 | — |
| 15-01.5f | conductivity ratio | 28 | — |
| 15-01.6g | speed lost to the load | 25 | % |
| 15-01.7d | ratio of mechanical to electrical time constant | 12.5 | — |
| 15-01.8c | slow eigenvalue | 38.2 | 1/s² |
| 15-01.8d | fast eigenvalue | 261.8 | 1/s² |
| 15-01.11e | fast junction jump | 26 | K |
| 15-01.11f | junction at 5 s | 72 | °C |
| 15-01.12d | operating speed | 2530 | rpm |
| 15-01.12e | fan damping 2cω* | 1.06e-4 | N·m·s/rad |
| 15-01.12f | total damping | 5.06e-4 | N·m·s/rad |
| 15-01.15a | total inertia at the motor | 1.2e-4 | kg·m² |
| 15-01.15b | gear ratio for the largest acceleration | 22.4 | — |
| 15-01.16a | DC gain | 0.5 | K/W |
| 15-01.16b | zero | −0.0317 | 1/s |
| 15-01.16c | fast pole | −1.356 | 1/s |
| 15-01.16d | slow pole | −0.00937 | 1/s |
