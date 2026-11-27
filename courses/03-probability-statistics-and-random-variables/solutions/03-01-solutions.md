# Solutions 03-01 · Probability in EE Language

Problems: [03-01 problems](../problems/03-01-problems.md) · Chapter: [03-01](../chapters/03-01-probability-in-ee-language.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_03_01.py](../verify/verify_03_01.py).

---

## Solutions

### Solution 03-01.1

(a) Inclusion–exclusion: $P(A \cup B) = 0.3 + 0.5 - 0.1 = $ **0.7**.

(b) $A^c \cap B^c$ is the complement of $A \cup B$ (De Morgan), so its probability is \$1 - 0.7 = \$ **0.3**.

(c) $P(A \cap B^c) = P(A) - P(A \cap B) = 0.3 - 0.1 = $ **0.2**.

(d) "Exactly one" is $(A \cap B^c) \cup (A^c \cap B)$, disjoint pieces with probabilities 0.2 and $0.5 - 0.1 = 0.4$, so **0.6**. Venn diagram: $A$ only 0.2, both 0.1, $B$ only 0.4, neither 0.3; the four regions sum to 1 ✓.

### Solution 03-01.2

Union bound: \$np = 10^9\times10^{-12} = \$ **1×10⁻³**. Exact: $1 - (1 - 10^{-12})^{10^9} = 1 - e^{-10^{-3}}$ (to excellent accuracy) \$= \$ **9.995×10⁻⁴**. The bound is high by only 0.05%, because $np = 10^{-3}$ is small: the chance of two or more flips, which the bound double-counts, is about $(np)^2/2 = 5\times10^{-7}$. (Compute the exact value with `-expm1(n * log1p(-p))`; the literal formula loses most of its digits to cancellation.)

### Solution 03-01.3

(a) Choose which 2 of the 8 positions hold the 1s: $\binom{8}{2} = 8\times7/2 = $ **28**.

(b) Each pattern with exactly 2 errors has probability $0.01^2\times0.99^6$, and there are 28 such patterns: \$28\times10^{-4}\times0.99^6 = \$ **0.002636**. No errors: \$0.99^8 = \$ **0.9227**.

### Solution 03-01.4

(a) Block failure is 3 or more errors:

$$
P(\text{fail}) = 1 - \sum_{k=0}^{2}\binom{255}{k}(10^{-3})^k(0.999)^{255 - k} .
$$

The three terms are $0.999^{255} = 0.7748$, $255\times10^{-3}\times0.999^{254} = 0.1978$ and $\binom{255}{2}\times10^{-6}\times0.999^{253} = 0.02514$, which sum to 0.9977. So \$P(\text{fail}) = \$ **2.263×10⁻³**.

(b) Uncoded: $1 - 0.999^{255} = $ **0.2252**.

(c) The ratio is $0.2252/0.002263 = $ **99.49**: about 100 times fewer failed blocks. The cost is the redundancy: to correct 2 errors in 255 bits, a code of this length uses 16 check bits (a BCH code carries 239 data bits), plus the encoder and decoder logic and latency. Note also that "failure" here means a wrong decoded block; a real system adds a CRC to detect most of those.

### Solution 03-01.5

(a) With $N = 2^{16} = 65{,}536$: $P(\text{no collision}) = \prod_{i=0}^{99}(1 - i/N) = 0.9272$, so \$P(\text{collision}) = \$ **0.07278**. The approximation $1 - e^{-k(k - 1)/(2N)} = 1 - e^{-0.07553} = 0.07275$ agrees.

(b) Solving $e^{-k^2/(2N)} = 0.5$ gives \$k \approx \sqrt{2N\ln2} = \$ **301.4**. The exact product first drops below 0.5 at \$k = \$ **302** devices.

(c) With $N = 2^{48}$, collisions become likely only near $\sqrt{N} \approx 1.7\times10^7$ devices, and for a few thousand devices the probability is around $10^{-8}$. Short random IDs collide surprisingly early, because the number of *pairs*, $k(k - 1)/2$, grows as $k^2$.

### Solution 03-01.6

(a) Total probability: $P(\text{NTF}) = 0.6\times0.25 + 0.4\times0.5 = 0.15 + 0.20 = $ **0.35**.

(b) Bayes: $P(A \mid \text{NTF}) = 0.15/0.35 = $ **0.4286**. Customer A sends 60% of returns but only 43% of the NTF ones.

### Solution 03-01.7

