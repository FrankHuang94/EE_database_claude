# Solutions 17-12 · Multiple Access, Cellular and Wi-Fi Systems

Problems: [17-12 problems](../problems/17-12-problems.md) · Chapter: [17-12](../chapters/17-12-multiple-access-and-cellular-wifi.md). Every number below is recomputed by [verify_17_12.py](../verify/verify_17_12.py).

---

## Solutions

### Solution 17-12.1

Usable time 0.9: downlink $0.9 \times 0.7$ = **0.63**, uplink $0.9 \times 0.3$ = **0.27** of airtime.

### Solution 17-12.2

Every pair's chip-by-chip product sums to zero (e.g. $[1,-1,1,-1]\cdot[1,1,-1,-1] = 1 - 1 - 1 + 1 = 0$). Shifting $[1,-1,1,-1]$ by one chip gives $[-1,1,-1,1]$, whose correlation with the original is $-4/4$ = **−1**: a one-chip timing error inverts this user's own despread output. It can also destroy orthogonality with other users: shifting $[1,1,-1,-1]$ by one chip gives $[-1,1,1,-1] = -[1,-1,-1,1]$, fully correlated with another user's code. That is why Walsh codes need chip-level synchronization.

### Solution 17-12.3

$G_p = 10^7/10^5 = 100$, **20** dB. $N = 1 + 100/3.162$ = **32.6** users. With activity 0.4 and $f$ = 0.5: $N = 1 + 100/(3.162 \times 0.4 \times 1.5)$ = **53.7** users.

### Solution 17-12.4

Despreading raises the weak user by 128 relative to the strong user's spread power: SIR $= 128 \times 10^{-2}$ = 1.28, **1.07** dB, barely usable. Power control, which would make both arrive equally, restores 21.07 dB.

### Solution 17-12.5

SIRs for clusters 3, 4, 7: $n$ = 3: 6.53, 8.41, 12.05 dB → **7**; $n$ = 3.5: 8.92, 11.10, 15.36 dB → **7**; $n$ = 4: 11.30, 13.80 dB → **4**. A steeper path loss lets the same SIR be reached with tighter reuse.

### Solution 17-12.6

Cells per area ∝ $1/R^2$: $(1/0.3)^2$ = **11.1**.

### Solution 17-12.7

$20p(1 - p)^{19}$: at $p$ = 0.05, **0.377**; at $p$ = 0.1, **0.270**. Doubling the attempt rate above the optimum loses 28% of the throughput.

### Solution 17-12.8

$2/(W + 1) = 1/20$ gives $W$ = **39**, and the success probability is $20 \times 0.05 \times 0.95^{19}$ = **0.377**, near $1/e$.

### Solution 17-12.9

$B(5, 2)$ = **3.67** %. For 50 Erlangs: $B(63, 50)$ = 1.09% and $B(64, 50)$ = **0.84** %, so **64** channels (occupancy $50 \times 0.992/64$ = 77%).

### Solution 17-12.10

$K$ = 4: $1 + \tfrac12 + \tfrac13 + \tfrac14$ = 2.083, **3.19** dB. $K$ = 50: 4.499, **6.53** dB. The gain grows like $\ln K$.

### Solution 17-12.11

The weak user wins when $1 \cdot X_w > 100 \cdot X_s$: probability $1/(1 + 100)$ = **0.0099**. Under max-SNR it is served in fewer than 1% of slots; proportional fair compares each user with its own average and serves it about half the time.

### Solution 17-12.12

Independent: throughput **0.7**, residual $0.3^4$ = **0.0081**. With combining, the probabilities of still failing after 1, 2, 3 transmissions are 0.3, 0.015, 0.00015, so the expected number of transmissions is $1 + 0.3 + 0.015 + 0.00015$ = **1.315** and the throughput $(1 - 3 \times 10^{-7})/1.315$ = **0.760**.

### Solution 17-12.13

(a) 25 MHz / 200 kHz = 125 channels. $N$ = 7: $\lfloor125/7\rfloor$ = **17** channels per cell, SIR $(\sqrt{21})^4/6 = 441/6 = 73.5$, **18.66** dB. $N$ = 4: **31** channels, SIR $144/6 = 24$, **13.80** dB.

(b) Solving $B(c, A) = 0.02$ with the Erlang B recursion: **10.66** Erlangs for 17 channels and **22.83** Erlangs for 31.

(c) Each subscriber offers $3/60$ = 0.05 Erlang, so **213** and **456** subscribers per cell.

(d) $N$ = 4 carries 2.1 times the traffic per cell but its 13.8 dB edge SIR misses the 15 dB requirement; $N$ = 7 meets it. Choose $N$ = 7 or, to keep $N$ = 4, add three-sector antennas (+4.8 dB, 18.6 dB) at the cost of splitting each cell's channels among sectors. Smaller clusters gain twice: more channels per cell and better trunking efficiency on the larger pool.

### Solution 17-12.14

