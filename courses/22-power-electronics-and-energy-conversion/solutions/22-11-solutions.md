# Solutions 22-11 · Electric Machines and Drives

Problems: [22-11 problem set](../problems/22-11-problems.md) · Chapter: [22-11](../chapters/22-11-electric-machines.md). Every number below is recomputed by [verify_22_11.py](../verify/verify_22_11.py).

---

## Solutions

### Solution 22-11.1

(a) $48/0.1$ = 480 rad/s = **4584** rpm; (b) $48/0.2$ = **240** A; (c) $0.1 \times 240$ = **24** N·m; (d) $I_a$ = 20 A, $E_a$ = 48 − 4 = 44 V, $\omega$ = 440 rad/s = **4202** rpm.

### Solution 22-11.2

$T = K\Phi I_a \propto I_a^2$, so doubling the current multiplies the torque by **4**. This is why series motors start heavy loads well, and why they run away at no load: with little current, the field is weak and the speed must rise to make enough back EMF.

### Solution 22-11.3

(a) $120 \times 60/6$ = **1200** rpm; (b) $(1200 - 1164)/1200$ = **3.0** %; (c) $0.03 \times 60$ = **1.8** Hz.

### Solution 22-11.4

(a) $50 - 1.5 - 1$ = **47.5** kW; (b) $0.025 \times 47.5$ = **1.19** kW; (c) **46.31** kW; (d) $46.31 - 0.6$ = **45.71** kW; (e) **91.4** %; (f) $\omega_m = 0.975 \times 188.5$ = 183.8 rad/s, so $45\,712/183.8$ = **248.7** N·m.

### Solution 22-11.5

(a) Torque scales with $V_{th}^2$: **0.81**. (b) In the linear region $T \propto V^2s$, so the slip rises to $0.03/0.81$ = **3.70** %. The rotor copper loss, $sP_{ag}$, rises with it: sags heat motors.

### Solution 22-11.6

(a) $s_{max}$ = 1 needs $R_2 = \sqrt{R_{th}^2 + (X_{th} + X_2)^2}$ = **2.03** Ω. (b) The starting torque becomes $T_{max}$ = **190.9** N·m. (c) At 3% slip the torque falls to **13.9** N·m. (d) To carry 65.4 N·m the slip must rise to **15.2** %, so 15% of the air-gap power is burned in the rotor. High starting torque costs running efficiency, which is why NEMA design D motors (high slip) are reserved for high-inertia loads, and why drives, which can start any motor at its best slip, have made the trade unnecessary.

### Solution 22-11.7

(a) $480/\sqrt3$ = **277.1** V; (b) $\sin\delta = 60\,000 \times 1.5/(3 \times 277.1 \times 300)$ = 0.361, $\delta$ = **21.2**°; (c) $3 \times 277.1 \times 300/1.5$ = **166.3** kW.

### Solution 22-11.8

(a) $460 \times 45/60$ = **345** V; (b) $120 \times 45/4$ = **1350** rpm.

### Solution 22-11.9

(a) **0.80**; (b) $0.8^2$ = **0.64**; (c) $0.8^3$ = **0.512**; (d) $30 \times (1 - 0.512) \times 6000$ = **87 840** kWh.

### Solution 22-11.10

(a) $0.612 \times 400$ = **245** V; (b) $400/\sqrt2$ = **283** V. For the same power an 800 V platform carries half the current of a 400 V one, so cables of the same cross-section lose a quarter as much. The machine's winding loss is not reduced this way: a winding for twice the voltage has twice the turns of half the area, so with the same copper its $I^2R$ is unchanged.

### Solution 22-11.11

(a) $400 \times 9/0.35$ = **10 286** N; (b) $10\,286/2000$ = **5.14** m/s²; (c) $(5000/9) \times 2\pi \times 0.35/60$ = **20.4** m/s; (d) **73.3** km/h; (e) $20.36/5.14$ = **3.96** s.

### Solution 22-11.12

(a) $11/0.91 - 11$ = **1.088** kW; (b) $11/0.93 - 11$ = **0.828** kW; (c) $0.260 \times 5000$ = **1300** kWh per year. Over a motor's life the energy cost dwarfs its purchase price, which is why efficiency regulations target motors.

### Solution 22-11.13

