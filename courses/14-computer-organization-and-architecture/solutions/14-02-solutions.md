# Solutions 14-02 · Instruction Set Architecture: RISC-V, Arm and x86

Problems: [14-02 problems](../problems/14-02-problems.md) · Chapter: [14-02](../chapters/14-02-isa-risc-v-arm-x86.md). Every number below is recomputed by [verify_14_02.py](../verify/verify_14_02.py). It encodes with an encoder written from the format table and checks each word against the LLVM assembler. It runs the RISC-V listings, assembled by LLVM, on a small instruction-set simulator, interprets the A64 and x86-64 listings, and discounts the cash flows year by year.

---

## Solutions

### Solution 14-02.1

(a) ADDI is I-type: opcode 0010011, funct3 000. The immediate −1 in 12-bit two's complement is 1111 1111 1111. The fields are imm = 111111111111, rs1 = 01010, funct3 = 000, rd = 01010, opcode = 0010011:

$$
111111111111\ 01010\ 000\ 01010\ 0010011 = \textbf{0xFFF50513} .
$$

(b) SRAI puts the shift amount 3 in imm[4:0] = 00011 and sets instruction bit 30, so imm[11:5] = 0100000 and the 12-bit field is 0x403. With rs1 = rd = 00101 and funct3 = 101:

$$
0100000\ 00011\ 00101\ 101\ 00101\ 0010011 = \textbf{0x4032D293} .
$$

Check with `llvm-mc`: the bytes print as 13 05 F5 FF and 93 D2 32 40, the same words in little-endian order.

### Solution 14-02.2

0xFFC52303 is 111111111100 01010 010 00110 0000011 in binary. The opcode 0000011 is LOAD (I format), and funct3 010 is LW. The destination is rd = 00110 = **6** (x6, t1) and the base is rs1 = 01010 = **10** (x10, a0). The immediate is 111111111100, which sign-extends to **−4**. The instruction is `lw x6, -4(x10)`. With x10 = 0x00002000 it loads the word at 0x2000 − 4 = **0x00001FFC**.

### Solution 14-02.3

(a) No. ADDI's immediate is 12-bit signed, so the largest is **2047**. The assembler rejects 3000; a compiler would build 3000 in a register first (LUI + ADDI) and then use ADD.

(b) −1 sign-extends to all ones: x5 = **0xFFFFFFFF** (−1 as a signed number, 4,294,967,295 unsigned).

(c) LUI puts 0xFFFFF in bits 31–12 and zeros below, giving 0xFFFFF000. As a signed number that is $-2^{12}$ = **−4096**.

(d) Nothing. x0 is hard-wired to zero, so the result is discarded. The specification reserves ADDI with rd = x0 (other than the canonical NOP, `addi x0, x0, 0`) as a *HINT* encoding. Today it executes as a no-op; a future extension may give it a performance meaning, never an architectural effect.

### Solution 14-02.4

(a) Little-endian order puts the least significant byte at the lowest address. Address 0x1000 holds **0xB3**, 0x1001 holds 0x02, 0x1002 holds 0x73 and 0x1003 holds **0x00**.

(b) Read big-endian, the byte at the lowest address becomes the most significant: **0xB3027300**. A dump that looks scrambled in this way is the classic sign of a byte-order mismatch between tool and target.

### Solution 14-02.5

The rule is hi = ⌊(C + 0x800)/4096⌋ mod 2²⁰, with lo = C − 4096·hi read as a signed 12-bit value.

(a) 0x12345678: the low 12 bits are 0x678 = 1656, below 2048, so no rounding is needed. hi = **0x12345** and lo = **1656**; two instructions.

(b) 0x00000800: the low 12 bits are 2048, which is too large for a signed 12-bit immediate. So lo = 2048 − 4096 = **−2048** and hi = **0x00001**: `lui x5, 1` gives 4096, then adding −2048 gives 2048. Two instructions.

(c) 0xFFFFF800: (0xFFFFF800 + 0x800) = 0x1_0000_0000, so hi = 0x100000 mod 2²⁰ = **0x00000** and lo = **−2048**. With hi = 0 the LUI is unnecessary: **1** instruction, `addi x5, x0, -2048`, because −2048 sign-extends to 0xFFFFF800.

