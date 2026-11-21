# Problems 17-08 · Channel Coding

Chapter: [17-08](../chapters/17-08-channel-coding.md) · Worked solutions: [17-08 solutions](../solutions/17-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All arithmetic on bits is in GF(2). BPSK maps bit $b$ to $1 - 2b$; $E_b/N_0$ is per information bit and $E_c = RE_b$ per coded bit. The (7,4) code is the systematic code of Example 17-08.1 ($p_1 = d_1 \oplus d_2 \oplus d_4$, $p_2 = d_1 \oplus d_3 \oplus d_4$, $p_3 = d_2 \oplus d_3 \oplus d_4$). The (7,5) code is the rate-1/2, $K$ = 3 convolutional code of §3.7, started in state 00 and terminated with two zeros. Problems marked *(lab)* can be checked with the lab's `coding.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-08.1 [A]

**Capability from distance.** A code has $d_{min}$ = 7. How many errors can it correct? How many can it detect if used only for detection? If it must correct 2 errors, how many errors can it detect at the same time?

### Problem 17-08.2 [A]

**Perfect codes.** Show that the (15,11) Hamming code and the (23,12) Golay code ($t$ = 3) meet the Hamming bound with equality: compute the number of words in one decoding sphere for each and compare with $2^{n-k}$.

### Problem 17-08.3 [A]

**A weak CRC.** NR's CRC6 is $g(x) = x^6 + x^5 + 1$. Does it detect every odd-weight error pattern? Give an undetected error pattern of odd weight. What fraction of 7-bit bursts, and of longer bursts, does it miss? *(lab: test all bursts exhaustively.)*

### Problem 17-08.4 [B]

**Miscorrection.** The (7,4) codeword 1011 010 is received with its first two bits flipped. Compute the syndrome, apply single-error syndrome decoding, and count how many bits of the decoded word are wrong.

### Problem 17-08.5 [B]

**SEC-DED sizing.** How many check bits does a SEC-DED code need for 128 data bits, and what is its overhead? Repeat for 32 data bits.

### Problem 17-08.6 [B]

**Longer Hamming codes.** On a BSC with $p = 10^{-3}$, find the block error probability of the (15,11) and (7,4) Hamming codes with bounded-distance decoding, and the rate of the (15,11) code. Which protects better, and what does it cost?

### Problem 17-08.7 [B]

**Repetition does not pay.** For the (3,1) repetition code with BPSK, find the asymptotic coding gain with soft decisions and with hard (majority) decisions. Explain the soft result physically.

### Problem 17-08.8 [B]

**Encoding.** Encode 1101 with the (7,5) code (including the tail). What is the weight of the output?

### Problem 17-08.9 [B]

**Viterbi.** *(lab)* The codeword of Problem 17-08.8 is received with its 3rd and 10th bits flipped. Decode it with hard-decision Viterbi and give the final path metric.

### Problem 17-08.10 [B]

**Decoder throughput.** A $K$ = 7 Viterbi decoder must run at 1 Gb/s. How many add-compare-select operations per second does it need? By what factor does that grow for $K$ = 9? About how long a traceback window would you use for $K$ = 7?

### Problem 17-08.11 [B]

**Puncturing.** A rate-1/2 mother code is punctured to rates 2/3, 3/4 and 5/6. In each case, what fraction of the mother code's output bits is deleted?

### Problem 17-08.12 [C]

**KP4 against KR4.** For RS(544,514) and RS(528,514) with independent symbol errors of probability $q$, find the codeword failure probability at $q = 10^{-3}$ and $q = 3 \times 10^{-3}$. Explain the different slopes.

### Problem 17-08.13 [C]

**Polarization by hand.** *(lab)* For $N$ = 4 channels built from a BEC with ε = 0.3, compute the four synthesized erasure probabilities (index bits MSB first: 0 → $2z - z^2$, 1 → $z^2$), check that the capacity is conserved, choose the information set for a rate-1/2 code, and bound its block erasure probability under successive cancellation.

### Problem 17-08.14 [C]

**A coding-gain budget.** A free-space link needs $P_b = 10^{-6}$ with BPSK. Find the uncoded requirement, the $K$ = 7 soft-decision union-bound requirement, the gain, and the resulting range multiplier. Repeat for an LDPC code operating 1 dB above the rate-1/2 BPSK-input limit (0.19 dB).

### Problem 17-08.15 [C]

**Transfer function.** Derive $T(D, N)$ for the (7,5) code from its state equations, extract $A_d$ and $B_d$ for $d$ = 5 to 8, and evaluate the union bound on $P_b$ at $E_b/N_0$ = 6 dB.

### Problem 17-08.16 [B]

**Check-node messages.** A degree-3 check node receives LLRs $L_1 = 2$ and $L_2 = -1$ from two of its bits. Compute the exact message to the third bit, the min-sum approximation, and the normalized min-sum value with factor 0.75.

### Problem 17-08.17 [B]

**From H to G.** A shortened Hamming code has the parity-check matrix

$$
\mathbf{H} = \left[\begin{array}{ccc|ccc}1&1&0&1&0&0\\1&0&1&0&1&0\\0&1&1&0&0&1\end{array}\right] .
$$

(a) Write the systematic generator matrix $\mathbf{G}$ and check $\mathbf{G}\mathbf{H}^\mathsf{T} = \mathbf{0}$. (b) Find $n$, $k$, the number of codewords of weight 3 and $d_{min}$. (c) Build the syndrome table. Which syndrome has no single-error pattern, and what is the weight of its coset leader? (d) Encode the message 101, flip the second bit, and decode.

### Problem 17-08.18 [B]

**RS(255,223) and interleaving.** The classic RS(255,223) code over GF($2^8$) protects deep-space and storage links. (a) Find $d_{min}$, $t$ and the longest burst, in bits, that one codeword always corrects. (b) Four codewords are block-interleaved (depth $I$ = 4). What is the longest burst, in symbols and in bits, that is always corrected, and how many bytes must the receiver buffer before decoding?

### Problem 17-08.19 [B]

**A CRC by long division.** *(lab)* Compute the CRC6 ($g(x) = x^6 + x^5 + 1$) check bits of the 10-bit message 1011001110 by polynomial long division, write the transmitted 16-bit word, and confirm that the receiver's division leaves remainder zero. Check your answer with the lab's shift-register routine.

### Problem 17-08.20 [C]

**One min-sum iteration.** The (7,4) code of Example 17-08.1 has checks $c_1$ on bits 1, 2, 4, 5; $c_2$ on bits 1, 3, 4, 6; and $c_3$ on bits 2, 3, 4, 7. The channel LLRs (positive favours 0) are $(-2.5, 1.8, 0.4, -3.0, 2.2, -1.6, 1.2)$. (a) Make hard decisions and compute the syndrome. (b) Starting with each bit's message equal to its channel LLR, compute the (unscaled) min-sum message from each check to bit 3. (c) Compute every bit's LLR after one iteration (channel LLR plus all incoming check messages), the decisions, and the syndrome.

---

## Objective coverage

| Learning objective (chapter 17-08) | Problems |
|---|---|
| 1. Rate, distance, capability, Hamming bound | 1, 2, 5, 6 |
| 2. Linear codes, syndrome decoding | 4, 17 |
| 3. CRCs | 3, 19 |
| 4. Convolutional codes and Viterbi | 8, 9, 10, 11, 15 |
| 5. RS, LDPC and polar codes | 12, 13, 16, 18, 20 |
| 6. Coding gain and the gap to capacity | 7, 14, 15 |
