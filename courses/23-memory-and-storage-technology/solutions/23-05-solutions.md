# Solutions 23-05 · HBM in Depth

Problems: [23-05 problems](../problems/23-05-problems.md) · Chapter: [23-05](../chapters/23-05-hbm-in-depth.md)

Every number is recomputed by [verify_23_05.py](../verify/verify_23_05.py).

---

## Solutions

### Solution 23-05.1

(a) $8 \times 16/8$ = **16** GB; (b) $16 \times 32/8$ = **64** GB, JEDEC's HBM4 maximum; (c) $8 \times 64$ = **512** GB; (d) $8 \times 24/8$ = **24** GB, the 8-high HBM3E size.

### Solution 23-05.2

(a) $1024 \times 8/8$ = **1024** GB/s; (b) $2048 \times 10/8$ = **2560** GB/s.

(c) $16 \times 2$ = **32**; (d) $32 \times 2$ = **64**.

(e) $1024/32$ = **32** bits; (f) $2048/64$ = **32** bits. HBM4 doubled the number of pseudo-channels, not their width.

### Solution 23-05.3

(a) $70\ \text{GB}/19.2\ \text{TB/s}$ = **3.65** ms; (b) $1/3.65\ \text{ms}$ = **274** tokens/s.

(c) $4 \times 1228.8\ \text{GB/s}/70\ \text{GB}$ = **70.2** tokens/s.

Each token at batch size 1 needs every weight once (23-01), so bandwidth divided by model size bounds the decode rate.

### Solution 23-05.4

(a) $0.9\ \text{pF} \times 0.75^2$ = **0.506** pJ; (b) a quarter: **0.127** pJ/bit.

(c) $2048 \times 10^9 \times 8 \times 0.1266\ \text{pJ}$ = **2.07** W.

A higher I/O voltage costs energy as $V^2$, which is why the 0.4 V swing of HBM3 (Example 23-05.3) was a deliberate choice.

### Solution 23-05.5

(a) $2\pi \times 3.9 \times 8.854 \times 10^{-12} \times 40\ \mu\text{m}/\ln(3.5/3)$ = **56.3** fF.

(b) $1.72 \times 10^{-8} \times 40\ \mu\text{m}/(\pi \times (3\ \mu\text{m})^2)$ = **24.3** mΩ.

(c) $\ln(3.25/3)$ is about half of $\ln(3.5/3)$, so **108** fF. Halving a thin liner roughly doubles the capacitance.

### Solution 23-05.6

$30{,}000 \times (30\ \mu\text{m})^2 = 27\ \text{mm}^2$, of 121 mm²: **22.3** %. Keep-out rules, not copper, decide how many TSVs a die can afford.

### Solution 23-05.7

(a) $(775 - 150)/12$ = **52.1** µm; (b) $52.08 - 15$ = **37.1** µm.

(c) $625/16$ = **39.1** µm; (d) **24.1** µm.

(e) $625/20$ = **31.25** µm; (f) **16.25** µm.

### Solution 23-05.8

(a) $10\ \mu\text{m}/(2.5 \times 140.8\ \text{mm}^2)$ = **0.0284** K/W; (b) plus the silicon's 0.00142 K/W: **0.0298** K/W.

(c) $0.02983 \times 280$ = **8.35** K; (d) $0.02983 \times 186$ = **5.55** K.

A better gap fill lets a 16-high stack run cooler than the 12-high stack of Example 23-05.6.

### Solution 23-05.9

Number the nodes from the base die (0) up to the top die (16), which the lid holds at 75 °C. Layer $j$ lies between nodes $j - 1$ and $j$ and carries $P_b + (j - 1)P_c$. Summing the drops from the top down to node $k$:

$$
T_k = 75 + R_L\sum_{j=k+1}^{16}\left[10 + (j - 1)\right] = 75 + R_L\left[280 - 9k - \tfrac{k(k + 1)}{2}\right]\ {}^\circ\text{C},
$$

with $R_L$ = 0.04877 K/W.

(a) $k = 0$: **88.66** °C. (b) $k = 5$: $75 + 0.04877 \times 220$ = **85.73** °C. (c) $k = 6$: $75 + 0.04877 \times 205$ = **85.00** °C.

(d) Core dies 1 to 5 exceed 85 °C: **5** dies, plus the base die. Die 6 sits within a hundredth of a degree of the threshold.

Those dies (and their banks) would need doubled refresh. Controllers with per-die temperature reporting can refresh only the hot part of the stack.

### Solution 23-05.10

(a) $0.998^{16}$ = **0.968**; (b) $0.95^{1/16}$ = **0.9968**; (c) $0.95^{16}$ = **0.440**.

### Solution 23-05.11

(a) $(0.25/0.10)/(0.75/0.90)$ = **3.00**. (b) $1.5/0.9$ = **1.67**. (c) $3.00/1.67$ = **1.80**.