(d) 0x7FFFF800: hi = (0x7FFFF800 + 0x800)/4096 = **0x80000** and lo = **−2048**. LUI gives 0x80000000. Adding −2048 gives 0x7FFFF800: the addition wraps modulo 2³², which is exactly what the hardware does. Two instructions.

### Solution 14-02.6

(a) The offset 16 in 13 bits is 0 0000 0001 0000, so imm[12] = 0, imm[11] = 0, imm[10:5] = 000000 and imm[4:1] = 1000. Placing them in the B format (instruction bit 31 = imm[12], bits 30–25 = imm[10:5], bits 11–8 = imm[4:1], bit 7 = imm[11]) with rs2 = 00110, rs1 = 00101 and funct3 = 000:

$$
0\ 000000\ 00110\ 00101\ 000\ 1000\ 0\ 1100011 = \textbf{0x00628863} .
$$

(b) The offset −32 in 13 bits is 8192 − 32 = 1 1111 1110 0000, so imm[12] = 1, imm[11] = 1, imm[10:5] = 111111 and imm[4:1] = 0000. With rs2 = 01011, rs1 = 01010 and funct3 = 101:

$$
1\ 111111\ 01011\ 01010\ 101\ 0000\ 1\ 1100011 = \textbf{0xFEB550E3} .
$$

### Solution 14-02.7

0x001000EF is 0 0000000000 1 00000000 00001 1101111 in binary, split as the J format: imm[20], imm[10:1], imm[11], imm[19:12], rd, opcode. The opcode 1101111 is JAL and rd = 00001 = x1 (ra). Only imm[11] is set, so the offset is $2^{11}$ = **2048** bytes. The target is 0x00010040 + 0x800 = **0x00010840**. JAL writes the address of the next instruction, 0x00010040 + 4 = **0x00010044**, into x1: this is a function call that will return to the instruction after the JAL.

### Solution 14-02.8

(a) The most negative branch offset is −4096 bytes. With 4-byte instructions the branch can reach back **1024** instructions; with 2-byte instructions, **2048**.

(b) The offset 0x00300F00 is 3,149,568 bytes, beyond JAL's +1,048,574, so JAL cannot reach it. Split the offset like a constant. Its low 12 bits, 0xF00 = 3840, exceed 2047, so lo = 3840 − 4096 = **−256** and hi = (0x00300F00 + 0x800) >> 12 = **0x301**. Check: 0x301000 − 256 = 0x300F00. The call is:

```text
auipc t1, 0x301        # t1 = pc + 0x301000        -> 0x00301317
jalr  ra, -256(t1)     # pc = t1 - 256, ra = pc + 4 -> 0xF00300E7
```

AUIPC (U format) is 0x301 in bits 31–12, rd = 00110 and opcode 0010111, giving **0x00301317**. JALR (I format) is imm = 0xF00, rs1 = 00110, funct3 = 000, rd = 00001 and opcode 1100111, giving **0xF00300E7**.

### Solution 14-02.9

(a) Count each version as three parts: instructions before the loop, $n$ passes through the loop, and the final exit.

- **RV32I:** 1 instruction (`addi`) before the loop. Each pass runs `beq` (not taken), `lw`, `add`, `addi`, `addi` and `jal`, which is 6. Then come the final, taken `beq` and `addi`, `jalr`, which is 3. The total is $6n + 4$ = **6004**.
- **A64:** 1 + 5n + 3 (the final `cbz`, then `mov` and `ret`) = $5n + 4$ = **5004**.
- **x86-64:** 1 + 6n + 3 (the final `testq`, `je` and `ret`) = $6n + 4$ = **6004**.

(b) In the rotated versions the exit test is the loop's own backward branch, so the separate jump disappears.

- **RV32I:** 2 + 5n + 2 = $5n + 4$ = **5004**.
- **A64:** 2 + 4n + 2 = $4n + 4$ = **4004**.
- **x86-64:** 3 + 4n + 1 = $4n + 4$ = **4004**.

