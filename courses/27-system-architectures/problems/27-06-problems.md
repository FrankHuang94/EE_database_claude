# Problems 27-06 · Automotive E/E Architecture and ADAS Compute

Chapter: [27-06](../chapters/27-06-automotive-ee-architecture.md) · Worked solutions: [27-06 solutions](../solutions/27-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All parameters are assumed unless a source is cited. A classic CAN frame with $n$ data bytes has $34 + 8n + 13$ bits plus at most $\lfloor(34 + 8n - 1)/4\rfloor$ stuff bits; response times follow the iteration of §3.2; camera data rate is $Pfb$; peak TOPS is $N_cfG/u$; range loss is $P_c/(P_c + ev)$; stopping distance is $vt + v^2/(2a)$; residual failure rate is $\lambda(1 - DC)$.

---

## Problems

### Problem 27-06.1 [A]

**Which link?** Choose classic CAN, CAN FD, 10BASE-T1S, 1000BASE-T1 or a camera SerDes link for each, and say why in a phrase: (a) a window switch; (b) a cluster of eight ultrasonic parking sensors in a bumper; (c) a front camera; (d) the link from a zone controller to central compute; (e) a brake-system message that needs 32 data bytes every 10 ms.

### Problem 27-06.2 [A]

**Frame lengths.** Find the worst-case length (with stuffing) and the length without stuffing of classic CAN frames with 0, 2, 4 and 8 data bytes, and the worst-case time of each at 500 kb/s.

### Problem 27-06.3 [B]

**Room on the bus.** A 500 kb/s bus carries 8-byte messages every 10, 20, 50 and 100 ms and a 4-byte message every 20 ms. Find its load (worst-case frames), and how many more 8-byte messages at a 10 ms period it can take before the load exceeds 50%.

### Problem 27-06.4 [B]

**Response times.** Three 8-byte messages share a 500 kb/s bus with periods of 5, 10 and 20 ms, in that priority order. Find each worst-case response time.

### Problem 27-06.5 [A]

**One camera.** Find the data rate of a 3-megapixel camera at 60 frames/s with 12-bit raw pixels, and with 8 bits per pixel after on-camera processing.

### Problem 27-06.6 [B]

**More cameras.** A system with 11 cameras at 30 frames/s runs a network of 50 billion operations per frame. Find the sustained TOPS and the peak needed at 25% utilization.

### Problem 27-06.7 [B]

**A range budget.** In urban driving at 7.5 kW, what compute power costs at most 2% of range?

### Problem 27-06.8 [B]

**Milliseconds and metres.** At 100 km/h, how many milliseconds of latency add 1 m of travel, and what is the stopping distance with 150 ms of latency at 7 m/s²?

### Problem 27-06.9 [B]

**Splitting a safety budget.** An item's 5 FIT residual budget is split 3 FIT to the SoC (raw 400 FIT) and 2 FIT to the PMIC (raw 250 FIT). Find each part's required diagnostic coverage, and the item's residual rate if the SoC achieves 99.5% and the PMIC 99%.

### Problem 27-06.10 [B]

**An update.** A 3 GB update downloads at an effective 20 Mb/s. How long does it take, how much data does it move across a fleet of 2 million cars, and what does that cost at an assumed $0.50/GB?

### Problem 27-06.11 [C]

**Three zones instead of four.** Repeat Example 27-06.5's zonal design with three zones: one front zone at (0.5, 0.9) m serving both front clusters, and rear zones at (4.0, 0.3) and (4.0, 1.5) m. Find the endpoint wiring, backbone and total, and compare with four zones and with the domain design.

### Problem 27-06.12 [C]

**CAN FD.** Approximate a CAN FD frame with 64 data bytes as 30 bits at the 500 kb/s arbitration rate plus $8 \times 64 + 30$ bits at a 2 Mb/s data rate, ignoring stuffing. Find its time and compare with sending the same 64 bytes as eight worst-case classic 8-byte frames at 500 kb/s.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Architectures and zonal wiring | 11 |
| 2. CAN frames, load, response; choosing links | 1, 2, 3, 4, 12 |
| 3. Sensor bandwidth, compute and range | 5, 6, 7 |
| 4. Latency, stopping distance and safety budgets | 8, 9 |
| 5. Software-defined vehicles and updates | 10 |
