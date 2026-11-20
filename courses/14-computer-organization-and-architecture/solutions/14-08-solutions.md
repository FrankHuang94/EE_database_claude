# Solutions 14-08 · Out-of-Order and Superscalar Execution

Problems: [14-08 problems](../problems/14-08-problems.md) · Chapter: [14-08](../chapters/14-08-out-of-order-and-superscalar.md). Every number below is recomputed by [verify_14_08.py](../verify/verify_14_08.py).

- The short fragments are re-parsed from the published text and analysed by a renamer and scheduler independent of the lab's model.
- The cycle counts come from the lab's trace-driven model (`ooo.py`), run on traces of each program from the course simulator. The script also checks that every program computes the right answer.

---

## Solutions

### Solution 14-08.1

(a) **RAW** (true) on t0: `sub` needs the value `add` produces. Renaming cannot remove it.

(b) **WAR** on t1: `addi` must not overwrite t1 before `add` has read it. Renaming gives `addi` a new physical register, which removes the dependence.

(c) **WAW** on t0: the final t0 must be 7. Renaming removes it. The load still executes, because it can fault, but nothing waits for it.

(d) **RAW through memory**: the load reads the word the store wrote. Register renaming does not help. The load must receive the store's data, which the load/store queue forwards.

(e) **No dependence**: the addresses differ (offsets 0 and 8 from the same a0). The hardware only knows this once both addresses are computed. Until then, a memory-dependence predictor guesses that the load may go first.

### Solution 14-08.2

All four loads are independent and finish at cycle 3.

- **Chain:** the three adds are serial, so they finish at 4, 5 and 6. The critical path is **6** cycles and IPC ≤ 7/6 = **1.167**.
- **Tree:** `t0 + t1` and `t2 + t3` both finish at 4, and their sum at 5. The critical path is **5** cycles and IPC ≤ 7/5 = **1.4**.

For $n$ words, a chain has $n - 1$ dependent adds and a balanced tree has $\log_2 n$ levels. For 64 words:

- chain: $3 + 63$ = **66** cycles;
- tree: $3 + 6$ = **9** cycles.

Reassociating a sum turns a chain into a tree, which changes the dataflow limit from linear to logarithmic.

### Solution 14-08.3

(a) $6 \times 40$ = **240** entries.

(b) $512 / 8$ = **64** cycles.

(c) The instructions in the window cannot retire until the missing load does, so the window fills. Over the miss, at most 128 instructions enter, so IPC ≈ 128/100 = **1.28** while the miss is outstanding, however wide the core.

### Solution 14-08.4

(a) I10 to I13 retire in order, each once it has finished. I12 has finished but waits behind I11.

(b) When I14 reaches the head of the ROB, the fault is taken. I14 to I20 are squashed: **7** instructions. I17's result sits in a physical register that never becomes architectural, so no program or operating system ever sees it.

(c) The map table must return to its state just after I13, either from a checkpoint or by undoing the younger instructions' mappings from the ROB. The physical registers that I14 to I20 allocated go back to the free list. The operating system then handles the page fault and restarts the program at I14.

### Solution 14-08.5

(a) Dependences:

- **RAW:** I2 ← I1 (x5), I3 ← I2 (x6), I4 ← I3 (x5), I4 ← I2 (x6), I5 ← I2 (x6). That is **5**.
- **WAR:** I1 reads x6, then I2 writes it; I2 reads x5, then I3 writes it; I3 and I4 read x6, then I5 writes it. That is **4**.
- **WAW:** I1 and I3 both write x5; I2 and I5 both write x6. That is **2**.

(b) Each destination takes the next free register, and each source reads the current mapping:

| | Instruction | Renamed | Map change |
|---|---|---|---|
| I1 | `add x5, x6, x7` | `add p32, p6, p7` | x5 → p32 |
| I2 | `lw x6, 0(x5)` | `lw p33, 0(p32)` | x6 → p33 |
| I3 | `add x5, x6, x8` | `add p34, p33, p8` | x5 → p34 |
| I4 | `sw x5, 4(x6)` | `sw p34, 4(p33)` | none |
| I5 | `addi x6, x6, 4` | `addi p35, p33, 4` | x6 → p35 |

