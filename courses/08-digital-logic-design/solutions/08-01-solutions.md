# Solutions 08-01 · Number Systems and Codes

Problems: [08-01 problems](../problems/08-01-problems.md) · Chapter: [08-01](../chapters/08-01-number-systems-and-codes.md). Every number below is recomputed by [verify_08_01.py](../verify/verify_08_01.py), by bit-level simulation, exact rational arithmetic, enumeration of every pattern of a format, or matrix arithmetic over GF(2). Bit patterns are keyed by their unsigned integer values.

---

## Solutions

### Solution 08-01.1

(a) 3F7₁₆ = 3 × 256 + 15 × 16 + 7 = **1015**. Each hex digit is four bits: 0011 1111 0111₂ = 11 1111 0111₂.

(b) Repeated division by 2 gives 245 = **1111 0101₂**. Grouping the bits in threes from the right, 11 110 101₂ = **365₈**; in fours, 1111 0101₂ = **F5₁₆**.

(c) 0.375: ×2 = 0.75 (0), ×2 = 1.5 (1), ×2 = 1.0 (1), and the fraction reaches 0, so 0.375 = **0.011₂** exactly (0.0110 0000 with 8 bits). 0.3: ×2 = 0.6 (0), 1.2 (1), 0.4 (0), 0.8 (0), 1.6 (1), 1.2 (1), 0.4 (0), 0.8 (0), giving 0.0100 1100…₂, and the remainder 0.8 never reaches 0. 0.375 = 3/8 has a power-of-two denominator; 0.3 = 3/10 has the factor 5, so its expansion repeats forever (the block 1001 recurs).

### Solution 08-01.2

(a) $\lceil\log_2 1000\rceil = $ **10** bits ($2^{10}$ = 1024 states).

(b) 3.3 V / 0.1 mV = 33 000 steps, so **33 001** levels including 0 V. Since $2^{15}$ = 32 768 is too few and $2^{16}$ = 65 536 is enough, it needs **16** bits.

### Solution 08-01.3

(a) −1 = **FF₁₆** (all ones). 77 = 0100 1101; inverting gives 1011 0010, and adding 1 gives 1011 0011 = **B3₁₆**. −128 = **80₁₆**.

(b) 80₁₆ = **−128** (only the sign bit, weight −128). C9₁₆ = 1100 1001 = −128 + 64 + 8 + 1 = **−55**.

(c) Inverting 1100 1001 gives 0011 0110, and adding 1 gives 0011 0111 = **37₁₆** = **55**, the negation of −55 ✓.

### Solution 08-01.4

In 4 bits the range is −8 to +7. Writing each operand in binary and adding:

| Sum | Patterns | 4-bit result | $c_3$ | $c_4$ | $V = c_4 \oplus c_3$ | True sum |
|---|---|---|---|---|---|---|
| (a) 5 + 4 | 0101 + 0100 = 1001 | **−7** | 1 | 0 | **1** | 9 (overflow ✓) |
| (b) −8 + (−1) | 1000 + 1111 = (1)0111 | **7** | 0 | 1 | **1** | −9 (overflow ✓) |
| (c) 7 + (−8) | 0111 + 1000 = 1111 | **−1** | 0 | 0 | **0** | −1 (correct ✓) |
| (d) −3 + (−6) | 1101 + 1010 = (1)0111 | **7** | 0 | 1 | **1** | −9 (overflow ✓) |

In (c) the operands have opposite signs, so overflow is impossible, as the sign rule says.

### Solution 08-01.5

(a) $\bar B$ = $\overline{0101\,1010}$ = 1010 0101. Then 0011 0101 + 1010 0101 + 1 = 1101 1011 = **DB₁₆**, with carry out **0**.

(b) As signed, DB₁₆ = −128 + 91 = **−37**, and indeed 35₁₆ − 5A₁₆ = 53 − 90 = −37 ✓.

(c) For unsigned operands, carry out 0 means a borrow occurred: $A < B$, which is right, since 53 < 90. (The carry out of $A + \bar B + 1$ is 1 exactly when $A \ge B$; some processors store the borrow as the inverted carry for this reason.)

### Solution 08-01.6

(a) Range: −8 to $8 - 2^{-12}$ = **7.999755859**. Resolution: $2^{-12}$ = **2.441 × 10⁻⁴**.

(b) 3.14159 × 4096 = 12 867.95, which rounds to **12 868**. That represents 12 868/4096 = **3.141601563**, an error of **1.156 × 10⁻⁵** (well within half an LSB).

