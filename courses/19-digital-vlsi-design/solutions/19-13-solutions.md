# Solutions 19-13 · Verification: Simulation, UVM, Formal and Emulation

Problems: [19-13 problem set](../problems/19-13-problems.md) · Chapter: [19-13](../chapters/19-13-verification-methods.md). Every number below is recomputed by [verify_19_13.py](../verify/verify_19_13.py).

---

## Solutions

### Solution 19-13.1

(a) (i) **Verification**: it shows that the netlist implements the RTL. (ii) **Validation** (post-silicon): it checks the real part in a real system. (iii) **Test**: it screens each die for manufacturing defects. (iv) **Verification**. (v) **Validation** of the specification itself: is it the right target? (vi) **Test**: it screens packaged parts for defects, including those that burn-in brings out.

(b) The LFSR that raises requests is the **sequence** (with its sequencer): it decides what stimulus to produce. Holding each request until it is granted is the **driver**'s job: turning the stimulus into legal pin activity under the interface protocol. The four checks are the **scoreboard** (fed by a monitor that observes `req` and `gnt`), or equivalently concurrent assertions bound to the interface. The counters are the **coverage collector**, a subscriber to the monitor. The lab collapses these into one module because the interface is tiny; UVM separates them so each can be reused or swapped.

### Solution 19-13.2

(a) $H_{32} = 4.0585$, so $32H_{32}$ = **129.9** samples.

(b) $H_{64} = 4.7439$, so $64H_{64}$ = **303.6** samples, about 4.7 per bin.

(c) Each bin is missed by all 64 samples with probability $(63/64)^{64} = 0.3650$, close to $e^{-1}$, so the expected number of empty bins is $64 \times 0.3650$ = **23.36**. After as many samples as bins, more than a third of the bins are still empty, the 08-05 result seen from the other side.

### Solution 19-13.3

(a) Inclusion–exclusion with $n = 8$, $t = 30$:

$$
\Pr = \sum_{k=0}^{8} (-1)^k \binom{8}{k}\left(1 - \frac{k}{8}\right)^{30} = 1 - 0.145657 + 0.005000 - 0.000042 + \cdots = 0.8593 ,
$$

so 30 samples fill all 8 bins with probability **0.8593**; the later terms are below $10^{-7}$.

(b) Evaluating the sum for increasing $t$: $t = 50$ gives 0.98994 and $t = 51$ gives 0.99119, so **51** samples are needed, more than twice the mean $8H_8 = 21.7$.

### Solution 19-13.4

(a) With $p = (0.5, 0.3, 0.15, 0.05)$, sum $1/p(S)$ over the 15 nonempty subsets with alternating signs:

- singles: $1/0.5 + 1/0.3 + 1/0.15 + 1/0.05 = 2 + 3.3333 + 6.6667 + 20 = 32.0000$;
- pairs: $1/0.8 + 1/0.65 + 1/0.55 + 1/0.45 + 1/0.35 + 1/0.2 = 14.6860$;
- triples: $1/0.95 + 1/0.85 + 1/0.7 + 1/0.5 = 5.6577$;
- all four: $1/1 = 1$.

$E[T] = 32.0000 - 14.6860 + 5.6577 - 1$ = **21.97** samples, only 10 % above the floor $1/p_{\min}$ = **20**: the rarest bin decides almost everything.

(b) Equal bins: $4H_4 = 4 \times 2.0833$ = **8.33** samples. Re-weighting the constraints cuts closure time by a factor of 2.6 without a single extra directed test.

### Solution 19-13.5

(a) $N - 1$ = **5** grants (the distance argument of §3.4).

(b) After losing the first arbitration, a requester sees at most 7 bursts by others in all, counting the one it just lost to, so its own burst starts at most $7 \times 16$ = **112** cycles after that arbitration.

(c) Fixed priority grants requester 0 on every cycle. The attempt that starts on cycle 1 needs `gnt[1]` on one of cycles 1 to 4; none comes, so it fails at the end of its window, on cycle **4**, and every later attempt fails three cycles after it starts.

