# Solutions 24-03 · SerDes Architecture and Equalization

Problems: [24-03 problems](../problems/24-03-problems.md) · Chapter: [24-03](../chapters/24-03-serdes-architecture.md)

Every number is recomputed by [verify_24_03.py](../verify/verify_24_03.py).

---

## Solutions

### Solution 24-03.1

(a) $128/2$ = **64** GBd and UI = **15.625** ps.

(b) $64/4$ = **16.0** GHz.

(c) 90° is one UI, so 1° is $15.625/90$ = **0.174** ps.

(d) $64/64$ = **1.00** GS/s.

### Solution 24-03.2

(a) $I = 1.0/50$ = 20 mA, so $P = 1.2 \times 20$ = **24.0** mW.

(b) The current is $1.0/200$ = 5 mA from 1.2 V: **6.0** mW, a quarter of (a).

(c) $1.0^2/200$ = **5.0** mW.

The regulator's own loss is the difference between (b) and (c); the 4 : 1 advantage over CML holds whatever the supply, because both draw from it.

### Solution 24-03.3

(a) With $c_1 = -c_0e^{-2}$, for $k \ge 1$:

$$
g_k = c_0h_k + c_1h_{k-1} = c_0h_0e^{-2k} - c_0e^{-2}h_0e^{-2(k-1)} = 0 .
$$

Every post-cursor cancels because the channel's tail is geometric: each cursor is the previous one times $e^{-2}$, and the second tap subtracts exactly that.

(b) $c_0 + \lvert c_1\rvert = c_0(1 + e^{-2}) = 1$, so $c_0 = 1/(1 + e^{-2})$ = **0.8808** and $c_1$ = **−0.1192**.

(c) $g_0 = c_0h_0 = (1 - e^{-2})/(1 + e^{-2}) = \tanh 1$ = **0.7616**.

(d) $c_0 + c_1 = 0.7616$, so the de-emphasis is $20\log_{10}(1/0.7616)$ = **2.37** dB.

(e) With no ISI left, the NRZ eye is **0.7616** and the PAM4 eye $0.7616/3$ = **0.2539**, against 0.7293 and 0.1529 unequalized. PAM4 gains most, because ISI costs it three times as much relative to its signal.

### Solution 24-03.4

(a) Solving $c_{-1}h_0 + c_0h_{-1} = 0$, $c_{-1}h_2 + c_0h_1 + c_1h_0 = 0$ and $-c_{-1} + c_0 - c_1 = 1$ gives $c_{-1}$ = **−0.1062**, $c_0$ = **0.6372** and $c_1$ = **−0.2566**. The equalized cursors are $g_0$ = **0.3301**, $g_{-2}$ = −0.0106, $g_2$ = −0.0323 and $g_3$ = −0.0128, with $g_{\pm1}$ = 0. The residual ISI is **0.0558**, so the NRZ eye is **0.274**, against $0.60 - 0.40$ = **0.20** unequalized.

(b) $c_{-1} = -c_0h_{-1}/h_0 = -c_0/6$ and $c_0(1 + 1/6) = 1$, so $c_0$ = **0.8571** and $c_{-1}$ = **−0.1429**. The main cursor is $c_{-1}h_1 + c_0h_0$ = **0.4786**. The DFE removes $g_1$ and $g_2$, leaving only $g_{-2} = c_{-1}h_{-1}$ = −0.0143, so the NRZ eye is **0.464**.

The transmitter FFE should spend its swing only on what the DFE cannot reach, the pre-cursors. That is the classic split: a short TX FFE for pre-cursors, the DFE for post-cursors.

### Solution 24-03.5

(a) 12 dB is a ratio of $10^{12/20}$ = 3.981, so $g_mR_S/2$ = 2.981 and $R_S$ = **238.5** Ω. Then $C_S = 1/(2\pi R_Sf_z)$ = **445** fF.

(b) $f_{p1} = 3.981 \times 1.5$ = **5.97** GHz and $f_{p2} = 1/(2\pi \times 160 \times 30\ \text{fF})$ = **33.2** GHz.

(c) $g_mR_D/3.981 = 4/3.981$ = **1.005**, essentially 0 dB.

(d) Evaluating $\lvert H\rvert$ at 13.28 GHz: **3.41**, a boost of **10.61** dB.

