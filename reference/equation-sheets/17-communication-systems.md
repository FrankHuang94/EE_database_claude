# Equation Sheet · 17 Communication Systems

The relations to know cold from Course 17, each with its conditions and the chapter that derives it.

Conventions:

- white noise has two-sided PSD $N_0/2$; $kT_0$ = −174 dBm/Hz; powers and energies of voltage waveforms are into 1 Ω;
- $E_b$, $E_s$ are energies per bit and per symbol; γ is an SNR, $\bar\gamma$ its average per branch in fading; $Q(x) = \tfrac12\operatorname{erfc}(x/\sqrt2)$;
- bandwidths are one-sided at baseband and RF (occupied) around a carrier; α is the raised-cosine roll-off;
- symbol reuse, as in the chapters: $N$ is a noise power, the number of subcarriers or antennas, or a cluster size, as each row says; $L$ is a loss, a number of channel taps or of diversity branches.

## Random processes and PSD

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Mean $m_X(t) = E[X(t)]$; autocorrelation $R_X(t_1, t_2) = E[X(t_1)X(t_2)]$; WSS: constant mean, $R_X$ depends on $\tau = t_1 - t_2$ only | Real processes | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| $R_X(0) = E[X^2]$ = power $\ge \lvert R_X(\tau)\rvert$; $R_X(-\tau) = R_X(\tau)$ | WSS | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| Wiener–Khinchin: $S_X(f) = \int R_X(\tau)e^{-j2\pi f\tau}d\tau \ge 0$; power $= \int S_X\,df$ | A valid $R_X$ must have a nonnegative transform | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| Random-phase sinusoid $A\cos(2\pi f_0t + \Theta)$: $R_X = (A^2/2)\cos 2\pi f_0\tau$, lines of $A^2/4$ at $\pm f_0$ | Θ uniform | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| LTI: $m_Y = H(0)m_X$; $S_Y = \lvert H\rvert^2S_X$; $R_Y = h * h(-\cdot) * R_X$ | WSS input | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| White noise: $S = N_0/2$, $R = (N_0/2)\delta(\tau)$; output power $N_0B_N\lvert H(0)\rvert^2$ with $B_N = \int_0^\infty\lvert H\rvert^2df/\lvert H(0)\rvert^2$ | One-sided $N_0$ | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| One-pole filter: $B_N = (\pi/2)f_{3\text{dB}}$; output $R \propto e^{-\lvert\tau\rvert/RC}$; $\overline{v^2} = kT/C$ for any RC |  | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| Random polar NRZ of amplitude $A$: $S(f) = A^2T\operatorname{sinc}^2(fT)$ | Independent equiprobable bits | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |
| Bandpass noise $n = n_I\cos\omega_ct - n_Q\sin\omega_ct$: $n_I$, $n_Q$ each carry the full bandpass power | Any WSS bandpass noise; uncorrelated at all lags only if the PSD is symmetric about $f_c$ | [17-01](../../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md) |

## Noise and link budgets

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Available noise power $kTB$; $kT_0$ = −174 dBm/Hz at $T_0$ = 290 K; $-174 + 10\log_{10}B$ dBm | $4kTR$ V²/Hz open circuit | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |
| $F = 1 + T_e/T_0$; NF $= 10\log_{10}F$; passive loss $L$ at $T_0$: $F = L$ |  | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |
| Friis cascade: $F = F_1 + (F_2 - 1)/G_1 + (F_3 - 1)/(G_1G_2) + \dots$; $T_e = T_1 + T_2/G_1 + \dots$ | Available gains | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |
| $\text{SNR} = (E_b/N_0)(R_b/B) = (E_s/N_0)(R_s/B)$; $C/N_0 = \text{SNR}\cdot B$ | $B$ = noise bandwidth | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |
| Sensitivity $P_{sens} = -174 + 10\log_{10}B + \text{NF} + \text{SNR}_{req}$ (+ implementation margin) dBm | Antenna at 290 K | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |
| System noise temperature $T_{sys} = T_A + T_e$; $N_0 = kT_{sys}$ |  | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |
| Correlation over $N$ chips (processing gain) raises SNR by $N$; a signal below the noise is detectable if $C/N_0 \cdot T_{int}$ is large | Spread spectrum, GPS | [17-02](../../courses/17-communication-systems/chapters/17-02-noise-and-snr.md) |

