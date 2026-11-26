# Course 27 · Final Exam Solutions

Questions: [README.md](README.md). Every number is recomputed, mostly by a second route, by [verify_27_exam.py](../verify/verify_27_exam.py). Intermediate values are shown rounded but carried at full precision.

---

**1 · A power and thermal budget.**
(a) The LDO's efficiency is $1.8/3.8 = 47.4\%$. Then $P_{batt} = 1.2/0.9 + 0.6/0.85 + 0.15/0.474 = 1.333 + 0.706 + 0.317$ = **2.36** W. The system efficiency is $1.95/2.36$ = **82.8**%, and the loss is **0.406** W, almost half of it in the LDO for a 0.15 W load.
(b) $0.9 \times 15/2.356$ = **5.73** h.
(c) $P_{sus} = (43 - 25)/9$ = **2.00** W.
(d) $T_\infty = 25 + 6 \times 9 = 79$ °C and $T_0 = 25 + 1 \times 9 = 34$ °C, so $t_b = 300\ln[(79 - 34)/(79 - 43)]$ = **66.9** s. The duty cycle is $d = (2.0 - 1.0)/(6.0 - 1.0)$ = **20.0**%.

**2 · Bottlenecks.**
(a) $\beta = 8\ \text{B} \times 8533 \times 10^6$ = **68.3** GB/s. The decode bound is $68.26 \times 10^9/(3 \times 10^9 \times 0.5)$ = **45.5** tokens/s.
(b) $1/(0.6 + 0.4/10)$ = **1.56**.
(c) By Little's law, $68.26\ \text{GB/s} \times 120\ \text{ns}$ = **8.19e3** bytes, that is **128** cache lines in flight.
(d) $d\ln(\text{perf}) = dP/(3P_{dyn}) = 0.3/9.0$ = **3.33**%.

**3 · Energy per instruction and memory traffic.**
(a) At 1 GHz, $V$ = 0.75 V and $E = 10^{-9} \times 0.5625/2 + 0.1/(2 \times 10^9)$ = **0.331** nJ. At 3 GHz, $V$ = 1.25 V and $E$ = **0.798** nJ.
(b) Bisection on $2ck(V_0 + kf)f^2 - P_s = 0$ gives $f^*$ = **0.559** GHz.
(c) $E(f^*)$ = **0.294** nJ. Below this frequency leakage per instruction grows faster than the dynamic energy falls.
(d) DRAM traffic: $30 \times 0.6 + 10 \times 0.8 + 15 \times 0.4$ = **32.0** GB/s. The interface gives $9600 \times 10^6 \times 8$ = **76.8** GB/s, so utilization is **41.7**%.

**4 · A smartwatch's day.**
(a) $P = \pi L_vA\,\text{APL}/\eta_v = \pi \times 400 \times 9 \times 10^{-4} \times 0.2/5$ = **45.2** mW.
(b) $Q = 2 \times 0.4 + 5 \times 0.25 + 6 \times 0.1$ = **2.65** µC (mA × ms = µC). Then $I = 3 + 2.65/0.1$ = **29.5** µA.
(c) $E_b = 0.300 \times 3.85$ = **1.155** Wh. $E_{day} = 0.0452 \times 2 + (0.020 + 0.003 + 0.005) \times 24$ = **0.762** Wh. $L = 24 \times 0.9 \times 0.9 \times 1.155/0.762$ = **29.4** h.
(d) $50 \times 20\ \mu\text{J} + 50 \times 2\ \text{mJ}/100$ = **2.00** mW batched; **101** mW unbatched.

**5 · Earbuds.**
(a) $-20\log_{10}[2\sin(\pi f\tau)]$: **28.5** dB at 200 Hz and **14.5** dB at 1 kHz.
(b) $1/(6\tau)$ = **5.56** kHz.
(c) $-20\log_{10}(0.03)$ = **30.5** dB.
(d) $E_b = 55 \times 3.85 = 211.75$ mWh. Life $= 211.75 \times 0.85/18$ = **10.0** h. Recharges $= 0.70 \times 500 \times 3.85/(2 \times 211.75)$ = **3.18**.

