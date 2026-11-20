# Course 14 · Final Exam (Computer Organization and Architecture)

**Time limit:** 210 minutes.
**Allowed:** a scientific calculator, and the [Course 14 equation sheet](../../../reference/equation-sheets/14-computer-organization-and-architecture.md) printed without its chapter links. No notes, no Python, no simulator, no assembler.

**Instructions.**

- Answer all 14 questions and show every step.
- Question 1 [A] is worth 8 points (2 per part), each [B] 8, and Questions 13 and 14 [C] 12 each (4 per part): 120 points in total. 84 or more (70%) is a strong pass.
- Within a question the lettered parts carry equal weight.
- Give numerical answers to 3–4 significant figures, with units.
- Question 13 asks for derivations; Question 14 is a diligence question, partly graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- RISC-V RV32I unless stated; byte addresses; 1 KiB = 1024 bytes.
- The five-stage pipeline resolves branches in EX (2-cycle flush per taken branch) and stalls 1 cycle per load-use hazard: cycles = $N + 4 + S + 2T$.
- Caches use LRU replacement and write-back with write-allocate unless stated.
- H100 SXM: 67 TFLOPS FP32, 989.5 TFLOPS dense BF16, 3.35 TB/s (R-220).

---

**1 [A] · Performance.** (14-01)
(a) A program executes $2 \times 10^9$ instructions at a CPI of 1.5 on a 2.5 GHz processor. How long does it take?
(b) A redesign runs it at a CPI of 1.1 but only 2.0 GHz. What is the speedup?
(c) 80% of another program parallelizes perfectly. What is its speedup on 8 cores, and its limit on infinitely many?
(d) Dynamic power is $\alpha C V^2 f$. Lowering both the supply voltage and the clock by 10% saves what fraction of dynamic power?

**2 [B] · Instruction encoding.** (14-02)
(a) Encode `addi x5, x6, -3` as a 32-bit hexadecimal word.
(b) Decode the word 0x00A28233.
(c) What is the largest forward byte offset a conditional branch can reach?
(d) How many instructions does it take to load 0x12345678 into a register, and which?

**3 [B] · Assembly and calls.** (14-03)
(a) A loop body of 5 instructions executes 100 times, with 4 instructions of setup and return around it. How many instructions execute?
(b) A function saves ra and s0–s2 and needs 8 bytes for local variables. How large is its stack frame under the RISC-V ILP32 ABI?
(c) Which of t0, s1, a0 and ra must the *callee* preserve?
(d) Why does a leaf function usually need no stack frame?

**4 [B] · Numbers.** (14-04)
(a) In 8-bit two's complement, what does 100 + 50 produce, and is there overflow?
(b) Encode −6.25 in IEEE 754 single precision, in hexadecimal, and give its bfloat16 encoding.
(c) What is the spacing of FP32 numbers just above 1.0, and what does 1 + 2⁻²⁴ round to?
(d) Symmetric INT8 quantization of a tensor whose largest magnitude is 3.81: find the scale, and the integer and dequantized value of 1.0.

**5 [B] · Single-cycle datapath.** (14-05)
Delays: instruction memory 200 ps, register-file read 100 ps, ALU 150 ps, data memory 200 ps, write-back multiplexer 25 ps, register-file setup 50 ps.
(a) Find the critical-path delays of a load and of an R-type instruction, and the maximum clock frequency.
(b) A five-stage pipeline of the same logic has a slowest stage of 200 ps plus 30 ps of pipeline-register overhead. Find its clock frequency and its speedup on a long program with no stalls.

**6 [B] · Pipelining.** (14-06)
(a) A program of 1000 instructions has 150 load-use hazards and 100 taken branches. Find the cycles and the CPI on the five-stage pipeline.
(b) What would forwarding have to do to remove the load-use stalls, and why can it not?

**7 [B] · Branch prediction.** (14-07)
(a) A 2-bit saturating counter starts at 1 (weakly not taken). Trace the outcomes T, T, N, T, N, N, T, T and count the mispredictions.
(b) 20% of instructions are branches, the predictor is 90% accurate, and a misprediction costs 15 cycles. With a base CPI of 1, what is the CPI?

