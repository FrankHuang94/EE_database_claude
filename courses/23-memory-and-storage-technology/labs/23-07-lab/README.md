# Lab 23-07 · Simulating a Flash Translation Layer

Chapter: [23-07 · SSD Controllers and Storage Systems](../../chapters/23-07-ssd-controllers.md)

## Objective

Run a page-mapped flash translation layer in software, measure its write amplification under random writes, and compare it with the closed form of §3.3. Then see how skewed workloads and stream separation change it, and how a hard-decision code's failure probability falls off a cliff.

## Background

§3.3 derived the write amplification of FIFO garbage collection under uniform random writes, $A = \alpha/(\alpha + W(-\alpha e^{-\alpha}))$, with $\alpha$ the ratio of physical to user capacity, and quoted Desnoyers' greedy-cleaning results [1]. §3.5 gave the binomial failure probability of a code that corrects $t$ errors. A simulator lets you test both models and explore cases they do not cover, such as hot and cold data.

## Files

- `ssd.py`: the chapter's models and `simulate_ftl`, a page-mapped FTL with 64-page blocks, FIFO or greedy cleaning, optional hot/cold traffic and optional stream separation. It fills the drive once, warms up for two drive writes, then measures.
- `23-07-ssd-lab.ipynb`: the notebook for all three parts.

No circuit simulator is needed: an FTL is an algorithm, and software is its natural test bench.

## Procedure

**Part 1 · Write amplification against over-provisioning.**

1. Predict $A$ at 7%, 14% and 28% OP from the closed form.
2. Run `simulate_ftl` with FIFO cleaning at each OP and compare.
3. Switch to greedy cleaning. *Predict first:* better or worse, and by how much?
4. Rerun greedy and FIFO with `pages_per_block=512`. *Predict* whether greedy's advantage grows or shrinks.

**Part 2 · Hot and cold data.** Send 90% of the writes to 10% of the LBAs at 7% OP with greedy cleaning. *Predict* whether $A$ rises or falls compared with uniform writes. Then turn on `separate_streams`, which writes hot and cold data to different open blocks, as a host using Flexible Data Placement could.

**Part 3 · The ECC cliff.** Plot the failure probability of 1 KiB codewords with BCH-style codes correcting $t$ = 20, 40 and 60 errors against raw error rate (chapter Figure 3). For each, find the raw error rate at which the failure probability is $10^{-15}$.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-07.a | FIFO write amplification, 7% OP (closed form) | 7.82 | |
| Lab 23-07.b | FIFO write amplification, 14% OP (closed form) | 4.25 | |
| Lab 23-07.c | FIFO write amplification, 28% OP (closed form) | 2.48 | |
| Lab 23-07.d | raw error rate for 10⁻¹⁵, t = 20 | 2.15e-4 | |
| Lab 23-07.e | raw error rate for 10⁻¹⁵, t = 40 | 9.74e-4 | |
| Lab 23-07.f | raw error rate for 10⁻¹⁵, t = 60 | 1.98e-3 | |
| Lab 23-07.g | ratio of tolerable raw error rates, t = 60 to t = 20 | 9 | |
| Lab 23-07.h | parity ratio, t = 60 to t = 20 | 3 | |

- Part 1: with 65,536 user pages, the simulated FIFO values land within about 1% of the closed form. Greedy cleaning gives lower write amplification with 64-page blocks, by roughly a tenth at 7% OP and only a few percent at 28%, close to Desnoyers' values for that block size. At 512 pages per block the gap shrinks to a percent or two, and for the thousands of pages in real 3D NAND blocks it nearly vanishes.
- Part 2: the skewed workload makes greedy cleaning worse than under uniform writes, because victims keep carrying cold pages. Separating the streams lowers $A$ by roughly a fifth in the default setting. The exact values depend on the skew and the seed.
- Part 3: tripling $t$ from 20 to 60 raises the tolerable raw error rate about ninefold, while the parity grows threefold.

## Discussion

1. Why does FIFO cleaning, which ignores how full each block is, come so close to greedy cleaning under uniform random writes?

   <details><summary>Answer</summary>

   Under uniform writes, every block ages the same way, so the oldest block is usually also among the emptiest. Greedy gains only from the random variation between blocks of similar age, and that variation shrinks as blocks hold more pages (the valid count of a large block averages over more pages). With skewed traffic, age and fullness decouple, but without hot/cold separation both policies suffer, because cold pages dilute every victim (Part 2).

   </details>

2. Why does the skewed workload hurt greedy cleaning?

   <details><summary>Answer</summary>

   Hot pages are invalidated quickly, but they share blocks with cold pages that stay valid. Each time such a block is cleaned, its cold pages are copied again. Over-provisioning is shared evenly between hot and cold data, although only the hot data benefits from it. Separating the streams puts cold data in blocks that rarely need cleaning.

   </details>

3. What does the simulator leave out?

   <details><summary>Answer</summary>

   Wear leveling, which adds copies of cold data; mapping-table persistence, which adds metadata writes; and read-disturb and retention refresh, which rewrite data the host did not touch. Each of these raises real write amplification above the model's. TRIM and workload locality lower it. Multi-die superblocks enlarge the erase unit, which pushes greedy cleaning toward FIFO's result.

   </details>

## Optional hardware

On a Linux machine with an NVMe drive, `nvme smart-log /dev/nvme0` reports the host data written and the percentage of the drive's endurance used. Some drives also report NAND writes in vendor-specific logs, from which you can compute your own write amplification (NAND writes divided by host writes) over a week of normal use.

## References

1. P. Desnoyers, "Analytic Modeling of SSD Write Performance," SYSTOR 2012.
