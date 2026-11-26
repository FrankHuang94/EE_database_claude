# Course 27 · Final Exam (System Architectures)

**Time limit:** 210 minutes, best taken in two sittings: Questions 1–7 (about 110 minutes), then Questions 8–12 (about 100 minutes).
**Allowed:** a scientific calculator and the [Course 27 equation sheet](../../../reference/equation-sheets/27-system-architectures.md) printed without its chapter links. No notes, no Python and no spreadsheet.

**Instructions.**

- Answer all 12 questions and show every step.
- Scoring:
  - Questions 1–10 are [B] and worth 8 points each, 2 per part.
  - Questions 11 and 12 are [C] and worth 12 points each, 3 per part.
  - The total is 104 points; 73 or more (70%) is a strong pass.
- Give numerical answers to 3 significant figures, with units, unless a part asks otherwise; exact values (dollar amounts, symbol times, energies that come out exact) may be given in full. Carry intermediate values at full calculator precision and round only final answers.
- One part needs a short iteration on the calculator (bisection is fine); say what you iterated on.
- Questions 11(d) and 12(a) ask for derivations: a result quoted from the equation sheet earns no credit unless derived. Question 12(d) is a short written answer; its rubric is at the end of the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These follow the chapters.

- The day is 24 h and the year 8760 h (3.1536 × 10⁷ s).
- LDO efficiency is $V_{out}/V_{in}$.
- LoRa uses 125 kHz, coding rate 4/5, an 8-symbol preamble, an explicit header and CRC, with $DE = 1$ only when the symbol time exceeds 16 ms.
- The 1% duty cycle allows 36 s of airtime per hour.
- "Assumed" values are illustrative.

---

**1 [B] · A power and thermal budget.** (27-01)
A handheld's battery sits at 3.8 V. It feeds a 1.2 W SoC through a 90%-efficient buck, a 0.6 W display through an 85%-efficient boost, and a 0.15 W radio at 1.8 V through an LDO.
(a) Find the battery power, the system efficiency and the conversion loss.
(b) Find the battery life on a 15 Wh battery of which 90% is usable.
(c) The case may reach 43 °C in 25 °C air, with 9 K/W from case to air. Find the sustained power.
(d) From equilibrium at 1.0 W, a 6.0 W burst starts; the thermal time constant is 300 s. How long until the case reaches its limit? What maximum burst duty cycle keeps the long-run average at the sustained power?

**2 [B] · Bottlenecks.** (27-01, 27-02)
(a) A phone's memory is 64 bits wide at 8533 MT/s. Find its bandwidth, and the decode speed bound for a 3-billion-parameter model stored at 4 bits.
(b) An NPU speeds up 40% of a workload tenfold. Find the overall speed-up.
(c) The memory's latency is 120 ns. How many bytes must be in flight to sustain the bandwidth of (a), and how many 64-byte cache-line requests is that?
(d) Under a power cap, with performance varying as $P_{dyn}^{1/3}$, an SoC with 3.0 W of dynamic power receives 0.3 W more dynamic power budget. Estimate the performance gain to first order.

**3 [B] · Energy per instruction and memory traffic.** (27-02)
A core switches $c$ = 1.0 nF per cycle at $V = V_0 + kf$ with $V_0$ = 0.5 V and $k$ = 0.25 V/GHz, runs at IPC = 2 and leaks 0.1 W (all assumed).
(a) Find the energy per instruction at 1 GHz and at 3 GHz.
(b) Find the frequency that minimizes energy per instruction. Iterate on $2ck(V_0 + kf)f^2 = P_s$.
(c) Find the minimum energy per instruction.
(d) The GPU, ISP and CPU demand 30, 10 and 15 GB/s with system-cache hit rates of 0.4, 0.2 and 0.6. Find the DRAM traffic, the bandwidth of a 64-bit LPDDR5X interface at 9600 MT/s, and its utilization.

**4 [B] · A smartwatch's day.** (27-03)
(a) The display is a Lambertian emitter of 9.0 cm² at 400 nits and an average pixel level of 0.2, with an efficacy of 5 lm/W. Find its emission power (ignore the driver IC).
(b) A BLE connection event draws 2 mA for 400 µs of ramp, 5 mA for 100 µs of receive plus the 150 µs gap, and 6 mA for 100 µs of transmit. Find its charge, and the average current at a 100 ms interval with a 3 µA sleep floor (ignore window widening).
(c) The battery is 300 mAh at 3.85 V, 90% usable through 90%-efficient conversion. Each day the display of (a) runs 2 h, and the SoC (20 mW), sensors (3 mW) and radio (5 mW) run 24 h. Find the battery energy, the daily rail energy and the life.
(d) A sensor samples at 50 Hz at 20 µJ per sample, and waking the application processor costs 2 mJ. Find the power with batches of 100 samples and with no batching.

**5 [B] · Earbuds.** (27-04)
(a) A feedforward ANC path has 30 µs of delay and perfect gain. Find the attenuation at 200 Hz and at 1 kHz.
(b) Above what frequency does it amplify noise?
(c) A headset's motion-to-photon latency is 12 ms. Find the registration error during a 200°/s head turn, and the latency that keeps the error at or below 1°.
(d) A 55 mAh, 3.85 V bud draws 18 mW through 85% conversion. Find its life, and the full recharges of the pair that a 500 mAh, 3.85 V case delivering 70% of its energy provides.