**8 [B] · Out-of-order execution.** (14-08)
For `I1: lw t0, 0(a0)`, `I2: add t1, t0, a1`, `I3: sub t0, a2, a3`, `I4: mul t2, t1, t0`, with latencies 3 (load and multiply) and 1 (otherwise):
(a) List the RAW, WAR and WAW dependences, and find the critical path.
(b) A 6-wide core must keep issuing through a 200-cycle miss. How many window entries does Little's law require? What IPC can a 512-entry window sustain during such a miss?

**9 [B] · Caches.** (14-09)
(a) A 16 KB, 4-way cache has 64-byte blocks and 32-bit addresses. Find the sets, the field widths, and the tag, index and offset of 0xABCD1234.
(b) L1 hits in 1 cycle and misses on 3% of accesses; L2 hits in 10 cycles and misses on 25% of its accesses; memory takes 120 cycles. Find the AMAT.
(c) A 4-block direct-mapped cache with 16-byte blocks sees the addresses 0x00, 0x40, 0x10, 0x00, 0x50, 0x40. Count the misses, and the misses of a fully associative LRU cache of the same size.

**10 [B] · Virtual memory.** (14-10)
(a) Split the Sv32 virtual address 0xC0FFEE00 into VPN[1], VPN[0] and offset.
(b) Find the reach of a 128-entry TLB with 4 KiB pages and with 4 MiB megapages.
(c) What cause code does a load page fault produce, and an `ecall` from user mode? After which of the two does the handler return to the same instruction?

**11 [B] · Coherence, consistency and I/O.** (14-11, 14-12)
(a) Under MESI, three cores perform: P0 reads X, P1 reads X, P0 writes X, P2 reads X, P1 writes X. Count the bus transactions and invalidations.
(b) How many outcomes of the store-buffering litmus test does sequential consistency allow, and how many does TSO allow?
(c) Find the per-direction bandwidth of a PCIe 5.0 x16 link (32 GT/s, 128b/130b).

**12 [B] · GPUs.** (14-13)
(a) In a warp, threads with `tid % 8 == 0` run 24 instructions and the rest 8. Find the issue slots and the SIMD efficiency.
(b) A warp reads 4-byte elements with a stride of 4 elements. How many 32-byte sectors does it touch, and what fraction of the bytes is used?
(c) An SM has 65,536 registers and room for 64 warps. A kernel uses 96 registers per thread in 256-thread blocks. Find the resident warps and the occupancy.

**13 [C] · Derivations.** (14-09, 14-14, 14-13)
(a) Derive the two-level AMAT formula, defining local and global miss rates, and evaluate it for Question 9(b)'s numbers with the global L2 miss rate.
(b) Show that an output-stationary systolic array computes an $M \times K$ by $K \times N$ product in $K + M + N - 2$ cycles, and evaluate it for M = N = 8, K = 64 on an 8 × 8 array, with the utilization.
(c) Derive the number of warps a scheduler needs to hide a latency $L$ when each warp issues $k$ instructions between waits, and evaluate it for $L$ = 600 and $k$ = 15.

**14 [C] · Diligence: an accelerator start-up.** (14-13 to 14-15)
A start-up's deck claims "4,000 TOPS — 10× an H100", "2 TB/s of HBM", and "a 70-billion-parameter model served at 500 tokens/s per chip". The fine print says the TOPS are FP4 with 2:4 sparsity.
(a) Assuming sparsity doubles the rate and each halving of precision doubles it, find the chip's dense BF16-equivalent rate and compare it with H100's.
(b) Find its ridge point at that rate.
(c) Find the batch-1 token rate that its bandwidth allows for the 70B model with BF16 weights and with FP4 weights, and the batch size the 500 tokens/s claim implies with FP4 weights.
(d) List four questions you would ask the founders, and what a strong answer looks like for each.
