# Solutions 06-03 · Kirchhoff's Laws, Series/Parallel and Dividers

Problems: [06-03 problems](../problems/06-03-problems.md) · Chapter: [06-03](../chapters/06-03-kirchhoffs-laws.md). Every number below is recomputed by [verify_06_03.py](../verify/verify_06_03.py); the networks of Problems 06-03.6, 06-03.12 and 06-03.13 are also confirmed in ngspice ([lab netlist](../labs/06-03-lab/networks.cir)).

---

## Solutions

### Solution 06-03.1

(a) KCL: $n - 1 = $ **3**; KVL: $b - n + 1 = 6 - 4 + 1 = $ **3**; unknowns $2b = $ **12** (six branch voltages and six currents), matched by 6 Kirchhoff equations and 6 element laws.

(b) Every branch current leaves one node and enters another, so summing the KCL equations of all four nodes gives $0 = 0$; any one of them is the negative of the sum of the other three.

(c) For a planar circuit the meshes are a set of $b - n + 1 = $ **3** independent loops.

### Solution 06-03.2

(a) $1 + 2.2 + 4.7 = $ **7.9 kΩ**. (b) $1\ \text{kΩ}/3 = $ **333.3 Ω**. (c) $2\parallel3 = 6/5 = 1.2$ kΩ, plus 1.8 kΩ: **3.0 kΩ**. (d) $G = 1/10 + 1/15 + 1/30 = (3 + 2 + 1)/30 = 6/30$ S, so $R$ = **5 Ω**.

### Solution 06-03.3

(a) $v = 5\times3.3/(6.8 + 3.3) = 5\times3.3/10.1 = $ **1.634 V**.

(b) The current divider with the crossover: $i_{470} = 10\ \text{mA}\times1000/(470 + 1000) = $ **6.803 mA** (the smaller resistor takes the larger share; the 1 kΩ takes 3.197 mA).

### Solution 06-03.4

(a) $1 + R_1/R_2 = 3.30/0.800 = 4.125$, so $R_1 = 3.125\times10.0 = $ **31.25 kΩ**, not a standard value.

(b) $0.8(1 + 3.16) = $ **3.328 V** (+0.85%) with 31.6 kΩ; $0.8(1 + 3.09) = $ **3.272 V** (−0.85%) with 30.9 kΩ.

(c) The output depends on the ratio $R_1/R_2$. It is largest with $R_1$ high and $R_2$ low: $31.6\times1.01/(10.0\times0.99) = 3.2238$, giving $0.8\times4.2238 = $ **3.379 V**; smallest with $R_1$ low and $R_2$ high: $31.6\times0.99/(10.0\times1.01) = 3.0974$, giving **3.278 V**. The ratio's error approaches the *sum* of the two tolerances because the worst case moves them in opposite directions; a matched pair, whose errors move together, does much better. (The reference voltage's own tolerance adds on top.)

### Solution 06-03.5

The meter is in parallel with the bottom 100 kΩ.

(a) $100\ \text{k}\parallel10\ \text{M} = 99.01$ kΩ, so the reading is $10\times99.01/199.01 = $ **4.975 V**, low by **0.50%** (the divider's source resistance, 50 kΩ, is 1/200 of the meter's).

(b) $100\ \text{k}\parallel1\ \text{M} = 90.91$ kΩ: $10\times90.91/190.91 = $ **4.762 V**, low by **4.76%**. High-resistance circuits need high-resistance meters (06-11).

### Solution 06-03.6

$R_2\parallel R_3 = 6\times3/9 = 2$ Ω, so $R_{eq} = 2 + 2 + 1 = $ **5 Ω** and $I = 12/5 = $ **2.4 A**. The parallel pair has $2.4\times2 = 4.8$ V across it: $i_2 = 4.8/6 = $ **0.8 A** and $i_3 = 4.8/3 = $ **1.6 A** (KCL: $0.8 + 1.6 = 2.4$ ✓). Powers: $R_1$: $2.4^2\times2 = $ **11.52 W**; $R_2$: $4.8^2/6 = $ **3.84 W**; $R_3$: $4.8^2/3 = $ **7.68 W**; $R_4$: $2.4^2\times1 = $ **5.76 W**. Total 28.8 W $= 12\times2.4$ ✓.

### Solution 06-03.7

(a) Balance: $R_1R_4 = R_2R_3$, so $R_2 = R_1R_4/R_3 = 1000\times1372.5/1000 = $ **1372.5 Ω**.

(b) $v_{out} = 5\left(\dfrac{1372.5}{2372.5} - \dfrac{1373.5}{2373.5}\right) = $ **−0.888 mV**: a 1 Ω (0.07%) imbalance gives under a millivolt, which is why a bridge needs a sensitive detector.

(c) At balance the output is zero for any excitation, so the balance point, and hence $R_2$, depends only on the ratio arms; the excitation only sets how sensitive the detector is near balance.

