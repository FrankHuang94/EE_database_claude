# Solutions 08-05 · Introduction to Verilog/SystemVerilog and Testbenches

Problems: [08-05 problems](../problems/08-05-problems.md) · Chapter: [08-05](../chapters/08-05-verilog-and-testbenches.md). Every number below is recomputed by [verify_08_05.py](../verify/verify_08_05.py), which models Verilog's width, signedness, four-valued and scheduling rules in Python. The worked examples of the chapter are also checked in Icarus Verilog by the lab's `semantics_tb.v`.

---

## Solutions

### Solution 08-05.1

$a = 200$ and $b = 100$.

(a) $300$ does not fit in 8 bits: $300 - 256$ = **44**.

(b) A 9-bit destination widens the addition: **300**.

(c) $200 - 100$ = **100**.

(d) $100 - 200 = -100$, stored modulo 256: $256 - 100$ = **156**, which as a signed 8-bit number is **−100**.

### Solution 08-05.2

(a) A₁₆ = **10**. (b) 101011₂ = 32 + 8 + 2 + 1 = **43** (the underscore is only for readability). (c) 0F0₁₆ = 15 × 16 = **240**.

(d) An unsized literal is **32** bits wide. A based literal such as `'hFF` is unsigned unless written with `s` (`'shFF`); only unsized *decimal* literals such as `255` are signed.

### Solution 08-05.3

`a` = 1010 0110.

(a) AND-reduction **0** (some bit is 0); OR-reduction **1**; XOR-reduction **0** (four 1s, even parity).

(b) `a[3:0]` = 0110, replicated twice: 0110 0110 = **102**.

(c) `a[7:4]` = 1010 = **10**.

(d) Shifting left by 3 and keeping 8 bits: 0011 0000 = **48** (the top three bits fall off).

### Solution 08-05.4

(a) 1010 as a signed 4-bit number is $-8 + 2$ = **−6**.

(b) `p >>> 2` is an arithmetic shift of a signed operand: 1110 = **−2** ($-6/4 = -1.5$, rounded toward $-\infty$). `p >> 2` is logical: 0010 = **2**.

(c) $-6 + 7 = 1$: **1** (1010 + 0111 = 1 0001; the carry out is discarded).

(d) Assigning a signed value to a wider signed variable sign-extends it: 1111 1010 = **250** as an unsigned number (−6 as signed).

(e) `p < 4'd0` mixes in an unsigned operand, so the comparison is unsigned: $10 < 0$ is false, **0**. `p < 0` compares two signed values: $-6 < 0$, **1**.

### Solution 08-05.5

(a) `1'bx | 1'b0` = **x** (the unknown decides); `1'bz & 1'b0` = **0** (0 dominates AND, and Z behaves as X in logic); `~1'bz` = **x**.

(b) `==` meets an X bit and returns **x**; `===` compares the literal four-valued patterns, which are identical: **1**.

(c) OR is definite when either input is 1 or both are 0: $4 + 4 - 1 = 7$ combinations with a 1, plus (0, 0): **8**. NAND is the complement of AND, which is definite in 8 combinations, so **8**. XNOR, like XOR, needs both inputs known: **4**.

### Solution 08-05.6

- Block 1 assigns `y1` on both branches: no latch.
- Block 2 has no branch for `sel` = 3: `y2` is a latch.
- Block 3 gives `y3` a default but assigns `y4` only when `en` = 1: `y4` is a latch.

**2** latched outputs. Fix block 2 with a `default:` and block 3 with a default for `y4`.

### Solution 08-05.7

(a) In reverse order every stage reads its neighbor *before* that neighbor is overwritten: `q4` gets the old `q3`, `q3` the old `q2`, and so on. It behaves as a true shift register: the 1 reaches `q4` after **4** edges.

(b) In forward order `q1 = d` happens first and every later stage copies the new value: **1** edge.

(c) The behavior depends on statement order, so a harmless-looking edit (reordering, or splitting the block in two, which also creates a race between blocks) silently breaks it. Non-blocking assignments give the right behavior in any order and state the intent.

