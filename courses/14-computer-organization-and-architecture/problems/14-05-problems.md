# Problems 14-05 · Single-Cycle Datapath and Control

Chapter: [14-05](../chapters/14-05-single-cycle-datapath.md) · Worked solutions: [14-05 solutions](../solutions/14-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** the single-cycle datapath and control of §3.2–3.3, with the selector encodings of Example 14-05.2 (ResultSrc 0 = ALU, 1 = memory, 2 = PC + 4; ASel 0 = rs1, 1 = PC, 2 = zero; BSel 0 = rs2, 1 = immediate; ImmSel 0 = I, 1 = S, 2 = B, 3 = U, 4 = J); the component delays of §3.4 unless a problem changes them; branches use the ALU's subtract for ALUOp, with the decision from the separate comparator.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-05.1 [A]

**Control signals.** Give ResultSrc and BSel for `lw`, and RegWrite and Branch for `bne`.

### Problem 14-05.2 [A]

**The immediate generator.** Give the 32-bit immediate (in hexadecimal) that the immediate generator produces for each instruction word, with the ImmSel the decoder chooses: 0xFFC52303 (`lw`), 0x00512623 (`sw`), 0xFE051CE3 (`bne`) and 0x001000EF (`jal`).

### Problem 14-05.3 [A]

**Tracing a load.** Trace `lw x6, -4(x10)` at PC = 0x200, with x10 = 0x00002000 and the word 0x12345678 at address 0x1FFC. Give the ALU result, the value written to x6, and the next PC.

### Problem 14-05.4 [B]

**A faster data memory.** The data memory's read time drops from 200 ps to 120 ps; nothing else changes. Find the new load path, the new clock period and frequency, and the instruction class now closest to setting the clock.

### Problem 14-05.5 [B]

**A slower instruction memory.** Starting again from §3.4's delays, the instruction memory's read time rises to 300 ps. Find the new clock period and frequency. Why does the instruction memory's speed matter more than the data memory's in this design?

### Problem 14-05.6 [B]

**Another mix.** For a mix of 20% loads, 10% stores, 50% ALU instructions, 15% branches and 5% JAL, find the mix-weighted average path and the single-cycle efficiency.

### Problem 14-05.7 [B]

**A stuck control signal.** A manufacturing defect holds RegWrite at 1 for every instruction. (a) What does `sw x5, 12(x2)` now do to the register file, with x2 = 0x3FF0? (b) And `beq x1, x2, 16`, with x1 = x2 = 5? (c) Which instruction classes are unaffected?

### Problem 14-05.8 [B]

**Multi-cycle instead.** A multi-cycle version of the datapath uses a 285 ps cycle, set by its slowest step, a memory access with register overhead ($40 + 200 + 25 + 20$ ps, as in 14-06). Loads take 5 cycles, stores and ALU instructions 4, branches and JAL 3. For the mix of Example 14-05.4, find the CPI, the average time per instruction, and its ratio to the single-cycle machine's 730 ps. What does the result say about why multi-cycle designs were used?

### Problem 14-05.9 [B]

**A bigger workload on the lab core.** The lab program computes `fib(10)`. If it computed `fib(15)` instead, how many cycles would the run take on the single-cycle core, and how long at 730 ps?

### Problem 14-05.10 [C]

**Register-file ports.** A processor that executes $w$ instructions per cycle needs $2w$ read ports and $w$ write ports on its register file. In a first-order model each port adds a word line and a bit line to every cell, so cell area grows as the square of the total number of ports. (a) How many ports do 2-wide and 4-wide designs need? (b) By what factor does the register-file area grow relative to the single-issue design, in each case?

### Problem 14-05.11 [C]

**Adding instructions.** (a) A custom indexed load, `lwr rd, rs1, rs2`, loads the word at address rs1 + rs2. It uses the R-type format with an otherwise unused major opcode. What must change in the datapath, and what new row does the main decoder need? (b) A post-increment load, `lw.pi rd, imm(rs1)`, loads from rs1 + imm and also writes rs1 + 4 back to rs1. What new hardware does it need, and why do RISC-style ISAs avoid such instructions?

### Problem 14-05.12 [C]

**Energy per instruction.** Take these energies per access from Horowitz's 45 nm figures (08-09 §3.9, R-157): instruction fetch from an 8 KB cache 10 pJ; register file 6 pJ; 32-bit ALU add 0.1 pJ; data access to a 32 KB cache 20 pJ. Ignore clocking and control. (a) In the single-cycle datapath, every instruction reads the data memory whether or not it needs it. What is the energy per instruction? (b) If a control signal disables the data memory for instructions that do not access it, what is the average for the mix of Example 14-05.4 (35% loads and stores)? (c) What fraction is saved?

---

## Objective coverage

| Learning objective (chapter 14-05) | Problems |
|---|---|
| 1. Datapath elements and their roles | 3, 10, 11 |
| 2. Tracing instructions and their control signals | 1, 3, 7 |
| 3. Main decoder, ALU decoder and immediate generator | 1, 2, 7, 11 |
| 4. Critical paths, clock period and the iron law | 4, 5, 6, 8, 12 |
| 5. The Verilog core | 9, 11 |