The remaining factor would come from other losses: extra process steps that cut wafer throughput, test and repair overheads, and capacity tied up in qualification and ramp.

### Solution 23-05.12

(a) $\pi \times 300^2/8000 - \pi \times 300/\sqrt{4000}$ = 20.4, so **20**; (b) $\pi \times 300^2/16000 - \pi \times 300/\sqrt{8000}$ = 7.1, so **7**.

(c) $20 \times 120{,}000 \times 0.85$ = **2.04** million; (d) $7 \times 120{,}000 \times 0.85$ = **0.714** million.

Doubling the interposer area cuts packages per wafer by almost a factor of 3, because more of the round wafer's edge is wasted.

### Solution 23-05.13

(a) **1.46**, the "approximately 46%" above the standard; (b) **1.22**, the "1.22x"; (c) **1.35**.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-05.1a | 8-high, 16 Gb | 16 | GB |
| 23-05.1b | 16-high, 32 Gb | 64 | GB |
| 23-05.1c | eight 64 GB stacks | 512 | GB |
| 23-05.1d | 8-high, 24 Gb | 24 | GB |
| 23-05.2a | HBM3E at 8 Gb/s | 1024 | GB/s |
| 23-05.2b | HBM4 at 10 Gb/s | 2560 | GB/s |
| 23-05.2c | HBM3 pseudo-channels | 32 | |
| 23-05.2d | HBM4 pseudo-channels | 64 | |
| 23-05.2e | bits per HBM3 pseudo-channel | 32 | |
| 23-05.2f | bits per HBM4 pseudo-channel | 32 | |
| 23-05.3a | time to read 70 GB | 3.65 | ms |
| 23-05.3b | token-rate bound, 19.2 TB/s | 274 | tokens/s |
| 23-05.3c | token-rate bound, four HBM3E stacks | 70.2 | tokens/s |
| 23-05.4a | transition energy | 0.506 | pJ |
| 23-05.4b | energy per bit | 0.127 | pJ |
| 23-05.4b1 | energy per bit, 4 s.f. | 0.1266 | pJ |
| 23-05.4c | interface power | 2.07 | W |
| 23-05.5a | TSV capacitance | 56.3 | fF |
| 23-05.5b | TSV resistance | 24.3 | mΩ |
| 23-05.5c | capacitance, thinner liner | 108 | fF |
| 23-05.6 | keep-out fraction | 22.3 | % |
| 23-05.6a | keep-out area | 27 | mm² |
| 23-05.7a | pitch, 12 layers | 52.1 | µm |
| 23-05.7a1 | pitch, 12 layers, 4 s.f. | 52.08 | µm |
| 23-05.7b | die, 12 layers | 37.1 | µm |
| 23-05.7c0 | height for layers | 625 | µm |
| 23-05.7c | pitch, 16 layers | 39.1 | µm |
| 23-05.7d | die, 16 layers | 24.1 | µm |
| 23-05.7e | pitch, 20 layers | 31.25 | µm |
| 23-05.7f | die, 20 layers | 16.25 | µm |
| 23-05.8a | gap resistance | 0.0284 | K/W |
| 23-05.8b | layer resistance | 0.0298 | K/W |
| 23-05.8b1 | layer resistance, 4 s.f. | 0.02983 | K/W |
| 23-05.8c | base rise, 16 layers | 8.35 | K |
| 23-05.8d | base rise, 12 layers | 5.55 | K |
| 23-05.9a | base die temperature | 88.66 | °C |
| 23-05.9b | core die 5 temperature | 85.73 | °C |
| 23-05.9c | core die 6 temperature | 85.00 | °C |
| 23-05.9d | core dies above 85 °C | 5 | |
| 23-05.9x1 | bracket sum, die 5 | 220 | |
| 23-05.9x2 | bracket sum, die 6 | 205 | |
| 23-05.10a | 16-high yield | 0.968 | |
| 23-05.10b | per-layer yield for 95% | 0.9968 | |
| 23-05.10c | untested 16-high yield | 0.440 | |
| 23-05.11a | wafers per bit | 3.00 | |
| 23-05.11b | factor explained | 1.67 | |
| 23-05.11c | factor remaining | 1.80 | |
| 23-05.12a0 | estimate, 2,000 mm² | 20.4 | |
| 23-05.12a | interposers, 2,000 mm² | 20 | |
| 23-05.12b0 | estimate, 4,000 mm² | 7.1 | |
| 23-05.12b | interposers, 4,000 mm² | 7 | |
| 23-05.12c | packages per month, 2,000 mm² | 2.04e6 | |
| 23-05.12d | packages per month, 4,000 mm² | 0.714e6 | |
| 23-05.12x | packages-per-wafer ratio | 3 | |
| 23-05.13a | 11.7 over 8 | 1.46 | |
| 23-05.13b | 11.7 over 9.6 | 1.22 | |
| 23-05.13c | 13 over 9.6 | 1.35 | |
