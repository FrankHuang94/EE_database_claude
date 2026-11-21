# Lab 17-12 · Sharing the Spectrum

Chapter: [17-12 · Multiple Access, Cellular and Wi-Fi Systems](../../chapters/17-12-multiple-access-and-cellular-wifi.md)

## Objective

Model the multi-user layer of a wireless system and check the chapter's results:

- frequency-reuse geometry and edge SIR;
- ALOHA and slotted-ALOHA throughput against offered load;
- CSMA/CA success and collision probabilities as stations multiply, for two backoff windows;
- Erlang B blocking against a simulated loss system;
- round-robin, max-SNR and proportional-fair scheduling, with Jain's fairness index;
- HARQ throughput and residual error.

## Background

Hexagonal reuse with cluster size $N$ gives edge SIR ≈ $(\sqrt{3N})^n/6$ (§3.3). ALOHA's throughput is $Ge^{-2G}$ and slotted ALOHA's $Ge^{-G}$ (§3.4). With $n$ stations each transmitting with probability τ per slot, a slot succeeds with probability $n\tau(1 - \tau)^{n-1}$ (§3.4). Erlang B gives the blocking of $c$ channels offered $A$ Erlangs (§3.5). A max-SNR scheduler serves the best of $K$ independently fading users (§3.6).

## Files

- `access.py`: `fdma_tdma_users`, `cdma_processing_gain`, `cdma_users`, `reuse_distance_ratio`, `sir_first_tier`, `valid_cluster_sizes`, `aloha`, `slotted_aloha`, `simulate_slotted_aloha`, `simulate_pure_aloha`, `slot_outcomes`, `tau_from_window`, `simulate_slots`, `erlang_b`, `channels_for`, `ergodic_rayleigh`, `max_snr_capacity`, `simulate_schedulers`, `jain`, `harq_throughput`.
- `17-12-access-lab.ipynb`: the guided notebook.

## Procedure

1. **Reuse.** Tabulate the edge SIR for cluster sizes 1 to 12 at path-loss exponents 3, 3.5 and 4; find the smallest cluster that meets 12 dB for each.
2. **ALOHA.** Predict the offered load at which each ALOHA variant peaks; plot analytic throughput and simulate both from $G$ = 0.1 to 3.
3. **CSMA/CA.** For $W$ = 16 and $W$ = 64, predict which window serves 5 stations better and which serves 50 better; simulate slot outcomes.
4. **Erlang B.** Simulate a 10-channel loss system with Poisson arrivals and exponential holding times at 5 and 7 Erlangs; compare blocking with the formula.
5. **Schedulers.** Simulate five users at mean SNRs of 20, 15, 10, 5 and 0 dB under the three schedulers; compare per-user rates, sum rate and Jain's index.
6. **HARQ.** Predict throughput and residual error for $p$ = 0.1 and 0.3 with up to 1, 2 and 4 transmissions; simulate.

## Expected results

- Part 1: SIR grows with $N$ and with $n$; for 12 dB the smallest clusters are 7, 7 and 4.
- Part 2: peaks of 0.184 at $G$ = 0.5 (pure) and 0.368 at $G$ = 1 (slotted); simulation on the curves.
- Part 3: with 5 stations $W$ = 16 is better (success 0.357 against 0.136); with 50 stations $W$ = 64 is far better (0.333 against 0.013).
- Part 4: blocking about 1.8% at 5 Erlangs and 7.9% at 7 Erlangs, matching the formula.
- Part 5: max-SNR gives the highest sum rate but starves the 0 and 5 dB users (Jain's index about 0.3); proportional fair keeps most of the sum rate with a fairness index near 0.8; round robin gives the 20 dB user 1.18 b/s/Hz.
- Part 6: throughput $1 - p$ whatever the number of transmissions; residual error $p^M$.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-12.a | edge SIR, N = 9, n = 3.5 | 17.27 | dB |
| Lab 17-12.b | pure ALOHA throughput at G = 0.25 | 0.152 | — |
| Lab 17-12.c | CSMA success, W = 64, 50 stations | 0.333 | — |
| Lab 17-12.d | blocking, 10 channels, 7 Erl | 7.87 | % |
| Lab 17-12.e | round-robin rate of the 20 dB user | 1.18 | b/s/Hz |

## Discussion

1. Why does the optimal backoff window grow with the number of stations, and how does binary exponential backoff approximate that without knowing the number?
2. Why does max-SNR scheduling starve the weak user almost completely, while proportional fair does not?
3. If HARQ with independent attempts does not raise throughput, why do systems use it?

## Answers

1. The success probability $n\tau(1 - \tau)^{n-1}$ is maximized at τ = $1/n$, so the window (≈ $2/\tau$) should be about $2n$. Collisions become more frequent as $n$ grows, and each collision doubles the colliding stations' windows, so the windows drift upward until collisions become rare: an implicit estimate of $n$.
2. A user whose mean SNR is 20 dB lower almost never has the higher instantaneous SNR ($1/101$ of the time). Proportional fair divides each user's instantaneous rate by its own average, so each user competes against its own history and wins when it is near its own peak.
3. It turns a 10% first-attempt error rate into a $10^{-4}$ residual error, which allows aggressive link adaptation: the higher-rate modulation and coding scheme carries much more per attempt than a conservative one that almost never fails, so overall throughput rises. With combining, retransmissions also succeed more often than independent attempts.

## Optional hardware

Two Wi-Fi adapters in monitor mode can capture the airtime of a busy access point: count collisions (retransmissions), backoff idle time and successful frames, and compare the fractions with the slot model as the number of active clients rises.
