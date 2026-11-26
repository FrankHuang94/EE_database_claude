# Solutions 27-03 · Wearables I: The Smartwatch

Problems: [27-03 problems](../problems/27-03-problems.md) · Chapter: [27-03](../chapters/27-03-wearables-smartwatch.md). Every number is recomputed by [verify_27_03.py](../verify/verify_27_03.py). Intermediate values are shown rounded but carried at full precision.

---

## Solutions

### Solution 27-03.1

(a) **Hub**: steady, simple arithmetic on every sample, no latency need beyond the daily total. (b) **Hub**: it must watch every sample with a latency of about 150 ms, which would wake the AP many times a second. (c) **AP**: graphics and large data, and the user is looking at the screen anyway. (d) **Hub** (with the display driver): a tiny, scheduled update that should not wake the AP. (e) **AP** (or the phone): a speech model needs far more compute and memory than a hub; a small keyword detector on the hub can decide when to wake it. (f) **Hub**: buffering is exactly the night watchman's job, and the AP can read the batch later.

### Solution 27-03.2

(a) $E_b = 455 \times 3.87$ = **1760.85** mWh = **1.76** Wh.

(b) $\bar P_b = 1760.85/40$ = **44.0** mW.

(c) $0.8 \times 1760.85/36$ = **39.1** mW.

Units: mAh × V = mWh; mWh/h = mW. ✓

### Solution 27-03.3

(a) Items (mWh): floor $4 \times 24 = 96$; wrist raises $220 \times 200 \times 5/3600 = 61.1$; notifications $260 \times 60 \times 5/3600 = 21.7$; app $450 \times 0.5 = 225$; workout $180 \times 0.5 = 90$; heart rate $1.5 \times 24 = 36$. Total $E_{day}$ = **529.8** mWh.

(b) $529.8/0.85$ = **623.3** mWh.

(c) $E_b = 300 \times 3.85 = 1155$ mWh; $L = 24 \times 1155/623.3$ = **44.5** h = **1.85** days.

(d) App use: $225/529.8$ = **42.5**% of the day. Thirty minutes of app use cost more than the 24-hour floor and heart-rate sampling together (132 mWh).

### Solution 27-03.4

Octets = preamble + 4 + 2 + payload + MIC + 3.

(a) $1 + 4 + 2 + 20 + 4 + 3 = 34$ octets: $34 \times 8/1$ Mb/s = **272** µs.

(b) The 2M preamble is 2 octets: 35 octets, $35 \times 8/2$ = **140** µs.

(c) $1 + 4 + 2 + 251 + 4 + 3 = 265$ octets: **2120** µs.

(d) $251/265$ = **94.7**%. Long packets amortize the 14 octets of overhead; short ones (a 20-octet payload is **59**% of its 34-octet packet) do not.

### Solution 27-03.5

(a) $I_{avg} = 1.86 + 1.456/T$ µA (T in s). Setting it to 10 µA: $1.456/T = 8.14$, so $T$ = 0.1789 s = **179** ms.

(b) With latency 9 the watch listens every $10 \times 30$ ms = 0.3 s: $I_{avg} = 1.86 + 1.456/0.3$ = **6.71** µA. A message from the phone can wait up to **300** ms for an event the watch attends. A message from the watch goes at the next 30 ms event, since peripheral latency lets the watch wake for any event when it has data: up to **30** ms.

(c) $1.86 + 1.456/10$ = **2.01** µA, not 0.33 µA. The sleep current (1.5 µA) and the window-widening current (0.36 µA, proportional to the interval and so constant per second) do not fall with the interval; only the event term does.

### Solution 27-03.6

(a) The driver at 60 Hz draws $2 + 0.3 \times 60 = 20$ mW, leaving 130 mW for emission: $L_v = 0.130 \times 10/(\pi \times 1.4 \times 10^{-3} \times 0.40)$ = **739** cd/m².

(b) Only the refresh term changes: $0.3\ \text{mJ} \times (60 - 10)$ Hz = **15.0** mW, **15**% of the 99.2 mW the screen draws at 60 Hz (Example 27-03.2c).

### Solution 27-03.7

$t_{hold} = C_{st}\Delta V/I_{off}$.

(a) $0.2 \times 10^{-12} \times 0.01/(0.1 \times 10^{-12})$ = **0.020** s = 20 ms: the panel must refresh at least **50** Hz.

