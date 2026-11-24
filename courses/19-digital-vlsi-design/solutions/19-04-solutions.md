# Solutions 19-04 · Transistor Sizing and Logical Effort

Problems: [19-04 problem set](../problems/19-04-problems.md) · Chapter: [19-04](../chapters/19-04-sizing-and-logical-effort.md). Every number below is recomputed by [verify_19_04.py](../verify/verify_19_04.py).

---

## Solutions

### Solution 19-04.1

$h$ = 3 in each case. NAND3: $\tfrac53 \times 3 + 3$ = **8**. NOR3: $\tfrac73 \times 3 + 3$ = **10**. NAND4: $2 \times 3 + 4$ = **10**. The NAND4 matches the NOR3: its smaller logical effort is offset by its larger parasitic delay.

### Solution 19-04.2

$G = 1 \times \tfrac43 \times 1$ = **1.33**, $F = GH = \tfrac43 \times 12$ = **16**, $\hat f = 16^{1/3}$ = **2.52**, and $P = 1 + 2 + 1$ = 4, so $\hat D = 3 \times 2.52 + 4$ = **11.56**. The stage effort is below 4 because the path has more stages than its effort needs; with $F$ = 16 two stages would be ideal, but the function needs three.

### Solution 19-04.3

(a) $b = (1 + 2)/1$ = **3**: the gate drives three equal inputs, one on the path.

(b) $b = (1 + 2 + 1)/1$ = **4**. A fixed wire is off-path capacitance like any other; unlike a gate input it does not scale when the path is resized, so in practice it is counted with the load it is attached to (19-05).

### Solution 19-04.4

$G = \tfrac53 \times \tfrac53 \times 1$ = **2.78**, $H$ = 120/6 = 20, $F$ = **55.6**, $\hat f = 55.6^{1/3}$ = **3.82**, $P$ = 3 + 2 + 1 = 6, $\hat D = 3 \times 3.82 + 6$ = **17.45**.

Backward: inverter $C_{in}$ = 120/3.82 = **31.4**; NOR2 $C_{in} = \tfrac53 \times 31.4/3.82$ = **13.7**; NAND3 $C_{in} = \tfrac53 \times 13.7/3.82$ = **6.0**, matching the given input.

### Solution 19-04.5

$H$ = 2000/3 = **667**. $\hat N = \ln 667/\ln 3.59$ = **5.09**. Four stages: $4 \times 667^{1/4} + 4$ = **24.33**; five: $5 \times 667^{1/5} + 5$ = **23.35**; six: **23.73**. Five stages are best: 23.35 × 15 ps = **350.3** ps. If the clock must arrive uninverted, four or six stages cost about 4% or 2% more.

### Solution 19-04.6

(a) $d = \tfrac43 \times 50 + 2$ = **68.67**.

(b) $F = \tfrac43 \times 50$ = 66.7; two stages: $2\sqrt{66.7} + 3$ = **19.33**.

(c) Three stages: $3 \times 66.7^{1/3} + 4$ = **16.16**, with stage effort **4.05**, almost exactly the rule of thumb.

### Solution 19-04.7

Unit-sized stages see electrical efforts 1, 1 and 64: $D = (1 + 1) + (1 + 1) + (64 + 1)$ = **69** τ, more than the single inverter's 65 and **4.6** times the optimal 15. Adding stages helps only if they are sized up.

### Solution 19-04.8

An FO4 inverter has $d$ = 5, so τ = 22/5 = **4.4** ps. NAND2 FO4: $7.33 \times 4.4$ = **32.3** ps. Example 3's path: $18.39 \times 4.4$ = **80.9** ps. With $p_{inv}$ = 0.5 an FO4 is 4.5τ, so τ = 22/4.5 = **4.89** ps, **11.1** % larger. Calibrating τ from a chain absorbs the input-slope effect (§3.6), so these estimates are closer to simulation than ones based on a step-driven inverter.

### Solution 19-04.9

(a) $G = \tfrac53$, $F = \tfrac53 \times 10$ = 16.7, $P$ = 2 + 1 = 3: $\hat D = 2\sqrt{16.7} + 3$ = **11.16**.

(b) $G = 1 \times \tfrac43$, $F$ = 13.3, $P$ = 1 + 2 = 3: $\hat D = 2\sqrt{13.3} + 3$ = **10.30**.

The NAND-based version is faster because NAND has the smaller logical effort; the cost is an inverter per input (more area, and an extra load on whatever drives each input).

### Solution 19-04.10

(a) An $N$-stage inverter chain with path effort $F$ has $D(N) = NF^{1/N} + Np_{inv}$. Since $\frac{d}{dN}F^{1/N} = -F^{1/N}\ln F/N^2$,

