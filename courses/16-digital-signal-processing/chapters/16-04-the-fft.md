<!-- status: verified -->
# 16-04 · The FFT Algorithm

| | |
|---|---|
| **Course** | [16 · Digital Signal Processing](../README.md) |
| **University equivalent** | The fast Fourier transform chapter of a senior DSP course: radix-2 decimation in time and in frequency, butterflies and signal-flow graphs, bit reversal and in-place computation, operation counts, radix-4 and real-input FFTs, and FFT hardware (Oppenheim & Schafer, *Discrete-Time Signal Processing*, ch. 9; Lyons, *Understanding Digital Signal Processing*, ch. 4) |
| **Prerequisites** | [16-03 The DFT and Its Properties](16-03-the-dft.md), [08-09 Arithmetic Circuits](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md), [14-04 Computer Arithmetic and Number Formats](../../14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the radix-2 decimation-in-time FFT from the DFT definition, draw its butterflies and signal-flow graph, and explain bit-reversed ordering and in-place computation.
2. Derive the decimation-in-frequency form and compare it with decimation in time.
3. Count the butterflies, complex multiplications and non-trivial twiddle multiplications of radix-2 and radix-4 FFTs, and the savings for real-valued inputs.
4. Compute small FFTs by hand and inverse FFTs with a forward FFT.
5. Size FFT hardware (memory-based and pipelined architectures) for a throughput target, in butterfly units, multipliers, memory and latency.
6. Predict word growth in a fixed-point FFT and choose a scaling strategy, including the overflow case that per-stage halving does not prevent.

---

## 1. Big picture

A direct $N$-point DFT costs $N^2$ complex multiply-adds: a million for $N = 1024$. The **fast Fourier transform** (FFT), published by Cooley and Tukey in 1965 [1] (with roots going back to Gauss), computes exactly the same numbers with about $(N/2)\log_2N$ multiplications: 5,120 for $N = 1024$, two hundred times fewer. That factor is the reason spectrum analysis, OFDM radios, radar, fast convolution and much of scientific computing are practical at all. The idea is a single trick applied recursively: split the DFT into two half-length DFTs and combine them with a cheap "butterfly". This chapter derives the trick, counts its cost exactly, and then turns to silicon, where the FFT is one of the most important datapaths a chip architect lays out.

- **Every OFDM modem** (Wi-Fi, LTE, 5G, DSL, cable) runs an inverse FFT to transmit and an FFT to receive, on every symbol.
- **Radar** chips compute range FFTs over each chirp and Doppler FFTs across chirps, millions of points per second per antenna.
- **Instruments** (spectrum analyzers, oscilloscopes, ADC testers) compute FFTs of captured records, some continuously in real time.
- **Fast convolution and correlation** (16-03 §3.7) rest on FFTs.

## 2. Intuition first

**Divide and conquer.** A DFT of eight samples asks for eight correlations of eight samples each. But the even-indexed samples $x[0], x[2], x[4], x[6]$ are themselves a signal sampled at half the rate, and so are the odd ones. Their two four-point DFTs together contain everything needed: the full spectrum is the even part's spectrum plus the odd part's spectrum, the latter rotated by a phase that accounts for its one-sample offset. Each four-point DFT splits again into two-point DFTs, which are just a sum and a difference. Three levels of halving turn **64** multiplications into **12** butterflies.

**Analogy: a tournament bracket.** Sixteen players can be ranked by playing every pair (120 matches), or by a bracket that halves the field each round (15 matches). The FFT is a bracket for correlations: each round combines results already computed instead of starting over. **Where the analogy breaks:** a bracket discards losers and loses information, while the FFT keeps every partial result. Each butterfly produces two outputs from two inputs, so nothing is lost and the transform stays exactly invertible.

```text
  x[0] ──●───────●──────────●──── X[0]       one butterfly (decimation in time):
  x[4] ──●─W0────●──────────●──── X[1]
  x[2] ──●───────●─W0───────●──── X[2]            a ──────●────── a + W·b
  x[6] ──●─W0────●─W2───────●──── X[3]                     ╲ ╱
  x[1] ──●───────●──────────●─W0─ X[4]                      ╳
  x[5] ──●─W0────●──────────●─W1─ X[5]                     ╱ ╲
  x[3] ──●───────●─W0───────●─W2─ X[6]            b ──W───●────── a − W·b
  x[7] ──●─W0────●─W2───────●─W3─ X[7]
        stage 1  stage 2   stage 3            (W = W_8^k labels the twiddle on the lower input)
```

*Figure 1. The 8-point radix-2 decimation-in-time FFT, schematically: bit-reversed inputs on the left, three stages of four butterflies, natural-order outputs on the right. Figure 2 in §3.3 draws the full signal-flow graph with every crossing.*

## 3. Theory

### 3.1 The cost of the direct DFT

$X[k] = \sum_{n=0}^{N-1}x[n]W_N^{kn}$ for $N$ values of $k$, each a sum of $N$ complex products: $N^2$ complex multiplications and $N(N - 1)$ complex additions. A complex multiplication is four real multiplications and two real additions (or three and five with a rearrangement). For $N = 1024$ that is about $10^6$ complex multiplications per transform.

### 3.2 Radix-2 decimation in time

Let $N$ be a power of 2. Split the sum into even and odd $n$, with $n = 2r$ and $n = 2r + 1$:

$$
X[k] = \sum_{r=0}^{N/2-1}x[2r]\,W_N^{2rk} + \sum_{r=0}^{N/2-1}x[2r + 1]\,W_N^{(2r+1)k} .
$$

Since $W_N^2 = e^{-j2\pi\cdot2/N} = W_{N/2}$, the first sum is the $(N/2)$-point DFT of the even samples, $G[k]$, and the second, after pulling out $W_N^k$, is $W_N^k$ times the $(N/2)$-point DFT of the odd samples, $H[k]$:

$$
X[k] = G[k] + W_N^k\,H[k], \qquad k = 0, 1, \dots, N - 1 .
$$

$G$ and $H$ have period $N/2$, and the **twiddle factor** $W_N^k$ satisfies $W_N^{k + N/2} = -W_N^k$. So for $k = 0, \dots, N/2 - 1$,

$$
X[k] = G[k] + W_N^kH[k], \qquad X[k + N/2] = G[k] - W_N^kH[k] .
$$

This pair is the **butterfly**: one complex multiplication ($W_N^kH[k]$), one addition and one subtraction produce two outputs. One level of splitting turns an $N$-point DFT into two $N/2$-point DFTs plus $N/2$ butterflies. Splitting recursively down to 2-point DFTs (which are butterflies with $W = 1$) takes $\log_2N$ levels, each with $N/2$ butterflies:

$$
\text{butterflies} = \frac N2\log_2N, \qquad \text{complex multiplications} \le \frac N2\log_2N, \qquad \text{complex additions} = N\log_2N .
$$

### 3.3 Bit reversal and in-place computation

Unrolling the recursion shows which input sample feeds each first-stage butterfly. The first split separates by the last bit of the index (even/odd), the next by the second-to-last bit, and so on. So the input order at the first stage is the natural order with each index's $\log_2N$ bits written backwards: **bit-reversed order**. For $N = 8$: $0 = 000 \to 000 = 0$, $1 = 001 \to 100 = 4$, $2 = 010 \to 010 = 2$, $3 = 011 \to 110 = 6$, and so on, giving $(0, 4, 2, 6, 1, 5, 3, 7)$. With the input permuted this way, every butterfly reads two memory locations and writes its two results back to the same two locations: the FFT runs **in place**, needing only $N$ complex words of memory plus the twiddle table, and the output emerges in natural order.

![Signal-flow graph of an 8-point radix-2 decimation-in-time FFT: eight inputs on the left in bit-reversed order x[0], x[4], x[2], x[6], x[1], x[5], x[3], x[7]; three columns of butterflies connecting pairs of lines one, two and four positions apart; twiddle labels W8^0 in stage 1, W8^0 and W8^2 in stage 2, and W8^0 to W8^3 in stage 3; outputs X[0] to X[7] on the right in natural order.](../../../assets/figures/16-04/flowgraph.svg)

*Figure 2. The 8-point decimation-in-time signal-flow graph. Butterfly spans are 1, 2 and 4 in the three stages; the twiddles (blue) $W_8^2 = -j$ and $W_8^0 = 1$ need no multiplier.*

### 3.4 Decimation in frequency

Instead of splitting the *input* into even and odd samples, split the *output* into even and odd bins, and the input into its first and second halves. For even bins $X[2k]$:

$$
X[2k] = \sum_{n=0}^{N/2-1}\bigl(x[n] + x[n + N/2]\bigr)W_{N/2}^{kn} ,
$$

because $W_N^{2k(n + N/2)} = W_N^{2kn}$. For odd bins,

$$
X[2k + 1] = \sum_{n=0}^{N/2-1}\bigl[(x[n] - x[n + N/2])\,W_N^n\bigr]W_{N/2}^{kn} ,
$$

because $W_N^{(2k+1)N/2} = -1$. So the decimation-in-frequency (DIF) butterfly forms the sum $a + b$ and the twiddled difference $(a - b)W_N^n$, then feeds them to two half-length DFTs. The operation count is the same as for decimation in time. The input is in natural order and the output in bit-reversed order: the mirror image of DIT. Hardware pipelines often pair a DIF forward transform with a DIT inverse, so that neither needs an explicit reordering step in between.

### 3.5 Counting multiplications exactly

Not every twiddle needs a multiplier: $W^0 = 1$ needs none, and $W_N^{N/4} = -j$ only swaps the real and imaginary parts and flips a sign. In decimation in time, stage $s$ ($s = 1, \dots, \log_2N$) combines $2^{s-1}$-point DFTs with the twiddles $W_{2^s}^j$, $j = 0, \dots, 2^{s-1} - 1$, each used $N/2^s$ times. Stage 1 uses only $W^0$; stage 2 uses $W^0$ and $-j$; for $s \ge 3$, two of the $2^{s-1}$ twiddles are trivial. The number of non-trivial complex multiplications is therefore

$$
\sum_{s=3}^{\log_2N}\left(2^{s-1} - 2\right)\frac N{2^s} = \frac N2(\log_2N - 2) - N\left(\frac12 - \frac2N\right) = \frac N2\log_2N - \frac{3N}2 + 2 \quad (N \ge 4) .
$$

For $N = 1024$: 3,586 of the 5,120 butterflies need a real complex multiplier. (Twiddles such as $W_8 = (1 - j)/\sqrt2$ can be done with two real multiplications instead of four; production code exploits such special cases further.)

### 3.6 Radix-4, split radix and real inputs

- **Radix-4.** Splitting into four interleaved subsequences gives a 4-point butterfly whose internal twiddles are $\pm1$ and $\pm j$ (free) and three external twiddle multiplications. There are $N/4$ butterflies per stage and $\log_4N = \frac12\log_2N$ stages, so at most $3\cdot\frac N4\cdot\frac12\log_2N = \frac{3N}8\log_2N$ complex multiplications: **75**% of radix-2. Hardware likes radix-4 (and radix-$2^2$, which keeps radix-2 butterflies but radix-4's twiddle pattern) for this saving.
- **Split radix** combines a radix-2 split of the even outputs with a radix-4 split of the odd ones and has the lowest known operation count among the classical algorithms (Oppenheim & Schafer §9.5) [2].
- **Real inputs.** A real sequence has a conjugate-symmetric DFT, so half the outputs are redundant. Two real sequences $a$ and $b$ can share one complex FFT: with $z = a + jb$, $A[k] = (Z[k] + Z^*[N - k])/2$ and $B[k] = (Z[k] - Z^*[N - k])/(2j)$. Alternatively, one $N$-point real FFT is computed as an $(N/2)$-point complex FFT of $x[2r] + jx[2r + 1]$ plus $N/2$ extra twiddle multiplications: about $\frac N4\log_2\frac N2 + \frac N2$ complex multiplications, **55**% of the complex FFT for $N = 1024$.
- **Inverse FFT.** $x[n] = \frac1N\left(\sum_kX^*[k]W_N^{kn}\right)^*$: conjugate the input, run the forward FFT, conjugate the output, divide by $N$. One FFT engine serves both directions.

### 3.7 FFT hardware

The butterfly maps directly onto silicon: one complex multiplier (four real multipliers and two adders) and two complex adders. Architectures differ in how many butterflies they instantiate and how data reaches them:

- **Memory-based (in-place).** One or a few butterfly units read operands from a RAM, compute and write back, stage by stage. An $N$-point transform needs $\frac N2\log_2N$ butterfly operations, so with $B$ butterfly units at clock $f_{clk}$ the transform takes $\frac{N\log_2N}{2Bf_{clk}}$. Small area; throughput limited by the butterflies and the RAM ports. Continuous streaming needs a second buffer (ping-pong) so one record can be captured while the previous one is transformed.
- **Pipelined (streaming).** One butterfly per stage, $\log_2N$ stages in a row, one sample in and one out per clock. In the classic **radix-2 single-path delay feedback** (R2SDF) pipeline, stage $s$ of a DIF transform holds $N/2^s$ samples in a delay line so that each input meets its partner from half a block earlier; the delays total $N/2 + N/4 + \dots + 1 = N - 1$ words. Each butterfly is busy half the time (it computes during one half of the block and passes data during the other). By §3.5's twiddle pattern, the last two stages need only trivial twiddles, so a general complex multiplier is needed between the other $\log_2N - 2$ stages. Throughput is one sample per clock at any $N$; latency is about one block.
- **Parallel (multi-path).** For sample rates above the clock rate (radar, optical links), several pipelines run side by side, or the whole flow graph is laid out in hardware, as in this chapter's lab: Figure 2 drawn literally, one butterfly per node.

The design choice trades area against throughput and latency, in the four currencies of 16-01 (Example 16-04.4).

### 3.8 Word growth and scaling in fixed point

Each radix-2 stage can double a magnitude: $\lvert a \pm Wb\rvert \le \lvert a\rvert + \lvert b\rvert$. Over $\log_2N$ stages the worst case is a factor of $N$, which is attained by a full-scale DC input ($X[0] = \sum x[n]$). An unscaled fixed-point FFT therefore needs $\log_2N$ extra integer bits; a 1024-point transform of 16-bit data needs 26-bit words to be safe. The common alternative is to **scale by 1/2 at every stage**, keeping 16-bit words and producing $X[k]/N$. That loses dynamic range for small signals (each scaling discards a bit, adding rounding noise; 16-10 quantifies it), and **it does not fully prevent overflow**: the real or imaginary *component* of $a + Wb$ can grow by $1 + \sqrt2 \approx 2.41$ in one stage. If $a$ is real and $b$ has equal real and imaginary parts, the twiddle can rotate all of $b$'s magnitude, $\sqrt2$ times its component size, onto the real axis (Example 16-04.5). Production FFTs therefore add a guard bit, saturate, or use **block floating point**: scale a stage by 1/2 only when the data actually grow, and keep a shared exponent.

## 4. Worked examples

### Example 16-04.1 · How much faster? (tier A)

**Setup.** Compare the complex multiplications of a direct DFT and a radix-2 FFT for $N$ = 256, 1024 and 4096, and give the non-trivial count for $N$ = 1024.

**Solution.**

| $N$ | Direct, $N^2$ | Radix-2, $\frac N2\log_2N$ | Ratio |
|---|---|---|---|
| 256 | 65,536 | 1,024 | **64** |
| 1024 | 1,048,576 | 5,120 | **204.8** |
| 4096 | 16,777,216 | 24,576 | **682.7** |

The ratio is $2N/\log_2N$: it grows almost linearly with $N$. For $N$ = 1024, $\frac N2\log_2N - \frac{3N}2 + 2$ = **3,586** of the multiplications are non-trivial (70%).

**Units check.** Counts of complex multiplications.

**Sanity check.** For $N = 2$ the FFT is one butterfly with $W = 1$: no multiplications, as the trivial-twiddle count says.

### Example 16-04.2 · A four-point FFT by hand (tier A)

**Setup.** Compute the DFT of $x = (1, 2, 3, 4)$ with the radix-2 decimation-in-time FFT and compare with Example 16-03.1.

**Solution.** Even samples $(1, 3)$: 2-point DFT $G = (1 + 3, 1 - 3) = (4, -2)$. Odd samples $(2, 4)$: $H = (6, -2)$. Twiddles $W_4^0 = 1$, $W_4^1 = -j$:

- $X[0] = G[0] + H[0]$ = **10**; $X[2] = G[0] - H[0]$ = **−2**.
- $X[1] = G[1] + (-j)H[1] = -2 + 2j$; $X[3] = G[1] - (-j)H[1] = -2 - 2j$.

These are Example 16-03.1's values, from 4 butterflies (two in each stage) and no non-trivial multiplication, instead of 16 complex products.

**Units check.** Same units as $x$.

**Sanity check.** $X[0]$ is the sum of the samples and $X[2]$ the alternating sum.

### Example 16-04.3 · Bit reversal and the twiddle pattern for N = 16 (tier B)

**Setup.** For $N = 16$: (a) give the bit-reversed input order; (b) list each stage's twiddles and count the non-trivial multiplications; (c) check the closed form of §3.5.

**Solution.** (a) Reversing 4 bits: $(0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15)$. Index 3 ($0011$) goes to 12 ($1100$); palindromes such as 6 ($0110$) stay put.

(b) Four stages of 8 butterflies:

- Stage 1 (size 2): $W^0$ only: 0 non-trivial.
- Stage 2 (size 4): $W_4^0 = 1$, $W_4^1 = -j$: 0.
- Stage 3 (size 8): $W_8^0, \dots, W_8^3$, each used twice; $W_8^1$ and $W_8^3$ are non-trivial: **4**.
- Stage 4 (size 16): $W_{16}^0, \dots, W_{16}^7$, each used once; all but $W^0$ and $W_{16}^4 = -j$ are non-trivial: **6**.

Total **10** non-trivial multiplications out of 32 butterflies.

(c) $\frac{16}2 \times 4 - \frac{3 \times 16}2 + 2 = 32 - 24 + 2$ = 10.

**Units check.** Counts.

**Sanity check.** The lab's instrumented FFT counts the same 32 butterflies and 10 non-trivial multiplications.

### Example 16-04.4 · Sizing an FFT engine for a 100 MS/s stream (tier C)

**Setup.** A radar receiver must transform a continuous 100 MS/s complex stream in 1024-point blocks. Compare (a) a memory-based engine with radix-2 butterfly units, each completing one butterfly per clock at 500 MHz, and (b) an R2SDF pipeline at 100 MHz. Give the butterfly units, complex multipliers, data memory and latency.

**Solution.** A new block arrives every $1024/(100 \times 10^6)$ = **10.24** µs, and each block needs $\frac{1024}2 \times 10$ = 5,120 butterflies.

(a) Memory-based: 5,120 butterflies in 10.24 µs require **500** million butterflies per second: exactly one unit at 500 MHz, with no margin for pipeline bubbles or memory conflicts. A real design uses **2** units (or a radix-4 unit). Memory: the in-place buffer plus a second buffer to capture the next block, $2 \times 1024$ = **2048** complex words. Latency: one block to fill the buffer plus the transform time, about two blocks.

(b) R2SDF at 100 MHz, one sample per clock: **10** butterfly units (one per stage, each 50% busy), $\log_2N - 2$ = **8** general complex multipliers, and **1023** words of delay memory. Latency is about one block (1023 samples) plus pipeline registers, roughly half that of (a).

The pipeline uses more butterflies but runs **5** times slower, needs no address generation, and has half the memory and latency; the memory-based engine is smaller when the throughput demand is lower. That is the usual choice: pipelines for continuous streams, memory-based engines for bursts.

**Units check.** Butterflies per second against clock rate; memory in complex words.

**Sanity check.** At one sample per clock, the pipeline must finish a 1024-point block every 1024 clocks, and its delay lines hold 512 + 256 + ... + 1 = 1023 samples: one block in flight.

### Example 16-04.5 · When halving every stage is not enough (tier C)

**Setup.** In the lab's 8-point Q1.15 FFT, a stage-3 butterfly with twiddle $W_8^1 = (23170 - j23170)/2^{15}$ receives $a = 32767 + j0$ and $b = 32767 + j32767$ (full-scale codes). Compute $Wb$, the scaled outputs $(a \pm Wb)/2$, and explain the result.

**Solution.** $W_8^1b = \frac{(23170 - j23170)(32767 + j32767)}{2^{15}}$. The product's real part is $23170 \times 32767 \times 2$ = **1,518,422,780**, and its imaginary part is 0. After rounding by $2^{15}$, $Wb$ = **46339** + $j0$: the twiddle has rotated $b$, whose magnitude is $\sqrt2 \times 32767$, onto the real axis. Then $(a + Wb)/2 = (32767 + 46339)/2$ = **39553**, which exceeds the 16-bit maximum of 32,767: it overflows, and the hardware saturates it to 32,767. The other output is $(a - Wb)/2$ = **−6786**, in range. The component grew by $1 + \sqrt2$ = **2.414**, more than the factor 2 that the halving removes. In this example, as in most real signals, such inputs are rare, but a saturating or block-floating-point FFT must be designed for them, and the lab's test vectors include one.

**Units check.** Integer codes; $W$ in Q1.15.

**Sanity check.** $\lvert b\rvert = 32767\sqrt2$ = **46340**, and a twiddle has unit magnitude, so $\lvert Wb\rvert$ must be about 46,340, as found (46,339 after rounding).

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 16-04.1a | ratio, N = 256 | 64 | — |
| Ex 16-04.1b | ratio, N = 1024 | 204.8 | — |
| Ex 16-04.1c | ratio, N = 4096 | 682.7 | — |
| Ex 16-04.1d | non-trivial multiplications, N = 1024 | 3586 | — |
| Ex 16-04.1e | direct multiplications, N = 1024 | 1048576 | — |
| Ex 16-04.1f | FFT multiplications, N = 1024 | 5120 | — |
| Ex 16-04.2a | X[0] | 10 | — |
| Ex 16-04.2b | X[2] | −2 | — |
| Ex 16-04.3a | non-trivial in stage 3 | 4 | — |
| Ex 16-04.3b | non-trivial in stage 4 | 6 | — |
| Ex 16-04.3c | non-trivial total | 10 | — |
| Ex 16-04.4a | block period | 10.24 | µs |
| Ex 16-04.4b | butterfly rate required | 500 | M/s |
| Ex 16-04.4c | butterfly units, memory-based | 2 | — |
| Ex 16-04.4d | ping-pong memory | 2048 | words |
| Ex 16-04.4e | pipeline butterfly units | 10 | — |
| Ex 16-04.4f | pipeline general multipliers | 8 | — |
| Ex 16-04.4g | pipeline delay memory | 1023 | words |
| Ex 16-04.5a | Wb | 46339 | — |
| Ex 16-04.5b | (a + Wb)/2 before saturation | 39553 | — |
| Ex 16-04.5c | (a − Wb)/2 | −6786 | — |
| Ex 16-04.5d | worst-case component growth | 2.414 | — |
| Ex 16-04.5e | real part of the twiddle product before rounding | 1518422780 | — |
| Ex 16-04.5f | magnitude of b | 46340 | — |
| Ex 16-04.4h | clock ratio, memory-based to pipeline | 5 | — |
| Ex 16-04.1g | direct multiplications, N = 256 | 65536 | — |
| Ex 16-04.1h | FFT multiplications, N = 256 | 1024 | — |
| Ex 16-04.1i | direct multiplications, N = 4096 | 16777216 | — |
| Ex 16-04.1j | FFT multiplications, N = 4096 | 24576 | — |
| Txt 16-04.a | direct 8-point multiplications | 64 | — |
| Txt 16-04.b | 8-point butterflies | 12 | — |
| Txt 16-04.c | real-input FFT cost relative to complex, N = 1024 | 55 | % |
| Txt 16-04.d | radix-4 relative to radix-2 | 75 | % |
| Txt 16-04.e | Q2 stages | 5 | — |
| Txt 16-04.f | Q2 butterflies | 80 | — |
| Txt 16-04.g | Q2 bit-reversed position of 3 | 24 | — |
| Txt 16-04.h | Q6 word length | 24 | bits |

## 5. Simulate it

The lab, [labs/16-04-lab](../labs/16-04-lab/README.md), provides `fft.py` (recursive and in-place iterative radix-2 FFTs with operation counters, decimation in frequency, the inverse via conjugation, two real FFTs for the price of one, and a bit-exact model of a fixed-point 8-point FFT) and a Verilog 8-point FFT (`fft8.v`, built from `bfly.v`) with a self-checking testbench. You:

1. **Check the algorithms** against `numpy.fft` for $N$ up to 4096, and count butterflies and non-trivial multiplications.
2. **Time direct DFT against FFT** in Python for growing $N$ and fit the $N^2$ and $N\log N$ trends.
3. **Exploit real inputs**: two real FFTs with one complex FFT, and the inverse with a forward FFT.
4. **Run the hardware FFT**: simulate `fft8_tb.v`, which compares all 16 output words of 65 test vectors with the Python model bit for bit, and inspect the saturation case of Example 16-04.5.
5. **Measure fixed-point error**: compare the Q1.15 FFT's outputs with the exact DFT/8 for random inputs and see the error stay within a few LSBs.

**Guided exercise (predict, then run).** **Before Part 2,** predict the speed-up of the FFT over the direct DFT at $N$ = 1024 in Python. (Far below 205: interpreted loops add overhead per butterfly, while the direct DFT runs as one matrix product in compiled code. Asymptotically the FFT still wins; with `numpy.fft`, which is compiled, it wins by orders of magnitude.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| FFT length $N$ | Finer bins; amortized cost per point ($\log_2N$ per sample) | Latency, memory, word growth ($\log_2N$ bits) | System or algorithm architect |
| Radix (2, 4, $2^2$, split) | Fewer multiplications (radix-4: 75% of radix-2) | More complex butterflies and control | DSP hardware designer |
| Memory-based versus pipelined | Memory-based: small area at low throughput; pipeline: one sample per clock, simple control | Memory-based: RAM bandwidth, address logic; pipeline: $\log_2N$ butterflies, idle half the time | SoC architect |
| Word length and scaling | Wider words or block floating point: dynamic range and no overflow | Area and power grow with word length | Hardware designer |
| Twiddle precision | Lower spurs and error | Wider multipliers, larger ROM | Hardware designer |
| Real-input FFT tricks | About half the computation for real data | Extra pre- and post-processing logic | Firmware or hardware designer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Direct DFT | $N^2$ complex multiplications | §3.1 |
| Radix-2 FFT | $\frac N2\log_2N$ butterflies and multiplications; $N\log_2N$ complex additions | §3.2 |
| Non-trivial twiddles, radix-2 | $\frac N2\log_2N - \frac{3N}2 + 2$ (3,586 for $N$ = 1024) | §3.5 |
| Radix-4 | $\frac{3N}8\log_2N$ complex multiplications (75% of radix-2) | §3.6 |
| R2SDF pipeline | $\log_2N$ butterflies, $\log_2N - 2$ general multipliers, $N - 1$ delay words, one sample per clock | §3.7 |
| Word growth | up to $\log_2N$ bits; up to $1 + \sqrt2$ per stage in a component | §3.8 |
| Origin | Cooley and Tukey, 1965 [1] | Established |

## 8. Common mistakes

- **Forgetting the bit reversal** (or applying it twice) between a DIT input and a DIF output.
- **Counting all $\frac N2\log_2N$ multiplications as real hardware multipliers.** Trivial twiddles need none; special ones need fewer.
- **Assuming per-stage 1/2 scaling makes overflow impossible.** Components can grow by 2.41 in a stage.
- **Ignoring the latency of block transforms** in a closed loop or a low-latency link.
- **Using an $N$ that is not a power of 2 with a radix-2 routine.** Pad, or use a mixed-radix or prime-factor algorithm.
- **Forgetting the $1/N$ on the inverse** when reusing a forward FFT.
- **Comparing Python loop timings with compiled library timings** and drawing conclusions about algorithms.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **FFTs are hardened blocks.** FPGA vendors ship parameterized FFT IP (radix-2 and radix-4, burst and pipelined streaming architectures, block floating point), and modem and radar SoCs embed dedicated FFT accelerators beside their DSP cores **[Established; vendor documentation and textbooks]**.
- **The OFDM numerology sets the FFT.** Wi-Fi 802.11a/g transforms 64 points every 4 µs; LTE uses a 2048-point FFT at 30.72 MHz for a 20 MHz carrier, and 5G NR scales that numerology by powers of two (R-236) **[Established]**. A 5G NR baseband for wide carriers and many antennas therefore runs many FFTs of a few thousand points continuously, one reason baseband power scales with bandwidth and antenna count.
- **Software FFTs are tuned per processor.** Libraries such as FFTW choose among algorithm variants at run time for the cache and vector units of the target machine; on DSP cores, vendor libraries hand-schedule radix-4 butterflies onto SIMD MACs **[Established]**.

### Why it matters commercially

The FFT is the most widely licensed and most re-implemented DSP kernel, so FFT efficiency (points per second per watt, per mm²) is a direct competitive metric for modem, radar and instrument chips. An architecture that hits the throughput with fewer multipliers or less memory, or that avoids overflow without wasting bits, saves area on every chip shipped. When diligence covers a baseband or radar-processing company, the FFT engine's architecture (streaming versus memory-based, radix, word length, scaling) is a concrete place to test whether the claimed efficiency is real.

### Marketing vs Reality

- **"Our FFT is N times faster."** Faster than what? A direct DFT is a straw man; compare with a well-tuned FFT library or another FFT accelerator on the same $N$, word length and precision.
- **"Floating-point accuracy at fixed-point cost."** Block floating point recovers much of the dynamic range, but not all; ask for SQNR versus input level across the expected range.
- **"Supports any FFT size."** Often only powers of 2 natively; other sizes may be padded (changing the bin frequencies) or run at lower throughput.
- **"Zero overflow by design."** Per-stage halving still allows component growth of 2.41; ask how saturation or guard bits are handled.

### Questions for engineering leaders

1. **"What are the FFT engine's throughput, latency and area, and how do they scale with $N$?"** *Strong:* gives points per clock, latency in samples, and memory per point. *Evasive:* "it's real-time".
2. **"Streaming pipeline or memory-based, and why?"** *Strong:* ties the choice to burst versus continuous data and to latency. *Evasive:* no reason given.
3. **"How do you scale, and what is the SQNR for small and large signals?"** *Strong:* describes block floating point or a scaling schedule, with measured SQNR curves. *Evasive:* only the full-scale number.
4. **"How many non-trivial multipliers does your radix choice need?"** *Strong:* knows the count and the trade against butterfly complexity. *Evasive:* treats every twiddle as a multiplier, or none.
5. **"Which sizes are native, and what happens to the others?"** *Strong:* lists native sizes and the mixed-radix or padding strategy. *Evasive:* "any size".

## 10. Concept check

**Q1.** Why does $W_N^{k + N/2} = -W_N^k$ make the butterfly possible?

<details><summary>Answer</summary>

It lets the outputs $X[k]$ and $X[k + N/2]$ share one product $W_N^kH[k]$: one is $G + WH$ and the other $G - WH$. Without it, the second half of the outputs would need its own multiplications.

</details>

**Q2.** In a 32-point radix-2 FFT, how many stages and butterflies are there, and where does input sample 3 appear in bit-reversed order?

<details><summary>Answer</summary>

$\log_232$ = 5 stages of 16 butterflies, 80 in total. Index 3 = 00011 reverses to 11000 = 24.

</details>

**Q3.** Name the main difference between decimation in time and decimation in frequency.

<details><summary>Answer</summary>

DIT splits the input into even and odd samples (bit-reversed input, natural output; twiddle before the add/subtract). DIF splits the output into even and odd bins (natural input, bit-reversed output; twiddle after the subtraction). The operation counts are the same.

</details>

**Q4.** How can a forward FFT compute an inverse FFT?

<details><summary>Answer</summary>

Conjugate the spectrum, apply the forward FFT, conjugate the result and divide by $N$.

</details>

**Q5.** Why does a pipelined R2SDF FFT need $N - 1$ words of memory?

<details><summary>Answer</summary>

Each stage must hold half of its current block so that every sample can meet its butterfly partner: $N/2 + N/4 + \dots + 1 = N - 1$ samples in total.

</details>

**Q6.** A 4096-point FFT of 12-bit real samples is computed without scaling. How many bits must the words have to rule out overflow?

<details><summary>Answer</summary>

$12 + \log_24096 = 12 + 12$ = 24 bits: the magnitude can grow by at most $N = 2^{12}$, attained by a full-scale DC input at bin 0, and each component is bounded by the magnitude.

</details>

Practice: [Problems 16-04](../problems/16-04-problems.md) · [Solutions](../solutions/16-04-solutions.md)

## 11. Key terms

[Fast Fourier transform (FFT)](../../../reference/glossary.md#fast-fourier-transform-fft) · [Butterfly](../../../reference/glossary.md#butterfly) · [Twiddle factor](../../../reference/glossary.md#twiddle-factor) · [Decimation in time](../../../reference/glossary.md#decimation-in-time) · [Decimation in frequency](../../../reference/glossary.md#decimation-in-frequency) · [Bit-reversed order](../../../reference/glossary.md#bit-reversed-order) · [In-place computation](../../../reference/glossary.md#in-place-computation) · [Radix-4 FFT](../../../reference/glossary.md#radix-4-fft) · [Pipelined FFT](../../../reference/glossary.md#pipelined-fft) · [Block floating point](../../../reference/glossary.md#block-floating-point)

## 12. Connections

- **Builds on:** [16-03 The DFT](16-03-the-dft.md), [08-09 Arithmetic Circuits](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) (adders and multipliers), [14-04 Computer Arithmetic](../../14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md) (fixed point, saturation).
- **Next:** [16-05 Spectral Analysis and Windowing](16-05-spectral-analysis-and-windowing.md) puts the FFT to work on real measurements.
- **Used later:** fast convolution and filter banks in [16-09](16-09-multirate-dsp.md); fixed-point FFT noise in [16-10](16-10-quantization-and-fixed-point.md); FFT accelerators in [16-11](16-11-dsp-hardware-architectures.md); OFDM in Course 17.

## 13. Further study

- Oppenheim & Schafer, *Discrete-Time Signal Processing*, 3rd ed., ch. 9 (FFT algorithms: decimation in time and frequency, in-place computation, general N).
- Lyons, *Understanding Digital Signal Processing*, 3rd ed., ch. 4 (the FFT, butterflies, bit reversal).
- J. W. Cooley and J. W. Tukey [1], the paper that started it, three pages long.
- MIT OCW 6.341 *Discrete-Time Signal Processing* (Fall 2005), FFT lectures.

## 14. Sources

1. J. W. Cooley and J. W. Tukey, "An Algorithm for the Machine Calculation of Complex Fourier Series", *Mathematics of Computation* 19(90), 297–301, 1965.
2. A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Pearson, 2010, ch. 9.
3. R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed., Prentice Hall, 2011, ch. 4.
4. OFDM numerology (802.11a/g, LTE, NR). Research log [R-236].