(c) 1.5 is stored as 6144 and 2.25 as 9216. Their 32-bit product is 56 623 104 in **Q8.24** (8 integer bits, 24 fractional), which is 3.375. Rounding back to Q4.12 (add $2^{11}$, shift right by 12) gives **13 824** = 3.375 exactly.

(d) 3.5 × 3.5 = 12.25 exceeds the Q4.12 maximum of 7.9998. Simply keeping 16 bits would wrap to a negative number. A signal datapath should **saturate** to the largest value, 32 767 (7.9998), and flag the event.

### Solution 08-01.7

(a) A 16 × 16-bit product needs **32** bits, in Q2.30. The second integer bit is needed only for (−1) × (−1) = +1, which Q1.31 cannot represent: the most-negative-squared corner of §3.5.

(b) Summing 64 products adds $\log_2 64$ = 6 guard bits: **38** bits (Q8.30).

(c) If the coefficients' absolute values sum to at most 1 (as for a filter with gain no greater than 1 for any input), the sum of products can never exceed one input's full scale. Then no guard bits beyond the product's are needed, and many designs keep 32 bits plus a little margin. The worst-case 38-bit width covers arbitrary coefficients.

### Solution 08-01.8

(a) For binary16 the bias is 15, and a normal number is $(-1)^s \times 1.F \times 2^{E - 15}$:

- 1.0 = 1.0 × 2⁰: $s$ = 0, $E$ = 15 = 01111, $F$ = 0. The bits are 0 01111 0000000000 = **3C00₁₆**.
- −2.5 = −1.25 × 2¹: $s$ = 1, $E$ = 16 = 10000, $F$ = 0100000000. The bits are 1 10000 0100000000 = **C100₁₆**.
- 65 504 = (2 − 2⁻¹⁰) × 2¹⁵: $s$ = 0, $E$ = 30 = 11110, $F$ = all ones. The bits are 0 11110 1111111111 = **7BFF₁₆**, the largest finite FP16 value.

(b) C500₁₆ = 1 10001 0100000000: $s$ = 1, $E$ = 17, $F$ = 0.25, so the value is −1.25 × 2² = **−5**.

(c) 2048 = 2¹¹, and with 10 fraction bits the spacing in $[2^{11}, 2^{12})$ is $2^{11-10}$ = **2**. 2049 lies exactly halfway between 2048 and 2050. Round-to-nearest-even picks the neighbor with an even last fraction bit, **2048**. Above 2048, FP16 cannot represent every integer.

### Solution 08-01.9

(a) 40490FDB₁₆: the low 16 bits, 0FDB₁₆, are below half (8000₁₆), so rounding to nearest keeps the upper half: **4049₁₆**. That is $s$ = 0, $E$ = 128 (exponent 1), $F$ = 1001001₂ = 0.5703125, so the value is 1.5703125 × 2 = **3.140625**, a relative error of **−0.03080%**.

(b) In E4M3, π lies in $[2, 4)$ where the spacing is $2^{1-3}$ = 0.25, so the candidates are 3.0 and 3.25. π/0.25 = 12.57, which rounds to 13: **3.25**, a relative error of **+3.451%**.

(c) The bounds are $2^{-8}$ = 0.391% for bfloat16 and $2^{-4}$ = 6.25% for E4M3. Both errors are within them.

### Solution 08-01.10

(a) 0000, 0001, 0011, 0010, 0110, 0111, 0101, 0100, from $G = B \oplus (B \gg 1)$ or by reflecting the 3-bit code.

(b) $b_3 = g_3 = 1$; $b_2 = g_2 \oplus b_3 = 1 \oplus 1 = 0$; $b_1 = g_1 \oplus b_2 = 0$; $b_0 = g_0 \oplus b_1 = 1$. So 1101 in Gray code is **1001₂** = **9**. Check: $1001 \oplus 0100$ = 1101 ✓.

(c) From 7 to 8 (0111 → 1000) all four bits change. If the drivers switch at slightly different speeds, intermediate patterns such as 1111 (15) appear briefly. In Gray code, 7 = 0100 and 8 = 1100 differ in one bit, so only 7 or 8 can ever be shown. (A counter driving a display should usually also be registered at the display, which removes the glitch whatever the code.)

### Solution 08-01.11

(a) U+03A9 = 011 1010 1001₂ needs 11 bits, so it takes two bytes: 110xxxxx 10xxxxxx with the bits 01110 | 101001. That gives 1100 1110 1010 1001 = **CE A9**.

