# Solutions 10-04 · Small-Signal Models

Problems: [10-04 problems](../problems/10-04-problems.md) · Chapter: [10-04](../chapters/10-04-small-signal-models.md). Every number below is recomputed by [verify_10_04.py](../verify/verify_10_04.py), which finds each parameter as a numerical derivative of the large-signal law and solves each small-signal circuit as a set of nodal equations.

---

## Solutions

### Solution 10-04.1

$g_m$ = 0.2 mA/25.852 mV = **7.736** mS; $r_\pi = 150/g_m$ = **19.39** kΩ; $r_e = \alpha/g_m = (150/151)/g_m$ = **128.4** Ω; $r_o$ = 75 V/0.2 mA = **375** kΩ; $g_mr_o = V_A/V_T$ = **2901**.

At a fifth of a milliampere every resistance is five times its 1 mA value; the intrinsic gain does not change with current.

### Solution 10-04.2

(a) $V_{ov} = \sqrt{2I_D/k_n}$ = **0.5** V; $g_m = \sqrt{2k_nI_D}$ = **1.0** mS; $r_o = 1/(\lambda I_D)$ = **40** kΩ; $g_mr_o$ = **40**.

(b) Same size, double current: $V_{ov}$ rises by √2 to **0.707** V, $g_m$ by √2 to **1.414** mS; $r_o$ halves to **20** kΩ; $g_mr_o$ falls to **28.3**.

(c) Double width, same overdrive: $g_m = 2I_D/V_{ov}$ doubles to **2.0** mS; $r_o$ = **20** kΩ; $g_mr_o$ stays **40**.

Widening the device is the efficient knob: the same extra current buys twice the $g_m$ and keeps the intrinsic gain, at the cost of area and capacitance. Raising the overdrive buys only √2 and degrades the intrinsic gain, though it improves linearity (§3.6) and speed.

### Solution 10-04.3

- $V_{DD}$ becomes ground, so $R_1$ and $R_2$ appear in parallel from gate to ground ($R_G = R_1 \parallel R_2$), and $R_D$ runs from drain to ground.
- $C_1$ and $C_2$ become shorts: $v_{sig}$ and $R_{sig}$ drive the gate directly, and $R_L$ sits in parallel with $R_D$.
- $C_S$ shorts $R_S$, so the source is at signal ground.
- The transistor becomes $g_mv_{gs}$ from drain to source (with no gate current).

Then $v_g = v_{sig}R_G/(R_G + R_{sig})$ and $v_o = -g_mv_g(R_D \parallel R_L)$, so

$$
\frac{v_o}{v_{sig}} = -\frac{R_G}{R_G + R_{sig}}\,g_m(R_D \parallel R_L) .
$$

### Solution 10-04.4

(a) $g_m$ = 0.5/25.852 = **19.34** mS; $r_\pi = 80/g_m$ = **4.136** kΩ; $r_e = (80/81)/g_m$ = **51.07** Ω.

(b) $r_\pi = \beta/g_m$ and $r_e = \alpha/g_m = \beta/[(\beta + 1)g_m]$, so $r_\pi/r_e = \beta + 1$. Numerically $81 \times 51.07$ Ω = **4.136** kΩ.

### Solution 10-04.5

(a) $g_m$ = 2/25.852 = **77.36** mS; $r_\pi = 120/g_m$ = **1.551** kΩ; $R_{in}$ = 20 ∥ 1.551 = **1.439** kΩ.

(b) $1.439/(1.439 + 1)$ = **0.590**.

(c) $r_o$ = 60/2 = **30** kΩ, and the collector sees $R_C \parallel R_L \parallel r_o$ = 3 ∥ 6 ∥ 30 = **1.875** kΩ.

(d) $-g_m \times 1.875$ kΩ = **−145.1** from base to output, and overall $-145.1 \times 0.590$ = **−85.6**. The source resistance is comparable to $r_\pi$, so 41% of the signal is lost before it reaches the transistor: the input resistance of a CE stage at 2 mA is low, a theme of 10-05 and 10-07.

### Solution 10-04.6

$g_m = \sqrt{2 \times 5 \times 0.4}$ = **2.0** mS and $V_{ov} = \sqrt{0.8/5}$ = **0.4** V. With the source grounded, $-g_mR_D$ = **−10.0**. With $R_S$ unbypassed, the source voltage follows the current, $v_s = i_dR_S$, so $i_d = g_m(v_g - i_dR_S)$, $i_d = g_mv_g/(1 + g_mR_S)$ and the gain is $-g_mR_D/(1 + g_mR_S)$ = **−5.0**.

### Solution 10-04.7

