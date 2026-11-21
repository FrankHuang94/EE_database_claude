# Solutions 17-07 · Information Theory and Shannon Capacity

Problems: [17-07 problems](../problems/17-07-problems.md) · Chapter: [17-07](../chapters/17-07-information-theory-and-shannon.md). Every number below is recomputed by [verify_17_07.py](../verify/verify_17_07.py): entropies directly, Huffman codes by implementation, channel capacities in closed form and by the Blahut–Arimoto algorithm, Gaussian quantities by numerical integration, and water-filling by a constrained optimizer.

---

## Solutions

### Solution 17-07.1

- Die: $\log_26$ = **2.585** bits.
- Biased coin: $h(0.9) = -0.9\log_20.9 - 0.1\log_20.1$ = **0.469** bits: a long record of such flips compresses to under half its length.
- Source (0.4, 0.3, 0.2, 0.1): $0.4(1.322) + 0.3(1.737) + 0.2(2.322) + 0.1(3.322)$ = **1.846** bits.

### Solution 17-07.2

Merge 0.1 and 0.2 (0.3); merge that with 0.3 (0.6); merge with 0.4. Codewords: 0.4 → 0, 0.3 → 10, 0.2 → 110, 0.1 → 111. Average length $0.4 + 0.6 + 0.6 + 0.3$ = **1.9** bits; efficiency $1.846/1.9$ = **0.972**. The 3% loss comes from probabilities that are not powers of 1/2; coding pairs of symbols would reduce it.

### Solution 17-07.3

Lengths 1, 2, 2, 3: $\tfrac12 + \tfrac14 + \tfrac14 + \tfrac18$ = **1.125** > 1, impossible: once 0, 10 and 11 are used, every 3-bit word begins with one of them. Lengths 1, 2, 3, 3: the sum is exactly 1, achieved by 0, 10, 110, 111.

### Solution 17-07.4

The marginals are uniform, so $H(X)$ = 1. Given $X$, $Y$ equals $X$ with probability 0.8: $H(Y\mid X) = h(0.2) = 0.722$. Hence $I(X; Y) = H(Y) - H(Y\mid X) = 1 - 0.722$ = **0.278** bits. This is a BSC with $p$ = 0.2 driven by a uniform input: each use conveys 0.278 bits, its capacity.

### Solution 17-07.5

BEC: $1 - 0.2$ = **0.8**. BSC: $1 - h(0.2)$ = **0.278**. With erasures the receiver knows which 20% of the bits are missing and only needs to replace them; with errors it must also find which bits are wrong, and that location information, $h(0.2)$ = 0.72 bits per use, is what the redundancy has to pay for.

### Solution 17-07.6

Let $\pi = P(X = 1)$. A 0 is always received as 0, and a 1 arrives as 1 with probability $1 - q$, so $P(Y = 1) = \pi(1 - q)$ and $H(Y\mid X) = \pi h(q)$. Hence

$$
I(\pi) = h\big(\pi(1 - q)\big) - \pi h(q) ,
$$

which is concave in π. Using $h'(u) = \log_2[(1 - u)/u]$, setting $dI/d\pi = 0$ gives

$$
(1 - q)\log_2\frac{1 - \pi(1 - q)}{\pi(1 - q)} = h(q)
\quad\Rightarrow\quad
\pi^* = \frac{1}{(1 - q)\big(1 + 2^{h(q)/(1 - q)}\big)} .
$$

With $q$ = 0.5, $h(q)$ = 1 and $2^{1/0.5}$ = 4, so $\pi^* = 1/(0.5 \times 5)$ = **0.4**, and $C = h(0.2) - 0.4 \times 1 = 0.722 - 0.4$ = **0.322** bits per use. The general closed form is $C = \log_2(1 + (1 - q)q^{q/(1 - q)})$; at $q$ = 0.5 it is $\log_21.25$, the same number. The channel is asymmetric: a 0 is always received correctly, while a 1 is ambiguous, so the input should favour the reliable symbol. The Blahut–Arimoto algorithm finds the same result numerically.

### Solution 17-07.7

$C = 10^6\log_2 11$ = **3.459** Mb/s. 10 b/s/Hz needs $\text{SNR} = 2^{10} - 1 = 1023$, **30.10** dB.

### Solution 17-07.8

Solve $B\log_2(1 + (S/N_0)/B) = 10^7$. With $S/N_0 = 10^7$ Hz, $x = (S/N_0)/B$ must satisfy $\log_2(1 + x)/x = 1$, so $x = 1$ and $B$ = **10** MHz (η = 1, and $E_b/N_0 = (S/N_0)/R_b$ = 0 dB, exactly the Shannon limit at η = 1). With 73 dB-Hz ($10^{7.3} = 1.995 \times 10^7$ Hz) there is no closed form. Solve $B\log_2(1 + 1.995 \times 10^7/B) = 10^7$ numerically, for example by bisection: the left side grows with $B$, and it is 0.88 × 10⁷ at $B$ = 3 MHz and 1.03 × 10⁷ at 4 MHz. The root is $B$ = **3.77** MHz: more power buys a much narrower channel. (Rounding $S/N_0$ to 2 × 10⁷ Hz gives 3.76 MHz; at this step the third digit is sensitive to the rounding.)

