# Solutions 19-03 · Combinational Logic Families

Problems: [19-03 problem set](../problems/19-03-problems.md) · Chapter: [19-03](../chapters/19-03-logic-families.md). Every number below is recomputed by [verify_19_03.py](../verify/verify_19_03.py).

---

## Solutions

### Solution 19-03.1

(a) The output is low when $A$ is 1 and either $B$ or $C$ is 1: the PDN is $A$ in series with ($B$ parallel to $C$). The PUN is the dual: $A$ in parallel with ($B$ in series with $C$). Six transistors (**6**).

(b) The longest PDN path has two series NMOS ($A$ and one of $B$, $C$), so all three NMOS have width **2**. The longest PUN path is $B$ in series with $C$: those PMOS have width **4**; the PMOS for $A$ conducts alone and has width **2**.

(c) Input $A$: $2 + 2 = 4$ units, **1.33** times the inverter's 3. Inputs $B$ and $C$: $2 + 4 = 6$ units, **2.0** times.

### Solution 19-03.2

(a) Static CMOS: $2N$ = **8**. (b) Pseudo-NMOS: four NMOS and one load, **5**. (c) Footed dynamic: four NMOS, the precharge PMOS and the foot, **6**. (d) Domino: add the two-transistor inverter, **8**; the transistor count matches static CMOS, but the inputs drive only NMOS.

### Solution 19-03.3

Multiply each capacitor by the resistance it shares with the path to the node of interest.

At node 2: $C_1R_1 + C_2(R_1 + R_2) + C_3R_1 = 10 + 60 + 30$ = **100** ps, so $t_p \approx$ **69.3** ps.

At node 3: $C_1R_1 + C_2R_1 + C_3(R_1 + R_3) = 10 + 20 + 120$ = **150** ps, so $t_p \approx$ **104.0** ps.

$C_3$ loads node 2 only through the shared $R_1$; it does not charge through $R_2$.

### Solution 19-03.4

Each NMOS has $R/3$ = 3.33 kΩ. Number the internal nodes from ground.

(a) $\tau_E = (R/3)(1.5\ \text{fF}) + (2R/3)(1.5\ \text{fF}) + R(20\ \text{fF}) = 5 + 10 + 200$ = **215** ps, $t_p$ = **149.0** ps.

(b) The two lower transistors were on, so the internal nodes are already at 0 V and only the output must discharge: $\tau_E = R \times 20\ \text{fF}$ = **200** ps, $t_p$ = **138.6** ps.

(c) A **7.0** % improvement, for free: synthesis and place-and-route tools use pin swapping of this kind.

### Solution 19-03.5

(a) $V_{OL}$ is largest with one input on, so the condition is $\tfrac12k_p(0.7)^2 \le 150\ \mu \times (0.7 \times 0.15 - 0.15^2/2)$, giving $k_p \le 150\ \mu \times 0.09375/0.245$ = **57.4** µA/V².

(b) $I = \tfrac12 \times 57.4\ \mu \times 0.49$ = 14.06 µA, so $P$ = **14.06** µW at 1.0 V.

(c) Two inputs on double the pull-down strength: solving with $2k_n$ gives $V_{OL}$ = **0.0705** V.

### Solution 19-03.6

(a) Solve $V = 1.0 - [0.3 + 0.5(\sqrt{0.7 + V} - \sqrt{0.7})]$: $V$ = **0.558** V, with the threshold raised to 0.442 V.

(b) The following PMOS has $V_{SG} = 1.0 - 0.558$ = **0.442** V > 0.3 V: it stays **on**, and the inverter draws static current. A level restorer or a TG is needed.

### Solution 19-03.7

(a) $0.69 \times 4\ \text{kΩ} \times 3\ \text{fF} \times 16 \times 17/2$ = **1131** ps.

(b) $m_{opt} = \sqrt{2 \times 25/(0.693 \times 12)}$ = **2.45**.

(c) $m$ = 2: $8 \times 0.693 \times 12 \times 3 + 7 \times 25$ = **374.6** ps. $m$ = 4: $4 \times 0.693 \times 12 \times 10 + 3 \times 25$ = **407.7** ps. $m$ = 8: **623.9** ps. Segments of 2 are best, **3.02** times faster than the unbuffered chain.

### Solution 19-03.8

(a) Equalizing all three nodes would give $1.2 \times 12/16$ = **0.900** V, above $V_{DD} - V_{TN}$ = 0.85 V, so the conducting transistors cut off with both internal nodes at 0.85 V. The charge taken is $4\ \text{fF} \times 0.85\ \text{V}$ = 3.4 fC, so the output is $1.2 - 3.4/12$ = **0.917** V.

(b) $1.2 \times 6/10$ = 0.72 V < 0.85 V, so the nodes equalize at **0.72** V, close to a 0.6 V switching threshold: the gate is near failure. Halving the output capacitance raised the disturbance from 0.283 V to 0.48 V.

### Solution 19-03.9

(a) $t_{hold} = 5\ \text{fF} \times 0.15\ \text{V}/20\ \text{nA}$ = **37.5** ns.

(b) $f_{min} = 1/(2 \times 37.5\ \text{ns})$ = **13.3** MHz. Clock gating or a slow test mode would break the gate.

(c) A keeper supplies the leaked charge while the output is high, removing the minimum frequency; it must be weak enough that the pull-down network still wins when it discharges the node.

### Solution 19-03.10

(a) Each section has $R_w/n$ and $C_w/n$. Node $i$ shares $iR_w/n$ with the path to the end, so