(d) It passes all three. It never grants two requesters at once (`a_onehot`), grants only a requester (`a_subset`) and never idles while someone waits (`a_busy`). Only the fairness property separates it from round-robin. An assertion set checks exactly what was written down; a requirement nobody turned into a property ("no requester starves") is not checked at all, which is why verification plans are reviewed against the specification line by line.

### Solution 19-13.6

(a) The attempt that starts on cycle 2 needs `ack` on cycle 3 or 4. `ack` is high on cycle 4, so it **passes**.

(b) The attempt that starts on cycle 6 needs `ack` on cycle 7 or 8. Neither has it, so it fails at the end of the window, on cycle **8**. (The `ack` on cycle 9 is too late and does not rescue it.)

(c) `req |=> ##[1:2] ack` means `req |-> ##[2:3] ack`. The attempt from cycle 2 now needs `ack` on cycle 4 or 5 (passes, cycle 4) and the one from cycle 6 on cycle 8 or 9 (passes, cycle 9): **0** failures. The two properties encode different latency specifications; choosing the wrong operator silently moves the window by a cycle.

(d) `req` is low on 8 of the 10 cycles, so the original property passes vacuously **8** times. A cover property on `req` would confirm that the antecedent occurs at all.

### Solution 19-13.7

(a) The root tests $a$. If $a = 0$ the function is $bc$: test $b$; $b = 0$ gives 0, $b = 1$ leads to a node testing $c$. If $a = 1$ the function is $b + c$: test $b$; $b = 1$ gives 1, $b = 0$ leads to the same $c$ node (the function $c$, merged). Nodes: $a$, two $b$ nodes, one $c$ node: **4**.

(b) Fixing $x_1, \ldots, x_{i-1}$ leaves either $x_i \oplus \cdots \oplus x_n$ or its complement, depending on the parity of the fixed bits. Both depend on $x_i$, and they are different functions. So level 1 has one node and each later level two: $1 + 2(n - 1) = 2n - 1$. Parity is symmetric (it treats all variables alike), so every order gives the same count. For $n = 5$: **9** nodes.

### Solution 19-13.8

(a) Interleaved: at level $a_i$ the only non-zero subfunction is "the remaining bits are equal" (any earlier mismatch already gave 0), one node. After reading $a_i$, the diagram must remember its value for one step, so level $b_i$ has two nodes ($b_i$ must equal 0, or must equal 1). Three nodes per bit: $3n$.

(b) Separated: at level $a_i$, the rest of the function must remember all of $a_1, \ldots, a_{i-1}$, since each will be compared with its $b$ later; the $2^{i-1}$ assignments give distinct subfunctions, each depending on $a_i$, for $\sum_{i=1}^{n} 2^{i-1} = 2^n - 1$ nodes. At level $b_i$, with no mismatch yet, the subfunction is "$b_i..b_n$ equals the stored $a_i..a_n$", distinct for each of the $2^{n-i+1}$ values of $a_i..a_n$ and each depending on $b_i$: $\sum_{i=1}^{n} 2^{n-i+1} = 2^{n+1} - 2$ nodes. Total $3 \cdot 2^n - 3$.

(c) $n = 4$: **12** and **45** nodes. $n = 16$: **48** and **196 605** nodes.

### Solution 19-13.9

(a) The dropped term $p_{k-1}\cdots p_1 g_0$ is 1 when $a_0 = b_0 = 1$ (probability $1/4$) and each of the $k - 1$ bits 1 to $k - 1$ propagates ($a_j \ne b_j$, probability $1/2$ each). Then every $g_j$ with $1 \le j \le k - 1$ is 0, so the remaining terms of the carry vanish and the dropped term was the only 1: the carry is wrong and flips sum bit $k$. The probability is $2^{-2} \cdot 2^{-(k-1)} = 2^{-(k+1)}$.

