# Solutions 27-02 · The Smartphone SoC

Problems: [27-02 problems](../problems/27-02-problems.md) · Chapter: [27-02](../chapters/27-02-smartphone-soc.md). Every number is recomputed by [verify_27_02.py](../verify/verify_27_02.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-02.1

(a) **Always-on island** (a tiny DSP and memory that run while the rest of the chip is power-gated). (b) **Video encoder**, a fixed-function block far more efficient than the CPU or GPU. (c) **Efficiency (little) core**, below the crossover. (d) **GPU**, built for parallel shading. (e) **ISP and NPU**, which align and merge frames in dedicated hardware.

### Solution 27-02.2

$14{,}400 \times 10^6 \times 8$ bytes = **115.2** GB/s; $10{,}667 \times 10^6 \times 8$ = **85.3** GB/s; ratio **1.35**.

### Solution 27-02.3

$2400 \times 1080 \times 4 \times 120$ = **1.244** GB/s; at 1 Hz **0.0104** GB/s; ratio **120**. A static screen need not be re-read 120 times a second; dropping the refresh rate saves display-engine and DRAM energy (and panel power), which is why always-on displays refresh slowly.

### Solution 27-02.4

The SLC catches $0.35 \times 45$ = **15.75** GB/s, leaving **44.25** GB/s for DRAM. Power saved: $15.75 \times 10^9 \times 8 \times 4.0 \times 10^{-12}$ = **0.504** W.

### Solution 27-02.5

(a) $V = 0.45 + 0.15 \times 2$ = 0.75 V; $E = 0.6 \times 0.75^2/4 + 0.05/(4 \times 2)$ = **0.0906** nJ.

(b) $P = 0.6 \times 0.75^2 \times 2 + 0.05$ = **0.725** W; performance $4 \times 2$ = **8** GIPS.

(c) $0.0906 \times 8$ = **0.725** W. ✓

### Solution 27-02.6

Solve $2ck(V_0 + kf)f^2 = P_s$: $0.18(0.45 + 0.15f)f^2 = 0.05$, numerically $f^*$ = **0.707** GHz, $V$ = **0.556** V, $E$ = **0.0641** nJ.

### Solution 27-02.7

(a) $1.5 \times 9600$ = **14,400** MT/s at 64 bits. (b) $1.5 \times 64$ = **96** bits at 9,600 MT/s. (c) $1.5 \times 76.8$ = **115.2** GB/s either way. Option (a) sits at the top of LPDDR6's 10,667–14,400 MT/s range, while the assumed 9,600 MT/s of (b) is below that range, so (b) means a wider LPDDR5X-class bus and package. The claim alone does not say which was done.

### Solution 27-02.8

Solve $1.2(0.45 + 0.12f)^2f + 0.10 = 2.0$: $f$ = **2.67** GHz, **63.5**% of maximum, **16.0** GIPS.

### Solution 27-02.9

(a) $7 \times 10^9 \times 4/8$ = **3.5** GB per token; $115.2/3.5$ = **32.9** tokens/s. (b) $3.5/12$ = **29.2**% of the DRAM, before the operating system, apps and the KV cache.

### Solution 27-02.10

(a) DPW **500**, yield **0.881**, cost **$41.98**.

(b) DPW **572**, yield **0.895**, cost **$36.15**.

(c) Modem DPW **2694**, yield **0.980**, cost **$4.54**; total $36.15 + 4.54 + 1.50$ = **$42.19**.

Integration is cheaper by about **$0.21** here, a small margin. The decision also weighs the chip-to-chip link's power, board area, the schedule coupling of the modem to the AP's node, and strategy (who designs the modem).

### Solution 27-02.11

(a) Pacing: $f = 2 \times 10^9/(6 \times 10^9)$ = 0.333 GHz; $E_{inst}$ = 0.098 nJ, so **0.196** J. Racing: $E_{inst}$ = 0.186 nJ at 4.2 GHz, **0.372** J, finishing in **0.0794** s.

(b) With $P_s$ = 0.6 W: pacing **0.696** J (leakage for the whole second dominates); racing **0.412** J.

(c) The leakage. With low leakage, pacing at low voltage beats racing; with high leakage, finishing fast and power-gating beats pacing. Neither is optimal in general (part d).

(d) Minimizing $E_{inst}(f)$: cool die $f^*$ = **0.798** GHz, above the 0.333 GHz deadline frequency, so Option C runs at $f^*$, finishes in 0.418 s and power-gates: $2 \times 10^9 \times 0.0805$ nJ = **0.161** J, less than pacing (0.196 J) or racing (0.372 J). Hot die: $f^*$ = **1.77** GHz and **0.289** J, less than racing (0.412 J). Even with high leakage, $f^*$ stays well below 4.2 GHz, so pure racing is an approximation to the optimum, not the optimum itself.

### Solution 27-02.12

(a) Memory $150 of a $600 BOM: **25**%.

(b) Before: $(1099 - 540)/1099$ = **50.9**%; after: $(1099 - 640)/1099$ = **41.8**%, a fall of **9.1** points.

(c) $640/(1 - 0.509)$ = **$1,302.52**, a rise of **$203.52**.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-02.2 | 14,400 MT/s bandwidth | 115.2 | GB/s |
| 27-02.2a | 10,667 MT/s bandwidth | 85.3 | GB/s |
| 27-02.2b | ratio | 1.35 | |
| 27-02.3 | 120 Hz read | 1.244 | GB/s |
| 27-02.3a | 1 Hz read | 0.0104 | GB/s |
| 27-02.3b | ratio | 120 | |
| 27-02.4 | caught by the SLC | 15.75 | GB/s |
| 27-02.4a | DRAM traffic | 44.25 | GB/s |
| 27-02.4b | power saved | 0.504 | W |
| 27-02.5a0 | voltage at 2 GHz | 0.75 | V |
| 27-02.5a | energy per instruction | 0.0906 | nJ |
| 27-02.5b | power | 0.725 | W |
| 27-02.5b1 | performance | 8 | GIPS |
| 27-02.5c | check | 0.725 | W |
| 27-02.6 | minimum-energy frequency | 0.707 | GHz |
| 27-02.6a | voltage | 0.556 | V |
| 27-02.6b | energy per instruction | 0.0641 | nJ |
| 27-02.7a | data rate at 64 bits | 14400 | MT/s |
| 27-02.7b | width at 9,600 MT/s | 96 | bits |
| 27-02.7c | bandwidth | 115.2 | GB/s |
| 27-02.8 | frequency at 2.0 W | 2.67 | GHz |
| 27-02.8a | fraction of maximum | 63.5 | % |
| 27-02.8b | performance | 16.0 | GIPS |
| 27-02.9a | bytes per token | 3.5 | GB |
| 27-02.9a1 | tokens per second | 32.9 | |
| 27-02.9b | share of DRAM | 29.2 | % |
| 27-02.10a | integrated dies per wafer | 500 | |
| 27-02.10a1 | integrated yield | 0.881 | |
| 27-02.10a2 | integrated cost | 41.98 | $ |
| 27-02.10b | smaller AP dies per wafer | 572 | |
| 27-02.10b1 | smaller AP yield | 0.895 | |
| 27-02.10b2 | smaller AP cost | 36.15 | $ |
| 27-02.10c | modem dies per wafer | 2694 | |
| 27-02.10c1 | modem yield | 0.980 | |
| 27-02.10c2 | modem cost | 4.54 | $ |
| 27-02.10c3 | split total | 42.19 | $ |
| 27-02.10c4 | integration saving | 0.21 | $ |
| 27-02.11a0 | paced frequency | 0.333 | GHz |
| 27-02.11a1 | paced energy per instruction | 0.098 | nJ |
| 27-02.11a | paced energy | 0.196 | J |
| 27-02.11a2 | race energy | 0.372 | J |
| 27-02.11a3 | race time | 0.0794 | s |
| 27-02.11b | paced energy, hot | 0.696 | J |
| 27-02.11b1 | race energy, hot | 0.412 | J |
| 27-02.11d | minimum-energy frequency, cool | 0.798 | GHz |
| 27-02.11d1 | Option C energy, cool | 0.161 | J |
| 27-02.11d2 | minimum-energy frequency, hot | 1.77 | GHz |
| 27-02.11d3 | Option C energy, hot | 0.289 | J |
| 27-02.12a | memory share | 25 | % |
| 27-02.12b | margin before | 50.9 | % |
| 27-02.12b1 | margin after | 41.8 | % |
| 27-02.12b2 | fall | 9.1 | points |
| 27-02.12c | restoring price | 1302.52 | $ |
| 27-02.12c1 | price rise | 203.52 | $ |
