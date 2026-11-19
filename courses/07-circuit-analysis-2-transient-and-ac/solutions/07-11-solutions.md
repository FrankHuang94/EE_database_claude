# Solutions 07-11 · Three-Phase Circuits

Problems: [07-11 problems](../problems/07-11-problems.md) · Chapter: [07-11](../chapters/07-11-three-phase-circuits.md). Every number below is recomputed by [verify_07_11.py](../verify/verify_07_11.py), mostly by building the three-phase circuit from its three sources and solving it whole (not per phase), or by integrating sampled waveforms; values marked † are also confirmed by ngspice in [labs/07-11-lab](../labs/07-11-lab/README.md).

---

## Solutions

### Solution 07-11.1

(a) $\sqrt3\times120$ = **207.8 V** (the "208 V" system) and $\sqrt3\times277$ = **479.8 V** (480 V). (b) $400/\sqrt3$ = **230.9 V**. (c) $\sqrt3\times10$ = **17.32 A**.

### Solution 07-11.2

$\mathbf{V}_{bn} = 277\angle{-120°}$ V and $\mathbf{V}_{cn} = 277\angle120°$ V. $\mathbf{V}_{bc} = \mathbf{V}_{bn} - \mathbf{V}_{cn}$ = **479.8 V ∠ −90°**, and $\mathbf{V}_{ca} = \mathbf{V}_{cn} - \mathbf{V}_{an}$ = **479.8 V ∠ 150°**: each line voltage leads its first phase voltage by 30°, as for $\mathbf{V}_{ab}$ (§3.1).

### Solution 07-11.3

$Z_Y = Z_\Delta/3$ = **10 + j5 Ω**.

### Solution 07-11.4

$V_p = 208/\sqrt3$ = **120.1 V**. $\lvert Z\rvert$ = 15 Ω at 36.87°, so $\mathbf{I}_a$ = **8.006 A ∠ −36.87°**. $P = 3\times8.006^2\times12$ = **2307 W**, $Q = 3\times8.006^2\times9$ = **1731 var**, power factor **0.800** lagging.

### Solution 07-11.5

$I_L = 40\,000/(\sqrt3\times480\times0.85)$ = **56.60 A**; in Δ the winding current is $I_L/\sqrt3$ = **32.68 A**; $Q = P\tan(\arccos0.85)$ = **24.79 kvar**.

### Solution 07-11.6

$Z_Y = 8 + j6$ Ω. Per phase: $\mathbf{I}_a = 230.9/(8.5 + j7)$ = **20.97 A ∠ −39.47°**. The load phase voltage is $20.97\times10$ = 209.7 V, a line voltage of **363.3 V**. The Δ phase current is $20.97/\sqrt3$ = **12.11 A** (check: $363.3/30$ = 12.11 A ✓). Load power $3\times20.97^2\times8$ = **10.56 kW**.

### Solution 07-11.7

$\mathbf{I}_a = 120/12$ = 10 A ∠ 0°, $\mathbf{I}_b$ = 10 A ∠ −120°, and $\mathbf{I}_c = 120\angle120°/(j12)$ = **10.00 A ∠ 30.00°**. The neutral carries $\mathbf{I}_a + \mathbf{I}_b + \mathbf{I}_c$ = **14.14 A ∠ −15.00°**, more than any phase current, although all three phase currents have the same magnitude: equal magnitudes are not enough; the angles must be 120° apart.

### Solution 07-11.8