(a) $P(\text{alarm}) = 10^{-4}\times0.95 + 0.9999\times0.002 = 9.5\times10^{-5} + 1.9998\times10^{-3} = 2.0948\times10^{-3}$. So \$P(\text{fail} \mid \text{alarm}) = 9.5\times10^{-5}/2.0948\times10^{-3} = \$ **0.04535**: under 5% of alarms are real.

(b) $10^5\times2.0948\times10^{-3} = $ **209.5** alarms a day, of which $10^5\times9.5\times10^{-5} = $ **9.5** are real. An operations team that sees 200 false alarms a day stops trusting the detector.

(c) Half real means true alarms equal false ones: $9.5\times10^{-5} = 0.9999\,f$, so \$f = \$ **9.501×10⁻⁵**, about 21 times lower than today. For rare conditions, the false-positive rate, not the detection rate, is the specification that matters.

### Solution 03-01.8

(a) $P(\text{recv }1) = 0.5\times0.99 + 0.5\times0.001 = 0.4955$, so \$P(1 \mid \text{recv }1) = 0.495/0.4955 = \$ **0.9990**. $P(\text{recv }0) = 0.5\times0.01 + 0.5\times0.999 = 0.5045$, so \$P(1 \mid \text{recv }0) = 0.005/0.5045 = \$ **0.009911**.

(b) Both posteriors favor believing the received bit, so MAP decides 1 for a received 1 and 0 for a received 0 (here the same as ML). It errs when a 1 is missed or a 0 is read as 1: $0.5\times0.01 + 0.5\times0.001 = $ **0.0055**.

(c) The noise is not the same on the two levels. Photon arrivals are random (shot noise), and their fluctuation grows with the optical power, so the "1" level is much noisier than the dark "0" level. A threshold midway between the levels therefore sits fewer noise standard deviations from the 1 level than from the 0 level, and misses of 1s dominate. The error-minimizing threshold sits below the midpoint, toward the quieter 0 level (Problem 03-02.20 works this out).

### Solution 03-01.9

(a) \$P(A)P(B) = 0.2\times0.3 = \$ **0.06** $= P(A \cap B)$: independent.

(b) \$P(A \mid B) = 0.1/0.3 = \$ **0.3333**, against $P(A) = 0.2$. Failing $B$ raises the chance of failing $A$ by two-thirds: the failures share a cause, such as a marginal supply voltage or a defect cluster that affects both tested blocks.

### Solution 03-01.10

(a) $b_1 = 1$ and $b_3 = 1$ require $b_2 = 0$: probability \$0.5\times0.5 = \$ **0.25** $= P(b_1 = 1)P(b_3 = 1)$, since $P(b_3 = 1) = 0.5$. The other combinations work the same way, so $b_1$ and $b_3$ are independent; by symmetry so are the other pairs.

(b) $b_1 = b_2 = 1$ forces $b_3 = 0$, so \$P(b_1 = b_2 = b_3 = 1) = \$ **0**, not $1/8$. The bits are pairwise independent but not mutually independent: knowing any two determines the third, which is what makes parity useful for error detection.

### Solution 03-01.11

(a) The fan bank works with 4 good fans or exactly 3: $R_{3/4} = 0.97^4 + 4\times0.97^3\times0.03 = 0.8853 + 0.1095 = $ **0.9948**.

(b) Power: $1 - 0.02^2 = 0.9996$. The three blocks are in series: \$R = 0.9996\times0.995\times0.9948 = \$ **0.9894**. The motherboard (0.50% failure probability) and the 3-of-4 fan bank (0.52%) contribute almost equally to the 1.06%; the redundant supplies contribute only 0.04%.

### Solution 03-01.12

(a) Independent: $0.02^2 = $ **4×10⁻⁴**.

(b) With β = 0.05: common-mode $\beta q = 0.001$, independent part $(1 - \beta)q = 0.019$. Then \$P(\text{both fail}) = 0.001 + 0.999\times0.019^2 = 0.001 + 0.000361 = \$ **1.361×10⁻³**.

(c) $1.361\times10^{-3}/4\times10^{-4} = $ **3.402**: a 5% common-mode share more than triples the risk, and the common-mode term alone is larger than the independent double failure.

### Solution 03-01.13

(a) The voter is in series with the 2-out-of-3 modules: $R = 0.999\times(3\times0.95^2 - 2\times0.95^3) = 0.999\times0.99275 = $ **0.9918**, against 0.95 for one module.

(b) $0.999(3R^2 - 2R^3) = R$ has the root $R = 0$ and, after dividing by $R$, the quadratic $1.998R^2 - 2.997R + 1 = 0$:

$$
R = \frac{2.997 \pm \sqrt{2.997^2 - 4\times1.998}}{2\times1.998} = \frac{2.997 \pm 0.9950}{3.996} .
$$

The roots are **0.5010** and **0.9990**. TMR helps for $0.5010 < R < 0.9990$.

(c) A very reliable module (failure probability below 0.1%) is already better than the voter, whose own failure probability is 0.1%. Adding a single point of failure less reliable than the thing it protects makes the system worse. Voters must be far more reliable than the modules, which is why they are small and simple.

### Solution 03-01.14

(a) $1 - Y^{1 - T} = 5\times10^{-5}$ gives \$1 - T = \ln(1 - 5\times10^{-5})/\ln0.7 = 5.000\times10^{-5}/0.3567 = \$ **1.402×10⁻⁴**, so \$T = \$ **0.99986**.

(b) $1 - 0.9^{1.402\times10^{-4}} = 1.477\times10^{-5}$: **14.77 DPPM**, less than a third of before.

(c) The defect level is $P(\text{bad} \mid \text{pass})$. The test's escape probability for a bad die is unchanged, but higher yield means fewer bad dies reach the tester: the prior $P(\text{bad})$ falls. Bayes' rule then lowers the posterior. In the model, DL ≈ $(1 - T)\ln(1/Y)$, and $\ln(1/0.9)/\ln(1/0.7) = 0.295$ ✓.

### Solution 03-01.15

(a) $n = -\ln(0.01)/10^{-12} = $ **4.605×10¹²** bits, which at 112 Gb/s takes **41.12 s**.

(b) Solve $1 - e^{-m}(1 + m) = 0.95$ for $m = np$ numerically: \$m = \$ **4.744**. Allowing one error raises the required bits from $3.0/p$ to $4.74/p$, but makes the test robust to a single stray error.

(c) \$p_{95} = -\ln(0.05)/10^{12} = \$ **3.0×10⁻¹²**. Zero errors in $10^{12}$ bits does *not* show BER < $10^{-12}$; it shows only that the BER is below about $3\times10^{-12}$ at 95% confidence.

### Solution 03-01.16

(a) If the defective fraction were 1%, the chance of zero failures in 231 would be $0.99^{231} = 0.098$. So zero failures supports "below 1%" with confidence \$1 - 0.098 = \$ **0.9019**.

(b) Need $0.999^n \le 0.1$: $n \ge \ln0.1/\ln0.999 = 2301.4$, so **2302** units.

(c) $n \ge \ln0.1/\ln(1 - 10^{-5}) = 230{,}257.4$: **230,258** units, all passing.

(d) Demonstrating ppm-level quality by sampling would take hundreds of thousands of units per qualification, which is impractical. Qualification shows the design and process are sound (no systematic failure mechanism at the 1% level); DPPM is controlled by statistical process control, screening and test coverage, and verified by field returns over millions of shipped parts.

### Solution 03-01.17

(a) Treat $A \cup B$ as one event: $P((A \cup B) \cup C) = P(A \cup B) + P(C) - P((A \cup B) \cap C)$. Distribute the intersection, $(A \cup B) \cap C = (A \cap C) \cup (B \cap C)$, and apply the two-event rule again, noting that $(A \cap C) \cap (B \cap C) = A \cap B \cap C$:

$$
P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C) + P(A \cap B \cap C) .
$$

(b) $B$ is the disjoint union of $A \cap B$ and $A^c \cap B$, so $P(A^c \cap B) = P(B) - P(A)P(B) = (1 - P(A))P(B) = P(A^c)P(B)$. Applying the same argument with $A^c$ in place of $B$'s partner gives $P(A^c \cap B^c) = P(A^c) - P(A^c \cap B) = P(A^c)(1 - P(B)) = P(A^c)P(B^c)$.

(c) Device $i + 1$ avoids the $i$ IDs already taken with probability $1 - i/N$, so $P(\text{no collision}) = \prod_{i=0}^{k-1}(1 - i/N) \approx \exp\big(-\sum_{i=0}^{k-1}i/N\big) = e^{-k(k-1)/(2N)} \approx e^{-k^2/(2N)}$, using $1 - x \approx e^{-x}$. Setting this to ½ gives $k^2 = 2N\ln2$, so \$k_{50} = \sqrt{2\ln2}\,\sqrt N = \$ **1.177**$\sqrt N$. For $N = 10^6$: **1177.4**, and the exact product first passes 50% at **1178** codes.

### Solution 03-01.18

