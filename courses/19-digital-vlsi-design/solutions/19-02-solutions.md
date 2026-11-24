# Solutions 19-02 · The CMOS Inverter: Dynamic Behavior and Delay

Problems: [19-02 problem set](../problems/19-02-problems.md) · Chapter: [19-02](../chapters/19-02-cmos-inverter-dynamic.md). Every number below is recomputed by [verify_19_02.py](../verify/verify_19_02.py).

---

## Solutions

### Solution 19-02.1

$C_g = 1.2 \times (0.3 + 0.6)$ = **1.08** fF and $C_{int} = 1.0 \times 0.9$ = **0.90** fF. The external load is $3 \times 1.08 + 1.5$ = **4.74** fF, so $C_L$ = **5.64** fF, and γ = 0.90/1.08 = **0.833**. As in Example 19-02.1, the fan-out is most of the load.

### Solution 19-02.2

(a) $C_{int} = C_{dn} + C_{dp} + 2(C_{gdn} + C_{gdp}) = 0.3 + 0.3 + 2 \times 0.2$ = **1.0** fF.

(b) Counting $C_{gd}$ once gives **0.8** fF, 20% low.

(c) $C_{gd}$ connects the input to the output. During the transition the input rises by $V_{DD}$ while the output falls by $V_{DD}$, so the charge it takes is $C_{gd} \cdot 2V_{DD}$. To the output, that looks like a capacitance of $2C_{gd}$ to a fixed node: the Miller effect for a gain of −1 (12-03).

### Solution 19-02.3

(a) $t_p = 1/(2Nf) = 1/(2 \times 31 \times 450\ \text{MHz})$ = **35.8** ps.

(b) $f = 1/(2 \times 51 \times 35.84\ \text{ps})$ = **273.5** MHz, smaller by the factor 31/51. Test chips use long rings so that the frequency is low enough to measure easily off chip.

### Solution 19-02.4

$V_{ov}$ = 0.7 V and $I_{sat} = \tfrac12 \times 300\ \mu\text{A/V}^2 \times 0.49$ = 73.5 µA. The NMOS stays saturated until the output has fallen by $V_{TN}$ = 0.3 V:

$$
t_1 = \frac{C_LV_{TN}}{I_{sat}} = \frac{15\ \text{fF} \times 0.3\ \text{V}}{73.5\ \mu\text{A}} = \mathbf{61.2}\ \text{ps}.
$$

In the linear region, from 0.7 V to 0.5 V:

$$
t_2 = \frac{C_L}{k_nV_{ov}}\ln\left(\frac{4V_{ov}}{V_{DD}} - 1\right) = 71.43\ \text{ps} \times \ln 1.8 = \mathbf{42.0}\ \text{ps},
$$

so $t_{pHL}$ = **103.2** ps. Units: F·V/A = s.

### Solution 19-02.5