**6 · A laptop SoC.**
(a) $0.6 \times 0.5 + 0.3 \times 3 + 0.1 \times 15$ = **2.70** W; $60/(2.70 + 2.5)$ = **11.5** h.
(b) $28\ln[(55 - 5)/(55 - 28)]$ = **17.3** s.
(c) $16\ \text{B} \times 8533 \times 10^6$ = **136.5** GB/s; $136.5/(8 \times 0.5)$ = **34.1** tokens/s.
(d) $2 \times 8 \times 10^9 \times 2000/(45 \times 10^{12} \times 0.3)$ = **2.37** s.

**7 · A car.**
(a) $34 + 32 + 13 + \lfloor 65/4 \rfloor$ = **95** bits, taking **190** µs.
(b) $8.3 \times 10^6 \times 30 \times 12$ = **2.99** Gb/s.
(c) $v$ = 27.78 m/s. Then $27.78 \times 0.15 + 27.78^2/14$ = **59.3** m, of which **4.17** m is latency.
(d) $P_d = 150 \times 50$ = 7.5 kW, so $300/(300 + 7500)$ = **3.85**%.

**8 · Training at scale.**
(a) $6 \times 70 \times 10^9 \times 2 \times 10^{12}$ = **8.4e23** FLOP. Time: $8.4 \times 10^{23}/(1024 \times 0.4 \times 10^{15})$ s = **23.7** days.
(b) $2 \times (7/8) \times 2\ \text{GB}/200\ \text{GB/s}$ = **17.5** ms.
(c) The shard is $2/8$ GB. Cross-server: $2 \times (127/128) \times 0.25/50$ s = **9.92** ms; total **27.4** ms.
(d) $2 \times (1023/1024) \times 2/50$ s = **79.9** ms, **2.91** times slower.

**9 · Failures and serving.**
(a) $60\,000/20\,000$ = **3.00** h.
(b) $\sqrt{2 \times 30 \times 10\,800}$ = **805** s.
(c) $\sqrt{60/10\,800} + 300/10\,800$ = **10.2**%, so **89.8**% effective.
(d) $W = 140$ GB. Step time: $(140 + 64 \times 0.5)\ \text{GB}/(0.6 \times 64\ \text{TB/s})$ = **4.48** ms. Throughput: $64/4.48\ \text{ms}$ = **1.43e4** tokens/s. Per user: **223** tokens/s. Energy: $60\ \text{kW}/1.43 \times 10^4$ = **4.20** J per token.

**10 · At the edge.**
(a) $16 \times 16 \times 32 \times 9 \times 16$ = **1.18e6** MACs.
(b) CPU: **11.8** ms and **118** µJ. NPU: $1.18 \times 10^6/(64 \times 0.3 \times 10^8)$ = **0.614** ms and **9.22** µJ.
(c) $T_s = 256/125\ \text{kHz}$ = **2.048** ms. Payload: $8 + \lceil(96 - 32 + 28 + 16)/32\rceil \times 5$ = **28** symbols. Time on air: $(12.25 + 28) \times 2.048$ = **82.4** ms. Packets: $\lfloor 36/0.0824 \rfloor$ = **436** an hour.
(d) Streaming: $8000 \times 12 \times 50\ \text{nJ}$ = **4.80** mW. Local: $10 \times 9.22\ \mu\text{J} + 0.2\ \text{mW}$ = **0.292** mW, **16.4** times less.

**11 · An energy-neutral greenhouse sensor.**
(a) $8000/105$ = **76.2** W/m²; $76.19 \times 12 \times 10^{-4} \times 0.18 \times 0.8$ = **13.2** mW; $13.17\ \text{mW} \times 36\,000$ s = **474** J a day.
(b) $0.5 + 48 \times 0.040/86\,400 \times 10^3$ = **0.522** mW; **45.1** J a day; margin **10.5**.
(c) $0.522\ \text{mW} \times 72 \times 3600$ s = **135** J; $C = 2 \times 135.4/(25 - 6.25)$ = **14.4** F.
(d) With $I = -C\,dV/dt$, $P = VI = -CV\,dV/dt$, so $P\,dt = -CV\,dV$. Integrating from $V_{max}$ to $V_{min}$ at constant $P$:
$$
Pt = C\int_{V_{min}}^{V_{max}} V\,dV = \tfrac12 C(V_{max}^2 - V_{min}^2), \qquad t = \frac{C(V_{max}^2 - V_{min}^2)}{2P}.
$$
For 10 F: $t = 10 \times 18.75/(2 \times 0.522 \times 10^{-3})$ = **1.80e5** s = **49.9** h. That is short of the 72 h in (c), as expected from the 14.4 F it needs.