(b) $0.2 \times 10^{-12} \times 0.01/10^{-15}$ = **2.0** s: refresh down to **0.5** Hz, so 1 Hz is safe.

(c) $C = I_{off}t/\Delta V = 0.1 \times 10^{-12} \times 1/0.01 = 10^{-11}$ F = **10** pF, **50** times the original. There is no room for such a capacitor in a pixel a few tens of micrometres across, which is why the switch, not the capacitor, changed.

### Solution 27-03.8

(a) $P_{AP}(N) = f_sE_s + f_sE_w/N = 0.10 + 25/N$ mW. Setting it at or below 0.208 mW: $25/N \le 0.1083$, so $N \ge 230.8$: **231** samples, a latency of $231/50$ = **4.62** s. Fine for step counting, useless for a wrist raise.

(b) $P_{AP}(7) = 0.10 + 25/7$ = **3.67** mW, **17.6** times the hub. With a tight deadline the wake overhead dominates, however cheap the AP's per-sample work.

### Solution 27-03.9

(a) $I^* = V_{in}(I_{q,b} - I_{q,l})/(V_{in} - V_{out}/\eta) = 4.0 \times 1.2/(4.0 - 0.8/0.88)$ = **1.55** µA.

(b) At 100 µA the output is 80 µW. Buck input: $80/0.88 + 1.5 \times 4.0 = 90.9 + 6.0 = 96.9$ µW, efficiency **82.6**%. LDO input: $4.0 \times 100.3 = 401.2$ µW, efficiency **19.9**%. An LDO from the battery to a 0.8 V rail can never beat $0.8/4.0$ = 20%; below about 1.55 µA, where the buck's quiescent current dominates, it wins anyway.

### Solution 27-03.10

(a) $t_{BE} = 60/(20 - 0.5)$ = **3.08** s.

(b) Per 20 s period: $19.5 \times 20 - 60 = 330$ µJ saved; per day $2000 \times 330$ µJ = **0.660** J = **0.183** mWh, about 0.03% of the 715.2 mWh day of Example 27-03.1.

(c) $19.5 \times 2 - 60$ = **−21** µJ: a loss of 21 µJ per period. Gate only when the predicted idle time exceeds $t_{BE}$.

### Solution 27-03.11

$I_{avg} = I_{sl} + Q_p/T_c$.

- DRX 1.28 s: $20 + 480/1.28$ = **395** µA, $\times 3.85$ V = **1.52** mW, $\times 24$ h = **36.5** mWh per day.
- eDRX 20.48 s: $20 + 480/20.48$ = **43.4** µA, **0.167** mW, **4.01** mWh per day.

At 1.28 s, paging alone would add about 4% to the 841 mWh daily battery energy of Example 27-03.1; at 20.48 s, about 0.5%. The cost is reachability: an incoming call or message can wait up to 20.48 s instead of 1.28 s before the network can reach the watch.

### Solution 27-03.12

(a) $P = 500 \times 3.0 \times 10^{-4} \times 0.08$ W = **12.0** mW; for 3 h, **36.0** mWh per day, of which $0.8 \times 36.0$ = **28.8** mWh reaches the battery.

(b) The battery's daily drain falls from 841.4 to 812.6 mWh: $L = 24 \times 1232/812.6$ = **36.4** h, against 35.1 h, a gain of **3.5**%.

(c) Without the harvest: $1232/48$ = **25.7** days. With it: $1232/(48 - 28.8)$ = **64.2** days.

(d) Energy neutrality needs $48/(12.0 \times 0.8)$ = **5.0** h of such light a day.

The same harvest is **3**% of a smartwatch's daily drain but **60**% of the sports watch's: solar is worth its cost only when the floor and display are already tiny.

### Solution 27-03.13

(a) $48 = 24 \times 0.85 \times 1232/E_{day}$ gives $E_{day}$ = **523.6** mWh, a cut of $715.2 - 523.6$ = **191.6** mWh (27%).

(b) Lives: always-on display off ($-113.9$ mWh) **41.8** h; floor 6 → 4 mW ($-48$) **37.7** h; workout 150 → 100 mW ($-50$) **37.8** h; app 500 → 400 mW ($-25$) **36.4** h. None reaches 48 h alone.

