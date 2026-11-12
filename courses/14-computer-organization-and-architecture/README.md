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
| [14-01 · Performance, Power and the Iron Law](chapters/14-01-performance-power-iron-law.md) | 7 | ⬜ planned | — |
| [14-02 · Instruction Set Architecture: RISC-V, Arm and x86](chapters/14-02-isa-risc-v-arm-x86.md) | 10 | ⬜ planned | — |
| [14-03 · Assembly and the Compilation Stack](chapters/14-03-assembly-and-the-compilation-stack.md) | 8 | ⬜ planned | — |
| [14-04 · Computer Arithmetic and Number Formats](chapters/14-04-computer-arithmetic-and-number-formats.md) | 7 | ⬜ planned | — |
| [14-05 · Single-Cycle Datapath and Control](chapters/14-05-single-cycle-datapath.md) | 8 | ⬜ planned | — |
| [14-06 · Pipelining and Hazards](chapters/14-06-pipelining-and-hazards.md) | 10 | ⬜ planned | — |
| [14-07 · Branch Prediction and Speculation](chapters/14-07-branch-prediction-and-speculation.md) | 7 | ⬜ planned | — |
| [14-08 · Out-of-Order and Superscalar Execution](chapters/14-08-out-of-order-and-superscalar.md) | 9 | ⬜ planned | — |
| [14-09 · Memory Hierarchy and Caches](chapters/14-09-memory-hierarchy-and-caches.md) | 10 | ⬜ planned | — |
| [14-10 · Virtual Memory, TLBs and the OS Interface](chapters/14-10-virtual-memory.md) | 7 | ⬜ planned | — |
| [14-11 · I/O, Buses and Interconnect](chapters/14-11-io-buses-and-interconnect.md) | 5 | ⬜ planned | — |
| [14-12 · Multicore, Coherence and Memory Consistency](chapters/14-12-multicore-coherence-consistency.md) | 8 | ⬜ planned | — |
| [14-13 · GPUs and SIMT](chapters/14-13-gpus-and-simt.md) | 7 | ⬜ planned | — |
| [14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision](chapters/14-14-ai-accelerators.md) | 9 | ⬜ planned | — |
| [14-15 · The Roofline Model, Benchmarks and How They Are Gamed](chapters/14-15-roofline-and-benchmarks.md) | 4 | ⬜ planned | — |

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

*(Hand-written notes for this course go below the generated block.)*