**4** new physical registers are used, since the store has no destination. The final mappings are x5 → **p34** and x6 → **p35**. Only the 5 RAW dependences survive.

(c) A physical register is freed when the instruction that *replaced* its mapping retires, because no older instruction can still need it after that. So p5 is freed when I1 retires, p6 when I2 retires, p32 when I3 retires, and p33 when I5 retires.

### Solution 14-08.6

(a) **In order, one per cycle.** Each issue cycle is the later of (previous issue + 1) and (sources ready):

| | I1 | I2 | I3 | I4 | I5 | I6 |
|---|---|---|---|---|---|---|
| Issue | 0 | 3 | 4 | 7 | 8 | 11 |
| Result ready | 3 | 4 | 7 | 8 | 11 | 12 |

The last result is ready in cycle **12**.

(b) **Out of order, unlimited width.** I1, I3 and I5 issue in cycle 0 and are ready at 3; I2 and I4 issue at 3 and are ready at 4; I6 issues at 4. The last result is ready in cycle **5**, which is the dataflow limit.

(c) **Compiler-scheduled, in order.** Issue cycles are I1 0, I3 1, I5 2, I2 3, I4 4 and I6 5, so the last result is ready in cycle **6**. Static scheduling recovers almost all of the out-of-order benefit here, because the compiler can see the whole fragment. It cannot do the same with latencies it does not know, such as cache misses, or across unpredictable branches. That is the case for dynamic scheduling.

### Solution 14-08.7

(a) Every `mul t0, t0, t1` needs the previous product, so the 128 multiplies form one chain of $128 \times 3$ = 384 cycles. It starts after `li a0` (1 cycle) and the first load (3 cycles): $4 + 384$ = **388**.

(b) **390** cycles at 4-wide, and **390** at 8-wide. The loop's 643 instructions need only about 161 cycles of dispatch at 4-wide, so the multiply chain sets the pace.

(c) The four chains each have 32 multiplies ($32 \times 3$ = 96 cycles after the first loads, at 4). Two levels of combining multiplies add 6, so the critical path is $4 + 96 + 6$ = **106**. The model gives **110** cycles at 4-wide and **108** at 8-wide. The speedup at 4-wide is 390/110 = **3.545**.

(d) Integer multiplication (and addition) modulo $2^{32}$ is associative, so regrouping gives the identical result. Floating-point addition and multiplication are not associative, because each operation rounds (14-04), so regrouping can change the result. Compilers therefore reassociate floating-point reductions only when allowed to, for example with `-ffast-math`.

### Solution 14-08.8

The array loop's only long chain is the accumulation `add t0, t0, t1` and the induction variables. The loads are independent, since each address comes from `addi a0`, not from memory.

- The critical path is **104** cycles: 100 one-cycle adds after `li a0` (1 cycle) and the first load (3).
- The 4-wide model gives **131** cycles, IPC 503/131 = **3.840**, close to the width.
- The linked list took 304 cycles, so the array is 304/131 = **2.321** times faster, despite executing 101 more instructions.

The data structure, not the instruction count, decides the speed.

### Solution 14-08.9

With renaming, **259** cycles. Every `lw t1` gets a fresh physical register, so the four element updates per iteration are as independent as with four architectural registers (262 cycles; the small difference comes from the different instruction order).

Without renaming, **1092** cycles. Every instruction now writes or reads t1, so each `lw t1` must wait for the previous `sw t1` to read t1 (WAR) and for the previous `add t1` to complete (WAW). The whole loop is serialized, which is worse even than the four-register version without renaming (388), where only reuse across iterations is serialized. Renaming makes the out-of-order core insensitive to the compiler's register allocation. In-order cores do not have that luxury, which is why their compilers allocate registers to avoid such reuse.

### Solution 14-08.10

(a) The cost per misprediction is the extra cycles divided by 42:

- 4-wide: $(1027 - 491)/42$ = **12.76** cycles;
- 8-wide: $(819 - 255)/42$ = **13.43** cycles.

(b) On the 8-wide core, $564/819$ = **68.9**% of the time is lost to mispredictions. The wider core loses a larger fraction, because its correct-path work goes faster while each misprediction costs about the same.

(c) Three effects add up:

- The misprediction is discovered only when the branch executes, and the branch waits for its operands. A return waits for `lw ra` to reload the return address from the stack, for example.
- The refill then costs 10 cycles.
- The window restarts empty, so the instructions after the branch cannot overlap with those before it, as they would with correct prediction.

### Solution 14-08.11

(a) With the window full, 70% of 256 = 179.2 instructions hold new results, so 180 in the worst case, in addition to the 32 committed architectural values: $32 + 180$ = **212** physical registers. (A design that never gives x0 a physical register needs one fewer.)

(b) $240 - 16$ = **224** integer results can be in flight, which is **50**% of the 448-entry ROB. Many ROB entries hold stores, branches or vector operations that need no integer register, so this ratio is a design choice, not a shortage. With two threads, the architectural state doubles to 32 registers, and the same ROB is split between the threads. This is a rough estimate: it ignores renamed flags and microcode temporaries, which AMD's disclosure does not break down.

### Solution 14-08.12

(a) Each element costs a load (3), the add (1) and the store (1) before the next load can read it: **5** cycles per element.

(b) The critical path is $1 + 256 \times 5$ = **1281** cycles, including `li a0` at the start. The model gives **1283** cycles at both 4-wide and 8-wide: width is useless against a recurrence.

(c) With the value kept in t1, the chain is one `addi` per element (1 cycle), and the stores no longer feed loads. The model gives **327** cycles at 4-wide, where it is limited by dispatching 1283 instructions 4 per cycle. The speedup is 1283/327 = **3.924**. (That 1283 is both the first version's cycle count and the second version's instruction count is a coincidence.) Compilers make this transformation, called register promotion, when they can prove that no other pointer aliases the array.

### Solution 14-08.13

(a) Little's law gives IPC ≈ $W/L$ when the window is the limit:

| Window | Estimate |
|---|---|
| 16 | 16/25 = **0.64** |
| 32 | 32/25 = **1.28** |
| 64 | 64/25 = **2.56** |

Four per cycle needs $4 \times 25$ = **100** entries.

(b) The model gives:

| Window | Model IPC |
|---|---|
| 16 | **0.717** |
| 32 | **1.410** |
| 64 | **2.514** |
| 128 | **3.562** |

Above about 100 entries the window stops being the limit. 256 entries give the same 3.562, limited by width and the start-up of the loop.

(c) Summing each instruction's residence time from dispatch to retirement gives an average of **22.2** cycles at $W$ = 16. The average occupancy is the total residence divided by the run time: **15.9** entries, just under 16, because the window is nearly always full. Little's law, occupancy = throughput × residence, holds exactly: 0.717 × 22.2 ≈ 15.9. The estimate was low because it assumed every instruction stays 25 cycles. In the model, the divides and adds do stay about 24–25 cycles, but the loads and branches spend only about 18. They enter the full window as soon as older entries leave, and they leave right behind the add they wait for.

### Solution 14-08.14

(a) Comparators $= 2 w Q$:

- 4-wide with 48 entries: $2 \times 4 \times 48$ = **384**;
- 8-wide with 96 entries: $2 \times 8 \times 96$ = **1536**.

(b) Each of $w$ results goes to $2w$ inputs: $2w^2$ = **32** paths at 4-wide, and **128** at 8-wide.

