# Problems 08-01 · Number Systems and Codes

Chapter: [08-01](../chapters/08-01-number-systems-and-codes.md) · Worked solutions: [08-01 solutions](../solutions/08-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** a subscript gives the base (1011₂, 3F7₁₆); "8-bit" means two's complement unless a number is called unsigned; Hamming(7,4) bit positions are numbered 1 to 7 from the left, with check bits at positions 1, 2 and 4, as in the chapter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-01.1 [A]

**Conversions.** (a) Convert 3F7₁₆ to decimal and to binary. (b) Convert 245 to binary, octal and hexadecimal. (c) Convert 0.375 and 0.3 to binary, giving 8 fractional bits, and say which conversion terminates and why.

### Problem 08-01.2 [A]

**How many bits?** (a) How many bits does a counter need to count 1000 distinct states? (b) A sensor interface must represent 0 to 3.3 V in steps of at most 0.1 mV. How many levels is that, and how many bits?

### Problem 08-01.3 [A]

**Two's complement.** In 8 bits: (a) write −1, −77 and −128 in hexadecimal; (b) give the values of the patterns 80₁₆ and C9₁₆; (c) negate C9₁₆ by inverting and adding one, and check the result.

### Problem 08-01.4 [B]

**Overflow in 4 bits.** For each 4-bit two's-complement sum, give the 4-bit result as a signed number, the carries $c_3$ (into the top column) and $c_4$ (out of it), and whether signed overflow occurred: (a) 5 + 4; (b) −8 + (−1); (c) 7 + (−8); (d) −3 + (−6). Check each verdict against the true sum.

### Problem 08-01.5 [B]

**Subtracting with an adder.** An 8-bit adder computes $A - B$ as $A + \bar B + 1$. For $A$ = 35₁₆ and $B$ = 5A₁₆: (a) find the 8-bit result and the carry out; (b) interpret the result as signed; (c) for unsigned numbers, a carry out of 0 means a borrow. What does it say here, and is that right?

### Problem 08-01.6 [B]

**A Q4.12 datapath.** A signed 16-bit format has 4 integer bits (including the sign) and 12 fractional bits. (a) Find its range and resolution. (b) Store π (use 3.14159), rounding to nearest; give the stored integer, the value it represents and the error. (c) Multiply 1.5 by 2.25 in Q4.12: what format and raw value does the 32-bit product have, and what Q4.12 integer results after rounding back? (d) What happens to 3.5 × 3.5, and what should a signal-processing datapath output?

### Problem 08-01.7 [B]

**Sizing an FIR filter's accumulator.** A 64-tap filter multiplies 16-bit samples by 16-bit coefficients, both in Q1.15, and sums the 64 products. (a) What width and Q format does each product need, and why does one extra bit appear? (b) What accumulator width is overflow-free for every input? (c) Name one property of a real filter's coefficients that would justify fewer guard bits.

### Problem 08-01.8 [B]

**FP16 by hand.** (a) Encode 1.0, −2.5 and 65 504 in IEEE binary16 and give each as four hex digits. (b) Decode C500₁₆. (c) What is the spacing between FP16 numbers just above 2048, and what happens when 2049 is converted to FP16?

### Problem 08-01.9 [B]

**Narrowing π.** The FP32 pattern for π is 40490FDB₁₆. (a) Round it to bfloat16 by rounding away the low 16 bits to nearest; give the bfloat16 pattern, its value and its relative error. (b) What is the nearest E4M3 value to π, and its relative error? (c) Compare each error with the format's bound $2^{-(m+1)}$.

### Problem 08-01.10 [A]

**Gray code.** (a) List the 4-bit reflected Gray code for 0 to 7. (b) Convert the Gray code word 1101 to binary. (c) A 4-bit binary up-counter drives an LED display through slow drivers, and the display sometimes flashes 15 when the count passes from 7 to 8. Explain, and say what a Gray counter would change.

### Problem 08-01.11 [B]

**UTF-8.** (a) Encode Ω (U+03A9) in UTF-8. (b) Decode the bytes E6 97 A5. (c) How many bytes does the string "Ω=1€" occupy in UTF-8? (d) A receiver joins a UTF-8 stream mid-character. How does it find the start of the next character?

### Problem 08-01.12 [B]

**Hamming(7,4) decoding.** (a) Encode the data $d_1d_2d_3d_4$ = 0110. (b) The word 1110110 is received. Compute the syndrome, correct the word and extract the data. (c) With an added overall parity bit, how does a SEC-DED decoder classify (i) syndrome 0 and overall parity correct, (ii) syndrome 5 and overall parity failing, (iii) syndrome 5 and overall parity correct?

### Problem 08-01.13 [C]

**ECC for a 32-bit memory.** (a) How many check bits does a SEC-DED code need for 32 data bits, and what is the code rate? (b) Bits fail independently with probability $10^{-9}$ per read. Estimate the probability that a 32-bit word without ECC is read wrong, and the probability that a SEC-DED-protected word has an uncorrectable (two or more bit) error. (c) By what factor does ECC reduce the rate of bad reads? (d) Real memories also suffer multi-bit upsets from a single particle strike. What does that do to the argument, and what do designers do about it?

### Problem 08-01.14 [C]

**A 4-bit CRC.** Use the generator $g(x) = x^4 + x + 1$ (10011). (a) Compute the CRC of the message 1010011101 and write the transmitted word. (b) Show that a burst error flipping four adjacent bits anywhere in the transmitted word is detected. (c) Construct an error pattern that this CRC cannot detect, and explain why every CRC has such patterns.

### Problem 08-01.15 [B]

**BCD arithmetic.** (a) Write 2026 in BCD and give the BCD word in hexadecimal. (b) Add the BCD numbers 0857 and 0479 digit by digit, showing each +6 correction. (c) How many bits does BCD need for numbers up to 9999, compared with binary?

---

## Objective coverage

| Learning objective (chapter 08-01) | Problems |
|---|---|
| 1. Base conversion and why fractions may not terminate | 1, 2 |
| 2. Two's complement, negation, sign extension, overflow | 3, 4, 5 |
| 3. Fixed point, product and accumulator widths, rounding and saturation | 6, 7 |
| 4. Floating-point fields, range and precision | 8, 9 |
| 5. BCD, Gray code, UTF-8 | 10, 11, 15 |
| 6. Parity, Hamming SEC-DED and CRC | 12, 13, 14 |
