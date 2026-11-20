# Solutions 15-03 · Time Response and Specifications

Problems: [15-03 problems](../problems/15-03-problems.md) · Chapter: [15-03](../chapters/15-03-time-response.md)

Every number below is recomputed by [verify_15_03.py](../verify/verify_15_03.py) from exact step responses (matrix exponential, crossings and peaks refined by root finding), with the closed-form formulas checked against them.

---

## Solutions

### Solution 15-03.1

The DC gain is 5 V / 1 V = **5**. The output covers 3.16/5 = 63.2% = $1 - e^{-1}$ of its change in 4 ms, so $\tau$ = **4** ms and the pole is at $-1/\tau$ = **−250** s⁻¹. Then

$$
t_r = \tau\ln 9 = \mathbf{8.79}\ \text{ms}, \qquad t_s = \tau\ln 50 = \mathbf{15.6}\ \text{ms}, \qquad f_B = \frac{1}{2\pi\tau} = \mathbf{39.8}\ \text{Hz} .
$$

**Check.** $t_rf_B$ = 8.79 ms × 39.8 Hz = 0.350.

### Solution 15-03.2

From the inverted overshoot formula with $\ln 0.25 = -1.386$:

$$
\zeta = \frac{1.386}{\sqrt{\pi^2 + 1.386^2}} = \mathbf{0.404} .
$$

From $t_p = \pi/\omega_d$: $\omega_d = \pi/0.002$ = **1571** rad/s. Then $\omega_n = \omega_d/\sqrt{1 - \zeta^2}$ = **1717** rad/s, $\sigma = \zeta\omega_n$ = **693** s⁻¹, so the poles are $-693 \pm j1571$ s⁻¹, and the rule gives $t_s = 4/\sigma$ = **5.77** ms.

**Check.** $\sigma^2 + \omega_d^2$ = 693² + 1571² = 1717², as it must.

### Solution 15-03.3

Compare each with $s^2 + 2\zeta\omega_ns + \omega_n^2$: $\omega_n$ is the square root of the constant and $\zeta$ is the $s$ coefficient divided by $2\omega_n$.

| | $\omega_n$ (rad/s) | $\zeta$ | Type | Poles |
|---|---|---|---|---|
| (a) $s^2 + 4s + 20$ | **4.472** | **0.447** | underdamped | $-2 \pm j4$ |
| (b) $s^2 + 6s + 9$ | **3** | **1** | critically damped | −3, −3 |
| (c) $s^2 + 5s + 4$ | **2** | **1.25** | overdamped | −1, −4 |
| (d) $s^2 + 16$ | **4** | **0** | undamped (oscillates forever) | $\pm j4$ |
| (e) $s^2 - 2s + 5$ | **2.236** | **−0.447** | unstable | $1 \pm j2$ |

A negative $\zeta$ puts the poles in the right half-plane: the oscillation grows.

### Solution 15-03.4

**(a)** Write $\sigma = \zeta\omega_n$, $\omega_d = \omega_n\sqrt{1 - \zeta^2}$, so the quadratic is $(s + \sigma)^2 + \omega_d^2$. The residue at $s = 0$ is 1, so

$$
Y(s) = \frac1s + \frac{As + B}{(s + \sigma)^2 + \omega_d^2}, \qquad 1 \cdot [(s + \sigma)^2 + \omega_d^2] + (As + B)s = \omega_n^2 .
$$

Matching $s^2$: $1 + A = 0$, so $A = -1$. Matching $s$: $2\sigma + B = 0$, so $B = -2\sigma$. (The constant term, $\sigma^2 + \omega_d^2 = \omega_n^2$, checks.) Then split $s + 2\sigma = (s + \sigma) + \sigma$:

$$
Y(s) = \frac1s - \frac{s + \sigma}{(s + \sigma)^2 + \omega_d^2} - \frac{\sigma}{\omega_d}\frac{\omega_d}{(s + \sigma)^2 + \omega_d^2}
\;\Rightarrow\;
y(t) = 1 - e^{-\sigma t}\left(\cos\omega_dt + \frac{\sigma}{\omega_d}\sin\omega_dt\right) .
$$

