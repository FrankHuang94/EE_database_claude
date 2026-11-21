<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 17 · Communication Systems

How information moves over noisy channels: random processes and noise, analog and digital modulation, matched filtering and BER, information theory and Shannon capacity, channel coding, wireless channels, OFDM, MIMO and multiple access, how 4G/5G and Wi-Fi apply them, and the computer-networking layer above.

| | |
|---|---|
| **Term** | 5 |
| **Study hours** | ≈ 103 |
| **University equivalents** | Communication Systems / Digital Communications (senior); MIT 6.450; Berkeley EE121 |
| **Textbook alignment** | Lathi & Ding, *Modern Digital and Analog Communication Systems*; Proakis & Salehi, *Communication Systems Engineering*; Tse & Viswanath, *Fundamentals of Wireless Communication* (free online); Kurose & Ross, *Computer Networking: A Top-Down Approach* (networking chapter) |
| **Free courses** | MIT OCW 6.450 Principles of Digital Communication I; MIT OCW 6.02 Introduction to EECS II: Digital Communication Systems |
| **Prerequisites** | [03 · Probability, Statistics and Random Variables for EE](../03-probability-statistics-and-random-variables/README.md), [11 · Signals and Systems](../11-signals-and-systems/README.md) |
| **FE areas** | Communications, Computer Networks |
| **Deeper** | Companion repo(s): datacenter networking |

## Learning objectives

