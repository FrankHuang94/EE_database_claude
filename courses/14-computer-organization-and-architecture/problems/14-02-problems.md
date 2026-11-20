# Problems 14-02 · Instruction Set Architecture: RISC-V, Arm and x86

Chapter: [14-02](../chapters/14-02-isa-risc-v-arm-x86.md) · Worked solutions: [14-02 solutions](../solutions/14-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** RV32I unless stated; register numbers are written x0–x31, with ABI names (a0 = x10, a1 = x11, t0 = x5, t1 = x6, ra = x1) where the listings use them; encodings are given in hexadecimal, most significant digit first; offsets are in bytes; "instruction count" means instructions executed. The format table and opcodes are in §3.3 of the chapter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution. You can check any encoding yourself with the assembler used in the lab: `llvm-mc -triple=riscv32 -mattr=-c -show-encoding`.

---

## Problems

### Problem 14-02.1 [A]

**Encoding I-type instructions.** (a) Encode `addi x10, x10, -1`. (b) Encode `srai x5, x5, 3`. (The shift-immediate instructions are I-type with funct3 101; the shift amount sits in the low 5 bits of the immediate field, and SRAI is distinguished from SRLI by setting instruction bit 30.)

### Problem 14-02.2 [A]

**Decoding a load.** Decode the RV32I word 0xFFC52303: give the instruction's format, mnemonic, destination register, base register and offset. If x10 holds 0x00002000, from which address does it load?

### Problem 14-02.3 [A]

**Immediates are signed.** (a) Can `addi x5, x5, 3000` be encoded? Give the largest immediate ADDI accepts. (b) After `addi x5, x0, -1`, what does x5 hold, in hexadecimal? (c) After `lui x5, 0xFFFFF`, what does x5 hold, as a signed decimal number? (d) What does `addi x0, x5, 7` do?

### Problem 14-02.4 [A]

**Byte order.** The instruction `add x5, x6, x7` (0x007302B3) is stored at address 0x1000. (a) Which byte is stored at address 0x1000, and which at 0x1003? (b) A debugging tool mistakenly reads the four bytes as a big-endian 32-bit word. What value does it display?

### Problem 14-02.5 [B]

**Building constants.** For each constant, give the LUI immediate (hi) and the ADDI immediate (lo) that build it, and say whether one instruction would do: (a) 0x12345678; (b) 0x00000800; (c) 0xFFFFF800; (d) 0x7FFFF800.

### Problem 14-02.6 [B]

**Encoding branches.** Encode (a) `beq x5, x6, 16` and (b) `bge x10, x11, -32` (BGE has funct3 101). Show the immediate's bits being placed into the B format.

### Problem 14-02.7 [B]

**Decoding a jump.** The word 0x001000EF sits at address 0x00010040. Decode it, and give the jump target and the value written to the destination register.

### Problem 14-02.8 [B]

**Reaching far.** (a) A loop ends with a conditional branch back to its first instruction. If every instruction is 32 bits, how many instructions can the branch jump back over at most? How many if every instruction is a 16-bit compressed one? (b) A function at offset +0x00300F00 bytes from a call site is to be called. Can JAL reach it? Give the AUIPC and JALR immediates of a two-instruction call through t1, and encode both instructions, `auipc t1, hi` and `jalr ra, lo(t1)`.

### Problem 14-02.9 [B]

**Static size against dynamic count.** Example 14-02.5's array-sum loops test the count at the top. *Loop rotation* moves the test to the bottom, after one check at entry. The rotated versions (in the lab as `sum_*_rot.s`) are:

```text
RV32I                     A64                       x86-64
sum:  addi t0, zero, 0    sum:  mov  w2, wzr        sum:  xorl  %eax, %eax
      beq  a1, zero, done       cbz  x1, done             testq %rsi, %rsi
loop: lw   t1, 0(a0)      loop: ldr  w3, [x0], #4         je    done
      add  t0, t0, t1           add  w2, w2, w3     loop: addl  (%rdi), %eax
      addi a0, a0, 4            sub  x1, x1, #1           addq  $4, %rdi
      addi a1, a1, -1           cbnz x1, loop             decq  %rsi
      bne  a1, zero, loop done: mov  w0, w2               jne   loop
done: addi a0, t0, 0            ret                 done: ret
      jalr zero, 0(ra)
```

(a) For an array of $n$ = 1000 elements, find the number of instructions each original (top-tested) version executes. (b) Repeat for the rotated versions. (c) By what percentage does rotation cut the RISC-V instruction count? (d) Which ISA feature lets the rotated x86-64 loop omit a separate test instruction?

### Problem 14-02.10 [B]

**Finding instruction boundaries.** A front end fetches 16 aligned bytes per cycle. The original (top-tested) sum function starts at the beginning of a fetch block. The x86-64 instruction lengths in bytes are 2, 3, 2, 2, 4, 3, 2, 1; the RV32IC lengths are 2, 2, 4, 2, 2, 2, 2, 2, 2. (a) How many complete instructions does the first 16-byte block contain for x86-64, RV32I and RV32IC? (b) Why is finding those boundaries harder for x86-64 than for RV32IC, even though both have variable lengths?

### Problem 14-02.11 [B]

**Code density and the instruction cache.** A product's performance-critical code occupies 48 KiB as RV32I and must fit in a 32 KiB instruction cache. (a) With a 28% saving from compression, does it fit? Give its size. (b) What saving would be needed? (c) What size would it have with the 44.4% saving of the array-sum loop, and why is that figure an unsafe planning assumption?

### Problem 14-02.12 [B]

**The encoding budget.** (a) RV32I R-type instructions use funct7 and funct3 to distinguish operations under one major opcode. How many distinct operations can one major opcode hold? (b) With 64 registers, three register fields and a 7-bit opcode, how many bits are left for function fields, and how many operations could one opcode hold? (c) RVC's three-bit register fields address how many registers? (d) A 16-bit compressed instruction with two full 5-bit register fields leaves how many bits for its opcode and function fields?

### Problem 14-02.13 [C]

**Multi-word addition without a carry flag.** RISC-V has no carry flag. The carry out of an unsigned addition $s = a + b \bmod 2^{32}$ is 1 exactly when $s < a$ (unsigned), which `sltu` computes. (a) Prove this carry rule. (b) Write the RV32I sequence that adds two 64-bit numbers held as pairs of 32-bit words, and count its instructions. (c) Generalize to $n$ words: show that the count is $5n - 6$ for $n \ge 2$, and find it for a 256-bit addition. (d) x86-64 in 32-bit-word form uses one `add` and then `adc` (add with carry) for each further word. Find its count for 256 bits and the ratio of the two.

### Problem 14-02.14 [C]

**The economics of an ISA choice.** *The figures in this problem are hypothetical, chosen for the exercise; real licence terms are confidential and vary.* A microcontroller line will ship 40 million units a year for five years at an average selling price of $2.00. Option L licenses a ready-made core: a $1.5 M licence fee now and a royalty of 1.5% of the selling price on every unit, paid as units ship. Option O builds an in-house RISC-V core: $6 M of engineering now and $0.5 M a year to maintain it, with no royalty. Treat each year's flows as occurring at year-end, and discount at 10% a year. (a) Find the present value of each option's cost. (b) Find the annual volume at which the two cost the same. (c) At 80 million units a year, which is cheaper, and by how much in present value? (d) Name three costs or risks this comparison leaves out.

---

## Objective coverage

| Learning objective (chapter 14-02) | Problems |
|---|---|
| 1. What an ISA specifies and leaves to the implementation | 3, 4, 9, 12 |
| 2. Encode and decode RV32I in all formats | 1, 2, 6, 7 |
| 3. Build constants; compute the reach of branches and jumps | 3, 5, 8 |
| 4. Contrast RISC-V, A64 and x86-64; relate to the iron law | 9, 10, 11, 13 |
| 5. Open, architecture-licence and core-licence models | 14 |