## Analog modulation

| Relation | Conditions / notes | Chapter |
|---|---|---|
| DSB-SC and SSB: $\text{SNR}_o = \gamma = S_R/(N_0W)$; AM with envelope detection: $\text{SNR}_o = \eta\gamma$, $\eta = k_a^2P_m/(1 + k_a^2P_m)$ (1/3 for a full tone) | Above threshold | [17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md) |
| Tone FM: $s = A_c\cos(\omega_ct + \beta\sin\omega_mt) = A_c\sum J_n(\beta)\cos(\omega_c + n\omega_m)t$; $\beta = \Delta f/f_m$; carrier nulls at β = 2.405, 5.520 |  | [17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md) |
| Carson: $B_T = 2(\Delta f + W) = 2W(D + 1)$ | About 99% of the power for β ≳ 1 | [17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md) |
| FM: $\text{SNR}_o = 3D^2(P_m/\max m^2)\gamma$; tone: $\tfrac32\beta^2\gamma$ | CNR ≳ 10 dB (threshold) | [17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md) |
| PM: $\text{SNR}_o = k_p^2P_m\gamma$; FM noise PSD is parabolic, PM's flat |  | [17-03](../../courses/17-communication-systems/chapters/17-03-analog-modulation.md) |

## Baseband transmission and ISI

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Nyquist zero-ISI: $\sum_kP(f - k/T) = T$; minimum bandwidth $1/(2T)$ | Sampled at symbol centres | [17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md) |
| Raised cosine: $(1 + \alpha)/(2T)$ at baseband, $(1 + \alpha)/T$ around a carrier; RRC at each end gives RC overall | $0 \le \alpha \le 1$ | [17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md) |
| M-PAM: $\log_2M$ bits per symbol; at equal peak, eye height $1/(M - 1)$ of binary (PAM4: −9.54 dB; −6.99 dB at equal average power) |  | [17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md) |
| One-pole channel: $r = e^{-T/\tau}$, $h_0 = 1 - r$, $h_k = (1 - r)r^k$; worst-case NRZ eye $1 - 2r$; PAM4 $(1 - 4r)/3$ of NRZ's ideal | Sampled at end of symbol | [17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md) |
| Manchester: twice the bandwidth, no DC; 8b/10b 25%, 64b/66b 3.125% overhead |  | [17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md) |
| Zero-forcing equalizer: solve $\sum_kc_kh_{n-k} = \delta_n$ over the taps | Noise enhancement | [17-04](../../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md) |

## Matched filters and detection

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Matched filter $h(t) = ks(T - t)$; peak SNR $2E/N_0$ for any pulse shape | White noise | [17-05](../../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md) |
| RC filter on a rectangular pulse: $\text{SNR}/(2E/N_0) = 2(1 - e^{-x})^2/x$, $x = T/\tau$; best 0.8145 (−0.89 dB) at $x$ = 1.256 |  | [17-05](../../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md) |
| Two signals at distance $d$: $P_e = Q(d/\sqrt{2N_0})$; antipodal $Q(\sqrt{2E_b/N_0})$; orthogonal, and on-off at equal average energy, $Q(\sqrt{E_b/N_0})$ | Equal priors, ML | [17-05](../../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md) |
| MAP threshold for $\pm\sqrt E$: $t = (N_0/(4\sqrt E))\ln(P_-/P_+)$ | Priors $P_\pm$ | [17-05](../../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md) |
| Union bound: $P_e \le \sum_{j\ne i}Q(d_{ij}/\sqrt{2N_0})$; nearest neighbours dominate at high SNR |  | [17-05](../../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md) |
| $Q(x) \approx e^{-x^2/2}/(x\sqrt{2\pi})$ for $x \gtrsim 3$; $Q^{-1}(10^{-5})$ = 4.265, $Q^{-1}(10^{-6})$ = 4.753 |  | [17-05](../../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md) |

