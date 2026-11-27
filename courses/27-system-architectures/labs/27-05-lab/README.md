# Lab 27-05 · Inside a Laptop SoC

**Objective.** Use small models of a laptop SoC to see how deep-idle residency sets battery life, how an averaged power limit shapes turbo, how memory bandwidth bounds local language models, and where splitting a die into tiles starts to pay.

**Chapter:** [27-05 · The PC SoC](../../chapters/27-05-pc-soc.md)

## Background

§3.2 gave average SoC power as residency-weighted state power and battery life as energy over total power. §3.3 derived turbo duration under an exponentially weighted power limit, $\tau\ln[(P_2 - P_0)/(P_2 - P_1)]$. §3.4 bounded decoding by bandwidth over model size and prefill by compute. §3.6 compared monolithic and tiled cost with 25-04's die-cost model. All parameters are assumed, as in the chapter's examples.

## Files

- `pcsoc.py`: residency power and battery life; turbo duration and an EWMA power trace; bus bandwidth, model footprint, decode bound and prefill time; accelerator power; dies per wafer, Poisson yield, die cost, chiplet package cost and link power.
- `27-05-pcsoc-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Deep idle and battery life** (notebook). *Predict* the battery life of Example 27-05.1 if deep-idle residency rises to 85% (active 8%, shallow idle 7%). Then plot life against deep-idle residency from 50% to 90%.

**Part 2 · Turbo** (notebook). *Predict* the turbo duration of Example 27-05.2's package if $\tau$ doubles to 56 s. Then simulate the averaged power through a 60 s task for both time constants.

**Part 3 · Local models** (notebook). *Predict* the largest 4-bit model that still decodes at 10 tokens/s on a 256 GB/s bus. Then plot tokens/s against model size for 136.5 and 256 GB/s.

**Part 4 · When do tiles pay?** (notebook). *Predict* the smallest total area at which two equal tiles on a 3 nm-class wafer (\$18,500, $D_0$ = 0.10 cm⁻²) in a \$10 package with 97% assembly yield cost less than one monolithic die. Then plot both costs against area.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 27-05.a | SoC power at 85% deep idle | 0.697 | W |
| Lab 27-05.a1 | battery life at 85% deep idle | 18.9 | h |
| Lab 27-05.b | turbo duration with a 56 s time constant | 27.7 | s |
| Lab 27-05.c | largest 4-bit model at 10 tokens/s | 51.2 | billion |
| Lab 27-05.d | break-even total area (whole mm²) | 225 | mm² |

## Discussion

1. Raising deep-idle residency from 70% to 85% lowers the SoC's average to **0.697** W and lengthens life from 18.2 to **18.9** h; the curve is flat because the display dominates, but losing deep idle altogether costs hours (Example 27-05.1d).
2. Doubling $\tau$ doubles the turbo to **27.7** s; vendors tune $\tau$ to the chassis's real thermal time constant, so a thin laptop with a large $\tau$ overheats and throttles thermally instead.
3. At 256 GB/s a 4-bit model of up to **51.2** billion parameters decodes at 10 tokens/s or faster; capacity, not bandwidth, is usually what excludes larger ones.
4. With these assumptions (and no interface area), two tiles beat one die from about **225** mm² of total area; below that the package cost and assembly loss outweigh the yield gain. Moving part of the design to a cheaper node (Example 27-05.5) moves the break-even far lower.

## Optional hardware

None needed. On a laptop, compare battery drain in a few minutes of video playback with a browser tab running an animation in the background and without it; operating-system power reports often show the change in idle residency.
