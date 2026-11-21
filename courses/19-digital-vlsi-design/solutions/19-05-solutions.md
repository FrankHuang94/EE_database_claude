# Solutions 19-05 · Interconnect

Problems: [19-05 problem set](../problems/19-05-problems.md) · Chapter: [19-05](../chapters/19-05-interconnect.md). Every number below is recomputed by [verify_19_05.py](../verify/verify_19_05.py).

---

## Solutions

### Solution 19-05.1

$L/W$ = 2 mm/0.1 µm = **20000** squares, so $R$ = 0.08 × 20000 = **1.6** kΩ. $C$ = 0.2 fF/µm × 2000 µm = **400** fF. The distributed delay is $0.379 \times 1.6\ \text{kΩ} \times 400\ \text{fF}$ = **242.6** ps.

### Solution 19-05.2

$R_w = rL = R_d$ gives $L$ = 2 kΩ/(10 Ω/µm) = **200** µm. Shorter wires are mainly capacitive loads; longer ones need the full RC treatment and eventually repeaters.

### Solution 19-05.3

$\Delta V = 0.8 \times 3/(3 + 15)$ = **0.133** V, and it stays until the node is precharged again.

### Solution 19-05.4

$R_wC_w$ = 500 ps. Distributed: $0.379 \times 500$ = **189.5** ps. Lumped: $0.69 \times 500$ = **346.6** ps, 83% high. Elmore: $0.69 \times 250$ = **173.3** ps, 8.5% low.

### Solution 19-05.5

(a) $R_w$ = 10 kΩ and $C_w$ = 400 fF. $t = 0.69 \times 500 \times 420\ \text{fF} + 10\ \text{kΩ} \times (0.379 \times 400 + 0.69 \times 20)\ \text{fF}$ = 145.6 + 1654.6 = **1800.2** ps.

(b) With 125 Ω: 36.4 + 1654.6 = **1691.0** ps, only **6.1** % faster. The wire's own term dominates.

### Solution 19-05.6

$k_{opt} = \sqrt{0.379 \times 10\ \text{kΩ} \times 400\ \text{fF}/(0.69 \times 8\ \text{kΩ} \times 0.2\ \text{fF})}$ = **37.0** segments, every **54** µm. $h_{opt} = \sqrt{8\ \text{kΩ} \times 400\ \text{fF}/(10\ \text{kΩ} \times 0.2\ \text{fF})}$ = **40**. $T_{min}$ = **192.9** ps, **96.5** ps/mm, **9.3** times faster than Problem 5(a).

### Solution 19-05.7

$T_{min} \propto \sqrt{R_0C_0}$, so it changes by $\sqrt{0.5}$ = **0.707**: halving the repeaters' delay buys only 29% on repeated wires.

### Solution 19-05.8

(a) Miller factors 0 to 2 on both neighbors: from **60** to **180** fF, a factor of three.

(b) The shield's coupling always counts once; the remaining neighbor contributes 0 to 60 fF: from **90** to **150** fF.

### Solution 19-05.9

Each plane: $3.0 \times 8.854 \times 10^{-12} \times 40/80$ F/m = 13.3 aF/µm, so **26.6** aF/µm for both. Each neighbor: $3.0 \times 8.854 \times 10^{-12} \times 80/40$ = 53.1 aF/µm, so **106.3** aF/µm for both. Total **132.8** aF/µm, **80** % of it coupling.

### Solution 19-05.10

(a) $T = 0.69R_0C_w/h + 0.69kR_0C_0 + 0.379R_wC_w/k + 0.69R_whC_0$. The $k$ terms are $ak + b/k$ with $a = 0.69R_0C_0$ and $b = 0.379R_wC_w$; their minimum is at $k = \sqrt{b/a}$ with value $2\sqrt{ab}$. The $h$ terms are $c/h + dh$ with $c = 0.69R_0C_w$ and $d = 0.69R_wC_0$; minimum at $h = \sqrt{c/d} = \sqrt{R_0C_w/(R_wC_0)}$ with value $2\sqrt{cd} = 2 \times 0.69\sqrt{R_0C_0R_wC_w}$. So

