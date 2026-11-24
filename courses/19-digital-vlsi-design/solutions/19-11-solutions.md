# Solutions 19-11 · The ASIC Flow II: Floorplan, Place and Route, Signoff

Problems: [19-11 problem set](../problems/19-11-problems.md) · Chapter: [19-11](../chapters/19-11-place-route-signoff.md). Every number below is recomputed by [verify_19_11.py](../verify/verify_19_11.py).

---

## Solutions

### Solution 19-11.1

Core area $120\,000/0.70$ = **171 429** µm². With height = 2 × width, $W^2 \times 2 = 171\,429$, so $W$ = **292.77** µm and the target height is 585.54 µm. Rows: $585.54/2.72 = 215.27$, rounded up to **216** rows, a height of $216 \times 2.72$ = **587.52** µm. Sites per row: $\lfloor 292.77/0.46 \rfloor$ = **636**. Achieved utilization: $120\,000/(292.77 \times 587.52)$ = **69.76** %, slightly under target because of the rounding up. With the width snapped to whole sites, $636 \times 0.46$ = **292.56** µm, it is **69.81** %.

### Solution 19-11.2

(a) Both ends: $IR/8 = 0.020 \times 2.0/8$ = **5.0** mV. One end: $IR/2$ = **20** mV.

(b) Each half has resistance 1.0 Ω and carries 10 mA: $0.010 \times 1.0/8$ = **1.25** mV, a factor of **4** lower. The drop scales as $iL^2$: halving the length between feeds quarters it.

### Solution 19-11.3

(a) $x$ spans 2 to 10 and $y$ spans 3 to 11: HPWL $= 8 + 8$ = **16**.

(b) Run a vertical trunk at $x = 6$ from $y = 3$ to $y = 11$ (length 8), reaching (6, 11) directly, and horizontal branches at $y = 3$ from $x = 2$ to 6 (length 4) and at $y = 5$ from $x = 6$ to 10 (length 4): total **16**, equal to the HPWL. For any three pins, a trunk at the middle pin's $x$ spanning the full $y$ range, plus branches to the other two pins, totals exactly the box's half-perimeter.

(c) With many pins, the tree must reach pins inside the box too, which needs extra branches beyond the box's two spans; HPWL counts only the spans.

### Solution 19-11.4

(a) Setting the derivatives of the spring energy to zero: for A, $(1 + 2 + 1)x_A - 2x_B = 1 \times 0 + 1 \times 12$, so $4x_A - 2x_B = 12$; for B, $(2 + 1)x_B - 2x_A = 12$, so $3x_B - 2x_A = 12$. From the first, $x_A = 3 + x_B/2$; substituting, $2x_B - 6 = 12$, so $x_B$ = **9** and $x_A$ = **7.5**.

(b) A: $(1 \times 0 + 2 \times 9 + 1 \times 12)/4 = 30/4 = 7.5$. B: $(2 \times 7.5 + 1 \times 12)/3 = 27/3 = 9$. Both check.

(c) Both move right by **3** (to 10.5 and 12): the system is linear and a uniform shift of the fixed pins is a solution shifted by the same amount (Problem 11).

### Solution 19-11.5

(a) Manhattan distance $|6 - 0| + |3 - 3|$ = **6**. The wall blocks column 3 in rows 0–5, so a path must cross column 3 in row 6. The shortest path goes down from row 3 to row 6 (3 steps), across six columns (6 steps), and up to row 3 (3 steps): **12** steps. Lee's wavefront finds it (or another of the same length).

(b) Any path from column 0 to column 6 makes at least 6 horizontal moves, and it must visit row 6 (the only gap), which is 3 rows from both the start and the end, so it makes at least 3 + 3 vertical moves: at least 12.

### Solution 19-11.6

(a) HPWL $= 4 + 4$ = **8**. Every pair of pins is exactly 4 apart in Manhattan distance (for example (0, 2) to (2, 0) is 2 + 2, and (0, 2) to (4, 2) is 4 + 0), so any spanning tree uses three edges of length 4: RMST **12**. The RSMT adds a Steiner point at (2, 2), 2 from every pin: **8**.

