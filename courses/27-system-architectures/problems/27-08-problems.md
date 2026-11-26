# Problems 27-08 · Edge AI and IoT

Chapter: [27-08](../chapters/27-08-edge-ai-and-iot.md) · Worked solutions: [27-08 solutions](../solutions/27-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All device parameters are assumed unless a source is cited. The models are:

- convolution MACs $HWC_{\text{out}}k^2C_{\text{in}}$; inference time $\text{MACs}/(muf)$;
- LoRa symbol time $2^{SF}/BW$ and the data sheet's payload-symbol formula (§3.3), with $DE = 1$ when the symbol time exceeds 16 ms;
- photovoltaic power $(E_v/K)A\eta_{pv}\eta_c$; supercapacitor $C = 2E/(V_{\max}^2 - V_{\min}^2)$.

Unless stated otherwise, use the keyword spotter and parameters of Example 27-08.1 and the sensor node of Example 27-08.4.

---

## Problems

### Problem 27-08.1 [A]

**Which radio?** Choose a radio family for each device and give the deciding reason:

- (a) a battery-powered light switch in a smart home;
- (b) a water meter in a basement reporting once a day for 15 years, in a city with mobile coverage;
- (c) a security camera streaming video;
- (d) a soil-moisture sensor on a farm 5 km from the farmhouse, with no mobile coverage;
- (e) a fitness tracker.

### Problem 27-08.2 [A]

**One layer.** A 1 × 1 convolution maps a 12 × 12 × 32 tensor to 12 × 12 × 64. Find:

- (a) its MACs;
- (b) its int8 weight bytes (ignore biases);
- (c) the SRAM for its input and output tensors at one byte each.

### Problem 27-08.3 [A]

**Symbol times.** Find LoRa's symbol time at 125 kHz for SF7 to SF12, the ratio from SF7 to SF12, and the SF7 symbol time at 250 kHz.

### Problem 27-08.4 [B]

**Listening faster.** The keyword spotter of Example 27-08.1 must run every 40 ms instead of every 100 ms. Find the average power and coin-cell life on the CPU and on the NPU.

### Problem 27-08.5 [B]

**A vibration sensor.** A three-axis accelerometer samples at 3.2 kHz with 16 bits per axis. Find:

- (a) the raw rate and its radio power at 20 nJ per bit;
- (b) the radio power to send a 64-byte spectrum summary each second, and the total if computing the summary costs 50 µW;
- (c) the ratio of (a) to the total in (b).

### Problem 27-08.6 [B]

**A longer packet.** Find the symbol time, payload symbols and time on air of a 51-byte packet at SF9, 125 kHz, coding rate 4/5, 8-symbol preamble, explicit header and CRC.

### Problem 27-08.7 [B]

**Messages per hour.** For Example 27-08.3's 20-byte packet at SF10, find:

- (a) the symbol time, payload symbols and time on air;
- (b) the packets per hour allowed in a 1% sub-band and in a 0.1% sub-band.

### Problem 27-08.8 [B]

**Reporting less often.** Example 27-08.4's node is stuck at SF12. It reports hourly instead of every 15 minutes. Find:

- (a) its daily energy;
- (b) its life without and with self-discharge;
- (c) its daily airtime. Does it now meet a 30-second daily fair-use limit?

### Problem 27-08.9 [B]

**Only the night.** Size the supercapacitor (4.0 V to 2.2 V) for Example 27-08.5's node if it only has to bridge 16 hours of darkness.

### Problem 27-08.10 [C]

**Brighter light.** Under 500 lux for 10 hours a day, with the same cell efficiency and converter as Example 27-08.5, find the daily harvest per square centimetre and the cell area that would make the always-listening NPU node energy-neutral.

### Problem 27-08.11 [B]

**A bigger image.** With a hash engine at 2 cycles per byte and 64 MHz, find the secure-boot hash time for a 2 MiB image, the total boot-check time with a 62.5 ms signature check, and the energy at 10 mW.

### Problem 27-08.12 [C]

**Gateways or batteries?** A utility deploys 10,000 nodes like Example 27-08.4's for ten years. With its current gateways they run at SF12 (life 4.89 years, from Example 27-08.4). A battery-replacement visit costs $60 (assumed). Adding 20 gateways at an installed and operated cost of $1,000 each over the ten years (assumed; it must cover installation, backhaul and upkeep) would let every node run at SF7. Find:

- (a) the replacements per node and the total replacement cost over ten years at SF12;
- (b) the gateway cost and the saving.

What does this say about who should pay for network density?

### Problem 27-08.13 [A]

**Reading the NPU claim.** Arm says the Ethos-U85 scales from 128 to 2048 MACs and gives "up to 4 TOPs of performance at 1 GHz" [R-695]. Counting two operations per MAC, find the peak at 1 GHz for the smallest and largest configurations, and at a 200 MHz microcontroller clock for both.

### Problem 27-08.14 [B]

**Two derivations.**

- (a) Derive the ratio of the MACs of a depthwise-separable convolution ($k \times k$ depthwise, then $1 \times 1$ pointwise) to those of a standard $k \times k$ convolution with the same input and output shapes. Evaluate it, and the reduction factor, for $k = 5$ and $C_{\text{out}} = 128$.
- (b) Starting from a capacitor's stored energy $\tfrac{1}{2}CV^2$, derive the energy it can deliver between $V_{\max}$ and $V_{\min}$ and hence the sizing formula $C = 2E/(V_{\max}^2 - V_{\min}^2)$. Show that the usable fraction of the full stored energy is $1 - (V_{\min}/V_{\max})^2$, and evaluate it for 4.0 V to 2.2 V and for a window of 2:1.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. MACs, memory, latency and energy per inference | 2, 4, 13, 14 |
| 2. Edge compute against sending data | 5 |
| 3. LoRa time on air, duty cycle and radio choice | 1, 3, 6, 7 |
| 4. Battery life, harvesting and storage | 8, 9, 10, 12, 14 |
| 5. Secure boot, updates and claims | 11, 13 |
