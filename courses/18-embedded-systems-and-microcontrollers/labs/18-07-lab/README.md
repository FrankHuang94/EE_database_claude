# Lab 18-07 · Scheduling, Blocking and Priority Inversion

Chapter: [18-07 · RTOS Concepts](../../chapters/18-07-rtos-concepts.md)

## Objective

- Find the two-task rate-monotonic bound numerically and compare it with the derivation.
- Compare the Liu & Layland bound, the hyperbolic bound and exact response-time analysis on random task sets.
- Simulate fixed-priority and EDF schedules and watch where each misses deadlines.
- Reproduce priority inversion and its cure by inheritance and ceiling protocols.
- Measure queue occupancy against a consumer's stalls.

## Background

Fixed-priority tasks meet their deadlines if their response times $R_i = C_i + B_i + \sum_{hp}\lceil R_i/T_j\rceil C_j$ do not exceed their deadlines (§3.3). RM is schedulable below $n(2^{1/n} - 1)$; EDF up to $U = 1$ (§3.2–3.3). A mutex without a protocol lets medium-priority tasks extend a high-priority task's blocking without limit; inheritance and ceilings bound it to one critical section (§3.4).

The simulator steps time in integer units. A real kernel adds tick and switch overhead, which can be folded into each $C_i$ (§3.1).

## Files

- `rtsched.py`: `Task`, `simulate` (policies `"fp"` and `"edf"`, protocols `"none"`, `"inherit"`, `"ceiling"`), `utilization`, `ll_bound`, `hyperbolic_ok`, `rm_priorities`, `response_time`, `blocking_ceiling`, `queue_max_occupancy`, `two_task_min_utilization`, `random_task_sets`, `acceptance`.
- `18-07-rtos-lab.ipynb`: the guided notebook.

## Procedure

1. **The two-task bound.** Predict the smallest utilization of a just-schedulable two-task set and the period ratio where it occurs; run `two_task_min_utilization` with $T_1$ = 1000.
2. **Bounds against exactness.** Generate 2000 random three-task sets at $U$ = 0.80 and 0.90 with `random_task_sets` (random utilization splits, periods from 10 to 100); predict the fraction each test accepts; run `acceptance`.
3. **RM against EDF.** Predict when Example 18-07.3's task B first misses under RM; simulate 10 hyperperiods with both policies. Then raise B's WCET to 5 and simulate EDF.
4. **Priority inversion.** Predict H's response in Example 18-07.4 for medium-task lengths of 1, 5 and 20 under each protocol; simulate and plot the timelines.
5. **Queues.** A producer adds an item every 10 units; the consumer stalls for 45 units starting at an arrival, then one unit later, then for 50 units. Predict the largest queue occupancy in each case; run `queue_max_occupancy`.

## Expected results

- Part 1: a minimum of 0.8284 at $T_2/T_1$ = 1.414, matching $2(\sqrt2 - 1)$ at $\sqrt2$.
- Part 2: at $U$ = 0.80 the Liu & Layland test (0.780) accepts no set, the hyperbolic test about 70% and exact analysis all of them; at 0.90, none, about 5% and about 75%. Each test accepts everything the previous one does.
- Part 3: under RM, B's first deadline passes unmet at 7 (its first job finishes at 8); EDF meets every deadline. With B's WCET at 5 ($U$ = 1.11), EDF misses deadlines of both tasks, whereas RM would sacrifice only B.
- Part 4: without a protocol H's response is $6 + m$ for a medium task of length $m$: 7, 11 and 26; with inheritance or ceiling it stays at 6.
- Part 5: 5, 4 and 6 items.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-07.a | numerical two-task minimum utilization | 0.8284 | — |
| Lab 18-07.b | period ratio at the minimum | 1.414 | — |
| Lab 18-07.c | B's first missed deadline under RM | 7 | ms |
| Lab 18-07.d | H's response, no protocol, m = 20 | 26 | ms |
| Lab 18-07.e | H's response, inheritance, m = 20 | 6 | ms |
| Lab 18-07.f | deepest queue, 45-unit stall at an arrival | 5 | items |
| Lab 18-07.g | deepest queue, 50-unit stall | 6 | items |

## Discussion

1. Why does the hyperbolic test accept every set the Liu & Layland test accepts?
2. Why does a synchronous release (all tasks at time 0) reveal the worst interference but not necessarily the worst blocking?
3. Under overload, why can EDF make *every* task miss, while RM confines misses to low-priority tasks?

## Answers

1. For a fixed total $U$, $\prod(U_i + 1)$ is largest when all $U_i$ are equal, at $(U/n + 1)^n$. Setting that equal to 2 gives $U = n(2^{1/n} - 1)$, the Liu & Layland bound. So any set under the Liu & Layland bound has $\prod(U_i + 1) \le 2$.
2. Interference from higher-priority tasks is worst when they all release with the task (the critical instant). Blocking needs a lower-priority task to be *inside* a critical section at that instant, which a synchronous release never produces because the lowest-priority task has not started yet. The analysis adds $B_i$ for exactly this reason (Problem 18-07.4(d)).
3. EDF always runs the earliest deadline; when demand exceeds capacity, jobs that are already late keep the earliest deadlines and keep running, delaying every other task past its deadline in turn (a domino effect). RM keeps serving high-priority tasks at their normal rate, so only the lowest-priority tasks starve.

## Optional hardware

On a board with FreeRTOS or Zephyr, create three tasks at different priorities that toggle GPIOs while running, and a mutex shared by the high and low tasks. Watch the pins on a logic analyzer: reproduce Example 18-07.4's inversion with a binary semaphore, then switch to a mutex and see the low task's pin take over while the high task waits.
