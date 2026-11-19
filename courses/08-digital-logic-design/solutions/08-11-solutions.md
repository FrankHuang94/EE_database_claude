# Solutions 08-11 · Memories and Programmable Logic

Problems: [08-11 problems](../problems/08-11-problems.md) · Chapter: [08-11](../chapters/08-11-memories-and-programmable-logic.md). Every number below is recomputed by [verify_08_11.py](../verify/verify_08_11.py): memory organizations by arithmetic on the address split, LUT counts by actually building the LUT networks and checking them against the function on every input, PLA sizes from exactly minimized products, and resource and cost figures from the problem data.

---

## Solutions

### Solution 08-11.1

(a) $262\,144 \times 32$ = **8 388 608** bits ($2^{23}$, 8 Mbit); $\log_2 262\,144$ = **18** address bits.

(b) With columns $= 2 \times$ rows, $2R^2 = 2^{23}$ gives $R$ = **2048** rows and **4096** columns, holding $4096/32$ = **128** words per row.

(c) **11** bits to the row decoder and **7** to the column multiplexers ($11 + 7 = 18$ ✓).

### Solution 08-11.2

(a) $2^4 \times 7$ = **112** bits.

(b) $2^8 \times 8$ = **2048** bits, against **7** XOR gates ($g_i = b_i \oplus b_{i+1}$ for $i$ = 0 to 6, and $g_7 = b_7$). Functions with simple structure are far cheaper as logic.

### Solution 08-11.3

(a) $2^{2^2}$ = **16**: every two-input function of 08-02.

(b) $2^{2^5} = 2^{32}$ = **4.29 × 10⁹**.

### Solution 08-11.4

(a) $16 \times 64$ = **1024** bits.

(b) Each read port is a 64-bit 16:1 multiplexer, $64 \times 15 = 960$ two-input multiplexers: $3 \times 960$ = **2880**.

(c) Two decoders of 16 outputs: **32**.

(d) $(5/3)^2$ = **2.78** times the cell area of a 2R1W file.

### Solution 08-11.5

(a) Two LUTs AND 4 inputs each and a third ANDs their outputs: **3** LUTs, **2** levels.

(b) Level 1: 8 LUTs (32/4); level 2: 2 LUTs; level 3: 1 LUT. **11** LUTs, **3** levels.

(c) Level 1: $\lceil 32/6 \rceil = 6$ LUTs; level 2: one LUT combines 6 outputs. **7** LUTs, **2** levels.

### Solution 08-11.6

(a) With 4-input LUTs, which can only act as 2:1 multiplexers, the recursion gives $2^{8-4+1} - 1$ = **31** LUTs. A 6-input LUT is a 4:1 multiplexer (2 selects and 4 data inputs), so expand on two variables at once: four 6-input cofactors, one LUT each, and one multiplexer LUT, **5** six-input LUTs. (The plain 2:1 recursion would give $2^{8-6+1} - 1 = 7$.) Both numbers are what the construction guarantees, upper bounds for an arbitrary function.

(b) Two LUTs compute the parity of 4 inputs each and a third XORs their outputs: **3** LUTs. Structure matters far more than the input count.

### Solution 08-11.7

(a) PLA: $2 \times 4 \times 9 + 9 \times 3$ = **99** crosspoints; ROM: $2^4 \times 3$ = **48** bits. The ROM is smaller.

(b) PLA: $2 \times 16 \times 40 + 40 \times 4$ = **1440**; ROM: $2^{16} \times 4$ = **262 144** bits. The PLA is about 180 times smaller.

### Solution 08-11.8

$8192 \times 50\ \text{ns} = 409.6$ µs of refresh every 64 ms: **0.64**% of the time. Small, but it grows with the number of rows per array, which is why DRAM refresh overhead is a concern as densities rise ([23-03](../../23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md)).

### Solution 08-11.9

(a) $320 \times 240$ = 76 800 bits, $76\,800/4096 = 18.75$: **19** block RAMs, **63.3**% of the 30. Packing matters: the iCE40's block RAMs come in 256 × 16, 512 × 8, 1024 × 4 and 2048 × 2 configurations, none one bit wide ([R-159](../../../reference/research-log.md#r-159--fpga-devices-and-the-fpga-industry)), so storing one pixel per word would use 2048 pixels per block and need **38** blocks, more than the device has.

(b) 128 KB = $128 \times 1024 \times 8$ = 1 048 576 bits = 1 Mbit: all **4** single-port RAMs.

### Solution 08-11.10

