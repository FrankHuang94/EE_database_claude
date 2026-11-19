# Solutions 08-07 · Registers, Counters and Shift Registers

Problems: [08-07 problems](../problems/08-07-problems.md) · Chapter: [08-07](../chapters/08-07-registers-counters-shift-registers.md). Every number below is recomputed by [verify_08_07.py](../verify/verify_08_07.py): registers and counters are simulated cycle by cycle from their next-state rules, LFSR cycles by stepping the register, and polynomial facts by arithmetic over GF(2).

---

## Solutions

### Solution 08-07.1

Each clock shifts the word left and puts the new bit in $Q_0$, so the first bit received ends in $Q_7$. After 8 clocks the register holds the bits in arrival order: 1011 0010 = **178**.

### Solution 08-07.2

(a) 5A₁₆ = 0101 1010. Least significant bit first: **0, 1, 0, 1, 1, 0, 1, 0**.

(b) **4** ones.

(c) Changes between consecutive bits: 0→1, 1→0, 0→1, (1→1 none), 1→0, 0→1, 1→0: **6** transitions. Line codes and scramblers exist to guarantee transitions like these, which the receiver needs to recover the clock.

### Solution 08-07.3

(a) $2^5 = 32 < 60 \le 64 = 2^6$: **6** flip-flops, **4** unused states.

(b) $2^4 = 16 < 24 \le 32$: **5** flip-flops, **8** unused states.

### Solution 08-07.4

(a) $2 - 5 = -3 \equiv 13 \pmod{16}$: **13** (1101).

(b) Bit $i$ toggles when every lower bit is 0: $T_i = \overline{Q_0}\,\overline{Q_1}\cdots\overline{Q_{i-1}}$ (a borrow reaches it).

(c) From 1000, every lower bit of bit 3 is 0, so all four bits toggle: **4**, giving 0111.

### Solution 08-07.5

(a) $T_7 = Q_0Q_1\cdots Q_6$ built as a chain: $T_2 = Q_0Q_1$ needs one AND, and each further term one more, so $T_7$ needs **6** ANDs, 150 ps. The path is $t_{pcq} + 150 + t_{XOR} + t_{\text{setup}} = 60 + 150 + 30 + 40$ = **280** ps: $f_{\max}$ = **3.57** GHz.

(b) Seven inputs need $\lceil \log_2 7 \rceil$ = **3** levels of two-input ANDs, 75 ps: $60 + 75 + 30 + 40$ = 205 ps, $f_{\max}$ = **4.88** GHz. The lookahead structure of fast adders ([08-09](../chapters/08-09-arithmetic-circuits.md)) does the same for every bit at once.

### Solution 08-07.6

(a) Each stage halves the frequency: $100\ \text{MHz}/2^{10}$ = **97.66** kHz.

(b) In the worst case the change ripples through all ten stages: $10 \times 0.5$ = **5** ns.

(c) A clock divider's output is used only as a slower clock (its edges are delayed, but consistently), so a fixed lag is harmless to logic clocked only by the divided clock, and nothing samples the intermediate stages. If that logic exchanges data with the source clock domain, the lag becomes clock skew between the two domains and must be included in their timing (08-10). A counter whose value is read needs all bits valid at the same time, and during the 5 ns ripple its outputs pass through transient states.

### Solution 08-07.7

(a) $2n = 10$ gives **5** flip-flops; $32 - 10$ = **22** unused states.

(b) Each output is 1 for 5 consecutive states and 0 for the other 5: a **50**% duty cycle at one tenth of the clock frequency, a clean divide-by-10.

(c) One two-input AND per state: **10** gates.

### Solution 08-07.8

(a) 1100 → 0110 → 0011 → 1001 → 1100: a cycle of 4 states with two 1s circulating. It never reaches the one-hot cycle.

(b) Grouping the 16 states by rotation: {0000}, {1111}, {0101, 1010}, the four one-hot states, the four states with three 1s, and the four with two adjacent 1s: **6** cycles. Only one is the intended sequence.

