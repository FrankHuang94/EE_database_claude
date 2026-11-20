<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 14 · Computer Organization and Architecture

How processors and accelerators are built and why they perform the way they do: ISAs (RISC-V primary, with Arm and x86 and their licensing models), pipelines, speculation, out-of-order execution, memory hierarchy, multicore, GPUs and AI accelerators, roofline analysis, and how benchmarks are gamed.

| | |
|---|---|
| **Term** | 4 |
| **Study hours** | ≈ 122 |
| **University equivalents** | Computer Organization + Computer Architecture (junior/senior); MIT 6.004 / 6.823; Berkeley CS61C / CS152; Stanford EE282 |
| **Textbook alignment** | Patterson & Hennessy, *Computer Organization and Design* (RISC-V Edition); Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*; Harris & Harris, *Digital Design and Computer Architecture* (RISC-V Edition) |
| **Free courses** | MIT OCW 6.004 Computation Structures; MIT OCW 6.823 Computer System Architecture; Berkeley CS61C (public lecture materials) |
| **Prerequisites** | [05 · Programming for Engineers](../05-programming-for-engineers/README.md), [08 · Digital Logic Design](../08-digital-logic-design/README.md) |
| **FE areas** | Computer Systems, Digital Systems |
| **Deeper** | Companion repo(s): LLM inference engineering; datacenter networking |

## Learning objectives

