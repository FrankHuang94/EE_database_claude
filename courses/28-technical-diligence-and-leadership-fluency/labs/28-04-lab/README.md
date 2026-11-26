# Lab 28-04 · Checking the Answers Behind the Question Banks

**Objective.** Use small models to see what an iso-power CPU claim demands, where decode sits on an accelerator's roofline as the batch grows, what memory bandwidth costs in power at rising pin rates, and how a scored interview moves belief answer by answer.

**Chapter:** [28-04 · Domain Question Banks I](../../chapters/28-04-question-banks-digital-ai-memory-interconnect.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: an iso-power claim of ratio $R$ with IPC ratio $g_{\text{IPC}}$ and capacitance ratio $g_C$ needs the power at the new operating point to fall by $1 - 1/[g_C(R/g_{\text{IPC}})^3]$ (energy per operation against the previous product falls only by $1 - 1/R$).
- §3.2: decode intensity $2B/b_w$ FLOP per byte against the ridge point $F/B_{\text{mem}}$.
- §3.3–3.5: power = bits per second × energy per bit.
- §3.6: posterior odds = prior odds × the likelihood ratio of each answer.

## Files

- `qbank.py`: the models (iso-power requirement, DDR channel bandwidth, ridge point, decode intensity and attainable throughput, devices needed, stack bandwidth, link and port power, dB conversions, posterior odds and trajectory).
- `28-04-qbank-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · An iso-power claim** (notebook). *Predict* the energy-per-operation reduction Example 28-04.1 needs if the IPC gain is 20% instead of 15% (performance +25%, capacitance +10%). Then map the requirement against IPC gain from 0 to 25% for claimed gains of 15%, 25% and 35%.

**Part 2 · Decode against batch** (notebook). For Example 28-04.2's accelerator (2 PFLOP/s, 8 TB/s), *predict* the batch at which decode reaches the ridge with 4-bit weights, and the share of peak at batch 16. Then plot the share of peak against batch for 8-bit and 4-bit weights.

**Part 3 · Memory power at rising pin rates** (notebook). *Predict* the power of one 2,048-bit stack at 11.7 Gb/s and 6.5 pJ/bit at full read bandwidth, and of eight such stacks. Then plot stack power against pin rate from 6.4 to 13 Gb/s for 5.5, 6.5 and 7.5 pJ/bit.

**Part 4 · Scoring an interview** (notebook). *Predict* the posterior if a sixth answer in Example 28-04.6 is evasive (ratio 0.4). Then plot the posterior's trajectory answer by answer.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-04.a | frequency ratio, IPC +20% | 1.042 | — |
| Lab 28-04.a1 | power factor, IPC +20% | 1.243 | — |
| Lab 28-04.a2 | required reduction, IPC +20% | 19.6 | % |
| Lab 28-04.b | batch at ridge, 4-bit weights | 62.5 | sequences |
| Lab 28-04.b1 | share of peak at batch 16, 4-bit weights | 25.6 | % |
| Lab 28-04.c | one stack at 11.7 Gb/s, 6.5 pJ/bit | 156 | W |
| Lab 28-04.c1 | eight stacks | 1246 | W |
| Lab 28-04.c2 | one stack at 5.5 pJ/bit | 132 | W |
| Lab 28-04.c3 | one stack at 7.5 pJ/bit | 180 | W |
| Lab 28-04.d | odds after a sixth, evasive answer | 4.32 | — |
| Lab 28-04.d1 | probability after it | 81.2 | % |

## Discussion

1. With 20% more IPC the frequency rises only **1.042** times, the power factor is **1.243** and the claim needs a **19.6**% power cut at the new operating point, well within a node step. Each point of IPC the vendor can show lowers the burden on the process, so question D1 asks for the split between IPC, frequency and node.
2. With 4-bit weights the ridge is reached at batch **62.5**, and at batch 16 decode uses **25.6**% of peak, twice the 8-bit share. Halving the bytes per weight doubles decode throughput on a memory-bound machine, which is why quantization claims must come with accuracy at that precision (question A1, "the precision our models use").
3. One stack at 11.7 Gb/s draws about **156** W at full read bandwidth and eight draw **1246** W, more than most accelerators' whole budget; between 5.5 and 7.5 pJ/bit the single-stack figure moves from **132** W to **180** W. Real workloads do not read at full bandwidth all the time, but the sensitivity shows why the energy per bit at the shipping pin rate (M2) is a first-order question.
4. A sixth, evasive answer takes the odds from 10.8 to **4.32** and the probability from 91.5% to **81.2**%. One evasion costs less than one strong answer gains only because $0.4 > 1/3$; a likelihood ratio near 0.1 for a dodge on the central question would undo two strong answers.

## Optional hardware

None. As an exercise, take a public accelerator datasheet and compute its ridge point and the batch at which decode reaches it for the model sizes and precisions the vendor advertises.