### Solution 08-05.8

(a) Non-blocking: all right-hand sides are read first (2, 3, 1), then assigned: $a, b, c$ = **2, 3, 1**. Each edge rotates the values one place, so after three edges they are back to **1, 2, 3**.

(b) Blocking: `a = b` makes $a$ = 2; `b = c` makes $b$ = 3; `c = a` reads the *new* $a$: $c$ = 2. Result **2, 3, 2**; the 1 is lost.

### Solution 08-05.9

(a) The clock toggles every 5 ns, so its period is 10 ns: **100** MHz.

(b) `clk` rises at 5 ns, 15 ns, …, 995 ns: $(995 - 5)/10 + 1$ = **100** rising edges.

(c) $1000 \bmod 256$ = **232**: the counter wraps around three times (at 256, 512 and 768 edges).

### Solution 08-05.10

The block re-runs only when `a` or `b` changes.

| Step | $(a, b, c)$ | re-run? | simulated `y` | hardware `y` |
|---|---|---|---|---|
| $c \to 1$ | (0, 0, 1) | no | 0 | 1 |
| $a \to 1$ | (1, 0, 1) | yes | 1 | 1 |
| $c \to 0$ | (1, 0, 0) | no | 1 | 0 |
| $b \to 1$ | (1, 1, 0) | yes | 1 | 1 |

**2** mismatches, both on changes of the forgotten input `c`.

### Solution 08-05.11

(a) $2^{4 + 4 + 3} = 2^{11}$ = **2048** vectors.

(b) $1 - (1 - 1/2048)^{2048}$ ≈ **63.2**%.

(c) We need $(1 - 1/M)^N \le 0.01$, so $N \ge \ln 0.01 / \ln(1 - 1/M) = 9429.1$: **9430** vectors, 4.6 times the exhaustive count, for only 99% expected coverage. (The approximation $N \approx M \ln 100 = 9431$ is close.)

### Solution 08-05.12

(a) $H_{1024} = \sum_{j=1}^{1024} 1/j$ = 7.509, so $E[N_{\text{all}}] = 1024 \times 7.509$ ≈ **7689** vectors, **7.51** times $M$.

(b) After $k$ distinct inputs have been seen, a new draw is new with probability $p_k = (M - k)/M$. The number of draws until the next new input is geometric with mean $1/p_k = M/(M - k)$. Adding the expected waits for $k = 0, 1, \ldots, M - 1$:

$$
E[N_{\text{all}}] = \sum_{k=0}^{M-1} \frac{M}{M - k} = M \sum_{j=1}^{M} \frac{1}{j} = M H_M .
$$

The last term alone, finding the final unseen input, has mean $M/1 = M$ draws: as many as an entire exhaustive test. Split the sum in halves: collecting the first half of the inputs ($k < M/2$) takes $M(H_M - H_{M/2}) \approx M \ln 2$ draws, about **709** for $M = 1024$, while the second half takes $M H_{M/2}$, about **6980**. Random testing finds most inputs quickly and then spends almost all its effort on the last few, which is why random tests plateau and need directed or coverage-driven tests to close the final holes.

### Solution 08-05.13

(a) If the `x` block runs first: `x = y` gives $x$ = 1, then `y = x` gives $y$ = 1: (1, 1). If the `y` block runs first: `y = x` gives $y$ = 0, then `x = y` gives $x$ = 0: (0, 0). **2** possible outcomes, and the standard allows either: a race.

(b) With `x <= y;` and `y <= x;` both right-hand sides are read before either update: the result is always (1, 0), a swap, whatever the order.

### Solution 08-05.14

(a) One full adder per bit: **32** full adders, and $32 \times 5$ = **160** gates.

(b) It never runs on the hardware. A `generate` loop is unrolled at elaboration time, before simulation or synthesis begins, producing 32 copies of the full adder wired together; the loop variable exists only at compile time. A `for` loop inside an `always` block is likewise unrolled by synthesis.

### Solution 08-05.15

