# Solutions 10-06 · MOS Single-Stage Amplifiers

Problems: [10-06 problems](../problems/10-06-problems.md) · Chapter: [10-06](../chapters/10-06-mos-single-stage-amplifiers.md). Every number below is recomputed by [verify_10_06.py](../verify/verify_10_06.py), which solves each small-signal circuit as a nodal matrix and finds output resistances with a test source.

---

## Solutions

### Solution 10-06.1

(a) Common drain (source follower), non-inverting. (b) Common gate, non-inverting. (c) Common source, inverting. (d) Common source with degeneration, inverting, with gain reduced by about $1 + g_mR_S$.

### Solution 10-06.2

$V_{ov} = \sqrt{2 \times 0.2/2}$ = **0.4472** V; $g_m = \sqrt{2 \times 2 \times 0.2}$ = **0.8944** mS; $r_o$ = **50** kΩ; $A_v = -0.8944 \times (10 \parallel 50)$ = **−7.454**. Without $r_o$, $g_mR_D$ = **8.944**, and $V_{RD}$ = 2 V gives $2 \times 2/0.4472$ = 8.944, the same.

### Solution 10-06.3

$A_v = g_m/(g_m + g_{mb} + 1/r_o) = 3/(3 + 0.45 + 0.0333)$ = **0.8612**; $R_{out} = 1/(3.4833\text{ mS})$ = **287.1** Ω.

### Solution 10-06.4

(a) $R_D/(1/g_m + R_S) = 4$ gives $1/g_m + R_S$ = 2 kΩ, so $R_S$ = **1.5** kΩ.

(b) $g_m$ = 1.6 mS: $1/g_m$ = 625 Ω and the gain is $-8/(0.625 + 1.5)$ = **−3.765**, a change of **−5.88**%.

(c) The undegenerated stage goes from **−16** to **−12.8**, a 20% change. Degeneration cut the sensitivity to $g_m$ by the factor $1 + g_mR_S$ = 4 (to first order), in exchange for a fourfold lower gain.

### Solution 10-06.5

$R_{out} = r_o + R_S + (g_m + g_{mb})r_oR_S = 100 + 2 + 1.2 \times 100 \times 2$ = **342** kΩ; without the body effect, **302** kΩ. Here the body effect *helps*: the source moves, so the body voltage relative to the source changes, adding to the feedback that opposes current changes.

### Solution 10-06.6

(a) $R_{in} = 1/(1.2\text{ mS})$ = **833.3** Ω.

(b) The sensor current divides between 1 MΩ and 833 Ω: $1/(1 + 833.3/10^6)$ = **0.9992** enters the stage.

(c) The CG stage passes its input current to the drain with unity current gain, so $v_{out}/i_{sig} = 0.9992 \times 20$ kΩ = **19.98** mV/µA.

(d) Directly across 20 kΩ, the sensor sees 1 MΩ ∥ 20 kΩ = **19.61** kΩ: almost the same gain here. The CG stage's advantage is not gain but isolation: the sensor sees 833 Ω instead of 20 kΩ, so its voltage barely moves (useful against its own capacitance, Course 12), and the output resistance and load can be changed without disturbing the sensor.

### Solution 10-06.7

Active load: $-1 \times (50 \parallel 40)$ = **−22.22**. Resistor: $-1 \times (10 \parallel 50)$ = **−8.333**. The 10 kΩ resistor drops 1 V at 100 µA; the PMOS needs only 0.2 V, yet gives 2.7 times the gain. That is the case for active loads.

### Solution 10-06.8

$R_{in} = (r_o + R_D)/(1 + (g_m + g_{mb})r_o) = (40 + R_D)\text{ kΩ}/97$: **412.4** Ω, **824.7** Ω and **4536** Ω. With an ideal current-source load, $R_{in} \to \infty$: no signal current can flow through a stage whose drain cannot accept any, so the source voltage follows the input with no current. In practice the load is the output resistance of another stage, and the input resistance is finite but can be far above $1/g_m$.

### Solution 10-06.9

(a) Let $T = g_mR_S$ and write the incremental drain current $i = g_mv_{gs} + \tfrac12k_nv_{gs}^2$ with $v_{gs} = v_{in} - iR_S$. To first order, $i_1 = g_mv_{in}/(1 + T)$ and $v_{gs1} = v_{in}/(1 + T)$. The second-order part $i_2$ satisfies $i_2 = g_m(-i_2R_S) + \tfrac12k_nv_{gs1}^2$, so $i_2 = \tfrac12k_nv_{in}^2/(1 + T)^3$. For $v_{in} = \hat v\cos\omega t$, the second harmonic of $i_2$ has amplitude $k_n\hat v^2/[4(1 + T)^3]$ and the fundamental $g_m\hat v/(1 + T)$, so