(b) $p = 2^{-16} = 1.526 \times 10^{-5}$. $N = \ln(0.01)/\ln(1 - 2^{-16})$ = **3.02 × 10⁵** vectors, which take **0.302** s at $10^6$ per second. A unit-level random test finds this one easily.

(c) $p = 2^{-64}$ and $\ln(1 - p) \approx -p$, so $N = 4.605 \times 2^{64}$ = **8.50 × 10¹⁹** vectors: $8.5 \times 10^{13}$ s, or **2.69 × 10⁶** years at $10^6$ per second. A miter proves the same fault in a fraction of a second because the adder's BDDs are small in interleaved order.

### Solution 19-13.10

(a) $3 \times 3 \times 2$ = **18** states.

(b) Breadth-first search from (I, I, 0) reaches every combination except the two with both processes in C: **16** states.

(c) **Yes.** A process enters C only if the other is not in C at that moment, so the only way both could enter is from (R, R, turn) in the same step, and there the rule admits only the process named by `turn`. Together with the 16 reachable states (none has both in C), this confirms the property; it is even 1-inductive over all 18 states.

(d) Without the turn rule, both requesters see the other "not in C" and enter together: (I, I, 0) → (R, R, 0) → (C, C, 0), a counterexample of length **2**. The bug is a classic simultaneous-check race; simulation would hit it only when both requests arrive on exactly the same cycle.

### Solution 19-13.11

(a) From 0 the counter visits 0 to 9 and returns to 0: **10** reachable states (10 to 15 are unreachable).

(b) State 11 satisfies $P$ and steps to 12, so $P$ is not 1-inductive; the counterexample to induction is the unreachable state **11**.

(c) Work backwards from 12: its only predecessor is 11; 11's is 10; 10 has none (9 goes to 0, not 10). So at most two $P$-states (10, 11) can precede a 12. For $k = 2$ the path 10, 11, 12 breaks the step; for $k = 3$ no path of three $P$-states reaches 12. The base case (no violation within 2 steps from 0: the states 0, 1, 2) holds, so $P$ is **3**-inductive.

(d) The lemma $x \le 9$: it holds at 0, and every successor of a value from 0 to 9 is again from 0 to 9, so it is 1-inductive, and it implies $x \ne 12$.

### Solution 19-13.12

(a) $5 \times 10^8 / 10^6$ = **500** s per test; 200 tests one at a time take $10^5$ s = **27.8** h.

(b) $27.8/4$ = **6.94** h.

(c) $5 \times 10^8/(25 \times 10^6) = 20$ s per test; $200 \times 20$ s = 4000 s = **66.7** min.

(d) $5 \times 10^8/100 = 5 \times 10^6$ s = **57.9** days for a single test.

(e) The emulator keeps deep signal visibility, so a failing test can be debugged from captured waveforms; prototypes expose only a few probed signals. And the emulator recompiles quickly as the RTL changes daily, while a multi-FPGA prototype often needs re-partitioning and timing closure on each new RTL drop, so prototypes lag the latest design.

### Solution 19-13.13

(a) A plan row names a feature, its checker and its coverage. For example:

| Feature | Checked by | Measured by |
|---|---|---|
| Data come out in order, none lost or duplicated | Scoreboard with a reference queue in simulation | Coverage of the level × operation cross |
| `count` stays within 0 to 8 and tracks pushes and pops | Assertions, proven formally | Cover properties reaching 0 and 8 |
| `full` and `empty` match `count` | Assertions, proven formally | Bins for empty and full |
| Push when full and pop when empty are ignored | Assertion in simulation (and formal without the assumption) | Cross bins for push-on-full and pop-on-empty |

(b) One set of answers:

```systemverilog
a_bound:   assert property (@(posedge clk) disable iff (rst) count <= 8);
a_empty:   assert property (@(posedge clk) disable iff (rst) empty == (count == 0));
a_full:    assert property (@(posedge clk) disable iff (rst) full == (count == 8));
a_noover:  assert property (@(posedge clk) disable iff (rst) (full && push && !pop) |=> full);
m_nounder: assume property (@(posedge clk) disable iff (rst) !(pop && empty));
```