(b) E6 97 A5 = 1110 0110, 10 010111, 10 100101: a three-byte sequence with payload 0110 010111 100101 = 0110 0101 1110 0101 = **U+65E5**, the character 日 ("sun", "day").

(c) Ω takes 2 bytes, "=" and "1" one each, and € three (E2 82 AC): **7** bytes for 4 characters.

(d) Every continuation byte starts with 10, and every first byte does not. The receiver skips bytes of the form 10xxxxxx until it reaches one that is not; that is the start of a character.

### Solution 08-01.12

(a) For $d$ = 0110: $p_1 = d_1 \oplus d_2 \oplus d_4 = 0 \oplus 1 \oplus 0 = 1$; $p_2 = d_1 \oplus d_3 \oplus d_4 = 1$; $p_4 = d_2 \oplus d_3 \oplus d_4 = 0$. The code word ($p_1p_2d_1p_4d_2d_3d_4$) is **1100110**.

(b) In 1110110, positions 1, 3, 5, 7 hold 1, 1, 1, 0, odd, so $s_1 = 1$; positions 2, 3, 6, 7 hold 1, 1, 1, 0, odd, so $s_2 = 1$; positions 4, 5, 6, 7 hold 0, 1, 1, 0, even, so $s_4 = 0$. The syndrome is 011 = **3**: data bit $d_1$ flipped. Correcting it gives 1100110, with data **0110** ✓.

(c) The classification:

- (i) No error.
- (ii) A single error at position 5, which is corrected.
- (iii) A double error, which is detected but not corrected.

### Solution 08-01.13

(a) The smallest $r$ with $2^r \ge 32 + r + 1$ is 6 ($2^6$ = 64 ≥ 39), and DED adds 1: **7** check bits, a (39,32) code with rate 32/39 = **0.8205**.

(b) Without ECC, a read fails if any of 32 bits flips: $1 - (1 - 10^{-9})^{32} \approx$ **3.2 × 10⁻⁸**. With SEC-DED, a word fails only if two or more of its 39 bits flip, and that is dominated by $\binom{39}{2}p^2 = 741 \times 10^{-18} = $ **7.41 × 10⁻¹⁶**.

(c) The ratio is about **4.32 × 10⁷**: ECC turns roughly one bad read in 30 million into one in about 10¹⁵.

(d) The calculation assumes independent bit errors. A single particle can upset several adjacent cells, which defeats a SEC code if they belong to the same word. Designers **interleave** physically adjacent cells into different code words, so that a multi-cell upset becomes several single errors in different words, and use stronger symbol-based codes (chipkill-style ECC) that correct a whole failed chip. In addition, they **scrub** memory periodically so that single errors are corrected before a second one accumulates in the same word.

### Solution 08-01.14

(a) Append four zeros to 1010011101 and divide by 10011 with XOR (§3.8). The remainder is **0010**, so the transmitted word is 1010011101 0010.

(b) A burst that flips four adjacent bits starting at position $k$ is the error polynomial $E(x) = (x^3 + x^2 + x + 1)\,x^k$. Since $g(x)$ has a nonzero constant term, it shares no factor with $x^k$. And $x^3 + x^2 + x + 1$ has lower degree than $g(x)$, so $g(x)$ cannot divide it. Hence $g(x)$ never divides $E(x)$, and every such burst leaves a nonzero remainder. The same argument covers every burst of length 4 or less, whatever its interior bits.

(c) Any error pattern that is itself a multiple of $g(x)$ passes undetected: for example $E(x) = g(x)\,x^3$, which flips bits 7, 4 and 3 of the 14-bit word (counting from the right, from 0). The received word is then still a multiple of $g(x)$, so its remainder is **0**. Every CRC has such patterns, because $r$ check bits can distinguish at most $2^r$ remainders. A random error pattern therefore escapes with probability about $2^{-r}$, here 1/16, which is why links use 32-bit CRCs.

### Solution 08-01.15

(a) 2026 → digits 2, 0, 2, 6 → 0010 0000 0010 0110, which in hexadecimal is **2026₁₆**. The hex digits of a BCD word read as the decimal number, a convenient property for debugging.

(b) Working from the right:

- 7 + 9 = 16 > 9: add 6, giving 22 = 1 0110, so the digit is 6 with a carry.
- 5 + 7 + 1 = 13 > 9: add 6, giving 19 = 1 0011, so the digit is 3 with a carry.
- 8 + 4 + 1 = 13: the digit is 3 with a carry.
- 0 + 0 + 1 = 1.

The result is **1336** ✓.

