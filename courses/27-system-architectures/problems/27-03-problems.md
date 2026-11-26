# Problems 27-03 · Wearables I: The Smartwatch

Chapter: [27-03](../chapters/27-03-wearables-smartwatch.md) · Worked solutions: [27-03 solutions](../solutions/27-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All device parameters are assumed unless a source is cited. Battery energy is capacity times nominal voltage; battery life is $L = 24\ \text{h} \times u\,\eta\,E_b/E_{day}$ with rail energy $E_{day}$. The display model is $P = \pi L_vA\,\text{APL}/\eta_v + P_0 + E_ff_r$, with the panel of Example 27-03.2 ($A = 1.4 \times 10^{-3}$ m², $\eta_v = 10$ lm/W, $P_0 = 2$ mW, $E_f = 0.3$ mJ). The BLE link of Example 27-03.4 has $Q_{ev} = 1.456$ µC per idle event, a 1.5 µA sleep current and 0.36 µA of window-widening current. The watch of Example 27-03.1 has a 1232 mWh cell, a daily rail energy of 715.2 mWh and 85% converter efficiency.

---

## Problems

### Problem 27-03.1 [A]

**Which domain?** For each function, say whether it belongs in the always-on domain (sensor hub) or needs the application processor, and why in a phrase: (a) counting steps; (b) detecting a raised wrist; (c) rendering a scrolling map; (d) updating the always-on clock face once a minute; (e) transcribing a dictated message; (f) buffering accelerometer data during sleep.

### Problem 27-03.2 [A]

**Battery energy and average power.** A watch has a 455 mAh cell at 3.87 V nominal. Find (a) its energy in Wh, (b) the average battery power that gives 40 h of life, and (c) the average battery power that gives 36 h once the cell has faded to 80% of its capacity.

### Problem 27-03.3 [A]

**A lighter day.** A 300 mAh, 3.85 V watch has no always-on display. Its day: a 4 mW floor for 24 h; 200 wrist raises of 5 s at 220 mW; 60 notifications of 5 s at 260 mW; 30 min of app use at 450 mW; a 30 min workout at 180 mW; heart-rate sampling at 1.5 mW for 24 h. All rails run at 85% efficiency. Find (a) the daily rail energy, (b) the daily battery energy, (c) the battery life in hours and days, and (d) the largest item and its share.

### Problem 27-03.4 [A]

**Air time.** Find the air time of (a) an encrypted packet with a 20-octet payload on the LE 1M PHY, (b) the same packet on the 2M PHY, (c) an encrypted 251-octet packet on the 1M PHY, and (d) the payload's share of the octets in (c).

### Problem 27-03.5 [B]

**Choosing the interval.** For the BLE link of the conventions: (a) find the connection interval that gives an average current of 10 µA; (b) find the average current with a 30 ms interval and a peripheral latency of 9, and the worst-case delay of a message from the phone and from the watch; (c) find the average current when the watch attends one event every 10 s (a 1 s interval with peripheral latency 9; BLE caps the connection interval itself at a few seconds) and explain why it is not a tenth of the 1 s value (3.32 µA).

### Problem 27-03.6 [B]

**A display budget.** For the panel of the conventions at 60 Hz: (a) find the highest luminance a screen at APL 0.40 can have within a 150 mW display budget; (b) a static screen at 600 cd/m² and APL 0.30 drops from 60 Hz to 10 Hz refresh. How much power does it save?

### Problem 27-03.7 [B]

**Why LTPO.** A pixel's storage capacitor is 0.2 pF and the eye tolerates a 10 mV droop. Find the hold time and the minimum refresh rate (a) with an LTPS switch leaking 0.1 pA and (b) with an oxide switch leaking 1 fA. (c) What capacitor would the LTPS pixel need to hold for 1 s?

### Problem 27-03.8 [B]

**When batching ties the hub.** An efficient AP spends $E_s = 2$ µJ per accelerometer sample and $E_w = 0.5$ mJ per wake; the sensor runs at 50 Hz. The hub of Example 27-03.3 draws 0.208 mW in total. (a) Find the smallest batch for which the AP's batched power is at or below the hub's, and the latency it implies. (b) For wrist-raise detection the batch is limited to 7 samples: find the AP's power and its ratio to the hub's.

### Problem 27-03.9 [B]

**A 0.8 V always-on rail.** The hub's 0.8 V rail is fed from a 4.0 V cell. The buck converts at 88% (excluding its quiescent current) and draws 1.5 µA quiescent; an LDO alternative draws 0.3 µA quiescent. Find (a) the load current below which the LDO draws less battery power, and (b) both converters' efficiencies at a 100 µA load.

### Problem 27-03.10 [B]

**Gating a frame buffer.** A 512 kB SRAM bank holding the always-on face's frame buffer leaks 20 µW in retention and 0.5 µW when switched off; restoring its contents costs 60 µJ. Find (a) the break-even idle time, (b) the energy saved per day by gating it during 2000 idle periods of 20 s (in J and mWh), and (c) the energy lost per period if the idle periods are only 2 s.

### Problem 27-03.11 [B]

**Paging cycles.** A cellular watch's modem sleeps at 20 µA from a 3.85 V cell and spends 480 µC on each paging wake. Find the average current, power and daily energy at a DRX cycle of 1.28 s and at an eDRX cycle of 20.48 s. What is the cost in reachability?

### Problem 27-03.12 [C]

**Is solar worth it?** A ring of photovoltaic cells of 3.0 cm² at 8% efficiency sees 500 W/m² for 3 h a day; 80% of the harvest reaches the battery. Find (a) the harvested power and daily energy, (b) the life of the watch of Example 27-03.1 with the harvest, and (c) the life of a sports watch with the same 1232 mWh cell that draws 48 mWh per day from the battery, with and without the harvest. (d) How many hours of such light a day would make the sports watch energy-neutral?

### Problem 27-03.13 [C]

**Two days.** The product team wants the watch of Example 27-03.1 to last 48 h new. (a) What daily rail energy does that require, and how much must be cut? (b) Find the life with each knob alone: always-on display off; floor from 6 to 4 mW; workout from 150 to 100 mW; app use from 500 to 400 mW. (c) If the always-on display must stay, apply the other three knobs together: find the life and the battery energy (and its increase) still needed. (d) Find the life with the always-on display off and the floor and workout knobs applied.

### Problem 27-03.14 [B]

**Fast charging heats the watch.** The 320 mAh cell of Example 27-03.1 charges from 0 to 80% in 45 min. Find (a) the average charging current and C-rate; (b) the heat in the cell's 0.30 Ω internal resistance; (c) the charging power into the cell at an average 3.9 V; and (d) the power the charger must deliver, and the total heat dissipated in the watch and the charging pad together, if the wireless link and charger are 70% efficient.

### Problem 27-03.15 [B]

**Two derivations.**

- (a) A rail at $V_{out}$ is fed from a cell at $V_{in}$ either by a buck of efficiency $\eta$ (excluding its quiescent current $I_{q,b}$) or by an LDO with quiescent current $I_{q,l}$. Write each one's battery power at load current $I$ and derive the crossover $I^* = V_{in}(I_{q,b} - I_{q,l})/(V_{in} - V_{out}/\eta)$ below which the LDO draws less.
- (b) Setting $P_{AP}(N) = P_{hub}$ (§3.4), derive the break-even batch $N^* = f_sE_w/(P_{hub} - f_sE_s)$, and say what happens when $f_sE_s \ge P_{hub}$.
- (c) For Example 27-03.3's hub and an AP that spends only 2 µJ per sample (same 50 Hz and 0.5 mJ per wake), find the hub's power, $N^*$, the smallest whole batch that beats the hub, and its latency.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Architecture and domain partitioning | 1, 8 |
| 2. Day budget, battery life and leverage | 2, 3, 13 |
| 3. Display power and LTPO | 6, 7 |
| 4. Radio energy and latency | 4, 5, 11 |
| 5. Microwatt choices, battery and charging | 9, 10, 12, 14, 15 |
