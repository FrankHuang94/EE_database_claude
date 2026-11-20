<!-- status: verified -->
# 14-11 · I/O, Buses and Interconnect

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The input/output and interconnect unit of a computer organization course: memory-mapped I/O, polling and interrupts, DMA, buses and their protocols, on-chip networks, and serial links such as PCI Express (Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 6 (online sections on I/O); Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, App. D and F) |
| **Prerequisites** | [14-10 Virtual Memory, TLBs and the OS Interface](14-10-virtual-memory.md) (traps and interrupts), [14-09 Memory Hierarchy and Caches](14-09-memory-hierarchy-and-caches.md) (Little's law and bandwidth) |
| **Estimated study hours** | 5 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain how software controls devices through memory-mapped registers, and why those accesses must bypass the caches and keep their order.
2. Compare polling, interrupts, interrupt coalescing and DMA by the CPU time they cost and the latency they add.
3. Describe a valid/ready handshake bus such as AXI, and compute its throughput and the outstanding transactions it needs, using Little's law.
4. Estimate the hop count, latency and bisection bandwidth of a mesh network-on-chip.
5. Compute the bandwidth of a serial link such as PCI Express from its transfer rate, lane count and encoding, and place PCIe and CXL generations on a timeline.

---

## 1. Big picture

A processor is useless without input and output: storage, networks, displays, sensors and accelerators. They differ enormously in speed, from a keyboard producing ten events a second to a network port delivering a packet every few nanoseconds. Inside a chip, cores, caches, memory controllers and accelerators must also exchange data at hundreds of gigabytes per second. This chapter is a survey of the mechanisms that connect them, at the depth needed to reason about a system's bottlenecks:

- **Memory-mapped I/O** lets ordinary loads and stores control devices.
- **Interrupts and DMA** keep the processor from wasting time waiting on slow devices or copying data byte by byte.
- **On-chip buses and networks** (AXI, meshes) carry the traffic inside a system-on-chip.
- **Serial links** such as PCI Express connect chips and cards, and they set the bandwidth of every GPU, SSD and network card in a server.

Deeper treatments of the physical links are in [24-03](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) and [24-05](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md), and of microcontroller peripherals in [18-03](../../18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md) and [18-04](../../18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md).

> **Deeper:** see companion repo *Datacenter Networking* for networks between servers.

## 2. Intuition first

**An office building.** Each department (device) has a mailbox at a known address (its registers). To ask for something, you put a note in the box (a store); to see the answer, you look in the box (a load).

- You can walk to the box every few minutes to check (**polling**).
- You can ask the department to ring your phone when it is done (an **interrupt**).
- For bulk deliveries you hire a courier who moves the boxes and calls you at the end (**DMA**).
- The building's corridors are the **bus** or **network**: everyone shares them, and their width and the number of deliveries in progress at once set the throughput.

**Where the analogy breaks.** Mailboxes in a computer have side effects: reading a device's register can change it (it clears a flag or pops a byte from a queue), so such reads must never be repeated, reordered or served from a cache. Corridors carry signals that follow strict handshake rules, which is why designers can connect blocks from different companies and have them work.

## 3. Theory

### 3.1 Talking to devices: memory-mapped I/O

A device presents a few **registers**, typically control (what to do), status (what happened) and data (a byte or word to transfer). In **memory-mapped I/O**, these registers occupy physical addresses, and the processor reads and writes them with ordinary loads and stores. RISC-V, Arm and most modern systems use only memory mapping; x86 also keeps a separate I/O-port space.

Device registers are not memory, so they need three precautions:

- **No caching.** The page tables or platform attributes mark device regions uncacheable, so every access reaches the device.
- **No reordering or merging.** A write to "start" must not overtake the write that set up the parameters. Device regions are strongly ordered, and software adds fences where the architecture allows reordering.
- **No compiler tricks.** In C, device registers are accessed through `volatile` pointers, so the compiler performs every access, in order ([05-07](../../05-programming-for-engineers/chapters/05-07-bit-manipulation.md)).

### 3.2 Polling and interrupts

How does software learn that a device needs attention?

- **Polling:** read the status register repeatedly. It is simple, and its response is fast if the loop is tight, but every poll that finds nothing is wasted. Its cost per second is (polls per second) × (cycles per poll), whether or not anything happens.
- **Interrupts:** the device raises an interrupt line, and the processor traps to a handler (14-10). It costs nothing when idle, but each event pays a fixed overhead: the trap, saving and restoring registers, the handler, and the cache and TLB disturbance. That is typically hundreds to thousands of cycles. Its cost per second is (events per second) × (cycles per interrupt).

Interrupts win for infrequent events, and polling wins when events arrive faster than the interrupt overhead can sustain. High-rate devices such as network cards use **interrupt coalescing**: one interrupt for every $n$ packets or after a timeout, whichever comes first, trading latency for CPU time (Example 14-11.2). The extreme is dedicating cores to busy polling, as some high-performance network software does.

### 3.3 Direct memory access

Moving a block of data with loads and stores (**programmed I/O**) occupies the core for every word, and device registers are slow, uncached accesses. A **DMA engine** moves the data instead:

1. Software writes a **descriptor**: source, destination, length, and often a pointer to the next descriptor, so that a chain of descriptors can gather scattered buffers (**scatter-gather**).
2. The DMA engine performs the transfer as a bus manager, while the core does other work.
3. The engine raises an interrupt when it finishes.

DMA writes into memory that the CPU may have cached, so the system must keep the two consistent. Either the DMA is **coherent** (the interconnect snoops the caches, 14-12), or the driver flushes and invalidates the affected lines before and after the transfer. A forgotten invalidate is a classic driver bug: the CPU reads stale data from its cache while the fresh data sits in memory.

### 3.4 Buses and the valid/ready handshake

A **bus** connects **managers** (which start transactions: cores, DMA engines) to **subordinates** (which respond: memories, device registers). Arm's AMBA AXI is a widely used on-chip bus protocol, and Arm describes the AMBA specifications as "royalty free" [1, R-217]. AXI has five independent channels [1, R-217]:

| Channel | Direction | Carries |
|---|---|---|
| AW | manager → subordinate | write address |
| W | manager → subordinate | write data |
| B | subordinate → manager | write response |
| AR | manager → subordinate | read address |
| R | subordinate → manager | read data and response |

Every channel uses the same **valid/ready handshake**:

- The sender drives the information and raises VALID.
- The receiver raises READY when it can accept.
- A transfer happens on each clock edge where both are high.
- A sender must not wait for READY before raising VALID, which rules out deadlock: either side may stall, but the protocol cannot hang with each side waiting for the other.
- Once a sender raises VALID, it must keep VALID high, and its information unchanged, until the transfer happens. It cannot withdraw or alter an offer the receiver may be about to take.

The lab's AXI4-Lite register block (§3.7) accepts one write or read every 2 cycles. Full AXI adds **bursts** (one address, many data beats) and **IDs**, which let a manager keep many transactions **outstanding** and lets responses return out of order. As with caches (14-09), Little's law sets the bandwidth:

$$
\text{bandwidth} = \frac{\text{outstanding transactions} \times \text{bytes per transaction}}{\text{latency}}.
$$

A bus's **peak** bandwidth is its data width times its clock frequency. Delivered bandwidth is lower: handshake bubbles, arbitration between managers, turnaround and protocol overhead all take cycles.

### 3.5 Networks-on-chip

A single shared bus serializes all traffic, and a full crossbar's area grows as the square of the number of ports. Large chips therefore use a **network-on-chip (NoC)**: routers connected by point-to-point links, often in a 2D **mesh**. A packet travels from router to router, so latency grows with the number of hops. For uniform random traffic on a $k \times k$ mesh with dimension-ordered routing, the average hop count, including pairs where source and destination coincide, is

$$
\bar{H} = \frac{2(k^2 - 1)}{3k} \approx \frac{2k}{3}.
$$

(The average distance along one dimension is $(k^2-1)/(3k)$; the two dimensions add.) The **bisection bandwidth** is the capacity of the links that cross a cut splitting the chip in half. For a mesh it is $k$ links in each direction, so it grows only as the square root of the number of nodes. That is why traffic patterns matter on many-core chips (14-12).

> **Math refresher — average distance on a line.** For positions $i, j$ chosen independently and uniformly from $0, \ldots, k-1$, $E|i - j| = \frac{1}{k^2}\sum_{i,j}|i-j| = \frac{2}{k^2}\sum_{d=1}^{k-1} d\,(k-d) = \frac{k^2-1}{3k}$. The sum counts, for each distance $d$, the $k - d$ pairs at that distance in each order.

### 3.6 Serial links: PCI Express and CXL

Off-chip, wide parallel buses gave way to **serial links**: a few differential pairs per direction (**lanes**), each running at many gigatransfers per second, with the clock recovered from the data ([24-03](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md)). A link's bandwidth in one direction is

$$
\text{BW} = \frac{\text{rate (GT/s)} \times \text{lanes} \times \text{encoding efficiency}}{8} \;\text{GB/s}.
$$

The line **encoding** costs a fraction of the raw rate:

- 8b/10b (efficiency 0.8) in PCIe 1.0 and 2.0;
- 128b/130b (0.985) from PCIe 3.0 [2, R-216];
- PAM4 signalling with fixed-size **Flits** and forward error correction from PCIe 6.0 [3, R-216].

PCI-SIG doubles the rate roughly every three years [3, R-216]:

| Generation | Rate per lane | Encoding | Date |
|---|---|---|---|
| PCIe 2.0 | 5.0 GT/s | 8b/10b | 2006 |
| PCIe 3.0 | 8.0 GT/s | 128b/130b | — |
| PCIe 4.0 | 16.0 GT/s | 128b/130b | Oct 2017 |
| PCIe 5.0 | 32.0 GT/s | 128b/130b | May 2019 |
| PCIe 6.0 | 64 GT/s | PAM4, Flit, FEC | Jan 2022 |
| PCIe 7.0 | 128.0 GT/s | PAM4, Flit (R-216 records these two) | Jun 2025 |
| PCIe 8.0 | 256.0 GT/s (target) | — | planned by 2028 |

PCI-SIG quotes bidirectional totals: "up to 256 GB/s via x16" for PCIe 6.0 is 64 GT/s × 16 lanes × 2 directions / 8, before Flit and FEC overhead [3, R-216].

**CXL (Compute Express Link)** runs on the PCIe physical layer but adds protocols for cache-coherent access to devices and their memory, which allows memory expansion and pooling. CXL 4.0 (November 2025) doubles its rate from 64 to 128 GT/s [4, R-217]. PCIe, CXL and Ethernet are compared in depth in [24-05](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md).

### 3.7 The lab's models

The lab has two parts:

- `axil_regs.v` is a small AXI4-Lite subordinate with four registers and an interrupt output. Its self-checking testbench, `axil_regs_tb.v`, measures cycles per transaction and exercises the error response and the interrupt.
- `io_models.py` evaluates the overhead formulas of §3.2–3.3 and computes mesh hop counts by enumerating every source–destination pair.

## 4. Worked examples

### Example 14-11.1 · Polling a UART (tier A)

**Setup.** A microcontroller at 100 MHz sends 1000 bytes through a UART at 115,200 baud with 8N1 framing (a start bit, 8 data bits and a stop bit). It polls the "transmitter empty" flag before writing each byte. How long does the transfer take, and how many CPU cycles are spent waiting?

**Solution.** Each character is 10 bits, so it takes $10 / 115200 = 86.8$ µs. 1000 bytes take **86.8** ms. The CPU spends essentially all of that time in the polling loop: $0.0868 \times 10^8 \approx$ **8.68** million cycles, to move 1000 bytes.

**Units check.** bits / (bits/s) = s; s × cycles/s = cycles.

**Sanity check.** At 100 MHz the core could execute about 8,700 instructions per byte sent. That is the case for an interrupt or a DMA channel even on a microcontroller.

### Example 14-11.2 · Interrupts at network rates (tier B)

**Setup.** A 1 Gb/s network port receives back-to-back 1500-byte packets (ignore the preamble and inter-frame gap that Ethernet adds on the wire; they lower the packet rate slightly). Each interrupt costs 2000 cycles on a 3 GHz core. (a) What fraction of the core do per-packet interrupts consume? (b) With coalescing of 32 packets per interrupt? (c) What latency can coalescing add?

**Solution.**

(a) Packets arrive at $10^9 / (1500 \times 8) = 83{,}333$ per second. The overhead is $83{,}333 \times 2000 / (3 \times 10^9)$ = **5.56**% of a core, before any protocol processing.

(b) With one interrupt per 32 packets, $2604$ interrupts per second cost **0.174**%.

(c) A packet may wait for 31 more to arrive. Each takes 12 µs on the wire, so the first can wait up to $31 \times 12$ = **372** µs. Real drivers add a timeout to cap that.

**Units check.** packets/s × cycles/packet / (cycles/s) = fraction.

**Sanity check.** At 100 Gb/s the per-packet rate is 100 times higher: per-packet interrupts would need several cores, which is why fast network cards coalesce, poll, and spread queues over cores.

### Example 14-11.3 · DMA against programmed I/O (tier B)

**Setup.** A driver must move 4 KiB from a device buffer to memory. With programmed I/O, each 4-byte uncached load from the device takes 50 cycles. With DMA, setting up a descriptor takes 300 cycles of CPU time and the completion interrupt 2000. Compare the CPU cycles. If the DMA is not coherent and lines are 64 bytes, how many lines must the driver invalidate?

**Solution.**

- **Programmed I/O:** $4096 / 4 = 1024$ loads × 50 cycles = **51,200** cycles, plus the stores.
- **DMA:** $300 + 2000$ = **2300** cycles of CPU time, **95.5**% less, and the core is free during the transfer.
- **Coherence:** without coherent DMA, the driver invalidates $4096 / 64$ = **64** cache lines covering the buffer (assuming the buffer is 64-byte aligned; otherwise it touches one more line, **65**), so that later loads fetch the new data from memory.

**Units check.** Cycles; lines = bytes / bytes per line.

**Sanity check.** For a 64-byte transfer, DMA's fixed 2300 cycles would cost more than 16 loads of 50 cycles (800 cycles). Small transfers are often done by programmed I/O.

### Example 14-11.4 · An AXI4-Lite register block (tier B)

**Setup.** The lab's AXI4-Lite subordinate runs at 100 MHz. Its testbench measures 16 cycles for 8 back-to-back 32-bit writes, 16 cycles for 8 reads, and 5 cycles for one write whose response the manager accepts 3 cycles late. (a) What is the throughput of register writes in MB/s? (b) A full AXI port with 64-byte bursts sees 200 ns of latency to memory. How many transactions must be outstanding to sustain 16 GB/s?

**Solution.**

(a) Each write takes 16/8 = **2** cycles, one for the address and data handshake and one for the response. That gives 4 bytes per 20 ns = **200** MB/s. A late response stretches the write to $2 + 3$ = **5** cycles, because this subordinate accepts no new write while a response is pending.

(b) By Little's law, $16 \times 10^9 \times 200 \times 10^{-9} / 64$ = **50** transactions in flight. This is why full AXI has transaction IDs, which let responses return out of order. AXI4-Lite has no IDs, so its responses must return in order. It does not forbid several outstanding transactions, but a subordinate may limit them with READY, and the lab's block accepts one at a time.

**Units check.** bytes / s; (bytes/s × s) / bytes = transactions.

**Sanity check.** AXI4-Lite is meant for control registers, where 200 MB/s is ample. Bulk data uses full AXI with bursts.

### Example 14-11.5 · A mesh NoC and a PCIe link (tier B)

**Setup.** (a) An 8 × 8 mesh NoC has 3-cycle routers and 1-cycle links. Find the average hop count and the average zero-load latency for uniform traffic, counting each hop as a router plus a link. Find the bisection bandwidth with 32-byte links at 2 GHz. (b) Find the per-direction bandwidth of a PCIe 3.0 x16 link, and the raw per-direction bandwidth of a PCIe 6.0 x16 link.

**Solution.**

(a) $\bar{H} = 2(64 - 1)/(3 \times 8)$ = **5.25** hops, confirmed by enumerating all 4096 pairs. The latency is $5.25 \times (3 + 1)$ = **21** cycles. The bisection has 8 links in each direction: $8 \times 32 \text{ B} \times 2 \times 10^9$ = **512** GB/s per direction.

(b) PCIe 3.0: $8 \times 16 \times (128/130) / 8$ = **15.75** GB/s per direction. PCIe 6.0: $64 \times 16 / 8$ = **128** GB/s raw per direction, the "256 GB/s" bidirectional figure of the PCI-SIG release.

**Units check.** GT/s × lanes / (bits per byte) = GB/s.

**Sanity check.** Three generations (eight times the rate) take the x16 link from about 16 to 128 GB/s per direction.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-11.1a | time per character | 86.8 | µs |
| Ex 14-11.1b | transfer time | 86.8 | ms |
| Ex 14-11.1c | CPU cycles spent polling | 8.68 | million |
| Ex 14-11.2a | packets per second | 83333 | /s |
| Ex 14-11.2b | overhead, per-packet interrupts | 5.56 | % |
| Ex 14-11.2c | overhead, coalescing 32 | 0.174 | % |
| Ex 14-11.2d | added latency, worst case | 372 | µs |
| Ex 14-11.3a | CPU cycles, programmed I/O | 51200 | — |
| Ex 14-11.3b | CPU cycles, DMA | 2300 | — |
| Ex 14-11.3c | saving | 95.5 | % |
| Ex 14-11.3d | lines to invalidate | 64 | — |
| Ex 14-11.3e | lines, unaligned buffer | 65 | — |
| Ex 14-11.4a | cycles per write | 2 | — |
| Ex 14-11.4b | write throughput | 200 | MB/s |
| Ex 14-11.4c | cycles, late response | 5 | — |
| Ex 14-11.4d | outstanding transactions for 16 GB/s | 50 | — |
| Ex 14-11.5a | average hops, 8 × 8 mesh | 5.25 | — |
| Ex 14-11.5b | average zero-load latency | 21 | cycles |
| Ex 14-11.5c | bisection bandwidth per direction | 512 | GB/s |
| Ex 14-11.5d | PCIe 3.0 x16 per direction | 15.75 | GB/s |
| Ex 14-11.5e | PCIe 6.0 x16 raw per direction | 128 | GB/s |

## 5. Simulate it

The lab, [labs/14-11-lab](../labs/14-11-lab/README.md), has the AXI4-Lite register block with its self-checking testbench, run with Icarus Verilog, and `io_models.py`. You:

1. **Run the testbench** and read the waveform of a write, a read, a stalled response and the interrupt.
2. **Change the subordinate** so that it can accept a new write while the previous response is still waiting, and measure the throughput again.
3. **Explore the overhead models** for polling, interrupts and coalescing at different event rates, and find the crossover.
4. **Enumerate mesh distances** for $k$ = 2 to 16 and compare with the closed form.

**Guided exercise (predict, then run).** **Before Part 1,** predict how many cycles a write takes if the manager holds BREADY low for 3 cycles. (5: the subordinate holds BVALID until the handshake and accepts no new write meanwhile.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Polling against interrupts | Latency (polling), idle CPU time (interrupts) | Wasted polls; per-event overhead | Driver and firmware engineers |
| Interrupt coalescing | CPU time at high event rates | Added latency | Network and storage driver engineers |
| DMA | CPU time, bandwidth for bulk data | Setup cost, coherence handling, engine area | SoC architect, driver engineer |
| Bus width and clock | Peak bandwidth | Wires, area, power, timing closure | SoC architect |
| Outstanding transactions (IDs, queues) | Delivered bandwidth at high latency | Buffering, ordering logic | Interconnect architect |
| Mesh NoC against crossbar or bus | Scalability to many nodes | Hop latency, router area and power | SoC architect |
| Link generation and width (PCIe lanes) | Off-chip bandwidth | SerDes power and area, board cost, signal integrity | Platform architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| UART, 8N1 | 10 bits per byte; 115,200 baud ≈ 11.5 kB/s | Example 14-11.1 |
| Interrupt overhead | hundreds to thousands of cycles per interrupt | §3.2 |
| AXI channels | AW, W, B, AR, R, each with VALID/READY | [1, R-217] |
| Mesh average hops | $2(k^2-1)/(3k) \approx 2k/3$ | §3.5 |
| PCIe encodings | 8b/10b (1.0–2.0), 128b/130b (3.0–5.0), PAM4 with Flits (6.0+) | [2, 3, R-216] |
| PCIe per-lane rates | 8, 16, 32, 64, 128 GT/s for 3.0 to 7.0; 256 GT/s target for 8.0 | [2, 3, R-216] |
| CXL 4.0 | 128 GT/s (Nov 2025) | [4, R-217] |

## 8. Common mistakes

- **Caching device registers.** A cached status register never changes. Device regions must be uncacheable and strongly ordered.
- **Forgetting `volatile`.** The compiler may delete a polling loop's repeated reads, or merge writes to a device.
- **Interrupting per event at high rates.** The fixed overhead per interrupt can consume whole cores. Coalesce or poll.
- **Ignoring DMA coherence.** Without coherent DMA, stale cache lines hide the newly transferred data.
- **Quoting bidirectional bandwidth as one-way.** "256 GB/s" for PCIe 6.0 x16 is both directions together, and before Flit and FEC overhead.
- **Assuming a VALID may wait for READY.** In AXI it must not; designs that do can deadlock.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **AXI keeps evolving.** Arm's AXI specification is at Issue L (August 2025), which covers AXI5 and adds options such as a credited transport [1, R-217] **[Established]**.
- **PCIe doubling continues.** PCIe 7.0 (128 GT/s) was released to members in June 2025, and PCIe 8.0 (256 GT/s) is planned for release to members by 2028 [3, R-216] **[Established]** (from PCI-SIG releases, read as reprints).
- **CXL for memory expansion.** CXL 4.0 (November 2025) runs at 128 GT/s and adds bundled ports [4, R-217] **[Established]**. How widely CXL-attached memory is deployed in production is outside this chapter's sources.

### Why it matters commercially

- **I/O sets accelerator performance.** A GPU or AI accelerator fed over PCIe is limited by the link whenever data does not stay on the device, which is why accelerators also have dedicated scale-up links ([24-06](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).
- **Interconnect is IP that is licensed or built.** On-chip fabrics and SerDes are major licensable IP categories, and their quality decides whether an SoC meets its bandwidth.

### Marketing vs Reality

- **"X GB/s link."** *Reality:* often a bidirectional raw figure. *Sanity check:* ask for one-way delivered bandwidth after encoding, Flit and protocol overhead, at the packet sizes you use.
- **"Low-latency interrupts."** *Reality:* the hardware path is short, but software overhead dominates. *Sanity check:* ask for measured end-to-end latency and CPU cost per event at your event rate.

### Questions for engineering leaders

1. **"Where is the bottleneck between the accelerator and its data?"**
   *Strong:* measured link utilization, transfer sizes, and overlap with compute. *Evasive:* the link's peak rate.
2. **"How many outstanding transactions do your fabric ports support, and at what latency?"**
   *Strong:* specific numbers, with the Little's-law bandwidth they imply. *Evasive:* "enough".
3. **"How is DMA kept coherent with the caches?"**
   *Strong:* hardware coherence, or a clear driver discipline with tests. *Evasive:* silence.
4. **"How do you verify interconnect protocol compliance?"**
   *Strong:* protocol checkers, formal properties for handshake rules, interoperability testing. *Evasive:* "it works in simulation".

## 10. Concept check

**Q1.** Why must device registers be uncacheable?

<details><summary>Answer</summary>

Their values change independently of the processor, and reads or writes can have side effects. A cached copy would return stale status, and a cached write might never reach the device or reach it out of order.

</details>

**Q2.** When does polling beat interrupts?

<details><summary>Answer</summary>

When events are frequent enough that the per-interrupt overhead exceeds the cost of polling, or when the lowest latency matters and a core can be dedicated to the device.

</details>

**Q3.** What does a DMA engine do, and what problem does it create?

<details><summary>Answer</summary>

It moves data between devices and memory without the CPU, interrupting when done. Because it writes memory behind the caches' backs, the system needs coherent DMA or explicit cache maintenance.

</details>

**Q4.** What is the AXI handshake rule that prevents deadlock?

<details><summary>Answer</summary>

A transfer occurs when VALID and READY are both high, and a sender may not wait for READY before asserting VALID; so the two sides can never wait on each other.

</details>

**Q5.** Why do large chips use meshes instead of one bus?

<details><summary>Answer</summary>

A shared bus serializes all traffic, and a crossbar grows as the square of the ports. A mesh scales by adding routers and links, at the cost of latency that grows with hop count.

</details>

**Q6.** What three factors give a PCIe link's bandwidth?

<details><summary>Answer</summary>

The transfer rate per lane, the number of lanes, and the encoding efficiency (plus, from PCIe 6.0, Flit and FEC overhead), divided by 8 bits per byte, for each direction.

</details>

Now work the [problem set](../problems/14-11-problems.md).

## 11. Key terms

[Memory-mapped I/O](../../../reference/glossary.md#memory-mapped-i-o) · [Polling](../../../reference/glossary.md#polling) · [Interrupt](../../../reference/glossary.md#interrupt) · [Interrupt coalescing](../../../reference/glossary.md#interrupt-coalescing) · [Direct memory access (DMA)](../../../reference/glossary.md#direct-memory-access-dma) · [Valid/ready handshake](../../../reference/glossary.md#valid-ready-handshake) · [AXI](../../../reference/glossary.md#axi) · [Network-on-chip (NoC)](../../../reference/glossary.md#network-on-chip-noc) · [Bisection bandwidth](../../../reference/glossary.md#bisection-bandwidth) · [PCI Express (PCIe)](../../../reference/glossary.md#pci-express-pcie) · [Lane (serial link)](../../../reference/glossary.md#lane-serial-link) · [Compute Express Link (CXL)](../../../reference/glossary.md#compute-express-link-cxl)

## 12. Connections

- **Builds on:** traps and interrupts ([14-10](14-10-virtual-memory.md)); caches and Little's law ([14-09](14-09-memory-hierarchy-and-caches.md)); volatile and bit manipulation in C ([05-07](../../05-programming-for-engineers/chapters/05-07-bit-manipulation.md)).
- **Next:** [14-12 Multicore, Coherence and Memory Consistency](14-12-multicore-coherence-consistency.md), where the interconnect also keeps caches coherent.
- **Used later:** microcontroller interrupts and DMA ([18-03](../../18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md), [18-04](../../18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md)); SerDes, PCIe, CXL and die-to-die links ([24-03](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md), [24-05](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md), [24-06](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)).

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, the online chapter on storage and other I/O topics.
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, App. D (storage systems) and App. F (interconnection networks).
- W. J. Dally and B. Towles, *Principles and Practices of Interconnection Networks*, Morgan Kaufmann, 2004 (topologies, routing, flow control).
- Arm, *AMBA AXI Protocol Specification* (IHI 0022), the handshake and channel chapters.

## 14. Sources

1. Arm, "AMBA AXI Protocol Specification," ARM IHI 0022 Issue L (Aug 2025), and Arm's AMBA web pages. Issue J (2023) removed the AXI3, AXI4 and AXI4-Lite content, so the AXI4-Lite rules used here are those of the earlier issues (Issue H and before). [R-217](../../../reference/research-log.md#r-217--amba-axi-issue-l-and-cxl-40)
2. D. Das Sharma, "What's the Difference Going from PCIe 3.0 to PCIe 6.0?", *Electronic Design*. [R-216](../../../reference/research-log.md#r-216--pci-express-generations-1080)
3. PCI-SIG releases for PCIe 6.0 (Jan 2022), 7.0 (Jun 2025) and 8.0 (Aug 2025), read as reprints. [R-216](../../../reference/research-log.md#r-216--pci-express-generations-1080)
4. CXL Consortium, "CXL Consortium Releases the Compute Express Link 4.0 Specification," 18 Nov 2025. [R-217](../../../reference/research-log.md#r-217--amba-axi-issue-l-and-cxl-40)

Memory-mapped I/O, polling, interrupts, DMA, handshakes and mesh analysis are textbook material (Further study). The register block's cycle counts come from the lab's testbench, re-run by the verify script.