### Solution 06-03.8

Exact: $10\left(\dfrac{1010}{2010} - \dfrac12\right) = $ **24.88 mV**. Approximation: $\dfrac{10}{4}\times0.010 = $ **25.0 mV**, high by 0.5%, about $\Delta R/(2R)$.

### Solution 06-03.9

(a) $S = 60$ Ω: $R_a = R_{ab}R_{ca}/S = 10\times30/60 = $ **5 Ω**; $R_b = R_{ab}R_{bc}/S = 10\times20/60 = $ **3.333 Ω**; $R_c = R_{bc}R_{ca}/S = 20\times30/60 = $ **10 Ω**.

(b) $P = R_aR_b + R_bR_c + R_cR_a = 200 + 600 + 300 = 1100$ Ω²: $R_{ab} = P/R_c = $ **36.67 Ω**; $R_{bc} = P/R_a = $ **110 Ω**; $R_{ca} = P/R_b = $ **55 Ω**.

(c) Wye: $R_a + R_b = 8.333$ Ω. Delta with c open: $R_{ab}\parallel(R_{bc} + R_{ca}) = 10\parallel50 = 500/60 = 8.333$ Ω ✓.

### Solution 06-03.10

Conductances 50, 40 and 33.33 S sum to 123.33 S; the current divider gives $i_k = 6\,G_k/123.33$: **2.432 A**, **1.946 A** and **1.622 A**. Powers $i^2R$: **0.1183 W**, **0.0947 W** and **0.0789 W**. The lowest-resistance (shortest) wire carries the most current and dissipates the most, so it is at greatest risk of fusing or of electromigration (04-05). In practice the wires heat unequally, and copper or gold resistance rises with temperature, which pushes current toward the cooler wires and partly evens the sharing out (a stabilizing effect); contact resistance at each bond, which is not in the simple model, can dominate the differences.

### Solution 06-03.11

Let $a = \text{GF}\,\varepsilon = 2.0\times500\times10^{-6} = 10^{-3}$ and $t = 5\times10^{-4}$ (the thermal change).

(a) Quarter bridge, active gauge $R(1 + a + t)$ in the bottom arm, three fixed arms $R$: $v_{out} = V\,\dfrac{a + t}{2(2 + a + t)} = 2.5\times\dfrac{1.5\times10^{-3}}{2\times2.0015} = $ **0.9368 mV**. Dividing by $V\,\text{GF}/4 = 1.25$ V per unit strain gives **749 µε** (750 µε in the linear approximation): the 10 K warm-up has added about 250 µε of false strain.

(b) With the dummy $R(1 + t)$ on top and the active gauge $R(1 + a + t)$ below it: $v_A = V\,\dfrac{1 + a + t}{2 + a + 2t}$ and $v_B = V/2$, so

$$
v_{out} = V\left(\frac{1 + a + t}{2 + a + 2t} - \frac12\right) = V\,\frac{a}{2(2 + a + 2t)} = 2.5\times\frac{10^{-3}}{2\times2.002} = \textbf{0.6244 mV},
$$

against **0.6247 mV** at the reference temperature ($t = 0$): the temperature effect is reduced from 50% of the reading to 0.05%.

(c) The thermal change multiplies both resistors of the divider by the same factor $(1 + t)$ to first order, leaving their ratio, and so $v_A$, unchanged; only the strain, which affects one of them, unbalances the bridge. The dummy must be identical and see the same temperature, so it is mounted near the active gauge on an unstrained piece of the same material.

### Solution 06-03.12

(a) Work from the far end. At N4 the 2R leg and the 2R termination are in parallel: $2R\parallel2R = R$. Seen from N3, the series $R$ plus that $R$ make $2R$, in parallel with N3's own 2R leg: $R$ again. The same holds at N2 and N1, so the resistance looking into N1 is **$R$ = 10 kΩ**, and the input current is $5/10\ \text{k} = $ **0.5 mA**.

(b) At each node the current meets two equal paths of $2R$ (the leg, and the rest of the ladder), so it halves: legs at N1 to N4 carry **0.25, 0.125, 0.0625 and 0.03125 mA**, and the termination another 0.03125 mA.

(c) Code 1011 sums the legs of N1, N3 and N4: $0.25 + 0.0625 + 0.03125 = $ **0.34375 mA** (that is $\tfrac{11}{16}$ of 0.5 mA). The legs return to ground or to a virtual ground at the same potential, so steering them does not change the ladder's currents. Only two values, $R$ and $2R$, are needed whatever the number of bits, and their *ratio* is what must be accurate: easy to match on a chip (06-02), far easier than binary-weighted resistors spanning a range of $2^N$.

### Solution 06-03.13

