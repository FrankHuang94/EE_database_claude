# Problems 08-12 · FPGA Implementation Flow

Chapter: [08-12](../chapters/08-12-fpga-implementation-flow.md) · Worked solutions: [08-12 solutions](../solutions/08-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** measured values are from the lab's reports (Yosys 0.71, nextpnr-ice40 0.11.1, iCE40 UP5K in the SG48 package, seed 1 unless stated): the chapter's §3.7 table and Examples 08-12.1 to 08-12.7. The UP5K has 5280 logic cells, 8 DSP blocks and 39 user I/O in this package; its bitstream is 104 090 bytes.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-12.1 [A]

**Which step decides what?** For each of the following, name the step of the flow that decides it: (a) whether a multiplier uses a DSP block; (b) which logic cell a given LUT occupies; (c) which wire segments connect two cells; (d) whether the design meets its clock constraint; (e) the encoding of a state machine.

### Problem 08-12.2 [A]

**Utilization.** (a) What fraction of the UP5K's logic cells does the binary-encoded FSM (37 cells) use? (b) The DSP multiplier harness uses 79 cells and 1 DSP block. What fractions of the cells and of the DSP blocks is that?

### Problem 08-12.3 [A]

**Slack at 48 MHz.** The binary FSM reaches 54.20 MHz and the one-hot FSM 79.23 MHz. What is each one's minimum period and slack at 48 MHz?

### Problem 08-12.4 [B]

**A LUT multiplier's critical path.** The LUT multiplier harness's critical path is clock-to-Q 1.390 ns, logic 14.352 ns, routing 21.752 ns and setup 0.824 ns. (a) What is the total, and the maximum frequency? (b) What fractions are routing and logic?

### Problem 08-12.5 [B]

**If routing were cheaper.** Suppose a better router halved the routing delay on the gate-level adder's critical path (36.981 ns of 57.337 ns). (a) What would the period and maximum frequency become? (b) Would it then match the carry-chain adder's 52.09 MHz?

### Problem 08-12.6 [B]

**Pipelining the LUT multiplier.** Split the LUT multiplier's 38.32 ns critical path into two stages with equal logic and routing, each paying the register overhead of clock-to-Q plus setup (2.214 ns). What period and frequency result, and would it meet 48 MHz?

### Problem 08-12.7 [B]

**Which designs meet 48 MHz?** Using the six measured frequencies of §3.7, which designs would work from the UP5K's 48 MHz internal oscillator, and which would not?

### Problem 08-12.8 [B]

**Placement seeds.** The gate-level adder was placed and routed with seeds 1 to 8, giving maximum frequencies of 17.44, 17.28, 16.94, 17.44, 17.44, 17.28, 17.44 and 17.44 MHz. (a) What are the best, worst and mean? (b) By what percentage does the best exceed the worst? (c) How many of the eight seeds reach the best value?

### Problem 08-12.9 [B]

**Configuration flash.** How many complete UP5K bitstreams fit in (a) a 1 Mbit (128 KB) SPI flash, and (b) a 4 Mbit (512 KB) flash?

### Problem 08-12.10 [C]

**Multiplier throughput.** (a) Using all 8 DSP blocks as multipliers at the DSP harness's measured 100.88 MHz, how many multiplications per second can a UP5K perform? (b) Using LUT multipliers instead (at most 6 copies by logic cells, at 26.10 MHz), how many? (c) What is the ratio?

### Problem 08-12.11 [C]

**Boot time.** An FPGA reads its bitstream from SPI flash one bit per clock. How long does loading 104 090 bytes take with a 12 MHz and with a 48 MHz configuration clock (ignoring overheads)? Compare with the data sheet's maximum configuration times of 140 ms and 50 ms.

### Problem 08-12.12 [C]

**From FPGA flow to ASIC flow.** Name four steps that an ASIC implementation flow needs and an FPGA flow does not, and explain for each why the FPGA does not need it.


### Problem 08-12.13 [B]

**Writing the constraints.** A UP5K design has two clocks: a 12 MHz board clock on a pin, and the 48 MHz internal oscillator, which runs the main logic. A sensor chip, clocked by the 12 MHz board clock, drives a data input that changes up to 20 ns after each board-clock edge; the two clock domains exchange data only through a FIFO with synchronizers. For each item, say what constraint is needed and what goes wrong without it: (a) the 48 MHz clock; (b) the sensor input; (c) the paths between the 12 MHz and 48 MHz domains; (d) the data pins. (e) With the input delay of (b), how much of the 83.33 ns board-clock period is left for the input's path inside the FPGA, ignoring board wiring?

---

## Objective coverage

| Learning objective (chapter 08-12) | Problems |
|---|---|
| 1. Steps of the flow | 1, 9, 11 |
| 2. Constraints | 3, 7, 13 |
| 3. Reading reports and critical paths | 2, 3, 4, 5, 8 |
| 4. Coding style and hard blocks | 5, 6, 10 |
| 5. Open-source, vendor and ASIC flows | 12 |
