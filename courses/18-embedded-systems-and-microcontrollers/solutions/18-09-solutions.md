# Solutions 18-09 · Ultra-Low-Power Design

Problems: [18-09 problem set](../problems/18-09-problems.md) · Chapter: [18-09](../chapters/18-09-ultra-low-power-design.md). Every number below is recomputed by [verify_18_09.py](../verify/verify_18_09.py).

---

## Solutions

### Solution 18-09.1

(a) $1.000\ \text{A} \times 3600\ \text{s}$ = **3600** C.

(b) $3600\ \text{C} \times 3.7\ \text{V}$ = **13 320** J (3.7 Wh).

(c) $13\,320/0.015$ s = **246.7** h, about ten days.

### Solution 18-09.2

(a) $3\ \text{mA} \times 1.2\ \text{V}$ = **3.6** mW.

(b) Half the clock, half the current: **1.5** mA.

(c) $1.5 \times 0.9/1.2$ = **1.125** mA.

(d) $1.125\ \text{mA} \times 0.9\ \text{V}$ = **1.0125** mW, **0.281** of (a): halving the clock halves the power, and the voltage step cuts it by another $(0.9/1.2)^2 = 0.5625$.

### Solution 18-09.3

(a) Active charge per second: $25 \times 1\ \text{ms} \times 1.2\ \text{mA} = 30\ \mu\text{C}$, $10 \times 1.2\ \text{ms} \times 5\ \text{mA} = 60\ \mu\text{C}$, $15\ \text{ms} \times 3\ \text{mA} = 45\ \mu\text{C}$. Sleep fills the remaining 0.948 s at 4 µA, 3.792 µC. So $\bar I$ = **138.8** µA.

(b) $150\ \text{mAh}/138.8\ \mu\text{A} = 1081$ h = **45.0** days.

(c) Radio (60 µA), display (45 µA), heart rate (30 µA), sleep (3.8 µA). The radio's connection interval is the first lever, then the display's update rate.

### Solution 18-09.4

(a) $3\ \text{ms} \times 1.5\ \text{mA} = 4.5\ \mu\text{C}$; $t_{be} = 4.5\ \mu\text{C}/(5 - 0.4)\ \mu\text{A}$ = **0.978** s.

(b) Stop: $5\ \mu\text{A} \times 10\ \text{s}$ = **50** µC. Standby: $0.4\ \mu\text{A} \times 10\ \text{s} + 4.5\ \mu\text{C}$ = **8.5** µC, **5.9** times less.

(c) Stop: 2.5 µC. Standby: $0.2 + 4.5 = 4.7$ µC. **Stop** wins, as 0.5 s is below the break-even time.

### Solution 18-09.5

(a) Range 1: the task takes 25 ms at $50 \times 80 + 600 = 4600\ \mu\text{A}$, 115 µC, plus 0.975 µC asleep: **116.0** µC. Range 2: 76.9 ms at $35 \times 26 + 300 = 1210\ \mu\text{A}$, 93.08 µC, plus 0.923 µC: **94.0** µC.

(b) Range 2, by **19** %.

(c) Race to idle holds *at a fixed voltage*. Here the slower range also lowers the voltage, which cuts both the charge per cycle (35 against 50 µA/MHz) and the fixed current (300 against 600 µA). Within each range the rule still applies: run at that range's top clock.

### Solution 18-09.6

(a) **10** mA, whatever the battery voltage.

(b) $1.8 \times 10/(0.9 \times 4.2)$ = **4.76** mA at 4.2 V; **6.67** mA at 3.0 V.

(c) The buck conserves power, so its battery current is proportional to $1/V_{bat}$; as the cell's voltage falls, it must draw more current for the same power. The LDO's current stays at the load current, but it wastes the whole headroom, $V_{bat} - V_{out}$, as heat.

### Solution 18-09.7