$$
\frac{dD}{dN} = F^{1/N} - \frac{F^{1/N}\ln F}{N} + p_{inv} = 0 .
$$

With $\rho = F^{1/N}$, $\ln F/N = \ln\rho$, so $\rho - \rho\ln\rho + p_{inv} = 0$, that is $\rho(\ln\rho - 1) = p_{inv}$.

(b) At the optimum $N = \ln F/\ln\rho$, so $D/\ln F = (\rho + p_{inv})/\ln\rho$. Substituting $p_{inv} = \rho\ln\rho - \rho$ gives $D/\ln F = \rho\ln\rho/\ln\rho = \rho$.

(c) Solving $\rho(\ln\rho - 1)$ = 0.5 numerically: ρ = **3.18**.

### Solution 19-04.11

| Stages | Stage effort | Delay (τ) | Total input capacitance |
|---|---|---|---|
| 2 | 8 | **18** | 1 + 8 = **9** |
| 3 | 4 | **15** | 1 + 4 + 16 = **21** |
| 4 | 2.83 | **15.31** | 1 + 2.83 + 8 + 22.6 = **34.5** |

Two stages are **20** % slower than three but use **57** % less inverter capacitance, and so less area and switching energy. Four stages are both slower and larger than three. Near the delay optimum, a little delay buys a lot of area and energy; this is the shallow-minimum argument of §3.5 seen from the cost side.

### Solution 19-04.12

With $B$ = 1, $F = GH$ for each topology.

- $H$ = 1: (a) $2\sqrt{3.33} + 9$ = **12.65**; (b) **9.65**; (c) $4 \times 2.96^{1/4} + 7$ = **12.25**. The two-stage NAND4 + NOR2 wins.
- $H$ = 100: (a) **45.51**; (b) **42.51**; (c) **23.60**. The four-stage tree wins by a wide margin.

With a small load, the path effort is small and extra stages add more parasitic delay than they save; with a large load, the path needs about $\log_4 F$ stages, and the tree supplies them with useful logic instead of buffers.

### Solution 19-04.13

(a) Pull-down: two series pairs, each NMOS width 2. Pull-up: the pair A, B in parallel, in series with the pair C, D in parallel, so each PMOS has width 4. Every input presents 2 + 4 = 6 units: $g$ = 6/3 = **2** for each. The output node carries NMOS A and C (2 each) and PMOS C and D (4 each): 12 units, $p$ = 12/3 = **4** $p_{inv}$.

(b) With μ = 2.5 the unit inverter has NMOS 1 and PMOS 2.5, 3.5 units of input. Series PMOS pairs need width 5. AOI21: inputs A and B present 2 + 5 = 7 units, $g$ = 7/3.5 = **2.00**; input C presents 1 + 5 = 6, $g$ = 6/3.5 = **1.71**; output diffusion 2 + 1 + 5 = 8, $p$ = 8/3.5 = **2.29** $p_{inv}$. AOI22: every input 2 + 5 = 7, $g$ = **2.00**; output 2 + 2 + 5 + 5 = 14, $p$ = **4.00** $p_{inv}$.

(c) $g_C$ rose slightly and $p$ fell slightly for the AOI21; the AOI22's numbers did not move. An input whose pull-down and pull-up are both two-deep stacks scales exactly like the inverter: its NMOS width doubles (2 against 1) and its PMOS width doubles (2μ against μ), so the ratio to the inverter's $1 + \mu$ stays 2 for any μ. Input C has a single NMOS (width 1) but a two-deep PMOS (width 2μ), so its ratio $(1 + 2\mu)/(1 + \mu)$ grows with μ.

### Solution 19-04.14

(a) Input capacitance 1 + 1 = 2 units. Falling output: unit pull-down, compared with a unit inverter (3 units): $g_d$ = 2/3 = **0.667**. Rising output: the pull-up of a half-size inverter (1.5 units): $g_u$ = 2/1.5 = **1.33**. Average **1.00**.

(b) Input capacitance per input 1 + 2 = 3 units. Rising output: unit pull-up, compared with the unit inverter: $g_u$ = 3/3 = **1.00**. Falling output: half-strength pull-down, compared with a half-size inverter: $g_d$ = 3/1.5 = **2.00**. Average **1.50**, against 4/3 for the unskewed NAND2.

