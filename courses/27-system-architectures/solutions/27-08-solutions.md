# Solutions 27-08 · Edge AI and IoT

Problems: [27-08 problems](../problems/27-08-problems.md) · Chapter: [27-08](../chapters/27-08-edge-ai-and-iot.md). Every number is recomputed by [verify_27_08.py](../verify/verify_27_08.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-08.1

(a) **IEEE 802.15.4 (Thread or Zigbee) or Bluetooth LE.** Short range inside a home with a hub, and the lowest energy per message.

(b) **NB-IoT or LTE-M.** Deep indoor coverage through repetition (21-11), no gateways to install, and a mobile operator already serving the city.

(c) **Wi-Fi.** Only Wi-Fi offers megabits per second at home, and a camera is usually mains-powered.

(d) **LoRaWAN with a private gateway at the farmhouse.** Kilometres of range in unlicensed spectrum without mobile coverage; the data rate is tiny, so duty-cycle limits do not bind.

(e) **Bluetooth LE.** The phone is the gateway, and BLE's energy per connection event suits a small battery (27-03).

### Solution 27-08.2

(a) $12 \times 12 \times 32 \times 64$ = **294912** MACs.

(b) $32 \times 64$ = **2048** bytes.

(c) Input $12 \times 12 \times 32$ = **4608** bytes and output **9216** bytes, so **13824** bytes of SRAM.

### Solution 27-08.3

$T_s = 2^{SF}/125\ \text{kHz}$: **1.024**, **2.048**, **4.096**, **8.192**, **16.384** and **32.768** ms for SF7 to SF12. That is a ratio of **32**, five doublings. At 250 kHz, SF7's symbol takes **0.512** ms.

### Solution 27-08.4

At 25 inferences a second:

- **CPU:** $25 \times 177\ \mu\text{J} + 0.305\ \text{mW}$ = **4.73** mW, lasting **5.94** days on the coin cell.
- **NPU:** $25 \times 16.6\ \mu\text{J} + 0.305\ \text{mW}$ = **0.720** mW, lasting **39.1** days.

The faster rate hurts the CPU far more, because its inference energy dominates.

### Solution 27-08.5

(a) $3 \times 3200 \times 16$ = **153600** b/s, costing **3.07** mW.

(b) $64 \times 8 \times 20\ \text{nJ}$ = **10.2** µW of radio; with 50 µW of computation, **60.2** µW in total.

(c) $3.072\ \text{mW}/60.2\ \mu\text{W}$ = **51.0**. A spectrum summary is the classic edge-compute win for machine monitoring.

### Solution 27-08.6

$T_s$ = **4.096** ms and $DE = 0$. The payload takes $8 + \lceil(408 - 36 + 28 + 16)/36\rceil \times 5 = 8 + 12 \times 5$ = **68** symbols. Time on air: $(12.25 + 68) \times 4.096$ = **329** ms.

### Solution 27-08.7

(a) $T_s$ = **8.192** ms and $DE = 0$. The payload takes $8 + \lceil(160 - 40 + 28 + 16)/40\rceil \times 5 = 8 + 5 \times 5$ = **33** symbols. Time on air: $(12.25 + 33) \times 8.192$ = **371** ms.

(b) $\lfloor 36/0.3707 \rfloor$ = **97** packets an hour in a 1% sub-band, and $\lfloor 3.6/0.3707 \rfloor$ = **9** in a 0.1% sub-band.

### Solution 27-08.8

(a) $24 \times 139\ \text{mJ} + 0.864\ \text{J}$ = **4.19** J a day.

(b) $26\,957/4.19$ days = **17.6** years; with 0.923 J a day of self-discharge, **14.4** years.

(c) $24 \times 1.319$ s = **31.7** s a day, still just over 30 s. It needs at most **22** messages a day (Example 27-08.3) to stay within fair use.

### Solution 27-08.9

The energy is $17.3\ \mu\text{W} \times 16 \times 3600\ \text{s}$ = **0.999** J. Then $C = 2 \times 0.999/(16 - 4.84)$ = **0.179** F, a quarter of the weekend-sized store.

### Solution 27-08.10

At 500 lux, $(500/300) \times 10^{-4} \times 0.2 \times 0.8$ W = **26.7** µW per cm². Over 10 h that is **0.960** J per cm² a day. The node needs **40.7** J a day, so **42.4** cm² of cell: still the size of a palm.

### Solution 27-08.11

$2 \times 2^{20} \times 2/64 \times 10^6$ = **65.5** ms for the hash, **128** ms with the signature check, and **1.28** mJ at 10 mW.

### Solution 27-08.12

(a) $\lfloor 10/4.89 \rfloor$ = **2** replacements per node, so $10\,000 \times 2 \times 60$ = **1200000** dollars.

(b) $20 \times 1000$ = **20000** dollars for gateways, a saving of **1180000** dollars, and the SF7 nodes outlast the deployment (Example 27-08.4).

Network density is a battery-life investment. Whoever bears the maintenance visits, the device owner or the operator under a service contract, should pay for the gateways. Splitting the two decisions between parties is how fleets end up at SF12.

### Solution 27-08.13

- At 1 GHz: $128 \times 2 \times 10^9$ = **0.256** TOPS and $2048 \times 2 \times 10^9$ = **4.10** TOPS, matching "256 GOP/s up to 4 TOPs".
- At 200 MHz: **0.0512** and **0.819** TOPS.

A microcontroller's clock, not the NPU's datasheet clock, sets what a product can claim.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-08.2a | pointwise MACs | 294912 | MAC |
| 27-08.2b | weight bytes | 2048 | bytes |
| 27-08.2c | input tensor | 4608 | bytes |
| 27-08.2d | output tensor | 9216 | bytes |
| 27-08.2e | SRAM for both | 13824 | bytes |
| 27-08.3a | symbol time SF7 | 1.024 | ms |
| 27-08.3b | symbol time SF8 | 2.048 | ms |
| 27-08.3c | symbol time SF9 | 4.096 | ms |
| 27-08.3d | symbol time SF10 | 8.192 | ms |
| 27-08.3e | symbol time SF11 | 16.384 | ms |
| 27-08.3f | symbol time SF12 | 32.768 | ms |
| 27-08.3g | ratio SF12 to SF7 | 32 | — |
| 27-08.3h | SF7 symbol at 250 kHz | 0.512 | ms |
| 27-08.4a | average power, CPU | 4.73 | mW |
| 27-08.4b | life, CPU | 5.94 | days |
| 27-08.4c | average power, NPU | 0.720 | mW |
| 27-08.4d | life, NPU | 39.1 | days |
| 27-08.5a | raw rate | 153600 | b/s |
| 27-08.5b | raw radio power | 3.07 | mW |
| 27-08.5c | summary radio power | 10.2 | µW |
| 27-08.5d | summary total | 60.2 | µW |
| 27-08.5e | ratio | 51.0 | — |
| 27-08.6a | symbol time | 4.096 | ms |
| 27-08.6b | payload symbols | 68 | symbols |
| 27-08.6c | time on air | 329 | ms |
| 27-08.7a | symbol time | 8.192 | ms |
| 27-08.7b | payload symbols | 33 | symbols |
| 27-08.7c | time on air | 371 | ms |
| 27-08.7d | packets per hour at 1% | 97 | packets |
| 27-08.7e | packets per hour at 0.1% | 9 | packets |
| 27-08.8a | daily energy | 4.19 | J |
| 27-08.8b | life without self-discharge | 17.6 | years |
| 27-08.8c | life with self-discharge | 14.4 | years |
| 27-08.8d | daily airtime | 31.7 | s |
| 27-08.8e | messages a day within 30 s | 22 | messages |
| 27-08.9a | energy for 16 h | 0.999 | J |
| 27-08.9b | supercapacitor | 0.179 | F |
| 27-08.10a | harvest per cm² | 26.7 | µW |
| 27-08.10b | daily harvest per cm² | 0.960 | J |
| 27-08.10c | daily need | 40.7 | J |
| 27-08.10d | cell area | 42.4 | cm² |
| 27-08.11a | hash time | 65.5 | ms |
| 27-08.11b | boot-check time | 128 | ms |
| 27-08.11c | boot-check energy | 1.28 | mJ |
| 27-08.12a | replacements per node | 2 | — |
| 27-08.12b | replacement cost | 1200000 | $ |
| 27-08.12c | gateway cost | 20000 | $ |
| 27-08.12d | saving | 1180000 | $ |
| 27-08.13a | smallest at 1 GHz | 0.256 | TOPS |
| 27-08.13b | largest at 1 GHz | 4.10 | TOPS |
| 27-08.13c | largest at 200 MHz | 0.819 | TOPS |
| 27-08.13d | smallest at 200 MHz | 0.0512 | TOPS |