**6 [B] · A laptop SoC.** (27-05)
(a) The SoC spends 60% of the time at 0.5 W, 30% at 3 W and 10% at 15 W; the display adds 2.5 W. Find the average SoC power and the life on a 60 Wh battery.
(b) PL1 = 28 W, PL2 = 55 W and $\tau$ = 28 s. Starting from a 5 W average, how long does the chip turbo at PL2?
(c) The memory is 256 bits wide at 8000 MT/s. Find the bandwidth and the decode bound for a 14-billion-parameter model at 4 bits.
(d) For the model of (c), find the prefill time for a 4,000-token prompt on a 50 TOPS NPU at 35% utilization.

**7 [B] · A car.** (27-06)
(a) Find the worst-case length of a 6-byte classic CAN frame (11-bit identifier; count the 3-bit interframe space) and its duration at 500 kb/s.
(b) A braking ECU's raw failure rate is 800 FIT and its ASIL budget allows 8 FIT of undetected (residual) failures. Find the diagnostic coverage required, and the residual rate at 98% coverage.
(c) Find the stopping distance at 120 km/h with 250 ms of latency and 6.5 m/s² of braking, and the part due to latency.
(d) An electric car uses 150 Wh/km at 50 km/h. What share of its range does a 300 W computer cost?

**8 [B] · Training at scale.** (27-07)
(a) A 70-billion-parameter dense model is trained on 2 trillion tokens. Find the training compute, and the days on 1,024 accelerators of 1 PFLOP/s peak at 40% MFU.
(b) Eight GPUs in a server ring all-reduce 2 GB over links of 200 GB/s per direction. Find the time, ignoring latency.
(c) 1,024 GPUs sit in 128 such servers with 50 GB/s per direction of network per GPU. Find the cross-server time of a hierarchical all-reduce, and its total, ignoring latency.
(d) Find a flat ring over all 1,024 GPUs at network speed, and how many times slower it is than (c).

**9 [B] · Failures and serving.** (27-07)
(a) Each GPU-equivalent has an MTBF of 60,000 h. Find the mean time between interruptions of a 20,000-GPU job.
(b) Find Young's checkpoint interval for 30 s saves.
(c) With checkpoints at Young's interval and 5-minute restarts, find the lost fraction and the effective training time.
(d) A 70-billion-parameter model at 16 bits is served from a rack with 64 TB/s of HBM bandwidth, achieving 60% of it. Each sequence's KV cache is 0.5 GB and the batch is 64. Assuming decode is memory-bound, find the step time, throughput, per-user speed and energy per token at 60 kW.

**10 [B] · At the edge.** (27-08)
(a) A 3 × 3 convolution maps 16 input channels to 32 output channels on a 16 × 16 output. Find its MACs.
(b) Find its latency and energy on a CPU at 1 MAC/cycle, 100 MHz and 10 mW, and on an NPU at 64 MACs/cycle, 30% utilization, 100 MHz and 15 mW.
(c) Find the symbol time, payload symbols and time on air of a 12-byte LoRa packet at SF8, and the packets per hour a 1% duty cycle allows.
(d) Streaming 8 kHz, 12-bit audio costs 50 nJ/bit. Find its radio power, the power of running the NPU layer of (b) ten times a second with a 0.2 mW front end instead, and the ratio of the two.

**11 [C] · An energy-neutral greenhouse sensor.** (27-08, 27-01)
A 12 cm² cell sees 8,000 lux for 10 hours a day (assume 105 lm/W for daylight, 18% cell efficiency and 80% converter efficiency).
(a) Find the irradiance, the harvested power while lit and the daily harvest.
(b) The node's sensing chain draws 0.5 mW continuously and it sends 48 LoRa messages a day at 40 mJ each. Find its average power, its daily energy and the ratio of daily harvest to daily consumption.
(c) Find the energy for 72 hours without harvest, and the supercapacitor that stores it between 5.0 V and 2.5 V.
(d) Starting from $P = VI$ and $I = -C\,dV/dt$, derive the time a capacitor carries a constant-power load from $V_{max}$ to $V_{min}$. Then find it for a 10 F capacitor and this node.

**12 [C] · Rack decisions.** (27-07)
(a) Derive the ring all-reduce time for $p$ devices, an $S$-byte vector, bandwidth $B$ per direction and a start-up latency $\alpha$ per step.
(b) Apply it to 72 GPUs, 4 GB, 900 GB/s and $\alpha$ = 2 µs, giving the bandwidth and latency terms and the total.
(c) A rack costs $3.6 M over 4 years (assumed), draws 140 kW at a PUE of 1.25 and $0.07/kWh, and delivers 1.2 × 10⁵ tokens/s while busy; it is busy 50% of the time. Find the annual capital and energy costs, the tokens per year, the cost per million tokens and energy's share.
(d) A vendor says its new rack delivers "3x the tokens per second at the same power". Give three questions you would ask before using the claim in a business case, and say what answers would make it credible.