(a) Delta a–c–d ($R_{ac}$ = 6, $R_{ad}$ = 12, $R_{cd}$ = 6; $S$ = 24 Ω) to wye: $R_{na} = 6\times12/24 = 3$ Ω, $R_{nc} = 6\times6/24 = 1.5$ Ω, $R_{nd} = 12\times6/24 = 3$ Ω. Then $(1.5 + 12)\parallel(3 + 6) = 13.5\parallel9 = 5.4$ Ω, and $R_{eq} = 3 + 5.4 = $ **8.4 Ω**.

(b) With 1 A in: $v_a - v_n = 3$ V; the two paths share the 1 A as $9/22.5 = 0.4$ A through $13.5$ Ω and $0.6$ A through 9 Ω. Taking node b as 0 V: $v_n = 5.4$ V, $v_c = 0.4\times12 = 4.8$ V, $v_d = 0.6\times6 = 3.6$ V. The bridge current is $(4.8 - 3.6)/6 = $ **0.2 A, from c to d**.

### Solution 06-03.14

(a) $7/1.5 = 4.67$, so **5 cells**, giving **7.5 V**.

(b) Parallel current sources add: $2 - 0.5 + 1 = $ **2.5 mA**, referenced into the node.

(c) Equal sources in parallel: the open-circuit voltage stays **6 V**, and the internal resistances are in parallel: **0.5 Ω**. (06-08 makes this a special case of combining Thevenin equivalents.)

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-03.1a | independent KCL equations | 3 | — |
| 06-03.1b | independent KVL equations | 3 | — |
| 06-03.1c | unknowns | 12 | — |
| 06-03.2a | series | 7.9 | kΩ |
| 06-03.2b | three 1 kΩ in parallel | 333.3 | Ω |
| 06-03.2c | (2 k ∥ 3 k) + 1.8 k | 3.0 | kΩ |
| 06-03.2d | 10 ∥ 15 ∥ 30 | 5 | Ω |
| 06-03.3a | divider output | 1.634 | V |
| 06-03.3b | current in 470 Ω | 6.803 | mA |
| 06-03.4a | exact R_1 | 31.25 | kΩ |
| 06-03.4b | output with 31.6 kΩ | 3.328 | V |
| 06-03.4c | output with 30.9 kΩ | 3.272 | V |
| 06-03.4d | worst-case maximum | 3.379 | V |
| 06-03.4e | worst-case minimum | 3.278 | V |
| 06-03.5a | reading with 10 MΩ meter | 4.975 | V |
| 06-03.5b | error with 10 MΩ meter | 0.50 | % |
| 06-03.5c | reading with 1 MΩ meter | 4.762 | V |
| 06-03.5d | error with 1 MΩ meter | 4.76 | % |
| 06-03.6a | equivalent resistance | 5 | Ω |
| 06-03.6b | source current | 2.4 | A |
| 06-03.6c | current in R_2 | 0.8 | A |
| 06-03.6d | current in R_3 | 1.6 | A |
| 06-03.6e | power in R_1 | 11.52 | W |
| 06-03.6f | power in R_3 | 7.68 | W |
| 06-03.7a | unknown resistance | 1372.5 | Ω |
| 06-03.7b | output 1 Ω off balance | −0.888 | mV |
| 06-03.8a | exact output | 24.88 | mV |
| 06-03.8b | linear approximation | 25.0 | mV |
| 06-03.9a | wye R_a | 5 | Ω |
| 06-03.9b | wye R_b | 3.333 | Ω |
| 06-03.9c | wye R_c | 10 | Ω |
| 06-03.9d | delta R_ab | 36.67 | Ω |
| 06-03.9e | delta R_bc | 110 | Ω |
| 06-03.9f | delta R_ca | 55 | Ω |
| 06-03.9g | resistance a–b with c open | 8.333 | Ω |
| 06-03.10a | current in 20 mΩ wire | 2.432 | A |
| 06-03.10b | current in 25 mΩ wire | 1.946 | A |
| 06-03.10c | current in 30 mΩ wire | 1.622 | A |
| 06-03.10d | power in 20 mΩ wire | 0.1183 | W |
| 06-03.11a | quarter-bridge output, warm | 0.9368 | mV |
| 06-03.11b | reported strain, quarter bridge | 749 | µε |
| 06-03.11c | output with dummy, warm | 0.6244 | mV |
| 06-03.11d | output at reference temperature | 0.6247 | mV |
| 06-03.12a | input resistance | 10 | kΩ |
| 06-03.12b | input current | 0.5 | mA |
| 06-03.12c | current in N4's leg | 0.03125 | mA |
| 06-03.12d | summed current for code 1011 | 0.34375 | mA |
| 06-03.13a | equivalent resistance | 8.4 | Ω |
| 06-03.13b | bridge current | 0.2 | A |
| 06-03.14a | battery voltage | 7.5 | V |
| 06-03.14b | combined current source | 2.5 | mA |
| 06-03.14c | combined internal resistance | 0.5 | Ω |
