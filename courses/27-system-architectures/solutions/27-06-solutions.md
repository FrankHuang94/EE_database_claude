# Solutions 27-06 · Automotive E/E Architecture and ADAS Compute

Problems: [27-06 problems](../problems/27-06-problems.md) · Chapter: [27-06](../chapters/27-06-automotive-ee-architecture.md). Every number is recomputed by [verify_27_06.py](../verify/verify_27_06.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-06.1

(a) **Classic CAN** (or LIN): a few bits, rarely, at the lowest cost. (b) **10BASE-T1S**: a multidrop bus suits many nearby nodes on one pair. (c) **Camera SerDes**: gigabits per second of raw video. (d) **1000BASE-T1** (or faster): a backbone carrying many zones' traffic. (e) **CAN FD**: up to 64 data bytes with the CAN priority model; classic CAN would need four frames.

### Solution 27-06.2

| Data bytes | Worst case (bits) | No stuffing (bits) | Time at 500 kb/s |
|---|---|---|---|
| 0 | **55** | **47** | **110** µs |
| 2 | **75** | **63** | **150** µs |
| 4 | **95** | **79** | **190** µs |
| 8 | **135** | **111** | **270** µs |

### Solution 27-06.3

Frame times: 8 bytes 270 µs, 4 bytes 190 µs. Load $= 0.27/10 + 0.27/20 + 0.19/20 + 0.27/50 + 0.27/100$ = **5.81**%. Each extra 10 ms message adds 2.7%: $(50 - 5.81)/2.7 = 16.4$, so **16** more fit, for a load of **49.0**%.

### Solution 27-06.4

$C = 0.27$ ms for each. Message 1: blocked by at most one lower-priority frame, $R_1 = 0.27 + 0.27$ = **0.54** ms. Message 2: blocking 0.27 plus one instance of message 1: **0.81** ms. Message 3: no lower-priority blocking, one instance each of messages 1 and 2: **0.81** ms.

### Solution 27-06.5

$3 \times 10^6 \times 60 \times 12$ = **2.16** Gb/s raw; at 8 bits per pixel **1.44** Gb/s.

### Solution 27-06.6

$11 \times 30 \times 50 \times 10^9$ = **16.5** TOPS sustained; at 25% utilization **66** TOPS peak.

### Solution 27-06.7

$P_c/(P_c + 7500) \le 0.02$ gives $P_c \le 0.02 \times 7500/0.98$ = **153** W.

### Solution 27-06.8

$v = 27.8$ m/s, so 1 m takes $1/27.8$ s = **36** ms. Stopping: $27.8 \times 0.15 + 27.8^2/(2 \times 7)$ = **59.3** m.

### Solution 27-06.9

SoC: $1 - 3/400$ = **99.25**%. PMIC: $1 - 2/250$ = **99.2**%. Achieved: $400 \times 0.005 + 250 \times 0.01 = 2.0 + 2.5$ = **4.5** FIT, within 5 FIT even though the PMIC's own 2.5 FIT exceeds its 2 FIT share: the SoC's margin covers it, a trade the safety case must document.

### Solution 27-06.10

$3 \times 8000/20$ = 1200 s = **20** min. Fleet data: $2 \times 10^6 \times 3$ GB = 6 million GB = **6** PB, about **$3.0** million at $0.50/GB.

### Solution 27-06.11

Endpoint wiring **24.6** m, backbone **6.45** m, total **31.05** m: more than four zones (25.0 m), because the front zone sits between the front clusters and their endpoint runs lengthen, but still far less than the domain design (112.8 m). Fewer zones save controllers at the cost of wire.

### Solution 27-06.12

CAN FD: $30/500\,000 + 542/2\,000\,000$ s = $60 + 271$ = **331** µs. Classic: $8 \times 270$ = **2160** µs. CAN FD is **6.5** times faster for the same 64 bytes.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-06.2a | 0 bytes, worst case | 55 | bits |
| 27-06.2a1 | 0 bytes, no stuffing | 47 | bits |
| 27-06.2a2 | 0 bytes, time | 110 | µs |
| 27-06.2b | 2 bytes, worst case | 75 | bits |
| 27-06.2b1 | 2 bytes, no stuffing | 63 | bits |
| 27-06.2b2 | 2 bytes, time | 150 | µs |
| 27-06.2c | 4 bytes, worst case | 95 | bits |
| 27-06.2c1 | 4 bytes, no stuffing | 79 | bits |
| 27-06.2c2 | 4 bytes, time | 190 | µs |
| 27-06.2d | 8 bytes, worst case | 135 | bits |
| 27-06.2d1 | 8 bytes, no stuffing | 111 | bits |
| 27-06.2d2 | 8 bytes, time | 270 | µs |
| 27-06.3a | bus load | 5.81 | % |
| 27-06.3a1 | load per extra message | 2.7 | % |
| 27-06.3a2 | ratio | 16.4 | — |
| 27-06.3b | extra messages | 16 | — |
| 27-06.3c | resulting load | 49.0 | % |
| 27-06.4a | message 1 response | 0.54 | ms |
| 27-06.4b | message 2 response | 0.81 | ms |
| 27-06.4c | message 3 response | 0.81 | ms |
| 27-06.5a | raw rate | 2.16 | Gb/s |
| 27-06.5b | 8-bit rate | 1.44 | Gb/s |
| 27-06.6a | sustained | 16.5 | TOPS |
| 27-06.6b | peak at 25% | 66 | TOPS |
| 27-06.7 | compute power for 2% | 153 | W |
| 27-06.8v | speed | 27.8 | m/s |
| 27-06.8a | latency per metre | 36 | ms |
| 27-06.8b | stopping distance | 59.3 | m |
| 27-06.9a | SoC coverage | 99.25 | % |
| 27-06.9b | PMIC coverage | 99.2 | % |
| 27-06.9c | SoC residual | 2.0 | FIT |
| 27-06.9d | PMIC residual | 2.5 | FIT |
| 27-06.9e | item residual | 4.5 | FIT |
| 27-06.10a | download seconds | 1200 | s |
| 27-06.10b | download minutes | 20 | min |
| 27-06.10c | fleet data | 6 | PB |
| 27-06.10d | fleet cost | 3.0 | million $ |
| 27-06.11a | endpoint wiring | 24.6 | m |
| 27-06.11b | backbone | 6.45 | m |
| 27-06.11c | total | 31.05 | m |
| 27-06.12a | CAN FD time | 331 | µs |
| 27-06.12a1 | arbitration-phase time | 60 | µs |
| 27-06.12a2 | data-phase time | 271 | µs |
| 27-06.12b | classic time | 2160 | µs |
| 27-06.12c | speedup | 6.5 | — |