(a) With $X$ exponential, $\mathbb E[\log_2(1 + \bar\gamma X)] = \int_0^\infty\log_2(1 + \bar\gamma x)e^{-x}dx$ = 5.88 b/s/Hz at 20 dB and 0.860 at 0 dB. Round robin halves each: **2.94** and **0.430** b/s/Hz.

(b) The normalized SNRs $X_1 = \gamma_1/\bar\gamma_1$ and $X_2 = \gamma_2/\bar\gamma_2$ are independent Exp(1) variables, so by symmetry each is the larger half the time, whatever the means. When user $k$ is served its $X_k$ is the maximum of two exponentials, whose density is $2e^{-x}(1 - e^{-x})$. Its throughput is

$$
R_k = \tfrac12\int_0^\infty\log_2(1 + \bar\gamma_kx)\,2e^{-x}(1 - e^{-x})\,dx ,
$$

giving **3.42** b/s/Hz for the strong user and **0.600** for the weak one: both gain over round robin (16% and 40%) because each is served near its own peaks, and the weak user gains proportionally more.

(c) The lab's rate-based proportional fair gives about 3.69 and 0.58 b/s/Hz: close, with the strong user served somewhat more than half the time because the metric compares rates, not SNRs. Max-SNR serves the 0 dB user only when its SNR beats the 20 dB user's, which almost never happens: about 5.88 and 0.01 b/s/Hz, the largest sum rate and complete starvation of the weak user.

### Solution 17-12.15

- (a) **17-08** (channel coding): LDPC codes approach capacity at long block lengths with parallel decoders; the trade is decoder area, power and latency against the dB of coding gain.
- (b) **17-10** (OFDM) with 17-09: the 2.34 μs prefix must cover the macro cell's delay spread, while the 30 kHz spacing keeps Doppler ICI negligible; the trade is prefix overhead against delay-spread and Doppler tolerance.
- (c) **17-11** (MIMO): receive diversity and up to four layers of spatial multiplexing; the trade is antennas, RF chains and power against capacity and reliability.
- (d) **17-12** with 17-08: retransmissions combined with earlier copies raise the effective SNR; the trade is latency and buffer memory against throughput at a given block error rate.
- (e) **17-12** (random access): the backoff window trades idle slots against collisions as the number of contenders changes.
- (f) **17-06** (bandpass modulation) and 17-07 (capacity): each extra two bits per symbol costs about 6 dB of SNR; link adaptation chooses the most bits the current SNR supports.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-12.1a | downlink share | 0.63 | — |
| 17-12.1b | uplink share | 0.27 | — |
| 17-12.2a | shifted correlation | −1 | — |
| 17-12.3a | processing gain | 20 | dB |
| 17-12.3b | single-cell users | 32.6 | — |
| 17-12.3c | users with activity and other-cell interference | 53.7 | — |
| 17-12.4a | weak-user SIR | 1.07 | dB |
| 17-12.5a | cluster for n = 3 | 7 | — |
| 17-12.5b | cluster for n = 3.5 | 7 | — |
| 17-12.5c | cluster for n = 4 | 4 | — |
| 17-12.6a | cells per area factor | 11.1 | — |
| 17-12.7a | success at p = 0.05 | 0.377 | — |
| 17-12.7b | success at p = 0.1 | 0.270 | — |
| 17-12.8a | window | 39 | slots |
| 17-12.8b | success | 0.377 | — |
| 17-12.9a | blocking, 5 channels, 2 Erl | 3.67 | % |
| 17-12.9b | blocking at 64 channels, 50 Erl | 0.84 | % |
| 17-12.9c | channels for 50 Erl at 1% | 64 | — |
| 17-12.10a | gain, 4 users | 3.19 | dB |
| 17-12.10b | gain, 50 users | 6.53 | dB |
| 17-12.11a | weak user's share | 0.0099 | — |
| 17-12.12a | independent throughput | 0.7 | — |
| 17-12.12b | independent residual error | 0.0081 | — |
| 17-12.12c | expected transmissions with combining | 1.315 | — |
| 17-12.12d | throughput with combining | 0.760 | — |
| 17-12.13a | channels per cell, N = 7 | 17 | — |
| 17-12.13b | SIR, N = 7 | 18.66 | dB |
| 17-12.13c | channels per cell, N = 4 | 31 | — |
| 17-12.13d | SIR, N = 4 | 13.80 | dB |
| 17-12.13e | Erlangs at 2%, 17 channels | 10.66 | E |
| 17-12.13f | Erlangs at 2%, 31 channels | 22.83 | E |
| 17-12.13g | subscribers per cell, N = 7 | 213 | — |
| 17-12.13h | subscribers per cell, N = 4 | 456 | — |
| 17-12.14a | round robin, strong user | 2.94 | b/s/Hz |
| 17-12.14b | round robin, weak user | 0.430 | b/s/Hz |
| 17-12.14c | normalized-SNR scheduler, strong user | 3.42 | b/s/Hz |
| 17-12.14d | normalized-SNR scheduler, weak user | 0.600 | b/s/Hz |
| 17-12.4x | power-control restoration | 21.07 | dB |
| 17-12.7x | throughput lost beyond the optimum | 28 | % |
