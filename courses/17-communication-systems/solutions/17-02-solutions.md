# Solutions 17-02 · Noise and SNR in Communication Systems

Problems: [17-02 problems](../problems/17-02-problems.md) · Chapter: [17-02](../chapters/17-02-noise-and-snr.md). Every number below is recomputed by [verify_17_02.py](../verify/verify_17_02.py): decibel arithmetic from the constants, cascades both by the Friis formula and by a stage-by-stage noise-temperature recursion, noise bandwidths by numerical integration, and the simulation-scaling and correlation results by Monte Carlo.

---

## Solutions

### Solution 17-02.1

$kT_0 = 4.004 \times 10^{-21}$ W/Hz = −173.975 dBm/Hz. Adding $10\log_{10}B$ (carry the third decimal, then round):

- 1 Hz: **−173.98** dBm.
- 200 kHz: $-173.975 + 53.010$ = **−120.96** dBm.
- 20 MHz: $-173.975 + 73.010$ = **−100.96** dBm.
- 400 MHz: $-173.975 + 86.021$ = **−87.95** dBm.

The open-circuit voltage is $\sqrt{4kT_0RB} = \sqrt{4 \times 4.004 \times 10^{-21} \times 50 \times 4 \times 10^8} = \sqrt{3.203 \times 10^{-10}}$ = **17.9** µV rms. Units: $\sqrt{\text{W/Hz}\cdot\Omega\cdot\text{Hz}} = \sqrt{\text{W}\cdot\Omega}$ = V.

### Solution 17-02.2

$T_e = (10^{\text{NF}/10} - 1) \times 290$:

- 0.5 dB: $(1.1220 - 1) \times 290$ = **35.4** K.
- 2 dB: $(1.5849 - 1) \times 290$ = **169.6** K.
- 10 dB: $9 \times 290$ = **2610** K.

$\text{NF} = 10\log_{10}(1 + T_e/290)$: 35 K gives $10\log_{10}(1.1207)$ = **0.49** dB, and 150 K gives $10\log_{10}(1.5172)$ = **1.81** dB. Near 0 dB the relation is nearly linear, about 67 K per dB; at high noise figures the temperature grows exponentially.

### Solution 17-02.3

A matched passive component at physical temperature $T_p$ has $T_e = (L - 1)T_p$ and $F = 1 + (L - 1)T_p/T_0$ (chapter §3.4).

- At 290 K, $F = L$: **3.00** dB.
- At 77 K: $T_e = (1.9953 - 1) \times 77$ = **76.6** K and $\text{NF} = 10\log_{10}(1 + 76.6/290)$ = **1.02** dB. Cooling does not change the loss, so the signal is still halved, but the noise the attenuator adds falls with its temperature.
- 0.5 dB at 330 K: $L = 1.1220$, $T_e = 0.1220 \times 330$ = **40.3** K, $\text{NF} = 10\log_{10}(1 + 40.3/290)$ = **0.56** dB, slightly worse than its 0.5 dB loss because it is hotter than $T_0$.

### Solution 17-02.4

Linear values: $F_1 = 1.3183$, $G_1 = 31.62$; $F_2 = 7.943$, $G_2 = 6.310$; $F_3 = 2.512$. Friis:

$$
F = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1G_2} = 1.31826 + \frac{6.9433}{31.623} + \frac{1.5119}{199.53} = 1.31826 + 0.21957 + 0.00758 = 1.54541 .
$$

The cascade has NF = **1.89** dB and $T_e = 0.54541 \times 290$ = **158.2** K. The contributions to the noise factor are **1.318**, **0.220** and **0.0076**: the mixer, despite its 9 dB noise figure, adds 0.22 because only 15 dB of gain precedes it; the IF amplifier is negligible.

For a 1.5 dB cascade ($F$ = 1.4125), solve $F_1 + [(F_2 - 1) + (F_3 - 1)/G_2]/G = 1.4125$:

$$
G = \frac{6.9433 + 1.5119/6.3096}{1.41254 - 1.31826} = \frac{7.1829}{0.09428} = 76.19 ,
$$

which is **18.82** dB. Another 3.8 dB of LNA gain, a costly increase in a front end that must also handle strong signals.

