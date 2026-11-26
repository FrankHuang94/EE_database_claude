# Lab 28-08 · Synergies, Paths and Registers

**Objective.** Use small models to see how integration delay erodes synergy value, how correlation between overlapping programs changes the case for keeping both, how a chip's export-control metrics are computed, and how an expected-loss register ranks integration risks.

**Chapter:** [28-08 · Post-Acquisition Integration Risk](../../chapters/28-08-integration-risk.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: synergy value $\rho S[1 - (1 + r)^{-n}]/r \times (1 + r)^{-d}$.
- §3.3: the parallel-path gain $W[1 - P(\text{both fail}) - \max(p_1, p_2)]$.
- §3.5: TPP = dense TOPS × bit length and performance density = TPP/die area [R-659].
- §3.6: expected loss $\sum p_iI_i$ and earn-out value $pC(1 + r)^{-T}$.

## Files

- `integrate.py`: the models.
- `28-08-integration-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Delay** (notebook). *Predict* the value of Example 28-08.1's plan if integration slips three years with 80% realization. Then plot value against delay for 60%, 80% and 100% realization.

**Part 2 · Correlated paths** (notebook). *Predict* the gain from keeping both of Example 28-08.3's programs if they fail together with probability 0.35. Then plot the gain against the joint-failure probability, with the $30M cost.

**Part 3 · Export metrics** (notebook). *Predict* the TPP of an accelerator with 2,000 dense FP8 TFLOP/s. Then tabulate TPP and density for a set of hypothetical chips against the 3A090.a thresholds.

**Part 4 · The register** (notebook). *Predict* Example 28-08.6's expected loss if the license risk is resolved before signing. Then plot each risk's expected loss before and after the mitigations.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-08.a | value, three years late, 80% | 113.9 | $M |
| Lab 28-08.b | gain with joint failure 0.35 | 10 | $M |
| Lab 28-08.c | TPP, 2,000 FP8 TFLOP/s | 16000 | — |
| Lab 28-08.d | expected loss, license resolved | 34 | $M |

## Discussion

1. Three years late at 80%, the plan is worth **113.9** $M, 60% of its headline. Integration plans that take years should be valued as such, not at the synergy run rate.
2. With a joint-failure probability of 0.35 the second program adds only **10** $M against a $30M cost. Correlation between programs is the most common reason a parallel path is worth less than it seems.
3. At 2,000 dense FP8 TFLOP/s the TPP is **16000**, more than three times the 4800 threshold; an acquisition that adds such products must plan for licensing under the rules in force [R-659].
4. Resolving the license risk takes the expected loss from $49M to **34** $M, the largest single improvement available, which is why license review belongs before signing.

## Optional hardware

None. As an exercise, take a public acquisition announcement in the semiconductor industry, list the integration risks you would put in its register, and estimate their probabilities and impacts before reading later news about the deal.
