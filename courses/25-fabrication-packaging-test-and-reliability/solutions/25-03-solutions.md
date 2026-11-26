# Solutions 25-03 · Deposition, Etch, CMP, Implant and Metrology

Problems: [25-03 problems](../problems/25-03-problems.md) · Chapter: [25-03](../chapters/25-03-deposition-etch-cmp-implant-metrology.md)

Every number is recomputed by [verify_25_03.py](../verify/verify_25_03.py).

---

## Solutions

### Solution 25-03.1

$20 \times 1.0/21$ = **0.952** cm/s, within 5% of $h_g$: transport-limited. Raising temperature barely helps; increase the gas supply (flow, partial pressure) or thin the boundary layer (lower pressure, better reactor geometry).

### Solution 25-03.2

(a) Supply $F_1 = h_g(C_g - C_s)$ and reaction $F_2 = k_sC_s$ are equal at steady state, so $C_s = h_gC_g/(h_g + k_s)$ and $F = k_sC_s = k_sh_gC_g/(k_s + h_g)$. Dividing by $N$ gives $v$. If $k_s \ll h_g$, $v \approx k_sC_g/N$ (reaction-limited); if $k_s \gg h_g$, $v \approx h_gC_g/N$ (transport-limited).

(b) With $k_s = h_g = h$: $h^2/(2h) = h/2$.

(c) Solve $0.050\,e^{-(1.5/k)(1/T - 1/923.15)} = 2.0$ for $T$: **875** °C. Below it the process is reaction-limited, above it transport-limited.

### Solution 25-03.3

$3.0/0.09$ = 33.3, so **34** cycles, taking $34 \times 3.0$ = **102** s.

### Solution 25-03.4

(a) $0.020 \times 63.55/(2 \times 96{,}485 \times 8.96)$ cm/s = **7.35** nm/s.

(b) $1500/7.35$ = **204** s.

(c) $0.020\ \text{A/cm}^2 \times 707\ \text{cm}^2 \times 204\ \text{s}$ = **2.9e3** C. The charge for a given thickness does not depend on the current density; only the time does.

### Solution 25-03.5

Nominal clearing is $80/60$ = 1.333 min, so the recipe runs **1.73** min. The fastest region (64.8 nm/min) clears at **1.23** min and its stop layer is exposed for **0.499** min. Requiring $0.499 \times 64.8/S \le 1.0$ gives $S \ge$ **32.3**, so about 33:1.

### Solution 25-03.6

(a) $300 \times 1.1$ = **330** nm per edge.

(b) $1000 - 2 \times 330$ = **340** nm.

(c) The undercut is as large as the film is thick, so features narrower than about twice the film thickness disappear; anisotropic plasma etching avoids it.

### Solution 25-03.7

(a) $2.4 \times 10^{-13} \times 3.0 \times 6895 \times 1.5$ m/s = **447** nm/min.

(b) $400/447$ = **0.90** min.

### Solution 25-03.8

(a) $199/0.50$ = **397** nm/min.

(b) $300/397$ = **0.76** min. Compared with the 25% region's 794 nm/min, this region planarizes half as fast: the two regions finish at different times, which is the origin of within-die thickness variation.

### Solution 25-03.9

(a) $5 \times 10^{15} \times 1.602 \times 10^{-19} \times 707/0.0050$ = **113** s.

(b) $5 \times 10^{15}/(\sqrt{2\pi} \times 20 \times 10^{-7})$ = **9.97e20** cm⁻³.

### Solution 25-03.10

$\sqrt{2\ln(9.97 \times 10^{20}/10^{17})}$ = **4.29**, so $x_j = 50 + 20 \times 4.29$ = **136** nm.

### Solution 25-03.11

(a) At 950 °C, $kT$ = **0.1054** eV and $D = 0.76\,e^{-3.46/0.1054}$ = **4.21e-15** cm²/s.

(b) $30 \times 1.53 \times 10^{-14}/4.21 \times 10^{-15}$ = **109** min.

(c) The same diffusion can be bought at lower temperature, but activation, damage annealing and other temperature-sensitive steps (silicides, gate stacks) differ; a lower temperature for a longer time also lengthens cycle time. Equal $Dt$ is only one of several constraints.

### Solution 25-03.12

(a) $\sigma_m = 0.10 \times 3.0/6$ = **0.050** nm.

(b) $\sqrt{0.40^2 + 0.050^2}$ = **0.403** nm, less than 1% above the true spread.

### Solution 25-03.13

(a) DRAM: $38.8/1.390$ = **27.9** $B; foundry/logic: $78.0/1.189$ = **65.6** $B.

(b) $143.9 - 116.9$ = **27.0** $B.

### Solution 25-03.14

(a) $0.5431 + 0.30 \times (0.5658 - 0.5431)$ = **0.5499** nm.

(b) $(0.5499 - 0.5431)/0.5431$ = **1.25**%.

(c) Compression: the SiGe film's natural spacing is larger than silicon's, and it is squeezed in the plane to match.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-03.1a | effective rate constant | 0.952 | cm/s |
| 25-03.2c | temperature where ks = hg | 875 | °C |
| 25-03.3a | cycles | 34 | |
| 25-03.3a0 | exact cycles | 33.3 | |
| 25-03.3b | time | 102 | s |
| 25-03.4a | plating rate | 7.35 | nm/s |
| 25-03.4b | time for 1.5 µm | 204 | s |
| 25-03.4c | charge | 2.9e3 | C |
| 25-03.5a0 | nominal clearing time | 1.333 | min |
| 25-03.5a | recipe time | 1.73 | min |
| 25-03.5b0 | fastest etch rate | 64.8 | nm/min |
| 25-03.5b | fastest clearing time | 1.23 | min |
| 25-03.5b1 | stop-layer exposure | 0.499 | min |
| 25-03.5c | required selectivity | 32.3 | |
| 25-03.6a | undercut per edge | 330 | nm |
| 25-03.6b | remaining width | 340 | nm |
| 25-03.7a | removal rate | 447 | nm/min |
| 25-03.7b | time for 400 nm | 0.90 | min |
| 25-03.8a | rate on 50% features | 397 | nm/min |
| 25-03.8b | time to remove a 300 nm step | 0.76 | min |
| 25-03.9a | implant time | 113 | s |
| 25-03.9b | peak concentration | 9.97e20 | cm⁻³ |
| 25-03.10a | square-root factor | 4.29 | |
| 25-03.10b | junction depth | 136 | nm |
| 25-03.11a0 | kT at 950 C | 0.1054 | eV |
| 25-03.11a | D at 950 C | 4.21e-15 | cm²/s |
| 25-03.11b | equivalent time | 109 | min |
| 25-03.12a | gauge sigma for P/T = 0.1 | 0.050 | nm |
| 25-03.12b | apparent spread | 0.403 | nm |
| 25-03.13a | DRAM 2025 | 27.9 | $B |
| 25-03.13a1 | foundry/logic 2025 | 65.6 | $B |
| 25-03.13b | WFE increase | 27.0 | $B |
| 25-03.14a | SiGe lattice constant | 0.5499 | nm |
| 25-03.14b | mismatch | 1.25 | % |
