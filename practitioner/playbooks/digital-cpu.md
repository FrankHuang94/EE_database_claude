# Playbook · Digital Logic and CPUs

**Use it for:** CPU cores and SoC IP, custom silicon programs, RISC-V companies, and any claim of "x% faster at the same power". **Core chapters:** [14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md) to [14-12](../../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md), [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md), [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) to [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md). **Question bank:** [digital and computing](../question-banks/digital-and-computing.md).

## What decides it

1. **Is the performance claim measured on silicon, at a stated clock, voltage and workload?** Simulated or projected performance on a benchmark the company chose is the weakest evidence in the domain.
2. **What is the power at that performance point?** Performance without the matching power is half a claim, because the dynamic power $\alpha CV^2f$ rises steeply with voltage.
3. **Can the team close timing and verification at the next node, on schedule?** Respins are the dominant schedule and cost risk ([26-05](../../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md)).
4. **Who owns the instruction set and the IP, and what changes on a change of control?** Arm licenses, x86 rights, RISC-V extensions, and third-party SerDes and memory PHYs all carry terms ([26-04](../../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md)).
5. **Does real software run?** Upstream compilers, the ABI, and customers' code running unchanged ([14-03](../../courses/14-computer-organization-and-architecture/chapters/14-03-assembly-and-the-compilation-stack.md)).

## First-principles checks

| Claim | Check | Where derived |
|---|---|---|
| "x% faster" | Iron law: time = instructions × CPI × cycle time. Which factor moved, and does the workload change the instruction count? | [14-01](../../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md) |
| "Same power, higher clock" | $P = \alpha C V^2 f$. A higher $f$ needs a higher $V$ beyond the knee, so power rises as roughly $f^3$ there. Ask for the voltage–frequency curve | [19-06](../../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md) |
| "More cores, linear scaling" | Amdahl's law with the serial fraction; coherence traffic and memory bandwidth per core | [14-12](../../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md) |
| "Big cache, low latency" | Average memory access time = hit time + miss rate × miss penalty; larger arrays are slower | [14-09](../../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md) |
| "Closed timing at x GHz" | At which corner, with which on-chip-variation margins and which parasitics (post-route or estimated)? | [19-10](../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md), [19-11](../../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md) |
| "Verification complete" | Coverage closure, bug-discovery trend flattening, formal on the control logic | [19-13](../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md), [28-03](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md) |

## Evidence ladder

From weakest to strongest:

1. a slide;
2. a simulated benchmark;
3. an FPGA or emulator run;
4. silicon at a stated voltage and clock on the company's benchmark;
5. silicon on the customer's own code;
6. production volume with field data.

## Red flags and green flags

**Red flags:**

- performance quoted without power, or power without the clock;
- the benchmark changed between product generations;
- "taped out" given as evidence of working silicon;
- verification described by headcount instead of coverage;
- a custom ISA extension the compilers do not support upstream.

**Green flags:**

- voltage–frequency curves measured on several lots;
- first-pass or one-respin silicon history;
- named compiler versions with upstream patches;
- a bug-trend chart that flattened before tape-out.

## A 90-minute meeting

| Minutes | Topic |
|---|---|
| 0–15 | The workload and the claim: which benchmark, which competitor, which operating point |
| 15–35 | Power and the voltage–frequency curve; process corner and temperature |
| 35–55 | Implementation: timing closure, verification coverage, the respin history |
| 55–75 | Software and IP: compilers, ABI, licenses and their change-of-control terms |
| 75–90 | The roadmap against the team's past cadence |

## Documents to request

- Silicon characterization reports: voltage–frequency curves, power by workload, across lots.
- The verification plan with coverage results and bug-trend data.
- The tape-out and respin history with root causes.
- The IP and license register with change-of-control terms.
- Compiler release notes and upstream commit history.

## Go deeper

- The [C2 capstone](../../capstones/C2-digital-design/README.md): RTL to synthesis and timing.
- [28-02](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md): validating benchmark claims.
- [28-07](../../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md): evaluating the team.
