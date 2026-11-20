<!-- status: reviewed -->
# 14-06 · Pipelining and Hazards

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The pipelining sections of a computer organization course: the five-stage pipeline, pipeline registers, data hazards and forwarding, load-use stalls, control hazards and flushing, and pipeline performance (Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, §§4.5–4.9; Harris & Harris, *Digital Design and Computer Architecture*, RISC-V Edition, §7.5) |
| **Prerequisites** | [14-05 Single-Cycle Datapath and Control](14-05-single-cycle-datapath.md), [14-01 Performance, Power and the Iron Law](14-01-performance-power-iron-law.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain how pipelining raises throughput without shortening any instruction, and compute pipelined cycle counts, clock periods and speedups, including fill time and register overhead.
2. Describe the five-stage RISC-V pipeline: what each stage does and what each pipeline register carries.
3. Detect data hazards, specify the forwarding paths and their priority, and identify when a load-use stall is unavoidable.
4. Explain control hazards, flushing and the branch penalty, and evaluate alternatives (earlier resolution, prediction).
5. Predict a program's cycle count from its hazards, $N + (k - 1) + S + 2T$, and confirm it on a pipelined Verilog core.

---

## 1. Big picture

The single-cycle machine of [14-05](14-05-single-cycle-datapath.md) uses each piece of hardware for a fraction of every long cycle. **Pipelining** puts it all to work at once. The datapath is cut into stages separated by registers, and a new instruction starts every cycle while earlier ones move through the later stages. No instruction finishes faster (it actually takes slightly longer), but one *finishes every cycle*, at a clock set by the slowest stage rather than the slowest instruction. Every processor sold today, from the smallest microcontroller to the largest server core, is pipelined.

- **Throughput, not latency.** Pipelining is the same trick as a factory assembly line or a laundry with separate washer and dryer: overlap the steps of successive jobs.
- **Hazards are the price.** Instructions depend on each other. A result is needed before it has been written back, and a branch decides what to fetch after the next instructions are already fetched. Handling these *hazards* is most of the design work.
- **CPI drifts above 1.** Stalls and flushed instructions add cycles: CPI = 1 + (stall and flush cycles per instruction). Branches cost the most, which is why the next chapter is about predicting them.
- **Depth is a trade-off.** More stages give a faster clock but more register overhead, larger hazard penalties and more power, so commercial pipeline depths settled in a middle range.

## 2. Intuition first

**The laundry.** Washing, drying and folding a load takes three hours if done one load at a time with one person doing everything. With a washer, a dryer and a folding table used at the same time on successive loads, a new load finishes every hour once the pipeline is full. Each load still takes three hours from start to finish. The throughput tripled; the latency did not improve.

**Why the slowest step sets the pace.** If the dryer takes 80 minutes and the washer 40, every step must wait for the dryer: the line runs at one load per 80 minutes. Balancing the stages matters as much as their number. Every handoff also costs a little time, like carrying the basket to the next machine; in a processor, that is the pipeline register's clock-to-Q and setup time.

**Hazards in the laundry.** Suppose load 2 can only be washed with the detergent left over after load 1 is *dried and checked*. Load 2 must wait: a **data hazard**. If the checker can hand the detergent straight back to the washer as soon as it is known, before load 1 reaches the folding table, the wait shrinks or disappears: **forwarding**. Now suppose load 1's result decides which basket to wash next, but load 2 was already started from the default basket. It must be thrown out and restarted: a **control hazard**.

**Where the analogy breaks.** Laundry loads rarely depend on each other; instructions do all the time, typically on a result produced one or two instructions earlier. And unlike a laundry, a processor cannot pause to ask: every hazard must be detected and resolved by hardware within a single clock cycle.

## 3. Theory

### 3.1 The pipelining principle

Cut a single-cycle datapath whose total logic delay is $t_{\text{logic}}$ into $k$ stages, separated by **pipeline registers** that each add an overhead $t_{\text{reg}} = t_{\text{clk-q}} + t_{\text{setup}}$. If the stages are perfectly balanced, the clock period becomes

$$
T_{\text{pipe}} = \frac{t_{\text{logic}}}{k} + t_{\text{reg}} ,
$$

and in general it is set by the slowest stage, $T_{\text{pipe}} = \max_i t_{\text{stage},i} + t_{\text{reg}}$. A sequence of $N$ instructions, with no hazards, takes $k - 1$ cycles to fill the pipeline and then completes one instruction per cycle:

$$
\text{cycles} = N + (k - 1), \qquad \text{speedup} = \frac{N\,T_{\text{single}}}{\big(N + k - 1\big)\,T_{\text{pipe}}} \;\xrightarrow{N \to \infty}\; \frac{T_{\text{single}}}{T_{\text{pipe}}} .
$$

Three things keep the speedup below $k$:

1. **Unbalanced stages.** The slowest stage sets the clock.
2. **Register overhead.** It is paid in every stage.
3. **Hazards.** They add cycles.

**Latency** (the time for one instruction to pass through) grows from $T_{\text{single}}$ to $k\,T_{\text{pipe}}$, which is always at least as long.

### 3.2 The five-stage RISC-V pipeline

The classic RISC pipeline cuts the 14-05 datapath at its natural seams:

| Stage | Work | Pipeline register written at the end |
|---|---|---|
| **IF** (fetch) | read the instruction memory at PC; PC ← PC + 4 (or a redirect) | IF/ID: instruction, PC |
| **ID** (decode) | decode; read rs1 and rs2; generate the immediate | ID/EX: register values, immediate, register numbers, control signals |
| **EX** (execute) | ALU; branch comparison and target; JALR target | EX/MEM: ALU result, store data, rd, control |
| **MEM** (memory) | read or write the data memory | MEM/WB: result (ALU, memory or PC + 4), rd, control |
| **WB** (write back) | write rd in the register file | — |

Two design points make it work.

- **Control travels with the instruction.** The decoder runs once, in ID, and its signals ride along in the pipeline registers, so that each stage applies the right instruction's control. An instruction's RegWrite is used three stages after decoding, in WB.
- **The register file is written early and read late within a cycle.** In the lab's core, a write in WB is passed straight through to a read of the same register in ID during the same cycle ("write-before-read"). An instruction three behind its producer therefore needs no special help.

**Stage delays.** With 14-05's illustrative delays, each stage is $t_{\text{clk-q}}$ (40 ps) plus its logic plus $t_{\text{setup}}$ (20 ps):

- IF: instruction-memory read 200, so 260 ps in all. The PC register drives the memory directly. The next-PC multiplexer sits in front of the PC register, and its slowest input comes from EX (below).
- ID: register read 100 + write-through multiplexer 25, so 185 ps.
- EX: two paths. The ALU path is forwarding multiplexer 25 + ALU-input multiplexer 25 + ALU 120, so 230 ps. The redirect path carries a JALR target from the ALU through the next-PC multiplexer (25) into the PC register, so 255 ps.
- MEM: memory 200 + result multiplexer 25, so 285 ps.

The clock is set by the data-memory stage, MEM, at 285 ps (Example 14-06.2): 2.56 times faster than the single-cycle 730 ps, not 5 times, because the memory stage dominates and every stage pays 60 ps of register overhead.

### 3.3 Data hazards and forwarding

A **read-after-write (RAW) dependence** exists when an instruction reads a register that an earlier instruction writes. In the pipeline the value is computed in EX and written in WB, two cycles later, but the next instruction wants it in its own EX, one cycle after the producer's. Without help it would read a stale value from the register file. The cure is **forwarding** (also called *bypassing*): route the result from the pipeline register where it already sits straight to the ALU input that needs it.

Two forwarding paths cover every distance an ALU result needs:

- **From EX/MEM** (producer one instruction ahead): the previous instruction's ALU result, or its PC + 4 for JAL and JALR.
- **From MEM/WB** (producer two instructions ahead): the result about to be written back, whether from the ALU, the memory or PC + 4.

Producers three or more ahead are covered by the register file's write-before-read. The forwarding multiplexer for rs1 in EX selects

$$
\text{A} = \begin{cases} \text{EX/MEM result} & \text{if EX/MEM writes } rd = rs_1 \ne 0, \\ \text{MEM/WB result} & \text{else if MEM/WB writes } rd = rs_1 \ne 0, \\ \text{register value from ID/EX} & \text{otherwise,} \end{cases}
$$

and likewise for rs2, the branch comparator and the store data. Three details matter:

- **x0 is never forwarded.** An instruction "writing" x0 does not change it.
- **The newest producer wins.** If both stages write the same register, EX/MEM holds the more recent value (Problem 14-06.5).
- **Only real operands count.** An I-type instruction's "rs2" field is part of its immediate, so the decoder supplies *uses-rs1* and *uses-rs2* signals, and forwarding and stalling consult them.

**The load-use hazard.** A load's data is available only at the end of MEM. An instruction immediately after it needs the value at the start of its EX, which is the same moment. No forwarding path can deliver data backward in time, so the hazard unit **stalls**:

1. It freezes the PC and the IF/ID register for one cycle.
2. It inserts a **bubble** (a no-op) into EX.
3. Next cycle the load's data is in MEM/WB and is forwarded normally.

The stall costs one cycle per load immediately followed by a user of its result. Compilers avoid it by **scheduling**: they move an independent instruction between the load and its use (Example 14-06.4).

### 3.4 Control hazards

A branch's outcome and target are known only in EX. By then the pipeline has already fetched the next two instructions from PC + 4 and PC + 8. The lab's core uses the simplest policy, **predict not taken**: keep fetching sequentially; if the branch turns out to be taken (and for every JAL and JALR, which always jump), **flush** the two wrong-path instructions by turning them into bubbles and redirect the PC to the target. Each taken branch or jump therefore costs **two cycles**. Flushed instructions have not yet written anything, since no register or memory is written before MEM, so discarding them is safe.

![Pipeline diagram over twelve clock cycles: lw passes IF, ID, EX, MEM, WB in cycles 1 to 5; add is fetched in cycle 2, is held in ID during cycle 4 (stall) and executes in cycle 5; beq is held in IF during cycle 4 and resolves in EX in cycle 6; the wrong-path sub and or, fetched in cycles 5 and 6, are shown crossed out; the target xor is fetched in cycle 7 and the final ebreak completes WB in cycle 12.](../../../assets/figures/14-06/pipeline.svg)

*Figure 1. A load-use stall and a taken branch. The stall delays the add and everything behind it by one cycle; the taken branch, resolved in EX, flushes two wrong-path instructions. Five useful instructions finish in $5 + 4 + 1 + 2 = 12$ cycles, the model of §3.5. The verify script runs this sequence on the lab's Verilog core.*

Ways to reduce the penalty:

- **Resolve earlier.** Comparing registers and computing the target in ID cuts the penalty to one cycle, at the cost of a comparator and forwarding paths into ID, which lengthens that stage. It also creates new data hazards: a branch that tests an ALU result from the instruction just before it must stall one cycle (the result exists only at the end of EX), and one that tests a just-loaded value must stall two (Problem 14-06.12).
- **Delayed branches.** Older ISAs such as MIPS defined that the instruction after a branch *always* executes, so the compiler could fill that "delay slot". The rule bakes one pipeline's timing into the ISA forever, and RISC-V deliberately omits it.
- **Predict.** Guess the outcome and target in IF from history, so that most taken branches cost nothing. This is the subject of [14-07](14-07-branch-prediction-and-speculation.md), and the reason modern cores can have deep pipelines.

### 3.5 Pipeline performance

Counting cycles for a program of $N$ instructions on a $k$-stage pipeline with $S$ load-use stalls and $T$ taken branches and jumps, each costing a penalty of $P$ cycles:

$$
\text{cycles} = N + (k - 1) + S + P\,T, \qquad \text{CPI} = \frac{\text{cycles}}{N} \approx 1 + \frac{S + P\,T}{N} .
$$

The lab's core has $k = 5$ and $P = 2$. The lab's program (the array sum and recursive `fib(10)` of Lab 14-05) executes $N$ = 1924 instructions, including the final EBREAK, which must reach WB. It has $S$ = 10 load-use stalls and $T$ = 456 taken branches and jumps, so the formula predicts $1924 + 4 + 10 + 912 = 2850$ cycles. The Verilog core takes exactly 2850 (Example 14-06.6). The control-hazard term dominates: this recursive program jumps a lot.

### 3.6 Structural hazards and the limits of depth

A **structural hazard** occurs when two instructions need the same hardware in the same cycle.

- **Memory.** A single memory port shared by IF and MEM would block fetch on every load and store; this is why pipelines need separate instruction and data paths (split L1 caches, 14-09).
- **Register file ports.** One instruction per cycle needs two read ports and one write port.
- **Unpipelined units.** An iterative divider occupying EX for 20 cycles stalls everything behind it (Problem 14-06.9).

**How deep?** More stages shorten $t_{\text{logic}}/k$, but the register overhead $t_{\text{reg}}$ stays, and the branch penalty grows roughly with the number of stages before branch resolution. The time per instruction is then roughly

$$
t(k) = \Big(\frac{t_{\text{logic}}}{k} + t_{\text{reg}}\Big)\big(1 + c\,k\big),
$$

where $c$ captures the hazard cost per extra stage. It has a minimum at

$$
k^{*} = \sqrt{\frac{t_{\text{logic}}}{c\,t_{\text{reg}}}} ,
$$

derived by setting $dt/dk = 0$ (Problem 14-06.11). Deeper pipelines also burn more power in their registers and clock network. Commercial designs went through a period of very deep pipelines chasing clock frequency before power limits (14-01) pushed them back to moderate depths.

## 4. Worked examples

All cycle counts in these examples are confirmed on the lab's pipelined Verilog core, which also matches the course's Python simulator register write for register write.

### Example 14-06.1 · Fill time and speedup (tier A)

**Setup.** A program of $N$ = 100 instructions runs without hazards on the five-stage pipeline (285 ps clock) and on the single-cycle machine (730 ps). Find the pipelined cycle count, both execution times, and the speedup. What is the limit as $N$ grows?

**Solution.** Cycles = $100 + 4$ = **104**. Times: $104 \times 285$ ps = **29.64** ns pipelined, against $100 \times 730$ ps = 73.0 ns single-cycle, a speedup of 73.0/29.64 = **2.463**. As $N \to \infty$ the fill time vanishes and the speedup tends to $730/285$ = **2.561**.

**Units check.** Cycles × ps = ps.

**Sanity check.** Five stages, but a speedup of only 2.6: the IF and MEM stages each hold a 200 ps memory, and every stage carries 60 ps of overhead.

### Example 14-06.2 · Stage delays and the clock (tier B)

**Setup.** Using 14-05's delays (clock-to-Q 40 ps, setup 20 ps, memories 200 ps, register read 100 ps, multiplexers 25 ps, ALU 120 ps), find each stage's delay, the clock period and frequency, and one instruction's latency.

**Solution.** From §3.2:

- IF: $40 + 200 + 20$ = **260** ps.
- ID: $40 + 100 + 25 + 20$ = **185** ps.
- EX: the ALU path is $40 + 25 + 25 + 120 + 20$ = 230 ps, and the redirect path adds the next-PC multiplexer: $230 + 25$ = **255** ps.
- MEM: $40 + 200 + 25 + 20$ = **285** ps.

The clock period is the maximum, **285** ps, so $f$ = **3.509** GHz. One instruction's latency is $5 \times 285$ = **1425** ps, almost twice the single-cycle 730 ps.

**Units check.** All stage delays in ps; $1/285$ ps = 3.509 GHz.

**Sanity check.** Latency got worse while throughput got 2.6 times better: the defining trade of pipelining.

### Example 14-06.3 · Forwarding paths (tier A)

**Setup.** Which forwarding paths, if any, does each instruction use in this sequence, and how many cycles does it take (with the closing EBREAK, starting from an empty pipeline)?

```asm
_start:
    li   x6, 3
    li   x7, 4
    li   x9, 1
    add  x5, x6, x7
    sub  x8, x5, x9
    or   x10, x5, x8
    ebreak
```

**Solution.**

- `add` reads x7 from **MEM/WB** (`li x7` is two ahead; the instruction just ahead, in EX/MEM, is `li x9`). It reads x6 from the register file: `li x6` wrote back while `add` was in ID, and write-before-read passed it through.
- `sub` reads x5 from **EX/MEM**, and x9 from MEM/WB.
- `or` reads x5 from **MEM/WB** (two ahead) and x8 from **EX/MEM** (one ahead).

There are no loads and no branches, so **0** stalls, and the 7 instructions take $7 + 4$ = **11** cycles.

**Units check.** Cycles count clock periods.

**Sanity check.** The example shows all three ways an operand can arrive: from EX/MEM (one ahead), from MEM/WB (two ahead) and from the register file (three or more ahead). Every dependence is on an ALU result, so forwarding covers it without a stall.

### Example 14-06.4 · A load-use stall and how to schedule it away (tier B)

**Setup.** Count the cycles for each sequence (memory word at 0x2000 = 42):

```asm
_start:                      # (a)
    li   x10, 0x2000
    li   x7, 5
    lw   x5, 0(x10)
    add  x6, x5, x7
    ebreak
```

```asm
_start:                      # (b) the same work, reordered
    li   x10, 0x2000
    lw   x5, 0(x10)
    li   x7, 5
    add  x6, x5, x7
    ebreak
```

**Solution.** (a) `add` uses x5 immediately after the load: **1** load-use stall, so $5 + 4 + 1$ = **10** cycles. (b) The independent `li x7, 5` now sits between the load and its use; by the time `add` reaches EX, the loaded value is in MEM/WB and is forwarded. That is **0** stalls and **9** cycles. Both compute x6 = 47.

**Units check.** One stall adds one cycle.

**Sanity check.** Reordering changed no result, only the timing: a compiler with knowledge of the pipeline does this routinely.

### Example 14-06.5 · What a loop costs per element (tier B)

**Setup.** Using the cycle model of §3.5, find the cycles per array element for three versions of the array-sum loop: (a) the top-tested loop of Lab 14-02; (b) the rotated loop of Problem 14-02.9; (c) the rotated loop with the load moved away from its use:

```asm
sum:
    addi t0, zero, 0
    beq  a1, zero, 2f
1:  lw   t1, 0(a0)
    addi a0, a0, 4
    addi a1, a1, -1
    add  t0, t0, t1
    bne  a1, zero, 1b
2:  addi a0, t0, 0
    jalr zero, 0(ra)
```

**Solution.** Per element:

- **(a)** Six instructions (`beq` not taken, `lw`, `add`, two `addi`, `jal`), plus one load-use stall (`add` right after `lw`), plus two flush cycles for the taken `jal`: $6 + 1 + 2$ = **9**.
- **(b)** Five instructions, one stall, and two flush cycles for the taken `bne`: $5 + 1 + 2$ = **8**.
- **(c)** Five instructions, no stall, two flush cycles: **7**.

The Verilog core confirms each figure, measured as the difference between runs with 10 and 11 elements. With perfect branch prediction (c) would take 5.

**Units check.** Cycles per element.

**Sanity check.** Of the 7 cycles in (c), 2 are spent flushing wrong-path instructions: 29% of the time. Branch prediction exists to recover it.

### Example 14-06.6 · The whole program on the pipelined core (tier C)

**Setup.** The lab's program executes 1924 instructions, including the final EBREAK. It has 10 load-use stalls and 456 taken branches and jumps. Predict its cycles, CPI and run time at 285 ps, and its speedup over the single-cycle core (1923 cycles at 730 ps). How many cycles would perfect branch prediction save?

**Solution.**

- **Cycles:** $1924 + 4 + 10 + 2 \times 456$ = **2850**.
- **CPI:** 2850/1924 = **1.481**.
- **Run time:** $2850 \times 285$ ps = **812.25** ns.
- **Speedup:** the single-cycle core takes $1923 \times 730$ ps = 1403.79 ns, so 1403.79/812.25 = **1.728**.

With no branch penalty the count would be $1924 + 4 + 10$ = **1938** cycles. That is 912 fewer, raising the speedup to **2.542**. The testbench measures exactly 2850 cycles, 10 stalls and 456 flushes.

**Units check.** Cycles × 285 ps = ps.

**Sanity check.** The program's taken-jump rate is high (456 of 1924 instructions, 24%) because recursion and short loops branch constantly. In typical code the rate is lower, but the lesson holds: without prediction, control hazards eat most of a pipeline's gain.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-06.1a | pipelined cycles | 104 | — |
| Ex 14-06.1b | pipelined time | 29.64 | ns |
| Ex 14-06.1c | speedup for N = 100 | 2.463 | — |
| Ex 14-06.1d | limiting speedup | 2.561 | — |
| Ex 14-06.2a | IF stage | 260 | ps |
| Ex 14-06.2b | ID stage | 185 | ps |
| Ex 14-06.2c | EX stage (redirect path) | 255 | ps |
| Ex 14-06.2h | EX ALU path | 230 | ps |
| Ex 14-06.2d | MEM stage | 285 | ps |
| Ex 14-06.2e | clock period | 285 | ps |
| Ex 14-06.2f | clock frequency | 3.509 | GHz |
| Ex 14-06.2g | latency of one instruction | 1425 | ps |
| Ex 14-06.3a | stalls | 0 | — |
| Ex 14-06.3b | cycles | 11 | — |
| Ex 14-06.4a | stalls in (a) | 1 | — |
| Ex 14-06.4b | cycles for (a) | 10 | — |
| Ex 14-06.4c | stalls in (b) | 0 | — |
| Ex 14-06.4d | cycles for (b) | 9 | — |
| Ex 14-06.5a | cycles per element, top-tested | 9 | — |
| Ex 14-06.5b | cycles per element, rotated | 8 | — |
| Ex 14-06.5c | cycles per element, scheduled | 7 | — |
| Ex 14-06.6a | cycles | 2850 | — |
| Ex 14-06.6b | CPI | 1.481 | — |
| Ex 14-06.6c | run time | 812.25 | ns |
| Ex 14-06.6d | speedup over single-cycle | 1.728 | — |
| Ex 14-06.6e | cycles with perfect prediction | 1938 | — |
| Ex 14-06.6f | speedup with perfect prediction | 2.542 | — |

## 5. Simulate it

The lab, [labs/14-06-lab](../labs/14-06-lab/README.md), is a five-stage pipelined RV32I core in Verilog, built from 14-05's modules plus pipeline registers, a forwarding unit and a hazard unit:

1. **Run the program** of Lab 14-05 and read the testbench's report: cycles, CPI, stalls and flushes, all checked against the model of §3.5.
2. **Check correctness** by comparing the register-write trace with the Python simulator's (identical to the single-cycle core's).
3. **Micro-programs (notebook):** run the sequences of Examples 14-06.3 to 14-06.5 and watch stalls and flushes appear and disappear.
4. **Break it:** disable a forwarding path or the load-use stall and see which instruction first goes wrong.