$$
\text{HD}_2 = \frac{k_n\hat v}{4g_m(1 + T)^2} = \frac{\hat v}{4V_{ov}(1 + T)^2} .
$$

(b) **2.5**% and **0.625**%.

(c) $\hat v$ = 100 mV: **1.25**%. At the same output amplitude, degeneration halves the distortion here ($1/(1 + T)$), and at the same input it quarters it.

(d) The perturbation keeps only the leading term; the exact square law with feedback generates higher-order terms that add slightly to the second harmonic (and create a small third harmonic, which the undegenerated square law does not have).

### Solution 10-06.10

(a) $r_o + r_o + (g_m + g_{mb})r_o^2 = 40 + 40 + 2.4 \times 1600$ = **3920** kΩ.

(b) The lower device's drain voltage is $-g_mr_ov_{in}$, multiplied by $1 + (g_m + g_{mb})r_o$ = 97 at the output: $A_v = -80 \times 97$ = **−7760**. The body effect of the upper device raises both by about 20% over Example 10-06.7.

### Solution 10-06.11

(a) $2 \times 0.45/0.15$ = **6.0**. (b) $V_{ov} = 2 \times 0.45/10$ = **0.09** V. (c) No: 90 mV is close to $2nV_T$ (about 67 mV for $n$ = 1.3), where the device is in moderate inversion and $g_m/I_D$ is below the square law's $2/V_{ov}$ (10-04 §3.7). The real gain would be lower than 10; low-voltage designs reach gain with active loads instead.

### Solution 10-06.12

(a) $R_{eq} = (1/g_{mb}) \parallel 50 = 250 \parallel 50$ = **41.67** Ω; the follower gain $A_f = g_mR_{eq}/(1 + g_mR_{eq}) = 20 \times 0.04167/(1 + 20 \times 0.04167)$ = **0.4545**; $R_{out} = 1/(g_m + g_{mb})$ = **41.67** Ω.

(b) $-10 \times 0.4545$ = **−4.545**.

(c) $10/0.4545$ = **22.0**. A 50 Ω load is heavy even for a 20 mS follower: its output resistance is comparable to the load. Driving 50 Ω efficiently needs more current or a different output stage (12-07).

### Solution 10-06.13

(a) $V_G = 5 \times 100/400$ = **1.25** V. With $I_D = \tfrac12k_nV_{ov}^2$ and $V_G = V_{GS} + I_DR_S$, writing $V_{GS} = 0.5 + V_{ov}$: $1.25 = 0.5 + V_{ov} + 1\text{ kΩ} \times 1\text{ mA/V}^2 \times V_{ov}^2$, i.e. $V_{ov}^2 + V_{ov} - 0.75 = 0$, so $V_{ov}$ = **0.5** V (the other root is negative) and $I_D$ = **0.25** mA. Then $V_S$ = 0.25 V, $V_D = 5 - 0.25 \times 5$ = 3.75 V and $V_{DS}$ = **3.5** V, well above $V_{ov}$: saturated.

(b) $g_m = 2I_D/V_{ov}$ = **1.0** mS; $r_o = 1/(0.02 \times 0.25\text{ mA})$ = **200** kΩ.

(c) $R_{in} = R_1 \parallel R_2$ = **75** kΩ. The drain sees $R_D \parallel R_L \parallel r_o = 5 \parallel 10 \parallel 200$ = 3.279 kΩ, so the gain from the gate is **−3.279**, and with the input divider $75/85$ the overall gain is **−2.893**. The bias step fixes $g_m$; every small-signal number follows from it, which is why a bias error carries straight into the gain.

### Solution 10-06.14

(a) M1's drain current $g_{m1}v_{in}$ flows down through M2. M2's gate and drain are at the supply (AC ground), so its small-signal current is $-(g_{m2} + g_{mb2})v_o = -g_{m2}(1 + \chi)v_o$ flowing *up* from the output. Equating, $g_{m1}v_{in} = -g_{m2}(1 + \chi)v_o$:

$$
A_v = -\frac{g_{m1}}{g_{m2}(1 + \chi)} = -\frac{1}{1 + \chi}\sqrt{\frac{k_{n1}}{k_{n2}}} ,
$$