(c) For RISC-V, rotation cuts (6004 − 5004)/6004 = **16.7**% of the instructions without changing the static size: still 9 instructions, 36 bytes, or 20 with compression. A compiler optimization changed IC in the iron law, not the ISA.

(d) **Condition flags.** `decq` sets the zero flag as a side effect, so `jne` can test it directly. RISC-V's `bne a1, zero, loop` does the same job by comparing a register with zero. A64 does it with `cbnz`, a compare-and-branch on zero. The remaining gap between RISC-V (5 per element) and the others (4) comes from A64's post-increment load and x86's memory-operand add. Each of those does in one instruction what RISC-V does in two.

### Solution 14-02.10

(a) Count instructions whose last byte falls within bytes 0–15.

- **x86-64:** the running ends are 2, 5, 7, 9, 13, 16, 18 and 19, so **6** complete instructions.
- **RV32I:** 16/4 = **4**.
- **RV32IC:** the ends are 2, 4, 8, 10, 12, 14, 16, 18 and 20, so **7**.

(b) In RV32IC every instruction starts on a 2-byte boundary, and the bottom two bits of each 16-bit parcel say whether it starts a 32-bit instruction (11) or is a whole 16-bit one. A decoder can examine all eight parcels of a 16-byte block at once with a few gates each. In x86-64 the length depends on the prefixes, the opcode, the ModRM and SIB bytes and the sizes of the displacement and immediate. Finding where instruction $k$ starts needs the lengths of all earlier instructions, a serial chain. Wide x86 decoders therefore compute a candidate length at every byte offset in parallel, store pre-decode marks with the cached instructions, or cache already-decoded micro-operations (14-08). Each of these costs area and power that a fixed-length or simply marked ISA avoids.

### Solution 14-02.11

(a) 48 × (1 − 0.28) = **34.56** KiB, more than 32 KiB: it does not fit.

(b) The saving needed is 1 − 32/48 = **33.3**%.

(c) The loop's saving is exactly 16/36 = 44.4%, giving 48 × 20/36 = **26.67** KiB. But a six-instruction loop (nine instructions in the whole function) that happens to use mostly compressible instructions is not a program. The specification's typical whole-program saving is 25–30%, and at those figures the code still would not fit (it needs 33.3%). Plan on measured results for the actual code, compiled with the actual compiler.

### Solution 14-02.12

(a) funct7 and funct3 together are 10 bits: **1024** operations under one opcode. RV32I uses only a handful, which leaves room for extensions such as M.

(b) Three 6-bit register fields take 18 bits and the opcode 7, leaving 32 − 25 = **7** bits of function code: **128** operations per opcode, an eighth as many.

(c) Three bits address **8** registers (x8–x15 in RVC). That is why the C extension's most compact forms reach only those eight.

(d) 16 − 10 = **6** bits. RVC formats such as C.ADD do exactly this: two bits mark the instruction as 16-bit, and the other four select the operation.

### Solution 14-02.13

(a) Let $a, b \in [0, 2^{32})$. If $a + b < 2^{32}$ there is no carry and $s = a + b \ge a$. Otherwise there is a carry and $s = a + b - 2^{32} = a - (2^{32} - b) < a$, because $2^{32} - b > 0$. So the carry is 1 exactly when $s < a$ (as unsigned numbers). With a carry-in $c$, add in two steps: $t = a + b$ with carry $c_1 = (t < a)$, then $s = t + c$ with carry $c_2 = (s < t)$. Both cannot be 1. If $c_1 = 1$ then $t = a + b - 2^{32} \le 2^{32} - 2$, so adding 1 cannot wrap. The carry-out is therefore $c_1$ OR $c_2$.

(b) With $a$ = (x11 : x10) and $b$ = (x13 : x12), high word first:

```text
add  x14, x10, x12     # low word of the sum
sltu x15, x14, x10     # carry out of the low word
add  x16, x11, x13     # high word
add  x16, x16, x15     # plus the carry
```

That is **4** instructions; the carry out of the top word is discarded.