**12 · Rack decisions.**
(a) Split each device's vector into $p$ chunks of $S/p$ bytes and arrange the devices in a ring. In the reduce-scatter, step $k$ ($k = 1, \dots, p - 1$) has each device send one chunk to its neighbour, which adds it to its own copy. After $p - 1$ steps, each device holds one chunk summed over all $p$ devices. In the all-gather, $p - 1$ further steps circulate the reduced chunks until every device has all of them. Every step sends and receives $S/p$ bytes on every link at once (full duplex), taking $\alpha + S/(pB)$. Hence
$$
T = 2(p - 1)\left(\alpha + \frac{S}{pB}\right) = 2\frac{p - 1}{p}\frac{S}{B} + 2(p - 1)\alpha .
$$
(b) Bandwidth: $2 \times (71/72) \times 4\ \text{GB}/900\ \text{GB/s}$ = **8.77** ms. Latency: $2 \times 71 \times 2\ \mu\text{s}$ = **0.284** ms. Total **9.05** ms.
(c) Capital **900000** dollars a year. Energy: $140 \times 1.25 \times 8760 \times 0.07$ = **107310** dollars. Tokens: $1.2 \times 10^5 \times 0.5 \times 3.15 \times 10^7$ = **1.89e12** a year. Cost: $1\,007\,310/1.892 \times 10^6$ = **0.532** dollars per million tokens, of which energy is **10.7**%.
(d) See the rubric below.

---

**Rubric for 12(d)** (3 points, one per question with a credible answer).