The assumption removes every trace with a pop on an empty FIFO, so the proof says nothing about how the design handles underflow: a bug there would pass. Either check underflow in simulation, or run a second formal job without the assumption, or turn the assumption into an assertion on the consumer block.

(c)

```systemverilog
covergroup fifo_cg @(posedge clk);
  cp_level: coverpoint count { bins empty = {0}; bins part = {[1:7]}; bins full = {8}; }
  cp_op:    coverpoint {push, pop};          // 00, 01, 10, 11
  x_level_op: cross cp_level, cp_op;
endgroup
```

The cross has $3 \times 4$ = **12** bins. Under the assumption, pop with an empty FIFO never happens, so (empty, 01) and (empty, 11) cannot be hit: **10** bins are coverable, and the other two should be marked `ignore_bins` (or the assumption dropped) rather than left as permanent holes.

(d) Prove the counter and flag properties formally: they involve a 4-bit counter and two inputs, a tiny state space, and a proof covers every sequence, including corner cases such as simultaneous push and pop at full. Leave data ordering to simulation with a scoreboard (or to formal with abstraction): it depends on the data values in all eight entries, a much larger state space, and a reference model expresses it naturally.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-13.2a | expected samples, 32 bins | 129.9 | — |
| 19-13.2b | expected samples, 64-bin cross | 303.6 | — |
| 19-13.2c | expected empty bins after 64 samples | 23.36 | — |
| 19-13.3a | probability 30 samples fill 8 bins | 0.8593 | — |
| 19-13.3b | samples for 99 % closure | 51 | — |
| 19-13.4a | expected samples, unequal bins | 21.97 | — |
| 19-13.4b | floor 1/p_min | 20 | — |
| 19-13.4c | expected samples, equal bins | 8.33 | — |
| 19-13.5a | worst grants to others, 6 requesters | 5 | — |
| 19-13.5b | worst wait for a burst, 8 requesters | 112 | cycles |
| 19-13.5c | cycle of the first fairness failure | 4 | — |
| 19-13.6a | cycle of the failure | 8 | — |
| 19-13.6b | failures of the non-overlapping version | 0 | — |
| 19-13.6c | vacuous passes | 8 | — |
| 19-13.7a | ROBDD nodes, 3-input majority | 4 | — |
| 19-13.7b | ROBDD nodes, 5-input parity | 9 | — |
| 19-13.8a | comparator nodes, interleaved, n = 4 | 12 | — |
| 19-13.8b | comparator nodes, separated, n = 4 | 45 | — |
| 19-13.8c | comparator nodes, interleaved, n = 16 | 48 | — |
| 19-13.8d | comparator nodes, separated, n = 16 | 196605 | — |
| 19-13.9a | vectors for 99 % detection, k = 15 | 3.02e5 | — |
| 19-13.9b | time at 10^6 vectors per second | 0.302 | s |
| 19-13.9c | vectors for 99 % detection, k = 63 | 8.50e19 | — |
| 19-13.9d | time at 10^6 vectors per second, k = 63 | 2.69e6 | years |
| 19-13.10a | states in the model | 18 | — |
| 19-13.10b | reachable states | 16 | — |
| 19-13.10c | counterexample length, buggy protocol | 2 | — |
| 19-13.11a | reachable states | 10 | — |
| 19-13.11b | counterexample to 1-induction | 11 | — |
| 19-13.11c | smallest k | 3 | — |
| 19-13.12a | emulator time per test | 500 | s |
| 19-13.12b | emulator suite time | 27.8 | h |
| 19-13.12c | suite time on 4 partitions | 6.94 | h |
| 19-13.12d | prototype suite time | 66.7 | min |
| 19-13.12e | RTL simulation time for one test | 57.9 | days |
| 19-13.13a | cross bins | 12 | — |
| 19-13.13b | coverable cross bins under the assumption | 10 | — |
