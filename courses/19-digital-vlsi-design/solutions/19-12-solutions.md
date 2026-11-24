# Solutions 19-12 · Design for Test: Scan, BIST and ATPG

Problems: [19-12 problem set](../problems/19-12-problems.md) · Chapter: [19-12](../chapters/19-12-design-for-test.md). Every number below is recomputed by [verify_19_12.py](../verify/verify_19_12.py).

---

## Solutions

### Solution 19-12.1

(a) $\text{DL} = 1 - 0.9^{0.05}$ = 0.005254, or **5254** DPPM.

(b) $1 - T = \ln(1 - 10^{-5})/\ln 0.9 = 9.49 \times 10^{-5}$, so $T$ = **99.9905** %. Single-digit DPPM needs coverage within a hundredth of a percent of complete, which is why automotive flows add cell-aware, transition and in-system tests on top of stuck-at.

### Solution 19-12.2

(a) Four lines (A, B, C, Y), **8** faults. Any input stuck-at-0 forces Y = 1, like Y/1: one class of four. A/1, B/1, C/1 and Y/0 are each alone: **5** classes.

(b) 111 detects the first class (good Y = 0, faulty 1) and Y/0. A/1 needs A = 0 with B = C = 1 (011); B/1 needs 101; C/1 needs 110. **4** tests. No vector detects two of A/1, B/1, C/1 (each needs a different input at 0 and the others at 1), and none of those three vectors detects the 111 class, so 4 is the minimum: $n + 1$ for an $n$-input NAND.

### Solution 19-12.3

(a) A slow-to-rise fault changes only the *time* at which a node reaches 1. A single pattern sets static values and waits; the node eventually reaches the right value, so nothing differs. The test must create a 0-to-1 transition (an initializing pattern then a launching pattern) and capture the result one clock period later.

(b) **Launch-on-shift** (skewed load): the last shift of the scan chain creates the transition, and the capture follows at speed with scan enable switched off in between. **Launch-on-capture** (broadside): the first functional capture creates the transition from the scanned-in state, and a second capture observes it.

(c) Launch-on-shift usually reaches higher coverage with fewer patterns, but scan enable must switch at functional speed, a hard timing requirement on a high-fanout signal. Launch-on-capture needs only a slow scan enable and is easier to close, at the cost of more patterns.

### Solution 19-12.4

(a) N3 feeds N10 and N11; N11 feeds N16 and N19; N16 feeds N22 and N23: three nets with fanout two, adding 6 branches to 11 stems (5 inputs and 6 gate outputs). 17 lines, **34** faults.

(b) **21** functional equivalence classes; **0** undetectable faults (c17 has no redundancy).

(c) **4** vectors, for example (N1, N2, N3, N6, N7) = 00100, 01100, 10011 and 11111; an exhaustive search over all three-vector subsets finds none that covers every fault.

### Solution 19-12.5

(a) A/1: activate with A = 0; propagate through the OR with B = 0 (non-controlling for OR); propagate through the NAND with C = 1 (non-controlling for NAND). The only test is ABC = **001** (good o = 0, F = 1; faulty o = 1, F = 0).

(b) o/0: activate with o = 1 (A = 1 or B = 1); propagate with C = 1. Tests: **011, 101 and 111**, three vectors.

(c) Activation requires the fault site to carry the opposite of the stuck value; propagation requires every side input along the path to be non-controlling. A/1 constrains all three inputs, so it has one test; o/0 constrains o and C only.

### Solution 19-12.6

(a) $p = 2^{-8}$: $N = \ln 0.01/\ln(1 - 1/256)$ = 1176.6, so **1177** patterns.

(b) Output stuck-at-1 is detected whenever the good output is 0, which is every pattern except all ones: probability $1 - 2^{-8} = 0.996$ per pattern.

(c) Split the AND into two halves and add an observation point (a scan flip-flop or a test-only XOR into a compactor) at each half's output, or a control point forcing one half to 1 in test mode. Each half then needs only 4 specific inputs, $p = 2^{-4}$.

### Solution 19-12.7

(a) The first pattern needs $L$ shifts to load. Each pattern then needs one capture cycle. While pattern $k + 1$ shifts in ($L$ cycles), the response to pattern $k$ shifts out of the same chain. After the last capture, $L$ more shifts unload the final response. Total: $L$ (first load) $+ P$ captures $+ (P - 1)L$ (overlapped loads) $+ L$ (final unload) $= P(L + 1) + L$.

(b) $L = 500\,000/16 = 31\,250$; cycles $= 5000 \times 31\,251 + 31\,250 = 156\,286\,250$; at 25 MHz, **6.25** s.

(c) $L = \lceil 500\,000/1600 \rceil = 313$; cycles $= 5000 \times 314 + 313 = 1\,570\,313$, **62.8** ms.

(d) Ratio **99.5**, not 100, because the capture cycle per pattern does not shrink and $L$ rounds up to 313.

### Solution 19-12.8

(a) With feedback from bits 3 and 2 into bit 1: 001, 010, 101, 011, 111, 110, 100, then 001 again: period **7** $= 2^3 - 1$, so $x^3 + x^2 + 1$ is primitive.

(b) **6**. $x^4 + x^2 + 1 = (x^2 + x + 1)^2$ factors, so it is not primitive, and the register cycles through shorter loops that depend on the starting state.