### Solution 17-02.5

(a) For $\lvert H\rvert^2 = 1/(1 + (f/f_c)^2)$, with $\lvert H(0)\rvert = 1$,

$$
B_N = \int_0^\infty\frac{df}{1 + (f/f_c)^2} = f_c\big[\arctan(f/f_c)\big]_0^\infty = \frac{\pi}{2}f_c .
$$

The ratio is **1.571**. Using $f_c$ underestimates the noise by $10\log_{10}(\pi/2)$ = **1.96** dB and overstates the SNR by the same amount.

(b) With $u = f/f_c$, $B_N = f_c\int_0^\infty du/(1 + u^{2n})$, and the standard integral $\int_0^\infty du/(1 + u^{m}) = (\pi/m)/\sin(\pi/m)$ with $m = 2n$ gives the stated formula. For $n$ = 4: $(\pi/8)/\sin(\pi/8) = 0.3927/0.3827$ = **1.026**, an error of only **0.11** dB. Sharper filters have noise bandwidths close to their 3 dB bandwidths.

### Solution 17-02.6

QPSK carries $\log_2 4 = 2$ bits per symbol, so $E_s/N_0 = 10 + 10\log_{10}2$ = **13.01** dB and $R_b$ = 4 Mb/s.

- **Occupied bandwidth.** $R_s(1 + \alpha) = 2 \times 1.25$ = **2.5** MHz.
- **SNR in the occupied bandwidth.** $S/(N_0B) = (E_s/N_0)(R_s/B) = 13.01 + 10\log_{10}(2/2.5)$ = **12.04** dB.
- **SNR at the matched-filter output.** With noise bandwidth $R_s$, the SNR equals $E_s/N_0$: **13.01** dB. The occupied bandwidth contains slightly more noise than the matched filter passes, because the filter's response rolls off over the excess band.
- **$C/N_0$.** $E_b/N_0 + 10\log_{10}R_b = 10 + 66.02$ = **76.02** dB-Hz.

### Solution 17-02.7

Refer every noise source to the antenna terminals, multiplying a source behind a loss by $L$ and dividing one behind a gain by that gain:

- antenna: $T_A$ = 50 K;
- feed: $(L - 1) \times 290$ with $L = 10^{0.03} = 1.0715$, giving **20.7** K;
- LNB: $60 \times L$ = **64.3** K;
- receiver: $T_{rx} = (10 - 1) \times 290 = 2610$ K, referred as $2610 \times L/10^{5.5}$ = **0.0088** K.

$T_{sys} = 50 + 20.7 + 64.3 + 0.0088$ = **135.0** K, so $N_0 = kT_{sys}$ = **−177.29** dBm/Hz and

$$
C/N_0 = -95 + 177.29 = \textbf{82.29}\ \text{dB-Hz}, \qquad E_s/N_0 = 82.29 - 10\log_{10}(3 \times 10^7) = \textbf{7.52}\ \text{dB}.
$$

Without the feed loss, $T_{sys} = 50 + 60 + 0.008 = 110.0$ K. The 0.3 dB loss raises $T_{sys}$ by a factor of 1.228, costing **0.89** dB of $C/N_0$: three times its loss, because in a cold-sky system the feed's 20.7 K is large next to the 110 K budget. This is why satellite feeds are kept short and why the LNB sits at the focus of the dish.

### Solution 17-02.8

(a) $P = -174 + 60 + 7 + 9 + 2$ = **−96.0** dBm.

(b) With $R_b$ eight times smaller and the same $E_b/N_0$, the required SNR in the same bandwidth falls by $10\log_{10}8$ = 9.03 dB (§3.7, $\text{SNR} = \eta E_b/N_0$). The sensitivity becomes $-96.0 - 9.03$ = **−105.03** dBm. In practice the receiver would also narrow its filter or correlate over the longer symbols to realize this gain (§3.9).

(c) Received power scales as $1/d^2$, so a 9.03 dB (factor 8) improvement allows $d$ to grow by $\sqrt 8$ = **2.83**. Range is bought with data rate.

### Solution 17-02.9

(a) $-96.1 + 10\log_{10}(273/24) = -96.1 + 10.56$ = **−85.54** dBm.