(a) $\hat v = 4V_T \times 0.02$ = **2.068** mV at the input, and **206.8** mV at the output.

(b) $\hat v = 4 \times 0.15 \times 0.02$ = **12.0** mV at the input and **240** mV at the output. The MOSFET stage takes a larger input but has less gain; at the output, the two deliver similar clean swings.

### Solution 10-04.8

(a) $\chi = 0.5/(2\sqrt{1.3})$ = **0.219** and $g_{mb}$ = **0.329** mS.

(b) Current into $R_S$ is the drain current: $v_s/R_S = g_mv_{gs} + g_{mb}v_{bs} = g_m(v_g - v_s) - g_{mb}v_s$. Collecting $v_s$: $v_s[1/R_S + g_m + g_{mb}] = g_mv_g$, which gives the stated formula. With the body effect, **0.778**; without it, $15/16$ = **0.9375**. The body effect costs 17% of the follower's gain, which is why followers in sensitive paths put the transistor in its own well with the body tied to the source (10-06).

### Solution 10-04.9

(a) $I = g_mV_T$ = **51.70** µA.

(b) $I = g_mV_{ov}/2$ = **250** µA, with $k_n = g_m/V_{ov}$ = **8.0** mA/V².

(c) $I = g_mnV_T$ = **72.39** µA.

The bipolar transistor needs a fifth of the strong-inversion current; weak inversion closes most of the gap.

### Solution 10-04.10

(a) With $x = \hat v/V_T$ and $v_{be} = \hat v\cos\omega t$, the cubic term is $I_C(x\cos\omega t)^3/6$. Since $\cos^3\theta = \tfrac34\cos\theta + \tfrac14\cos3\theta$, it contributes $I_Cx^3/24$ at $3\omega$. Against the fundamental $I_Cx$, $\text{HD}_3 = x^2/24$.

(b) $x$ = 5/25.852 = 0.1934: $\text{HD}_2 = x/4$ = **4.84**% and $\text{HD}_3$ = **0.156**%. The exact Fourier coefficients, $I_2(x)/I_1(x)$ and $I_3(x)/I_1(x)$ (the Going-deeper callout of §3.6), give **4.83**% and **0.1555**%: the first-order formulas are within 1% of themselves at this amplitude.

(c) The square law is a quadratic: $i_D = \tfrac12k_n(V_{ov} + v_{gs})^2$ has no cubic term, so no $3\omega$ component. Real MOSFETs depart from the square law through mobility degradation, velocity saturation (09-10) and channel-length modulation, all of which add higher-order terms; that is why measured CMOS amplifiers do show third-order distortion.

### Solution 10-04.11

(a) The gate is the drain, so $v_{gs} = v_{ds} = v$ and the current is $g_mv + v/r_o$: the resistance is $(1/g_m) \parallel r_o$ = 1 kΩ ∥ 40 kΩ = **975.6** Ω, close to $1/g_m$.

(b) With the base at the collector, $i = g_mv + v/r_\pi$, so the resistance is $(1/g_m) \parallel r_\pi = 1/[g_m(1 + 1/\beta)] = \alpha/g_m = r_e$ = **25.60** Ω. A diode-connected transistor looks like a resistor of about $1/g_m$: the basis of the current mirrors of 10-08.

### Solution 10-04.12

(a) $x$ = 5/25.852 = 0.1934. For +5 mV, $\Delta i_C = 1\text{ mA}(e^{x} - 1)$ = 0.2134 mA, so $\Delta v_C = -5\text{ kΩ} \times 0.2134$ mA = **−1.067** V. For −5 mV, $\Delta i_C = 1\text{ mA}(e^{-x} - 1)$ = −0.1759 mA and $\Delta v_C$ = **+0.879** V.

(b) The small-signal prediction is $\mp g_mR_C \times 5$ mV = $\mp$**0.967** V. The falling output is **10.3**% larger than predicted; the rising output is **9.08**% smaller.

(c) The output's negative half-cycles (collector falling, current rising) are stretched and its positive half-cycles compressed: an asymmetric wave whose average sits below the bias point, the signature of second-harmonic distortion. The lab's Part 2 shows it.

### Solution 10-04.13

(a)

- (i) $2/(\lambda V_{ov}) \ge 50$ gives $V_{ov} \le$ **0.4** V.
- (ii) $2\text{ mV}/(4V_{ov}) \le 0.01$ gives $V_{ov} \ge$ **0.05** V.
- (iii) $2I_D/V_{ov} \ge 1$ mS gives $V_{ov} \le$ **0.2** V.

