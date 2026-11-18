# Problems 03-01 · Probability in EE Language

Chapter: [03-01](../chapters/03-01-probability-in-ee-language.md) · Worked solutions: [03-01 solutions](../solutions/03-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** bit errors, defects and failures are independent unless the problem says otherwise. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 03-01.1 [A]

Events $A$ and $B$ have $P(A) = 0.3$, $P(B) = 0.5$ and $P(A \cap B) = 0.1$. Find (a) $P(A \cup B)$; (b) $P(A^c \cap B^c)$; (c) $P(A \cap B^c)$; (d) the probability that exactly one of the two occurs. Draw the Venn diagram with the probability of each region.

### Problem 03-01.2 [A]

**Soft errors in a memory.** A memory holds $10^9$ bits. During a mission each bit flips with probability $10^{-12}$, independently. Use the union bound to estimate the probability that at least one bit flips, then compute the exact value. How good is the bound, and why?

### Problem 03-01.3 [A]

(a) How many 8-bit words contain exactly two 1s? (b) Each bit of a byte is received in error with probability 0.01. Find the probability of exactly two errors, and of no errors.

### Problem 03-01.4 [B]

**What an error-correcting code buys.** A block code sends 255 bits and corrects any pattern of up to 2 bit errors. The channel's BER is $10^{-3}$.

(a) Find the probability that a block is decoded wrongly (3 or more errors).
(b) Without coding, find the probability that 255 bits contain at least one error.
(c) By what factor does the code reduce the block failure rate? What does it cost?

### Problem 03-01.5 [B]

**Address collisions.** Devices on a network pick random 16-bit identifiers, all $2^{16}$ values equally likely.

(a) Find the probability of at least one collision among 100 devices.
(b) Find the smallest number of devices for which a collision is more likely than not. Compare with the approximation $k \approx \sqrt{2N\ln2}$.
(c) Why do protocols that rely on random IDs use 48 or more bits?

### Problem 03-01.6 [A]

**Field returns.** Customer A accounts for 60% of a product's field returns and customer B for 40%. Of A's returns, 25% are "no trouble found" (NTF: the part works when retested); of B's, 50%. (a) What fraction of all returns are NTF? (b) Given that a return is NTF, what is the probability it came from customer A?

### Problem 03-01.7 [B]

**A predictive-maintenance alarm.** In a fleet of 100,000 servers, each has an impending disk failure on a given day with probability $10^{-4}$. A detector flags 95% of impending failures and also flags 0.2% of healthy servers each day.

(a) Given an alarm, what is the probability that the disk really is about to fail?
(b) How many alarms per day does the fleet produce, and how many are real?
(c) What false-positive rate would make half the alarms real?

### Problem 03-01.8 [B]

**An optical link.** A receiver decides whether a 1 (light) or a 0 (dark) was sent; each is sent with probability 0.5. A sent 1 is missed (read as 0) with probability 0.01; a sent 0 is read as 1 with probability 0.001.

(a) Find the posterior probability that a 1 was sent, given a received 1 and given a received 0.
(b) What is the MAP decision for each received value, and the resulting error probability?
(c) Explain why the two kinds of error are so different in a photodetector.

### Problem 03-01.9 [A]

Two test failures $A$ and $B$ occur with $P(A) = 0.2$ and $P(B) = 0.3$. (a) If $P(A \cap B) = 0.06$, are they independent? (b) If instead $P(A \cap B) = 0.1$, find $P(A \mid B)$ and say what the dependence suggests physically.

### Problem 03-01.10 [A]

**Parity.** $b_1$ and $b_2$ are independent bits, each 1 with probability 0.5, and $b_3 = b_1 \oplus b_2$. (a) Find $P(b_1 = 1, b_3 = 1)$ and check pairwise independence of $b_1$ and $b_3$. (b) Find $P(b_1 = 1, b_2 = 1, b_3 = 1)$. Are the three bits mutually independent?

### Problem 03-01.11 [B]

**A server's reliability block diagram.** A server needs its motherboard (reliability 0.995 over a year), at least one of two power supplies (0.98 each) and at least 3 of its 4 fans (0.97 each). Find (a) the reliability of the fan bank; (b) the server's reliability.

### Problem 03-01.12 [B]

**Common-mode failure.** Two redundant units each fail during a year with probability 0.02. Find the probability that both fail (a) if failures are independent, and (b) if 5% of each unit's failure probability is common-mode (β = 0.05). (c) By what factor does the common-mode term raise the risk?

### Problem 03-01.13 [B]

**A voter is a single point of failure.** Three modules of reliability $R = 0.95$ feed a majority voter of reliability 0.999.

(a) Find the system's reliability.
(b) For which module reliabilities is this TMR system better than one module alone? Solve $0.999(3R^2 - 2R^3) = R$.
(c) Explain the upper limit you find.

### Problem 03-01.14 [B]

**Coverage for an automotive target.** A design has 70% yield.

(a) Using the Williams–Brown model, what fault coverage is needed for a defect level of 50 DPPM?
(b) The yield then improves to 90% with the same test. What defect level results?
(c) Explain, using Bayes' rule, why better yield lowers the defect level even though the test is unchanged.

### Problem 03-01.15 [C]

**Planning a BER test.** A 112 Gb/s lane must be shown to have BER below $10^{-12}$.

(a) How many error-free bits demonstrate this with 99% confidence, and how long does the test take?
(b) If the test is allowed to see one error, the confidence that BER < $p$ after $n$ bits is $1 - e^{-np}(1 + np)$ (Poisson, [03-02](../chapters/03-02-random-variables-and-distributions.md)). Find the $np$ needed for 95% confidence.
(c) A lab reports "zero errors in $10^{12}$ bits". What upper bound on the BER does that support at 95% confidence?

### Problem 03-01.16 [B]

**What a qualification sample proves.** (a) Zero failures in 231 units: with what confidence is the defective fraction below 1%? (b) How many units with zero failures would show a defective fraction below 0.1% at 90% confidence? (c) Below 10 ppm? (d) What does this say about using qualification to demonstrate automotive DPPM targets?

### Problem 03-01.17 [B]

**Three derivations.** (a) Starting from $P(A \cup B) = P(A) + P(B) - P(A \cap B)$, derive inclusion–exclusion for three events, $P(A \cup B \cup C)$. (b) Prove that if $A$ and $B$ are independent, so are $A^c$ and $B$, and so are $A^c$ and $B^c$. (c) Show that $k$ devices with random IDs from $N$ equally likely values avoid any collision with probability about $e^{-k^2/(2N)}$, and derive the 50% collision point $k_{50} \approx \sqrt{2N\ln2} \approx 1.18\sqrt N$. Evaluate it for six-digit codes ($N = 10^6$).

### Problem 03-01.18 [B]

**Retest and conditional independence.** 5% of dies are bad. A test flags a bad die with probability 0.9 and a good die with probability 0.04. Two runs of the test on the same die are conditionally independent given whether the die is bad.
(a) Draw the probability tree for two test runs.
(b) Find $P(\text{flag}_1)$, $P(\text{flag}_1 \cap \text{flag}_2)$ and $P(\text{flag}_2 \mid \text{flag}_1)$. Are the two runs' results independent?
(c) Find $P(\text{bad} \mid \text{flag}_1)$ and $P(\text{bad} \mid \text{both flag})$, and say what retesting buys.

### Problem 03-01.19 [B]

**Nines of availability.** A web service needs two servers in series (both must be up). Each is available 99.95% of the time, and outages are independent.
(a) Find the service's availability and its downtime in minutes per year.
(b) Each server is replaced by a redundant pair that works if either member is up. Find the availability and the yearly downtime in seconds.
(c) Now 10% of each server's downtime comes from a cause that takes down both members of its pair at once. Treating unavailabilities like failure probabilities in the beta-factor model, find the yearly downtime in minutes, and comment.

### Problem 03-01.20 [C]

**Designing the test: coverage against escape cost.** A product has 85% yield. Raising the fault coverage $T$ costs tester time: model the test cost per shipped die as $c_0\ln\big(1/(1 - T)\big)$ with $c_0 = \$0.02$, so each e-fold cut in the untested fraction costs another two cents. Each defective part that ships costs \$L in returns, penalties and lost business. Use $\text{DL} \approx (1 - T)\ln(1/Y)$.
(a) With $L = \$500$, write the cost per shipped die as a function of $u = 1 - T$, find the coverage that minimizes it, and the resulting defect level and cost.
(b) Repeat for an automotive customer whose escapes cost \$5000 each.
(c) Show that the optimal defect level is $c_0/L$, independent of yield, and interpret the result.
(d) A supplier promises 1 DPPM to a customer who charges \$500 per escape. What does (c) say about that promise?

---

## Objective coverage

| Learning objective (chapter 03-01) | Problems |
|---|---|
| 1. Sample spaces, axioms, inclusion–exclusion, union bound | 1, 2, 17 |
| 2. Counting; rare-event approximation | 2, 3, 4, 5, 17 |
| 3. Conditional probability, multiplication rule, total probability, probability trees | 6, 7, 11, 18 |
| 4. Bayes' rule, base rates, MAP detection | 7, 8, 14 |
| 5. Independence, conditional independence, system reliability | 9, 10, 11, 12, 13, 17, 18, 19 |
| 6. Sanity-checking BER, DPPM, availability and qualification claims | 2, 14, 15, 16, 19, 20 |
