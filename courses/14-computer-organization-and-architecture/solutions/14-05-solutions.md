# Solutions 14-05 · Single-Cycle Datapath and Control

Problems: [14-05 problems](../problems/14-05-problems.md) · Chapter: [14-05](../chapters/14-05-single-cycle-datapath.md). Every number below is recomputed by [verify_14_05.py](../verify/verify_14_05.py). It reads the control table from the lab's Verilog decoder, derives immediates by assembling single-bit immediates with LLVM, recomputes path delays from the delay table, and runs the lab program on both the Verilog core (Icarus) and the Python simulator.

---

## Solutions

### Solution 14-05.1

`lw` writes memory data to rd, so ResultSrc = **1**. It adds an immediate offset, so BSel = **1** (immediate). `bne` writes no register, RegWrite = **0**, and is a branch, Branch = **1**.

### Solution 14-05.2

| Word | Instruction | ImmSel | Immediate |
|---|---|---|---|
| 0xFFC52303 | `lw x6, -4(x10)` | I | **0xFFFFFFFC** (−4) |
| 0x00512623 | `sw x5, 12(x2)` | S | **0x0000000C** (12) |
| 0xFE051CE3 | `bne x10, x0, -8` | B | **0xFFFFFFF8** (−8) |
| 0x001000EF | `jal x1, 2048` | J | **0x00000800** (2048) |

Each follows 14-02's decoding (Examples 14-02.2 and Solutions 14-02.2 and 14-02.7). The immediate generator just wires the fields into place and copies bit 31 into the upper bits.

### Solution 14-05.3

1. The ALU adds x10 and the sign-extended offset: 0x2000 − 4 = **0x00001FFC**.
2. The data memory returns the word there, and ResultSrc = memory passes it to the register file: x6 = **0x12345678**.
3. The next PC is 0x200 + 4 = **0x00000204**.

### Solution 14-05.4

The load path loses 80 ps: $730 - 80$ = **650** ps. The other paths are unchanged (R-type 530, store 505, branch 465, JAL 415), so the load still sets the period: $T$ = **650** ps, $f$ = **1.538** GHz. The R-type and JALR paths (530 ps) are now the next longest, 120 ps behind.

### Solution 14-05.5

The instruction memory is on *every* path, so every path grows by 100 ps. The load becomes 830 ps, so $T$ = **830** ps and $f$ = **1.205** GHz. The data memory affects only loads and stores; the instruction memory affects every instruction. In a single-cycle design both are on the critical (load) path, but only instruction fetch can never be avoided.

### Solution 14-05.6

$0.20(730) + 0.10(505) + 0.50(530) + 0.15(465) + 0.05(415)$ = **552.0** ps. The efficiency is 552.0/730 = **75.6**%.

### Solution 14-05.7

(a) A store's bits 11–7 hold imm[4:0] = 12, so the register file writes x**12**. ResultSrc is "don't care" for a store; in the lab core it is 0, the ALU result, which is the address x2 + 12 = **0x00003FFC**. A store now silently corrupts x12.

(b) For `beq x1, x2, 16`, bits 11–7 hold imm[4:1] and imm[11]. The offset 16 makes imm[4:1] = 1000 and imm[11] = 0, so the field reads 10000 = **16**. The ALU subtracts for branches, so x16 receives 5 − 5 = **0**.

(c) Instructions that write rd anyway (R-type, I-type, loads, JAL, JALR, LUI, AUIPC) are unaffected. Stores and branches corrupt the register named by their immediate bits, unless that field happens to be 0 (x0).

### Solution 14-05.8

The CPI is $0.25(5) + 0.10(4) + 0.45(4) + 0.15(3) + 0.05(3)$ = **4.05**, so the average time is $4.05 \times 250$ = **1012.5** ps per instruction. That is 1012.5/730 = **1.387** times *slower* than the single-cycle machine.

Splitting the work did not help speed here: the step overheads (each cycle has its own register clock-to-Q and setup) and the uneven split cost more than skipping unneeded steps saved. Multi-cycle designs were valuable when logic was expensive. They let one ALU and one memory port do the work of several adders and two memories. Their speed advantage depends on a good balance of steps; pipelining then overlaps the steps to get both a short cycle and CPI near 1.

### Solution 14-05.9

The `fib` part grows from $21F(11) - 18 = 1851$ to $21F(16) - 18 = 21 \times 987 - 18 = 20\,709$ instructions; the rest of the program (72 instructions) is unchanged. The total is $1923 - 1851 + 20\,709$ = **20781** cycles, or $20\,781 \times 730$ ps = **15.17** µs.