- **Which operating point?** Throughput at what per-user speed and latency target, model, precision, context length and batch, compared with the old rack at the same per-user speed. Credible: the full throughput–interactivity curves of both racks, with the 3× at a stated, useful point.
- **Same power measured how?** Rack input or facility power, including networking and cooling, measured or nameplate. Credible: measured all-in power at both operating points, or tokens per joule at the meter.
- **What changed to produce 3×?** Lower precision, sparsity, a larger scale-up domain, more HBM, or software alone. Credible: a decomposition that adds up (for example 2× from FP4 against FP8 and 1.5× from batching enabled by more memory), with any accuracy cost of lower precision stated.
- **Also accept:** whether the old rack ran the same, current software (a fair baseline); and what the cost per million tokens is, since a 3× throughput at a much higher price may not lower cost.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X27.1a | battery power | 2.36 | W |
| X27.1a1 | system efficiency | 82.8 | % |
| X27.1a2 | conversion loss | 0.406 | W |
| X27.1a3 | LDO efficiency | 47.4 | % |
| X27.1b | battery life | 5.73 | h |
| X27.1c | sustained power | 2.00 | W |
| X27.1d | burst time | 66.9 | s |
| X27.1d1 | maximum burst duty | 20.0 | % |
| X27.2a | bandwidth | 68.3 | GB/s |
| X27.2a1 | decode bound | 45.5 | tokens/s |
| X27.2b | speed-up | 1.56 | — |
| X27.2c | bytes in flight | 8.19e3 | bytes |
| X27.2c1 | cache lines in flight | 128 | lines |
| X27.2d | performance gain | 3.33 | % |
| X27.3a | energy per instruction at 1 GHz | 0.331 | nJ |
| X27.3a1 | energy per instruction at 3 GHz | 0.798 | nJ |
| X27.3b | optimal frequency | 0.559 | GHz |
| X27.3c | minimum energy per instruction | 0.294 | nJ |
| X27.3d | DRAM traffic | 32.0 | GB/s |
| X27.3d1 | interface bandwidth | 76.8 | GB/s |
| X27.3d2 | utilization | 41.7 | % |
| X27.4a | display power | 45.2 | mW |
| X27.4b | connection-event charge | 2.65 | µC |
| X27.4b1 | average current | 29.5 | µA |
| X27.4c | battery energy | 1.155 | Wh |
| X27.4c1 | daily energy | 0.762 | Wh |
| X27.4c2 | battery life | 29.4 | h |
| X27.4d | power, batched | 2.00 | mW |
| X27.4d1 | power, unbatched | 101 | mW |
| X27.5a | attenuation at 200 Hz | 28.5 | dB |
| X27.5a1 | attenuation at 1 kHz | 14.5 | dB |
| X27.5b | amplification threshold | 5.56 | kHz |
| X27.5c | attenuation with 3% gain error | 30.5 | dB |
| X27.5d | bud life | 10.0 | h |
| X27.5d1 | recharges | 3.18 | — |
| X27.6a | average SoC power | 2.70 | W |
| X27.6a1 | battery life | 11.5 | h |
| X27.6b | turbo time | 17.3 | s |
| X27.6c | bandwidth | 136.5 | GB/s |
| X27.6c1 | decode bound | 34.1 | tokens/s |
| X27.6d | prefill time | 2.37 | s |
| X27.7a | frame length | 95 | bits |
| X27.7a1 | frame time | 190 | µs |
| X27.7b | camera rate | 2.99 | Gb/s |
| X27.7c | stopping distance | 59.3 | m |
| X27.7c1 | latency distance | 4.17 | m |
| X27.7d | range share | 3.85 | % |
| X27.8a | training compute | 8.4e23 | FLOP |
| X27.8a1 | training time | 23.7 | days |
| X27.8b | in-server all-reduce | 17.5 | ms |
| X27.8c | cross-server all-reduce | 9.92 | ms |
| X27.8c1 | hierarchical total | 27.4 | ms |
| X27.8d | flat ring | 79.9 | ms |
| X27.8d1 | flat over hierarchical | 2.91 | — |
| X27.9a | mean time between interruptions | 3.00 | h |
| X27.9b | Young's interval | 805 | s |
| X27.9c | lost fraction | 10.2 | % |
| X27.9c1 | effective training time | 89.8 | % |
| X27.9d | step time | 4.48 | ms |
| X27.9d1 | throughput | 1.43e4 | tokens/s |
| X27.9d2 | per-user speed | 223 | tokens/s |
| X27.9d3 | energy per token | 4.20 | J |
| X27.10a | MACs | 1.18e6 | MAC |
| X27.10b | CPU latency | 11.8 | ms |
| X27.10b1 | CPU energy | 118 | µJ |
| X27.10b2 | NPU latency | 0.614 | ms |
| X27.10b3 | NPU energy | 9.22 | µJ |
| X27.10c | symbol time | 2.048 | ms |
| X27.10c1 | payload symbols | 28 | symbols |
| X27.10c2 | time on air | 82.4 | ms |
| X27.10c3 | packets per hour | 436 | packets |
| X27.10d | streaming power | 4.80 | mW |
| X27.10d1 | local power | 0.292 | mW |
| X27.10d2 | ratio | 16.4 | — |
| X27.11a | irradiance | 76.2 | W/m² |
| X27.11a1 | harvested power | 13.2 | mW |
| X27.11a2 | daily harvest | 474 | J |
| X27.11b | average power | 0.522 | mW |
| X27.11b1 | daily energy | 45.1 | J |
| X27.11b2 | margin | 10.5 | — |
| X27.11c | energy for 72 h | 135 | J |
| X27.11c1 | supercapacitor | 14.4 | F |
| X27.11d | time on 10 F | 1.80e5 | s |
| X27.11d1 | time on 10 F | 49.9 | h |
| X27.12b | bandwidth term | 8.77 | ms |
| X27.12b1 | latency term | 0.284 | ms |
| X27.12b2 | total | 9.05 | ms |
| X27.12c | annual capital | 900000 | $ |
| X27.12c1 | annual energy | 107310 | $ |
| X27.12c2 | tokens per year | 1.89e12 | tokens |
| X27.12c3 | cost per million tokens | 0.532 | $ |
| X27.12c4 | energy share | 10.7 | % |
