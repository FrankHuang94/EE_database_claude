# Solutions 14-06 · Pipelining and Hazards

Problems: [14-06 problems](../problems/14-06-problems.md) · Chapter: [14-06](../chapters/14-06-pipelining-and-hazards.md). Every number below is recomputed by [verify_14_06.py](../verify/verify_14_06.py), which runs each listed program on the lab's pipelined Verilog core in Icarus Verilog and compares cycles, stalls, flushes and the register-write trace with the Python simulator and the cycle model, and evaluates the formulas and optimizations numerically.

---

## Solutions

### Solution 14-06.1

$N + k - 1$: $1000 + 4$ = **1004** cycles on 5 stages and $1000 + 9$ = **1009** on 10. For long programs the fill time is negligible, so the deeper pipeline's cost lies elsewhere (in hazard penalties, Problem 14-06.11).

### Solution 14-06.2

- `add x6, x5, x5` uses the loaded x5 in the very next instruction: a load-use hazard, **1** stall. After the stall, x5 is forwarded from MEM/WB.
- `sub x7, x6, x5` gets x6 from EX/MEM (one ahead). It gets x5 from the register file: while `sub` was in ID, the load was in WB, and write-before-read passed x5 straight through. (MEM/WB holds the stall's bubble when `sub` reaches EX.)
- `sw x7, 4(x10)` gets its store data x7 from EX/MEM.
- `lw` gets its base x10 from **EX/MEM**: `li x10` is the instruction just ahead. `sw` gets x10 from the register file, since `li x10` wrote back long before.

The six instructions (with EBREAK) take $6 + 4 + 1$ = **11** cycles.

### Solution 14-06.3

The slowest stage sets the clock: $T = 300 + 30$ = **330** ps. The single-cycle design of the same logic has period $1000 + 30 = 1030$ ps, so the speedup limit is 1030/330 = **3.121**, far from 5, because the stages are unbalanced and each pays 30 ps of overhead.

### Solution 14-06.4

Now the slowest stage is 250 ps: $T = 250 + 30$ = **280** ps, and the limit is 1030/280 = **3.679**. The cost is a sixth stage: one more pipeline register (power and area) and, if the split stage lies before branch resolution, one more cycle of branch penalty. Whether the gain survives depends on how often the pipeline flushes (Problem 14-06.11).

### Solution 14-06.5

When `add` is in EX, EX/MEM holds `li x5, 10` (one ahead) and MEM/WB holds `li x5, 3` (two ahead). The forwarding unit must pick the most recent producer, EX/MEM, so both operands are 10 and x6 = **20**. If it preferred MEM/WB, both would be 3 and x6 = **6**: wrong, because the program order says x5 = 10.

### Solution 14-06.6

(a) Each `add` uses a value loaded by the instruction just before it: **2** stalls, and $6 + 4 + 2$ = **12** cycles.

(b) The two loads are moved together. Now `add x6, x5, x5` follows `lw x7`, two instructions after `lw x5`, so x5 is forwarded from MEM/WB. And `add x8, x7, x6` is two after `lw x7`. That is **0** stalls and $6 + 4$ = **10** cycles.

Both versions compute x8 = 91 from memory words 42 and 7.

### Solution 14-06.7

Taken control transfers per instruction: $0.20 \times 0.60 + 0.05 = 0.17$.

- With penalty 2: CPI = $1 + 2 \times 0.17$ = **1.34**.
- With penalty 1: CPI = $1 + 0.17$ = **1.17**.

Resolving in ID saves 13% of the time, if it does not lengthen the clock or add stalls (Problem 14-06.12).

### Solution 14-06.8

Each load or store costs one extra fetch cycle: CPI = $1 + 0.35$ = **1.35**. This is why pipelined processors have separate instruction and data paths, split L1 caches in practice (14-09).

### Solution 14-06.9

The division holds EX for 20 cycles instead of 1, so the instructions behind it wait **19** cycles. With 1% divisions, CPI = $1 + 0.01 \times 19$ = **1.19**. A pipelined or faster divider, or the multiply-and-shift replacement for constant divisors (14-04), reduces this.

### Solution 14-06.10

From the simulator's trace, the run has $S$ = 10 load-use stalls (all in the sum loop, unchanged) and $T$ = 4946 taken branches and jumps. Cycles = $20\,782 + 4 + 10 + 2 \times 4946$ = **30688**, and CPI = 30688/20782 = **1.477**.

That is close to the `fib(10)` run's 1.481 because the recursion dominates both runs. Each call to `fib` executes the same mix: two calls, a return and a taken base-case branch per leaf. So the fraction of taken transfers, and with it the CPI, barely changes with $n$.

### Solution 14-06.11

(a) Expanding the product gives $t(k) = t_{\text{logic}}/k + c\,t_{\text{logic}} + t_{\text{reg}} + c\,t_{\text{reg}}k$. Setting the derivative to zero:

$$
\frac{dt}{dk} = -\frac{t_{\text{logic}}}{k^2} + c\,t_{\text{reg}} = 0 \quad\Longrightarrow\quad k^* = \sqrt{\frac{t_{\text{logic}}}{c\,t_{\text{reg}}}} = \sqrt{\frac{1000}{0.1 \times 50}} = \textbf{14.14} .
$$

(b) Compare the neighbours:

- $t(14) = (71.43 + 50)(2.4)$ = 291.43 ps;
- $t(15) = (66.67 + 50)(2.5)$ = 291.67 ps.

The best integer depth is **14**, at **291.4** ps per instruction. The curve is very flat near the optimum, so designers trade a few stages for power or simplicity.

(c) $t_{\text{reg}}$ is the fixed cost of each pipeline register: clock-to-Q, setup, and the clock skew margin. $c$ is the hazard cost per stage: how much the average stall and flush time per instruction grows as more stages separate fetch from branch resolution and loads from their users. Better branch prediction lowers $c$ and pushes the optimum deeper.

### Solution 14-06.12

(a) In the rotated loop, `bne` immediately follows `addi a1, a1, -1`.

- **Resolved in EX:** 5 instructions, 1 load-use stall and 2 flush cycles: **8** per element.
- **Resolved in ID:** `bne` must wait one cycle for `addi`'s result, and a taken branch then costs 1. That is $5 + 1 + 1 + 1$ = **8**: no gain at all.

(b) In the scheduled loop, `addi a1` is two instructions before `bne`, so its result is ready in time.

- **Resolved in EX:** **7** per element.
- **Resolved in ID:** $5 + 0 + 0 + 1$ = **6**.

Earlier resolution pays only when the compiler schedules the branch's inputs early. Hardware and compiler work as a pair.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-06.1a | cycles, 5 stages | 1004 | — |
| 14-06.1b | cycles, 10 stages | 1009 | — |
| 14-06.2a | stalls | 1 | — |
| 14-06.2b | cycles | 11 | — |
| 14-06.3a | clock period | 330 | ps |
| 14-06.3b | speedup limit | 3.121 | — |
| 14-06.4a | clock period | 280 | ps |
| 14-06.4b | speedup limit | 3.679 | — |
| 14-06.5a | x6 | 20 | — |
| 14-06.5b | x6 with the wrong priority | 6 | — |
| 14-06.6a | stalls in (a) | 2 | — |
| 14-06.6b | cycles for (a) | 12 | — |
| 14-06.6c | stalls in (b) | 0 | — |
| 14-06.6d | cycles for (b) | 10 | — |
| 14-06.7a | CPI, penalty 2 | 1.34 | — |
| 14-06.7b | CPI, penalty 1 | 1.17 | — |
| 14-06.8a | CPI with one memory port | 1.35 | — |
| 14-06.9a | stall cycles per division | 19 | — |
| 14-06.9b | CPI | 1.19 | — |
| 14-06.10a | cycles with fib(15) | 30688 | — |
| 14-06.10b | CPI | 1.477 | — |
| 14-06.11a | optimal depth | 14.14 | — |
| 14-06.11b | best integer depth | 14 | — |
| 14-06.11c | time per instruction | 291.4 | ps |
| 14-06.12a | rotated loop, EX resolution | 8 | cycles |
| 14-06.12b | rotated loop, ID resolution | 8 | cycles |
| 14-06.12c | scheduled loop, EX resolution | 7 | cycles |
| 14-06.12d | scheduled loop, ID resolution | 6 | cycles |
