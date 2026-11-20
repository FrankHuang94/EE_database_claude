# Course 14 · Final Exam Solutions (Computer Organization and Architecture)

Exam: [README.md](README.md). Every number below is recomputed by [verify_14_exam.py](../verify/verify_14_exam.py).

- Encodings are cross-checked with the LLVM assembler when it is installed, and floating-point encodings with Python's `struct`.
- Cache, coherence, virtual-memory, SIMT and systolic results come from the labs' simulators.
- The rest is from the formulas.

---

## Solutions

### Solution 1

(a) $T = 2 \times 10^9 \times 1.5 / (2.5 \times 10^9)$ = **1.2** s.

(b) $T = 2 \times 10^9 \times 1.1 / (2.0 \times 10^9) = 1.1$ s, a speedup of $1.2/1.1$ = **1.091**. The lower CPI more than pays for the lower clock.

(c) $1/(0.2 + 0.8/8)$ = **3.333** on 8 cores; the limit is $1/0.2$ = **5**.

(d) $P \propto V^2 f$, so $0.9^2 \times 0.9 = 0.729$: a saving of **27.1**%.

### Solution 2

(a) I-type: imm[11:0] = −3 = 0xFFD, rs1 = 6, funct3 = 0, rd = 5, opcode = 0x13. The word is 0xFFD << 20 | 6 << 15 | 5 << 7 | 0x13 = **0xFFD30293**.

(b) The fields of 0x00A28233 are opcode 0x33 (R-type), rd = 4, funct3 = 0, rs1 = 5, rs2 = 10 and funct7 = 0: **add x4, x5, x10**.

(c) The branch immediate is a 13-bit signed byte offset with bit 0 always 0, so the largest forward offset is $2^{12} - 2$ = **4094** bytes (about ±4 KiB).

(d) **2** instructions: `lui x?, 0x12345` sets the upper 20 bits, then `addi x?, x?, 0x678` adds the lower 12. Because 0x678 < 0x800, its sign extension adds nothing and needs no correction.

### Solution 3

(a) $5 \times 100 + 4$ = **504** instructions.

(b) Four saved registers (16 bytes) plus 8 bytes of locals make 24 bytes. The ILP32 ABI keeps sp 16-byte aligned, so the frame is rounded up to **32** bytes.

(c) Only **s1**. The s registers are callee-saved; t0 and a0 are caller-saved, and ra is overwritten by the callee's own calls, so a caller that needs it saves it itself.

(d) A leaf makes no calls, so it need not save ra. If it uses only t and a registers, it touches no callee-saved state and needs no frame at all.

### Solution 4

(a) 150 does not fit in −128…127. The bit pattern 150 = 0x96 reads as 150 − 256 = **−106**: overflow, since two positive operands produced a negative result.

(b) −6.25 = −1.5625 × 2², so the sign is 1, the biased exponent 2 + 127 = 129 = 0x81, and the fraction 0.5625 = 0.1001₂. The encoding is **0xC0C80000**. bfloat16 keeps the top 16 bits: **0xC0C8**, exact, because the fraction needs only 4 bits.

(c) The spacing is $2^{-23}$ = **1.19 × 10⁻⁷**. 1 + 2⁻²⁴ lies exactly halfway between 1 and 1 + 2⁻²³, and round-to-nearest-even gives **1.0**.

(d) The scale is $3.81/127$ = **0.03**. 1.0/0.03 = 33.3 rounds to **33**, which dequantizes to **0.99**.

### Solution 5

(a) Load: $200 + 100 + 150 + 200 + 25 + 50$ = **725** ps. R-type skips the data memory: **525** ps. The clock must fit the load: $1/725$ ps = **1.379** GHz.

(b) $1/230$ ps = **4.348** GHz, a speedup of $725/230$ = **3.152**. That is not 5, because the stages are unbalanced (the slowest sets the clock) and the pipeline registers add overhead.

### Solution 6

(a) $1000 + 4 + 150 + 2 \times 100$ = **1354** cycles, a CPI of **1.354**.

(b) A load's data exists only at the end of MEM, but the dependent instruction needs it at the start of EX in the very next cycle. Forwarding cannot send data back in time, so one bubble remains unless the compiler schedules an independent instruction between them.

### Solution 7

(a) The counter goes 1 → 2 → 3 → 2 → 3 → 2 → 1 → 2 → 3. It predicts taken when ≥ 2: predictions N, T, T, T, T, T, N, T against outcomes T, T, N, T, N, N, T, T. That is **5** mispredictions, at the first, third, fifth, sixth and seventh outcomes.

(b) CPI = $1 + 0.2 \times 0.1 \times 15$ = **1.3**.

### Solution 8

(a) The dependences are:

- **RAW:** I2 ← I1 (t0), I4 ← I2 (t1), I4 ← I3 (t0);
- **WAR:** I3 writes t0, which I2 reads;
- **WAW:** I3 and I1 both write t0.

The critical path is I1 → I2 → I4: $3 + 1 + 3$ = **7** cycles. I3 can run in parallel once renaming removes the name dependences.