The output pole is now well above $f_{p1}$, so most of the 12 dB is available at Nyquist; the rest is lost because 13.28 GHz is only 2.2 times $f_{p1}$, where the gain has not yet flattened.

### Solution 24-03.6

(a) The CTLE's DC gain is $1/5$ of its high-frequency gain:

$$
H(f) = \frac{1}{1 + jf/5} \cdot \frac{1}{5}\,\frac{1 + jf/5}{(1 + jf/25)(1 + jf/40)} = \frac{0.2}{(1 + jf/25)(1 + jf/40)} ,
$$

with $f$ in GHz. The zero cancels the channel's pole.

(b) $20\log_{10}0.2$ = **−13.98** dB.

(c) Solving $\lvert H\rvert = 0.2/\sqrt2$ numerically: **19.6** GHz, **3.92** times the channel's 5 GHz.

(d) Signal amplitude: the whole response is 14 dB lower. Whatever noise the following stages add is now 14 dB larger relative to the signal, and the CTLE's own noise is boosted at high frequency. Bandwidth has been bought with SNR.

### Solution 24-03.7

The UI is $1/64$ GBd = **15.625** ps.

(a) $7 + 6 + 4$ = **17** ps > 15.625 ps: no.

(b) $7 + 3 + 4$ = **14** ps, a slack of **1.625** ps: yes.

(c) Two unrolled taps need each of the 3 slicers for each of $4^2$ = 16 combinations of the two previous symbols: **48** comparators.

### Solution 24-03.8

(a) $\sigma = 1/Q^{-1}(10^{-5}) = 1/4.265$ = **0.2345**.

(b) $\tfrac12Q(0.2/0.2345) + \tfrac12Q(1.8/0.2345)$ = **0.098**.

(c) $1/(1 - 0.098)$ = **1.11**.

(d) $10^{-5} \times 1.11$ = **1.11** × 10⁻⁵.

Propagation adds about 11% to the error count here, but makes errors arrive in pairs about one time in ten, which matters more to the FEC than the count.

### Solution 24-03.9

(a) $0.21088/2^{-8}$ = 53.99, so **54** updates.

(b) $54 \times 64$ UI × 18.82 ps = **65.1** ns.

(c) ±$2^{-8}$ = ±0.0039, or **0.53**% of $h_0$.

A smaller step would dither less but adapt more slowly: the classic LMS trade between tracking speed and steady-state error.

### Solution 24-03.10

The linearized gain is $\sqrt{2/\pi}/\sigma$ per UI, and the bandwidth is $f_c = \delta\rho(\sqrt{2/\pi}/\sigma)f_{baud}/2\pi$.

(a) At 0.01 UI: gain **79.8** per UI and $f_c$ = **49.6** MHz.

(b) At 0.04 UI: gain **19.9** per UI and $f_c$ = **12.4** MHz.

(c) $0.5 \times 2^{-13}$ = 6.10 × 10⁻⁵ UI per UI, or **61.0** ppm.

Quadrupling the jitter cuts the bandwidth by four. A CDR characterized with clean data behaves differently under stress, which is why jitter-tolerance tests add the stress first.

### Solution 24-03.11

(a) A type-2 loop has error transfer $E/\Phi_d = s^2/(s^2 + 2\zeta\omega_ns + \omega_n^2)$. A frequency step is a phase ramp, $\Phi_d = \Delta\omega/s^2$, so $E(s) = \Delta\omega/(s^2 + 2\zeta\omega_ns + \omega_n^2)$. By the final-value theorem, $sE(s) \to 0$ as $s \to 0$: the steady-state error is **0** UI.

(b) Inverting, $e(t) = (\Delta\omega/\omega_d)e^{-\zeta\omega_nt}\sin\omega_dt$, with $\omega_d = \omega_n\sqrt{1 - \zeta^2}$ = 8.886 × 10⁶ rad/s. Setting $de/dt = 0$ gives $\tan\omega_dt = \sqrt{1 - \zeta^2}/\zeta = 1$, so $t^* = (\pi/4)/\omega_d$ = **88.4** ns. With Δω = 5.3125 × 10⁶ UI/s, $e(t^*)$ = **0.193** UI.

(c) A first-order loop at 2 MHz settles to $\Delta\omega/(2\pi \times 2\ \text{MHz})$ = **0.423** UI and stays there.