(a) $1000\ \text{mAh}/3\ \mu\text{A} = 333\,333$ h = **38.1** years, longer than any cell's shelf life.

(b) 1% a year of 1000 mAh is 10 mAh a year, an equivalent **1.14** µA. Then $1000/(3 + 1.14)\ \mu\text{A}$ gives **27.6** years.

(c) $0.85 \times 27.6$ = **23.4** years.

(d) 3% a month is 30 mAh a month, an equivalent **41.7** µA, fourteen times the electronics' current. The life is **2.56** years, set almost entirely by the chemistry. Long-life products use primary lithium chemistries with very low self-discharge.

### Solution 18-09.8

(a) $3.3/10\ \text{kΩ}$ = **330** µA, more than a hundred times a good sleep current.

(b) $3.3/40\ \text{kΩ}$ = **82.5** µA.

(c) $3.3/2.2\ \text{kΩ}$ = **1.50** mA.

(d) On the press interrupt, switch the pin to input without pull-up (or to the opposite pull), and poll it slowly until release; or sample the button through a pull-up that is enabled only for a few microseconds at each check. Also add a timeout or bus-clear routine for a stuck I²C line (18-05).

### Solution 18-09.9

(a) $10\ \text{mA} \times 30\ \Omega$ = **0.30** V, exactly at the limit, so no capacitor is strictly needed at room temperature, but there is no margin at all.

(b) $1.5\,(1 - e^{-3\ \text{ms}/\tau}) = 0.3$ gives $e^{-3\ \text{ms}/\tau} = 0.8$, so $\tau = 3\ \text{ms}/\ln 1.25 = 13.4$ ms and $C = \tau/150\ \Omega$ = **89.6** µF. A 100 µF part with low leakage fits.

### Solution 18-09.10

(a) Per hour: fix $30 \times 25 = 750$ mC, report $5 \times 120 + 2 \times 200 = 1000$ mC, sleep for the remaining $3600 - 37$ s, $3\ \mu\text{A} \times 3563\ \text{s} = 10.69$ mC: **1760.7** mC. Average **0.489** mA. Life $0.8 \times 2400/0.489$ = 3926 h = **164** days.

(b) The LTE-M report (57%), then the fix (43%); sleep is under 1%.

(c) Per 4 h: fix 125 mC, report 1000 mC, sleep $3\ \mu\text{A} \times (14\,400 - 12)\ \text{s} = 43.16$ mC, total 1168.2 mC over 14 400 s, so **81.1** µA. Life **2.70** years.

(d) The LTE-M report's real duration and peak current in weak coverage (retries and higher transmit power can multiply it), the primary cell's capacity at those pulse currents and at temperature (and whether a buffer capacitor is needed), the fix time when assistance data is stale, and self-discharge over a multi-year life.

### Solution 18-09.11

(a) $5 \times 10$ = 50 µW harvested; $0.75 \times 50$ = **37.5** µW delivered while lit. Over 50 lit hours: $37.5\ \mu\text{W} \times 50 \times 3600\ \text{s}$ = **6.75** J a week.

(b) Energy neutrality (§3.8) means the week's consumption may not exceed the week's harvest: $6.75\ \text{J}/(168 \times 3600\ \text{s})$ = **11.2** µW of continuous load, or **3.72** µA at 3 V. The node cannot use the 37.5 µW of (a): that power is available only 50 of the week's 168 hours, and a load that took all of it while lit would leave nothing to charge the storage for the other 118 hours.

(c) $11.16\ \mu\text{W} \times 64 \times 3600\ \text{s}$ = **2.57** J must be stored by Friday evening. $\frac12 C(3.3^2 - 2.0^2) = 2.57$ J gives $C$ = **0.746** F: a supercapacitor of about 1 F, whose leakage must be well below the 3.7 µA load. Real storage loses energy on the way in and out, and offices have darker weeks (holidays), so a design would add margin to both the capacitor and the load budget.

### Solution 18-09.12