(b) RMST/RSMT = 12/8 = **1.5**, exactly Hwang's bound: this configuration is the worst case.

(c) At the center (2, 2), on the Hanan grid. Each spanning-tree edge between two pins detours around the center; the Steiner point lets all four pins share it.

### Solution 19-11.7

(a) $x = \dfrac{t_2 - t_1 + rL(C_2 + cL/2)}{r(C_1 + C_2 + cL)}$. With $rL = 150$ Ω and $cL = 100$ fF: numerator $2.0 + 150 \times (60 + 50) \times 10^{-3}$ ps $= 2.0 + 16.5 = 18.5$ ps; denominator $0.30 \times 200$ fF = 60 Ω·fF per µm = 0.060 ps/µm. $x = 18.5/0.060$ = **308.3** µm from subtree 1.

(b) Delay $t_1 + rx(cx/2 + C_1) = 10.0 + 0.30 \times 308.3 \times (30.83 + 40) \times 10^{-3}$ ps = **16.55** ps (check: from the other side, $12.0 + 0.30 \times 191.7 \times (19.17 + 60) \times 10^{-3} = 16.55$ ps). Capacitance $40 + 60 + 100$ = **200** fF.

(c) With $t_2 = 80$ ps, $x = (70 + 16.5)/0.060$ = **1442** µm, beyond the 500 µm wire: even tapping at subtree 2's root leaves subtree 1 too fast. The wire to subtree 1 must be lengthened (snaked) until $r\ell(c\ell/2 + C_1) = 70$ ps: $0.03\,\ell^2 + 12\,\ell - 70\,000 = 0$ (ℓ in µm, terms in fs), so ℓ = **1341** µm, **841** µm more than the 500 µm straight route. In practice a delay buffer is cheaper than that much wire.

### Solution 19-11.8

(a) $4^3$ = **64** sinks.

(b) Path $D(1 - 2^{-3}) = 2.0 \times 0.875$ = **1.75** mm; total $1.5D(2^3 - 1) = 1.5 \times 2.0 \times 7$ = **21** mm.

(c) $21\,000 \times 0.2$ fF = **4.2** pF.

### Solution 19-11.9

(a) Flip-flops $20\,000 \times 1.794$ fF = 35.88 pF; total **41.88** pF. $P = CV^2f = 41.88 \times 10^{-12} \times 1.8^2 \times 10^8$ = **13.57** mW.

(b) The flip-flop clock pins, **86** % of the capacitance. Clock gating (19-06), which stops the clock to idle registers, attacks the dominant term; shortening wires helps less.

### Solution 19-11.10

(a) $r = R_\square/W$: metal 1 $0.125/0.14$ = **0.893** Ω/µm; metal 3 $0.047/0.30$ = **0.157** Ω/µm; metal 5 $0.0285/1.6$ = **0.0178** Ω/µm. Fifty times less resistance per micrometre from bottom to top.