**(b)** Differentiating, the $\cos$ terms cancel: $\dot y = e^{-\sigma t}(\sigma^2/\omega_d + \omega_d)\sin\omega_dt = (\omega_n^2/\omega_d)e^{-\sigma t}\sin\omega_dt$. The first zero after $t$ = 0 is at $\omega_dt = \pi$, so $t_p = \pi/\omega_d$. There $\cos = -1$ and $\sin = 0$, so $y(t_p) = 1 + e^{-\sigma\pi/\omega_d}$ and $M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$.

**(c)** With $\zeta$ = 0.3 and $\omega_n$ = 10: $\sigma$ = 3 s⁻¹ and $\omega_d = 10\sqrt{0.91}$ = **9.539** rad/s.

- Overshoot: $e^{-0.3\pi/0.954}$ = **37.2**%.
- Peak time: $\pi/9.539$ = **0.329** s.
- Settling time by the rule: $4/3$ = **1.33** s; by the envelope: $\ln[1/(0.02 \times 0.954)]/3$ = **1.32** s.
- The exact response leaves the 2% band for the last time at **1.12** s, 16% sooner than the rule.

### Solution 15-03.5

**(a)** Overshoot at most 5%: $\zeta \ge -\ln 0.05/\sqrt{\pi^2 + \ln^2 0.05}$ = **0.690**. Settling at most 2 s: $\sigma \ge 4/2$ = **2** s⁻¹. Rise time at most 0.6 s: $\omega_n \ge 1.8/0.6$ = **3** rad/s.

**(b)** For each pair, $\omega_n = \lvert p\rvert$ and $\zeta = \sigma/\omega_n$:

| Pair | $\zeta$ | $\sigma$ | $\omega_n$ | Rules |
|---|---|---|---|---|
| A: $-2 \pm j2$ | 0.707 | 2 | 2.83 | fails rise time |
| B: $-3 \pm j2$ | 0.832 | 3 | 3.61 | **passes** |
| C: $-1 \pm j1$ | 0.707 | 1 | 1.41 | fails settling and rise |
| D: $-4 \pm j5$ | 0.625 | 4 | 6.40 | fails overshoot (8.1%) |
| E: $-4 \pm j3$ | 0.8 | 4 | 5 | **passes** |

**(c)** Exact responses:

- B: overshoot **0.90**%, settling **1.12** s, but rise time **0.719** s, above 0.6 s: **fails**. At $\zeta$ = 0.83 the rule $1.8/\omega_n$ (0.50 s) underestimates the rise time by 30%.
- E: overshoot **1.52**%, settling **0.751** s, rise time **0.493** s: **passes** all three.

The rules found the region; only the exact check separates B from E.

### Solution 15-03.6

The closed loop is $K/(s^2 + 40s + K)$, so $2\zeta\omega_n = 40$. For $\zeta$ = 0.7: $\omega_n = 20/0.7$ = **28.57** rad/s and $K = \omega_n^2$ = **816** s⁻². Then:

- overshoot $e^{-0.7\pi/0.714}$ = **4.60**%;
- $\omega_d = 28.57 \times 0.714$ = **20.40** rad/s and $t_p = \pi/\omega_d$ = **0.154** s;
- the rule gives $t_s = 4/20$ = **0.2** s;
- the exact settling time is **0.209** s.

Here the rule is slightly optimistic: at $\zeta$ = 0.7 the overshoot (4.6%) exceeds the 2% band, so the response must swing back before it settles.

### Solution 15-03.7

**(a)** $e^{-t/\tau} \le 0.001$ at $t$ = 10 µs requires $\tau \le 10\ \mu\text{s}/\ln 1000$ = **1.448** µs. The bandwidth must be at least $1/(2\pi\tau)$ = **109.9** kHz.

**(b)** Half an LSB of 16 bits is $2^{-17}$ of full scale, so $\tau \le 10\ \mu\text{s}/(17\ln 2)$ = **0.849** µs, and $f_B \ge$ **187.5** kHz. Each extra bit of accuracy costs another $\ln 2$ = 0.69 time constants.