## Bandpass modulation

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $s(t) = I(t)\cos\omega_ct - Q(t)\sin\omega_ct = \operatorname{Re}\{\tilde s(t)e^{j\omega_ct}\}$ | Complex envelope $\tilde s = I + jQ$ | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |
| BPSK, Gray QPSK: $P_b = Q(\sqrt{2E_b/N_0})$; QPSK $P_s = 2q - q^2$ with $q = Q(\sqrt{E_s/N_0})$ |  | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |
| M-PSK: $P_s \approx 2Q(\sqrt{2E_s/N_0}\sin(\pi/M))$ | $M \ge 4$ | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |
| Square M-QAM: $p = 2(1 - 1/\sqrt M)Q(\sqrt{3E_s/((M - 1)N_0)})$ per dimension, $P_s = 1 - (1 - p)^2$; Gray $P_b \approx P_s/\log_2M$ |  | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |
| DPSK $\tfrac12e^{-E_b/N_0}$; coherent BFSK $Q(\sqrt{E_b/N_0})$; noncoherent BFSK $\tfrac12e^{-E_b/(2N_0)}$ |  | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |
| Spectral efficiency $\eta = \log_2M/(1 + \alpha)$ b/s/Hz | Raised cosine | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |
| $\text{SNR}_{\text{EVM}} = 1/\text{EVM}^2$; independent impairments add: $1/\text{SNR} = \sum1/\text{SNR}_i$ | Noise-like | [17-06](../../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md) |

## Information theory

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $I(x) = -\log_2p(x)$; $H = -\sum p\log_2p \le \log_2M$; Huffman: $H \le \bar L < H + 1$ | Bits | [17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md) |
| BSC: $C = 1 - h(p)$, $h(p) = -p\log_2p - (1 - p)\log_2(1 - p)$; BEC: $C = 1 - \epsilon$ | Per channel use | [17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md) |
| Shannon–Hartley: $C = B\log_2(1 + S/N)$ | AWGN, complex baseband $B$ = RF bandwidth | [17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md) |
| $E_b/N_0 \ge (2^\eta - 1)/\eta$; η → 0: ln 2 = −1.59 dB; 1.76 dB at η = 2, 5.74 dB at η = 4 |  | [17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md) |
| $C_\infty = S/(N_0\ln2) = 1.443\,S/N_0$ | Infinite bandwidth | [17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md) |
| Water-filling: $P_i = (\mu - N_i/g_i)^+$, $\sum P_i = P$ | Parallel channels | [17-07](../../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md) |

## Channel coding

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $(n, k)$ code: rate $R = k/n$; corrects $t = \lfloor(d_{min} - 1)/2\rfloor$, detects $d_{min} - 1$ |  | [17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md) |
| Hamming: $n = 2^m - 1$, $k = n - m$, $d_{min} = 3$; block error $1 - (1 - p)^n - np(1 - p)^{n-1}$ | Hard decisions | [17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md) |
| CRC of degree $r$: detects all bursts ≤ $r$; random patterns escape ≈ $2^{-r}$ |  | [17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md) |
| RS$(n, k)$ over GF($2^m$): $t = (n - k)/2$ symbols; any burst ≤ $m(t - 1) + 1$ bits |  | [17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md) |
| Asymptotic coding gain: soft $10\log_{10}(Rd_{min})$; hard ≈ $10\log_{10}(R(t + 1))$, about 3 dB less | Equal $E_b/N_0$; coded bits carry $E_c = RE_b$ | [17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md) |
| Convolutional: union bound $P_b \lesssim \sum_dB_dQ(\sqrt{2dRE_b/N_0})$; Viterbi keeps one survivor per state, $2^{K-1}$ states | Soft decisions | [17-08](../../courses/17-communication-systems/chapters/17-08-channel-coding.md) |