### Solution 14-05.10

(a) A 2-wide design needs **4** read and **2** write ports (6 in all); a 4-wide design needs 8 read and 4 write (12).

(b) Relative to $2 + 1 = 3$ ports for single issue: $(6/3)^2$ = **4** times the area, and $(12/3)^2$ = **16** times. Register files therefore become large, slow and power-hungry as issue width grows. Wide out-of-order cores split them into clusters or banks (14-08).

### Solution 14-05.11

(a) The datapath needs **no** new elements: the B multiplexer can already select rs2, the ALU can add, and the result multiplexer can select memory data. Only the main decoder changes, with one new row for the new opcode:

| RegWrite | ASel | BSel | MemWrite | ResultSrc | Branch | Jump | JALR | ALUOp |
|---|---|---|---|---|---|---|---|---|
| 1 | rs1 | rs2 | 0 | memory | 0 | 0 | 0 | add |

(b) Writing both rd and rs1 in one cycle needs a **second register-file write port**, plus an adder or ALU path for rs1 + 4 and a multiplexer for its value. Write ports are among the most expensive things to add (Problem 14-05.10). Every later design (pipelines, renaming, 14-08) must also track two results per instruction. RISC-V and similar ISAs therefore keep one destination register per instruction and spend a second instruction on the pointer update. Arm's A64 does provide post-increment addressing and pays these costs (14-02 §3.6).

### Solution 14-05.12

(a) Every instruction fetches (10 pJ), reads the register file (6 pJ), uses the ALU (0.1 pJ) and accesses the data memory (20 pJ): **36.1** pJ.

(b) Only the 35% of instructions that are loads or stores use the data memory. The average is $10 + 6 + 0.1 + 0.35 \times 20$ = **23.1** pJ.

(c) The saving is $13.0/36.1$ = **36.0**%. Disabling units that an instruction does not need (gating their clocks or enables) is a basic low-power technique. The ALU's 0.1 pJ shows that the arithmetic itself is a small part of the energy: fetching instructions and moving data dominate, as Horowitz's figures predict.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-05.1a | ResultSrc for lw | 1 | — |
| 14-05.1b | BSel for lw | 1 | — |
| 14-05.1c | RegWrite for bne | 0 | — |
| 14-05.1d | Branch for bne | 1 | — |
| 14-05.2a | immediate of 0xFFC52303 | 0xFFFFFFFC | — |
| 14-05.2b | immediate of 0x00512623 | 0x0000000C | — |
| 14-05.2c | immediate of 0xFE051CE3 | 0xFFFFFFF8 | — |
| 14-05.2d | immediate of 0x001000EF | 0x00000800 | — |
| 14-05.3a | ALU result | 0x00001FFC | — |
| 14-05.3b | value written to x6 | 0x12345678 | — |
| 14-05.3c | next PC | 0x00000204 | — |
| 14-05.4a | load path | 650 | ps |
| 14-05.4b | clock period | 650 | ps |
| 14-05.4c | clock frequency | 1.538 | GHz |
| 14-05.5a | clock period | 830 | ps |
| 14-05.5b | clock frequency | 1.205 | GHz |
| 14-05.6a | average path | 552.0 | ps |
| 14-05.6b | efficiency | 75.6 | % |
| 14-05.7a | register corrupted by the store | 12 | — |
| 14-05.7b | value written | 0x00003FFC | — |
| 14-05.7c | register corrupted by the branch | 16 | — |
| 14-05.7d | value written | 0 | — |
| 14-05.8a | multi-cycle CPI | 4.05 | — |
| 14-05.8b | average time per instruction | 1012.5 | ps |
| 14-05.8c | ratio to single-cycle | 1.387 | — |
| 14-05.9a | cycles with fib(15) | 20781 | — |
| 14-05.9b | run time | 15.17 | µs |
| 14-05.10a | read ports, 2-wide | 4 | — |
| 14-05.10b | write ports, 2-wide | 2 | — |
| 14-05.10c | area factor, 2-wide | 4 | — |
| 14-05.10d | area factor, 4-wide | 16 | — |
| 14-05.11a | new datapath elements for lwr | 0 | — |
| 14-05.11b | write ports for lw.pi | 2 | — |
| 14-05.12a | energy per instruction, always reading memory | 36.1 | pJ |
| 14-05.12b | with the data memory disabled when unused | 23.1 | pJ |
| 14-05.12c | saving | 36.0 | % |
