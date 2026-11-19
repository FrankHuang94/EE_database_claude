# Problems 08-11 · Memories and Programmable Logic

Chapter: [08-11](../chapters/08-11-memories-and-programmable-logic.md) · Worked solutions: [08-11 solutions](../solutions/08-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 1 kbit = 1024 bits and 1 Mbit = 1024 kbit. A tree of two-input multiplexers implementing an $N$:1 multiplexer has $N - 1$ of them. LUT counts assume each LUT is used as a single-output function.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-11.1 [A]

**Organizing a memory.** A 256 K × 32 SRAM is laid out with twice as many columns as rows. (a) How many bits and address bits? (b) How many rows, columns and words per row? (c) How many address bits go to the row decoder and to the column multiplexers?

### Problem 08-11.2 [A]

**ROM sizes.** (a) How many bits does a ROM need to implement a 7-segment decoder (4 inputs, 7 outputs)? (b) An 8-bit binary-to-Gray converter as a ROM? How many two-input XOR gates does the same converter need as logic (08-01)?

### Problem 08-11.3 [A]

**Counting functions.** How many different functions can (a) a 2-input LUT and (b) a 5-input LUT implement?

### Problem 08-11.4 [B]

**A multi-ported register file.** A register file has 16 registers of 64 bits, 3 read ports and 2 write ports. (a) How many storage bits? (b) How many two-input multiplexers do the read ports need? (c) How many decoder outputs do the write ports need in total? (d) If cell area grows as the square of the number of ports, how much larger is each cell than in a file with 2 read ports and 1 write port?

### Problem 08-11.5 [B]

**Wide ANDs in LUTs.** How many LUTs, and how many levels, implement (a) an 8-input AND with 4-input LUTs; (b) a 32-input AND with 4-input LUTs; (c) a 32-input AND with 6-input LUTs?

### Problem 08-11.6 [B]

**Worst case and best case.** (a) By Shannon expansion, how many 4-input LUTs does an arbitrary 8-input function need in the worst case? How many 6-input LUTs? (b) How many 4-input LUTs does 8-input parity need, built as a tree?

### Problem 08-11.7 [B]

**PLA or ROM?** Compare the PLA crosspoints with the ROM bits for (a) a 4-input, 3-output function that needs 9 distinct product terms, and (b) a 16-input, 4-output function that needs 40 product terms.

### Problem 08-11.8 [B]

**The cost of refresh.** A DRAM has 8192 rows, each of which must be refreshed every 64 ms, and refreshing a row occupies the array for 50 ns (hypothetical numbers). What fraction of the time is the array busy refreshing?

### Problem 08-11.9 [B]

**Buffers in a small FPGA.** On an iCE40 UP5K (30 block RAMs of 4 kbit, 4 single-port RAMs of 256 kbit): (a) How many block RAMs does a 320 × 240 one-bit display buffer need, and what fraction of them is that? (b) How many single-port RAMs hold a 128 KB (kilobyte) frame buffer?

### Problem 08-11.10 [B]

**Time-sharing a DSP block.** A 64-tap FIR filter runs at a 16 kHz sample rate on one DSP block clocked at 12 MHz, one multiply per clock. (a) How many multiplies per second does the filter need, and what fraction of the DSP block's capacity is that? (b) How many taps could one DSP block handle at this sample rate?

### Problem 08-11.11 [B]

**Configuration bits.** How many configuration bits do the lookup tables alone of a UP5K's 5280 four-input LUTs hold?

### Problem 08-11.12 [C]

**FPGA or ASIC over a product's life.** Hypothetical numbers: an ASIC has USD 20 million of NRE and costs USD 8 per unit; the FPGA solution costs USD 35 per unit. (a) What is the break-even volume? (b) The product sells 300 000 units a year for 3 years. What is the total cost of each option, and which is cheaper by how much? (c) What else should the decision weigh?

### Problem 08-11.13 [C]

**Why memories are banked.** A read activates one wordline, and every bitline on that row swings, but only the selected word is used. (a) In the 1024 × 1024 array of Example 08-11.1 with 16-bit words, what fraction of the bitlines that swing deliver output bits? (b) If the array is split into 4 banks of 1024 × 256 and only one bank is activated per read, what is the fraction?

### Problem 08-11.14 [C]

**Scale.** The VU19P has 3840 DSP slices and the UP5K 8 DSP blocks. How many times as many DSP blocks does the larger device have? Why is the DSP ratio smaller than the LUT ratio of Example 08-11.7, and what does that say about the two devices' intended uses?

---

## Objective coverage

| Learning objective (chapter 08-11) | Problems |
|---|---|
| 1. Memory array organization | 1, 13 |
| 2. Memory types | 8, 13 |
| 3. Register files | 4 |
| 4. Logic in ROMs, PLAs and LUTs | 2, 3, 5, 6, 7, 11 |
| 5. FPGA architecture and resource use | 9, 10, 12, 14 |