### Solution 17-07.9

(a) $(2^{1.5} - 1)/1.5 = 1.219$, **0.86** dB: the Gaussian-input bound at 1.5 b/s/Hz, for any modulation.

(b) QPSK is two independent BPSK dimensions, each carrying 0.75 bit per use. The BPSK soft-decision capacity (§3.7) reaches 0.75 bit at $E_s/N_0$ = 0.377 dB per dimension; with 0.75 information bit per dimension, $E_b/N_0 = E_s/N_0 - 10\log_{10}0.75$ = **1.63** dB. Restricting the input to QPSK costs 0.77 dB at this rate.

(c) $E_b/N_0 = 4.03 - 10\log_{10}1.487473$ = **2.31** dB, 1.45 dB from the unconstrained bound (evaluated at 1.5 b/s/Hz) but only 0.68 dB from the QPSK bound. The second gap is the honest measure of the code: 64 800-bit LDPC codes at quasi-error-free operation sit within a decibel of what their constellation allows.

### Solution 17-07.10

$S/N_0 = 10^6$ Hz. Unlimited bandwidth: $10^6/\ln2$ = **1.443** Mb/s. With 1 MHz the SNR is 1 and $C$ = **1.0** Mb/s; with 10 MHz, SNR 0.1 and $C = 10^7\log_2 1.1$ = **1.375** Mb/s. Ten times the bandwidth gained only 37.5%: at low SNR the link is power-limited.

### Solution 17-07.11

For $f(x) = (2\pi\sigma^2)^{-1/2}e^{-x^2/(2\sigma^2)}$, $-\log_2f(x) = \tfrac12\log_2(2\pi\sigma^2) + \frac{x^2}{2\sigma^2}\log_2e$. Averaging, with $\mathbb E[x^2] = \sigma^2$, $h = \tfrac12\log_2(2\pi\sigma^2) + \tfrac12\log_2e = \tfrac12\log_2(2\pi e\sigma^2)$, which is **2.047** bits for σ = 1.

For $Y = X + Z$: $I(X; Y) = h(Y) - h(Y\mid X) = h(Y) - h(Z)$, since given $X$ the only uncertainty is $Z$. $\operatorname{Var}Y = P + \sigma^2$, and **by the maximum-entropy property** $h(Y) \le \tfrac12\log_2(2\pi e(P + \sigma^2))$, with equality when $Y$ is Gaussian, which happens when $X$ is Gaussian. Subtracting $h(Z)$: $C = \tfrac12\log_2(1 + P/\sigma^2)$.

### Solution 17-07.12

Minimize $L = \sum p_i\ell_i + \lambda(\sum2^{-\ell_i} - 1)$. Setting $\partial L/\partial\ell_i = p_i - \lambda\ln2\,2^{-\ell_i} = 0$ gives $2^{-\ell_i} \propto p_i$; the constraint fixes $2^{-\ell_i} = p_i$, so $\ell_i = -\log_2p_i$ and the minimum average length is $H$. Real lengths must be integers: choosing $\ell_i = \lceil-\log_2p_i\rceil$ still satisfies Kraft and adds less than one bit to each, so $\bar\ell < H + 1$.

### Solution 17-07.13

Floors $1/g$ = 0.5, 1 and 5. Trying all three channels gives μ = (1 + 0.5 + 1 + 5)/3 = 2.5, below the third floor, so drop it. With two, μ = (1 + 0.5 + 1)/2 = **1.25**: $p$ = (**0.75**, **0.25**, 0). Capacity $\log_2(1 + 1.5) + \log_2(1 + 0.25)$ = **1.644** b/s/Hz, against **1.245** for an equal split of 1/3 each: water-filling adds 32%.

### Solution 17-07.14

With σ² = $N_0/2$ and $E_s/N_0$ = 1:

- Gaussian input: $\tfrac12\log_2(1 + 2E_s/N_0) = \tfrac12\log_23$ = **0.792** bits per use.
- BPSK, soft: by numerical integration, **0.721** (91%).
- BPSK, hard: a BSC with $p = Q(\sqrt2)$ = 0.0786, $1 - h(0.0786)$ = **0.603** (76%).

At this SNR soft BPSK keeps most of the Gaussian capacity; hard decisions throw away almost a quarter of it.

### Solution 17-07.15

(a) With $2^\eta = e^{\eta\ln2} = 1 + \eta\ln2 + (\eta\ln2)^2/2 + \dots$,

$$
\frac{2^\eta - 1}{\eta} = \ln2 + \frac{\eta(\ln2)^2}{2} + \dots \to \ln2 = 0.693 ,
$$

