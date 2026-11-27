# C2 Reference · Design Report: an 8-Tap FIR Block from Arithmetic to Timing

This is the reference solution to [Capstone C2](../README.md), Route 1. Every hand-calculated number below is recomputed by [verify_c2.py](verify_c2.py), which also re-runs the testbench against deliberately broken RTL to show that it catches the bugs. Every synthesis number comes from [synth.py](synth.py) and is tabulated in [results.md](results.md), which CI regenerates and compares.

**Prerequisites used:** [16-06](../../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) (FIR design), [16-10](../../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) (fixed point), [19-10](../../../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md) (synthesis and STA) and [19-13](../../../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md) (verification).

---

## 1. Arithmetic (M1)

**The filter.** The coefficients sum to **32768** = $2^{15}$, so the DC gain is exactly 1. The magnitude response is **−0.93** dB at $f_s/8$, **−6.05** dB at $f_s/4$ and **−18.9** dB at $3f_s/8$. At $f_s/2$ it is exactly zero, as for every even-length symmetric FIR: pairing taps $k$ and $7 - k$, the terms $(-1)^k$ and $(-1)^{7-k}$ cancel. The linear phase gives a constant group delay of **3.5** samples.

**Products.** A 16-bit sample times a 16-bit coefficient is a 32-bit product.

**Accumulator.** The general bound adds $\lceil\log_2 8\rceil$ = 3 bits for eight terms, which with a guard bit gives the 36 bits the RTL uses. The tight bound uses the coefficients themselves. The largest possible sum is $\sum\lvert h_k\rvert \times 2^{15} + 2^{14}$ = **1.194 × 10⁹**, below $2^{31}$ = 2.147 × 10⁹. So a **32**-bit signed accumulator would never overflow. The RTL keeps 36 bits, which is simpler to reason about, at the cost of four bits of adder per partial sum. §6 lists this as the first area saving to take.

**Rounding and saturation.** Adding $2^{14}$ before the 15-bit arithmetic shift rounds half up. Since $\sum\lvert h_k\rvert$ = **36444** exceeds $2^{15}$, the worst-case gain is **1.112**, and a full-scale input with the coefficients' sign pattern drives the output past both rails. Saturation is therefore required, not just defensive.

## 2. Verification plan and golden model (M2)

[golden.py](golden.py) implements the filter with Python integers (no overflow, arithmetic shifts), and writes [stim.hex](stim.hex) and [expected.hex](expected.hex). The stimulus has **476** samples spread over **617** cycles; the **141** idle cycles carry random junk data with `in_valid` low. It covers four cases:

1. an impulse, which reads the coefficients out directly;
2. a step, which checks the DC gain of 1;
3. a worst-case pattern aligned with, then against, the coefficients' signs, which hits $+32767$ **5** times and $-32768$ **5** times;
4. 400 seeded random samples.

[fir_tb.v](fir_tb.v) drives all three RTL versions with the same stimulus. It compares every output in order with the golden model, counts them, and measures each version's latency from the impulse. It prints `TEST PASSED` under Icarus (`tools/run_hdl.py`) and under Verilator ([sim_verilator.py](sim_verilator.py)).

**Does the testbench catch bugs?** A testbench that has never failed proves little. `verify_c2.py` copies the transposed RTL, injects one bug at a time, and checks that the testbench then fails. The three bugs are dropping the rounding constant, removing the saturation, and letting the partial sums advance on idle cycles. All **3** of **3** are caught.

Two real bugs also surfaced during development, both in the verification infrastructure rather than the RTL:

- The golden model's "against the signs" pattern first produced +32768, which wraps to −32768 in 16 bits. All three RTL versions agreed with one another and disagreed with the model, which pointed straight at the model.
- The testbench sampled outputs one edge late, so every latency read one too high.

A third bug was in the RTL: the transposed versions reset only the last partial sum to the rounding constant. In steady state, each partial sum carries the constant exactly once, so after reset the first few outputs lacked it and were off by one least-significant bit. The impulse case caught it.