(c) Reset to a one-hot state at power-up, and add self-correcting feedback: for example, shift in a 1 only when all the other bits are 0 ($Q_{\text{in}} = \overline{Q_3}\,\overline{Q_2}\,\overline{Q_1}$ for a 4-bit ring), so any extra 1s are shifted out and the counter falls into the one-hot cycle within a few clocks.

### Solution 08-07.9

(a) $x^3 + x^2 + 1$ means $Q_1^{\text{next}} = Q_3 \oplus Q_2$. Stepping from $Q_1Q_2Q_3$ = 100 visits all 7 nonzero states: period **7**.

(b) **4** ones in one period ($2^{3-1}$).

(c) Yes: $x^3 + x + 1$ is the reciprocal polynomial of $x^3 + x^2 + 1$ (the taps mirrored), and also primitive; its period is 7 too. These are the only two irreducible cubics over GF(2), and both are primitive: an irreducible polynomial's period divides $2^3 - 1 = 7$, which is prime, so it must be 7.

### Solution 08-07.10

(a) $x^5 + x^3 + 1$ is primitive: period **31**.

(b) $x^5 + x^4 + 1$ splits the 31 nonzero states into cycles of **3**, **7** and **21**.

(c) $x^5 + x^4 + 1 = (x^2 + x + 1)(x^3 + x + 1)$: check by multiplying out, the $x^3$, $x^2$ and $x$ terms each appear twice and cancel. The factors have orders 3 and 7, and states that involve both have period $\operatorname{lcm}(3, 7) = 21$: $3 + 7 + 21 = 31$ ✓.

### Solution 08-07.11

(a) **16** ones and **15** zeros.

(b) **16** runs in total ($2^{n-1}$), of which **8** have length 1 (half), 4 have length 2, 2 length 3, and then one run of 4 zeros and one of 5 ones.

(c) **5** ones (the all-ones state appears once).

(d) **15** agreements and 16 disagreements, for every nonzero shift: $(N - 1)/2$ out of $N = 31$. In ±1 form the autocorrelation is $(15 - 16)/31 = -1/31$.

### Solution 08-07.12

(a) $25.78125 \times 10^9 \times 600$ = **1.547 × 10¹³** bits.

(b) $3/N$ = **1.94 × 10⁻¹³**: the test supports BER < $1.94 \times 10^{-13}$ at 95% confidence, not "zero errors".

(c) $3/10^{-15} = 3 \times 10^{15}$ bits, which at 25.78125 Gb/s takes about **32.3** hours.

### Solution 08-07.13

(a) 4 message bits plus 3 appended zeros: **7** clock cycles.

(b) The register follows the long division of 08-01: whenever the bit leaving the top of the 3-bit register is 1, the generator's lower bits (011, for $x^3 + x + 1$ without its top term) are XORed in. Clocking in 1, 1, 0, 1, 0, 0, 0 leaves 001, remainder **1**, matching Example 08-01.7. The CRC hardware of every Ethernet port is this circuit with 32 bits.

### Solution 08-07.14

(a) Bit $i$ toggles $2^{16-i}$ times per cycle of $2^{16}$ counts: $(2^{17} - 2)/2^{16}$ = **1.99997** toggles per count.

(b) **1**, by construction.

(c) $P = (\text{toggles per count}) \times E \times f$: binary $1.99997 \times 5\ \text{fJ} \times 100\ \text{MHz}$ = **1.000** µW; Gray **0.500** µW. Small numbers, but in an always-on timer they are a measurable share of a sleeping chip's budget, and the clock power of 16 flip-flops comes on top of both.

### Solution 08-07.15

(a) $36 + 24$ = **60** transistors per bit, **1920** in total.

(b) $36/60$ = **60**%: in this implementation the flexibility costs more than the storage. Real libraries use transmission-gate multiplexers or scan-style multiplexed flip-flops to cut this cost.

