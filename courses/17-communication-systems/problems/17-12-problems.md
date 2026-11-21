# Problems 17-12 · Multiple Access, Cellular and Wi-Fi Systems

Chapter: [17-12](../chapters/17-12-multiple-access-and-cellular-wifi.md) · Worked solutions: [17-12 solutions](../solutions/17-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Reuse SIR uses six first-tier interferers at the co-channel distance, $\text{SIR} = (\sqrt{3N})^n/6$. Random-access stations transmit in a slot independently with probability τ. Rayleigh users fade independently with unit-mean exponential SNR scaled by their mean. Problems marked *(lab)* can be checked with the lab's `access.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 17-12.1 [A]

**A TDD frame.** A TDD frame spends 10% of its time in guard periods and splits the rest 7:3 between downlink and uplink. What fraction of airtime does each direction get?

### Problem 17-12.2 [A]

**Walsh codes and timing.** Check that the length-4 Walsh codes $[1,1,1,1]$, $[1,-1,1,-1]$, $[1,1,-1,-1]$, $[1,-1,-1,1]$ are mutually orthogonal. Then compute the normalized correlation of $[1,-1,1,-1]$ with itself shifted cyclically by one chip.

### Problem 17-12.3 [B]

**CDMA capacity.** A system spreads 100 kb/s users at 10 Mchip/s and needs $E_b/I_0$ = 5 dB. Find the processing gain in dB and the single-cell capacity, then the capacity with voice-like activity 0.4 and other-cell interference 50% of in-cell.

### Problem 17-12.4 [B]

**Near-far.** With processing gain 128, a weak user is received 20 dB below a strong one and nothing else is present. What is the weak user's SIR after despreading?

### Problem 17-12.5 [B]

**Choosing a cluster.** *(lab)* A system needs 12 dB edge SIR. Find the smallest valid cluster size for path-loss exponents 3, 3.5 and 4.

### Problem 17-12.6 [A]

**Cell splitting.** By what factor does the number of cells (and so, roughly, capacity) per area grow when the cell radius shrinks from 1 km to 300 m?

### Problem 17-12.7 [B]

**Slotted ALOHA with finite users.** Twenty users each transmit in a slot with probability $p$. Find the success probability per slot at the optimal $p = 1/20$ and at $p$ = 0.1.

### Problem 17-12.8 [B]

**Sizing a backoff window.** For 20 contending stations, which window $W$ makes τ = 2/(W + 1) equal to the optimum 1/n? What success probability results?

### Problem 17-12.9 [B]

**Erlang B.** *(lab)* Find the blocking of 5 channels offered 2 Erlangs, and the channels needed to carry 50 Erlangs with at most 1% blocking (give the blocking at that size and one fewer).

### Problem 17-12.10 [B]

**Best of K.** The mean of the largest of $K$ unit exponentials is $\sum_{k=1}^K1/k$. Find the mean SNR gain of the max-SNR scheduler in dB for 4 and for 50 users.

### Problem 17-12.11 [B]

**Starving the edge.** Two Rayleigh users have mean SNRs of 20 dB and 0 dB. Under max-SNR scheduling, what fraction of slots does the weak user win? (For independent exponentials, $P(aX > bY) = a/(a + b)$.)

### Problem 17-12.12 [C]

**HARQ with combining.** Independent attempts that each fail with probability 0.3, up to 4 transmissions: find the throughput and residual error. With combining, the conditional failure probabilities become 0.3, 0.05, 0.01, 0.002: find the expected number of transmissions and the throughput.

### Problem 17-12.13 [B]

**Reuse and trunking together.** *(lab)* An operator has 25 MHz of spectrum in 200 kHz channels and hexagonal cells with path-loss exponent 4. For cluster sizes $N$ = 7 and $N$ = 4: (a) how many channels does each cell get, and what is the first-tier edge SIR? (b) How many Erlangs can each cell carry at 2% blocking? (c) How many subscribers per cell is that, if each makes one 3-minute call in the busy hour? (d) Which would you choose if the modulation needs 15 dB?

### Problem 17-12.14 [B]

**Scheduling a strong and a weak user.** *(lab)* Two users share a channel with Rayleigh fading that is independent from slot to slot, at mean SNRs of 20 dB and 0 dB. (a) Under round robin, find each user's throughput $\tfrac12\mathbb E[\log_2(1 + \bar\gamma X)]$, $X$ ~ Exp(1). (b) A simple stand-in for proportional fair serves whichever user has the larger *normalized* SNR $\gamma_k/\bar\gamma_k$. Show that each user is then served half the time, always when its normalized SNR is the larger of two independent exponentials, and find each user's throughput. (c) Compare with the lab's rate-based proportional-fair simulation and with max-SNR, and explain the weak user's fate under each.

### Problem 17-12.15 [A]

**Where the course lives in a modem.** For each feature of NR or Wi-Fi, name the chapter of this course that explains it and the quantity it trades: (a) LDPC codes on data channels; (b) the choice of 30 kHz subcarrier spacing for a 3.5 GHz macro cell; (c) four receive antennas on a phone; (d) HARQ with soft combining; (e) CSMA/CA with exponential backoff; (f) link adaptation between QPSK and 256-QAM.

---

## Objective coverage

| Learning objective (chapter 17-12) | Problems |
|---|---|
| 1. FDMA/TDMA/CDMA/OFDMA, duplexing | 1, 2, 3, 4 |
| 2. Cellular reuse and SIR | 5, 6, 13 |
| 3. ALOHA and CSMA/CA | 7, 8 |
| 4. Erlang B | 9, 13 |
| 5. Scheduling, multi-user diversity, HARQ | 10, 11, 12, 14 |
| 6. NR and Wi-Fi as applications of the course | 15 |
