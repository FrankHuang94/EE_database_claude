# Solutions 17-11 · MIMO and Beamforming Basics

Problems: [17-11 problems](../problems/17-11-problems.md) · Chapter: [17-11](../chapters/17-11-mimo-and-beamforming.md). Every number below is recomputed by [verify_17_11.py](../verify/verify_17_11.py).

---

## Solutions

### Solution 17-11.1

(a) **Array gain only**: coherent addition doubles the SNR, but both antennas fade together, so the error-rate slope is unchanged. (b) **Diversity** (order $N$) with a smaller array gain than MRC. (c) **Diversity** of order 2 with no array gain: the power split costs 3 dB, cancelling the coherent-combining gain, so the mean SNR equals SISO's. (d) **Multiplexing** gain (up to 4), plus diversity and array gain on each stream depending on the receiver.

### Solution 17-11.2

EGC: $(1 + 0.5)^2/2$ = **1.125**. MRC: $1 + 0.25$ = **1.25**. EGC loses $10\log_{10}(1.25/1.125)$ = 0.46 dB here because it gives the weak branch as much weight as the strong one.

### Solution 17-11.3

$\sum_{k=1}^3 1/k$ = **1.833**; $\sum_{k=1}^8 1/k$ = **2.718**, against MRC's 8: a shortfall of $10\log_{10}(8/2.718)$ = **4.69** dB. Selection keeps the diversity but wastes most of the array gain.

### Solution 17-11.4

$1 - e^{-0.1}(1 + 0.1 + 0.005)$ = **1.55e-4**; approximation $0.1^3/6$ = **1.67e-4** (8% high); selection $(1 - e^{-0.1})^3$ = **8.62e-4**, about 5.6 times worse: the same slope, a $1/3!$ versus $(0.0952/0.1)^3$ difference in the constant.

### Solution 17-11.5

Solving $\bar P_b = 10^{-6}$ with the MRC formula: 1 branch **53.98** dB, 2 branches **26.36** dB, 4 branches **12.63** dB. The first extra antenna saves 27.6 dB; the next two save 13.7 dB more. AWGN would need 10.53 dB.

### Solution 17-11.6

Gain $10\log_{10}16$ = **12.04** dB; beamwidth **6.36**° at broadside; first null $\arcsin(1/8)$ = **7.18**°; grating-free spacing at 45°: $1/(1 + \sin45°)$ = **0.586** λ.

### Solution 17-11.7

Each array adds $10\log_{10}64$ = 18.06 dB, 36.1 dB in total. Free-space received power falls as $1/d^2$, so range scales by $10^{36.1/20}$ = **64**: equal to the element count, because the two $\sqrt{64}$ factors multiply.

### Solution 17-11.8

$\mathbf H\mathbf H^H = \begin{bmatrix}2 & 2\\2 & 2\end{bmatrix}$ has eigenvalues 4 and 0: singular values **2** and **0** (rank 1). Capacity $\log_2(1 + 50 \times 4)$ = **7.65** b/s/Hz. With $\mathbf H = \mathbf I_2$: $2\log_2(1 + 50)$ = **11.34** b/s/Hz. The LOS channel delivers array gain (the single mode has gain 4) but only one stream.

### Solution 17-11.9

Equal power (0.5 each): $\log_2(1.5) + \log_2(1 + 0.045)$ = **0.648** b/s/Hz. Water-filling: floors $1/1$ and $1/0.09$ = 11.1; with total power 1 the level stays below the second floor, so all power goes to the strong mode: $\log_2 2$ = **1.0** b/s/Hz, 54% more. At low SNR, beamforming on the strongest eigenmode beats spreading power.

### Solution 17-11.10

Singular values **1.9** and **0.1**; condition number **19**. $(\mathbf H^H\mathbf H)^{-1}$ has diagonal entries $(1 + 0.81)/(0.19)^2 = 50.1$, so each ZF stream's SNR is $50/50.1$ = **−0.01** dB. ZF sum rate $2\log_2(1 + 0.998)$ = **2.00** b/s/Hz; capacity $\log_2(1 + 50 \times 3.61) + \log_2(1 + 50 \times 0.01)$ = **8.09** b/s/Hz. Alone, a stream would be received by MRC on its own column with SNR $(\rho/N_t)\|\mathbf h_k\|^2 = 50 \times 1.81$ = **19.57** dB: ZF gives up almost 20 dB per stream to cancel the other. MMSE does better on this ill-conditioned channel: $(\mathbf I + 50\mathbf H^H\mathbf H)^{-1}$ has diagonal entries 0.336, so each stream's SINR is $1/0.336 - 1 = 1.975$, **2.96** dB, and the sum rate is $2\log_2(2.975)$ = **3.15** b/s/Hz: it accepts some interference instead of amplifying noise. MMSE-SIC or ML detection recovers most of the remaining gap to capacity.

### Solution 17-11.11

