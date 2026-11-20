# Solutions 14-07 · Branch Prediction and Speculation

Problems: [14-07 problems](../problems/14-07-problems.md) · Chapter: [14-07](../chapters/14-07-branch-prediction-and-speculation.md). Every number below is recomputed by [verify_14_07.py](../verify/verify_14_07.py), which collects control-flow traces on the course simulator, replays them through the predictor models of the lab's `bpred.py`, and counts stalls with 14-06's hazard model.

---

## Solutions

### Solution 14-07.1

CPI $= 1 + 0.15 \times 0.08 \times 12$ = **1.144**.

### Solution 14-07.2

(a) The 2-bit counter starts at 1 (predict N). Each row shows the counter before the outcome:

| Outcome | T | T | N | T | T | T | N | N | T |
|---|---|---|---|---|---|---|---|---|---|
| Counter | 1 | 2 | 3 | 2 | 3 | 3 | 3 | 2 | 1 |
| Prediction | N | T | T | T | T | T | T | T | N |
| Right? | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

That is **5** mispredictions, and the counter ends at **2**.

(b) The 1-bit predictor repeats the last outcome: predictions N, T, T, N, T, T, T, N, N. It is wrong at positions 1, 3, 4, 7 and 9, also **5** mispredictions. On this irregular sequence the two do equally badly.

### Solution 14-07.3

(a) A forward branch is predicted not taken, which is right 70% of the time: **70**%. (b) A backward branch is predicted taken, which is right on 19 of every 20 executions: **95**%.

### Solution 14-07.4

In steady state the 2-bit counter mispredicts only the exit: accuracy $(n - 1)/n$. The 1-bit predictor mispredicts the exit and the next first iteration: $(n - 2)/n$. For $n$ = 3: **66.7**% against **33.3**%. Short loops are where hysteresis matters most.

### Solution 14-07.5

The simulation finds the mispredictions drop to warm-up level at $h$ = **4** for $k$ = 4 and at $h$ = **10** for $k$ = 10.

The global history also contains the outer loop's branch, which is taken just before each inner-loop execution starts. Before the inner exit iteration, the last $k$ outcomes are $k$ takens: the outer branch's T, then $k - 1$ inner T's. Before the iteration just before it, they are the previous exit's N followed by $k - 1$ T's. Only a history of at least $k$ bits tells the two apart. With $k - 1$ bits both read "all taken".

### Solution 14-07.6

The deepest nesting is **10** calls: `main` → `fib(10)` → … → `fib(2)` → `fib(1)`. The mispredicted fetches are:

- depth 2: **127**;
- depth 4: **106**;
- depth 16: **93**.

Depth 16 is the same as for any depth of 10 or more, since the stack never overflows. Shallow stacks lose the bottom of deep recursions, and each return past the lost entries is mispredicted.

### Solution 14-07.7

The index is (PC >> 2) mod 1024: 0x1000 >> 2 = 1024, which gives entry **0**, and 0x2000 >> 2 = 2048, also entry **0**. If one branch is mostly taken and the other mostly not, they keep pushing the shared counter in opposite directions, and both are mispredicted much of the time. A **2048**-entry table, indexed by bits 12–2, puts them in entries 1024 and 0. A tagged design or a hash with history (gshare) would also separate them.

### Solution 14-07.8

CPI added $= \text{MPKI}/1000 \times P$: **0.01** with $P$ = 2, and **0.075** with $P$ = 15. The same predictor costs 7.5 times more on the deep pipeline.

### Solution 14-07.9

Cycles $= N + 4 + S + PM$:

| Version | $P$ = 2 | $P$ = 15 |
|---|---|---|
| Branchy | $5526 + 4 + 1000 + 2 \times 504$ = **7538** | $5526 + 4 + 1000 + 15 \times 504$ = **14090** |
| Branchless | $6010 + 4 + 0 + 2 \times 3$ = **6020** | $6010 + 4 + 0 + 15 \times 3$ = **6059** |

