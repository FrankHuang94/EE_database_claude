# Solutions 15-09 · Lead and Lag Compensation

Problems: [15-09 problems](../problems/15-09-problems.md) · Chapter: [15-09](../chapters/15-09-lead-lag-compensation.md)

Every number below is recomputed by [verify_15_09.py](../verify/verify_15_09.py): designs with `labs/15-09-lab/compensate.py`, margins by root finding, and step responses exactly.

---

## Solutions

### Solution 15-09.1

$\alpha = (1 + \sin\phi)/(1 - \sin\phi)$: **3.00** for 30°, **5.83** for 45° and **13.9** for 60°. The ratio grows fast: the last 15° costs more than doubling $\alpha$.

### Solution 15-09.2

The lag's phase at crossover is $\arctan(\omega_c/z) - \arctan(\omega_c/p)$ with $p = z/10$. For $f$ = 10: $\arctan 10 - \arctan 100$ = **−5.14**°. For $f$ = 5: $\arctan 5 - \arctan 50$ = **−10.2**°. Halving the separation roughly doubles the cost.

### Solution 15-09.3

$R_1 = (\alpha - 1)R_2$ = **30** kΩ. The zero is at $\omega_m/\sqrt\alpha$ = 500 rad/s, so $C_1 = 1/(R_1 \times 500)$ = **66.7** nF. The pole is at $\alpha \times 500$ = 2000 rad/s, and the peak at their geometric mean, 1000 rad/s.

### Solution 15-09.4

$K_v = K/2$ = 20, so $K$ = **40**. Uncompensated: crossover **6.17** rad/s, PM **18.0**°. The lead must add $50 - 18.0 + 10 = 42.0°$, so $\alpha$ = **5.05**. The uncompensated $\lvert 40P\rvert = 1/\sqrt\alpha$ at **9.38** rad/s, the new crossover; $T$ = 0.0474 s, the zero at **4.17** rad/s and the pole at **21.1** rad/s. Result: PM = **54.1**°, overshoot **18.1**%, 2% settling **0.629** s.

### Solution 15-09.5

The phase $-90° - \arctan(\omega/2)$ equals −125° at $\omega_c' = 2\tan 35°$ = **1.40** rad/s, where $\lvert 40P\rvert$ = 11.7, so $\beta$ = **11.7**. Zero at **0.140** rad/s, pole at **0.0120** rad/s. Result: PM = **49.7**°, overshoot **22.3**%, settling **9.86** s. The lag meets the margin by slowing the loop (crossover 1.40 against the lead's 9.38 rad/s) and settles sixteen times more slowly.

### Solution 15-09.6

At $s_d = -3 + j4$: $\angle s_d$ = 126.9° and $\angle(s_d + 2)$ = 104.0°, so $\angle P = -230.9°$ and the deficiency is **50.9**°. The zero at −3 contributes 90°; the pole must contribute $90° - 50.9° = 39.1°$, so it sits at $-3 - 4/\tan 39.1°$ = **−7.92**. The gain is $\lvert s_d\rvert\,\lvert s_d + 2\rvert\,\lvert s_d + 7.92\rvert/\lvert s_d + 3\rvert$ = **32.7**. The third closed-loop pole is at **−3.92** (constant sum: $-3 - 3 - 3.92 = -9.92 = -2 - 7.92$), and $K_v = 32.7 \times 3/(7.92 \times 2)$ = **6.19** s⁻¹.

### Solution 15-09.7

Crossover is at 1.82 rad/s, so the lag zero is at **0.182** rad/s and the pole at **0.0182** rad/s. The loop gain at low frequency rises tenfold: $K_v$ = **20** s⁻¹. The phase margin falls to **60.3**° (by 5.2°), and crossover barely moves.

### Solution 15-09.8

**(a)** $K_v = K/5$ = 10 gives $K$ = 50. Routh on $s^3 + 6s^2 + 5s + 50$: $6 \times 5 = 30 < 50$, unstable. The gain margin is **0.6** (it would need to fall by 40%).