$2\int\log_2(1 + \rho\lambda/2)p(\lambda)d\lambda$: at 10 dB **5.55** b/s/Hz; at 30 dB **17.74** b/s/Hz. From 20 to 30 dB it rises by **6.45** b/s/Hz, close to $2 \times 3.32$; SISO rises by **3.26** b/s/Hz. Ten decibels buy about $\log_210$ = 3.3 b/s/Hz per eigenmode at high SNR, so about 6.6 with two eigenmodes; the 2×2 gain of 6.45 is already close to that.

### Solution 17-11.12

Uplink: $10^{-6} \times 2 \times 8 \times 0.9258 \times (273 \times 12 \times 28\,000) \times 0.92$ = **1250** Mb/s. FR2 downlink: $T_s = 10^{-3}/112$; $10^{-6} \times 2 \times 6 \times 0.9258 \times (264 \times 12 \times 112\,000) \times 0.82$ = **3232** Mb/s: four times the bandwidth more than compensates for the lower modulation order and higher overhead.

### Solution 17-11.13

$1/\sqrt{100}$ = **0.1**: the beamformed gain varies by only about ±10%, so the scheduler can assign rates from the average channel without tracking fast fading, one of massive MIMO's practical advantages.

### Solution 17-11.14

MRC at 20 dB: **1.84e-5**. Alamouti (MRC formula at half the SNR, 17 dB): **7.26e-5**. To match 1.84e-5, Alamouti needs 3 dB more: **23.01** dB.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-11.2a | EGC gain | 1.125 | — |
| 17-11.2b | MRC gain | 1.25 | — |
| 17-11.3a | SC mean gain, 3 branches | 1.833 | — |
| 17-11.3b | SC mean gain, 8 branches | 2.718 | — |
| 17-11.3c | shortfall against MRC, 8 branches | 4.69 | dB |
| 17-11.4a | MRC3 outage | 1.55e-4 | — |
| 17-11.4b | approximation | 1.67e-4 | — |
| 17-11.4c | SC3 outage | 8.62e-4 | — |
| 17-11.5a | 1 branch at 1e-6 | 53.98 | dB |
| 17-11.5b | 2 branches at 1e-6 | 26.36 | dB |
| 17-11.5c | 4 branches at 1e-6 | 12.63 | dB |
| 17-11.6a | 16-element gain | 12.04 | dB |
| 17-11.6b | broadside beamwidth | 6.36 | ° |
| 17-11.6c | first null | 7.18 | ° |
| 17-11.6d | grating-free spacing at 45° | 0.586 | λ |
| 17-11.7a | range factor | 64 | — |
| 17-11.8a | largest singular value | 2 | — |
| 17-11.8b | smallest singular value | 0 | — |
| 17-11.8c | LOS capacity | 7.65 | b/s/Hz |
| 17-11.8d | identity-channel capacity | 11.34 | b/s/Hz |
| 17-11.9a | equal-power capacity | 0.648 | b/s/Hz |
| 17-11.9b | water-filling capacity | 1.0 | b/s/Hz |
| 17-11.10a | largest singular value | 1.9 | — |
| 17-11.10b | smallest singular value | 0.1 | — |
| 17-11.10c | condition number | 19 | — |
| 17-11.10d | ZF stream SNR | −0.01 | dB |
| 17-11.10e | ZF sum rate | 2.00 | b/s/Hz |
| 17-11.10f | capacity | 8.09 | b/s/Hz |
| 17-11.10g | single-stream MRC SNR | 19.57 | dB |
| 17-11.10h | MMSE stream SINR | 2.96 | dB |
| 17-11.10i | MMSE sum rate | 3.15 | b/s/Hz |
| 17-11.11a | 2×2 ergodic at 10 dB | 5.55 | b/s/Hz |
| 17-11.11b | 2×2 ergodic at 30 dB | 17.74 | b/s/Hz |
| 17-11.11c | 2×2 increase, 20 → 30 dB | 6.45 | b/s/Hz |
| 17-11.11d | SISO increase, 20 → 30 dB | 3.26 | b/s/Hz |
| 17-11.12a | NR uplink, 2 layers | 1250 | Mb/s |
| 17-11.12b | NR FR2 downlink, 2 layers | 3232 | Mb/s |
| 17-11.13a | hardening spread, M = 100 | 0.1 | — |
| 17-11.14a | MRC BER at 20 dB | 1.84e-5 | — |
| 17-11.14b | Alamouti BER at 20 dB | 7.26e-5 | — |
| 17-11.14c | Alamouti SNR to match | 23.01 | dB |
| 17-11.5x | saving of the second antenna | 27.6 | dB |
| 17-11.5y | further saving with four antennas | 13.7 | dB |
| 17-11.5z | AWGN requirement at 1e-6 | 10.53 | dB |
| 17-11.2x | EGC loss against MRC | 0.46 | dB |
| 17-11.9x | water-filling gain over equal power | 54 | % |
