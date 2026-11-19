# Solutions 08-12 · FPGA Implementation Flow

Problems: [08-12 problems](../problems/08-12-problems.md) · Chapter: [08-12](../chapters/08-12-fpga-implementation-flow.md). Every measured number below is read by [verify_08_12.py](../verify/verify_08_12.py) from the lab's committed nextpnr reports, and every derived number is recomputed from them.

---

## Solutions

### Solution 08-12.1

(a) **Synthesis**, during inference of special structures (with DSP inference enabled). (b) **Placement**. (c) **Routing**. (d) **Timing analysis** after routing, against the constraints. (e) **Synthesis** (FSM extraction and recoding), unless the designer fixes it with an attribute.

### Solution 08-12.2

(a) $37/5280$ = **0.70**%.

(b) $79/5280$ = **1.50**% of the cells and $1/8$ = **12.5**% of the DSP blocks: the scarce resource for multiplier-heavy designs is the DSP blocks, not the logic.

### Solution 08-12.3

At 48 MHz the period is 20.83 ns. Binary FSM: period $1000/54.20$ = **18.45** ns, slack **2.38** ns. One-hot FSM: **12.62** ns, slack **8.21** ns. Both pass; the one-hot version has more than three times the margin.

### Solution 08-12.4

(a) $1.390 + 14.352 + 21.752 + 0.824 = 38.318$, so **38.32** ns, and $f_{\max} = 1000/38.318$ = **26.10** MHz, as reported.

(b) Routing $21.752/38.318$ = **56.8**%; logic $14.352/38.318$ = **37.5**%.

### Solution 08-12.5

(a) $57.337 - 36.981/2$ = **38.85** ns: **25.74** MHz.

(b) No: still about half the carry-chain adder's 52.09 MHz. Even with cheaper routing, 20 LUTs of carry logic in series cost more than a dedicated chain; the gain from using the right hardware is structural, not just a matter of wire delay.

### Solution 08-12.6

Each stage carries half of the $38.318 - 2.214 = 36.104$ ns of logic and routing, plus the overhead: $36.104/2 + 2.214$ = **20.27** ns, **49.3** MHz. It would just meet 48 MHz (20.83 ns), with half a nanosecond of slack, at the cost of one extra cycle of latency and the register bits. (In practice the two halves are rarely exactly equal, so the real result would be a little worse.)

### Solution 08-12.7

Pass at 48 MHz (period 20.83 ns): the carry-chain adder (52.09 MHz), the DSP multiplier (100.88), the one-hot FSM (79.23) and the binary FSM (54.20): **4** designs. Fail: the gate-level adder (17.44) and the LUT multiplier (26.10): **2** designs. Both failures are the designs that avoided the hard resources.

### Solution 08-12.8

(a) Best **17.44** MHz, worst **16.94** MHz, mean **17.34** MHz.

(b) $(17.44 - 16.94)/16.94$ = **2.95**%.

(c) **5** of the 8 seeds reach the best value. Seed sweeps buy a few percent, useful when a design is just short of its constraint, but never the factor of three that the carry chain gives.

### Solution 08-12.9

(a) $131\,072/104\,090 = 1.26$: **1** bitstream. (b) $524\,288/104\,090 = 5.04$: **5** bitstreams, enough for a factory image plus updates (multi-boot schemes keep a known-good image in case an update fails).

### Solution 08-12.10

(a) $8 \times 100.88 \times 10^6$ = **8.07 × 10⁸** multiplications per second.

(b) $6 \times 26.10 \times 10^6$ = **1.57 × 10⁸**.

(c) **5.15** times more with the DSP blocks, while leaving almost all the logic cells free.

### Solution 08-12.11

$104\,090 \times 8 = 832\,720$ bits. At 12 MHz: **69.4** ms; at 48 MHz: **17.3** ms. Both are within the data sheet's maxima (140 ms at the default frequency, 50 ms at medium), which also include power-on and initialization overheads. For a wearable, tens of milliseconds of FPGA boot is usually invisible, but for a system that must respond within milliseconds of power-up, the internal non-volatile configuration memory or an always-powered design is needed.

