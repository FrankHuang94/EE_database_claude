# Solutions 27-07 · The AI Datacenter Server and Rack

Problems: [27-07 problems](../problems/27-07-problems.md) · Chapter: [27-07](../chapters/27-07-ai-datacenter-server-and-rack.md). Every number is recomputed by [verify_27_07.py](../verify/verify_27_07.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-07.1

(a) **HBM bandwidth.** Each token reads all the weights for one sequence. Respond by batching, by quantizing the weights, or by spreading the model over more devices for aggregate bandwidth.

(b) **The scale-up fabric.** Tensor parallelism exchanges activations several times per layer, and half the group sits on the other side of the network. Respond by keeping tensor parallelism inside one NVLink domain, or by using a larger domain.

(c) **The scale-out network**, through its latency term (2 × 3,999 steps) as well as its bandwidth. Respond with a hierarchical all-reduce that uses the scale-up domain, and by overlapping it with the backward pass.

(d) **Power** (provisioned, not average). Respond with power capping and smoothing to lower the provisioned power per rack, a lower PUE, or more efficient accelerators.

(e) **Reliability.** The job is interrupted every few minutes to tens of minutes. Respond with fast asynchronous checkpoints, spare nodes and automated restart.

### Solution 27-07.2

HBM: $13.4 \times 1.5$ = **20.1** TB, **279** GB per GPU. Dense FP4: $720 \times 1.5$ = **1080** PFLOPS, **15.0** PFLOP/s per GPU. The two grow together, so the ratio of capacity to compute is unchanged. The extra memory buys larger batches and longer contexts (§3.7).

### Solution 27-07.3

$6 \times 70 \times 10^9 \times 15 \times 10^{12}$ = **6.3e24** FLOP. Time: $6.3 \times 10^{24}/(4096 \times 400 \times 10^{12})$ = 3.85 × 10⁶ s = **44.5** days.

### Solution 27-07.4

(a) $72 \times 1.4 = 100.8$ kW of GPUs. Adding the same 10.8 + 10.8 + 7.2 + 2.0 kW gives **131.6** kW at the busbar and $131.6/0.97$ = **135.7** kW at the input.

(b) $100.8/135.7$ = **74.3**%.

(c) $100\,000/(135.7 \times 1.2) = 614.2$, so **614** racks and **44208** GPUs, 11% fewer than with 1.2 kW GPUs. A faster, hotter GPU must be faster by more than its all-in power ratio to win at a power-limited site: here $49\,608/44\,208$ = **1.12**, not the chip ratio $1.4/1.2$ = **1.17**, because the rest of the rack does not grow with the GPU.

### Solution 27-07.5

(a) Each GPU sends $2 \times (7/8) \times 4$ = **7.00** GB.

(b) $7.00\ \text{GB}/450\ \text{GB/s}$ = **15.6** ms.

(c) $2 \times 7 \times 3\ \mu\text{s}$ = **42** µs, negligible at this size: in a small ring, bandwidth dominates.

### Solution 27-07.6

$B = 2 \times (1151/1152) \times 10\ \text{GB}/24.5\ \text{ms}$ = **815** GB/s = **6.52** Tb/s per GPU, more than eight 800 Gb/s ports for every GPU. That is far beyond any NIC budget, which is why the scale-up domain does the heavy lifting.

### Solution 27-07.7

(a) The counts sum to **419**, as the text states.

(b) $148/419$ = **35.3**%, not the printed 30.1%.

(c) The GPU categories sum to $148 + 72 + 19 + 17 + 6 + 6 = 268$, which is **64.0**% of 419.

(d) 30.1% of 419 is **126**. With 126 faulty-GPU interruptions, the GPU share is $(126 + 120)/419$ = **58.7**%, the text's figure, but then the counts would sum to 397, not 419.

The printed count, percentage and GPU share cannot all be right, and the percentages settle which is wrong. They sum to **94.9**%, **5.1** points short of 100%, which matches the **5.2**-point gap between 35.3% and the printed 30.1% to within rounding. So the faulty-GPU percentage is the misprint: the count 148 agrees with the 419 total, and the text's 58.7% GPU share was computed from the wrong percentage (the counts give 64.0%). The conclusion that GPUs and their memory dominate holds either way. Foot every table before quoting it.

### Solution 27-07.8

(a) $M = 16\,384 \times 11\,135\ \text{s}/100\,000$ = **1824** s = **30.4** min.

(b) $\tau^* = \sqrt{2 \times 10 \times 1824}$ = **191** s.

(c) The checkpoint term is $\sqrt{20/1824}$ = **10.5**% and the restart term $300/1824$ = **16.4**%, a total of **26.9**%, so the effective training time is **73.1**%. At this scale restarts dominate, and the remedies are spares and in-memory redundancy that shrink $R$, not a better $\tau$.

### Solution 27-07.9

(a) $e^{-3600/11\,135}$ = **0.724**.

(b) $e^{-3 \times 3600/11\,135}$ = **0.379**.

(c) $1 - e^{-86\,400/11\,135}$ = **99.96**%. A day without an interruption is very rare: such a job must be designed to fail and resume routinely.

### Solution 27-07.10

(a) $40\,625 \times 700\ \text{W} \times 720\ \text{h}$ = **20475** MWh.

(b) $20.475 \times 1.65$ = **33.8** GWh.

(c) **2.70** million dollars.

(a) exceeds 18.4 GWh because 10% of the elapsed time is lost to checkpoints, rework and restarts, and the GPUs draw power through it. Energy follows elapsed time, not useful compute.

### Solution 27-07.11

(a) A per-user speed of 50 tokens/s needs $t_{\text{step}} \le 20$ ms. Then $(0.5 \times 10^{12} + B \times 0.8 \times 10^9)/288 \times 10^{12} \le 0.02$, so $B \le (5.76 - 0.5) \times 10^{12}/0.8 \times 10^9$ = **6575**.

(b) Throughput $6575/0.02$ = **3.29 × 10⁵** tokens/s; energy $130\ \text{kW}/3.29 \times 10^5$ = **0.395** J per token.

(c) The KV cache uses $6575 \times 0.8$ GB = **5.26** TB, which fits in 13.4 TB with the weights.

(d) Compute: $2 \times 4 \times 10^{10} \times 6575/7.2 \times 10^{17}$ = **0.731** ms, far below 20 ms. The step is memory-bound.

### Solution 27-07.12

Annual cost is unchanged at $750\,000 + 109\,325 = 859\,325$ dollars.

At 60%: tokens $3.29 \times 10^5 \times 0.6 \times 3.1536 \times 10^7 = 6.22 \times 10^{12}$ a year, so **0.138** dollars per million tokens.

At 30%: **0.276** dollars per million tokens.

Relaxing the latency target from 409 to 50 tokens/s per user cut the cost per token by a factor of 3.1. Halving utilization doubles it. Electricity price matters far less (lab Part 4).

### Solution 27-07.13

The GPU power step is $16\,384 \times 600\ \text{W}$ = **9.83** MW, and $9.83/0.97$ = **10.1** MW at the rack inputs. Multiplying by the all-in factor 1.5 instead gives **14.7** MW, but that assumes the CPUs, NICs, switches and fans drop in proportion, which they largely do not, so it is an upper bound; cooling load also follows more slowly than the electrical step. That is a large fraction of the site's load switching within milliseconds to seconds, in step, repeatedly. It stresses upstream converters, generators and the grid connection, and calls for energy storage and ramp control at rack or site level (22-10, Example 22-10.8). Meta reports swings "on the order of tens of megawatts" [R-694].

### Solution 27-07.14

(a) $df/d\tau = -\delta/\tau^2 + 1/(2M)$. Setting it to zero gives $\tau^2 = 2\delta M$, so $\tau^* = \sqrt{2\delta M}$. There the save term is $\delta/\tau^* = \delta/\sqrt{2\delta M} = \sqrt{\delta/(2M)}$ and the rework term is $\tau^*/(2M) = \sqrt{2\delta M}/(2M) = \sqrt{\delta/(2M)}$: equal, with sum $2\sqrt{\delta/(2M)} = \sqrt{2\delta/M}$. The second derivative is $d^2f/d\tau^2 = 2\delta/\tau^3 > 0$ for every $\tau > 0$, so the stationary point is the minimum. The restart term $R/M$ does not depend on $\tau$ and drops out of the derivative.

(b) $M = 14\,400$ s. $\tau^* = \sqrt{2 \times 30 \times 14\,400}$ = **929.5** s = **15.5** min. Checkpoint loss $\sqrt{60/14\,400}$ = **6.45**%; restart loss $300/14\,400$ = **2.08**%; total **8.54**%.

(c) In the memory-bound region $1/s = (W + BK)/(\eta B_{\text{mem}})$, so $BK = \eta B_{\text{mem}}/s - W$ and $B = (\eta B_{\text{mem}}/s - W)/K$. Multiplying by $s$: $\Theta = Bs = \eta B_{\text{mem}}/K - (W/K)s$, a straight line in $s$. With $\eta B_{\text{mem}}$ = 288 TB/s, $W$ = 0.5 TB and $K$ = 0.8 GB: at $s \to 0$, $\Theta = 288 \times 10^{12}/0.8 \times 10^9$ = **3.60 × 10⁵** tokens/s (the KV-cache ceiling); $\Theta = 0$ at $s = \eta B_{\text{mem}}/W$ = **576** tokens/s (a batch of nearly zero, reading only the weights); slope $W/K$ = **625** tokens/s of throughput per token/s of per-user speed.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-07.2a | GB300 rack HBM | 20.1 | TB |
| 27-07.2b | GB300 HBM per GPU | 279 | GB |
| 27-07.2c | GB300 rack dense FP4 | 1080 | PFLOPS |
| 27-07.2d | GB300 dense FP4 per GPU | 15.0 | PFLOP/s |
| 27-07.3a | training compute | 6.3e24 | FLOP |
| 27-07.3b | compute time | 3.85e6 | s |
| 27-07.3c | compute time | 44.5 | days |
| 27-07.4a | GPU power | 100.8 | kW |
| 27-07.4b | busbar load | 131.6 | kW |
| 27-07.4c | input power | 135.7 | kW |
| 27-07.4d | GPU share | 74.3 | % |
| 27-07.4e | racks in 100 MW (fractional) | 614.2 | racks |
| 27-07.4f | racks in 100 MW | 614 | racks |
| 27-07.4g | GPUs in 100 MW | 44208 | GPUs |
| 27-07.4h | fewer GPUs than with 1.2 kW | 11 | % |
| 27-07.5a | bytes sent per GPU | 7.00 | GB |
| 27-07.5b | bandwidth time | 15.6 | ms |
| 27-07.5c | latency term | 42 | µs |
| 27-07.6a | network bandwidth to match | 815 | GB/s |
| 27-07.6b | network bandwidth to match | 6.52 | Tb/s |
| 27-07.6c | 800 Gb/s ports per GPU | 8 | ports |
| 27-07.7a | sum of counts | 419 | — |
| 27-07.7b | faulty-GPU share from count | 35.3 | % |
| 27-07.7c | GPU categories | 268 | — |
| 27-07.7d | GPU share from counts | 64.0 | % |
| 27-07.7e | count implied by 30.1% | 126 | — |
| 27-07.7f | GPU share with 126 | 58.7 | % |
| 27-07.7g | sum of counts with 126 | 397 | — |
| 27-07.7h | sum of printed percentages | 94.9 | % |
| 27-07.8a | mean time between interruptions | 1824 | s |
| 27-07.8b | mean time between interruptions | 30.4 | min |
| 27-07.8c | Young's interval | 191 | s |
| 27-07.8d | checkpoint term | 10.5 | % |
| 27-07.8e | restart term | 16.4 | % |
| 27-07.8f | total lost fraction | 26.9 | % |
| 27-07.8g | effective training time | 73.1 | % |
| 27-07.9a | no interruption in an hour | 0.724 | — |
| 27-07.9b | no interruption in three hours | 0.379 | — |
| 27-07.9c | at least one in a day | 99.96 | % |
| 27-07.10a | GPU energy | 20475 | MWh |
| 27-07.10b | facility energy | 33.8 | GWh |
| 27-07.10c | electricity cost | 2.70 | M$ |
| 27-07.11a | largest batch | 6575 | sequences |
| 27-07.11b | throughput | 3.29e5 | tokens/s |
| 27-07.11c | energy per token | 0.395 | J |
| 27-07.11d | KV-cache memory | 5.26 | TB |
| 27-07.11e | compute time per step | 0.731 | ms |
| 27-07.12a | annual cost | 859325 | $ |
| 27-07.12b | tokens per year at 60% | 6.22e12 | tokens |
| 27-07.12c | cost per million tokens at 60% | 0.138 | $ |
| 27-07.12d | cost per million tokens at 30% | 0.276 | $ |
| 27-07.12e | cost reduction from relaxed latency | 3.1 | — |
| 27-07.13a | GPU power step | 9.83 | MW |
| 27-07.13b | step at the rack inputs | 10.1 | MW |
| 27-07.13c | upper bound with the all-in factor | 14.7 | MW |
| 27-07.4i | all-in break-even speed-up | 1.12 | — |
| 27-07.4j | chip power ratio | 1.17 | — |
| 27-07.7i | shortfall of printed percentages | 5.1 | points |
| 27-07.7j | gap between computed and printed share | 5.2 | points |
| 27-07.14a | Young's interval | 929.5 | s |
| 27-07.14b | Young's interval | 15.5 | min |
| 27-07.14c | checkpoint loss | 6.45 | % |
| 27-07.14d | restart loss | 2.08 | % |
| 27-07.14e | total loss | 8.54 | % |
| 27-07.14f | throughput at zero speed | 3.60e5 | tokens/s |
| 27-07.14g | per-user speed at zero throughput | 576 | tokens/s |
| 27-07.14h | frontier slope | 625 | — |