## Wireless channels

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Friis: $P_r = P_tG_tG_r(\lambda/4\pi d)^2$; $L_{fs} = 32.45 + 20\log_{10}f_{\text{MHz}} + 20\log_{10}d_{\text{km}}$ dB | Far field | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| Two-ray beyond $d_{BP} = 4h_th_r/\lambda$: $P_r \approx P_tG_tG_rh_t^2h_r^2/d^4$ (40 dB/decade) | Flat ground, reflection −1 | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| Log-distance: $PL(d) = PL(d_0) + 10n\log_{10}(d/d_0) + X_\sigma$; margin $z\sigma$ (1.28σ for 90%) | Shadowing lognormal | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| RMS delay spread $\tau_{rms}$; coherence bandwidth (50%) $0.276/\tau_{rms}$ for an exponential PDP |  | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| Doppler $f_D = vf_c/c$; Clarke correlation $J_0(2\pi f_D\tau)$; $T_c = 1.521/(2\pi f_D) \approx 0.242/f_D$ | 50% correlation | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| Rayleigh: $\lvert h\rvert^2$ exponential; outage $1 - e^{-1/M} \approx 1/M$ for margin $M$ |  | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |
| BPSK in Rayleigh: $\tfrac12(1 - \mu)$, $\mu = \sqrt{\bar\gamma/(1 + \bar\gamma)}$, ≈ $1/(4\bar\gamma)$; $L$-branch MRC exactly $\big(\tfrac{1 - \mu}{2}\big)^L\sum_{k=0}^{L-1}\binom{L - 1 + k}{k}\big(\tfrac{1 + \mu}{2}\big)^k$, ≈ $\binom{2L-1}{L}(4\bar\gamma)^{-L}$ | Per-branch $\bar\gamma$, i.i.d. branches | [17-09](../../courses/17-communication-systems/chapters/17-09-wireless-channels.md) |

## OFDM

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Subcarriers $\Delta f = 1/T$ orthogonal over $T$; IFFT/FFT of size $N$; sample rate $N\Delta f$ |  | [17-10](../../courses/17-communication-systems/chapters/17-10-ofdm.md) |
| CP of $G \ge L - 1$ samples: $Y[k] = H[k]X[k]$; overhead $T_{CP}/(T + T_{CP})$; NR normal CP $144/2048$ = 7.03% of $T$, overhead $144/2192$ = 6.57% | Channel shorter than CP | [17-10](../../courses/17-communication-systems/chapters/17-10-ofdm.md) |
| CFO ICI ≈ $(\pi\varepsilon)^2/3$, ε = offset/spacing; Doppler ICI ≈ $(\pi f_D/\Delta f)^2/6$ | ε ≪ 1 | [17-10](../../courses/17-communication-systems/chapters/17-10-ofdm.md) |
| Design: $T_{CP} > \tau_{max}$ and $f_D \ll \Delta f$; NR $\Delta f = 15 \cdot 2^\mu$ kHz |  | [17-10](../../courses/17-communication-systems/chapters/17-10-ofdm.md) |
| PAPR exceeded with probability $p$: ≈ $\ln(N/p)$ (Gaussian approximation) | Many subcarriers | [17-10](../../courses/17-communication-systems/chapters/17-10-ofdm.md) |

## MIMO and beamforming

