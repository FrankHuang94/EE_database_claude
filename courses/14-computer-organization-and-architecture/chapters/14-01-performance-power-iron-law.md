<!-- status: verified -->
# 14-01 · Performance, Power and the Iron Law

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The performance chapter of a computer organization course: execution time, CPI and the iron law, Amdahl's law, benchmarks and their means, and power and energy (Patterson & Hennessy, *Computer Organization and Design*, ch. 1; Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 1) |
| **Prerequisites** | [09-11 CMOS and Scaling](../../09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md), [07-02 First-Order RC and RL Transients](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md), [08-09 Arithmetic Circuits](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Compute execution time from instruction count, CPI and clock rate (the iron law), and CPI from an instruction mix.
2. Apply Amdahl's and Gustafson's laws to predict the speedup of an enhancement or of parallel execution.
3. Choose the right mean (arithmetic, harmonic or geometric) to summarize benchmark results, and explain why a wrong one misleads.
4. Compute dynamic and leakage power and energy per task, and predict how voltage and frequency scaling change them.
5. Compare designs by performance per watt, energy per task and the energy-delay products, and evaluate a vendor's performance and efficiency claims.

---

## 1. Big picture

A processor is judged by one number above all others: how long it takes to do the work you care about, and, increasingly, how much energy it spends doing it. Everything in this course (instruction sets, pipelines, caches, multicore, GPUs, accelerators) is a way to shorten that time or cut that energy, and every design decision trades one against the other and against area, which is cost. This chapter builds the measuring stick. The **iron law** splits execution time into three factors owned by different people (the compiler writer, the microarchitect and the circuit designer); **Amdahl's law** says how much any one improvement can help; the right **mean** turns many benchmark results into a fair summary; and the physics of **dynamic and leakage power** explains why clock rates stopped rising and why performance per watt is now the figure of merit.

- **Product claims** ("2× faster", "40% better performance per watt") are statements about these quantities, usually measured under conditions chosen by the vendor.
- **Datacenter economics** are set by performance per watt: power and cooling, not chip price alone, dominate the cost of running a server for years.
- **Battery life** in phones, wearables and IoT devices is energy per task, not power.
- **Parallel hardware** (multicore, GPUs, accelerators) is limited by the part of the work that does not parallelize, which Amdahl's law quantifies.

## 2. Intuition first

**Time is the only honest measure.** A faster clock, more instructions per cycle or more cores all sound like performance, but each can be traded away by another factor. A program runs faster only if it finishes sooner. Rates (instructions per second, operations per second) are useful only when the work being counted is the same.

**Three knobs multiply.** To run a program you must execute some number of instructions; each instruction takes some number of clock cycles on average; each cycle takes some time. Execution time is the product. Halving one factor while doubling another gains nothing, and the three factors are coupled: a simpler instruction set may need more instructions but fewer cycles each, and a deeper pipeline allows a faster clock but loses more cycles on each mispredicted branch.

**An analogy from finance, and its limits.** The iron law is a DuPont decomposition. Return on equity splits into margin × asset turnover × leverage, so an analyst can see which lever moved; execution time splits into instructions × cycles per instruction × seconds per cycle, so an architect can see which design choice helped. The analogy holds in that each factor has an owner and that the factors trade off. It breaks where the decomposition is causal: cycles per instruction is not an independent input but an outcome of the instruction mix, the memory system and the clock rate itself (a faster clock makes each memory access cost more cycles), whereas a margin is not changed by the asset base in the same mechanical way.

**The serial part dominates.** If a tenth of a job cannot be sped up, no amount of hardware makes the whole job more than ten times faster: the unimproved part ends up taking all the time. This is Amdahl's law, and it is why architects attack the common case and why "100× faster" claims usually apply to a kernel, not to the application.

**Power is charge moved times voltage, many times a second.** Every logic transition charges or discharges a capacitance, drawing energy $CV^2$ from the supply per charge-discharge cycle (07-02, 09-11). Do it $f$ times a second on a fraction α of the nodes and the power is $\alpha CV^2f$. Because a faster clock needs a higher voltage, power rises much faster than frequency: roughly as its cube near the top of the range. That one fact ended the clock-rate race and pushed the industry to multicore.

## 3. Theory

### 3.1 Performance and speedup

The **execution time** $T$ of a program is the wall-clock time from start to finish; **performance** is its reciprocal, $1/T$. For a fixed workload, machine A is $n$ times faster than B when

$$
n = \frac{\text{Performance}_A}{\text{Performance}_B} = \frac{T_B}{T_A} .
$$

The **speedup** of an improvement is the same ratio, $S = T_{old}/T_{new}$. "30% faster" means $S$ = 1.3, so the new time is $1/1.3$ = 77% of the old, not 70%: a common slip.

Two kinds of performance matter. **Latency** (response time) is the time for one task; **throughput** (bandwidth) is tasks completed per unit time. Adding a second server doubles throughput without shortening any single request; a faster processor usually improves both. Most of this chapter is about latency of a single program; Chapters 14-12 to 14-15 return to throughput.

### 3.2 The iron law

A program executes $\text{IC}$ instructions (the **instruction count**, dynamic, as executed, not as written). Each instruction occupies the processor for some number of clock cycles; the average is the **cycles per instruction**, CPI. Each cycle lasts the **clock period** $T_c = 1/f$. The total cycle count is $\text{IC} \times \text{CPI}$ by the definition of the average, and multiplying by the period gives

$$
T = \text{IC} \times \text{CPI} \times T_c = \frac{\text{IC} \times \text{CPI}}{f} .
$$

Units check: instructions × (cycles/instruction) × (seconds/cycle) = seconds. This is the **iron law of performance**. Its reciprocal factors are often more natural: **IPC** = 1/CPI (instructions per cycle), the measure quoted for superscalar processors that complete several instructions per cycle.

Each factor has an owner:

| Factor | Set mainly by | Improved by |
|---|---|---|
| IC | algorithm, compiler, instruction set | better algorithms, richer instructions, vector instructions |
| CPI | microarchitecture, memory system, program behaviour | pipelining, superscalar issue, caches, branch prediction |
| $T_c$ | circuit design, process technology, pipeline depth | faster transistors, shorter logic per stage |

**CPI from an instruction mix.** Group instructions into classes $i$ (arithmetic, loads, stores, branches...), with frequency $F_i$ (the fraction of executed instructions in class $i$, $\sum F_i = 1$) and average cycles $\text{CPI}_i$. The total cycles are $\sum_i(\text{IC}\,F_i)\,\text{CPI}_i$, so

$$
\text{CPI} = \sum_i F_i\,\text{CPI}_i ,
$$

a frequency-weighted average. The share of *time* spent in class $i$ is $F_i\text{CPI}_i/\text{CPI}$, which can be much larger than its share of instructions: loads that miss in the cache are a small fraction of instructions and a large fraction of time.

**Why MIPS misleads.** The rate MIPS (millions of instructions per second) is $\text{IC}/(T \times 10^6) = f/(\text{CPI} \times 10^6)$. It ignores IC, so a machine (or compiler) that executes more, simpler instructions can post a higher MIPS and still finish later (Example 14-01.1). The same trap applies to any rate that counts operations whose number depends on the implementation: FLOPS when one design uses more floating-point operations for the same answer, or TOPS (14-15) when the operations counted are not the ones the workload needs.

### 3.3 Amdahl's law

An enhancement speeds up part of a task. Let $p$ be the fraction of the original execution time that can use it and $s$ the speedup of that part. The other fraction $1 - p$ runs as before, so the new time is

$$
T_{new} = T_{old}\Big[(1 - p) + \frac{p}{s}\Big] ,
$$

and the overall speedup is

$$
S = \frac{T_{old}}{T_{new}} = \frac{1}{(1 - p) + p/s} .
$$

As $s \to \infty$, $S \to 1/(1 - p)$: the untouched part sets a hard ceiling. For parallel execution on $N$ processors with a perfectly parallel fraction $p$, $s = N$ and

$$
S(N) = \frac{1}{(1 - p) + p/N} .
$$

Two consequences follow directly.

- **Diminishing returns.** The efficiency $S(N)/N$ falls as $N$ grows. Reaching a fraction $x$ of the ceiling, $S = x/(1 - p)$, needs $N = p\,x/[(1 - x)(1 - p)]$: for $p$ = 0.9 and $x$ = 0.8, $N$ = 36 processors to get 8× out of a possible 10×.
- **Make the common case fast.** The benefit of a 10× improvement to 1% of the time is at most 1%; a 1.2× improvement to half the time gains 9%. Effort should follow the time profile.

> **Math refresher — inverting a sum of fractions.** Speedups do not add; times do. If a task's time divides into parts $t_1, t_2, \ldots$ and each part is sped up by $s_k$, the new time is $\sum t_k/s_k$ and the speedup is $\sum t_k/\sum(t_k/s_k)$: a weighted harmonic mean of the $s_k$, weighted by the time fractions. Amdahl's law is the two-part case with $s_1 = 1$.

**Gustafson's law.** Amdahl assumes a fixed problem. In practice, bigger machines are used to solve bigger problems in the same time. Measure the fractions on the *parallel* machine instead: let a run on $N$ processors spend fraction $\sigma$ of its time in serial code and $1 - \sigma$ in parallel code. The same work on one processor would take $\sigma + N(1 - \sigma)$ in those units, so the **scaled speedup** is

$$
S_{scaled}(N) = \sigma + N(1 - \sigma) = N - \sigma(N - 1) ,
$$

which grows linearly with $N$. Both laws are correct; they answer different questions. Amdahl asks "how much faster does *this* job get?", Gustafson "how much more work can I do in the same time?". A vendor quoting linear scaling is usually answering Gustafson's question; a user with a fixed job is asking Amdahl's.

![Two panels. Left: speedup against number of processors on log scales for parallel fractions 0.5, 0.9, 0.95 and 0.99, each curve flattening toward its ceiling of 2, 10, 20 and 100, with Gustafson's scaled speedup for a 10% serial fraction rising as a straight line. Right: energy per task against clock frequency from 0.2 to 4 GHz, with dynamic energy rising with frequency, leakage energy falling, and their total reaching a minimum near 0.89 GHz](../../../assets/figures/14-01/amdahl.svg)

*Figure 1. Left: Amdahl's fixed-problem speedup flattens at $1/(1 - p)$ (dotted lines), while Gustafson's scaled speedup keeps growing. Right: for the core of Problem 14-01.11, dynamic energy per task rises with frequency (the voltage must rise with it) while leakage energy falls (the task finishes sooner), so the total has a minimum (§3.6).*

> **Going deeper — when parallel speedup falls.** Real parallel programs pay overheads that grow with $N$: communication, synchronization and load imbalance. A simple model adds a term $cN$ (or $c\log N$) to the parallel time; then $S(N)$ reaches a maximum and falls, and adding processors makes the job slower. Measured scaling curves that bend over are the signature of these costs, which 14-12 examines.

### 3.4 Summarizing many benchmarks

A suite of benchmarks gives many times or ratios; a summary needs a mean, and the right mean depends on what is being summarized.

- **Times for a fixed set of jobs: the arithmetic mean** (or simply the total). If a workload runs each program once, the total time $\sum T_i$ is the truth, and $\frac1n\sum T_i$ is proportional to it. Weighted by how often each program runs, $\sum w_iT_i$.
- **Rates for equal work: the harmonic mean.** If each benchmark does the same work $W$ at rate $r_i$, the total time is $\sum W/r_i$ and the average rate over the whole run is $nW/\sum(W/r_i) = n/\sum(1/r_i)$: the harmonic mean. The arithmetic mean of rates overweights the fast ones.
- **Ratios to a reference: the geometric mean.** Benchmark suites such as SPEC report each program's time as a ratio to a reference machine, $R_i = T_{ref,i}/T_i$, and summarize by $\text{GM} = (\prod R_i)^{1/n}$.

The geometric mean is used for ratios because it is the only one of the three that does not depend on the reference. For machines A and B,

$$
\frac{\text{GM}_A}{\text{GM}_B} = \frac{(\prod T_{ref,i}/T_{A,i})^{1/n}}{(\prod T_{ref,i}/T_{B,i})^{1/n}} = \Big(\prod_i\frac{T_{B,i}}{T_{A,i}}\Big)^{1/n} :
$$

the reference times cancel. The arithmetic mean of ratios does not have this property, and changing the reference machine can reverse which machine looks faster (Example 14-01.6). The price is that the geometric mean does not track any real workload's total time: a machine can win the geometric mean and lose on the job you actually run. Summaries answer the question they were built for, and a careful reader asks which question that was.

### 3.5 Dynamic and static power

**Dynamic power.** Charging a node capacitance $C$ from 0 to $V$ through any resistance draws charge $CV$ from the supply at voltage $V$, energy $CV^2$; half is stored on the capacitor and half is dissipated in the resistance, whatever its value, and discharging dissipates the stored half (07-02 derives this from the RC transient). If, averaged over all the nodes of a block of total capacitance $C$, a fraction α (the **activity factor**) makes a rising transition each clock cycle, the block draws

$$
P_{dyn} = \alpha CV^2f ,
$$

with energy per cycle $\alpha CV^2$. Short-circuit current during input transitions adds a little more, usually a small fraction (09-11).

**Static (leakage) power.** Transistors that are "off" still conduct: subthreshold, gate and junction leakage (09-10). With total leakage current $I_{leak}$, $P_{static} = VI_{leak}$, paid every second the block is powered, whether or not it computes. Leakage grows exponentially as the threshold voltage falls and roughly doubles every few tens of degrees of temperature rise, which is why it became a large share of power once threshold voltages could not be raised.

**Voltage and frequency are linked.** A gate's delay is roughly the time to move charge $CV$ with a current that rises with gate overdrive, so $T_c \propto CV/I_{on}(V)$. A common approximation (the alpha-power law) gives

$$
f_{max} \propto \frac{(V - V_{TH})^a}{V}, \qquad 1 < a \le 2 ,
$$

with $a$ near 1 for velocity-saturated short-channel devices. Well above threshold, $f_{max}$ is roughly proportional to $V$. Then running at the highest frequency each voltage allows gives

$$
P_{dyn} \propto V^2f \propto f^3, \qquad E_{op} = \alpha CV^2 \propto f^2 :
$$

power grows as the cube of frequency and energy per operation as its square. Halving the frequency (and the voltage with it) cuts dynamic power by 8× and energy per operation by 4×, at twice the time. This is the basis of **dynamic voltage and frequency scaling** (DVFS): run slow and low when the work allows. The approximation fails near threshold, where frequency falls much faster than voltage and leakage energy, paid for the longer run time, starts to dominate (§3.6).

**Why clocks stopped getting faster.** Under constant-field (Dennard) scaling, each process generation shrank dimensions and voltage by $1/\kappa$, so power per transistor fell as $1/\kappa^2$ while transistor density rose as $\kappa^2$: power density stayed constant while the clock rose by κ (09-11 derives the rules). Once supply voltage stopped scaling, because threshold voltage cannot fall without exponential leakage (subthreshold swing is at least $\ln10\,kT/q$ ≈ 60 mV per decade at room temperature, 09-10), power per transistor stopped falling and power density rose with every generation. Chips hit the **power wall** in the mid-2000s; designers turned the extra transistors into more cores, larger caches and specialized units instead of a faster clock, and accepted **dark silicon**: parts of the chip that cannot all switch at once within the power budget.

### 3.6 Energy, performance per watt and the delay products

For a task of $N_c$ cycles at frequency $f$ and voltage $V$, the run time is $t = N_c/f$ and the energy is

$$
E = \underbrace{\alpha CV^2N_c}_{\text{dynamic}} + \underbrace{VI_{leak}\,\frac{N_c}{f}}_{\text{static}} .
$$

The dynamic term depends on voltage but not on how fast the work runs; the static term grows with run time. Lowering $V$ and $f$ together shrinks the first and stretches the second, so for a given leakage there is an **energy-optimal operating point**. Two policies follow.

- **DVFS:** run at the lowest voltage and frequency that meets the deadline. It wins when dynamic energy dominates.
- **Race to idle (race to halt):** run at full speed and then power-gate the block (cut its supply), so leakage stops. It wins when leakage, or the fixed power of the rest of the system (memory, display, radios) that stays on while the task runs, is large.

Which wins is a quantitative question (Example 14-01.5, Problem 14-01.12).

**Metrics.** Performance per watt, $(1/T)/P$, equals operations per joule, the reciprocal of energy per task: at a fixed workload it is the same as minimizing energy. For comparing designs at their best operating points, two products are used:

- the **energy-delay product**, $\text{EDP} = E \times T$, which weights energy and speed equally;
- the **energy-delay-squared product**, $\text{ED}^2\text{P} = E \times T^2$.

Under the cubic model above, with dynamic energy only, $E \propto V^2$ and $T \propto 1/f \propto 1/V$, so

$$
E \times T^2 \propto V^2 \times V^{-2} = \text{constant} :
$$

ED²P does not change when one design is simply run at a different voltage. It therefore compares *architectures* rather than operating points: a design with lower ED²P can be voltage-scaled to beat the other in both energy and speed. Comparing two chips by performance per watt at different operating points, by contrast, rewards whichever was measured lower on its voltage curve (§9).

## 4. Worked examples

### Example 14-01.1 · The iron law and the MIPS trap (tier A)

**Setup.** A program compiled with compiler A executes 2.5 × 10⁹ instructions at CPI 1.2 on a 3.0 GHz processor. Compiler B produces 2.0 × 10⁹ instructions of more complex kinds, with CPI 1.4 on the same processor. Find each execution time, the speedup of B over A, and each MIPS rating.

**Solution.** By the iron law, $T_A = 2.5 \times 10^9 \times 1.2/(3.0 \times 10^9)$ = **1.000** s and $T_B = 2.0 \times 10^9 \times 1.4/(3.0 \times 10^9)$ = **0.9333** s, so B is **1.071** times faster. MIPS = IC/($T \times 10^6$): A rates **2500** MIPS and B **2143** MIPS.

**Units check.** (instructions)(cycles/instruction)/(cycles/s) = s; MIPS is instructions/s divided by 10⁶.

**Sanity check.** B wins on time but loses on MIPS, because MIPS ignores how much work each instruction does. Only time compares the two.

### Example 14-01.2 · CPI from an instruction mix (tier B)

**Setup.** A workload's dynamic mix is 45% ALU instructions (CPI 1), 25% loads (average CPI 2.5, including cache misses), 10% stores (CPI 1) and 20% branches (average CPI 1.8, including mispredictions). Find the CPI and the fraction of time spent on loads. A better cache cuts the average load CPI to 1.6: find the speedup, and check it with Amdahl's law.

**Solution.** $\text{CPI} = 0.45(1) + 0.25(2.5) + 0.10(1) + 0.20(1.8)$ = **1.535**. Loads take $0.625/1.535$ = **40.72**% of the time though they are 25% of the instructions. With load CPI 1.6, $\text{CPI}$ = 1.535 − 0.25 × 0.9 = **1.31**, so (IC and clock unchanged) the speedup is $1.535/1.31$ = **1.172**. Amdahl's law with $p$ = 0.4072 and $s$ = 2.5/1.6 = 1.5625 gives $1/(0.5928 + 0.4072/1.5625)$ = 1.172, the same.

**Units check.** CPI is a weighted average of cycles per instruction, so it stays in cycles/instruction; the time fraction is a ratio.

**Sanity check.** Loads were 40% of the time and got 1.56× faster, so the gain must lie between 1 and 1/(1 − 0.41) = 1.69; 1.17 does.

### Example 14-01.3 · Amdahl against Gustafson (tier B)

**Setup.** A job is 90% parallelizable. (a) Find its speedup on 16 processors and the limit for unlimited processors. (b) How many processors reach 80% of that limit? (c) A larger problem run on 16 processors spends 10% of its time in serial code. Find the scaled speedup.

**Solution.** (a) $S(16) = 1/(0.1 + 0.9/16)$ = **6.4**; the limit is $1/0.1$ = **10**. (b) 80% of the limit is 8, and $1/(0.1 + 0.9/N) = 8$ gives $0.9/N$ = 0.025, $N$ = **36**. (c) $S_{scaled} = 0.1 + 0.9 \times 16$ = **14.5**.

**Units check.** All are ratios of times.

**Sanity check.** Sixteen processors at 6.4× is 40% efficiency; the scaled speedup is higher because the parallel part grew with the machine while the serial part did not.

### Example 14-01.4 · Dynamic and static power (tier A)

**Setup.** A processor core has an effective switched capacitance $\alpha C$ of 1.5 nF. It runs at 0.9 V and 3.2 GHz, and leaks 1.2 W at that voltage. Find its dynamic power, the energy per clock cycle and the total power.

**Solution.** $P_{dyn} = \alpha CV^2f = 1.5 \times 10^{-9} \times 0.81 \times 3.2 \times 10^9$ = **3.888** W. The energy per cycle is $\alpha CV^2$ = **1.215** nJ. Total: 3.888 + 1.2 = **5.088** W.

**Units check.** F × V² = C·V = J, and J × (1/s) = W.

**Sanity check.** Leakage is 24% of the total, typical of a core at a moderate voltage; it does not fall when the core stops switching, only when it is power-gated.

### Example 14-01.5 · DVFS or race to idle? (tier B)

**Setup.** The core of Example 14-01.4 must run a task of 3.2 × 10⁹ cycles. Option 1: run at 0.9 V and 3.2 GHz, then power-gate (no energy afterwards). Option 2: run at 0.75 V and 2.4 GHz. Leakage current is the same at both voltages, so leakage power scales with $V$. Find the dynamic power at option 2, and the energy of each option.

**Solution.** Option 2 dynamic power is $1.5 \times 10^{-9} \times 0.5625 \times 2.4 \times 10^9$ = **2.025** W, **0.5208** of option 1's. The leakage current is 1.2/0.9 = 1.333 A, so option 2 leaks 1.0 W.

- Option 1: dynamic energy $\alpha CV^2N_c$ = 1.215 nJ × 3.2 × 10⁹ = 3.888 J; it runs for 1 s, so leakage energy is 1.2 J; total **5.088** J.
- Option 2: dynamic energy 1.5 nF × 0.5625 × 3.2 × 10⁹ = **2.7** J; it runs for **1.333** s, so leakage energy is 1.0 × 1.333 = 1.333 J; total **4.033** J.

Option 2 saves **20.73**% of the energy and takes a third longer.

**Units check.** Dynamic energy is (F)(V²)(cycles) = J per cycle × cycles; leakage energy is W × s = J.

**Sanity check.** Dynamic energy fell by $(0.75/0.9)^2$ = 0.694, while leakage energy rose because the run is longer. If leakage were several times larger, racing to idle would win (Problem 14-01.12 finds the crossover).

### Example 14-01.6 · Which mean? (tier C)

**Setup.** Two machines run two programs. Program 1 takes 1 s on A and 10 s on B; program 2 takes 1000 s on A and 100 s on B. (a) Which is faster for a workload that runs each once? (b) Normalize to A and average B's ratios arithmetically, then normalize to B and average A's ratios. (c) Do the same with the geometric mean.

**Solution.** (a) Totals: A 1001 s, B 110 s, so B is **9.1** times faster for this workload. (b) Normalized to A, B's time ratios are 10 and 0.1, arithmetic mean **5.05**: "B is 5 times slower". Normalized to B, A's ratios are 0.1 and 10, mean 5.05: "A is 5 times slower". The arithmetic mean of ratios contradicts itself. (c) The geometric mean of 10 and 0.1 is **1** either way: on a typical-ratio basis the machines are equal, whichever is the reference.

**Units check.** Times in seconds; ratios and means of ratios dimensionless.

**Sanity check.** Each machine is 10× faster on one program. The geometric mean says "even"; the total time says B, because the program B wins on is the long one. Both are right about different questions, and only the workload's own mix of run times decides which matters.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-01.1a | time with compiler A | 1.000 | s |
| Ex 14-01.1b | time with compiler B | 0.9333 | s |
| Ex 14-01.1c | speedup of B over A | 1.071 | — |
| Ex 14-01.1d | MIPS with A | 2500 | — |
| Ex 14-01.1e | MIPS with B | 2143 | — |
| Ex 14-01.2a | CPI | 1.535 | — |
| Ex 14-01.2b | fraction of time in loads | 40.72 | % |
| Ex 14-01.2c | CPI with the better cache | 1.31 | — |
| Ex 14-01.2d | speedup | 1.172 | — |
| Ex 14-01.3a | speedup on 16 processors | 6.4 | — |
| Ex 14-01.3b | limit | 10 | — |
| Ex 14-01.3c | processors for 80% of the limit | 36 | — |
| Ex 14-01.3d | scaled speedup | 14.5 | — |
| Ex 14-01.4a | dynamic power | 3.888 | W |
| Ex 14-01.4b | energy per cycle | 1.215 | nJ |
| Ex 14-01.4c | total power | 5.088 | W |
| Ex 14-01.5a | dynamic power at 0.75 V, 2.4 GHz | 2.025 | W |
| Ex 14-01.5b | ratio to full speed | 0.5208 | — |
| Ex 14-01.5c | energy at full speed | 5.088 | J |
| Ex 14-01.5d | dynamic energy at low speed | 2.7 | J |
| Ex 14-01.5e | run time at low speed | 1.333 | s |
| Ex 14-01.5f | energy at low speed | 4.033 | J |
| Ex 14-01.5g | energy saved | 20.73 | % |
| Ex 14-01.6a | workload speedup of B | 9.1 | — |
| Ex 14-01.6b | arithmetic mean of ratios | 5.05 | — |
| Ex 14-01.6c | geometric mean of ratios | 1 | — |
| Sim 14-01.a | supply power, 1 pF switched at 100 MHz, 1 V | 100 | µW |
| Sim 14-01.b | resistor energy per charge | 0.5 | pJ |

## 5. Simulate it

The lab, [labs/14-01-lab](../labs/14-01-lab/README.md), has a notebook and an ngspice netlist:

1. An iron-law explorer: compute time, CPI and the time share of each instruction class from a mix, and see how a change in one class moves the total.
2. Amdahl and Gustafson curves for several parallel fractions, and an overhead model whose speedup peaks and falls.
3. DVFS: energy per task against frequency for a core with dynamic and leakage power, the energy-optimal frequency, and the leakage at which race-to-idle wins.
4. The means paradox: two machines, a suite of benchmarks, and how the arithmetic and geometric means of ratios behave when the reference changes.

The netlist [switched_cap.cir](../labs/14-01-lab/switched_cap.cir) charges and discharges a 1 pF capacitor through a resistor from a 1 V supply 100 million times a second and measures the average supply power and the energy dissipated in the resistor.

**Guided exercise (predict, then run).** **Before running the netlist,** predict the average supply power and the energy lost in the resistor during one charge. Then run it; the netlist repeats the run with the resistor changed from 100 Ω to 300 Ω. (The power is $CV^2f$ = **100** µW and the resistor takes $\tfrac12CV^2$ = **0.5** pJ per charge, whatever its value: the resistance sets only how fast the charge moves, not how much energy is lost.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Richer instructions (lower IC) | Fewer instructions per task | Harder decoding, longer cycle or higher CPI; ISA complexity forever | ISA architect, compiler team |
| Deeper pipeline (shorter $T_c$) | Clock rate | More cycles lost per mispredict and per hazard; more latches and power | Microarchitect |
| Wider issue, out-of-order (lower CPI) | IPC | Area and power that grow faster than IPC | Microarchitect |
| Higher supply voltage | Frequency | Power ∝ $V^2f$, about $f^3$; reliability and thermal limits | Circuit and power teams, product management |
| More cores | Throughput, scaled speedup | Amdahl limit on fixed jobs; coherence and memory bandwidth | Chip architect, software ecosystem |
| Lower threshold voltage | Speed at low supply | Exponentially more leakage | Process and circuit teams |
| Power gating | Removes leakage of idle blocks | Wake-up latency and energy; area of switches | SoC power architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Iron law | $T = \text{IC} \times \text{CPI}/f$ | §3.2 |
| Amdahl ceiling | $1/(1 - p)$ | 90% parallel → 10× at most |
| Dynamic power | $\alpha CV^2f$, energy $\alpha CV^2$ per cycle | 07-02, 09-11 |
| Power against frequency with DVFS | roughly $f^3$ near the top of the range | §3.5 |
| Subthreshold swing limit | about 60 mV/decade at 300 K | 09-10 |
| End of clock-rate scaling | about 2004, clocks around 5 GHz | IRDS [1] |

## 8. Common mistakes

- **Comparing rates instead of times.** MIPS, FLOPS and TOPS count operations whose number depends on the machine and compiler. Compare execution times for the same work.
- **"30% faster" means 70% of the time.** It means 1/1.3 = 77% of the time.
- **Applying a speedup to the whole program.** A 10× faster kernel that is 30% of the run gives 1.37×, not 10×.
- **Averaging ratios arithmetically.** The result depends on the reference; use the geometric mean for ratios, the total or a weighted mean for a real workload.
- **Treating CPI as a property of the processor alone.** It depends on the program's mix, its memory behaviour and even the clock rate (memory latency is fixed in nanoseconds, so a faster clock means more cycles per miss).
- **Assuming lower power means lower energy.** Running slower lowers power but stretches the time over which leakage and the rest of the system draw power.
- **Comparing performance per watt at different operating points.** A chip measured at a low point on its voltage curve looks more efficient than the same design at full speed.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Frequency stopped scaling two decades ago.** The IEEE IRDS 2024 executive summary places the power limit in 2004 and puts processor clocks at about 5 GHz since then [1] **[Established]**. Gains since have come from IPC, more cores, larger caches and specialized hardware (14-13, 14-14).
- **Efficiency claims are operating-point claims.** Because power rises roughly as the cube of frequency near the top of the range (§3.5), the same design can show very different performance per watt depending on where on its voltage–frequency curve it is measured. A claim of better efficiency at "iso-performance" (equal speed) and one at "iso-power" (equal power) can describe the same chips and differ several-fold (our derivation).

### Why it matters commercially

- **Datacenter total cost of ownership** includes years of electricity and cooling, so buyers rank servers and accelerators by performance per watt on their own workloads **[Established]**.
- **Mobile and wearable products** live on energy per task; the operating system's DVFS and idle policies are as important as the silicon (Course 22) **[Established]**.
- **Parallel products** (many-core CPUs, GPUs) are sold on throughput; customers with fixed, partly serial jobs see Amdahl's limit, not the peak.

### Marketing vs Reality

- **"Up to 2× performance."** *Reality:* "up to" is the best case, usually one benchmark or kernel. *Sanity check:* ask for the geometric mean across a named suite and for the workload you run, at the same power.
- **"40% better performance per watt."** *Reality:* efficiency depends on the operating point; a new chip measured at a lower point on its voltage curve than the old one gains "efficiency" without any architectural improvement. *Sanity check:* ask for the full performance-against-power curve of both chips, or compare at equal performance and at equal power.
- **"Linear scaling to 1,000 cores."** *Reality:* usually weak (Gustafson) scaling with the problem grown in proportion. *Sanity check:* ask for strong scaling (fixed problem) and the serial fraction it implies.
- **"N TOPS."** *Reality:* a peak rate of operations at a stated precision, often with sparsity counted as work done (14-15). *Sanity check:* ask for delivered throughput on a named model, at a stated precision and batch size.

### Questions for engineering leaders

1. **"On which workloads, at what power, did you measure the speedup?"**
   *Strong:* a named suite and named customer workloads, run at equal power and at equal performance, with the geometric mean and the per-benchmark spread. *Evasive:* "up to" a single number on one kernel.
2. **"Where does the time go?"**
   *Strong:* a measured breakdown (compute, memory stalls, branch mispredictions, synchronization) that justifies what the new design changed. *Evasive:* the improvement is described only by peak rates.
3. **"What fraction of your target applications is serial, and what does that cap your speedup at?"**
   *Strong:* profiled serial fractions and the Amdahl ceiling, with strong-scaling curves. *Evasive:* weak-scaling results only.
4. **"How much of your power is leakage, and how do you manage idle?"**
   *Strong:* the dynamic/static split at typical operating points, power-gating granularity and wake-up costs. *Evasive:* only peak power or TDP.
5. **"Show me the voltage–frequency and performance–power curves."**
   *Strong:* full curves for both the new and the competing chip. *Evasive:* a single operating point chosen for the comparison.

## 10. Concept check

**Q1.** Write the iron law and name who owns each factor.

<details><summary>Answer</summary>

$T = \text{IC} \times \text{CPI} \times T_c$. Instruction count: the algorithm, the compiler and the instruction set. CPI: the microarchitecture and memory system (and the program's behaviour). Clock period: circuit design, process technology and pipeline depth.

</details>

**Q2.** Why can a machine with a higher MIPS rating be slower?

<details><summary>Answer</summary>

MIPS counts instructions per second and ignores how many instructions the program needs. A machine or compiler that uses more, simpler instructions can execute them faster and still take longer in total.

</details>

**Q3.** A task is 95% parallel. What is the most it can be sped up by parallel hardware?

<details><summary>Answer</summary>

$1/(1 - 0.95)$ = 20×, however many processors are used, under Amdahl's fixed-problem assumption.

</details>

**Q4.** When is Gustafson's law the right model, and when is Amdahl's?

<details><summary>Answer</summary>

Gustafson's when the problem size grows with the machine and the run time is held fixed (scaled speedup, "do more in the same time"); Amdahl's when the problem is fixed and the question is how much faster it finishes.

</details>

**Q5.** Why is the geometric mean used for benchmark ratios?

<details><summary>Answer</summary>

Because the ratio of two machines' geometric means does not depend on the reference machine: the reference times cancel. The arithmetic mean of ratios can rank machines differently depending on the reference.

</details>

**Q6.** Why does power rise roughly as the cube of frequency at the top of the range?

<details><summary>Answer</summary>

Dynamic power is $\alpha CV^2f$, and the highest frequency a design can run at is roughly proportional to its supply voltage well above threshold. Raising $f$ requires raising $V$ in proportion, so power goes as $V^2f \propto f^3$.

</details>

**Q7.** When does racing to idle beat running slowly?

<details><summary>Answer</summary>

When leakage (or the power of other parts of the system that stay on while the task runs) is large, so that the extra time of the slow run costs more static energy than the lower voltage saves in dynamic energy, and the block can be power-gated when it finishes.

</details>

**Q8.** Why is ED²P useful for comparing architectures?

<details><summary>Answer</summary>

Under the simple model where energy scales as $V^2$ and delay as $1/V$, $E \times T^2$ does not change when a design is run at a different voltage. So it compares designs independently of the operating point chosen, unlike performance per watt at one point.

</details>

Now work the [problem set](../problems/14-01-problems.md).

## 11. Key terms

[Iron law of performance](../../../reference/glossary.md#iron-law-of-performance) · [CPI](../../../reference/glossary.md#cpi) · [IPC](../../../reference/glossary.md#ipc) · [Speedup](../../../reference/glossary.md#speedup) · [Amdahl's law](../../../reference/glossary.md#amdahls-law) · [Gustafson's law](../../../reference/glossary.md#gustafsons-law) · [Geometric mean](../../../reference/glossary.md#geometric-mean) · [Dynamic power](../../../reference/glossary.md#dynamic-power) · [Activity factor](../../../reference/glossary.md#activity-factor) · [Static power](../../../reference/glossary.md#static-power) · [Dynamic voltage and frequency scaling (DVFS)](../../../reference/glossary.md#dynamic-voltage-and-frequency-scaling-dvfs) · [Race to idle](../../../reference/glossary.md#race-to-idle) · [Energy-delay product](../../../reference/glossary.md#energy-delay-product) · [Power wall](../../../reference/glossary.md#power-wall) · [Dark silicon](../../../reference/glossary.md#dark-silicon) · [Latency](../../../reference/glossary.md#latency) · [Throughput](../../../reference/glossary.md#throughput)

## 12. Connections

- **Builds on:** the energy of charging a capacitor ([07-02](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md)); CMOS power, Dennard scaling and its end ([09-11](../../09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md)); leakage and the subthreshold swing ([09-10](../../09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md)).
- **Next:** [14-02 Instruction Set Architecture](14-02-isa-risc-v-arm-x86.md), which sets the instruction count.
- **Used later:** CPI and the clock period in pipelining ([14-06](14-06-pipelining-and-hazards.md)); memory stalls in CPI ([14-09](14-09-memory-hierarchy-and-caches.md)); Amdahl's law in multicore ([14-12](14-12-multicore-coherence-consistency.md)); roofline and benchmark gaming ([14-15](14-15-roofline-and-benchmarks.md)); power management in Course 22.

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design* (RISC-V Edition), ch. 1 (performance, power wall, Amdahl's law, fallacies and pitfalls).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, ch. 1 (quantitative principles, power and energy, measuring and summarizing performance).
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on performance and power.
- J. L. Gustafson, "Reevaluating Amdahl's law", *Communications of the ACM* 31(5), 1988.

## 14. Sources

1. IEEE IRDS, 2024 Edition, Executive Summary, pp. 64–66 (power limits in 2004, frequency limit): [IRDS 2024 Executive Summary](https://irds.ieee.org/images/files/pdf/2024/2024IRDS_ES.pdf). [R-172](../../../reference/research-log.md#r-172--cmos-and-scaling-references).

The theory (iron law, Amdahl's and Gustafson's laws, means, CMOS power and its scaling) is textbook material (Further study).