1. Use the iron law of performance and Amdahl's law to reason about speedups.
2. Read and write RISC-V assembly, and contrast RISC-V, Arm and x86 ISAs and their business models.
3. Design single-cycle and pipelined datapaths and resolve data and control hazards.
4. Analyze caches, virtual memory and multicore coherence quantitatively.
5. Explain GPU (SIMT) and AI-accelerator (systolic, dataflow, low-precision) architectures and analyze them with the roofline model.
6. Critically evaluate benchmark and TOPS claims.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [14-01 · Performance, Power and the Iron Law](chapters/14-01-performance-power-iron-law.md) | 7 | 🏁 reviewed | [problems](problems/14-01-problems.md) · [solutions](solutions/14-01-solutions.md) · [lab](labs/14-01-lab/README.md) · [verify](verify/verify_14_01.py) |
| [14-02 · Instruction Set Architecture: RISC-V, Arm and x86](chapters/14-02-isa-risc-v-arm-x86.md) | 10 | 🏁 reviewed | [problems](problems/14-02-problems.md) · [solutions](solutions/14-02-solutions.md) · [lab](labs/14-02-lab/README.md) · [verify](verify/verify_14_02.py) |
| [14-03 · Assembly and the Compilation Stack](chapters/14-03-assembly-and-the-compilation-stack.md) | 8 | 🏁 reviewed | [problems](problems/14-03-problems.md) · [solutions](solutions/14-03-solutions.md) · [lab](labs/14-03-lab/README.md) · [verify](verify/verify_14_03.py) |
| [14-04 · Computer Arithmetic and Number Formats](chapters/14-04-computer-arithmetic-and-number-formats.md) | 7 | 🏁 reviewed | [problems](problems/14-04-problems.md) · [solutions](solutions/14-04-solutions.md) · [lab](labs/14-04-lab/README.md) · [verify](verify/verify_14_04.py) |
| [14-05 · Single-Cycle Datapath and Control](chapters/14-05-single-cycle-datapath.md) | 8 | 🏁 reviewed | [problems](problems/14-05-problems.md) · [solutions](solutions/14-05-solutions.md) · [lab](labs/14-05-lab/README.md) · [verify](verify/verify_14_05.py) |
| [14-06 · Pipelining and Hazards](chapters/14-06-pipelining-and-hazards.md) | 10 | 🏁 reviewed | [problems](problems/14-06-problems.md) · [solutions](solutions/14-06-solutions.md) · [lab](labs/14-06-lab/README.md) · [verify](verify/verify_14_06.py) |
| [14-07 · Branch Prediction and Speculation](chapters/14-07-branch-prediction-and-speculation.md) | 7 | 🏁 reviewed | [problems](problems/14-07-problems.md) · [solutions](solutions/14-07-solutions.md) · [lab](labs/14-07-lab/README.md) · [verify](verify/verify_14_07.py) |
| [14-08 · Out-of-Order and Superscalar Execution](chapters/14-08-out-of-order-and-superscalar.md) | 9 | 🏁 reviewed | [problems](problems/14-08-problems.md) · [solutions](solutions/14-08-solutions.md) · [lab](labs/14-08-lab/README.md) · [verify](verify/verify_14_08.py) |
| [14-09 · Memory Hierarchy and Caches](chapters/14-09-memory-hierarchy-and-caches.md) | 10 | 🏁 reviewed | [problems](problems/14-09-problems.md) · [solutions](solutions/14-09-solutions.md) · [lab](labs/14-09-lab/README.md) · [verify](verify/verify_14_09.py) |
| [14-10 · Virtual Memory, TLBs and the OS Interface](chapters/14-10-virtual-memory.md) | 7 | 🏁 reviewed | [problems](problems/14-10-problems.md) · [solutions](solutions/14-10-solutions.md) · [lab](labs/14-10-lab/README.md) · [verify](verify/verify_14_10.py) |
| [14-11 · I/O, Buses and Interconnect](chapters/14-11-io-buses-and-interconnect.md) | 5 | 🏁 reviewed | [problems](problems/14-11-problems.md) · [solutions](solutions/14-11-solutions.md) · [lab](labs/14-11-lab/README.md) · [verify](verify/verify_14_11.py) |
| [14-12 · Multicore, Coherence and Memory Consistency](chapters/14-12-multicore-coherence-consistency.md) | 8 | 🏁 reviewed | [problems](problems/14-12-problems.md) · [solutions](solutions/14-12-solutions.md) · [lab](labs/14-12-lab/README.md) · [verify](verify/verify_14_12.py) |
| [14-13 · GPUs and SIMT](chapters/14-13-gpus-and-simt.md) | 7 | 🏁 reviewed | [problems](problems/14-13-problems.md) · [solutions](solutions/14-13-solutions.md) · [lab](labs/14-13-lab/README.md) · [verify](verify/verify_14_13.py) |
| [14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision](chapters/14-14-ai-accelerators.md) | 9 | 🏁 reviewed | [problems](problems/14-14-problems.md) · [solutions](solutions/14-14-solutions.md) · [lab](labs/14-14-lab/README.md) · [verify](verify/verify_14_14.py) |
| [14-15 · The Roofline Model, Benchmarks and How They Are Gamed](chapters/14-15-roofline-and-benchmarks.md) | 4 | 🏁 reviewed | [problems](problems/14-15-problems.md) · [solutions](solutions/14-15-solutions.md) · [lab](labs/14-15-lab/README.md) · [verify](verify/verify_14_15.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/14-computer-organization-and-architecture.csv) · [Equation sheet](../../reference/equation-sheets/14-computer-organization-and-architecture.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 14 is planned at about 122 hours: the chapters' own estimates add to 116, plus review and the exam. Course 08 built logic from gates up to small datapaths. This course builds a whole computer: the instruction set as a contract, the processors that implement it ever faster, the memory system that feeds them, the operating-system interface, and finally the throughput machines (GPUs and AI accelerators) that dominate today's chip industry.

The fifteen chapters fall into five blocks:

- **Performance and the ISA (14-01 to 14-04).** The iron law, Amdahl and power; RISC-V, Arm and x86 as architectures and as businesses; assembly, calling conventions and linking; integer, floating-point and low-precision arithmetic.
- **Building a processor (14-05 to 14-08).** A single-cycle RISC-V core in Verilog; a five-stage pipeline with forwarding and stalls; branch prediction, speculation and Spectre; out-of-order superscalar execution and the limits of instruction-level parallelism.
- **Memory and the OS (14-09 and 14-10).** Caches, AMAT, the three Cs, tiling and prefetching; virtual memory, TLBs, page faults and traps.
- **Systems (14-11 and 14-12).** Devices, interrupts, DMA, buses and networks-on-chip, PCIe and CXL; multicore coherence and memory consistency.
- **Throughput machines (14-13 to 14-15).** GPUs and SIMT; AI accelerators, systolic arrays and quantization; the roofline model and how benchmarks are read, and gamed.

Work at least the [A] and [B] problems of every chapter (153 of the 199 problems; the 46 [C] problems are the stretch). The labs form a toolchain that the course builds on itself:

- an RV32IM simulator in Python (`verify/_rv32.py`) runs code assembled and compiled with LLVM;
- single-cycle and pipelined RISC-V cores in Verilog must match the simulator's register writes instruction for instruction;
- trace-driven models replay the simulator's traces through branch predictors, an out-of-order scheduler and caches, and C kernels compiled with clang provide realistic memory traces;
- further models cover Sv32 page tables, a MESI system with invariant checks, exhaustive litmus tests, SIMT warps, and a systolic array in both Python and Verilog.

Every verify script recomputes the chapters' numbers through these models and checks them against independent closed forms, so a mismatch in your own work usually means a wrong method, not rounding.

**What to master cold.** The equation sheet collects the relations; these are the ideas behind them:

- performance is instructions × CPI × cycle time, and every design change trades one factor against another (14-01);
- an ISA is a contract that outlives every implementation; its encoding and its licence both shape the industry (14-02);
- pipelining overlaps instructions, hazards break the overlap, and forwarding, stalls and prediction repair it (14-05 to 14-07);
- out-of-order cores find parallelism dynamically, but true dependences, branches and memory bound it, and Little's law sizes the window (14-08);
- locality makes caches work; misses are compulsory, capacity or conflict; and software (loop order, tiling) often matters more than hardware (14-09);
- virtual memory is translation plus protection, cached by the TLB, and traps are how hardware hands control to the OS precisely (14-10);
- coherence orders writes to one address, consistency orders accesses to different addresses, and false sharing and fences are where they bite (14-12);
- GPUs hide latency with threads, and divergence, coalescing and occupancy decide how much of their peak a kernel gets (14-13);
- accelerators win by reuse and low precision; data movement, not arithmetic, sets energy and speed (14-14);
- the roofline tells you whether peak FLOPS or bandwidth limits a kernel, and benchmark numbers must be read with their rules (14-15).

The [equation sheet](../../reference/equation-sheets/14-computer-organization-and-architecture.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 210 minutes, with a calculator and the equation sheet but no Python, simulator or assembler. Aim for at least 70%. Questions 1 to 12 follow the chapters; Question 13 asks for three short derivations (two-level AMAT, systolic latency, warps to hide latency); Question 14 is a diligence question about an accelerator start-up's claims, partly graded against a rubric. The course maps onto the FE Electrical and Computer exam's Computer Systems and Digital Systems areas ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification)). The [flashcards](../../flashcards/14-computer-organization-and-architecture.csv) (96 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Architecture claims are where marketing and engineering meet most often. This course teaches you to ask:

- whether a performance claim is peak or delivered, dense or sparse, at which precision, batch size and power;
- whether a workload is compute- or memory-bound on the hardware in question, using its ridge point;
- what an ISA or IP choice (RISC-V, Arm, x86) implies for licensing, software ecosystem and switching costs;
- how much of a product's advantage comes from the memory system (caches, HBM, interconnect) rather than from the arithmetic units;
- whether a benchmark result follows the benchmark's rules (SPEC base, MLPerf Closed) and covers the workloads you care about.