(b) $\text{BW} = 273 \times 12 \times 30$ kHz = 98.28 MHz, $10\log_{10}\text{BW}$ = 79.92 dB, and $P = -174 + 79.92 + 10 - 1 + 2.5 - 3$ = **−85.58** dBm.

(c) At 24 RB, $\text{BW}$ = 8.64 MHz (69.37 dB) and the equation gives **−96.13** dBm, which the table rounds to −96.1 dBm. The table's formula scales that rounded anchor by the RB ratio, so it inherits the 0.03 dB rounding, and (a) is 0.03 dB less stringent than (b). Both agree to the 0.1 dB the specification resolves.

### Solution 17-02.10

(a) Work in sample units (sample spacing 1, so the sample rate is 1 and the band is $\lvert f\rvert < 1/2$). A bit's energy is the sum of its squared samples, $E_b = 8 \times 1^2 = 8$. White noise of two-sided density $N_0/2$ over a band of total width 1 has variance $\sigma^2 = N_0/2$, so $N_0 = 2\sigma^2$. For $E_b/N_0 = 10^{0.6} = 3.981$: $N_0 = 8/3.981 = 2.0095$ and

$$
\sigma^2 = N_0/2 = \textbf{1.005}, \qquad \text{per-sample SNR} = 1/1.005 = \textbf{−0.02}\ \text{dB}.
$$

In general $E_b/N_0 = \text{SNR}_{sample} \times L/2$ for real signals with $L$ samples per bit: the 8 samples add 9.03 dB and $N_0 = 2\sigma^2$ subtracts 3.01 dB, so the per-sample SNR sits 6.02 dB below $E_b/N_0$.

Check with the detector: summing the 8 samples gives signal $\pm8$ and noise variance $8\sigma^2$, so the error probability is $Q(8/\sqrt{8\sigma^2}) = Q(\sqrt{8/\sigma^2}) = Q(\sqrt{2E_b/N_0})$, the BPSK formula of 17-06.

(b) Setting the per-sample SNR to 6 dB means $\sigma^2 = 1/3.981 = 0.2512$, so $N_0 = 0.5024$ and $E_b/N_0 = 8/0.5024 = 15.92$, which is **12.02** dB: 6 dB optimistic. The correct simulation gives $Q(\sqrt{2 \times 3.981}) = Q(2.822)$ = **2.39 × 10⁻³**; the incorrect one gives $Q(\sqrt{2 \times 15.92}) = Q(5.64)$ = **8.3 × 10⁻⁹**, five orders of magnitude too good. The lab's Part 3 shows both.

### Solution 17-02.11

(a) $N_0 = k \times 210.3 = -175.37$ dBm/Hz, so $C/N_0 = -150 + 175.37$ = **25.37** dB-Hz.

(b) $CT/N_0 = 15$ dB needs $10\log_{10}T = 15 - 25.37 = -10.37$, so $T = 10^{-1.037}$ = **91.8** ms.

(c) Coherent integration across a data-bit boundary can cancel the signal, so the receiver integrates 20 ms blocks coherently and adds their energies. Collecting 91.8 ms of energy needs $\lceil 91.8/20\rceil$ = **5** blocks. Non-coherent combining loses some sensitivity (a squaring loss), so a real receiver needs more blocks, or it removes the data with assistance data and integrates coherently for longer.

### Solution 17-02.12

(a) Let the source have temperature $T_s$. Stage 1's available output noise is $G_1k(T_s + T_{e1})B$. Stage 2 adds $kT_{e2}B$ at its input and multiplies by $G_2$; stage 3 adds $kT_{e3}B$ and multiplies by $G_3$:

$$
N_o = G_3\Big\{G_2\big[G_1k(T_s + T_{e1})B + kT_{e2}B\big] + kT_{e3}B\Big\} = G_1G_2G_3\,k\Big(T_s + T_{e1} + \frac{T_{e2}}{G_1} + \frac{T_{e3}}{G_1G_2}\Big)B .
$$

The bracket is $T_s$ plus the cascade's noise temperature, $T_{e1} + T_{e2}/G_1 + T_{e3}/(G_1G_2)$. Dividing by $T_0$ and using $F_i - 1 = T_{ei}/T_0$ gives Friis's formula.