## 3. Three architectures (M3, M5)

| Version | Structure | Latency (edges) | Distinct multipliers |
|---|---|---|---|
| [fir_direct.v](fir_direct.v) | Delay line, eight products, one adder tree | 2 | 8 |
| [fir_transposed.v](fir_transposed.v) | Each register holds a partial sum; one multiplier and one adder per path | 1 | 4 (symmetry shares them) |
| [fir_pipelined.v](fir_pipelined.v) | Transposed, plus a registered input and registered products | 3 | 4 |

**Multiplier cost by hand.** Constant multipliers become shift-and-add networks, and the canonical signed-digit (CSD) form needs one adder per nonzero digit after the first. The coefficients 169, 750, 3170 and 14133 have **4**, **4**, **5** and **7** nonzero CSD digits, so they cost **3**, **3**, **4** and **6** adders.

- **Direct form:** two copies of each multiplier (**32** adders) plus eight to sum nine terms, **40** adders in all.
- **Transposed form:** one copy of each multiplier (**16** adders) plus eight in the chain, **24** adders.

The hand estimate is therefore a logic area ratio of **0.60**. Synthesis gives **0.635** (§4). Yosys does not use exactly CSD recoding, and the adders differ in width, so this is good agreement for a count of adders.

## 4. Synthesis and timing (M4)

From [results.md](results.md):

| Version | Logic area (µm²) | Register area (µm²) | Area (µm²) | Gates on the critical path | Maximum clock (MHz) | Meets 800 MHz? | Meets 6000 µm²? |
|---|---|---|---|---|---|---|---|
| Direct | **5620.0** | **758.0** | **6378.0** | **70** | **441** | no | no |
| Transposed | **3570.8** | **1304.6** | **4875.4** | **53** | **584** | no | yes |
| Pipelined | **3570.8** | **1937.8** | **5508.6** | **30** | **1025** | yes | yes |

**Reading the table.**

- **Direct form** has the fewest registers (**146**: the delay line and the outputs) but the most logic. Its critical path is a multiplier followed by the whole adder tree (line 21, the sum), **70** gates deep.
- **Transposing** removes the adder tree from the path and halves the multipliers. Logic area falls by **36**%, at the price of wider registers: partial sums are 36 bits, not 16. But a multiplier still feeds an adder in one cycle, which limits it to **584** MHz.
- **Pipelining** puts a register between every multiplier and every adder. The registers cost **633** µm², which brings the total to **5508.6** µm², still inside the budget, and the clock rises to **1025** MHz, meeting the 800 MHz target with **28**% margin.

The final critical path (lines 20 and 23) is the output adder, $p_0 + s_1$, followed by the saturation comparators. No multiplier is on it.

**Latency.** The pipelined version takes **3** edges, inside the 4-edge limit: **3.75** ns at 800 MHz.

## 5. Results against the specification

| Requirement | Result |
|---|---|
| Bit-exact function | 476 of 476 outputs match, for all three versions, under Icarus and Verilator |
| Throughput | One sample per clock (no stalls in any version) |
| Latency ≤ 4 | 3 (pipelined) |
| Clock ≥ 800 MHz | **1025** MHz (period **976** ps) |
| Area ≤ 6000 µm² | **5508.6** µm², a margin of **491** µm² |
| Lint | `verilator --lint-only -Wall` clean on every RTL file |

## 6. Tradeoffs and next steps

| Knob | Improves | Costs |
|---|---|---|
| Transposed form | Removes the adder tree from the critical path; shares the symmetric products | Wider registers (partial sums) |
| Pipelining products | Clock: the multiplier and adder no longer share a cycle | Registers (+**633** µm² here) and two edges of latency |
| Sharing symmetric products | Halves the multipliers | Only in forms where one input feeds all taps (the transposed form) |
| 32-bit accumulator | About 4/36 of the partial-sum adders and registers | A tighter overflow argument that must be re-proved if the coefficients change |

