# Solutions 17-08 · Channel Coding

Problems: [17-08 problems](../problems/17-08-problems.md) · Chapter: [17-08](../chapters/17-08-channel-coding.md). Every number below is recomputed by [verify_17_08.py](../verify/verify_17_08.py): code properties by enumeration and GF(2) algebra, CRC behaviour by exhaustive burst tests, error rates from binomial tails, distance spectra from the state diagram, and decoders by running them.

---

## Solutions

### Solution 17-08.1

$t = \lfloor(7 - 1)/2\rfloor$ = **3** errors corrected. Used only for detection, it catches up to $d_{min} - 1$ = **6**. Correcting $t'$ = 2 and detecting $s$ needs $t' + s + 1 \le 7$, so $s$ = **4**: patterns of 3 or 4 errors land outside every radius-2 sphere and are flagged rather than miscorrected.

### Solution 17-08.2

(15,11), $t$ = 1: a sphere holds $1 + 15$ = **16** words, and $2^{n-k} = 2^4 = 16$. (23,12), $t$ = 3: $1 + 23 + 253 + 1771$ = **2048** = $2^{11}$. In both cases $2^k \times$ (sphere size) $= 2^n$ exactly: the spheres tile the space and the codes are perfect.

### Solution 17-08.3

$g(1) = 1 + 1 + 1 = 1$ (three terms), so $x + 1$ does not divide $g$ and not every odd-weight pattern is caught. The simplest undetected one is $g(x)$ itself: the error pattern 1100001 (weight **3**) is a multiple of $g$ and leaves the remainder unchanged. Bursts: every burst of length ≤ 6 is detected. A 7-bit burst is $x^i b(x)$ with $b$ of degree 6 and $b(0) = 1$; of the $2^5 = 32$ such $b$, only $b = g$ is a multiple of $g$, so the miss fraction is $2^{-5}$ = **0.03125**. Longer bursts are missed with fraction $2^{-6}$ = **0.015625**.

### Solution 17-08.4

Received 0111 010. The errors are in positions 1 and 2, so $\mathbf{s}$ = column 1 + column 2 of $H$ = 110 + 101 = 011, which is column 3. The decoder flips bit 3, giving 0101 010, a valid codeword (check: $p_1 = 0 \oplus 1 \oplus 1 = 0$, $p_2 = 0 \oplus 0 \oplus 1 = 1$, $p_3 = 1 \oplus 0 \oplus 1 = 0$). It differs from the sent 1011 010 in positions 1, 2 and 3: **3** wrong bits, one more than the channel caused. This is why SEC-DED adds a parity bit: two errors leave the overall parity even while the syndrome is nonzero, and the decoder flags rather than "corrects".

### Solution 17-08.5

128 bits: the smallest $r$ with $2^r \ge 128 + r + 1$ is $r$ = 8 ($256 \ge 137$; $r$ = 7 gives $128 < 136$). Adding the overall parity bit: **9** check bits, a (137,128) code, overhead $9/128$ = **7.03** %. 32 bits: $r$ = 6 ($64 \ge 39$), plus parity: **7** check bits, (39,32), overhead $7/32$ = **21.9** %. Wider words amortize the check bits, which is why memory ECC works on wide words.

### Solution 17-08.6

Bounded-distance decoding fails with two or more errors.

- (15,11): $1 - (1 - p)^{15} - 15p(1 - p)^{14}$ = **1.04e-4** ($\approx \binom{15}{2}p^2 = 105p^2$).
- (7,4): $1 - (1 - p)^7 - 7p(1 - p)^6$ = **2.09e-5** ($\approx 21p^2$).

The (15,11) code has rate $11/15$ = **0.733** against 0.571: it spends less redundancy but fails five times as often per block (about 1.8 times as often per information bit), because a single error-correcting capability is spread over twice as many bits.

### Solution 17-08.7

$R = 1/3$, $d_{min}$ = 3, $t$ = 1. Soft: $10\log_{10}(\tfrac13 \times 3)$ = **0** dB. Hard: $10\log_{10}(\tfrac13 \times 2)$ = **−1.76** dB. With soft decisions the receiver simply adds the three samples, recovering exactly the energy $3E_c = E_b$ of one uncoded bit: repetition is a matched filter, not a code gain. With hard decisions it first throws away information on each third, then votes, and loses.

### Solution 17-08.8

From state 00 with inputs 1, 1, 0, 1, 0, 0 (outputs: $u_t \oplus u_{t-1} \oplus u_{t-2}$, then $u_t \oplus u_{t-2}$):

