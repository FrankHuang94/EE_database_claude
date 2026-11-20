<!-- status: verified -->
# 14-07 · Branch Prediction and Speculation

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The control-hazard and dynamic branch prediction sections of computer organization and graduate architecture courses: static prediction, branch history tables and 2-bit counters, correlating (global-history) predictors, branch target buffers, return-address stacks, speculative execution and its security consequences (Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, §4.9; Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, §3.3) |
| **Prerequisites** | [14-06 Pipelining and Hazards](14-06-pipelining-and-hazards.md), [03-01 Probability in EE Language](../../03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain why deep pipelines need branch prediction, and compute the CPI cost of mispredictions from branch frequency, accuracy and penalty.
2. Trace static, 1-bit, 2-bit and global-history (gshare) predictors on a branch sequence and explain which patterns each learns.
3. Describe the branch target buffer and the return-address stack, and say which control transfers each predicts.
4. Evaluate predictors by trace-driven simulation and turn their misprediction counts into cycle counts.
5. Explain speculative execution, how a misprediction is undone, and why speculation leaks information (Spectre), with the main classes of mitigation.

---

## 1. Big picture

In [14-06](14-06-pipelining-and-hazards.md) the five-stage pipeline lost two cycles on every taken branch and jump. On the lab's program, that was 912 of its 2850 cycles. A modern high-performance core is far deeper: a branch may not resolve until 15 or more cycles after it is fetched, and the core fetches several instructions per cycle. Waiting for every branch would waste most of the machine. Instead, the core **predicts** each branch's direction and target at fetch time, keeps fetching and executing down the predicted path, and **undoes** the work if the prediction was wrong. Today's predictors are right well over 90% of the time on typical code, and every remaining misprediction costs a pipeline's worth of work.

- **Prediction is the front end's main job.** Fetch must know the next address every cycle, long before any branch is decoded, let alone executed.
- **Accuracy is worth area.** Predictors use history tables of several kilobytes; one percentage point of accuracy can be worth several percent of performance on branchy code.
- **Some branches cannot be predicted.** A branch on random data is right about half the time whatever the predictor. Programmers and compilers then remove the branch or make the data predictable (Example 14-07.6).
- **Speculation has a security cost.** Executing instructions that will be thrown away leaves traces in caches. The Spectre attacks, disclosed in January 2018, read secrets through exactly those traces.

## 2. Intuition first

**Guessing the road.** A driver on an unfamiliar road who stops at every junction to read the signs is safe but slow. A regular commuter drives through junctions at speed, taking the usual turn, and only brakes and reverses on the rare day the usual turn is wrong. Branch prediction makes the processor a commuter. Each branch's past behaviour is a good guide to its next outcome, because most branches are loop branches (taken many times, then once not) or tests that rarely change.

**Why two bits beat one.** A 1-bit predictor remembers only the last outcome. At the end of every loop it mispredicts the exit, then mispredicts again when the loop restarts, because it remembered "not taken". A 2-bit counter needs two wrong guesses in a row to change its mind. It survives the single anomalous exit and predicts the restart correctly, halving the loop's mispredictions (Example 14-07.2).

**History as context.** Some branches follow patterns: taken three times, then not, then repeat. Others depend on what nearby branches just did. A predictor that indexes its counters by the recent history of outcomes (a *global history*) learns such patterns, as a commuter learns that the bridge is closed on Tuesdays (Example 14-07.3).

**A finance analogy, and its limit.** Speculative execution is like a trader acting on a forecast before the data is published, with the right to unwind the position at no cost if the forecast is wrong. The hardware's "unwind" really does restore the architectural state exactly. Where the analogy breaks is the leak. A trader's unwound trade leaves a record that others can see, and so does speculation: it changes *microarchitectural* state, such as which data sits in the cache. That is invisible to correct programs but measurable by an attacker with a stopwatch (§3.6).

## 3. Theory

### 3.1 The cost of misprediction

Let a fraction $b$ of instructions be control transfers, let a fraction $m$ of those be mispredicted, and let each misprediction cost $P$ cycles (the number of stages between fetch and resolution, plus any recovery time). Then

$$
\text{CPI} = \text{CPI}_{\text{base}} + b\,m\,P .
$$

In the five-stage pipeline $P = 2$. In a deep pipeline with $P = 15$ and $b = 0.2$, accuracy $1 - m = 95\%$ adds 0.15 to CPI, and 99% adds 0.03 (Example 14-07.4). The deeper and wider the machine, the more each misprediction costs, so the more accuracy is worth. In the 14-06 cycle model, a misprediction replaces "taken": cycles $= N + 4 + S + 2M$, where $M$ counts fetches whose predicted next address was wrong.

### 3.2 Static prediction

A static predictor uses no run-time history.

- **Predict not taken:** fetch sequentially, as the 14-06 pipeline does. Every taken branch is a misprediction.
- **Backward taken, forward not taken (BTFN):** a branch to a lower address is probably a loop's closing branch, so predict taken; a forward branch is probably an `if` that skips code, so predict not taken. The target is computed from the instruction's offset, so fetch must partially decode the instruction (*predecode*).
- **Compiler hints and layout:** compilers arrange code so that the likely path falls through, and some ISAs carry hint bits.

Static schemes are cheap but cannot adapt: a loop with 10 iterations is predicted 90% right by BTFN, but a data-dependent `if` is a coin toss.

### 3.3 Dynamic direction predictors

**The branch history table (BHT).** A table of $2^n$ entries, indexed by the low bits of the branch's address (bits above the two always-zero bits), records recent behaviour. Branches whose addresses share those bits share an entry, which is called **aliasing**. The table has no tags, so a wrong entry merely costs accuracy, never correctness.

- **1-bit:** predict what this branch did last time. A loop branch is mispredicted twice per loop execution: at the exit, and at the first iteration of the next execution.
- **2-bit saturating counter:** values 0–3, predict taken if ≥ 2, count up on taken and down on not taken, saturating at 0 and 3. A strongly taken loop branch (3) drops only to 2 at the exit and still predicts taken next time, so it is mispredicted once per loop execution.

A counter of more bits adapts more slowly, rarely worth it. Two bits capture the important asymmetry: one anomaly should not change the prediction.

**Correlating (global-history) predictors.** A **global history register** (GHR) shifts in each conditional branch's outcome. The **gshare** predictor indexes its counter table by the XOR of the branch address bits and the last $h$ outcomes, so that the same branch gets different counters in different contexts.

- **Short repeating patterns.** An inner loop with 4 iterations produces the pattern T, T, T, N. A history of at least 4 outcomes distinguishes the exit iteration, and the counters learn it (Example 14-07.3).
- **Correlated branches.** `if (x > 0) … if (x > 5)` lets the second branch's outcome be predicted from the first's.

Real predictors combine several tables, using different history lengths, with selection logic. The published state of the art consists of refinements of the TAGE ("tagged geometric history length") family and of perceptron-based predictors (Further study); vendors describe their production designs only in general terms.

### 3.4 Predicting targets: the BTB and the return-address stack

A direction is not enough: to redirect fetch in the cycle *after* fetching a branch, the core must know the target before the instruction is even decoded.

**The branch target buffer (BTB)** is a cache indexed by the fetch address. It is tagged so that a hit means "the instruction at this address is a control transfer". Each entry stores the target taken last time. On a hit predicted taken, fetch jumps to the stored target in the next cycle. The BTB serves conditional branches (whose target never changes), direct jumps and calls, and indirect jumps.

**Returns are special.** A function called from several places returns to a different address each time, so the BTB's last-target guess is often wrong. The **return-address stack (RAS)** fixes this:

1. Every call pushes its return address (PC + 4).
2. Every return pops the stack, and the popped address is the predicted target.

The prediction is correct unless the stack overflows (very deep recursion) or is corrupted by mispredicted paths. RISC-V makes returns easy to recognize: the standard calling convention uses `jalr x0, 0(ra)`, and the specification's hint conventions for x1 and x5 tell the hardware which JALRs push and which pop the stack [1].

On the lab program, recursion makes returns 178 of the 554 control transfers. A 64-entry BTB with 2-bit counters mispredicts 205 fetches; adding a 16-entry RAS cuts that to 93 (Example 14-07.5).

![Two bar charts. Left: cycles for the lab program on the five-stage pipeline: 2850 with no prediction, 2348 with 2-bit counters and a BTB, 2124 adding a return-address stack, 2022 with gshare, a BTB and a RAS. Right: cycles for counting elements above 128 in 1000 bytes at a 15-cycle penalty: 14090 for branchy code on random data, 6620 on sorted data, 6059 for branchless code on random data.](../../../assets/figures/14-07/predictors.svg)

*Figure 1. Left: prediction recovers most of the five-stage pipeline's control-hazard losses on the lab program; the return-address stack matters most because of the recursion. Right: on a data-dependent branch, sorting the data or removing the branch is worth more than any predictor (Examples 14-07.5 and 14-07.6, Problem 14-07.9).*

### 3.5 Speculative execution

A pipeline that predicts a branch and keeps fetching is **speculating**: the instructions after the branch are executed before it is certain they should be. Correctness requires that speculative instructions change no **architectural state** (registers, memory, the PC as seen by the program) until the branch is confirmed.

- In the five-stage pipeline this is automatic. The branch resolves in EX, before any younger instruction reaches MEM or WB, so a flush discards work that has had no visible effect (14-06 §3.4).
- In a deep out-of-order core, dozens of younger instructions may have executed by the time a branch resolves. They are held in a reorder buffer and only **retire** (commit their results) in program order once all older branches are confirmed. On a misprediction, everything younger than the branch is squashed and the register mapping is restored (14-08).

Either way the architectural state is exactly as if the wrong path had never been fetched.

### 3.6 When speculation leaks: Spectre

Speculation does change **microarchitectural state**:

- which lines are in the caches (14-09);
- predictor tables;
- TLB entries.

None of it is architecturally visible, but all of it changes timing. In 2017, Google's Project Zero found that this can be exploited. It reported the issue to Intel, AMD and ARM on 1 June 2017 and published on 3 January 2018 [2]. The attacks were catalogued as three variants [2, 3]:

- **Variant 1, bounds check bypass** (Spectre, CVE-2017-5753). Code such as

  ```text
  if (x < array1_size)
      y = array2[array1[x] * 4096];
  ```

  is safe architecturally. But if the predictor has been trained to expect the bounds check to pass, a malicious out-of-range `x` makes the processor speculatively read `array1[x]`, a secret byte anywhere in the address space. It then loads the array2 element that the secret selects. The misprediction is squashed, but that element of `array2` is now in the cache. The attacker times accesses to `array2` (a "flush and reload" measurement) and learns which element is fast, hence the secret.
- **Variant 2, branch target injection** (Spectre, CVE-2017-5715): the attacker trains the BTB so that a victim's indirect jump speculatively goes to a "gadget" of the attacker's choosing.
- **Variant 3, rogue data cache load** (Meltdown, CVE-2017-5754): on affected processors, a user-mode load from kernel memory returns data speculatively before the permission check squashes it.

The official CVE description states the essence: "Systems with microprocessors utilizing speculative execution and branch prediction may allow unauthorized disclosure of information to an attacker with local user access via a side-channel analysis" [3] **[Established]**.

**Mitigations** come in four layers:

- **Software:** speculation barriers after security-relevant bounds checks; masking indices so that even a speculative access stays in bounds; and, for variant 2, "retpolines", which replace indirect jumps with returns that a controlled RAS predicts.
- **Hardware:** isolating predictor state between privilege levels and processes, and new processors designed so that speculative loads cannot cross protection boundaries (the fix for Meltdown).
- **Operating systems:** separate kernel page tables (the Meltdown mitigation).
- **Architecture:** treating the leak as part of the ISA contract. Some ISAs now define constant-time or speculation-control features.

Every layer costs some performance, and the field remains active **[Established]** (the existence and categories of mitigations; their costs vary by processor and workload and are **[Contested]**).

## 4. Worked examples

All counts in these examples come from trace-driven simulation: programs run on the course's RV32I simulator, and the resulting sequence of control transfers is replayed through each predictor model in the lab's `bpred.py`. The models use a 1024-entry table of 1-bit flags or 2-bit counters (initialized weakly not taken), an 8-bit global history for gshare, and a 64-entry direct-mapped BTB with full tags. Conditional branches are predicted by the direction predictor; jumps and calls are always predicted taken; returns use the RAS when one is present.

### Example 14-07.1 · Static prediction of a loop (tier A)

**Setup.** An inner loop of 10 iterations, ending in a backward `bnez`, is run 100 times by an outer loop. For the inner branch, find the accuracy of predict-not-taken and of BTFN.

**Solution.** The inner branch executes 1000 times: taken 900 times (back to the loop top) and not taken 100 times (the exits). Predict-not-taken is right only on the exits: **10.0**%. BTFN predicts the backward branch taken and is right on the 900 continuations: **90.0**%. In the simulation the outer branch adds 100 more executions (99 taken), so the totals are 999 and **101** mispredictions out of 1100 branches.

**Units check.** Accuracies are fractions of executions.

**Sanity check.** BTFN's misses are exactly the 100 loop exits plus the outer loop's single exit.

### Example 14-07.2 · One bit against two (tier B)

**Setup.** For the same loops, compare 1-bit and 2-bit dynamic predictors.

**Solution.** A 1-bit entry for the inner branch flips to "not taken" at each exit. When the outer loop restarts the inner loop, the first iteration is then mispredicted too: **2** mispredictions per inner-loop execution. The 2-bit counter sits at 3 (strongly taken) during the loop, drops to 2 at the exit (still predicting taken) and is right on the restart: **1** misprediction per execution. The simulation, including the outer branch and warm-up, gives **202** mispredictions for 1-bit and **103** for 2-bit out of 1100 branches.

**Units check.** Mispredictions are counts.

**Sanity check.** The 2-bit counter's extra mispredictions over 100 come from warm-up: it starts weakly not taken, so the first loop's first iterations are guessed wrong before the counter saturates.

### Example 14-07.3 · Learning a pattern with global history (tier B)

**Setup.** The inner loop now has 4 iterations (pattern T, T, T, N), still run 100 times. Compare the 2-bit predictor with gshare (8 bits of history).

**Solution.** The 2-bit counter still mispredicts every exit: **103** mispredictions in 500 branches, **79.4**% accuracy. gshare's history, the last 8 outcomes, distinguishes the fourth iteration ("three takens just happened") from the others. After a warm-up, it predicts the exit correctly too: **12** mispredictions, **97.6**% accuracy.

**Units check.** Accuracy = 1 − mispredictions/branches.

**Sanity check.** History helps only when the pattern fits in it. A loop of 100 iterations has a period longer than 8 bits of history, and gshare would do no better than 2-bit counters there.

### Example 14-07.4 · What accuracy is worth in a deep pipeline (tier B)

**Setup.** A deep pipeline has a 15-cycle misprediction penalty and a base CPI of 1. Control transfers are 20% of instructions. Find the CPI at 90%, 95% and 99% accuracy.

**Solution.** CPI $= 1 + 0.2 \times (1 - \text{accuracy}) \times 15$:

- 90%: **1.30**;
- 95%: **1.15**;
- 99%: **1.03**.

Going from 95% to 99% makes the machine 1.15/1.03 = **1.117** times faster.

**Units check.** $b$ and $m$ are fractions; $P$ is cycles; the product is cycles per instruction.

**Sanity check.** Each percentage point of accuracy is worth 0.03 CPI here, about 3%, which justifies kilobytes of predictor tables.

### Example 14-07.5 · The lab program under five predictors (tier C)

**Setup.** The lab program of 14-05 and 14-06 (an array sum and recursive `fib(10)`) executes $N$ = 1924 instructions, with $S$ = 10 load-use stalls and 554 control transfers (188 conditional branches, 178 calls and 178 returns, 456 of the transfers taken). On the five-stage pipeline, cycles $= N + 4 + S + 2M$. Find the cycles with no prediction, with a BTB and 2-bit counters, with a RAS added, and with gshare plus RAS.

**Solution.** The simulation gives the mispredicted fetches $M$:

| Predictor | $M$ | Cycles |
|---|---|---|
| None (always PC + 4, as in 14-06) | 456 | **2850** |
| 2-bit counters + BTB | 205 | **2348** |
| 2-bit counters + BTB + 16-entry RAS | 93 | **2124** |
| gshare + BTB + RAS | **42** | **2022** |

The RAS removes most of the return mispredictions; gshare learns `fib`'s base-case branch better than a single counter can. With the best predictor the program runs 2850/2022 = **1.409** times faster than without prediction.

**Units check.** Cycles from the 14-06 model, which the lab's Verilog pipeline matches exactly for the no-prediction case.

**Sanity check.** Even the best predictor leaves 42 mispredictions. Some are cold misses (the first time each branch is seen); others are `fib`'s data-dependent base case.

### Example 14-07.6 · A branch on random data (tier B)

**Setup.** A loop counts the elements greater than 128 in an array of 1000 bytes. The same values are tested in random order and in sorted order. With 2-bit counters, a BTB and a RAS, find the mispredictions in each case, and the extra cycles on a pipeline with a 15-cycle penalty.

**Solution.** Unsorted, the data-dependent branch is taken about half the time at random, and the simulation gives **504** mispredictions. Sorted, the branch goes one way for the first part of the array and the other way after, and it is mispredicted **6** times. The difference, 498 mispredictions, costs $498 \times 15$ = **7470** cycles on the deep pipeline. That is more than the loop's 5526 instructions: the unsorted run takes more than twice as long for the same work.

**Units check.** Mispredictions × cycles per misprediction = cycles.

**Sanity check.** No history-based predictor can beat 50% on truly random outcomes: gshare is no better here. The remedies are to remove the branch (compute the count with arithmetic, as 14-03's branchless code does) or to make the data predictable.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-07.1a | predict-not-taken accuracy, inner branch | 10.0 | % |
| Ex 14-07.1b | BTFN accuracy, inner branch | 90.0 | % |
| Ex 14-07.1c | BTFN mispredictions, both loops | 101 | — |
| Ex 14-07.2a | 1-bit mispredictions per inner-loop execution | 2 | — |
| Ex 14-07.2b | 2-bit mispredictions per inner-loop execution | 1 | — |
| Ex 14-07.2c | 1-bit total | 202 | — |
| Ex 14-07.2d | 2-bit total | 103 | — |
| Ex 14-07.3a | 2-bit mispredictions, 4-iteration loop | 103 | — |
| Ex 14-07.3b | 2-bit accuracy | 79.4 | % |
| Ex 14-07.3c | gshare mispredictions | 12 | — |
| Ex 14-07.3d | gshare accuracy | 97.6 | % |
| Ex 14-07.4a | CPI at 90% | 1.30 | — |
| Ex 14-07.4b | CPI at 95% | 1.15 | — |
| Ex 14-07.4c | CPI at 99% | 1.03 | — |
| Ex 14-07.4d | speedup from 95% to 99% | 1.117 | — |
| Ex 14-07.5a | cycles, no prediction | 2850 | — |
| Ex 14-07.5b | cycles, 2-bit + BTB | 2348 | — |
| Ex 14-07.5c | cycles, 2-bit + BTB + RAS | 2124 | — |
| Ex 14-07.5d | mispredictions, gshare + BTB + RAS | 42 | — |
| Ex 14-07.5e | cycles, gshare + BTB + RAS | 2022 | — |
| Ex 14-07.5f | speedup over no prediction | 1.409 | — |
| Ex 14-07.6a | mispredictions, unsorted | 504 | — |
| Ex 14-07.6b | mispredictions, sorted | 6 | — |
| Ex 14-07.6c | extra cycles at a 15-cycle penalty | 7470 | — |

## 5. Simulate it

The lab, [labs/14-07-lab](../labs/14-07-lab/README.md), provides `bpred.py`: it runs RISC-V programs on the course simulator to collect their control-flow traces and replays them through predictor models. In the notebook you:

1. **Reproduce** the loop examples and watch each predictor's state evolve branch by branch.
2. **Compare predictors** on the lab program and plot cycles against predictor type and table size.
3. **Sorted against random data:** measure the data-dependent branch, then remove it with branchless code and measure again.
4. **Aliasing:** shrink the tables until different branches collide, and watch accuracy fall.

**Guided exercise (predict, then run).** **Before Part 2,** predict which helps the lab program more: replacing 2-bit counters with gshare, or adding a return-address stack. (The RAS: it removes 112 mispredictions, against 51 more for gshare on top, because recursion makes returns a third of all control transfers.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Larger prediction tables | Fewer aliasing mispredictions | Area, power, access time in the fetch stage | CPU front-end architect |
| Longer global history | Learns longer patterns and correlations | Slower training; needs larger tables | CPU front-end architect |
| BTB size | More branches redirected without delay | Area; often multi-level (small fast plus large slow) | CPU front-end architect |
| Return-address stack depth | Correct returns in deep call chains | Area; recovery logic after mispredictions | CPU front-end architect |
| Deeper speculation | More work done before branches resolve | Larger misprediction penalty; more state to undo; side-channel exposure | CPU architect, security architect |
| Speculation mitigations | Security | Performance, varying by workload | CPU, OS and compiler teams together |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| CPI cost of mispredictions | $b \times m \times P$ | §3.1 |
| Loop branch, 1-bit against 2-bit | 2 against 1 mispredictions per loop execution | Example 14-07.2 |
| Random-data branch | about 50% mispredicted, whatever the predictor | Example 14-07.6 |
| Five-stage penalty (resolved in EX) | 2 cycles | 14-06 |
| Example deep-pipeline penalty | 15 cycles | illustrative |
| Zen 5 front end | 16K-entry L1 BTB, 52-entry return stack | AMD, Hot Chips 2024 [4] |
| Spectre and Meltdown disclosure | reported 1 Jun 2017; public 3 Jan 2018 | [2] |

## 8. Common mistakes

- **Equating accuracy with performance.** A 95%-accurate predictor on a branch-dense workload with a large penalty can still cost more than the rest of the pipeline's stalls combined.
- **Forgetting targets.** A correct "taken" prediction is useless without the target in the same cycle; that is the BTB's job.
- **Predicting returns with the BTB.** Functions called from several places need a return-address stack.
- **Assuming squashed work leaves no trace.** It leaves no *architectural* trace; caches, TLBs and predictors still change, which is what Spectre exploits.
- **Trusting a predictor on random data.** No amount of history predicts a coin toss; remove the branch instead.
- **Measuring cold.** Short traces exaggerate warm-up mispredictions; real predictors see millions of branches.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Front ends are large.** AMD's Zen 5 core, for example, has a 16K-entry level-1 BTB and a 52-entry return-address stack, and fetches two 32-byte blocks per cycle [4, R-212] **[Established]** (vendor disclosure). Vendors rarely disclose the organization of their direction predictors in detail.
- **Prediction algorithms.** In the research literature, TAGE-style predictors (tagged tables indexed by geometrically increasing history lengths) and perceptron-style predictors are the state of the art; production designs are disclosed only in outline **[Established]** (for the literature; vendor internals are not public).
- **Speculative-execution attacks remain an active area.** New variants and mitigations continue to be published after the 2018 originals; mitigations combine hardware isolation, microcode and OS changes, and compiler barriers [2, 3, R-213] **[Established]** (the original CVEs and their disclosure dates are primary facts; the performance cost of mitigations is workload-dependent and **[Contested]**).

### Why it matters commercially

- **Branchy workloads expose the front end.** Databases, interpreters, compilers and control software run far below peak IPC, much of the gap being branch misprediction. Datacenter buyers measure on their own code.
- **Security is a design constraint.** Since 2018, processors are evaluated on their side-channel exposure as well as speed; for cloud providers, isolation between tenants is a product requirement.

### Marketing vs Reality

- **"99% branch prediction accuracy."** *Reality:* accuracy is workload-dependent and usually quoted on benchmark suites. *Sanity check:* ask for mispredictions per thousand instructions (MPKI) on the customer's workload, and for the misprediction penalty in cycles.
- **"Not affected by Spectre."** *Reality:* any processor that speculates past branches and has caches is, in principle, exposed to variant 1; what differs is how hard exploitation is and which mitigations are on by default. *Sanity check:* ask which CVE variants have been evaluated and which mitigations are enabled, with their measured cost.

### Questions for engineering leaders

1. **"What are your misprediction penalty and MPKI on our workload?"**
   *Strong:* measured numbers from performance counters, with a breakdown by branch type. *Evasive:* a single accuracy percentage.
2. **"How do you isolate predictor state between security domains?"**
   *Strong:* specific mechanisms (flushing or partitioning on context switch, tagging by privilege level) and their cost. *Evasive:* "we follow industry guidance".
3. **"What do mitigations cost on our software stack?"**
   *Strong:* measured slowdowns with mitigations on and off, per workload. *Evasive:* "negligible".
4. **"How do you evaluate predictor changes?"**
   *Strong:* trace-driven and cycle-level simulation on large trace libraries, validated against silicon counters. *Evasive:* "on benchmarks".

## 10. Concept check

**Q1.** Why does a deep pipeline need branch prediction more than a five-stage one?

<details><summary>Answer</summary>

The misprediction penalty grows with the number of stages between fetch and resolution, and the CPI cost is $b \times m \times P$. A wide core also loses several instructions' worth of fetch per cycle of penalty.

</details>

**Q2.** Why does a 2-bit counter mispredict a loop branch once per loop execution, while a 1-bit predictor mispredicts twice?

<details><summary>Answer</summary>

The single not-taken outcome at the loop exit moves the 2-bit counter from strongly to weakly taken, still predicting taken, so the restart is predicted correctly. The 1-bit predictor flips to not taken at the exit and so mispredicts the first iteration of the next execution too.

</details>

**Q3.** What does gshare use that a simple BHT does not, and what does it buy?

<details><summary>Answer</summary>

Global history: the recent outcomes of all branches, XORed with the branch address to index the counters. It lets one branch use different counters in different contexts, which learns short repeating patterns and correlations between branches.

</details>

**Q4.** Why does the BTB not predict returns well, and what does?

<details><summary>Answer</summary>

A function returns to different call sites, but the BTB remembers only the last target. A return-address stack pushes the return address at each call and pops it at each return, matching the nesting of calls.

</details>

**Q5.** In Spectre variant 1, what does the processor do wrong, and why is the result visible?

<details><summary>Answer</summary>

Nothing wrong architecturally. It speculatively executes past a bounds check it predicted would pass, reads an out-of-bounds secret, and uses it to index a load, then squashes all of it. The squashed load left a cache line behind, and timing which line is cached reveals the secret.

</details>

**Q6.** Why can no predictor do well on a branch over random data, and what can be done instead?

<details><summary>Answer</summary>

The outcomes carry no pattern for history to learn, so any predictor is right about half the time. Remove the branch (compute the result arithmetically, or with a conditional move or select) or reorder the data so that outcomes are predictable.

</details>

Now work the [problem set](../problems/14-07-problems.md).

## 11. Key terms

[Branch prediction](../../../reference/glossary.md#branch-prediction) · [Branch history table (BHT)](../../../reference/glossary.md#branch-history-table-bht) · [Two-bit saturating counter](../../../reference/glossary.md#two-bit-saturating-counter) · [Global history](../../../reference/glossary.md#global-history) · [gshare](../../../reference/glossary.md#gshare) · [Branch target buffer (BTB)](../../../reference/glossary.md#branch-target-buffer-btb) · [Return-address stack (RAS)](../../../reference/glossary.md#return-address-stack-ras) · [Aliasing (predictor)](../../../reference/glossary.md#aliasing-predictor) · [Speculative execution](../../../reference/glossary.md#speculative-execution) · [Side channel](../../../reference/glossary.md#side-channel) · [Spectre](../../../reference/glossary.md#spectre)

## 12. Connections

- **Builds on:** control hazards and the cycle model ([14-06](14-06-pipelining-and-hazards.md)); calls and returns ([14-03](14-03-assembly-and-the-compilation-stack.md)); probability ([03-01](../../03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md)).
- **Next:** [14-08 Out-of-Order and Superscalar Execution](14-08-out-of-order-and-superscalar.md), which speculates far beyond one branch.
- **Used later:** caches as the side channel ([14-09](14-09-memory-hierarchy-and-caches.md)); privilege and isolation ([14-10](14-10-virtual-memory.md)); GPUs, which avoid prediction by switching threads ([14-13](14-13-gpus-and-simt.md)).

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §4.9 (control hazards and dynamic prediction).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, §3.3 (advanced branch prediction).
- S. McFarling, "Combining Branch Predictors," DEC WRL Technical Note TN-36, 1993 (gshare).
- A. Seznec and P. Michaud, "A case for (partially) TAgged GEometric history length branch prediction," *Journal of Instruction-Level Parallelism*, 2006 (TAGE).
- P. Kocher et al., "Spectre Attacks: Exploiting Speculative Execution," IEEE Symposium on Security and Privacy, 2019; M. Lipp et al., "Meltdown: Reading Kernel Memory from User Space," USENIX Security, 2018.

## 14. Sources

1. RISC-V International, *The RISC-V Instruction Set Manual, Volume I*, version 20260120, RV32I chapter (JAL and JALR, and the return-address-stack hints for x1 and x5). [R-201](../../../reference/research-log.md#r-201--risc-v-unprivileged-isa-manual-version-20260120)
2. J. Horn, Google Project Zero, "Reading privileged memory with a side-channel," 3 Jan 2018. [R-213](../../../reference/research-log.md#r-213--spectre-and-meltdown-disclosure-and-cves)
3. MITRE CVE records CVE-2017-5753, CVE-2017-5715 and CVE-2017-5754. [R-213](../../../reference/research-log.md#r-213--spectre-and-meltdown-disclosure-and-cves)
4. AMD, "Next Generation 'Zen 5' Core," Hot Chips 2024. [R-212](../../../reference/research-log.md#r-212--amd-zen-5-core-hot-chips-2024)

Every misprediction count in this chapter comes from the lab's trace-driven models, re-run by the verify script on traces from the course simulator.