**Next steps:**

- Narrow the accumulator to 32 bits (§1).
- Retime the saturation into its own stage if a higher clock is needed, since it now sits on the critical path.
- For Route 2, take the pipelined version through an open-source place-and-route flow, where wire delay will dominate the teaching library's gate-only model.

**Limits of these numbers.** The teaching library ignores wire capacitance and uses a single delay per gate type, and Yosys's generic mapping is not a commercial mapper. The architecture comparison (direct, then transposed, then pipelined) is robust. The absolute clock and area are not silicon predictions.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| H.sum | sum of the coefficients | 32768 | — |
| H.db8 | magnitude at fs/8 | -0.93 | dB |
| H.db4 | magnitude at fs/4 | -6.05 | dB |
| H.db38 | magnitude at 3fs/8 | -18.9 | dB |
| H.gd | group delay | 3.5 | samples |
| H.accmax | largest accumulator magnitude | 1.194e9 | — |
| H.accbits | accumulator bits needed | 32 | bits |
| H.sumabs | sum of coefficient magnitudes | 36444 | — |
| H.gmax | worst-case gain | 1.112 | — |
| T.samples | samples in the stimulus | 476 | — |
| T.cycles | cycles in the stimulus | 617 | — |
| T.gaps | idle cycles | 141 | — |
| T.sathi | outputs at +32767 | 5 | — |
| T.satlo | outputs at −32768 | 5 | — |
| T.mut | injected bugs caught | 3 | — |
| T.mutn | injected bugs tried | 3 | — |
| A.csd169 | nonzero CSD digits of 169 | 4 | — |
| A.csd750 | nonzero CSD digits of 750 | 4 | — |
| A.csd3170 | nonzero CSD digits of 3170 | 5 | — |
| A.csd14133 | nonzero CSD digits of 14133 | 7 | — |
| A.add169 | adders for 169 | 3 | — |
| A.add750 | adders for 750 | 3 | — |
| A.add3170 | adders for 3170 | 4 | — |
| A.add14133 | adders for 14133 | 6 | — |
| A.muld | multiplier adders, direct form | 32 | — |
| A.totd | adders, direct form | 40 | — |
| A.mult | multiplier adders, transposed form | 16 | — |
| A.tott | adders, transposed form | 24 | — |
| A.ratio | predicted logic-area ratio | 0.60 | — |
| S.ratio | synthesized logic-area ratio | 0.635 | — |
| S.logicsave | logic-area saving of the transposed form | 36 | % |
| S.ffd | flip-flops, direct form | 146 | — |
| S.regcost | register area added by pipelining | 633 | µm² |
| S.fmaxmar | clock margin over 800 MHz | 28 | % |
| S.areamar | area margin under 6000 µm² | 491 | µm² |
| S.lat | latency at 800 MHz | 3.75 | ns |
| S.ld | logic area, direct | 5620.0 | µm² |
| S.rd | register area, direct | 758.0 | µm² |
| S.ad | area, direct | 6378.0 | µm² |
| S.dd | gates on the critical path, direct | 70 | — |
| S.fd | maximum clock, direct | 441 | MHz |
| S.lt | logic area, transposed | 3570.8 | µm² |
| S.rt | register area, transposed | 1304.6 | µm² |
| S.at | area, transposed | 4875.4 | µm² |
| S.dt | gates on the critical path, transposed | 53 | — |
| S.ft | maximum clock, transposed | 584 | MHz |
| S.lp | logic area, pipelined | 3570.8 | µm² |
| S.rp | register area, pipelined | 1937.8 | µm² |
| S.ap | area, pipelined | 5508.6 | µm² |
| S.dp | gates on the critical path, pipelined | 30 | — |
| S.fp | maximum clock, pipelined | 1025 | MHz |
| S.pp | minimum period, pipelined | 976 | ps |