(b) Linearity improves with overdrive, so take the largest allowed value, $V_{ov}$ = 0.2 V, set by the $g_m$ requirement. Then $k_n = 2I_D/V_{ov}^2$ = **5.0** mA/V², the intrinsic gain is $2/(0.1 \times 0.2)$ = **100** (twice the requirement) and $\text{HD}_2 = 2/(4 \times 200)$ = **0.25**% (a quarter of the limit). The $g_m$ requirement has no margin.

(c) 50 mV is below $2nV_T$ (about 67 mV for $n$ = 1.3), where the square law no longer holds (§3.7). There the device behaves exponentially, and its distortion approaches the bipolar-like $\hat v/(4nV_T)$, about 1.5% for 2 mV: the square-law bound is optimistic, and the real minimum overdrive for 1% is higher.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-04.1a | g_m | 7.736 | mS |
| 10-04.1b | r_pi | 19.39 | kΩ |
| 10-04.1c | r_e | 128.4 | Ω |
| 10-04.1d | r_o | 375 | kΩ |
| 10-04.1e | intrinsic gain | 2901 | — |
| 10-04.2a | V_ov | 0.5 | V |
| 10-04.2b | g_m | 1.0 | mS |
| 10-04.2c | r_o | 40 | kΩ |
| 10-04.2d | intrinsic gain | 40 | — |
| 10-04.2e | V_ov, doubled current | 0.707 | V |
| 10-04.2f | g_m, doubled current | 1.414 | mS |
| 10-04.2g | r_o, doubled current | 20 | kΩ |
| 10-04.2h | intrinsic gain, doubled current | 28.3 | — |
| 10-04.2i | g_m, doubled width | 2.0 | mS |
| 10-04.2j | r_o, doubled width | 20 | kΩ |
| 10-04.2k | intrinsic gain, doubled width | 40 | — |
| 10-04.4a | g_m | 19.34 | mS |
| 10-04.4b | r_pi | 4.136 | kΩ |
| 10-04.4c | r_e | 51.07 | Ω |
| 10-04.4d | (β + 1) r_e | 4.136 | kΩ |
| 10-04.5a | g_m | 77.36 | mS |
| 10-04.5b | r_pi | 1.551 | kΩ |
| 10-04.5c | R_in | 1.439 | kΩ |
| 10-04.5d | input fraction | 0.590 | — |
| 10-04.5e | r_o | 30 | kΩ |
| 10-04.5f | collector load | 1.875 | kΩ |
| 10-04.5g | gain from base | -145.1 | — |
| 10-04.5h | overall gain | -85.6 | — |
| 10-04.6a | g_m | 2.0 | mS |
| 10-04.6b | V_ov | 0.4 | V |
| 10-04.6c | gain, source grounded | -10.0 | — |
| 10-04.6d | gain, degenerated | -5.0 | — |
| 10-04.7a | BJT input amplitude | 2.068 | mV |
| 10-04.7b | BJT output amplitude | 206.8 | mV |
| 10-04.7c | MOSFET input amplitude | 12.0 | mV |
| 10-04.7d | MOSFET output amplitude | 240 | mV |
| 10-04.8a | χ | 0.219 | — |
| 10-04.8b | g_mb | 0.329 | mS |
| 10-04.8c | follower gain with body effect | 0.778 | — |
| 10-04.8d | follower gain without body effect | 0.9375 | — |
| 10-04.9a | BJT current | 51.70 | µA |
| 10-04.9b | strong-inversion current | 250 | µA |
| 10-04.9c | k_n needed | 8.0 | mA/V² |
| 10-04.9d | weak-inversion current | 72.39 | µA |
| 10-04.10a | HD2 at 5 mV | 4.84 | % |
| 10-04.10b | HD3 at 5 mV | 0.156 | % |
| 10-04.10c | exact HD2 at 5 mV | 4.83 | % |
| 10-04.10d | exact HD3 at 5 mV | 0.1555 | % |
| 10-04.11a | diode-connected MOSFET | 975.6 | Ω |
| 10-04.11b | diode-connected BJT | 25.60 | Ω |
| 10-04.12a | output change, +5 mV | -1.067 | V |
| 10-04.12b | output change, −5 mV | 0.879 | V |
| 10-04.12c | small-signal prediction | 0.967 | V |
| 10-04.12d | error, falling output | 10.3 | % |
| 10-04.12e | error, rising output | -9.08 | % |
| 10-04.13a | V_ov bound from gain | 0.4 | V |
| 10-04.13b | V_ov bound from distortion | 0.05 | V |
| 10-04.13c | V_ov bound from g_m | 0.2 | V |
| 10-04.13d | k_n | 5.0 | mA/V² |
| 10-04.13e | intrinsic gain | 100 | — |
| 10-04.13f | HD2 | 0.25 | % |
