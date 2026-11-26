# Solutions 27-01 · Method: Analyzing a System End to End

Problems: [27-01 problems](../problems/27-01-problems.md) · Chapter: [27-01](../chapters/27-01-system-analysis-method.md). Every number is recomputed by [verify_27_01.py](../verify/verify_27_01.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-01.1

(a) $1.8/3.85$ = **46.8**%.

(b) Core $2.0/0.90$ = **2.222** W; I/O $0.3/0.468$ = **0.642** W; total **2.864** W.

(c) $2.3/2.864$ = **80.3**%; loss **0.564** W, of which the LDO wastes $0.642 - 0.3$ = **0.342** W, more than its load.

### Solution 27-01.2

(a) **Energy and volume**: the battery is tiny and cannot grow, so battery life binds. (b) **Sustained thermal power**: without a fan, an hour of gaming runs at the surface-temperature limit, not at the burst limit. (c) **Memory bandwidth**: single-user decode is far below the ridge point. (d) **Cost**: in a commodity part sold in millions, every cent of BOM matters more than performance beyond the requirement.

### Solution 27-01.3

(a) $0.1 \times 3.0 + 0.9 \times 0.25$ = **0.525** W; $13.5/0.525$ = **25.7** h.

(b) Halving standby: **0.4125** W, **32.7** h. Halving active: **0.375** W, **36.0** h. Here the active mode's $d \times P$ (0.30 W) exceeds standby's (0.225 W), so halving active power is worth more, although the device is active only 10% of the time.

### Solution 27-01.4

Fan on: $(100 - 35)/2.6$ = **25.0** W. Fan off: $65/6.5$ = **10.0** W. The fan multiplies sustained power by 2.5.

### Solution 27-01.5

(a) $\tau = 5.0 \times 45$ = **225** s; $T_0 = 25 + 1.0 \times 5.0$ = **30** °C.

(b) $T_\infty = 25 + 6.0 \times 5.0$ = **55** °C; $t_b = 225\ln[(55 - 30)/(55 - 42)]$ = **147** s.

(c) $(42 - 25)/5.0$ = **3.4** W.

### Solution 27-01.6

(a) $40 \times 10^{12}/(64 \times 10^9)$ = **625** operations/byte.

(b) 900 > 625: compute bound at **40** TOPS.

(c) $2 \times 64$ = **128** GOPS, **0.32**% of peak.

(d) $3 \times 10^9 \times 0.5$ = **1.5** GB per token; $64/1.5$ = **42.7** tokens/s. With 4-bit weights the intensity doubles to 4 operations/byte, still far below the ridge, so the step stays bandwidth-bound.

### Solution 27-01.7

(a) **70** GB per token: $3.2 \times 10^{12}/(70 \times 10^9)$ = **45.7** tokens/s.

(b) Intensity $2B$ reaches 125 at $B$ = **62.5**, so **63** users.

### Solution 27-01.8

(a) **8** Gb/s, set by the second stage.

(b) $8 \times 10^9/(1500 \times 8)$ = **6.67e5** packets/s.

(c) $L = 6.67 \times 10^5 \times 0.002$ = **1333** packets; $8 \times 10^9 \times 0.002/8$ bytes = **2.0** MB.

### Solution 27-01.9

(a) BOM **$96**; COGS **$110**; GM $(249 - 110)/249$ = **55.8**%.

(b) $22/96$ = **22.9**%.

(c) COGS must be at most $0.40 \times 249$ = **$99.60**, a reduction of **$10.40**, about a tenth of the COGS.

### Solution 27-01.10

(a) $1/(0.6 + 0.4/20)$ = **1.61**.

(b) $1/0.6$ = **1.67**.

(c) $1/(0.6/1.25 + 0.4/20) = 1/0.50$ = **2.0**: the unaccelerated part limits the gain, so speeding it up is worth more than a faster NPU.

### Solution 27-01.11

(a) At the cap, $P_{dyn}$ is fixed. With $P_{dyn} = kpf^3$ after the change and $kf_0^3$ before, $f/f_0 = p^{-1/3}$. Performance is IPC × $f$, so it changes by $g\,p^{-1/3}$, which exceeds 1 only if $g > p^{1/3}$.

(b) $1.40^{1/3}$ = **1.119** > 1.10: performance falls to **0.983**, **1.7**% slower.

(c) $1.20^{1/3}$ = **1.063** < 1.08: performance rises to **1.016**, **1.6**% faster.

### Solution 27-01.12

(a) $1/(50 \times 10^{12})$ J = **20** fJ per operation.

(b) $8 \times 3.9$ = **31.2** pJ per operation, **1560** times the compute energy.

(c) Almost all operands must come from on-chip memory: each byte fetched from DRAM must be reused about 1,560 times just for memory energy to equal compute energy, and since the 20 fJ per operation is the whole 1 W budget, the reuse must be well above that. HBM's 3.9 pJ/bit is also optimistic for an edge NPU, which would use LPDDR at a higher energy per bit, so the 1,560 is a lower bound. The claim is plausible only for workloads with high reuse (convolutions with weights held on chip), at the lowest precision and peak utilization; it says nothing about memory-bound workloads such as decode.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-01.1a | LDO efficiency | 46.8 | % |
| 27-01.1b | core battery-side power | 2.222 | W |
| 27-01.1b1 | I/O battery-side power | 0.642 | W |
| 27-01.1b2 | battery power | 2.864 | W |
| 27-01.1c | system efficiency | 80.3 | % |
| 27-01.1c1 | total loss | 0.564 | W |
| 27-01.1c2 | LDO loss | 0.342 | W |
| 27-01.3a | average power | 0.525 | W |
| 27-01.3a1 | battery life | 25.7 | h |
| 27-01.3b | average, standby halved | 0.4125 | W |
| 27-01.3b1 | life, standby halved | 32.7 | h |
| 27-01.3b2 | average, active halved | 0.375 | W |
| 27-01.3b3 | life, active halved | 36.0 | h |
| 27-01.3c | active share of the average | 0.30 | W |
| 27-01.3c1 | standby share of the average | 0.225 | W |
| 27-01.4 | sustained power, fan on | 25.0 | W |
| 27-01.4a | sustained power, fan off | 10.0 | W |
| 27-01.4b | fan's multiple | 2.5 | |
| 27-01.5a | time constant | 225 | s |
| 27-01.5a1 | starting temperature | 30 | °C |
| 27-01.5b | burst final temperature | 55 | °C |
| 27-01.5b1 | burst duration | 147 | s |
| 27-01.5c | sustained power | 3.4 | W |
| 27-01.6a | ridge point | 625 | ops/byte |
| 27-01.6b | convolution rate | 40 | TOPS |
| 27-01.6c | decode rate | 128 | GOPS |
| 27-01.6c1 | fraction of peak | 0.32 | % |
| 27-01.6d0 | bytes per token | 1.5 | GB |
| 27-01.6d | tokens per second | 42.7 | |
| 27-01.7a0 | bytes per token | 70 | GB |
| 27-01.7a | single-user tokens per second | 45.7 | |
| 27-01.7b | batch at the ridge | 62.5 | |
| 27-01.7b1 | users needed | 63 | |
| 27-01.8a | throughput | 8 | Gb/s |
| 27-01.8b | packet rate | 6.67e5 | per s |
| 27-01.8c | packets in flight | 1333 | |
| 27-01.8c1 | buffer memory | 2.0 | MB |
| 27-01.9a | BOM | 96 | $ |
| 27-01.9a1 | COGS | 110 | $ |
| 27-01.9a2 | gross margin | 55.8 | % |
| 27-01.9b | display share | 22.9 | % |
| 27-01.9c | COGS for 60% margin | 99.60 | $ |
| 27-01.9c1 | reduction needed | 10.40 | $ |
| 27-01.10a | speedup | 1.61 | |
| 27-01.10b | limit | 1.67 | |
| 27-01.10c | speedup with a faster CPU part | 2.0 | |
| 27-01.11b | threshold, p = 1.40 | 1.119 | |
| 27-01.11b1 | performance factor | 0.983 | |
| 27-01.11b2 | loss | 1.7 | % |
| 27-01.11c | threshold, p = 1.20 | 1.063 | |
| 27-01.11c1 | performance factor | 1.016 | |
| 27-01.11c2 | gain | 1.6 | % |
| 27-01.12a | compute energy | 20 | fJ/op |
| 27-01.12b | memory energy | 31.2 | pJ/op |
| 27-01.12b1 | ratio | 1560 | |