(c) The first word takes 2 instructions (`add`, `sltu`). Each middle word takes 5: `add`, `sltu` for $c_1$, `add` of the carry-in, `sltu` for $c_2$, and `or`. The last word takes 2 (`add`, `add` of the carry-in). The total is $2 + 5(n - 2) + 2 = 5n - 6$. A 256-bit addition has $n$ = 8 words: **34** instructions.

(d) x86-64 needs one `add` and 7 `adc`: **8** instructions, a ratio of 34/8 = **4.25**. The carry flag earns its keep in multi-precision arithmetic (public-key cryptography, big-number libraries). For ordinary code, where such chains are rare, the cost is negligible, and having no flags simplifies out-of-order hardware (14-08). The ratio is also a count, not a time: the carry chain is serial in both ISAs, and a wide core can overlap the independent `add` and `sltu` instructions.

### Solution 14-02.14

(a) The royalty is 1.5% × \$2.00 = \$0.03 per unit, or 40 M × \$0.03 = \$1.2 M a year. The five-year annuity factor at 10% is $\sum_{k=1}^{5} 1.1^{-k}$ = 3.7908.

- Option L: $1.5 + 1.2 \times 3.7908$ = **6.049** \$M.
- Option O: $6 + 0.5 \times 3.7908$ = **7.895** \$M.

At this volume licensing is cheaper by **1.846** $M.

(b) Setting $1.5 + 0.03V \times 3.7908 = 7.895$, with $V$ in millions of units a year, gives $V$ = **56.24** million units a year.

(c) At 80 M units a year, option L costs $1.5 + 2.4 \times 3.7908$ = **10.60** \$M. Building is cheaper by **2.70** \$M. Royalties scale with volume and price; engineering is a fixed cost. The finance analogy is operating leverage: option O has high fixed cost and low marginal cost.

(d) It leaves out:

- verification, quality and security-certification cost and risk for an in-house core;
- the software and toolchain ecosystem, and porting the existing code;
- time to market and the risk of slipping;
- future core generations (option O must keep investing; option L gets roadmap upgrades);
- royalty rates that fall with volume, as Arm's filing describes;
- the middle option of licensing a commercial RISC-V core;
- the strategic value of custom extensions and of not depending on a licensor;
- the licence's change-of-control and assignment terms.

### Solution 14-02.15

(a) SW is STORE (opcode 0100011) with funct3 010. The fields are rs2 = x15 = 01111 (the data), rs1 = x10 = 01010 (the base) and imm = 40 = 0000001 01000. The S format puts imm[11:5] = 0000001 in bits 31–25 and imm[4:0] = 01000 in bits 11–7:

0000001 01111 01010 010 01000 0100011 = **0x02F52423**.

(b) In binary: 1111111 01010 01000 000 01100 0100011. Opcode 0100011 is STORE (S format), and funct3 000 is SB (store byte). rs2 = 01010 = x10, the value stored; rs1 = 01000 = x8, the base. The immediate joins bits 31–25 (1111111) and bits 11–7 (01100) into 1111111 01100, which as a 12-bit signed number is **−20**. The instruction is `sb x10, -20(x8)`: store the low byte of x10 at x8 − 20.