$$
T_{min} = \left(2\sqrt{0.69 \times 0.379} + 1.386\right)\sqrt{R_0C_0R_wC_w} = 2.41\sqrt{R_0C_0R_wC_w} .
$$

(b) At $k_{opt}$, $ak = b/k$: $0.69R_0C_0 = 0.379R_wC_w/k^2$, and $0.379(R_w/k)(C_w/k)$ is one segment's distributed wire delay.

(c) At $h_{opt}$, $c/h = dh$: the delay of each repeater charging its wire segment equals that of the wire segment's resistance charging the next repeater.

### Solution 19-05.11

(a) $1.25/0.49$ = **2.55**.

(b) $\sqrt{0.7 \times 2.55}$ = **1.34** per node, and relative to gates $1.34/0.7$ = **1.91**.

(c) $1.34^3$ = **2.39** in absolute delay and $1.91^3$ = **6.96** relative to gates: the same wire is about seven times "longer" in gate delays after three nodes.

### Solution 19-05.12

(a) $6 \times 123.7$ = **742.5** ps.

(b) 200 ps/123.7 ps per mm = **1.62** mm per cycle.

(c) 6/1.62 = 3.7, so **4** cycles: the wire needs three pipeline flip-flops along its route, and the microarchitecture must tolerate four cycles of latency.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-05.1a | squares | 20000 | — |
| 19-05.1b | resistance | 1.6 | kΩ |
| 19-05.1c | capacitance | 400 | fF |
| 19-05.1d | distributed delay | 242.6 | ps |
| 19-05.2a | crossover length | 200 | µm |
| 19-05.3a | victim disturbance | 0.133 | V |
| 19-05.4a | distributed delay | 189.5 | ps |
| 19-05.4b | lumped estimate | 346.6 | ps |
| 19-05.4c | Elmore estimate | 173.3 | ps |
| 19-05.5a | delay, 500 Ω driver | 1800.2 | ps |
| 19-05.5b | delay, 125 Ω driver | 1691.0 | ps |
| 19-05.5c | improvement | 6.1 | % |
| 19-05.6a | optimal segments | 37.0 | — |
| 19-05.6b | spacing | 54 | µm |
| 19-05.6c | optimal size | 40 | — |
| 19-05.6d | minimum delay | 192.9 | ps |
| 19-05.6e | delay per mm | 96.5 | ps/mm |
| 19-05.6f | speed-up over Problem 5(a) | 9.3 | — |
| 19-05.7a | delay factor | 0.707 | — |
| 19-05.8a | minimum effective capacitance | 60 | fF |
| 19-05.8b | maximum effective capacitance | 180 | fF |
| 19-05.8c | minimum with a shield | 90 | fF |
| 19-05.8d | maximum with a shield | 150 | fF |
| 19-05.9a | plate capacitance, both planes | 26.6 | aF/µm |
| 19-05.9b | coupling, both neighbors | 106.3 | aF/µm |
| 19-05.9c | total | 132.8 | aF/µm |
| 19-05.9d | coupling fraction | 80 | % |
| 19-05.10a | repeated-delay coefficient | 2.41 | — |
| 19-05.11a | resistance per length factor | 2.55 | — |
| 19-05.11b | repeated delay factor per node | 1.34 | — |
| 19-05.11c | relative to gates per node | 1.91 | — |
| 19-05.11d | absolute factor over three nodes | 2.39 | — |
| 19-05.11e | relative factor over three nodes | 6.96 | — |
| 19-05.12a | repeated delay of 6 mm | 742.5 | ps |
| 19-05.12b | distance per cycle | 1.62 | mm |
| 19-05.12c | cycles | 4 | — |