### Solution 19-12.9

(a) $10 \times 131\,072$ = **1 310 720** operations; at 100 MHz, **13.1** ms.

(b) A coupling fault in which a transition in cell $i$ disturbs cell $j$ is detected only if cell $j$ is read after cell $i$ has made the transition. If $i < j$, an ascending element does this; if $i > j$, a descending one. Using both orders, with reads of the expected value before each write, catches coupling faults in either direction.

### Solution 19-12.10

(a) $256/10\ \text{MHz}$ = **25.6** µs.

(b) Each bypassed chip adds one bit: $256 + 3 = 259$ bits, **25.9** µs. BYPASS exists precisely so that one chip can be accessed through a chain without shifting every other chip's full register.

(c) **32** bits.

### Solution 19-12.11

(a) As in §3.1: with $N$ independent sites each faulty with probability $p$, $Y = (1 - p)^N$; the test passes a die exactly when its $TN$ tested sites are fault-free, probability $(1 - p)^{TN} = Y^T$; good dies always pass, so $P(\text{defective} \mid \text{pass}) = 1 - Y/Y^T = 1 - Y^{1-T}$.

(b) $Y^{1-T} = e^{(1-T)\ln Y} \approx 1 + (1 - T)\ln Y$, so $\text{DL} \approx (1 - T)(-\ln Y)$. At $Y = 0.5$, $T = 0.9$: exact $1 - 0.5^{0.1}$ = **0.0670**; approximate $0.1 \ln 2$ = **0.0693**; relative error **3.5** %, an overestimate.

(c) Defects cluster on wafers, so faulty dies tend to have many faults and are easier to catch: the model overestimates escapes. And many real defects are not modeled faults at all (delays, bridges, cell-internal defects), so stuck-at coverage overstates true coverage: the model underestimates escapes. Practitioners calibrate with field-return data.

### Solution 19-12.12

(a) The MISR update $s' = A s \oplus w$ is linear over GF(2), with $A$ the shift-and-feedback matrix. Starting from 0, the final signature is $\sum_k A^{m-k} w_k$, linear in the response words. With faulty words $w_k \oplus e_k$, the signature is the good one XOR $\sum_k A^{m-k} e_k$, the signature of the error stream alone. The fault escapes if and only if that is 0.

(b) A single-bit error in word $k$ contributes $A^{m-k}$ applied to a unit vector. $A$ is invertible (a shift with feedback from the last bit), so its powers are invertible and map a nonzero vector to a nonzero vector: the signature is nonzero and the error is caught.

(c) The map from the $nm$-bit error stream to the $n$-bit signature is linear, and onto, because the last word alone can produce any signature. Its kernel therefore has dimension $nm - n$ and contains $2^{n(m-1)}$ streams, one of them zero. The aliasing fraction among nonzero streams is $(2^{n(m-1)} - 1)/(2^{nm} - 1)$. For $n = 4$, $m = 3$: $255/4095$ = **0.06227**, against $2^{-4}$ = 0.0625.

(d) Simulating all 4095 nonzero error streams through the lab's 4-bit MISR finds **255** that alias, as predicted.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-12.1a | defect level at 95 % coverage | 5254 | DPPM |
| 19-12.1b | coverage for 10 DPPM | 99.9905 | % |
| 19-12.2a | faults of a NAND3 | 8 | — |
| 19-12.2b | equivalence classes of a NAND3 | 5 | — |
| 19-12.2c | minimal tests for a NAND3 | 4 | — |
| 19-12.4a | c17 faults | 34 | — |
| 19-12.4b | c17 equivalence classes | 21 | — |
| 19-12.4c | c17 undetectable faults | 0 | — |
| 19-12.4d | c17 minimal test set | 4 | — |
| 19-12.5a | tests for A stuck-at-1 | 1 | — |
| 19-12.5b | tests for o stuck-at-0 | 3 | — |
| 19-12.6a | random patterns for 99 % confidence | 1177 | — |
| 19-12.6b | stuck-at-1 detection probability per pattern | 0.996 | — |
| 19-12.7a | cycles with 16 chains | 156286250 | — |
| 19-12.7b | test time with 16 chains | 6.25 | s |
| 19-12.7c | cycles with 1600 chains | 1570313 | — |
| 19-12.7d | test time with 1600 chains | 62.8 | ms |
| 19-12.7e | time ratio | 99.5 | — |
| 19-12.8a | period of the 3-bit LFSR | 7 | — |
| 19-12.8b | period of x^4 + x^2 + 1 from 0001 | 6 | — |
| 19-12.9a | March C- operations | 1310720 | — |
| 19-12.9b | March C- time | 13.1 | ms |
| 19-12.10a | EXTEST shift time, one chip | 25.6 | µs |
| 19-12.10b | shift time with three bypassed chips | 25.9 | µs |
| 19-12.10c | IDCODE length | 32 | bits |
| 19-12.11a | exact defect level | 0.0670 | — |
| 19-12.11b | first-order defect level | 0.0693 | — |
| 19-12.11c | relative error of the approximation | 3.5 | % |
| 19-12.12a | exact aliasing fraction, n = 4, m = 3 | 0.06227 | — |
| 19-12.12b | aliasing error streams found | 255 | — |