since both carry the same current and $g_m = \sqrt{2k_nI_D}$. The diode-connected load looks like a resistance $1/[g_{m2}(1 + \chi)]$.

(b) $g_{m1}$ = **2.0** mS and $g_{m2}$ = **1.0** mS, so $A_v = -2/1.2$ = **−1.667**. Overdrives: $V_{ov1} = \sqrt{2I_D/k_{n1}}$ = **0.5** V and $V_{ov2}$ = **1.0** V.

(c) $\sqrt{k_{n1}/k_{n2}} = 5 \times 1.2 = 6$, so $k_{n1}/k_{n2}$ = **36**: $k_{n2}$ = 0.111 mA/V² and $V_{ov2} = \sqrt{2 \times 0.5/0.111}$ = **3.0** V. The gain is set by a size ratio, so it is insensitive to bias current and tracks process, which is the attraction; but each factor in gain costs its square in size ratio and multiplies M2's overdrive, which eats the headroom. A diode-connected load suits gains of a few at most.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-06.2a | V_ov | 0.4472 | V |
| 10-06.2b | g_m | 0.8944 | mS |
| 10-06.2c | r_o | 50 | kΩ |
| 10-06.2d | gain | -7.454 | — |
| 10-06.2e | g_m R_D | 8.944 | — |
| 10-06.3a | follower gain | 0.8612 | — |
| 10-06.3b | output resistance | 287.1 | Ω |
| 10-06.4a | R_S | 1.5 | kΩ |
| 10-06.4b | gain after the shift | -3.765 | — |
| 10-06.4c | change | -5.88 | % |
| 10-06.4d | undegenerated gain | -16 | — |
| 10-06.4e | undegenerated gain after the shift | -12.8 | — |
| 10-06.5a | R_out with body effect | 342 | kΩ |
| 10-06.5b | R_out without body effect | 302 | kΩ |
| 10-06.6a | R_in | 833.3 | Ω |
| 10-06.6b | fraction entering | 0.9992 | — |
| 10-06.6c | output per µA | 19.98 | mV/µA |
| 10-06.6d | direct resistance | 19.61 | kΩ |
| 10-06.7a | active-load gain | -22.22 | — |
| 10-06.7b | resistor-load gain | -8.333 | — |
| 10-06.8a | R_in, R_D = 0 | 412.4 | Ω |
| 10-06.8b | R_in, R_D = 40 kΩ | 824.7 | Ω |
| 10-06.8c | R_in, R_D = 400 kΩ | 4536 | Ω |
| 10-06.9a | HD2, no degeneration | 2.5 | % |
| 10-06.9b | HD2, g_m R_S = 1 | 0.625 | % |
| 10-06.9c | HD2, doubled input | 1.25 | % |
| 10-06.9d | exact HD2, (b) | 0.626 | % |
| 10-06.9e | exact HD2, (c) | 1.255 | % |
| 10-06.10a | cascode R_out | 3920 | kΩ |
| 10-06.10b | cascode gain | -7760 | — |
| 10-06.11a | gain | 6.0 | — |
| 10-06.11b | overdrive for gain 10 | 0.09 | V |
| 10-06.12a | R_eq | 41.67 | Ω |
| 10-06.12b | follower gain | 0.4545 | — |
| 10-06.12c | follower R_out | 41.67 | Ω |
| 10-06.12d | overall gain | -4.545 | — |
| 10-06.12e | CS gain needed | 22.0 | — |
| 10-06.13a | V_G | 1.25 | V |
| 10-06.13b | V_ov | 0.5 | V |
| 10-06.13c | I_D | 0.25 | mA |
| 10-06.13d | V_DS | 3.5 | V |
| 10-06.13e | g_m | 1.0 | mS |
| 10-06.13f | r_o | 200 | kΩ |
| 10-06.13g | R_in | 75 | kΩ |
| 10-06.13h | gain from the gate | -3.279 | — |
| 10-06.13i | overall gain | -2.893 | — |
| 10-06.14a | g_m1 | 2.0 | mS |
| 10-06.14b | g_m2 | 1.0 | mS |
| 10-06.14c | gain | -1.667 | — |
| 10-06.14d | V_ov1 | 0.5 | V |
| 10-06.14e | V_ov2 | 1.0 | V |
| 10-06.14f | size ratio for gain −5 | 36 | — |
| 10-06.14g | V_ov2 for gain −5 | 3.0 | V |