(b) $1.20565/0.893$ = **1.35**. An estimate used before routing must cover wires that end up narrower than drawn after etch, hotter than 25 °C, or broken by vias; setting it high keeps early timing pessimistic, so that real routing is less likely to make things worse. (The flow's file does not document its derivation, so this is a plausible reason, not a stated one.)

(c) $2000 \times 0.157$ = **313** Ω.

(d) Metal 1: $2.8 \times 0.14$ = **0.392** mA. Metal 3: $6.8 \times 0.30$ = **2.04** mA. A 1.5 mA metal-1 rail needs $1.5/2.8$ = **0.536** µm, nearly four times the minimum width: power wiring is sized by electromigration as well as by IR drop.

### Solution 19-11.11

(a) Without fixed pins, $Q$ is the graph Laplacian: each row has the sum of a cell's weights on the diagonal and minus each weight off it, so every row sums to zero and $Q\mathbf{1} = \mathbf{0}$. $Q$ is singular, and the energy $\sum w_{ij}(x_i - x_j)^2$ is unchanged when every cell moves by the same amount: the flat direction is a uniform translation.

(b) With fixed pins, $Q = L + D$, where $D$ is diagonal with each cell's total weight to fixed pins. Then $\mathbf{x}^{\mathsf T}Q\mathbf{x} = \sum_{(i,j)} w_{ij}(x_i - x_j)^2 + \sum_i D_{ii}x_i^2 \ge 0$. It is zero only if all connected cells have equal $x$ (first sum) and every cell tied to a fixed pin has $x = 0$ (second sum); with at least one such cell in a connected netlist, that forces $\mathbf{x} = \mathbf{0}$. So $Q$ is positive definite and the optimum is unique.

(c) $\mathbf{b}$ is linear in the fixed positions: $b_i = \sum_k w_{ik}x_k$. Shifting every fixed pin by $d$ adds $d\sum_k w_{ik} = dD_{ii}$ to each $b_i$, which is $d\,(Q\mathbf{1})_i$ because $L\mathbf{1} = \mathbf{0}$. So $\mathbf{x} + d\mathbf{1}$ solves the new system: every cell shifts by $d$.

### Solution 19-11.12

(a) The point load $I_p$ at $a$ returns to the two feeds through $R_1 = ra$ and $R_2 = r(L - a)$ in parallel, so the drop at $a$ is $I_p R_1R_2/(R_1 + R_2) = I_p r a(L - a)/L$, falling linearly to zero at each end: $I_p r x(L - a)/L$ for $x \le a$ and $I_p r a(L - x)/L$ for $x \ge a$. Here it is $2\ \text{mA} \times 0.5 \times 50 \times 150/200$ Ω = **37.5** mV at $x = 50$ µm.

(b) The uniform load adds $r i x(L - x)/2$ with $i = 5$ µA/µm. For $x < a$ both terms rise; for $x > a$ the slope is $r[i(L - 2x)/2 - I_p a/L]$, which is already negative at $x = a$ ($0.5 \times [2.5 - 5.0] \times 10^{-4}$ V/µm), so the maximum is at the macro: $0.5 \times 5 \times 10^{-6} \times 50 \times 150/2 = 9.375$ mV plus 37.5 mV = **46.9** mV at **50** µm.

(c) The uniform load alone gives $IR/8 = 1\ \text{mA} \times 100\ \Omega/8$ = **12.5** mV. With the macro at the middle, its own drop is $2\ \text{mA} \times 0.5 \times 100 \times 100/200 = 50$ mV, and the total worst drop is **62.5** mV. Putting heavy loads near the feeds (or adding a feed beside them) is a floorplanning decision.

### Solution 19-11.13

(a) Metal 1, 400 µm: $R_w = 1.20565 \times 400 = 482.26$ Ω, $C_w = 0.172375 \times 400 = 68.95$ fF, $C_L = 4 \times 2.302 = 9.208$ fF. Driver term $1410 \times (68.95 + 9.208)$ fF = **110.20** ps; wire term $482.26 \times (0.38 \times 68.95 + 0.69 \times 9.208)$ fF = **15.70** ps; total **125.90** ps.

(b) 600 µm: $R_w = 723.39$ Ω, $C_w = 103.425$ fF. Driver term $1410 \times 112.633$ fF = 158.81 ps, wire term $723.39 \times 45.655$ fF = 33.03 ps; total **191.84** ps, so the path loses **65.94** ps of slack. The detour adds 50 % to the length but 52 % to the delay, because the wire term grows as the square of the length.

(c) Opposite-direction switching doubles the charge through the coupling capacitance (the Miller effect, 19-05), adding $\Delta C = 300 \times 0.05 = 15$ fF to the effective capacitance; same-direction switching removes it. The change is $1410 \times 15\ \text{fF} + 723.39 \times 0.38 \times 15\ \text{fF} = 21.15 + 4.12$ = **±25.27** ps: slower for opposite switching, which matters for setup, and faster for same-direction switching, which matters for hold. This is why signoff STA checks both with signal-integrity analysis.

(d) Metal 3, 600 µm: driver term $1410 \times (128.977 + 9.208)$ fF = 194.84 ps, wire term 5.52 ps, total **200.36** ps, *worse* than metal 1, because this net is driver-dominated and the flow's metal-3 estimate has more capacitance per micrometre. The stronger driver: $705 \times 112.633$ fF + 33.03 ps = **112.43** ps, better than the placement estimate. Its cost is about twice the input capacitance, which loads the previous stage and slows it, twice the area and more leakage. As in Example 19-11.6, upper metal helps only once the wire's own RC dominates.

### Solution 19-11.14

| Defect | Check | What it protects against |
|---|---|---|
| (a) missing vias, local droop | Power-integrity (static and dynamic IR drop) analysis | Cells slower than the timing assumed, or failing, where the supply sags |
| (b) 0.10 µm spacing | DRC | Shorts and opens from lithography and etch the foundry cannot print reliably |
| (c) swapped mux inputs | Logical equivalence check of the final netlist against the RTL | A netlist that does not compute the specified function |
| (d) hold fails with parasitics | Signoff STA at every corner with extracted RC | Races that corrupt data at any clock frequency |
| (e) charge on a gate-only wire | Antenna check (part of DRC) | Gate-oxide damage during manufacture |
| (f) fill short to VDD | LVS | A layout whose connectivity differs from the netlist |
| (g) excessive current density | Electromigration check | Wires that open or short after years of operation |

(h) The budget is $0.05 \times 1.80$ = **90** mV; the measured droop is $0.08 \times 1.80$ = **144** mV, **54** mV over. Either the grid is strengthened (more straps or vias, decoupling, spreading the switching activity) until the droop is within budget, or timing is re-signed at the lower voltage with the margin that implies; the block cannot be signed off as is.

### Solution 19-11.15

(a) Connections crossing between A = {1, 2, 4} and B = {3, 5, 6}: (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (2, 5). The cut is **6**; only (1, 2) and (5, 6) are internal.

(b) Gains, as external minus internal connections:

| Cell | Side | External | Internal | Gain |
|---|---|---|---|---|
| 1 | A | 1 (to 3) | 1 (to 2) | **0** |
| 2 | A | 2 (to 3, 5) | 1 (to 1) | **1** |
| 4 | A | 3 (to 3, 5, 6) | 0 | **3** |
| 3 | B | 3 (to 1, 2, 4) | 0 | **3** |
| 5 | B | 2 (to 2, 4) | 1 (to 6) | **1** |
| 6 | B | 1 (to 4) | 1 (to 5) | **0** |

(c) Moving cell $a$ alone reduces the cut by $g_a$, and likewise $b$. If $a$ and $b$ are connected, each gain counted their connection as removed, but after the swap it still crosses, now in the other direction; subtracting it twice gives $g_a + g_b - 2w_{ab}$. The best swap is 4 with 3: $3 + 3 - 2 \times 1$ = **4**, against 3 for swapping 4 with 5 ($3 + 1 - 2$) and 3 for swapping 4 with 6 ($3 + 0 - 0$). The new partition A = {1, 2, 3}, B = {4, 5, 6} has a cut of $6 - 4$ = **2**: (3, 4) and (2, 5).

(d) New gains: cells 1 and 6 have $-2$; cells 2, 3, 4 and 5 have $-1$. Every swap gain is at most $-1 + (-1) - 0$ = **−2**, so no single swap helps. A Fiduccia–Mattheyses pass would still make these moves tentatively and keep the best prefix, which here is the swap already made.

(e) There are $\binom{6}{3}/2$ = **10** distinct bisections. Checking all ten gives cuts of 2, 4, 4, 5, 5, 5, 5, 6, 6 and 6, so the result is the unique global minimum. Here the two triangles {1, 2, 3} and {4, 5, 6} are the natural clusters, which is what multilevel partitioners find by coarsening first.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-11.1a | core area | 171429 | µm² |
| 19-11.1b | core width | 292.77 | µm |
| 19-11.1c | rows | 216 | — |
| 19-11.1d | core height | 587.52 | µm |
| 19-11.1e | sites per row | 636 | — |
| 19-11.1f | achieved utilization | 69.76 | % |
| 19-11.1g | site-aligned core width | 292.56 | µm |
| 19-11.1h | utilization with site-aligned width | 69.81 | % |
| 19-11.2a | drop fed at both ends | 5.0 | mV |
| 19-11.2b | drop fed at one end | 20 | mV |
| 19-11.2c | drop with a middle feed | 1.25 | mV |
| 19-11.3a | HPWL of the three-pin net | 16 | — |
| 19-11.3b | tree length of the three-pin net | 16 | — |
| 19-11.4a | position of B | 9 | — |
| 19-11.4b | position of A | 7.5 | — |
| 19-11.4c | shift of each cell | 3 | — |
| 19-11.5a | Manhattan distance | 6 | — |
| 19-11.5b | shortest legal path | 12 | — |
| 19-11.6a | HPWL of the plus net | 8 | — |
| 19-11.6b | RMST of the plus net | 12 | — |
| 19-11.6c | RSMT of the plus net | 8 | — |
| 19-11.6d | RMST over RSMT | 1.5 | — |
| 19-11.7a | tapping point from subtree 1 | 308.3 | µm |
| 19-11.7b | merged Elmore constant | 16.55 | ps |
| 19-11.7c | merged capacitance | 200 | fF |
| 19-11.7d | unconstrained tapping point, 80 ps case | 1442 | µm |
| 19-11.7e | balancing wire length | 1341 | µm |
| 19-11.7f | extra wire beyond 500 µm | 841 | µm |
| 19-11.8a | sinks | 64 | — |
| 19-11.8b | source-to-sink length | 1.75 | mm |
| 19-11.8c | total H-tree length | 21 | mm |
| 19-11.8d | H-tree wire capacitance | 4.2 | pF |
| 19-11.9a | total clock capacitance | 41.88 | pF |
| 19-11.9b | clock power | 13.57 | mW |
| 19-11.9c | flip-flop share of clock capacitance | 86 | % |
| 19-11.10a | metal-1 resistance per length | 0.893 | Ω/µm |
| 19-11.10b | metal-3 resistance per length | 0.157 | Ω/µm |
| 19-11.10c | metal-5 resistance per length | 0.0178 | Ω/µm |
| 19-11.10d | flow estimate over PDK value, metal 1 | 1.35 | — |
| 19-11.10e | 2 mm metal-3 wire resistance | 313 | Ω |
| 19-11.10f | metal-1 minimum-width current limit | 0.392 | mA |
| 19-11.10g | metal-3 minimum-width current limit | 2.04 | mA |
| 19-11.10h | metal-1 width for 1.5 mA | 0.536 | µm |
| 19-11.12a | point-load drop at the macro | 37.5 | mV |
| 19-11.12b | worst total drop | 46.9 | mV |
| 19-11.12c | position of worst drop | 50 | µm |
| 19-11.12d | uniform-load drop alone | 12.5 | mV |
| 19-11.12e | worst drop with the macro at the middle | 62.5 | mV |
| 19-11.13a | driver term, 400 µm metal 1 | 110.20 | ps |
| 19-11.13b | wire term, 400 µm metal 1 | 15.70 | ps |
| 19-11.13c | delay, 400 µm metal 1 | 125.90 | ps |
| 19-11.13d | delay, 600 µm metal 1 | 191.84 | ps |
| 19-11.13e | slack lost to the detour | 65.94 | ps |
| 19-11.13f | crosstalk delay change, each way | 25.27 | ps |
| 19-11.13g | delay, 600 µm metal 3 | 200.36 | ps |
| 19-11.13h | delay, 600 µm metal 1, stronger driver | 112.43 | ps |
| 19-11.14a | IR-drop budget | 90 | mV |
| 19-11.14b | measured IR drop | 144 | mV |
| 19-11.14c | excess drop | 54 | mV |
| 19-11.15a | initial cut | 6 | — |
| 19-11.15b | gain of cell 4 | 3 | — |
| 19-11.15c | gain of cell 3 | 3 | — |
| 19-11.15d | gain of cell 2 | 1 | — |
| 19-11.15e | gain of cell 5 | 1 | — |
| 19-11.15f | gain of cells 1 and 6 | 0 | — |
| 19-11.15g | best swap gain | 4 | — |
| 19-11.15h | cut after the swap | 2 | — |
| 19-11.15i | best swap gain afterwards | -2 | — |
| 19-11.15j | distinct balanced bisections | 10 | — |
