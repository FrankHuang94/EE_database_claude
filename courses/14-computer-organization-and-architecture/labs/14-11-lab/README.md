# Lab 14-11 · I/O, Buses and Interconnect

Chapter: [14-11 I/O, Buses and Interconnect](../../chapters/14-11-io-buses-and-interconnect.md)

## Objective

See the valid/ready handshake at the level of individual clock cycles, by driving a small AXI4-Lite register block from a self-checking testbench. Then use simple models to compare polling, interrupts and DMA, and to compute the distances inside a mesh network-on-chip.

## Background

Memory-mapped registers (§3.1), polling and interrupts (§3.2), DMA (§3.3), the AXI handshake and Little's law (§3.4), meshes (§3.5) and serial links (§3.6).

## Tools

Icarus Verilog (`iverilog`, `vvp`), with GTKWave optional for waveforms; Python.

## Files

- [axil_regs.v](axil_regs.v): an AXI4-Lite subordinate with CTRL, DATA, STATUS (read-only, cleared-on-read pending flag and a write counter) and SCRATCH registers, and an interrupt output.
- [axil_regs_tb.v](axil_regs_tb.v): a self-checking manager. It performs 8 writes and 8 reads, a write whose response is accepted 3 cycles late, the interrupt sequence and a refused write to the read-only register. It prints the measured cycles and `TEST PASSED`.
- [io_models.py](io_models.py): UART timing, event overheads, link bandwidth, Little's law and mesh hop counts by enumeration.

Run the testbench with `python tools/run_hdl.py 14-11` from the repository root, or directly from the course directory:

```bash
iverilog -g2012 -o axil labs/14-11-lab/axil_regs_tb.v labs/14-11-lab/axil_regs.v && vvp axil
```

## Procedure

1. **The handshake (Part 1).** Run the testbench and, with `$dumpvars` added, view a write: AWVALID/WVALID and AWREADY/WREADY high in the same cycle, then BVALID the next cycle. *Predict first:* how many cycles does a write take when the manager delays BREADY by 3 cycles?
2. **More throughput (Part 2).** Modify the subordinate to accept a new write in the cycle in which the previous response is accepted, and update the testbench's expected counts. What is the new cycles-per-write?
3. **Overheads (Part 3).** With `io_models.overhead_fraction`, plot the CPU fraction spent on polling (fixed rate) and on interrupts (per event) against the event rate, and find the crossover of Problem 14-11.4.
4. **Meshes (Part 4).** Enumerate `io_models.mesh_hops(k)` for $k$ = 2 to 16, and compare with $2(k^2 - 1)/(3k)$.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Handshake | 16 cycles for 8 writes, 16 for 8 reads, 5 for the stalled write; the interrupt rises on a DATA write and clears when STATUS is read |
| 2 | Overlapped responses | 1 cycle per write when the manager is always ready |
| 3 | Crossover | polling every 10 µs at 100 cycles beats 1500-cycle interrupts above 6667 events/s |
| 4 | Mesh | 2.5 hops at 4 × 4, 5.25 at 8 × 8, 10.625 at 16 × 16, exactly the closed form |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-11.a | cycles, 8 writes | 16 | — |
| Lab 14-11.b | cycles, 8 reads | 16 | — |
| Lab 14-11.c | cycles, write with BREADY 3 cycles late | 5 | — |
| Lab 14-11.d | average hops, 16 × 16 mesh | 10.625 | — |
| Lab 14-11.e | crossover event rate | 6667 | /s |

*These are recomputed by [verify_14_11.py](../../verify/verify_14_11.py), which also runs the testbench when Icarus Verilog is installed.*

## Discussion questions

1. Why must a VALID signal never depend on READY, while a READY may depend on VALID?
2. The register block refuses a write to STATUS with SLVERR. Why respond at all, rather than ignore the write silently?
3. Why does reading STATUS clear the pending flag, and what race does that create if two pieces of software poll it?

### Answers

1. If both sides waited for the other, neither would ever raise its signal: a deadlock. The rule gives one side, the sender, the obligation to go first. The receiver may then decide, even combinationally, whether to accept what is offered.
2. Every AXI write must receive exactly one response, or the manager waits forever. An error response also tells software it has made a mistake, which a silent ignore would hide.
3. Clear-on-read lets an interrupt handler acknowledge the event with a single access. But if two readers poll the register, the first read consumes the event and the second never sees it. Drivers therefore use one reader, or write-one-to-clear registers, which make the acknowledgement explicit.

## Optional hardware extension

On a Linux machine, watch the interrupt counts per device in `/proc/interrupts` while generating network or disk traffic, and look for the coalescing settings of a network card with `ethtool -c`.
