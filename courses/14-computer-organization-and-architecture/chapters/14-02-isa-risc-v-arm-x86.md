<!-- status: reviewed -->
# 14-02 · Instruction Set Architecture: RISC-V, Arm and x86

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The instruction-set chapter of a computer organization course: architectural state, instruction formats and encoding, immediates and addressing, RISC against CISC, and the major commercial ISAs (Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 2; Harris & Harris, *Digital Design and Computer Architecture*, RISC-V Edition, ch. 6) |
| **Prerequisites** | [14-01 Performance, Power and the Iron Law](14-01-performance-power-iron-law.md), [08-01 Number Systems and Codes](../../08-digital-logic-design/chapters/08-01-number-systems-and-codes.md), [05-07 Bit Manipulation](../../05-programming-for-engineers/chapters/05-07-bit-manipulation.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. State what an instruction set architecture specifies and what it leaves to the implementation.
2. Encode and decode RV32I instructions in all six formats, including their scrambled immediates, and check them against an assembler.
3. Build any 32-bit constant with LUI and ADDI, and compute the reach of loads, branches and jumps.
4. Contrast RISC-V, Arm (A64) and x86-64 in instruction length, operands, addressing, flags and code density, and relate each choice to the iron law.
5. Explain the open, architecture-license and core-license business models and what each means for a chip company.

---

## 1. Big picture

The **instruction set architecture** (ISA) is the contract between software and hardware: the registers, memory model and instructions that every implementation must honour, bit for bit, so that a program compiled once runs on every chip that claims the ISA. Implementations come and go every year or two; the contract lasts decades, because the software written against it is worth far more than any chip. That is why the ISA is both an engineering object (it sets the instruction count in the iron law and shapes how easily hardware can run fast) and a business asset (whoever controls it controls who may build compatible chips).

- **Three ISAs dominate.** x86-64 in PCs and most servers, Arm in phones, embedded systems and a growing share of servers, and RISC-V, an open standard spreading through microcontrollers, accelerators' control cores and custom silicon.
- **ISA choice is a licensing decision.** Building an x86 chip is effectively closed to newcomers; Arm sells either the right to design your own cores or ready-made cores; RISC-V is free to implement.
- **Compatibility is the moat.** An ISA's value is the software that runs on it: operating systems, compilers, libraries and applications.
- **Custom accelerators** often embed small general-purpose cores to control them; an open ISA lets a company add its own instructions without asking permission.

## 2. Intuition first

**An ISA is a vocabulary, not a machine.** It says which words exist (add, load, branch), what each means exactly, and how each is spelled in bits. It does not say how fast a word is spoken, whether several are spoken at once, or where the speaker keeps notes: those are the implementation's choices (14-05 to 14-09). Two chips with the same ISA can differ tenfold in speed and power and still run the same binary.

**Regular spelling is fast to read.** If every word has the same length and the same parts in the same places, a reader can find the parts without first working out where the word ends. RISC-V instructions are 32 bits with the register fields always in the same positions, so hardware can start reading the registers before it even knows which instruction it has. x86 instructions are 1 to 15 bytes long, and a decoder must work out where each one ends before it can find the next: a cost paid on every instruction, in every chip, forever.

**An analogy from finance, and its limits.** An ISA is like an accounting standard such as IFRS. Every company (implementation) must report in the standard's terms so that any reader (program) can interpret the accounts; the standard says what must be reported, not how the books are kept internally. And like a standard, it is sticky: changing it is far costlier than complying. The analogy breaks on enforcement: an accounting standard tolerates judgement, but an ISA is exact. One bit of different behaviour, in one corner case, breaks some program somewhere, which is why ISA specifications run to hundreds of pages of precise rules.

## 3. Theory

### 3.1 What an ISA specifies

An ISA defines the **architectural state** and how each instruction changes it:

- **Registers.** In RV32I, 32 integer registers x0–x31 of 32 bits each, with x0 hard-wired to zero, plus the program counter (PC). RV64I widens them to 64 bits.
- **Memory.** A byte-addressed address space, the sizes of loads and stores, their alignment rules, byte order (little-endian means the least significant byte sits at the lowest address: x86 is little-endian; RISC-V and Arm permit either order for data but are little-endian in practice, and RISC-V instructions are always stored as little-endian 16-bit parcels [1]), and the memory consistency model for multiple cores (14-12).
- **Instructions.** Their encodings and exact semantics, including corner cases (what a shift by more than the word width does, what happens on division by zero).
- **Privilege and exceptions.** Which state user programs may touch, and what happens on an illegal instruction, a page fault or an interrupt (14-10).

It deliberately leaves out how many cycles anything takes, how many instructions run at once, caches, and branch prediction. The split between **architecture** (the contract) and **microarchitecture** (one implementation) is what lets the same software run on a microcontroller and a server core.

**Load–store versus memory operands.** RISC-style ISAs (RISC-V, Arm) compute only on registers; memory is touched only by explicit loads and stores. x86 lets most arithmetic instructions read or write memory directly (`add eax, [rdi]`). Load–store designs need more instructions but each is simpler, which keeps pipelines regular (14-06); x86 processors internally split memory-operand instructions into load, operate and store micro-operations (14-08), so modern x86 cores are load–store machines underneath.

### 3.2 Design principles

Four principles explain most of RISC-V's choices. The first three are the design principles of Patterson and Hennessy's instruction-set chapter [7]; the fourth is one of the "great ideas" of their first chapter.

1. **Simplicity favours regularity.** All base instructions are 32 bits; register specifiers sit in the same bit positions in every format.
2. **Smaller is faster.** 32 registers, not 128: each register specifier costs bits in every instruction, and a larger register file is slower and costs more power per access.
3. **Good design demands good compromises.** Immediates are only 12 bits in most instructions, so that they fit beside three register fields; larger constants need two instructions (§3.4).
4. **Make the common case fast.** Most constants are small and most branches are short, so the common forms take one instruction; the rare long forms take two.

**The encoding budget.** A 32-bit instruction has 2³² patterns to share among all instructions. RISC-V spends its 7-bit major opcode (bits 6–0) on instruction groups, a 3-bit funct3 and, for register–register operations, a 7-bit funct7 to tell the members apart. Every register field costs $\log_2(\text{number of registers})$ bits: three fields of 5 bits each take 15 of the 32. With 64 registers, the three fields would take 18 bits. Formats with two register fields beside the immediate (I, S and B) would lose 2 immediate bits, and those with one (U and J) would lose 1 (Example 14-02.6). This is the concrete cost behind "smaller is faster".

### 3.3 The six RV32I formats

Every RV32I instruction has one of six formats. Bits are numbered 31 (most significant) down to 0, and the opcode always occupies bits 6–0.

| Format | 31–25 | 24–20 | 19–15 | 14–12 | 11–7 | 6–0 | Used by |
|---|---|---|---|---|---|---|---|
| R | funct7 | rs2 | rs1 | funct3 | rd | opcode | register–register arithmetic |
| I | imm[11:5] | imm[4:0] | rs1 | funct3 | rd | opcode | immediates, loads, JALR |
| S | imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode | stores |
| B | imm[12, 10:5] | rs2 | rs1 | funct3 | imm[4:1, 11] | opcode | conditional branches |
| U | imm[31:12] (bits 31–12) | | | | rd | opcode | LUI, AUIPC |
| J | imm[20, 10:1, 11, 19:12] (bits 31–12) | | | | rd | opcode | JAL |

(In the I format the 12-bit immediate fills bits 31–20; it is split above only to line up with the other rows.)

![The six RV32I formats drawn as 32-bit fields with bit 31 on the left. The opcode is always bits 6–0, rd always bits 11–7, rs1 always 19–15 and rs2 always 24–20; immediate fields fill the remaining positions, and in the B and J formats the immediate's bits are reordered so that each lands where the I and S formats put it.](../../../assets/figures/14-02/formats.svg)

*Figure 1. The RV32I instruction formats. Small boxes labelled 12, 11 and 20 hold the single immediate bits imm[12], imm[11] and imm[20].* The major opcodes used in this course are OP (0110011, 0x33) for register arithmetic, OP-IMM (0010011, 0x13), LOAD (0000011, 0x03), STORE (0100011, 0x23), BRANCH (1100011, 0x63), JAL (1101111, 0x6F), JALR (1100111, 0x67), LUI (0110111, 0x37) and AUIPC (0010111, 0x17).

**Why the immediates are scrambled.** Three rules shape the S, B and J layouts.

- The **sign bit** of every immediate is instruction bit 31, so sign extension can start before the format is known (the specification: "to speed sign-extension circuitry" [1]).
- **rs1, rs2 and rd never move**, so the register file can be read in parallel with decoding.
- **The same immediate bits sit in the same instruction bits** wherever possible. Bits 10:5, for instance, are always in instruction bits 30:25. This minimizes the multiplexers that assemble the immediate.

Branch and jump offsets are always even (instructions are at least 2 bytes long when the compressed extension is present), so their bit 0 is not stored. That frees a bit: B stores imm[12:1] in 12 bits, giving a 13-bit signed byte offset, and J stores imm[20:1] in 20 bits, a 21-bit signed byte offset. The awkward-looking placements (imm[11] of a branch in instruction bit 7, imm[11] of a jump in bit 20) are the price of keeping every other bit where the I and S formats put it.

**Decoding by hand.** To decode a word: read the opcode (bits 6–0) to get the format, then slice the fields. For an immediate, gather its bits into place and sign-extend from bit 31. Example 14-02.2 decodes a branch.

**Ranges.** A field of $n$ bits holding a two's-complement value spans $-2^{n-1}$ to $2^{n-1} - 1$ (08-01). Hence:

| Immediate | Bits | Range (bytes or value) |
|---|---|---|
| I, S (ADDI, loads, stores) | 12 | −2048 to +2047 |
| B (branches) | 13, even | −4096 to +4094 |
| J (JAL) | 21, even | −1,048,576 to +1,048,574 (±1 MiB) |
| U (LUI, AUIPC) | 20, placed in bits 31–12 | any multiple of 4096 |

### 3.4 Building constants and reaching far

**Any 32-bit constant in two instructions.** LUI places a 20-bit value in the upper bits of a register and clears the lower 12; ADDI then adds a 12-bit *signed* immediate. To build a constant $C$, split it as $C = \text{hi} \times 4096 + \text{lo}$ with $-2048 \le \text{lo} \le 2047$. If the low 12 bits of $C$, read as unsigned, are 2048 or more, the signed value lo is negative (it is the low 12 bits minus 4096), and the upper part must be one larger to compensate:

$$
\text{hi} = \Big\lfloor\frac{C + 2048}{4096}\Big\rfloor \bmod 2^{20}, \qquad \text{lo} = C - 4096\,\text{hi} \ (\text{taken modulo } 2^{32}, \text{ then as a signed 12-bit value}) .
$$

Adding 2048 (0x800) before dropping the low 12 bits is exactly the "round up when the low part is negative" rule. Assemblers do this automatically for the pseudo-instruction `li` (load immediate); Example 14-02.3 does it by hand.

**Reaching far.** AUIPC adds a 20-bit upper immediate to the PC, so AUIPC + JALR (or AUIPC + load) reaches anywhere within ±2 GiB of the current instruction: the standard way to call a distant function or load a distant global. A conditional branch to a target beyond ±4 KiB is replaced by an inverted branch over a JAL.

### 3.5 Extensions and the naming scheme

RISC-V is a small base plus optional, separately ratified extensions:

| Letter | Extension | Adds |
|---|---|---|
| I | base integer | 40 instructions [1]: arithmetic, logic, shifts, loads, stores, branches, jumps, fences, system calls |
| M | multiply/divide | MUL, MULH, DIV, REM |
| A | atomics | load-reserved/store-conditional, atomic memory operations (14-12) |
| F, D | floating point | single and double precision, 32 floating-point registers (14-04) |
| C | compressed | 16-bit encodings of common instructions, mixed freely with 32-bit ones |
| V | vector | variable-length vector registers and instructions |
| Zicsr, Zifencei | control | control/status registers, instruction-fetch fences |

A core is named by its base and extensions: RV64IMAFDC, abbreviated **RV64GC** (G for the general-purpose set IMAFD plus Zicsr and Zifencei). **Profiles** bundle a set of extensions that software can assume, so that operating systems can target one name instead of a list of options; RVA23 is the current profile for 64-bit application processors (§9).

**Compressed instructions.** The C extension re-encodes the most common instructions in 16 bits by restricting their operands: many use only the eight registers x8–x15 (3-bit fields), small immediates, or the same register as source and destination (`c.addi a0, 1` means `addi a0, a0, 1`). Because 16- and 32-bit instructions mix freely, the bottom two bits of every instruction say which it is (11 for 32-bit). The specification reports that typically half or more of a program's instructions can use a 16-bit form, shrinking code by about 25–30% [1]; the cost is a more complex decoder.

### 3.6 Arm A64 and x86-64 in contrast

| Feature | RISC-V (RV64) | Arm A64 | x86-64 |
|---|---|---|---|
| Instruction length | 32 bits (16 with C) | 32 bits, fixed | 1 to 15 bytes |
| General registers | 31 + zero register | 31 + zero register / stack pointer | 16 |
| Operands | 3 (rd, rs1, rs2) | 3 | 2 (destination is also a source) |
| Memory in arithmetic | no (load–store) | no (load–store) | yes |
| Condition codes | none: compare-and-branch | flags (NZCV) set by explicit instructions | flags set by most arithmetic |
| Addressing | base + 12-bit offset | base + offset, base + scaled index, pre/post-increment | base + index × {1, 2, 4, 8} + displacement |
| Byte order | instructions little-endian; data little-endian in practice | little-endian in practice (bi-endian capable) | little-endian |

**Arm A64.** Fixed 32-bit instructions like RISC-V, but with richer forms: load/store pair (`ldp`, `stp`, two registers in one instruction), post-increment addressing (`ldr w3, [x0], #4` loads and advances the pointer), conditional select, and condition flags. These pack more work into each instruction, lowering IC at some decoding cost. The older 32-bit Arm and Thumb instruction sets (with 16-bit Thumb encodings) are separate.

**x86-64.** A variable-length encoding grown over decades: optional prefixes, an opcode of one to three bytes, a ModRM byte naming registers and addressing mode, an optional SIB byte for scaled-index addressing, and displacement and immediate fields. The architectural limit on an instruction's length is 15 bytes. Two-operand instructions overwrite their first source (`add rax, rbx` computes rax ← rax + rbx), and most arithmetic sets the flags. The format is dense for common operations (Example 14-02.5) but hard to decode in parallel: to decode several instructions per cycle, a decoder must find where each starts, which modern x86 cores handle with pre-decode marks and caches of already-decoded micro-operations (14-08).

**Flags against compare-and-branch.** x86 and Arm set condition flags as a side effect (or by a compare instruction) and then branch on them. RISC-V branches compare two registers directly (`beq`, `blt`) and has no flags at all. Flags create a hidden dependence between instructions that out-of-order hardware must rename (14-08); compare-and-branch avoids it, at the cost of having no carry flag for multi-word arithmetic (an overflow or carry must be computed with an explicit comparison, Problem 14-02.13).

### 3.7 The ISA and the iron law

The ISA's main lever is **instruction count**, and its main constraints are on **CPI** and **clock period**.

- **Richer instructions** (memory operands, scaled addressing, load pair, post-increment) lower IC. They raise CPI only if the implementation cannot do the extra work in parallel, which modern out-of-order cores often can.
- **Regular, fixed-length encodings** make decoding cheap and parallel, helping both clock period and the number of instructions decoded per cycle.
- **Code density** matters through the instruction cache and memory traffic: smaller code means fewer instruction-cache misses (14-09) and less memory for small devices.

The "RISC versus CISC" debate of the 1980s is largely settled into a hybrid. Every high-performance core translates instructions into simple internal operations; what remains of the difference is decoder complexity and power, code density, and, above all, the software ecosystem and the business model.

### 3.8 Business models

An ISA is intellectual property, and three models govern who may implement one.

- **Open standard (RISC-V).** The specifications are published by RISC-V International and may be implemented by anyone without a licence fee or royalty; members participate in developing the standards. Companies may add custom, non-standard extensions. The trade-off: the ISA is free, but a competitive core is not, so companies either design their own or license cores from IP vendors, and software ecosystems mature more slowly than for an incumbent.
- **Licensed ISA with two tiers (Arm).** Arm licenses both its architecture and its own core designs. With an **implementation (core) licence**, a company builds Arm-designed cores into its chips for a licence fee. With an **architecture licence**, a company designs its own cores that comply with the Arm ISA, for an architecture licence fee. In both cases Arm also collects a royalty on each chip shipped, and both bring the full Arm software ecosystem.
- **Closed ISA (x86).** x86-64 processors come almost entirely from Intel and AMD. AMD's rights rest on a patent cross-licence with Intel, and AMD itself describes the x86 instruction set as controlled by Intel (§9).

These are business arrangements and change over time; §9 gives the current, sourced terms. The engineering consequence is general: a company building a chip chooses, through its ISA, between paying for a mature ecosystem and owning its roadmap.

## 4. Worked examples

### Example 14-02.1 · Encoding an R-type instruction (tier A)

**Setup.** Encode `add x5, x6, x7` in RV32I, in binary and hexadecimal. Then encode `sub x5, x6, x7`, which differs only in funct7 (0100000).

**Solution.** ADD is R-type with opcode 0110011, funct3 000, funct7 0000000. The fields, from bit 31 down, are funct7 = 0000000, rs2 = 7 = 00111, rs1 = 6 = 00110, funct3 = 000, rd = 5 = 00101, opcode = 0110011:

$$
0000000\ 00111\ 00110\ 000\ 00101\ 0110011 = \texttt{0x007302B3} .
$$

SUB changes funct7 to 0100000, which sets bit 30: **0x407302B3**. Stored in little-endian memory, ADD's bytes are B3 02 73 00, which is what the assembler prints (Lab, Part 1).

**Units check.** 7 + 5 + 5 + 3 + 5 + 7 = 32 bits.

**Sanity check.** The low byte B3 = 1011 0011 ends in 11 (a 32-bit instruction) and its low 7 bits are 0110011, the OP opcode.

### Example 14-02.2 · Decoding a branch (tier A)

**Setup.** Decode the RV32I word 0xFE051CE3.

**Solution.** In binary: 1111111 00000 01010 001 11001 1100011. The opcode 1100011 is BRANCH (B format); funct3 001 is BNE; rs1 = 01010 = x10 (a0); rs2 = 00000 = x0. The immediate is gathered from four places: imm[12] = bit 31 = 1; imm[10:5] = bits 30–25 = 111111; imm[4:1] = bits 11–8 = 1100; imm[11] = bit 7 = 1. So imm[12:1] = 1 1 111111 1100 and, with imm[0] = 0, the 13-bit value is 1111111111000, which as a signed number is **−8**. The instruction is `bne x10, x0, -8`: branch back two instructions if a0 is not zero.

**Units check.** The offset is in bytes; −8 is two 4-byte instructions back.

**Sanity check.** Bit 31 is 1, so the offset must be negative, as a loop's backward branch should be.

### Example 14-02.3 · Building a 32-bit constant (tier B)

**Setup.** Load 0xDEADBEEF into x5 with LUI and ADDI. Give the two immediates and both encodings.

**Solution.** The low 12 bits are 0xEEF = 3823, which is 2048 or more, so as a signed 12-bit value they are 3823 − 4096 = **−273**. The upper part must be rounded up: $\text{hi} = (\text{0xDEADBEEF} + \text{0x800}) \gg 12$ = **0xDEADC**. Check: 0xDEADC000 − 273 = 0xDEADC000 − 0x111 = 0xDEADBEEF. The instructions are `lui x5, 0xDEADC` = **0xDEADC2B7** and `addi x5, x5, -273` = **0xEEF28293**.

**Units check.** LUI's immediate fills bits 31–12 (20 bits); ADDI's fills bits 31–20 (12 bits).

**Sanity check.** Using the "obvious" upper part 0xDEADB would give 0xDEADB000 − 273 = 0xDEADAEEF, off by 4096: forgetting the rounding is the classic bug.

### Example 14-02.4 · How far can a branch reach? (tier B)

**Setup.** (a) Give the largest forward and backward branch offsets in bytes and in 4-byte instructions. (b) A loop body is 1500 instructions long, all 32-bit. Can its closing branch reach the top? (c) Give the reach of JAL.

**Solution.** (a) The B-type offset is a 13-bit signed even number: from −4096 to **+4094** bytes, that is **−1024** to +1023 instructions back or forward (the assembler confirms that `beq x5, x6, 4094` and `beq x5, x6, -4096` both encode). (b) Branching back over 1500 instructions needs −6000 bytes, beyond −4096: no. The compiler inverts the condition and branches *forward* over a JAL, which can jump back up to 1 MiB. (c) JAL's 21-bit even offset spans **±1 MiB** (−1,048,576 to +1,048,574 bytes).

**Units check.** Offsets are bytes; dividing by 4 gives instructions.

**Sanity check.** The asymmetry (−4096 but +4094) is the two's-complement range of a 13-bit number with its last bit forced to zero.

### Example 14-02.5 · Code density across ISAs (tier B)

**Setup.** One function sums an array of 32-bit integers (pointer in the first argument register, count in the second). Written as directly as possible in each ISA and assembled with LLVM's assembler, it takes 9 instructions in RV32I, 8 in A64 and 8 in x86-64. Find the code size in each case, with and without RISC-V's compressed extension, and compare.

The three listings (in the lab as `sum_rv32.s`, `sum_a64.s` and `sum_x86.s`; x86 in AT&T syntax, source before destination) are:

```text
RV32I                     A64                       x86-64
sum:  addi t0, zero, 0    sum:  mov  w2, wzr        sum:  xorl  %eax, %eax
loop: beq  a1, zero, done loop: cbz  x1, done       loop: testq %rsi, %rsi
      lw   t1, 0(a0)            ldr  w3, [x0], #4         je    done
      add  t0, t0, t1           add  w2, w2, w3           addl  (%rdi), %eax
      addi a0, a0, 4            sub  x1, x1, #1           addq  $4, %rdi
      addi a1, a1, -1           b    loop                 decq  %rsi
      jal  zero, loop     done: mov  w0, w2               jmp   loop
done: addi a0, t0, 0            ret                 done: ret
      jalr zero, 0(ra)
```

**Solution.** Assembling each version (Lab, Part 3): RV32I **36** bytes (9 × 4); RV32IC **20** bytes (8 of the 9 compress; `lw t1, 0(a0)` does not, because t1 is outside x8–x15); A64 **32** bytes (8 × 4); x86-64 **19** bytes (instructions of 1 to 3 bytes, with one 4-byte `add $4, %rdi`). Compression saves **44.4**% of RV32I's size here, bringing RISC-V within one byte of x86-64.

**Units check.** Bytes are counted from the assembled object file's text section.

**Sanity check.** A64 needs one fewer instruction than RV32I because its post-increment load does a load and a pointer update in one instruction; x86-64 is densest because its common instructions are short and it can add from memory directly. A tiny loop exaggerates the differences: for whole programs the specification's typical saving from compression is 25–30% [1].

### Example 14-02.6 · What more registers would cost (tier C)

**Setup.** In an I-type instruction, a 7-bit opcode, a 3-bit funct3 and two register fields share the 32 bits with the immediate. Find the immediate's width and range with 16, 32 and 64 registers.

**Solution.** A field naming one of $R$ registers needs $\log_2R$ bits. The immediate gets $32 - 7 - 3 - 2\log_2R$ bits: with 16 registers, **14** bits (−8192 to +8191); with 32, **12** bits (−2048 to +2047); with 64, **10** bits (−512 to +511). R-type instructions would need $3\log_2R$ = 18 bits of register fields with 64 registers, leaving 14 for opcodes and functions.

**Units check.** All quantities are bit counts; ranges are $-2^{n-1}$ to $2^{n-1} - 1$.

**Sanity check.** Doubling the registers costs one bit per register field, and every bit halves the immediate range: more registers mean fewer spills to memory (lower IC) but more constants and offsets that need two instructions (higher IC). 32 is the compromise RISC-V and A64 both chose.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-02.1a | encoding of add x5, x6, x7 | 0x007302B3 | — |
| Ex 14-02.1b | encoding of sub x5, x6, x7 | 0x407302B3 | — |
| Ex 14-02.2a | branch offset of 0xFE051CE3 | −8 | bytes |
| Ex 14-02.3a | ADDI immediate for 0xDEADBEEF | −273 | — |
| Ex 14-02.3b | LUI immediate | 0xDEADC | — |
| Ex 14-02.3c | LUI encoding | 0xDEADC2B7 | — |
| Ex 14-02.3d | ADDI encoding | 0xEEF28293 | — |
| Ex 14-02.4a | largest forward branch | 4094 | bytes |
| Ex 14-02.4b | largest backward branch | −1024 | instructions |
| Ex 14-02.4c | JAL reach | 1 | MiB |
| Ex 14-02.5a | RV32I code size | 36 | bytes |
| Ex 14-02.5b | RV32IC code size | 20 | bytes |
| Ex 14-02.5c | A64 code size | 32 | bytes |
| Ex 14-02.5d | x86-64 code size | 19 | bytes |
| Ex 14-02.5e | saving from compression | 44.4 | % |
| Ex 14-02.6a | immediate width with 16 registers | 14 | bits |
| Ex 14-02.6b | immediate width with 32 registers | 12 | bits |
| Ex 14-02.6c | immediate width with 64 registers | 10 | bits |

## 5. Simulate it

The lab, [labs/14-02-lab](../labs/14-02-lab/README.md), is a notebook that uses `llvm-mc`, the LLVM assembler (installation in the [lab handout](../labs/14-02-lab/README.md#tools) and [SETUP](../../../SETUP.md)):

1. An RV32I encoder and decoder written from the format table, checked instruction by instruction against `llvm-mc`.
2. A constant builder for LUI + ADDI, tested on 100,000 random constants, with a count of how many low halves need the upper part rounded up.
3. Code size: assemble the array-sum function for RV32I, RV32IC, A64 and x86-64 and print each instruction's bytes.
4. A 30-line RV32I simulator that loads the assembler's machine code, runs the top-tested and rotated loops on an array, and counts the instructions executed, connecting static size to dynamic instruction count.

**Guided exercise (predict, then run).** **Before running Part 3,** predict which of the four versions is smallest and which is largest. Then run it. (x86-64 at 19 bytes is smallest and RV32I at 36 bytes largest; RV32IC at 20 bytes nearly matches x86-64.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Fixed instruction length | Simple, parallel decode; precise fetch | Code size | ISA architect |
| Variable length / compressed forms | Code density, I-cache hit rate | Decoder complexity and power | ISA architect, CPU team |
| More registers | Fewer spills (lower IC) | Shorter immediates, bigger register file | ISA architect |
| Richer addressing and fused operations | Lower IC | Decode complexity; more work per instruction | ISA architect, compiler team |
| Condition flags | Compact compare-and-branch sequences, carry chains | Hidden dependences to rename | ISA architect |
| Custom extensions | Big speedups on a target workload | Software fragmentation; compiler support | Product architect |
| Open versus licensed ISA | Freedom and no royalty (open); mature ecosystem (licensed) | Engineering and ecosystem work (open); fees, royalties and roadmap dependence (licensed) | CEO, CTO, corporate development |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| RV32I instruction | 32 bits; opcode in bits 6–0; rd 11–7, rs1 19–15, rs2 24–20 | §3.3 |
| I/S immediate range | −2048 to +2047 | 12 bits |
| Branch reach | −4096 to +4094 bytes | 13-bit even offset |
| JAL reach | ±1 MiB | 21-bit even offset |
| x86-64 instruction length | 1 to 15 bytes | §3.6 |
| Compressed RISC-V saving | 44% on the array-sum loop | Example 14-02.5 |
| RISC-V NOP | 0x00000013 (`addi x0, x0, 0`) | canonical encoding |

## 8. Common mistakes

- **Forgetting that immediates are signed.** ADDI with 0xFFF adds −1, not 4095; a constant with bit 11 set needs the LUI part rounded up.
- **Mis-assembling B and J immediates.** Their bits are scrambled and bit 0 is implicit; slice them field by field.
- **Reading bytes in the wrong order.** x86 is little-endian, RISC-V and Arm systems almost always are, and RISC-V instructions always are: the first byte in memory is the least significant.
- **Equating the ISA with performance.** A fast implementation of any of the three ISAs beats a slow implementation of another; the ISA sets instruction count and decoding cost, not the outcome.
- **Assuming "RISC-V is free" means free chips.** The specification costs nothing; a competitive core, its verification and its software ecosystem cost as much as for any other ISA.
- **Mixing up the two Arm licences.** A core licence buys Arm's designs; an architecture licence buys the right to design your own compatible cores.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **RISC-V specifications.** The ratified manuals are now versioned by date. The current set, 20260120, has the base RV32I and RV64I at version 2.1 and the machine- and supervisor-level privileged architecture at 1.13 [1, R-201] **[Established]**.
- **Profiles.** RVA23 (version 1.0, ratified in Oct 2024) is the profile for 64-bit application processors. It makes the vector (V) and hypervisor extensions mandatory, where RVA22 left them optional, and Google described it as the baseline requirement for the Android RISC-V ABI [2, R-202] **[Established]**.
- **RISC-V licensing.** RISC-V International, a non-profit founded in 2015 and incorporated in Switzerland, states that there is no fee to use the ISA and that implementations may be proprietary and closed-source; using the RISC-V *trademark* requires a licence, granted to members for compliant implementations [3, R-203] **[Established]**.
- **Arm's model and its economics.** Arm's Form 20-F for the year to 31 Mar 2026 lists five licensing models: Compute Subsystems (CSS), Arm Total Access, Arm Flexible Access, technology licence agreements (TLAs, one core design for a fixed fee) and architecture licence agreements (ALAs, the right to design compliant cores). "Regardless of the license model", Arm receives a royalty on substantially every chip, set as a percentage of the chip's average selling price or a fixed amount per chip, with rates that typically fall as volume grows. Revenue was $4,920 M: royalties $2,613 M (53%) and licence and other revenue $2,307 M [4, R-204] **[Established]**.
- **x86.** AMD's rights rest on its 2009 settlement and patent cross-licence with Intel: Intel paid AMD $1.25 billion, the licences are royalty-free, and the agreement terminates automatically if either party undergoes a change of control. AMD's latest 10-K still describes the x86 instruction set as "controlled by Intel" [5, R-205] **[Established]**. In Oct 2024 the two companies formed the x86 Ecosystem Advisory Group to align their extensions; at its first anniversary AMD reported FRED (event delivery) finalized, AVX10 (vectors) established, a ChkTag memory-tagging specification introduced, and ACE (matrix extensions) accepted [6, R-206] **[Established]**.
- **x86 instruction length.** Intel's current manual (Sep 2026) states that "the maximum length of an Intel 64 and IA-32 instruction remains 15 bytes" [8, R-207] **[Established]**.

### Why it matters commercially

- **ISA control is roadmap control.** A company on a licensed ISA depends on the licensor's terms and timetable; one on an open ISA owns its roadmap but carries the engineering **[Established]**.
- **Software compatibility is the moat.** Moving a product line to another ISA means recompiling, re-verifying and re-certifying its software, which is why ISA transitions are rare and slow **[Established]**.
- **Custom instructions sell accelerators.** An open ISA lets a company add domain-specific instructions to a control core inside its own chips without a licensor's permission.
- **ISA rights travel badly in M&A.** The AMD–Intel cross-licence terminates on a change of control of either party [5], so an acquirer of either company would put its x86 rights in play. Arm's 20-F discloses litigation with Qualcomm over architecture-licence rights after Qualcomm's acquisition of Nuvia, with a Sep 2025 judgment for Qualcomm that Arm was appealing at the filing date [4]. In diligence on any processor company, read the change-of-control and assignment clauses of its ISA and core licences **[Established]**.
- **Royalties scale with the customer's success.** A royalty set as a percentage of chip price taxes every unit and every price increase; an architecture licence or an open ISA converts that variable cost into fixed engineering cost (Problem 14-02.14).

### Marketing vs Reality

- **"RISC-V is free."** *Reality:* the ISA licence is free; cores, verification, compilers, operating-system support and security certification are not. *Sanity check:* ask what the company pays for its cores, toolchain and verification, and how much of its software runs on RISC-V today.
- **"Our ISA makes our chip efficient."** *Reality:* the ISA sets decoding cost and instruction count, but process, microarchitecture, caches and design quality dominate efficiency. *Sanity check:* compare chips of the same process node and power class across ISAs.
- **"Licensing revenue is surging."** *Reality:* Arm's licence and other revenue rose from $1,839 M to $2,307 M in FY2026, but licence and other revenue from related parties rose from $418 M to $1,009 M, more than the whole increase [4]. *Sanity check:* read the related-party note before extrapolating licence growth to the market.
- **"Drop-in compatible."** *Reality:* compatibility is defined by the specification and its profiles; custom extensions and missing optional ones break binaries. *Sanity check:* ask which profile the chip conforms to, and whether it passes the official compatibility tests.

### Questions for engineering leaders

1. **"Why this ISA, and what would it cost to move?"**
   *Strong:* a quantified comparison of licence costs, core performance, ecosystem readiness and switching cost. *Evasive:* "industry standard" with no numbers.
2. **"Which profile or architecture version do your cores implement, and how is compatibility verified?"**
   *Strong:* a named profile or version and the official test suites passed. *Evasive:* "fully compatible".
3. **"Which custom instructions have you added, and how does your software use them?"**
   *Strong:* specific extensions, compiler support and measured speedups on target workloads. *Evasive:* "proprietary acceleration".
4. **"What is your licence model and royalty exposure per unit?"**
   *Strong:* the licence type, royalty basis and how it scales with volume and price. *Evasive:* "standard terms".
5. **"How mature is the software ecosystem on this ISA for your market?"**
   *Strong:* named operating systems, toolchains, libraries and certifications available today. *Evasive:* "the community is growing fast".

## 10. Concept check

**Q1.** What does an ISA specify, and what does it leave to the implementation?

<details><summary>Answer</summary>

It specifies the architectural state (registers, PC, memory and its model), every instruction's encoding and exact effect, and privilege and exception behaviour. It leaves out timing, parallelism, caches, branch prediction and all other microarchitectural choices.

</details>

**Q2.** Why do the register fields of RISC-V instructions never move between formats?

<details><summary>Answer</summary>

So that the hardware can read the register file using bits 19–15 and 24–20 before it has decoded which instruction it has, overlapping register read with decode.

</details>

**Q3.** Why is the sign bit of every RISC-V immediate in bit 31?

<details><summary>Answer</summary>

So that sign extension, which depends only on the sign bit, can begin immediately and identically for every format.

</details>

**Q4.** Why does building 0xDEADBEEF need LUI 0xDEADC rather than 0xDEADB?

<details><summary>Answer</summary>

ADDI's 12-bit immediate is signed. The low 12 bits, 0xEEF, exceed 2047, so they act as −273; the upper part must be one larger (0xDEADC000) so that adding −273 lands on 0xDEADBEEF.

</details>

**Q5.** Name two ways x86-64 differs from RISC-V in its instruction format and operands.

<details><summary>Answer</summary>

Variable length (1 to 15 bytes) against fixed 32 bits; two operands with the destination also a source against three operands; arithmetic that can take a memory operand against load–store only; condition flags against compare-and-branch.

</details>

**Q6.** What is the difference between an Arm architecture licence and a core licence?

<details><summary>Answer</summary>

A core (implementation) licence lets a company use Arm's own processor designs; an architecture licence lets it design its own cores that implement the Arm ISA. Both pay Arm; the second requires far more engineering and gives more control.

</details>

**Q7.** Why can code density matter for performance, not just memory size?

<details><summary>Answer</summary>

Denser code fits more of a program in the instruction cache and moves fewer bytes from memory, so it causes fewer instruction-cache misses and stalls (14-09).

</details>

Now work the [problem set](../problems/14-02-problems.md).

## 11. Key terms

[Instruction set architecture (ISA)](../../../reference/glossary.md#instruction-set-architecture-isa) · [Microarchitecture](../../../reference/glossary.md#microarchitecture) · [Load–store architecture](../../../reference/glossary.md#load-store-architecture) · [RISC-V](../../../reference/glossary.md#risc-v) · [Instruction format](../../../reference/glossary.md#instruction-format) · [Immediate](../../../reference/glossary.md#immediate) · [Sign extension](../../../reference/glossary.md#sign-extension) · [Compressed instructions](../../../reference/glossary.md#compressed-instructions) · [Endianness](../../../reference/glossary.md#endianness) · [Condition codes](../../../reference/glossary.md#condition-codes) · [Code density](../../../reference/glossary.md#code-density) · [Architecture license](../../../reference/glossary.md#architecture-license) · [Core license](../../../reference/glossary.md#core-license)

## 12. Connections

- **Builds on:** two's complement and sign extension ([08-01](../../08-digital-logic-design/chapters/08-01-number-systems-and-codes.md)); bit fields and masks ([05-07](../../05-programming-for-engineers/chapters/05-07-bit-manipulation.md)); the iron law ([14-01](14-01-performance-power-iron-law.md)).
- **Next:** [14-03 Assembly and the Compilation Stack](14-03-assembly-and-the-compilation-stack.md), which writes programs in these instructions.
- **Used later:** decoding in the single-cycle datapath ([14-05](14-05-single-cycle-datapath.md)); flags and renaming ([14-08](14-08-out-of-order-and-superscalar.md)); privilege and exceptions ([14-10](14-10-virtual-memory.md)); atomics ([14-12](14-12-multicore-coherence-consistency.md)); vector and accelerator instructions ([14-13](14-13-gpus-and-simt.md), [14-14](14-14-ai-accelerators.md)).

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 2 (instructions: language of the computer).
- S. L. Harris and D. M. Harris, *Digital Design and Computer Architecture*, RISC-V Edition, ch. 6 (architecture).
- The RISC-V Instruction Set Manual, Volume I: Unprivileged Architecture (RISC-V International), chapters on RV32I and the compressed extension.
- MIT OpenCourseWare 6.004, *Computation Structures*: the lectures on the RISC-V ISA and assembly.
- D. Patterson and A. Waterman, *The RISC-V Reader: An Open Architecture Atlas* (Strawberry Canyon, 2017).

## 14. Sources

1. RISC-V International, *The RISC-V Instruction Set Manual, Volume I: Unprivileged Architecture*, version 20260120: chapters "RV32I Base Integer Instruction Set" (40 instructions; register fields in fixed positions; sign bit in bit 31; branch range ±4 KiB; JAL ±1 MiB; NOP as ADDI x0, x0, 0), "Introduction" (memory endianness and little-endian instruction parcels) and "C Extension" (50–60% of instructions compressible, 25–30% code-size reduction). [R-201](../../../reference/research-log.md#r-201--risc-v-unprivileged-isa-manual-version-20260120)
2. RISC-V International, *RVA23 Profiles*, version 1.0 (2024-10-17), and press release "RISC-V Announces Ratification of the RVA23 Profile Standard" (21 Oct 2024). [R-202](../../../reference/research-log.md#r-202--risc-v-rva23-profile)
3. RISC-V International, FAQ and About pages (read Nov 2026). [R-203](../../../reference/research-log.md#r-203--risc-v-licensing-and-trademark-model)
4. Arm Holdings plc, Form 20-F for the fiscal year ended 31 Mar 2026 (filed with the SEC 26 May 2026). [R-204](../../../reference/research-log.md#r-204--arm-licensing-models-and-fy2026-revenue-form-20-f)
5. Advanced Micro Devices, Form 8-K (report dated 11 Nov 2009) on the Intel settlement and patent cross-licence; Form 10-K for the fiscal year ended 27 Dec 2025. [R-205](../../../reference/research-log.md#r-205--amdintel-patent-cross-licence-2009)
6. Intel and AMD, "Intel and AMD Form x86 Ecosystem Advisory Group…" (press release, 15 Oct 2024); AMD, "AMD and Intel Celebrate First Anniversary of x86 Ecosystem Advisory Group…" (blog, 13 Oct 2025). [R-206](../../../reference/research-log.md#r-206--x86-ecosystem-advisory-group)
7. D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 1–2 (design principles).
8. Intel, *Intel 64 and IA-32 Architectures Software Developer's Manual*, Vol. 2, order no. 325383-093US (Sep 2026), §2.3.11. [R-207](../../../reference/research-log.md#r-207--x86-maximum-instruction-length)

Every encoding, range check and code size in this chapter is reproduced by the LLVM assembler (`llvm-mc`, version 18) in the verify script, alongside an independent encoder written from the format table.