(a) The active phases take 24 µC a second and the node sleeps 0.995 s. With 4 µA: $24 + 4 \times 0.995$ = **27.98** µA, and $220\ \text{mAh}/27.98\ \mu\text{A}$ = 7863 h = **328** days. With 40 µA: $24 + 39.8$ = **63.8** µA and **144** days, less than half the 360 days of Example 18-09.1.

(b) The life claim must use the sleep current at the temperatures the product will actually see, at the maximum (or a stated percentile) rather than the typical, because leakage roughly doubles every 10 °C or so and varies widely from part to part. Ask the supplier for the distribution of sleep current over temperature and process, whether the figure includes the RTC and SRAM retention the product needs, and how many hours a year the product spends hot (in a car, on a sunny windowsill, next to a motor).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-09.1a | charge | 3600 | C |
| 18-09.1b | energy | 13320 | J |
| 18-09.1c | run time at 15 mW | 246.7 | h |
| 18-09.2a | dynamic power | 3.6 | mW |
| 18-09.2b | current at 24 MHz, 1.2 V | 1.5 | mA |
| 18-09.2c | current at 24 MHz, 0.9 V | 1.125 | mA |
| 18-09.2d | power at 24 MHz, 0.9 V | 1.0125 | mW |
| 18-09.2e | fraction of the original power | 0.281 | — |
| 18-09.3a | average current | 138.8 | µA |
| 18-09.3b | battery life | 45.0 | days |
| 18-09.4a | break-even idle time | 0.978 | s |
| 18-09.4b | charge per 10 s in stop | 50 | µC |
| 18-09.4c | charge per 10 s in standby | 8.5 | µC |
| 18-09.4d | ratio | 5.9 | — |
| 18-09.5a | charge per second, range 1 | 116.0 | µC |
| 18-09.5b | charge per second, range 2 | 94.0 | µC |
| 18-09.5c | saving of range 2 | 19 | % |
| 18-09.6a | LDO battery current | 10 | mA |
| 18-09.6b | buck battery current at 4.2 V | 4.76 | mA |
| 18-09.6c | buck battery current at 3.0 V | 6.67 | mA |
| 18-09.7a | life without self-discharge | 38.1 | years |
| 18-09.7b | self-discharge as a current, 1% per year | 1.14 | µA |
| 18-09.7c | life with 1% per year | 27.6 | years |
| 18-09.7d | life with 85% usable | 23.4 | years |
| 18-09.7e | self-discharge as a current, 3% per month | 41.7 | µA |
| 18-09.7f | life with 3% per month | 2.56 | years |
| 18-09.8a | 10 kΩ pull-up held | 330 | µA |
| 18-09.8b | 40 kΩ pull-up held | 82.5 | µA |
| 18-09.8c | I²C line held low | 1.50 | mA |
| 18-09.9a | droop at room temperature | 0.30 | V |
| 18-09.9b | capacitance for the cold case | 89.6 | µF |
| 18-09.10a | charge per hour | 1760.7 | mC |
| 18-09.10b | average current | 0.489 | mA |
| 18-09.10c | life | 164 | days |
| 18-09.10d | average current, proposal | 81.1 | µA |
| 18-09.10e | life, proposal | 2.70 | years |
| 18-09.11a | power delivered while lit | 37.5 | µW |
| 18-09.11b | usable energy per week | 6.75 | J |
| 18-09.11c | largest energy-neutral load | 11.2 | µW |
| 18-09.11d | that load's current at 3 V | 3.72 | µA |
| 18-09.11e | weekend energy | 2.57 | J |
| 18-09.11f | supercapacitor | 0.746 | F |
| 18-09.12a | average current, 4 µA sleep | 27.98 | µA |
| 18-09.12b | life, 4 µA sleep | 328 | days |
| 18-09.12c | average current, 40 µA sleep | 63.8 | µA |
| 18-09.12d | life, 40 µA sleep | 144 | days |