(c) Doubling the width, and the queue with it, quadruples both. The wake-up and select loop must also finish in one cycle for dependent instructions to issue back to back, so the larger structures also slow the clock. This is why wide cores split their execution units into clusters with partial bypassing, and why widths have stayed near 8 for decades.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-08.2a | critical path, chain of 4 | 6 | cycles |
| 14-08.2b | critical path, tree of 4 | 5 | cycles |
| 14-08.2c | IPC limit, chain | 1.167 | — |
| 14-08.2d | IPC limit, tree | 1.4 | — |
| 14-08.2e | critical path, chain of 64 | 66 | cycles |
| 14-08.2f | critical path, tree of 64 | 9 | cycles |
| 14-08.3a | window for 6-wide, 40 cycles | 240 | entries |
| 14-08.3b | latency covered by 512 entries at 8-wide | 64 | cycles |
| 14-08.3c | IPC during a 100-cycle miss, 128 entries | 1.28 | — |
| 14-08.4a | instructions squashed | 7 | — |
| 14-08.5a | RAW dependences | 5 | — |
| 14-08.5b | WAR dependences | 4 | — |
| 14-08.5c | WAW dependences | 2 | — |
| 14-08.5d | new physical registers | 4 | — |
| 14-08.5e | final mapping of x5 | 34 | (p34) |
| 14-08.5f | final mapping of x6 | 35 | (p35) |
| 14-08.6a | last result, in order | 12 | cycle |
| 14-08.6b | last result, out of order | 5 | cycle |
| 14-08.6c | last result, compiler-scheduled | 6 | cycle |
| 14-08.7a | critical path, one accumulator | 388 | cycles |
| 14-08.7b | cycles, one accumulator, 4-wide | 390 | — |
| 14-08.7c | cycles, one accumulator, 8-wide | 390 | — |
| 14-08.7d | critical path, four accumulators | 106 | cycles |
| 14-08.7e | cycles, four accumulators, 4-wide | 110 | — |
| 14-08.7f | cycles, four accumulators, 8-wide | 108 | — |
| 14-08.7g | speedup at 4-wide | 3.545 | — |
| 14-08.8a | critical path, array | 104 | cycles |
| 14-08.8b | cycles, array, 4-wide | 131 | — |
| 14-08.8c | IPC, array, 4-wide | 3.840 | — |
| 14-08.8d | speedup over the linked list | 2.321 | — |
| 14-08.9a | cycles with renaming | 259 | — |
| 14-08.9b | cycles without renaming | 1092 | — |
| 14-08.10a | cost per misprediction, 4-wide | 12.76 | cycles |
| 14-08.10b | cost per misprediction, 8-wide | 13.43 | cycles |
| 14-08.10c | time lost, 8-wide | 68.9 | % |
| 14-08.11a | physical registers needed | 212 | — |
| 14-08.11b | Zen 5 integer results in flight | 224 | — |
| 14-08.11c | as a share of the ROB | 50 | % |
| 14-08.12a | chain cost per element | 5 | cycles |
| 14-08.12b | critical path | 1281 | cycles |
| 14-08.12c | cycles, 4- and 8-wide | 1283 | — |
| 14-08.12d | cycles, value in a register, 4-wide | 327 | — |
| 14-08.12e | speedup | 3.924 | — |
| 14-08.13a | estimated IPC, 16 entries | 0.64 | — |
| 14-08.13b | estimated IPC, 32 entries | 1.28 | — |
| 14-08.13c | estimated IPC, 64 entries | 2.56 | — |
| 14-08.13d | window for IPC 4 | 100 | entries |
| 14-08.13e | model IPC, 16 entries | 0.717 | — |
| 14-08.13f | model IPC, 32 entries | 1.410 | — |
| 14-08.13g | model IPC, 64 entries | 2.514 | — |
| 14-08.13h | model IPC, 128 entries | 3.562 | — |
| 14-08.13i | average residence, 16 entries | 22.2 | cycles |
| 14-08.13j | average occupancy, 16 entries | 15.9 | entries |
| 14-08.14a | comparators, 4-wide, 48 entries | 384 | — |
| 14-08.14b | comparators, 8-wide, 96 entries | 1536 | — |
| 14-08.14c | bypass paths, 4-wide | 32 | — |
| 14-08.14d | bypass paths, 8-wide | 128 | — |