(a) The tree branches first on the die's state (bad 0.05, good 0.95), then on run 1 (flag or pass), then on run 2 with the same conditional probabilities as run 1: that is what conditional independence means.

(b) \$P(\text{flag}_1) = 0.05(0.9) + 0.95(0.04) = \$ **0.083**. \$P(\text{both}) = 0.05(0.9)^2 + 0.95(0.04)^2 = \$ **0.04202**. So \$P(\text{flag}_2 \mid \text{flag}_1) = 0.04202/0.083 = \$ **0.5063**, far above $P(\text{flag}_2) = 0.083$: the runs' results are strongly *dependent*, because both depend on the same die. Conditional independence given the state does not make the results independent.

(c) $P(\text{bad} \mid \text{flag}_1) = 0.045/0.083 = $ **0.5422**; $P(\text{bad} \mid \text{both}) = 0.0405/0.04202 = $ **0.9638**. One flag is a coin toss, because false flags from the large good population rival true ones; a second, conditionally independent flag makes the die almost certainly bad. Retesting rejects is a cheap way to recover good dies (overkill), provided the test's errors are random rather than systematic.

### Solution 03-01.19

(a) Series: $A = 0.9995^2 = $ **0.9990**. Downtime $(1 - 0.99900025)\times8766\times60 = $ **525.8 min** a year (about 8.8 hours).

(b) A pair is down only when both members are: $1 - 0.0005^2$. Two pairs in series: \$A = (1 - 2.5\times10^{-7})^2 = \$ **0.9999995**, and the downtime is **15.78 s** a year.

(c) Each pair's unavailability is $\beta u + (1 - \beta u)\big((1 - \beta)u\big)^2 \approx 0.1\times0.0005 = 5.0\times10^{-5}$, and two pairs give about **52.81 min** a year: 200 times the independent result, and only a tenfold gain over no redundancy. Independent redundancy buys "six nines"; a 10% common-mode share caps it near four. (Availability is a long-run fraction, so these figures also assume outages that are short and independent of each other.)

### Solution 03-01.20

(a) With $u = 1 - T$, the cost per shipped die is $C(u) = c_0\ln(1/u) + L\,u\ln(1/Y)$. Setting $dC/du = -c_0/u + L\ln(1/Y) = 0$ gives

$$
u^* = \frac{c_0}{L\ln(1/Y)} = \frac{0.02}{500\times0.1625} = 2.461\times10^{-4} .
$$

So $T^* = $ **0.999754**, $\text{DL} = u^*\ln(1/Y) = $ **40.00 DPPM**, and the cost is $0.02\ln(1/u^*) + 500\times4\times10^{-5} = 0.1662 + 0.0200 = $ **\$0.1862** per shipped die.

(b) With $L = \$5000$, \$u^* = \$ **2.461×10⁻⁵**, \$T^* = \$ **0.9999754**, \$\text{DL} = \$ **4.000 DPPM**, and the cost rises to **\$0.2322**.

(c) $\text{DL}^* = u^*\ln(1/Y) = c_0/L$: the yield cancels. At the optimum, the escape cost per shipped die, $L\cdot\text{DL}^* = c_0$, equals the price of one more e-fold of coverage. A higher liability buys a proportionally lower defect level; a lower yield needs more coverage to reach it, but the target itself is set by economics, not by the process.

