# Problems 24-05 · Interconnect Standards: PCIe, CXL and Ethernet

Chapter: [24-05](../chapters/24-05-pcie-cxl-ethernet.md) · Worked solutions: [24-05 solutions](../solutions/24-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Bandwidth is per direction unless stated, and GB means 10⁹ bytes.
- Encoding efficiencies: 8b/10b 0.8; 128b/130b 128/130; flit TLP space 236/256.
- TLP overhead is 24 bytes (assumed, as in §3.1).
- A DDR5-6400 channel moves 51.2 GB/s over 64 data pins.
- Two-tier fabrics connect $k^2/2$ hosts.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-05-lab/links.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-05.1 [A]

**A PCIe 4.0 x8 link.** *(lab)* Find (a) its bandwidth after encoding and (b) its payload bandwidth with 128-byte TLPs.

### Problem 24-05.2 [A]

**Reading a headline.** PCI-SIG quotes 512 GB/s for PCIe 7.0 x16. (a) What is the flit payload bandwidth in each direction? (b) What fraction of the headline is that?

### Problem 24-05.3 [B]

**Why 8 GT/s?** Compare PCIe 3.0 at 8 GT/s with 128b/130b against a hypothetical 10 GT/s with 8b/10b. Find (a) the per-lane bandwidth of each and (b) each one's NRZ Nyquist frequency. (c) Which would you choose, and why?

### Problem 24-05.4 [B]

**Too few credits.** *(lab)* A PCIe 5.0 x8 receiver has 16 KB of buffer and an 800 ns credit round trip (assumed). Find (a) the raw bandwidth, (b) the bandwidth-delay product, and (c) the fraction of the raw bandwidth the link can sustain and the resulting throughput.

### Problem 24-05.5 [B]

**What retimers cost in buffers.** Two retimers each add 10 ns in each direction (assumed) to a 128 GB/s link. How much more credit buffer does the receiver need?

### Problem 24-05.6 [B]

**CXL 4.0 against DDR5.** Find (a) the flit payload bandwidth of a x16 CXL 4.0 link at 128 GT/s and (b) how many DDR5-6400 channels it equals. (c) Counting both directions over the link's 64 signal wires, compare its bandwidth per wire with a DDR5 channel's per data pin.

### Problem 24-05.7 [B]

**How much can go to the slow tier?** Local DRAM takes 100 ns and CXL memory 200 ns (assumed). What is the largest share of accesses that may go to CXL memory if the average must stay at or below 110 ns?

### Problem 24-05.8 [A]

**800 GbE on two lane rates.** Find the lane count and aggregate line rate of an 800 Gb/s port on (a) 200 Gb/s lanes and (b) 100 Gb/s lanes, and (c) the symbol rate of a 100 Gb/s lane.

### Problem 24-05.9 [B]

**A 102.4 Tb/s switch.** Find the radix and two-tier fabric size at (a) 800 Gb/s and (b) 1.6 Tb/s per port.

### Problem 24-05.10 [C]

**Design a leaf–spine fabric.** Connect 4,096 hosts at 400 Gb/s with full bisection bandwidth using 51.2 Tb/s switch chips. Find (a) the radix, (b) whether two tiers suffice, (c) the number of leaf switches, (d) the number of uplinks and (e) the number of spine switches.

### Problem 24-05.11 [A]

**A longer retry loop.** A 1.6 Tb/s port's link round trip is 2 µs. What replay buffer does link-level retry need?

### Problem 24-05.12 [B]

**Extrapolating PCIe.** If the three-year doubling continued past PCIe 8.0 (256 GT/s, PAM4), a hypothetical next generation would run at 512 GT/s. With PAM4, find (a) its symbol rate, (b) its Nyquist frequency and (c) its UI. This is an extrapolation, not a roadmap.

### Problem 24-05.13 [A]

**GT/s, GBd, GHz.** For PCIe 7.0 at 128 GT/s with PAM4, find (a) the symbol rate, (b) the Nyquist frequency and (c) the UI.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Layers and the PHY's place | 3, 13 |
| 2. Raw and effective bandwidth, packet overhead | 1, 2, 3 |
| 3. Credit and retry buffers | 4, 5, 11 |
| 4. CXL bandwidth and latency | 6, 7 |
| 5. Ethernet lanes and fabric size | 8, 9, 10 |
| 6. Cadence and roadmaps | 12 |
