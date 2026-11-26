# Lab 27-07 · Racks, Collectives, Failures and Tokens

**Objective.** Use small models of an AI cluster to see how the size of the scale-up domain sets the cost of synchronizing gradients, how failures and checkpoints set a large job's effective training time, and how batch size trades a rack's throughput against each user's speed and the cost per token.

**Chapter:** [27-07 · The AI Datacenter Server and Rack](../../chapters/27-07-ai-datacenter-server-and-rack.md)

## Background

The lab uses the chapter's models, with its assumed parameters:

- §3.2: the rack and facility power budget.
- §3.3: training compute $6ND$ and time $6ND/(nF_{\text{peak}}u)$.
- §3.5: the ring all-reduce $2(p-1)S/(pB)$ and its hierarchical form.
- §3.6: job MTBF $m/N$, Young's interval $\sqrt{2\delta M}$ and the lost fraction $\delta/\tau + (\tau/2 + R)/M$.
- §3.7: the decode step time, the throughput–interactivity frontier and the cost per million tokens.

## Files

- `rackmodel.py`: the models.
  - Per-device datasheet figures and machine balance; the rack and facility power.
  - Training compute, time, GPUs for a deadline, and energy.
  - Ring and hierarchical all-reduce.
  - Mean time between interruptions, Young's interval, lost fraction and the largest restart time.
  - Decode step time, largest batch and cost per million tokens.
- `27-07-rack-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · The size of the scale-up domain** (notebook). *Predict* the hierarchical all-reduce time for Example 27-07.4's 10 GB on 1,152 GPUs if they come in 8-GPU servers (144 servers) instead of 72-GPU racks. Then plot all-reduce time against domain size from 1 to 144.

**Part 2 · A bigger job** (notebook). *Predict* Young's interval and the effective training time for Example 27-07.5's job doubled to 32,768 GPUs, with 60 s saves and 10-minute restarts. Then plot effective training time against checkpoint interval for 10 s and 60 s saves.

**Part 3 · The frontier** (notebook). *Predict* the step time, throughput and per-user speed of Example 27-07.6's rack at B = 1024. Then plot per-user speed against throughput from B = 1 to the memory limit.

**Part 4 · What drives token cost?** (notebook). *Predict* Example 27-07.6's cost per million tokens if electricity doubles to $0.16/kWh. Then plot cost against utilization for both prices.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-07.a | in-server phases, 8-GPU servers | 19.4 | ms |
| Lab 27-07.a1 | cross-server all-reduce | 24.8 | ms |
| Lab 27-07.a2 | hierarchical total, 8-GPU servers | 44.3 | ms |
| Lab 27-07.b | mean time between interruptions, 32,768 GPUs | 5568 | s |
| Lab 27-07.b1 | Young's interval | 817 | s |
| Lab 27-07.b2 | Young's interval | 13.6 | min |
| Lab 27-07.b3 | lost fraction | 25.5 | % |
| Lab 27-07.b4 | effective training time | 74.5 | % |
| Lab 27-07.b5 | save or rework loss each | 7.3 | % |
| Lab 27-07.b6 | checkpoint loss | 14.7 | % |
| Lab 27-07.b7 | restart loss | 10.8 | % |
| Lab 27-07.c | step time at B = 1024 | 4.58 | ms |
| Lab 27-07.c1 | throughput at B = 1024 | 2.24e5 | tokens/s |
| Lab 27-07.c2 | per-user speed at B = 1024 | 218 | tokens/s |
| Lab 27-07.c3 | throughput against B = 256 | 2.14 | — |
| Lab 27-07.c4 | per-user speed against B = 256 | 0.534 | — |
| Lab 27-07.d | cost per million tokens at $0.16/kWh | 0.489 | $ |
| Lab 27-07.d1 | cost increase | 12.7 | % |

## Discussion

1. With 8-GPU servers the all-reduce takes **44.3** ms, against 24.5 ms with 72-GPU racks. The in-server phases (**19.4** ms) barely change, but the network now carries 1/8 of the gradient per GPU instead of 1/72, and its share (**24.8** ms) dominates.
2. Doubling the job halves the mean time between interruptions to **5568** s. Young's interval shrinks only by √2, to **817** s (**13.6** min), but the lost fraction rises to **25.5**%, leaving **74.5**% effective training time. The 10-minute restart, **10.8**%, is now the largest single loss once the **14.7**% checkpoint term is split into its equal save and rework halves (**7.3**% each).
3. At B = 1024 a step takes **4.58** ms, so the rack produces **2.24 × 10⁵** tokens/s at **218** tokens/s per user: **2.14** times Example 27-07.6's throughput at **0.534** of its per-user speed.
4. Doubling the electricity price raises the cost per million tokens from $0.434 to **$0.489**, **12.7**% more: exactly the energy share of the original cost. Halving utilization would double it.

## Optional hardware

None needed. On any machine with two or more GPUs and a collective-communication library, time an all-reduce for message sizes from 1 MB to 1 GB. Fit $T = a + bS$ and compare the slope with $2(p-1)/(pB)$ for your link.