The second-order loop's transient peak is less than half the first-order loop's permanent error, and it decays to zero within a few hundred nanoseconds.

### Solution 24-03.12

(a) $72 \times 224 \times 10^9 \times 3 \times 10^{-12}$ = **48.4** W.

(b) At 1.11 pJ/b: **17.9** W.

(c) **30.5** W.

That difference is why accelerators keep their highest-bandwidth links short (24-06) and why extra-short-reach SerDes is a separate product line.

### Solution 24-03.13

(a) The factor is $0.5(\sqrt2 - 1) + 0.5$ = 0.7071, so PAM4 wins above $9.54/0.7071$ = **13.5** dB.

(b) $18 \times 0.7071$ = **12.73** dB.

(c) $12.73 - 9.54$ = **3.2** dB.

### Solution 24-03.14

(a) NRZ with FFE: the eye is 208.0 mV, its half 104.0 mV, $Q(13.0)$ = **6.1** × 10⁻³⁹. With DFE: 283.6 mV, $Q(17.7)$ = **1.3** × 10⁻⁷⁰.

(b) PAM4 with FFE: the eye is 62.0 mV, its half 31.0 mV, the argument **3.9** and SER $= 1.5Q(3.875)$ = **8.0** × 10⁻⁵, so BER = **4.0** × 10⁻⁵. With DFE: 87.6 mV, argument **5.5**, SER = **3.3** × 10⁻⁸ and BER = **1.6** × 10⁻⁸.

(c) Both PAM4 options meet 10⁻⁴; only the DFE meets 10⁻⁶.