(a) Request at cycle 1: `ack` must appear at cycle 2, 3 or 4; it is 1 at cycle 3: pass. Request at cycle 4: window 5 to 7; `ack` is not 1 at any of them: fail. Request at cycle 7: window 8 to 10; `ack` at cycle 8: pass. **2** pass, **1** fails.

(b) The request at cycle 4 is never acknowledged within three cycles (the next acknowledge, at cycle 8, belongs to the request at cycle 7). In a real design this could be a lost request, an arbiter that starves one requester, or a protocol where acknowledges are matched to the wrong requests. Assertions catch such bugs at the cycle they occur, instead of many cycles later when a wrong result finally reaches an output.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-05.1a | `a + b` in 8 bits | 44 | — |
| 08-05.1b | `a + b` in 9 bits | 300 | — |
| 08-05.1c | `a - b` in 8 bits | 100 | — |
| 08-05.1d | `b - a` in 8 bits | 156 | — |
| 08-05.1e | `b - a` as signed | -100 | — |
| 08-05.2a | `4'hA` | 10 | — |
| 08-05.2b | `6'b101_011` | 43 | — |
| 08-05.2c | `12'h0F0` | 240 | — |
| 08-05.2d | width of an unsized literal | 32 | bit |
| 08-05.3a | AND-reduction | 0 | — |
| 08-05.3b | OR-reduction | 1 | — |
| 08-05.3c | XOR-reduction | 0 | — |
| 08-05.3d | `{2{a[3:0]}}` | 102 | — |
| 08-05.3e | `a[7:4]` | 10 | — |
| 08-05.3f | `a << 3` in 8 bits | 48 | — |
| 08-05.4a | $p$ as signed | -6 | — |
| 08-05.4b | `p >>> 2` | -2 | — |
| 08-05.4c | `p >> 2` | 2 | — |
| 08-05.4d | `p + 4'sd7` | 1 | — |
| 08-05.4e | `p` sign-extended to 8 bits, unsigned | 250 | — |
| 08-05.4f | `p < 4'd0` | 0 | — |
| 08-05.4g | `p < 0` | 1 | — |
| 08-05.5a | z AND 0 | 0 | — |
| 08-05.5b | `===` of identical patterns with x | 1 | — |
| 08-05.5c | definite OR results of 16 | 8 | — |
| 08-05.5d | definite NAND results of 16 | 8 | — |
| 08-05.5e | definite XNOR results of 16 | 4 | — |
| 08-05.6a | latched outputs | 2 | — |
| 08-05.7a | edges to `q4`, reverse-order blocking | 4 | — |
| 08-05.7b | edges to `q4`, forward-order blocking | 1 | — |
| 08-05.8a | $a$ after one non-blocking edge | 2 | — |
| 08-05.8b | $b$ after one non-blocking edge | 3 | — |
| 08-05.8c | $c$ after one non-blocking edge | 1 | — |
| 08-05.8d | $c$ after one blocking edge | 2 | — |
| 08-05.9a | clock frequency | 100 | MHz |
| 08-05.9b | rising edges in 1 µs | 100 | — |
| 08-05.9c | 8-bit counter after 1000 edges | 232 | — |
| 08-05.10a | mismatching steps | 2 | — |
| 08-05.11a | exhaustive vectors | 2048 | — |
| 08-05.11b | coverage with 2048 random vectors | 63.2 | % |
| 08-05.11c | random vectors for 99% expected coverage | 9430 | — |
| 08-05.11d | the approximation $M \ln 100$ | 9431 | — |
| 08-05.12a | expected vectors to cover 1024 inputs | 7689 | — |
| 08-05.12b | ratio to $M$ | 7.51 | — |
| 08-05.12c | draws for the first half of the inputs | 709 | — |
| 08-05.12d | draws for the second half | 6980 | — |
| 08-05.13a | possible race outcomes | 2 | — |
| 08-05.14a | full adders for W = 32 | 32 | — |
| 08-05.14b | gates for W = 32 | 160 | — |
| 08-05.15a | requests that pass | 2 | — |
| 08-05.15b | requests that fail | 1 | — |
