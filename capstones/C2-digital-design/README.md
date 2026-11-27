# Capstone C2 · Digital Design: RTL to Verified, Synthesized Block

**Brief.** Design an 8-tap FIR filter block for a sensor front end: RTL that is bit-exact against a golden model, a self-checking testbench, and synthesis and timing results that meet an area and a clock target. Then take it as far toward layout as your tools allow.

| | |
|---|---|
| **Prerequisites** | [Course 19](../../courses/19-digital-vlsi-design/README.md) (synthesis, STA, verification), with [Course 16](../../courses/16-digital-signal-processing/README.md) for the filter arithmetic and [Course 08](../../courses/08-digital-logic-design/README.md) for RTL |
| **Estimated hours** | About 50 |
| **Tools** | Icarus Verilog and Verilator (simulation and lint), Yosys (synthesis, from PyPI as `yowasp-yosys`), Python with numpy; optionally an open-source RTL-to-GDS flow |
| **Deliverables** | RTL, golden model, self-checking testbench, synthesis and timing reports, design report |

The two routes in the [capstone list](../README.md) are:

- **Route 1 (the reference):** RTL, a passing testbench under Verilator, and a synthesis report. Everything runs in CI.
- **Route 2 (an extension):** take the same block through an open-source place-and-route flow such as OpenLane with the SkyWater 130 nm PDK, and add layout, DRC/LVS and post-route timing to the deliverables. The repository has not verified that flow's current installation steps (open issue 4 in [PROGRESS.md](../../PROGRESS.md)), so follow the flow's own documentation, and expect the post-route clock to be well below the teaching library's numbers.

---

## Specification

**Function.** $y[n] = \text{sat}_{16}\big((\sum_{k=0}^{7}h_kx[n - k] + 2^{14}) \gg 15\big)$: an arithmetic right shift (round half up), then saturation to the 16-bit two's-complement range. The coefficients are fixed, in Q1.15:

$$
h = [-169,\ -750,\ 3170,\ 14133,\ 14133,\ 3170,\ -750,\ -169].
$$

They are symmetric, sum to exactly $2^{15}$ (unity DC gain), and form a low-pass filter with its −6 dB point at $f_s/4$. The output must match the golden model ([reference/golden.py](reference/golden.py)) bit for bit.

**Interface.**

| Port | Direction | Meaning |
|---|---|---|
| `clk` | in | Rising-edge clock |
| `rst` | in | Synchronous reset, active high |
| `in_valid`, `in_data[15:0]` | in | A signed sample, accepted on every clock edge where `in_valid` is high |
| `out_valid`, `out_data[15:0]` | out | One output per accepted sample, in order |

The delay line advances only on accepted samples, so gaps in `in_valid` must not change the outputs.

**Targets** (in the C2 teaching library, as measured by [reference/synth.py](reference/synth.py)):

| Requirement | Target |
|---|---|
| Throughput | One sample per clock |
| Latency | ≤ 4 clock edges from the accepting edge to the output register |
| Clock | ≥ 800 MHz (minimum period ≤ 1250 ps) |
| Area | ≤ 6000 µm² |
| Verification | Self-checking testbench, bit-exact on an impulse, a step, inputs that drive the output to both saturation limits, seeded random data and random input gaps; passes under Icarus and Verilator; `verilator --lint-only -Wall` clean |

**The teaching library.** `synth.py` maps Yosys's generic gates onto a small library of round-number areas and delays (an XOR or mux costs about two NANDs, a flip-flop about seven), and runs its own static timing analysis on the netlist. It stands in for a foundry Liberty file and timing tool; use it to compare architectures, not to quote silicon speeds.

## Milestones

| # | Milestone | Output | Hours |
|---|---|---|---|
| M1 | **Arithmetic.** Fix every word length (products, accumulator, output), the rounding and the saturation; prove that the accumulator cannot overflow | One page with the bounds | 4 |
| M2 | **Golden model and test plan.** A bit-exact model in Python and the vectors it writes; the cases you will cover and why | `golden.py`, vectors, test plan | 6 |
| M3 | **First RTL.** The straightforward (direct-form) architecture, passing the testbench and lint | RTL, testbench | 12 |
| M4 | **Synthesis and timing.** Synthesize; find the critical path; compare area and clock with the targets | Reports | 8 |
| M5 | **Architecture iterations.** Change the architecture (not the testbench) until both targets are met; keep every version passing | RTL versions, a comparison table | 12 |
| M6 | **Report.** Decisions, results, the critical path of the final design, and what you would do next | Report of 8 to 12 pages | 8 |

## Rubric (100 points)

| Criterion | Points | Full credit |
|---|---|---|
| Arithmetic and word lengths | 15 | Every width justified by a bound; rounding and saturation exactly as specified |
| Verification | 25 | Bit-exact on every case; gaps and both saturation limits covered; the testbench fails when a bug is injected (show one) |
| RTL quality | 15 | Lint-clean, synchronous, readable; latency documented |
| Synthesis and timing | 20 | Both targets met; critical path identified and explained in RTL terms |
| Architecture reasoning | 15 | At least two architectures compared with numbers; the choice follows from them |
| Report | 10 | Reproducible (scripts run as delivered), with tradeoffs and next steps |

## Running the reference

In [reference/](reference/):

```bash
python golden.py
```

```bash
python sim_verilator.py
```

```bash
python synth.py --check
```

`golden.py` rewrites the test vectors; `sim_verilator.py` builds and runs the testbench with Verilator; `synth.py` synthesizes all three versions and compares with [reference/results.md](reference/results.md). The Icarus run is part of `tools/run_hdl.py`, and the hand calculations in the report are checked by `tools/run_verify.py C2`. Install Yosys with `pip install yowasp-yosys==0.71.0.0.post1285` (the version CI pins, so the results reproduce exactly).

**Reference solution:** [design report](reference/design-report.md) and [synthesis results](reference/results.md). Open them only after your own design passes, or when you are stuck at a milestone.