### Solution 15-03.8

| | $\zeta$ = 1 | $\zeta$ = 0.707 |
|---|---|---|
| Overshoot | **0** | **4.32**% |
| Rise time | **33.6** ms | **21.5** ms |
| 2% settling time | **58.3** ms | **59.6** ms |

The underdamped response's rise time is 36% shorter, but its 4.3% overshoot leaves the 2% band, so it must come back, and it settles slightly later than the critically damped response. Critical damping is not the fastest-settling choice either: at $\zeta$ = 0.8 the overshoot (1.5%) stays inside the band, and settling takes only 3.76/$\omega_n$ = **37.6** ms (§3.3 table). The best damping for settling depends on the band.

### Solution 15-03.9

**(a)** The poles are −10 and $-1 \pm j3$. The complex pair's real part (−1) is ten times closer to the imaginary axis than the real pole, so the pair dominates. Keeping the DC gain, $100/(10 \times 10) = 1$, the approximation replaces $10/(s + 10)$ by 1:

$$
T(s) \approx \frac{10}{s^2 + 2s + 10}, \qquad \omega_n = 3.162\ \text{rad/s}, \quad \zeta = \mathbf{0.316} .
$$

**(b)**

| | Approximation | Exact |
|---|---|---|
| Overshoot | **35.1**% | **33.2**% |
| Peak time | **1.047** s | **1.154** s |
| Settling time | **3.54** s | **3.63** s |

The third pole delays the peak by 0.1 s and lowers the overshoot by about two points: errors of 2.5–9%, acceptable for a first design.

### Solution 15-03.10

**(a)** With $\omega_n$ = 2 and $\zeta$ = 0.5, the zero-free response overshoots by **16.3**%. The zero at $z$ = 3 adds $\dot y/3$ and raises the overshoot to **21.7**%, with a rise time of **0.611** s (against **0.819** s without it).

**(b)** The overshoot falls monotonically as $z$ moves left. Solving $M_p(z) = 0.25$ numerically gives $z$ = **2.44** s⁻¹.

