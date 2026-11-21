# Problems 17-07 · Information Theory and Shannon Capacity

Chapter: [17-07](../chapters/17-07-information-theory-and-shannon.md) · Worked solutions: [17-07 solutions](../solutions/17-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Logarithms are base 2 unless stated; $h(p)$ is the binary entropy function; capacities are per channel use, per real sample or per second as stated; $N_0$ is one-sided. Problems marked *(lab)* can be checked with the lab's `infotheory.py` or an equivalent tool.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-07.1 [A]

**Entropies.** Find the entropy of a fair six-sided die, of a coin that lands heads with probability 0.9, and of a source with probabilities 0.4, 0.3, 0.2, 0.1.

### Problem 17-07.2 [A]

**A Huffman code.** *(lab)* Build a Huffman code for the four-symbol source of Problem 17-07.1 and find its average length and its efficiency $H/\bar\ell$.

### Problem 17-07.3 [A]

**Kraft.** Can a prefix code have codeword lengths 1, 2, 2, 3? Lengths 1, 2, 3, 3? Explain with the Kraft sum.

### Problem 17-07.4 [B]

**Mutual information.** $X$ and $Y$ are binary with joint probabilities $p(0,0) = p(1,1) = 0.4$ and $p(0,1) = p(1,0) = 0.1$. Find $H(X)$, $H(Y\mid X)$ and $I(X; Y)$, and interpret the result as a channel.

### Problem 17-07.5 [B]

**Erasures against errors.** Compare the capacity of a binary erasure channel with ε = 0.2 and a binary symmetric channel with $p$ = 0.2. Why are erasures so much cheaper?

### Problem 17-07.6 [B]

**The Z-channel.** *(lab)* Input 0 is always received as 0; input 1 is received as 1 with probability 0.5 and as 0 otherwise. Find the capacity and the optimal probability of sending 1. (For crossover probability $q$, $C = \log_2(1 + (1 - q)q^{q/(1-q)})$.) Why is the optimal input not uniform?

### Problem 17-07.7 [B]

**Shannon–Hartley.** Find the capacity of a 1 MHz channel at 10 dB SNR, and the SNR needed for 10 b/s/Hz.

### Problem 17-07.8 [B]

**The least bandwidth.** A link must carry 10 Mb/s with a received $S/N_0$ of 70 dB-Hz. What is the minimum bandwidth? Repeat for 73 dB-Hz.

### Problem 17-07.9 [B]

**A coded QPSK system.** QPSK with a rate-3/4 code and ideal Nyquist pulses carries 1.5 b/s/Hz. (a) What is the smallest $E_b/N_0$ that any system at 1.5 b/s/Hz could need? (b) What is the smallest for a system that, like this one, must send equiprobable QPSK symbols (soft decisions)? (c) DVB-S2's QPSK 3/4 mode needs $E_s/N_0$ = 4.03 dB at a spectral efficiency of 1.487473 b/s/Hz ([R-276](../../../reference/research-log.md)). How far is it from each bound?

### Problem 17-07.10 [B]

**Power-limited.** With $S/N_0$ = 60 dB-Hz, find the capacity with unlimited bandwidth, with 1 MHz and with 10 MHz.

### Problem 17-07.11 [C]

**The Gaussian channel.** Derive the differential entropy of $\mathcal N(0, \sigma^2)$ and evaluate it for σ = 1. Then derive $C = \tfrac12\log_2(1 + P/\sigma^2)$, stating where the maximum-entropy property is used.

### Problem 17-07.12 [C]

**Optimal code lengths.** Minimize $\sum p_i\ell_i$ subject to $\sum2^{-\ell_i} = 1$ (treating lengths as real) with a Lagrange multiplier, and show the minimum is $H$. Why does a real code's average length lie below $H + 1$?

### Problem 17-07.13 [C]

**Water-filling three channels.** *(lab)* Channels with noise-normalized gains 2, 1 and 0.2 share a total power of 1. Find the water-filling allocation and capacity, and compare with an equal split.

### Problem 17-07.14 [C]

**Constrained capacity at 0 dB.** *(lab)* At $E_s/N_0$ = 0 dB on a real AWGN channel, compute the capacity per use with a Gaussian input, with BPSK and soft decisions, and with BPSK and hard decisions. What fraction of the Gaussian capacity does each binary option achieve?

### Problem 17-07.15 [B]

**The ultimate limit and a real gap.** (a) Show that $(2^\eta - 1)/\eta \to \ln2$ as $\eta \to 0$, using a Taylor series, and express the limit in dB. (b) DVB-S2's 8PSK rate-2/3 mode needs $E_s/N_0$ = 6.62 dB at a spectral efficiency of 1.980636 b/s/Hz ([R-276](../../../reference/research-log.md)). Find its $E_b/N_0$, the Shannon limit at its efficiency, and the gap between them.

### Problem 17-07.16 [B]

**Water-filling from the KKT conditions.** Two parallel Gaussian channels have noise-normalized gains $g_1$ = 2 and $g_2$ = 0.5 per unit power. (a) Write the Lagrangian for maximizing $\log_2(1 + g_1p_1) + \log_2(1 + g_2p_2)$ subject to $p_1 + p_2 = P$ and $p_k \ge 0$, and derive the water-filling rule. (b) With $P$ = 1, find the powers and the capacity. (c) Above what total power does the weaker channel receive any power?

---

## Objective coverage

| Learning objective (chapter 17-07) | Problems |
|---|---|
| 1. Entropy and source coding | 1, 2, 3, 12 |
| 2. Mutual information, BSC, BEC | 4, 5, 6 |
| 3. AWGN capacity and regimes | 7, 8, 10, 11 |
| 4. Shannon limit | 8, 9, 15 |
| 5. Constrained inputs, soft decisions | 14 |
| 6. Water-filling | 13, 16 |