(c) Three knobs: $E_{day} = 715.2 - 48 - 50 - 25 = 592.2$ mWh, $L$ = **42.4** h. For 48 h the cell must hold $2 \times 592.2/0.85$ = **1393** mWh, **13.1**% more than 1232 mWh (about **13**% more volume at the same density).

(d) $715.2 - 113.9 - 48 - 50 = 503.3$ mWh: $L$ = **49.9** h, meeting the target without a bigger cell. The decision is a product one: a two-day watch without an always-on display, or a 13% thicker cell.

### Solution 27-03.14

(a) $I = 0.8 \times 320\ \text{mAh}/0.75\ \text{h}$ = **341** mA, a rate of $341/320$ = **1.07** C.

(b) $I^2R = 0.3413^2 \times 0.30$ = **35.0** mW.

(c) $0.3413 \times 3.9$ = **1.33** W.

(d) $1.33/0.70$ = **1.90** W from the charger, of which $1.90 - 1.33$ = **0.571** W becomes heat in the coils and charger (plus the cell's 35 mW). That is nearly three times the 0.20 W sustained limit estimated in §3.9 of the chapter, so fast charging must taper or the watch must sit on a charger that spreads the heat.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 27-03.2a | battery energy | 1760.85 | mWh |
| 27-03.2a1 | battery energy | 1.76 | Wh |
| 27-03.2b | average power for 40 h | 44.0 | mW |
| 27-03.2c | average power for 36 h at 80% | 39.1 | mW |
| 27-03.3a | daily rail energy | 529.8 | mWh |
| 27-03.3b | daily battery energy | 623.3 | mWh |
| 27-03.3c | battery life | 44.5 | h |
| 27-03.3c1 | battery life | 1.85 | days |
| 27-03.3d | app share | 42.5 | % |
| 27-03.4a | 20-octet encrypted packet, 1M | 272 | µs |
| 27-03.4b | 20-octet encrypted packet, 2M | 140 | µs |
| 27-03.4c | 251-octet encrypted packet, 1M | 2120 | µs |
| 27-03.4d | payload share | 94.7 | % |
| 27-03.5a | interval for 10 µA | 179 | ms |
| 27-03.5b | current at 30 ms, latency 9 | 6.71 | µA |
| 27-03.5b1 | worst delay from phone | 300 | ms |
| 27-03.5b2 | worst delay from watch | 30 | ms |
| 27-03.5c | current at 10 s | 2.01 | µA |
| 27-03.6a | luminance within 150 mW | 739 | cd/m² |
| 27-03.6b | refresh saving 60 to 10 Hz | 15.0 | mW |
| 27-03.7a | LTPS hold time | 0.020 | s |
| 27-03.7a1 | LTPS minimum refresh | 50 | Hz |
| 27-03.7b | oxide hold time | 2.0 | s |
| 27-03.7b1 | oxide minimum refresh | 0.5 | Hz |
| 27-03.7c | capacitor for 1 s with LTPS | 10 | pF |
| 27-03.7c1 | capacitor ratio | 50 | — |
| 27-03.8a | break-even batch | 231 | samples |
| 27-03.8a1 | break-even latency | 4.62 | s |
| 27-03.8b | AP power at N = 7 | 3.67 | mW |
| 27-03.8b1 | ratio to hub | 17.6 | — |
| 27-03.9a | buck/LDO crossover | 1.55 | µA |
| 27-03.9b | buck efficiency at 100 µA | 82.6 | % |
| 27-03.9b1 | LDO efficiency at 100 µA | 19.9 | % |
| 27-03.10a | break-even idle time | 3.08 | s |
| 27-03.10b | daily saving | 0.660 | J |
| 27-03.10b1 | daily saving | 0.183 | mWh |
| 27-03.10c | energy per 2 s period | -21 | µJ |
| 27-03.11a | average current, DRX 1.28 s | 395 | µA |
| 27-03.11a1 | power, DRX 1.28 s | 1.52 | mW |
| 27-03.11a2 | daily energy, DRX 1.28 s | 36.5 | mWh |
| 27-03.11b | average current, eDRX 20.48 s | 43.4 | µA |
| 27-03.11b1 | power, eDRX 20.48 s | 0.167 | mW |
| 27-03.11b2 | daily energy, eDRX 20.48 s | 4.01 | mWh |
| 27-03.12a | harvested power | 12.0 | mW |
| 27-03.12a1 | harvested energy per day | 36.0 | mWh |
| 27-03.12a2 | energy reaching battery | 28.8 | mWh |
| 27-03.12b | smartwatch life with harvest | 36.4 | h |
| 27-03.12c | sports watch life without harvest | 25.7 | days |
| 27-03.12c1 | sports watch life with harvest | 64.2 | days |
| 27-03.12d | hours for energy neutrality | 5.0 | h |
| 27-03.13a | required daily rail energy | 523.6 | mWh |
| 27-03.13a1 | cut needed | 191.6 | mWh |
| 27-03.13b | life, always-on display off | 41.8 | h |
| 27-03.13b1 | life, floor 4 mW | 37.7 | h |
| 27-03.13b2 | life, workout 100 mW | 37.8 | h |
| 27-03.13b3 | life, app 400 mW | 36.4 | h |
| 27-03.13c | life, three knobs | 42.4 | h |
| 27-03.13c1 | battery energy for 48 h | 1393 | mWh |
| 27-03.13c2 | battery increase | 13.1 | % |
| 27-03.13d | life, display off plus two knobs | 49.9 | h |
| 27-03.14a | charging current | 341 | mA |
| 27-03.14a1 | C-rate | 1.07 | C |
| 27-03.14b | heat in internal resistance | 35.0 | mW |
| 27-03.14c | power into the cell | 1.33 | W |
| 27-03.14d | charger power | 1.90 | W |
| 27-03.14d1 | heat in coils and charger | 0.571 | W |
| 27-03.3a1 | wrist-raise energy | 61.1 | mWh |
| 27-03.3a2 | notification energy | 21.7 | mWh |
| 27-03.3c2 | battery energy, 300 mAh cell | 1155 | mWh |
| 27-03.3d1 | floor plus heart rate | 132 | mWh |
| 27-03.4a1 | octets, 20-octet payload on 1M | 34 | octets |
| 27-03.4b2 | octets, 20-octet payload on 2M | 35 | octets |
| 27-03.4c1 | octets, 251-octet payload | 265 | octets |
| 27-03.4d1 | payload share, 20-octet packet | 59 | % |
| 27-03.5a1 | interval-independent current | 1.86 | µA |
| 27-03.5a2 | event term at 10 µA | 8.14 | µA |
| 27-03.5a3 | interval for 10 µA | 0.1789 | s |
| 27-03.6a1 | driver power at 60 Hz | 20 | mW |
| 27-03.6a2 | emission budget | 130 | mW |
| 27-03.6b1 | saving as share of screen power | 15 | % |
| 27-03.8a2 | per-sample floor | 0.10 | mW |
| 27-03.8a3 | wake term allowed | 0.1083 | mW |
| 27-03.8a4 | batch bound | 230.8 | samples |
| 27-03.9b2 | output power at 100 µA | 80 | µW |
| 27-03.9b3 | buck conversion input | 90.9 | µW |
| 27-03.9b4 | buck quiescent input | 6.0 | µW |
| 27-03.9b5 | buck input power | 96.9 | µW |
| 27-03.9b6 | LDO input power | 401.2 | µW |
| 27-03.9b7 | LDO efficiency bound | 20 | % |
| 27-03.10a1 | leakage saved while gated | 19.5 | µW |
| 27-03.10b2 | saving per 20 s period | 330 | µJ |
| 27-03.10b3 | saving as share of the day | 0.03 | % |
| 27-03.11c | DRX paging share of daily battery energy | 4 | % |
| 27-03.11c1 | eDRX paging share of daily battery energy | 0.5 | % |
| 27-03.12b1 | daily drain with harvest | 812.6 | mWh |
| 27-03.12b2 | life gain | 3.5 | % |
| 27-03.12d1 | harvest share, smartwatch | 3 | % |
| 27-03.12d2 | harvest share, sports watch | 60 | % |
| 27-03.13a2 | cut as share of the day | 27 | % |
| 27-03.13c3 | three-knob daily rail energy | 592.2 | mWh |
| 27-03.13c4 | volume increase | 13 | % |
| 27-03.13d1 | daily rail energy, display off plus two knobs | 503.3 | mWh |
| 27-03.14b1 | charging current | 0.3413 | A |
