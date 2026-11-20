<!-- status: reviewed -->
# 14-08 · Out-of-Order and Superscalar Execution

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The instruction-level-parallelism material of a computer architecture course: dependences, multiple issue, dynamic scheduling (Tomasulo's algorithm), register renaming, the reorder buffer and precise exceptions, and the limits of ILP (Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 3; Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, §4.11) |
| **Prerequisites** | [14-06 Pipelining and Hazards](14-06-pipelining-and-hazards.md), [14-07 Branch Prediction and Speculation](14-07-branch-prediction-and-speculation.md) |
| **Estimated study hours** | 9 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Classify the dependences between instructions as true (read-after-write) or name dependences (write-after-read, write-after-write), and explain which ones register renaming removes.
2. Compute the dataflow limit of a code sequence from its critical path, and explain why it bounds every machine.
3. Explain how a superscalar out-of-order core works: renaming with a map table and physical registers, dispatch into a window, issue when operands are ready, and in-order retirement from a reorder buffer.
4. Use a trace-driven scheduling model to measure how issue width, window size, renaming and branch prediction each limit instruction-level parallelism.
5. Size a reorder buffer with Little's law and explain why high-performance cores have windows of hundreds of instructions.

---

## 1. Big picture

The pipelines of 14-06 and 14-07 complete at most one instruction per cycle, and they stop whenever the next instruction in program order must wait, for a load or a multiply. Programs contain much more parallelism than that: in a loop that updates an array, every iteration's work is independent of the others. A **superscalar** processor fetches, decodes and executes several instructions per cycle. An **out-of-order** (OoO) processor goes further. It looks ahead through a window of upcoming instructions, executes each as soon as its inputs are ready, whatever its position in the program, and then puts the results back in program order so that software sees the same behaviour as on the simplest in-order machine. Almost every high-performance core of the last 25 years works this way, and it is why a modern core runs several instructions per cycle on ordinary code.

- **Instruction-level parallelism (ILP)** is the hidden parallelism in a sequential program; out-of-order hardware finds it automatically, without help from the programmer.
- **Renaming removes false dependences.** Reusing a register name does not mean reusing a value; the hardware gives every result its own physical register.
- **The reorder buffer keeps the illusion.** Instructions execute out of order but retire in order, so exceptions and mispredictions are precise.
- **The limits are dependences, branches and memory.** A chain of dependent loads (pointer chasing) runs at the speed of one load at a time, whatever the width of the machine (Example 14-08.5).

## 2. Intuition first

**A restaurant kitchen.** Orders arrive in sequence and must be served in sequence, but the kitchen does not cook them strictly one after another. While the steak for order 1 sears, the cook makes the salad for order 3, which needs nothing from order 1 or 2. Dishes wait at the pass until everything ahead of them has been served. The waiter (the **reorder buffer**) serves in order. The cooks (execution units) work on whatever is ready. The ticket rail (the **window**) shows how far ahead the cooks can look.

**Why reusing a name is not a real dependence.** Suppose order 2 says "use the large pan" and order 4 also says "use the large pan", for unrelated dishes. If the kitchen owns only one large pan, order 4 must wait, a conflict over the *name*, not the food. Give the kitchen many pans and label each dish's pan separately, and the conflict disappears. Register **renaming** does this: the 31 architectural register names are mapped to a much larger pool of physical registers, so each new value gets its own.

**Where the analogy breaks.** A kitchen can cook any order it likes, but a processor cannot fetch instructions it has not yet reached: the window is filled in program order, and a mispredicted branch fills it with dishes nobody ordered, all thrown away (14-07). And some recipes are strictly sequential: if each step needs the previous step's result, as when following a chain of pointers through memory, no number of cooks helps.

## 3. Theory

### 3.1 Dependences and the dataflow limit

Between two instructions $i$ (earlier) and $j$ (later) there are three kinds of register dependence:

- **Read after write (RAW), a true dependence:** $j$ reads a register that $i$ writes. $j$ needs $i$'s *value*, so $j$ cannot finish before $i$ produces it.
- **Write after read (WAR), an anti-dependence:** $j$ writes a register that $i$ reads. $j$ must not overwrite the register before $i$ has read it.
- **Write after write (WAW), an output dependence:** both write the same register. The final value must be $j$'s.

Only RAW dependences carry data. WAR and WAW are **name dependences**: they exist only because two values happen to share a register name, and giving the second value a different register removes them. Memory adds the same three kinds through load and store addresses. A load that reads a word an earlier store wrote is a true dependence through memory.

If every instruction could start the moment its true dependences were satisfied, with unlimited execution units, perfect branch prediction and no name dependences, a program would take as long as its **critical path**: the longest chain of RAW dependences, weighted by latencies. That is the **dataflow limit**:

$$
\text{cycles} \ge \text{critical path}, \qquad \text{IPC} \le \frac{N}{\text{critical path}} .
$$

No machine, however wide or clever, beats it (Example 14-08.2). Real machines fall short of it because of finite width, finite windows, branch mispredictions and memory latency.

### 3.2 Superscalar issue, in order

A **superscalar** processor fetches, decodes and issues up to $w$ instructions per cycle (its **width**). In an **in-order** superscalar, instructions issue in program order: a group goes together only if none depends on another in the group, and an instruction waiting for an operand blocks every younger one behind it. Doubling the width therefore never doubles performance. On the lab's unrolled loop, going from 1 to 2 to 4 wide raises IPC from 1.0 to 1.7 to 2.3 (Example 14-08.4), because every stalled load blocks the whole group behind it.

Multiple issue also multiplies hardware: $2w$ register-file read ports and $w$ write ports ([14-05 Problem 10](../problems/14-05-problems.md)), $w$ ALUs, and forwarding paths that grow as $w^2$, since every result may go to every input.

The alternative is **static** multiple issue, the **VLIW** (very long instruction word) approach. The compiler packs independent operations into fixed-format bundles, one per functional-unit slot, and the hardware checks nothing: the compiler must respect every latency, filling empty slots with no-ops. Unrolling loops gives it independent operations to pack (Problem 14-08.16). VLIW cores are common in DSPs and AI accelerators, where code is regular and the compiler sees it all. They are rare in general-purpose CPUs, where latencies vary (cache misses) and binary compatibility across generations matters.

### 3.3 Out-of-order execution: renaming, the window and the reorder buffer

An out-of-order core separates the in-order front end from an out-of-order execution core. Each instruction passes through these steps:

1. **Fetch and decode, in order**, $w$ per cycle, guided by the branch predictor (14-07).
2. **Rename, in order.**
   - A **register alias table** (map table) gives the current physical register for each architectural register (x1–x31; x0 is always zero and needs none).
   - The instruction's sources are looked up in it.
   - Its destination gets a *new* physical register from a free list, and the table is updated.
   - After renaming, only true dependences remain: two writes to x5 now write different physical registers, and a reader of the old x5 keeps its own copy.
3. **Dispatch, in order**, into two structures: the **issue queue** (reservation stations), where it waits for its operands, and the **reorder buffer (ROB)**, which records program order.
4. **Issue and execute, out of order.**
   - When all of an instruction's source physical registers are ready, it becomes eligible.
   - Each cycle a selection circuit issues up to $w$ ready instructions (usually oldest first) to the execution units.
   - Results are broadcast so that waiting instructions see that their operands are ready (Tomasulo's "common data bus").
5. **Retire (commit), in order.**
   - The oldest instruction in the ROB retires once it has finished. Its result becomes architectural, and the physical register it replaced returns to the free list.
   - In the simplest scheme, a mispredicted branch or a faulting instruction is handled when it reaches the head of the ROB: everything younger is squashed and the map table is restored. Real cores recover from a mispredicted branch as soon as it resolves, from a checkpoint of the map table taken at the branch. Exceptions still wait for the head, so that they stay precise.
   - Exceptions are therefore **precise**: the state is exactly as if all older instructions had finished and no younger one had started. That is what lets the operating system handle a page fault and resume the program (14-10).

This organization descends from Tomasulo's algorithm for the IBM System/360 Model 91 floating-point unit (1967). The ROB and in-order retirement were added later to make speculation and exceptions precise.

**Memory.** Loads and stores also go out of order. A **load/store queue** keeps stores in program order (memory is written only when a store retires) and checks whether each load overlaps an older store. If it does, the store's data is forwarded to the load; if not, the load may go ahead of the store. Cores predict which loads are safe to move early (**memory dependence prediction**) and replay any that guessed wrong.

### 3.4 What limits ILP

Four limits interact:

- **True dependences.** The dataflow limit. Pointer chasing, recursive reductions and long arithmetic chains have little ILP.
- **Width.** At most $w$ instructions per cycle are fetched, issued and retired.
- **Window size.** The machine can look only $W$ instructions ahead. A long-latency instruction, such as a cache miss of hundreds of cycles, fills the window with waiting instructions, and fetch stops. To hide a latency $L$ while sustaining $w$ instructions per cycle, the window needs about $w \times L$ entries, by **Little's law** (occupancy = throughput × time in the system; Example 14-08.6).
- **Branch mispredictions.** Every misprediction discards the window's work beyond the branch and restarts fetch. With a large window, the cost of each misprediction grows, because the window takes many cycles to refill.

![Two line charts from the lab's trace-driven model. Left: IPC against width 1, 2, 4 and 8 with a 256-entry window. The lab program with perfect prediction nearly tracks the width, reaching 7.54 at 8-wide; the unrolled loop out of order reaches 6.72, but in order only 2.77; the lab program with gshare mispredictions and a 10-cycle refill reaches 2.35; the linked list stays at 1.32 from 4-wide on. Right: IPC of a loop with one 20-cycle divide per element at width 4 against window size 8 to 256: 0.48, 0.72, 1.41, 2.51, then 3.56 at 128 and 256, close to the Little's-law estimate of the smaller of 4 and the window divided by 25.](../../../assets/figures/14-08/ilp-limits.svg)

*Figure 1. Left: each workload hits a different limit. Right: the window needed to hide a long latency follows Little's law (Problem 14-08.13).*

Each knob costs area and power superlinearly. Wider rename and issue logic, larger issue queues searched every cycle, more register-file ports and more physical registers all grow faster than linearly with width. This is why designs settled at widths of 4 to 8, with windows of a few hundred instructions, and why power, not transistor count, now caps single-thread performance (14-01, 14-12).

### 3.5 A trace-driven model of the machine

The lab's `ooo.py` replays a program's dynamic instruction stream, recorded by the course's simulator, through the steps of §3.3:

- dispatch of up to $w$ per cycle into a window of $W$ entries, in order;
- issue of up to $w$ ready instructions per cycle, oldest first, with latencies of 1 cycle (ALU), 3 (load, a cache hit, and multiply) and 20 (divide);
- loads waiting for the most recent older store to the same word, as with a perfect memory-dependence predictor;
- in-order retirement of up to $w$ per cycle;
- the window is the ROB: an entry is freed only when its instruction retires;
- an instruction issues at the earliest in the cycle after it is dispatched;
- fetch is unlimited across correctly predicted taken branches;
- optionally, in-order issue, no renaming (then WAR and WAW also stall), and mispredictions taken from 14-07's predictor models. A mispredicted branch stops dispatch after itself; no wrong-path instructions are simulated, and fetch resumes a fixed **refill** time after the branch completes. The refill models recovery at resolution plus the front end's restart, in cycles.

It has no caches, no port limits and no front-end details, so its IPC values are upper bounds for each configuration. Its point is to separate the limits.

### 3.6 Practical machines

A modern high-performance core combines everything in this chapter. AMD's Zen 5, for example, as disclosed by AMD:

- dispatches, renames and retires up to 8 instructions per cycle;
- has a reorder buffer of 448 entries (when one thread runs);
- has 240 integer physical registers, against the 16 general-purpose registers of the x86-64 architecture, with 6 integer ALUs and 4 address-generation units;
- has a 48 KB level-1 data cache serving 4 memory operations per cycle [1, R-212] **[Established]** (vendor disclosure).

Every number above was chosen with the trade-offs of §3.4 in mind. 448 entries at 8 per cycle cover about 56 cycles of latency at the peak rate. At a sustained 2 to 3 instructions per cycle, the same window covers 149 to 224 cycles. A DRAM access, hundreds of cycles at multi-GHz clocks (14-09), still fills it. Simultaneous multithreading (14-12) uses the same window for two threads when one alone cannot fill it.

## 4. Worked examples

All cycle counts in Examples 14-08.4 and 14-08.5 come from the lab's trace-driven model, run on instruction traces from the course simulator. Latencies are 1 cycle for ALU operations, branches and stores, 3 for loads and multiplies.

### Example 14-08.1 · Finding the dependences (tier A)

**Setup.** Classify every register dependence among these six instructions:

```text
I1: lw   t1, 0(a0)
I2: add  t2, t1, a1
I3: sub  t1, a2, a3
I4: mul  t3, t2, t1
I5: addi t2, a4, 1
I6: sw   t3, 4(a0)
```

**Solution.**

- **RAW (true):** I2 ← I1 (t1), I4 ← I2 (t2), I4 ← I3 (t1), I6 ← I4 (t3). That is **4**.
- **WAR:** I3 writes t1, which I2 reads; I5 writes t2, which I4 reads. That is **2**.
- **WAW:** I3 and I1 both write t1; I5 and I2 both write t2. That is **2**.

After renaming, I3's t1 and I5's t2 get new physical registers. Their name dependences vanish, so both can execute in the first cycle. The renamer allocates **5** physical registers, one per destination (I1–I5).

**Units check.** Counts of dependence pairs.

**Sanity check.** I4 reads the *new* t1, from I3, and the *old* t2, from I2. Renaming must give it exactly those, which the map table does because I4 is renamed after I3 and before I5.

### Example 14-08.2 · The dataflow limit (tier B)

**Setup.** With latencies of 3 for loads and multiplies and 1 otherwise, find the critical path of Example 14-08.1's six instructions and the highest possible IPC.

**Solution.** Follow the RAW chains, with each instruction finishing at the later of its producers' finish times plus its own latency:

- I1 finishes at 3.
- I2 finishes at $3 + 1 = 4$.
- I3 finishes at 1 (no producers).
- I4 finishes at $\max(4, 1) + 3 = 7$.
- I6 finishes at $7 + 1 = 8$.
- I5 finishes at 1.

The critical path is **8** cycles, so IPC ≤ 6/8 = **0.75**, however wide the machine.

**Units check.** Cycles are sums of latencies along a chain.

**Sanity check.** Two of the six instructions, I3 and I5, lie off the critical path. They are free in a wide machine, but nothing can shorten the chain I1 → I2 → I4 → I6.

### Example 14-08.3 · Renaming step by step (tier B)

**Setup.** At the start of Example 14-08.1, the map table holds t1 → p11, t2 → p12, t3 → p13, and the free list is p40, p41, p42, …. Rename I1 to I5.

**Solution.** Each destination takes the next free register, and each source reads the current mapping:

- I1: `lw p40, 0(a0)`; now t1 → p40.
- I2: `add p41, p40, a1`; now t2 → p41.
- I3: `sub p42, a2, a3`; now t1 → p42.
- I4: `mul p43, p41, p42`; now t3 → p43.
- I5: `addi p44, a4, 1`; now t2 → p44.

The old physical registers p11, p12 and p13, and later p40 and p41, return to the free list when the instructions that overwrote them retire. At that point no older instruction can still need them. The renamer used **5** new physical registers, and the final mapping is t1 → **p42**, t2 → p44, t3 → p43.

**Units check.** Physical-register numbers are labels; the count is what matters.

**Sanity check.** I4 reads p41 (I2's t2) and p42 (I3's t1): the true dependences of Example 14-08.1, with the false ones gone.

### Example 14-08.4 · Width, window and renaming on an independent loop (tier B)

**Setup.** A loop adds a constant to 256 array elements, unrolled four times: 901 instructions in all, whose iterations are independent. Using the trace-driven model with perfect branch prediction, find the cycles and IPC for a 1-wide in-order pipeline, 2-wide and 4-wide in-order superscalars, a 4-wide out-of-order core (64-entry window) with and without renaming, and an 8-wide out-of-order core with a 256-entry and with a 16-entry window.

**Solution.** The model gives:

| Machine | Cycles | IPC |
|---|---|---|
| 1-wide, in order | **905** | 0.996 |
| 2-wide, in order | **518** | 1.739 |
| 4-wide, in order | **389** | 2.316 |
| 4-wide, out of order | **262** | **3.439** |
| 4-wide, out of order, no renaming | **388** | 2.322 |
| 8-wide, out of order, 256 entries | **134** | **6.724** |
| 8-wide, out of order, 16 entries | **240** | 3.754 |

The critical path is only **69** cycles, so there is ample ILP. In-order issue gains little beyond 2-wide, because each load stalls its group. Out-of-order issue at the same width is 389/262 = **1.485** times faster. Without renaming, the reused registers t1–t4 in each unrolled iteration serialize the iterations, and the out-of-order core falls back to in-order performance. The 8-wide core needs its large window: with 16 entries it cannot see far enough ahead to fill its width.

**Units check.** IPC = 901 instructions / cycles.

**Sanity check.** Even the 8-wide machine stays well above the 69-cycle dataflow limit, because it can dispatch only 8 instructions per cycle, which takes at least ⌈901/8⌉ = **113** cycles. It achieves 134.

### Example 14-08.5 · Pointer chasing: when width does not help (tier B)

**Setup.** A loop sums the values in a linked list of 100 nodes. Each iteration loads the value, loads the next pointer, adds, and branches: 402 instructions in all. Find the critical path and the cycles on a 1-wide in-order pipeline and on 4-wide and 8-wide out-of-order cores.

**Solution.** Each iteration's `lw a0, 0(a0)` needs the previous iteration's `lw a0`, a chain of 100 loads of 3 cycles each. The critical path is **302** cycles. The model gives **505** cycles in order (1-wide), and **304** for both the 4-wide and the 8-wide out-of-order core: IPC **1.322**. The extra width buys nothing.

**Units check.** 100 dependent loads × 3 cycles ≈ 300 cycles.

**Sanity check.** The out-of-order core is already within 2 cycles of the dataflow limit. Only a shorter load latency (a faster cache, 14-09) or a different data structure (an array instead of a list) can help.

### Example 14-08.6 · How big a window? (tier C)

**Setup.** A 4-wide core must keep issuing while a load misses all the way to DRAM, taking 100 cycles. How many instructions must its window hold? What latency does Zen 5's 448-entry ROB cover at its 8-wide dispatch rate?

**Solution.** By Little's law, occupancy = throughput × time in the system. To keep 4 instructions per cycle flowing past a 100-cycle stall, the window must hold the $4 \times 100$ = **400** instructions fetched while the load waits. Zen 5's 448 entries at 8 per cycle last 448/8 = **56** cycles: and that assumes the peak dispatch rate. At a sustained 2 to 3 per cycle, the same window lasts 448/3 = **149** to 448/2 = **224** cycles. Either way, a DRAM access of hundreds of cycles stalls the core once the window fills.

**Units check.** Instructions per cycle × cycles = instructions.

**Sanity check.** This is why memory-level parallelism (several misses outstanding at once) and prefetching (14-09) matter as much as the window itself.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-08.1a | RAW dependences | 4 | — |
| Ex 14-08.1b | WAR dependences | 2 | — |
| Ex 14-08.1c | WAW dependences | 2 | — |
| Ex 14-08.1d | physical registers allocated | 5 | — |
| Ex 14-08.2a | critical path | 8 | cycles |
| Ex 14-08.2b | maximum IPC | 0.75 | — |
| Ex 14-08.3a | new physical registers used | 5 | — |
| Ex 14-08.3b | final mapping of t1 | 42 | (p42) |
| Ex 14-08.4a | 1-wide in-order cycles | 905 | — |
| Ex 14-08.4b | 4-wide in-order cycles | 389 | — |
| Ex 14-08.4c | 4-wide out-of-order cycles | 262 | — |
| Ex 14-08.4d | 4-wide out-of-order IPC | 3.439 | — |
| Ex 14-08.4e | 8-wide out-of-order cycles | 134 | — |
| Ex 14-08.4f | 8-wide out-of-order IPC | 6.724 | — |
| Ex 14-08.4g | critical path | 69 | cycles |
| Ex 14-08.4h | out-of-order speedup at 4-wide | 1.485 | — |
| Ex 14-08.4i | 2-wide in-order cycles | 518 | — |
| Ex 14-08.4j | 1-wide in-order IPC | 0.996 | — |
| Ex 14-08.4k | 2-wide in-order IPC | 1.739 | — |
| Ex 14-08.4l | 4-wide in-order IPC | 2.316 | — |
| Ex 14-08.4m | 4-wide out-of-order cycles, no renaming | 388 | — |
| Ex 14-08.4n | 4-wide out-of-order IPC, no renaming | 2.322 | — |
| Ex 14-08.4o | 8-wide cycles, 16-entry window | 240 | — |
| Ex 14-08.4p | 8-wide IPC, 16-entry window | 3.754 | — |
| Ex 14-08.4q | dispatch bound at 8-wide | 113 | cycles |
| Ex 14-08.5a | critical path | 302 | cycles |
| Ex 14-08.5b | out-of-order cycles (4- or 8-wide) | 304 | — |
| Ex 14-08.5c | IPC | 1.322 | — |
| Ex 14-08.5d | 1-wide in-order cycles | 505 | — |
| Ex 14-08.6a | window needed | 400 | instructions |
| Ex 14-08.6b | latency covered by Zen 5's ROB | 56 | cycles |
| Ex 14-08.6c | window lifetime at 3 per cycle | 149 | cycles |
| Ex 14-08.6d | window lifetime at 2 per cycle | 224 | cycles |

## 5. Simulate it

The lab, [labs/14-08-lab](../labs/14-08-lab/README.md), provides `ooo.py`, the trace-driven model of §3.5. In the notebook you:

1. **Measure the dataflow limit** of the unrolled loop, the linked list and the lab program.
2. **Sweep width and window** for each workload and plot IPC.
3. **Turn renaming off** and watch name dependences serialize the loop.
4. **Add branch mispredictions** from 14-07's predictors to the lab program, and see how much of the out-of-order core's advantage survives.

**Guided exercise (predict, then run).** **Before Part 2,** predict the IPC of the 8-wide core on the linked list. (1.32, the same as the 4-wide core's: the chain of dependent loads, not the width, sets the pace.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Issue width | Peak IPC | Rename, issue and forwarding logic growing faster than linearly; register-file ports | CPU architect |
| Window (ROB, issue queue) size | Latency tolerance (Little's law) | Area, power, and the cycle time of the wake-up and select loop | CPU architect |
| Physical register count | Instructions in flight without stalling rename | Register-file area and access time | CPU architect |
| Out-of-order against in-order | Performance on irregular code | Several times the core area and power | Product architect (big against little cores) |
| Memory-dependence prediction | Loads go early | Replays when wrong | CPU architect |
| Simultaneous multithreading | Fills idle width with a second thread | Shared resources, security isolation (14-07) | CPU architect, product manager |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Name dependences | WAR and WAW, removed by renaming | §3.1 |
| Dataflow limit | IPC ≤ $N$ / critical path | §3.1 |
| Window needed to hide latency $L$ at width $w$ | about $w \times L$ entries | Little's law |
| Zen 5 | 8-wide dispatch and retire; 448-entry ROB; 240 integer physical registers; 6 ALUs | AMD, Hot Chips 2024 [1] |
| Pointer chasing | IPC ≈ instructions per node / load latency, whatever the width | Example 14-08.5 |

## 8. Common mistakes

- **Treating WAR and WAW as real.** They are artefacts of register names; renaming removes them.
- **Forgetting memory dependences.** A load can depend on an earlier store to the same address; overlooking that makes ILP look larger than it is.
- **Assuming wider is always faster.** Width helps only when the code has independent instructions and the window is large enough to find them.
- **Equating out-of-order with "unordered".** Results retire in order; programs never see the reordering, except through timing.
- **Ignoring branch prediction.** A wide, deep window is wasted if a misprediction flushes it every few dozen instructions.
- **Quoting peak IPC.** Real code achieves a fraction of the width, set by its critical path, branches and memory.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Wide, deep cores.** Flagship cores now dispatch about 8 instructions per cycle with reorder buffers of several hundred entries. AMD's Zen 5 is an example (8-wide dispatch and retire, 448-entry ROB, 6 integer ALUs, 48 KB L1 data cache), with a claimed instructions-per-clock gain of up to 16% over Zen 4 [1, R-212] **[Established]** for the structure; the IPC claim is a vendor figure from AMD's own testing **[Industry estimate]**.
- **Big and little cores.** Phone, PC and some server processors pair wide out-of-order cores with small, efficient in-order or narrow out-of-order cores, and the operating system places threads by need **[Established]**.

### Why it matters commercially

- **Single-thread performance still sells.** Interactive and serial workloads (user interfaces, compilers, databases' critical paths) are paced by one core's IPC × frequency, and out-of-order width is where IPC comes from.
- **Area and power decide the mix.** A wide out-of-order core costs several times the area and power of a small core; how many of each go on a chip is a product-level decision (14-12).

### Marketing vs Reality

- **"8-wide core."** *Reality:* the width is the maximum per cycle in one stage; sustained IPC on real code is usually far lower, limited by dependences, branches and cache misses. *Sanity check:* ask for measured IPC on representative workloads, and where the bottleneck is (front end, back end, memory).
- **"+16% IPC."** *Reality:* AMD's figure is an "up to" claim, the best result over its chosen benchmarks at fixed frequency; the average is lower. *Sanity check:* ask which benchmarks, and how the gain varies (memory-bound code may gain nothing).

### Questions for engineering leaders

1. **"What limits IPC on our workload: front end, execution or memory?"**
   *Strong:* a top-down breakdown from performance counters, with the dominant stall named. *Evasive:* a peak-width figure.
2. **"How large is your window, and what latency does it hide?"**
   *Strong:* ROB, scheduler and load/store-queue sizes, and the latencies they cover. *Evasive:* "industry-leading".
3. **"What did the last generation's IPC gain cost in area and power?"**
   *Strong:* specific numbers, and the trade-off reasoning. *Evasive:* "the new node paid for it".
4. **"How do you verify the out-of-order core?"**
   *Strong:* reference-model comparison at retirement, random tests, and formal checks of the rename and recovery logic. *Evasive:* "extensive simulation".

## 10. Concept check

**Q1.** Which dependences does register renaming remove, and why can it not remove the others?

<details><summary>Answer</summary>

It removes WAR and WAW, which exist only because two values share a register name. Giving each new value its own physical register removes the conflict. RAW dependences carry an actual value from producer to consumer, and no renaming can supply it earlier.

</details>

**Q2.** What is the dataflow limit, and why is no real machine faster?

<details><summary>Answer</summary>

The execution time with unlimited resources and perfect prediction, which is the longest chain of true dependences weighted by latencies. Any machine must respect those dependences, so it can only equal this time or be slower.

</details>

**Q3.** If instructions execute out of order, how are exceptions precise?

<details><summary>Answer</summary>

Results retire from the reorder buffer in program order. When a faulting instruction reaches the head, everything older has retired and everything younger is squashed and its renaming undone, so the state is exactly as if execution stopped at the fault.

</details>

**Q4.** Why does an in-order superscalar gain little beyond two-wide on loops with loads?

<details><summary>Answer</summary>

Each load's user stalls, and in order nothing younger can pass it, so the extra slots go unused. Out-of-order issue lets independent later instructions use them.

</details>

**Q5.** Why does pointer chasing not speed up with width?

<details><summary>Answer</summary>

Each address comes from the previous load, so the loads form a single chain whose length times the load latency sets the time; extra width has nothing independent to execute.

</details>

**Q6.** How does Little's law set the window size?

<details><summary>Answer</summary>

To keep $w$ instructions per cycle flowing while a long-latency instruction takes $L$ cycles, the window must hold the $wL$ instructions that enter during that time.

</details>

Now work the [problem set](../problems/14-08-problems.md).

## 11. Key terms

[Instruction-level parallelism (ILP)](../../../reference/glossary.md#instruction-level-parallelism-ilp) · [Superscalar](../../../reference/glossary.md#superscalar) · [Out-of-order execution](../../../reference/glossary.md#out-of-order-execution) · [True dependence](../../../reference/glossary.md#true-dependence) · [Name dependence](../../../reference/glossary.md#name-dependence) · [Register renaming](../../../reference/glossary.md#register-renaming) · [Reorder buffer (ROB)](../../../reference/glossary.md#reorder-buffer-rob) · [Reservation station](../../../reference/glossary.md#reservation-station) · [Precise exception](../../../reference/glossary.md#precise-exception) · [Dataflow limit](../../../reference/glossary.md#dataflow-limit) · [Little's law](../../../reference/glossary.md#littles-law)

## 12. Connections

- **Builds on:** pipelines and hazards ([14-06](14-06-pipelining-and-hazards.md)); prediction and speculation ([14-07](14-07-branch-prediction-and-speculation.md)); dependences in compiled code ([14-03](14-03-assembly-and-the-compilation-stack.md)).
- **Next:** [14-09 Memory Hierarchy and Caches](14-09-memory-hierarchy-and-caches.md), where the latencies this chapter tries to hide come from.
- **Used later:** precise exceptions and interrupts ([14-10](14-10-virtual-memory.md)); multithreading and multicore as the alternative to more ILP ([14-12](14-12-multicore-coherence-consistency.md)); GPUs, which trade ILP for thread-level parallelism ([14-13](14-13-gpus-and-simt.md)).

## 13. Further study

- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 3 (instruction-level parallelism and its exploitation).
- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §4.11 (multiple issue).
- R. M. Tomasulo, "An Efficient Algorithm for Exploiting Multiple Arithmetic Units," *IBM Journal of Research and Development* 11(1), 1967.
- J. E. Smith and A. R. Pleszkun, "Implementing Precise Interrupts in Pipelined Processors," *IEEE Transactions on Computers*, 1988 (the reorder buffer).
- D. W. Wall, "Limits of Instruction-Level Parallelism," DEC WRL Research Report 93/6, 1993.

## 14. Sources

1. AMD, "Next Generation 'Zen 5' Core," Hot Chips 2024. [R-212](../../../reference/research-log.md#r-212--amd-zen-5-core-hot-chips-2024)

The dependence analysis, Tomasulo's algorithm, the reorder buffer and Little's law are textbook material (Further study). Every cycle count in the examples comes from the lab's trace-driven model and is re-run by the verify script.
