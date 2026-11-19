# Lab 08-11 · Memories and Lookup Tables

**Chapter:** [08-11](../../chapters/08-11-memories-and-programmable-logic.md) · **Notebook:** [08-11-memories-lut.ipynb](08-11-memories-lut.ipynb) · **Time:** about 2 hours

## Objective

1. Compute memory array organizations and address splits from 1 kbit to 1 Gbit.
2. Map functions onto 4-input LUTs by Shannon expansion with sharing, and compare random and structured functions.
3. Compare ROM sizes with logic implementations.
4. Budget block RAM, single-port RAM and DSP blocks for a small design on a real low-power FPGA.
5. Write and test a block-RAM-style RAM, a RISC-V-style register file, a ROM decoder and a LUT network in Verilog.

## Background

Chapter sections 3.1 to 3.5 and Examples 08-11.1 to 08-11.7. You need Python with NumPy and Matplotlib, and Icarus Verilog (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-11-memories-lut.ipynb](08-11-memories-lut.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s and this handout's key |
| [mem.v](mem.v) | `ram_sp` (synchronous, read-first), `regfile32` (2 read ports, 1 write port, `x0` = 0), `sevenseg_rom`, `lut4`, and `lut6_from_lut4` (a 6-input function from seven 4-input LUTs) | `mem_tb.v` |
| [mem_top.v](mem_top.v) | A top level for lint tools | Lint only |
| [mem_tb.v](mem_tb.v) | 2000 random RAM operations and 2000 register-file operations against reference models (including reads of the location being written), the ROM's segment counts, and the LUT network on all 64 inputs | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_notebooks.py 08-11
```

```bash
python tools/run_hdl.py
```

## Procedure

1. **Organizations (Part 1).** Tabulate rows, columns and address splits for 32-bit-word memories from $2^{10}$ to $2^{30}$ bits.
2. **LUT mapping (Part 2, the chapter's guided exercise).** *Predict first:* how many 4-input LUTs does a random 8-input function need, and does sharing identical sub-functions help? The notebook maps 1000 random functions and 8-input parity, checking each network on every input.
3. **ROM or logic (Part 3).** Compare the ROM size of multipliers, a Gray converter and a 7-segment decoder with their logic implementations.
4. **FPGA budget (Part 4).** Fit an audio buffer, a display buffer and a filter into an iCE40 UP5K.
5. **Verilog.** Run `mem_tb.v`. Then change `ram_sp` to write-first (output the new data when writing) and predict which check fails.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | 1 Gbit memory, square | 32 768 rows; 15 row-address bits and 10 column-address bits (see the key) |
| 2 | LUT mapping | random 8-input functions need 31 LUTs almost always; parity collapses to 9 with sharing, and 3 as an XOR tree |
| 3 | ROM or logic | the 8 × 8 multiplier ROM is 1 Mbit; the Gray converter is 2048 ROM bits against 7 XORs |
| 4 | UP5K budget | the two buffers need 35 block RAMs of 30; moving the display buffer into one single-port RAM fixes it; a 64-tap filter at 16 kHz uses 8.5% of one DSP block |
| Verilog | testbench | `TEST PASSED`; with a write-first RAM, the read checks on writing cycles fail |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-11.a | rows of a square 1 Gbit array | 32768 | — |
| Lab 08-11.b | row-address bits | 15 | — |
| Lab 08-11.c | column-address bits, 32-bit words | 10 | — |
| Lab 08-11.d | average 4-LUTs, random 8-input functions | 30.998 | — |
| Lab 08-11.e | 4-LUTs for 8-input parity, Shannon with sharing | 9 | — |
| Lab 08-11.f | 4-LUTs for 8-input parity, XOR tree | 3 | — |
| Lab 08-11.g | block RAMs needed by both buffers | 35 | — |
| Lab 08-11.h | random RAM operations in the testbench | 2000 | — |
| Lab 08-11.i | LUT-network inputs checked | 64 | — |

**Reading the key.** A random 8-input function has 16 different 4-input cofactors with overwhelming probability (each is one of 65 536 functions), so the Shannon tree needs $16 + 8 + 4 + 2 + 1 = 31$ LUTs; only 2 of the 1000 sampled functions repeated a cofactor and saved one LUT. Parity's cofactors at each level are just "parity" and "inverted parity" of the remaining inputs: 2 distinct 4-input leaves and $2 + 2 + 2 + 1 = 7$ multiplexers, 9 LUTs.

## Discussion questions

1. Why is a 1 Gbit memory never built as a single 32 768 × 32 768 array?
2. Why does sharing identical sub-functions almost never help for random functions, but help a great deal for parity?
3. In `ram_sp`, why does reading the address being written return the old data, and why do FPGA block RAMs offer a choice of behaviors?
4. The register file's read ports are combinational, but `ram_sp`'s is registered. Why the difference?
5. Why did the iCE40 budget move the display buffer rather than the audio buffer into single-port RAM?

<details><summary>Answers to the discussion questions</summary>

1. Each wordline and bitline would cross 32 768 cells: long, heavily loaded wires with large delay and energy, and a read would swing 32 768 bitlines to deliver 32 bits. Real memories split the capacity into many banks and sub-arrays, each with short lines and local sense amplifiers, and activate only the one being accessed (Problem 08-11.13).
2. A random 4-input sub-function is one of 65 536 possibilities, so two of them coincide only by chance (about 2 of the 1000 sampled functions shared one). Parity is highly structured: every cofactor is parity or its complement over the remaining inputs, so only two distinct leaves exist at each level and sharing removes most of the tree.
3. The read and the write happen on the same clock edge; the registered output captures the memory's contents as they were before the edge, which is the old word. Some designs want the new word (write-first, convenient for forwarding) and some want the output unchanged during writes (no-change, saving power), so FPGA block RAMs make it a configuration option, and RTL must match the option chosen.
4. A register file is small and must deliver operands in the same cycle the instruction reads them, so its reads are combinational (multiplexer trees). Block RAMs are large arrays with sense amplifiers; registering the address and output makes them fast and their timing independent of surrounding logic, at the cost of one cycle of latency.
5. The display buffer is read and written in long sequential bursts, which suits a single-port RAM; the audio buffer is typically written by the input stream and read by the filter at the same time, which needs the two ports of block RAM.

</details>

## Optional hardware

On an iCE40 UltraPlus development board, synthesize `ram_sp` with the open-source tools of [08-12](../../chapters/08-12-fpga-implementation-flow.md) and read the utilization report: with a registered read it maps to block RAM; change it to an asynchronous read (`assign dout = mem[addr]`) and watch the tool build the memory from logic cells instead, at a far larger cost.