(b) Order 1-then-2 is no worse when

$$
F_1 + \frac{F_2 - 1}{G_1} \le F_2 + \frac{F_1 - 1}{G_2} \iff (F_1 - 1)\Big(1 - \frac{1}{G_2}\Big) \le (F_2 - 1)\Big(1 - \frac{1}{G_1}\Big) .
$$

For amplifiers ($G_i > 1$) both brackets are positive; dividing by them gives $(F_1 - 1)/(1 - 1/G_1) \le (F_2 - 1)/(1 - 1/G_2)$, that is, $M_1 \le M_2$. The noise measure is the noise factor an infinite chain of identical stages would have, minus 1, so the amplifier with the better "infinite-chain" noise goes first.

(c) $M_A = 0.2589/(1 - 0.1)$ = **0.288** and $M_B = 0.2023/(1 - 0.2512)$ = **0.270**, so **B goes first** despite its lower gain. B then A: $F = 1.2023 + 0.2589/3.981 = 1.2673$, **1.03** dB. A then B: $F = 1.2589 + 0.2023/10 = 1.2791$, **1.07** dB.

### Solution 17-02.13

(a) $F = 1.2589 + (199.53 - 1)/G$:

- 10 dB: $1.2589 + 19.85 = 21.11$, **13.25** dB;
- 20 dB: $1.2589 + 1.985 = 3.244$, **5.11** dB;
- 30 dB: $1.2589 + 0.1985 = 1.457$, **1.64** dB.

(b) $G = 198.53/(1.5849 - 1.2589) = 609$, which is **27.85** dB.

(c) The full scale referred to the LNA input is $0.97 - 27.85$ = **−26.88** dBm. Every dB of gain that lowers the noise figure also lowers the largest signal (or blocker) the chain can accept before the ADC clips, so the receiver's dynamic range is fixed by the ADC, and gain only slides the window. Gain steps (§9) and automatic gain control move the window as conditions change.

### Solution 17-02.14

(a) At capacity, $R_b = C = B\log_2(1 + \text{SNR})$, so $\eta = \log_2(1 + \text{SNR})$ and $\text{SNR} = 2^\eta - 1$. With $\text{SNR} = \eta E_b/N_0$ (§3.7), $E_b/N_0 = (2^\eta - 1)/\eta$.

(b) In dB:

- $\eta$ = 0.5: $(\sqrt2 - 1)/0.5 = 0.828$, **−0.82** dB;
- $\eta$ = 1: 1, **0** dB;
- $\eta$ = 4: $15/4 = 3.75$, **5.74** dB;
- $\eta$ = 8: $255/8 = 31.9$, **15.03** dB.

As $\eta \to 0$, $2^\eta - 1 \approx \eta\ln2$, so the bound tends to $\ln 2 = 0.693$, **−1.59** dB.

