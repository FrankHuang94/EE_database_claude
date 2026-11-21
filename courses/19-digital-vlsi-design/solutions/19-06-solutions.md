# Solutions 19-06 · Power and Low-Power Design

Problems: [19-06 problem set](../problems/19-06-problems.md) · Chapter: [19-06](../chapters/19-06-power-and-low-power-design.md). Every number below is recomputed by [verify_19_06.py](../verify/verify_19_06.py).

---

## Solutions

### Solution 19-06.1

$CV^2 = 5\ \text{fF} \times 0.81$ = **4.05** fJ per full cycle, of which **2.025** fJ is dissipated while charging. $P = 0.15 \times 5\ \text{fF} \times 0.81 \times 1.5\ \text{GHz}$ = **0.911** µW.

### Solution 19-06.2

(a) α = 1: $200\ \text{pF} \times 0.81 \times 2\ \text{GHz}$ = **0.324** W.

(b) **0.130** W saved. Clock gating also stops the logic behind the gated registers from switching, so the total saving is usually larger.

### Solution 19-06.3

$S = nV_{th}\ln 10$: **83.3** mV/decade at 300 K and, scaling with absolute temperature, **105.6** mV/decade at 380 K. A hot chip needs more gate voltage per decade of current, which is one reason leakage grows with temperature.

### Solution 19-06.4

(a) $P_{sc}$ scales with τ: $4 \times 0.104$ = **0.417** µW, **5.8** % of the dynamic power. Slow edges matter; this is why libraries constrain maximum transition times (19-02).

(b) $(0.8 - 0.7)^3/(0.5)^3 = 1/125$: **0.00333** µW. Near $2V_T$ the overlap window almost closes.

### Solution 19-06.5

At 380 K, $V_T = 0.35 - 0.8\ \text{mV/K} \times 80\ \text{K}$ = 0.286 V and $nV_{th} = 1.3 \times 32.75$ mV = 42.57 mV. The ratio is $\exp(-0.286/0.04257 + 0.35/0.03361)$ = **40.3**. Under these assumptions leakage rises forty-fold from room temperature to 107 °C; with a temperature-dependent $I_0$ the real figure differs, but the conclusion holds: leakage must be signed off hot.

### Solution 19-06.6

Balancing the two currents as in Example 4: η = 0.05 gives **50.2** mV and a **4.80** times reduction; η = 0.2 gives **143.0** mV and a **164.7** times reduction. The stronger the DIBL, the more the single device benefits from its full drain bias, and the more the stack gains by denying it.

### Solution 19-06.7

Solving $V/(V - 0.35)^{1.3} = 3/(0.65)^{1.3}$: $V$ = **0.518** V. Power relative to full speed: $(0.518)^2/3$ = **0.0896**; energy per operation: $(0.518)^2$ = **0.269**.

### Solution 19-06.8

(a) Recharging from the supply costs $CV^2 = 500\ \text{pF} \times 0.64$ = 0.32 nJ, plus 0.08 nJ: **0.40** nJ.

(b) $0.40\ \text{nJ}/2\ \text{mW}$ = **200** ns.

(c) The saved leakage is 1.98 mW: **202** ns. Sleeping for less than about 200 ns costs energy; power managers use idle-time prediction to decide.

### Solution 19-06.9

$0.9 + 0.1 \times 12.9$ = **2.19** times, and $0.7 + 0.3 \times 12.9$ = **4.57** times. A small share of low-threshold cells dominates the leakage, which is why timing closure tries to use as few as possible.

### Solution 19-06.10

(a) For an unloaded inverter the output follows the static transfer curve. Below $V_{DD}/2$ the NMOS is saturated (region B of 19-01) and the current is its saturation current $\tfrac12\beta(v_{in} - V_T)^2$; above, the PMOS's, symmetrically. With $v_{in} = V_{DD}t/\tau$, $dt = (\tau/V_{DD})dv$, so