| Input | State before | Output | State after |
|---|---|---|---|
| 1 | 00 | 11 | 10 |
| 1 | 10 | 01 | 11 |
| 0 | 11 | 01 | 01 |
| 1 | 01 | 00 | 10 |
| 0 | 10 | 10 | 01 |
| 0 | 01 | 11 | 00 |

Output 11 01 01 00 10 11, weight **7**.

### Solution 17-08.9

Received 11 11 01 00 11 11 (bits 3 and 10 flipped). Running the add-compare-select steps (as in Example 17-08.4) and tracing back from state 00 gives inputs 1101 then 00, re-encoding to the transmitted word at Hamming distance **2** from the received one: both errors corrected. They fall in branches 2 and 5, far enough apart that no competing path within distance 2 exists ($d_{free}$ = 5).

### Solution 17-08.10

64 states, one ACS per state per bit: $64 \times 10^9$ = **6.4e10** ACS/s, usually spread over parallel ACS units. $K$ = 9 has 256 states: **4** times as many. A traceback depth of about five constraint lengths, **35** bits, makes the survivors merge with high probability.

### Solution 17-08.11

Rate 2/3: two input bits produce four mother bits, of which three are sent: delete $1/4$ = **0.25**. Rate 3/4: three input bits give six, four are sent: delete $2/6$ = **0.333**. Rate 5/6: five give ten, six are sent: delete $4/10$ = **0.4**. One Viterbi decoder serves all rates; deleted positions get zero LLR (an erasure).

### Solution 17-08.12

With $X \sim$ Binomial($n$, $q$), failure is $P(X > t)$:

| | $q = 10^{-3}$ | $q = 3 \times 10^{-3}$ |
|---|---|---|
| RS(544,514), $t$ = 15 | **1.37e-18** | **2.19e-11** |
| RS(528,514), $t$ = 7 | **8.96e-8** | **2.36e-4** |

The failure probability is dominated by the first uncorrectable term, $\binom{n}{t+1}q^{t+1}(1 - q)^{n-t-1}$, which grows as $q^{16}$ for KP4 and $q^{8}$ for KR4. Tripling $q$ would multiply them by $3^{16} \approx 4.3 \times 10^7$ and $3^8 = 6561$ if the $(1 - q)^{n-t-1}$ factor stayed fixed; it falls by about a factor of 3 here, so the actual ratios are about $1.6 \times 10^7$ and 2600. The steeper slope is what more parity buys.

### Solution 17-08.13

Start with $z$ = 0.3. First split: 0 → $2(0.3) - 0.09 = 0.51$; 1 → 0.09. Second split:

- index 0 (00): $2(0.51) - 0.2601$ = **0.7599**;
- index 1 (01): $0.51^2$ = **0.2601**;
- index 2 (10): $2(0.09) - 0.0081$ = **0.1719**;
- index 3 (11): $0.09^2$ = **0.0081**.

Sum $= 1.2 = 4 \times 0.3$, so the total capacity $4 - 1.2 = 2.8 = 4 \times 0.7$ is conserved. Rate 1/2: put information on indices 2 and 3 and freeze 0 and 1. Successive cancellation fails only if a used channel is erased, so the block erasure probability is at most $0.1719 + 0.0081$ = **0.18** (union bound).

### Solution 17-08.14

Uncoded BPSK: $Q(\sqrt{2E_b/N_0}) = 10^{-6}$ needs 10.53 dB. $K$ = 7 union bound $\sum B_dQ(\sqrt{dE_b/N_0}) = 10^{-6}$: **4.79** dB, a gain of **5.74** dB. In free space received power falls as $1/r^2$, so range scales by $10^{G/20}$ = **1.94**. LDPC at $0.19 + 1 = 1.19$ dB: gain **9.34** dB, range × **2.93**. (A practical coded system also loses the rate: at rate 1/2 the coded symbols occupy twice the bandwidth.)

### Solution 17-08.15

With the branch labels of §3.7 (state 10 = b, 01 = c, 11 = d):

$$
X_b = D^2N + NX_c,\qquad X_c = DX_b + DX_d,\qquad X_d = DNX_b + DNX_d,\qquad T = D^2X_c .
$$

Then $X_d = \frac{DN}{1 - DN}X_b$, $X_c = \frac{D}{1 - DN}X_b$, and $X_b\big(1 - \frac{DN}{1 - DN}\big) = D^2N$, so $X_b = \frac{D^2N(1 - DN)}{1 - 2DN}$ and