**Guided exercise (predict, then run).** **Before running the testbench,** predict its cycle count from $N + 4 + S + 2T$ with $N$ = 1924, $S$ = 10 and $T$ = 456. (2850 cycles, CPI 1.481. If your prediction is off, find which term you miscounted.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| More pipeline stages | Clock frequency | Register overhead, branch and load penalties, power, verification effort | CPU architect |
| Forwarding paths | Removes most data stalls | Multiplexers on the critical EX path; wiring | CPU designer |
| Branch resolution in ID instead of EX | Penalty 1 instead of 2 cycles | A comparator and forwarding into ID; longer ID stage; new stalls when a branch tests a result from just before it (1 cycle after an ALU op, 2 after a load) | CPU designer |
| Branch prediction (14-07) | Removes most control stalls | Predictor tables, recovery logic | CPU architect |
| Compiler scheduling | Removes load-use and other stalls for free | Compiler complexity; code tuned to one pipeline | Compiler team |
| Stage balancing (splitting memory access) | Clock frequency | More stages and penalties | CPU architect, physical designer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Cycles for $N$ instructions on a $k$-stage pipeline | $N + (k - 1)$ + stalls + flush penalties | §3.5 |
| Load-use stall in the five-stage pipeline | 1 cycle | even with forwarding |
| Taken-branch penalty, resolved in EX | 2 cycles | 1 if resolved in ID |
| Forwarding paths into EX | 2 (from EX/MEM and MEM/WB) | plus register-file write-through |
| Example clock period | 285 ps (3.51 GHz) against 730 ps single-cycle | illustrative delays |
| Optimal depth (simple model) | $k^* = \sqrt{t_{\text{logic}}/(c\,t_{\text{reg}})}$ | §3.6 |

## 8. Common mistakes

- **Thinking pipelining makes instructions faster.** It makes each one slower; it makes more of them finish per second.
- **Forwarding from the wrong stage first.** The most recent producer (EX/MEM) must take priority over the older one (MEM/WB).
- **Forwarding into x0** or stalling on a register field that is really an immediate. Check rd ≠ 0 and the uses-rs signals.
- **Forgetting that JAL and JALR always jump.** In a predict-not-taken pipeline each costs the full flush penalty.
- **Letting a flushed instruction have side effects.** Nothing may write registers or memory before its instruction is known to be on the correct path.
- **Ignoring fill time for short sequences.** For a 10-instruction function, $k - 1 = 4$ extra cycles are 40%.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Pipelines in products.** Small microcontroller cores use two- to five-stage pipelines; high-performance cores use pipelines of well over ten stages from fetch to retirement, combined with branch prediction, out-of-order execution and multiple issue (14-07, 14-08). AMD's Zen 5, for example, dispatches and retires up to eight instructions per cycle [1, R-212] **[Established]** (vendor disclosure). Exact pipeline depths are rarely published as a single number, because modern pipelines have variable-length paths.
- **Why depth stopped growing.** The clock-frequency race of the early 2000s ended at the power limit (14-01 and its sources); designs then traded depth for width and efficiency **[Established]**.

### Why it matters commercially

- **Clock frequency is a pipeline property.** A core's maximum frequency comes from its slowest stage, and stage design is a joint decision of architects and physical designers. Comparing GHz between different pipelines says little.
- **Branchy code runs slower than its instruction count suggests.** Interpreters, databases and control-heavy firmware stress the front end; streaming numeric code stresses the back end. Benchmarks should match the target workload (14-15).

### Marketing vs Reality

- **"Executes one instruction per cycle."** *Reality:* an ideal pipeline does; real code adds stalls and flushes. The lab's program, on a perfectly working five-stage core, runs at CPI 1.48. *Sanity check:* ask for measured CPI or IPC on the customer's code, not peak issue rate.
- **"Deeper pipeline, higher frequency, faster chip."** *Reality:* each extra stage raises the cost of every mispredicted branch and every load miss. *Sanity check:* compare performance per clock and performance per watt on real workloads, not frequency.

### Questions for engineering leaders

1. **"What is your branch-misprediction penalty and your load-to-use latency, in cycles?"**
   *Strong:* specific numbers for both, and how they compare with competitors. *Evasive:* "industry-leading".
2. **"Where is your critical path, and how did you balance the stages?"**
   *Strong:* a named stage and path, and the trade made (for example, splitting cache access over two stages). *Evasive:* "we hit our frequency target".
3. **"What CPI do you measure on our workload, and how much of the loss is front end against back end?"**
   *Strong:* a top-down breakdown from performance counters. *Evasive:* a peak-IPC figure.
4. **"How do you verify the pipeline against the ISA?"**
   *Strong:* lock-step comparison with a reference model under random and directed tests, with coverage of hazard combinations. *Evasive:* "we boot Linux".

## 10. Concept check

**Q1.** Why does pipelining increase throughput but not reduce latency?

<details><summary>Answer</summary>

Each instruction still passes through every stage, now with register overhead added and at the pace of the slowest stage, so its own latency grows. But a new instruction starts every cycle, so instructions complete at one per (shorter) cycle.

</details>

**Q2.** Which two forwarding paths does the five-stage pipeline need, and why is no third path needed for a producer three instructions earlier?

<details><summary>Answer</summary>

From EX/MEM (producer one ahead) and from MEM/WB (producer two ahead). A producer three ahead is in WB while the consumer is in ID, and the register file's write-before-read passes the value straight to the read port.

</details>

**Q3.** Why can forwarding not remove the load-use stall?

<details><summary>Answer</summary>

The load's data exists only at the end of its MEM stage, which is the same moment the next instruction needs it at the start of EX. Forwarding can move data sideways in time, not backward, so one cycle must be inserted.

</details>

**Q4.** What happens to the two instructions fetched after a taken branch, and why is that safe?

<details><summary>Answer</summary>

They are flushed: turned into bubbles before they reach MEM. No instruction writes registers or memory before MEM and WB, so they have changed nothing.

</details>

**Q5.** Why must forwarding check the uses-rs signals, not just the register numbers?

<details><summary>Answer</summary>

Instructions that do not read a register still have bits in that field. For example, an `addi`'s "rs2" field is part of its immediate. Matching on those bits would forward into an unused input harmlessly, but stalling on them would waste cycles.

</details>

**Q6.** Why does a deeper pipeline not keep getting faster?

<details><summary>Answer</summary>

Each stage adds fixed register overhead, so the clock period stops shrinking, while hazard penalties (branch misprediction, load-use) grow with the number of stages. There is an optimum depth, and power rises with depth too.

</details>

Now work the [problem set](../problems/14-06-problems.md).

## 11. Key terms

[Pipelining](../../../reference/glossary.md#pipelining) · [Pipeline register](../../../reference/glossary.md#pipeline-register) · [Pipeline hazard](../../../reference/glossary.md#pipeline-hazard) · [Data hazard](../../../reference/glossary.md#data-hazard) · [Forwarding (bypassing)](../../../reference/glossary.md#forwarding-bypassing) · [Load-use hazard](../../../reference/glossary.md#load-use-hazard) · [Stall](../../../reference/glossary.md#stall) · [Bubble](../../../reference/glossary.md#bubble) · [Control hazard](../../../reference/glossary.md#control-hazard) · [Flush](../../../reference/glossary.md#flush) · [Branch penalty](../../../reference/glossary.md#branch-penalty) · [Structural hazard](../../../reference/glossary.md#structural-hazard)

## 12. Connections

- **Builds on:** the single-cycle datapath ([14-05](14-05-single-cycle-datapath.md)); the iron law ([14-01](14-01-performance-power-iron-law.md)); loops and calls in assembly ([14-03](14-03-assembly-and-the-compilation-stack.md)); flip-flop timing ([08-10](../../08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md)).
- **Next:** [14-07 Branch Prediction and Speculation](14-07-branch-prediction-and-speculation.md), which attacks the dominant hazard of Example 14-06.6.
- **Used later:** out-of-order execution generalizes forwarding and stalling ([14-08](14-08-out-of-order-and-superscalar.md)); cache misses as long stalls ([14-09](14-09-memory-hierarchy-and-caches.md)); pipelining in digital design and DSP datapaths ([Course 19](../../19-digital-vlsi-design/README.md)).

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, §§4.5–4.9.
- S. L. Harris and D. M. Harris, *Digital Design and Computer Architecture*, RISC-V Edition, §7.5 (with HDL).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, appendix C (pipelining basics).
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on pipelined processors.

## 14. Sources

1. AMD, "Zen 5" core architecture disclosure, Hot Chips 2024 (dispatch and retire width). [R-212](../../../reference/research-log.md#r-212--amd-zen-5-core-hot-chips-2024)

The pipeline organization, hazard handling and performance model are textbook material (Further study). The stage delays are the illustrative delays of 14-05. The Verilog core and its measured cycle counts are this course's own and are re-run by the verify script and by CI.
