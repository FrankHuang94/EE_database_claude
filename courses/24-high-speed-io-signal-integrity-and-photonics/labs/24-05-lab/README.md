# Lab 24-05 · Bandwidth, Credits and Fabrics

**Objective.** Compute effective PCIe bandwidth by generation, width and payload; simulate credit-based flow control and confirm the bandwidth-delay rule; and size Ethernet lanes, switch radix and leaf–spine fabrics.

**Chapter:** [24-05 · Interconnect Standards: PCIe, CXL and Ethernet](../../chapters/24-05-pcie-cxl-ethernet.md)

## Background

§3.1 gave the bandwidth per direction, $NR\eta/8$, and the TLP efficiency $P/(P + H)$. §3.2 showed that a credit-flow-controlled link sustains full rate only when its buffer covers the bandwidth-delay product $B\,t_{RTT}$. §3.4 derived the Ethernet lane rate and the $k^2/2$ two-tier fabric size.

## Files

- `links.py`: PCIe rates and encodings, bandwidth and TLP efficiency, an event-driven credit simulator, Ethernet lane rates, radix and fabric sizes, replay-buffer sizing.
- `24-05-links-lab.ipynb`: the notebook for all three parts.

## Procedure

**Part 1 · Bandwidth** (notebook). Tabulate per-lane bandwidth for PCIe 1.0 to 7.0. *Predict* the payload bandwidth of a PCIe 4.0 x8 link with 128-byte TLPs, then compute it.

**Part 2 · Credits** (notebook). Simulate a 128 GB/s link with 256-byte packets for buffers from 8 to 160 KB and credit round trips of 250, 500 and 1,000 ns. *Predict* the throughput with a 32 KB buffer at 500 ns, then read it from the simulation.

**Part 3 · Fabrics** (notebook). *Predict* how many hosts a two-tier fabric of 102.4 Tb/s switches connects at 800 Gb/s per host, then compute it, and compute the lane rate of 200 Gb/s Ethernet.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-05.a | PCIe 4.0 x8 payload bandwidth, 128-byte TLPs | 13.27 | GB/s |
| Lab 24-05.b | throughput with 32 KB at 500 ns | 64 | GB/s |
| Lab 24-05.c | buffer for full rate at 500 ns | 64 | KB |
| Lab 24-05.d | two-tier hosts with 102.4 Tb/s switches at 800G | 8192 | |
| Lab 24-05.e | 200 Gb/s Ethernet lane rate | 212.5 | Gb/s |

- Part 1: PCIe 4.0 x8 carries 15.75 GB/s each way after encoding and 13.27 GB/s of payload with 128-byte TLPs.
- Part 2: the simulated throughput rises in proportion to the buffer and saturates at 128 GB/s once the buffer reaches the bandwidth-delay product: 32, 64 and 128 KB for the three round trips. With 32 KB at 500 ns the link carries 64 GB/s, half its rate.
- Part 3: radix 128 gives 8,192 hosts in two tiers; a 200 Gb/s Ethernet lane runs at 212.5 Gb/s.

## Discussion

1. Why does the simulated throughput grow linearly with the buffer below the bandwidth-delay product?

   <details><summary>Answer</summary>

   With $C$ credits of $S$ bytes, at most $CS$ bytes can be in flight, and each credit returns once per round trip. So the sender delivers $CS$ bytes per $t_{RTT}$, a throughput of buffer$/t_{RTT}$, until that exceeds the link rate.

   </details>

2. A link adds a retimer that adds 20 ns to the round trip. Which links suffer most?

   <details><summary>Answer</summary>

   The fastest ones with the tightest buffers: the extra buffer needed is bandwidth × 20 ns, which doubles with each generation, so a buffer sized for the old round trip falls short by more at higher rates.

   </details>

3. Why does a two-tier fabric hold $k^2/2$ hosts rather than $k^2$?

   <details><summary>Answer</summary>

   For full bisection bandwidth each leaf must send as much up to the spines as it receives from its hosts, so only half its $k$ ports face hosts. There can be at most $k$ leaves, one per spine port, giving $k \times k/2$ hosts.

   </details>

## Optional hardware

On a Linux machine, `lspci -vv` reports each PCIe device's negotiated link speed and width (LnkSta) and its maximum payload size (DevCtl MaxPayload). Comparing them with this lab's numbers shows what a real link delivers.