$$
T(D, N) = \frac{D^5N}{1 - 2DN} = D^5N + 2D^6N^2 + 4D^7N^3 + 8D^8N^4 + \cdots
$$

$A_5, A_6, A_7, A_8$ = 1, 2, 4, **8**; $\partial T/\partial N|_{N=1} = D^5/(1 - 2D)^2$ gives $B_5, B_6, B_7, B_8$ = 1, **4**, 12, **32**. At 6 dB ($E_b/N_0 = 3.981$, $2R = 1$): $P_b \le \sum_{d \ge 5}(d - 4)2^{d-5}Q(\sqrt{3.981d})$ = **7.28e-6**.

### Solution 17-08.16

Exact: $2\tanh^{-1}\big(\tanh(1)\tanh(-0.5)\big) = 2\tanh^{-1}(0.7616 \times -0.4621) = 2\tanh^{-1}(-0.3519)$ = **−0.735**. Min-sum: sign $(+)(-) = -$, magnitude $\min(2, 1)$: **−1**. Normalized: $0.75 \times -1$ = **−0.75**. Min-sum overstates the confidence because the less reliable input dominates a parity check but the other input still adds doubt; the scale factor corrects much of the excess.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-08.1a | correctable errors | 3 | — |
| 17-08.1b | detectable errors | 6 | — |
| 17-08.1c | detectable while correcting 2 | 4 | — |
| 17-08.2a | (15,11) sphere size | 16 | words |
| 17-08.2b | Golay sphere size | 2048 | words |
| 17-08.3a | weight of an undetected odd pattern | 3 | — |
| 17-08.3b | 7-bit burst miss fraction | 0.03125 | — |
| 17-08.3c | longer burst miss fraction | 0.015625 | — |
| 17-08.4a | wrong bits after decoding | 3 | — |
| 17-08.5a | check bits for 128 data bits | 9 | — |
| 17-08.5b | overhead for 128 data bits | 7.03 | % |
| 17-08.5c | check bits for 32 data bits | 7 | — |
| 17-08.5d | overhead for 32 data bits | 21.9 | % |
| 17-08.6a | (15,11) block error | 1.04e-4 | — |
| 17-08.6b | (7,4) block error | 2.09e-5 | — |
| 17-08.6c | (15,11) rate | 0.733 | — |
| 17-08.7a | repetition soft gain | 0 | dB |
| 17-08.7b | repetition hard gain | −1.76 | dB |
| 17-08.8a | output weight | 7 | — |
| 17-08.9a | path metric | 2 | — |
| 17-08.10a | ACS rate | 6.4e10 | 1/s |
| 17-08.10b | growth for K = 9 | 4 | — |
| 17-08.10c | traceback depth | 35 | bits |
| 17-08.11a | deleted fraction, rate 2/3 | 0.25 | — |
| 17-08.11b | deleted fraction, rate 3/4 | 0.333 | — |
| 17-08.11c | deleted fraction, rate 5/6 | 0.4 | — |
| 17-08.12a | KP4 at q = 1e-3 | 1.37e-18 | — |
| 17-08.12b | KP4 at q = 3e-3 | 2.19e-11 | — |
| 17-08.12c | KR4 at q = 1e-3 | 8.96e-8 | — |
| 17-08.12d | KR4 at q = 3e-3 | 2.36e-4 | — |
| 17-08.13a | erasure, index 0 | 0.7599 | — |
| 17-08.13b | erasure, index 1 | 0.2601 | — |
| 17-08.13c | erasure, index 2 | 0.1719 | — |
| 17-08.13d | erasure, index 3 | 0.0081 | — |
| 17-08.13e | block erasure bound | 0.18 | — |
| 17-08.14a | K = 7 requirement at 1e-6 | 4.79 | dB |
| 17-08.14b | K = 7 gain | 5.74 | dB |
| 17-08.14c | K = 7 range multiplier | 1.94 | — |
| 17-08.14d | LDPC gain | 9.34 | dB |
| 17-08.14e | LDPC range multiplier | 2.93 | — |
| 17-08.15a | A_8 | 8 | — |
| 17-08.15b | B_6 | 4 | — |
| 17-08.15c | B_8 | 32 | — |
| 17-08.15d | union bound at 6 dB | 7.28e-6 | — |
| 17-08.16a | exact check message | −0.735 | — |
| 17-08.16b | min-sum message | −1 | — |
| 17-08.16c | normalized min-sum message | −0.75 | — |
