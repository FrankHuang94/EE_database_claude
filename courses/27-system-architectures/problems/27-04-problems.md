# Problems 27-04 · Wearables II: Earbuds and Smart Glasses / XR

Chapter: [27-04](../chapters/27-04-wearables-earbuds-and-glasses.md) · Worked solutions: [27-04 solutions](../solutions/27-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All device parameters are assumed unless a source is cited. Speaker power is $P = 1\ \text{mW} \times 10^{(\text{SPL} - S)/10}$; ANC attenuation with delay $\tau$ and gain $g$ is $-20\log_{10}|1 - g\,e^{-j2\pi f\tau}|$; LE packets on the 2M PHY carry 15 octets of overhead when encrypted (2 preamble, 4 access address, 2 header, 4 MIC, 3 CRC) and take $8 \times \text{octets}/2$ µs; heat shed is $hA\Delta T$; waveguide display power is $L_v\,\text{APL}/(\eta_{wg}\eta_{src})$ for an emissive source; registration error is $\omega\tau$.

---

## Problems

### Problem 27-04.1 [A]

**Which constraint binds?** For each device name the constraint that binds first (battery energy, heat, weight, latency or bandwidth) and one design response: (a) a true-wireless earbud; (b) audio-and-camera glasses without a display; (c) display glasses; (d) a mixed-reality headset; (e) a hearing aid worn 16 hours a day.

### Problem 27-04.2 [A]

**Loudness.** A driver has a sensitivity of 98 dB SPL/mW. Find the electrical power for (a) 90 dB SPL and (b) 115 dB SPL, and (c) the power ratio for every 6 dB of extra loudness.

### Problem 27-04.3 [A]

**An LC3 packet.** LC3 at 160 kb/s in 7.5 ms frames: find the octets per frame and the encrypted packet's air time on the LE 2M PHY and on the LE 1M PHY (1-octet preamble).

### Problem 27-04.4 [B]

**An ANC delay budget.** (a) Find the largest delay that gives 15 dB of cancellation at 300 Hz with perfect gain. (b) With that delay, find the attenuation at 1 kHz. (c) Above what frequency does that delay amplify noise?

### Problem 27-04.5 [B]

**Gain accuracy.** (a) With no delay, what gain accuracy is needed for 30 dB of cancellation? (b) With a 20 µs delay at 200 Hz, find the attenuation with perfect gain and with a 2% gain error.

### Problem 27-04.6 [B]

**An earbud and its case.** A 45 mAh, 3.85 V earbud draws 22.0 mW at the rails with ANC on and 15.0 mW with it off, through 85% conversion. Its case holds 480 mAh at 3.85 V and delivers 65% of its energy to the buds. Find (a) the bud's energy, (b) its life with ANC on and off, (c) the number of full recharges of the pair the case provides, and (d) the total listening time with ANC on.

### Problem 27-04.7 [B]

**Where to spend the effort?** At 85 dB SPL a driver of 105 dB SPL/mW sits behind an amplifier with 90% switching efficiency and 1.0 mW quiescent draw. Find the amplifier's input power, and the saving from (a) halving the quiescent draw and (b) raising the switching efficiency to 95%.

### Problem 27-04.8 [B]

**Cool glasses.** Glasses with 45 cm² of warm surface, $h$ = 6 W/m²·K and a 6 K limit idle at 80 mW. (a) Find the sustained power. (b) A camera pipeline adds 250 mW: can it run continuously? (c) With a 240 s thermal time constant, how long can it run starting from the idle equilibrium?

### Problem 27-04.9 [B]

**How bright can it be?** A display-glasses waveguide delivers 500 nits per lumen and the emissive (micro-LED) projector 15 lm/W. Within a 50 mW display budget, find the largest luminance at APL 0.10.

### Problem 27-04.10 [B]

**Offload a vision model?** Running a model on the glasses costs 2.0 J per inference. Sending a 200 kB image to the phone costs 20 nJ/bit of radio energy (the result returned is negligible). Find the radio energy and how many times cheaper offload is for the glasses' battery. What does the comparison leave out?

### Problem 27-04.11 [C]

**Sizing the fovea.** A headset with a 100° field renders the periphery at one third of the linear resolution. How large a square fovea (in degrees) can it render at full resolution for 15% of the full-resolution shading work?

### Problem 27-04.12 [C]

**A latency target.** For a registration error of at most 1° during a 300°/s head turn, find the allowed motion-to-photon latency. Which pipeline stages of Example 27-04.6 must reprojection hide, and is the target met with 2 ms tracking, 2 ms reprojection, 1 ms response and a display that scans out in 1.1 ms on average?

### Problem 27-04.13 [C]

**Battery life on the head.** A headset with a 35 Wh battery draws 12 W rendering locally and 5.5 W with split rendering. Find both battery lives and the latency the second option adds in Example 27-04.6.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Architectures and binding constraints | 1, 10, 13 |
| 2. Speaker power and the earbud budget | 2, 7 |
| 3. ANC delay and gain limits | 4, 5 |
| 4. LE Audio streams, battery and case | 3, 6 |
| 5. Glasses heat and displays; headset pixels and latency | 8, 9, 11, 12, 13 |