| Relation | Conditions / notes | Chapter |
|---|---|---|
| MRC: SNR $= \lVert\mathbf h\rVert^2E_s/N_0$, mean $N\bar\gamma$; selection: mean $\bar\gamma\sum_{k\le N}1/k$; diversity $N$ | i.i.d. branches | [17-11](../../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md) |
| Alamouti 2×1: SNR $= (\lvert h_1\rvert^2 + \lvert h_2\rvert^2)E_s/(2N_0)$: diversity 2, rate 1, 3 dB below 1×2 MRC | No transmit CSI | [17-11](../../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md) |
| ULA array factor $\sum_ne^{jn\pi(\sin\theta - \sin\theta_0)}$ for $d = \lambda/2$; gain $N$; HPBW ≈ $101.5°/N$ at broadside |  | [17-11](../../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md) |
| $C = \log_2\det(\mathbf I + (\rho/N_t)\mathbf H\mathbf H^H) = \sum_i\log_2(1 + \rho\sigma_i^2/N_t)$ | Equal power, no transmit CSI | [17-11](../../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md) |
| ZF: $\mathbf W = (\mathbf H^H\mathbf H)^{-1}\mathbf H^H$, diversity $N_r - N_t + 1$; MMSE: $(\mathbf H^H\mathbf H + (N_t/\rho)\mathbf I)^{-1}\mathbf H^H$ | Linear receivers | [17-11](../../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md) |

## Multiple access and cellular systems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| CDMA processing gain $G_p = R_c/R_b$ |  | [17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md) |
| Hexagonal reuse: $N = i^2 + ij + j^2$, $D/R = \sqrt{3N}$, SIR ≈ $(\sqrt{3N})^n/6$ | Six first-tier interferers | [17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md) |
| Pure ALOHA $S = Ge^{-2G}$ (max $1/2e$); slotted $S = Ge^{-G}$ (max $1/e$) | Poisson load $G$ | [17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md) |
| CSMA/CA slot success $n\tau(1 - \tau)^{n-1}$, best at τ = $1/n$ | $n$ saturated stations | [17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md) |
| Erlang B: $B(c, A) = (A^c/c!)/\sum_{k\le c}A^k/k!$; recursion $B(k) = AB(k - 1)/(k + AB(k - 1))$, $B(0) = 1$; Erlang C (calls wait) $C = cB/(c - A(1 - B))$ | Blocked calls cleared (B), delayed (C, $A < c$) | [17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md) |
| HARQ with independent attempts and at most $M$: throughput $(1 - p^M)/\sum_{k<M}p^k$, which is $1 - p$ for any $M$; mean transmissions $\sum_{k<M}p^k$ ($1/(1 - p)$ unlimited); residual failure $p^M$ |  | [17-12](../../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md) |

## Computer networks

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Wire bytes per Ethernet frame: $8 + 14 + \max(\text{L3}, 46) + 4 + 12$; efficiency = payload / wire bytes | IPv4 20, IPv6 40, TCP 20, UDP 8 bytes | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| IPv4 /p: $2^{32-p} - 2$ usable hosts; longest-prefix match forwards | $p \le 30$ | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| Dijkstra (link state) and Bellman–Ford $d_u = \min_w(c_{uw} + d_w)$ (distance vector; counts to infinity after failures) |  | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| Window limit $W/\text{RTT}$; BDP $= R \cdot \text{RTT}$; window scaling $65\,535 \cdot 2^s$, $s \le 14$ | RFC 7323 | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| Mathis: $R = (\text{MSS}/\text{RTT})\sqrt{3/(2p)}$; slow start doubles per RTT | AIMD with one loss every $1/p$ packets; random loss raises the constant by about 7%, delayed ACKs lower it by $\sqrt2$ | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| RFC 6298: first sample SRTT = $R$, RTTVAR = $R/2$; then RTTVAR ← ¾ RTTVAR + ¼ $\lvert\text{SRTT} - R\rvert$ and SRTT ← ⅞ SRTT + ⅛ $R$; RTO = SRTT + max($G$, 4 RTTVAR), at least 1 s; doubles on each timeout | $G$ = clock granularity | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| M/M/1: $T = 1/(\mu - \lambda)$; Little's law $N = \lambda T$ | Poisson arrivals, exponential service | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
| Brute force: half of $2^k$ keys on average; birthday collision after ≈ $\sqrt{2\ln2}\sqrt{2^b} = 1.177\sqrt{2^b}$ hashes | 50% collision probability | [17-13](../../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md) |