### Solution 08-12.12

Any four of:

- **Floorplanning and power-grid design:** an FPGA's die, power distribution and block locations are fixed by the vendor.
- **Clock-tree synthesis:** an FPGA has prebuilt global clock networks; an ASIC must build and balance its own clock tree.
- **Physical routing on metal layers with design rules:** FPGA routing only chooses among existing wires and switches, already verified by the vendor.
- **Parasitic extraction:** FPGA wire delays come from the vendor's characterized timing models.
- **Sign-off checks (DRC, LVS) and mask generation (GDSII):** the FPGA is already manufactured; only a bitstream is generated.

All of these are the price of the ASIC's advantages in speed, power, area and unit cost (08-11 §3.5).

### Solution 08-12.13

(a) A **clock definition** with a period of 20.83 ns for the oscillator's clock. Without it the 48 MHz logic is checked against the wrong period, or not at all, and the report's "PASS" means nothing (Example 08-12.2).

(b) An **input delay** of 20 ns relative to the 12 MHz board clock, so that timing analysis knows the data arrives late in the period. Without it, the tool assumes the input arrives at the clock edge and may let the internal path use time that does not exist.

(c) The two clocks are declared **asynchronous** (a clock group or false paths between them). Their crossings are handled by the FIFO's synchronizers, not by timing, and without the exception the tool would try to time paths between unrelated clocks, report meaningless violations and possibly distort the placement to fix them.

(d) **Pin assignments** in the PCF file, with the I/O standard of each pin. Without them the tool picks pins itself, which will not match the board.

(e) $83.33 - 20$ = **63.33** ns, minus the input flip-flop's setup time: the data must reach the first register within that time after the board-clock edge.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-12.2a | binary FSM utilization | 0.70 | % |
| 08-12.2b | DSP harness cell utilization | 1.50 | % |
| 08-12.2c | DSP block utilization | 12.5 | % |
| 08-12.3a | binary FSM period | 18.45 | ns |
| 08-12.3b | binary FSM slack at 48 MHz | 2.38 | ns |
| 08-12.3c | one-hot FSM period | 12.62 | ns |
| 08-12.3d | one-hot FSM slack at 48 MHz | 8.21 | ns |
| 08-12.4a | LUT multiplier critical path | 38.32 | ns |
| 08-12.4b | maximum frequency | 26.10 | MHz |
| 08-12.4c | routing share | 56.8 | % |
| 08-12.4d | logic share | 37.5 | % |
| 08-12.5a | period with routing halved | 38.85 | ns |
| 08-12.5b | frequency with routing halved | 25.74 | MHz |
| 08-12.6a | pipelined period | 20.27 | ns |
| 08-12.6b | pipelined frequency | 49.3 | MHz |
| 08-12.7a | designs meeting 48 MHz | 4 | — |
| 08-12.7b | designs failing 48 MHz | 2 | — |
| 08-12.8a | best seed | 17.44 | MHz |
| 08-12.8b | worst seed | 16.94 | MHz |
| 08-12.8c | mean | 17.34 | MHz |
| 08-12.8d | best over worst | 2.95 | % |
| 08-12.8e | seeds reaching the best | 5 | — |
| 08-12.9a | bitstreams in 1 Mbit | 1 | — |
| 08-12.9b | bitstreams in 4 Mbit | 5 | — |
| 08-12.10a | multiplications per second, DSP | 8.07e8 | 1/s |
| 08-12.10b | multiplications per second, LUTs | 1.57e8 | 1/s |
| 08-12.10c | ratio | 5.15 | — |
| 08-12.11a | load time at 12 MHz | 69.4 | ms |
| 08-12.11b | load time at 48 MHz | 17.3 | ms |
| 08-12.13a | 48 MHz period | 20.83 | ns |
| 08-12.13b | time left for the internal input path | 63.33 | ns |