(b) $6 \times 200$ = **1200** entries. A 512-entry window fills during the miss and sustains at most $512/200$ = **2.56** instructions per cycle.

### Solution 9

(a) $16384/(64 \times 4)$ = **64** sets: a 6-bit offset, a 6-bit index and a 20-bit tag. For 0xABCD1234:

- offset 0x34 = **52**;
- index (0x1234 >> 6) & 0x3F = **8**;
- tag **0xABCD1**.

(b) $\text{AMAT} = 1 + 0.03\,(10 + 0.25 \times 120)$ = **2.2** cycles.

(c) The block numbers are 0, 4, 1, 0, 5, 4. Direct-mapped (set = block mod 4): 0 and 4 collide in set 0, and 1 and 5 in set 1, so every access misses: **6**. Fully associative LRU: 0, 4, 1 miss, 0 hits, 5 misses, 4 hits: **4** misses, all compulsory. The other 2 are conflict misses.

### Solution 10

(a) VPN[1] = 0xC0FFEE00 >> 22 = 0x303 = **771**; VPN[0] = (>> 12) & 0x3FF = 0x3FE = **1022**; the offset is 0xE00 = **3584**.

(b) $128 \times 4$ KiB = **512** KiB with base pages, and $128 \times 4$ MiB = **512** MiB with megapages.

(c) A load page fault is cause **13** and an `ecall` from user mode cause **8**. After the page fault the handler returns to the same instruction, which re-executes once the page is mapped; after the `ecall` it returns to mepc + 4.

### Solution 11

(a) The transactions are:

1. P0 BusRd (E).
2. P1 BusRd (both S).
3. P0 BusUpgr, invalidating P1.
4. P2 BusRd: P0 writes back, and P0 and P2 hold S.
5. P1 BusRdX, invalidating P0 and P2.

That is **5** transactions and **3** invalidations.

(b) SC allows **3** outcomes and TSO **4**: TSO adds r1 = r2 = 0.

(c) $32 \times 16 \times (128/130) / 8$ = **63.02** GB/s per direction.

### Solution 12

(a) Both paths run: $24 + 8$ = **32** slots. The useful lane-slots are $4 \times 24 + 28 \times 8 = 320$ of $32 \times 32 = 1024$, an efficiency of **31.25**%.

(b) The elements are 16 bytes apart, so the warp spans 512 bytes: **16** sectors, of which only 128 bytes are used, **25**%.

(c) Each block needs $96 \times 256 = 24{,}576$ registers, so $\lfloor 65536 / 24576 \rfloor = 2$ blocks fit: **16** warps, **25**% occupancy.

### Solution 13