(a) $64 \times 16\,000$ = **1 024 000** multiplies per second, **8.53**% of 12 million.

(b) $12 \times 10^6 / 16\,000$ = **750** taps.

### Solution 08-11.11

$5280 \times 2^4$ = **84 480** bits, before the much larger number of routing configuration bits.

### Solution 08-11.12

(a) $V^{*} = 20\,000\,000/(35 - 8)$ = **740 741** units.

(b) 900 000 units in total. FPGA: $35 \times 900\,000$ = **31.5** million USD. ASIC: $20 + 8 \times 0.9$ = **27.2** million USD. The ASIC saves **4.3** million USD.

(c) The ASIC must also be designed, verified and manufactured before the first sale: if that delays the product, lost revenue and market share can outweigh the saving. Other factors: the risk of a respin, power and board area (often decisive in wearables), the need for field upgrades, and whether the volume forecast is reliable. A common path is to launch on an FPGA and move to an ASIC once volume is proven.

### Solution 08-11.13

(a) 16 of the 1024 bitlines that swing deliver data: **1.56**%.

(b) $16/256$ = **6.25**%, four times better. Banking, activating only part of the array, is how large memories save energy and keep bitlines short; the price is more decoders and sense amplifiers.

### Solution 08-11.14

$3840/8$ = **480** times the DSP blocks, against about 774 times the LUTs. The large device is aimed at ASIC prototyping and emulation, which is mostly general logic, so it has relatively more LUTs; the small device is aimed at low-power signal processing next to sensors, so a few DSP blocks are a larger share of its resources. Resource ratios reveal a device's intended market.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-11.1a | bits | 8388608 | bit |
| 08-11.1b | address bits | 18 | — |
| 08-11.1c | rows | 2048 | — |
| 08-11.1d | columns | 4096 | — |
| 08-11.1e | words per row | 128 | — |
| 08-11.1f | row-address bits | 11 | — |
| 08-11.1g | column-address bits | 7 | — |
| 08-11.2a | 7-segment ROM bits | 112 | bit |
| 08-11.2b | Gray-converter ROM bits | 2048 | bit |
| 08-11.2c | Gray-converter XOR gates | 7 | — |
| 08-11.3a | functions of a 2-input LUT | 16 | — |
| 08-11.3b | functions of a 5-input LUT | 4.29e9 | — |
| 08-11.4a | storage bits | 1024 | bit |
| 08-11.4b | read multiplexers | 2880 | — |
| 08-11.4c | decoder outputs | 32 | — |
| 08-11.4d | cell-area factor | 2.78 | — |
| 08-11.5a | 4-LUTs, 8-input AND | 3 | — |
| 08-11.5b | levels | 2 | — |
| 08-11.5c | 4-LUTs, 32-input AND | 11 | — |
| 08-11.5d | levels | 3 | — |
| 08-11.5e | 6-LUTs, 32-input AND | 7 | — |
| 08-11.5f | levels | 2 | — |
| 08-11.6a | 4-LUTs that suffice, 8 inputs | 31 | — |
| 08-11.6b | 6-LUTs that suffice, 8 inputs | 5 | — |
| 08-11.6c | 4-LUTs for 8-input parity | 3 | — |
| 08-11.7a | PLA crosspoints, small function | 99 | — |
| 08-11.7b | ROM bits, small function | 48 | bit |
| 08-11.7c | PLA crosspoints, large function | 1440 | — |
| 08-11.7d | ROM bits, large function | 262144 | bit |
| 08-11.8a | refresh busy fraction | 0.64 | % |
| 08-11.9a | block RAMs for the display buffer | 19 | — |
| 08-11.9b | share of block RAMs | 63.3 | % |
| 08-11.9c | single-port RAMs for 128 KB | 4 | — |
| 08-11.9d | block RAMs without packing (2048 × 2 mode) | 38 | — |
| 08-11.10a | multiplies per second | 1024000 | — |
| 08-11.10b | DSP utilization | 8.53 | % |
| 08-11.10c | taps per DSP block | 750 | — |
| 08-11.11a | LUT configuration bits | 84480 | bit |
| 08-11.12a | break-even volume | 740741 | — |
| 08-11.12b | FPGA total cost | 31.5 | MUSD |
| 08-11.12c | ASIC total cost | 27.2 | MUSD |
| 08-11.12d | ASIC saving | 4.3 | MUSD |
| 08-11.13a | useful bitline fraction | 1.56 | % |
| 08-11.13b | with 4 banks | 6.25 | % |
| 08-11.14a | DSP ratio | 480 | — |