Phase RMS current: $\sqrt{10^2 + 4^2 + 2^2}$ = **10.95 A** (07-06's quadrature rule). The fundamentals cancel in the neutral, and so do the fifth harmonics: the fifth harmonic of phase $b$ is shifted by $5\times(-120°) = -600° \equiv 120°$, so the three fifth-harmonic currents still form a balanced set (in negative sequence) and sum to **0**. The third harmonics are all in phase and add: the neutral carries **12.0 A**, more than any phase.

### Solution 07-11.9

$P = W_1 + W_2$ = **8.00 kW**; $Q = \sqrt3(W_2 - W_1)$ = **20.78 kvar**; power factor $8/\sqrt{8^2 + 20.78^2}$ = **0.359** lagging (θ = 68.95°). A reading passes through zero when $30° + \theta = 90°$, i.e. θ = 60°: power factor **0.5**. Below that, as here, it reads negative.

### Solution 07-11.10

$Q_C = 300(\tan\theta_{0.75} - \tan\theta_{0.95}) = 300(0.8819 - 0.3287)$ = **166.0 kvar**. Per Δ capacitor, $55.32\ \text{kvar}/(2\pi\times60\times480^2)$ = **636.9 µF**. Line current falls from $300\,000/(\sqrt3\times480\times0.75)$ = **481.1 A** to **379.8 A**.

### Solution 07-11.11

(a) A single-phase load's power is $p = P + \lvert S\rvert\cos(2\omega t - \theta)$ (07-06), swinging between $P - \lvert S\rvert$ and $P + \lvert S\rvert$. With $\lvert S\rvert = 12.8/0.8 = 16$ kVA: from **−3.2 kW** (power flows back to the source) to **28.8 kW**, at 100 Hz.

(b) §3.4: the three double-frequency terms are equal in amplitude and 240° apart, so they cancel, leaving **12.8 kW** at every instant. The verify script confirms it by sampling.

(c) A generator's shaft torque is power divided by speed. Constant power means constant torque, with no 100 or 120 Hz torque pulsation to shake the machine, which is why large motors and generators are three-phase.

### Solution 07-11.12

(a) Each conductor's resistance is 0.06 Ω. At 415 V, $I = 17\,300/(\sqrt3\times415)$ = 24.07 A and the loss is $3\times24.07^2\times0.06$ = **104.3 W**. At 208 V, $I$ = 48.02 A and the loss is **415.1 W**, about four times as much.

(b) Correct values: three-phase 208 V, 30 A, 80% continuous: $0.8\times\sqrt3\times208\times30$ = **8.65 kW** (the vendor lists 10.8 kW: wrong); three-phase 208 V, 60 A, full: **21.62 kW** (vendor 17.3 kW: wrong); three-phase 415 V, 30 A, full: **21.56 kW** (vendor 21.6 kW: correct); single-phase 208 V, 30 A, full: **6.24 kW** (vendor 6.2 kW: correct).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-11.1a | line voltage, 120 V phase | 207.8 | V |
| 07-11.1b | line voltage, 277 V phase | 479.8 | V |
| 07-11.1c | phase voltage, 400 V system | 230.9 | V |
| 07-11.1d | Δ line current | 17.32 | A |
| 07-11.2a | $V_{bc}$ | 479.8 | V |
| 07-11.2b | its angle | −90 | ° |
| 07-11.2c | $V_{ca}$ | 479.8 | V |
| 07-11.2d | its angle | 150 | ° |
| 07-11.3a | Y resistance | 10 | Ω |
| 07-11.3b | Y reactance | 5 | Ω |
| 07-11.4a | phase voltage | 120.1 | V |
| 07-11.4b | line current | 8.006 | A |
| 07-11.4c | its angle | −36.87 | ° |
| 07-11.4d | real power | 2307 | W |
| 07-11.4e | reactive power | 1731 | var |
| 07-11.4f | power factor | 0.800 | — |
| 07-11.5a | line current | 56.60 | A |
| 07-11.5b | winding current | 32.68 | A |
| 07-11.5c | reactive power | 24.79 | kvar |
| 07-11.6a | line current | 20.97 | A |
| 07-11.6b | its angle | −39.47 | ° |
| 07-11.6c | load line voltage | 363.3 | V |
| 07-11.6d | Δ phase current | 12.11 | A |
| 07-11.6e | load power | 10.56 | kW |
| 07-11.7a | phase c current | 10.00 | A |
| 07-11.7b | its angle | 30.00 | ° |
| 07-11.7c | neutral current | 14.14 | A |
| 07-11.7d | its angle | −15.00 | ° |
| 07-11.8a | RMS phase current | 10.95 | A |
| 07-11.8b | RMS neutral current | 12.0 | A |
| 07-11.8c | fifth-harmonic neutral current | 0 | A |
| 07-11.9a | P | 8.00 | kW |
| 07-11.9b | Q | 20.78 | kvar |
| 07-11.9c | power factor | 0.359 | — |
| 07-11.9d | impedance angle | 68.95 | ° |
| 07-11.9e | power factor at which one reading is zero | 0.5 | — |
| 07-11.10a | capacitive reactive power | 166.0 | kvar |
| 07-11.10b | Δ capacitance per phase | 636.9 | µF |
| 07-11.10c | line current before | 481.1 | A |
| 07-11.10d | line current after | 379.8 | A |
| 07-11.11a | single-phase minimum power | −3.2 | kW |
| 07-11.11b | single-phase maximum power | 28.8 | kW |
| 07-11.11c | three-phase power | 12.8 | kW |
| 07-11.12a | cable loss at 415 V | 104.3 | W |
| 07-11.12b | cable loss at 208 V | 415.1 | W |
| 07-11.12c | 208 V, 30 A, 80% | 8.65 | kW |
| 07-11.12d | 208 V, 60 A, full | 21.62 | kW |
| 07-11.12e | 415 V, 30 A, full | 21.56 | kW |
| 07-11.12f | single-phase 208 V, 30 A | 6.24 | kW |
