# Solutions 14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision

Problems: [14-14 problems](../problems/14-14-problems.md) · Chapter: [14-14](../chapters/14-14-ai-accelerators.md). Every number below is recomputed by [verify_14_14.py](../verify/verify_14_14.py).

- Cycle counts come from the cycle-accurate simulator, checked against $K + M + N - 2$ and against the Verilog array.
- Quantization is recomputed directly, and the specifications are those of R-208, R-220 and R-222.

---

## Solutions

### Solution 14-14.1

$256^2$ = **65,536** MACs per cycle; $65536 \times 2 \times 0.94 \times 10^9$ = **123.2** TFLOPS.

### Solution 14-14.2

$32 + 8 + 8 - 2$ = **46** cycles. Utilization is $8 \times 32 \times 8 / (64 \times 46)$ = **69.6**%.

### Solution 14-14.3

The product does $2n^3$ FLOP on $3n^2$ values of 2 bytes: $2n^3 / 6n^2$ = $n/3$ FLOP/byte.

- For $n = 512$ that is **170.7** FLOP/byte, below the 229 ridge, so it is memory-bound if each matrix crosses the HBM interface once.
- The product becomes compute-bound from $n/3 \ge 229.2$, that is $n \ge$ **688**.

(Larger on-chip buffers do not change the minimum traffic, only how close a kernel gets to it.)

### Solution 14-14.4

(a) There are $16 \times 16 = 256$ output tiles of $512 + 254 = 766$ cycles each: **196,096** cycles. The ideal is $2048 \times 512 \times 2048 / 128^2 = 131{,}072$, so the utilization is **66.8**%. The short K makes fill and drain a third of each tile.

(b) With perfect overlap, the time is $256 \times 512 + 254$ = **131,326** cycles, a utilization of **99.8**%. Hiding fill and drain matters most when K is small, as in this layer.

### Solution 14-14.5

The energy per MAC is $162.5/B$ pJ for the weight from DRAM plus $2.5/128 = 0.0195$ pJ for the activation from SRAM:

| $B$ | Energy per MAC |
|---|---|
| 1 | **162.52** pJ, 707 times the MAC |
| 16 | **10.18** pJ |
| 256 | **0.654** pJ, still 2.8 times the MAC |

Batching attacks the dominant term. Only reuse in the thousands brings DRAM traffic down to the MAC's own energy, which is why weights are kept on chip whenever the model allows.

### Solution 14-14.6

$\max|x| = 2.54$, so the scale is $2.54/127$ = **0.02**. The integers are 25, −60, 2, 127, −127 and 50; 0.031/0.02 = 1.55 rounds to 2. The largest error is that element's: $|0.031 - 0.04|$ = **0.009**, within half a step (0.01).

### Solution 14-14.7

(a) $6.02 \times 6 + 1.76$ = **37.88** dB.

(b) BF16: $7 \times 10^9 \times 2$ = **14** GB. INT8: **7** GB. INT4: **3.5** GB (plus a small overhead for the scales). Halving the bits halves the memory traffic of every token in a bandwidth-bound decoder.

### Solution 14-14.8

- **BF16:** each token reads 14 GB: $2765 / 14$ = **197.5** tokens/s.
- **INT8:** **395** tokens/s, twice as many, because the traffic halves.

The ridge point is $459 / 2.765$ = **166.0** FLOP/byte, so batch 1, at about 1 FLOP/byte, is far below it.

### Solution 14-14.9

(a) **1000** TFLOPS dense.

(b) By Amdahl's law, $1/(0.2 + 0.8/2)$ = **1.667**, not 2: the 20% of non-matrix work is untouched.

### Solution 14-14.10

$100 + 4 + 4 - 2$ = **106** cycles, a utilization of $100/106$ = **94.3**%. 90% needs $K/(K + 6) \ge 0.9$, that is $K \ge 54$: **54**.

### Solution 14-14.11

The pod sustains $9216 \times 2307 \times 10^{12} \times 0.4 = 8.50 \times 10^{18}$ FLOP/s, so $10^{25}$ FLOP takes $1.18 \times 10^6$ s = **13.6** days.

### Solution 14-14.12

| Chip | Ridge point (FLOP/byte) |
|---|---|
| TPU v5p | **166.0** |
| TPU v4 | 229.2 |
| H100 (dense BF16) | **295.4** |
| TPU7x | 312.6 |

For batch-1 decoding, which is bandwidth-bound, what matters is bandwidth itself, not the ridge point. TPU7x's **7380** GB/s gives the most tokens per second per chip. A low ridge point (v5p) means less compute sits idle at small batch, which matters for cost per token rather than for speed.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-14.1a | MACs per cycle | 65536 | — |
| 14-14.1b | peak | 123.2 | TFLOPS |
| 14-14.2a | cycles | 46 | — |
| 14-14.2b | utilization | 69.6 | % |
| 14-14.3a | intensity, n = 512 | 170.7 | FLOP/B |
| 14-14.3b | smallest compute-bound n | 688 | — |
| 14-14.4a | cycles, sequential tiles | 196096 | — |
| 14-14.4b | utilization, sequential | 66.8 | % |
| 14-14.4c | cycles, overlapped | 131326 | — |
| 14-14.4d | utilization, overlapped | 99.8 | % |
| 14-14.5a | energy per MAC, B = 1 | 162.52 | pJ |
| 14-14.5b | energy per MAC, B = 16 | 10.18 | pJ |
| 14-14.5c | energy per MAC, B = 256 | 0.654 | pJ |
| 14-14.6a | scale | 0.02 | — |
| 14-14.6b | largest error | 0.009 | — |
| 14-14.7a | SQNR, 6 bits | 37.88 | dB |
| 14-14.7b | weights, BF16 | 14 | GB |
| 14-14.7c | weights, INT8 | 7 | GB |
| 14-14.7d | weights, INT4 | 3.5 | GB |
| 14-14.8a | tokens/s, BF16 | 197.5 | — |
| 14-14.8b | tokens/s, INT8 | 395 | — |
| 14-14.8c | ridge point | 166.0 | FLOP/B |
| 14-14.9a | dense rate | 1000 | TFLOPS |
| 14-14.9b | overall speedup | 1.667 | — |
| 14-14.10a | cycles, K = 100 | 106 | — |
| 14-14.10b | utilization | 94.3 | % |
| 14-14.10c | K for 90% | 54 | — |
| 14-14.11a | training time | 13.6 | days |
| 14-14.12a | ridge, TPU v5p | 166.0 | FLOP/B |
| 14-14.12b | ridge, H100 | 295.4 | FLOP/B |
| 14-14.12c | bandwidth, TPU7x | 7380 | GB/s |
