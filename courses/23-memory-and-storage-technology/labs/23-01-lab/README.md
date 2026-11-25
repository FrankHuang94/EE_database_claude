# Lab 23-01 · The Cost of Moving Data

Chapter: [23-01 · The Memory Hierarchy and the Memory Wall](../../chapters/23-01-memory-hierarchy-and-memory-wall.md)

## Objective

Confirm in a circuit simulator that charging a wire costs $CV^2$ from the supply whatever its resistance, then use the chapter's models to see how energy per bit, bandwidth, latency and the KV cache bound a memory system and the transformer decoding that runs on it.

## Background

§3.2 derived the supply energy of a 0 → 1 transition, $CV^2$, half of it stored and half dissipated. §3.3 turned energy per bit into power, §3.5 related bandwidth to data in flight through Little's law, and §3.7 built the decode model: bytes per step $W + Bkn$, FLOPs per step $B(2P + 4Ldn)$, and the capacity limit on the batch. `memwall.py` implements each relation; the verify script recomputes the chapter's numbers by independent routes.

## Files

- `wire_energy.cir`: a 1 mm wire as a 20-section RC ladder (200 fF and 2 kΩ in total, assumed), driven through 1 kΩ and then 10 kΩ from a 0.75 V step. It integrates the power the source delivers and computes the stored and dissipated energy.
- `memwall.py`: the chapter's models (wire energy, power budgets, interface bandwidth, Little's law, ridge points, the `Transformer` decode model).
- `23-01-memory-wall-lab.ipynb`: the notebook for Parts 2 to 4.

## Procedure

**Part 1 · Wire energy in ngspice.**

1. Predict the energy the source delivers (Example 23-01.2(b)), the energy left on the wire and the energy the resistors dissipate.
2. Run `ngspice -b wire_energy.cir`. Read `esup1` (1 kΩ driver), `estore`, `ediss1` and `esup2` (10 kΩ driver).
3. Explain why `esup2` equals `esup1` although the charging is several times slower.

**Part 2 · Power budgets and pins** (notebook).

1. Reproduce Examples 23-01.3 and 23-01.4 with `max_bandwidth`, `link_power`, `interface_bandwidth` and `per_pin_rate`.
2. Plot the bandwidth a 60 W budget allows against energy per bit from 1 to 20 pJ/bit, and mark GDDR5 and HBM2.

**Part 3 · Little's law** (notebook).

1. Reproduce Example 23-01.5.
2. With 75,000 requests of 64 bytes outstanding, plot the deliverable bandwidth against latency from 200 ns to 2 µs.

**Part 4 · Decode with a KV cache** (notebook).

1. Build Example 23-01.7's model with `Transformer` and reproduce its numbers.
2. Plot intensity against batch for 4k, 32k and 128k contexts, with the 625 FLOP/B ridge.
3. Change the KV cache to 4-bit entries and repeat.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-01.a | energy stored on the wire | 56.25 | fJ |
| Lab 23-01.b | energy dissipated in the resistors, 1 kΩ driver | 56.25 | fJ |
| Lab 23-01.c | largest batch, 4-bit KV cache, 32k context | 81 | |
| Lab 23-01.d | intensity limit, 4-bit KV cache, 32k context | 84.2 | FLOP/B |
| Lab 23-01.e | bandwidth with 75,000 requests at 1.2 µs | 4.0 | TB/s |

- Part 1: `esup1` and `esup2` within 0.2% of 112.5 fJ, `estore` 56.25 fJ, `ediss1` within 0.4% of 56.25 fJ.
- Part 4: with 4-bit KV entries, the KV bytes per token halve, so about twice as many sequences fit (81) and the intensity limit doubles (84.2 FLOP/B), still far below the ridge.

## Discussion

1. Why does the source deliver $CV^2$ whatever the resistance?

   <details><summary>Answer</summary>

   The source holds its voltage at $V$ while it pushes charge $CV$ onto the wire, so it delivers $QV = CV^2$. The resistance sets only how fast the charge flows, and the loss in it, $\int i^2R\,dt$, comes out at $\tfrac12CV^2$ for any $R$ (22-01). Only a slower *source* edge, which keeps the voltage across the resistance small, reduces the loss: that is adiabatic charging.

   </details>

2. Why does the 4-bit KV cache double the batch but not the tokens per second at a fixed batch?

   <details><summary>Answer</summary>

   Capacity is set by the KV bytes per sequence, which halve. At a fixed batch, the step still reads all the weights plus the (halved) KV caches. When the weights are a large share of the traffic, the step time falls by less than half.

   </details>

3. Why does doubling the latency halve the bandwidth in Part 3?

   <details><summary>Answer</summary>

   With a fixed number of requests in flight, Little's law gives bandwidth = data in flight / latency.

   </details>

## Optional hardware

On any Linux machine, the `lat_mem_rd` test of lmbench or a pointer-chasing loop measures load-to-use latency as the working set grows through the cache levels into DRAM. A STREAM-style copy measures sustained bandwidth. Compare both with the platform's datasheet peak.