(c) A store writes no register, so it has no rd, but it reads two registers. The S format keeps rs1 and rs2 in the same bit positions as every other format, so the register file can be read before the format is known. The immediate therefore fills the two leftover slots, bits 31–25 and the rd position 11–7. Its sign stays in bit 31, as in every format, so sign extension can start at once.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-02.1a | encoding of addi x10, x10, -1 | 0xFFF50513 | — |
| 14-02.1b | encoding of srai x5, x5, 3 | 0x4032D293 | — |
| 14-02.2a | destination register | 6 | — |
| 14-02.2b | base register | 10 | — |
| 14-02.2c | offset | −4 | bytes |
| 14-02.2d | load address | 0x00001FFC | — |
| 14-02.3a | largest ADDI immediate | 2047 | — |
| 14-02.3b | x5 after addi x5, x0, -1 | 0xFFFFFFFF | — |
| 14-02.3c | x5 after lui x5, 0xFFFFF (signed) | −4096 | — |
| 14-02.4a | byte at 0x1000 | 0xB3 | — |
| 14-02.4b | byte at 0x1003 | 0x00 | — |
| 14-02.4c | big-endian misreading | 0xB3027300 | — |
| 14-02.5a | hi for 0x12345678 | 0x12345 | — |
| 14-02.5b | lo for 0x12345678 | 1656 | — |
| 14-02.5c | hi for 0x00000800 | 0x00001 | — |
| 14-02.5d | lo for 0x00000800 | −2048 | — |
| 14-02.5e | hi for 0xFFFFF800 | 0x00000 | — |
| 14-02.5f | lo for 0xFFFFF800 | −2048 | — |
| 14-02.5g | instructions needed for 0xFFFFF800 | 1 | — |
| 14-02.5h | hi for 0x7FFFF800 | 0x80000 | — |
| 14-02.5i | lo for 0x7FFFF800 | −2048 | — |
| 14-02.6a | encoding of beq x5, x6, 16 | 0x00628863 | — |
| 14-02.6b | encoding of bge x10, x11, -32 | 0xFEB550E3 | — |
| 14-02.7a | jump offset | 2048 | bytes |
| 14-02.7b | jump target | 0x00010840 | — |
| 14-02.7c | link address in x1 | 0x00010044 | — |
| 14-02.8a | instructions reachable back, 32-bit | 1024 | — |
| 14-02.8b | instructions reachable back, 16-bit | 2048 | — |
| 14-02.8c | AUIPC immediate | 0x301 | — |
| 14-02.8d | JALR offset | −256 | bytes |
| 14-02.8e | AUIPC encoding | 0x00301317 | — |
| 14-02.8f | JALR encoding | 0xF00300E7 | — |
| 14-02.9a | RV32I count, top-tested | 6004 | instructions |
| 14-02.9b | A64 count, top-tested | 5004 | instructions |
| 14-02.9c | x86-64 count, top-tested | 6004 | instructions |
| 14-02.9d | RV32I count, rotated | 5004 | instructions |
| 14-02.9e | A64 count, rotated | 4004 | instructions |
| 14-02.9f | x86-64 count, rotated | 4004 | instructions |
| 14-02.9g | RISC-V reduction from rotation | 16.7 | % |
| 14-02.10a | complete instructions in 16 bytes, x86-64 | 6 | — |
| 14-02.10b | complete instructions in 16 bytes, RV32I | 4 | — |
| 14-02.10c | complete instructions in 16 bytes, RV32IC | 7 | — |
| 14-02.11a | compressed size at 28% saving | 34.56 | KiB |
| 14-02.11b | saving needed to fit | 33.3 | % |
| 14-02.11c | size at 44.4% saving | 26.67 | KiB |
| 14-02.12a | R-type operations per opcode | 1024 | — |
| 14-02.12b | function bits with 64 registers | 7 | bits |
| 14-02.12c | operations per opcode with 64 registers | 128 | — |
| 14-02.12d | registers addressable by 3 bits | 8 | — |
| 14-02.12e | opcode/function bits in a 16-bit two-register format | 6 | bits |
| 14-02.13a | RV32I instructions, 64-bit add | 4 | — |
| 14-02.13b | RV32I instructions, 256-bit add | 34 | — |
| 14-02.13c | x86-64 instructions, 256-bit add | 8 | — |
| 14-02.13d | ratio | 4.25 | — |
| 14-02.14a | present value, option L | 6.049 | $M |
| 14-02.14b | present value, option O | 7.895 | $M |
| 14-02.14c | advantage of L at 40 M units/yr | 1.846 | $M |
| 14-02.14d | break-even volume | 56.24 | M units/yr |
| 14-02.14e | present value of L at 80 M units/yr | 10.60 | $M |
| 14-02.14f | advantage of O at 80 M units/yr | 2.70 | $M |
| 14-02.15a | encoding of sw x15, 40(x10) | 0x02F52423 | — |
| 14-02.15b | decoded offset of 0xFEA40623 | −20 | bytes |