$B(\theta, t) = B_m[\cos\omega t\cos\theta + \sin\omega t\sin\theta] = B_m\cos(\theta - \omega t)$: a rotating field of amplitude (a) **1.0** times one winding's peak, against (b) the three-phase **1.5** times, a ratio of **0.67**.

### Solution 22-11.14

(a) $V = 13\,800/\sqrt3$ = **7967** V and $I = P/(3V\cos\varphi) = 40\ \text{MW}/(3 \times 7967 \times 0.9)$ = **1859** A, lagging by 25.84°. (b) As a generator, $\mathbf E_f = \mathbf V + jX_s\mathbf I = 7967 + j4.0 \times 1859\angle{-25.84°} = 7967 + 3246 + j6693$ V, so $E_f$ = **13.06** kV at δ = **30.84**°. Check: $3VE_f\sin\delta/X_s$ = 40.0 MW. ✓ (c) $3VE_f/X_s$ = **78.0** MW. (d) $Q = 3VI\sin\varphi$ = **19.37** MVAr delivered. (e) At unity power factor $\mathbf I$ is in phase with $\mathbf V$, $I$ = 1673 A, and $E_f = \sqrt{V^2 + (X_sI)^2}$ = **10.41** kV. Lowering the field from 13.06 to 10.41 kV removes the reactive output while the governor holds the power: excitation sets reactive power, the prime mover sets real power.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-11.1a | no-load speed | 4584 | rpm |
| 22-11.1b | stall current | 240 | A |
| 22-11.1c | stall torque | 24 | N·m |
| 22-11.1d | speed at 2 N·m | 4202 | rpm |
| 22-11.2 | torque factor | 4 | |
| 22-11.3a | synchronous speed | 1200 | rpm |
| 22-11.3b | slip | 3.0 | % |
| 22-11.3c | rotor frequency | 1.8 | Hz |
| 22-11.4a | air-gap power | 47.5 | kW |
| 22-11.4b | rotor copper loss | 1.19 | kW |
| 22-11.4c | mechanical power | 46.31 | kW |
| 22-11.4d | output power | 45.71 | kW |
| 22-11.4e | efficiency | 91.4 | % |
| 22-11.4f | output torque | 248.7 | N·m |
| 22-11.5a | torque factor | 0.81 | |
| 22-11.5b | new slip | 3.70 | % |
| 22-11.6a | rotor resistance | 2.03 | Ω |
| 22-11.6b | starting torque | 190.9 | N·m |
| 22-11.6c | torque at 3% slip | 13.9 | N·m |
| 22-11.6d | slip for 65.4 N·m | 15.2 | % |
| 22-11.7a | phase voltage | 277.1 | V |
| 22-11.7b | power angle | 21.2 | ° |
| 22-11.7c | pull-out power | 166.3 | kW |
| 22-11.8a | voltage at 45 Hz | 345 | V |
| 22-11.8b | synchronous speed | 1350 | rpm |
| 22-11.9a | flow | 0.80 | |
| 22-11.9b | head | 0.64 | |
| 22-11.9c | power | 0.512 | |
| 22-11.9d | energy saved | 87840 | kWh |
| 22-11.10a | SPWM line voltage | 245 | V |
| 22-11.10b | SVPWM line voltage | 283 | V |
| 22-11.11a | wheel force | 10286 | N |
| 22-11.11b | acceleration | 5.14 | m/s² |
| 22-11.11c | speed at base speed | 20.4 | m/s |
| 22-11.11d | speed at base speed | 73.3 | km/h |
| 22-11.11e | time to base speed | 3.96 | s |
| 22-11.12a | losses at 91% | 1.088 | kW |
| 22-11.12b | losses at 93% | 0.828 | kW |
| 22-11.12c | energy saved | 1300 | kWh |
| 22-11.13a | two-phase amplitude | 1.0 | |
| 22-11.13b | three-phase amplitude | 1.5 | |
| 22-11.13c | ratio | 0.67 | |
| 22-11.14a | phase voltage | 7967 | V |
| 22-11.14b | phase current | 1859 | A |
| 22-11.14c | excitation EMF | 13.06 | kV |
| 22-11.14d | power angle | 30.84 | ° |
| 22-11.14e | pull-out power | 78.0 | MW |
| 22-11.14f | reactive power delivered | 19.37 | MVAr |
| 22-11.14g | EMF for unity power factor | 10.41 | kV |