**Check.** The answer lies between $z$ = 3 (21.7%) and $z$ = 1, which gives about 70% (Example 15-03.5's $z$ = 0.5 case, scaled by $\omega_n$ = 2).

### Solution 15-03.11

**(a)** By the initial-value theorem, $\dot y(0^+) = \lim_{s\to\infty}s \cdot sY(s) = \lim_{s\to\infty}sT(s) = -4/z$: **−0.5** s⁻¹ for $z$ = 8 and **−4** s⁻¹ for $z$ = 1.

**(b)** From the exact responses: for $z$ = 8, the output dips to an undershoot of **2.65**% at **0.110** s; for $z$ = 1, it dips by **75.2**% at **0.412** s before recovering. Both settle at 1.

**(c)** A right-half-plane zero at $z$ makes the loop first respond the wrong way, and a controller that pushes harder only makes the wrong-way dip larger and faster. Speeding the loop up means placing its closed-loop poles further from the origin, toward the zero, which deepens the undershoot (compare $z/\omega_n$ = 4 with 0.5). In practice the loop's crossover is kept well below the zero's frequency (15-07, 22-07).

### Solution 15-03.12

The closed-loop pole is at $\beta\cdot$GBW = 8 MHz, so $\tau = 1/(2\pi \times 8\ \text{MHz})$ = **19.9** ns. The 0.01% band of a 10 V step is 1 mV.

**(a)** Slewing the whole 10 V at 55 V/µs takes **182** ns; linear settling by a factor of $10^4$ takes $\tau\ln 10^4$ = **183** ns; the sum is **365** ns.

**(b)** The slewing ends when the linear response's slope, $V/\tau$, falls to SR, at $V_L = \mathrm{SR}\cdot\tau$ = 55 V/µs × 19.9 ns = **1.09** V. Slewing covers 10 − 1.09 = 8.91 V in **162** ns, then the linear response decays from 1.09 V to 1 mV in $\tau\ln(1094)$ = **139** ns. The total is **301** ns.

**(c)** Both estimates are below the typical 550 ns. A single-pole model ignores the amplifier's non-dominant poles, which add ringing, any doublet tail, the time to recover from slewing (internal nodes that saturated) and thermal settling. The estimates are lower bounds: if a datasheet beats them, something is unusual; if it is close to twice them, as here, the higher-order dynamics dominate the last bits.

### Solution 15-03.13

**(a)** The tail amplitude is about $\delta/(1 + \delta)$. Exact simulations give 0.1% settling of **616** ns at $\delta$ = 0.05, **366** ns at $\delta$ = 0.01 and **112** ns at $\delta$ = 0.002.

**(b)** After the fast pole has died (by 50 ns, $e^{-\omega_ct} = e^{-31}$), the error is the tail, $\dfrac{\omega_c}{\omega_c - p}\dfrac{\delta}{1 + \delta}e^{-pt}$. Setting it equal to 0.001 at $t$ = 50 ns, where $e^{-pt}$ = 0.730, gives $\delta$ = **0.00136**: the zero must match the pole within about 0.14%.

**Check.** Simulating at 0.1% below and above this $\delta$ gives settling times of **49.8** ns and **50.2** ns.

### Solution 15-03.14

$K$ = **2** (the final value for a unit step). The overshoot is (2.4 − 2)/2 = 20%, so $\zeta = -\ln 0.2/\sqrt{\pi^2 + \ln^2 0.2}$ = **0.456**. From $t_p$ = 0.5 s, $\omega_d = \pi/0.5$ = 6.283 rad/s, so $\omega_n = 6.283/\sqrt{1 - 0.456^2}$ = **7.06** rad/s. Then

$$
G(s) = \frac{K\omega_n^2}{s^2 + 2\zeta\omega_ns + \omega_n^2} = \frac{99.7}{s^2 + 6.44s + 49.8} .
$$

**Check.** Simulating this $G$ gives a peak of **2.400** at **0.500** s.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-03.1a | DC gain | 5 | — |
| 15-03.1b | time constant | 4 | ms |
| 15-03.1c | pole | −250 | 1/s |
| 15-03.1d | rise time | 8.79 | ms |
| 15-03.1e | settling time | 15.6 | ms |
| 15-03.1f | bandwidth | 39.8 | Hz |
| 15-03.2a | ζ | 0.404 | — |
| 15-03.2b | ωd | 1571 | rad/s |
| 15-03.2c | ωn | 1717 | rad/s |
| 15-03.2d | σ | 693 | 1/s |
| 15-03.2e | settling time by the rule | 5.77 | ms |
| 15-03.3a | ωn (a) | 4.472 | rad/s |
| 15-03.3b | ζ (a) | 0.447 | — |
| 15-03.3c | ωn (b) | 3 | rad/s |
| 15-03.3d | ζ (b) | 1 | — |
| 15-03.3e | ωn (c) | 2 | rad/s |
| 15-03.3f | ζ (c) | 1.25 | — |
| 15-03.3g | ωn (d) | 4 | rad/s |
| 15-03.3h | ζ (d) | 0 | — |
| 15-03.3i | ωn (e) | 2.236 | rad/s |
| 15-03.3j | ζ (e) | −0.447 | — |
| 15-03.4a | overshoot | 37.2 | % |
| 15-03.4b | peak time | 0.329 | s |
| 15-03.4c | settling by the rule | 1.33 | s |
| 15-03.4d | settling by the envelope | 1.32 | s |
| 15-03.4e | exact settling time | 1.12 | s |
| 15-03.5a | minimum ζ | 0.690 | — |
| 15-03.5b | minimum σ | 2 | 1/s |
| 15-03.5c | minimum ωn | 3 | rad/s |
| 15-03.5d | exact rise time, pair B | 0.719 | s |
| 15-03.5e | overshoot, pair E | 1.52 | % |
| 15-03.5f | settling time, pair E | 0.751 | s |
| 15-03.5g | rise time, pair E | 0.493 | s |
| 15-03.6a | ωn | 28.57 | rad/s |
| 15-03.6b | K | 816 | 1/s² |
| 15-03.6c | overshoot | 4.60 | % |
| 15-03.6d | peak time | 0.154 | s |
| 15-03.6e | settling by the rule | 0.2 | s |
| 15-03.6f | exact settling time | 0.209 | s |
| 15-03.7a | largest τ, 0.1% | 1.448 | µs |
| 15-03.7b | smallest bandwidth, 0.1% | 109.9 | kHz |
| 15-03.7c | largest τ, 16 bits | 0.849 | µs |
| 15-03.7d | smallest bandwidth, 16 bits | 187.5 | kHz |
| 15-03.8a | overshoot, ζ = 1 | 0 | % |
| 15-03.8b | rise time, ζ = 1 | 33.6 | ms |
| 15-03.8c | settling time, ζ = 1 | 58.3 | ms |
| 15-03.8d | overshoot, ζ = 0.707 | 4.32 | % |
| 15-03.8e | rise time, ζ = 0.707 | 21.5 | ms |
| 15-03.8f | settling time, ζ = 0.707 | 59.6 | ms |
| 15-03.9a | ζ of the dominant pair | 0.316 | — |
| 15-03.9b | approximate overshoot | 35.1 | % |
| 15-03.9c | exact overshoot | 33.2 | % |
| 15-03.9d | approximate peak time | 1.047 | s |
| 15-03.9e | exact peak time | 1.154 | s |
| 15-03.9f | approximate settling time | 3.54 | s |
| 15-03.9g | exact settling time | 3.63 | s |
| 15-03.10a | zero-free overshoot | 16.3 | % |
| 15-03.10b | overshoot, z = 3 | 21.7 | % |
| 15-03.10c | rise time, z = 3 | 0.611 | s |
| 15-03.10d | zero for 25% overshoot | 2.44 | 1/s |
| 15-03.11a | initial slope, z = 8 | −0.5 | 1/s |
| 15-03.11b | initial slope, z = 1 | −4 | 1/s |
| 15-03.11c | undershoot, z = 8 | 2.65 | % |
| 15-03.11d | time of undershoot, z = 8 | 0.110 | s |
| 15-03.11e | undershoot, z = 1 | 75.2 | % |
| 15-03.11f | time of undershoot, z = 1 | 0.412 | s |
| 15-03.12a | closed-loop time constant | 19.9 | ns |
| 15-03.12b | crude estimate | 365 | ns |
| 15-03.12c | transition error V_L | 1.09 | V |
| 15-03.12d | refined estimate | 301 | ns |
| 15-03.13a | settling, δ = 0.05 | 616 | ns |
| 15-03.13b | settling, δ = 0.01 | 366 | ns |
| 15-03.13c | settling, δ = 0.002 | 112 | ns |
| 15-03.13d | largest δ for 50 ns | 0.00136 | — |
| 15-03.14a | K | 2 | — |
| 15-03.14b | ζ | 0.456 | — |
| 15-03.14c | ωn | 7.06 | rad/s |
| 15-03.14d | numerator | 99.7 | 1/s² |
| 15-03.14e | s coefficient | 6.44 | 1/s |
| 15-03.14f | constant | 49.8 | 1/s² |
| 15-03.4f | ωd | 9.539 | rad/s |
| 15-03.5h | overshoot, pair B | 0.90 | % |
| 15-03.5i | settling time, pair B | 1.12 | s |
| 15-03.6g | ωd | 20.40 | rad/s |
| 15-03.8g | settling time, ζ = 0.8 | 37.6 | ms |
| 15-03.10e | zero-free rise time | 0.819 | s |
| 15-03.12e | full-step slewing time | 182 | ns |
| 15-03.12f | linear settling time | 183 | ns |
| 15-03.12g | refined slewing time | 162 | ns |
| 15-03.12h | refined linear settling time | 139 | ns |
| 15-03.13e | settling just below δ | 49.8 | ns |
| 15-03.13f | settling just above δ | 50.2 | ns |
| 15-03.14g | simulated peak | 2.400 | — |
| 15-03.14h | simulated peak time | 0.500 | s |
