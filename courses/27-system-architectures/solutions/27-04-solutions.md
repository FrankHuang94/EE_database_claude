# Solutions 27-04 · Wearables II: Earbuds and Smart Glasses / XR

Problems: [27-04 problems](../problems/27-04-problems.md) · Chapter: [27-04](../chapters/27-04-wearables-earbuds-and-glasses.md). Every number is recomputed by [verify_27_04.py](../verify/verify_27_04.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-04.1

(a) **Battery energy**: a cell of a few tens of mWh must last hours; respond with low-quiescent amplifiers, hardware ANC filters, LE Audio and a recharging case. (b) **Heat** (and weight): offload heavy compute to the phone, keep a low-power SoC on the glasses, split the battery between the temples. (c) **Heat and display efficiency**: sparse, low-APL content through an efficient waveguide; brightness only when ambient light demands it. (d) **Latency and pixel bandwidth** (with heat on the face): eye-tracked foveated rendering, late-stage reprojection, an external battery. (e) **Battery energy over a long day**, plus comfort: the lowest-power audio path, often a disposable or larger rechargeable cell, and no streaming when not needed.

### Solution 27-04.2

(a) $10^{(90 - 98)/10}$ = **0.158** mW. (b) $10^{(115 - 98)/10}$ = **50.1** mW, far more than a tiny driver can take continuously; such levels are brief peaks. (c) $10^{0.6}$ = **3.98**: every 6 dB of loudness costs about four times the power.

### Solution 27-04.3

$n = 160\,000 \times 0.0075/8$ = **150** octets. On 2M: $150 + 15 = 165$ octets, $8 \times 165/2$ = **660** µs. On 1M the preamble is 1 octet: $164$ octets, $8 \times 164$ = **1312** µs. The 2M PHY halves the air time, and so roughly the receive energy, which is why LE Audio links prefer it.

### Solution 27-04.4

(a) $2\sin(\pi f\tau) = 10^{-15/20} = 0.178$, so $\tau = \arcsin(0.0889)/(\pi \times 300)$ = **94.5** µs.

(b) At 1 kHz, $2\sin(\pi \times 1000 \times 94.5 \times 10^{-6}) = 0.585$: **4.66** dB.

(c) Amplification starts at $1/(6\tau)$ = **1.76** kHz.

A delay that suffices for low-frequency rumble is useless for speech-band noise; feedforward paths are tuned for the band where the delay allows cancellation.

### Solution 27-04.5

(a) At $\tau = 0$ the residual is $|1 - g|$, so $|1 - g| \le 10^{-30/20} = 0.0316$: the gain must be right to within **±3.16**%.

(b) $\phi = 2\pi \times 200 \times 20 \times 10^{-6} = 0.0251$. Perfect gain: $|R| = 2\sin(\phi/2) = 0.0251$, **32.0** dB. With $g = 1.02$: $|R|^2 = (1 - 1.02\cos\phi)^2 + (1.02\sin\phi)^2$, $|R| = 0.0323$, **29.8** dB. At low frequency, gain matching matters as much as delay; real ANC adapts its gain because ear-tip seal and fit change it.

### Solution 27-04.6

(a) $E_b = 45 \times 3.85$ = **173.25** mWh.

(b) ANC on: $173.25 \times 0.85/22.0$ = **6.69** h; off: $173.25 \times 0.85/15.0$ = **9.82** h.

(c) The case holds $480 \times 3.85 = 1848$ mWh and delivers $0.65 \times 1848$ = 1201 mWh; a pair needs $2 \times 173.25 = 346.5$ mWh per recharge: **3.47** recharges.

(d) $(1 + 3.47) \times 6.69$ = **29.9** h with ANC on.

### Solution 27-04.7

Output power $10^{(85 - 105)/10}$ = 0.0100 mW. Input $0.01/0.9 + 1.0$ = **1.011** mW. (a) Halving the quiescent draw saves **0.500** mW. (b) Raising efficiency to 95% saves $0.01/0.9 - 0.01/0.95$ = **0.000585** mW (0.585 µW), about **855** times less. At listening levels, only the idle draw matters.

### Solution 27-04.8

(a) $P = 6 \times 0.0045 \times 6$ = **0.162** W.

(b) $0.080 + 0.250$ = **0.330** W, about twice the sustained limit: not continuously.

(c) Steady rise at 0.330 W: $0.330/(6 \times 0.0045)$ = **12.2** K; idle rise $0.080/0.027$ = **2.96** K. $t = 240\ln[(12.22 - 2.96)/(12.22 - 6)]$ = **95.4** s: about a minute and a half of capture before the frame reaches its limit, after which the pipeline must throttle or move to the phone.

### Solution 27-04.9

$L_v = P\,\eta_{wg}\eta_{src}/\text{APL} = 0.050 \times 500 \times 15/0.10$ = **3750** nits. At full white the same budget gives only 375 nits, too dim outdoors.

### Solution 27-04.10

$200 \times 10^3 \times 8$ bits $\times\ 20$ nJ/bit = **0.032** J, **62.5** times less than 2.0 J. The comparison leaves out the phone's energy for the inference (the system still pays it, from a much larger battery), the radio's wake-up and idle costs, the added latency of the round trip, and what happens when the phone is out of range.

### Solution 27-04.11

With $x = (\theta_f/100)^2$ and $s^2 = 1/9$: $x + (1 - x)/9 = 0.15$, so $x(1 - 1/9) = 0.15 - 1/9$ and $x$ = **0.04375**. Then $\theta_f = 100\sqrt{0.04375}$ = **20.9**°.

### Solution 27-04.12

$\tau \le 1°/(300°/\text{s})$ = **3.33** ms. Reprojection hides the rendering frame and any network delay, but not tracking, the reprojection itself, scan-out or the display's response: $2 + 2 + 1.1 + 1$ = **6.1** ms, an error of $300 \times 0.0061$ = **1.83**°. The target is not met. Headsets close the gap by **pose prediction**: extrapolating the head's motion forward by the known latency, so the residual error is the prediction error rather than $\omega\tau$.

### Solution 27-04.13

Local: $35/12$ = **2.92** h. Split: $35/5.5$ = **6.36** h, more than twice as long, at the cost of the **16** ms of encoding, network and decoding latency of Example 27-04.6, which reprojection must hide, and of a phone, PC or server doing the rendering.

### Solution 27-04.14

(a) $R = 1 - g\cos\phi + jg\sin\phi$, since $e^{-j\phi} = \cos\phi - j\sin\phi$. Its squared magnitude is $(1 - g\cos\phi)^2 + g^2\sin^2\phi = 1 - 2g\cos\phi + g^2(\cos^2\phi + \sin^2\phi) = 1 - 2g\cos\phi + g^2$. With $g = 1$: $|R|^2 = 2 - 2\cos\phi = 4\sin^2(\phi/2)$, using $1 - \cos\phi = 2\sin^2(\phi/2)$, so $|R| = 2|\sin(\pi f\tau)|$.

(b) With $\phi = 0$: $|R|^2 = 1 - 2g + g^2 = (1 - g)^2$, so $|R| = |\varepsilon|$. Twenty decibels needs $|R| \le 0.1$: the gain must lie between 0.9 and 1.1, that is from **-0.92** dB to **+0.83** dB. Gain matching across the band is as hard a requirement as delay.

(c) Substitute $g = 1 + \varepsilon$: $|R|^2 = 1 - 2(1 + \varepsilon)\cos\phi + (1 + \varepsilon)^2 = \varepsilon^2 + 2(1 + \varepsilon)(1 - \cos\phi)$. For small $\phi$, $1 - \cos\phi \approx \phi^2/2$, and dropping $\varepsilon\phi^2$ leaves $|R|^2 \approx \varepsilon^2 + \phi^2$: gain and phase errors add in quadrature. Here $\phi = 2\pi \times 500 \times 20\ \mu\text{s}$ = **0.0628** rad. Approximate: $|R| = \sqrt{0.0025 + 0.003948}$ = **0.0803**, **21.9** dB. Exact: **0.0815**, **21.8** dB.

### Solution 27-04.15

(a) $n = 32\,000 \times 0.0075/8$ = **30** octets. Each packet is $30 + 15 = 45$ octets on air, $8 \times 45/2$ = **180** µs, in both directions.

(b) Radio on: $180 + 150 + 180$ = **510** µs per 7.5 ms, a duty cycle of **6.80**% (plus the wake-up).

(c) Charge: $1.2 \times 200 + 3.6 \times (180 + 150) + 4.1 \times 180 = 240 + 1188 + 738$ = **2166** nC per event. $I_{avg} = 2166\ \text{nC}/7.5\ \text{ms}$ = **288.8** µA, and $3.0 \times 0.2888$ = **0.866** mW.

(d) The battery holds $55 \times 3.85$ = **211.75** mWh. The bud draws $9.0 + 0.866$ = **9.87** mW, so it lasts **21.5** h. A two-way voice stream costs the radio about what one-way music at 96 kb/s does (Example 27-04.4), because the per-event overheads dominate.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-04.2a | power at 90 dB SPL | 0.158 | mW |
| 27-04.2b | power at 115 dB SPL | 50.1 | mW |
| 27-04.2c | power ratio per 6 dB | 3.98 | — |
| 27-04.3a | octets per frame | 150 | octets |
| 27-04.3b | packet octets on 2M | 165 | octets |
| 27-04.3c | air time on 2M | 660 | µs |
| 27-04.3d | packet octets on 1M | 164 | octets |
| 27-04.3e | air time on 1M | 1312 | µs |
| 27-04.4a | residual for 15 dB | 0.178 | — |
| 27-04.4a1 | sine argument | 0.0889 | — |
| 27-04.4a2 | largest delay | 94.5 | µs |
| 27-04.4b | residual at 1 kHz | 0.585 | — |
| 27-04.4b1 | attenuation at 1 kHz | 4.66 | dB |
| 27-04.4c | amplification threshold | 1.76 | kHz |
| 27-04.5a | gain accuracy | 3.16 | % |
| 27-04.5a1 | residual for 30 dB | 0.0316 | — |
| 27-04.5b | phase at 200 Hz | 0.0251 | rad |
| 27-04.5b1 | residual, perfect gain | 0.0251 | — |
| 27-04.5b2 | attenuation, perfect gain | 32.0 | dB |
| 27-04.5b3 | residual, 2% gain error | 0.0323 | — |
| 27-04.5b4 | attenuation, 2% gain error | 29.8 | dB |
| 27-04.6a | bud energy | 173.25 | mWh |
| 27-04.6b | life with ANC on | 6.69 | h |
| 27-04.6b1 | life with ANC off | 9.82 | h |
| 27-04.6c | case energy | 1848 | mWh |
| 27-04.6c1 | energy delivered by case | 1201 | mWh |
| 27-04.6c2 | energy per pair recharge | 346.5 | mWh |
| 27-04.6c3 | recharges | 3.47 | — |
| 27-04.6d | total listening time | 29.9 | h |
| 27-04.7a | output power | 0.0100 | mW |
| 27-04.7b | amplifier input power | 1.011 | mW |
| 27-04.7c | saving from halving quiescent | 0.500 | mW |
| 27-04.7d | saving from 95% efficiency | 0.000585 | mW |
| 27-04.7e | ratio of the two savings | 855 | — |
| 27-04.8a | sustained power | 0.162 | W |
| 27-04.8b | camera plus idle power | 0.330 | W |
| 27-04.8b1 | ratio to sustained | 2 | — |
| 27-04.8c | steady rise | 12.2 | K |
| 27-04.8c1 | idle rise | 2.96 | K |
| 27-04.8c2 | time to limit | 95.4 | s |
| 27-04.9a | largest luminance at APL 0.10 | 3750 | nits |
| 27-04.9b | luminance at full white | 375 | nits |
| 27-04.10a | radio energy | 0.032 | J |
| 27-04.10b | offload advantage | 62.5 | — |
| 27-04.11a | fovea area fraction | 0.04375 | — |
| 27-04.11b | fovea size | 20.9 | deg |
| 27-04.12a | allowed latency | 3.33 | ms |
| 27-04.12b | perceived latency with reprojection | 6.1 | ms |
| 27-04.12c | error with reprojection | 1.83 | deg |
| 27-04.13a | life rendering locally | 2.92 | h |
| 27-04.13b | life with split rendering | 6.36 | h |
| 27-04.13c | added latency | 16 | ms |
| 27-04.14a | lower gain limit | -0.92 | dB |
| 27-04.14b | upper gain limit | 0.83 | dB |
| 27-04.14c | phase at 500 Hz, 20 µs | 0.0628 | rad |
| 27-04.14d | approximate residual | 0.0803 | — |
| 27-04.14e | approximate attenuation | 21.9 | dB |
| 27-04.14f | exact residual | 0.0815 | — |
| 27-04.14g | exact attenuation | 21.8 | dB |
| 27-04.15a | octets per frame | 30 | octets |
| 27-04.15b | packet air time | 180 | µs |
| 27-04.15c | radio on time | 510 | µs |
| 27-04.15d | duty cycle | 6.80 | % |
| 27-04.15e | charge per event | 2166 | nC |
| 27-04.15f | average current | 288.8 | µA |
| 27-04.15g | radio power | 0.866 | mW |
| 27-04.15h | battery energy | 211.75 | mWh |
| 27-04.15i | total draw | 9.87 | mW |
| 27-04.15j | life | 21.5 | h |