NRZ is effectively error-free with either equalizer on this gentle channel. PAM4 at the same symbol rate needs both the DFE and FEC, a reminder that PAM4 is chosen for steep channels, not easy ones.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-03.1a | symbol rate | 64 | GBd |
| 24-03.1a1 | UI | 15.625 | ps |
| 24-03.1b | clock | 16.0 | GHz |
| 24-03.1c | timing per degree | 0.174 | ps |
| 24-03.1d | sub-ADC rate | 1.00 | GS/s |
| 24-03.2a0 | CML current | 20 | mA |
| 24-03.2a | CML power | 24.0 | mW |
| 24-03.2b0 | SST current | 5 | mA |
| 24-03.2b | SST power through a regulator | 6.0 | mW |
| 24-03.2c | SST power, ideal supply | 5.0 | mW |
| 24-03.2d | CML-to-SST ratio | 4 | |
| 24-03.3b | main tap | 0.8808 | |
| 24-03.3b1 | post-cursor tap | -0.1192 | |
| 24-03.3c | equalized main cursor | 0.7616 | |
| 24-03.3d | de-emphasis | 2.37 | dB |
| 24-03.3e | PAM4 eye | 0.2539 | |
| 24-03.3e0 | unequalized NRZ eye | 0.7293 | |
| 24-03.3e1 | unequalized PAM4 eye | 0.1529 | |
| 24-03.4a | pre-cursor tap | -0.1062 | |
| 24-03.4a1 | main tap | 0.6372 | |
| 24-03.4a2 | post-cursor tap | -0.2566 | |
| 24-03.4a3 | main cursor | 0.3301 | |
| 24-03.4a4 | g at -2 | -0.0106 | |
| 24-03.4a5 | g at 2 | -0.0323 | |
| 24-03.4a6 | g at 3 | -0.0128 | |
| 24-03.4a7 | residual ISI | 0.0558 | |
| 24-03.4a8 | NRZ eye with FFE | 0.274 | |
| 24-03.4a9 | unequalized NRZ eye | 0.20 | |
| 24-03.4a10 | unequalized ISI | 0.40 | |
| 24-03.4b | main tap, two-tap FFE | 0.8571 | |
| 24-03.4b1 | pre-cursor tap, two-tap FFE | -0.1429 | |
| 24-03.4b2 | main cursor | 0.4786 | |
| 24-03.4b3 | g at -2 | -0.0143 | |
| 24-03.4b4 | NRZ eye with FFE and DFE | 0.464 | |
| 24-03.5a0 | peaking ratio | 3.981 | |
| 24-03.5a1 | half gm RS | 2.981 | |
| 24-03.5a | RS | 238.5 | Ω |
| 24-03.5a2 | CS | 445 | fF |
| 24-03.5b | first pole | 5.97 | GHz |
| 24-03.5b1 | output pole | 33.2 | GHz |
| 24-03.5c | DC gain | 1.005 | |
| 24-03.5d | gain at 13.28 GHz | 3.41 | |
| 24-03.5d1 | boost at 13.28 GHz | 10.61 | dB |
| 24-03.5d2 | Nyquist over first pole | 2.2 | |
| 24-03.6b | DC gain | -13.98 | dB |
| 24-03.6c | bandwidth | 19.6 | GHz |
| 24-03.6c1 | bandwidth ratio | 3.92 | |
| 24-03.6d | signal loss | 14 | dB |
| 24-03.7a0 | UI | 15.625 | ps |
| 24-03.7a | direct loop | 17 | ps |
| 24-03.7b | unrolled loop | 14 | ps |
| 24-03.7b1 | slack | 1.625 | ps |
| 24-03.7c0 | previous-symbol combinations | 16 | |
| 24-03.7c | comparators for two PAM4 taps | 48 | |
| 24-03.8a0 | inverse Q at 1e-5 | 4.265 | |
| 24-03.8a | sigma | 0.2345 | |
| 24-03.8b | continuation probability | 0.098 | |
| 24-03.8c | mean burst | 1.11 | |
| 24-03.8d | error rate with propagation | 1.11e-5 | |
| 24-03.8e | extra errors | 11 | % |
| 24-03.9a0 | updates, exact | 53.99 | |
| 24-03.9a | updates | 54 | |
| 24-03.9b | adaptation time | 65.1 | ns |
| 24-03.9c0 | step | 0.0039 | |
| 24-03.9c | dither as share of h0 | 0.53 | % |
| 24-03.10a | gain at 0.01 UI | 79.8 | 1/UI |
| 24-03.10a1 | bandwidth at 0.01 UI | 49.6 | MHz |
| 24-03.10b | gain at 0.04 UI | 19.9 | 1/UI |
| 24-03.10b1 | bandwidth at 0.04 UI | 12.4 | MHz |
| 24-03.10c0 | slew limit | 6.10e-5 | UI/UI |
| 24-03.10c | slew limit in ppm | 61.0 | ppm |
| 24-03.11a | steady-state error | 0 | UI |
| 24-03.11b0 | damped frequency | 8.886e6 | rad/s |
| 24-03.11b | time of peak | 88.4 | ns |
| 24-03.11b1 | drift rate | 5.3125e6 | UI/s |
| 24-03.11b2 | peak error | 0.193 | UI |
| 24-03.11c | first-order error | 0.423 | UI |
| 24-03.12a | power at 3 pJ/b | 48.4 | W |
| 24-03.12b | power at 1.11 pJ/b | 17.9 | W |
| 24-03.12c | saving | 30.5 | W |
| 24-03.13a0 | loss factor | 0.7071 | |
| 24-03.13a | break-even loss | 13.5 | dB |
| 24-03.13b | NRZ extra loss | 12.73 | dB |
| 24-03.13c | PAM4 advantage | 3.2 | dB |
| 24-03.14a0 | NRZ FFE eye | 208.0 | mV |
| 24-03.14a00 | NRZ FFE half eye | 104.0 | mV |
| 24-03.14a1 | NRZ FFE Q | 13.0 | |
| 24-03.14a | NRZ BER with FFE | 6.1e-39 | |
| 24-03.14a2 | NRZ DFE eye | 283.6 | mV |
| 24-03.14a3 | NRZ DFE Q | 17.7 | |
| 24-03.14a4 | NRZ BER with DFE | 1.3e-70 | |
| 24-03.14b0 | PAM4 FFE eye | 62.0 | mV |
| 24-03.14b00 | PAM4 FFE half eye | 31.0 | mV |
| 24-03.14b1 | PAM4 FFE argument | 3.9 | |
| 24-03.14b | PAM4 SER with FFE | 8.0e-5 | |
| 24-03.14b2 | PAM4 BER with FFE | 4.0e-5 | |
| 24-03.14b3 | PAM4 DFE eye | 87.6 | mV |
| 24-03.14b4 | PAM4 DFE argument | 5.5 | |
| 24-03.14b5 | PAM4 SER with DFE | 3.3e-8 | |
| 24-03.14b6 | PAM4 BER with DFE | 1.6e-8 | |