that is $10\log_{10}0.693$ = **−1.59** dB. L'Hôpital's rule gives the same: the derivative of the numerator is $2^\eta\ln2 \to \ln2$.

(b) $E_b/N_0 = 6.62 - 10\log_{10}1.980636$ = **3.65** dB. The limit at η = 1.980636 is $(2^{1.980636} - 1)/1.980636$ = 1.488, **1.73** dB, so the gap is **1.93** dB. Part of the gap is the 8PSK constellation constraint and part is the finite (64 800-bit) block length and the quasi-error-free target.

### Solution 17-07.16

(a) With a multiplier λ for the power constraint and $\nu_k \ge 0$ for $p_k \ge 0$,

$$
L = \log_2(1 + 2p_1) + \log_2(1 + 0.5p_2) - \lambda(p_1 + p_2 - P) + \nu_1p_1 + \nu_2p_2 .
$$

$\partial L/\partial p_k = 0$ gives $g_k/[(1 + g_kp_k)\ln2] = \lambda - \nu_k$. For an active channel ($p_k > 0$, so $\nu_k = 0$), $1/g_k + p_k = 1/(\lambda\ln2) \equiv \mu$; for an inactive one, $\nu_k \ge 0$ means $1/g_k \ge \mu$. So $p_k = (\mu - 1/g_k)^+$. The objective is concave and the constraints linear, so these conditions give the global maximum.

(b) The floors are $1/g_1$ = 0.5 and $1/g_2$ = 2. Try channel 1 alone: $p_1$ = 1 puts the water level at μ = 1.5, below channel 2's floor of 2, so channel 2 stays dry: $p_1$ = **1**, $p_2$ = **0**, and $C = \log_2(1 + 2)$ = **1.585** bits per use.

(c) Channel 2 starts to fill when μ reaches its floor, 2: then $p_1 = 2 - 0.5$ = 1.5, so the threshold is $P$ = **1.5**. Above it both channels fill to a common level.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-07.1a | die entropy | 2.585 | bits |
| 17-07.1b | biased coin entropy | 0.469 | bits |
| 17-07.1c | four-symbol entropy | 1.846 | bits |
| 17-07.2a | Huffman average length | 1.9 | bits |
| 17-07.2b | efficiency | 0.972 | — |
| 17-07.3a | Kraft sum, lengths 1, 2, 2, 3 | 1.125 | — |
| 17-07.4a | mutual information | 0.278 | bits |
| 17-07.5a | BEC capacity | 0.8 | bits/use |
| 17-07.5b | BSC capacity | 0.278 | bits/use |
| 17-07.6a | Z-channel capacity | 0.322 | bits/use |
| 17-07.6b | optimal P(X = 1) | 0.4 | — |
| 17-07.7a | 1 MHz at 10 dB | 3.459 | Mb/s |
| 17-07.7b | SNR for 10 b/s/Hz | 30.10 | dB |
| 17-07.8a | minimum bandwidth at 70 dB-Hz | 10 | MHz |
| 17-07.8b | minimum bandwidth at 73 dB-Hz | 3.77 | MHz |
| 17-07.9a | limit at 1.5 b/s/Hz | 0.86 | dB |
| 17-07.9b | QPSK-constrained limit at 1.5 b/s/Hz | 1.63 | dB |
| 17-07.9c | DVB-S2 QPSK 3/4 Eb/N0 | 2.31 | dB |
| 17-07.10a | unlimited-bandwidth capacity | 1.443 | Mb/s |
| 17-07.10b | capacity in 1 MHz | 1.0 | Mb/s |
| 17-07.10c | capacity in 10 MHz | 1.375 | Mb/s |
| 17-07.11a | differential entropy of N(0,1) | 2.047 | bits |
| 17-07.13a | water level | 1.25 | — |
| 17-07.13b | power to channel 1 | 0.75 | — |
| 17-07.13c | power to channel 2 | 0.25 | — |
| 17-07.13d | water-filling capacity | 1.644 | b/s/Hz |
| 17-07.13e | equal-split capacity | 1.245 | b/s/Hz |
| 17-07.14a | Gaussian-input capacity | 0.792 | bits/use |
| 17-07.14b | BPSK soft capacity | 0.721 | bits/use |
| 17-07.14c | BPSK hard capacity | 0.603 | bits/use |
| 17-07.15a | ultimate limit | −1.59 | dB |
| 17-07.15b | DVB-S2 8PSK 2/3 Eb/N0 | 3.65 | dB |
| 17-07.15c | Shannon limit at 1.980636 b/s/Hz | 1.73 | dB |
| 17-07.15d | gap | 1.93 | dB |
| 17-07.16a | power in the stronger channel at P = 1 | 1 | — |
| 17-07.16b | power in the weaker channel at P = 1 | 0 | — |
| 17-07.16c | capacity at P = 1 | 1.585 | bits/use |
| 17-07.16d | total power at which the weaker channel opens | 1.5 | — |