### Solution 08-07.16

A reference solution is in [hdl/p08-07-16](hdl/p08-07-16/): `updown.v` and `updown_tb.v`, run by `tools/run_hdl.py`.

(a) From 0 the 4-bit counter counts 1, 2, …, 15 and wraps to 0 at the **16**th count.

(b) $0 - 1$ wraps to $2^7 - 1$ = **127**.

(c) The design is one clocked block with `if (rst) … else if (load) … else if (en) …`, which encodes the priority directly. The testbench's model applies the same rules in the same order; it also checks that the 4-bit counter actually wrapped at least once, so the test cannot pass on a counter that never reaches its edge cases. With load and enable swapped, cycles that assert both are counted instead of loaded, and the testbench reports well over a thousand mismatches.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-07.1a | received word | 178 | — |
| 08-07.2a | ones in the stream | 4 | — |
| 08-07.2b | transitions | 6 | — |
| 08-07.3a | flip-flops, modulo 60 | 6 | — |
| 08-07.3b | unused states, modulo 60 | 4 | — |
| 08-07.3c | flip-flops, modulo 24 | 5 | — |
| 08-07.3d | unused states, modulo 24 | 8 | — |
| 08-07.4a | down counter after 5 edges | 13 | — |
| 08-07.4b | bits toggling from 1000 | 4 | — |
| 08-07.5a | ANDs in the chain to $T_7$ | 6 | — |
| 08-07.5b | minimum period, chain | 280 | ps |
| 08-07.5c | maximum frequency, chain | 3.57 | GHz |
| 08-07.5d | levels in the tree | 3 | — |
| 08-07.5e | minimum period, tree | 205 | ps |
| 08-07.5f | maximum frequency, tree | 4.88 | GHz |
| 08-07.6a | output frequency | 97.66 | kHz |
| 08-07.6b | worst-case ripple delay | 5 | ns |
| 08-07.7a | flip-flops for 10 states | 5 | — |
| 08-07.7b | unused states | 22 | — |
| 08-07.7c | duty cycle | 50 | % |
| 08-07.7d | decoding AND gates | 10 | — |
| 08-07.8a | states in the trapped cycle | 4 | — |
| 08-07.8b | rotation cycles of 4 bits | 6 | — |
| 08-07.9a | period of $x^3 + x^2 + 1$ | 7 | — |
| 08-07.9b | ones per period | 4 | — |
| 08-07.9c | period of $x^3 + x + 1$ | 7 | — |
| 08-07.10a | period of $x^5 + x^3 + 1$ | 31 | — |
| 08-07.10b | shortest cycle of $x^5 + x^4 + 1$ | 3 | — |
| 08-07.10c | middle cycle | 7 | — |
| 08-07.10d | longest cycle | 21 | — |
| 08-07.11a | ones per period | 16 | — |
| 08-07.11b | zeros per period | 15 | — |
| 08-07.11c | runs per period | 16 | — |
| 08-07.11d | runs of length 1 | 8 | — |
| 08-07.11e | longest run of ones | 5 | — |
| 08-07.11f | agreements with a shifted copy | 15 | — |
| 08-07.12a | bits checked | 1.547e13 | — |
| 08-07.12b | 95% BER bound | 1.94e-13 | — |
| 08-07.12c | time for a $10^{-15}$ bound | 32.3 | h |
| 08-07.13a | clock cycles | 7 | — |
| 08-07.13b | remainder | 1 | — |
| 08-07.14a | binary toggles per count | 1.99997 | — |
| 08-07.14b | binary counter power | 1.000 | µW |
| 08-07.14c | Gray counter power | 0.500 | µW |
| 08-07.15a | transistors per bit | 60 | — |
| 08-07.15b | transistors in total | 1920 | — |
| 08-07.15c | multiplexer share | 60 | % |
| 08-07.16a | up-counts to wrap, 4 bits | 16 | — |
| 08-07.16b | 0 - 1 at 7 bits | 127 | — |