$$
\tau_E = \sum_{i=1}^{n}\frac{C_w}{n}\cdot\frac{iR_w}{n} = \frac{R_wC_w}{n^2}\cdot\frac{n(n+1)}{2} = R_wC_w\frac{n+1}{2n} \;\to\; \frac{R_wC_w}{2} .
$$

(b) With $R_w = C_w$ = 1 (the ratio is scale-free), exact step responses from the matrix exponential give 50% delays of 0.693, 0.471 and 0.410 against $0.69\tau_E$ = 0.693, 0.433 and 0.375: ratios of **1.000**, **1.087** and **1.092**. The ratio settles near 1.09 for long ladders, toward the continuous line's $0.38R_wC_w$ against $0.35R_wC_w$. For wires, 19-05 therefore uses $0.38RC$ rather than $0.69 \times RC/2$.

### Solution 19-03.11

(a) The top NMOS cuts off when its source reaches $V = 1.2 - V_{TN}(V)$, the same equation as Example 19-03.4: **0.715** V.

(b) The nodes equalize below the cut-off if $1.2C_L/(C_L + C_a) < 0.715$, so the boundary is $C_a/C_L = 1.2/0.715 - 1$ = **0.677**.

(c) $V_{out} = 1.2 - 0.3 \times 0.715$ = **0.985** V, against 0.945 V without the body effect. Here the body effect **helps**: the raised threshold cuts the transistor off earlier, so less charge leaves the output.

### Solution 19-03.12

(a) The dynamic gate's PDN computes the condition for discharging: ($A$ in series with $B$) in parallel with $C$. The dynamic output is $\overline{AB + C}$ after evaluation, and the inverter gives $F = AB + C$.

(b) Footed: three logic NMOS, the precharge PMOS, the foot, and the two-transistor inverter: **7**. A static AOI21 (6) plus an inverter (2): **8**.

(c) $\overline F$ would require a domino stage whose output falls when its inputs rise, which would violate the monotonicity required of the next stage's inputs: every domino stage is non-inverting. The usual remedy is **dual-rail** domino, which computes $F$ and $\overline F$ in two stages from both polarities of every input.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-03.1a | transistor count | 6 | — |
| 19-03.1b | NMOS width | 2 | units |
| 19-03.1c | PMOS width for B and C | 4 | units |
| 19-03.1d | PMOS width for A | 2 | units |
| 19-03.1e | input A capacitance ratio | 1.33 | — |
| 19-03.1f | inputs B and C capacitance ratio | 2.0 | — |
| 19-03.2a | static CMOS NOR4 | 8 | transistors |
| 19-03.2b | pseudo-NMOS NOR4 | 5 | transistors |
| 19-03.2c | footed dynamic NOR4 | 6 | transistors |
| 19-03.2d | domino NOR4 | 8 | transistors |
| 19-03.3a | Elmore constant at node 2 | 100 | ps |
| 19-03.3b | delay at node 2 | 69.3 | ps |
| 19-03.3c | Elmore constant at node 3 | 150 | ps |
| 19-03.3d | delay at node 3 | 104.0 | ps |
| 19-03.4a | worst-case Elmore constant | 215 | ps |
| 19-03.4b | worst-case delay | 149.0 | ps |
| 19-03.4c | Elmore constant, best ordering | 200 | ps |
| 19-03.4d | delay, best ordering | 138.6 | ps |
| 19-03.4e | improvement | 7.0 | % |
| 19-03.5a | largest load kp | 57.4 | µA/V² |
| 19-03.5b | static power | 14.06 | µW |
| 19-03.5c | V_OL with two inputs high | 0.0705 | V |
| 19-03.6a | passed high level | 0.558 | V |
| 19-03.6b | source-gate voltage of the next PMOS | 0.442 | V |
| 19-03.7a | unbuffered delay | 1131 | ps |
| 19-03.7b | optimal segment length | 2.45 | — |
| 19-03.7c | delay with segments of 2 | 374.6 | ps |
| 19-03.7d | delay with segments of 4 | 407.7 | ps |
| 19-03.7e | delay with segments of 8 | 623.9 | ps |
| 19-03.7f | speed-up with segments of 2 | 3.02 | — |
| 19-03.8a | equalized level, 12 fF | 0.900 | V |
| 19-03.8b | output, 12 fF | 0.917 | V |
| 19-03.8c | output, 6 fF | 0.72 | V |
| 19-03.8d | disturbance, 12 fF | 0.283 | V |
| 19-03.8e | disturbance, 6 fF | 0.48 | V |
| 19-03.9a | hold time | 37.5 | ns |
| 19-03.9b | minimum clock frequency | 13.3 | MHz |
| 19-03.10a | exact over estimate, n = 1 | 1.000 | — |
| 19-03.10h | exact delay over RwCw, n = 1 | 0.693 | — |
| 19-03.10b | exact over estimate, n = 4 | 1.087 | — |
| 19-03.10c | exact over estimate, n = 12 | 1.092 | — |
| 19-03.10d | exact delay over RwCw, n = 4 | 0.471 | — |
| 19-03.10e | exact delay over RwCw, n = 12 | 0.410 | — |
| 19-03.10f | estimate over RwCw, n = 4 | 0.433 | — |
| 19-03.10g | estimate over RwCw, n = 12 | 0.375 | — |
| 19-03.11a | cut-off level with body effect | 0.715 | V |
| 19-03.11b | boundary Ca/CL with body effect | 0.677 | — |
| 19-03.11c | output with 3 fF | 0.985 | V |
| 19-03.12a | domino transistor count | 7 | — |
| 19-03.12b | static AOI21 plus inverter | 8 | — |