(c) Link 1 ($\eta$ = 0.8) needs at least $(2^{0.8} - 1)/0.8 = 0.926$, −0.33 dB, and uses 9.97 dB: **10.30** dB from the bound. Link 2 ($\eta$ = 4) needs 5.74 dB and uses 13.98 dB: **8.24** dB from the bound. 17-06 and 17-08 show where such a gap goes: the modulation's own distance from capacity, and how much of it a code recovers.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-02.1a | kT0B, 1 Hz | −173.98 | dBm |
| 17-02.1b | kT0B, 200 kHz | −120.96 | dBm |
| 17-02.1c | kT0B, 20 MHz | −100.96 | dBm |
| 17-02.1d | kT0B, 400 MHz | −87.95 | dBm |
| 17-02.1e | rms noise, 50 Ω, 400 MHz | 17.9 | µV |
| 17-02.2a | Te at NF 0.5 dB | 35.4 | K |
| 17-02.2b | Te at NF 2 dB | 169.6 | K |
| 17-02.2c | Te at NF 10 dB | 2610 | K |
| 17-02.2d | NF at 35 K | 0.49 | dB |
| 17-02.2e | NF at 150 K | 1.81 | dB |
| 17-02.3a | NF, 3 dB pad at 290 K | 3.00 | dB |
| 17-02.3b | Te, 3 dB pad at 77 K | 76.6 | K |
| 17-02.3c | NF, 3 dB pad at 77 K | 1.02 | dB |
| 17-02.3d | Te, 0.5 dB filter at 330 K | 40.3 | K |
| 17-02.3e | NF, 0.5 dB filter at 330 K | 0.56 | dB |
| 17-02.4a | cascade NF | 1.89 | dB |
| 17-02.4b | cascade Te | 158.2 | K |
| 17-02.4c | LNA contribution | 1.318 | — |
| 17-02.4d | mixer contribution | 0.220 | — |
| 17-02.4e | IF contribution | 0.0076 | — |
| 17-02.4f | LNA gain for 1.5 dB | 18.82 | dB |
| 17-02.5a | one-pole BN/fc | 1.571 | — |
| 17-02.5b | one-pole SNR error | 1.96 | dB |
| 17-02.5c | 4th-order Butterworth BN/fc | 1.026 | — |
| 17-02.5d | 4th-order Butterworth error | 0.11 | dB |
| 17-02.6a | Es/N0 | 13.01 | dB |
| 17-02.6b | occupied bandwidth | 2.5 | MHz |
| 17-02.6c | SNR in occupied bandwidth | 12.04 | dB |
| 17-02.6d | C/N0 | 76.02 | dB-Hz |
| 17-02.7a | feed noise temperature | 20.7 | K |
| 17-02.7b | LNB referred | 64.3 | K |
| 17-02.7c | receiver referred | 0.0088 | K |
| 17-02.7d | system noise temperature | 135.0 | K |
| 17-02.7h | N0 | −177.29 | dBm/Hz |
| 17-02.7i | Tsys ratio with and without the feed loss | 1.228 | — |
| 17-02.7e | C/N0 | 82.29 | dB-Hz |
| 17-02.7f | Es/N0 | 7.52 | dB |
| 17-02.7g | cost of the feed loss | 0.89 | dB |
| 17-02.8a | sensitivity, 1 Mb/s | −96.0 | dBm |
| 17-02.8b | sensitivity, 125 kb/s | −105.03 | dBm |
| 17-02.8c | range factor | 2.83 | — |
| 17-02.9a | table formula, 273 RB | −85.54 | dBm |
| 17-02.9b | 3GPP equation, 273 RB | −85.58 | dBm |
| 17-02.9c | 3GPP equation, 24 RB | −96.13 | dBm |
| 17-02.10a | noise variance per sample | 1.005 | — |
| 17-02.10b | per-sample SNR | −0.02 | dB |
| 17-02.10c | Eb/N0 of the wrong simulation | 12.02 | dB |
| 17-02.10d | BER, correct | 2.39e-3 | — |
| 17-02.10e | BER, incorrect | 8.3e-9 | — |
| 17-02.11a | indoor C/N0 | 25.37 | dB-Hz |
| 17-02.11b | coherent integration time | 91.8 | ms |
| 17-02.11c | 20 ms blocks | 5 | — |
| 17-02.12a | noise measure of A | 0.288 | — |
| 17-02.12b | noise measure of B | 0.270 | — |
| 17-02.12c | NF, B then A | 1.03 | dB |
| 17-02.12d | NF, A then B | 1.07 | dB |
| 17-02.13a | cascade NF, 10 dB gain | 13.25 | dB |
| 17-02.13b | cascade NF, 20 dB gain | 5.11 | dB |
| 17-02.13c | cascade NF, 30 dB gain | 1.64 | dB |
| 17-02.13d | gain for 2 dB | 27.85 | dB |
| 17-02.13e | input full scale | −26.88 | dBm |
| 17-02.14a | bound at η = 0.5 | −0.82 | dB |
| 17-02.14b | bound at η = 1 | 0 | dB |
| 17-02.14c | bound at η = 4 | 5.74 | dB |
| 17-02.14d | bound at η = 8 | 15.03 | dB |
| 17-02.14e | limit as η → 0 | −1.59 | dB |
| 17-02.14f | link 1 distance from the bound | 10.30 | dB |
| 17-02.14g | link 2 distance from the bound | 8.24 | dB |
