# Solutions 27-05 · The PC SoC

Problems: [27-05 problems](../problems/27-05-problems.md) · Chapter: [27-05](../chapters/27-05-pc-soc.md). Every number is recomputed by [verify_27_05.py](../verify/verify_27_05.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-05.1

(a) **Media engine**: fixed-function decode at a fraction of the CPU's or GPU's energy. (b) **NPU**: a sustained, low-power neural workload. (c) **CPU** (performance cores): branchy, latency-sensitive, multi-threaded integer work. (d) **GPU**: massively parallel shading. (e) **GPU** (or CPU), using unified memory: the NPU's fixed formats and memory limits exclude it, and the GPU can address the shared pool.

### Solution 27-05.2

(a) $128/8 \times 9600 \times 10^6$ = **153.6** GB/s. (b) $512/8 \times 8533 \times 10^6$ = **546.1** GB/s.

### Solution 27-05.3

$\bar P_{SoC} = 0.05 \times 6.0 + 0.15 \times 1.5 + 0.80 \times 0.30$ = **0.765** W. Total **3.265** W; life $60/3.265$ = **18.4** h.

### Solution 27-05.4

(a) $t = 56\ln[(115 - 10)/(115 - 45)] = 56\ln(1.5)$ = **22.7** s.

(b) At a constant 5 W the average decays as $y(t) = 5 + (45 - 5)e^{-t/56}$; it reaches 10 W when $e^{-t/56} = 5/40$: $t = 56\ln 8$ = **116.4** s. A full recovery takes several time constants; back-to-back tasks get much less turbo.

### Solution 27-05.5

(a) At 4 bits each parameter takes 0.5 byte: $24/0.5$ = **48** billion parameters. At 8 bits: **24** billion.

(b) A 32B 4-bit model is 16 GB: $136.5/16$ = **8.53** tokens/s.

### Solution 27-05.6

Prefill: $2 \times 8 \times 10^9 \times 2000/(40 \times 10^{12} \times 0.5)$ = **1.60** s. Decode bound: $136.5/4$ = **34.1** tokens/s, so 500 tokens take **14.7** s. Total **16.3** s; here decoding dominates.

### Solution 27-05.7

NPU: $5 \times 10^{13}/(20 \times 10^{12})$ = **2.50** s; energy $5 \times 10^{13}/(6 \times 10^{12})$ = **8.33** J. GPU: $5 \times 10^{13}/(72 \times 10^{12})$ = **0.694** s; energy $33.3 + 0.5 \times 0.694$ = **33.7** J. The GPU is **3.6** times faster and uses **4.04** times the energy: the NPU is the battery choice, the GPU the waiting-time choice.

### Solution 27-05.8

Monolithic: **143** dies per wafer, yield $e^{-0.40}$ = **0.670**, cost **$193.00**. Tiles: 200 mm² gives **306** dies per wafer at yield 0.819, **$73.84** each; package $(2 \times 73.84 + 10)/0.97$ = **$162.56**. Ratio **0.842**: on the same node and with no interface area, splitting a large die still saves 16% because yield falls exponentially with area.

### Solution 27-05.9

$E_{bit} \le 1\ \text{W}/(10^{12} \times 8\ \text{bits/s})$ = **0.125** pJ/bit, close to on-die wiring energy; such links need very short, dense connections (hybrid bonding or silicon bridges, 25-07).

### Solution 27-05.10

$B = 1\ \text{W}/(8 \times 2 \times 10^{-12})$ = **62.5** GB/s of sustained traffic: heavy GPU or AI load, not office work.

### Solution 27-05.11

(a) $70/20 = 3.5$ W total, so the SoC may average $3.5 - 2.7$ = **0.80** W.

(b) $0.08 \times 5.0 + (0.92 - x) \times 1.2 + 0.25x = 0.80$, so $0.95x = 0.704$ and $x$ = **0.741**: the package must spend **74.1**% of the time in deep idle.

### Solution 27-05.12

Turbo runs 13.83 s at speed $(64/28)^{1/3} = 1.317$, completing $13.83 \times 1.317$ = **18.2** s of sustained-equivalent work. The remaining 41.8 s run at 28 W: total **55.6** s, **7.3**% less time (a speed gain of **7.9**%). Turbo transforms short tasks and barely moves long ones.

### Solution 27-05.13

(a) With $P = P_2$ constant, $\tau\,dy/dt = P_2 - y$. Separating, $dy/(P_2 - y) = dt/\tau$. Integrating from $P_0$ at $t = 0$ to $y$ at $t$: $-\ln[(P_2 - y)/(P_2 - P_0)] = t/\tau$, so

$$
y(t) = P_2 - (P_2 - P_0)\,e^{-t/\tau}.
$$

(b) Turbo ends when $y = P_1$: $P_2 - P_1 = (P_2 - P_0)e^{-t_{turbo}/\tau}$. Taking logarithms, $t_{turbo} = \tau\ln[(P_2 - P_0)/(P_2 - P_1)]$.

(c) Write the argument as $1 + x$ with $x = (P_1 - P_0)/(P_2 - P_1)$. For small $x$, $\ln(1 + x) \approx x$ (Taylor series), so $t_{turbo} \approx \tau(P_1 - P_0)/(P_2 - P_1)$: the headroom $P_1 - P_0$ is spent at the rate $P_2 - P_1$, scaled by $\tau$. Here $x = 3/36$. Exact: $28\ln(39/36)$ = **2.24** s. Approximate: $28 \times 3/36$ = **2.33** s, **4.1**% too long, because $\ln(1 + x) < x$.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-05.2a | 128-bit, 9600 MT/s | 153.6 | GB/s |
| 27-05.2b | 512-bit, 8533 MT/s | 546.1 | GB/s |
| 27-05.3a | SoC average power | 0.765 | W |
| 27-05.3b | total power | 3.265 | W |
| 27-05.3c | battery life | 18.4 | h |
| 27-05.4a | turbo duration | 22.7 | s |
| 27-05.4b | recovery to 10 W | 116.4 | s |
| 27-05.5a | largest model at 4 bits | 48 | billion |
| 27-05.5b | largest model at 8 bits | 24 | billion |
| 27-05.5c | 32B 4-bit footprint | 16 | GB |
| 27-05.5d | decode bound | 8.53 | tokens/s |
| 27-05.6a | prefill time | 1.60 | s |
| 27-05.6b | decode bound | 34.1 | tokens/s |
| 27-05.6c | decode time | 14.7 | s |
| 27-05.6d | total | 16.3 | s |
| 27-05.7a | NPU time | 2.50 | s |
| 27-05.7b | NPU energy | 8.33 | J |
| 27-05.7c | GPU time | 0.694 | s |
| 27-05.7d | GPU work energy | 33.3 | J |
| 27-05.7e | GPU energy | 33.7 | J |
| 27-05.7f | speed ratio | 3.6 | — |
| 27-05.7g | energy ratio | 4.04 | — |
| 27-05.8a | monolithic dies per wafer | 143 | — |
| 27-05.8b | monolithic yield | 0.670 | — |
| 27-05.8c | monolithic cost | 193.00 | $ |
| 27-05.8d | tile dies per wafer | 306 | — |
| 27-05.8e | tile yield | 0.819 | — |
| 27-05.8f | tile cost | 73.84 | $ |
| 27-05.8g | two-tile package cost | 162.56 | $ |
| 27-05.8h | cost ratio | 0.842 | — |
| 27-05.8i | saving | 16 | % |
| 27-05.9 | energy per bit | 0.125 | pJ/bit |
| 27-05.10 | traffic for 1 W saving | 62.5 | GB/s |
| 27-05.11a | allowed SoC power | 0.80 | W |
| 27-05.11b | deep-idle residency | 0.741 | — |
| 27-05.11c | deep-idle residency | 74.1 | % |
| 27-05.11d | equation coefficient | 0.704 | W |
| 27-05.12a | turbo work done | 18.2 | s |
| 27-05.12b | total time | 55.6 | s |
| 27-05.12c | time saved | 7.3 | % |
| 27-05.12f | speed gain | 7.9 | % |
| 27-05.13a | exact turbo duration | 2.24 | s |
| 27-05.13b | linearized duration | 2.33 | s |
| 27-05.13c | linearization error | 4.1 | % |
| 27-05.12d | turbo speed factor | 1.317 | — |
| 27-05.12e | remaining time | 41.8 | s |