**(b)** Two identical leads raise the gain by $\alpha$ at their peak, so the new crossover is where the uncompensated $\lvert L\rvert = 1/\alpha$. Solving for a 45° margin: $\alpha$ = **5.03**, each stage adding **41.9**° at $\omega_m$ = **5.71** rad/s. Each zero is at **2.55** rad/s and each pole at **12.8** rad/s. The compensated loop has gain margin **3.84** (11.7 dB). A single stage supplying the same 83.8° at that crossover would need $\alpha$ of more than 300: an impractical high-frequency gain.

### Solution 15-09.9

With $C$ = 70 µF: $f_0$ = **19.0** kHz and $Q$ = **8.37**. The plant's gain above $f_0$ rises (it falls as $1/(\omega^2LC)$, and $C$ is smaller), so crossover moves up to **81.1** kHz. The phase margin falls to **50.2**° and the gain margin to **16.5** dB. The design still holds, but with less margin and a crossover closer to the switching frequency; derated capacitance must be part of the corner analysis.

### Solution 15-09.10

The lead's high-frequency gain is $\alpha$ = 4.03, or **12.1** dB. Sensor noise above the lead's pole (8.88 rad/s) reaches the actuator four times larger than without the lead: the price of the extra phase.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-09.1a | α for 30° | 3.00 | — |
| 15-09.1b | α for 45° | 5.83 | — |
| 15-09.1c | α for 60° | 13.9 | — |
| 15-09.2a | lag phase, f = 10 | −5.14 | ° |
| 15-09.2b | lag phase, f = 5 | −10.2 | ° |
| 15-09.3a | R1 | 30 | kΩ |
| 15-09.3b | C1 | 66.7 | nF |
| 15-09.4a | K | 40 | 1/s |
| 15-09.4b | uncompensated crossover | 6.17 | rad/s |
| 15-09.4c | uncompensated phase margin | 18.0 | ° |
| 15-09.4d | α | 5.05 | — |
| 15-09.4e | new crossover | 9.38 | rad/s |
| 15-09.4f | zero | 4.17 | rad/s |
| 15-09.4g | pole | 21.1 | rad/s |
| 15-09.4h | phase margin | 54.1 | ° |
| 15-09.4i | overshoot | 18.1 | % |
| 15-09.4j | settling | 0.629 | s |
| 15-09.5a | new crossover | 1.40 | rad/s |
| 15-09.5b | β | 11.7 | — |
| 15-09.5c | zero | 0.140 | rad/s |
| 15-09.5d | pole | 0.0120 | rad/s |
| 15-09.5e | phase margin | 49.7 | ° |
| 15-09.5f | overshoot | 22.3 | % |
| 15-09.5g | settling | 9.86 | s |
| 15-09.6a | angle deficiency | 50.9 | ° |
| 15-09.6b | lead pole | −7.92 | 1/s |
| 15-09.6c | K | 32.7 | 1/s² |
| 15-09.6d | third pole | −3.92 | 1/s |
| 15-09.6e | Kv | 6.19 | 1/s |
| 15-09.7a | lag zero | 0.182 | rad/s |
| 15-09.7b | lag pole | 0.0182 | rad/s |
| 15-09.7c | Kv | 20 | 1/s |
| 15-09.7d | phase margin | 60.3 | ° |
| 15-09.8a | uncompensated gain margin | 0.6 | — |
| 15-09.8b | α per stage | 5.03 | — |
| 15-09.8c | phase per stage | 41.9 | ° |
| 15-09.8d | crossover | 5.71 | rad/s |
| 15-09.8e | zero | 2.55 | rad/s |
| 15-09.8f | pole | 12.8 | rad/s |
| 15-09.8g | gain margin | 3.84 | — |
| 15-09.9a | f0 | 19.0 | kHz |
| 15-09.9b | Q | 8.37 | — |
| 15-09.9c | crossover | 81.1 | kHz |
| 15-09.9d | phase margin | 50.2 | ° |
| 15-09.9e | gain margin | 16.5 | dB |
| 15-09.10a | high-frequency gain increase | 12.1 | dB |
