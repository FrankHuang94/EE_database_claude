# Lab 26-02 · Reviewers, Blind Spots, Ballots and Royalties

**Objective.** See how shared blind spots cap what reviews find, measure the bias of capture–recapture estimates by simulation, test the IEEE SA ballot rules, and explore the value of designing to a draft standard.

**Chapter:** [26-02 · Design Reviews, Documentation and Standards Bodies](../../chapters/26-02-design-reviews-and-standards.md)

## Background

§3.2 derived the fraction of defects found by $k$ independent reviewers, $1 - (1 - p)^k$, and its saturation when some defects are invisible to the review method. §3.3 derived the Lincoln–Petersen and Chapman estimates of the total number of defects from two reviews. §3.5 quoted the IEEE SA ballot thresholds, and Example 26-02.6 valued designing to a draft standard.

## Files

- `reviews.py`: detection by independent and blind-spot-sharing reviewers; expected review cost and the optimal team size; Lincoln–Petersen and Chapman estimates and a Monte Carlo of two reviews; IEEE SA ballot checks; royalty stacks; the expected value of an early start.
- `26-02-reviews-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Blind spots** (notebook). Keep Example 26-02.2's average detection rate at 0.35 per reviewer, but let a hidden fraction $h$ of defects be invisible (the rest found with probability $0.35/(1 - h)$). *Predict* the fraction five reviewers find at $h$ = 50%, then plot it against $h$ from 0 to 50% and against the number of reviewers.

**Part 2 · Capture–recapture bias** (notebook). A document has 36 defects; 11 are hard (each reviewer finds them with probability 0.1) and 25 easy (found with probabilities 0.6 and 0.75 by the two reviewers). *Predict* whether Chapman's estimate is biased high or low, compute the estimate implied by the expected counts, then simulate 20,000 pairs of reviews and compare the average estimate with the truth.

**Part 3 · Blocking a ballot** (notebook). *Predict* the largest balloting group in which three Do Not Approve voters can block a ballot in which everyone else approves (full return, no abstentions), then check group sizes with `ieee_ballot`.

**Part 4 · Draft or freeze** (notebook). *Predict* how the break-even probability of Example 26-02.6(b) changes if the value of time to market doubles to $10 M a month, then compute it and plot the net value against the probability of a late change for both values.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-02.a | five reviewers, half the defects hidden | 49.9 | % |
| Lab 26-02.a1 | per-reviewer rate on visible defects | 0.70 | |
| Lab 26-02.b0 | expected n1 | 16.1 | |
| Lab 26-02.b1 | expected n2 | 19.85 | |
| Lab 26-02.b2 | expected overlap | 11.36 | |
| Lab 26-02.b | estimate from expected counts | 28.1 | |
| Lab 26-02.b3 | shortfall against the true 36 | 22 | % |
| Lab 26-02.c | largest group three voters can block | 11 | |
| Lab 26-02.c1 | approval at that size | 72.7 | % |
| Lab 26-02.d | break-even probability at $10 M a month | 0.706 | |

## Discussion

1. At $h$ = 50% the same average detection rate yields only 49.9% of the defects with five reviewers, against 88.4% when no defect is hidden. Averages hide the structure that matters; ask what kinds of defects a review can find at all.
2. Capture–recapture undercounts by about a fifth when difficulty varies (28.1 against 36): with same-trained reviewers it tends to run low, so treat a small estimate as weak reassurance rather than a count of what remains.
3. With full return and no abstentions, three voters block any group of 11 or fewer (8 of 11 is 72.7%); from 12 members up they need allies. Consensus rules protect large minorities, not small ones.
4. Doubling the value of time raises the break-even probability from 0.545 to 0.706: the more valuable the market window, the more draft-standard risk is worth taking.

## Optional hardware

None needed. If you have access to a real review, ask two colleagues to review the same short document independently, and apply the capture–recapture estimate to their findings.