$$
Q = 2\int_{V_T}^{V_{DD}/2}\tfrac12\beta(v - V_T)^2\,\frac{\tau}{V_{DD}}\,dv = \frac{\beta\tau}{3V_{DD}}\left(\frac{V_{DD}}2 - V_T\right)^3 = \frac{\beta\tau(V_{DD} - 2V_T)^3}{24V_{DD}} .
$$

It is exact because no capacitance delays the output: the static curve, and hence the current, holds at every instant (λ = 0).

(b) $Q = 100\ \mu \times 100\ \text{ps} \times 0.4^3/24$ = **0.0267** fC.

### Solution 19-06.11

(a) At the minimum, $L_de^{-x}(x - 2) = 2\alpha$, so $L_de^{-x} = 2\alpha/(x - 2)$. The leakage share is $L_de^{-x}/(\alpha + L_de^{-x}) = [2/(x-2)]/[1 + 2/(x-2)] = 2/x$.

(b) Dividing the optimality condition by α gives $(L_d/\alpha)e^{-x}(x - 2) = 2$: only the ratio appears.

(c) $L_d/\alpha$ = 500, the same as Example 6's α = 0.1 and $L_d$ = 50: $x$ = **7.16** and $V_{min}$ = **241** mV.

### Solution 19-06.12

(a) Two-way parallelism at 0.611 V uses $(1 + o) \times 0.611^2$ of the power, which is below 1 while $o <$ **1.68**: even 168% capacitance overhead would break even.

(b) Each copy at a quarter of the frequency: $V$ = **0.477** V. Power ratio $(0.477)^2$ = **0.227** with no overhead and **0.295** with 30%. The returns diminish as $V$ approaches $V_T$, and the area grows four-fold.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-06.1a | energy per full cycle | 4.05 | fJ |
| 19-06.1b | dissipated while charging | 2.025 | fJ |
| 19-06.1c | average power | 0.911 | µW |
| 19-06.2a | clock power | 0.324 | W |
| 19-06.2b | clock-gating saving | 0.130 | W |
| 19-06.3a | slope at 300 K | 83.3 | mV/decade |
| 19-06.3b | slope at 380 K | 105.6 | mV/decade |
| 19-06.4a | short-circuit power, 200 ps ramps | 0.417 | µW |
| 19-06.4b | share of dynamic power | 5.8 | % |
| 19-06.4c | short-circuit power at 0.8 V | 0.00333 | µW |
| 19-06.5a | off-current ratio, 380 K over 300 K | 40.3 | — |
| 19-06.6a | stack node, eta = 0.05 | 50.2 | mV |
| 19-06.6b | reduction, eta = 0.05 | 4.80 | — |
| 19-06.6c | stack node, eta = 0.2 | 143.0 | mV |
| 19-06.6d | reduction, eta = 0.2 | 164.7 | — |
| 19-06.7a | supply for one-third frequency | 0.518 | V |
| 19-06.7b | power ratio | 0.0896 | — |
| 19-06.7c | energy per operation ratio | 0.269 | — |
| 19-06.8a | wake-up energy | 0.40 | nJ |
| 19-06.8b | break-even time | 200 | ns |
| 19-06.8c | break-even with residual leakage | 202 | ns |
| 19-06.9a | leakage factor, 10% low-threshold | 2.19 | — |
| 19-06.9b | leakage factor, 30% low-threshold | 4.57 | — |
| 19-06.10a | short-circuit charge per transition | 0.0267 | fC |
| 19-06.11a | normalized optimum x | 7.16 | — |
| 19-06.11b | minimum-energy supply | 241 | mV |
| 19-06.12a | break-even overhead | 1.68 | — |
| 19-06.12b | supply for four-way parallelism | 0.477 | V |
| 19-06.12c | power ratio, no overhead | 0.227 | — |
| 19-06.12d | power ratio, 30% overhead | 0.295 | — |