1. Characterize random processes by autocorrelation and PSD and compute noise power and SNR through systems.
2. Analyze baseband and bandpass digital modulation (PAM, PSK, QAM) including pulse shaping and ISI.
3. Derive the matched filter and compute bit-error rates in AWGN.
4. Apply Shannon capacity and explain how channel codes approach it.
5. Explain OFDM, MIMO and multiple-access schemes and map them onto 4G/5G and Wi-Fi.
6. Describe layered network models, addressing and routing at FE level.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [17-01 · Random Processes and Power Spectral Density](chapters/17-01-random-processes-and-psd.md) | 9 | ✅ verified | [problems](problems/17-01-problems.md) · [solutions](solutions/17-01-solutions.md) · [lab](labs/17-01-lab/README.md) · [verify](verify/verify_17_01.py) |
| [17-02 · Noise and SNR in Communication Systems](chapters/17-02-noise-and-snr.md) | 6 | ✅ verified | [problems](problems/17-02-problems.md) · [solutions](solutions/17-02-solutions.md) · [lab](labs/17-02-lab/README.md) · [verify](verify/verify_17_02.py) |
| [17-03 · Analog Modulation (Brief)](chapters/17-03-analog-modulation.md) | 5 | ✅ verified | [problems](problems/17-03-problems.md) · [solutions](solutions/17-03-solutions.md) · [lab](labs/17-03-lab/README.md) · [verify](verify/verify_17_03.py) |
| [17-04 · Baseband Digital Transmission](chapters/17-04-baseband-digital-transmission.md) | 8 | ✅ verified | [problems](problems/17-04-problems.md) · [solutions](solutions/17-04-solutions.md) · [lab](labs/17-04-lab/README.md) · [verify](verify/verify_17_04.py) |
| [17-05 · Matched Filters and Optimal Detection](chapters/17-05-matched-filters-and-detection.md) | 8 | ✅ verified | [problems](problems/17-05-problems.md) · [solutions](solutions/17-05-solutions.md) · [lab](labs/17-05-lab/README.md) · [verify](verify/verify_17_05.py) |
| [17-06 · Bandpass Digital Modulation and BER](chapters/17-06-bandpass-digital-modulation.md) | 10 | ✅ verified | [problems](problems/17-06-problems.md) · [solutions](solutions/17-06-solutions.md) · [lab](labs/17-06-lab/README.md) · [verify](verify/verify_17_06.py) |
| [17-07 · Information Theory and Shannon Capacity](chapters/17-07-information-theory-and-shannon.md) | 8 | ✅ verified | [problems](problems/17-07-problems.md) · [solutions](solutions/17-07-solutions.md) · [lab](labs/17-07-lab/README.md) · [verify](verify/verify_17_07.py) |
| [17-08 · Channel Coding](chapters/17-08-channel-coding.md) | 9 | ✅ verified | [problems](problems/17-08-problems.md) · [solutions](solutions/17-08-solutions.md) · [lab](labs/17-08-lab/README.md) · [verify](verify/verify_17_08.py) |
| [17-09 · Wireless Channels: Fading and Multipath](chapters/17-09-wireless-channels.md) | 6 | ✅ verified | [problems](problems/17-09-problems.md) · [solutions](solutions/17-09-solutions.md) · [lab](labs/17-09-lab/README.md) · [verify](verify/verify_17_09.py) |
| [17-10 · OFDM](chapters/17-10-ofdm.md) | 7 | ✅ verified | [problems](problems/17-10-problems.md) · [solutions](solutions/17-10-solutions.md) · [lab](labs/17-10-lab/README.md) · [verify](verify/verify_17_10.py) |
| [17-11 · MIMO and Beamforming Basics](chapters/17-11-mimo-and-beamforming.md) | 6 | ✅ verified | [problems](problems/17-11-problems.md) · [solutions](solutions/17-11-solutions.md) · [lab](labs/17-11-lab/README.md) · [verify](verify/verify_17_11.py) |
| [17-12 · Multiple Access, Cellular and Wi-Fi Systems](chapters/17-12-multiple-access-and-cellular-wifi.md) | 8 | ✅ verified | [problems](problems/17-12-problems.md) · [solutions](solutions/17-12-solutions.md) · [lab](labs/17-12-lab/README.md) · [verify](verify/verify_17_12.py) |
| [17-13 · Computer Networks Fundamentals](chapters/17-13-computer-networks-fundamentals.md) | 8 | ✅ verified | [problems](problems/17-13-problems.md) · [solutions](solutions/17-13-solutions.md) · [lab](labs/17-13-lab/README.md) · [verify](verify/verify_17_13.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/17-communication-systems.csv) · [Equation sheet](../../reference/equation-sheets/17-communication-systems.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 17 is planned at about 103 hours: the chapters' own estimates add to 98, plus 5 hours of review and the exam. Course 03 gave you random variables, Course 11 the Fourier transform and Course 16 the DFT and filters. This course uses them to answer one question in every form it takes: how many bits per second can cross a noisy, bandwidth-limited, fading channel, and at what cost in power, bandwidth, antennas and silicon? Every link budget, modem data sheet, Wi-Fi or 5G rate claim, SerDes eye and network throughput figure in a semiconductor portfolio is an answer to that question.

The thirteen chapters fall into five blocks:

- **Noise (17-01 to 17-02).** Random processes, autocorrelation and PSD through LTI systems; then thermal noise, noise figure, Friis cascades, $E_b/N_0$ and receiver sensitivity from −174 dBm/Hz.
- **Modulation and detection (17-03 to 17-06).** Analog AM and FM with their noise performance; baseband PAM, ISI, the Nyquist criterion and PAM4 against NRZ; the matched filter, signal space and ML/MAP detection; bandpass PSK, QAM and FSK with their error rates, spectral efficiency and EVM.
- **Limits and codes (17-07 to 17-08).** Entropy, channel capacity, Shannon–Hartley and the −1.59 dB limit; block codes, CRCs, Reed–Solomon, convolutional codes with Viterbi decoding, LDPC and polar codes, and coding gain.
- **Wireless systems (17-09 to 17-12).** Path loss, shadowing, delay spread, Doppler and Rayleigh fading; OFDM with the cyclic prefix and NR numerology; diversity, beamforming and MIMO capacity; multiple access, cellular reuse, ALOHA, CSMA/CA, Erlang B, scheduling and HARQ.
- **Networks (17-13).** Layering and headers, IPv4 addressing, routing, TCP windows and congestion control, queueing and the arithmetic of network security.

Work at least the [A] and [B] problems of every chapter. Each lab ships one module, imported by its own notebook and verify script:

- `randproc.py` (17-01) and `noisebudget.py` (17-02) generate and filter noise processes and compute cascades and sensitivities; `analogmod.py` (17-03) builds AM and FM signals and simulates their detectors;
- `baseband.py` (17-04), `detection.py` (17-05) and `modulation.py` (17-06) cover pulses, eyes and equalizers, matched filters and decision rules, and every constellation with Monte Carlo error rates and EVM;
- `infotheory.py` (17-07) and `coding.py` (17-08) compute entropies and capacities and implement Hamming, CRC, convolutional, LDPC and polar coding with their decoders;
- `channels.py` (17-09), `ofdm.py` (17-10), `mimo.py` (17-11) and `access.py` (17-12) simulate fading channels, a complete OFDM link, combining and MIMO detection, and random access and traffic;
- `netlab.py` (17-13) covers subnetting, routing, TCP's window and loss limits, queues and a firewall;
- three ngspice netlists confirm the circuit results: resistor noise in an RLC tank (17-01), a matched pad's noise (17-02) and the pulse response of an RC channel (17-04).

The verify scripts recompute the chapters' numbers, mostly by a route independent of the lab code (numerical integration, simulation, exhaustive enumeration), and check prose claims as well as answer keys, so a mismatch in your own work usually means a wrong method, not rounding.

**What to master cold.** The [equation sheet](../../reference/equation-sheets/17-communication-systems.md) collects the relations; these are the ideas behind them:

- noise is a power density: $kT_0$ = −174 dBm/Hz, every hertz you let in adds noise, and the first stage's noise figure dominates the cascade (17-01, 17-02);
- sensitivity is a sum in decibels: −174 + 10 log₁₀ B + NF + required SNR; every rate, range and battery claim can be checked with it (17-02, 17-09);
- the matched filter makes the detection SNR $2E/N_0$ whatever the pulse shape, so error rates depend only on energy and on distances between signals (17-05);
- each extra bit per symbol costs about 3 dB (PSK more, QAM less), and coding buys some of it back; Shannon's $(2^\eta - 1)/\eta$ is the floor no design crosses (17-06 to 17-08);
- bandwidth is not free either: Nyquist's $1/(2T)$ plus roll-off, Carson's $2(\Delta f + W)$, and PAM4's 9.5 dB penalty for halving it (17-03, 17-04);
- fading turns exponential error curves into $1/\bar\gamma$ ones, and diversity of order $L$ restores $\bar\gamma^{-L}$: antennas, frequency and time are bought for diversity first (17-09, 17-11);
- OFDM converts a frequency-selective channel into many flat ones at the price of a cyclic prefix, sensitivity to frequency offset and a high peak-to-average ratio (17-10);
- MIMO capacity grows with the number of strong eigenmodes, not with the antenna count as such (17-11);
- shared channels lose to collisions and are sized by traffic statistics: ALOHA's $1/e$, Erlang B, reuse SIR (17-12);
- end to end, throughput is the minimum of the link rate, window/RTT and the loss limit, and delay explodes as load approaches capacity (17-13).

**Assessment.** The [course final exam](exam/README.md) has 14 questions and takes 240 minutes, with a calculator and the equation sheet but no Python or simulator. Aim for at least 70%. Questions 1 to 9 follow the chapters from random processes to fading; Question 10 combines OFDM and MIMO, Question 11 covers multiple access and Question 12 networks. Question 12 adds a Dijkstra routing problem to the TCP arithmetic. Question 13 asks for three derivations (the matched filter, the Shannon limit, the cyclic prefix's one-tap equalization). Question 14 is a diligence question about an IoT radio start-up's rate, sensitivity and range claims, partly graded against a rubric. The course maps onto the FE Electrical and Computer exam's Communications area (5–8 questions) and Computer Networks area (4–6 questions) ([R-001](../../reference/research-log.md#r-001--ncees-fe-electrical-and-computer-specification), [R-295](../../reference/research-log.md#r-295--ncees-fe-electrical-and-computer-computer-networks-topics)). The [flashcards](../../flashcards/17-communication-systems.csv) (102 cards) are for spaced review alongside the chapters.

**Deeper:** see companion repo *Datacenter Networking* for RDMA, lossless Ethernet, congestion control in AI fabrics and switch silicon architecture, which build on 17-04, 17-08 and 17-13.