(c) BCD needs 4 bits per digit: **16** bits for 9999, against $\lceil\log_2 10\,000\rceil$ = **14** bits in binary. BCD is 14% larger here, the price of easy decimal conversion.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-01.1a | 3F7₁₆ in decimal | 1015 | — |
| 08-01.1b | 245 in octal, 365₈, as the integer of its digits | 365 | — |
| 08-01.1c | 245 in hexadecimal, F5₁₆, as an integer | 245 | — |
| 08-01.1d | 0.375 in binary, first 8 fractional bits as an integer (0110 0000₂) | 96 | — |
| 08-01.1e | 0.3 in binary, first 8 fractional bits as an integer (0100 1100₂) | 76 | — |
| 08-01.2a | bits for 1000 states | 10 | bits |
| 08-01.2b | levels from 0 to 3.3 V at 0.1 mV | 33001 | — |
| 08-01.2c | bits for those levels | 16 | bits |
| 08-01.3a | −77 as an unsigned 8-bit pattern (B3₁₆) | 179 | — |
| 08-01.3b | value of C9₁₆ | −55 | — |
| 08-01.3c | negation of C9₁₆ | 55 | — |
| 08-01.4a | 5 + 4 in 4 bits | −7 | — |
| 08-01.4b | −8 + (−1) in 4 bits | 7 | — |
| 08-01.4c | 7 + (−8) in 4 bits | −1 | — |
| 08-01.4d | −3 + (−6) in 4 bits | 7 | — |
| 08-01.5a | 35₁₆ − 5A₁₆ as an unsigned pattern (DB₁₆) | 219 | — |
| 08-01.5b | carry out | 0 | — |
| 08-01.5c | signed result | −37 | — |
| 08-01.6a | Q4.12 largest value | 7.999755859 | — |
| 08-01.6b | Q4.12 resolution | 2.441e-4 | — |
| 08-01.6c | π in Q4.12 (integer) | 12868 | — |
| 08-01.6d | value represented | 3.141601563 | — |
| 08-01.6e | error | 1.156e-5 | — |
| 08-01.6f | raw Q8.24 product of 1.5 and 2.25 | 56623104 | — |
| 08-01.6g | Q4.12 result | 13824 | — |
| 08-01.6h | saturated Q4.12 output | 32767 | — |
| 08-01.7a | product width | 32 | bits |
| 08-01.7b | accumulator width | 38 | bits |
| 08-01.8a | FP16 pattern of 1.0 (3C00₁₆) | 15360 | — |
| 08-01.8b | FP16 pattern of −2.5 (C100₁₆) | 49408 | — |
| 08-01.8c | FP16 pattern of 65 504 (7BFF₁₆) | 31743 | — |
| 08-01.8d | value of C500₁₆ | −5 | — |
| 08-01.8e | FP16 spacing above 2048 | 2 | — |
| 08-01.8f | 2049 converted to FP16 | 2048 | — |
| 08-01.9a | bfloat16 pattern of π (4049₁₆) | 16457 | — |
| 08-01.9b | its value | 3.140625 | — |
| 08-01.9c | its relative error | −0.03080 | % |
| 08-01.9d | nearest E4M3 value to π | 3.25 | — |
| 08-01.9e | its relative error | 3.451 | % |
| 08-01.10a | Gray 1101 in binary (1001₂) | 9 | — |
| 08-01.11a | UTF-8 of Ω, CE A9 as a 16-bit integer | 52905 | — |
| 08-01.11b | code point decoded from E6 97 A5 (U+65E5) | 26085 | — |
| 08-01.11c | bytes in "Ω=1€" | 7 | — |
| 08-01.12a | code word for 0110 (1100110₂) | 102 | — |
| 08-01.12b | syndrome of 1110110 | 3 | — |
| 08-01.13a | SEC-DED check bits for 32 data bits | 7 | — |
| 08-01.13b | code rate | 0.8205 | — |
| 08-01.13c | bad-read probability without ECC | 3.2e-8 | — |
| 08-01.13d | uncorrectable-error probability with SEC-DED | 7.41e-16 | — |
| 08-01.13e | improvement factor | 4.32e7 | — |
| 08-01.14a | CRC of 1010011101 (0010₂) | 2 | — |
| 08-01.14b | remainder for the error g(x)·x³ | 0 | — |
| 08-01.15a | 2026 in BCD, 2026₁₆, as an integer | 8230 | — |
| 08-01.15b | BCD sum 0857 + 0479 | 1336 | — |
| 08-01.15c | BCD bits for 9999 | 16 | bits |
| 08-01.15d | binary bits for 9999 | 14 | bits |