(a) Every access pays the L1 hit time $t_1$. A fraction $m_1$ (L1's miss rate) also pays L2's hit time $t_2$. Of those, the fraction $m_{2,\text{local}}$ that also misses in L2 pays the memory time:

$$
\text{AMAT} = t_1 + m_1\bigl(t_2 + m_{2,\text{local}}\,t_\text{mem}\bigr).
$$

The local rate is L2's misses over L2's accesses; the global rate, $m_1 m_{2,\text{local}}$, is L2's misses over all accesses. With Question 9's numbers, the global rate is $0.03 \times 0.25$ = **0.75**%, and AMAT = $1 + 0.03 \times 10 + 0.0075 \times 120$ = **2.2** cycles, the same as before.

(b) Row $i$ of $A$ enters $i$ cycles late and moves one PE per cycle, so $a_{ik}$ reaches column $j$ at cycle $k + i + j$. Column $j$ of $B$ enters $j$ cycles late and moves down, so $b_{kj}$ reaches row $i$ at cycle $k + j + i$: the same cycle. The last pair ($i = M-1$, $j = N-1$, $k = K-1$) meets at cycle $K + M + N - 3$, so counting from cycle 0 the product takes $K + M + N - 2$ cycles. For M = N = 8 and K = 64 that is **78** cycles, a utilization of $8 \cdot 64 \cdot 8/(64 \times 78)$ = **82.1**%.

(c) A warp issues for $k$ cycles, then waits $L$, so it is ready for a fraction $k/(k + L)$ of the time. A scheduler issuing every cycle needs $N k \ge k + L$, so $N \ge 1 + L/k$. This is Little's law: in-flight work equals the issue rate times the time each item spends in the system. For $L$ = 600 and $k$ = 15, $N$ = **41** warps.

### Solution 14

(a) Removing the sparsity and going from FP4 to FP8 to BF16 divides by $2^3$: **500** TFLOPS dense BF16-equivalent, which is **0.505** times H100's 989.5. The "10×" compares a sparse FP4 figure with something else, perhaps H100's FP32.

(b) $500 \times 10^{12} / 2 \times 10^{12}$ = **250** FLOP/byte.

(c) Each token reads every weight once:

- BF16 (140 GB): $2 \times 10^{12}/1.4 \times 10^{11}$ = **14.3** tokens/s;
- FP4 (35 GB): **57.1** tokens/s.

500 tokens/s per chip therefore implies batching at least $500/57.1$ = **8.75**, so 9 sequences decoding concurrently. The figure is an aggregate throughput, not the speed one user sees, and it assumes the model is accurate at FP4.

(d) Rubric. Award 1 point per question with a strong answer, up to 4.

1. **"What is your dense throughput at BF16 or FP8 on our models?"** *Strong:* measured numbers at stated precision and utilization. *Evasive:* the sparse FP4 peak.
2. **"What accuracy do you lose at FP4 with 2:4 sparsity?"** *Strong:* benchmark accuracy against BF16, with the calibration method. *Evasive:* "negligible".
3. **"At what batch size and latency is 500 tokens/s measured?"** *Strong:* batch, time to first token and per-token latency at a percentile. *Evasive:* throughput alone.
4. **"What do the HBM, the package and the software stack cost, and what is the delivered performance per watt and per dollar?"** *Strong:* a bill of materials and measured power. *Evasive:* TOPS per watt at peak.

Other good questions: MLPerf Closed results; compiler maturity on new models; supply of HBM; roofline placement of the customer's workloads.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X14.1a | run time | 1.2 | s |
| X14.1b | speedup | 1.091 | — |
| X14.1c | Amdahl speedup, 8 cores | 3.333 | — |
| X14.1d | Amdahl limit | 5 | — |
| X14.1e | dynamic power saving | 27.1 | % |
| X14.2a | encoding of addi x5, x6, -3 | 0xFFD30293 | — |
| X14.2b | rd of the decoded word | 4 | — |
| X14.2c | rs1 | 5 | — |
| X14.2d | rs2 | 10 | — |
| X14.2e | largest forward branch offset | 4094 | B |
| X14.2f | instructions to load the constant | 2 | — |
| X14.3a | instructions executed | 504 | — |
| X14.3b | stack frame | 32 | B |
| X14.4a | 8-bit result | -106 | — |
| X14.4b | FP32 encoding | 0xC0C80000 | — |
| X14.4c | bfloat16 encoding | 0xC0C8 | — |
| X14.4d | spacing above 1.0 | 1.19e-7 | — |
| X14.4e | 1 + 2⁻²⁴ in FP32 | 1.0 | — |
| X14.4f | INT8 scale | 0.03 | — |
| X14.4g | integer for 1.0 | 33 | — |
| X14.4h | dequantized value | 0.99 | — |
| X14.5a | load path | 725 | ps |
| X14.5b | R-type path | 525 | ps |
| X14.5c | single-cycle clock | 1.379 | GHz |
| X14.5d | pipelined clock | 4.348 | GHz |
| X14.5e | pipeline speedup | 3.152 | — |
| X14.6a | cycles | 1354 | — |
| X14.6b | CPI | 1.354 | — |
| X14.7a | mispredictions | 5 | — |
| X14.7b | CPI | 1.3 | — |
| X14.8a | critical path | 7 | cycles |
| X14.8b | window entries | 1200 | — |
| X14.8c | IPC with 512 entries | 2.56 | — |
| X14.9a | sets | 64 | — |
| X14.9b | offset of 0xABCD1234 | 52 | — |
| X14.9c | index | 8 | — |
| X14.9d | tag | 0xABCD1 | — |
| X14.9e | AMAT | 2.2 | cycles |
| X14.9f | misses, direct-mapped | 6 | — |
| X14.9g | misses, fully associative | 4 | — |
| X14.10a | VPN[1] | 771 | — |
| X14.10b | VPN[0] | 1022 | — |
| X14.10c | offset | 3584 | — |
| X14.10d | reach, 4 KiB pages | 512 | KiB |
| X14.10e | reach, megapages | 512 | MiB |
| X14.10f | cause, load page fault | 13 | — |
| X14.10g | cause, ecall from U | 8 | — |
| X14.11a | bus transactions | 5 | — |
| X14.11b | invalidations | 3 | — |
| X14.11c | SB outcomes, SC | 3 | — |
| X14.11d | SB outcomes, TSO | 4 | — |
| X14.11e | PCIe 5.0 x16 per direction | 63.02 | GB/s |
| X14.12a | issue slots | 32 | — |
| X14.12b | SIMD efficiency | 31.25 | % |
| X14.12c | sectors | 16 | — |
| X14.12d | bytes used | 25 | % |
| X14.12e | resident warps | 16 | — |
| X14.12f | occupancy | 25 | % |
| X14.13a | global L2 miss rate | 0.75 | % |
| X14.13b | AMAT | 2.2 | cycles |
| X14.13c | systolic cycles | 78 | — |
| X14.13d | utilization | 82.1 | % |
| X14.13e | warps needed | 41 | — |
| X14.14a | dense BF16-equivalent | 500 | TFLOPS |
| X14.14b | ratio to H100 | 0.505 | — |
| X14.14c | ridge point | 250 | FLOP/B |
| X14.14d | tokens/s, BF16 weights | 14.3 | — |
| X14.14e | tokens/s, FP4 weights | 57.1 | — |
| X14.14f | implied batch | 8.75 | — |