(d) With $c_0/L = 0.02/500 = 40$ DPPM, a 1 DPPM promise is 40 times below this supplier's economic optimum. Either their test cost per e-fold is far lower than \$0.02, or the customer's escape cost is far higher than they admit, or the promise rests on something other than test coverage (screening, process control). Ask which.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 03-01.1a | P(A ∪ B) | 0.7 | — |
| 03-01.1b | P(neither) | 0.3 | — |
| 03-01.1c | P(A only) | 0.2 | — |
| 03-01.1d | P(exactly one) | 0.6 | — |
| 03-01.2a | union bound | 1×10^-3 | — |
| 03-01.2b | exact probability | 9.995×10^-4 | — |
| 03-01.3a | 8-bit words with two 1s | 28 | — |
| 03-01.3b | P(exactly two errors) | 0.002636 | — |
| 03-01.3c | P(no errors) | 0.9227 | — |
| 03-01.4a | coded block failure | 2.263×10^-3 | — |
| 03-01.4b | uncoded block error | 0.2252 | — |
| 03-01.4c | improvement factor | 99.49 | — |
| 03-01.5a | collision probability, 100 devices | 0.07278 | — |
| 03-01.5b | approximate 50% point | 301.4 | devices |
| 03-01.5c | exact 50% point | 302 | devices |
| 03-01.6a | P(NTF) | 0.35 | — |
| 03-01.6b | P(A given NTF) | 0.4286 | — |
| 03-01.7a | P(failure given alarm) | 0.04535 | — |
| 03-01.7b | alarms per day | 209.5 | — |
| 03-01.7c | real alarms per day | 9.5 | — |
| 03-01.7d | false-positive rate for 50% precision | 9.501×10^-5 | — |
| 03-01.8a | P(1 given received 1) | 0.9990 | — |
| 03-01.8b | P(1 given received 0) | 0.009911 | — |
| 03-01.8c | error probability | 0.0055 | — |
| 03-01.9a | P(A)P(B) | 0.06 | — |
| 03-01.9b | P(A given B) | 0.3333 | — |
| 03-01.10a | P(b1 = 1, b3 = 1) | 0.25 | — |
| 03-01.10b | P(all three bits 1) | 0 | — |
| 03-01.11a | fan-bank reliability | 0.9948 | — |
| 03-01.11b | server reliability | 0.9894 | — |
| 03-01.12a | both fail, independent | 4×10^-4 | — |
| 03-01.12b | both fail, beta = 0.05 | 1.361×10^-3 | — |
| 03-01.12c | risk factor | 3.402 | — |
| 03-01.13a | TMR with voter | 0.9918 | — |
| 03-01.13b | lower break-even | 0.5010 | — |
| 03-01.13c | upper break-even | 0.9990 | — |
| 03-01.14a | untested fraction for 50 DPPM | 1.402×10^-4 | — |
| 03-01.14b | coverage for 50 DPPM | 0.99986 | — |
| 03-01.14c | defect level at 90% yield | 14.77 | DPPM |
| 03-01.15a | bits for 99% confidence | 4.605×10^12 | — |
| 03-01.15b | test time at 112 Gb/s | 41.12 | s |
| 03-01.15c | np for 95% with one error allowed | 4.744 | — |
| 03-01.15d | 95% upper bound after 1e12 clean bits | 3.0×10^-12 | — |
| 03-01.16a | confidence from 0 of 231 | 0.9019 | — |
| 03-01.16b | units for 0.1% at 90% | 2302 | — |
| 03-01.16c | units for 10 ppm at 90% | 230258 | — |
| 03-01.17a | sqrt(2 ln 2) | 1.177 | — |
| 03-01.17b | approximate 50% point, N = 1e6 | 1177.4 | codes |
| 03-01.17c | exact 50% point, N = 1e6 | 1178 | codes |
| 03-01.18a | P(flag on run 1) | 0.083 | — |
| 03-01.18b | P(flag on both runs) | 0.04202 | — |
| 03-01.18c | P(flag 2 given flag 1) | 0.5063 | — |
| 03-01.18d | P(bad given one flag) | 0.5422 | — |
| 03-01.18e | P(bad given two flags) | 0.9638 | — |
| 03-01.19a | series availability | 0.9990 | — |
| 03-01.19b | series downtime | 525.8 | min/yr |
| 03-01.19c | availability with redundant pairs | 0.9999995 | — |
| 03-01.19d | downtime with redundant pairs | 15.78 | s/yr |
| 03-01.19e | downtime with 10% common mode | 52.81 | min/yr |
| 03-01.19f | common-mode unavailability per pair, approx | 5.0×10^-5 | — |
| 03-01.20a | optimal untested fraction, L = 500 | 2.461×10^-4 | — |
| 03-01.20b | optimal coverage, L = 500 | 0.999754 | — |
| 03-01.20c | optimal defect level, L = 500 | 40.00 | DPPM |
| 03-01.20d | test cost at the optimum, L = 500 | 0.1662 | $ |
| 03-01.20e | total cost per die, L = 500 | 0.1862 | $ |
| 03-01.20f | optimal untested fraction, L = 5000 | 2.461×10^-5 | — |
| 03-01.20g | optimal coverage, L = 5000 | 0.9999754 | — |
| 03-01.20h | optimal defect level, L = 5000 | 4.000 | DPPM |
| 03-01.20i | total cost per die, L = 5000 | 0.2322 | $ |
| 03-01.20j | ln(1/Y) at 85% yield | 0.1625 | — |
| 03-01.11c | motherboard failure probability | 0.50 | % |
| 03-01.11d | fan-bank failure probability | 0.52 | % |
| 03-01.11e | supply-pair failure probability | 0.04 | % |