(c) During evaluation the dynamic node can only fall, so the inverter's output can only rise; precharge, when the output falls, is off the critical path. A HI-skew inverter makes that rising edge cheaper (0.833 against 1) and also lightens the load on the dynamic node, at the cost of a slow falling edge that does not matter.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-04.1a | NAND3 FO3 delay | 8 | τ |
| 19-04.1b | NOR3 FO3 delay | 10 | τ |
| 19-04.1c | NAND4 FO3 delay | 10 | τ |
| 19-04.2a | path logical effort | 1.33 | — |
| 19-04.2b | path effort | 16 | — |
| 19-04.2c | best stage effort | 2.52 | — |
| 19-04.2d | minimum delay | 11.56 | τ |
| 19-04.3a | branching effort | 3 | — |
| 19-04.3b | branching effort with the wire | 4 | — |
| 19-04.4a | path logical effort | 2.78 | — |
| 19-04.4b | path effort | 55.6 | — |
| 19-04.4c | best stage effort | 3.82 | — |
| 19-04.4d | minimum delay | 17.45 | τ |
| 19-04.4e | inverter input capacitance | 31.4 | units |
| 19-04.4f | NOR2 input capacitance | 13.7 | units |
| 19-04.4g | NAND3 input capacitance (check) | 6.0 | units |
| 19-04.5a | electrical effort | 667 | — |
| 19-04.5b | continuous best stage count | 5.09 | — |
| 19-04.5c | four stages | 24.33 | τ |
| 19-04.5d | five stages | 23.35 | τ |
| 19-04.5e | six stages | 23.73 | τ |
| 19-04.5f | minimum delay | 350.3 | ps |
| 19-04.5g | four-stage penalty | 4 | % |
| 19-04.5h | six-stage penalty | 2 | % |
| 19-04.6a | NAND2 alone | 68.67 | τ |
| 19-04.6b | with one inverter | 19.33 | τ |
| 19-04.6c | with two inverters | 16.16 | τ |
| 19-04.6d | stage effort with two inverters | 4.05 | — |
| 19-04.7a | equal-size chain delay | 69 | τ |
| 19-04.7b | ratio to the optimum | 4.6 | — |
| 19-04.8a | tau | 4.4 | ps |
| 19-04.8b | NAND2 FO4 delay | 32.3 | ps |
| 19-04.8c | Example 3 path delay | 80.9 | ps |
| 19-04.8d | tau with p_inv = 0.5 | 4.89 | ps |
| 19-04.8e | difference between calibrations | 11.1 | % |
| 19-04.9a | NOR2 + INV delay | 11.16 | τ |
| 19-04.9b | INV + NAND2 delay | 10.30 | τ |
| 19-04.10a | best stage effort, p_inv = 0.5 | 3.18 | — |
| 19-04.11a | two-stage delay | 18 | τ |
| 19-04.11b | two-stage capacitance | 9 | units |
| 19-04.11c | three-stage delay | 15 | τ |
| 19-04.11d | three-stage capacitance | 21 | units |
| 19-04.11e | four-stage delay | 15.31 | τ |
| 19-04.11f | four-stage capacitance | 34.5 | units |
| 19-04.11g | two stages slower by | 20 | % |
| 19-04.11h | two stages smaller by | 57 | % |
| 19-04.12a | NAND8 + INV, H = 1 | 12.65 | τ |
| 19-04.12b | NAND4 + NOR2, H = 1 | 9.65 | τ |
| 19-04.12c | tree, H = 1 | 12.25 | τ |
| 19-04.12d | NAND8 + INV, H = 100 | 45.51 | τ |
| 19-04.12e | NAND4 + NOR2, H = 100 | 42.51 | τ |
| 19-04.12f | tree, H = 100 | 23.60 | τ |
| 19-04.13a | AOI22 logical effort, each input | 2 | — |
| 19-04.13b | AOI22 parasitic delay | 4 | p_inv |
| 19-04.13c | AOI21 logical effort A and B, mu = 2.5 | 2.00 | — |
| 19-04.13d | AOI21 logical effort C, mu = 2.5 | 1.71 | — |
| 19-04.13e | AOI21 parasitic delay, mu = 2.5 | 2.29 | p_inv |
| 19-04.13f | AOI22 logical effort, mu = 2.5 | 2.00 | — |
| 19-04.13g | AOI22 parasitic delay, mu = 2.5 | 4.00 | p_inv |
| 19-04.14a | LO-skew inverter falling effort | 0.667 | — |
| 19-04.14b | LO-skew inverter rising effort | 1.33 | — |
| 19-04.14c | LO-skew inverter average effort | 1.00 | — |
| 19-04.14d | HI-skew NAND2 rising effort | 1.00 | — |
| 19-04.14e | HI-skew NAND2 falling effort | 2.00 | — |
| 19-04.14f | HI-skew NAND2 average effort | 1.50 | — |