(a) Numerically, $R_{eq} = \dfrac{1}{0.5\ \text{V}}\displaystyle\int_{0.5}^{1.0}\frac{V}{I_D(V)}dV$ = **10.29** kΩ (Problem 10's closed form gives the same). The approximation is $3 \times 1.0/(4 \times 73.5\ \mu\text{A})$ = **10.20** kΩ.

(b) $\ln 2 \times 10.29\ \text{kΩ} \times 15\ \text{fF}$ = **107.0** ps, **3.7** % above the exact 103.2 ps.

(c) With 10.20 kΩ, **106.1** ps, 2.8% high. The approximation happens to land closer, because its error partly cancels the RC model's.

### Solution 19-02.6

(a) $t_p = (40 + 100)/2$ = **70** ps.

(b) The PMOS resistance falls by 2.5, so $t_{pLH}$ = 100/2.5 = **40** ps, and $t_p$ = **40** ps. With the load fixed and the inverter's own capacitance negligible, nothing is lost.

(c) The input capacitance is proportional to $W_n + W_p$: from $2W$ to $3.5W$, a factor of **1.75**. The gate driving this inverter pays, because its load grew. Problem 11 shows that, once the inverter's own capacitance and its fan-out's grow with the PMOS too, equal rise and fall is no longer optimal.

### Solution 19-02.7

(a) $t_{p0} = \ln 2 \times 10\ \text{kΩ} \times 1.5\ \text{fF}$ = **10.4** ps.

(b) γ = 1.5/2 = **0.75**, and $t_{FO4} = t_{p0}(1 + 4/\gamma) = 10.40 \times 6.333$ = **65.8** ps.

(c) $t_p = 10.40 \times (1 + 100/1.5)$ = **703.5** ps.

(d) $10.40 \times (1 + 100/15)$ = **79.7** ps, nearly nine times faster, but the input capacitance is now **20** fF. Driving 20 fF is itself a load: 19-04 shows how to split a large fan-out across a chain of progressively larger stages.

### Solution 19-02.8

(a) $t_p = 1/(2 \times 101 \times 150\ \text{MHz})$ = **33.0** ps.

(b) With γ = 1, an FO1 inverter has $t_p = t_{p0}(1 + 1)$, so $t_{p0}$ = 16.5 ps and $t_{FO4} = 5t_{p0}$ = **82.5** ps.

(c) $3 \times 33.0$ = **99.0** ps.

(d) $(1 + 4/\gamma) = 3(1 + 1/\gamma)$ gives $1/\gamma$ = 2, so γ = **0.5**. The two estimates differ by 20%, which is about as well as a rule of thumb can do; the ring's stage delay also includes the input-slope effect of §3.6.

### Solution 19-02.9

(a) The delay ratio is

$$
\frac{0.5/(0.2)^{1.4}}{0.9/(0.6)^{1.4}} = \frac{0.5}{0.9}\times 3^{1.4} = 0.5556 \times 4.656 = \mathbf{2.59}.
$$

(b) $(0.5/0.9)^2$ = **0.309**: the energy falls by a factor of 3.24.

(c) The EDP ratio is $0.309 \times 2.59$ = **0.798**, 20% lower: at α = 1.4 the energy saving outweighs the slowdown.

(d) $3V_{TH}/(3 - \alpha) = 0.9/1.6$ = **0.5625** V, close to the new supply.

### Solution 19-02.10

(a) Split the integral at $V_{ov}$. Above it the transistor is saturated, $I = I_{sat} = \tfrac12kV_{ov}^2$:

$$
\int_{V_{ov}}^{V_{DD}}\frac{V}{I_{sat}}\,dV = \frac{V_{DD}^2 - V_{ov}^2}{2I_{sat}} = \frac{V_{DD}^2 - V_{ov}^2}{kV_{ov}^2} .
$$

Below it, $I = k(V_{ov}V - V^2/2)$, so $V/I = 1/[k(V_{ov} - V/2)]$:

$$
\int_{V_{DD}/2}^{V_{ov}}\frac{dV}{k(V_{ov} - V/2)} = \frac2k\ln\frac{V_{ov} - V_{DD}/4}{V_{ov}/2} = \frac2k\ln\frac{4V_{ov} - V_{DD}}{2V_{ov}} .
$$

Dividing the sum by the interval $V_{DD}/2$ gives the stated result. Units: $(V_{DD}^2 - V_{ov}^2)/(kV_{ov}^2)$ has units V²/(A/V² · V²) = V²/A, and multiplied by $2/V_{DD}$ it is V/A = Ω.

(b) $(1.44 - 0.7225)/(200\ \mu \times 0.7225)$ = 4965 Ω; $\ln(2.2/1.7) = 0.2578$, times $2/k$ = 2578 Ω; the sum, 7544 Ω, times $2/1.2$, is **12.57** kΩ.

(c) Both delays are proportional to $C/(k\,V_{DD})$ times a function of $V_{TN}/V_{DD}$, so their ratio depends only on that ratio: **1.032** at 0.2 and **1.039** at 0.4. The RC model is 3–4% pessimistic over the whole practical range, a consistent bias that does not matter when comparing designs.

### Solution 19-02.11

(a) Let a unit-width NMOS have resistance $R_n$ and gate capacitance $C'$, with self-loading $\gamma C'$ per unit width. The inverter's input capacitance is $C'W_n(1 + \beta)$, and its load, its own drains plus $N$ copies of itself, is $(\gamma + N)C'W_n(1 + \beta)$. The pull-down resistance is $R_n/W_n$ and the pull-up $rR_n/(\beta W_n)$, so

$$
t_p = \frac{0.69}{2}\,\frac{R_n}{W_n}\left(1 + \frac r\beta\right)(\gamma + N)C'W_n(1 + \beta) \propto (1 + \beta)\left(1 + \frac r\beta\right) = 1 + r + \beta + \frac r\beta .
$$

Setting the derivative $1 - r/\beta^2$ to zero gives $\beta_{opt} = \sqrt r$.

(b) $\beta_{opt} = \sqrt{2.5}$ = **1.58**. The delay factor is $(1 + 1.581)^2$ = 6.66, against $3.5 \times 2$ = 7 for β = 2.5 and $2 \times 3.5$ = 7 for β = 1: the optimum is **4.8** % faster than either.

(c) Widening the PMOS speeds up the rising edge but adds capacitance that slows both edges, its own and its fan-out's. At equal rise and fall the last increment of width costs more on the falling edge than it gains on the rising one. The minimum is shallow, which is why libraries often choose β between 1 and $r$ for area or noise-margin reasons (19-01 §3.2).

### Solution 19-02.12

(a) $\ln(E\,D^n) = (2 + n)\ln V_{DD} - n\alpha\ln(V_{DD} - V_{TH})$ plus a constant. The derivative is zero when $(2 + n)/V_{DD} = n\alpha/(V_{DD} - V_{TH})$, that is $V_{DD}(2 + n - n\alpha) = (2 + n)V_{TH}$, which has a positive solution above $V_{TH}$ only if $2 + n > n\alpha$. For $n$ = 1 it is the chapter's $3V_{TH}/(3 - \alpha)$.

(b) $n$ = 1: **0.618** V; $n$ = 2: $4 \times 0.35/1.4$ = **1.00** V; $n$ = 3: $5 \times 0.35/1.1$ = **1.59** V.

(c) For α = 2 and $n$ = 2, $2 + n - n\alpha$ = 0: $E\,D^2 \propto [V_{DD}/(V_{DD} - V_{TH})]^4$ falls monotonically toward a constant as the supply rises, so there is no interior optimum. The more a metric weights delay, the higher its optimal supply; a designer who values speed above all runs at the highest supply that reliability and power delivery allow, which is why turbo modes exist (19-06).

### Solution 19-02.13

(a) Per micrometre of width, the channel gives $8.5 \times 0.15 = 1.275$ fF and the two overlaps 0.6 fF, 1.875 fF/µm in all. With 1.5 µm of total width, $C_g$ = **2.81** fF.

(b) NMOS: bottom $0.5 \times 0.5 \times 1.0 \times 0.62 = 0.155$ fF; sidewall $(2 \times 0.5 + 0.5) \times 0.25 \times 0.75 = 0.281$ fF; Miller overlap $2 \times 0.3 \times 0.5 = 0.3$ fF; total **0.736** fF. PMOS: bottom $1.0 \times 0.5 \times 0.62 = 0.31$ fF; sidewall $(2 \times 0.5 + 1.0) \times 0.25 \times 0.75 = 0.375$ fF; overlap 0.6 fF; total **1.285** fF. $C_{int}$ = **2.02** fF.

(c) γ = 2.021/2.8125 = **0.719**, between the textbook 1 and the 0.5 that the FO1/FO4 rule implies (§3.5). FO4 load: $C_{int} + 4C_g$ = **13.27** fF.

Units: fF/µm² × µm² = fF, and fF/µm × µm = fF.

### Solution 19-02.14

$V_{ov}$ = 0.85 V and $kV_{ov}^2/2$ = 72.25 µA. The output stays in saturation until it falls to $V_{ov}$ (by $V_{TN}$ from the top), discharging at a constant current; below $V_{ov}$ the linear-region integral of §3.3 gives $t = \frac{C}{kV_{ov}}\ln\frac{2V_{ov} - V}{V}$ measured from the end of saturation.

- 90 % (1.08 V) is still in saturation: $t_{90} = 20\ \text{fF} \times 0.12\ \text{V}/72.25\ \mu\text{A}$ = **33.2** ps.
- End of saturation: $20\ \text{fF} \times 0.35/72.25\ \mu\text{A}$ = 96.9 ps. Then to 10 % (0.12 V): $\frac{20\ \text{fF}}{170\ \mu\text{A/V}}\ln\frac{1.70 - 0.12}{0.12} = 117.6 \times 2.578$ = 303.3 ps, so $t_{10}$ = **400.1** ps.

The fall time is $400.1 - 33.2$ = **366.9** ps, **2.18** times $t_{pHL}$ = 168.2 ps. The RC model gives $\ln 9 \times 12.573\ \text{kΩ} \times 20\ \text{fF}$ = **552.5** ps, **51** % too long. $R_{eq}$ was fitted to reproduce the 50 % crossing; the real discharge is a constant current at first and an exponential only near the end, so the single pole stretches the edge. Use $R_{eq}$ for delays, and the device equations (or the library's transition tables, 19-10) for slews.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-02.1a | input capacitance | 1.08 | fF |
| 19-02.1b | intrinsic capacitance | 0.90 | fF |
| 19-02.1c | external load | 4.74 | fF |
| 19-02.1d | total load | 5.64 | fF |
| 19-02.1e | gamma | 0.833 | — |
| 19-02.2a | intrinsic capacitance with Miller doubling | 1.0 | fF |
| 19-02.2b | intrinsic capacitance without it | 0.8 | fF |
| 19-02.3a | stage delay, 31 stages at 450 MHz | 35.8 | ps |
| 19-02.3b | frequency with 51 stages | 273.5 | MHz |
| 19-02.4a | time in saturation | 61.2 | ps |
| 19-02.4b | time in the linear region | 42.0 | ps |
| 19-02.4c | t_pHL | 103.2 | ps |
| 19-02.5a | R_eq by averaging | 10.29 | kΩ |
| 19-02.5b | R_eq approximation | 10.20 | kΩ |
| 19-02.5c | RC-model delay | 107.0 | ps |
| 19-02.5d | RC-model error | 3.7 | % |
| 19-02.5e | RC-model delay with the approximate R_eq | 106.1 | ps |
| 19-02.5f | its error | 2.8 | % |
| 19-02.6a | t_p with equal widths | 70 | ps |
| 19-02.6b | t_pLH with the PMOS 2.5 times wider | 40 | ps |
| 19-02.6c | t_p with the PMOS 2.5 times wider | 40 | ps |
| 19-02.6d | input capacitance growth | 1.75 | — |
| 19-02.7a | intrinsic delay | 10.4 | ps |
| 19-02.7b | gamma | 0.75 | — |
| 19-02.7c | FO4 delay | 65.8 | ps |
| 19-02.7d | delay driving 100 fF | 703.5 | ps |
| 19-02.7e | delay driving 100 fF at ten times the size | 79.7 | ps |
| 19-02.7f | input capacitance at ten times the size | 20 | fF |
| 19-02.8a | FO1 stage delay | 33.0 | ps |
| 19-02.8b | FO4 estimate, gamma = 1 | 82.5 | ps |
| 19-02.8c | FO4 estimate, FO1 = FO4/3 | 99.0 | ps |
| 19-02.8d | implied gamma | 0.5 | — |
| 19-02.9a | delay ratio, 0.5 V to 0.9 V | 2.59 | — |
| 19-02.9b | energy ratio | 0.309 | — |
| 19-02.9e | energy reduction factor | 3.24 | — |
| 19-02.9c | EDP ratio | 0.798 | — |
| 19-02.9d | EDP-optimal supply | 0.5625 | V |
| 19-02.10a | R_eq from the closed form | 12.57 | kΩ |
| 19-02.10b | RC over exact delay, V_TN/V_DD = 0.2 | 1.032 | — |
| 19-02.10c | RC over exact delay, V_TN/V_DD = 0.4 | 1.039 | — |
| 19-02.11a | delay-optimal Wp/Wn, r = 2.5 | 1.58 | — |
| 19-02.11b | speed gain over beta = r | 4.8 | % |
| 19-02.11c | delay factor at the optimum | 6.66 | — |
| 19-02.12a | optimal supply for E D | 0.618 | V |
| 19-02.12b | optimal supply for E D squared | 1.00 | V |
| 19-02.12c | optimal supply for E D cubed | 1.59 | V |
| 19-02.13a | input capacitance | 2.81 | fF |
| 19-02.13b | NMOS self-loading | 0.736 | fF |
| 19-02.13c | PMOS self-loading | 1.285 | fF |
| 19-02.13d | total self-loading | 2.02 | fF |
| 19-02.13e | gamma | 0.719 | — |
| 19-02.13f | FO4 load capacitance | 13.27 | fF |
| 19-02.14a | time to 90 percent | 33.2 | ps |
| 19-02.14b | time to 10 percent | 400.1 | ps |
| 19-02.14c | 90-10 fall time | 366.9 | ps |
| 19-02.14d | fall time over t_pHL | 2.18 | — |
| 19-02.14e | RC-model fall time | 552.5 | ps |
| 19-02.14f | RC-model overestimate | 51 | % |
