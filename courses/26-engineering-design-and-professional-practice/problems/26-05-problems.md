# Problems 26-05 · Schedule and Risk: Why Respins Happen

Chapter: [26-05](../chapters/26-05-schedule-and-respin-risk.md) · Worked solutions: [26-05 solutions](../solutions/26-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- PERT: $\mu = (a + 4m + b)/6$, $\sigma = (b - a)/6$; tasks are independent and path durations approximately normal.
- Probabilities, durations and costs are assumed unless a source is cited; money in $ M unless stated.

---

## Problems

### Problem 26-05.1 [A]

**One task.** A block's verification is estimated at 6 weeks (optimistic), 8 (most likely) and 16 (pessimistic). Find its PERT mean and standard deviation and, with the normal approximation, the chance it is done within 10 weeks.

### Problem 26-05.2 [A]

**Pick the fix.** For each bug found in bring-up, name the cheapest likely fix (workaround, fuse or trim, metal-only ECO, full respin): (a) a control register resets to the wrong value; (b) a state machine misses one transition, and spare cells sit nearby; (c) an SRAM sense amplifier's transistors are too small to read reliably at low voltage; (d) a PLL's loop bandwidth is too low, and the design has bandwidth trim bits; (e) a speculative-execution path leaks data between processes, found after the chip has shipped.

### Problem 26-05.3 [B]

**A three-task path.** Physical design runs floorplanning (3, 4, 7 weeks), place and route (6, 8, 13) and signoff (2, 3, 6) in sequence. Find (a) each task's mean and standard deviation, (b) the path's mean and standard deviation, (c) the chance of finishing within 17 weeks, and (d) the date with a 95% chance.

### Problem 26-05.4 [B]

**Merge bias with four paths.** Four independent paths must finish before tape-out, and each has a 90% chance of finishing by the committed date. (a) What is the chance all four do? (b) What chance must each path have for the joint chance to be 90%? (c) By how many of its own standard deviations must each path's date move to achieve that?

### Problem 26-05.5 [B]

**Expected tape-outs.** A team expects first silicon to be production-worthy with probability 0.4, a second spin with 0.8 and a third certainly. Each respin adds 16 weeks and costs $15 M. Find (a) the expected number of tape-outs, (b) the probability of needing three, and (c) the expected delay and respin cost.

### Problem 26-05.6 [B]

**What a survey number means for you.** Suppose later spins succeed with probability 0.6 and then 1. Find the expected number of tape-outs if the first-spin success probability is (a) 0.14, (b) 0.05 and (c) 0.30. (d) What do the results say about how much the headline first-silicon statistic matters?

### Problem 26-05.7 [B]

**ECO or respin at 5 nm.** A chip has 90 mask layers, of which the last 30 are metal and via layers, and the fab averages 1.4 days per layer. A full mask set costs $25 M, the metal masks $6 M. A metal ECO needs $1.5 M of engineering and 3 weeks before the fab restart; a full respin needs $4 M and 5 weeks. Delay costs $2 M a week. Find (a) the fab time of each, (b) the total delay and cost of each, and (c) what the ECO saves.

### Problem 26-05.8 [B]

**A smaller register.** Risks (probability, impact in $ M): R1 (0.3, 12), R2 (0.1, 50), R3 (0.4, 4). Mitigations (cost, probability after): R1 ($1.5 M, 0.1), R2 ($2.5 M, 0.04), R3 ($0.5 M, 0.2). Find (a) the EMV, (b) each mitigation's net benefit, and (c) the best set with a $3 M budget and with a $4.5 M budget.

### Problem 26-05.9 [C]

**Correlated risks.** Two risks each have probability 0.2 and impact $10 M. (a) Find the EMV. (b) Find the probability of losing $20 M, and the standard deviation of the loss, if the risks are independent. (c) Repeat if they always occur together. (d) What does EMV miss?

### Problem 26-05.10 [C]

**How much timing margin?** Silicon maximum frequency is normally distributed around the design target with a standard deviation of 4% (model error). The specification is set a margin $\Delta$ (in %) below the target. Each 1% of margin costs $0.5 M (area and power across the product's life), and missing the specification forces a $40 M respin. (a) Find the miss probability and the total expected cost for $\Delta$ = 0, 4% and 8%. (b) Derive the optimal margin and find it, its miss probability and its expected cost.

### Problem 26-05.11 [C]

**When to tape out, another program.** $N_0$ = 60 remaining bugs, $\tau$ = 5 weeks, $\phi$ = 0.2, a respin costs $30 M and a week of verification $1 M. Find (a) $k$ and $\lambda^*$, (b) the optimal verification time, (c) the respin probability and expected cost there, and (d) the expected cost of taping out at once.

### Problem 26-05.12 [C]

**Formal verification instead of emulation.** In Example 26-05.5, formal verification of the cache-coherence protocol costs $2 M and exhaustively checks the protocol, so that half of the respin-class bugs are found and fixed before final verification (so $\phi N_0$ falls from 10 to 5), without changing $\tau$. Find (a) the new optimal time and respin probability, (b) the expected cost including the formal work, and (c) explain why the respin probability at the optimum does not change while the optimal time does.

### Problem 26-05.13 [A]

**Reading the survey.** A headline says "Only 5% of chips work the first time". Give three reasons why this does not mean that 95% of chip programs fail or that first silicon is usually unusable.

### Problem 26-05.14 [B]

**Find the critical path.** A block's tasks (duration in weeks, predecessors): A, specification (4, none); B, RTL (10, A); C, verification environment (6, A); D, verification (8, B and C); E, physical design (7, B); F, signoff (3, D and E). (a) Do a forward pass (earliest start and finish) and find the project duration. (b) Do a backward pass, find each task's total float, and name the critical path. (c) Physical design slips by 2 weeks. By how much does the project slip? (d) Which single tasks could be shortened by 2 weeks to bring the project to 23 weeks, and why does shortening verification alone not do it?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Schedules, three-point estimates and merge bias | 1, 3, 4, 14 |
| 2. Expected tape-outs and survey statistics | 5, 6, 13 |
| 3. Respin causes and fixes | 2, 7 |
| 4. Risk registers and EMV | 8, 9, 10 |
| 5. When to tape out and the value of mitigation | 11, 12 |