The branchless version wins by a factor of 1.252 at $P$ = 2, and by **2.325** at $P$ = 15, although it executes more instructions.

It also avoids the stalls because the loaded value is used two instructions after the load (`addi a0` sits in between). The branchy version tests the loaded value immediately, so every iteration stalls. Scheduling and branch removal go together.

### Solution 14-07.10

(a) $1000 \;\&\; 255$ = **232**: still inside the array, even when the bounds check is mispredicted.

(b) Speculation can now only read inside `a`, so it can no longer reach a secret elsewhere in the address space. The mask works only for a power-of-two size, where $x \;\&\; (\text{size} - 1)$ is $x \bmod \text{size}$. For other sizes, compilers use a conditional select (data-dependent, not predicted) to clamp the index.

(c) One AND instruction per protected access, and no extra misprediction. That is much cheaper than a speculation barrier, which stops all younger instructions until the branch resolves.

### Solution 14-07.11

(a) $2^{12} \times 2$ bits + 12 bits = 8204 bits, about **1.0** KiB.

(b) $1024 \times (20 + 30 + 1)$ = 52,224 bits = **6.4** KiB.

The BTB is the larger structure, because each entry stores a target address. Real front ends use several BTB levels, small and fast near fetch, larger and slower behind.

### Solution 14-07.12

`fib`'s base-case branch is taken (base case) or not (recursive case) in a pattern set by the shape of the recursion tree, not by a stable bias: across its 177 executions it is taken 89 times. A 2-bit counter needs two consecutive outcomes to change its prediction. On a branch that alternates often, it lags behind and is wrong more often than a 1-bit predictor, which at least gets runs of two right. Hysteresis helps only when anomalies are isolated, as with loop exits.

Global history helps because the outcome is predictable from context. Whether `fib` was just called from `fib(n-1)` or `fib(n-2)`, and what the previous base-case tests did, shows up in the recent outcomes of the same and nearby branches. gshare cuts the branch's errors from 87 to 35.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-07.1a | CPI | 1.144 | — |
| 14-07.2a | 2-bit mispredictions | 5 | — |
| 14-07.2b | final counter state | 2 | — |
| 14-07.2c | 1-bit mispredictions | 5 | — |
| 14-07.3a | BTFN accuracy, forward branch | 70 | % |
| 14-07.3b | BTFN accuracy, backward branch | 95 | % |
| 14-07.4a | 2-bit accuracy, n = 3 | 66.7 | % |
| 14-07.4b | 1-bit accuracy, n = 3 | 33.3 | % |
| 14-07.5a | minimum history, k = 4 | 4 | bits |
| 14-07.5b | minimum history, k = 10 | 10 | bits |
| 14-07.6a | deepest call nesting | 10 | — |
| 14-07.6b | mispredicted fetches, RAS depth 2 | 127 | — |
| 14-07.6c | mispredicted fetches, RAS depth 4 | 106 | — |
| 14-07.6d | mispredicted fetches, RAS depth 16 | 93 | — |
| 14-07.7a | BHT entry for both branches | 0 | — |
| 14-07.7b | table size that separates them | 2048 | entries |
| 14-07.8a | CPI added, penalty 2 | 0.01 | — |
| 14-07.8b | CPI added, penalty 15 | 0.075 | — |
| 14-07.9a | branchy cycles, P = 2 | 7538 | — |
| 14-07.9b | branchy cycles, P = 15 | 14090 | — |
| 14-07.9c | branchless cycles, P = 2 | 6020 | — |
| 14-07.9d | branchless cycles, P = 15 | 6059 | — |
| 14-07.9e | branchless speedup, P = 15 | 2.325 | — |
| 14-07.10a | masked index | 232 | — |
| 14-07.11a | gshare storage | 1.0 | KiB |
| 14-07.11b | BTB storage | 6.4 | KiB |
