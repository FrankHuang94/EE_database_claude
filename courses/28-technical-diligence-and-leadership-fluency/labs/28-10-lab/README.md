# Lab 28-10 · Live Checks, Debriefs and Calibration

**Objective.** Practise the pocket-card calculations until each takes about a minute, score meetings as evidence with grouping by cause, and measure your own calibration with the Brier score.

**Chapter:** [28-10 · Conversation Scenarios](../../chapters/28-10-conversation-scenarios.md)

## Background

The lab collects the live checks of §3.5 (from chapters 28-02 to 28-09) as functions, adds a debrief scorer that counts answers sharing a cause once, and a Brier-score calculator (§3.4).

## Files

- `convo.py`: pocket-card functions, the debrief scorer, trajectories, the Brier score and a random drill generator.
- `28-10-convo-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · A follow-up answer** (notebook). *Predict* the posterior of Example 28-10.26 if the follow-up on the evasive answer comes back weak (likelihood ratio 0.3). Then plot the posterior's path answer by answer.

**Part 2 · Timed drills** (notebook). *Predict* how many of 12 random live checks you can finish within a minute each. Then run the drills, writing your answer before revealing the computed one, and record your times and errors.

**Part 3 · Calibration** (notebook). *Predict* the Brier score of a forecaster who said 0.8 on five claims that came true and 0.6 on five that did not. Then compute it and compare with always saying 0.5 and with an overconfident forecaster.

**Part 4 · Shared causes** (notebook). *Predict* Example 28-10.26's posterior if its two ratios of 3 come from the same fact. Then compare both debriefs.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-10.a | posterior after a weak follow-up | 64.3 | % |
| Lab 28-10.c | Brier score of the first forecaster | 0.20 | — |
| Lab 28-10.d | posterior with the repeat counted once | 66.7 | % |

## Discussion

1. A weak follow-up takes the posterior from about 86% to **64.3**%: one well-chosen question can undo much of a good meeting, which is why the debrief identifies the answer most worth chasing.
2. The drills show which checks are not yet automatic. Repeat the slow ones until each takes about a minute; in a meeting, a check that takes five minutes does not get done.
3. The first forecaster scores **0.20**, better than always saying 0.5 (0.25), while an overconfident forecaster scores worse than 0.5. Calibration rewards honest uncertainty.
4. Counting the repeated strong answer once lowers the posterior only to **66.7**% here, because the meeting had other evidence; grouping by cause matters most when the repeated answer dominates.

## Optional hardware

None. As an exercise, keep a debrief sheet for your next five real meetings and score your forecasts once the outcomes are known.
